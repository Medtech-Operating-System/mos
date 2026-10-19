# Design Inputs — {{device}}

Company: {{company}}
Written: {{date}} · Source: MOS design-inputs skill · Mode: {{draft / review}}

*Notes: The requirements the design of this device must meet, each stated so it can be verified
and traced to where it came from. They say what the device must do and be, not how: the parts,
materials and mechanisms that meet them are design outputs, recorded in the specifications.*

## Source Documents

The documents these design inputs answer, at the revision read.

| Document | File | Revision |
|---|---|---|
| Target product profile | {{context/product/...}} | {{revA / unreviewed draft}} |
| User needs | {{}} | {{}} |
| Hazards identification | {{}} | {{}} |
| Risk analysis | {{path — or None yet}} | {{}} |
| Precedent search | {{path — or None}} | {{}} |
| Classification | {{path — or None}} | {{}} |
| Standard requirements | {{each design-inputs-<standard> document — or None yet}} | {{}} |
| {{Brought document, such as a product requirements document}} | {{path}} | {{as found}} |

Intended use: {{one sentence, from the target product profile}}
Users and settings: {{who uses it, on whom, where}}

## Design Inputs

| ID | Section | Requirement | Acceptance criterion | Verification method | Sources | Safety-related | Rationale |
|---|---|---|---|---|---|---|---|
| DI-001 | {{section}} | The device shall {{what it must do or be, at its boundary}}. | {{measurable value, with its conditions — Proposed: value — or Not set yet}} | {{Test / Inspection / Analysis / Demonstration — and a test-method standard where one applies}} | {{UN-, HZ-, RC-, TPP row, 21 CFR special control, comparison row, standard document, brought document, interview}} | {{Yes / Yes, provisional / No}} | {{why the value is what it is, in one line; the TPP target; where an outside constraint comes from}} |

{{Rows are grouped by section, in this order, leaving out sections with no rows: Performance;
User interface; Electrical safety and EMC; Mechanical; Materials and body contact; Security;
Environment; Reliability and life; Packaging and sterility; Labeling; Manufacturability;
Standards.}}

### Definitions

**ID** — each design input keeps its ID permanently. A deleted row's ID is retired, never reused,
and the others are not renumbered.

**Acceptance criterion** — the value verification must show, with the conditions it is measured
under. Where the target product profile gives a minimum acceptable and a target level, the
criterion is the minimum; the target is in the rationale as a design goal. **Proposed** marks a
value drawn from the cited evidence that the team has not yet confirmed: delete the word when the
value is confirmed in review. **Not set yet** marks a value nobody has decided.

**Verification method** — *Test*: measured on the device. *Inspection*: examined against the
requirement, by eye or with a gauge. *Analysis*: shown by calculation, simulation or review of
records. *Demonstration*: shown by operating the device, with no measurement.

**Safety-related** — *Yes* where the row is a risk control, or answers a hazard. *Yes,
provisional* where it answers a hazard with a control FDA, a standard or a predicate already
names, before any risk analysis has confirmed it.

**Standards** — a row in the Standards section names a product standard the device must conform
to. The clauses that apply, and what each asks of this device, are in that standard's own design
input document, incorporated at the revision named.

## Working Notes

### Coverage

Every input these design inputs must answer, and the rows that answer it.

| Input | What it says | Answered by |
|---|---|---|
| {{UN-001}} | {{the need, short}} | {{DI-IDs — or None: on the issues list}} |
| {{HZ-001}} | {{hazard → harm, short}} | {{DI-IDs — or Awaiting risk analysis: on the issues list}} |
| {{21 CFR xxx.xxxx (b)(1)}} | {{the special control, short}} | {{DI-IDs}} |
| {{TPP 4: battery life}} | {{minimum and target}} | {{DI-IDs}} |

### The Predicate Comparison

Each row of the precedent search's comparison table, for {{K123456, and reference devices}}. A
row that describes a design output is tied to the design input that states the requirement behind
it, so the subject device's column can be filled from the specifications later.

| Comparison row | Predicate | Kind | Design input |
|---|---|---|---|
| {{Key specifications}} | {{what the predicate has}} | {{Requirement / Design output}} | {{DI-IDs — and, for a design output, what it achieves}} |

{{Or: No precedent search was available. Running product-code and precedent-search would add it.}}

### Set Aside

Lines from brought documents that are not design inputs, and where each belongs.

| Line | From | Kind | Where it belongs |
|---|---|---|---|
| {{the line}} | {{document and section}} | {{Design output / User need / Product target / Untestable}} | {{the specifications, related to DI-ID / user-needs / the target product profile / nowhere, and why}} |

### Process Standards

Standards that set how the work is done, not what the device must be. They belong in the design
and development plan, not here.

| Standard | Process it governs |
|---|---|
| {{ISO 14971:2019}} | {{risk management}} |

### Review of Existing Rows

{{Review mode only. Each existing row, checked against the rules: ID | Finding | Action (keep /
rewrite / merge with / move to the specifications / delete). Or: Not applicable: no earlier design
inputs.}}

### Challenges

{{Where these design inputs and what the team brought disagreed, the evidence, and whether each
was revised or confirmed over the challenge — or None.}}

The open questions, gaps and contradictions this draft raised are on the company's issues list.

---

*Generated with MOS and not reviewed. MOS provides no warranty. This document must be reviewed and
approved by qualified personnel at your company before it is used for any regulated purpose.*
