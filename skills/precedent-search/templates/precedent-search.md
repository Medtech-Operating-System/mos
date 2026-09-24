# Precedent Search — {{device}}

Company: {{company}}
Written: {{date}} · Source: MOS precedent-search skill · Mode: {{Discover / Vet}}
FDA data as of: {{openFDA dates, one per dataset searched}}

*Notes: A draft. It ranks the marketed devices whose FDA record matters to this device's
submission; it does not choose a predicate or a pathway, which is a regulatory decision for a
qualified person. Facts about each device come from FDA's records and the applicant's own summary,
cited to the query that returned them. Statements about this device come from a company document,
with its path, an unreviewed MOS draft, or this session's interview. FDA's 2023 guidance on
predicate selection is cited as a draft; check whether it has been finalized.*

## Starting Point

Product code: {{ABC — FDA device name}} — {{chosen in context/regulatory/classification.md / leaned toward in an unreviewed draft / given in this session}}

Regulation: 21 CFR {{xxx.xxxx}} — {{identification, quoted}}

Path the code points to: {{510(k) / 510(k) exempt / PMA / other — in plain words}}

Indications for use — the new device: {{statement word for word, and its source}}

How it works: {{principle of operation, in plain words}}

Predicate named by the company: {{device and number, and why it was chosen — or None}}

## Candidates

{{510(k) only. Ranked; none is a recommendation. The criterion that decided each place is stated.}}

| Rank | Number | Device | Applicant | Decided | Code | Intended-use gate | Technology | Safety signals |
|---|---|---|---|---|---|---|---|---|
| Candidate 1 | {{K123456}} | {{name}} | {{applicant}} | {{date}} | {{code}} | {{Passes / Unclear}} | {{Same / Different — how}} | {{None / recall, events}} |

### Candidate 1 — {{K123456}}, {{device name}}

Its indications for use: {{word for word from the summary}}

The intended-use gate: {{Passes / Unclear}} — {{how far the new indications move up the ladder of
specificity, and which decision criteria bear on it}}

Technology: {{what is the same, and what is different}}

FDA's predicate best practices: {{established methods; expected safety and performance; use- or
design-related safety issues; design-related recalls — one line each, with the evidence}}

Its own predicate: {{number and device, its recall history, and any drift in intended use or
technology}}

Why it ranks here: {{the deciding criterion}}

### Devices that fail the intended-use gate

{{Each, with the specific reason. They show where the boundary is.}}

## Multiple-Predicate Scenario

{{Only when no single candidate passes the gate for every part of the indications; delete
otherwise. Both routes, side by side; the choice is the company's.}}

| Part of the indications | Covered by | Its product code | Same intended use as the device? |
|---|---|---|---|
| {{condition / patient group / body site / function}} | {{K123456 — device}} | {{code}} | {{Yes / No — why}} |

Primary predicate: {{number — and why it is most similar overall}}

Checks against FDA's guidance: {{shared intended use, or one predicate per function without
interference; specific indications that may change the intended use; technological differences
from each predicate; the four best practices applied to each; why this is not a split predicate}}

The single-predicate route: {{the indications narrowed to what the best single candidate covers,
and what that gives up — including any must-have claim}}

The multiple-predicate route: {{the full indications, which predicate covers which part, and the
extra testing and argument each adds}}

## Comparison Table

{{The new device beside the top two or three candidates. Same or Different on each row; for each
difference, the question it raises. Whether FDA would see it as a different question of safety and
effectiveness is argued in the submission, not here.}}

| Row | New device | {{Candidate 1}} | {{Candidate 2}} | Same or different |
|---|---|---|---|---|
| Indications for use | {{}} | {{}} | {{}} | {{Same / Different — the question it raises}} |
| Intended use | | | | |
| Users and setting | | | | |
| Body site and patient contact | | | | |
| Principle of operation | | | | |
| Energy source | | | | |
| Materials | | | | |
| Sterility and use | | | | |
| Software | | | | |
| Key specifications | | | | |
| Performance testing cited | | | | |

## Requirements: Special Controls, Guidance and Standards

{{What a submission for this device must show, and the standards that help show it, as checked on
{{date}}. This is where a test plan starts, not the plan.}}

### Special controls

Regulation: 21 CFR {{xxx.xxxx}} — {{listed in the regulation / a guidance document named as the
special control / none named}}

