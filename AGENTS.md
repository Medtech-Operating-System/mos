# MOS skills

Instructions for any AI with access to this folder. Each skill below is a directory under `mos/skills/` holding a `SKILL.md` — numbered steps to follow exactly — and the templates it fills.

To run one: read `mos/skills/<name>/SKILL.md` and follow it. Read `mos/context-standard.md` first; it defines the folder structure every skill reads and writes.

| Skill | What it does | Status |
|---|---|---|
| `differentiation` | Work out how a medical device will win against the alternatives a buyer has — competitors, current practice, doing nothing — and which claims that difference rests on. Use when a team needs to define its competitive position, sharpen its value proposition for each stakeholder, or settle the claims its marketing will need before the regulatory work begins. | draft |
| `indications-strategy` | Draft three or four versions of a medical device's indications for use statement — from one as close to the predicate as possible, with the fewest clinical studies, to one that carries the claims that set the device apart — and compare what each costs in pathway, clinical evidence, time and money. Use when a team needs to decide what to ask FDA to clear, weigh a 510(k) against a De Novo or PMA, or see what a more compelling indication would cost in clinical studies. | draft |
| `precedent-search` | Find the marketed devices whose FDA record informs a device's submission, including candidate predicates for a 510(k), the nearest devices and special controls for a De Novo, and earlier approvals and their clinical evidence for a PMA. Use when a team needs to find or test a predicate, show that none exists, or learn what evidence FDA accepted for devices like theirs. | draft |
| `product-code` | Find the FDA product codes that may fit a medical device, and report what each one implies for its class and path to market, from FDA's public classification database. Use when a team needs to classify a device, check a classification it has assumed, or learn which regulatory pathway a product code points to. | draft |
| `reimbursement` | Work out how a medical device would be paid for in the US — whether billing codes exist for it, whether Medicare covers it, and who gets paid under which system in each setting where it is used — and what it would take to close each gap. Use when a team needs to know whether its device can be paid for, find the codes and coverage policies that apply, or understand what payers will want before choosing its indications. | draft |
| `setup` | Map a company's existing files and interview them about their device, producing a context map and a populated context folder. Use this the first time someone runs MOS, or when their context map needs rebuilding. | draft |
| `user-needs` | Draft user needs for a medical device from a company's existing context, interviewing for what is missing. Use when a team needs user needs captured, converted from notes, or reviewed for gaps. | draft |

Skills read and write only the paths their frontmatter declares. Anything outside that, and anything not listed in `context/context-map.md`, requires asking the user first — naming the file and why.

Word documents are written and read with `python mos/lib/mosdocx.py` — `read <file>` to read one. See `mos/context-standard.md`.

Drafts go to `outputs/` and are not approved records. Every output must be reviewed by qualified people at the company before it is used for any regulated purpose.
