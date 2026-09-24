#!/usr/bin/env python3
"""openfda — FDA's public device databases, for MOS skills.

The regulatory research skills (product-code, precedent-search, reference-devices)
make every call to FDA through this script, so the searches behave the same
whichever AI runs them. It needs Python 3.8 or later and nothing else.

What leaves the machine: the search terms given on the command line, sent to
api.fda.gov; the document numbers given to `fetch`, and product codes and standard numbers
given to `standards`, sent to www.accessdata.fda.gov; guidance pages asked for by
`guidance`, from www.fda.gov; and regulation numbers given to `regulation`, sent to
www.ecfr.gov. Nothing else. No file is read and no company text is
sent. Every command prints the exact query it ran, so a skill can show the user
what went and log it in the deliverable.

Commands:

  check
      Confirm FDA's API can be reached, and report the date openFDA was last
      updated. Sends one query.

  classify TERM [TERM ...] [--any] [--limit N]
      Search product codes by device name and FDA's definition. Each TERM is a
      word or a quoted phrase. By default a code must match every term; --any
      matches codes with at least one. Prints code, class, submission type,
      regulation and name, with the start of each definition.

  devices TERM [TERM ...] [--any] [--limit N]
      Search cleared and approved devices by name, across every product code:
      510(k) clearances and De Novo grants by device name, PMA approvals by trade
      and generic name. Reports which product codes the matches sit under, so a
      device named like this one can be traced to its code, and lists the newest.

  code CODE
      Everything about one product code: the full classification record,
      decoded; how many 510(k) clearances, De Novo grants and PMA approvals sit
      under it; its recalls and adverse event reports, counted; and its most
      recent clearances.

  family REGULATION
      Every product code under one classification regulation, such as 886.4150,
      with how many clearances and De Novo grants each holds. A 510(k) predicate
      almost always shares the new device's regulation, so these are the codes
      to search first.

  clearances (--code CODE | --regulation REG) [--since YEAR] [--denovo] [--limit N]
      510(k) clearances and De Novo grants under a product code, or under every
      code in a regulation, newest first. De Novo grants are the DEN numbers.
      --denovo lists only those.

  pma --code CODE [--supplements] [--limit N]
      PMA approvals under a product code, originals only unless --supplements.

  recalls (--code CODE | --number K123456) [--limit N]
      Recalls for a product code, or for one cleared device.

  events (--code CODE | --brand NAME [--manufacturer NAME])
      Adverse event reports (MAUDE), counted by type, for a product code or for
      one device by brand name. Brand matching is loose: reports name devices
      inconsistently, so a count by brand is a signal, not a total.

  udi --code CODE [--limit N]
      Brand names and companies listing devices under a product code in GUDID.

  regulation SECTION [--limits]
      The current text of a classification regulation, such as 886.4150, from
      the eCFR: FDA's identification of the device type, its class, any special
      controls and any exemption. --limits adds the part's ".9" section, which
      sets the limits on 510(k) exemptions. Sends only the section number, to
      www.ecfr.gov, run by the Office of the Federal Register.

  standards (--code CODE | --number NUMBER) [--details]
      FDA-recognized consensus standards. With --code, the device-specific
      standards and guidance documents FDA lists for a product code. With
      --number, a standard's current FDA recognition, such as 10993-1 or
      60601-1. --details reads each standard's recognition page for the extent
      of recognition and any transition between editions (ten at most, one
      second apart). Titles and numbers only; never a standard's text.

  guidance URL --out DIR
      Save an FDA guidance document from its page on www.fda.gov — the links
      `standards --code` prints, including special controls guidance documents.
      Downloads the PDF where FDA offers one; many older guidance documents are
      published as the page itself, and then the page's text is saved instead.

  fetch NUMBER [NUMBER ...] --out DIR
      Download the public summary for each K, DEN or P number: the 510(k)
      summary, the De Novo decision summary, or the PMA summary of safety and
      effectiveness data. Ten at most per call, one second apart. Where no
      summary is online, prints the FDA database page to check by hand.

Add --json to any search command to print FDA's records as returned.

An openFDA API key is optional. Without one FDA allows 1,000 queries a day from
one address; with one, 120,000. Set OPENFDA_API_KEY in the environment or in a
.env file in the working directory. The key is never printed.

openFDA's own terms apply to everything this script returns: the data is
public, updated about weekly, and FDA says to treat it as unvalidated. A skill
checks what matters against the source documents.
"""

import argparse
import json
import os
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

VERSION = '0.1.0'  # a shared contract: a change in behaviour is a new MOS release

API = 'https://api.fda.gov/device/'
DOCS = 'https://www.accessdata.fda.gov/'
# FDA's abuse detection refuses agents that do not start with Mozilla, and any
# agent carrying a URL. This one passes and still names itself.
AGENT = 'Mozilla/5.0 (compatible; MOS-openfda/%s)' % VERSION
PAGE = 1000          # openFDA's most records per call
MAX_SKIP = 25000     # openFDA's paging ceiling
MAX_FETCH = 10

