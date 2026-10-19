# Target product profile — {{device}}

Company: {{company}}
Written: {{date}} · Source: MOS setup skill

*Notes: A draft. It records what the team said the product must be, and has not been reviewed.
Where each answer came from is listed at the end.*

## How to read this document

This is the reference for what the product must be. Every MOS skill reads it.

- **Minimum acceptable** is the least the product can be and still be worth building. Below it,
  the team rethinks the project, not the specification.
- **Target** is what the team is aiming for: the product that wins.
- Each value carries its direction — `≥ 95%`, `≤ $400`, `no later than Q3 2028` — so there is no
  doubt which way is better.
- **Not set yet** means nobody has decided. It is a question for the team, not an oversight. The
  ones something is waiting on are on the company's issues list, with everything else still open.

MOS skills never edit it. When a skill finds something that bears on a row, it raises an issue
naming the row and what it found, and the team decides, on the issues list or during the skill's
run. To make the next revision, run `setup`: it drafts it from the closed issues that change a row,
and lists each change below. A team may also redline this document in Word and save the result as
a new revision — `target-product-profile_revB.docx` — in `context/product/`.

## Product summary

{{Three to five sentences: what the device is, who uses it on whom, what it does for them, and why
someone would buy it over what they use today.}}

## 1. The device

| Attribute | Description |
|---|---|
| What it is | {{physically or technically}} |
| Type | {{hardware / software / consumable / combination}} |
| Sterile | {{yes, sold sterile / sterilized before use / no / Not known yet}} |
| What touches the patient, and for how long | {{skin, tissue, blood — minutes, days, permanent — or nothing}} |
| How far into the body | {{none / on the skin / natural opening / surgical / implanted}} |
| Energy | {{none, or electrical, radiation, heat, light, sound — what kind}} |
| Software | {{none / supports the device / is the device}} |

## 2. Use

| Attribute | Statement |
|---|---|
| Intended use — what the device does | {{one sentence}} |
| Indications for use — the condition, the patients and the body site | {{statement word for word, or Not written yet}} |
| Condition it diagnoses, treats, prevents or monitors | {{condition, or General tool, no specific condition}} |
| Patients | {{age, sex, severity, setting}} |
| Part of the body | {{site}} |
| Who should not use it — contraindications | {{situations, or Not known yet}} |
| Operated by | {{user, and their training}} |
| Setting | {{hospital / clinic / home / pre-hospital / laboratory}} |
| Lay users involved | {{yes / no}} |
| The clinical problem | {{problem}} |
| What people do today instead | {{current standard of care}} |

## 3. Clinical performance

What the device must do for patients, and the risk it may carry. At concept stage most of these
are not set yet; that is normal.

| Attribute | Minimum acceptable | Target |
|---|---|---|
| Main clinical benefit, and how it is measured | {{e.g. ≥ 90% sensitivity for X}} | {{}} |
| Safety — the serious harm to avoid, and the rate tolerated | {{}} | {{}} |

## 4. Technical performance

The two to five numbers that decide whether the device works, then the device's life.

| Attribute | Minimum acceptable | Target |
|---|---|---|
| {{device-specific attribute, e.g. accuracy, battery life, procedure time}} | {{}} | {{}} |
| Use life or shelf life | {{}} | {{}} |

## 5. Usability and form

| Attribute | Minimum acceptable | Target |
|---|---|---|
| Size and weight | {{}} | {{}} |
| Time to set up, or to use | {{}} | {{}} |
| Training the user needs | {{}} | {{}} |

## 6. Claims

What the company needs to be able to say about the device, in its own words. Not yet checked
against the regulatory path or the evidence it would need.

| Claim | Priority | Already published? |
|---|---|---|
| {{claim, in the founder's or the site's words}} | {{Must have / Nice to have}} | {{no / yes — page}} |

## 7. Commercial

| Attribute | Minimum acceptable | Target |
|---|---|---|
| Who pays, and who decides to buy | {{statement}} | — |
| Why they would choose it — the value proposition | {{statement}} | — |
| Competitors, and the one to beat | {{names}} | — |
| Selling price | {{e.g. ≥ $X per unit}} | {{}} |
| Cost to make — cost of goods | {{e.g. ≤ $Y per unit}} | {{}} |
| How it gets paid for — reimbursement | {{existing code / new code needed / not reimbursed / Not known yet}} | — |

## 8. Regulatory

The company's expectations, not yet checked against FDA's records. The MOS skill `product-code`
checks the classification.

| Attribute | Expectation |
|---|---|
| Where it is sold first — target geography | {{US / EU / other}} |
| How risky FDA is expected to consider it — class | {{I / II / III, or Not known yet}} |
| How it gets to market — pathway | {{510(k) / De Novo / PMA / CE mark / Not chosen yet}} |
| A marketed device it would be compared to — predicate | {{device, or none identified}} |
| Clinical study expected before submission | {{yes / no / Not known yet}} |

## 9. Timeline

| Milestone | Latest acceptable | Target |
|---|---|---|
| First use in people | {{}} | {{}} |
| Submission | {{}} | {{}} |
| Clearance or approval | {{}} | {{}} |
| Launch | {{}} | {{}} |

## Appendix A: Changes in This Revision

{{"First draft" — or each change: the row, from what to what, and the issue that decided it.}}

| Row | Was | Now | Decided in |
|---|---|---|---|
| {{4.2 Battery life — minimum}} | {{≥ 8 h}} | {{≥ 12 h}} | {{ISS-014, by Jane Doe, 2026-10-17}} |

## Working Notes

### Where the answers came from

- **Setup interview, {{date}}** — {{who answered}}. Everything not listed below.
- **{{document path}}** — {{the sections or rows it supplied}}
- **{{web page address}}, read {{date}}** — {{the rows it supplied}}, confirmed by the user

---

*Generated with MOS and not reviewed. MOS provides no warranty. This document must be reviewed and
approved by qualified personnel at your company before it is used for any regulated purpose.*
