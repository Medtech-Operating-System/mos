---
name: precedent-search
description: Find the marketed devices whose FDA record informs a device's submission, including candidate predicates for a 510(k), the nearest devices and special controls for a De Novo, and earlier approvals and their clinical evidence for a PMA. Use when a team needs to find or test a predicate, show that none exists, or learn what evidence FDA accepted for devices like theirs.
version: 0.1.0
maintainer: Eric Sugalski
phase: [00-concept, 01-definition, 04-submission]
discipline: [regulatory]
reads:
  - context/context-map.md
  - context/product/**
  - context/regulatory/**
  - context/commercial/**
  - context/templates/**
writes:
  - outputs/regulatory/
  - context/regulatory/precedent.md    # only on the user's approval, after a person has chosen
  - context/product/device-profile.md   # only on the user's approval, to record a predicate
status: draft
---

# Precedent search

Finds the devices already on the market whose FDA record matters to this one, and says what each
means for the submission. For a 510(k), that is candidate **predicates**: the devices a new device
is compared with to show it is as safe and effective. For a De Novo, it is the nearest devices and
why none of them is a predicate, and the special controls FDA set for similar devices. For a PMA,
it is earlier approvals and the clinical evidence FDA accepted. The output is a Word document in
`outputs/regulatory/`, built from the company's template: a draft for review, not a controlled
record.

Read `mos/context-standard.md` before starting if you have not already, then read
`context/context-map.md` to find out what you are allowed to read.

## The thing this skill is actually for

**The predicate is the foundation of a 510(k).** Every comparison, every test and every argument in
the submission is built against it. A predicate chosen because a competitor used it, or because it
was the first result, is the most common reason a 510(k) ends in a finding that the device is not
substantially equivalent, and a year is lost.

**Intended use is a gate, not a score.** A candidate whose intended use does not cover the new
device's indications cannot be the predicate, however similar its technology. The skill tests that
first and ranks only what passes.

**The skill ranks; a person chooses.** Choosing the predicate is the regulatory decision a qualified
person owns. Every candidate is labeled a candidate. None is labeled the recommendation.

## Rules for this skill

- **Never send company text outside.** Queries carry product codes, regulation numbers, K numbers
  and generic device words — never the company's product name, indications, description or any
  file's contents.
- **Show every query before it runs.** Every command that reaches FDA or the eCFR. Batch them so the
  user approves a step at a time, and log every one.
- **Test what the user brings before relying on it.** A predicate the team has chosen, a product
  code, a planned pathway: search and judge independently, then compare. Where the evidence
  disagrees, say so plainly, show it, and ask the user to reconsider. Once they have heard the
  challenge and confirmed, accept it, and record that it was confirmed over the challenge.
- **Search the same classification regulation first.** FDA's 2014 guidance on substantial
  equivalence says a new device with an added feature must have at least one predicate from the
  same regulation, and in practice the primary predicate almost always shares it. A device outside
  the regulation can still matter, as a reference device. Proposing one as the predicate needs a
  strong reason, stated.
- **Flag a split predicate; never propose one.** Using one device for intended use and another for
  technology is, in FDA's words, inconsistent with the 510(k) standard. Where the evidence only
  supports that, say so: it usually means a De Novo.
- **Do not invent.** Every indication, date, recall and test named comes from a record or a summary
  in the search log. Where a summary could not be read, say so; do not fill it from memory.
- **Cite FDA's 2023 predicate guidance as a draft.** *Best Practices for Selecting a Predicate
  Device* was issued as draft guidance in September 2023. Tell the user to check whether it has been
  finalized before relying on its wording.
- **Do not write into `context/`** without approval of that specific write.
- **Plain words first, the term beside them.**

## Steps

### 1. Establish what context exists

Check for `context/context-map.md`.

- **It exists** — read it. Read, weighing each by the order of trust in the context standard:
  - **The product code.** `context/regulatory/classification.md`, if a person has chosen one. If
    not, a product code analysis in `context/regulatory/` or, unreviewed, in `outputs/regulatory/`.
    From a draft, say which code it leaned toward and ask the user to confirm it before searching.
  - **The device.** `context/product/device-profile.md`: intended use, indications for use,
    contraindications, how it works, patient contact, users and setting.
  - **The claims.** The differentiation analysis in `context/commercial/` or, unreviewed,
    `outputs/commercial/`. Its must-have claims are checked against each candidate in step 8.
  - **Earlier work.** `context/regulatory/precedent.md`, if a predicate has been chosen before; an
    earlier precedent search, reviewed or draft; and any predicate the company has named — in the
    device profile, a regulatory strategy, or the conversation.

  Read Word documents with `python mos/lib/mosdocx.py read <file>`. Tell the user what you found and
  which of it is unreviewed. List contradictions; do not resolve them.
- **It does not exist** — say so, and say that running `setup` and `product-code` first will make
  this skill better. Then offer to continue from the conversation: you need a product code and the
  indications for use.

**Without a product code, stop and say so.** Offer the `product-code` skill, or take a code the user
gives and test it with `openfda.py code` before relying on it.

Anything you need outside the declared paths, ask for by name and say why.

### 2. Confirm the pathway and the mode

Run `code` on the product code, and tell the user, in plain words, which path its record points to:

```
python mos/lib/openfda.py code ABC
```

| The code's submission type | The search this skill runs |
|---|---|
| **510(k)** | Candidate predicates: step 4 onward |
| **510(k) exempt** | Read the exemption limits first (`regulation --limits`). If the device plainly stays within them, say that no premarket submission is likely needed, name the limits that could apply, and stop. If it may fall outside them, run the 510(k) search |
| **PMA** | Earlier approvals and their evidence: step 13 |
| **Contact FDA, HDE, enforcement discretion, unclassified** | Say what the record means, recommend a Pre-Submission, and run the 510(k) search only if the user asks |

**If the company expects a De Novo**, or the 510(k) search finds no candidate that passes the
intended-use gate, run step 12.

Then confirm the mode:

- **Discover** — no predicate in mind. Find and rank candidates.
- **Vet** — the team has named one. Run the full Discover search anyway, then test the named device
  against the same criteria and set it beside what the search found. If a stronger candidate exists,
  or the named one fails a criterion, say so and ask.

If `python` is not found, use the command `setup` found — `python3` or `py -3`. If FDA cannot be
reached, write each search as a plain instruction for FDA's 510(k), De Novo and PMA databases and
ask the user to run them; everything after this step still applies.

### 3. Tell the user what will leave the machine

In one short paragraph: product codes, regulation numbers, K numbers and generic device words go to
FDA's public database; document numbers go to FDA's website to download summaries; regulation
numbers go to the eCFR; product codes and standard numbers go to FDA's website to look up
recognized standards; and guidance pages are read from FDA's website. Nothing else.

### 4. Build the candidate pool

The primary predicate almost always sits in the same classification regulation, so start with
every code under it:

```
python mos/lib/openfda.py family 886.4150
python mos/lib/openfda.py clearances --regulation 886.4150 --limit 300
```

`family` lists the codes and how many devices each holds. `clearances --regulation` lists every
510(k) clearance and De Novo grant under all of them, with whether a summary is online. It costs one
or two queries and no downloads.

Then search device names across all codes, to catch devices like this one that sit elsewhere:

```
python mos/lib/openfda.py devices vitreous biopsy --any
```

Devices outside the regulation are unlikely predicates. Keep a note of the close ones: they may be
reference devices later.

**Screen the list by name, date and summary availability** into a longlist of about fifteen to
twenty-five. Prefer devices that sound like this one over the newest; keep the most recent few
regardless, because recent clearances show what FDA accepts now. A clearance with only a 510(k)
*statement*, not a summary, cannot be compared on indications; keep it only if nothing better
exists, and say why. Record every device screened out, with the reason, for Appendix A.

### 5. Read, and apply the intended-use gate

From the longlist, choose **five to ten** to read in full: the closest by name and function, and the
most recent. Download their summaries, ten at most per call:

```
python mos/lib/openfda.py fetch K212763 K220030 K170183 --out outputs/regulatory/summaries
```

**If you cannot read PDF files**, say so plainly. List the summaries the user should read, and tell
them this step works best with an AI that can read PDFs — Claude, for example — and that switching
for this step is worth considering. Do not guess at a summary's contents.

For each summary, record its **indications for use word for word**, and its technology, energy
source, materials and patient contact, sterility, software, and the performance testing it cites.

Then apply the gate: **do the new device's indications fall within this device's intended use?**
If the indications name more than one condition, patient group, body site or function, apply the
gate to each part separately. A candidate may cover some parts and not others, and that is what
makes a multiple-predicate scenario possible in step 9.
Use the 1998 FDA guidance on general and specific intended use:

- **How far does the difference move up the ladder of specificity?** Function, then tissue type,
  then organ or organ system, then a specific disease or population, then an effect on clinical
  outcome. The further up, the likelier a new intended use.
- **The decision criteria:** does the new use bring new risks; affect public health more; lack an
  accepted body of knowledge that it is a subset of the general use; need different endpoints; turn
  a tool into a treatment; need another product alongside it; or need design changes that fit it
  less well for the general use?

Record each as **Passes**, **Fails** or **Unclear**, with the reason. Candidates that fail stay in
the analysis, with why: they show where the boundary is.

### 6. Check each candidate against FDA's predicate best practices

For every candidate that passes or is unclear, check the four practices in FDA's 2023 draft
guidance:

1. **Cleared using well-established methods** — does the summary cite recognized standards and
   test methods, or novel ones?
2. **Meets or exceeds expected safety and performance** — anything in the summary or the record
   suggesting it underperforms devices of its type?
3. **No unmitigated use-related or design-related safety issues:**
   ```
   python mos/lib/openfda.py events --brand "UniVit" --manufacturer "Visioncare"
   ```
   Report counts as a signal, with the caution the script prints. Brand matching is loose.
4. **No design-related recall:**
   ```
   python mos/lib/openfda.py recalls --number K212763
   ```
   Recalls are linked by K number and are reliable. Read the root cause: a labeling or
   manufacturing recall is not the same as a design recall, and the draft guidance is about design.

### 7. Follow each candidate's own predicate, one level back

Each summary names the predicate it was cleared against. Record it, and check that device's recall
history. Note where the chain drifts: a candidate cleared against a predicate with a different
intended use or a different technology is weaker than its own summary suggests. Download that
predicate's summary only when the drift matters to the ranking.

**The reading budget:** up to ten summaries in the first round; with the user's agreement, up to
ten more for predicates of predicates or close calls. Twenty is the ceiling for one run. Record how
many were read, and why that was enough.

### 8. Rank the candidates, and check the claims

Rank in this order, and say which criterion decided each place:

1. **The intended-use gate** — Passes above Unclear. Fails are not ranked.
2. **Technological characteristics** — the same, or different in ways that do not raise different
   questions of safety and effectiveness, above differences that might.
3. **The four best practices** — a design recall or an unmitigated safety signal weighs heavily.
4. **Recency** — flag a predicate cleared more than about ten years ago; older is not disqualifying,
   and it is worth saying why it is still the best choice.
5. **A summary online** — a candidate that can be compared on indications above one that cannot.

Label them **Candidate 1, 2, 3**. Never "recommended". Where two are close, say so rather than
forcing an order.

If one candidate passes the gate for every part of the indications, say which would be primary and
why. If none does, go to step 9 before the ranking is final. If the only way to cover the device is
one device for intended use and another for technology, that is a **split predicate**: flag it, and
say it points toward a De Novo.

**Then check the claims.** Set each must-have claim from the differentiation analysis against the
indications of the top candidates. A claim outside every candidate's intended use is a claim the
510(k) will not carry as things stand. Name it, and say it is a question for `indications-strategy`,
not something this skill resolves.

### 9. When no single predicate covers the indications: a multiple-predicate scenario

FDA's 2014 guidance on substantial equivalence allows more than one predicate in three situations:
combining features from predicates that share an intended use; a device with **more than one
intended use**; or **more than one indication under the same intended use**. FDA's 2023 draft
guidance repeats this. This step uses the last two, to cover the indications the company wants. It
is not a way to explain away technological differences; those belong in the comparison table and a
reference-device search.

**Offer it** when no single candidate passes the gate for every part of the indications, but each
part passes with some candidate. Build it this way:

1. **Map each part of the indications** — each condition, patient group, body site or function —
   to the candidates that pass the gate for it.
2. **Choose the primary**: the candidate whose indications and technology are most similar
   overall. FDA recommends naming one primary predicate.
3. **Add the fewest further predicates** that cover what the primary does not. FDA asks that the
   number be kept to the minimum needed.
4. **Test it against the guidance:**
   - *More than one indication, one intended use.* Every predicate must share the device's overall
     intended use. FDA's example is a bone plate for fractures of both the shaft and the end of a
     long bone, citing one predicate for each: both are fracture fixation of the long bone.
   - *More than one intended use.* Each function has its own predicate, and the functions must not
     interfere with each other. FDA's example is a multi-parameter monitor with a predicate for each
     parameter.
   - Each specific indication may need its own performance testing.
   - A specific indication can itself change the overall intended use, and then the scenario does
     not apply. Judge that with the 1998 general and specific intended use guidance, as in step 5.
   - Technological differences from each predicate must not raise different questions of safety
     and effectiveness.
   - Apply the four best practices in step 6 to **every** predicate, not only the primary. The 2023
     draft guidance asks the submission to say how they were applied to each.
   - **It is not a split predicate.** Every predicate here passes the gate itself for the part it
     covers. A split predicate takes intended use from one device and technology from another device
     with a different intended use; that is not allowed.
5. **Search other product codes when the scenario needs them.** Separate functions, and sometimes
   separate indications, are often cleared under their own product codes, and sometimes their own
   regulations. Start from the other codes the product code analysis listed, and search device names
   for where each uncovered indication or function has been cleared:
   ```
   python mos/lib/openfda.py devices "temperature" "thermometer" --any
   python mos/lib/openfda.py family 880.2910
   python mos/lib/openfda.py clearances --code FLL --limit 200
   ```
   Put what you find through steps 5 to 7, under the same reading budget. Keep the primary in the
   device's own classification regulation: the 2014 guidance says a device with an added feature
   still needs at least one predicate from its own regulation.
6. **Set both routes side by side.** The single-predicate route, with the indications narrowed to
   what the best single candidate covers; and the multiple-predicate route, with the full
   indications, showing which predicate covers which part and what each adds in testing and
   argument. Set the must-have claims against both. Which route to take is the company's decision.

### 10. Draft the comparison table

For the top two or three candidates — and, in a multiple-predicate scenario, every predicate in it
— draft the comparison a 510(k) carries: the new device beside each, row by row.

| Row | What to compare |
|---|---|
| Indications for use | Word for word |
| Intended use | The general purpose |
| Users and setting | Who, where, prescription or over-the-counter |
| Body site and patient contact | Where, what tissue, for how long |
| Principle of operation | How it works, in plain words |
| Energy source | Mains, battery, pneumatic, manual |
| Materials | Patient-contacting materials |
| Sterility and use | Sterile or not; single-use or reusable |
| Software | None, embedded, standalone |
| Key specifications | The few that matter for this device type |
| Performance testing cited | What the candidate's summary says was tested |

For each row, say **Same** or **Different**. For each difference, say what question it raises —
biocompatibility, electrical safety, performance, usability — without concluding whether FDA would
see it as a *different* question of safety and effectiveness. That is argued in the submission.

**The Different rows are the handoff.** They are the technological differences a reference-device
search works through, one at a time, once a person has chosen the primary predicate.

### 11. Set out the requirements: special controls, guidance and standards

Three kinds of requirement shape what a submission must show. Set them out in this order, because
each one explains the next.

#### Special controls

A Class II device is subject to FDA's **general controls** — registration, listing, labeling, the
quality system, adverse event reporting — and to **special controls**: requirements FDA sets for
one device type because general controls alone cannot assure it is safe and effective. They are
binding. A 510(k) for a Class II device must show the device meets its special controls as well as
being substantially equivalent to its predicate.

Read the regulation for the product code, and for every code in a multiple-predicate scenario:

```
python mos/lib/openfda.py regulation 870.1025
```

The classification paragraph takes one of three forms. Say which:

1. **Listed in the regulation** — for example, clinical performance testing, software
   verification, human factors testing, required labeling. Record each one.
2. **A guidance document named as the special control** — the regulation says a named guidance
   document "will serve as the special control". The requirements live in that document: get it
   with `guidance`, below, and read it.
3. **None named** — the regulation says only "Class II (special controls)". Common for device types
   classified decades ago. Say so plainly: with nothing written, what FDA expects is best read from
   the predicates' testing and from the guidance FDA links to the code.

#### Guidance

`standards --code` lists the guidance documents FDA links to the product code, including a special
controls guidance where there is one. Save and read the ones that bear on the device:

```
python mos/lib/openfda.py guidance https://www.fda.gov/regulatory-information/search-fda-guidance-documents/... --out outputs/regulatory/guidance
```

It downloads the PDF where FDA offers one. Many older guidance documents are published as the web
page itself, and then it saves the page's text. List every guidance document you read, and any you
found and did not, with why. A guidance document is FDA's current thinking, not a requirement —
except one named as a special control, which the company must address, either by following it or
by another means that gives equivalent assurance.

#### Consensus standards

A submission usually rests on conformity to **consensus standards**: published test methods and
requirements that FDA recognizes. Recognition matters: FDA accepts a declaration of conformity to a
recognized standard in place of some test detail. A standard is a way to meet a requirement, not the
requirement itself. List the standards the device is likely to need, from four sources, each
checked against FDA's current recognition.

1. **Specific to the product code.** FDA lists recognized standards, and linked guidance, for each
   code. Run it for the product code and for every code in a multiple-predicate scenario:
   ```
   python mos/lib/openfda.py standards --code ABC --details
   ```
2. **Cited by the candidates.** The testing sections of the summaries read in step 5 name the
   standards each predicate was tested to. Those are strong evidence of what FDA expects.
3. **Triggered by the device's characteristics.** General standards are not listed by product code.
   From the device profile, look up the ones that apply:

   | If the device | Look up |
   |---|---|
   | Is a medical device at all | ISO 14971 (risk management), IEC 62366-1 (usability), ISO 15223-1 (labeling symbols) |
   | Touches the patient | ISO 10993-1, then the parts of the ISO 10993 series its evaluation calls for |
   | Is electrically powered | IEC 60601-1 (basic safety), IEC 60601-1-2 (electromagnetic compatibility) |
   | Is used in the home | IEC 60601-1-11 |
   | Has alarms | IEC 60601-1-8 |
   | Contains software | IEC 62304 |
   | Is sold sterile | The sterilization standard for its method — ISO 11135 (ethylene oxide), ISO 11137-1 (radiation) or ISO 17665-1 (moist heat); ISO 11607-1 and -2 (packaging); ASTM F1980 (accelerated aging, for shelf life) |
   | Is reusable | ISO 17664-1 (information for processing) |

4. **Named by a special control.** A special control, or a special controls guidance, sometimes
   names a standard or a test method.

Check each one's current recognition:

```
python mos/lib/openfda.py standards --number 10993-1 --details
```

Record the FDA recognition number, the edition, the **extent of recognition** — *Complete*, or
*Partial*, where FDA does not accept conformity to part of the standard and the recognition page
says which — and any **transition** between editions, with its deadline. A standard the lookup does
not find is not FDA-recognized: say so, and keep it only if a predicate or a special control relies
on it. `--details` reads at most ten recognition pages per call, one second apart; FDA's site
blocks requests that come too fast.

#### Map the requirements together

For each special control — and, where none are named, for each risk the predicates' testing
addressed — record: **what it requires**; **how the top candidates' summaries addressed it**;
**which recognized standards support it**; and whether anything is left **open**. A requirement
that no standard, predicate or guidance addresses is flagged: it is where the company will have to
design its own evidence, and a question for a Pre-Submission.

**Rules for this step.** Quote a regulation's special controls, which are public law; summarize a
guidance document rather than copying it at length. For standards, numbers, titles and FDA's
recognition details only: never a standard's text, which is copyrighted. This is where a test plan
starts, not the plan; which clauses apply, and whether a declaration of conformity is enough, is the
company's judgment. Special controls, guidance and recognition all change, so the section carries
the date it was checked.

### 12. When there is no predicate: the De Novo search

When no candidate passes the gate, or the only route is a split predicate, or the company expects a
De Novo:

1. **The nearest devices, and why each fails as a predicate.** From the 510(k) search: the closest
   candidates, with the specific reason — a different intended use, technology that raises different
   questions of safety and effectiveness, or no device in the regulation at all. This is the
   argument a De Novo request needs: that no predicate exists.
2. **Similar De Novo grants.** Search for them by name and code:
   ```
   python mos/lib/openfda.py devices "sampling" "biopsy" --any
   python mos/lib/openfda.py clearances --code ABC --denovo
   ```
   Read their decision summaries; they set out the risks FDA identified and how each was mitigated.
3. **Their special controls.** Each De Novo grant creates a classification regulation. Read it:
   ```
   python mos/lib/openfda.py regulation 870.2345
   ```
   The special controls in similar regulations are the best available guide to what FDA will ask of
   this device. Summarize them; do not decide which apply.

Say plainly that whether a De Novo is the right route is a question for a Pre-Submission.

### 13. When the pathway is PMA: earlier approvals and their evidence

```
python mos/lib/openfda.py pma --code ABC --limit 50
python mos/lib/openfda.py fetch P210015 --out outputs/regulatory/summaries
```

For the closest approvals, read the **summary of safety and effectiveness data** (SSED) and record
the clinical study that supported approval: design (randomized, single-arm, registry), primary
endpoints, number of patients, length of follow-up, comparator or control, and the main result as
the SSED states it. This table is what a clinical strategy discussion starts from. Report it; do not
design the study.

### 14. Write the draft

Fill `templates/precedent-search.md`, keeping only the sections that apply to the pathway. Write
dates in the Date format from `context/templates/document-settings.md`, if it exists. The search log
lists every query in order. Show the user the complete content. Confirm.

Save the filled template to `outputs/regulatory/precedent-search.source.md` and run:

```
python mos/lib/mosdocx.py render --in outputs/regulatory/precedent-search.source.md --out outputs/regulatory/precedent-search_draft.docx --title "Precedent Search — <device>" --remove-input
```

If `precedent-search_draft.docx` already exists, the script refuses to overwrite it. Show what
changed and ask; add `--force` only on a yes. If the script cannot run, write the filled template to
`outputs/regulatory/precedent-search.md` instead, and say that Word output needs the step in
`setup`.

Tell the user how the draft becomes the record: review and redline it in Word, save it with the
revision in its name — `precedent-search_revA.docx` — in `context/regulatory/`, or in the quality
system with the map pointing at it, then delete the draft from `outputs/regulatory/`. Until then,
later skills read the draft and say it is unreviewed.

### 15. Offer to record the decision

The analysis ranks; it does not choose. When a person has chosen — a primary predicate and any
secondary ones for a 510(k), or the position that no predicate exists — fill
`templates/precedent-record.md` and offer to write it to `context/regulatory/precedent.md`. It
records who chose, when, and the technological differences from the chosen predicate. Show it in
full; write only on a yes. If nobody has chosen yet, say the record waits until they have.

If the device profile names a predicate that differs from the one chosen, offer to update it.

## Working at three levels of context

| What the company has | How this skill behaves |
|---|---|
| Nothing | Asks for the product code and indications, tests the code before relying on it, and runs Discover. Explains each step in plain words — what a predicate is, why intended use is a gate. Every statement about the device is marked as from the conversation |
| Some files | Starts from the classification record or the product code draft, the device profile and any differentiation draft; says which are unreviewed; interviews only for the gaps. Runs Vet when the company has named a predicate |
| A full document set | Tests the chosen predicate against FDA's current record: new recalls, a newer and closer clearance, a finalized guidance. Flags contradictions between the precedent record, the indications and the claims rather than resolving them |

## Interviewing style

- One question at a time.
- When the team names a predicate, ask why: a competitor used it, a consultant chose it, it was the
  first search result. The reason tells you what to test.
- Do not argue the pathway until the search is done. Collect the facts first.

## Boundaries

This skill does not choose a predicate or a pathway, write the substantial equivalence argument,
design testing or a clinical study, write a test plan from the standards it lists, or search for
reference devices. It reads FDA's public records
and the eCFR; it does not know what FDA told any other company privately, and a summary is the
applicant's account of its own device.

## Where this skill is weakest

Recorded so it gets fixed rather than rediscovered:

- It reads at most twenty summaries. In a code with hundreds of clearances, the best predicate can
  sit among the ones screened out by name.
- Adverse event counts by brand are noisy: reports name devices inconsistently, and summary
  reporting bundles malfunctions.
- Older clearances often have no summary online, so their indications cannot be compared.
- Whether a technological difference raises *different* questions of safety and effectiveness is
  FDA's judgment. The skill names the question; a Pre-Submission settles it.
