---
name: setup
description: Map a company's existing files and interview them about their device, producing a context map and a populated context folder. Use this the first time someone runs MOS, or when their context map needs rebuilding.
version: 0.3.0
maintainer: Eric Sugalski
phase: [all]
discipline: [all]
reads:
  - context/context-map.md
  - context/product/**
  - context/templates/**
writes:
  - context/context-map.md
  - context/product/device-profile.md
  - context/templates/
status: draft
---

# Setup

This is the first tool anyone runs. It produces the **context map**, which tells every other MOS
tool where the company's work lives and what it may read; the **document settings** and the
**document template** built from them, which give every Word document MOS writes the same format;
and the **device profile**, which tells tools what the device is.

Budget about twenty minutes. Most of it is the interview in step 8; the mapping in steps 2–5 goes
fast because the user is confirming proposals rather than writing anything.

Read `mos/context-standard.md` before starting. It defines the eight domains, the map format and
the conventions used throughout these steps.

## Rules for this tool

- **Do not read file contents while mapping.** Steps 2 and 3 use directory and file *names* only.
  Names are enough to propose a map, and reading a company's documents before they have told you
  what is readable inverts the whole point of the map.
- **Do not move, rename, copy or reorganize anything the user already has.** Mapping points at
  files where they sit. If a folder is badly organized, say so once and map it anyway.
- **Do not invent answers.** Anything the user does not know is written as `Not known yet`. A
  guessed device class or a plausible-sounding intended use is worse than a blank, because it looks
  like a decision someone made.
- **Confirm before every write**, showing the full content first. This tool writes into `context/`,
  which no tool does without explicit approval.
- **Install nothing without asking.** Step 7 may need Python. Say what it is for, name the
  command, and run it only on a yes.

## Steps

### 1. Find out where you are

Check for `context/context-map.md`.

- **It exists** — this is a re-run. Read it, tell the user what is currently mapped, and ask
  whether they want to add newly created areas, revise what is there, or start over. Skip to the
  step that matches. Never overwrite an existing map without showing what changes.
- **It does not exist** — ask one question before anything else: *does the company already have
  files for this device somewhere, or are we starting from nothing?* Everything downstream forks
  here.

Confirm the company root — the folder `context/`, `mos/` and `outputs/` sit inside. Everything in
the map is relative to it where possible.

Ask for the company's name as it should appear on its documents. Do not take it from the folder
name, and do not confuse it with the device name.

### 2. Look around

Skip if starting from nothing.

Ask the user where their work lives — a drive letter, a synced folder, a few separate locations.
List the directory names under each, three levels deep. File names, not contents.

Report back what you found in plain language: how many folders, what they appear to be, anything
that looks like it holds more than one kind of work. Do not classify yet.

If a location is enormous — thousands of folders, or an entire shared drive — say so and ask the
user to narrow it to where this device's work lives. Mapping the whole company drive is how a map
becomes meaningless.

### 3. Propose a map

Go domain by domain, in the order the context standard lists them. For each one, propose the paths
you believe belong to it and ask the user to confirm, correct or say *not mapped yet*.

Work in batches of two or three domains, not one at a time and not all eight at once.

Where a folder name is ambiguous — `Documents`, `Project files`, `Old stuff` — ask about it once,
by name, rather than guessing. Where a folder clearly holds several domains, map it once per domain
with a narrowing path, or exclude the parts that do not belong.

A domain with nothing to map gets `- not mapped yet`. Do not force a match.

### 4. Flag what should stay out

Before writing anything, ask directly about the four categories the context standard treats as
restricted regardless of mapping:

- Patient health information or subject-level clinical data
- Anything under a BAA or a third-party NDA
- Unfiled patent material — mention this one explicitly, because it is the category founders
  most often have not thought about
- Crown-jewel process or formulation detail

Anything named here goes in the map as a `restricted:` line, with a short reason. Where a
restricted area has a de-identified summary or a pointer document, map that instead so tools know
the material exists.

Also scan the folder names you listed for anything that looks like it belongs in these categories —
`subjects`, `PHI`, `provisional`, `patent`, `IRB` — and raise it. Advisory only. The user decides.

### 5. Write the context map

Fill `templates/context-map.md` with what steps 2–4 produced. Show the user the complete file.
Confirm. Write it to `context/context-map.md`.

Tell them plainly what the file means: anything listed is readable by MOS tools, anything not
listed is invisible to them, and they can edit it by hand at any time.

### 6. Scaffold what is missing

Create `context/`, `outputs/`, `context/inbox/`, `context/templates/`, and a folder for each of
the eight domains that does not already map to an existing location. List what you created.

Do not create subfolders inside the domains. Do not create placeholder files.

### 7. Set up Word documents

Every MOS tool delivers its work as a Word document, built from one company template by the script
`mos/lib/mosdocx.py`, and reads the Word documents the company has reviewed. This step makes sure
that works, and builds the template.

**Check first.** Run `python mos/lib/mosdocx.py check`. If `python` is not found, try `python3`,
then `py -3`. Whichever works is the command every later tool uses; say which.

**If none works**, explain what it is for in one sentence — MOS writes and reads Word documents
through a short script, and the script needs Python — and ask whether to install it:

- Windows: `winget install --id Python.Python.3.12 -e`
- macOS: `brew install python`, or the installer from python.org
- Linux: the distribution's package manager

Run it only on a yes, then run the check again. Nothing else is installed: the script uses Python's
standard library and no packages.

**If the user declines**, or you cannot run commands in this environment, say plainly what follows:
tools will write their drafts as Markdown files instead of Word documents, and cannot read `.docx`
files. Skip the template and continue with step 8. Running setup again later picks this step up.

**Then the document format.** Every document MOS writes for this company — user needs today, a
risk plan or a design input list later — gets the same cover page, footer, font and page layout.
This step decides that format once, writes it down in `context/templates/document-settings.md`,
and builds the template every document starts from. The script reads the settings every time, so
consistency does not depend on anyone remembering them.

Ask first: *does the company already have a controlled Word template for its quality documents?*

**If it does**, use theirs. Ask for the file and copy it to
`context/templates/document-template.docx`. Check it:

```
python mos/lib/mosdocx.py inspect
```

The report lists the fields MOS fills — `{{document_name}}`, `{{document_number}}`,
`{{revision}}`, `{{related_documents}}` — and where the template has each one. For any marked
`MISSING`, tell the user where it would normally go, and that they add it by typing the field,
braces included, into the template in Word. The template's body becomes the cover page of every
document, and the content starts on the page after it. Then write the settings from
`templates/document-settings.md` with `Template: Company`; only Company, Date format, Document
number and First revision matter in that case.

**If it does not**, ask about the format in one batch, offering the defaults so that a user who
does not care can accept them all at once:

- The logo — a PNG or JPEG file, by path. Copy it to `context/templates/logo.png` (or `.jpg`) so
  the template can be rebuilt later from files the company controls. No logo is fine; the
  company name takes its place.
- Font and body size — default Calibri, 10.5 pt.
- Page size — Letter or A4. Default Letter, and A4 for a company outside North America.
- Date format — M/D/YYYY, YYYY-MM-DD or DD-Mon-YYYY. Default M/D/YYYY.
- Document numbering — the pattern, if the company has one (`DOC-XXXX`), and the first revision
  (`A`, `01`). Default is to leave both as placeholders until a document is numbered.
- A page header — off by default. On adds the logo at the left and the document number and
  revision at the right of every page but the cover.

Fill `templates/document-settings.md`, show it in full, confirm, and write it to
`context/templates/document-settings.md`. Then build the template:

```
python mos/lib/mosdocx.py template
```

It writes `context/templates/document-template.docx`: a cover page with the logo top left, a
control table holding Document Name, Document Number, Revision, and Related SOPs / Template Files
with their release dates, and a revision history table; a footer on every page with the company
name, the document name and revision, and the page number; and the header if it is on.

Tell the user how to change the format later: edit a value in `document-settings.md` and run
`python mos/lib/mosdocx.py template --force`. The next document follows the new settings;
documents already written keep theirs. Editing `document-template.docx` in Word by hand also
works, but the next rebuild from the settings replaces it — changes that should last belong in
the settings.

### 8. Interview about the device

**First, read whatever the map points at in `product/`.** If the company already has an intended
use statement, a device description or a pitch deck in a mapped location, read it and ask about
what is missing rather than about everything. Say which answers you drew from existing documents,
and where they came from.

Ask in batches, grouped by topic. Nine areas, and the user is allowed to not know:

1. **The device.** What it is physically or technically. What it does. Hardware, software,
   consumable, or a combination. Sterile, implanted, energy-delivering, patient-contacting.
2. **Users and setting.** Who operates it, who it is used on, and where — hospital, clinic, home,
   ambulance, laboratory. Whether a lay user ever touches it.
3. **What it is for.** The intended use in one sentence. Indications for use if they exist.
   The clinical problem, and what people do today instead.
4. **Stage.** Where the project actually is, mapped to a phase on the lifecycle map: concept,
   definition, design, verification and validation, submission, launch, or post-market. Ask what
   they are working on this month — it is a better question than asking them to pick a phase.
5. **What already exists.** Which documents they have, even in draft: intended use, user needs,
   risk file, design inputs, test reports, a submission. This tells later tools what to build on.
6. **Regulatory position.** Target geography. Expected class. Intended pathway if chosen — 510(k),
   De Novo, PMA, CE mark. A predicate or comparable device, if they have one in mind. Any agency
   contact so far.
7. **Risk profile.** Invasiveness, software level of concern, sterility, biocompatibility,
   electrical or radiation safety, and whether any part is novel enough that there is no standard
   to point at.
8. **Timeline and constraint.** The date that matters and what it is driven by — funding, a study,
   a partner, a competitor. What is most likely to slip.
9. **Team.** Who does what, what is outsourced, and which disciplines nobody covers. This tells
   later tools how much to explain.

Do not ask all of these if the answers are already in front of you, and do not ask a question a
company at concept stage cannot possibly answer. Skip ahead when the user says they do not know
yet, and write `Not known yet`.

### 9. Write the device profile

Fill `templates/device-profile.md`. Show it in full. Confirm. Write it to
`context/product/device-profile.md`.

Where an answer came from an existing document, cite that document's path in the profile. Where it
came from the interview, say so. A later reader needs to know which statements have a source and
which are someone's recollection on a Tuesday.

### 10. Report and hand off

Tell the user:

- What was created, by path
- Which domains are mapped, which are scaffolded and empty, and which are `not mapped yet`
- What is marked restricted
- Whether Word output works, with which Python command, and whose template is in use — the one
  built from the settings, with or without a logo, or the company's own
- Anything you noticed and did not act on — several revisions of one document outside `archive/`,
  a domain that looks like it holds two kinds of work, a location they mentioned but never mapped

Then say what to do next, based on their stage. Do not name a tool that has not shipped. Where the
obvious next step has no tool yet, say that plainly — it is true, and it is how the roadmap gets
built.

Point at `context/inbox/` and explain it: anything useful that turns up — a call summary, a
supplier email, meeting notes — goes in there, and gets filed later. Capture is the step that
fails.

Finally, explain how MOS is updated, because it decides where their work must live:

- **`mos/` is replaced whole, never patched.** A newer MOS comes as one download holding every
  tool. To update, delete the `mos/` folder and unzip the new one in its place. There is no
  per-tool download.
- **Nothing of theirs is in `mos/`, so nothing of theirs is lost.** The context map, the device
  profile, the document settings and template, and every draft live in `context/` and `outputs/`,
  which an update never touches. That is why nothing in `mos/` should ever be edited: a change
  made there disappears at the next update. Anything the company wants to customize belongs in
  `context/`.
- **They choose when to update.** Keeping the download they are using lets them stay on a version
  they have reviewed, which matters if MOS output feeds their quality system. Updating is a
  decision, not something that happens to them.
- **When updating, also remove the entries in `.claude/skills/` that came with MOS** — one folder
  per tool, named after the tool — before unzipping. Unzipping adds files but never deletes them,
  so a tool that a later release retires would otherwise stay listed. Their own skills in the
  same folder are not touched.

## Working at three levels of context

| What the company has | How this tool behaves |
|---|---|
| Nothing | Skips steps 2–4, scaffolds the layout, sets up Word output, and runs the full interview. Produces a map pointing only at the new `context/` folders, and a device profile built entirely from the conversation |
| Some files | Maps what exists, and the interview starts from what those documents already say. Asks about gaps, not about everything |
| A full document set | Most of the work is mapping. The interview becomes a confirmation pass, and step 10 is where the value is — naming what is missing, stale or duplicated across a set the company thought was complete |

## Where this tool is weakest

Recorded so it gets fixed rather than rediscovered:

- Mapping a large shared drive by folder name alone is guesswork. The proposal is only as good as
  the company's naming, and some companies name folders after people.
- The interview cannot tell a confident wrong answer from a correct one. A founder who believes
  they are Class II when they are Class III will produce a device profile that says Class II, and
  every downstream tool inherits it.
- A company's own Word template works only if its fields survive editing. Word sometimes splits
  typed text like `{{revision}}` into pieces internally, and a split field is not found.
  `mosdocx.py inspect` reports the fields it cannot find, and the user re-types them.
- There is no check yet that a mapped path still exists. A map written today survives a
  reorganization six months from now only until someone runs a tool and it fails.
