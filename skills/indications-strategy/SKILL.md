---
name: indications-strategy
description: Draft three or four versions of a medical device's indications for use statement — from one as close to the predicate as possible, with the fewest clinical studies, to one that carries the claims that set the device apart — and compare what each costs in pathway, clinical evidence, time and money. Use when a team needs to decide what to ask FDA to clear, weigh a 510(k) against a De Novo or PMA, or see what a more compelling indication would cost in clinical studies.
version: 0.1.0
maintainer: Eric Sugalski
phase: [00-concept, 01-definition]
discipline: [regulatory, clinical, commercial]
reads:
  - context/context-map.md
  - context/product/**
  - context/users-and-needs/**
  - context/risk/**
  - context/commercial/**
  - context/regulatory/**
  - context/clinical/**
  - context/templates/**
writes:
  - outputs/regulatory/
  - context/regulatory/indications-strategy.md    # only on the user's approval, after a person has chosen
  - context/product/device-profile.md             # only on the user's approval, to record the chosen indications
status: draft
---

# Indications strategy

Drafts three or four versions of the device's **indications for use** — the statement of which
condition the device treats or diagnoses, in which patients, where on the body and in what setting,
which is what FDA clears — and compares them. At one end is a version as close to the predicate's
indications as possible: the fastest path, with as few clinical studies as the device allows. At the
other is a version that carries the claims that set the device apart, on a harder pathway that
likely needs clinical data. For each version the skill works out the pathway, the evidence FDA will
want, the studies that evidence needs, and their time and cost. The output is a Word document in
`outputs/regulatory/`, built from the company's template: a draft for review, not a controlled
record.

Read `mos/context-standard.md` before starting if you have not already, then read
`context/context-map.md` to find out what you are allowed to read.

## The thing this skill is actually for

**The indications statement is what FDA clears, and the regulated claims live inside it.** A
company may say, in its labeling and its marketing, what its cleared indications support. A claim
about a disease, a patient group or a clinical outcome that the statement does not carry cannot be
made. So the choice of wording is the choice of what the company will be able to say.

**Close to the predicate is fast; far from it is compelling.** An indications statement that tracks
the predicate's closely is the safest route through a 510(k), and it may leave the device with
nothing to say that makes a buyer switch. A statement that names a disease, a patient group or a
benefit the predicate does not can need a De Novo or a PMA and a clinical study that costs more than
everything else in the program. Founders tend to find this out after they have chosen.

**The clinical study is usually the cost driver.** What separates a $2 million path from a $30
million one is almost always the clinical evidence, not the submission. This skill puts a rough
time and price on the studies each version needs, so the trade-off is visible before it is made.

**A narrow statement does not shrink the safety question.** The wording decides what the company
may say; the device's risks and its differences from the predicate decide what it must prove,
whatever it says. A device with a new material, energy source or mechanism of action may need
bench, animal or clinical safety data under the narrowest 510(k). Special controls can require
clinical data outright. So every version's evidence has two sources: what its wording claims, and
the questions the device's risks and technology raise. A version that looks cheap because its
wording is modest, while its technology needs a safety study, is the error this skill most needs to
avoid.

**The skill scores; a person chooses.** Choosing what to ask FDA for turns on money, appetite for
risk and strategy the skill cannot see. Versions are scored on fixed dimensions, unweighted, with no
total. None is labeled the recommendation.

**It is much stronger with context.** It can run from a conversation, but a version built without
`setup`'s risk profile, `user-needs`' safety-critical needs, `differentiation`'s claims,
`product-code`'s classification and `precedent-search`'s predicates, technology comparison and
special controls rests on the founder's beliefs, and says so on every line. Tell the user this at
the start when those are missing, and name the skill that would fill each gap.

## Rules for this skill

- **Never send company text outside.** Queries to FDA and ClinicalTrials.gov carry product codes,
  conditions, generic device words and competitor names — never the company's product name,
  indications, claims, description or any file's contents.
- **Show every query before it runs.** Every command that reaches FDA or ClinicalTrials.gov. Batch
  them so the user approves a step at a time, and log every one.
- **Never do arithmetic by hand.** Every sample size, timeline, budget and total comes from
  `mos/lib/studies.py`, and the output shows the command and its inputs. If the script cannot run,
  write the calculation out in full for the user to check, and say it was not run.
- **Every number carries its source.** A figure comes from `mos/lib/reference/clinical-cost-bands.md`
  (name the section), from a script's output, from an FDA record or ClinicalTrials.gov record (name
  the number), or from the user (say so). Where no source exists, say the figure is missing. Never
  supply one from memory.
- **Estimate every study by one method.** Every estimate uses `mos/lib/studies.py` and the cost
  bands, at the same depth for every version, so no version looks better only because it got a
  closer look. Any deeper estimate made later, once a version is chosen, uses the same script and
  bands. Say plainly that these estimates are light.
- **Test what the user brings before relying on it.** An indications statement the team has
  drafted, a pathway it expects, a difference it calls minor, a study it thinks FDA will accept:
  analyse independently, then compare. Where the analysis disagrees, say so plainly, give the
  evidence, and ask the user to reconsider. Once they have heard the challenge and confirmed, accept
  it, and record that it was confirmed over the challenge.
- **Score; never rank or recommend.** No version is called the best, the recommended or the
  preferred one. No total score unless the team supplies its own weights.
- **Do not write into `context/`** without approval of that specific write.
- **Plain words first, the term beside them.**

## Steps

### 1. Establish what context exists

Check for `context/context-map.md`.

- **It exists** — read it. Read, weighing each by the order of trust in the context standard:
  - **The device.** `context/product/device-profile.md`: intended use, the indications for use as
    the team has drafted them, contraindications, how it works, users and setting, commercial
    intent — and its **risk profile**: invasiveness, software documentation level, sterility,
    patient contact, energy, novel aspects with no standard to point at, and the hazards the team is
    already worried about.
  - **The risks.** Anything in `context/risk/` or, unreviewed, `outputs/risk/`: a hazard analysis,
    a risk management file, a list of hazards and harms. For each serious harm, note its severity
    and the risk control that is meant to prevent it. A risk control whose effectiveness has to be
    shown in people is an evidence question.
  - **The user needs.** The user needs in `context/users-and-needs/` or, unreviewed,
    `outputs/users-and-needs/`. The ones marked **safety-critical** — a realistic failure could
    harm a patient or user — and the ones marked Critical need validation evidence: human factors,
    and sometimes clinical.
  - **The claims.** The differentiation analysis in `context/commercial/` or, unreviewed,
    `outputs/commercial/`: each claim's ID, wording, stakeholder, type and priority.
  - **The classification.** `context/regulatory/classification.md`, if a person has chosen a
    code; otherwise a product code analysis in `context/regulatory/` or `outputs/regulatory/`.
  - **The precedent.** `context/regulatory/precedent.md`, if a predicate has been chosen; the
    precedent search, reviewed or draft. Read six parts of it:
    - the **predicates' indications for use**, word for word. The closest version starts here;
    - the **claims check**: the claims outside every candidate's intended use;
    - the **comparison table**: every row marked Different, and the question each raises. The
      precedent record lists the differences from the chosen predicate;
    - the **requirements map**: each special control, what it requires, how the predicates met it,
      the standards that support it, and what is left open;
    - for a De Novo, the **risks FDA identified** in similar grants and the special controls that
      mitigate them;
    - for a PMA, the **clinical studies behind earlier approvals**: design, endpoints, patients,
      follow-up. Study estimates start there.
  - **Reimbursement.** A reimbursement analysis in `context/commercial/` or `outputs/commercial/`,
    if one exists.
  - **Clinical evidence the company already has.** Anything in `context/clinical/`: published
    literature, earlier studies, a clinical strategy.
  - **Earlier work.** `context/regulatory/indications-strategy.md` and any earlier draft.

  Read Word documents with `python mos/lib/mosdocx.py read <file>`. Tell the user what you found and
  which of it is unreviewed. List contradictions; do not resolve them.
- **It does not exist** — say so. Say that this skill is much stronger after `setup`,
  `user-needs`, `differentiation`, `product-code` and `precedent-search`, and what each would add.
  Then offer to continue from the conversation.

Then tell the user plainly what is missing and what it costs the analysis, one line each:

| Missing | What the analysis loses |
|---|---|
| Risk profile (`setup`) or a risk file | The evidence questions are drawn from the device description alone. A risk the team knows about and did not mention will not shape any study |
| User needs (`user-needs`) | No safety-critical needs to validate, so human factors and clinical validation are estimated blind |
| Claims (`differentiation`) | The top of the spectrum is built on claims captured in step 5, from the founder alone, with no view of what buyers need |
| Classification (`product-code`) | The pathway for each version is reasoned from the device description, not from FDA's record |
| Precedent (`precedent-search`) | No predicate wording to anchor the closest version, no technological differences or special controls to test, and study estimates start from general averages rather than studies of devices like this one |
| Reimbursement analysis | The reimbursement score reads "Not assessed" |

Anything you need outside the declared paths, ask for by name and say why.

### 2. Check the connections

```
python mos/lib/openfda.py check
python mos/lib/studies.py check
```

If `python` is not found, use the command `setup` found — `python3` or `py -3`. If FDA or
ClinicalTrials.gov cannot be reached, write each search as a plain instruction for the user to run
on the website, and continue; everything after this step still applies.

### 3. Tell the user what will leave the machine

In one short paragraph: product codes, document numbers and generic device words go to FDA's
public database and website; conditions, generic intervention words and study numbers go to
ClinicalTrials.gov, run by the US National Library of Medicine. The calculations run on this
machine and send nothing. Nothing else leaves.

### 4. Take the predicate's indications apart

Get the likely predicate's indications for use, word for word: from the precedent search, or from
the predicate's 510(k) summary or De Novo decision summary:

```
python mos/lib/openfda.py fetch K212763 --out outputs/regulatory/summaries
```

If there is no predicate — the device is headed for a De Novo or a PMA — use the nearest devices the
precedent search found, and say that none is a predicate.

Break the predicate's statement into its **elements**, and the team's own draft beside it, if there
is one:

| Element | The plain question | Predicate | Team's draft |
|---|---|---|---|
| **Function** | What does the device do, mechanically? | | |
| **Condition** | Which disease or condition, if any is named? | | |
| **Benefit** | Does it state a clinical outcome, or only that the device is "for use in"? | | |
| **Patients** | Which patients: age, severity, anything that narrows them? | | |
| **Body site** | Where on or in the body? | | |
| **Setting** | Hospital, clinic, home? | | |
| **Role** | Used alone, or alongside another test or treatment? | | |
| **User** | Who uses it, and is it prescription or over the counter? | | |

Say which elements of the team's draft already differ from the predicate. A difference here is
where the 510(k) question starts.

**Whether a difference changes the intended use** is the hinge between a 510(k) and a De Novo. A
510(k) device may have different indications from its predicate and still share its intended use,
if the difference does not raise new questions of safety and effectiveness. FDA's 2014 guidance on
substantial equivalence sets out that test. A new disease, a patient group with different risks, a
different part of the body, or a stated clinical outcome the predicate does not claim often does
raise them. For each element the team's draft moves, say whether it could, and why, citing the
precedent search's intended-use gate where it ran. Do not decide: this is a question for FDA.

### 5. Read the claims the wording would carry

From the differentiation analysis, take the **regulated claims**: those about a disease or
condition, a patient group, a clinical outcome, or safety or effectiveness compared with another
treatment. For each, record which element of the indications statement it needs to move, and how:
"fewer wound infections at 30 days" needs a **condition** and a **benefit** the predicate does not
state.

If there is no differentiation analysis, ask the founder what they need to be able to say, briefly,
and which of it is a **must-have** — the device does not sell without it. Give the claims IDs
`CL-001` onward. Say that `differentiation` would do this properly.

Sharpen each claim until it could be tested. "Better outcomes" is not a claim; "fewer wound
infections at 30 days than standard closure" is. A claim that cannot be made specific cannot be
placed in a statement; say so and set it aside.

Mark every claim that names or clearly points to a competitor as **comparative**: it needs
head-to-head evidence whatever the wording.

**Claims about workflow, ease of use, speed or cost** usually need no change to the indications. Note
them in one line, as claims any version could support with the right evidence, and leave them to
`differentiation`. This skill does not analyse or cost them.

Show the list. Confirm before going on.

### 6. Set out what the evidence must answer, whatever the wording

The wording is one source of evidence. The other is the device itself: what could go wrong, and how
it differs from what FDA has already seen. Build a list of **evidence questions** from four
sources, with IDs `EQ-01` onward, local to this document:

| Source | What becomes an evidence question |
|---|---|
| **Risk profile and risk file** | Each hazard that could cause death, serious injury or irreversible harm; each hazard the team is already worried about; each risk control whose effectiveness can only be shown in use; each novel aspect with no standard to test against |
| **Safety-critical user needs** | Each need marked safety-critical: the validation that shows users meet it. Human factors testing always; clinical validation where the need is about an outcome in patients |
| **Technological differences** | Each row marked Different in the precedent search's comparison with the predicate a version relies on, with the question the precedent search said it raises |
| **Special controls and open requirements** | Each special control, and each requirement the precedent search's map left open. A special control that names clinical performance testing is a clinical study, whatever the wording |

For each question, record:

- **The question**, in plain words, answerable yes or no: "Does the new coating cause more tissue
  reaction than the predicate's uncoated surface?"
- **Where it came from**: the hazard, the need (`UN-004`), the comparison row or the special
  control, with the document it is in.
- **How serious it is**: what happens to the patient if the answer is bad.
- **The evidence that could answer it**, cheapest first: bench testing to a recognized standard,
  other bench performance testing, biocompatibility, software verification, an animal study, a
  human factors study, clinical data. Say what the predicates' summaries and similar De Novo
  decision summaries show was used for the same question. That is the strongest guide there is.
- **Whether clinical data is likely needed**, and why. It is likely when a special control requires
  it; when the predicates or similar grants used clinical data for the same question; when the
  question is how the body responds over time and no bench or animal model is accepted for it;
  when the difference changes how the device acts on the body, or which tissue it acts on; or when
  a serious hazard's risk control can only be shown working in patients. Otherwise say bench or
  animal evidence is likely enough, and why.

Precedent decides this more than reasoning does. Do not conclude that a difference needs no
clinical data when the predicates' testing shows otherwise, and do not add a clinical study that
neither the precedent nor the risks point to. Where it is uncertain, say so: that uncertainty is a
question for FDA.

**The questions do not go away with narrower wording.** Most apply to every version. The
technological differences depend on the predicate each version relies on; a De Novo version has no
predicate, so its questions come from the risks and from the special controls of similar De Novo
grants. Which versions each question applies to is settled in step 8.

**Test what the team believes.** A team that says a difference is minor, or that a risk needs no
clinical data, is making a claim like any other. Check it against the predicates' testing and the
similar grants. Where they disagree, say so with the evidence and ask.

Show the list. Confirm before going on.

### 7. Draft the versions

Draft three or four versions of the indications statement, from closest to the predicate to most
compelling. Label them **V1** onward. Two are always there:

| Version | What it is |
|---|---|
| **V1. Closest to the predicate** | The predicate's statement, changed only where the device truly differs — its name, and any element it cannot share. The fastest pathway, and the fewest clinical studies the device allows: none for the wording, and only what the evidence questions force. This is the safe, cost-effective anchor |
| **V2, V3. In between** | One or two elements moved from V1, chosen where one element carries the most value for the least evidence: often a named patient group or condition without a stated outcome. Draft one or two, not every combination |
| **Last. Most compelling** | The wording that carries every must-have regulated claim, and the pathway and studies that follow: a 510(k) with clinical data if the intended use still matches a predicate, a De Novo if it does not and the risk is low to moderate, a PMA if the risk is high |

A **sequence** — V1 cleared first, the most compelling version sought later in a second submission,
using data gathered after launch where it can serve — may take one of the four places, where it
differs from going straight to the top.

Collapse where versions would be the same. If V1 already carries every must-have claim, say so
plainly — the trade-off this skill exists to weigh does not arise, which is good news — and stop at
V1 and one alternative the team asks for. If the evidence questions already force a clinical study
under V1, say that too: the cost of the more compelling wording is then the difference between two
studies, or one larger study, not between no study and one.

If precedent shows a statement more compelling than the team has asked for is achievable — a
similar device cleared with a named condition the team did not think to claim — say so as a
suggestion, labeled as the skill's, never as one of the versions unless the team adds it.

For each version, write:

- **The indications for use, in full**, in FDA's form: "The [device] is indicated for [function] in
  [patients] with [condition] ... ". Every element stated. Mark it as a draft for this comparison.
- **What moved from the predicate**: the elements that differ from V1's anchor, and whether each
  could change the intended use.
- **Pathway and product code**, with the reason: the code's record, the predicate or its absence.
- **The predicate it relies on**, where there is one. It decides which technological differences
  become evidence questions for this version.
- **Jurisdiction**: US. Every version carries the tag.
- **Breakthrough Device designation**: raise it only where the version could plausibly qualify —
  the device treats or diagnoses a life-threatening or irreversibly debilitating condition, and
  offers a breakthrough technology, has no cleared or approved alternative, offers significant
  advantages over existing ones, or is in patients' best interest to make available. Say what it
  would change: more interaction with FDA during development and review, and possible routes to
  Medicare coverage. Do not assess eligibility; name it as a question for FDA.

Show the versions and invite the team to add, edit or drop them. **Test a version the team drafts**
as you would anything else they bring: if its pathway does not follow from its wording, or it omits
evidence its wording or an evidence question needs, say so and ask. Confirm the final set before
costing anything.

### 8. Build the grids

**What each version lets the company say.** Rows are the regulated claims, columns the versions.
Each cell gets one status:

| Status | Meaning |
|---|---|
| **Label** | The version's wording carries the claim, and its evidence supports it. FDA reviews it |
| **Can't say** | The claim needs an element the wording does not carry. Making it would be promotion outside the cleared indications |

Add the **comparative** marker to any Label cell where the claim names a competitor, with the
head-to-head evidence it needs.

Below the grid, say in plain words what it shows: which element of the wording is the expensive
one, and which must-have claims each version gives up. That paragraph is usually the most useful
thing in the document.

**How each version answers the evidence questions.** Rows are the evidence questions, columns the
versions. Each cell says how the question is answered: **Bench**, **Biocompatibility**,
**Software**, **Animal**, **Human factors**, **Clinical** — naming the study and the endpoint — or
**Does not apply**, with why: a version with a different predicate may not have the difference, or
a narrower patient group may not face the hazard.

Below it, say which questions force a clinical study under every version, and which only under
some. A question that needs clinical data under V1 is the floor on what the company will spend,
whatever it asks FDA to clear.

### 9. Find the evidence precedent

For each study a version needs, look for how devices like this one were studied before.

**From the precedent search**, if it ran: the clinical studies behind earlier De Novo grants and PMA
approvals — design, endpoint, patients, follow-up — and, for each evidence question that needs
clinical data, how similar devices showed the same thing: the safety endpoint, how adverse events
were defined, the follow-up, and the adverse event rates reported. A rate from a predicate's or a
similar grant's summary is where a safety goal starts.

**From ClinicalTrials.gov**: comparable device studies, for their size, length, sites and endpoints.
Show the planned queries, then run them. Search by condition and generic intervention words, never
the company's words:

```
python mos/lib/studies.py trials --condition "surgical site infection" --intervention "wound closure"
python mos/lib/studies.py trials --condition "..." --randomized --since 2015
python mos/lib/studies.py trial NCT01234567 NCT07654321
```

Read the two to five closest studies with `trial` for their endpoints, comparators and follow-up.
Record each query in the search log. Say that ClinicalTrials.gov records are entered by sponsors and
not verified, and that enrolled per site per month is a floor on the true rate.

### 10. Estimate each study, lightly

For each study, set out:

- **Design**: single arm against a performance goal, randomized against a control, non-inferiority,
  or diagnostic accuracy. Say why, from precedent.
- **Primary endpoint** and its time frame, tied to the element of the wording it earns — or, in a
  study that exists only to answer evidence questions, the primary safety endpoint.
- **Safety endpoints**: every study in patients carries them, drawn from the evidence questions.
  Name the harms as adverse events with a time frame, and the `EQ` each one answers. An evidence
  question the version answers clinically must appear here, in some study.
- **Comparator**, where there is one.
- **Patients**: from `studies.py size` where the inputs have a source — an expected rate from the
  literature or a precedent study, a performance goal FDA has accepted — or from the median of
  comparable studies where they do not. Say which, and state every input. Then check the number
  against the most serious safety question: `size safety` gives the patients needed to rule out an
  adverse event rate at the limit precedent or the risk file sets. Take the larger number, and say
  which question set it. For a study that exists only for safety, size it on the safety question
  alone: `size safety`, or `size performance-goal` with the expected adverse event rate against a
  safety goal from precedent.
- **Whether an investigational device exemption is likely needed**: a significant-risk device
  studied in the US needs FDA's approval of an IDE before the study starts. Name it; do not decide.
- **Sites and months**: from `studies.py timeline`. Take the enrollment rate from comparable studies;
  take start-up, ramp and close-out months from the user, or state them as assumptions.
- **Cost**: from `studies.py budget`, using the per-patient band in the reference file that fits
  the study, and FDA's fee. Where the band is for a harder study than this one, say so. Where the
  study's patients are largely Medicare beneficiaries, name Medicare coverage of routine costs in
  IDE studies CMS has approved (the reference file's last section) as something that could lower
  the cost. Do not estimate the saving.

**Evidence that is not a clinical study** — the bench, biocompatibility, software, animal and human
factors work each version needs — is listed with the evidence question it answers. Human factors
validation needs at least 15 participants for each distinct user group, per FDA's 2016 guidance on
human factors. Name this work in every version. The reference file has no costs for it: ask the
user for quotes, or mark it **not costed**, and say the version's total leaves it out.

```
python mos/lib/studies.py size performance-goal --p 0.92 --goal 0.85 --dropout 0.10
python mos/lib/studies.py size safety --max-rate 0.05 --dropout 0.10
python mos/lib/studies.py timeline --patients 180 --sites 8 --rate 1.1 --startup 6 --ramp 6 --followup 12 --closeout 6
python mos/lib/studies.py budget --patients 180 --per-patient 51117 88199 --fixed "FDA De Novo fee=191020"
```

Mark every estimate as light: an order of magnitude to compare versions by, not a budget. Once a
version is chosen, its studies need designing in depth — the design, the endpoints and the number
of patients a team can budget against and take to FDA. A study that could run outside the US for its
feasibility stage is noted as such; the reference file has no costs for studies abroad, so say that.

### 11. Total each version

Run `studies.py scenario` once per version, with every stage in order: each study, FDA's review
(the MDUFA goal and, for a PMA, the experienced average from the reference file), the fee, and the
non-clinical testing where the user has given a cost or a time for it. Where it is not costed, say
beside the total that the total leaves it out. Give each later stage its chance of being reached
from the reference file's odds, where they apply, for the secondary line.

```
python mos/lib/studies.py scenario --stage "Feasibility study; cost=1400000:2100000; months=18:24" --stage "Pivotal study; cost=12000000:20000000; months=36:48; reach=0.48" --stage "De Novo review; cost=191020; months=8:12; reach=0.363"
```

Report the total as the budget, and the risk-adjusted line beneath it as what it is: an average
across programs like this one, most of which stop early, and never a smaller budget.

Set the version's months against the whole-program figures in the reference file as a sanity
check. Where they differ widely, say why.

### 12. Say what payers will want

If a reimbursement analysis exists, read its position today for each setting, its routes to close
the gaps, and its table of what the indications would change. For each version, set the elements
the version moves against that table, and give one line: what payers would need to see before
covering and paying for the device under that wording, and whether the wording opens or closes a
route — a named condition under a coverage policy, a setting in another payment system, a benefit
strong enough to be the substantial clinical improvement that pass-through or add-on payment needs.
If none exists, write "Not assessed — run `reimbursement`" and leave it there. Do not research
coding, coverage or payment in this skill.

### 13. Score each version

Score each version 1 to 5 on each dimension. **5 is always the most favorable.** Give every score
its reason in one line, citing the step and source it rests on. Scores 2 and 4 fall between the
anchors.

| Dimension | 5 | 3 | 1 |
|---|---|---|---|
| **Time to first US revenue**, from today | Under 12 months | 24 to 36 months | Over 5 years |
| **Regulatory and clinical cash to first revenue** — studies, fees, testing; not engineering | Under $0.5 million | $2 to 10 million | Over $30 million |
| **Clinical risk** — the chance the evidence falls short | No clinical study needed, for the wording or for the evidence questions | Precedent for the endpoints exists; the size of the effect, or the adverse event rate, is uncertain | No precedent; the endpoint itself is unsettled, or a serious hazard has no accepted way to be shown safe |
| **Regulatory risk** | A 510(k) whose wording keeps the predicate's intended use, and no technological difference that recognized standards and the predicate's testing do not answer | A De Novo with a close precedent to model special controls on, or a 510(k) whose wording or differences need new performance or clinical data | A PMA for a novel device, or FDA's record says "contact FDA" |
| **Strength of the indications with buyers** | The wording carries every must-have claim | It carries most must-have claims | It carries none |
| **Reimbursement** | An existing code, covered, paid adequately | A code exists, but coverage is uncertain or payment is bundled | A new code and coverage are both needed |

Reimbursement reads "Not assessed" when there is no reimbursement analysis. Clinical risk scores 5
only when neither the wording nor the evidence questions need clinical data. Regulatory risk scores
5 only when no evidence question is left without an accepted way to answer it.

**No total.** If the team wants one, ask them for the weight of each dimension, record the weights
and who set them in the document, and show the weighted total beside the unweighted scores, never
in place of them.

### 14. Write the questions for FDA

For each version, the two or three questions a Pre-Submission meeting would need to settle before
the company commits: whether FDA sees the wording as the predicate's intended use, whether it agrees
with the pathway, whether it would accept the proposed study design and endpoint. Phrase each as a
question FDA could answer yes or no. A Pre-Submission has no fee; say so.

### 15. Write the draft

Fill `templates/indications-strategy.md`. Write dates in the Date format from
`context/templates/document-settings.md`, if it exists. The search log lists every query in order.
Show the user the complete content. Confirm.

Save the filled template to `outputs/regulatory/indications-strategy.source.md` and run:

```
python mos/lib/mosdocx.py render --in outputs/regulatory/indications-strategy.source.md --out outputs/regulatory/indications-strategy_draft.docx --title "Indications Strategy — <device>" --remove-input
```

If `indications-strategy_draft.docx` already exists, the script refuses to overwrite it. Show what
changed and ask; add `--force` only on a yes. If the script cannot run, write the filled template to
`outputs/regulatory/indications-strategy.md` instead, and say that Word output needs the step in
`setup`.

Tell the user how the draft becomes the record: review and redline it in Word, save it with the
revision in its name — `indications-strategy_revA.docx` — in `context/regulatory/`, or in the
quality system with the map pointing at it, then delete the draft from `outputs/regulatory/`. Until
then, later skills read the draft and say it is unreviewed.

### 16. Offer to record the choice

The analysis scores; it does not choose. When a person has chosen a version, fill
`templates/indications-strategy-record.md` and offer to write it to
`context/regulatory/indications-strategy.md`. It records who chose, when, the wording and pathway,
the evidence questions and how they will be answered, the studies planned, the claims carried and
given up, and any weights the team set. Show it in full; write only on a yes. If nobody has chosen
yet, say the record waits until they have.

Then say what the choice sets off:

- **If the chosen wording differs from the device profile's indications**, offer to update
  `context/product/device-profile.md`, the change marked as coming from this session. Write only on
  a yes.
- **If the wording changed**, `product-code` and `precedent-search` should be run again: different
  indications can mean a different code or predicate.
- **If the chosen version has a clinical study**, it needs designing in depth before a
  Pre-Submission: this skill's estimate is for choosing, not for budgeting. Say so, and that the
  record holds the starting point.

## Working at three levels of context

| What the company has | How this skill behaves |
|---|---|
| Nothing | Says plainly that the analysis is much stronger after `setup`, `user-needs`, `differentiation`, `product-code` and `precedent-search`. Asks for the nearest cleared device and reads its indications from FDA, captures the must-have claims briefly, asks what could go wrong and how the device differs from what is on the market to draw the evidence questions, estimates studies from ClinicalTrials.gov and the reference file's averages. Explains each idea as it comes — an indications statement, a predicate, an intended use, an endpoint. Every line resting on the conversation says so |
| Some files | Builds on the claims, classification and precedent that exist; says which are unreviewed; fills the gaps by interview, marked as such. Names which missing skill would change which score |
| A full document set | Versions trace to the predicate's wording, the claims, the risk file, the safety-critical needs, the technological differences, the special controls and the earlier studies. Flags contradictions — a must-have claim no version short of a PMA can carry, a serious hazard with no evidence planned, a team draft that already moves the intended use while the plan assumes a 510(k) — rather than resolving them |

## Interviewing style

- One question at a time.
- Ask which claims are must-haves before drafting the versions. A founder who says every claim is a
  must-have has not chosen yet; ask which one they would keep if they could keep one.
- When the team has already drafted its indications, ask where the wording came from: a
  competitor's label, a consultant, an investor deck. The answer tells you what to test.
- Do not argue for a version. Set out what each costs and let the grids speak.

## Boundaries

This skill does not choose the indications, analyse risk — it reads the risk file and the risk
profile, which `setup`, `user-needs` and the company's risk management build — analyse or cost
workflow and economic claims, write a test plan, write a study protocol, calculate a final sample
size, research reimbursement, write labeling or promotional material, or predict what FDA will
decide. Its study estimates are for comparing versions; the chosen version's studies are designed in
depth later, and a statistician and FDA settle them. It reads FDA's public records and ClinicalTrials.gov; it does
not know what FDA told any other company privately.

## Where this skill is weakest

Recorded so it gets fixed rather than rediscovered:

- Whether a change in wording changes the intended use is FDA's judgment, made case by case. The
  skill names the question for each element; a Pre-Submission settles it.
- The per-patient cost bands come from 2012 data on complex PMA devices. For the simpler studies
  behind most 510(k)s and De Novos they run high, and no public source gives a better figure.
- Non-clinical testing — bench, biocompatibility, animal, human factors — is named but not costed.
  No public source gives costs for it, and an animal study run under good laboratory practice can
  cost as much as a small clinical study.
- Evidence questions are only as complete as the risk file. At concept stage, with a short list of
  hazards, the questions will be short too; say so.
- Older predicates often have no summary online, so their wording cannot be read and V1 has no
  anchor. Say so, and use the closest device whose wording can be read.
- Enrollment rates from ClinicalTrials.gov are floors: the months counted include follow-up, and
  sponsors report sites unevenly.
- The odds of reaching each stage are averages for complex therapeutic devices. A given program's
  odds may be far better or far worse.
- Time to first revenue ignores engineering, manufacturing and the time a sales channel takes. It
  measures the regulatory and clinical path only.
