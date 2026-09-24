# Clinical cost bands

*v0.1, 2026-09-24. Used by `indications-strategy`, and by any later skill that estimates
clinical studies. Every figure here carries its source. A change to this file is checked against
every skill that uses it before it ships.*

The numbers a MOS skill uses to put a time and a price on a clinical study. They are planning
figures: good enough to tell a $2 million study from a $20 million one, and to show where a
scenario's money goes. They are not a budget. A company with a quote from a contract research
organization, or its own history, uses that instead, and the skill records that it did.

**How a skill uses this file.**

- **Cite the row.** Every cost or duration a skill writes names the line here it came from, or
  says the user supplied it.
- **Do the arithmetic in `lib/studies.py`**, never by hand: `budget`, `timeline` and `scenario`
  take these figures as inputs and print every step.
- **Say what is missing.** Where this file has no figure — see the last section — the skill says
  so and asks, rather than filling the gap with an estimate of its own.

## Inflation

Figures are adjusted to 2025 dollars with the Consumer Price Index for All Urban Consumers
(CPI-U), US city average, all items, annual averages (BLS).

| Year | CPI-U | Factor to 2025 |
|---|---|---|
| 2010 | 218.056 | 1.4764 |
| 2018 | 251.107 | 1.2821 |
| 2025 | 321.943 | 1.0000 |

The all-items index understates how fast clinical trial costs have risen; medical care prices and
trial complexity have both outpaced it. Treat the adjusted figures as a floor.

## Per-patient cost of a study

All-in: each figure covers investigator grants, site overhead and the sponsor's monitoring, so
**site and monitoring costs are not added on top of it.** Source: ASPE / Eastern Research Group
(2022), Table 4 and Table 3, from Medidata data for the "Devices and Diagnostics" therapeutic
area. ERG used Phase 1 costs for feasibility studies, and the average of Phase 2 and Phase 3 for
pivotal studies.

| Study | 2018 dollars | 2025 dollars | Range, 2025 dollars |
|---|---|---|---|
| Feasibility (first-in-human, pilot) | $34,059 | $43,667 | Point estimate only |
| Pivotal | $54,332 | $69,659 | $51,117 (Phase 3 figure) to $88,199 (Phase 2 figure) |
| Post-approval | $14,416 | $18,483 | Point estimate only |

**Limits.** The data behind these figures is from 2012, and it describes complex therapeutic
devices on the PMA path. No public source gives per-patient costs for the simpler studies that
support a 510(k) or De Novo; they are usually cheaper per patient, with shorter follow-up and
fewer visits. Where a skill uses the pivotal band for a simpler study, it says so, and names the
lower end as the more likely.

## Size and length of studies, for PMA devices

Averages across PMA approvals, January 2013 to September 2018. Source: ASPE / ERG (2022), Table 3.

| Measure | Feasibility | Pivotal | Post-approval |
|---|---|---|---|
| Patients enrolled, per PMA | 42 (27.5 per study × 1.53 studies) | 565 (402.5 per study × 1.40 studies) | 414 |
| Months the study runs | 28.0 | 56.9 | 81.2 |
| Out-of-pocket cost, 2025 dollars | $1,831,151 | $39,325,250 | $7,642,820 |

| Interval | Months |
|---|---|
| Start of feasibility to start of pivotal | 37.2 |
| Start of pivotal to PMA submission | 42.4 |
| FDA review of a PMA, submission to decision | 17.4 |

Seventy-nine percent of these PMAs rested on one pivotal study, 13% on two and 8% on three or
more.

For timelines on a specific device, precedent beats these averages: `lib/studies.py trials` gives
the enrollment, site count and length of comparable studies on ClinicalTrials.gov.

## Odds of reaching the next stage

For complex therapeutic devices. Source: ASPE / ERG (2022), Table 3. Used only for the secondary,
risk-adjusted line, never in place of the budget.

| From → to | Chance | Basis |
|---|---|---|
| Non-clinical work → feasibility study | 46.9% | Expert opinion |
| Feasibility study → pivotal study | 48.0% | ClinicalTrials.gov sample |
| Pivotal study → submission to FDA | 75.7% | ClinicalTrials.gov sample |
| FDA review → approval | 80.5% | FDA data |

The chance of reaching a later stage is the product of the steps before it: from the start of a
feasibility study, the chance of reaching a PMA submission is 48.0% × 75.7% = 36.3%. `studies.py
scenario` takes each stage's chance with its cost.

## FDA fees and review times

**User fees**, from FDA's MDUFA fee page. A small business — gross receipts of $100 million or less,
confirmed by FDA's small business determination before the submission — pays the lower fee. Use
the fee for the year the submission will be filed; FY2027 runs from 1 October 2026.

