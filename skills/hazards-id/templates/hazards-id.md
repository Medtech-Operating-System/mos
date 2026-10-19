# Hazards Identification — {{device}}

Company: {{company}}
Written: {{date}} · Source: MOS hazards-id skill

*Notes: A draft preliminary hazard list. It names what could hurt someone with this device, how,
and what harm would follow, so that user needs and design inputs can answer each hazard. It is not
a hazard analysis: no hazard is rated for severity or probability, and no risk control is
proposed. Each hazard notes its sources: an FDA record, with its number; a device's labeling,
with its source and date read; a line of the MOS hazard checklist, by ID; a clause of a standard
the company holds; or this session's interview, which has not been reviewed. Adverse event
reports show that a hazard exists, not how often it happens.*

## The Device as Considered

The features that decide which hazards are possible, as confirmed in this session.

Power: {{mains / battery / none}}
Body contact: {{what touches whom, where, for how long — or None}}
Sterile or reused: {{sold sterile / reused between patients / single use / not applicable}}
Stays in the body: {{yes, for how long / no}}
Delivers: {{energy, drug, fluid, force — or Nothing}}
Measures: {{what, and who acts on it — or Nothing}}
Software and connections: {{what it runs and connects to — or None}}
Users: {{who, with any training or limits that matter}}
Where it is used: {{use environments}}
Use steps: {{the steps, grouped by stage: prepare, use, monitor, complete, handoff}}

Product code: {{ABC — FDA device name, from the classification record or product code analysis
— or Not chosen yet}}
Predicates and reference devices: {{each, with its number and brand — or None named}}

## Hazard List

Each row runs from the hazard to the harm. The last column says which user need answers it, or
that none does yet.

| ID | Hazard | Sequence of events | Hazardous situation | Harm | Who is exposed | Use stage | Sources | For user needs |
|---|---|---|---|---|---|---|---|---|
| HZ-001 | {{the source of harm, in plain words}} ({{checklist section}}) | {{what has to happen for it to reach someone}} | {{the moment a person is exposed}} | {{injury or damage to health — or Harm not yet identified}} | {{patient / user / caregiver / bystander}} | {{prepare / use / monitor / complete / handoff / life cycle}} | {{every source: FDA record and number, label, HC-ID, standard and clause, interview}} | {{UN-ID — or No user need covers this}} |

**ID** — each hazard keeps its ID permanently. A retired hazard's ID is not reused, and the others
are not renumbered.

**Hazards from the checklist alone** have no evidence from similar devices behind them. They stay
on the list; the hazard analysis decides how much each matters.

## Appendix A: What FDA's Records Show

### Risks FDA has named

Special controls, and the risks to health in De Novo decision summaries, for this device type.

| Source | Risk FDA identified | Hazards |
|---|---|---|
| {{21 CFR xxx.xxxx / DEN123456}} | {{the risk, in plain words}} | {{HZ-IDs}} |

### Adverse event reports

{{Product code or brand}}, reports received from {{year}}: {{n}} in all. The problems most often
reported, as FDA's adverse event records name them:

| Kind | Problem | Reports | Hazards |
|---|---|---|---|
| {{Device / Patient}} | {{FDA's term}} | {{n}} | {{HZ-IDs — or Records no hazard}} |

{{Repeat for each product code and brand searched.}}

A report is an allegation, not a finding. Counts rise with how many devices are in use and how
much a manufacturer reports, and are not rates.

### Recalls

| Recall | Device | Date | Root cause | Hazards |
|---|---|---|---|---|
| {{number}} | {{device, with K or P number}} | {{date}} | {{root cause}} | {{HZ-IDs}} |

{{Or: No recalls found for {{code or number}}.}}

### Summaries of safety and effectiveness

{{For PMA devices only. The adverse events seen in each pivotal study, with the HZ-IDs they
support — or Not applicable.}}

## Appendix B: Labeling Reviewed

| Device | Document | Source | Read on | Hazards |
|---|---|---|---|---|
| {{brand, maker}} | {{instructions for use / label, with its revision where shown}} | {{context/inbox/... / URL}} | {{date}} | {{HZ-IDs}} |

{{Or: No labeling was available. Asked for: {{devices}}.}}

## Working Notes

### Checklist and Standards Coverage

#### The MOS hazard checklist

Every section of `mos/lib/reference/hazard-checklist.md`, v{{version}}, was walked.

| Section | Lines that applied or might | Hazards | Ruled out, and why |
|---|---|---|---|
| E — Energy | {{HC-IDs — or None}} | {{HZ-IDs}} | {{one sentence where the whole section was ruled out}} |
| B — Biological and chemical | {{}} | {{}} | {{}} |
| P — Performance | {{}} | {{}} | {{}} |
| S — Software and data | {{}} | {{}} | {{}} |
| U — Use | {{}} | {{}} | {{}} |
| L — Life cycle | {{}} | {{}} | {{}} |

#### The company's standards

{{Each standard read, with its edition and the clauses used, and the HZ-IDs it added — or: Not
done. The company's standards folder held none / the user chose not to send them. The check
against ISO 14971 Annex C and ISO/TR 24971 Annex A is outstanding.}}

No text from any standard is reproduced in this document.

### Search Log

Every query sent outside the company, in order. The terms named product codes, brand names,
submission numbers and device categories; no company document, product name or description was
sent.

| # | What was searched | Query | Sent to | Results returned |
|---|---|---|---|---|
| 1 | {{plain words}} | {{query exactly as run}} | {{FDA / web search}} | {{n}} |

### Challenges

{{Where this list and the company's existing hazard list or beliefs disagreed, the evidence, and
whether each was revised or confirmed over the challenge — or None}}

The open questions, gaps and contradictions this list raised are on the company's issues list.

---

*Generated with MOS and not reviewed. MOS provides no warranty. This document must be reviewed and
approved by qualified personnel at your company before it is used for any regulated purpose.*
