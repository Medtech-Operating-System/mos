# Hazard checklist

*v0.1, 2026-10-17. Used by `hazards-id`, and by any later skill that looks for what could go wrong
with a device. A change to this file is checked against every skill that uses it before it
ships.*

The prompts a MOS skill walks through to find a device's early hazards. It is a memory aid, not a
list of answers: most lines will not apply to a given device, and the hazards that matter most
usually come from FDA's records for the device type and from the user's own knowledge, not from
here. Its job is to make sure no whole category is missed.

**Where this came from.** Written for MOS from public sources: FDA guidance documents, which are
US government works, and the structure of the IMDRF adverse event terminology, whose documents
carry no restriction on reproduction or use. Inclusion here does not imply IMDRF endorsement. No
text is taken from ISO 14971, ISO/TR 24971 or any other copyrighted standard. Where the user has
put licensed copies of those in `context/regulatory/standards/`, the skill checks its list against
them as well; this file does not stand in for them.

## The words

Plain words first, the term beside them. A skill uses these in the same way every time.

| Plain words | Term | Example |
|---|---|---|
| Something about the device or its use that could hurt someone | **Hazard** | Electrical energy in a handheld unit |
| What has to happen for the hazard to reach a person | **Sequence of events** | Casing cracks when dropped; user keeps using it |
| The moment a person is exposed to it | **Hazardous situation** | User's hand touches a live part |
| The injury or damage to health that can follow | **Harm** | Electric shock; burn |

A hazard on its own hurts no one. A row is complete when it names all four, and a skill that
cannot name the harm says so rather than leaving the row looking finished.

## How a skill uses this file

- **Walk every section.** For each line, decide whether it applies to this device, might apply,
  or does not. Write a row for every line that applies or might. A line that does not apply needs
  no row, but a whole section ruled out gets one sentence saying why.
- **Cite the line.** Each row the checklist produced names its ID (`HC-E2`). A row that came
  from FDA's records or from a standard names that source instead, and may name a line here too.
- **Start from the triggers.** The table at the end says which sections a device feature makes
  likely. A section the triggers point at deserves more than a glance.
- **Name harms in IMDRF terms where one fits.** IMDRF Annex E (health effects: clinical signs,
  symptoms and conditions) and Annex F (health impact) give a shared vocabulary that FDA's own
  adverse event codes map onto. A plain description is fine where no term fits.

## E — Energy

What the device carries, stores or delivers that could injure if it reaches the wrong place or in
the wrong amount.

| ID | Prompt |
|---|---|
| HC-E1 | **Electricity.** Mains or battery power, leakage current through a patient connection, exposed conductors, a failed insulation barrier |
| HC-E2 | **Heat and cold.** Surfaces a person touches, tissue heated by the therapy itself, a battery that overheats, a cooled part that freezes skin |
| HC-E3 | **Moving parts and force.** Pinch points, crushing, entanglement, a motor that starts when it should not, force applied to tissue beyond what was intended |
| HC-E4 | **Stored energy.** Springs, compressed gas, pressurized fluid, a charged capacitor: anything that can release at once |
| HC-E5 | **Weight, shape and stability.** Tipping, falling, sharp edges and points, a part small enough to swallow or inhale |
| HC-E6 | **Radiation.** Ionizing (X-ray); non-ionizing: laser, UV, infrared, radio frequency, ultrasound, light bright enough to injure eyes |
| HC-E7 | **Sound and vibration.** Noise loud enough to damage hearing, vibration transmitted to the user |
| HC-E8 | **Magnetic fields.** Strong magnets in the device; the device taken into an MRI room (heating, pulling force, image artifact, malfunction). FDA guidance on the MR environment, 2023 |

## B — Biological and chemical

What touches the body, or gets into it, and what comes with it.

