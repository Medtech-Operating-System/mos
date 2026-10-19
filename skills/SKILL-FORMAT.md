# The MOS skill format

*v0.8, 2026-10-17. The contract every MOS skill is written to. Changes to this file are
architecture decisions and go through the decision log.*

A MOS skill is a folder of plain Markdown that an AI reads and follows. It is not a program. A
person could run one by hand with the templates and enough patience; the AI is there to do the
reading and the drafting. What skills share lives in `lib/`: `mosdocx.py`, which writes and reads
Word documents, and the scripts and reference data more than one skill needs. They need Python, and
`setup` asks before installing it.

## One job per skill

If the skill cannot be described in one sentence, it is two skills.

The sentence goes in the `description` field, and it is what an AI matches against when a user
says "run the user needs skill." Write it for that job: what the skill does, and when someone would
want it.

## Folder shape

```
skills/<skill-name>/
├── SKILL.md          <- the instructions the AI follows. Required
├── templates/        <- the documents it fills in
├── scripts/          <- deterministic work that should not be improvised
├── reference/        <- optional; background the AI reads only when SKILL.md says to
└── examples/         <- optional; a filled-in example helps more than prose
```

`SKILL.md` is the only required file. A skill with no templates and no scripts is still a skill.

Scripts belong to the skill that uses them and run when that skill runs. Use one when the work is
mechanical and an AI would get it wrong by improvising — comparing timestamps, checking a folder
against a list, counting. Do not use one for anything requiring judgment.

The exception is `lib/`, for what more than one skill needs. A skill does not carry its own copy
of anything there.

| Shared | What it is for | Used by |
|---|---|---|
| `lib/mosdocx.py` | Writes and reads every Word document, so they all look the same, makes the clean copy of a reviewed draft, and numbers documents in the register | Every skill |
| `lib/openfda.py` | Every call to FDA's databases and the eCFR | The regulatory and commercial skills |
| `lib/studies.py` | Every sample size, timeline and budget calculation, and every ClinicalTrials.gov query | `indications-strategy` |
| `lib/cms.py` | Every Medicare coverage policy search and every public billing-code lookup | `reimbursement` |
| `lib/layout.py` | Moves a company folder from an older layout to the current one | Every skill, at its first step |
| `lib/reference/` | Data files with their sources, such as `clinical-cost-bands.md` | The skills that name them |

Each new shared script or reference file needs a decision-log entry saying why it cannot belong to
one skill. A change to one is checked against every skill that uses it.

## SKILL.md

YAML frontmatter, then numbered execution steps. Nothing else.

```yaml
---
name: user-needs
description: Draft user needs for a medical device from a company's existing context, interviewing for what is missing. Use when a team needs user needs captured, converted from notes, or reviewed for gaps.
version: 0.1.0
maintainer: Jane Doe
phase: [01-definition]
discipline: [clinical, technical]
reads:
  - context/context-map.md
  - context/product/**
  - context/users-and-needs/**
writes:
  - context/users-and-needs/
status: draft
---
```

| Field | Rule |
|---|---|
| `name` | Folder name. Lowercase, hyphenated. This is what a user types: `run the user-needs skill` |
| `description` | The one sentence, plus when to use it. No marketing |
| `version` | Semantic. The first release of a skill is `0.1.0` |
| `maintainer` | A person, named. A skill with no maintainer does not ship |
| `phase` | Where it sits on the lifecycle map, by phase id. More than one is allowed |
| `discipline` | One or more of: technical, clinical, regulatory, quality, commercial, manufacturing |
| `reads` | Directories with patterns. See below |
| `writes` | Where output goes. The domain folder under `context/` its drafts belong to, such as `context/regulatory/` |
| `status` | `draft`, `testing` or `released`. Nothing reaches `released` without three testers |

### Declaring reads and writes

**Directories with patterns, never enumerated file lists.** `context/regulatory/**` is correct.
Listing four specific filenames is not, because the list goes stale the moment someone adds a fifth
file and the failure is silent. The folder structure is the index; a skill that reproduces part of
that index inside itself has built a second one that nobody maintains.

**Narrow by default.** Declare the domains the job needs and no others. A skill that reads the whole
context folder in case something is relevant fails review — that is a standard, not a preference.
The one exception is `issues-list`, because issues cross every domain. It declares all eight and
reads one only where an issue or a note points into it.

**Prefer digests.** Where a domain has a digest, read it instead of the full corpus, and pull raw
files only when the job genuinely needs them. A digest is a short summary a person reviewed and
approved, which is what makes it the right thing to send to a model.

