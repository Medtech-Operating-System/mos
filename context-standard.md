# The MOS context standard

*v0.8, 2026-10-17. The folder structure MOS skills read and write. This is the part of MOS that
compounds: skills are replaceable, context is not.*

Two things live on your machine. **Your context** — the files your company already has, wherever
they already are. And **`mos/`** — the skills, downloaded, replaceable, holding nothing of yours.

This document defines the first. It is deliberately small. A two-person company should be able to
adopt it in an afternoon and still be using it at fifty people.

## Two ways in

**You already have files.** Most companies do. MOS maps them where they sit. You keep your folder
names, your structure and your drive letters. Nothing is moved, renamed or copied. What you write
is a **context map**: a short file that says which of your existing folders holds which kind of
work.

**You are starting fresh.** MOS scaffolds the layout below, and the map points at it.

Most companies are a mix — some domains mapped to existing folders, some scaffolded empty and
filled in as the work happens. That is the expected state, not a transitional one.

## The layout

```
Acme Medical/                 <- your folder; sync it with anything, or nothing
├── mos/                      <- downloaded; replaceable; yours to delete
├── context/
│   ├── context-map.md        <- what MOS can read. Read first by every skill
│   ├── 261016_issues-list.docx  <- what is open, across every domain. Dated
│   ├── document-register.md  <- every document's number, revision and status
│   ├── inbox/                <- drop anything here; triaged later
│   ├── templates/            <- document settings, and the template built from them
│   ├── product/
│   ├── users-and-needs/
│   ├── risk/
│   ├── design/
│   ├── manufacturing/
│   ├── clinical/
│   ├── regulatory/
│   │   ├── standards/        <- standards your company has bought, if any
│   │   └── labeling/         <- other devices' labeling, one folder per device
│   └── commercial/
│       ├── reimbursement_draft.docx     <- written by MOS, not yet reviewed
│       └── differentiation_revA.docx    <- reviewed: a record
```

**One folder, and the filename says the status.** Everything lives in `context/`, by domain: your
own files, MOS drafts, and the records the team made from them. A draft is named
`<document>_draft.docx`, a record `<document>_revA.docx`, and a proposed change to a record
`<document>_revB_draft.docx`, beside the revision it would replace. A draft's place is obvious
before it is written, and reviewing it does not move it anywhere.

**Skills read drafts and records alike.** Everything MOS has drafted informs the skills that run
after it, reviewed or not. What changes with review is how far a skill trusts a document, not
whether it can see it: see *Which source wins* below.

**MOS writes only into this folder.** Where the map points a domain at your own controlled filing
— `S:/Quality/Regulatory Affairs/`, say — MOS reads it and never writes to it. Its drafts go in
the local `context/<domain>/`, and the map lists that folder too; where it does not yet, the skill
adds the line when it writes its first draft there, as part of that approved write. An unreviewed AI draft does not
belong in a quality system; the team files the reviewed document there themselves.

### The eight domains

Ordered by how the work flows: what the device is, who needs it, what can go wrong, how it is
designed, how it is made, what the evidence says, what the agency needs, and how it reaches a
market. Domains are where artifacts live, which is not the same cut as the disciplines on the
lifecycle map — a document in `design/` is usually the work of more than one discipline.

| Domain | What belongs here |
|---|---|
| `product/` | What the device is. The target product profile, the device profile, and the company's own device description, intended use or pitch material. The first thing every other skill reads |
| `users-and-needs/` | Who uses it and what they need. User needs, use environments, user profiles, use-related research |
| `risk/` | The risk file. Hazard analysis, risk management plan and report, risk controls and their verification |
| `design/` | Design inputs and outputs, design reviews, specifications, drawings, software architecture, verification and validation plans and reports |
| `manufacturing/` | How it gets made. Process development, make-versus-buy, suppliers, process validation, cost of goods |
| `clinical/` | Evidence. Clinical strategy, protocols, investigator materials, reports, literature, post-market clinical follow-up |
| `regulatory/` | Pathway and correspondence. Classification, predicate analysis, submission strategy, agency meetings and their minutes, the standards list, labeling, and in `standards/` the standards the company has bought |
| `commercial/` | Market and money. Market analysis, competitive landscape, pricing, reimbursement and coding, launch and distribution plans |

