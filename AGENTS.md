# MOS skills

Instructions for any AI with access to this folder. Each skill below is a directory under `mos/skills/` holding a `SKILL.md` — numbered steps to follow exactly — and the templates it fills.

To run one: read `mos/skills/<name>/SKILL.md` and follow it. Read `mos/context-standard.md` first; it defines the folder structure every skill reads and writes.

| Skill | What it does | Status |
|---|---|---|
| `setup` | Map a company's existing files and interview them about their device, producing a context map and a populated context folder. Use this the first time someone runs MOS, or when their context map needs rebuilding. | draft |
| `user-needs` | Draft user needs for a medical device from a company's existing context, interviewing for what is missing. Use when a team needs user needs captured, converted from notes, or reviewed for gaps. | draft |

Skills read and write only the paths their frontmatter declares. Anything outside that, and anything not listed in `context/context-map.md`, requires asking the user first — naming the file and why.

Word documents are written and read with `python mos/lib/mosdocx.py` — `read <file>` to read one. See `mos/context-standard.md`.

Drafts go to `outputs/` and are not approved records. Every output must be reviewed by qualified people at the company before it is used for any regulated purpose.
