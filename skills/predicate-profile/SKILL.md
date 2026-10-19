---
name: predicate-profile
description: Profile the marketed devices a team has chosen to study — its predicate, reference devices or a close competitor — from FDA's records, their labeling and what their makers publish, and sort what each shows into candidate inputs for the target product profile, user needs, hazards and design inputs. Use when a team has picked a predicate or reference device and needs to know it in depth, or wants to profile a different device in its place.
version: 0.2.0
maintainer: Eric Sugalski
phase: [00-concept, 01-definition, 02-design]
discipline: [regulatory, technical, commercial]
reads:
  - context/context-map.md
  - context/*_issues-list.*
  - context/product/**
  - context/regulatory/**
  - context/commercial/**
  - context/risk/**
  - context/templates/**
writes:
  - context/regulatory/
  - context/regulatory/summaries/    # FDA summaries it downloads, beside those other skills saved
  - context/regulatory/labeling/     # labeling of the devices profiled, one folder per device, on approval
  - context/inbox/
status: draft
---

# Predicate profile

Studies one to three marketed devices in depth: what each is, what it does and how well, how
people use it, what its maker warns about and claims, and what has gone wrong with it in the field.
Usually these are the predicate and reference devices a person chose after the precedent search; a
close competitor can be profiled the same way. Each finding is then sorted by where it goes next:
the target product profile, the user needs, the hazards, the design inputs, the claims. The output
is a Word document in `context/regulatory/`, built from the company's template: a draft for review,
not a controlled record.

Read `mos/context-standard.md` before starting if you have not already, then read
`context/context-map.md` to find out what you are allowed to read.

## The thing this skill is actually for

**The predicate sets the bar.** A 510(k) argues the new device is as safe and effective as its
predicate, so what the predicate does, how well, and what its labeling warns about are what the new
device will be compared with, row by row. A team that knows its predicate only from a two-page FDA
summary finds the rest out from a reviewer's questions.

**FDA's summary is the start, not the whole.** It gives the indications, the technology and the
testing. The instructions for use give the use steps, the warnings, the specifications and the
training. FDA's device identifier database gives sterility, latex, MRI safety and the models sold.
The maker's own material gives the features it competes on and the claims it makes. Each answers a
different question, and the draft says which answered what.

**A predicate's feature is not a requirement.** Most of what a predicate does is a benchmark the
team may match, beat or decide not to compete on. Only what substantial equivalence depends on —
the indications, and technological characteristics the submission will argue are the same — binds
the design. The skill says which is which, and leaves the choice of target to the team.

**Focus beats coverage.** A profile of one device read closely is worth more than five read
skimmingly. Every device in a run is there to answer a stated question, and the skill keeps the set
small.

## Rules for this skill

- **Profile the devices the user chooses.** Recommend, from the precedent search or the
  conversation; never add a device the user has not agreed to.
- **Test what the user brings.** Before profiling a device the user names, check that it resembles
  the device the company is developing: the same product code or regulation, an intended use
  close to the company's, a similar principle of operation. Where it does not, say so, show the
  evidence, and ask whether it is still the right device to study, and in what role. Once the user
  has heard the challenge and confirmed, profile it, and record that it was confirmed over the
  challenge.
- **Keep the set small.** One to three devices a run. More than three, ask which question each
  extra device answers that the others do not, and suggest a second run. Five is the ceiling.
- **Never send company text outside.** Searches send brand names, manufacturer names, model, K, DEN
  and P numbers, product codes and generic device words. Never the company's product name, its
  description, its indications or claims, or any file's contents.
- **Show every query before it runs**, to FDA or the web. Batch them so the user approves a step at
  a time, and log every one.
- **Cite every finding.** Each one carries its source: an FDA record with its number, a labeling
  document with its title, revision and page, a web page with its URL and the date read.
- **A maker's statement is a claim, not a fact.** Report marketing as what the maker says. A
  specification in the instructions for use is stronger than one in a brochure; a figure in FDA's
  summary is stronger than either.
- **Summarize labeling; do not reproduce it.** Instructions for use and brochures are copyrighted.
  Quote only short passages where the exact words matter — indications, contraindications, a
  warning — and summarize the rest with the page cited. Never copy figures, tables or whole
  sections.
- **Do not invent.** Where a document could not be found or read, say so; do not fill a
  specification from memory.
- **Do not write requirements into other documents.** This skill sorts findings and names where
  each should go. The target product profile is never edited; the user needs, hazards and design
  inputs are drafted by their own skills, which read this profile.
- **Do not write into `context/`** without approval of that specific write. That includes saving a
  device's labeling.
- **Plain words first, the term beside them.**

## Steps

### 1. Establish what context exists

**First, the folder layout.** If an `outputs/` folder sits beside `context/`, this company was
set up before MOS 0.3, when drafts were kept there. Run `python mos/lib/layout.py check` and show
the user what it lists, with one sentence on why: drafts now sit in `context/` beside the records
they would revise, and the filename says which is which. On a yes, run
`python mos/lib/layout.py apply`. For each file it lists as left over, ask whether to delete it,
move it where the script suggests, or leave it, and pass the answers as `--delete <path>` and
`--move <path>`. On a no, read and write drafts in `outputs/<domain>/` for this run instead of
`context/<domain>/`, and say that the next skill will ask again.

Check for `context/context-map.md`.

- **It exists** — read it, then read, weighing each by the order of trust in the context standard:
  - **The device.** The target product profile — the newest `target-product-profile_rev*.docx`
    in `context/product/`, or, unreviewed, `target-product-profile_draft.docx` there: intended
    use, indications for use, how it works, patient contact, users and setting, and the minimums
    and targets it sets. If there is none, an earlier `setup` put these in
    `context/product/device-profile.md`; read them there, and suggest re-running `setup` to
    convert it.
  - **The regulatory work** in `regulatory/`: `classification.md` for the product code;
    `precedent.md` for the predicate and reference devices a person chose; the precedent search,
    reviewed or draft, for its candidates, its comparison table and its standards list. The
    comparison table's *Different* rows say which differences the profile should look at most
    closely.
  - **The commercial work** in `commercial/`: the differentiation analysis, reviewed or draft, for
    the competitors named and the claims, by ID.
  - **Earlier profiles.** A predicate profile in `regulatory/`, reviewed or draft. If one exists,
    this run revises it: ask what has changed — a new device, a device replaced, new labeling, a
    new clearance, or only time — and keep every finding ID it already gave. Never renumber.
  - **Earlier research done outside MOS.** Teams often study their predicate before they run any
    skill: a comparison spreadsheet, notes from a sales rep or a clinician, a consultant's memo, a
    teardown, saved web pages. Look in `regulatory/` and `commercial/` for anything about the
    devices, whatever its name or format, and ask the user whether there is more elsewhere; if
    there is, ask for it by path and say why. Treat it as a company document: cite it by path,
    carry its findings forward with their sources, and check them against FDA's records and the
    labeling rather than redoing the work. Where it disagrees with what this run finds, say so and
    ask; do not overwrite it silently. Where it gives no source for a finding, keep the finding,
    mark it *Source not recorded*, and look for one.
  - **Labeling already saved** in `regulatory/labeling/`, and summaries in `regulatory/summaries/`.
    List the file names; read the ones for the devices chosen in step 2.

  Read Word documents with `python mos/lib/mosdocx.py read <file>`. Tell the user what you found and
  which of it is unreviewed. List contradictions; do not resolve them.
- **It does not exist** — say so, and say that running `setup`, `product-code` and
  `precedent-search` first will make this skill much better: they find and test the devices worth
  profiling. Then offer to continue from the conversation: you need the device to profile, and a
  description of the company's device good enough to judge resemblance.

**Offer clean copies of finished drafts.** For each `_draft` this skill reads, ask once:
*"Is the review of this document finished, and is it ready to route for signature?"* On a yes,
run `python mos/lib/mosdocx.py clean <file>`, show what it says it will do, and run it again with
`--apply` on a second yes. It writes the clean copy, `_revA`, without the working notes, and keeps
the full draft in `archive/`. If it refuses because of tracked changes or comments, say what to do
in Word first. MOS approves nothing: the clean copy becomes the record when it is signed in the
company's quality system. A draft that stays a draft is still read, and cited as unreviewed.

Anything you need outside the declared paths, ask for by name and say why. Write the answer back
to the context map so the question is not asked twice.

### 2. Choose the devices, and what each is for

Ask which device the user wants to study. Where they have not decided, recommend from what step 1
found, in this order:

1. **The primary predicate** in `precedent.md`, if a person has chosen one.
2. **The other predicates** in a multiple-predicate scenario, each for the part of the indications
   it covers.
3. **Reference devices** chosen for a technological difference.
4. **The top candidates** in the precedent search, where nobody has chosen yet — say plainly that
   profiling a candidate is not choosing it.
5. **A close competitor** from the differentiation analysis, where the question is commercial
   rather than regulatory.

For each device, agree on **its role and the question it answers**, in a sentence: *"The primary
predicate: what the new device must match, and what its users already expect."* *"A reference
device for the sensor: how its accuracy was specified and tested."* The question decides how
deep each area of step 6 goes. A reference device is studied for its difference, not profiled
end to end.

**Check resemblance** for every device the user names that the precedent search did not choose or
rank. Run `python mos/lib/openfda.py udi --brand "BRAND" --manufacturer "MAKER"` or look up its
number, and compare its product code, regulation and indications with the company's device. A
device under another regulation, for another body site or another condition, is a weak predicate
and may still be a good reference device or competitor; say which, and ask. If the user confirms
over the challenge, record it.

**Keep the set small.** One device is a good run. Three is the usual most. When the user asks for
more, ask what each extra device would answer that the others do not; where two answer the same
question, suggest the closer one. Above three, suggest a second run for the rest. Never more than
five in one run.

**On a re-run**, the user may add a device, replace one with an alternative, or refresh one. A
replaced device's section moves to an appendix with the reason, and its finding IDs are retired,
not reused.

### 3. Tell the user what will leave the machine

In one short paragraph: K, DEN and P numbers, brand names, manufacturer names and product codes go
to FDA's public database; document numbers go to FDA's website to download summaries. If the user
agrees to the web step, brand names, manufacturer names, model numbers and generic device words go
to the search service their AI uses, under that provider's terms, and the pages found are read from
the makers' and other public sites. Nothing about the company's device is sent.

### 4. Read FDA's records for each device

**Start from what is already gathered.** Before planning a single query, list for each device what
the context already holds, and from where:

- **The precedent search**, reviewed or draft: the device's indications word for word, its
  technology, the testing and standards its summary cites, its own predicate, its recalls and
  adverse event signals, and the date each search was run. Its search log says which queries were
  run; do not run them again.
- **Summaries** already in `regulatory/summaries/`, downloaded by `precedent-search`,
  `hazards-id` or an earlier run.
- **The hazards identification** in `context/risk/`, reviewed or draft: the adverse event
  problems, recalls and labeling it found for these devices by brand. Read only that; the rest of
  the risk file is not this skill's job.
- **The classification record and product code analysis**, for the code and regulation.
- **Earlier research** found in step 1.

Show that list beside the plan. Plan only what is missing: a record nobody has read, a device the
earlier work did not cover, or a search the user wants refreshed. A search run more than about
six months ago, or before a new clearance of the device, is worth refreshing for recalls and
adverse events; say so and let the user decide. Everything the profile takes from earlier work
cites that work, not a query of this run.

Show the planned commands, and run them on a yes:

```
python mos/lib/openfda.py fetch K212763 --out context/regulatory/summaries
python mos/lib/openfda.py udi --number K212763
python mos/lib/openfda.py udi --brand "UniVit" --manufacturer "Visioncare"
python mos/lib/openfda.py recalls --number K212763
python mos/lib/openfda.py problems --brand "UniVit" --manufacturer "Visioncare" --since 2021
```

- **The summary.** Look in `context/regulatory/summaries/` first; the precedent search may have
  downloaded it. Record the indications for use word for word, the device description, the
  technological characteristics, every specification it states, the performance testing and
  standards it cites, and its own predicate. If you cannot read PDF files, say so, list the
  summaries the user should read, and tell them this step works best with an AI that can read
  PDFs — Claude, for example. Do not guess at a summary's contents.
- **GUDID**, FDA's device identifier database. `udi --number` lists every model marketed under the
  clearance, with what the labeler recorded: prescription or over the counter, sterile and how,
  single use, latex, MRI safety, storage, sizes. `udi --brand` finds the other K numbers the brand
  is marketed under: later clearances of the same device are often its newer generations. Read
  the summary of the newest one that matters, and say which generation the profile describes.
  "Not stated" in GUDID means the field is empty, not no.
- **Recalls** by number are reliable. Read the root cause: design, labeling or manufacturing.
- **Adverse event reports** by brand are a signal, not a rate, and brand matching is loose. Use
  the narratives for how problems reach the user or patient.

For a reference device, read only what bears on its difference. For a De Novo grant or a PMA, the
decision summary or the summary of safety and effectiveness data takes the summary's place, and
its risks-to-health table or adverse events go to step 6's safety area.

If `python` is not found, use the command `setup` found — `python3` or `py -3`. If FDA cannot be
reached, say so, list the searches as plain instructions for FDA's databases, and continue.

### 5. Find and read the labeling and published material

**Ask first for what the company has.** Start from the labeling already saved in
`regulatory/labeling/`, and any labeling URLs the earlier work recorded; read those before searching
for more. Teams often hold a predicate's instructions for use from a sales rep, a conference or a
teardown. Suggest saving them in
`context/regulatory/labeling/<maker>-<brand>/`, one folder per device, kept apart from the company's
own labeling.

**Then offer the web, as its own step.** Say that it finds published instructions for use, user
manuals, specification sheets and product pages, that it sends brand names, manufacturer names,
model numbers and generic device words to the search service the AI uses, and ask whether to go
ahead. On a yes, list the searches and run them. Typical searches for one device:

- `"<brand>" "<maker>" instructions for use`
- `"<brand>" user manual pdf`, `"<brand>" operator's manual`
- `"<brand>" specifications`, `"<brand>" technical data sheet`
- `"<maker>" "<brand>"` for the product page
- for an implant or a Class III device sold in Europe, `"<brand>" summary of safety and clinical
  performance`, which EUDAMED publishes

Read sources in this order of weight, and label every finding with its tier:

| Tier | Source | What it is good for |
|---|---|---|
| 1 | FDA's summary and records | Indications, technology, testing, recalls |
| 2 | The US instructions for use, operator's manual and label | Use steps, warnings, contraindications, specifications, training, cleaning, storage |
| 3 | GUDID | Models, sizes, sterility, latex, MRI safety |
| 4 | The maker's specification sheets and product pages | Features, specifications, accessories |
| 5 | The maker's marketing: brochures, videos, press releases | Claims and the features the maker competes on |
| 6 | Others: published studies, distributor listings, reviews | Context; never a specification on its own |

Labeling found on the web may be out of date or for another market. Record for each document its
title, document number and revision where it has one, the market it is for, its URL and the date
read. Prefer the US version; where only another market's is found, say so on every finding that
rests on it. A labeling PDF the user wants kept is saved to the device's folder in
`context/regulatory/labeling/`, on approval of that write.

If this AI cannot search the web, say so, and ask the user to save what they can find into the
device's folder.

### 6. Profile each device

Fill each area from the sources, citing each finding. Go as deep as the device's question needs, and
say in each area where nothing was found.

| Area | What to record |
|---|---|
| Identity | Maker, brand, models, the clearance or approval numbers, product code, prescription or over the counter, which generation this is, whether it is still marketed |
| Indications and contraindications | From the US labeling, word for word, beside the summary's; any difference between them |
| Users, setting and training | Who uses it, where, what training the maker requires or offers |
| How it works | Principle of operation, energy source, software and connectivity, in plain words |
| Specifications | Each one stated, with value, unit, conditions and source: accuracy, range, size, weight, battery life, run time, shelf life, operating conditions |
| Use, step by step | Unpack and prepare, use, monitor, complete, hand off — the stages `user-needs` uses — and the steps the labeling gives for each, with the features that support them: controls, displays, alarms, indicators |
| Accessories and consumables | What it needs to work, what is sold separately, what it connects to |
| Safety information | Warnings, precautions, adverse events the labeling lists, sterility and reuse, cleaning and reprocessing, storage, latex, MRI safety |
| Testing and standards | What the summary and labeling say was tested, and to which standards |
| Field record | Recalls and their root causes; what adverse event reports describe |
| Claims | What the maker says about it, by source, as claims |

Then, for each device, compare with the company's device as the target product profile describes
it, area by area: **the same**, **different**, or **not yet decided** for the company. Where the
precedent search has a comparison table, check it against what the labeling shows. A specification
the summary did not state, or a labeling statement that contradicts the summary, is a finding.

### 7. Sort the findings into candidate inputs

The profile is a means. This step is what the later documents use. Give each finding that bears on
the company's device an ID, `PP-001` onward, and one kind:

| Kind | What it means | Where it goes |
|---|---|---|
| **Must match** | Substantial equivalence depends on it: the indications, or a technological characteristic the submission will argue is the same as the predicate's | `design-inputs`, as a constraint from outside the team, with this profile as its source |
| **Benchmark** | What the market already has: a specification, a feature, a time to set up. The team may match it, beat it or decide not to | A target product profile row to set or check, through the issues list; a *Proposed* value `design-inputs` may cite |
| **Use expectation** | How users of this device work, what they already know, what training they expect | `user-needs`, as a candidate need, worded as what the person must achieve, not as the feature |
| **Hazard** | A warning, contraindication, listed adverse event, recall or reported problem | `hazards-id`, with its source |
| **Labeling** | A statement the company's own labeling is likely to need, because the predicate's carries it | The company's labeling, when it is written; noted for `hazards-id` and `design-inputs` |
| **Testing** | A test, method or standard the device was shown to meet | `design-inputs` verification, and the standards list in the precedent search |
| **Claim** | Something the maker claims | `differentiation`, against the company's claims by ID |

For each candidate input, write what it is, its source and tier, which device it came from, and
why it matters to this device. Keep it to what the device must achieve or meet; never turn a
competitor's design into the company's. *"Its battery runs 12 hours on one charge (IFU, p. 34)"*
is a benchmark; *"use a 2,000 mAh lithium cell"* is a design choice and has no place here.

**Where the target product profile disagrees with a benchmark** — a minimum below what the
predicate already offers, a feature the predicate has that the profile does not mention — mark it
for step 8, with the row, what it says now and what the profile found. Do not change the target.

### 8. Put the target product profile rows to the team

The profile's benchmarks are mostly questions for the target product profile, and the team can
answer many of them now, while the evidence is in front of them. Say how many rows the findings
bear on, and offer to go through them. Then, one row at a time:

- **Show the row and the evidence**: what the row says now, what the predicate offers, its source
  and tier. Where several findings bear on one row, show them together.
- **Ask: keep the row, change it, or decide later?** *"The predicate's labeling gives 12 hours of
  battery life, and your minimum is 8. Keep 8, change it, or leave it for the team?"* Matching
  the predicate is one answer among several; beating it, or deciding not to compete on it, are
  others. Do not recommend a target; where the evidence is weak — a marketing figure, conditions
  not stated — say so.
- **For a change**, ask for the new value, at minimum or target, with its direction, and who is
  deciding. A decision needs a name; if the person in the session cannot make it, it is *decide
  later*.

Record each answer for step 10: a change becomes an issue line with `Decided:` and `Revise:` in the
form the context standard gives; *keep* becomes a line in the draft's working notes, so the next
run does not ask again; *decide later* becomes an open issue. The target product profile itself is
not touched: `setup` drafts its next revision once `issues-list` has closed the decided issues.

Leave out rows an earlier profile already put to the team, unless this run's evidence for them is
new: its working notes list each row and the answer. The user may stop at any point; every row not
yet asked about is *decide later*.

### 9. Write the draft

Fill `templates/predicate-profile.md`. Write dates in the Date format from
`context/templates/document-settings.md`, if it exists. The search log lists every query in order,
to FDA and to the web. Show the user the complete content. Confirm.

Save the filled template to `context/regulatory/predicate-profile.source.md` and run:

```
python mos/lib/mosdocx.py render --in context/regulatory/predicate-profile.source.md --out context/regulatory/predicate-profile_draft.docx --title "Predicate Profile — <device>" --remove-input
```

Where a reviewed `predicate-profile_rev*.docx` is already there, name the draft for the revision
after it instead — `predicate-profile_revB_draft.docx` beside `predicate-profile_revA.docx` — in the
command and everything below.

If `predicate-profile_draft.docx` already exists, the script refuses to overwrite it. Show what
changed and ask; add `--force` only on a yes. If the script cannot run, write the filled template to
`context/regulatory/predicate-profile_draft.md` instead, and say that Word output needs the step in
`setup`.

Tell the user how the draft becomes the record: review and redline it in Word, then accept or
reject every change and delete the comments. When the review is finished, make the clean copy: the
next MOS skill run offers it, or run `python mos/lib/mosdocx.py clean <draft> --apply`. It writes
`predicate-profile_revA.docx`, or `_revB` for a `_revB_draft`, without the working notes, and moves
the full draft, and the revision it replaces, into `archive/`. The clean copy goes for signature,
and becomes the record when it is signed in the company's quality system. Until then, later skills
read the draft and say it is unreviewed.

Then say which skills the candidate inputs feed, by kind and count — *"14 benchmarks for the target
product profile, 9 hazards for `hazards-id`, 6 use expectations for `user-needs`"* — and suggest
running them next.

### 10. Hand off the issues

List what this session found and did not settle: a device confirmed over a resemblance challenge;
labeling that could not be found, or was found only for another market; a summary and labeling that
disagree; target product profile rows the profile bears on — a minimum below the predicate's, a
feature or user group the profile does not mention — each with what the row says now and what the
profile found; a must-have claim the predicate's maker already makes. For each, give its type
(question, conflict, gap, assumption, risk to the plan), its domain, what it blocks and the next
step. Check the current issues list — the newest `<YYMMDD>_issues-list.docx` in `context/` — and
leave out what is already on it, unless this session found something new about it.

Show the list. On a yes, write it to `context/inbox/<YYMMDD>_issues_predicate-profile.md`, in the
format the context standard gives, including the decided rows from step 8 with their `Decided:`
and `Revise:` lines. Then ask the user to run `issues-list` now, while this session still holds what
was found. Where step 8 decided any changes, say what follows: `issues-list` logs them as closed,
and `setup` then drafts the next revision of the target product profile from them, for the team to
review. Never edit the issues list or the target product profile. If nothing is unsettled and
nothing was decided, say so and write no note.

## Working at three levels of context

| What the company has | How this skill behaves |
|---|---|
| Nothing | Asks which device to study and what the company's device is, checks resemblance from FDA's records before profiling, and explains each step in plain words — what a predicate is, why its labeling matters. Comparisons with the company's device are marked as from the conversation, and the draft says `precedent-search` would test the choice |
| Some files | Starts from the chosen or candidate predicates and the target product profile, says which are unreviewed, and profiles the devices the user confirms. Sorts findings against the target product profile's rows |
| A full document set | Checks the precedent search's comparison table against the labeling, finds newer generations and clearances of the chosen devices, sorts findings against the target product profile, and flags contradictions between the profile, the precedent record and the claims rather than resolving them |

## Interviewing style

- One question at a time.
- Ask what the team wants to learn from each device before searching. The answer sets the depth.
- When the team says they already know a device well, ask where from: a sales rep, a clinician who
  uses it, a teardown. Record it, and look for the labeling anyway.
- Ask what the people who use the predicate today complain about. It is often the opening the new
  device is built on, and no document records it.

## Boundaries

This skill does not choose a predicate or a reference device, argue substantial equivalence, set
the target product profile's targets, or write user needs, hazards or design inputs. It does not
search patents, which are a separate question with a wider scope, and it does not judge freedom to
operate. It does not buy, request or reverse-engineer a device. It reads FDA's public records,
labeling the user supplies, and what the web finds on the user's approval; a maker's published
material is that maker's account of its own device.

## Where this skill is weakest

Recorded so it gets fixed rather than rediscovered:

- Many makers do not publish their instructions for use, or publish them behind a login. Then the
  profile rests on FDA's summary and marketing, and the use steps and warnings are thin.
- Labeling on the web is often an older revision or another market's version, and not always
  dated.
- GUDID is filled in by each labeler, unevenly. An empty field says nothing.
- Specifications in marketing are often measured under the best conditions, and the conditions are
  rarely stated.
- A device that has changed since its clearance may be sold under the same K number; the profile
  can describe a generation that is no longer on the market, and says which it describes.