{{Form 1: each special control, quoted from the regulation. Form 2: the guidance named, and a summary
of the risks and measures it sets out. Form 3: "The regulation names no special controls. What FDA
expects is read from the predicates' testing and the guidance below."}}

### Guidance

| Guidance document | Status | Why it matters here | Read? |
|---|---|---|---|
| {{title}} | {{Final / Draft — issued date}} | {{special control / linked to code ABC / cited by a predicate}} | {{Yes / No — why}} |

### Consensus standards

Numbers, titles and FDA's recognition details only.

| Standard | Title | FDA recognition | Extent | Why it applies | Transition |
|---|---|---|---|---|---|
| {{ISO 10993-1 Sixth edition 2025-11}} | {{title}} | {{2-313}} | {{Complete / Partial}} | {{listed for code ABC / cited by K123456 / patient contact / named by a special control}} | {{deadline for the older edition, or None}} |

Standards named in the analysis but not FDA-recognized: {{each, with who relies on it — or None}}

### How the requirements fit together

| Requirement | What it requires | How the top candidates addressed it | Supporting standards | Open? |
|---|---|---|---|---|
| {{special control, or a risk the predicates tested for}} | {{in plain words}} | {{from their summaries}} | {{standards above}} | {{No / Yes — what is missing}} |

## Claims Check

{{Each must-have claim from the differentiation analysis against the top candidates' indications.
A claim outside every candidate's intended use is named here as a question for the claims
strategy.}}

| Claim | Covered by the top candidates' indications? | Note |
|---|---|---|
| {{CL-001 — claim}} | {{Yes / No / Unclear}} | {{which words it would need}} |

## Vetting the Named Predicate

{{Vet mode only; delete otherwise. The named device against the same criteria, beside what the
search found. Where the evidence challenges it: the challenge, and whether the company revised or
confirmed its choice.}}

## No Predicate: The De Novo Case

{{Only when no candidate passes the gate, the only route is a split predicate, or the company
expects a De Novo; delete otherwise.}}

Why no predicate exists: {{the nearest devices, each with the specific reason it fails}}

Similar De Novo grants:

| Number | Device | Granted | Regulation created | Risks FDA identified |
|---|---|---|---|---|
| {{DEN123456}} | {{name}} | {{date}} | {{21 CFR xxx.xxxx}} | {{from the decision summary}} |

Special controls in similar regulations: {{summarized from each regulation; which might apply is a
question for FDA}}

## PMA: Earlier Approvals and Their Evidence

{{Only when the path is PMA; delete otherwise. As each SSED states it.}}

| PMA | Device | Approved | Study design | Primary endpoints | Patients | Follow-up | Control | Main result |
|---|---|---|---|---|---|---|---|---|
| {{P123456}} | {{name}} | {{date}} | {{randomized / single-arm / registry}} | {{endpoints}} | {{n}} | {{length}} | {{comparator}} | {{as stated}} |

## What This Means for the Submission

{{Facts, not a choice. Which candidate would be primary and why; whether more than one predicate
is needed and each shares the intended use; any split predicate flagged; the technological
differences a reference-device search would work through; where a Pre-Submission would settle an
open question.}}

Next step: {{a qualified person chooses the primary predicate / the company decides between a
510(k) and a De Novo / resolve the questions in Appendix C first}}

## Appendix A: Devices Screened Out

Every device considered and set aside, with the reason, so the search can be checked.

| Number | Device | Decided | Code | Why it was set aside |
|---|---|---|---|---|
| {{K123456}} | {{name}} | {{date}} | {{code}} | {{name or function unlike this device / statement only / superseded}} |

## Appendix B: Search Log

Every query sent to FDA or the eCFR, in order, so it can be run again. No company document,
product name or claim was sent. All queries were run on {{date}}, unless a row says otherwise.

| # | What was searched | Query | Results returned |
|---|---|---|---|
| 1 | {{plain words}} | {{query exactly as printed by openfda.py}} | {{n found; n shown}} |

Summaries downloaded and read: {{numbers}} — {{n}} in all, and why that was enough.

## Appendix C: Open Questions and Challenges

{{Unclear gates; summaries that could not be read; contradictions between documents; beliefs the
evidence challenged, and whether each was revised or confirmed over the challenge.}}

---

*Generated with MOS and not reviewed. MOS provides no warranty. This document must be reviewed and
approved by qualified personnel at your company before it is used for any regulated purpose.*
