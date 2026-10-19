---
name: user-needs
description: Draft user needs for a medical device from a company's existing context, interviewing for what is missing. Use when a team needs user needs captured, converted from notes, or reviewed for gaps.
version: 0.7.0
maintainer: Eric Sugalski
phase: [01-definition]
discipline: [clinical, technical]
reads:
  - context/context-map.md
  - context/*_issues-list.*
  - context/product/**
  - context/users-and-needs/**
  - context/risk/**
  - context/regulatory/predicate-profile*    # the profile only; no other regulatory work
  - context/templates/**
writes:
  - context/users-and-needs/
  - context/inbox/
status: draft
---

# User needs

Produces a compact set of user needs for a medical device, written so that each one can be
validated. The output is a Word document in `context/users-and-needs/`, built from the company's
template — a draft for review, not a controlled record.

Read `mos/context-standard.md` before starting if you have not already, then read
`context/context-map.md` to find out what you are allowed to read.

## The thing this skill is actually for

**Compact beats comprehensive.** Every user need eventually requires validation through a clinical
study or a human factors evaluation. More needs does not mean better coverage — it means more
validation cost and more chance that a failed validation blocks a submission. The goal is the
smallest set that covers safety, effectiveness, workflow fit and patient experience. Merge
overlapping needs. Delete decorative ones. A well-scoped device usually lands at 10–25 needs.

A candidate that cannot survive *"what validation activity proves we met this?"* is not a user
need. It is redundant, too vague, or a design input wearing a costume.

## Rules for this skill

- **Do not write into `context/` without approval of that write.** The draft goes to
  `context/users-and-needs/`, named `_draft`, once the user has seen it. When the interview produces
  something that belongs in the company's context — a use environment nobody had written down, an
  agency comment about the population — offer to write it, name the file, and let the user decide.
- **Do not invent needs to fill a gap.** An empty cell in the coverage matrix is either out of
  scope, which you say, or a real gap, which goes on the issues list in step 10. Padding a list to look thorough is the
  failure mode this skill exists to prevent.
- **Do not renumber existing IDs.** Ever, for any reason. Retire an ID instead.
- **Do not resolve contradictions silently.** If the risk file and the device description disagree
  about who uses the device, say so and ask. Picking one is not your call.
- **Do not edit the hazard list.** A need that reveals a hazard the list does not have goes on the
  issues list in step 10, with the suggestion to run `hazards-id` again.
- **A need answers a hazard with an outcome, not a control.** *"The clinician shall not miss an
  interruption in therapy"* answers a hazard; *"the pump shall alarm"* is a risk control, and belongs
  to the hazard analysis and the design inputs.
- **Test the intended use before building on it.** An intended use from the target product profile or a
  company document is the anchor for every need, so read it critically first. Where it is too
  vague to validate against, names a user group the rest of the context does not support, or
  leaves out a use the interview reveals, say so, show why, and ask the user to reconsider. Once
  they confirm it, build on it as written, and note in the draft that it was confirmed over the
  challenge.
- **Do not reproduce text from ISO, IEC or AAMI standards.** Clause numbers are fine. Clause text
  is not, however much paraphrase surrounds it.

## The phrasing rule

Every user need is written as:

> **The [person-role] shall [outcome-based verb phrase].**

- **Subject** is a person or role — user, patient, physician, clinician, operator, caregiver,
  nurse, technician, reprocessor, service tech, purchaser. **Never** the device, system, software
  or product.
- **Modal verb** is **shall**. Not "needs to," "should," "must," "wants" or "requires."
- **One need per statement.** No compound sentences joining two distinct outcomes with "and." A
  scoped list of alternatives inside a single outcome is fine.
- **Describes an outcome** — what the person is able to do, experiences, receives, perceives or
  avoids. Not a prescribed action, not a work-instruction step.

### Outcome verbs, not action verbs

The single most common drafting error, and experienced drafters fall into it constantly. Even with
a person as the subject, a verb that prescribes a specific action — "shall apply," "shall remove,"
"shall complete" — reads as a device-centric work instruction rather than a need.

| Outcome type | Use when | Template |
|---|---|---|
| **Capability** | The user must be able to do something | The [role] shall **be able to** [action]. |
| **Experience** | The user must experience something | The [role] shall **experience** [outcome]. |
| **Receipt** | The user must receive or have available information, confidence, confirmation or value | The [role] shall **receive** / **be made aware** / **have available** [X]. |
| **Perception** | The user must perceive or distinguish something | The [role] shall **be able to recognize / distinguish / identify** [X]. |
| **Avoidance** | The user must avoid an adverse outcome | The [role] shall **not experience** / **not need to** / **not miss** [outcome]. |

**Reject bare action verbs** as the predicate — *apply, complete, initiate, remove, prepare,
access, compare, retrieve, use, place, perform, clean*. They read as SOP steps and are hard to
validate, because there is no measurable outcome, only a procedural step.

| Instruction-style (reject) | Outcome-style (accept) |
|---|---|
| The operator shall attach the device to the patient. | The operator shall **be able to obtain** a clinically usable reading on the first attempt. |
| The physician shall access the results. | The physician shall **be able to view** completed results at the point of care. |
| The caregiver shall complete setup within 3 minutes. | The caregiver shall **be able to complete** setup within the available visit window. |
| The operator shall remove the device. | The patient shall **not experience** discomfort when the device is removed. |
| The patient shall tolerate the procedure. | The patient shall **not experience** physical discomfort during the procedure. |

### Keep roles broad

Use the most general role that preserves the meaning of the outcome. Specific job titles narrow the
need unnecessarily and can force a validation study to recruit from an artificially narrow pool.
They also date quickly — who operates a device varies by site and changes over time.

| Too narrow | About right |
|---|---|
| The nurse or technician shall… | The **clinician** shall… |
| The interventional cardiologist or radiologist shall… | The **physician** shall… |
| The RN shall… | The **operator** shall… |
| The sterile-processing tech shall… | The **reprocessor** shall… |

Preserve specificity only where the outcome genuinely depends on the role: **patient** where the
subject of care is the stakeholder, **physician** where the outcome requires a specific scope of
practice, **caregiver** where the outcome specifically involves a non-clinical care provider.

Never write "the nurse or technician" or "the RN or LPN." Listing titles means you need an umbrella
term instead.

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

- **It exists** — read it. Read whatever it maps under `product/`, `users-and-needs/` and `risk/`.
  Tell the user what you found and what you are working from. Read Word documents with
  `python mos/lib/mosdocx.py read <file>`; it shows tracked changes as if accepted and says how
  many there are, which is worth telling the user — an unaccepted redline is not yet a decision.
  A reviewed user needs document, `user-needs_revB.docx` for example, is the current list and
  the starting point for Mode C.
  - **The hazard list.** If `risk/` holds a hazards identification — the newest
    `hazards-id_rev*.docx`, or, unreviewed, `hazards-id_draft.docx` — read its hazard list: each
    hazard's ID, its harm, its use stage and its last column, which names the user need that
    answers it or says none does. Those hazards are where safety-critical needs start, in step 4.
    If there is none, say that running `hazards-id` first gives the risk questions evidence from
    similar devices rather than memory, and offer to continue without it.
  - **The predicate profile.** If `regulatory/` holds one — the newest
    `predicate-profile_rev*.docx`, or, unreviewed, `predicate-profile_draft.docx` — read its
    candidate inputs of kind *Use expectation*, and its use steps for each device. They say how
    users of the device the company will be compared with already work, in step 4. Read nothing
    else in `regulatory/`.
  - Drafts sit beside the records in each domain, named `_draft`. Read them too. An earlier user needs draft that nobody cleaned is still the best starting point there is;
    say it is unreviewed, and where it disagrees with a reviewed document, the reviewed document
    wins and you ask. A draft older than the reviewed revision it would replace is superseded;
    ignore it.
- **It does not exist** — say so, and say that running the `setup` skill first will make this skill
  better. Then offer to continue anyway from the conversation alone. Do not refuse to work.

**Offer clean copies of finished drafts.** For each `_draft` this skill reads, ask once:
*"Is the review of this document finished, and is it ready to route for signature?"* On a yes,
run `python mos/lib/mosdocx.py clean <file>`, show what it says it will do, and run it again with
`--apply` on a second yes. It writes the clean copy, `_revA`, without the working notes, and keeps
the full draft in `archive/`. If it refuses because of tracked changes or comments, say what to do
in Word first. MOS approves nothing: the clean copy becomes the record when it is signed in the
company's quality system. A draft that stays a draft is still read, and cited as unreviewed.

Anything you need that sits outside the declared paths, ask for by name and say why. Write the
answer back to the context map so the question is not asked twice.

### 2. Confirm the mode

Ask which of three, and confirm before drafting anything. If it is unclear, default to A.

| Mode | When | What changes |
|---|---|---|
| **A — Interview** | A clinical problem, no drafted needs | Run steps 3–6 in full |
| **B — Convert** | Workshop output, interview notes, a feature wishlist | Skip the interview. Apply the screening in step 5 aggressively — most raw notes are solutions in disguise |
| **C — Gap-fill** | An existing list to stress-test | Apply the coverage matrix in step 6 and the review checklist in step 9. Propose additions only where a real validation gap exists. Flag redundancies for merger |

### 3. Write the intended use anchor

Before drafting any need, capture and confirm in writing:

1. **Intended use / indications for use** — one paragraph. Patient population, clinical condition,
   clinical purpose, use environment envelope, user profile.
2. **Primary users** — role, training level, expected frequency of use.
3. **Use environments** — clinical setting, home, sterile field, mobile, emergency.
4. **Regulatory class and pathway**, if known — this shapes how safety-critical needs connect to
   risk management.

**Draw these from context where context has them.** The target product profile, if the `setup`
skill has run, answers most of this: the newest `target-product-profile_rev*.docx` in
`context/product/`, or, unreviewed, `target-product-profile_draft.docx` there. Its use,
usability and clinical performance rows also point at needs — a set-up time target, the training
a user can be given, the harm the device must avoid. If there is no target product profile, an
earlier `setup` put these answers in `context/product/device-profile.md`; read them there, and
suggest re-running `setup` to convert it. Say which answers came from documents and which came
from the conversation. Where the company does not know, write `Not known yet` — a plausible-sounding
invented intended use is worse than a blank, because it looks like a decision someone made.

Every need must be defensible against this anchor. A need that does not map to someone inside the
user profile doing something inside the use environment is out of scope — either expand the anchor
or drop the need.

### 4. Interview (Mode A)

A loose sequence, not a script. **One focused question at a time.** Summarize back every few
exchanges. Skip anything the context already answers.

| # | Focus | What to get answered |
|---|---|---|
| 1 | Problem | What outcome is inadequate today, and what happens if nothing changes? |
| 2 | Users and stakeholders | Who uses it, who is affected, who is exposed to risk if it fails? |
| 3 | Use environment | Where, under what time pressure, with what distractions and constraints? |
| 4 | Desired outcomes | What must be true when the task succeeds? What matters most — safety, speed, comfort, accuracy, reliability, access? |
| 5 | User journey | Recognize need → prepare → initiate → perform → monitor → complete → confirm → document, clean, dispose. What is needed at each stage? |
| 6 | Pain points | Where do users struggle, err, work around, abandon, or get hurt today? |
| 7 | Human factors | What must the user perceive, decide and act on correctly? What could be confused, forgotten, or done out of order? |
| 8 | Patient-centered | What must the patient experience or avoid? What burden is unacceptable? What would make them refuse or stop? |
| 9 | Workflow fit | How does this sit with existing handoffs, staffing and adjacent equipment? |
| 10 | Risk lens | Which outcomes, if not achieved, cause harm or serious delay? Flag those as safety-critical. Where there is a hazard list, start from it: see below |
| 11 | Priority | Critical (safety, effectiveness) / Important (adoption, workflow) / Desirable (preference) |

**Convert solutions to needs every time, not occasionally.** When the interviewee proposes a
feature, do not write it down. Ask: *"What outcome does that enable? What would happen to the user
if it were missing?"* Capture the answer, not the feature.

> **Interviewee:** "It needs a big button so people can start it easily."
> **You:** "What outcome does the big button enable? What would happen if it wasn't there?"
> **Interviewee:** "They'd need to be sure they actually started therapy, not just touched it."
> **Need:** `UN-007 — The patient shall receive unambiguous confirmation that therapy has started
> before leaving the application site.`

**Work through the hazard list, if there is one.** For each hazard no user need covers, ask what
the person must be able to do, perceive, receive or avoid so that the hazard does not reach them:

> **Hazard:** HZ-004 — infusion stops without the clinician knowing; harm: low blood pressure.
> **You:** "What does the clinician need, so that a stopped infusion does not go unnoticed?"
> **Need:** `UN-009 — The clinician shall not miss an interruption in therapy.`

- **One need may answer several hazards.** Merge before adding; the compactness rule still holds.
- **Some hazards have no user need.** Leakage current or a leachable chemical is answered by design
  inputs and testing, with no outcome a person can perceive. Say so, and mark the hazard
  *Design inputs, not a user need* rather than inventing a need for it.
- **A need that answers a hazard is safety-critical**, and cites the hazard's ID.

**Work through the predicate profile's use expectations, if there is one.** Each says how people
already use a similar device: what they do at each stage, what they rely on, what training they
had. Treat each like a feature the interviewee proposed: ask what outcome it serves, and whether
this device's users need that outcome too. Capture the outcome, cite the `PP-` ID as its source,
and never the predicate's feature.

> **Use expectation:** PP-012 — the predicate shows remaining battery as a percentage on its main
> screen (IFU, p. 12).
> **You:** "What does the nurse need, so that the device does not run out mid-procedure?"
> **Need:** `UN-011 — The nurse shall know before starting a procedure whether the device can
> complete it.`

A use expectation the team decides this device's users do not share is set aside, with the
reason; that is a difference from the predicate worth recording.

Stop interviewing when two consecutive rounds produce no new non-redundant need.

### 5. Screen every draft before showing it

Rewrite any candidate that contains:

- a named component — cartridge, screen, button, battery, sensor, valve
- a named technology or protocol — Bluetooth, Wi-Fi, RFID, NFC, touchscreen, haptic
- a UI element — dropdown, alarm tone, LED colour, icon
- a packaging or form-factor claim — handheld, pocket-sized, single-use vial
- an engineering implementation — control loop type, encryption type, material grade
- a verification method in disguise — "shall pass [standard] testing"
- a marketing or business claim — "shall be best in class," "shall cost less than competitor"

Replace with the underlying outcome. *Why does the user want that? What does it let them do, know,
avoid or feel?*

| Raw statement | Rewritten |
|---|---|
| Needs a colour screen | The operator shall understand device status and required next steps at a glance. |
| Needs Bluetooth | The clinician shall transfer therapy data into the patient record without manual transcription. |
| Needs a disposable cartridge | The user shall minimize contamination risk during preparation and use. |
| Needs to be lightweight | The caregiver shall carry and position the device without physical strain over a full shift. |
| Shall pass [electrical safety standard] | *A design input and a verification activity, not a user need — remove.* |

**Then apply the validatability test.** For each need:

- Can you picture the specific study task, participant observation or clinical endpoint that would
  prove it was met? If not, it is too vague.
- Is the outcome singular and observable? Compound phrasing — "whether attended or unattended,"
  "either X or Y," "both during and after" — usually hides two needs. Split them.
- Does it reduce to a question with a yes/no or measurable answer for a given study participant?

Needs that fail are usually instructions in disguise, too abstract ("shall be intuitive," "shall be
easy to use"), or compound.

### 6. Check coverage

Confirm the list covers each **non-empty** cell of this intersection:

- **Stakeholders:** primary user, patient, caregiver, reprocessor or service tech, purchaser.
- **Journey:** prepare, use, monitor, complete, handoff or recover.

Empty cells are either legitimately out of scope — say so — or a real gap. Do not force a need into
every cell. Force coverage only of cells the intended use makes non-empty.

Where there is a hazard list, check it too: every hazard is answered by a need, marked *Design
inputs, not a user need*, or left open, and an open hazard goes on the issues list in step 10.

### 7. Stop

Stop drafting when **any** of these is true:

- Two consecutive interview rounds produce no new non-redundant need.
- Every non-empty coverage cell has at least one need, and every hazard on the hazard list is
  answered, marked for design inputs, or listed as open.
- Every Critical need maps to a validation activity the team can picture running.
- You reach about 25 needs. Beyond that, validation burden outweighs the coverage gained. If more
  are genuinely needed, **merge first**.

### 8. Write the draft

Fill `templates/user-needs.md`. Write dates in the Date format from
`context/templates/document-settings.md`, if it exists. Show the user the complete content. Confirm.

Then deliver it as a Word document. Save the filled template to
`context/users-and-needs/user-needs.source.md` and run:

```
python mos/lib/mosdocx.py render --in context/users-and-needs/user-needs.source.md --out context/users-and-needs/user-needs_draft.docx --title "User Needs — <device>" --remove-input
```

Where a reviewed `user-needs_rev*.docx` is already there, name the draft for the revision
after it instead — `user-needs_revB_draft.docx` beside `user-needs_revA.docx` — in the command and
everything below.

`--remove-input` deletes the Markdown once the Word document exists. The Word document is the
deliverable, and a second copy goes stale at the first redline. If `python` is not found, use
the command setup found — `python3` or `py -3`.

If `user-needs_draft.docx` already exists, the script refuses to overwrite it. Show what changed
and ask; add `--force` only on a yes.

If the script cannot run — no Python, or no way to run commands here — write the filled template
to `context/users-and-needs/user-needs_draft.md` instead, and say that Word output needs the step in `setup`.

Then tell them how the draft becomes the record: review and redline it in Word, then accept or
reject every change and delete the comments. When the review is finished, make the clean copy: the
next MOS skill run offers it, or run `python mos/lib/mosdocx.py clean <draft> --apply`. It writes
`user-needs_revA.docx`, or `_revB` for a `_revB_draft`, without the working notes, and moves the full
draft, and the revision it replaces, into `archive/`. The clean copy goes for signature, and
becomes the record when it is signed in the company's quality system. Where the company files
records there, file it there with the context map pointing at it, and delete the copy from
`context/users-and-needs/`. Until then, the next run of this skill, and every other skill
that reads the domain, still reads the draft, as an unreviewed draft.

Finally, tell them which answers from this session belong in `context/users-and-needs/`, named
file by file. Offer. Do not write.

### 9. Reviewing an existing list (Mode C)

Evaluate each entry against six things:

1. **Phrasing** — "The [role] shall…" Is the subject a person at the right level of generality? Is
   the verb a capability, experience, receipt, perception or avoidance outcome, not a bare action?
2. **Solution screening** — any named component, technology, UI element or implementation?
3. **Singularity** — one outcome, not two joined by "and" or a compound "whether X or Y"?
4. **Validatability** — can you picture the study task that proves it, with an observable outcome?
5. **Redundancy** — does another need already cover this?
6. **Scope** — does it trace to the intended use anchor?
7. **Hazards** — where there is a hazard list, is a need marked safety-critical without citing a
   hazard, or does a hazard have no need and no reason?

Report as: `UN-ID | Issue | Suggested rewrite or action (keep / merge with UN-X / delete / rewrite)`.

### 10. Hand off the issues

List what this session found and did not settle: real gaps in the coverage matrix and what would
close each; hazards no need answers and no reason given; hazards the interview raised that the
hazard list does not have; contradictions between documents or with the interview, with where each came from;
assumptions a need rests on that nobody has checked; and target product profile rows the session
bears on — an intended use revised over the challenge, a user group or setting the interview added
— each with what the row says now and what the session found. For each, give its type (question,
conflict, gap, assumption, risk to the plan), its domain, what it blocks and the next step. Check
the current issues list — the newest `<YYMMDD>_issues-list.docx` in `context/` — and leave out what
is already on it, unless this session found something new about it.

Show the list. On a yes, write it to `context/inbox/<YYMMDD>_issues_user-needs.md`, in the format
the context standard gives. Then ask the user to run `issues-list` now, while this session still
holds what was found. Never edit the issues list, the hazard list or the target product profile. If nothing is
unsettled, say so and write no note.

## Working at three levels of context

| What the company has | How this skill behaves |
|---|---|
| Nothing | Produces the template and runs the full interview, explaining why each column exists. The anchor in step 3 is built entirely from the conversation and is explicitly marked as such |
| Some files | Reads the intended use and whatever user research exists, drafts from it, and interviews only for the gaps. Every need is marked as drawn from a document or from the conversation |
| A full document set | Mostly Mode C. Traces each need to the document that supports it and each safety-critical need to the hazards it answers, and flags contradictions between the risk file, the hazard list, the device description and the existing needs rather than resolving them |

## Interviewing style

- One focused question at a time, not three stacked together.
- Keep the interviewee anchored in present workflow and desired outcomes.
- Challenge solution language gently and every time.
- Paraphrase what you heard into clean need language, and let them correct you.
- Park business goals, marketing claims, verification methods and regulatory strategy politely.
  They are real, and they are not user needs.
- Do not lecture on design controls unless asked.

## Boundaries

This skill does not generate design inputs, commit to a device architecture, frame bench-test
methods as needs, reduce patient needs to operator convenience, or inflate a list to look thorough.

## Where this skill is weakest

Recorded so it gets fixed rather than rediscovered:

- It cannot tell a confident wrong answer from a correct one. A team that believes its users are
  trained clinicians when half of them are not will get a need set built on that belief.
- The 10–25 range is judgement dressed as a number. It is a useful prior, not a limit, and a
  genuinely complex combination product may exceed it for real reasons.
- It has no way to check whether a need was already validated, or whether one contradicts a design
  input written later. Traceability is a separate job and there is no skill for it yet.
- Mode C on a long list is slow and gets less careful toward the end. Review in batches.