# openFDA documents 1-4. 6 and 7 are read from FDA's own classification pages.
SUBMISSION = {'1': '510(k)', '2': 'PMA', '3': 'Contact FDA', '4': '510(k) exempt',
              '6': 'HDE (humanitarian device exemption)', '7': 'Enforcement discretion'}
CLASS = {'1': 'I', '2': 'II', '3': 'III', 'U': 'Unclassified', 'N': 'Not classified',
         'F': 'HDE'}
UNCLASSIFIED = {'1': 'Pre-amendment', '2': 'IDE', '3': 'For export only', '4': 'Unknown',
                '5': 'Guidance under development', '6': 'Enforcement discretion'}
YESNO = {'Y': 'yes', 'N': 'no'}


def submission(v):
    if not v:
        return 'not stated'
    return SUBMISSION.get(v, 'type %s, not documented by openFDA; see the FDA page' % v)


def device_class(v):
    return CLASS.get((v or '').upper(), v or 'not stated')

_meta = {}  # dataset -> the date openFDA last updated it, as each response reports


class Refused(Exception):
    """A request FDA refused or could not answer. The message says why."""


# ------------------------------------------------------------------ plumbing

def api_key():
    key = os.environ.get('OPENFDA_API_KEY', '').strip()
    if key:
        return key
    try:
        with open('.env', encoding='utf-8') as f:
            for line in f:
                m = re.match(r'\s*OPENFDA_API_KEY\s*=\s*["\']?([^"\'\s#]+)', line)
                if m:
                    return m.group(1)
    except OSError:
        pass
    return ''


def get(url, binary=False):
    req = urllib.request.Request(url, headers={'User-Agent': AGENT})
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            return r.geturl(), r.headers.get('Content-Type', ''), r.read()
    except urllib.error.HTTPError as e:
        if binary:
            return url, 'error %d' % e.code, b''
        body = e.read()
        try:
            err = json.loads(body.decode('utf-8'))['error']
        except (ValueError, KeyError):
            err = {}
        if e.code == 404 and err.get('code') == 'NOT_FOUND':
            return url, 'application/json', b'{"results": []}'
        if e.code == 429:
            raise Refused('FDA\'s rate limit reached. Without an API key it allows 1,000 queries '
                          'a day; a free key from open.fda.gov raises that to 120,000. Set '
                          'OPENFDA_API_KEY.')
        raise Refused('FDA refused the query (%d): %s' % (e.code, err.get('message', e.reason)))
    except urllib.error.URLError as e:
        raise Refused('Cannot reach %s (%s). Check the connection. If this machine cannot '
                      'reach FDA, run the searches by hand from the queries printed above.'
                      % (urllib.parse.urlsplit(url).netloc, e.reason))


def term(t):
    """One search term, made safe: letters, digits, hyphens and spaces only."""
    t = re.sub(r'[^A-Za-z0-9\- ]', ' ', t).strip()
    t = re.sub(r'\s+', ' ', t)
    if not t:
        raise Refused('A search term is empty once punctuation is removed.')
    return '"%s"' % t.replace(' ', '+') if ' ' in t else t


def query(endpoint, search=None, count=None, sort=None, limit=None, skip=None):
    """Run one openFDA query. Prints it, returns the parsed response."""
    parts = []
    if search:
        parts.append('search=' + urllib.parse.quote(search, safe=':()[]"*+-'))
    if count:
        parts.append('count=' + count)
    if sort:
        parts.append('sort=' + sort)
    if limit:
        parts.append('limit=%d' % limit)
    if skip:
        parts.append('skip=%d' % skip)
    shown = API + endpoint + '.json?' + '&'.join(parts)
    print('Query: ' + shown)
    key = api_key()
    url = shown + ('&api_key=' + urllib.parse.quote(key) if key else '')
    _, _, body = get(url)
    data = json.loads(body.decode('utf-8'))
    updated = data.get('meta', {}).get('last_updated')
    if updated:
        _meta[endpoint] = updated
    return data


def records(endpoint, search, sort=None, limit=100):
    """Up to `limit` records, paging as openFDA requires. Returns (records, total)."""
    out, total, skip = [], 0, 0
    while len(out) < limit:
        if skip > MAX_SKIP:
            print('Stopped at openFDA\'s paging ceiling of %d records. Narrow the search.'
                  % MAX_SKIP)
            break
        n = min(PAGE, limit - len(out))
        data = query(endpoint, search, sort=sort, limit=n, skip=skip or None)
        batch = data.get('results', [])
        total = data.get('meta', {}).get('results', {}).get('total', len(batch))
        out.extend(batch)
        if len(batch) < n:
            break
        skip += n
    return out, total


def total(endpoint, search):
    data = query(endpoint, search, limit=1)
    return data.get('meta', {}).get('results', {}).get('total', 0)


def code_search(code):
    c = re.sub(r'[^A-Za-z0-9]', '', code).upper()
    if len(c) != 3:
        raise Refused('A product code is three letters, such as QBS. Got: %s' % code)
    return c


