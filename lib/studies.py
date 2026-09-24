#!/usr/bin/env python3
"""studies — clinical study arithmetic and ClinicalTrials.gov, for MOS skills.

The clinical planning skills (indications-strategy, for now) do every sample
size, timeline and budget calculation through this script, and send every
query to ClinicalTrials.gov through it, so the numbers come out the same
whichever AI runs them. It needs Python 3.8 or later and nothing else.

What leaves the machine: the search terms given to `trials`, and the NCT
numbers given to `trial`, sent to clinicaltrials.gov, run by the US National
Library of Medicine. Nothing else. The arithmetic commands send nothing. No
file is read and no company text is sent. Every query prints the exact URL it
ran, so a skill can show the user what went and log it in the deliverable.

Commands:

  check
      Confirm ClinicalTrials.gov can be reached, and report the date its data
      was last refreshed. Sends one query.

  trials [--condition TEXT] [--intervention TEXT] [--term TEXT]
         [--status completed|any] [--randomized] [--since YEAR] [--limit N]
      Interventional device studies matching the search, with enrollment,
      sites, dates, design and primary outcome, and the patients enrolled per
      site per month worked out for each. Medians across the list close the
      output. Completed studies only unless --status any.

  trial NCT [NCT ...]
      The design of each study in full: arms, primary and secondary outcomes
      with their time frames, eligibility, sites by country. Ten at most per
      call, one second apart.

  size two-proportions --p1 P --p2 P [--alpha A] [--power B] [--one-sided]
                       [--ratio R] [--dropout D]
      Patients for a comparison of two success or event rates: device against
      control. Two-sided alpha 0.05 and power 0.80 unless given.

  size non-inferiority --p-device P --p-control P --margin M
                       [--alpha A] [--power B] [--ratio R] [--dropout D]
      Patients to show the device's success rate is no worse than control's by
      more than the margin. One-sided alpha 0.025 unless given.

  size performance-goal --p P --goal G [--alpha A] [--power B] [--dropout D]
      Patients for a single-arm study tested against a fixed goal, such as a
      performance goal FDA has accepted for the device type. One-sided alpha
      0.05 unless given. Prints the normal approximation and the exact
      binomial answer; use the exact one.

  size two-means --difference D --sd S [--alpha A] [--power B] [--one-sided]
                 [--ratio R] [--dropout D]
      Patients to detect a difference in a continuous measure, such as
      procedure time, between two groups.

  size safety --max-rate R [--events K] [--confidence C] [--dropout D]
      Patients needed so that, if the study sees K or fewer adverse events
      (none unless given), it can say with the confidence asked for that the
      true rate is below R. The sizing a safety question needs when there is no
      effectiveness claim to size for. Exact binomial (Clopper-Pearson).

  size accuracy --expected P --half-width W [--prevalence Q]
                [--confidence C] [--dropout D]
      Cases to estimate a sensitivity or specificity to within plus or minus
      W. With --prevalence, the patients to screen to find those cases.

  timeline --patients N --sites S --rate R --startup M --ramp M
           --followup M --closeout M
      Months from study start-up to final report. Rate is patients per site
      per month. Sites are assumed to open evenly across the ramp.

  budget --patients N --per-patient LOW [HIGH] [--sites S --per-site LOW [HIGH]]
         [--fixed LABEL=LOW[:HIGH] ...] [--reach P]
      One study's cost, line by line, low and high. --reach is the chance of
      getting as far as this study; it adds a risk-adjusted line.

  scenario --stage "NAME; cost=LOW:HIGH; months=LOW:HIGH; reach=P" [--stage ...]
      Adds the stages of one scenario in sequence — studies, FDA review, fees,
      anything costed or timed — for its total cost and months to market, and,
      where a stage carries a chance of being reached, the risk-adjusted cost.
      Every part after the name is optional; a single number means low = high.

Every calculation prints its method, every input and every intermediate
figure, so a reader can check it by hand. The formulas are the standard normal
approximations (Chow, Shao, Wang and Lokhnygina, Sample Size Calculations in
Clinical Research, 3rd ed., 2017); the exact single-arm test is the binomial;
the diagnostic sample size follows Buderer (Academic Emergency Medicine,
1996). They size a plan. They do not replace a statistician on a protocol.

ClinicalTrials.gov's terms apply to everything `trials` and `trial` return:
the records are entered by sponsors and not verified. Enrollment and dates are
what the sponsor reported.
"""

import argparse
import json
import math
import statistics
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import date

VERSION = '0.1.0'  # a shared contract: a change in behaviour is a new MOS release

API = 'https://clinicaltrials.gov/api/v2/'
AGENT = 'Mozilla/5.0 (compatible; MOS-studies/%s)' % VERSION
Z = statistics.NormalDist()

