#!/usr/bin/env python3
"""cms — Medicare coverage policies and public billing codes, for MOS skills.

The reimbursement skill makes every call for coverage policies and codes
through this script, so the searches behave the same whichever AI runs them.
It needs Python 3.8 or later and nothing else.

What leaves the machine:

  To CMS (api.coverage.cms.gov, the Medicare Coverage Database): requests for
  the complete lists of national coverage determinations, local coverage
  determinations and billing articles, and the number of any national
  determination read in full. No search term goes to CMS: the lists are
  downloaded whole and searched on this machine.

  To the National Library of Medicine (clinicaltables.nlm.nih.gov, which also
  runs ClinicalTrials.gov): the words given to `hcpcs` and `icd10`, to look up
  public billing and diagnosis codes.

  To CMS (www.cms.gov), for `payment dme` and `payment drg`: requests for
  CMS's complete public payment files — the DMEPOS fee schedule and the
  inpatient final rule's tables 5 and 1A-1E. Downloaded whole, kept in a cache
  folder on this machine, and searched here. No code or term is sent.

Nothing else. No company text is sent, and the only file read is a CMS payment
file the user downloaded and saved (`payment pfs`, `opps`, `asc`). Every
command prints the exact URL it ran, so a skill can show the user what went and
log it.

Commands:

  check
      Confirm CMS and the National Library of Medicine can be reached. Sends
      one request to each.

  coverage TERM [TERM ...] [--any] [--type ncd|lcd|article|all]
      Coverage policies whose titles match: national coverage determinations
      (NCDs), local coverage determinations (LCDs) set by the regional Medicare
      contractors, and the billing and coding articles that go with them. A
      policy must match every term unless --any. Downloads the lists whole and
      searches them here.

  ncd NUMBER [--version V]
      One national coverage determination in full: benefit category, the item
      or service, indications and limitations. NUMBER is the document id the
      `coverage` command prints (for example 108), not the display number.

  lcd NUMBER
      Where to read one local coverage determination or article. Their full
      text is served only under the American Medical Association's CPT
      license, and this script does not accept a license on a user's behalf,
      so it prints the public page for a person to read.

  hcpcs TERM [TERM ...] [--limit N]
      HCPCS Level II codes — the codes CMS maintains for supplies, equipment,
      drugs and devices, including device pass-through codes — whose short
      descriptions match. HCPCS Level II is CMS's own and public.

  icd10 TERM [TERM ...] [--limit N]
      ICD-10-CM diagnosis codes whose names match. Coverage policies list the
      diagnoses they cover by these codes.

  payment dme CODE
      What Medicare pays for a HCPCS Level II equipment or supply code at home,
      from the DMEPOS fee schedule: for each modifier (new, used, rented), the
      lowest, middle and highest state amount, non-rural and rural. Fetches the
      current quarter's public file.

  payment drg NUMBER
      What Medicare pays a hospital for a stay in one MS-DRG, nationally: the
      group's weight times the national standardized amounts. Fetches the
      current fiscal year's public tables.

  payment pfs CODE [--file ZIP]
      What Medicare pays a physician for a code under the physician fee
      schedule: national amounts in an office and in a facility, and the lowest
      and highest locality. Reads the relative value file the user downloaded.

  payment opps CODE [--file ZIP]
      What Medicare pays a hospital outpatient department for a code, its APC,
      and, for a device-intensive procedure, the share CMS attributes to the
      device (the device offset). Reads the OPPS final rule addenda the user
      downloaded.

  payment asc CODE [--file ZIP]
      What Medicare pays an ambulatory surgery center for a code. Reads the ASC
      payment rate file the user downloaded.

  For pfs, opps and asc the file carries CPT codes, which are the American
  Medical Association's. CMS serves some of these files behind the AMA's
  license and some without it; either way this script does not fetch them on a
  user's behalf. Without --file it looks in context/commercial/cms-files/, and
  if the file is not there it prints the CMS page to download it from. It
  prints amounts by code number and never prints a CPT description.

CPT codes — the codes for procedures physicians bill — are the American
Medical Association's copyright. This script does not search them. A skill may
cite a CPT code number the user gives it, never the code's description.

Payment amounts are Medicare's published amounts before the adjustments a
claim gets: sequestration, a hospital's own wage index, teaching and
disproportionate share adjustments, outliers, multiple-procedure discounts.
They are a planning figure, not what any one claim will pay.

Medicare coverage policies change. Every result carries the date it was read;
the policy's own page is the authority.
"""

import argparse
import csv
import glob
import html
import io
import json
import os
import re
import statistics
import sys
import tempfile
import time
import urllib.error
import urllib.parse
import urllib.request
import zipfile
from datetime import date