| ID | Prompt |
|---|---|
| HC-B1 | **Body contact.** What contacts the patient or user, where (skin, mucosa, blood, tissue, bone) and for how long (minutes, up to 30 days, longer). That sets which biological effects need assessing: irritation, sensitization, toxicity, effects on blood, and for longer contact, implantation and long-term effects. FDA guidance on ISO 10993-1, 2023 |
| HC-B2 | **Infection.** A device sold sterile that is not, a sterile barrier breached in shipping, contamination during use, a surface that cannot be cleaned |
| HC-B3 | **Reuse between patients.** Cross-contamination when cleaning, disinfection or sterilization between uses fails or is skipped. FDA guidance on reprocessing in health care settings, 2015 |
| HC-B4 | **Residues and leachables.** Sterilant left behind, cleaning agents, manufacturing residues, chemicals that leach from plastics, adhesives or coatings, products of a material breaking down in the body |
| HC-B5 | **Particles.** Fragments, coating that flakes off, particulate in a fluid path |
| HC-B6 | **Drugs and biologics.** A drug or biologic delivered with or coated on the device: wrong amount, wrong rate, interaction, degradation over shelf life |
| HC-B7 | **Animal or human-derived materials.** Disease transmission, immune response |

## P — Performance

The device does not do what it is meant to, does it badly, or does it at the wrong time.

| ID | Prompt |
|---|---|
| HC-P1 | **Too much or too little.** Over- or under-delivery of energy, drug, fluid, pressure or force |
| HC-P2 | **Not at all.** Loss of function when it is needed: no therapy, no monitoring, no output, and what happens to the patient while it is out |
| HC-P3 | **Wrong timing.** Therapy delayed, started too early, stopped too soon, or not stopped |
| HC-P4 | **A wrong answer.** A measurement, reading or result that is off, leading to a wrong decision: a missed condition (false negative) or unneeded treatment (false positive) |
| HC-P5 | **Alarms.** An alarm that does not sound, sounds when nothing is wrong until people ignore it, or cannot be heard where the device is used |
| HC-P6 | **Wear and ageing.** Fatigue, wear, a battery that runs down, materials that degrade, performance drifting over the device's life or its shelf life |
| HC-P7 | **In the body.** An implant or indwelling part that moves, breaks, perforates, erodes or cannot be removed |
| HC-P8 | **Interference.** Electromagnetic interference with or from other equipment, wireless signals that drop or collide. FDA guidance on electromagnetic compatibility, 2022; on radio frequency wireless technology, 2013 |
| HC-P9 | **Working with other devices.** Accessories, connectors, consumables or systems it depends on: a wrong or incompatible one fitted, a connection that comes apart |

## S — Software and data

Where the device runs software, or creates, stores or sends data.

| ID | Prompt |
|---|---|
| HC-S1 | **Software faults.** A function that fails, hangs, resets or behaves wrongly, and what the device does while it does. FDA guidance on premarket content for device software functions, 2023 |
| HC-S2 | **Wrong data.** Data attached to the wrong patient, corrupted, lost, out of date, or shown in the wrong units |
| HC-S3 | **Cybersecurity.** Someone gains access and the device stops working, behaves wrongly, or exposes patient data. FDA guidance on cybersecurity in medical devices, 2026 |
| HC-S4 | **Algorithms.** A calculation or model that is wrong for some patients, used outside the conditions it was built for, or that changes over time |
| HC-S5 | **Connected systems.** A phone, app, cloud service or hospital system the device relies on goes down, updates, or sends something unexpected |

## U — Use

What people do with it: the mistakes they can make, and where they are when they make them. These
hazards turn most directly into user needs. FDA guidance on human factors and usability
engineering, 2016.