FIELDS = ','.join([
    'NCTId', 'BriefTitle', 'OverallStatus', 'StartDate', 'PrimaryCompletionDate',
    'EnrollmentCount', 'EnrollmentType', 'DesignAllocation', 'DesignMasking',
    'DesignPrimaryPurpose', 'LeadSponsorName', 'LocationCountry',
    'PrimaryOutcomeMeasure', 'PrimaryOutcomeTimeFrame',
])


# ---------------------------------------------------------------- network

def get(path, params=None):
    url = API + path
    if params:
        url += '?' + urllib.parse.urlencode(params)
    print('Query: ' + url)
    req = urllib.request.Request(url, headers={'User-Agent': AGENT, 'Accept': 'application/json'})
    for attempt in range(3):
        try:
            with urllib.request.urlopen(req, timeout=60) as r:
                return json.loads(r.read().decode('utf-8'))
        except urllib.error.HTTPError as e:
            if e.code == 429 and attempt < 2:  # about 50 queries a minute per address
                time.sleep(5 * (attempt + 1))
                continue
            if e.code == 404:
                return None
            sys.exit('ClinicalTrials.gov refused the query: HTTP %s' % e.code)
        except urllib.error.URLError as e:
            sys.exit('Could not reach ClinicalTrials.gov: %s' % e.reason)
    sys.exit('ClinicalTrials.gov kept refusing the query. Wait a minute and try again.')


def dig(d, *keys, default=None):
    for k in keys:
        if not isinstance(d, dict) or k not in d:
            return default
        d = d[k]
    return d


def parse_date(s):
    """ClinicalTrials.gov dates are YYYY-MM or YYYY-MM-DD. A month counts from its first day."""
    if not s:
        return None
    parts = s.split('-')
    try:
        return date(int(parts[0]), int(parts[1]) if len(parts) > 1 else 1, int(parts[2]) if len(parts) > 2 else 1)
    except ValueError:
        return None


def months_between(a, b):
    if not a or not b or b <= a:
        return None
    return (b - a).days / 30.44


def cell(v, width=None):
    s = '' if v is None else str(v)
    s = ' '.join(s.split())
    if width and len(s) > width:
        s = s[:width - 1] + '…'
    return s


def table(headers, rows):
    widths = [len(h) for h in headers]
    for r in rows:
        for i, v in enumerate(r):
            widths[i] = max(widths[i], len(v))
    line = lambda r: '  '.join(v.ljust(widths[i]) for i, v in enumerate(r)).rstrip()
    print(line(headers))
    print(line(['-' * w for w in widths]))
    for r in rows:
        print(line(r))


def sites_by_country(locations):
    us = sum(1 for loc in locations if loc.get('country') == 'United States')
    return len(locations), us, len(locations) - us


# ---------------------------------------------------------------- commands: ClinicalTrials.gov

def cmd_check(a):
    v = get('version')
    if not v:
        sys.exit('ClinicalTrials.gov did not answer.')
    print('Reached ClinicalTrials.gov. API %s, data refreshed %s.' % (v.get('apiVersion'), v.get('dataTimestamp')))