VERSION = '0.2.0'  # a shared contract: a change in behaviour is a new MOS release

MCD = 'https://api.coverage.cms.gov/v1/'
MCD_PAGE = 'https://www.cms.gov/medicare-coverage-database/view/'
NLM = 'https://clinicaltables.nlm.nih.gov/api/'
AGENT = 'Mozilla/5.0 (compatible; MOS-cms/%s)' % VERSION

LISTS = {
    'ncd': 'reports/national-coverage-ncd/',
    'lcd': 'reports/local-coverage-final-lcds/',
    'article': 'reports/local-coverage-articles/',
}


def get(url):
    print('Query: ' + url)
    req = urllib.request.Request(url, headers={'User-Agent': AGENT, 'Accept': 'application/json'})
    for attempt in range(3):
        try:
            with urllib.request.urlopen(req, timeout=90) as r:
                return json.loads(r.read().decode('utf-8'))
        except urllib.error.HTTPError as e:
            if e.code == 429 and attempt < 2:
                time.sleep(5 * (attempt + 1))
                continue
            if e.code == 401:
                sys.exit('The server asked for a license token. This script does not accept a license on a user\'s behalf.')
            sys.exit('The server refused the request: HTTP %s' % e.code)
        except urllib.error.URLError as e:
            sys.exit('Could not reach %s: %s' % (urllib.parse.urlparse(url).netloc, e.reason))
    sys.exit('The server kept refusing the request. Wait a minute and try again.')


def mcd_list(kind):
    """A whole list, following next_token if the API ever pages it."""
    out, token = [], ''
    while True:
        url = MCD + LISTS[kind] + (('?next_token=' + urllib.parse.quote(token)) if token else '')
        d = get(url)
        out.extend(d.get('data', []))
        token = (d.get('meta') or {}).get('next_token') or ''
        if not token:
            return out


def plain(text):
    """The API's fields are HTML, often escaped twice. Return readable text."""
    if not text:
        return ''
    t = html.unescape(html.unescape(str(text)))
    t = re.sub(r'<\s*(br|/p|/li|/h\d)\s*/?>', '\n', t, flags=re.I)
    t = re.sub(r'<\s*li[^>]*>', '- ', t, flags=re.I)
    t = re.sub(r'<[^>]+>', '', t)
    t = re.sub(r'[ \t\r\f\v]+', ' ', t)
    t = re.sub(r'\n\s*\n+', '\n\n', t)
    return t.strip()


def matches(title, terms, any_term):
    """A term matches at the start of a word: "tens" finds TENS, not "intensive"."""
    t = title.lower()
    hits = [re.search(r'(?<![a-z0-9])' + re.escape(term.lower()), t) is not None for term in terms]
    return any(hits) if any_term else all(hits)


def footer():
    print('\nRead %s. Medicare coverage policies change; the policy\'s own page is the authority.' % date.today().isoformat())


# ---------------------------------------------------------------- commands

def cmd_check(a):
    d = get(MCD + 'metadata/update-period')
    periods = d.get('data') or [{}]
    print('Reached the Medicare Coverage Database. Last weekly update: %s to %s.' % (
        periods[0].get('begin_date', '?'), periods[0].get('end_date', '?')))
    d = get(NLM + 'hcpcs/v3/search?terms=wound&maxList=1')
    print('Reached the National Library of Medicine code tables (%s HCPCS matches for "wound").' % d[0])


def cmd_coverage(a):
    kinds = ['ncd', 'lcd', 'article'] if a.type == 'all' else [a.type]
    print('Downloading the complete list%s and searching on this machine. No search term is sent.\n' %
          ('s' if len(kinds) > 1 else ''))
    label = {'ncd': 'National coverage determinations', 'lcd': 'Local coverage determinations',
             'article': 'Billing and coding articles'}
    for kind in kinds:
        rows = mcd_list(kind)
        hits = [r for r in rows if matches(r.get('title', ''), a.terms, a.any)]
        print('\n%s: %d of %d match.' % (label[kind], len(hits), len(rows)))
        for r in hits[:a.limit]:
            if kind == 'ncd':
                print('  NCD %s (id %s, version %s) — %s; updated %s' % (
                    r.get('document_display_id'), r.get('document_id'), r.get('document_version'),
                    plain(r.get('title')), r.get('last_updated')))
            else:
                contractor = plain(r.get('contractor_name_type', '')).split('\n')[0]
                print('  %s — %s; %s; effective %s%s' % (
                    r.get('document_display_id'), plain(r.get('title')), contractor, r.get('effective_date'),
                    '' if r.get('retirement_date') in (None, '', 'N/A') else '; retired %s' % r.get('retirement_date')))
        if len(hits) > a.limit:
            print('  ... %d more; narrow the terms or raise --limit.' % (len(hits) - a.limit))
    print('\nNCDs apply everywhere in Medicare. LCDs and articles apply only in the regions of the contractor')
    print('named. Read NCDs with `ncd`; LCDs and articles are read on their CMS page (`lcd`).')
    footer()


