---
name: differentiation
description: Work out how a medical device will win against the alternatives a buyer has — competitors, current practice, doing nothing — and which claims that difference rests on. Use when a team needs to define its competitive position, sharpen its value proposition for each stakeholder, or settle the claims its marketing will need before the regulatory work begins.
version: 0.1.0
maintainer: Eric Sugalski
phase: [00-concept, 01-definition]
discipline: [commercial]
reads:
  - context/context-map.md
  - context/product/**
  - context/users-and-needs/**
  - context/commercial/**
  - context/templates/**
writes:
  - outputs/commercial/
  - context/product/device-profile.md    # only on the user's approval, to update commercial intent
status: draft
---

# Differentiation

Works out where a device is better than the alternatives, for each person who has a say in
buying it, and turns that into a list of claims the company needs to be able to make. The output
is a Word document in `outputs/commercial/`, built from the company's template: a draft for
review, not a controlled record. Its Claims table is what the regulatory skills read, starting
with `product-code`: as an unreviewed draft until a person promotes it, as a record after.

Read `mos/context-standard.md` before starting if you have not already, then read
`context/context-map.md` to find out what you are allowed to read.

## The thing this skill is actually for

**A device does not compete with its competitors alone.** It competes with what the buyer does
today, with the cheapest workaround, and with doing nothing at all. Most founders compare
themselves to the one competitor they admire and miss the alternative that actually wins the
sale.

**A medtech device has several customers.** The patient, the clinician who uses it, the person or
committee that pays for it, and often an insurer. A device can win with clinicians and lose with
the hospital committee that weighs its price. The skill maps value for each one, because the gap
between them is often the real story.

**Claims are where differentiation becomes a commitment.** Every claim the company wants to make
later needs evidence, and some need a harder regulatory path. This skill settles *what the company
needs to say, and why*. What each claim costs in regulatory and clinical terms is weighed later,
once the regulatory research has been done. This skill does not cost claims; it flags the ones
that are likely to be expensive, so nobody is surprised.

## Rules for this skill

- **Be honest about where the device loses.** A comparison in which the device wins every row
  has not been examined. Name where it is the same or worse, and for whom.
- **Test what the user brings before relying on it.** "Nobody else does this" and "clinicians
  will love it" are beliefs. Check them against FDA's records and, if the user takes the web
  research step, against what competitors publish. Where the evidence disagrees, say so, show it,
  and ask the user to reconsider. Once they have heard the challenge and confirmed their
  position, accept it, and record in the draft that it was confirmed over the challenge.
- **Never send company text outside.** Searches of FDA's databases and of the web use generic
  terms: device categories, clinical functions, the names of competitors. Never the company's
  product name, its device description, its claims or any file's contents.
- **Show every query before it runs.** List the searches, say what each sends and where, and run
  them on a yes. The user may edit or drop any of them.
- **A competitor's marketing is a claim, not a fact.** Report what a competitor says as what it
  says, with the source and the date read. FDA's records are evidence of what was cleared; they
  are not evidence that it works as advertised.
- **Do not cost claims against the regulatory pathway.** Flag a claim that names a disease,
  promises an outcome, or compares the device with another, because those tend to need more
  evidence. Do not decide what it needs.
- **Do not write into `context/`** without approval of that specific write.
- **Plain words first, the term beside them.**

## Steps

### 1. Establish what context exists

Check for `context/context-map.md`.

- **It exists** — read it. Read `context/product/device-profile.md`, especially its commercial
  intent: the buyer, the value proposition, the claims the founder named and the competitors.
  Read whatever the map points at under `commercial/`, and the user needs under
  `users-and-needs/`, which say what clinicians and patients need from the device. Read Word
  documents with `python mos/lib/mosdocx.py read <file>`. Tell the user what you found.
  - Read the drafts in `outputs/product/`, `outputs/users-and-needs/` and `outputs/commercial/`
    too, and say that they are unreviewed. A reviewed document outranks a draft; where they
    disagree, say so and ask.
  - If a differentiation analysis exists already, reviewed or draft, its claims have IDs. Ask
    whether this run is to revise it or to start again. Never renumber an existing claim; the
    new draft carries the old IDs forward.
  - If documents disagree — the pitch deck names one buyer and the device profile another — list
    the contradictions. Do not pick one.
- **It does not exist** — say so, and say that running `setup` first will make this skill better.
  Then offer to continue from the conversation alone.

Anything you need outside the declared paths, ask for by name and say why. Write the answer back
to the context map so the question is not asked twice.

### 2. Name the alternatives

Ask what a buyer would do instead of buying this device. Push past the obvious competitor:

- *Which products already do this job?* The **competitors**.
- *What do clinicians do today, without any product like this?* The **current practice**, or
  standard of care.
- *What is the cheapest way to get most of the benefit?* The **workaround**.
- *What happens if they do nothing?* Doing nothing is always an alternative, and often the one
  that wins.

Record each alternative once, with who offers it where there is one.

### 3. Map who decides

Ask who is involved in the decision to buy and use the device. For each, ask what they care
about, what they use today, what would make them switch, and what would stop them.

| Stakeholder | Usually cares about |
|---|---|
| **Patient** | Outcome, comfort, risk, time, cost to them |
| **Clinician who uses it** | Results, speed, ease, fit with the way they already work, liability |
| **Buyer** — the person or committee that pays, often a hospital's value analysis committee | Total cost, budget, evidence, contracts, how many other departments it affects |
| **Payer** — the insurer, when one is involved | Whether it is covered, and whether it saves money elsewhere |
| **Others who can block it** | Nursing, IT, biomedical engineering, sterile processing, infection control |

Not every device has all of these. Record the ones that apply. Where the founder does not know
what a stakeholder cares about, write `Not known yet`, and say that is a question for customer
interviews, not for the AI to guess.

**What stops them matters as much as what attracts them.** Retraining, a capital purchase, a new
workflow, a missing reimbursement code, a contract with a competitor. Ask about each.

### 4. Look at the evidence on competitors

Two sources, in two parts. The user approves each before it runs.

**FDA's records.** Show the planned searches, then run them. Use device categories and clinical
functions, never the company's own words:

```
python mos/lib/openfda.py devices "vitreous" "biopsy" --any
python mos/lib/openfda.py udi --code ABC
```

`devices` shows who has cleared or approved devices with those words in the name, under which
codes, and when. `udi` lists the brands marketed under a code. This tells the skill who is
actually on the market, which is often not who the founder named. If `python` is not found, use
the command `setup` found — `python3` or `py -3`. If FDA cannot be reached, say so and continue.

**The web — offered as its own step.** Say what it adds: what competitors say about their
devices, their published evidence, prices where they are public, and how buyers describe them.
Say what it sends and where: search terms — competitor names and device categories, never the
company's own product or claims — to the search service the AI uses, which is a party outside
both the company and FDA. Then ask whether to go ahead. Most teams will.

On a yes, list the searches, and run them on approval. For every finding, record the source, its
URL and the date read. If this AI cannot search the web, say so, and suggest the user save the
competitor pages, brochures or papers they already have into `context/inbox/` for the skill to
read.

### 5. Say where the device wins and loses

For each attribute that matters to a stakeholder — outcome, safety, speed, ease of use, cost,
fit with workflow, training — compare the device with the strongest alternative for that
stakeholder:

- **Better, the same, or worse**, and by how much where anyone knows.
- **The evidence**: a document, an FDA record, a web source with its date, or the founder's
  belief, labeled as such.

Then write the **value proposition for each stakeholder**: one or two sentences on why that
person would choose this device. A stakeholder for whom there is no honest value proposition is
a finding, not a gap to paper over.

Test the founder's beliefs here. If the founder says no competitor offers something and FDA's
records or a competitor's own materials show one does, say so and ask.

### 6. Turn the differentiation into claims

A **claim** is something the company wants to be able to say about the device in its labeling,
marketing or sales conversations. Start from the claims the founder named in `setup`, add the
claims the differentiation in step 5 depends on, and merge duplicates. For each claim, record:

- **The claim**, in plain words. Keep the founder's wording where it came from the founder.
- **Who it is for**: the stakeholder it persuades.
- **Type**: clinical outcome, safety, performance, workflow and usability, or economic.
- **Priority**: must-have — the device does not sell without it — or nice to have. Ask; do not
  assume.
- **What evidence a buyer would expect** before believing it. This is the buyer's bar, not
  FDA's.
- **Likely to affect the indications or the evidence FDA wants**: flag `Yes` when the claim names
  a disease or condition, promises a clinical outcome, compares the device with a named
  competitor, or says it is safer or more effective. Those are the claims the regulatory skills
  must see. Do not say what they will cost.

Give each claim an ID, `CL-001` onward. **Never renumber an existing claim.** Retire an ID
instead, so a document that cites CL-004 always means the same claim.

Keep the list short. A claim nobody will act on is noise, and every must-have claim is a
commitment to find evidence for.

### 7. Write the draft

Fill `templates/differentiation.md`. Write dates in the Date format from
`context/templates/document-settings.md`, if it exists. The search log lists every query sent to
FDA and to the web, in order. Show the user the complete content. Confirm.

Save the filled template to `outputs/commercial/differentiation.source.md` and run:

```
python mos/lib/mosdocx.py render --in outputs/commercial/differentiation.source.md --out outputs/commercial/differentiation_draft.docx --title "Commercial Differentiation — <device>" --remove-input
```

If `differentiation_draft.docx` already exists, the script refuses to overwrite it. Show what
changed and ask; add `--force` only on a yes. If the script cannot run, write the filled template
to `outputs/commercial/differentiation.md` instead, and say that Word output needs the step
in `setup`.

Tell the user how the draft becomes the record: review and redline it in Word, save it with the
revision in its name — `differentiation_revA.docx` — in `context/commercial/`, or in their quality
system with the context map pointing at it, then delete the draft from `outputs/commercial/`. A
promotion moves the document; it is never in two places. Until then, `product-code` still reads
the draft's claims, and says they are unreviewed.

### 8. Offer to update the device profile

If the buyer, value proposition, claims or competitors have changed since `setup`, offer to update
the commercial intent in `context/product/device-profile.md`, each change marked as coming from
this session. Name the file, show the change, and write only on a yes.

There is no separate claims record. The claims live in the differentiation document, and every
skill that needs them reads them there.

## Working at three levels of context

| What the company has | How this skill behaves |
|---|---|
| Nothing | Runs the full interview, explaining why each stakeholder and each alternative matters, and marks every finding as from the conversation or from a search. Most stakeholder answers will be `Not known yet`, and the draft says which customer interviews would answer them |
| Some files | Starts from the commercial intent in the device profile and any pitch deck or market notes in `commercial/`, interviews for the gaps, and tests the founder's stated differentiation against FDA's records and, if chosen, the web |
| A full document set | Reconciles the existing differentiation analysis, market analysis and user needs, flags claims no longer supported by the differentiation, and flags contradictions between documents rather than resolving them |

## Interviewing style

- One question at a time.
- Ask for specifics: *which* hospital committee, *what* they paid last year, *who* said so.
- When the founder says the device is better, ask: better for whom, compared with what, and how
  would a buyer know?
- Treat "I don't know" as a finding. It usually means a customer conversation has not happened
  yet.

## Boundaries

This skill does not size the market, set a price, plan reimbursement and coding, or decide what
evidence FDA will require for a claim. It does not write marketing copy. It reads FDA's public
records and, if the user chooses, public web pages; it does not know what competitors have told
FDA or buyers privately.

## Where this skill is weakest

Recorded so it gets fixed rather than rediscovered:

- It can only be as good as the founder's knowledge of the buyer. Without customer
  conversations, the stakeholder map is a set of hypotheses, and the draft says so.
- FDA's records show what was cleared and when, not what sells. A competitor with one old
  clearance may dominate the market, and one with ten may have none.
- Web sources are marketing, and they date quickly. Every finding carries the date it was read.
- FDA's database matches words, not meaning. A competitor whose device is named differently can
  be missed.