def number_type(n):
    n = n.strip().upper()
    if re.fullmatch(r'K\d{6}', n):
        return n, '510(k)'
    if re.fullmatch(r'DEN\d{6}', n):
        return n, 'De Novo'
    if re.fullmatch(r'P\d{6}', n):
        return n, 'PMA'
    raise Refused('Not a K, DEN or P number: %s' % n)


def cell(v, width=None):
    v = '' if v is None else str(v)
    v = re.sub(r'\s+', ' ', v).replace('|', '/').strip()
    if width and len(v) > width:
        v = v[:width - 1].rstrip() + '…'
    return v


def table(headers, rows):
    print()
    print('| ' + ' | '.join(headers) + ' |')
    print('|' + '---|' * len(headers))
    for r in rows:
        print('| ' + ' | '.join(cell(x) for x in r) + ' |')
    print()


NAMES = {'classification': 'classification', '510k': '510(k) and De Novo', 'pma': 'PMA',
         'recall': 'recalls', 'event': 'adverse events', 'udi': 'GUDID'}


def footer():
    dates = {k: v for k, v in _meta.items() if k in NAMES}
    if dates:
        print('openFDA data as of: %s. Anything FDA recorded after these dates is not in these '
              'results.' % '; '.join('%s %s' % (NAMES[k], v) for k, v in dates.items()))


def ymd(d):
    d = d or ''
    return '%s-%s-%s' % (d[:4], d[4:6], d[6:8]) if re.fullmatch(r'\d{8}', d) else d


# ------------------------------------------------------------------ commands

def cmd_check(a):
    data = query('classification', 'product_code:QBS', limit=1)
    if not data.get('results'):
        raise Refused('FDA answered but returned nothing for a known product code.')
    print('openfda %s ok: FDA\'s device API answered. API key: %s.'
          % (VERSION, 'in use' if api_key() else 'none (1,000 queries a day)'))
    footer()


def cmd_classify(a):
    terms = [term(t) for t in a.terms]
    join = '+OR+' if a.any else '+AND+'
    fields = []
    for f in ('device_name', 'definition'):
        fields.append('(' + join.join('%s:%s' % (f, t) for t in terms) + ')')
    rows, n = records('classification', '+OR+'.join(fields), limit=a.limit)
    if a.json:
        print(json.dumps(rows, indent=2))
        return
    print('%d product code%s match; showing %d.' % (n, '' if n == 1 else 's', len(rows)))
    if rows:
        table(['Code', 'Class', 'Submission', 'Regulation', 'Device name', 'Definition'],
              [(r.get('product_code'), device_class(r.get('device_class')),
                submission(r.get('submission_type_id')),
                r.get('regulation_number'), r.get('device_name'),
                cell(r.get('definition'), 160)) for r in rows])
    footer()


def cmd_devices(a):
    terms = [term(t) for t in a.terms]
    join = '+OR+' if a.any else '+AND+'
    s = '(' + join.join('device_name:%s' % t for t in terms) + ')'
    counts = query('510k', s, count='product_code')
    rows, n = records('510k', s, sort='decision_date:desc', limit=a.limit)
    ps = '(' + join.join('trade_name:%s' % t for t in terms) + ')+OR+(' + \
         join.join('generic_name:%s' % t for t in terms) + ')'
    prows, pn = records('pma', '(' + ps + ')+AND+supplement_number:""', sort='decision_date:desc',
                        limit=min(a.limit, 25))
    if a.json:
        print(json.dumps({'by_code': counts.get('results', []), '510k': rows, 'pma': prows},
                         indent=2))
        return
    print('%d cleared device%s (510(k) and De Novo) with these words in the name; %d PMA '
          'original%s.' % (n, '' if n == 1 else 's', pn, '' if pn == 1 else 's'))
    by = counts.get('results', [])
    if by:
        print('\nWhich product codes they sit under:')
        table(['Code', 'Devices'], [(x['term'].upper(), x['count']) for x in by[:15]])
        if len(by) > 15:
            print('%d more codes, with fewer devices each.' % (len(by) - 15))
    if rows:
        print('Newest first:')
        table(['Number', 'Code', 'Decided', 'Applicant', 'Device'],
              [(r.get('k_number'), r.get('product_code'), r.get('decision_date'),
                r.get('applicant'), cell(r.get('device_name'), 120)) for r in rows])
    if prows:
        print('PMA approvals:')
        table(['Number', 'Code', 'Decided', 'Applicant', 'Trade name'],
              [(r.get('pma_number'), r.get('product_code'), r.get('decision_date'),
                r.get('applicant'), r.get('trade_name')) for r in prows])
    footer()