def cmd_ncd(a):
    params = {'ncdid': a.number}
    if a.version:
        params['ncdver'] = a.version
    else:
        rows = mcd_list('ncd')
        match = [r for r in rows if str(r.get('document_id')) == str(a.number)]
        if not match:
            sys.exit('No national coverage determination has id %s. Use the id `coverage` prints.' % a.number)
        params['ncdver'] = match[0].get('document_version')
    d = get(MCD + 'data/ncd?' + urllib.parse.urlencode(params))
    data = (d or {}).get('data') or []
    if not data:
        sys.exit('No text returned for NCD id %s.' % a.number)
    n = data[0]
    print('NCD %s — %s' % (n.get('document_display_id'), plain(n.get('title'))))
    print('Effective %s%s' % (n.get('effective_date'),
                              '' if n.get('effective_end_date') in (None, '', 'N/A') else '; ends %s' % n.get('effective_end_date')))
    print('Benefit category: %s' % plain(n.get('benefit_category')))
    for key, head in (('item_service_description', 'Item or service'),
                      ('indications_limitations', 'Indications and limitations of coverage'),
                      ('cross_reference', 'Cross reference'), ('other_text', 'Other')):
        body = plain(n.get(key))
        if body:
            print('\n%s\n%s\n%s' % (head, '-' * len(head), body))
    print('\nPage: %sncd.aspx?ncdid=%s&ncdver=%s' % (MCD_PAGE, a.number, params['ncdver']))
    footer()


def cmd_lcd(a):
    num = a.number.upper().lstrip('LA')
    kind = 'article' if a.number.upper().startswith('A') else 'lcd'
    page = '%s%s.aspx?%sid=%s' % (MCD_PAGE, 'article' if kind == 'article' else 'lcd',
                                  'article' if kind == 'article' else 'lcd', num)
    print('%s %s' % ('Article' if kind == 'article' else 'LCD', a.number.upper()))
    print('Read it here: %s' % page)
    print('\nIts full text, including the codes it covers, is served under the American Medical')
    print('Association\'s CPT license. This script does not accept that license for you. A person')
    print('reads the page; the skill records what it says about coverage, in its own words, and')
    print('cites CPT codes by number only.')


def nlm_search(table, terms, limit):
    params = {'terms': ' '.join(terms), 'maxList': limit,
              'df': 'code,display' if table == 'hcpcs' else 'code,name'}
    if table == 'icd10cm':
        params['sf'] = 'code,name'  # search names too; the default searches codes only
    q = urllib.parse.urlencode(params)
    d = get('%s%s/v3/search?%s' % (NLM, table, q))
    total, codes, _, rows = d[0], d[1], d[2], d[3]
    print('%d match; showing %d.\n' % (total, len(rows)))
    for r in rows:
        print('  %-9s %s' % (r[0], r[1]))
    return total


def cmd_hcpcs(a):
    nlm_search('hcpcs', a.terms, a.limit)
    print('\nHCPCS Level II: maintained by CMS, public. Short descriptions shown; the CMS HCPCS file')
    print('is the authority. C-codes are hospital outpatient device codes, often pass-through;')
    print('E, K and L codes are equipment and devices; A codes are supplies.')
    footer()


def cmd_icd10(a):
    nlm_search('icd10cm', a.terms, a.limit)
    print('\nICD-10-CM diagnosis codes, from the National Library of Medicine\'s tables.')
    footer()


# ---------------------------------------------------------------- payment amounts

CMS_FILES = 'https://www.cms.gov/files/zip/'
CACHE = os.path.join(tempfile.gettempdir(), 'mos-cms-cache')
SAVED = os.path.join('context', 'commercial', 'cms-files')

