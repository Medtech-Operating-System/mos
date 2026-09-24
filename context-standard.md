# The MOS context standard

*v0.3, 2026-09-24. The folder structure MOS skills read and write. This is the part of MOS that
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
│   ├── inbox/                <- drop anything here; triaged later
│   ├── templates/            <- document settings, and the template built from them
│   ├── product/
│   ├── users-and-needs/
│   ├── risk/
│   ├── design/
│   ├── manufacturing/
│   ├── clinical/
│   ├── regulatory/
│   └── commercial/
└── outputs/                  <- MOS drafts, before review. Not records
    ├── users-and-needs/      <- the same eight domains as context/,
    ├── regulatory/              created as skills write to them
    └── commercial/
```

**Two stages, one organization.** `context/` holds what your company stands behind; `outputs/`
holds what MOS drafted and nobody has reviewed yet. Both are organized by the same eight domains,
so a draft's place is obvious before it is written, and so is where it goes once reviewed.

**Skills read both.** Everything MOS has drafted informs the skills that run after it, reviewed or
not. What changes with review is how far a skill trusts a document, not whether it can see it: see
*Which source wins* below. Drafts are kept out of `context/` for one reason: for many companies,
the folders `context/` points at are their own controlled filing, and an unreviewed AI draft does
not belong there.

### The eight domains

Ordered by how the work flows: what the device is, who needs it, what can go wrong, how it is
designed, how it is made, what the evidence says, what the agency needs, and how it reaches a
market. Domains are where artifacts live, which is not the same cut as the disciplines on the
lifecycle map — a document in `design/` is usually the work of more than one discipline.

| Domain | What belongs here |
|---|---|
| `product/` | What the device is. Device description, intended use, indications for use, claims, current stage. The first thing every other skill reads |
| `users-and-needs/` | Who uses it and what they need. User needs, use environments, user profiles, use-related research |
| `risk/` | The risk file. Hazard analysis, risk management plan and report, risk controls and their verification |
| `design/` | Design inputs and outputs, design reviews, specifications, drawings, software architecture, verification and validation plans and reports |
| `manufacturing/` | How it gets made. Process development, make-versus-buy, suppliers, process validation, cost of goods |
| `clinical/` | Evidence. Clinical strategy, protocols, investigator materials, reports, literature, post-market clinical follow-up |
| `regulatory/` | Pathway and correspondence. Classification, predicate analysis, submission strategy, agency meetings and their minutes, the standards list, labeling |
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

A skill writes its draft to `outputs/<domain>/`, named `<document>_draft.docx`. It becomes a record
when a person makes it one:

1. Review and redline the draft in Word.
2. Save the result as a new file with the revision in its name — `user-needs_revA.docx` — in the
   domain it belongs to, or in the quality system with the map pointing at it.
3. Delete the draft from `outputs/`. **A promotion moves the document; it does not copy it.** From
   then on the reviewed file is the document, and one document never exists in two places.

A draft that is never promoted still counts: later skills read it, and say that they are relying
on an unreviewed draft. Promoting it makes it something they can rely on without saying so.

**A separate record only records a decision.** Most of what a skill produces lives in its
document. Where a person makes a decision the document does not hold — the analysis compares
product codes, and a person chooses one — a skill writes a short Markdown record of that decision
to the domain, with the user's approval. It never writes a record that restates a document.

### Which source wins

Skills weigh what they read in this order, highest first:

1. **Reviewed records in `context/`** — revisions a person saved into a domain, and decision
   records.
2. **The company's other documents in `context/`** — its own files, reviewed or not.
3. **MOS drafts in `outputs/`** — always cited as coming from an unreviewed draft.
4. **The conversation** — someone's recollection, not yet written down.

A lower source never overrides a higher one. Where they disagree, the skill says so and asks; it
does not pick one silently. Within a level, the newer revision wins, and a draft older than the
record it would revise is ignored as superseded.

### Revisions and `archive/`

Drafting against a superseded risk file is an error that survives into a submission. Three rules:

1. Put the revision in the filename: `risk-management-plan_revC.docx`.
2. Superseded revisions go in an `archive/` subfolder. **`archive/` is excluded by default
   everywhere**, without needing a line in the map.
3. Where a skill finds more than one revision of the same document outside `archive/`, it stops and
   says so rather than guessing.

### `inbox/`

`context/inbox/` is always in scope. Drop anything in — meeting notes, a photographed whiteboard, a
supplier email, a call summary — with no decision about where it goes. Capture is the step that
fails, so its cost is set to zero.

The trade is that something has to empty it. Until the context librarian skill ships, that is you:
move files into the right domain when you think of it. **An inbox nothing triages is a graveyard**,
which is why this is the only folder of its kind in the standard. There is no `notes/`, no `misc/`
and no `general/`.

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
| openFDA, FDA's device databases, fda.gov | FDA | `product-code`, `precedent-search`, `differentiation`, `indications-strategy` | Generic device words, product codes, regulation and submission numbers, competitor names |
| eCFR | Office of the Federal Register | `product-code`, `precedent-search` | Regulation numbers |
| ClinicalTrials.gov | National Library of Medicine | `indications-strategy` | Conditions, generic device words, competitor names |
| Clinical Tables | National Library of Medicine | `reimbursement` | Generic procedure, device and condition words |
| Medicare Coverage Database, cms.gov | CMS | `reimbursement` | No search terms. The skill downloads Medicare's complete policy lists and searches them on your machine, then reads national policies by number |

`differentiation` also offers an optional web search for what competitors publish. It runs through
your AI tool's own web search, under that provider's terms, and only if you say yes.

Skills are plain Markdown, so they also run against a local model, with nothing leaving the machine
but the public-record searches above. Output quality drops, and that path is documented rather than
recommended.

## Status

v0.3. The layout, the map format and the conventions above are settled enough to build against, and
are expected to change once skills have run against real companies. v0.2 follows the first such run:
deliverables moved to Word, and `templates/` and the path from draft to record were added. v0.3
makes drafts readable by every skill, organizes `outputs/` by the eight domains, and sets the order
in which sources are trusted.

Open, and worth arguing about:

1. Are eight domains the right cut, or does `design/` want splitting?
2. Should the map carry per-path dates, so skills can tell recent work from archaeology?
3. What is the minimum a two-person company adopts on day one without it feeling like bureaucracy —
   is it `product/` and the map, and nothing else?
4. Should the device profile become a Word deliverable too? It is reviewed like one, but every skill
   reads it, and it is kept in Markdown for now for that reason.