Empty domains are normal. A company at concept stage has three of these, and that is the correct
state for a company at concept stage.

## The context map

`context/context-map.md` is the file that makes MOS work on your machine. It says what exists and
where. **It is also the access boundary: anything not in the map is invisible to MOS skills.**

That is deliberate. A list of folders to avoid fails open — anything you forget to mark stays
readable, and you never find out. A list of folders to read fails closed: forgetting something
means a skill does not see it, which is visible and harmless. You write the map anyway to make
skills work at all, so there is no second chore.

### Format

One `##` section per domain. Under each, the paths that belong to it.

```markdown
# Context map — Acme Medical

Root: C:/Acme Medical
Last reviewed: 2026-09-20

## product
- `./context/product/` — created by MOS

## regulatory
- `S:/Quality/Regulatory Affairs/` — 510(k) work, agency correspondence
- `S:/Quality/Standards list.xlsx`
- exclude: `**/archive/**`

## clinical
- `S:/Clinical/Study 001/protocol/`
- restricted: `S:/Clinical/Study 001/subject-data/` — PHI. De-identified summary
  lives in `./context/clinical/study-001-summary.md`

## commercial
- not mapped yet
```

Three kinds of line:

- **A path** — a folder or a single file, with an optional note after an em dash. A folder includes
  everything under it.
- **`exclude:`** — a pattern inside an otherwise-mapped path that skills skip.
- **`restricted:`** — material that exists, is named, and is not to be read. The convention is that
  restricted holds the real thing while the mapped domain holds a de-identified summary or a
  pointer, so a skill knows a study exists and what its endpoints were without opening a subject
  record. This is what keeps minimization from making skills stupider.

Write `- not mapped yet` rather than deleting a domain heading. An empty heading is a question
someone can answer later; a missing one is invisible.

### Restricted by default, mapped or not

Four categories stay out regardless of what the map says:

- **PHI and subject-level clinical data**
- **Anything under a BAA or a third-party NDA**
- **Unfiled patent material** — the public-disclosure risk founders miss until their attorney
  raises it
- **Crown-jewel process or formulation detail**

### The map grows as you use it

You will not classify everything up front, and you should not try. People classify badly in the
abstract and well in context. A skill needing something outside the map asks for that file, names
it, and says why. Your answer is written back into the map. After a few weeks the map reflects
decisions you actually made rather than ones you anticipated.

### What this is not

These are conventions a cooperative AI follows. They are not a sandbox and not file permissions.
They lower the error rate; they do not eliminate it. A company that cannot tolerate a single
mistake should keep restricted material outside the working folder entirely, or deny the AI's
account access at the operating-system level.

## Conventions

### File formats

**Readable formats only: `.md`, `.docx`, `.xlsx`, `.pdf`, `.csv`, `.txt`.** Cloud-native stubs —
`.gdoc`, `.gsheet`, a SharePoint shortcut — contain a link and no content. An AI reading one learns
nothing. If your documents live in a cloud editor, sync them down or export.

MOS writes two kinds of file, in two formats:

| Kind | Format | Why |
|---|---|---|
| **Working files** — the context map, the device profile, digests | Markdown | Skills read these far more than people do. Markdown diffs cleanly, reads the same in every AI, and a founder can edit the map by hand |
| **Deliverables** — user needs, and every document a skill drafts for review | Word | Deliverables are reviewed, redlined and filed, and that happens in Word |

Deliverables are Word only, with no Markdown copy beside them. A copy goes stale at the first
redline, and a skill that later reads the stale one cites a version nobody approved.

Word documents are written and read by one script, `mos/lib/mosdocx.py`, so every document has the
same cover page, footer and styles whichever AI ran the skill. It needs Python 3.8 or later and nothing
else; `setup` checks for it and asks before installing it. Skills try `python`, then `python3`,
then `py -3`. To read a Word document, a skill runs `mosdocx.py read <file>`, which shows tracked
changes as if accepted and says how many are outstanding. Where Python is not available, skills
write Markdown and say so.

### `templates/`

Two files make every document a company receives from MOS look the same:

- **`document-settings.md`** — the company's document format, written down: company name, logo,
  font and body size, page size, date format, document numbering, first revision, and whether
  pages carry a header. Plain `Key: value` lines a person can read and edit. `setup` writes it.
- **`document-template.docx`** — built from those settings, and the base of every deliverable:
  a cover page with the logo, a control table (Document Name, Document Number, Revision, Related
  SOPs / Template Files with their release dates), the draft's opening lines and a revision
  history table; a footer on every page with the company, the document name and revision, and the
  page number; and a slim header if the settings turn one on.

The script reads the settings every time it writes a document, so consistency does not depend on
an AI remembering them. To change the format, edit the settings and rebuild the template with
`mosdocx.py template --force`. Documents already written keep their format; the next one follows
the new settings.

A company with its own controlled template puts it in place of the built one, and the settings
say `Template: Company` so MOS never overwrites it. Its body becomes the cover page, and its cover
and footer need the fields `{{document_name}}`, `{{document_number}}`, `{{revision}}` and
`{{related_documents}}` where those values belong; `mosdocx.py inspect` reports which it has.

Like `inbox/`, `templates/` is always in scope and needs no line in the map.

### From draft to record

A skill writes its draft to `context/<domain>/`, named `<document>_draft.docx`. Where a record of
the document is already there, the draft names the revision it proposes:
`user-needs_revB_draft.docx` beside `user-needs_revA.docx`. A draft ends with a section headed
**Working Notes**, in italics: what its reviewers need and the signed document does not, such as
the search log, coverage checks and the challenges a skill raised.

It becomes a record when a person makes it one:

1. Review and redline the draft in Word.
2. Accept or reject every change, and delete the comments.
3. Make the clean copy. MOS skills offer to when they find a draft whose review is finished, or run
   `python mos/lib/mosdocx.py clean <draft> --apply`. It writes `user-needs_revA.docx`, or `_revB`
   for a `_revB_draft`, without the working notes, and moves the full draft, and the revision it
   replaces, into `archive/`.
4. Route the clean copy for signature in your quality system. It becomes the record when it is
   signed. MOS approves nothing and records no signature. Where the company files records in its
   quality system, file it there with the map pointing at it, and delete the copy from `context/`.

**One document, one current file.** Outside `archive/` there is one record and at most one draft.
The full draft kept in `archive/` holds the reasoning behind that revision; skills never read it.

A draft that has no clean copy yet still counts: later skills read it, and say that they are
relying on an unreviewed draft. A clean copy is something they can rely on without saying so.

**A separate record only records a decision.** Most of what a skill produces lives in its
document. Where a person makes a decision the document does not hold — the analysis compares
product codes, and a person chooses one — a skill writes a short Markdown record of that decision
to the domain, with the user's approval. It never writes a record that restates a document.

### The document register

`context/document-register.md` lists every document MOS writes for the company: its number,
title, current file, revision and status. `setup` writes it, and `mos/lib/mosdocx.py` keeps it up
to date, so nobody has to remember to. A new draft gets the next number for its domain's prefix —
`DIR-001` for the design inputs, `REG-002` for the second regulatory document — and keeps that
number through every revision; each clean copy records its revision. The number goes on the cover
and in the footer. The prefixes are in the register, and the company may change them.

A company whose quality system assigns document numbers sets `Numbering: Quality system`. MOS then
assigns none: the team enters the number its system gives each document, and MOS uses it from then
on.

The status is `Draft`, `Draft of rev B`, `Clean copy, for signature`, `In quality system` — which
the team sets once the document is signed and filed — or `Retired`. A retired number is never
reused. The issues list and the decision records are not numbered.

### The target product profile and the device profile

`setup` writes two documents about the device, and each fact has one home:

- **The target product profile** records what the product must be: what the device is, its use and
  indications, its clinical and technical performance, usability, claims, price and cost of goods,
  regulatory expectations and milestone dates — each number at a minimum acceptable and a target
  level. It is a deliverable: a Word draft, `context/product/target-product-profile_draft.docx`,
  redlined by the team, and its clean copy is `target-product-profile_revA.docx`. It is the reference every skill reads for
  the product.
- **The device profile**, `context/product/device-profile.md`, records where the project is: stage,
  what already exists, agency contact so far, risk notes, what drives the timeline, and the team.
  It is a working file, and it says where the target product profile is.

**Skills never edit the target product profile.** When a skill finds something that bears on a row
— an expected class FDA's records do not support, a price the payment cannot carry, indications the
team chose in another form — it raises it as an issue for the issues list: the row, what it says
now and what the skill found. The team decides. A skill may put the question to the user during its
run, and send the answer with the issue. Once the issue is closed, `setup` drafts the next revision
from it: it reads the closed issues whose resolution revises a row, applies each change the team
confirms, and lists each in the revision's *Changes in this revision* appendix with the issue's
ID. The team reviews that draft like any other. A team that prefers to redline the profile in
Word may; `setup` then finds the row already says what the resolution asks, and leaves it.

A device profile written by a `setup` before 0.5.0 holds the product facts itself. Skills read them
there when no target product profile exists, and suggest re-running `setup`, which converts it.

### The issues list

Developing a device turns up questions faster than anyone answers them. The issues list is where
every one of them goes: one Word document for the company, across every domain, kept by the
`issues-list` skill. A question in one document's appendix is found only by someone who opens that
document; a question on the list is seen by the whole team.

| Type | The plain question |
|---|---|
| **Question** | What has not been decided yet? |
| **Conflict** | Where do two sources, or two people, disagree? |
| **Gap** | What is missing that something else needs? |
| **Assumption** | What did we take as true so the work could go on? |
| **Risk to the plan** | What could move the schedule, the cost or the pathway? |

Each issue has an ID, `ISS-001` onward, never renumbered or reused; a domain, one of the eight;
what it blocks — a skill, a target product profile row, a milestone; an owner; a status, `Open`,
`Closed` or `Won't do`; and the next step, which becomes the resolution once it is closed. The
list is grouped by domain, and closed issues stay on it, at the end, with what settled them.

**Where it lives.** `context/<YYMMDD>_issues-list.docx` — `261016_issues-list.docx` for one
written on 16 October 2026. It is a working document, not a draft waiting for a clean copy; it is never signed. The team
edits it directly in Word between runs: changes a status, writes a resolution, adds a row, leaves a
comment. Each run of `issues-list` reads those edits and writes the next list under that day's
date, and the one it replaces moves to `context/archive/`. The archive is the list's history. If
more than one list sits outside `archive/`, the skill stops and asks, as it would for any
document.

**How issues reach it.** No other skill edits the list, and no skill's document carries its own
open questions: each issue has one home. At the end of a run, a skill lists what it found and did
not settle, and on the user's approval writes it to a note in `context/inbox/`, named
`<YYMMDD>_issues_<skill>.md`, one line per issue:

```markdown
# Issues from product-code — 2026-10-16

- **Conflict · regulatory** — The target product profile expects Class II; the closest product
  codes are Class III. Blocks: precedent-search; target product profile row 8.1. Next step: decide
  the classification; a pre-submission meeting with FDA would confirm it.
```

**Decided in the session.** Where the question is one the user can answer during the run — keep a
target product profile row or change it — a skill may ask, one row at a time. The answer goes on
the issue's line, with who decided and when, and a `Revise:` line where it changes a document:

```markdown
- **Question · product** — The predicate's labeling gives 12 hours of battery life; the target
  product profile's minimum is 8 hours. Blocks: target product profile row 4.2. Next step: decide
  the minimum. Decided: raise the minimum to match the predicate, by Jane Doe, 2026-10-17.
  Revise: target product profile row 4.2 — minimum from "≥ 8 h" to "≥ 12 h".
```

`issues-list` logs a decided issue as closed, with the decision as its resolution, and does not ask
the question again. An answer of *decide later* is an open issue like any other.

Then it asks the user to run `issues-list`, which logs each note and deletes it once logged. A note
nobody logs is still in `inbox/`, where the next run of `issues-list` finds it.

**Closing an issue.** `issues-list` proposes; a person confirms. Closing an issue never edits
another document: where the resolution changes one — a target product profile row, a claim — the
resolution names it in a `Revise:` line, and the team makes the next revision. For the target
product profile, `setup` drafts it from those lines.

**What does not go on it.** A hazard to a patient or user belongs in the risk file in `risk/`. A
complaint, a nonconformance or a corrective action belongs in the quality system. The list is not a
project schedule, and a decision, once made, lives in the document or decision record that holds
it; the closed issue points there.

### Which source wins

Skills weigh what they read in this order, highest first:

1. **Reviewed records** — a `_rev` file with no `_draft` in its name, and decision records.
2. **The company's other documents** — its own files, reviewed or not.
3. **MOS drafts** — any file named `_draft`, always cited as coming from an unreviewed draft.
4. **The conversation** — someone's recollection, not yet written down.

A lower source never overrides a higher one. Where they disagree, the skill says so and asks; it
does not pick one silently. Within a level, the newer revision wins, and a draft older than the
record it would revise is ignored as superseded.

### Revisions and `archive/`

Drafting against a superseded risk file is an error that survives into a submission. Three rules:

1. Put the revision in the filename: `risk-management-plan_revC.docx`.
2. Superseded revisions go in an `archive/` subfolder. **`archive/` is excluded by default
   everywhere**, without needing a line in the map.
3. Outside `archive/`, a document has one record and at most one draft of the revision after it.
   Where a skill finds more — two records, two drafts, a draft that names no revision beside a
   record — it stops and says so rather than guessing.

### `inbox/`

`context/inbox/` is always in scope. Drop anything in — meeting notes, a photographed whiteboard, a
supplier email, a call summary — with no decision about where it goes. Capture is the step that
fails, so its cost is set to zero.

Skills put one thing there themselves: a note of the issues a run found, for `issues-list` to log.
See *The issues list* above.

The trade is that something has to empty it. Until the context librarian skill ships, that is you:
move files into the right domain when you think of it. **An inbox nothing triages is a graveyard**,
which is why this is the only folder of its kind in the standard. There is no `notes/`, no `misc/`
and no `general/`.

### Standards you have bought

MOS ships no text from ISO, IEC, AAMI or any other copyrighted standard. Some work goes better
with one: a list of hazards is stronger when checked against the examples in ISO 14971 and
ISO/TR 24971.
If your company holds licensed copies, put them in `context/regulatory/standards/`, one file per
standard, with the number and edition in the filename: `ISO 14971-2019.pdf`. It is the one
subfolder the standard defines inside a domain, because the skills that use a standard need to
find it without searching.

A skill that finds one asks before reading it. Reading a standard sends its text to your AI
provider as part of the prompt, and some publishers' licence terms restrict putting their documents
into AI tools. Whether yours allows it is your decision, and MOS does not rule on it. A skill cites
clause numbers from your standards and never copies their text or tables into a draft: drafts are
shared, and your licence covers your copy, not the people you send a draft to.

Without the folder, skills work from public sources and say which check they could not do.

### Digests

A digest is a short summary of one domain that a person wrote or reviewed, and that skills read
instead of the whole corpus. It lives at `context/<domain>/_digest.md` and records what it was
built from:

```markdown
---
sources:
  - path: S:/Quality/Regulatory Affairs/
    as-of: 2026-09-14
built: 2026-09-14
reviewed-by: Eric Sugalski
---
```

Digests are optional and matter most once a domain is large. They are the main way to keep the
volume of text crossing into a model bounded, and unlike a search index, **a person approved the
contents before they crossed**.

Digests go stale — that is what the `sources` block is for. Raw files never do: skills read what is
on disk at the moment they read it. There is no index to re-sync and no cache to invalidate.

## Moving from an older layout

Before v0.6, drafts went to a separate `outputs/` folder and a person moved them into `context/` to
make them records. Where a skill finds an `outputs/` folder, it stops before anything else and runs
`mos/lib/layout.py check`, which lists every move and writes nothing. On a yes, `layout.py apply`
moves each draft into `context/<domain>/`, named by the rules above, moves downloaded reference
material such as FDA summaries to the same place, and adds each local domain folder to the map.
Files that do not fit — a leftover render input, a Markdown copy beside its Word draft — are listed
and left alone unless you say what to do with each. `outputs/` is removed once it is empty.

## What not to add

The structure fails by accumulating, so:

- **No `notes/`, `misc/`, `general/` or `temp/`.** Anything that becomes a place to avoid making a
  decision becomes a place nothing is ever found. `inbox/` is the one exception, and it exists on
  the condition that it gets emptied.
- **No deep nesting.** Two levels under a domain is plenty. Structure you have to navigate is
  structure people route around.
- **Do not pre-create folders for work you have not started.** An empty `clinical/` on day one is
  fine; eleven empty subfolders inside it is bureaucracy, and it teaches people the structure is
  decorative.
- **Do not reorganize your existing folders to match this.** Map them. The point of the map is that
  you do not have to.
- **Nothing company-specific goes into `mos/`.** It is downloaded, and it gets replaced.

## Where your data goes

MOS has no account, no server and no copy of anything. What you download is a folder of
instructions and templates.

The AI you use is a different matter, and worth being exact about. **When you use a cloud AI, the
contents of every file it reads are sent to that provider for processing** — as prompt text, for
that request. That is the provider your company already contracted with, and MOS adds no new party
to the flow. Nothing is persisted in a MOS database, because there is no MOS database.

The map is what makes that exposure bounded and predictable: you set what is reachable, you see
which files were opened by name, and you approve what comes back. What counts as confidential, and
which AI vendor's terms your company accepts, stay your company's decisions. MOS does not classify
your data for you and does not filter it — a filter that is right most of the time is worse than
none, because people trust it.

**Public records a skill searches.** Some skills search government databases. Those requests go
from your machine straight to the agency, not through MOS, and carry only generic terms: device
types, product codes, regulation numbers, conditions, competitor names. Never your product's name,
its indications, its claims, its description or any file's contents. Every request is shown to you
before it runs, and every one is logged in the document it produces.

| Service | Run by | Used by | What is sent |
|---|---|---|---|
| openFDA, FDA's device databases, fda.gov | FDA | `product-code`, `precedent-search`, `predicate-profile`, `differentiation`, `indications-strategy`, `hazards-id` | Generic device words, product codes, regulation and submission numbers, competitor names |
| eCFR | Office of the Federal Register | `product-code`, `precedent-search`, `hazards-id` | Regulation numbers |
| ClinicalTrials.gov | National Library of Medicine | `indications-strategy` | Conditions, generic device words, competitor names |
| Clinical Tables | National Library of Medicine | `reimbursement` | Generic procedure, device and condition words |
| Medicare Coverage Database, cms.gov | CMS | `reimbursement` | No search terms. The skill downloads Medicare's complete policy lists and searches them on your machine, then reads national policies by number |

`differentiation` also offers an optional web search for what competitors publish, `hazards-id`
one for similar devices' published labeling, and `predicate-profile` one for the labeling,
specifications and product pages of the devices you chose to study. Each runs through your AI
tool's own web search, under that provider's terms, sends brand names, manufacturer names, model
numbers and device categories, and runs only if you say yes.

`setup` offers to read your company's own public website. The page addresses go to your site
through your AI tool's own web access, under that provider's terms, and only if you say yes.

Skills are plain Markdown, so they also run against a local model, with nothing leaving the machine
but the public-record searches above. Output quality drops, and that path is documented rather than
recommended.

## Status

v0.8. The layout, the map format and the conventions above are settled enough to build against, and
are expected to change once skills have run against real companies. v0.2 follows the first such run:
deliverables moved to Word, and `templates/` and the path from draft to record were added. v0.3
makes drafts readable by every skill, organizes `outputs/` by the eight domains, and sets the order
in which sources are trusted. v0.4 adds the target product profile and gives each fact about the
device one home. v0.5 adds the issues list, which takes the open questions out of every other
document. v0.6 retires `outputs/`: drafts sit in `context/` beside the records they would revise,
the filename carries the status, and promotion is a rename. v0.7 adds `regulatory/standards/`, where
a company puts the standards it has bought so skills can use them without MOS shipping their text.
v0.8 adds the document register, `regulatory/labeling/` for other devices' labeling, issues
decided during a skill's run, the path from a closed issue to the next revision of the target
product profile, and working notes and the clean copy: a reviewed draft's working notes are left out of the
version that goes for signature, and the full draft is kept in `archive/`.

Open, and worth arguing about:

1. Are eight domains the right cut, or does `design/` want splitting?
2. Should the map carry per-path dates, so skills can tell recent work from archaeology?
3. What is the minimum a two-person company adopts on day one without it feeling like bureaucracy —
   is it `product/` and the map, and nothing else?
4. ~~Should the device profile become a Word deliverable too?~~ Answered in part: what the product
   must be moved into the target product profile, a Word deliverable. The device profile stays a
   Markdown working file for project status.