# Where a user downloads the files that carry CPT codes. CMS serves them under the AMA's license.
LICENSED = {  # what the file is, where to get it, and a file name inside the zip that identifies it
    'pfs': ('the physician fee schedule relative value file for the latest quarter (RVUyyA to RVUyyD)',
            'https://www.cms.gov/medicare/payment/fee-schedules/physician/pfs-relative-value-files',
            r'^PPRRVU.*\.csv$'),
    'opps': ('the OPPS final rule addenda for the year: the zip of all addenda, with Addendum B and '
             'Addendum P inside, from the final rule\'s page',
             'https://www.cms.gov/medicare/payment/prospective-payment-systems/hospital-outpatient/regulations-notices',
             r'Addendum P.*Offsets.*\.csv$'),
    'asc': ('the ASC addenda for the latest quarter (Addendum AA inside)',
            'https://www.cms.gov/medicare/payment/prospective-payment-systems/ambulatory-surgical-center-asc/asc-payment-rates-addenda',
            r'ASC.?AA.*\.csv$'),
}


def fetch_file(name):
    """One public CMS zip, cached on this machine. None if CMS has no file by that name."""
    os.makedirs(CACHE, exist_ok=True)
    path = os.path.join(CACHE, name)
    if os.path.exists(path) and time.time() - os.path.getmtime(path) < 7 * 86400:
        print('Cached: %s (fetched from %s%s)' % (path, CMS_FILES, name))
        return path
    url = CMS_FILES + name
    print('Query: ' + url)
    req = urllib.request.Request(url, headers={'User-Agent': AGENT})
    try:
        with urllib.request.urlopen(req, timeout=180) as r:
            data = r.read()
    except urllib.error.HTTPError as e:
        if e.code == 404:
            return None
        sys.exit('The server refused the request: HTTP %s' % e.code)
    except urllib.error.URLError as e:
        sys.exit('Could not reach www.cms.gov: %s' % e.reason)
    if not data.startswith(b'PK'):
        return None  # a page, not a zip: CMS has not published that file
    with open(path, 'wb') as f:
        f.write(data)
    return path


def zip_text(path, pattern):
    """The text of the first file in a zip whose name matches the pattern."""
    with zipfile.ZipFile(path) as z:
        for n in z.namelist():
            if re.search(pattern, os.path.basename(n), re.I):
                return n, z.read(n).decode('latin-1')
            if n.lower().endswith('.zip'):
                inner = zipfile.ZipFile(io.BytesIO(z.read(n)))
                for m in inner.namelist():
                    if re.search(pattern, os.path.basename(m), re.I):
                        return m, inner.read(m).decode('latin-1')
    return None, None


def money(x):
    return '$' + format(x, ',.2f')


def num(s):
    s = (s or '').replace('$', '').replace(',', '').replace('"', '').replace('%', '').strip()
    try:
        return float(s)
    except ValueError:
        return None


def holds(path, pattern):
    try:
        return zip_text(path, pattern)[0] is not None
    except zipfile.BadZipFile:
        return False


def saved_file(kind, given, required=True):
    """A licensed CMS file the user downloaded, found by what is inside it, or instructions to get it."""
    what, page, inside = LICENSED[kind]
    if given:
        if not os.path.exists(given):
            sys.exit('No file at %s.' % given)
        if not holds(given, inside):
            sys.exit('%s is not %s.' % (given, what))
        return given
    for path in sorted(glob.glob(os.path.join(SAVED, '*.zip')), key=os.path.getmtime, reverse=True):
        if holds(path, inside):
            print('Reading the file you saved: %s' % path)
            return path
    if not required:
        return None
    print('This needs %s.' % what)
    print('It carries CPT codes, which are the American Medical Association\'s. CMS serves files like it')
    print('under the AMA\'s license, or with the AMA\'s notice. This script does not accept that license')
    print('or fetch the file for you.')
    print('\nDownload it from: %s' % page)
    print('Save the zip, unopened, in %s%s and run this again.' % (SAVED, os.sep))
    sys.exit(2)


def payment_footer(source):
    print('\nSource: %s. Read %s.' % (source, date.today().isoformat()))
    print('Published Medicare amounts before a claim\'s own adjustments (sequestration, local wage index,')
    print('teaching and safety-net adjustments, outliers, multiple-procedure discounts). A planning figure,')
    print('not what any one claim will pay. Private insurers set their own rates.')