def ecfr_section(section):
    """The current text of one section of 21 CFR, as plain paragraphs, from eCFR."""
    base = 'https://www.ecfr.gov/api/versioner/v1/'
    if 'ecfr_title' not in _meta:
        print('Query: ' + base + 'titles.json')
        _, _, body = get_compressed(base + 'titles.json')
        _meta['ecfr_title'] = [t for t in json.loads(body.decode('utf-8'))['titles']
                               if t['number'] == 21][0]
    title = _meta['ecfr_title']
    part = section.split('.')[0]
    url = base + 'full/%s/title-21.xml?part=%s&section=%s' % (title['latest_issue_date'], part,
                                                              section)
    print('Query: ' + url)
    _, _, body = get_compressed(url)
    x = body.decode('utf-8')
    if 'TYPE="SECTION"' not in x:
        raise Refused('No section 21 CFR %s in the current eCFR.' % section)
    head = re.search(r'<HEAD>(.*?)</HEAD>', x, re.S)
    paras = [re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', '', p)).strip()
             for p in re.findall(r'<P>(.*?)</P>', x, re.S)]
    return (head.group(1).strip() if head else section), [p for p in paras if p], \
        title['up_to_date_as_of']


def get_compressed(url):
    """eCFR's full-text endpoint refuses clients that cannot take compressed responses."""
    import gzip
    req = urllib.request.Request(url, headers={'User-Agent': AGENT, 'Accept-Encoding': 'gzip'})
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            body = r.read()
            if r.headers.get('Content-Encoding') == 'gzip':
                body = gzip.decompress(body)
            return r.geturl(), r.headers.get('Content-Type', ''), body
    except urllib.error.HTTPError as e:
        raise Refused('eCFR refused the request (%d).' % e.code)
    except urllib.error.URLError as e:
        raise Refused('Cannot reach www.ecfr.gov (%s). Read the regulation by hand at '
                      'https://www.ecfr.gov/current/title-21' % e.reason)


def cmd_regulation(a):
    section = re.sub(r'[^0-9.]', '', a.section)
    if not re.fullmatch(r'\d{3,4}\.\d{1,4}', section):
        raise Refused('A regulation number looks like 886.4150. Got: %s' % a.section)
    head, paras, asof = ecfr_section(section)
    print()
    print(head)
    for p in paras:
        print()
        print(p)
    print()
    print('Source: https://www.ecfr.gov/current/title-21/section-%s' % section)
    print('eCFR current as of: %s. The eCFR is an editorial compilation, not the official legal '
          'edition; the Federal Register is.' % asof)
    if a.limits:
        part = section.split('.')[0]
        print()
        print('--- Limits on exemptions for this part, 21 CFR %s.9 ---' % part)
        h, ps, _ = ecfr_section(part + '.9')
        print(h)
        for p in ps:
            print()
            print(p)


STD = DOCS + 'scripts/cdrh/cfdocs/cfStandards/'


def plain(x):
    """HTML fragment to one line of text."""
    import html
    return re.sub(r'\s+', ' ', html.unescape(re.sub(r'<[^>]+>', ' ', x or ''))).strip()


def get_page(url, data=None):
    """One page from FDA's website, as text. `data` makes it a form post."""
    print('Fetch: ' + url + ('  [search: %s]' % data if data else ''))
    body = urllib.parse.urlencode(data).encode() if data else None
    req = urllib.request.Request(url, data=body, headers={'User-Agent': AGENT})
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            final, text = r.geturl(), r.read().decode('utf-8', 'replace')
    except urllib.error.URLError as e:
        raise Refused('Cannot reach %s (%s).' % (urllib.parse.urlsplit(url).netloc,
                                                   getattr(e, 'reason', e)))
    if 'apology' in final or 'abuse-detection' in text[:2000]:
        raise Refused('FDA\'s site blocked the request as too fast or too many. Wait an hour, '
                      'then try again.')
    return text


def standard_detail(ident):
    """Extent of recognition and any transition, from a standard's FDA recognition page."""
    t = plain(get_page(STD + 'detail.cfm?standard__identification_no=%s' % ident))
    extent = re.search(r'Extent of Recognition (.*?) Rationale for Recognition', t)
    trans = re.search(r'Transition Period (.*?)(?: Public Law| Relevant FDA Guidance| Product Code|$)',
                      t)
    return (extent.group(1).strip() if extent else 'not stated',
            trans.group(1).strip()[:400] if trans else '')


