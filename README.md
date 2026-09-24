# Medtech Operating System

An open system of templates, skills and education covering the medtech lifecycle — technical, clinical, regulatory and commercial. It exists because nobody goes to school for medtech and the knowledge is tribal.

This repository is generated from the working root and is the public half of MOS. The website is at <https://medtechoperatingsystem.com>, and the download is the same content as a ZIP.

## How it works

A MOS skill is a folder of plain Markdown that an AI reads and follows. Nothing runs on its own, and nothing installs without your approval. Your company's own files stay where they are, in a folder structure `context-standard.md` defines, and skills read only the paths they declare.

MOS has no account, no server and no copy of anything. When you use a cloud AI, file contents are sent to that provider for processing — the provider your company already contracted with. MOS adds no new party to the data flow.

## Skills

| Skill | What it does | Status |
|---|---|---|
| `setup` | Map a company's existing files and interview them about their device, producing a context map and a populated context folder. Use this the first time someone runs MOS, or when their context map needs rebuilding. | draft |
| `user-needs` | Draft user needs for a medical device from a company's existing context, interviewing for what is missing. Use when a team needs user needs captured, converted from notes, or reviewed for gaps. | draft |

No skill has reached `released`. A skill reaches it with three testers and not before.

## Reading order

| File | What it holds |
|---|---|
| `CHARTER.md` | Why MOS exists, who it is for, its principles, the lifecycle map and how it gets built |
| `context-standard.md` | The folder structure a company adopts for its own files |
| `skills/SKILL-FORMAT.md` | The contract every skill is written to |
| `PROVENANCE.md` | Where content may come from, and what is not accepted |

## Contributing

Read `skills/SKILL-FORMAT.md` and `PROVENANCE.md` first. A skill ships with a named maintainer, works at three levels of context, and can state where its content came from. No text from ISO, IEC or AAMI standards — clause numbers are fine, clause text is not. Nothing specific to one company, ever.

## Licence and risk

Content is CC BY 4.0, code is MIT — see `LICENSE.md`. MOS provides no warranty. Everything a skill produces is a draft, and must be reviewed and approved by qualified people at your company before it is used for any regulated purpose.