def cmd_payment_dme(a):
    code = a.code.upper()
    today = date.today()
    q = (today.month - 1) // 3 + 1
    path, label = None, None
    for year in (today.year, today.year - 1):
        yy = str(year)[2:]
        quarters = range(q, 0, -1) if year == today.year else range(4, 0, -1)
        for qq in quarters:
            for name in (['dme%s.zip' % yy, 'dme%s-a.zip' % yy] if qq == 1 else ['dme%s-%s.zip' % (yy, 'abcd'[qq - 1])]):
                path = fetch_file(name)
                if path:
                    label = 'DMEPOS fee schedule, %s quarter %d (%s)' % (year, qq, name)
                    break
            if path:
                break
        if path:
            break
    if not path:
        sys.exit('Could not find a DMEPOS fee schedule file on cms.gov.')
    name, text = zip_text(path, r'^DMEPOS.*\.csv$')
    if not text:
        sys.exit('The DMEPOS zip has no fee schedule CSV in the layout this script knows.')
    rows = list(csv.reader(io.StringIO(text)))
    head = next(i for i, r in enumerate(rows) if r and r[0].strip().upper() == 'HCPCS')
    cols = rows[head]
    states = [(i, c) for i, c in enumerate(cols) if re.match(r'^[A-Z]{2} \((NR|R)\)$', c.strip())]
    hits = [r for r in rows[head + 1:] if r and r[0].strip().upper() == code]
    print('\n%s in the DMEPOS fee schedule: %d row%s.' % (code, len(hits), '' if len(hits) == 1 else 's'))
    if not hits:
        print('No fee schedule amount. The code may be paid another way (priced by the contractor, bundled,')
        print('or not a DMEPOS code), or not covered. A fee schedule amount never means coverage.')
    mods = {'NU': 'purchased, new', 'UE': 'purchased, used', 'RR': 'rented, per month', '': 'no modifier'}
    cats = {'IN': 'inexpensive or routinely purchased', 'FS': 'frequently serviced', 'CR': 'capped rental',
            'OX': 'oxygen', 'OS': 'ostomy, tracheostomy and urological', 'SD': 'surgical dressings',
            'PO': 'prosthetics and orthotics', 'SU': 'supplies', 'TE': 'TENS', 'TS': 'therapeutic shoes',
            'IL': 'intraocular lenses', 'SC': 'splints and casts', 'LC': 'lymphedema compression'}
    for r in hits:
        mod = r[1].strip()
        print('\n  %s %s — %s; category %s (%s)' % (code, mod, mods.get(mod, 'modifier ' + mod),
                                                    r[4].strip(), cats.get(r[4].strip(), '?')))
        for kind, word in (('NR', 'non-rural'), ('R', 'rural')):
            vals = [(c[:2], num(r[i])) for i, c in states if c.strip().endswith('(%s)' % kind)]
            vals = [(s, v) for s, v in vals if v]
            if not vals:
                continue
            amounts = sorted(v for _, v in vals)
            lo = min(vals, key=lambda x: x[1])
            hi = max(vals, key=lambda x: x[1])
            print('    %-9s lowest %s (%s), middle %s, highest %s (%s), across %d states and territories' % (
                word, money(lo[1]), lo[0], money(statistics.median(amounts)), money(hi[1]), hi[0], len(vals)))
    print('\nThe supplier is paid this amount; Medicare pays 80% and the patient 20%. Rural amounts apply')
    print('in rural ZIP codes, for items whose fees were adjusted with competitive bidding information.')
    payment_footer(label)


def cmd_payment_drg(a):
    drg = a.code.zfill(3)
    today = date.today()
    fy = today.year + 1 if today.month >= 10 else today.year
    t5 = t1 = None
    for year in (fy, fy - 1):
        t5 = fetch_file('fy%d-ipps-fr-table-5.zip' % year)
        t1 = fetch_file('fy%d-ipps-fr-table-1a-1e.zip' % year)
        if t5 and t1:
            fy = year
            break
    if not (t5 and t1):
        sys.exit('Could not find the inpatient final rule tables on cms.gov.')
    _, text = zip_text(t5, r'Table 5.*\.txt$')
    weight = row = None
    head = None
    for line in text.splitlines():
        cells = [c.strip().strip('"') for c in line.split('\t')]
        if cells and cells[0].upper().startswith('MS-DRG'):
            head = cells
            continue
        if head and cells and cells[0].zfill(3) == drg:
            row = dict(zip(head, cells))
            break
    if not row:
        sys.exit('MS-DRG %s is not in the FY %d table 5.' % (drg, fy))
    wkey = next((k for k in row if 'cap' in k.lower() and 'weight' in k.lower()), None) or \
        next(k for k in row if 'weight' in k.lower())
    weight = num(row[wkey])
    _, t1text = zip_text(t1, r'Tables? 1A.*\.txt$')
    lines = t1text.splitlines()
    op = cap = None
    for i, line in enumerate(lines):
        if 'TABLE 1B' in line.upper() and op is None:
            for nxt in lines[i + 1:i + 6]:
                amts = re.findall(r'\$[\d,]+\.\d\d', nxt)
                if len(amts) >= 2:
                    op = num(amts[0]) + num(amts[1])
                    break
        if 'TABLE 1D' in line.upper() and cap is None:
            for nxt in lines[i + 1:i + 5]:
                amts = re.findall(r'\$[\d,]+\.\d\d', nxt)
                if amts:
                    cap = num(amts[0])
                    break
    if op is None or cap is None:
        sys.exit('Could not read the standardized amounts from table 1.')
    los = next((row[k] for k in row if 'geometric' in k.lower()), '?')
    print('\nMS-DRG %s — %s' % (drg, row.get('MS-DRG Title', '?')))
    print('  Relative weight (FY %d): %.4f. Geometric mean length of stay: %s days.' % (fy, weight, los))
    print('  National standardized amount: operating %s + capital %s = %s per unit of weight.' % (
        money(op), money(cap), money(op + cap)))
    print('  National payment for the stay: about %s.' % money(weight * (op + cap)))
    print('\nPaid to the hospital for the whole stay, whatever devices it uses. Each hospital\'s payment is')
    print('adjusted by its wage index (the labor share of the operating amount), and may add teaching,')
    print('safety-net, outlier and new technology add-on payments. The operating amount is for a hospital')
    print('that reports quality data and is a meaningful EHR user, at a wage index of 1.')
    payment_footer('Inpatient prospective payment system, FY %d final rule, tables 5 and 1A-1E' % fy)