def cmd_trials(a):
    if not (a.condition or a.intervention or a.term):
        sys.exit('Give at least one of --condition, --intervention or --term.')
    advanced = ['AREA[InterventionType]DEVICE', 'AREA[StudyType]INTERVENTIONAL']
    if a.randomized:
        advanced.append('AREA[DesignAllocation]RANDOMIZED')
    if a.since:
        advanced.append('AREA[StartDate]RANGE[%d-01-01,MAX]' % a.since)
    params = {'filter.advanced': ' AND '.join(advanced), 'fields': FIELDS,
              'pageSize': min(a.limit, 100), 'countTotal': 'true', 'sort': 'StartDate:desc'}
    if a.condition:
        params['query.cond'] = a.condition
    if a.intervention:
        params['query.intr'] = a.intervention
    if a.term:
        params['query.term'] = a.term
    if a.status == 'completed':
        params['filter.overallStatus'] = 'COMPLETED'
    data = get('studies', params) or {}
    studies = data.get('studies', [])
    print('%s studies match; showing %d, newest start first.\n' % (data.get('totalCount', '?'), len(studies)))
    if not studies:
        return
    rows, outcomes, rates, sizes, spans = [], [], [], [], []
    for s in studies:
        p = s.get('protocolSection', {})
        nct = dig(p, 'identificationModule', 'nctId')
        start = parse_date(dig(p, 'statusModule', 'startDateStruct', 'date'))
        pcd = parse_date(dig(p, 'statusModule', 'primaryCompletionDateStruct', 'date'))
        n = dig(p, 'designModule', 'enrollmentInfo', 'count')
        ntype = dig(p, 'designModule', 'enrollmentInfo', 'type', default='')
        total, us, other = sites_by_country(dig(p, 'contactsLocationsModule', 'locations', default=[]))
        span = months_between(start, pcd)
        rate = None
        if n and total and span and ntype == 'ACTUAL':
            rate = n / total / span
            rates.append(rate)
            sizes.append(n)
            spans.append(span)
        rows.append([
            nct, cell(dig(p, 'statusModule', 'startDateStruct', 'date')),
            '' if span is None else '%.0f' % span,
            '' if n is None else '%d%s' % (n, '' if ntype == 'ACTUAL' else ' est'),
            '%d (US %d)' % (total, us) if total else '',
            '' if rate is None else '%.2f' % rate,
            cell(dig(p, 'designModule', 'designInfo', 'allocation'), 14),
            cell(dig(p, 'designModule', 'designInfo', 'maskingInfo', 'masking'), 10),
            cell(dig(p, 'sponsorCollaboratorsModule', 'leadSponsor', 'name'), 28),
        ])
        prim = dig(p, 'outcomesModule', 'primaryOutcomes', default=[])
        title = cell(dig(p, 'identificationModule', 'briefTitle'), 90)
        first = prim[0] if prim else {}
        outcomes.append('%s  %s\n    Primary: %s [%s]%s' % (
            nct, title, cell(first.get('measure'), 110), cell(first.get('timeFrame'), 50),
            '  (+%d more)' % (len(prim) - 1) if len(prim) > 1 else ''))
    table(['NCT', 'Start', 'Months', 'Enrolled', 'Sites', 'Pts/site/mo', 'Allocation', 'Masking', 'Sponsor'], rows)
    print('\nMonths runs from start to primary completion, so it includes the follow-up of the')
    print('last patient. Pts/site/mo is enrolled / sites / months: a floor on the true enrollment')
    print('rate, lower the longer the follow-up. Only studies reporting ACTUAL enrollment count.\n')
    for o in outcomes:
        print(o)
    if rates:
        print('\nAcross the %d studies with actual enrollment and dates:' % len(rates))
        print('  Median enrolled:       %.0f  (range %d to %d)' % (statistics.median(sizes), min(sizes), max(sizes)))
        print('  Median months:         %.0f  (range %.0f to %.0f)' % (statistics.median(spans), min(spans), max(spans)))
        print('  Median pts/site/month: %.2f  (range %.2f to %.2f)' % (statistics.median(rates), min(rates), max(rates)))
    print('\nRecords are entered by sponsors and not verified by ClinicalTrials.gov. Read today, %s.' % date.today().isoformat())


def cmd_trial(a):
    if len(a.nct) > 10:
        sys.exit('Ten studies at most per call.')
    for i, nct in enumerate(a.nct):
        if i:
            time.sleep(1)
            print('\n' + '=' * 78 + '\n')
        s = get('studies/' + nct.upper())
        if not s:
            print('%s: not found.' % nct)
            continue
        p = s.get('protocolSection', {})
        design = p.get('designModule', {})
        info = design.get('designInfo', {})
        locs = dig(p, 'contactsLocationsModule', 'locations', default=[])
        total, us, other = sites_by_country(locs)
        start = dig(p, 'statusModule', 'startDateStruct', 'date')
        pcd = dig(p, 'statusModule', 'primaryCompletionDateStruct', 'date')
        span = months_between(parse_date(start), parse_date(pcd))
        n = dig(design, 'enrollmentInfo', 'count')
        print('%s — %s' % (dig(p, 'identificationModule', 'nctId'), cell(dig(p, 'identificationModule', 'briefTitle'))))
        print('Sponsor: %s' % dig(p, 'sponsorCollaboratorsModule', 'leadSponsor', 'name'))
        print('Status: %s   Results posted: %s' % (dig(p, 'statusModule', 'overallStatus'), 'yes' if s.get('hasResults') else 'no'))
        print('Start: %s   Primary completion: %s   Months: %s' % (start, pcd, '' if span is None else '%.0f' % span))
        print('Enrolled: %s (%s)' % (n, dig(design, 'enrollmentInfo', 'type', default='')))
        countries = sorted({loc.get('country') for loc in locs if loc.get('country')})
        print('Sites: %d (US %d, elsewhere %d)%s' % (total, us, other, ('  ' + ', '.join(countries)) if countries else ''))
        if n and total and span:
            print('Enrolled per site per month: %.2f' % (n / total / span))
        print('Design: allocation %s; model %s; masking %s; purpose %s' % (
            info.get('allocation', 'n/a'), info.get('interventionModel', 'n/a'),
            dig(info, 'maskingInfo', 'masking', default='n/a'), info.get('primaryPurpose', 'n/a')))
        for arm in dig(p, 'armsInterventionsModule', 'armGroups', default=[]):
            print('  Arm: %s (%s)' % (cell(arm.get('label'), 70), arm.get('type', '')))
        elig = p.get('eligibilityModule', {})
        print('Eligibility: ages %s to %s; sex %s' % (elig.get('minimumAge', 'any'), elig.get('maximumAge', 'any'), elig.get('sex', 'ALL')))
        for kind, key, cap in (('Primary', 'primaryOutcomes', 10), ('Secondary', 'secondaryOutcomes', 10)):
            items = dig(p, 'outcomesModule', key, default=[])
            for o in items[:cap]:
                print('  %s: %s [%s]' % (kind, cell(o.get('measure'), 120), cell(o.get('timeFrame'), 60)))
            if len(items) > cap:
                print('  ... %d more %s outcomes' % (len(items) - cap, kind.lower()))
    print('\nRecords are entered by sponsors and not verified by ClinicalTrials.gov. Read today, %s.' % date.today().isoformat())