| Submission | FY2026 standard | FY2026 small business | FY2027 standard | FY2027 small business |
|---|---|---|---|---|
| 510(k) | $26,067 | $6,517 | $28,653 | $7,163 |
| De Novo | $173,782 | $43,446 | $191,020 | $47,755 |
| PMA | $579,272 | $144,818 | $636,732 | $159,183 |
| 180-day PMA supplement | $86,891 | $21,723 | $95,510 | $23,878 |
| 513(g) request for classification | $7,820 | $3,910 | $8,596 | $4,298 |
| Annual establishment registration | $11,423 | none | $13,785 | none |

A Pre-Submission meeting carries no fee.

**Review goals** under MDUFA V (fiscal years 2023 to 2027), in **FDA days**: the clock stops
whenever FDA is waiting on the company, so the time a company experiences is longer.

| Submission | FDA's goal |
|---|---|
| 510(k) | Decision within 90 FDA days |
| De Novo | Decision within 150 FDA days |
| PMA, no advisory panel | Decision within 180 FDA days |

The ASPE average of 17.4 months for a PMA review, above, is the experienced figure.

## Whole-program totals, as a check

Survey of more than 200 device companies, Makower and others, Stanford (2010). Self-reported, and
weighted toward venture-backed companies. Used to sanity-check a scenario's total, never as a line
in it.

| Path | Concept to market, 2010 dollars | 2025 dollars | Of which FDA-dependent, 2010 dollars |
|---|---|---|---|
| 510(k) | $31 million | $45.8 million | $24 million |
| PMA | $94 million | $138.8 million | $75 million |

The same survey found that a 510(k) needing a clinical study took an average of 31 months from
first contact with FDA to clearance.

## What lowers a study's cost: Medicare coverage of IDE studies

Medicare may pay for items and services in a study run under an investigational device exemption
(IDE) that CMS has approved. Source: 42 CFR 405.201 to 405.215.

- **Category A** (experimental: whether the device type can be safe and effective is not yet
  known) — Medicare may cover routine care in the study, not the device.
- **Category B** (nonexperimental or investigational: questions of safety and effectiveness for
  the device type are largely resolved) — Medicare may cover the device and routine care.

FDA assigns the category when it approves the IDE; CMS then approves the study for coverage. For a
study whose patients are largely Medicare beneficiaries, this can move a meaningful share of the
per-patient cost off the sponsor. A skill names it where it could apply. It does not
estimate the saving: the share depends on the patients and the procedure.

## What this file does not have

No public source was found for these. A skill asks the user, or says the figure is missing. It
never supplies one of its own.

- **Per-site start-up fees**, contract research organization fees, core laboratory, data safety
  monitoring board and clinical events committee costs, as separate lines. The per-patient
  figures above already include most of them.
- **Per-patient costs for 510(k) and De Novo studies** specifically.
- **Costs outside the US**, for a feasibility study placed abroad.
- **Months for start-up and close-out.** `studies.py timeline` asks for them; the skill gives the
  user's figure or says it is an assumption.

## Sources

1. Eastern Research Group, for the Office of the Assistant Secretary for Planning and Evaluation,
   US Department of Health and Human Services. *Therapeutic Complex Medical Device Development*,
   final report, 14 October 2022.
   https://aspe.hhs.gov/sites/default/files/documents/4d80ac6f010cc681973299f4dee519ca/therapeutic-complex-medical-device-development.pdf
2. US Food and Drug Administration. *Medical Device User Fee Amendments (MDUFA): Fees*. Content
   current as of 30 July 2026. Read 24 September 2026.
   https://www.fda.gov/industry/fda-user-fee-programs/medical-device-user-fee-amendments-mdufa-fees
3. US Food and Drug Administration. *MDUFA Performance Goals and Procedures, Fiscal Years 2023
   Through 2027*. https://www.fda.gov/media/158308/download
4. Makower J, Meer A, Denend L. *FDA Impact on U.S. Medical Technology Innovation: A Survey of
   Over 200 Medical Technology Companies*. November 2010.
   https://biodesign.stanford.edu/content/dam/sm/biodesign/documents/programs/policy-program/01112010_FDA-impact-on-US-medical-technology-innovation_Backgrounder.pdf
5. US Bureau of Labor Statistics. *Consumer Price Index for All Urban Consumers (CPI-U), US city
   average, all items, annual averages*. Read 24 September 2026.
   https://www.bls.gov/regions/northeast/data/consumerpriceindex_us_table.htm
6. 42 CFR Part 405, Subpart B — Medical Services Coverage Decisions That Relate to Health Care
   Technology. https://www.ecfr.gov/current/title-42/chapter-IV/subchapter-B/part-405/subpart-B