def cmd_payment_pfs(a):
    code = a.code.upper()
    path = saved_file('pfs', a.file)
    name, text = zip_text(path, r'^PPRRVU.*nonQPP.*\.csv$')
    if not text:
        name, text = zip_text(path, r'^PPRRVU.*\.csv$')
    if not text:
        sys.exit('That zip has no PPRRVU relative value CSV. Is it the physician fee schedule RVU file?')
    rows = list(csv.reader(io.StringIO(text)))
    head = next(i for i, r in enumerate(rows) if r and r[0].strip().upper() == 'HCPCS')
    hits = [r for r in rows[head + 1:] if r and r[0].strip().upper() == code]
    _, gtext = zip_text(path, r'^GPCI.*\.csv$')
    gpci = []
    if gtext:
        for r in csv.reader(io.StringIO(gtext)):
            if len(r) >= 7 and re.match(r'^\d{2}$', r[2].strip()):
                pw, pe, mp = num(r[4]), num(r[5]), num(r[6])
                if None not in (pw, pe, mp):
                    gpci.append(('%s %s' % (r[1].strip(), r[3].strip().rstrip('*')), pw, pe, mp))
    print('\n%s in the physician fee schedule (%s): %d row%s. Description not shown: CPT descriptions'
          % (code, os.path.basename(name), len(hits), '' if len(hits) == 1 else 's'))
    print('are the AMA\'s; the user reads them under their own license.')
    status = {'A': 'active, paid under the fee schedule', 'B': 'bundled into another service, not paid separately',
              'C': 'priced by the contractor', 'I': 'not valid for Medicare', 'N': 'not covered by Medicare',
              'R': 'restricted coverage', 'T': 'paid only when no other service is billed', 'X': 'excluded by statute',
              'E': 'excluded from the fee schedule by regulation', 'J': 'anesthesia service', 'M': 'measurement code, no payment',
              'P': 'bundled or excluded'}
    for r in hits:
        mod, st = r[1].strip(), r[3].strip()
        work, pe_nf, pe_f, mp = num(r[5]), num(r[6]), num(r[8]), num(r[10])
        tot_nf, tot_f, cf = num(r[11]), num(r[12]), num(r[25])
        print('\n  %s%s — status %s: %s' % (code, (' modifier ' + mod) if mod else '', st, status.get(st, '?')))
        if not cf or st not in ('A', 'R', 'T'):
            continue
        days = r[14].strip()
        print('    Conversion factor $%.4f. Global period: %s.' % (
            cf, days + ' days' if days.isdigit() else days + ' (none, or not applicable)'))
        for label, pe, tot, na in (('In an office (non-facility)', pe_nf, tot_nf, r[7].strip()),
                                   ('In a facility', pe_f, tot_f, r[9].strip())):
            if not tot or na == 'NA':
                print('    %s: not paid in this setting.' % label)
                continue
            line = '    %s: national %s (%.2f RVUs)' % (label, money(tot * cf), tot)
            if gpci and None not in (work, pe, mp):
                local = sorted((cf * (work * g[1] + pe * g[2] + mp * g[3]), g[0]) for g in gpci)
                line += '; localities from %s (%s) to %s (%s)' % (money(local[0][0]), local[0][1],
                                                                money(local[-1][0]), local[-1][1])
            print(line)
    print('\nIn a facility the hospital or surgery center is paid separately for its part (`payment opps` or')
    print('`payment asc`); the physician\'s facility amount covers the professional service only.')
    print('\nCPT® is a registered trademark of the American Medical Association. CPT codes are cited by number only.')
    payment_footer('Physician fee schedule relative value file, %s' % os.path.basename(path))