# ---------------------------------------------------------------- commands: arithmetic

def z(p):
    return Z.inv_cdf(p)


def check_rate(name, v, low=0.0, high=1.0):
    if not (low < v < high):
        sys.exit('%s must be between %g and %g, not %g.' % (name, low, high, v))


def with_dropout(n, dropout):
    return math.ceil(n / (1 - dropout)) if dropout else n


def report(method, formula, inputs, steps, per_group, groups, dropout, ratio=1.0):
    print('Method: ' + method)
    print('Formula: ' + formula)
    print('Inputs:')
    for k, v in inputs:
        print('  %-38s %s' % (k, v))
    for k, v in steps:
        print('  %-38s %s' % (k, v))
    if groups == 2:
        n1 = math.ceil(per_group)
        n2 = math.ceil(per_group * ratio)
        print('Result: %d device + %d control = %d evaluable patients' % (n2, n1, n1 + n2) if ratio != 1
              else 'Result: %d per group, %d evaluable patients in total' % (n1, 2 * n1))
        total = n1 + n2
    else:
        total = math.ceil(per_group)
        print('Result: %d evaluable patients' % total)
    if dropout:
        print('Enrol:  %d, allowing %.0f%% lost or unevaluable (evaluable / (1 - %.2f))' % (with_dropout(total, dropout), dropout * 100, dropout))
    print('\nA planning estimate from a standard approximation. The protocol\'s sample size needs a statistician.')


def cmd_two_proportions(a):
    for n, v in (('--p1', a.p1), ('--p2', a.p2)):
        check_rate(n, v)
    if a.p1 == a.p2:
        sys.exit('The two rates are equal: no study can detect a difference of zero.')
    za = z(1 - a.alpha / (1 if a.one_sided else 2))
    zb = z(a.power)
    k = a.ratio
    var = a.p2 * (1 - a.p2) + a.p1 * (1 - a.p1) / k
    n = (za + zb) ** 2 * var / (a.p1 - a.p2) ** 2
    report('two independent proportions, normal approximation',
           'n_control = (z_alpha + z_beta)^2 x [p2(1-p2) + p1(1-p1)/k] / (p1 - p2)^2; n_device = k x n_control',
           [('Device rate p1', a.p1), ('Control rate p2', a.p2), ('Alpha', '%g %s' % (a.alpha, 'one-sided' if a.one_sided else 'two-sided')),
            ('Power', a.power), ('Device:control ratio k', k)],
           [('z_alpha', '%.4f' % za), ('z_beta', '%.4f' % zb), ('n_control (unrounded)', '%.2f' % n)],
           n, 2, a.dropout, k)


def cmd_non_inferiority(a):
    for n, v in (('--p-device', a.p_device), ('--p-control', a.p_control)):
        check_rate(n, v)
    check_rate('--margin', a.margin)
    gap = a.p_device - a.p_control + a.margin
    if gap <= 0:
        sys.exit('The device is expected to be worse than control by the margin or more: non-inferiority cannot be shown.')
    za, zb, k = z(1 - a.alpha), z(a.power), a.ratio
    var = a.p_control * (1 - a.p_control) + a.p_device * (1 - a.p_device) / k
    n = (za + zb) ** 2 * var / gap ** 2
    report('non-inferiority of two proportions (higher is better), normal approximation',
           'n_control = (z_alpha + z_beta)^2 x [pc(1-pc) + pd(1-pd)/k] / (pd - pc + margin)^2',
           [('Device success rate pd', a.p_device), ('Control success rate pc', a.p_control), ('Margin', a.margin),
            ('Alpha', '%g one-sided' % a.alpha), ('Power', a.power), ('Device:control ratio k', k)],
           [('z_alpha', '%.4f' % za), ('z_beta', '%.4f' % zb), ('n_control (unrounded)', '%.2f' % n)],
           n, 2, a.dropout, k)
    print('FDA expects the margin to be justified from earlier evidence of the control\'s effect.')


