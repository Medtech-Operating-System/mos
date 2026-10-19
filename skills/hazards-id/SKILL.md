---
name: hazards-id
description: List the early hazards of a medical device — what could hurt someone, how, and what harm would follow — from FDA's records for similar devices, their labeling, a hazard checklist and any standards the company holds, so they shape user needs and design inputs. Use when a team needs a preliminary hazard list at concept or definition stage, before a hazard analysis.
version: 0.3.0
maintainer: Eric Sugalski
phase: [00-concept, 01-definition]
discipline: [technical, clinical, quality]
reads:
  - context/context-map.md
  - context/*_issues-list.*
  - context/product/**
  - context/users-and-needs/**
  - context/risk/**
  - context/regulatory/**
  - context/templates/**
writes:
  - context/risk/
  - context/regulatory/summaries/    # FDA summaries it downloads, beside those other skills saved
  - context/inbox/
status: draft
---

# Hazards identification

Lists what could hurt someone with this device, early enough to change the design. Each hazard
is traced from its source to the harm it could cause, and to the user needs it bears on. The
output is a Word document in `context/risk/`, built from the company's template: a draft for
review, not a controlled record. `user-needs` reads it, and so will the hazard analysis that
comes later.

Read `mos/context-standard.md` before starting if you have not already, then read
`context/context-map.md` to find out what you are allowed to read.

## The thing this skill is actually for

**Hazards found late are expensive.** A hazard found after design freeze becomes a redesign, a
retest or a warning label nobody reads. Found at concept stage, it becomes a user need, and the
design answers it from the start.

**Similar devices have already shown what goes wrong.** FDA has named the risks to health for
most device types, adverse event reports describe what happened in use, recalls show what reached
the market, and a competitor's warnings list the hazards its maker already acknowledged. A new
team rarely reads any of them. This skill reads all of them before asking the team to imagine
anything.

**This is identification, not analysis.** The list says what could happen. It does not score how
severe or how likely each hazard is, and it does not propose risk controls. Those come in the
hazard analysis, which builds on this list. Mixing them in now invites argument over numbers
before the list is complete.

## Rules for this skill

- **No scoring and no controls.** Do not rate severity or probability, and do not propose how a
  hazard is to be controlled. If the user asks, say that is the hazard analysis, and that this
  list is its input. A user need may say what the device must achieve for the person; it does not
  say how.
- **A hazard row is complete only when it names the harm.** Hazard, sequence of events,
  hazardous situation and harm, in the words `mos/lib/reference/hazard-checklist.md` defines.
  Where the harm cannot be named, write `Harm not yet identified` rather than leaving the row
  looking finished.
- **Every row names its source.** An FDA record with its number, a label with its device, a
  checklist line by ID, a clause of a standard the company holds, or this session's interview.
- **Standards are the company's, and so is the decision to send them.** Read a file in
  `context/regulatory/standards/` only after the user confirms their licence allows sending it to
  their AI provider. Cite clause numbers. Never copy a standard's text or tables into the draft.
- **Never send company text outside.** Searches of FDA's databases send product codes, brand
  names and submission numbers. Web searches send brand names and device categories. Never the
  company's product name, its device description or any file's contents.
- **Show every query before it runs.** List the searches, say what each sends and where, and run
  them on a yes. The user may edit or drop any of them.
- **An adverse event report is an allegation, not a finding.** It shows a hazard exists. It does
  not show how often it happens, and the draft never uses report counts as rates.
- **Do not write into `context/`** without approval of that specific write.
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

- **It exists** — read it, then read:
  - **The target product profile** — the newest `target-product-profile_rev*.docx` in
    `context/product/`, or, unreviewed, `target-product-profile_draft.docx` there — for the
    device, its intended use and indications, its users and where it is used. Read
    `context/product/device-profile.md` for the risk notes `setup` recorded.
  - **The user needs** under `users-and-needs/`: their IDs, use stages and which are marked
    safety-critical.
  - **The risk file** under `risk/`: any existing hazard list, hazard analysis or risk notes.
  - **The regulatory work** under `regulatory/`: `classification.md` for the product code,
    `precedent.md` for the chosen predicate and reference devices, and the product code analysis
    and precedent search, reviewed or draft. From the precedent search take the special
    controls, the risks FDA identified in similar De Novo grants, and any PMA approvals. From
    the predicate profile, reviewed or draft, take its candidate inputs of kind *Hazard*, its
    safety information and field record for each device, and the labeling it saved in
    `regulatory/labeling/`.
  - **The standards folder**, `context/regulatory/standards/`: list the file names only. Do not
    open them yet; step 5 asks first.

  Read Word documents with `python mos/lib/mosdocx.py read <file>`. Tell the user what you found.
  - Drafts sit beside the records in each domain, named `_draft`. Read them too, and say that
    they are unreviewed. A reviewed document outranks a draft; where they disagree, say so and
    ask.
  - If a hazards identification exists already, reviewed or draft, its hazards have IDs. Ask
    whether this run is to revise it or to start again. Never renumber an existing hazard; the
    new draft carries the old IDs forward.
  - If documents disagree — the risk notes name a hazard the user needs never mention, or two
    documents describe different users — list the contradictions. Do not pick one.
- **It does not exist** — say so, and say that running `setup` first, and `product-code` and
  `precedent-search` after it, will make this skill much better, because most of its evidence is
  found through the product code and the predicates. Then offer to continue from the
  conversation alone.

**Offer clean copies of finished drafts.** For each `_draft` this skill reads, ask once:
*"Is the review of this document finished, and is it ready to route for signature?"* On a yes,
run `python mos/lib/mosdocx.py clean <file>`, show what it says it will do, and run it again with
`--apply` on a second yes. It writes the clean copy, `_revA`, without the working notes, and keeps
the full draft in `archive/`. If it refuses because of tracked changes or comments, say what to do
in Word first. MOS approves nothing: the clean copy becomes the record when it is signed in the
company's quality system. A draft that stays a draft is still read, and cited as unreviewed.

Anything you need outside the declared paths, ask for by name and say why. Write the answer back
to the context map so the question is not asked twice.

### 2. Describe the device for hazards

Build a short description of the features that decide which hazards are possible. Fill what the
context already answers, and ask only for the rest, one question at a time:

- *Does it run on mains power or a battery, or neither?*
- *What touches the patient or the user, where on the body, and for how long?* The **body
  contact**: skin, mucosa, blood, tissue or bone; minutes, up to 30 days, or longer.
- *Is it sold sterile? Is it used on more than one patient?* **Sterility** and **reuse**.
- *Does it stay in the body?* An **implant**.
- *Does it deliver anything — energy, a drug, a fluid, force?*
- *Does it measure something a clinician or patient acts on?*
- *Does it run software, or connect to a phone, a network or another device?*
- *Who uses it, and where?* The **users** and the **use environment**: a clinician in a hospital,
  a patient at home, a caregiver, a child.
- *What are the steps of using it, from unpacking to disposal?* The **use steps**. Use the stages
  `user-needs` uses — prepare, use, monitor, complete, handoff — so the two documents line up.

Show the description back and confirm it. Then read the trigger table at the end of
`mos/lib/reference/hazard-checklist.md` and say which checklist sections these features point
at.

### 3. Read FDA's records for similar devices

FDA's records come first, because they are evidence of what has gone wrong with devices like this
one, not a guess at it. Show the planned searches, say that they send only product codes, brand
names and submission numbers to FDA, and run them on a yes:

```
python mos/lib/openfda.py regulation 880.5725
python mos/lib/openfda.py problems --code FRN --since 2021
python mos/lib/openfda.py problems --brand "BRAND" --manufacturer "MAKER" --since 2021
python mos/lib/openfda.py recalls --code FRN
python mos/lib/openfda.py recalls --number K123456
python mos/lib/openfda.py fetch DEN123456 P123456 --out context/regulatory/summaries
```

- **`regulation`** gives the special controls, which name risks FDA expects the device type to
  address. Where the precedent search has already recorded them, use that and do not search
  again.
- **`problems`** gives the device problems and patient problems reported in adverse event
  reports, with what happened in the reporters' words. Run it for the product code, and for each
  predicate and reference device by brand. `--since` keeps the evidence to recent designs; five
  years is a sensible start. Use the narratives to write the sequence of events: they often say
  exactly how a problem reached the patient.
- **`recalls`** gives failures that reached the market, with their root causes.
- **`fetch`** downloads De Novo decision summaries, whose "risks to health" table names each risk
  FDA identified with its mitigation, and PMA summaries of safety and effectiveness, which list
  adverse events from the pivotal study. Look in `context/regulatory/summaries/` first: the
  precedent search may have downloaded them already. Save any new ones there, and read them. Take the risks; leave the mitigations,
  which belong to the hazard analysis.

Where there is no product code yet, say that most of this step depends on one, and suggest
running `product-code`. Brand searches still work for any competitor the user can name. If
`python` is not found, use the command `setup` found — `python3` or `py -3`. If FDA cannot be
reached, say so and continue.

Where the predicate profile already ran a brand search for a device — its search log says which
and when — use its findings and do not run the search again, unless it is more than about six
months old; then say so and let the user decide.

Report what the records show before moving on, in plain words: the problems that come up most,
the harms reported, and the risks FDA named.

### 4. Read the labeling of similar devices

A competitor's labeling lists the hazards its maker already acknowledged: its warnings,
precautions, contraindications and adverse events. FDA's databases do not hold device labeling.

**Start from the predicate profile, if there is one.** It has read the predicate's and
reference devices' labeling already: take its *Hazard* findings and its safety information, and
read the labeling it saved in `context/regulatory/labeling/`. Search only for devices it did not
profile.

Otherwise, ask the user for the instructions for use of the predicate and reference devices, or any
competitor's, and suggest saving them in `context/regulatory/labeling/<maker>-<brand>/`, one folder
per device. Where a device needs studying in depth, suggest `predicate-profile`. Then offer the web
as its own step:
say that it finds published instructions for use and labels on manufacturers' sites, that it
sends brand names and device categories to the search service the AI uses, and ask whether to go
ahead. On approval, list the searches and run them. Record each label's device, source, URL and
the date read. If this AI cannot search the web, say so.

From each label, take the warnings, precautions, contraindications and listed adverse events.
Each is a hazard, a hazardous situation or a harm; place it in the chain rather than copying the
sentence.

### 5. Check against the company's standards

If `context/regulatory/standards/` holds files, name them, and say which bear on hazards: ISO
14971 Annex C and ISO/TR 24971 Annex A above all, and any device-specific standard. Then say,
plainly:

> Reading a standard sends its text to your AI provider as part of the prompt. Some publishers'
> licence terms restrict putting their documents into AI tools. Whether yours allows it is your
> decision; MOS does not rule on it. Shall I read them?

On a yes, read the parts that bear on hazards and use them to find hazards the other sources
missed. Cite each by standard, edition and clause. **Never copy a standard's text or tables into
the draft**, and do not paraphrase a table line by line: the draft is shared beyond the people
the licence covers.

If the folder is empty or missing, or the user says no, say which check was not done, and that a
company holding ISO 14971 and ISO/TR 24971 can put them in `context/regulatory/standards/` and run
this skill again. Do not work from what you may remember of a standard's text.

### 6. Walk the checklist and the use steps

Walk every section of `mos/lib/reference/hazard-checklist.md`, starting with the sections the
triggers in step 2 pointed at. For each line, decide whether it applies to this device, might
apply, or does not. A line already covered by a hazard from steps 3 to 5 needs nothing new; note
the line against that hazard.

Then walk the use steps with the user, stage by stage. For each, ask what the person is doing
and what could go wrong if they did it wrongly, late, or not at all. Users and their mistakes are
where the user knows more than any record, and these are the hazards that turn most directly into
user needs.

Ask the user, finally, what worries them that has not come up. Founders often know the hazard
that keeps them up at night and do not volunteer it.

### 7. Build the hazard list

Merge what steps 3 to 6 found into one list. One hazard that appears in a special control, in
adverse event reports and on a competitor's label is one row with three sources, not three rows.
For each hazard, record:

- **Hazard**: the source of harm, in plain words, with its checklist section.
- **Sequence of events**: what has to happen for it to reach someone.
- **Hazardous situation**: the moment a person is exposed.
- **Harm**: the injury or damage to health. Use an IMDRF health effect term where one fits.
- **Who is exposed**: patient, user, caregiver, bystander.
- **Use stage**: prepare, use, monitor, complete, handoff, or across the life cycle.
- **Sources**: every source that raised it.
- **For user needs**: the existing user need it bears on, by ID, or `No user need covers this`.

Give each hazard an ID, `HZ-001` onward. **Never renumber an existing hazard.** Retire an ID
instead, so a document that cites HZ-004 always means the same hazard.

A hazard with no source but the checklist is still a hazard. Mark it so; the hazard analysis
decides whether it matters.

### 8. Test what the user brings

If the company already has a hazard list or risk file, compare it with this one, and say plainly
where they differ:

- hazards FDA's records or a competitor's label show, which the company's list does not have;
- rows that are risk controls or requirements written as hazards, such as *"alarm must sound"*;
- rows that run hazard and harm together, so the chain between them is missing;
- hazards the company's list rules out that the evidence suggests are real.

Ask the user to reconsider each, with the evidence. The list is theirs: where they confirm a
hazard does not apply after hearing the challenge, accept it, remove the row or mark it, and
record that it was confirmed over the challenge.

### 9. Write the draft

Fill `templates/hazards-id.md`. Write dates in the Date format from
`context/templates/document-settings.md`, if it exists. The search log lists every query sent to
FDA and to the web, in order. Show the user the complete content. Confirm.

Save the filled template to `context/risk/hazards-id.source.md` and run:

```
python mos/lib/mosdocx.py render --in context/risk/hazards-id.source.md --out context/risk/hazards-id_draft.docx --title "Hazards Identification — <device>" --remove-input
```

Where a reviewed `hazards-id_rev*.docx` is already there, name the draft for the revision after
it instead — `hazards-id_revB_draft.docx` beside `hazards-id_revA.docx` — in the command and
everything below.

If `hazards-id_draft.docx` already exists, the script refuses to overwrite it. Show what changed
and ask; add `--force` only on a yes. If the script cannot run, write the filled template to
`context/risk/hazards-id_draft.md` instead, and say that Word output needs the step in `setup`.

Tell the user how the draft becomes the record: review and redline it in Word, then accept or
reject every change and delete the comments. When the review is finished, make the clean copy: the
next MOS skill run offers it, or run `python mos/lib/mosdocx.py clean <draft> --apply`. It writes
`hazards-id_revA.docx`, or `_revB` for a `_revB_draft`, without the working notes, and moves the full
draft, and the revision it replaces, into `archive/`. The clean copy goes for signature, and
becomes the record when it is signed in the company's quality system. Where the company files
records there, file it there with the context map pointing at it, and delete the copy from
`context/risk/`. Until then, `user-needs` still reads the draft, and says it is unreviewed.

Where hazards have no user need covering them, suggest running `user-needs` next.

### 10. Hand off the issues

List what this session found and did not settle: hazards whose harm could not be named; hazards
no user need covers; contradictions between documents; the standards check, if it was not done;
labeling the user could not find; and target product profile rows the hazards bear on — a user
group, a use environment or a claim that brings a hazard with it — each with what the row says now
and what the hazards suggest. For each, give its type (question, conflict, gap, assumption, risk
to the plan), its domain, what it blocks and the next step. Check the current issues list — the
newest `<YYMMDD>_issues-list.docx` in `context/` — and leave out what is already on it, unless
this session found something new about it.

Show the list. On a yes, write it to `context/inbox/<YYMMDD>_issues_hazards-id.md`, in the format
the context standard gives. Then ask the user to run `issues-list` now, while this session still
holds what was found. Never edit the issues list, the user needs or the target product profile.
If nothing is unsettled, say so and write no note.

## Working at three levels of context

| What the company has | How this skill behaves |
|---|---|
| Nothing | Builds the device description from the conversation, walks the full checklist and the use steps with the user, explaining what a hazard is and why the chain to harm matters. Brand searches run for any competitor the user names. The draft says the product-code and precedent searches would add FDA's own evidence |
| Some files | Starts from the target product profile and the product code, reads FDA's special controls, adverse event reports and recalls for the code, and interviews for the use steps and the labeling it could not find |
| A full document set | Adds the predicates' and reference devices' reports, recalls and labeling, checks against the company's standards where it may, compares with the existing risk file and user needs, and flags contradictions rather than resolving them |

## Interviewing style

- One question at a time.
- Ask about what people actually do, not what the instructions say they do.
- When the user says a hazard cannot happen, ask what stops it. If the answer is a design
  feature, the hazard is real and the feature is its control; the hazard stays on the list.
- Treat "I don't know" as a finding. It usually means a use step has not been watched yet.

## Boundaries

This skill does not rate severity or probability, estimate risk, decide whether a risk is
acceptable, or propose risk controls. It does not write user needs or design inputs; it says
which hazards they must answer. It is not a risk management plan and does not replace the hazard
analysis or the risk management file a submission needs. It reads FDA's public records, labeling
the user supplies or the web finds, and standards the company holds and agrees to send.

## Where this skill is weakest

Recorded so it gets fixed rather than rediscovered:

- Adverse event reports are dominated by the devices with the most units in use and the
  manufacturers that report most. A hazard common to a small competitor can be invisible.
- A new technology has no reports and no recalls. For a device with no close predicate, the
  checklist and the user carry most of the weight, and the draft says so.
- Labeling found on the web may be out of date or for another market. Every label carries its
  source and the date read.
- Without the company's standards, the check against ISO 14971 and ISO/TR 24971 is not done, and
  the checklist does not stand in for it.
