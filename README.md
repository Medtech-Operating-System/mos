# Medtech Operating System

An open system of templates, skills and education covering the medtech lifecycle — technical, clinical, regulatory and commercial. It exists because nobody goes to school for medtech and the knowledge is tribal.

This repository is generated from the working root and is the public half of MOS. The website is at <https://medtechoperatingsystem.com>, and the download is the same content as a ZIP.

## How it works

A MOS skill is a folder of plain Markdown that an AI reads and follows. Nothing runs on its own, and nothing installs without your approval. Your company's own files stay where they are, in a folder structure `context-standard.md` defines, and skills read only the paths they declare.

MOS has no account, no server and no copy of anything. When you use a cloud AI, file contents are sent to that provider for processing — the provider your company already contracted with. MOS adds no new party to the data flow.

## Skills

| Skill | What it does | Status |
|---|---|---|
| `design-inputs` | Draft the design inputs for a medical device — the verifiable requirements its design must meet — from its user needs, hazards, target product profile, precedent and standards, each traced to its source. Use when a team needs design inputs drafted, converted from a requirements document or spec, or reviewed. | draft |
| `differentiation` | Work out how a medical device will win against the alternatives a buyer has — competitors, current practice, doing nothing — and which claims that difference rests on. Use when a team needs to define its competitive position, sharpen its value proposition for each stakeholder, or settle the claims its marketing will need before the regulatory work begins. | draft |
| `hazards-id` | List the early hazards of a medical device — what could hurt someone, how, and what harm would follow — from FDA's records for similar devices, their labeling, a hazard checklist and any standards the company holds, so they shape user needs and design inputs. Use when a team needs a preliminary hazard list at concept or definition stage, before a hazard analysis. | draft |
| `indications-strategy` | Draft three or four versions of a medical device's indications for use statement — from one as close to the predicate as possible, with the fewest clinical studies, to one that carries the claims that set the device apart — and compare what each costs in pathway, clinical evidence, time and money. Use when a team needs to decide what to ask FDA to clear, weigh a 510(k) against a De Novo or PMA, or see what a more compelling indication would cost in clinical studies. | draft |
| `issues-list` | Keep a company's issues list — every open question, gap, conflict, assumption and risk to the plan that comes up while developing a medical device — and work through it as new context arrives. Use when a team wants to start an issues list, log the issues another MOS skill found, take in the edits the team made to the list, or check which open issues new documents or decisions now settle. | draft |
| `precedent-search` | Find the marketed devices whose FDA record informs a device's submission, including candidate predicates for a 510(k), the nearest devices and special controls for a De Novo, and earlier approvals and their clinical evidence for a PMA. Use when a team needs to find or test a predicate, show that none exists, or learn what evidence FDA accepted for devices like theirs. | draft |
| `predicate-profile` | Profile the marketed devices a team has chosen to study — its predicate, reference devices or a close competitor — from FDA's records, their labeling and what their makers publish, and sort what each shows into candidate inputs for the target product profile, user needs, hazards and design inputs. Use when a team has picked a predicate or reference device and needs to know it in depth, or wants to profile a different device in its place. | draft |
| `product-code` | Find the FDA product codes that may fit a medical device, and report what each one implies for its class and path to market, from FDA's public classification database. Use when a team needs to classify a device, check a classification it has assumed, or learn which regulatory pathway a product code points to. | draft |
| `reimbursement` | Work out how a medical device would be paid for in the US — whether billing codes exist for it, whether Medicare covers it, who gets paid under which system in each setting where it is used, how much Medicare pays, and how much of that payment is left for the device — and what it would take to close each gap. Use when a team needs to know whether its device can be paid for, what Medicare pays for the codes involved, find the codes and coverage policies that apply, or understand what payers will want before choosing its indications. | draft |
| `setup` | Read a company's website, map its existing files and interview them about their device, producing a context map, a target product profile and a device profile. Use this the first time someone runs MOS, when their context map needs rebuilding, or to draft the next revision of the target product profile from decisions on the issues list. | draft |
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