def log_binom_pmf(k, n, p):
    return math.lgamma(n + 1) - math.lgamma(k + 1) - math.lgamma(n - k + 1) + k * math.log(p) + (n - k) * math.log(1 - p)


def upper_tail(k, n, p):
    """P(X >= k) for X ~ Binomial(n, p)."""
    if k <= 0:
        return 1.0
    if k > n:
        return 0.0
    return min(1.0, sum(math.exp(log_binom_pmf(i, n, p)) for i in range(k, n + 1)))


def exact_single_arm(p, goal, alpha, power, cap=5000):
    """Smallest n where the exact one-sided binomial test of `goal` has the power asked for.

    Works on successes when p > goal, on failures when p < goal, so one routine covers both.
    Power is not monotone in n (the sawtooth), so the n returned is also checked for n+1..n+10.
    """
    if p < goal:
        p, goal = 1 - p, 1 - goal
    for n in range(5, cap + 1):
        k = next((k for k in range(n + 1) if upper_tail(k, n, goal) <= alpha), None)
        if k is None:
            continue
        if upper_tail(k, n, p) >= power:
            steady = all(
                upper_tail(next(kk for kk in range(m + 1) if upper_tail(kk, m, goal) <= alpha), m, p) >= power
                for m in range(n + 1, n + 11))
            return n, k, upper_tail(k, n, p), steady
    return None


def cmd_performance_goal(a):
    check_rate('--p', a.p)
    check_rate('--goal', a.goal)
    if a.p == a.goal:
        sys.exit('The expected rate equals the goal: no study can show it beats it.')
    za, zb = z(1 - a.alpha), z(a.power)
    n = (za * math.sqrt(a.goal * (1 - a.goal)) + zb * math.sqrt(a.p * (1 - a.p))) ** 2 / (a.p - a.goal) ** 2
    better = 'higher' if a.p > a.goal else 'lower'
    report('single arm against a fixed goal (%s is better), normal approximation' % better,
           'n = [z_alpha x sqrt(g(1-g)) + z_beta x sqrt(p(1-p))]^2 / (p - g)^2',
           [('Expected device rate p', a.p), ('Performance goal g', a.goal), ('Alpha', '%g one-sided' % a.alpha), ('Power', a.power)],
           [('z_alpha', '%.4f' % za), ('z_beta', '%.4f' % zb), ('n (unrounded)', '%.2f' % n)],
           n, 1, 0)
    ex = exact_single_arm(a.p, a.goal, a.alpha, a.power)
    print('\nExact binomial test (use this one; the approximation is poor for small studies or rates near 0 or 1):')
    if not ex:
        print('  No n up to 5,000 reaches the power asked for.')
        return
    n_ex, k, pw, steady = ex
    if a.p > a.goal:
        print('  %d evaluable patients. The study meets its goal with %d or more successes.' % (n_ex, k))
    else:
        print('  %d evaluable patients. The study meets its goal with %d or fewer events.' % (n_ex, n_ex - k))
    print('  Power at that size: %.3f' % pw)
    if not steady:
        print('  Power dips below %.2f at some sizes a little above %d (the binomial sawtooth); a statistician picks the final n.' % (a.power, n_ex))
    if a.dropout:
        print('  Enrol: %d, allowing %.0f%% lost or unevaluable' % (with_dropout(n_ex, a.dropout), a.dropout * 100))


def cmd_safety(a):
    check_rate('--max-rate', a.max_rate)
    if a.events < 0:
        sys.exit('--events cannot be negative.')
    tail = 1 - a.confidence
    n = None
    for m in range(max(a.events + 1, 1), 200001):
        # P(X <= K | m, R): if this is at most 1 - confidence, seeing K or fewer events rules R out
        p = sum(math.exp(log_binom_pmf(i, m, a.max_rate)) for i in range(0, a.events + 1))
        if p <= tail:
            n = m
            break
    print('Method: exact binomial (Clopper-Pearson) upper confidence bound on an adverse event rate')
    print('Formula: smallest n with P(X <= K | n, R) <= 1 - confidence')
    print('Inputs:')
    for k, v in (('Rate to rule out R', a.max_rate), ('Events the study may see K', a.events),
                 ('Confidence, one-sided', a.confidence)):
        print('  %-38s %s' % (k, v))
    if n is None:
        sys.exit('No study of up to 200,000 patients rules that rate out.')
    print('Result: %d evaluable patients' % n)
    if a.events == 0:
        print('Check: the rule of three gives about %.0f (3 / R) at 95%% confidence.' % (3 / a.max_rate))
    print('With %d patients and %s, the upper %.0f%% bound on the rate is below %g.' % (
        n, 'no events' if a.events == 0 else '%d or fewer events' % a.events, a.confidence * 100, a.max_rate))
    if a.dropout:
        print('Enrol:  %d, allowing %.0f%% lost or unevaluable' % (with_dropout(n, a.dropout), a.dropout * 100))
    print('\nThis says what the study can show if it sees few events, not how likely it is to see few.')
    print('If the device\'s true rate is near R, the study will usually see more. To size for power')
    print('against an expected rate, use performance-goal with the rate as p and R as the goal.')
    print('\nA planning estimate. The protocol\'s sample size needs a statistician.')


