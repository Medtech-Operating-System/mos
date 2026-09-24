# The MOS skill format

*v0.2, 2026-09-23. The contract every MOS skill is written to. Changes to this file are
architecture decisions and go through the decision log.*

A MOS skill is a folder of plain Markdown that an AI reads and follows. It is not a program. A
person could run one by hand with the templates and enough patience; the AI is there to do the
reading and the drafting. The one thing shared across skills is `lib/mosdocx.py`, which writes and
reads Word documents; it needs Python, and `setup` asks before installing it.

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
└── examples/         <- optional; a filled-in example helps more than prose
```

`SKILL.md` is the only required file. A skill with no templates and no scripts is still a skill.

Scripts belong to the skill that uses them and run when that skill runs. Use one when the work is
mechanical and an AI would get it wrong by improvising — comparing timestamps, checking a folder
against a list, counting. Do not use one for anything requiring judgment.

The exception is `lib/mosdocx.py`, shared by every skill because every skill delivers a Word
document and they must all look the same. A skill does not carry its own copy. A second shared
script needs a decision-log entry saying why it cannot belong to one skill.

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
  - outputs/user-needs/
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
| `writes` | Where output goes. Almost always a folder under `outputs/` |
| `status` | `draft`, `testing` or `released`. Nothing reaches `released` without three testers |

### Declaring reads and writes

**Directories with patterns, never enumerated file lists.** `context/regulatory/**` is correct.
Listing four specific filenames is not, because the list goes stale the moment someone adds a fifth
file and the failure is silent. The folder structure is the index; a skill that reproduces part of
that index inside itself has built a second one that nobody maintains.

**Narrow by default.** Declare the domains the job needs and no others. A skill that reads the whole
context folder in case something is relevant fails review — that is a standard, not a preference.

**Prefer digests.** Where a domain has a digest, read it instead of the full corpus, and pull raw
files only when the job genuinely needs them. A digest is a short summary a person reviewed and
approved, which is what makes it the right thing to send to a model.

**Anything outside the declaration requires asking**, naming the file and why. The user's answer is
written back to the context map, so the same question is not asked twice.

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
without the user approving that specific write. Drafts go to `outputs/`, and a human promotes them.

## Outputs are drafts

Everything a skill produces lands in `outputs/` as a pre-decisional draft. It is outside the quality
system and is not a controlled record until a qualified person reviews, approves and imports it.
The AI is a tool; the human is the author.

A skill's `templates/` hold Markdown: the structure the AI fills. The deliverable is a Word document
built from that filled template by `lib/mosdocx.py render`, on the company's document template,
named `<document>_draft.docx`. No Markdown copy is kept beside it. Where Python is not available,
the skill writes the Markdown instead and says so. The context standard covers how a draft becomes a
record.

Every output carries the disclaimer:

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

## Appendix A: <Supporting material>

...

---

*Generated with MOS and not reviewed. ...*
```

- **The `#` title and the lines before the first `##` go on the cover page.** Keep them to
  `Label: value` lines and one italic `*Notes: ...*` paragraph.
- **Body sections are `##` headings**, in title case where the name is a document term
  (*Intended Use*), sentence case otherwise.
- **Supporting material goes in lettered appendices** — `## Appendix A: ...`, `B`, `C` — in the
  order a reviewer needs them. Each starts on a new page. Coverage checks, open gaps and
  unresolved contradictions are appendices, not body sections.
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
