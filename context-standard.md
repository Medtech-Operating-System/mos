# The MOS context standard

*v0.2, 2026-09-23. The folder structure MOS skills read and write. This is the part of MOS that
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
└── outputs/                  <- drafts, before review. Not records
```

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

A skill writes its draft to `outputs/<skill>/`, named `<document>_draft.docx`. It becomes a record
when a person makes it one:

1. Review and redline the draft in Word.
2. Save the result as a new file with the revision in its name — `user-needs_revA.docx` — in the
   domain it belongs to, or in the quality system with the map pointing at it.
3. From then on, that file is the document. Skills read it and build on it. The draft in
   `outputs/` has done its job and can be deleted.

Saving the reviewed file into its domain is the step that turns a skill's output into context the
next skill can use. A draft left in `outputs/` is invisible to every skill that reads the domain.

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

Skills are plain Markdown, so they also run against a local model with nothing leaving the machine
at all. Output quality drops, and that path is documented rather than recommended.

## Status

v0.2. The layout, the map format and the conventions above are settled enough to build against, and
are expected to change once skills have run against real companies. v0.2 follows the first such run:
deliverables moved to Word, and `templates/` and the path from draft to record were added.

Open, and worth arguing about:

1. Are eight domains the right cut, or does `design/` want splitting?
2. Should the map carry per-path dates, so skills can tell recent work from archaeology?
3. What is the minimum a two-person company adopts on day one without it feeling like bureaucracy —
   is it `product/` and the map, and nothing else?
4. Should the device profile become a Word deliverable too? It is reviewed like one, but every skill
   reads it, and it is kept in Markdown for now for that reason.
