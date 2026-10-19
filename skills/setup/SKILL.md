---
name: setup
description: Read a company's website, map its existing files and interview them about their device, producing a context map, a target product profile and a device profile. Use this the first time someone runs MOS, when their context map needs rebuilding, or to draft the next revision of the target product profile from decisions on the issues list.
version: 0.9.0
maintainer: Eric Sugalski
phase: [all]
discipline: [all]
reads:
  - context/context-map.md
  - context/*_issues-list.*
  - context/product/**
  - context/templates/**
writes:
  - context/context-map.md
  - context/document-register.md
  - context/product/device-profile.md
  - context/templates/
  - context/inbox/
  - context/product/
  - context/regulatory/standards/
status: draft
---

# Setup

This is the first skill anyone runs. It produces:

- the **context map**, which tells every other MOS skill where the company's work lives and what it
  may read;
- the **document settings** and the **document template** built from them, which give every Word
  document MOS writes the same format;
- the **target product profile**, a Word document recording what the product must be — its use,
  performance, claims, price, regulatory expectations and milestones, each at a minimum acceptable
  and a target level. The team redlines it, and every later skill reads it;
- the **device profile**, a short working file recording where the project is: stage, what already
  exists, the team and what drives the timeline.

Each fact has one home. What the product must be lives in the target product profile; where the
project is lives in the device profile.

Budget about thirty minutes. Most of it is the interview in step 8; the mapping in steps 2–5 goes
fast because the user is confirming proposals rather than writing anything. A company website,
read in step 1, makes the interview shorter still: most companies have already written down their
name, what the device does, who it is for and who is on the team, and it is all public.

Read `mos/context-standard.md` before starting. It defines the eight domains, the map format and
the conventions used throughout these steps.

## Rules for this skill

- **Do not read file contents while mapping.** Steps 2 and 3 use directory and file *names* only.
  Names are enough to propose a map, and reading a company's documents before they have told you
  what is readable inverts the whole point of the map. The company's public website is not a
  file on their machine, and step 1 reads it, on a yes, before the map exists.
- **A website is the company's marketing, not a record.** It is written for investors or
  customers, often ahead of the device, and may describe a version that does not exist yet. Use it
  to draft answers and to ask better questions, never as a confirmed answer. Every statement taken
  from it goes to the user to confirm, and is cited in what setup writes by page address and the date it
  was read.
- **Do not move, rename, copy or reorganize anything the user already has.** Mapping points at
  files where they sit. If a folder is badly organized, say so once and map it anyway.
- **Do not invent answers.** Anything the user does not know is written as `Not known yet`. A
  guessed device class or a plausible-sounding intended use is worse than a blank, because it looks
  like a decision someone made.
- **Record beliefs as beliefs, and flag what does not hold together.** An expected class, an
  intended pathway or a predicate the user names goes in the target product profile as the
  company's expectation, not yet checked; the template's regulatory section says so. `setup` does
  not search FDA's records, so it does not rule on them. But where answers contradict each other or the device — an implanted, life-sustaining
  device expected to be Class I; a 510(k) planned for a device the user says has nothing like it
  on the market — say so, explain why in plain words, and ask. Record what the user confirms.
  Name `product-code` as the skill that checks a classification against FDA's records.
- **Confirm before every write**, showing the full content first. This skill writes into `context/`,
  which no skill does without explicit approval.
- **Install nothing without asking.** Step 7 may need Python. Say what it is for, name the
  command, and run it only on a yes.

## Steps

### 1. Find out where you are

**First, the folder layout.** If an `outputs/` folder sits beside `context/`, this company was
set up before MOS 0.3, when drafts were kept there. Run `python mos/lib/layout.py check` and show
the user what it lists, with one sentence on why: drafts now sit in `context/` beside the records
they would revise, and the filename says which is which. On a yes, run
`python mos/lib/layout.py apply`. For each file it lists as left over, ask whether to delete it,
move it where the script suggests, or leave it, and pass the answers as `--delete <path>` and
`--move <path>`. On a no, read and write drafts in `outputs/<domain>/` for this run instead of
`context/<domain>/`, and say that the next skill will ask again.

Check for `context/context-map.md`.

- **It exists** — this is a re-run. Read it, tell the user what is currently mapped, and ask
  whether they want to add newly created areas, revise what is there, or start over. Skip to the
  step that matches. Never overwrite an existing map without showing what changes.

  Then check for a target product profile: the newest `target-product-profile_rev*.docx` in
  `context/product/`, or `target-product-profile_draft.docx` there.

  - **None, and `context/product/device-profile.md` holds sections such as "What the device is",
    "What it is for" or "Commercial intent"** — the profile was written by an earlier setup,
    before the target product profile existed. Say so, and offer to convert it: its product
    content moves into a new target product profile draft, and the device profile keeps only the
    project status. Nothing is lost, and nothing is asked twice: every answer the old profile
    holds carries over, and its sources go in the working notes. Then
    ask only for what the target product profile adds — the minimum acceptable and target values
    in step 8's last area, and the product summary. Write both through step 9.
  - **A reviewed revision exists** — never edit it. If the user wants to change what it says,
    build a new draft from that revision with the changes, list each change in the draft's
    *Changes in this revision* appendix, and write it through step 9. The team redlines it and
    saves it as the next revision.

  Then check the issues list — the newest `<YYMMDD>_issues-list.docx` in `context/` — for closed
  issues with a `Revise: target product profile` line. Each is a change the team decided, often
  during another skill's run. Leave out any whose row already says what the line asks for, and any
  already in a revision's *Changes in this revision* appendix. If any remain, say how many, and
  offer to draft the next revision from them; see **Revising the target product profile from the
  issues list**, below.
- **Only a draft exists, and its review is finished** — offer its clean copy: run
  `python mos/lib/mosdocx.py clean context/product/target-product-profile_draft.docx`, show what it
  says it will do, and run it again with `--apply` on a second yes. It writes `_revA` without the
  working notes and keeps the full draft in `archive/`. If it refuses because of tracked changes or
  comments, say what to do in Word first. MOS approves nothing: the clean copy becomes the record
  when it is signed in the company's quality system.
- **It does not exist** — ask one question before anything else: *does the company already have
  files for this device somewhere, or are we starting from nothing?* Everything downstream forks
  here.

**Revising the target product profile from the issues list.** Read the newest target product
profile — the reviewed revision, or the draft if there is no revision. Then, for each closed issue
with a `Revise: target product profile` line:

1. **Show the change**: the row, what it says now, what the resolution asks, the issue's ID, and
   who decided and when.
2. **Check it before applying it.** Where the row now says something other than what the line
   says it said, someone changed it since; show both and ask. Where the change contradicts another
   row — a raised performance minimum against a cost of goods that cannot carry it, a new user group
   the use section does not name — say so and ask. Do not resolve it.
3. **Apply it on a yes**, one change at a time. A change the user declines is not applied: say it
   needs the issue reopened, and list it for step 11.

Then build the next draft with every change applied — `target-product-profile_revB_draft.docx`
beside `target-product-profile_revA.docx` — and fill its *Changes in this revision* appendix: each
row changed, from what to what, and the issue ID. Write it through step 9, without the interview.
Where only an unreviewed draft exists, read it with `mosdocx.py read` first: if it carries tracked
changes or comments, the team is reviewing it; ask them to finish and make its clean copy before
revising, rather than overwrite their review. Otherwise apply the changes to that draft, and
re-render it with `--force` on a yes.

Confirm the company root — the folder `context/` and `mos/` sit inside. Everything in
the map is relative to it where possible.

Ask for the company's name as it should appear on its documents. Do not take it from the folder
name, and do not confuse it with the device name.

**Then ask for the website.** *Does the company have a website, or a page about this device?* It
is the fastest place to start: most of what the interview asks, the company has already written
there for someone else.

If there is one, say what reading it involves before you read it: your AI tool fetches the pages
through its own web access, so the page addresses go to the site and to whatever service that
tool uses to fetch. Nothing from the company's files is sent. Read it only on a yes.

Read the home page and the pages that describe the company, the device, the team and recent news.
A handful of pages, not the whole site; list the ones you read. Take from them:

- **The company's name** as the site writes it. Still confirm it as the name for documents: a
  site often uses a brand or a shortened name.
- **The device** — what the site says it is, what it does, who it is for and where it is used.
  These become proposed answers in step 8, not answers.
- **The claims the site already makes.** What a company says publicly about its device is a
  claim it has already made. Record each in the site's words, with its page. If the device is not
  yet cleared or approved by FDA, and the site says it is safe, effective, or works for a
  condition, say so in plain words: FDA restricts promoting a device it has not cleared as safe or
  effective for a use. `setup` does not rule on this; it raises it, and a regulatory reviewer
  decides.
- **The team** — names and roles, for step 8's team question.
- **Stage signals** — a funding round, a study, a partnership, a launch date — for the stage and
  timeline questions.
- **The logo.** If the site has the logo as a PNG or JPEG file, offer to save it for the document
  template in step 7, and save it to `context/templates/logo.png` (or `.jpg`) only on a yes. An
  SVG or an image built into the page cannot be used by the template; ask for a PNG or JPEG file
  instead.

Show the user a short summary of what the site says, page by page, before going on, and say that
step 8 will ask them to confirm each part rather than take it as given.

If there is no website, or your AI tool cannot read web pages, carry on without it. The user can
paste the text of a page instead.

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

Every domain also keeps its local folder, `./context/<domain>/`, because MOS writes its drafts
there and nowhere else. A domain with nothing else to map has only that line. Do not force a
match.

### 4. Flag what should stay out

Before writing anything, ask directly about the four categories the context standard treats as
restricted regardless of mapping:

- Patient health information or subject-level clinical data
- Anything under a BAA or a third-party NDA
- Unfiled patent material — mention this one explicitly, because it is the category founders
  most often have not thought about
- Crown-jewel process or formulation detail

Anything named here goes in the map as a `restricted:` line, with a short reason. Where a
restricted area has a de-identified summary or a pointer document, map that instead so skills know
the material exists.

Also scan the folder names you listed for anything that looks like it belongs in these categories —
`subjects`, `PHI`, `provisional`, `patent`, `IRB` — and raise it. Advisory only. The user decides.

### 5. Write the context map

Fill `templates/context-map.md` with what steps 2–4 produced. Show the user the complete file.
Confirm. Write it to `context/context-map.md`.

Tell them plainly what the file means: anything listed is readable by MOS skills, anything not
listed is invisible to them, and they can edit it by hand at any time.

### 6. Scaffold what is missing

Create `context/`, `context/inbox/`, `context/templates/`, and a folder for each of the eight
domains under `context/`. MOS writes its drafts there, and never into a location the map points at
outside the company folder: where a domain maps to the company's own filing, the local folder holds
MOS's drafts and the map lists both. List what you created.

Do not create subfolders inside the domains, with one exception: create
`context/regulatory/standards/`, for standards the company has bought. Tell the user what it is
for: *If you hold licensed copies of standards — ISO 14971 for risk, say — put them here, one file
each, with the number and edition in the name. MOS ships no standards text; skills that find one
here ask before reading it, because whether your licence allows sending it to an AI is your call.*
It needs no line of its own in the map, because `./context/regulatory/` already covers it.

Do not create placeholder files.

### 7. Set up Word documents

Every MOS skill delivers its work as a Word document, built from one company template by the script
`mos/lib/mosdocx.py`, and reads the Word documents the company has reviewed. This step makes sure
that works, and builds the template.

**Check first.** Run `python mos/lib/mosdocx.py check`. If `python` is not found, try `python3`,
then `py -3`. Whichever works is the command every later skill uses; say which.

**If none works**, explain what it is for in one sentence — MOS writes and reads Word documents
through a short script, and the script needs Python — and ask whether to install it:

- Windows: `winget install --id Python.Python.3.12 -e`
- macOS: `brew install python`, or the installer from python.org
- Linux: the distribution's package manager

Run it only on a yes, then run the check again. Nothing else is installed: the script uses Python's
standard library and no packages.

**If the user declines**, or you cannot run commands in this environment, say plainly what follows:
skills will write their drafts as Markdown files instead of Word documents, and cannot read `.docx`
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
  the template can be rebuilt later from files the company controls. If step 1 saved the logo
  from the website, show it and ask whether to use it; a website logo is sometimes a reversed or
  cropped version that does not suit a white page. No logo is fine; the company name takes its
  place.
- Font and body size — default Calibri, 10.5 pt.
- Page size — Letter or A4. Default Letter, and A4 for a company outside North America.
- Date format — M/D/YYYY, YYYY-MM-DD or DD-Mon-YYYY. Default M/D/YYYY.
- The first revision — `A` or `01`. Default is to leave it as a placeholder.
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

**Then the document register.** Every document MOS writes gets a number and a line in
`context/document-register.md`: its title, current file, revision and status. The script keeps it
up to date, so nobody has to remember to. Ask one question: *does the company use a quality
system that assigns document numbers itself, such as Greenlight or MasterControl?*

- **No** — `Numbering: MOS`. A new document gets the next number for its domain: `TPP-001` for the
  target product profile, `DIR-001` for the design inputs. Show the prefixes in the template and
  say the company may change them.
- **Yes** — `Numbering: Quality system`. MOS assigns no numbers; the team enters the number their
  system gives each document in the register, and MOS puts it on every later revision.

Fill `templates/document-register.md`, show it, confirm, and write it to
`context/document-register.md`. Where `context/` already holds MOS documents — a company set up
before the register, or a re-run — run `python mos/lib/mosdocx.py register`, show the list, and on
a yes run it again with `--apply`. It numbers each document and puts the number on each draft's
cover. A record is never changed: its number goes on at its next revision. Never renumber a
document that already has a number.

### 8. Interview about the device

**First, read whatever the map points at in `product/`.** If the company already has an intended
use statement, a device description or a pitch deck in a mapped location, read it and ask about
what is missing rather than about everything. Say which answers you drew from existing documents,
and where they came from.

**Start from the website, if step 1 read it.** Where the site answers a question, put that answer
to the user rather than asking from blank: *your site says the device is for adults with chronic
low back pain, used at home — is that right for the device you are building now?* Ask especially
whether the site describes today's device or a later one. Where the site and the company's
documents disagree, say so and ask which holds.

**Say once what the answers become.** One or two sentences, before the first batch: the answers
fill a target product profile — a Word document the team can redline, recording what the product
must be, which investors and grant reviewers often ask for — and a short device profile of where
the project stands. Do not pitch it further. If the user asks what a target product profile is,
why it is worth writing, or whether it is only for drugs, read `reference/target-product-profile.md`
and answer the question they asked in a few sentences. The document is part of setup either way;
a user short on time answers what they can, and every row they skip is written `Not set yet`.

Ask in batches, grouped by topic. Eleven areas, and the user is allowed to not know. Areas 1–4, 7
and 11 fill the target product profile; areas 5, 6, 8's last three questions, 9's constraint and
10 fill the device profile:

1. **The device.** What it is physically or technically. What it does. Hardware, software,
   consumable, or a combination. Sterile, implanted, energy-delivering, patient-contacting.
2. **Users and setting.** Who operates it, who it is used on, and where — hospital, clinic, home,
   ambulance, laboratory. Whether a lay user ever touches it.
3. **What it is for.** Ask in plain words and name the regulatory term beside them. Founders
   often have the answer without knowing the term, and regulatory people need the term to find it.
   - *What does the device do, in one sentence?* FDA calls this the **intended use**: the general
     purpose of the device.
   - *Which medical condition does it diagnose, treat, prevent or monitor, in which patients, and
     where on or in the body?* FDA calls this the **indications for use**. Ask for each part
     separately: the condition, the patients (age, sex, severity, setting), and the part of the
     body. If a written statement exists, ask for it word for word.
   - *Or is it a general tool used across many conditions, like a scalpel?* Then it has no
     specific indication, and its intended use and indications are the same. Record that instead
     of pressing for a condition that does not exist.
   - *Is there anyone, or any situation, where it should not be used?* FDA calls these
     **contraindications**: situations where the risk clearly outweighs any benefit. Record them
     on their own line, not inside the indications. The labeling lists contraindications in
     their own section, separate from the indications.

   Say why this matters: the indications are central to which regulatory path a device takes.
   A new condition, patient group or body site can turn a planned 510(k) into a
   De Novo or a PMA. A company that has not written them yet is normal at concept stage. Write
   `Not written yet` and move on.

   Then ask about the clinical problem, and what people do today instead.
4. **Commercial intent.** A light pass: what the company needs the device to say in order to
   sell. Working out how the device wins against competitors is a separate job; here, capture
   what the founder already believes. Plain question first, the term beside it.
   - *Who pays for it, and who decides to buy it?* Often not the person who uses it: a
     hospital's purchasing committee, a practice owner, the patient, an insurer.
   - *Why would they choose it over what they use today?* The **value proposition**, in a
     sentence or two.
   - *What do you need to be able to say about it, in your marketing, for it to sell?* These are
     **claims**. Ask which are must-haves, without which the device does not sell, and which are
     nice to have. Record them in the founder's words; do not rewrite them into regulatory
     language.
   - *Who else sells something that does this job?* Names are enough.

   Claims the website already makes, from step 1, go in the claims table marked as already
   published, with the page each came from: they are claims made in public, not plans.

   Say why this is asked now: a claim the company needs can require different indications, a
   harder regulatory pathway or clinical evidence, and the regulatory skills need to know about
   it before they draft anything. "Not sure yet" is a normal answer at concept stage.
5. **Stage.** Where the project actually is, mapped to a phase on the lifecycle map: concept,
   definition, design, verification and validation, submission, launch, or post-market. Ask what
   they are working on this month — it is a better question than asking them to pick a phase.
6. **What already exists.** Which documents they have, even in draft: intended use, user needs,
   risk file, design inputs, test reports, a submission. This tells later skills what to build on.
7. **Regulatory position.** Plain question first, the term beside it. Most founders do not know
   these answers yet, and `Not known yet` is the right answer when that is true.
   - *Where do you plan to sell it first?* The **target geography**: US, EU, or elsewhere.
   - *How risky do you expect FDA to consider it?* FDA sorts devices into **Class I, II or III**,
     from lowest risk to highest.
   - *How do you plan to get it to market?* The **regulatory pathway**, if one is chosen: a
     **510(k)**, showing the device is as safe and effective as one already on the market; a
     **De Novo**, for a new low- or moderate-risk device with nothing like it on the market; a
     **PMA** (premarket approval), for high-risk devices, usually with clinical data; or a
     **CE mark** for Europe.
   - *Is there a device already on the market that does the same job, that you would compare
     yours to?* For a 510(k), FDA calls this the **predicate device**.
   - *Do you expect to need a clinical study before you submit?*
   - *Have you talked to FDA yet?* Formal contact is usually a **Pre-Submission**, a written
     request for FDA's feedback before filing. Note any meeting and its date. This one goes in
     the device profile: it is history, not a target.
8. **Risk profile.** Plain question first, the term beside it.
   - *Does it go into the body, and how far: on the skin, into a natural opening, or through
     surgery?* This is **invasiveness**.
   - *Does it contain software, and could a software failure seriously injure someone?* FDA sets
     a **documentation level** for device software, **Basic** or **Enhanced**, largely on that
     question. It replaced the older "level of concern" in 2023; if the user uses the old term,
     record their answer and note the change.
   - *Is it sold sterile, or sterilized before use?* **Sterility**.
   - *What touches the patient — skin, tissue, blood — and for how long?* This decides
     **biocompatibility** testing.
   - *Does it run on electricity, or give off radiation, heat, light or sound?* **Electrical and
     radiation safety**.
   - *Is any part of it new enough that no existing test standard covers it?*
   - *Which standards have you already identified, and which hazards worry you most?*

   The first, third, fourth and fifth answers describe the device and go in the target product
   profile's first section. The software documentation level, the novel aspects, the standards
   and the hazards go in the device profile's risk notes.
9. **Timeline and constraint.** The date that matters and what it is driven by — funding, a study,
   a partner, a competitor. What is most likely to slip. The dates themselves go in area 11.
10. **Team.** Who does what, what is outsourced, and which disciplines nobody covers. This tells
   later skills how much to explain.
11. **Targets.** The numbers the product must hit, each at two levels. Ask in plain words: *what is
    the least you would accept — below it, you would rethink the project — and what are you aiming
    for?* Write each value with its direction: `≥ 95%`, `≤ $400`, `no later than Q3 2028`.
    - *Which two to five numbers decide whether this device works?* Accuracy, battery life,
      procedure time, force, flow — whatever matters for this device. Do not supply a list of
      generic attributes; ask for the ones that matter here, and suggest one or two only if the
      user is stuck.
    - *What must it do for patients, and how would you measure it?* The main clinical benefit.
    - *What is the serious harm it must avoid, and how often is too often?*
    - *How long must it last — in use, or on the shelf?*
    - *How big can it be, how long can it take to set up or use, and how much training can its
      user be given?*
    - *What will you sell it for, and what can it cost to make?* The selling price and the
      **cost of goods**.
    - *How does it get paid for — an existing billing code, a new one, or out of pocket?*
      **Reimbursement**. `Not known yet` is normal; the `reimbursement` skill works it out.
    - *When must it be in people for the first time, submitted, cleared and on the market?* The
      latest acceptable date and the target for each.

    Many of these are `Not set yet` at concept stage, and that is the point: written down, they
    show the team what it has not agreed. Never fill a number the user did not give. Where the user
    gives one value, ask whether it is the minimum or the target; do not copy it into both.

Do not ask all of these if the answers are already in front of you, and do not ask a question a
company at concept stage cannot possibly answer. Skip ahead when the user says they do not know
yet, and write `Not known yet` or `Not set yet`.

### 9. Write the target product profile and the device profile

**Say where the answers came from.** In the target product profile, the working notes list each
source once — the interview, each document by path, each web page with the date read — and the
rows it supplied; anything not listed came from the interview. In the device profile, each section
notes its source. A later reader needs to know which statements have a source and which are
someone's recollection on a Tuesday, and which came from marketing copy.

**The target product profile.** Fill `templates/target-product-profile.md`:

- Write the product summary from the answers, in three to five sentences, and show it for
  correction. It is the paragraph most people will read.
- Write `Not set yet` where nobody has decided. Never leave a cell blank.
- On a first draft, the *Changes in this revision* appendix says `First draft`. On a revision, it
  lists each row changed, from what to what, and the issue ID or the conversation behind it.
- Add a row to section 4 for each number from area 11's first question. Remove the example row.
- Keep, for step 11, the `Not set yet` rows that something is waiting on and every contradiction
  the interview raised and did not resolve. They go on the issues list, not in this document.
- Write dates in the Date format from `context/templates/document-settings.md`.

Show the complete content. Confirm. Save it to `context/product/target-product-profile.source.md`
and run:

```
python mos/lib/mosdocx.py render --in context/product/target-product-profile.source.md --out context/product/target-product-profile_draft.docx --title "Target Product Profile — <device>" --remove-input
```

Where a reviewed `target-product-profile_rev*.docx` is already there, name the draft for the revision
after it instead — `target-product-profile_revB_draft.docx` beside `target-product-profile_revA.docx` — in the command and
everything below.

`--remove-input` deletes the Markdown once the Word document exists: the Word document is the
deliverable. If `python` is not found, use the command step 7 found. If the draft already exists,
the script refuses to overwrite it; show what changed and ask, and add `--force` only on a yes. If
Word output is not available, write the filled template to
`context/product/target-product-profile_draft.md` instead, and say so.

**The device profile.** Fill `templates/device-profile.md`, with the target product profile's path
and status at the top. Show it in full. Confirm. Write it to `context/product/device-profile.md`.

Do not repeat in the device profile anything the target product profile holds. Each fact has one
home, so a later change to one document cannot leave the other wrong.

### 10. Report and hand off

Tell the user:

- What was created, by path
- Which domains are mapped, which are scaffolded and empty, and which are `not mapped yet`
- What is marked restricted
- Whether Word output works, with which Python command, and whose template is in use — the one
  built from the settings, with or without a logo, or the company's own
- Anything you noticed and did not act on — several revisions of one document outside `archive/`,
  a domain that looks like it holds two kinds of work, a location they mentioned but never mapped
- How many target product profile rows are `Not set yet`, and the two or three that matter most
  to settle first

Then tell them how the target product profile becomes the record. Circulate the draft to the
team and redline it in Word: the rows not set yet are the reason to. Accept or reject every change
and delete the comments. When the review is finished, make the clean copy: the next MOS skill run
offers it, or run `python mos/lib/mosdocx.py clean context/product/target-product-profile_draft.docx
--apply`. It writes `target-product-profile_revA.docx` without the working notes and moves the
full draft into `archive/`. A later revision works the same way: a `_revB_draft` becomes `_revB`,
and `_revA` moves into `archive/`. The clean copy goes for signature, and becomes the record when it
is signed in the company's quality system. Until then, every skill reads the draft and says it is
relying on an unreviewed draft. MOS skills never edit it; when one finds something that bears on a
row, it raises it for the issues list, and the team makes the next revision.

Then say what to do next, based on their stage. Do not name a skill that has not shipped. Where the
obvious next step has no skill yet, say that plainly — it is true, and it is how the roadmap gets
built.

Point at `context/inbox/` and explain it: anything useful that turns up — a call summary, a
supplier email, meeting notes — goes in there, and gets filed later. Capture is the step that
fails.

Finally, explain how MOS is updated, because it decides where their work must live:

- **`mos/` is replaced whole, never patched.** A newer MOS comes as one download holding every
  skill. To update, delete the `mos/` folder and unzip the new one in its place. There is no
  per-skill download.
- **Nothing of theirs is in `mos/`, so nothing of theirs is lost.** The context map, the target
  product profile, the device profile, the document settings and template, and every draft live
  in `context/`, which an update never touches. That is why nothing in `mos/` should ever be edited: a change
  made there disappears at the next update. Anything the company wants to customize belongs in
  `context/`.
- **They choose when to update.** Keeping the download they are using lets them stay on a version
  they have reviewed, which matters if MOS output feeds their quality system. Updating is a
  decision, not something that happens to them.
- **When updating, also remove the entries in `.claude/skills/` that came with MOS** — one folder
  per skill, named after the skill — before unzipping. Unzipping adds files but never deletes them,
  so a skill that a later release retires would otherwise stay listed. Their own skills in the
  same folder are not touched.

### 11. Hand off the issues

Explain the issues list in a sentence: one Word document in `context/` that holds everything the
team has not settled, across every domain, kept by the `issues-list` skill. No MOS document keeps
its own open questions, the target product profile included.

List what this session found and did not settle: the `Not set yet` rows that something is waiting
on — a milestone, another row, a skill — and every contradiction the interview raised that the
user did not resolve. On a revision from the issues list, add each change the user declined or a
check left unresolved, with the issue it came from: that issue needs reopening. Leave off unset rows nothing waits on; say how many, so the user knows they
were not forgotten. For each, give its type (question, conflict, gap, assumption, risk to the
plan), its domain, what it blocks and the next step. If a list exists already — a re-run of setup
— leave out what is on it, unless this session found something new about it.

Show the list. On a yes, write it to `context/inbox/<YYMMDD>_issues_setup.md`, in the format the
context standard gives. Then ask the user to run `issues-list` now, while this session still holds
what was found: it starts the list from this note. Never write the issues list itself.

## Working at three levels of context

| What the company has | How this skill behaves |
|---|---|
| Nothing | Skips steps 2–4, scaffolds the layout, sets up Word output, and runs the full interview, starting from the website if there is one. Produces a map pointing only at the new `context/` folders, and a target product profile and device profile built from the conversation and the site, with most targets `Not set yet` |
| Some files | Maps what exists, and the interview starts from what those documents already say. Asks about gaps, not about everything |
| A full document set | Most of the work is mapping. The interview becomes a confirmation pass, and step 10 is where the value is — naming what is missing, stale or duplicated across a set the company thought was complete |

## Where this skill is weakest

Recorded so it gets fixed rather than rediscovered:

- Mapping a large shared drive by folder name alone is guesswork. The proposal is only as good as
  the company's naming, and some companies name folders after people.
- The interview cannot tell a confident wrong answer from a correct one. A founder who believes
  they are Class II when they are Class III will produce a target product profile that says
  Class II, and every downstream skill inherits it until `product-code` challenges it.
- A minimum and a target given by one founder in an interview are that founder's numbers. A
  table of numbers looks more settled than it is until the team has redlined it.
- A company's own Word template works only if its fields survive editing. Word sometimes splits
  typed text like `{{revision}}` into pieces internally, and a split field is not found.
  `mosdocx.py inspect` reports the fields it cannot find, and the user re-types them.
- A website describes the device the company wants to be seen building, which is not always the
  one on the bench. The interview asks, but a founder confirming their own marketing copy is the
  easiest yes in the session.
- There is no check yet that a mapped path still exists. A map written today survives a
  reorganization six months from now only until someone runs a skill and it fails.
