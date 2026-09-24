---
name: product-code
description: Find the FDA product codes that may fit a medical device, and report what each one implies for its class and path to market, from FDA's public classification database. Use when a team needs to classify a device, check a classification it has assumed, or learn which regulatory pathway a product code points to.
version: 0.1.0
maintainer: Eric Sugalski
phase: [00-concept, 01-definition]
discipline: [regulatory]
reads:
  - context/context-map.md
  - context/product/**
  - context/regulatory/**
  - context/commercial/**
  - context/templates/**
writes:
  - outputs/regulatory/
  - context/regulatory/classification.md    # only on the user's approval, after review
  - context/product/device-profile.md       # only on the user's approval, to add answers
status: draft
---

# Product code

Finds the FDA product codes that may fit a device and reports what each one implies: class,
regulation, submission type, and what that means for the path to market. The output is a Word
document in `outputs/regulatory/`, built from the company's template: a draft for review, not
a controlled record. It is the first of three regulatory research skills; `precedent-search`
and `reference-devices` build on the code a person chooses here.

Read `mos/context-standard.md` before starting if you have not already, then read
`context/context-map.md` to find out what you are allowed to read.

## The thing this skill is actually for

**A product code is FDA's name for a type of device.** It fixes the device's class, the
regulation that governs it, and the kind of submission FDA expects. A wrong code costs months: a
team prepares a 510(k) against the wrong regulation, or spends a year assuming a pathway that the
code never allowed.

The skill finds candidates and states the facts. **A person chooses the code.** Where the fit is
genuinely uncertain, the honest output is the uncertainty, stated plainly, with the question that
would settle it.

**Indications for use carry the weight.** Two devices that work the same way can sit under
different codes, or different pathways, because they treat a different condition, in different
patients, at a different body site. A product code search built on a vague intended use returns a
confident wrong answer. Get the indications right before searching.

## Rules for this skill

- **Never send company text to FDA.** Search terms are generic words written for FDA's database:
  a device type, a technology, a part of the body, a clinical function. Never the intended use,
  the indications, the device description or any file's contents. See `DECISIONS.md`,
  2026-09-24, and the "Where your data goes" section of the context standard.
- **Show every query before it runs.** Every command that reaches FDA or the eCFR — searches,
  `code`, `clearances`, `devices`, `regulation`, `fetch` — not only the first searches. List the
  commands, say what each one sends, and run them on a yes. Batch them so the user approves a
  step at a time rather than a command at a time. The user may edit or drop any of them.
- **Test what the user brings before relying on it.** An expected class, an assumed pathway, a
  code named in a strategy memo, an earlier classification record: search and judge
  independently first, then compare. Where the search disagrees, say so plainly, show the
  evidence, and ask the user to reconsider. Once they have heard the challenge and confirmed
  their direction, accept it, and record in the analysis that it was confirmed over the
  challenge.
- **Do not choose the code or the pathway.** Shortlist, compare and state the facts. Choosing is a
  regulatory decision for a qualified person.
- **Do not invent codes, definitions or counts.** Every fact about a code comes from a query in
  the search log. If a query failed, say so; do not fill the gap from memory.
- **Do not suggest a 513(g) request.** Where the classification is uncertain, point to a
  Pre-Submission instead. A Pre-Submission lets the company discuss the device with FDA before
  anything is written down; a 513(g) response is FDA's written view, formed without that
  discussion, and it is hard to move away from once it exists.
- **Scope is devices regulated by FDA's device center (CDRH).** If the device includes a drug or
  a biologic, or is used in blood collection and processing or with cell and tissue products,
  say that part is outside this skill, record it in Appendix B, and classify only the device
  function that is in scope.
- **Do not write into `context/`** without approval of that specific write. The classification
  record in step 9 is written only after a person has reviewed the analysis and chosen a code.
- **Plain words first, the term beside them.** Most people running this skill have never read a
  classification regulation.

## Steps

### 1. Establish what context exists

Check for `context/context-map.md`.

- **It exists** — read it. Read `context/product/device-profile.md` if it is there, and whatever
  the map points at under `product/` and `regulatory/`. Read the commercial intent in the device
  profile, and the differentiation analysis under `commercial/`, reviewed or draft: its Claims
  table lists the claims the company says it must be able to make, and they shape the
  indications this skill drafts. Read Word documents with
  `python mos/lib/mosdocx.py read <file>`. Tell the user what you found.
  - Read the drafts in `outputs/product/`, `outputs/regulatory/` and `outputs/commercial/` too.
    An earlier product code analysis, or a differentiation draft nobody has reviewed, still
    informs this run. Say which drafts you are relying on and that they are unreviewed. A
    reviewed document or record outranks a draft; where they disagree, say so and ask.
  - If `context/regulatory/classification.md` exists, a code has been chosen before. Ask whether
    this run is to check it or to start again, and do not overwrite it.
  - If documents disagree — the device profile says Class II and a strategy memo says Class III,
    or two documents give different indications — list the contradictions. Do not pick one.
- **It does not exist** — say so, and say that running `setup` first will make this skill better.
  Then offer to continue from the conversation alone. Do not refuse to work.

Anything you need outside the declared paths, ask for by name and say why. Write the answer back
to the context map so the question is not asked twice.

### 2. Check the connection to FDA

Tell the user, in one short paragraph, what this skill sends and where: search terms, to FDA's
public database at api.fda.gov; document numbers, to FDA's website when a summary is
downloaded; and regulation numbers, to the eCFR at www.ecfr.gov, when a regulation is read.
Nothing else. Then run:

```
python mos/lib/openfda.py check
```

If `python` is not found, use the command `setup` found — `python3` or `py -3`.

If the check fails, or the user's company does not allow outbound queries, continue without it:
write out each search as a plain-language instruction for FDA's Product Classification database,
`https://www.accessdata.fda.gov/scripts/cdrh/cfdocs/cfpcd/classification.cfm`, and ask the user
to run it and paste or save the results. Everything after this step still applies.

### 3. Interview for what is missing

The skill needs five things. Take each from the device profile or another document where one
answers it, say which, and ask only for the rest. One question at a time.

1. *What does the device do, in one sentence?* FDA calls this the **intended use**.
2. *Which condition does it diagnose, treat, prevent or monitor, in which patients, and where on
   or in the body?* FDA calls this the **indications for use**. Ask for the condition, the
   patients and the body site separately. If a written statement exists, take it word for word.
   If the device is a general tool used across many conditions, like a scalpel, record that
   instead of pressing for a condition.
3. *How does it work?* The mechanism and the technology: what it measures, delivers, removes or
   analyzes, and how. Hardware, software, or both.
4. *What touches the patient, and for how long?* Skin, mucous membrane, blood, tissue, bone;
   minutes, days, or permanently.
5. *Who uses it, and where?* A clinician in a hospital, a patient at home, a laboratory.

**When the indications are missing or vague, stay on them.** Explain why: they decide which
codes fit, and a new condition, patient group or body site can move a device from one pathway to
another. A company at concept stage may not have written them, and that is normal. Draft them
together in plain words, mark them as drafted in this session, and search anyway. The analysis
will say its answer depends on them.

**Also ask who should not use it.** *Is there anyone, or any situation, where the device should
not be used?* FDA calls these **contraindications**: situations where the risk of using the
device clearly outweighs any possible benefit. Record them separately. They belong in the
labeling, not in the indications statement.

#### Writing an indications statement

When drafting indications with the user, or reviewing ones they bring, hold to these. They come
from FDA's guidance on the content of a 510(k), its 2014 guidance on substantial equivalence and
its 1998 guidance on general and specific intended use.

**What goes in.** The condition the device diagnoses, treats, prevents, cures or mitigates; the
patients, stated positively (*adults*, *patients undergoing X*); the body site or tissue; and the
clinical setting or user where it matters (*in the home*, *by health care professionals*). A
general tool with no specific condition states its function, the tissue or body site, and the
setting, and stops there. Whether it is prescription or over-the-counter is recorded too; FDA's
indications form asks for it.

**What stays out.** Contraindications, warnings and precautions — each has its own section of
the labeling, and 21 CFR 801.109(d) lists them separately from indications. How the device
works, which is the device description. Performance claims and clinical outcomes (*reduces*,
*improves*, *prevents complications*), which raise the level of specificity FDA judges and the
evidence it will want. Marketing language. A statement like *not for use in eyes that have had a
vitrectomy* is a contraindication; if the limit defines who the device is for, state the
population positively instead.

**The statement must match everything else.** FDA expects the indications to be the same
wherever they appear: the indications form, the labeling, the instructions for use, the
advertising.

**For a 510(k), stay close to the predicate's wording.** The new device's indications must fall
within the predicate's intended use. Every word added beyond the cleared wording of devices under
the same code is a point FDA can argue creates a new intended use. So draft from the indications
of recent cleared devices under the leading code (read from their summaries in step 5), change
only what the device requires, and say what each change is. FDA's 1998 guidance judges a change
by how far it moves along a ladder of specificity: function (*cut*), then tissue type (*soft
tissue*), then organ or organ system, then a specific disease or population, then an effect on
clinical outcome. The further up the ladder, the likelier FDA sees a new intended use. A *tool*
claim (the device cuts tissue) is safer than a *treatment* claim (the device treats a disease).

**Check the draft against the claims the company needs.** Where the device profile or the
differentiation analysis — in `context/commercial/` or, unreviewed, in `outputs/commercial/` —
lists must-have claims, set each one against the draft indications. A
must-have claim the indications cannot carry is a conflict to name now, not after a code is
chosen: say which claim, which words it would need, and how far up the ladder they reach.

**Deviating can be worth it, and it has a price.** A narrower or more specific statement can be
what makes a device sellable: naming the condition a buyer cares about, or a setting a competitor
cannot claim. Where the company wants that, do not argue it away. Say which rung of the ladder the
change reaches, what evidence it is likely to require, and that the choice between a close match
and a stronger claim is a commercial and regulatory decision for the company. Record it in
Appendix B.

Then ask two scope questions: *Does the device contain or deliver a drug or a biologic?* and
*Is it used in blood collection or processing, or with cell or tissue products?* A yes to either
is recorded and handled as the scope rule says.

### 4. Write the search terms

From the answers, write search terms FDA's database will match. FDA's classification database
matches words, not meaning, so the terms have to use FDA's vocabulary:

- **Device-type nouns**, the way FDA names devices: *sensor, monitor, system, catheter, software,
  stimulator, implant, test*. FDA often names a device noun first: "System, Test, Blood Glucose."
- **The technology or mechanism**: *ultrasound, radiofrequency, electrode, image processing,
  laser*.
- **The clinical function**: *detection, ablation, monitoring, fixation, drainage*.
- **The body site or system**: *cardiac, knee, urinary, cranial*.
- **Synonyms for each**, because a search that says *meter* misses a code FDA named *test
  system*.

Plan several narrow searches, each combining two or three terms, and one broad search with
`--any` to catch what the narrow ones miss. Show the planned commands to the user, with what
each sends, before running them:

```
python mos/lib/openfda.py classify "blood glucose" test
python mos/lib/openfda.py classify glucose sensor
python mos/lib/openfda.py classify glucose "blood glucose" "continuous glucose" --any
```

**Check each term against the first rule before showing it.** A term that only this company
would use — a product name, a proprietary technique, a phrase from its indications — does not go.

### 5. Search, and shortlist

Run the approved searches. Keep every `Query:` line the script prints, with its result count and
the "openFDA data as of" line: they are the search log.

**Then search the devices, not only the codes.** A code's name can miss what is cleared under
it, and a device like this one may sit under a code no classification search found. Search
cleared and approved devices by name, across every code:

```
python mos/lib/openfda.py devices vitreous
python mos/lib/openfda.py devices vitrectomy cutter --any
```

The output counts which product codes the matching devices sit under. Any code there that the
classification searches missed goes on the list to examine.

Read the results as a regulatory reviewer would. A code matches on its **definition**, not its
name. Discard codes that share a word but not a function.

Shortlist **three to five** codes. If fewer than three are plausible, say so; do not pad the
list. For each, run:

```
python mos/lib/openfda.py code ABC
python mos/lib/openfda.py regulation 886.4150
```

`code` gives the full record, decoded, and what is marketed under the code: clearances, De Novo
grants, PMA approvals, recalls and adverse event reports. `regulation` gives the classification
regulation's own text from the eCFR: FDA's **identification** of the device type, which is the
legal definition every device under the code must fit; its class; any **special controls**,
which are the specific requirements FDA sets for that type; and any exemption. Many product codes
have no definition in FDA's database, but every classified code has a regulation, so the
identification is the definition to judge against. For a code that is 510(k) exempt, add
`--limits` to read the part's ".9" section, which sets the limits on the exemption.

**How much to read.** Summaries are where the evidence is, and they are slow to read, so read in
proportion to the uncertainty:

- **Always:** list every clearance under each Strong or Partial code with
  `clearances --code ABC --limit 200`. It costs one query and no downloads. Scan the names for
  devices that sound like this one, and read those first rather than only the newest.
- **At least two summaries for each Strong or Partial code:** the most similar by name, and the
  most recent. If a code has none online, say so and pick the next.
- **When the answer is close or uncertain** — two codes fit about equally, the device may be new
  to its code, or the regulation's identification does not plainly cover it — tell the user,
  and offer a second round of up to ten more summaries before writing the draft. Twenty in all
  is the ceiling for this skill. Finding a predicate is the next skill's job, and
  `precedent-search` reads more deeply under the one code that is chosen.

```
python mos/lib/openfda.py clearances --code ABC --limit 200
python mos/lib/openfda.py fetch K123456 DEN123456 --out outputs/regulatory/summaries
```

Record in Appendix B how many summaries were read under each code, and why that was enough.

**If you cannot read PDF files**, say so plainly. List the summaries the user should read, and
tell them this step works best with an AI that can read PDFs — Claude, for example — and that
switching for this step is worth considering. Do not guess at a summary's contents.

**If the device does more than one thing**, it may need more than one code: one for each
function, with one of them primary. Say which function each candidate covers. Choosing the
primary code is the user's call.

### 6. Judge each candidate's fit

For each code on the shortlist, write down:

- **Why it may fit** — the specific points where the regulation's identification, and the
  devices cleared under the code, match the intended use, the indications and the technology.
  Quote the identification; do not paraphrase it. Its verbs matter: a regulation for a device
  *intended to remove* tissue does not plainly cover a device intended to *sample* it.
- **Why it may not** — the specific points where they do not. Name the part of the indications
  or technology that falls outside. A candidate with no stated weakness has not been examined.
- **Fit: Strong, Partial or Weak** — a summary of the two lists, not a score.

### 7. Say what each code means for the path to market

Plain words first, the term beside them. The submission type in FDA's record points to the
pathway; it does not decide it.

| FDA's record says | What it means | Say also |
|---|---|---|
| **510(k)** | FDA expects a premarket notification: showing the device is as safe and effective as one already on the market, called the **predicate**. | Whether a predicate exists is the next skill's job, `precedent-search`. A code that allows a 510(k) does not guarantee one will work: new indications or technology can rule it out. |
| **510(k) exempt** | Devices under this code usually go to market without a premarket submission, though general controls — registration, listing, quality system, labeling — still apply. | Exemptions have limits, set out in the ".9" section of the regulation's part, such as 21 CFR 862.9, which `regulation --limits` prints. A device with a different intended use or a different fundamental technology can lose the exemption. Quote the limits that could apply; do not decide. |
| **PMA** | Premarket approval: FDA's pathway for high-risk devices, usually needing clinical data showing the device is safe and effective. | `precedent-search` finds earlier approvals and the evidence FDA accepted. |
| **Contact FDA** | FDA has not settled which submission applies to this code. | This is a question for a Pre-Submission. |
| **HDE** | Humanitarian device exemption: a route for devices that treat or diagnose a condition affecting small numbers of people in the US, where the device must show safety and probable benefit rather than full effectiveness. | It needs a humanitarian use designation from FDA first, and carries limits on profit and use. Name it; do not assess eligibility. |
| **Enforcement discretion** | FDA has said it does not currently intend to enforce premarket requirements for this device type. | That policy can change, and it may cover only some uses. Point to the FDA policy behind it for a person to read. |
| **Class U or N, unclassified** | FDA has not classified the device type; the record gives the reason. | Say what the reason means for this device, and that it is a Pre-Submission question. |
| **Anything else** | The script says the type is not documented by openFDA. | Read the code's FDA page, which the `code` command prints, and report what it says. Do not guess. |

Report the other facts in plain words where they apply: an **implant**; **life-sustaining or
life-supporting**; **exempt from GMP requirements** (some quality system manufacturing rules do
not apply); **eligible for third-party review** (an FDA-accredited outside organization can review
the 510(k), which is often faster). Report recall and adverse event counts as context, with the
caution the script prints: a report is an allegation, and counts rise with the number of devices
in use.

**If no code fits**, say so plainly and name the nearest codes with why each fails. That points
toward a **De Novo** request, FDA's pathway for a new type of low- or moderate-risk device with
nothing like it on the market; or toward a **PMA** if the risk is high. Say that this is a
possibility to confirm, not a conclusion, and that a Pre-Submission is how to confirm it.

### 8. Write the draft

Fill `templates/product-code.md`. Write dates in the Date format from
`context/templates/document-settings.md`, if it exists. The search log in Appendix A lists every
query the script printed, in order, with its result count. Show the user the complete content.
Confirm.

Then deliver it as a Word document. Save the filled template to
`outputs/regulatory/product-code.source.md` and run:

```
python mos/lib/mosdocx.py render --in outputs/regulatory/product-code.source.md --out outputs/regulatory/product-code_draft.docx --title "Product Code Analysis — <device>" --remove-input
```

If `product-code_draft.docx` already exists, the script refuses to overwrite it. Show what changed
and ask; add `--force` only on a yes. If the script cannot run, write the filled template to
`outputs/regulatory/product-code.md` instead, and say that Word output needs the step in
`setup`.

Tell the user how the draft becomes the record: review and redline it in Word, then save it with
the revision in its name — `product-code_revA.docx` — in `context/regulatory/`, or in their
quality system with the context map pointing at it. The summaries in
`outputs/regulatory/summaries/` are FDA's public documents; keep the ones the analysis relied on
beside it, or delete them.

### 9. Offer to write what belongs in context

Two offers. Name each file, show the full content, and write only on a yes.

1. **The classification record.** Once a person has reviewed the analysis and chosen a code —
   not before — fill `templates/classification-record.md` and offer to write it to
   `context/regulatory/classification.md`. It records who chose the code and when. The
   `precedent-search` skill reads it. If the user has not chosen yet, say that this file waits
   until they have.
2. **The device profile.** If the interview produced answers the profile lacks — indications
   drafted in this session, a patient-contact duration, a body site — offer to add them to
   `context/product/device-profile.md`, each marked as coming from this session.

## Working at three levels of context

| What the company has | How this skill behaves |
|---|---|
| Nothing | Runs the full interview, explaining in plain words why each answer matters to classification, and marks every description in the analysis as from the conversation. Where the indications are not written, drafts them with the user and says the shortlist depends on them |
| Some files | Takes intended use, indications and technology from the device profile or other documents, interviews only for the gaps, and says which answers came from where |
| A full document set | Checks an existing classification against FDA's current record: a code whose definition has changed, a regulation that has moved, a new code created since the choice was made. Flags contradictions between the chosen code and the indications in the company's documents rather than resolving them |

## Interviewing style

- One question at a time.
- Ask in plain words and name the term beside them; never make the user translate.
- When an answer is vague — "it's for heart patients" — ask the next question that makes it
  specific: which condition, which patients, where.
- Do not argue the pathway during the interview. Collect the facts first.

## Boundaries

This skill does not choose a product code or a pathway, search for predicates (that is
`precedent-search`), classify under any system other than FDA's, or handle combination products
and devices regulated by FDA's biologics center. It reads FDA's public records; it does not know
what FDA has told any other company privately.

## Where this skill is weakest

Recorded so it gets fixed rather than rediscovered:

- FDA's database matches words, not meaning. A code named in words the skill did not think of is
  missed. Several narrow searches with synonyms, and a search of device names across codes,
  reduce this; they do not remove it.
- Many older regulations have a one-sentence identification written decades ago, before the
  technology in question existed. Whether a new device fits one is a judgment the skill states and
  a Pre-Submission settles.
- The eCFR is an editorial compilation of the regulations, not the official legal edition; the
  Federal Register is. A regulation changed in the last few days may not show yet.
- openFDA is updated about weekly and FDA asks that it be treated as unvalidated. A code created
  in the last few weeks may be missing.
- A device that is genuinely new may match nothing, and the skill can only say so. Whether that
  means a De Novo is a question for FDA.