| ID | Prompt |
|---|---|
| HC-U1 | **Setup and steps.** A step missed, done in the wrong order, or done halfway; assembly that can be done wrong |
| HC-U2 | **Reading it wrong.** A display, label, colour, unit or alarm that can be misread, or read too late |
| HC-U3 | **Wrong patient, wrong place.** Used on the wrong person, the wrong body site, the wrong side |
| HC-U4 | **Misconnection.** A connector that fits something it should not, such as a feeding line into an IV line |
| HC-U5 | **Who uses it.** A lay user, a child, an elderly user, someone with limited vision, hearing, dexterity or reading ability, someone tired or stressed, someone untrained or trained long ago |
| HC-U6 | **Where it is used.** Home, ambulance, operating room, outdoors, an MRI suite; light, noise, moisture, temperature, interruptions. FDA guidance on devices intended for home use, 2014 |
| HC-U7 | **Foreseeable misuse.** Uses the company does not intend but can reasonably expect: off-label use, reuse of a single-use device, a workaround for an annoying step |
| HC-U8 | **The instructions themselves.** Warnings, contraindications or steps that are missing, unclear, wrong, or not where the user is when they need them |

## L — Life cycle

Hazards that arise before or after the moment of use.

| ID | Prompt |
|---|---|
| HC-L1 | **Manufacturing.** A defect that gets through: wrong part, bad assembly, a process that drifts |
| HC-L2 | **Packaging, shipping and storage.** Damage in transit, temperature or humidity out of range, a package that is hard to open without contaminating the contents |
| HC-L3 | **Installation, maintenance and service.** Installed wrongly, maintenance skipped, a repair that changes how it works, calibration lost |
| HC-L4 | **End of life and disposal.** Sharps, biohazardous waste, batteries, a device used past its expiry or service life |

## Triggers

A device feature that makes a section likely. Several will apply to most devices.

| If the device… | Look hard at |
|---|---|
| Is powered (mains or battery) | HC-E1, HC-E2, HC-P2, HC-P8 |
| Touches a patient or user | HC-B1, HC-B2, HC-E2 |
| Is sold sterile, or enters the body | HC-B2, HC-B4, HC-L2 |
| Is reused between patients | HC-B3, HC-U1, HC-L3 |
| Is implanted or stays in the body | HC-B1, HC-P6, HC-P7, HC-E8 |
| Delivers energy, a drug or a fluid | HC-P1, HC-P3, HC-P5, HC-E4, HC-E6 |
| Measures, monitors or diagnoses | HC-P4, HC-P5, HC-S2, HC-U2 |
| Runs software or an algorithm | HC-S1, HC-S2, HC-S4 |
| Connects wirelessly or to a network | HC-S3, HC-S5, HC-P8 |
| Is used at home or by lay users | HC-U5, HC-U6, HC-U8, HC-L4 |
| Could be taken into an MRI room | HC-E8 |
| Is used on children | HC-E5, HC-U5, HC-B1 |

## Where else hazards come from

This file is one source of six. The skill draws on all that it can reach; the checklist catches
what the others miss.

| Source | What it gives | Reached through |
|---|---|---|
| FDA special controls and De Novo decision summaries | The risks to health FDA has already named for the device type, each with its mitigation | `precedent-search`'s special-controls map; `openfda.py regulation`, `fetch` |
| Adverse event reports (MAUDE) | Device problems and patient problems reported for the product code or a predicate's brand, and what happened in the reporters' words | `openfda.py problems` |
| Recalls | Failures that reached the market, and their root causes | `openfda.py recalls` |
| PMA summaries of safety and effectiveness | Adverse events seen in the pivotal study, warnings, contraindications | `openfda.py fetch` |
| Labeling of predicate and reference devices | Warnings, precautions, contraindications and listed adverse events: hazards the manufacturer already acknowledged | The user, or the manufacturer's published instructions |
| Standards the user has bought | ISO 14971 Annex C, ISO/TR 24971 Annex A, device-specific standards | `context/regulatory/standards/`, read only after the user confirms their licence allows it |

An adverse event report is an allegation, not a finding. A hazard drawn from one is real enough to
list; how often it happens is not something these reports can tell.