def cmd_two_means(a):
    if a.sd <= 0 or a.difference == 0:
        sys.exit('--sd must be positive and --difference non-zero.')
    za = z(1 - a.alpha / (1 if a.one_sided else 2))
    zb = z(a.power)
    k = a.ratio
    n = (za + zb) ** 2 * a.sd ** 2 * (1 + 1 / k) / a.difference ** 2
    report('two independent means, normal approximation',
           'n_control = (z_alpha + z_beta)^2 x sd^2 x (1 + 1/k) / difference^2; n_device = k x n_control',
           [('Difference to detect', a.difference), ('Standard deviation', a.sd),
            ('Alpha', '%g %s' % (a.alpha, 'one-sided' if a.one_sided else 'two-sided')), ('Power', a.power), ('Device:control ratio k', k)],
           [('z_alpha', '%.4f' % za), ('z_beta', '%.4f' % zb), ('n_control (unrounded)', '%.2f' % n)],
           n, 2, a.dropout, k)


def cmd_accuracy(a):
    check_rate('--expected', a.expected)
    check_rate('--half-width', a.half_width, 0, 0.5)
    zc = z(1 - (1 - a.confidence) / 2)
    n = zc ** 2 * a.expected * (1 - a.expected) / a.half_width ** 2
    report('precision of a sensitivity or specificity (Buderer, 1996), normal approximation',
           'cases = z^2 x p(1-p) / w^2',
           [('Expected sensitivity or specificity p', a.expected), ('Half-width w', a.half_width), ('Confidence', a.confidence)],
           [('z', '%.4f' % zc), ('cases (unrounded)', '%.2f' % n)],
           n, 1, 0)
    cases = math.ceil(n)
    print('For sensitivity these are patients WITH the condition; for specificity, patients without it.')
    if a.prevalence:
        check_rate('--prevalence', a.prevalence)
        print('At prevalence %.3f: screen %d patients to find %d with the condition (for sensitivity),' % (
            a.prevalence, math.ceil(cases / a.prevalence), cases))
        print('                      or %d to find %d without it (for specificity).' % (math.ceil(cases / (1 - a.prevalence)), cases))
    if a.dropout:
        print('Enrol: %d cases, allowing %.0f%% unevaluable' % (with_dropout(cases, a.dropout), a.dropout * 100))


def cmd_timeline(a):
    if min(a.patients, a.sites) <= 0 or a.rate <= 0:
        sys.exit('--patients, --sites and --rate must be positive.')
    full = a.patients / (a.sites * a.rate)       # months at full site count
    enrol = full + a.ramp / 2                    # even opening across the ramp costs half the ramp
    total = a.startup + enrol + a.followup + a.closeout
    print('Method: sites open evenly across the ramp, so enrollment takes patients / (sites x rate) + ramp / 2.')
    print('Inputs:')
    for k, v in (('Patients to enrol', a.patients), ('Sites', a.sites), ('Patients per site per month', a.rate),
                 ('Start-up (to first site open)', '%g months' % a.startup), ('Site ramp', '%g months' % a.ramp),
                 ('Follow-up of last patient', '%g months' % a.followup), ('Close-out and report', '%g months' % a.closeout)):
        print('  %-32s %s' % (k, v))
    print('Months:')
    for k, v in (('Start-up', a.startup), ('Enrollment', enrol), ('Follow-up of last patient', a.followup), ('Close-out and report', a.closeout)):
        print('  %-32s %5.1f' % (k, v))
    print('  %-32s %5.1f   (%.1f years)' % ('Total', total, total / 12))
    if enrol > 36:
        print('\nEnrollment runs past three years. More sites, or a wider population, is usually the lever.')


def pair(vals, name):
    if len(vals) == 1:
        return vals[0], vals[0]
    if len(vals) == 2 and vals[0] <= vals[1]:
        return vals[0], vals[1]
    sys.exit('%s takes LOW or LOW HIGH, low first.' % name)


def money(v):
    return '${:,.0f}'.format(v)


def parse_range(text, name):
    try:
        if ':' in text:
            lo, hi = (float(x) for x in text.split(':'))
        else:
            lo = hi = float(text)
    except ValueError:
        sys.exit('%s: "%s" is not LOW or LOW:HIGH.' % (name, text))
    if lo > hi:
        sys.exit('%s: low is above high.' % name)
    return lo, hi


