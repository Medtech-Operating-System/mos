---
name: design-inputs
description: Draft the design inputs for a medical device — the verifiable requirements its design must meet — from its user needs, hazards, target product profile, precedent and standards, each traced to its source. Use when a team needs design inputs drafted, converted from a requirements document or spec, or reviewed.
version: 0.2.0
maintainer: Eric Sugalski
phase: [01-definition, 02-design]
discipline: [technical, quality, regulatory]
reads:
  - context/context-map.md
  - context/*_issues-list.*
  - context/product/**
  - context/users-and-needs/**
  - context/risk/**
  - context/regulatory/**
  - context/design/**
  - context/templates/**
writes:
  - context/design/
  - context/inbox/
status: draft
---

# Design inputs

Turns what a device must achieve for people into what the device itself must do and be, stated so
each can be verified. Every design input traces to where it came from: a user need, a hazard, a
risk control, the target product profile, a special control, the predicate, a standard. The
output is a Word document in `context/design/`, built from the company's template: a draft for
review, not a controlled record.

Read `mos/context-standard.md` before starting if you have not already, then read
`context/context-map.md` to find out what you are allowed to read.

## The thing this skill is actually for

**Design inputs say what, not how.** *The device shall apply at least 40 N of compression to the
limb* is a design input. *Motor torque ≥ 0.4 N·m* is a decision about one way of building it: a
design output, which belongs in the specifications. A design input that names a part locks the
design before anyone has designed it, and turns every later change of part into a change of
requirement.

**Every design input costs a verification.** Each row is a test, an inspection, an analysis or a
demonstration someone will have to run and document. A row with no source is work nobody asked
for. A user need with no design input is a gap that surfaces at validation, when it is most
expensive to close.

**The trace is the point.** A reviewer, an auditor and FDA all ask the same question of a design
input: *why is this here?* The Sources column answers it on every row.

## Rules for this skill

- **Design inputs are about the device, never about people.** No row names a person, and the
  rows, the sections and the questions are never organized by user group. Users enter only as
  the source of the user needs a row traces to. What a person must achieve stays in the user
  needs; the design input states what the device must do or be so they can achieve it.
- **No embodiments, except constraints from outside the team.** A row may not name a part, a
  material, a mechanism or a technology, unless the choice is not the team's to make: a standard
  requires it, the device must work with equipment already in use, the regulatory argument
  depends on matching the predicate, or a customer or contract requires it. Such a row's
  rationale names where the constraint comes from. If the only answer is *that is our design*, it
  is a design output and comes out.
- **Never open a standard.** Do not read any file in `context/regulatory/standards/`. This skill
  names standards from the precedent search's list and reads the company's own design input
  document for each standard, which `standards-requirements` writes. Do not work from what you
  may remember of a standard's text, and never reproduce a standard's text or tables.
- **Never invent a number.** A value comes from the target product profile, the team, or cited
  evidence — a predicate's summary, a special control, a guidance document — marked *Proposed*.
  Where there is none, write `Not set yet`. A plausible number nobody chose looks like a decision
  and is not one.
- **Do not propose risk controls of your own.** Safety rows come from a risk analysis, or from
  controls FDA, a standard or a predicate already names. Every other hazard waits for the risk
  analysis, on the issues list.
- **Do not renumber existing IDs.** Ever. Retire an ID instead. In Review mode, new rows continue
  the company's own ID scheme.
- **Do not edit another skill's document.** A line that belongs in the user needs, the hazard list
  or the target product profile goes on the issues list, naming the skill to run.
- **Do not write into `context/`** without approval of that specific write.
- **Sends nothing outside.** This skill reads only the company's context. It runs no searches;
  what it needs from FDA's records, the precedent search has already saved.
- **Plain words first, the term beside them.**

## The phrasing rule

Every design input is written as:

> **The device shall [what it must do or be, observable at its boundary].**

- **Subject** is the device, or the part of the product the row is about: its labeling, its
  packaging, an accessory, the software as a whole where the device is software. Never a person:
  what a person must achieve is a user need.
- **Shall**, one requirement per row. A row joined by *and* is usually two rows.
- **At the boundary**: what the device does to the patient, the user and its surroundings, and
  what they can observe or measure. Not what happens inside it.
- **The acceptance criterion is separate.** The requirement says what is needed; the criterion
  says how to tell it was met, with its conditions:

| Requirement | Acceptance criterion |
|---|---|
| The device shall deliver therapy for a full night on one charge. | ≥ 8 h at maximum output, from full charge, at 23 °C |
| The device shall not burn the skin it touches. | Applied-part surface ≤ 43 °C after 8 h continuous use, at 35 °C ambient |
| The labeling shall state the conditions the device can be stored in. | Inspection: storage temperature and humidity ranges on the label and in the instructions for use |

### Screen every row

Rewrite any row that names:

- a part — *motor, battery, sensor, valve, housing, cartridge, screen*
- a technology or protocol — *Bluetooth, NFC, touchscreen, piezoelectric*
- a material — *titanium, silicone, PEEK*
- an internal value — *torque, clock speed, cell capacity, wall thickness*
- a user interface element — *button, LED colour, alarm tone, icon*

Ask what it achieves at the boundary, and write that:

| Raw line | Design input |
|---|---|
| 2,000 mAh battery | The device shall deliver therapy for a full night on one charge. |
| Titanium housing | The device shall withstand a 1 m drop onto concrete without loss of function. *And:* The device shall be MR Conditional at 1.5 T and 3 T. |
| Bluetooth to the phone app | The device shall transfer each session's record to the patient's phone without manual entry. |
| Red LED when battery low | The device shall indicate low battery before it can no longer complete a session. |
| Luer connector to the IV line | *Kept as a constraint:* The device shall connect to standard IV administration sets. Rationale: interoperability with sets already in use. |

### Two sections that border other documents

- **User interface** holds what a person meets on the device, verifiable on the device itself:
  *operable with gloved hands*, *readable at 1 m in 300 to 1,000 lux*, *controls resist
  accidental activation*. IEC 62366-1 calls this the user interface specification. What the
  person must achieve with it stays in the user needs.
- **Security** holds device-level security requirements: *the device shall prevent unauthorized
  changes to therapy settings*, and physical access such as ports. How the software meets them —
  protocols, encryption, authentication methods — belongs in the software requirements
  specification, which traces back to these rows. The software bill of materials and the
  end-of-support date are labeling rows. Leave the section out for a device with no software or
  connection.

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

- **It exists** — read it, then read:
  - **The target product profile** — the newest `target-product-profile_rev*.docx` in
    `context/product/`, or, unreviewed, `target-product-profile_draft.docx` — for the intended
    use, the users and settings, and every row with a value: clinical and technical performance,
    the device's life, usability, the regulatory expectations.
  - **The user needs** in `users-and-needs/`: each need's ID, its use stage, whether it is
    safety-critical, and the hazards it cites.
  - **The risk file** in `risk/`: the hazards identification, and any risk analysis — a MOS
    risk analysis, or the company's own hazard analysis, design FMEA or risk table — with its
    risk controls and their IDs.
  - **The regulatory work** in `regulatory/`: the classification record, and the precedent
    search, for its special controls, its guidance, its standards list, its comparison table and
    the predicate and reference devices it names; and the predicate profile, reviewed or draft,
    for its candidate inputs. Do not open `regulatory/standards/`.
  - **The design folder**, `design/`: any existing design inputs, and any design input document
    for a single standard, `design-inputs-<standard>_*.docx`.

  Read Word documents with `python mos/lib/mosdocx.py read <file>`. Tell the user what you found.
- **It does not exist** — say so, and say that running `setup` and `user-needs` first will make
  this skill much better, because design inputs answer user needs and the target product profile.
  Then offer to continue from the conversation alone.

**Offer clean copies of the drafts this work rests on.** A design input should trace to a
reviewed user need, not a working draft. For each document read that is still a `_draft` — the
user needs, the hazards identification, the target product profile, the precedent search — ask:
*"Is the review of this document finished, and is it ready to route for signature?"* On a yes,
run `python mos/lib/mosdocx.py clean <file>` without `--apply`, show what it says it will do, and
run it with `--apply` on a second yes. It writes the clean copy, `_revA`, without the working
notes, and keeps the full draft in `archive/`. If it refuses because of tracked changes or
comments, say what the user must do in Word first. MOS approves nothing: the clean copy becomes
the company's record when it is signed in their quality system, and MOS records none of that. A
draft that stays a draft is still read, and cited as unreviewed.

**Where earlier design inputs exist,** ask which they are: a draft from an earlier run, to be
revised; or the company's own controlled design inputs, which means Review mode. For a draft from
an earlier run, ask whether its review is finished, and offer a clean copy as above. Before
cleaning one, read it for the word *Proposed*: each one left is a value the team has not
confirmed, so ask about them first.

**Where the team brings other documents** — a product requirements document, a spec sheet, a
design description, a feature list — ask for each by path and read it. Whatever it is called,
it is source material, not a mode. If it has been reviewed and approved as the company's design
inputs, it is the existing design inputs, and the mode is Review.

If documents disagree — the user needs and the target product profile name different users, a
brought spec contradicts a TPP value — list the contradictions. Do not pick one.

Anything you need outside the declared paths, ask for by name and say why. Write the answer back
to the context map so the question is not asked twice.

### 2. Confirm the mode

| Mode | When |
|---|---|
| **Draft** | No controlled design inputs yet. Builds them from every source, steps 3 to 9 |
| **Review** | The company already has design inputs under design control. Keeps every ID, checks each row against the rules in step 8, then checks coverage in step 7 and proposes rows only where a real gap is found |

Confirm before going on. If it is unclear, ask: *"Has this document been reviewed and approved as
your design inputs, or is it a working list?"*

### 3. Confirm what the design inputs answer

Set out, from the target product profile: the intended use, the indications, the users, the
settings, and the device in a sentence. Test it before building on it: where the intended use is
too vague to derive a requirement from, or a user group or setting in the user needs is missing
from it, say so, show why, and ask the user to reconsider. Once they confirm it, build on it as
written, and record that it was confirmed over the challenge.

Where there is no target product profile, build this from the conversation, mark it so, and say
that `setup` would write one.

### 4. Gather the candidate rows, source by source

Work through the sources in this order. A row that answers several sources is one row with
several sources, not several rows: merge as you go.

**a. User needs.** For each need, ask what the device must do or be so the person can achieve
it. The person drops out; the device becomes the subject:

| User need | Design input |
|---|---|
| The clinician shall not miss an interruption in therapy. | The device shall indicate an interruption in therapy within 10 s, perceivable from 3 m. |
| The reprocessor shall be able to make the device safe for the next patient. | The device shall withstand [N] cycles of the specified disinfection process without loss of function. |
| The technician shall be able to confirm the system works on the site's network. | The system shall report whether its network connection meets the conditions it needs to operate. |

Work need by need, and place each row in the section its device characteristic belongs to. Do
not group needs, rows or questions by user group: a reprocessor's need and a clinician's need
may land in the same section, and one need may give rows in several. Most needs give one to
three rows. A need the device cannot answer by itself — one met by
training, or by the clinical setting — has no design input; record why in the coverage table.

**b. The target product profile.** Each row with a value in clinical performance, technical
performance, the device's life, usability or regulatory expectations is a design input or part of
one. The acceptance criterion is the **minimum acceptable**; the **target** goes in the rationale
as a design goal. Service life, shelf life and manufacturability become rows; they shape design
and can be verified. Price, volume and cost of goods do not: they stay in the target product
profile, which this skill does not edit.

**c. Hazards and risk controls.** Safety rows come from three sources, in this order:

1. **A risk analysis**, MOS's or the company's own. Each risk control that is a design measure or
   a protective measure becomes a row, citing the control's ID. A control that is *information
   for safety* — a warning, an instruction — becomes a labeling row. These are not provisional.
   Where a control looks weaker than what a special control or a standard named in the precedent
   search requires, say so and ask.
2. **Controls an outside source already names**, for hazards no risk analysis covers yet: a
   special control, the mitigation column of a De Novo's risks-to-health table, a predicate's
   testing, a standard the precedent search links to the hazard. Each becomes a row marked
   *Yes, provisional*, citing the hazard and the source. These hold whatever the risk analysis
   later concludes, which is why they can be written now.
3. **Every other hazard** waits for the risk analysis. List it in the coverage table as
   *Awaiting risk analysis*, and on the issues list. Do not write a control for it.

Hazards the user needs marked *Design inputs, not a user need* — leakage current, a leachable
chemical — belong here, through one of the three.

**d. Special controls and guidance.** Each special control from the precedent search becomes one
or more rows; quote the special control in the Sources column, since it is public law. Where a
guidance document names a performance expectation, cite it as the source of a *Proposed* value.

**e. The predicate comparison.** Walk every row of the precedent search's comparison table, for
the primary predicate and each reference device. For each row, decide whether it describes a
requirement — *accuracy ±3% SpO₂ from 70 to 100%* — or a design output — *titanium housing*.

- A requirement becomes a row, or adds a source to one.
- A design output is never a row. Ask what it achieves for that device: strength, MR safety,
  biocompatibility, weight. Make sure a design input states that requirement, adding one if none
  does, and record the design output against it. When the specifications exist, they fill the
  subject device's column of the 510(k) comparison from the traced rows.

Nothing on a comparison table is left without a requirement behind it. Where there is no
precedent search, say that `product-code` then `precedent-search` would add it, and go on.

**The predicate profile.** Walk its candidate inputs, by kind, citing each by its `PP-` ID:

- **Must match** — a constraint from outside the team: a row, or a source added to one. The
  rationale says substantial equivalence depends on it.
- **Benchmark** — never a row by itself. Where a row already covers it, the benchmark goes in the
  rationale: what the predicate offers, and whether the acceptance criterion meets it. Where the
  target product profile sets no value, it may be the source of a *Proposed* value, in step 5.
  Where no row covers it and the team wants to compete on it, it goes on the issues list for the
  target product profile; the row follows once the profile has the target.
- **Testing** — the verification method on the rows it verifies, as for a test-method standard.
- **Hazard** and **Labeling** — reach this document only through the risk work in c. A
  predicate's warning is evidence of a hazard, not the company's risk control.

A profile finding that describes the predicate's design — its material, its cell, its mechanism
— is a design output of that device, and is treated like one on the comparison table: ask what it
achieves, and state that.

**f. Standards.** From the precedent search's standards list, sort each standard into one of
three kinds:

| Kind | Examples | What it becomes |
|---|---|---|
| **Product** | IEC 60601-1 and its collateral and particular standards; device-specific standards | One row in the Standards section: *The device shall conform to [standard, edition]* |
| **Test method** | ISO 10993-5, ASTM F1980, ISO 11607-1 | The verification method on the rows it verifies, not a row of its own |
| **Process** | ISO 14971, IEC 62366-1, IEC 62304, ISO 13485 | Listed in the working notes for the design and development plan; not a design input |

For each product standard's row: where `design/` holds that standard's design input document,
`design-inputs-<standard>_rev*.docx` or a `_draft`, the acceptance criterion is *conformity to
every clause marked applicable in* that document, at its revision; cite a draft as unreviewed.
Lift into the main table any row in it that the team marked as driving the design or that meets
another design input — an alarm clause beside a need about alarms — citing the standard's
document as its source. Where there is no such document, the criterion is *Applicability not
assessed*, and the issues list says to run `standards-requirements` for that standard.

**g. Documents the team brought.** Sort every line by what it is, not what the document is
called:

| A line that is… | Example | Where it goes |
|---|---|---|
| Something the device must do, verifiable at its boundary | *Runs 8 h on a charge* | A row, citing the document |
| A decision about how | *Aluminum housing*, *2,000 mAh cell* | Set aside as a design output, against the row it serves; kept only if it passes the outside-constraint test |
| An outcome for a person | *Clinicians must see status at a glance* | Set aside; on the issues list for `user-needs` if no need covers it |
| A product target | *Weight under 300 g*, *cost of goods under $45* | Set aside; on the issues list for `setup` if the target product profile lacks it. Until it is there, a row may cite the document directly |
| A wish nobody can test | *Best-in-class experience* | Set aside, with the reason |

### 5. Set the acceptance criteria

For each row, in order of preference:

1. **The team's value**, from the target product profile's minimum or from the interview.
2. **A Proposed value from cited evidence**: a predicate's tested figure, a specification in the
   predicate profile, a special control, a guidance document, a published study the team names.
   A profile specification is cited by its `PP-` ID and source tier; one from the maker's
   marketing or a third party, tiers 5 and 6, never sets a value on its own. Write *Proposed:* before the value, and
   the source in the rationale.
3. **`Not set yet`**, and the row goes on the issues list. The row stays in the table: a design
   input with no number yet is still a design input, and the gap stays visible.

State the conditions with the value: temperature, duration, load, the population measured.
Ask for values the team may know, one question at a time.

### 6. Check every row

Before showing the draft, check each row:

- The subject is the device or a part of the product, and it says *shall*.
- One requirement. Split rows joined by *and*.
- The acceptance criterion can be measured or observed, with conditions, or is `Not set yet`.
- No part, material, mechanism or technology, unless it passes the outside-constraint test with
  its source in the rationale.
- It is not a user need in other words: a row a person must achieve belongs in the user needs.
- It has at least one source. A row with none is flagged to the user: delete it, or name the
  input it answers.
- No other row says the same thing. Merge.

### 7. Check coverage

Fill the coverage table in the working notes. Every user need, hazard, special control, target
product profile value and product standard is answered by at least one row, or carries its
reason: met without a design input, awaiting risk analysis, or a gap. Every gap goes on the
issues list in step 10. Do not add a row only to fill a cell.

### 8. Test what the user brings

In Review mode, and for every design input the team brought: check each row against steps 6
and 7, and report it as `ID | Finding | Action` — keep, rewrite (with the rewrite), merge with,
move to the specifications, or delete. Where the team's requirement disagrees with the evidence —
a battery life below the predicate's, a value looser than a special control, a row that names a
part the team believes is a constraint — say so plainly, show the evidence, and ask the user to
reconsider. Where they confirm their direction after hearing it, accept it, and record in the
challenges table that it was confirmed over the challenge.

Never renumber. New rows continue the company's scheme.

### 9. Write the draft

Fill `templates/design-inputs.md`. Write dates in the Date format from
`context/templates/document-settings.md`, if it exists. Everything under `## Working Notes` is
for the reviewers and is left out of the clean copy that goes for signature; keep it the last
section. Show
the user the complete content. Confirm.

Save the filled template to `context/design/design-inputs.source.md` and run:

```
python mos/lib/mosdocx.py render --in context/design/design-inputs.source.md --out context/design/design-inputs_draft.docx --title "Design Inputs — <device>" --remove-input
```

Where a reviewed `design-inputs_rev*.docx` is already there, name the draft for the revision
after it instead — `design-inputs_revB_draft.docx` beside `design-inputs_revA.docx` — in the
command and everything below.

If `design-inputs_draft.docx` already exists, the script refuses to overwrite it. Show what
changed and ask; add `--force` only on a yes. If `python` is not found, use the command `setup`
found — `python3` or `py -3`. If the script cannot run, write the filled template to
`context/design/design-inputs_draft.md` instead, and say that Word output needs the step in
`setup`.

Tell the user how the draft becomes the record: review and redline it in Word, confirm or change
each *Proposed* value and delete the word, accept every change and delete the comments. Then the
clean copy: the next MOS skill run asks whether the review is finished and runs `mosdocx.py
clean`, which writes `design-inputs_revA.docx` without the working notes and keeps the full draft
in `archive/`. The clean copy is what goes for signature; it becomes the record when it is signed
in the company's quality system. Where the company files records there, file it there with the
context map pointing at it. The next revision goes the same way: a `_revB_draft`, reviewed, then
cleaned.

### 10. Hand off the issues

List what this session found and did not settle: rows with `Not set yet` criteria; hazards
awaiting risk analysis; product standards with applicability not assessed; user needs and special
controls no row answers; lines from brought documents that belong in the user needs or the target
product profile, each with what it says and the skill to run; contradictions between documents;
and design outputs that may be constraints nobody has confirmed. For each, give its type
(question, conflict, gap, assumption, risk to the plan), its domain, what it blocks and the next
step. Check the current issues list — the newest `<YYMMDD>_issues-list.docx` in `context/` — and
leave out what is already on it, unless this session found something new about it.

Show the list. On a yes, write it to `context/inbox/<YYMMDD>_issues_design-inputs.md`, in the
format the context standard gives. Then ask the user to run `issues-list` now, while this session
still holds what was found. Never edit the issues list, the user needs, the hazard list or the
target product profile. If nothing is unsettled, say so and write no note.

## Working at three levels of context

| What the company has | How this skill behaves |
|---|---|
| Nothing | Builds the intended use from the conversation, then interviews for what the device must do, one area at a time, explaining what a design input is, why it says what and not how, and why every row needs a source and a way to verify it. Most criteria are `Not set yet`. The draft says that `setup`, `user-needs`, `hazards-id` and `precedent-search` would each give it sources |
| Some files | Works from the target product profile and the user needs, takes safety rows from the hazard list where outside sources name controls, and interviews for values. Says which rows came from documents and which from the conversation |
| A full document set | Traces every row to approved user needs, risk controls, special controls, the predicate comparison and each standard's design input document. Mostly a check of coverage and of the team's own rows, flagging contradictions rather than resolving them |

## Interviewing style

- One question at a time.
- When the team names a part, ask what it achieves. Write the answer, not the part.
- When the team says a part is fixed, ask who fixed it. A standard, a customer or the predicate
  is a constraint; the team's own preference is a design output.
- Ask for numbers with their conditions: *8 hours, at what output, at what temperature?*
- Treat "we haven't decided" as a finding: `Not set yet`, on the issues list.

## Boundaries

This skill does not write specifications or choose an architecture, propose risk controls of its
own, read standards, write a software requirements specification, plan or run verification, or
write user needs. It does not edit the user needs, the hazard list, the risk analysis or the
target product profile; it says what each is missing.

## Where this skill is weakest

Recorded so it gets fixed rather than rediscovered:

- Without a risk analysis, most hazards have no safety row yet, and the draft is thin exactly
  where a reviewer looks first. It says so; it does not fill the gap.
- The line between a constraint and a design output is a judgement. The skill asks who fixed a
  part, but cannot check the answer.
- *Proposed* values from a predicate show what was cleared, not what this device needs. A team
  that accepts them unread inherits another company's choices.
- Software requirements, subsystem specifications and the trace onward to design outputs and
  verification are not here yet. The coverage table checks one direction only: from inputs to
  design inputs.