def cmd_standards(a):
    rows, guidance = [], []
    if a.code:
        c = code_search(a.code)
        page = get_page(DOCS + 'scripts/cdrh/cfdocs/cfpcd/classification.cfm?id=' + c)
        sec = page.split('Recognized Consensus Standards', 1)[-1].split('Guidance Document', 1)
        if 'Recognized Consensus Standards' in page:
            for m in re.finditer(r'<li>\s*([\d]+-[\d]+)&nbsp;(.*?)&nbsp;(.*?)<br>\s*<a[^>]*'
                                 r'identification_no=(\d+)"[^>]*>(.*?)</a>', sec[0], re.S):
                rows.append({'rec': m.group(1), 'sdo': plain(m.group(2)),
                             'designation': plain(m.group(3)), 'id': m.group(4),
                             'title': plain(m.group(5)), 'extent': ''})
        if len(sec) > 1:
            block = re.split(r'</table>', sec[1], maxsplit=1, flags=re.I)[0]  # the guidance list only
            for m in re.finditer(r'<li>\s*<a[^>]*href="([^"]+)"[^>]*>(.*?)</li>', block,
                                 re.S | re.I):
                guidance.append((plain(m.group(2)), m.group(1)))
        what = 'product code %s' % c
    else:
        num = re.sub(r'[^A-Za-z0-9.\- ]', '', a.number).strip()
        if not num:
            raise Refused('Give a standard number, such as 10993-1 or 60601-1.')
        page = get_page(STD + 'results.cfm', {'referencenumber': num, 'search': 'Search'})
        exact = re.compile(r'(?<![\d-])' + re.escape(num) + r'(?![\d])')
        for m in re.finditer(r'>(\d\d/\d\d/\d{4})</td>\s*<td[^>]*>(.*?)</td>\s*<td[^>]*>'
                             r'(\d+-\d+)</td>\s*<td[^>]*>(.*?)</td>.*?<td[^>]*nowrap[^>]*>(.*?)'
                             r'</td>\s*<td[^>]*>(.*?)</td>\s*<td align="left">.*?'
                             r'identification_no=(\d+).*?<span[^>]*>(.*?)</span>', page, re.S):
            designation = plain(m.group(6))
            if exact.search(designation):
                rows.append({'rec': m.group(3), 'sdo': plain(m.group(5)),
                             'designation': designation, 'id': m.group(7),
                             'title': plain(m.group(8)), 'extent': plain(m.group(4)),
                             'area': plain(m.group(2)), 'entered': m.group(1)})
        what = 'standard number %s' % num
    if a.details:
        for r in rows[:10]:
            time.sleep(1)
            r['extent'], r['transition'] = standard_detail(r['id'])
    if a.json:
        print(json.dumps({'standards': rows, 'guidance': guidance}, indent=2))
        return
    print('%d FDA-recognized standard%s for %s.' % (len(rows), '' if len(rows) == 1 else 's', what))
    if rows:
        table(['FDA recognition', 'Standard', 'Title', 'Extent'],
              [(r['rec'], '%s %s' % (r['sdo'], r['designation']), r['title'],
                r['extent'] or 'see --details') for r in rows])
        seen = set()
        for r in rows:
            if r.get('transition') and r['transition'] not in seen:
                seen.add(r['transition'])
                print('Transition: ' + r['transition'])
        print('Recognition changes as FDA adds and supersedes editions. Check each on FDA\'s '
              'standards database before declaring conformity: ' + STD + 'search.cfm')
    if guidance:
        print('\nGuidance FDA links to this product code:')
        for title, url in guidance:
            print('- %s: %s' % (title, url))