def cmd_budget(a):
    lines = []
    lo, hi = pair(a.per_patient, '--per-patient')
    lines.append(('Patients: %d x %s' % (a.patients, money(lo) if lo == hi else '%s to %s' % (money(lo), money(hi))), a.patients * lo, a.patients * hi))
    if a.per_site:
        if not a.sites:
            sys.exit('--per-site needs --sites.')
        slo, shi = pair(a.per_site, '--per-site')
        lines.append(('Sites: %d x %s' % (a.sites, money(slo) if slo == shi else '%s to %s' % (money(slo), money(shi))), a.sites * slo, a.sites * shi))
    for f in a.fixed or []:
        if '=' not in f:
            sys.exit('--fixed takes LABEL=LOW or LABEL=LOW:HIGH, not "%s".' % f)
        label, rng = f.split('=', 1)
        flo, fhi = parse_range(rng, '--fixed ' + label)
        lines.append((label, flo, fhi))
    total_lo, total_hi = sum(l[1] for l in lines), sum(l[2] for l in lines)
    w = max(len(l[0]) for l in lines + [('Total', 0, 0)])
    print('%-*s  %15s  %15s' % (w, 'Line', 'Low', 'High'))
    for label, l, h in lines:
        print('%-*s  %15s  %15s' % (w, label, money(l), money(h)))
    print('%-*s  %15s  %15s' % (w, 'Total', money(total_lo), money(total_hi)))
    if a.reach is not None:
        check_rate('--reach', a.reach, 0, 1.0000001)
        print('\nSecondary: risk-adjusted, if the chance of reaching this study is %.0f%%' % (a.reach * 100))
        print('%-*s  %15s  %15s' % (w, 'Total x %.3f' % a.reach, money(total_lo * a.reach), money(total_hi * a.reach)))
        print('This is what the study costs on average across programs like this one, most of which stop')
        print('earlier. It is not a smaller budget: if the study runs, it costs the total above.')
    if a.per_site:
        print('\nCheck the per-patient figure is not already all-in. Per-patient costs from the ASPE report')
        print('include site and monitoring costs; adding site costs on top of them counts them twice.')


def parse_stage(text):
    """NAME; cost=LOW[:HIGH]; months=LOW[:HIGH]; reach=P — every part after the name optional."""
    parts = [x.strip() for x in text.split(';') if x.strip()]
    if not parts or '=' in parts[0]:
        sys.exit('--stage starts with a name: "Pivotal study; cost=15000000:26000000; months=40:52; reach=0.48".')
    stage = {'name': parts[0], 'cost': None, 'months': None, 'reach': None}
    for part in parts[1:]:
        if '=' not in part:
            sys.exit('%s: "%s" is not key=value.' % (stage['name'], part))
        k, v = (x.strip() for x in part.split('=', 1))
        if k in ('cost', 'months'):
            stage[k] = parse_range(v, '%s %s' % (stage['name'], k))
        elif k == 'reach':
            try:
                stage['reach'] = float(v)
            except ValueError:
                sys.exit('%s: reach "%s" is not a number.' % (stage['name'], v))
            check_rate('reach for ' + stage['name'], stage['reach'], 0, 1.0000001)
        else:
            sys.exit('%s: unknown key "%s"; use cost, months or reach.' % (stage['name'], k))
    return stage


def cmd_scenario(a):
    stages = [parse_stage(s) for s in a.stage]
    label_total = 'Total, every stage in sequence'
    w = max(len(s['name']) for s in stages + [{'name': label_total}])
    print('%-*s  %14s  %14s  %7s  %7s  %6s' % (w, 'Stage', 'Cost low', 'Cost high', 'Mo low', 'Mo high', 'Reach'))
    cost_lo = cost_hi = mo_lo = mo_hi = risk_lo = risk_hi = 0.0
    any_reach = False
    for s in stages:
        c = s['cost'] or (0.0, 0.0)
        m = s['months'] or (0.0, 0.0)
        r = 1.0 if s['reach'] is None else s['reach']
        any_reach = any_reach or s['reach'] is not None
        cost_lo += c[0]; cost_hi += c[1]; mo_lo += m[0]; mo_hi += m[1]
        risk_lo += c[0] * r; risk_hi += c[1] * r
        print('%-*s  %14s  %14s  %7s  %7s  %6s' % (
            w, s['name'], money(c[0]) if s['cost'] else '', money(c[1]) if s['cost'] else '',
            '%.1f' % m[0] if s['months'] else '', '%.1f' % m[1] if s['months'] else '',
            '' if s['reach'] is None else '%.0f%%' % (s['reach'] * 100)))
    print('%-*s  %14s  %14s  %7.1f  %7.1f' % (w, label_total, money(cost_lo), money(cost_hi), mo_lo, mo_hi))
    print('\nMonths add as if each stage starts when the one before it ends. A stage that runs alongside')
    print('another should be given without months, and the overlap said in words.')
    if any_reach:
        print('\nSecondary: risk-adjusted cost (each stage x its chance of being reached; none given = certain)')
        print('%-*s  %14s  %14s' % (w, 'Risk-adjusted', money(risk_lo), money(risk_hi)))
        print('An average across programs like this one, most of which stop early. Not a budget.')