def csv_rows(path, pattern):
    name, text = zip_text(path, pattern)
    if not text:
        return name, []
    return name, list(csv.reader(io.StringIO(text.lstrip('﻿').replace('\x00', ''))))


def find_row(rows, code, header_first):
    """The header row (its first cell starts with header_first) and the row for one code, as a dict."""
    head = next((i for i, r in enumerate(rows) if r and r[0].strip().lower().startswith(header_first)), None)
    if head is None:
        return None
    cols = [c.strip() for c in rows[head]]
    for r in rows[head + 1:]:
        if r and r[0].strip().upper() == code:
            return {cols[i]: r[i].strip() for i in range(min(len(cols), len(r))) if cols[i]}
    return {}


def col(row, *words):
    """The value of the first column whose name holds every word."""
    for k, v in row.items():
        if all(w.lower() in k.lower() for w in words):
            return v
    return ''


def exact(row, name):
    """The value of the column with exactly this name, ignoring case."""
    return next((v for k, v in (row or {}).items() if k.lower() == name), '')


def device_offset(opps_zip, code):
    _, rows = csv_rows(opps_zip, r'Addendum P.*Offsets.*\.csv$')
    off = find_row(rows, code, 'hcpcs') if rows else None
    _, rows = csv_rows(opps_zip, r'Addendum P.*Device Intensive.*\.csv$')
    di = find_row(rows, code, 'hcpcs') if rows else None
    return off, bool(di)


def cmd_payment_opps(a):
    code = a.code.upper()
    path = saved_file('opps', a.file)
    name, rows = csv_rows(path, r'Addendum B.*\.csv$')
    row = find_row(rows, code, 'hcpcs')
    si_words = {'J1': 'comprehensive APC: one payment for the whole encounter', 'J2': 'comprehensive APC, observation',
                'T': 'procedure, paid separately; a lower-paid second procedure is discounted',
                'S': 'procedure, paid separately, not discounted', 'V': 'clinic or emergency visit',
                'X': 'ancillary service', 'Q1': 'packaged unless billed alone', 'Q2': 'packaged unless billed alone',
                'Q4': 'conditionally packaged laboratory test', 'N': 'packaged: no separate payment',
                'H': 'pass-through device: paid at cost', 'K': 'drug or biological, paid separately',
                'G': 'pass-through drug or biological', 'C': 'inpatient only: not paid in outpatient',
                'E1': 'not paid by Medicare', 'E2': 'not paid by Medicare outpatient', 'B': 'not paid under OPPS',
                'A': 'paid under another fee schedule', 'M': 'not paid to hospitals', 'P': 'partial hospitalization',
                'U': 'brachytherapy source', 'R': 'blood product'}
    print('\n%s in the OPPS final rule Addendum B (%s). Description not shown: CPT descriptions are the' % (
        code, os.path.basename(name)))
    print('AMA\'s; the user reads them under their own license.')
    if not row:
        print('\n  Not listed. The code may be new, packaged under another code, or not an outpatient code.')
    else:
        si = col(row, 'si')
        print('\n  Status indicator %s: %s' % (si, si_words.get(si, 'see Addendum D1')))
        apc, rate = col(row, 'apc'), num(col(row, 'payment rate'))
        if apc:
            print('  APC %s, relative weight %s.' % (apc, col(row, 'relative weight') or '?'))
        if rate:
            copay = col(row, 'national unadjusted copayment').strip('. ')
            print('  National payment to the hospital: %s. National unadjusted patient copayment: %s.' % (
                money(rate), copay or 'none listed'))
        else:
            print('  No separate payment listed for this code.')
        pt = col(row, 'pass-through')
        if pt:
            print('  Pass-through expiration: %s' % pt)
        off, intensive = device_offset(path, code)
        if off and num(exact(off, 'device offset percentage')):
            print('  Device offset: %s of the payment, %s, is what CMS attributes to device cost%s.' % (
                exact(off, 'device offset percentage'), exact(off, 'device offset amount') or '?',
                '. The procedure is device-intensive' if intensive else ''))
        else:
            print('  Device offset: none published for this code.')
    print('\nCMS\'s device offset is its estimate of device cost within the payment, from hospitals\' claims and')
    print('cost reports. It is not what a device maker is paid. Payment is adjusted for each hospital\'s wage')
    print('index. These are the final rule\'s rates for the year; CMS\'s quarterly Addendum B updates may change')
    print('a code.')
    print('\nCPT® is a registered trademark of the American Medical Association. CPT codes are cited by number only.')
    payment_footer('OPPS final rule addenda B and P, %s' % os.path.basename(path))