**A context domain includes its drafts.** Drafts sit in their domain beside the records, named
`_draft`, so declaring `context/regulatory/**` reads both. The skill weighs drafts below the
domain's other documents, in the order the context standard sets, and cites any draft it relies on
as an unreviewed draft.

**Anything outside the declaration requires asking**, naming the file and why. The user's answer is
written back to the context map, so the same question is not asked twice.

## Every skill checks the layout first

Before anything else, a skill looks for an `outputs/` folder at the company root. Companies set up
before MOS 0.3 have one, and their drafts are in it. Where it is there, the skill runs
`python mos/lib/layout.py check`, shows the user what it lists, and explains it in a sentence:
drafts now sit in `context/` beside the records they would revise, and the filename says which is
which. On a yes, it runs `layout.py apply`. For each file listed as left over, it asks whether to
delete it, move it where the script suggests, or leave it, and passes those answers to `apply` as
`--delete` and `--move`. On a no, it reads the drafts where they are, in `outputs/<domain>/`, and
writes its own draft there too, so one company's drafts stay in one place; it says so, and that
the next skill will ask again.

## Every skill offers clean copies

A draft is reviewed in Word, between runs, and then needs its clean copy: the version without the
working notes that goes for signature. People forget that step, so skills ask. For each `_draft`
a skill reads, it asks once: *"Is the review of this document finished, and is it ready to route
for signature?"* On a yes, it runs `python mos/lib/mosdocx.py clean <file>`, shows what it says it
will do, and runs it with `--apply` on a second yes. `clean` refuses while the draft has tracked
changes or comments, writes `_revA` without the working notes, and keeps the full draft in
`archive/`. MOS approves nothing: the clean copy becomes the record when it is signed in the
company's quality system. `issues-list` is the exception; its list is a working document, never
signed.

## Every skill works at three levels of context

This is the requirement that separates a MOS skill from a prompt with a template attached. Write the
steps so the skill degrades cleanly rather than failing.

| Context available | What the skill must still do |
|---|---|
| None | Produce a good template and walk the user through filling it, explaining why each part exists |
| Partial | Draft from what exists, interview for the rest, and say which is which |
| Full | Draft traceable to existing documents, and flag contradictions rather than resolving them silently |

Test all three before submitting. The empty case is the one contributors skip and the one new users
hit first.

## Skills build context, not only consume it

A skill that interviews a user is generating context. When someone says the agency pushed back on
the population, that belongs in `context/regulatory/` — not evaporating with the session.

Offer to write it, name the file, and let the user decide. Skills never write into `context/`
without the user approving that specific write, and that includes their drafts. A person makes a
draft a record: its clean copy goes for signature in their quality system.

A draft informs later skills whether or not anyone has made its clean copy. So a skill starts by reading the
drafts in its declared domains as well as the records, and says which it is relying on: a reviewed
record, or an unreviewed draft. Where they disagree, it asks.

## Skills hand off what they did not settle

Every run finds things it cannot settle: a question the founder could not answer, two documents
that disagree, an assumption the analysis had to make, a target product profile row its findings
contradict. None of them goes in the skill's own document. They go on the company's issues list,
which the context standard describes, so that every open item has one home.

The last step of every skill is the same:

1. List what this run found and did not settle, each with its type (question, conflict, gap,
   assumption, risk to the plan), its domain, what it blocks and the next step. Check the current
   issues list first, and leave out anything already on it, unless this run found something new
   about it — then say so on that line.
2. Show the list. On a yes, write it to `context/inbox/<YYMMDD>_issues_<skill>.md`, in the format
   the context standard gives.
3. Ask the user to run `issues-list` now, while the session still holds what was found, to add
   them to the issues list and see what else this run settled.

A skill never edits the issues list itself. Where a run found nothing unsettled, it says so, and
writes no note.

Some of what a run finds the user can decide on the spot: keep a target product profile row or
change it. A skill may ask, one item at a time, and send the answer on the note with `Decided:` —
what, by whom, when — and a `Revise:` line naming the document, the row, what it says now and what
it should say, in the form the context standard gives. `issues-list` logs such an item as closed.
The skill still edits nothing: the team makes the revision, and for the target product profile,
`setup` drafts it from the closed issues.

## Skills test what users bring

When a user brings a decision — a product code, a predicate, a class, a pathway, an intended use —
or a document that records one, the skill reads it and does its own analysis before relying on
it. Where the analysis disagrees, the skill says so plainly, shows the evidence, and asks the user
to reconsider.

It does not adopt the user's answer only because the user gave it, and it does not overrule the
user either: the decision is theirs, and their reasons may be ones the skill cannot see. Once the
user has heard the challenge and confirmed their direction, the skill accepts it, records in its
output that the direction was confirmed over a challenge, and builds on it.

