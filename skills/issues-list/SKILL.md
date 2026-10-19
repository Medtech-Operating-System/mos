---
name: issues-list
description: Keep a company's issues list — every open question, gap, conflict, assumption and risk to the plan that comes up while developing a medical device — and work through it as new context arrives. Use when a team wants to start an issues list, log the issues another MOS skill found, take in the edits the team made to the list, or check which open issues new documents or decisions now settle.
version: 0.2.0
maintainer: Eric Sugalski
phase: [all]
discipline: [all]
reads:
  - context/context-map.md
  - context/*_issues-list.*
  - context/archive/*_issues-list.*
  - context/inbox/**
  - context/templates/**
  - context/product/**
  - context/users-and-needs/**
  - context/risk/**
  - context/design/**
  - context/manufacturing/**
  - context/clinical/**
  - context/regulatory/**
  - context/commercial/**
writes:
  - context/
  - context/archive/
status: draft
---

# Issues list

Keeps one list of everything that is not settled — across product, users, risk, design,
manufacturing, clinical, regulatory and commercial — and helps the team close it. The output is a
Word document, `context/<YYMMDD>_issues-list.docx`, that the team edits directly between runs.
Each run reads those edits and the notes other skills left, logs what is new, and writes the next
list under that day's date.

Read `mos/context-standard.md` before starting if you have not already, especially *The issues
list*, then read `context/context-map.md` to find out what you are allowed to read.

## The thing this skill is actually for

**Capture is the step that fails.** An open question raised in a meeting, or in the appendix of a
document nobody opens again, is settled by accident or not at all. The list puts every one of them
in front of the whole team, with an owner and what it blocks.

**Closing is where the value is.** A list that only grows becomes a graveyard. Every run checks
whether new context — a new document, a decision, a finished analysis — settles something, and
puts it to the user to close.

**What an issue blocks matters more than how important it feels.** The list has no High, Medium
and Low. It says what each issue holds up: a skill, a target product profile row, a milestone.
That is harder to inflate, and it orders the work.

## Rules for this skill

- **The list is the only document this skill writes**, apart from a decision record the user asks
  for in step 5. It never edits another document. When closing an issue changes one — a target
  product profile row, a claim, a user need — the resolution names it in a `Revise:` line, and the
  team makes the next revision. For the target product profile, `setup` drafts it.
- **Propose; a person decides.** Never add, close or reword an issue without showing it first.
  Never close an issue because it looks stale.
- **Test what the user brings before relying on it.** When the user wants to close an issue, read
  what settles it. If the evidence does not support closing — the document they cite does not say
  that, or says something else — say so, show it, and ask them to reconsider. Once they have heard
  the challenge and confirmed, close it, and write in the resolution that it was closed over the
  challenge. The same applies to an issue the user says is not real.
- **Never renumber an issue or reuse an ID.** A document or a conversation that cites ISS-012 must
  always mean the same issue.
- **Do not invent issues to make the list look thorough**, and do not guess owners. An owner is a
  name someone gave, or `Unassigned`.
- **Read narrowly.** This skill may read every domain, because issues cross them, but it reads one
  only where an issue, a note or the user points into it.
- **Confirm before every write into `context/`**, and before moving or deleting any file.
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

- **It exists** — read it.
- **It does not exist** — say so, and say that running `setup` first will make this skill better:
  the list then has a device to be about, and the company's document format. Then offer to
  continue from the conversation alone, creating `context/` and `context/inbox/` on a yes.

Then find what this run works from. Read Word documents with `python mos/lib/mosdocx.py read
<file>`; if `python` is not found, use the command `setup` found — `python3` or `py -3`.

- **The current list.** The newest `<YYMMDD>_issues-list.docx` in `context/`, outside
  `archive/`. If there is more than one, stop: say which, and ask which is the list. Copies saved
  under other names split the team's edits, and guessing loses some of them.
  - If the read reports **tracked changes**, say how many, and that the next list will carry them
    as accepted. Ask whether the team agrees, or wants to accept and reject them in Word first.
  - If it reports **review comments**, they are listed at the end of the read, each with the text
    it is attached to. Each one is an edit to take in at step 4.
- **The last list before it**, the newest one in `context/archive/`. Step 4 compares the two to
  find what the team changed.
- **Notes from other skills.** Every `<YYMMDD>_issues_<skill>.md` in `context/inbox/`.
- **The target product profile** — the newest `target-product-profile_rev*.docx` in
  `context/product/`, or, unreviewed, `target-product-profile_draft.docx` there — and
  `context/product/device-profile.md`, for the device's name, stage and milestones.

Tell the user what you found: whether a list exists and how many issues are open, how many notes
are waiting, and whether the team edited the list since it was written.

### 2. Say what this run will do

A run does up to three things, in this order:

1. **Start** the list, if there is none — step 3.
2. **Log** what is new: the notes, the team's edits and comments, and anything the user brings —
   step 4.
3. **Work through** the open issues against new context — step 5. Offer it; the user may want only
   the logging today.

Say which apply and ask the user to confirm.

### 3. Start the list

Only when no list exists. Build the first one from four sources:

- **The notes** in `context/inbox/`, if any skill has run.
- **Target product profile rows marked `Not set yet` that something is waiting on** — a milestone,
  another row, a skill that cannot run well without it. Not every unset row: a list that opens with
  thirty issues teaches the team to ignore it. Say how many unset rows you left off, and why.
- **MOS documents written before the issues list existed**, which carry their own open questions
  in an appendix. Read those appendices in the MOS drafts and records the map points at — drafts
  sit in their domains, named `_draft`, or in `outputs/` for a company that kept the old layout — and log each item once, citing the document it came from. Do not read the
  company's other files for this.
- **The user.** Ask, one question at a time, and stop when the answers run out:
  - *What has the team not decided yet?*
  - *Where do people on the team disagree?*
  - *What are you taking as true that nobody has checked?* These are **assumptions**.
  - *What could move the schedule, the cost or the path to market?* These are **risks to the
    plan**. A way the device could hurt someone is a hazard, and belongs in the risk file instead:
    say so, and do not log it here.

Then log each one as step 4 describes.

### 4. Log what is new

Take in, in order:

1. **What the team changed in Word.** Compare the current list with the last one in `archive/`.
   Report every difference: a status changed, a resolution written, wording edited, a row added —
   with the ID `New` or none at all — or a row deleted. A deleted row is never dropped silently:
   ask whether it was closed, merged into another issue or raised in error, and record which.
2. **The review comments.** For each, say what it asks for and propose the change: a closing, a new
   owner, a reworded issue, a new issue. A comment that only discusses is noted to the user, not
   logged.
3. **The notes** in `context/inbox/`.
4. **Anything the user brings** in the conversation.

For each candidate issue:

- **Check it is not already on the list.** If an open issue covers the same thing, add what is new
  to that issue — another thing it blocks, a new fact — rather than opening a second one. If a
  closed issue covers it, say so, and ask whether it has reopened.
- **Check it is still open.** If a document you have read already settles it, say so and propose
  logging it as closed, with the resolution.
- **Write it in plain words, with the term beside them**: what is open, and why it matters. End
  with when it was raised and by whom — a skill or a person.
- **Give it a type**: Question, Conflict, Gap, Assumption or Risk to the plan.
- **Give it a domain**, one of the eight. An issue about the project rather than the device —
  funding, hiring, a partner — goes under Product, where the device profile keeps the project's
  status.
- **Say what it blocks**: a skill, a target product profile row, a milestone, a document. If it
  blocks nothing, write `Nothing yet`, and ask whether it belongs on the list at all.
- **Ask who owns it.** Write `Unassigned` if nobody does.
- **Say the next step**: what would settle it, and who. A decision by a named person, a test, a
  conversation with a customer or with FDA, a document, or a MOS skill. Name only a skill that is
  in `mos/skills/`; where none would settle it, say that plainly.

**A note line that carries `Decided:`** was settled during another skill's run: the user answered
it there. Log it as closed, in one step, with the decision, who made it and when as its resolution,
and *decided during the <skill> run*; carry its `Revise:` line into the resolution word for word.
Show it with the rest, but do not ask the question again. Test it as you would any closing: where a
document you have read contradicts the decision, or two decided lines contradict each other, say so
and ask before closing.

Give each new issue the next free ID. Show the user the issues to add and the changes to make, and
confirm them.

### 5. Work through the open issues

Offer this; do as much as the user wants. Take the open issues in order of what they block:
issues holding up the nearest milestone first, then those holding up a skill or another document,
then the rest. Or take the domain or the issues the user names.

For each issue:

1. **Look for new context.** Read what has appeared in the domains the issue points at since it was
   raised: a new document or revision, a new MOS draft, a decision record. Read nothing else.
2. **Say what you found**, and propose one of:
   - **Close it**, because a document settles it. Show the passage and cite the document by path,
     saying whether it is a reviewed record or an unreviewed draft. An issue settled only by an
     unreviewed draft can close, but its resolution says so.
   - **Settle it now**, because what is missing is a decision the user can make in this
     conversation. Ask plainly, in the form *"Who will use this at home — the patient, or a
     caregiver too? FDA calls this the intended user."* Record the answer, who gave it and the
     date. If the decision is one no document holds, offer to write a short decision record to the
     domain, as the context standard describes, on a yes.
   - **Route it**, because settling it takes analysis. Name the MOS skill that would, or say no
     skill does yet and name the kind of person who would know.
   - **Keep it open**, saying what changed, if anything, and updating the next step.
3. **Where the resolution changes another document**, write it as a `Revise:` line: the document
   and the row or section, what it says now and what it should say — *Revise: target product
   profile row 4.2 — minimum from "≥ 8 h" to "≥ 12 h"*. The team makes the change; for the target
   product profile, `setup` drafts it from these lines.

Confirm each closing before recording it.

### 6. Write the new list

Fill `templates/issues-list.md`:

- Open issues go under `## Open Issues`, one table per domain in the order of the eight domains —
  Product, Users and needs, Risk, Design, Manufacturing, Clinical, Regulatory, Commercial — leaving
  out domains with no open issue. Within a domain, in order of ID.
- Issues closed this run, and every issue closed before, go in the Closed Issues table, newest
  closing first. A `Won't do` issue goes there too, with its reason.
- Add a row to the update log: today's date, the IDs added, closed and edited, and where each came
  from — a note by name, the team's edits, the conversation.
- Write dates in the Date format from `context/templates/document-settings.md`, if it exists. The
  date code in the filename is always `YYMMDD`: `261016` for 16 October 2026.

Show the user what changed — issues added, closed and edited — and offer the full list. Confirm.
Save the filled template to `context/<YYMMDD>_issues-list.source.md` and run:

```
python mos/lib/mosdocx.py render --in context/261016_issues-list.source.md --out context/261016_issues-list.docx --title "Issues List — <device>" --set revision=261016 --remove-input
```

If a list with today's date exists already, the script refuses to overwrite it. Today's list was
read in step 1, so the new one holds everything in it: say so, and add `--force` on a yes. If the
script cannot run, write the filled template to `context/<YYMMDD>_issues-list.md` instead, and say
that Word output needs the step in `setup`.

Then, each on a yes:

- Move the list this one replaces into `context/archive/`, creating the folder if it is missing.
  Its comments and tracked changes stay with it there; the new list starts clean.
- Delete the notes from `context/inbox/` that were logged. Leave any the user chose not to log, and
  say which.

### 7. Report and hand off

Tell the user:

- The new list, by path, and how many issues are open in each domain
- What closed this run, and the three issues blocking the most
- Every document a resolution says to revise, with the row or section. Where any is the target
  product profile, say that `setup` drafts its next revision from those resolutions, and suggest
  running it now
- What to run next: the skills named in the next steps of the most-blocking issues

Then tell them how the team works with the list:

- **Edit it directly in Word.** To close an issue, change its Status to `Closed` and write what
  settled it in the last column. To add one, add a row with the ID `New`. Comments are read too.
- **Keep one list.** Do not save copies under other names; edit the one in `context/` and let the
  next run take the edits in.
- **Run `issues-list` after any other MOS skill**, which leaves its issues in `context/inbox/`, and
  whenever the team has edited the list or something has been decided.

## Working at three levels of context

| What the company has | How this skill behaves |
|---|---|
| Nothing | Explains what the list is for and builds the first one from the conversation alone, asking the four questions in step 3. Most issues are Questions and Assumptions, and most next steps are decisions only the team can make |
| Some files | Starts from the target product profile's unset rows that something waits on, the open questions in older MOS documents and the notes other skills left, then asks what else is open |
| A full document set | Most of the work is taking in the team's edits and checking open issues against new revisions. Flags issues that later documents settled without anyone closing them, and resolutions that point at a document revision that never happened |

## Interviewing style

- One question at a time.
- Ask for the specific: *who* has to decide, *by when*, *what* it holds up.
- When the user says an issue is settled, ask where that is written down. A decision only in
  someone's head is still an open issue, of a different kind.
- Treat "nobody knows" as a finding. It is usually the most useful line on the list.

## Boundaries

This skill does not settle issues that need analysis; it routes them to the skill or the person
who can. It is not the risk file: a hazard to a patient or user goes in `risk/`. It is not a
complaint, nonconformance or corrective action system, and not a project schedule. It does not
assign work or chase owners.

## Where this skill is weakest

Recorded so it gets fixed rather than rediscovered:

- It logs only what someone noticed. A question nobody raised is not on the list, and an empty
  list proves nothing.
- Whether a document settles an issue is a judgment. The skill shows the passage, and a person
  decides, but a confident wrong reading can still close something that is open.
- It reads the list back from Word. A table the team restructured — merged cells, columns moved or
  renamed — may not read cleanly. The skill says what it could not read, rather than guessing.
- "New since the issue was raised" relies on file dates and revision names. A sync tool that
  touches every file's date makes old documents look new.
- Comment threads read as separate comments; a reply is not tied to the comment it answers.