# ---------------------------------------------------------------- main

def main(argv=None):
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    p = argparse.ArgumentParser(prog='studies', description='Clinical study arithmetic and ClinicalTrials.gov for MOS skills.')
    p.add_argument('--version', action='version', version='studies ' + VERSION)
    sub = p.add_subparsers(dest='cmd', required=True)

    sub.add_parser('check')

    s = sub.add_parser('trials')
    s.add_argument('--condition')
    s.add_argument('--intervention')
    s.add_argument('--term')
    s.add_argument('--status', choices=['completed', 'any'], default='completed')
    s.add_argument('--randomized', action='store_true')
    s.add_argument('--since', type=int)
    s.add_argument('--limit', type=int, default=20)

    s = sub.add_parser('trial')
    s.add_argument('nct', nargs='+')

    size = sub.add_parser('size').add_subparsers(dest='method', required=True)

    def common(sp, alpha, one_sided_flag=False, ratio=True):
        sp.add_argument('--alpha', type=float, default=alpha)
        sp.add_argument('--power', type=float, default=0.80)
        sp.add_argument('--dropout', type=float, default=0.0)
        if one_sided_flag:
            sp.add_argument('--one-sided', action='store_true')
        if ratio:
            sp.add_argument('--ratio', type=float, default=1.0, help='device patients per control patient')

    s = size.add_parser('two-proportions')
    s.add_argument('--p1', type=float, required=True, help='device rate')
    s.add_argument('--p2', type=float, required=True, help='control rate')
    common(s, 0.05, one_sided_flag=True)

    s = size.add_parser('non-inferiority')
    s.add_argument('--p-device', type=float, required=True)
    s.add_argument('--p-control', type=float, required=True)
    s.add_argument('--margin', type=float, required=True)
    common(s, 0.025)

    s = size.add_parser('performance-goal')
    s.add_argument('--p', type=float, required=True, help='expected device rate')
    s.add_argument('--goal', type=float, required=True)
    common(s, 0.05, ratio=False)

    s = size.add_parser('two-means')
    s.add_argument('--difference', type=float, required=True)
    s.add_argument('--sd', type=float, required=True)
    common(s, 0.05, one_sided_flag=True)

    s = size.add_parser('safety')
    s.add_argument('--max-rate', type=float, required=True)
    s.add_argument('--events', type=int, default=0)
    s.add_argument('--confidence', type=float, default=0.95)
    s.add_argument('--dropout', type=float, default=0.0)

    s = size.add_parser('accuracy')
    s.add_argument('--expected', type=float, required=True)
    s.add_argument('--half-width', type=float, required=True)
    s.add_argument('--prevalence', type=float)
    s.add_argument('--confidence', type=float, default=0.95)
    s.add_argument('--dropout', type=float, default=0.0)

    s = sub.add_parser('timeline')
    s.add_argument('--patients', type=int, required=True)
    s.add_argument('--sites', type=int, required=True)
    s.add_argument('--rate', type=float, required=True, help='patients per site per month')
    for m in ('startup', 'ramp', 'followup', 'closeout'):
        s.add_argument('--' + m, type=float, required=True, help='months')

    s = sub.add_parser('budget')
    s.add_argument('--patients', type=int, required=True)
    s.add_argument('--per-patient', type=float, nargs='+', required=True)
    s.add_argument('--sites', type=int)
    s.add_argument('--per-site', type=float, nargs='+')
    s.add_argument('--fixed', action='append')
    s.add_argument('--reach', type=float)

    s = sub.add_parser('scenario')
    s.add_argument('--stage', action='append', required=True)

    a = p.parse_args(argv)
    for name in ('alpha', 'power', 'confidence'):
        if hasattr(a, name):
            check_rate('--' + name, getattr(a, name))
    if getattr(a, 'dropout', 0):
        check_rate('--dropout', a.dropout)
    if hasattr(a, 'ratio') and a.ratio <= 0:
        sys.exit('--ratio must be positive.')

    if a.cmd == 'size':
        {'two-proportions': cmd_two_proportions, 'non-inferiority': cmd_non_inferiority,
         'performance-goal': cmd_performance_goal, 'two-means': cmd_two_means,
         'safety': cmd_safety, 'accuracy': cmd_accuracy}[a.method](a)
    else:
        {'check': cmd_check, 'trials': cmd_trials, 'trial': cmd_trial, 'timeline': cmd_timeline,
         'budget': cmd_budget, 'scenario': cmd_scenario}[a.cmd](a)


if __name__ == '__main__':
    main()