## Outputs are drafts

Everything a skill produces lands in `context/<domain>/` as a pre-decisional draft, named so that it
says so. It is not a controlled record until a qualified person reviews it and its clean copy is signed in
the company's quality system,
and a skill never writes into a path the map points at outside the company folder — that is often
the quality system. The AI is a tool; the human is the author.

A skill's `templates/` hold Markdown: the structure the AI fills. The deliverable is a Word document
built from that filled template by `lib/mosdocx.py render`, on the company's document template,
named `<document>_draft.docx`, or `<document>_rev<next>_draft.docx` where a record of it is already
there: `product-code_revB_draft.docx` beside `product-code_revA.docx`. No Markdown copy is kept
beside it. Where Python is not available, the skill writes the Markdown, `<document>_draft.md`,
instead and says so. The context standard covers how a draft becomes a record: `mosdocx.py clean` writes
the clean copy and moves the full draft into `archive/`.

A skill writes a separate Markdown record into `context/` only to record a decision that no
document holds — a code a person chose, not a restatement of the analysis that compared codes.

Every draft carries the disclaimer, as its last lines, inside the working notes, so the clean copy
that goes for signature does not:

> Generated with MOS and not reviewed. MOS provides no warranty. This document must be reviewed and
> approved by qualified personnel at your company before it is used for any regulated purpose.

### One skeleton for every document

The format of a document — cover, footer, fonts, page size — comes from the company's document
settings, and no skill sets its own. The structure comes from this skeleton, which every skill's
Markdown template follows so that one company's documents read as a set:

```markdown
# <Document name> — {{device}}

Company: {{company}}
Written: {{date}} · Source: MOS <skill> skill

*Notes: What this draft is and is not, and how its sources are marked.*

## <First body section>

...

## Appendix A: <Supporting material the record keeps>

...

## Working Notes

### <Search log, challenges, coverage checks>

...

---

*Generated with MOS and not reviewed. ...*
```

- **The `#` title and the lines before the first `##` go on the cover page.** Keep them to
  `Label: value` lines and one italic `*Notes: ...*` paragraph.
- **Body sections are `##` headings**, in title case where the name is a document term
  (*Intended Use*), sentence case otherwise.
- **Supporting material the signed record keeps goes in lettered appendices** — `## Appendix A:
  ...`, `B`, `C` — such as the evidence a conclusion rests on: FDA's records, labeling reviewed,
  study estimates. Each starts on a new page.
- **Material only the reviewers need goes under one final `## Working Notes` heading**, as `###`
  sections: the search log, coverage checks, lines set aside, the challenges a skill raised and how
  each was answered. `render` sets it on a new page under a banner and in italics, and `clean`
  leaves it, and everything after it, out of the clean copy. It must be the last section.
- **Open questions, gaps and unresolved contradictions are not in the document at all**: they go
  on the issues list.
- **No `---` between sections.** Page breaks and headings separate them. The one rule sits above
  the disclaimer.
- **`Label: value` lines** each become their own paragraph with the label in bold. Use them for
  short facts; write prose as prose.
- **Dates use the Date format in `context/templates/document-settings.md`**, wherever they
  appear. The cover and revision history are filled in by the script; dates the skill writes
  itself follow the same format.
- **A table of six or more columns** is set on landscape pages automatically. Design wide tables
  for that rather than squeezing them.

## What fails review

A skill is sent back if it:

- reads the whole context folder, or declares domains it does not use
- enumerates filenames instead of directories with patterns
- does nothing useful with no context
- writes into `context/` without the user approving that write
- keeps open questions in its own document, or edits the issues list, instead of handing them off
- accepts a decision the user brings without assessing it independently, or overrules one the
  user has confirmed
- reproduces text from ISO, IEC, AAMI or any other copyrighted standard — clause numbers are fine,
  clause text is not
- contains anything specific to one company
- needs more than one sentence to describe
- cannot state where it came from — see `PROVENANCE.md`. Original work, or outside material
  whose licence permits it and whose notice travels with it. "I asked an AI to write it" is an
  acceptable answer; "I do not remember" is not
- has no named maintainer, or no testers

## Running on other AIs

Skills are plain Markdown so that any capable AI can run them. Mirror `SKILL.md` to `AGENTS.md` at
the repository root so runtimes that look for that file find the same instructions. Skills are
designed and tested on Claude first and are expected to work elsewhere; where they do not, that is
a bug in the skill.

## Versioning

Skills are self-contained and versioned independently. A user can replace one skill folder without
touching the rest of `mos/`. Breaking a template's structure, or changing what a skill writes where,
is a minor version at least — someone's context depends on it.
