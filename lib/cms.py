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

Nothing else. No file is read and no company text is sent. Every command
prints the exact URL it ran, so a skill can show the user what went and log it.

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

CPT codes — the codes for procedures physicians bill — are the American
Medical Association's copyright. This script does not search them. A skill may
cite a CPT code number the user gives it, never the code's description.

Medicare coverage policies change. Every result carries the date it was read;
the policy's own page is the authority.
"""

import argparse
import html
import json
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import date

VERSION = '0.1.0'  # a shared contract: a change in behaviour is a new MOS release

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
    t = title.lower()
    hits = [term.lower() in t for term in terms]
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
    a = p.parse_args(argv)
    {'check': cmd_check, 'coverage': cmd_coverage, 'ncd': cmd_ncd, 'lcd': cmd_lcd,
     'hcpcs': cmd_hcpcs, 'icd10': cmd_icd10}[a.cmd](a)


if __name__ == '__main__':
    main()