def cmd_guidance(a):
    url = a.url.strip()
    host = urllib.parse.urlsplit(url).netloc.lower()
    if not (host == 'www.fda.gov' or host.endswith('.fda.gov')):
        raise Refused('Only FDA guidance pages on www.fda.gov. Got: %s' % url)
    page = get_page(url)
    title = re.search(r'<h1[^>]*>(.*?)</h1>', page, re.S)
    title = plain(re.split(r'<span', title.group(1))[0]) if title else 'guidance'
    slug = re.sub(r'[^a-z0-9]+', '-', title.lower()).strip('-')[:80] or 'guidance'
    os.makedirs(a.out, exist_ok=True)
    link = re.search(r'<a[^>]*href="(/media/\d+/download[^"]*)"[^>]*>\s*(?:<[^>]+>\s*)*'
                     r'Download\s+the\s+(?:(?:Final|Draft)\s+)?Guidance', page, re.I)
    if link:
        time.sleep(1)
        final, ctype, body = get('https://www.fda.gov' + link.group(1), binary=True)
        print('Fetch: https://www.fda.gov' + link.group(1))
        if body[:4] == b'%PDF':
            path = os.path.join(a.out, slug + '.pdf')
            with open(path, 'wb') as f:
                f.write(body)
            print('Saved: %s — "%s" (PDF, %d KB)' % (path, title, len(body) // 1024))
            return
    # Many older guidance documents are published as the web page itself.
    body = re.search(r'<article[^>]*>(.*?)</article>', page, re.S) or \
        re.search(r'<main[^>]*>(.*?)</main>', page, re.S)
    if not body:
        raise Refused('Found no guidance text or download on that page. Open it by hand: ' + url)
    text = re.sub(r'<(script|style)[^>]*>.*?</\1>', '', body.group(1), flags=re.S | re.I)
    text = re.sub(r'</?(p|li|h[1-6]|tr|br|div)[^>]*>', '\n', text, flags=re.I)
    lines = [plain(line) for line in text.split('\n')]
    text = '\n\n'.join(line for line in lines if line)
    path = os.path.join(a.out, slug + '.txt')
    with open(path, 'w', encoding='utf-8') as f:
        f.write('%s\n\nSource: %s\nRead on: %s\n\n%s\n' % (title, url, time.strftime('%Y-%m-%d'),
                                                         text))
    print('Saved: %s — "%s" (published as a web page; text saved, %d KB)'
          % (path, title, len(text) // 1024))


def cmd_code(a):
    c = code_search(a.code)
    data = query('classification', 'product_code:' + c, limit=1)
    if not data.get('results'):
        raise Refused('No product code %s in FDA\'s classification database.' % c)
    r = data['results'][0]
    if a.json:
        print(json.dumps(r, indent=2))
        return
    reg = r.get('regulation_number') or ''
    print()
    print('Product code: %s — %s' % (c, r.get('device_name')))
    print('Class: %s' % device_class(r.get('device_class')))
    print('Submission type: %s' % submission(r.get('submission_type_id')))
    print('Regulation: %s' % ('21 CFR %s — https://www.ecfr.gov/current/title-21/section-%s'
                              % (reg, reg) if reg else "none in FDA's record"))
    print('Review panel: %s' % (r.get('medical_specialty_description') or r.get('review_panel')))
    print('Implant: %s' % YESNO.get(r.get('implant_flag'), r.get('implant_flag')))
    print('Life-sustaining or life-supporting: %s'
          % YESNO.get(r.get('life_sustain_support_flag'), r.get('life_sustain_support_flag')))
    print('Exempt from GMP requirements: %s'
          % YESNO.get(r.get('gmp_exempt_flag'), r.get('gmp_exempt_flag')))
    print('Eligible for third-party 510(k) review: %s'
          % YESNO.get(r.get('third_party_flag'), r.get('third_party_flag')))
    print('Summary malfunction reporting: %s' % r.get('summary_malfunction_reporting'))
    if r.get('unclassified_reason'):
        print('Why unclassified: %s' % UNCLASSIFIED.get(r['unclassified_reason'],
                                                         r['unclassified_reason']))
    print('FDA page: %sscripts/cdrh/cfdocs/cfpcd/classification.cfm?id=%s' % (DOCS, c))
    print()
    print('Definition: %s' % cell(r.get('definition')) if r.get('definition')
          else 'Definition: none given by FDA')
    print()
    k = total('510k', 'product_code:%s+AND+k_number:K*' % c)
    den = total('510k', 'product_code:%s+AND+k_number:DEN*' % c)
    pma = total('pma', 'product_code:%s+AND+supplement_number:""' % c)
    rec = total('recall', 'product_code:' + c)
    ev = query('event', 'device.device_report_product_code:' + c, count='event_type.exact')
    events = ', '.join('%s %d' % (x['term'] or 'Not stated', x['count'])
                       for x in ev.get('results', [])) or 'none'
    print()
    print('510(k) clearances: %d' % k)
    print('De Novo grants: %d' % den)
    print('PMA approvals (originals): %d' % pma)
    print('Recalls: %d' % rec)
    print('Adverse event reports: %s' % events)
    if k or den:
        recent, _ = records('510k', 'product_code:' + c, sort='decision_date:desc', limit=5)
        print()
        print('Most recent clearances and grants:')
        table(['Number', 'Decided', 'Applicant', 'Device'],
              [(x.get('k_number'), x.get('decision_date'), x.get('applicant'),
                x.get('device_name')) for x in recent])
    footer()


def regulation_number(r):
    r = re.sub(r'[^0-9.]', '', r or '')
    if not re.fullmatch(r'\d{3,4}\.\d{1,4}', r):
        raise Refused('A regulation number looks like 886.4150. Got: %s' % r)
    return r


def family_codes(reg):
    rows, _ = records('classification', 'regulation_number:' + reg, limit=100)
    if not rows:
        raise Refused("No product codes under 21 CFR %s in FDA's classification database." % reg)
    return rows


def cmd_family(a):
    reg = regulation_number(a.regulation)
    rows = family_codes(reg)
    codes = [r['product_code'] for r in rows]
    counts = query('510k', '+OR+'.join('product_code:' + c for c in codes), count='product_code')
    n = {x['term'].upper(): x['count'] for x in counts.get('results', [])}
    if a.json:
        print(json.dumps({'codes': rows, 'clearances': n}, indent=2))
        return
    print('%d product code%s under 21 CFR %s.' % (len(rows), '' if len(rows) == 1 else 's', reg))
    table(['Code', 'Class', 'Submission', 'Device name', '510(k) and De Novo'],
          [(r.get('product_code'), device_class(r.get('device_class')),
            submission(r.get('submission_type_id')), r.get('device_name'),
            n.get(r.get('product_code'), 0)) for r in rows])
    print('The primary predicate for a 510(k) almost always sits in the same classification '
          'regulation. These are the codes to search first.')
    footer()


def cmd_clearances(a):
    if a.regulation:
        reg = regulation_number(a.regulation)
        codes = [r['product_code'] for r in family_codes(reg)]
        c = '21 CFR %s (%s)' % (reg, ', '.join(codes))
        s = '(' + '+OR+'.join('product_code:' + x for x in codes) + ')'
    else:
        c = code_search(a.code)
        s = 'product_code:' + c
    if a.denovo:
        s += '+AND+k_number:DEN*'
    if a.since:
        s += '+AND+decision_date:[%d0101+TO+99991231]' % a.since
    rows, n = records('510k', s, sort='decision_date:desc', limit=a.limit)
    if a.json:
        print(json.dumps(rows, indent=2))
        return
    print('%d found under %s; showing %d, newest first.' % (n, c, len(rows)))
    table(['Number', 'Code', 'Type', 'Decided', 'Decision', 'Applicant', 'Device', 'Summary online'],
          [(r.get('k_number'), r.get('product_code'),
            'De Novo' if (r.get('k_number') or '').startswith('DEN')
            else '510(k)', r.get('decision_date'), r.get('decision_description'),
            r.get('applicant'), r.get('device_name'),
            {'Summary': 'yes', 'Statement': 'no — statement only'}.get(
                r.get('statement_or_summary'), 'check')) for r in rows])
    footer()


def cmd_pma(a):
    c = code_search(a.code)
    s = 'product_code:' + c + ('' if a.supplements else '+AND+supplement_number:""')
    rows, n = records('pma', s, sort='decision_date:desc', limit=a.limit)
    if a.json:
        print(json.dumps(rows, indent=2))
        return
    print('%d found under %s; showing %d, newest first.' % (n, c, len(rows)))
    table(['Number', 'Supplement', 'Decided', 'Applicant', 'Trade name', 'Generic name'],
          [(r.get('pma_number'), r.get('supplement_number') or 'original',
            r.get('decision_date'), r.get('applicant'), r.get('trade_name'),
            r.get('generic_name')) for r in rows])
    footer()


def cmd_recalls(a):
    if a.number:
        n, _ = number_type(a.number)
        s = 'k_numbers:' + n
    else:
        s = 'product_code:' + code_search(a.code)
    rows, n = records('recall', s, sort='event_date_initiated:desc', limit=a.limit)
    if a.json:
        print(json.dumps(rows, indent=2))
        return
    print('%d recall%s found; showing %d, newest first.' % (n, '' if n == 1 else 's', len(rows)))
    if rows:
        table(['Recall', 'Started', 'Status', 'Root cause', 'Cleared under', 'Product'],
              [(r.get('product_res_number'), r.get('event_date_initiated'),
                r.get('recall_status'), r.get('root_cause_description'),
                ', '.join(r.get('k_numbers') or []) or r.get('pma_numbers') or '',
                cell(r.get('product_description'), 120)) for r in rows])
    footer()


def cmd_events(a):
    if a.brand:
        c = 'brand "%s"%s' % (a.brand, ' from "%s"' % a.manufacturer if a.manufacturer else '')
        s = 'device.brand_name:' + term(a.brand)
        if a.manufacturer:
            s += '+AND+device.manufacturer_d_name:' + term(a.manufacturer)
    else:
        c = code_search(a.code)
        s = 'device.device_report_product_code:' + c
    data = query('event', s, count='event_type.exact')
    rows = data.get('results', [])
    if a.json:
        print(json.dumps(rows, indent=2))
        return
    n = sum(x['count'] for x in rows)
    print('%d adverse event report%s under %s.' % (n, '' if n == 1 else 's', c))
    if rows:
        table(['Event type', 'Reports'], [(x['term'] or 'Not stated', x['count']) for x in rows])
        print('A report is an allegation, not a finding. Counts rise with how many devices are in '
              'use, and summary reporting can bundle many malfunctions into one.')
    footer()


def cmd_udi(a):
    c = code_search(a.code)
    rows, n = records('udi', 'product_codes.code:' + c, limit=a.limit)
    if a.json:
        print(json.dumps(rows, indent=2))
        return
    seen = {}
    for r in rows:
        k = (r.get('company_name'), r.get('brand_name'))
        seen[k] = seen.get(k, 0) + 1
    print('%d device listings under %s; %d read, %d distinct brands.'
          % (n, c, len(rows), len(seen)))
    table(['Company', 'Brand', 'Listings'], [(k[0], k[1], v) for k, v in sorted(seen.items(),
          key=lambda kv: (str(kv[0][0]), str(kv[0][1])))])
    footer()


def summary_urls(n, kind):
    if kind == 'De Novo':
        return ['cdrh_docs/reviews/%s.pdf' % n]
    yy = int(n[1:3])
    if kind == '510(k)':
        folder = 'pdf' if 76 <= yy or yy < 2 else 'pdf%d' % yy
        return ['cdrh_docs/%s/%s.pdf' % (folder, n)]
    folder = 'pdf%d' % yy if yy < 76 else 'pdf'
    return ['cdrh_docs/%s/%sB.pdf' % (folder, n), 'cdrh_docs/%s/%sb.pdf' % (folder, n)]


def database_page(n, kind):
    return DOCS + {
        '510(k)': 'scripts/cdrh/cfdocs/cfpmn/pmn.cfm?ID=%s',
        'De Novo': 'scripts/cdrh/cfdocs/cfpmn/denovo.cfm?id=%s',
        'PMA': 'scripts/cdrh/cfdocs/cfpma/pma.cfm?id=%s',
    }[kind] % n


def cmd_fetch(a):
    nums = [number_type(n) for n in a.numbers]
    if len(nums) > MAX_FETCH:
        raise Refused('Ten documents at most per call; got %d. FDA blocks addresses that '
                      'download quickly.' % len(nums))
    os.makedirs(a.out, exist_ok=True)
    got, missing, requests = 0, [], 0
    for n, kind in nums:
        path = os.path.join(a.out, n + '.pdf')
        if os.path.exists(path):
            print('Already here: %s' % path)
            got += 1
            continue
        saved = False
        for rel in summary_urls(n, kind):
            if requests:
                time.sleep(1)
            requests += 1
            print('Fetch: ' + DOCS + rel)
            final, ctype, body = get(DOCS + rel, binary=True)
            if 'abuse' in final or 'apology' in final:
                raise Refused('FDA\'s site blocked the download as too fast or too many. Wait an '
                              'hour, then fetch fewer at a time.')
            if ctype.startswith('application/pdf') and body[:4] == b'%PDF':
                with open(path, 'wb') as f:
                    f.write(body)
                print('Saved: %s (%s summary, %d KB)' % (path, kind, len(body) // 1024))
                saved = True
                got += 1
                break
        if not saved:
            missing.append((n, kind))
    if missing:
        print()
        print('No summary online for these. Older clearances and statement-only 510(k)s often '
              'have none. Check the FDA page by hand:')
        for n, kind in missing:
            print('  %s  %s' % (n, database_page(n, kind)))
    print()
    print('%d of %d saved to %s.' % (got, len(nums), a.out))


# ------------------------------------------------------------------ entry

def main(argv=None):
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    p = argparse.ArgumentParser(prog='openfda', description='FDA\'s device databases for MOS skills.')
    sub = p.add_subparsers(dest='cmd', required=True)

    sub.add_parser('check')

    s = sub.add_parser('classify')
    s.add_argument('terms', nargs='+')
    s.add_argument('--any', action='store_true')
    s.add_argument('--limit', type=int, default=25)
    s.add_argument('--json', action='store_true')

    s = sub.add_parser('devices')
    s.add_argument('terms', nargs='+')
    s.add_argument('--any', action='store_true')
    s.add_argument('--limit', type=int, default=25)
    s.add_argument('--json', action='store_true')

    s = sub.add_parser('code')
    s.add_argument('code')
    s.add_argument('--json', action='store_true')

    s = sub.add_parser('family')
    s.add_argument('regulation')
    s.add_argument('--json', action='store_true')

    s = sub.add_parser('clearances')
    g = s.add_mutually_exclusive_group(required=True)
    g.add_argument('--code')
    g.add_argument('--regulation')
    s.add_argument('--since', type=int)
    s.add_argument('--denovo', action='store_true')
    s.add_argument('--limit', type=int, default=50)
    s.add_argument('--json', action='store_true')

    s = sub.add_parser('pma')
    s.add_argument('--code', required=True)
    s.add_argument('--supplements', action='store_true')
    s.add_argument('--limit', type=int, default=50)
    s.add_argument('--json', action='store_true')

    s = sub.add_parser('recalls')
    g = s.add_mutually_exclusive_group(required=True)
    g.add_argument('--code')
    g.add_argument('--number')
    s.add_argument('--limit', type=int, default=50)
    s.add_argument('--json', action='store_true')

    s = sub.add_parser('events')
    g = s.add_mutually_exclusive_group(required=True)
    g.add_argument('--code')
    g.add_argument('--brand')
    s.add_argument('--manufacturer')
    s.add_argument('--json', action='store_true')

    s = sub.add_parser('udi')
    s.add_argument('--code', required=True)
    s.add_argument('--limit', type=int, default=200)
    s.add_argument('--json', action='store_true')

    s = sub.add_parser('regulation')
    s.add_argument('section')
    s.add_argument('--limits', action='store_true')

    s = sub.add_parser('standards')
    g = s.add_mutually_exclusive_group(required=True)
    g.add_argument('--code')
    g.add_argument('--number')
    s.add_argument('--details', action='store_true')
    s.add_argument('--json', action='store_true')

    s = sub.add_parser('guidance')
    s.add_argument('url')
    s.add_argument('--out', required=True)

    s = sub.add_parser('fetch')
    s.add_argument('numbers', nargs='+')
    s.add_argument('--out', required=True)

    a = p.parse_args(argv)
    if getattr(a, 'limit', 1) < 1:
        p.error('--limit must be at least 1')
    try:
        globals()['cmd_' + a.cmd](a)
    except Refused as e:
        print('openfda: %s' % e, file=sys.stderr)
        return 1
    return 0


if __name__ == '__main__':
    sys.exit(main())
