---
name: reimbursement
description: Work out how a medical device would be paid for in the US — whether billing codes exist for it, whether Medicare covers it, and who gets paid under which system in each setting where it is used — and what it would take to close each gap. Use when a team needs to know whether its device can be paid for, find the codes and coverage policies that apply, or understand what payers will want before choosing its indications.
version: 0.1.0
maintainer: Eric Sugalski
phase: [00-concept, 01-definition]
discipline: [commercial]
reads:
  - context/context-map.md
  - context/product/**
  - context/commercial/**
  - context/regulatory/**
  - context/clinical/**
  - context/templates/**
writes:
  - outputs/commercial/
status: draft
---

# Reimbursement

Works out how the device would be paid for, in each setting where it is used, by answering three
questions: **coding** — is there a billing code for the procedure and the device; **coverage** —
will Medicare pay for it, and on what conditions; **payment** — who gets paid, under which
payment system, and whether the device is paid for separately or folded into a fixed payment.
Where there is a gap, it names the route to close it and what that route needs. The output is a
Word document in `outputs/commercial/`, built from the company's template: a draft for review, not
a controlled record.

Read `mos/context-standard.md` before starting if you have not already, then read
`context/context-map.md` to find out what you are allowed to read.

## The thing this skill is actually for

**A device that clears and is not paid for fails as surely as one that does not clear.** FDA
decides whether a device may be sold. Payers decide whether anyone is paid for using it. The two
are separate systems with separate evidence, and founders tend to meet the second after they have
spent their money on the first.

**The buyer is often not the one who gets paid.** A hospital that uses a device during a stay is
usually paid a fixed amount for the stay, whatever the device costs. A more expensive device is
then a cost the hospital absorbs, unless it saves money elsewhere — fewer complications, a shorter
stay. That mismatch sinks devices that work. This skill finds it and says so plainly.

**It comes before the indications are chosen.** Coverage can hinge on the indications: a named
condition may fall under a national coverage policy that a general tool would not; a home setting
moves the device into a different payment system. This skill says which elements of the
indications would change coding, coverage or payment, so `indications-strategy` can weigh them.

**Medicare first.** Medicare's rules are public, and many commercial payers follow them. Commercial
policies vary by payer and are often not public. This skill researches Medicare and names
commercial payers as a question for the team's own advisors.

## Rules for this skill

- **Never send company text outside.** CMS receives only requests for its complete lists of
  coverage policies and the numbers of the national policies read; the lists are searched on this
  machine. Code lookups send generic procedure, device and condition words to the National Library
  of Medicine. Never the company's product name, indications, claims, description or any file's
  contents.
- **Show every query before it runs**, and log every one.
- **CPT codes are the American Medical Association's copyright.** Cite a CPT code by its number,
  never its description, and only a number the user gives or a public source names. Do not look
  up CPT codes. Any document that cites one carries the AMA's copyright notice.
- **Do not accept a license on the user's behalf.** Local coverage policies and billing articles
  are served in full only under the AMA's license. List them with their public page; a person reads
  them. Record what a person reports they say, in plain words.
- **Do not invent a rate, a code or a timeline.** A payment amount comes from the user or a CMS
  source the user has read; a code from a lookup or the user; a timeline only where a public source
  states one. Where none exists, say it is not known.
- **Test what the user brings before relying on it.** "There is already a code for this", "the
  hospital will pay for it", "Medicare covers this": check each against the codes and policies
  found. Where they disagree, say so plainly, give the evidence, and ask the user to reconsider.
  Once they have heard the challenge and confirmed, accept it, and record that it was confirmed
  over the challenge.
- **This is not billing advice.** The skill maps the landscape for planning. How a claim is coded
  and billed is a decision for the company's coding and reimbursement advisors.
- **Do not write into `context/`** without approval of that specific write.
- **Plain words first, the term beside them.**

## Steps

### 1. Establish what context exists

Check for `context/context-map.md`.

- **It exists** — read it. Read, weighing each by the order of trust in the context standard:
  - **The device.** `context/product/device-profile.md`: what it does, the indications as drafted,
    users, use environments, single-use or reusable, commercial intent — especially **who buys**.
  - **The buyers and payers.** The differentiation analysis in `context/commercial/` or,
    unreviewed, `outputs/commercial/`: who decides, who pays, the value proposition for each, the
    competitors and the alternatives.
  - **The regulatory position.** A classification or precedent search in `context/regulatory/` or
    `outputs/regulatory/`: the class and pathway expected, and any Breakthrough Device designation.
  - **Clinical evidence.** Anything in `context/clinical/`. Coverage turns on evidence of benefit.
  - **Earlier work.** Any earlier reimbursement analysis in `context/commercial/` or
    `outputs/commercial/`.

  Read Word documents with `python mos/lib/mosdocx.py read <file>`. Tell the user what you found and
  which of it is unreviewed. List contradictions; do not resolve them.
- **It does not exist** — say so. Say that this skill is stronger after `setup` and
  `differentiation`, which record who buys and who pays. Then offer to continue from the
  conversation.

Anything you need outside the declared paths, ask for by name and say why.

### 2. Check the connections

```
python mos/lib/cms.py check
```

If `python` is not found, use the command `setup` found — `python3` or `py -3`. If CMS or the
National Library of Medicine cannot be reached, write each search as a plain instruction for the
Medicare Coverage Database and the HCPCS lookup, and ask the user to run them; everything after this
step still applies.

### 3. Tell the user what will leave the machine

In one short paragraph: CMS receives requests for its complete lists of coverage policies and the
numbers of national policies read, and nothing about the device, because the lists are searched on
this machine; generic procedure, device and condition words go to the National Library of Medicine
to look up public codes. Nothing else leaves.

### 4. Map where the device is used, and who is paid

Ask, a plain question at a time:

- **Where is it used?** In a hospital stay (**inpatient**); in a hospital without a stay
  (**hospital outpatient**); in an **ambulatory surgery center**; in a **physician's office**; at
  **home**. It can be more than one.
- **Is it used during a procedure, or on its own?** A device used during a procedure is usually paid
  through the procedure. One used on its own may be paid as an item.
- **Is it single-use, or capital equipment the facility buys once?**
- **Is it a diagnostic test?** If it is a laboratory test or an in vitro diagnostic, say that Medicare
  pays for these under the **Clinical Laboratory Fee Schedule**, that new tests often need a
  proprietary laboratory analysis code, and that molecular tests in many regions are reviewed by
  **MolDX**, a Medicare contractor program. Name the route and go no deeper: this version of the
  skill covers procedures and therapeutic devices.
- **How many of its patients are on Medicare?** Roughly: most, some, few. Where few are — a
  pediatric device, say — Medicare's rules matter less, and commercial payers and Medicaid more.

For each setting, record who uses the device, who buys it, and who is paid:

| Setting | Payment system | Who is paid |
|---|---|---|
| Inpatient | Inpatient prospective payment: a fixed payment per stay, by **diagnosis-related group** (MS-DRG) | The hospital, per stay |
| Hospital outpatient | Outpatient prospective payment: a payment per procedure group, by **ambulatory payment classification** (APC) | The hospital, per procedure |
| Ambulatory surgery center | The ASC payment system, related to the outpatient one | The center |
| Physician's office | The **physician fee schedule** | The physician, per service |
| Physician, in any facility | The physician fee schedule, for the professional service | The physician |
| Home | The fee schedule for **durable medical equipment, prosthetics, orthotics and supplies** (DMEPOS), through regional equipment contractors | The supplier |

### 5. Coding: is there a code?

Three kinds of code matter. Look for each, per setting.

- **The procedure.** Physicians bill procedures with **CPT** codes, which the American Medical
  Association owns and licenses. Ask the team which codes clinicians use today for the procedure
  the device is part of. If they do not know, say that a coding advisor or the specialty society
  will, and record the question. Cite any code by number only.
- **The device or supply.** CMS's own **HCPCS Level II** codes cover supplies, equipment and some
  devices; C-codes identify devices in hospital outpatient care, often for pass-through payment:

  ```
  python mos/lib/cms.py hcpcs negative pressure wound
  ```

- **The condition.** Coverage policies list the diagnoses they cover by **ICD-10-CM** code:

  ```
  python mos/lib/cms.py icd10 venous leg ulcer
  ```

For each, record one of: **An existing code fits** — it describes this procedure or device as it
is; **A code exists but fits badly** — it describes something close, and using it risks a denied
or wrong claim; **No code**. A code that fits badly is a finding, not an answer.

### 6. Coverage: will Medicare pay for it?

Search the coverage policies with generic words for the procedure, the condition and the device
type:

```
python mos/lib/cms.py coverage wound therapy
python mos/lib/cms.py coverage ulcer --type ncd
python mos/lib/cms.py ncd 217
python mos/lib/cms.py lcd L35125
```

- **National coverage determinations** (NCDs) apply across Medicare. Read each relevant one in
  full with `ncd`, and record, in plain words, who it covers, under what conditions, and any
  evidence it demands — including **coverage with evidence development**, where Medicare pays only
  for patients in a study or registry.
- **Local coverage determinations** (LCDs), and their billing articles, apply only in the regions of
  the Medicare contractor that wrote them. List the relevant ones with their contractor and page.
  Their text is under the AMA's license: ask the user to read the most relevant, and record what
  they report.

For each setting, record one of: **Covered nationally**; **Covered locally**, in some regions;
**A policy limits or denies coverage**; **No policy** — the contractor decides claim by claim
whether it is reasonable and necessary. No policy is not the same as covered.

**Commercial payers**: name the largest likely ones as a question for the team's advisors. Do not
research their policies.

### 7. Payment: who is paid, and is the device paid for?

For each setting, say:

- **The payment system** from step 4, and the likely code or group the procedure falls in, where
  step 5 found one.
- **Whether the device is paid separately or bundled.** In inpatient, hospital outpatient and
  surgery-center care, the device is usually folded into the facility's fixed payment. In a
  physician's office, a supply may be folded into the physician's payment. At home, equipment is
  usually paid as an item.
- **The payment amount**, only where the user supplies it or has read it from a CMS source. The
  skill does not look up or compute rates.
- **Who pays and who benefits.** Where the device is bundled into a fixed payment, say plainly that
  its price comes out of the facility's margin, and name the economic case the buyer will need:
  what the device saves elsewhere, such as complications, length of stay, readmissions or staff
  time. The case itself belongs in `differentiation`. This skill builds no economic model.

### 8. Where it stands today

For each setting, summarize the position in the terms `indications-strategy` scores by:

| Position | When |
|---|---|
| **Strong** | An existing code fits, it is covered, and it is paid adequately — adequacy only where a rate is known |
| **Partial** | A code exists but coverage is uncertain, or the device is bundled into a fixed payment |
| **Weak** | A new code and coverage are both needed |

Say where adequacy is unknown because no rate was supplied.

### 9. Name the routes to close each gap

For each gap, name the route, what it needs, and what is known about timing — only what a public
source states. The routes:

| Gap | Route | What it needs |
|---|---|---|
| No procedure code | **Category III CPT code**, a temporary code for an emerging technology, then **Category I** | An application to the AMA's CPT panel, usually with a specialty society. Category I needs FDA clearance or approval where required, use by many physicians across the country, and clinical efficacy documented in the peer-reviewed literature — which usually means years after launch |
| No device or supply code | A **HCPCS Level II** code | An application to CMS, on its published cycle |
| Bundled in hospital outpatient payment | **Transitional pass-through payment**, a separate payment for a new device for a limited period | A new device whose cost is not insignificant relative to the payment, and evidence of **substantial clinical improvement** over existing treatment — or, for a Breakthrough Device, an alternative route without that test |
| Bundled in inpatient payment | **New technology add-on payment**, an extra payment on top of the stay's fixed payment, for a limited period | A new technology, cost above a threshold, and substantial clinical improvement — or, for a Breakthrough Device, an alternative route |
| No coverage, for a Breakthrough Device | **Transitional Coverage for Emerging Technologies** (TCET) | A Breakthrough Device within a Medicare benefit category and not already under a national coverage determination. CMS expects to accept about five a year, and aims to finalize a national coverage decision within six months of FDA authorization |
| No coverage, otherwise | A request for a **national coverage determination**, or a request to the regional contractors for **local coverage** | Published clinical evidence that the device is reasonable and necessary for Medicare patients |
| Coverage only in a study | **Coverage with evidence development** | Enrollment in the study or registry CMS names |

**Substantial clinical improvement** is a clinical evidence question. Where a route needs it, say
so: it is evidence `indications-strategy` must plan for, and it may need the version of the
indications that carries a clinical benefit.

### 10. Say what the indications would change

For each element of the indications statement — condition, benefit, patients, body site, setting,
role, user — say whether moving it would change coding, coverage or payment, and how:

- naming a **condition** covered or limited by a national or local policy;
- a **patient group** mostly on, or mostly off, Medicare;
- a **setting** that moves the device into another payment system — home care into DMEPOS;
- a **benefit** strong enough to be the substantial clinical improvement that pass-through or
  add-on payment needs;
- **Breakthrough Device designation**, which opens TCET and the alternative routes, and depends on
  what the indications claim.

`indications-strategy` reads this table to score each version's reimbursement.

### 11. Write the questions for advisors and for CMS

The questions the team should take to a reimbursement or coding advisor — the CPT codes in use,
commercial payers' policies — and any to CMS or the Medicare contractors, such as whether a
policy applies. Phrase each so it could be answered plainly.

### 12. Write the draft

Fill `templates/reimbursement.md`. Write dates in the Date format from
`context/templates/document-settings.md`, if it exists. The search log lists every query in order.
Show the user the complete content. Confirm.

Save the filled template to `outputs/commercial/reimbursement.source.md` and run:

```
python mos/lib/mosdocx.py render --in outputs/commercial/reimbursement.source.md --out outputs/commercial/reimbursement_draft.docx --title "Reimbursement — <device>" --remove-input
```

If `reimbursement_draft.docx` already exists, the script refuses to overwrite it. Show what changed
and ask; add `--force` only on a yes. If the script cannot run, write the filled template to
`outputs/commercial/reimbursement.md` instead, and say that Word output needs the step in `setup`.

Tell the user how the draft becomes the record: review and redline it in Word, save it with the
revision in its name — `reimbursement_revA.docx` — in `context/commercial/`, or in their quality
system with the context map pointing at it, then delete the draft from `outputs/commercial/`. Until
then, `indications-strategy` reads the draft and says it is unreviewed.

## Working at three levels of context

| What the company has | How this skill behaves |
|---|---|
| Nothing | Says it is stronger after `setup` and `differentiation`. Asks what the device does, where it is used, who buys it and how many patients are on Medicare. Explains each idea as it comes — a code, coverage, a payment system, a bundled payment. Every line resting on the conversation says so |
| Some files | Starts from the device profile and the differentiation analysis; says which are unreviewed; interviews only for the settings and payers they leave out |
| A full document set | Traces each setting to the device profile, each payer to the differentiation analysis, each coverage condition to clinical evidence on file. Flags contradictions — a buyer who will absorb a bundled cost the value proposition does not address, a claim of coverage no policy supports — rather than resolving them |

## Interviewing style

- One question at a time.
- Ask where the device is used before anything else. Every answer after depends on the setting.
- When the team says a code or coverage already exists, ask where they heard it: a competitor, a
  consultant, a clinician. Then check it.
- Say plainly when the news is bad. A bundled device with no economic case is a finding the team
  needs early.

## Boundaries

This skill does not give billing or coding advice, research commercial payers' policies, look up
CPT codes, compute or look up payment rates, build an economic model, file any application, or go
deep on laboratory tests and in vitro diagnostics. It reads Medicare's public coverage database and
public code tables; it does not know what any payer decided privately.

## Where this skill is weakest

Recorded so it gets fixed rather than rediscovered:

- It cannot search CPT codes, which are licensed, so the procedure codes depend on the team or its
  advisors.
- It does not read local coverage policies in full, because their text is licensed; a person reads
  them, and what they report is only as good as that reading.
- It does not look up payment rates, so whether a payment is adequate is often unknown.
- Commercial payers are named, not researched. For a device whose patients are mostly not on
  Medicare, the analysis is thin.
- Searching coverage policy titles misses a policy whose title does not name the procedure or the
  condition. Try more than one set of words.