def cmd_payment_asc(a):
    code = a.code.upper()
    path = saved_file('asc', a.file)
    name, rows = csv_rows(path, r'ASC.?AA.*\.csv$')
    row = find_row(rows, code, 'hcpcs')
    pi_words = {'A2': 'surgical procedure, paid under the ASC rate', 'G2': 'surgical procedure, paid under the ASC rate',
                'J8': 'device-intensive procedure: the device portion is paid in full',
                'P2': 'office-based procedure, paid at the lower of the ASC or physician office rate',
                'P3': 'office-based procedure, paid at the physician fee schedule rate',
                'R2': 'office-based procedure, paid at the lower rate', 'N1': 'packaged: no separate payment',
                'H8': 'device-intensive procedure with a pass-through device', 'J7': 'pass-through device',
                'K2': 'drug or biological, paid separately', 'Z2': 'radiology, paid at the lower rate',
                'Z3': 'radiology, paid at the physician fee schedule rate', 'L1': 'influenza vaccine',
                'L6': 'new technology intraocular lens', 'F4': 'corneal tissue, paid at cost'}
    print('\n%s in the ASC Addendum AA (%s). Description not shown: CPT descriptions are the AMA\'s.' % (
        code, os.path.basename(name)))
    if not row:
        print('\n  Not on the list of surgical procedures Medicare pays an ASC for. It may be paid only in a')
        print('  hospital, or listed in Addendum BB as an ancillary service.')
    else:
        pi = col(row, 'payment indicator')
        rate = num(col(row, 'payment rate'))
        print('\n  Payment indicator %s: %s' % (pi, pi_words.get(pi, 'see Addendum DD1')))
        print('  National payment to the center: %s.' % (money(rate) if rate else 'no separate payment'))
        opps = saved_file('opps', None, required=False)
        if opps and rate:
            off, intensive = device_offset(opps, code)
            pct = num(exact(off, 'device offset percentage').rstrip('%')) if off else None
            if pct:
                print('  Device portion: %.2f%% (the OPPS device offset) of the ASC rate, about %s.' % (
                    pct, money(rate * pct / 100)))
        elif rate:
            print('  Device portion: save the OPPS final rule addenda too, to see CMS\'s device offset.')
    print('\nAdjusted for each center\'s wage index. A second procedure the same day is discounted where the')
    print('code is subject to multiple procedure discounting.')
    print('\nCPT® is a registered trademark of the American Medical Association. CPT codes are cited by number only.')
    payment_footer('ASC payment rates, %s' % os.path.basename(path))


def cmd_payment(a):
    {'dme': cmd_payment_dme, 'drg': cmd_payment_drg, 'pfs': cmd_payment_pfs,
     'opps': cmd_payment_opps, 'asc': cmd_payment_asc}[a.system](a)


def main(argv=None):
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    p = argparse.ArgumentParser(prog='cms', description='Medicare coverage policies and public billing codes for MOS skills.')
    p.add_argument('--version', action='version', version='cms ' + VERSION)
    sub = p.add_subparsers(dest='cmd', required=True)
    sub.add_parser('check')
    s = sub.add_parser('coverage')
    s.add_argument('terms', nargs='+')
    s.add_argument('--any', action='store_true')
    s.add_argument('--type', choices=['ncd', 'lcd', 'article', 'all'], default='all')
    s.add_argument('--limit', type=int, default=25)
    s = sub.add_parser('ncd')
    s.add_argument('number')
    s.add_argument('--version')
    s = sub.add_parser('lcd')
    s.add_argument('number')
    for name in ('hcpcs', 'icd10'):
        s = sub.add_parser(name)
        s.add_argument('terms', nargs='+')
        s.add_argument('--limit', type=int, default=15)
    s = sub.add_parser('payment')
    s.add_argument('system', choices=['dme', 'drg', 'pfs', 'opps', 'asc'])
    s.add_argument('code')
    s.add_argument('--file', help='a CMS payment file you downloaded (pfs, opps, asc)')
    a = p.parse_args(argv)
    {'check': cmd_check, 'coverage': cmd_coverage, 'ncd': cmd_ncd, 'lcd': cmd_lcd,
     'hcpcs': cmd_hcpcs, 'icd10': cmd_icd10, 'payment': cmd_payment}[a.cmd](a)


if __name__ == '__main__':
    main()
