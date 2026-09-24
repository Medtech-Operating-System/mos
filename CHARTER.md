# Medtech Operating System — Charter

*Draft, 2026-09-19. This file is the source of truth. An earlier Claude doc served the first review pass and is no longer authoritative.*

## Why MOS exists

Nobody goes to school for medtech. There is no degree that teaches you how to run design controls, scope a clinical study, choose a regulatory pathway, or price a device. People learn by doing it wrong first.

Three things make that worse than it needs to be:

- **The knowledge is tribal.** It lives in the heads of people who have done it before, and it leaves when they do.
- **Every company does it differently.** A design review at one company looks nothing like a design review at the next, so experience transfers poorly.
- **Even the words differ.** User needs, user requirements, product requirements and design inputs mean different things at different companies, which makes it hard to learn from anyone outside your own walls.

MOS exists to turn that tribal knowledge into something shared, structured and reusable: an open system that tells you what to produce, in what order, and gives you the tools to produce it.

It is built by the Medtech Mindset community, and it is unaffiliated. It is not a service provider's funnel.

## What MOS is

MOS is an operating system in the literal sense: a structure for your company's own information, a map of the work, and a set of tools that run against both.

**The litmus test.** Every design decision serves one sentence: *a founder with no medtech background produces a document a reviewer would accept, in an afternoon, using their own information.* A tool, template or layer that does not contribute to that does not ship.

| OS concept | MOS equivalent |
| --- | --- |
| File system | The **context standard**: a defined folder structure for a company's own information — intended use, user needs, risk file, design inputs, test reports, regulatory strategy, commercial plans |
| Process map | The **lifecycle map**: which phase you are in, what it produces, what depends on what |
| Applications | **Tools**: each one does a single job, reading from and writing to the context |
| Shell | The **AI** (Claude or another), which runs the tools on the user's machine |
| Manual | The **education layer**: why each step exists, taught through the Medtech Mindset Classroom |

The context standard is what separates MOS from a template library. It also solves the vocabulary problem: if the structure says a thing is called `design-inputs`, that is what it is called.

### What a user's machine looks like

```
Acme Medical/                 <- their folder; sync it with Drive, Dropbox, OneDrive or nothing
├── mos/                      <- downloaded from MOS; replaceable
│   ├── lifecycle-map.md
│   ├── context-standard.md
│   └── tools/
│       └── user-needs/
│           ├── SKILL.md      <- the instructions the AI follows
│           └── templates/
├── context/                  <- their data, in their own folder. MOS keeps no copy
│   ├── product/
│   ├── users-and-needs/
│   ├── risk/
│   ├── design/
│   ├── manufacturing/
│   ├── clinical/
│   ├── regulatory/
│   └── commercial/
└── outputs/
```

The eight folders under `context/` are the **context domains**, defined in `context-standard.md`.
They hold a company's documents; the lifecycle map's six disciplines are a different cut, because
most documents are the work of more than one discipline.

To use a tool: download it into `mos/`, point an AI at the folder, and say *"run the user needs tool."* The AI reads the tool's instructions, reads the existing context, interviews the user about the gaps, and writes a draft into `context/`.

### Tools get better as context fills in

Every tool must work at all three levels, and should improve at each one.

| Context available | What the user gets |
| --- | --- |
| None | A good template and an expert-written process — roughly what free template libraries offer today |
| Partial | Drafts specific to their device rather than generic boilerplate |
| Full | New work traceable to what already exists, with contradictions flagged |

Early tools should also **build** context, not just consume it. That is why user needs is the first tool.

## Who MOS is for

Three audiences, served by the same system but not by the same release.

| Audience | What they need | What MOS gives them |
| --- | --- | --- |
| **Founders and first hires** | To know what to produce and in what order, with nobody to ask | The lifecycle map, the context standard, and tools that produce real deliverables |
| **Early-career professionals** | To understand why the work is done this way, not just what to fill in | The education layer, plus the chance to build and be credited |
| **Subject-matter experts** | To execute familiar tasks faster | Tools that draft from their company's own context instead of from scratch |

Founders are the center of gravity for the first year. They have the sharpest pain and the least support. Each release should delight one audience first rather than half-serve all three.

## Principles

1. **Unaffiliated.** MOS belongs to no consultancy, vendor or service provider. No tool is a sales funnel, and that applies to the founder too.
2. **Context first.** A tool that cannot read a company's own information is a chatbot with a template. Context is the product.
3. **Whole lifecycle.** Technical, clinical, regulatory, quality, manufacturing and commercial. Most existing resources cover one slice; the gaps between slices are where projects actually fail.
4. **AI-agnostic.** Tools are written as plain Markdown that any capable AI can run. They are designed and tested on Claude first.
5. **Your data stays yours.** Context lives in the user's own folder. Nothing company-specific goes into the public repository, ever.
6. **No self-promotion.** Contribute expertise, not marketing. Credit is given generously; advertising is not.
7. **Use at your own risk.** MOS encodes good practice drawn from public standards and guidance. Every output must be reviewed and approved by qualified people at the user's company. MOS is not a regulatory consultant and does not assume responsibility for anyone's submission.
8. **Opinionated where it matters.** A system that accepts every preference becomes medtech soup. The architecture has a final decision-maker.

## The lifecycle map (v0.1)

The lifecycle map is the architecture. It fixes the phases, the vocabulary and the dependencies, and every tool is placed on it. This first cut is deliberately rough and is the community's first job to argue about.

Phases run left to right, but post-market evidence feeds back into design, which is where many teams lose traceability.

```
00 Concept → 01 Definition → 02 Design → 03 V&V → 04 Submission → 05 Launch → 06 Post-market
                                ↑________________________________________________|
                                                 feedback
```

Seven phases, six disciplines. Each piece of work sits under the discipline that leads it; most
involve others as well, and the map on medtechoperatingsystem.com shows which.

| Phase | Technical | Clinical | Regulatory | Quality | Manufacturing | Commercial |
| --- | --- | --- | --- | --- | --- | --- |
| **00 Concept** | Feasibility and technology options | Unmet need and standard of care | Preliminary classification and pathway | Initial hazard identification | Manufacturing feasibility and process options | Market size and competitive landscape; freedom to operate and IP landscape |
| **01 Definition** | Product requirements and architecture | Target population and endpoints | Intended use, indications for use, risk plan; applicable standards and guidance list | Design and development plan | Make-versus-buy and supplier strategy | Value proposition, pricing hypothesis, reimbursement path |
| **02 Design** | Design inputs and outputs, design reviews; verification and validation planning; prototype builds and design iterations | Early human factors and clinician input; usability engineering file opened | — | Risk file, design controls, supplier controls | — | Cost of goods and business case |
| **03 V&V** | Verification testing, biocompatibility, software validation | Usability validation, pilot or pivotal study; clinical evaluation report | — | Test plans and reports, traceability; design review and design freeze | Sterilization and packaging validation | Launch readiness and KOL engagement |
| **04 Submission** | Technical file assembly | Clinical evidence summary | 510(k), De Novo, PMA, CE mark; submission strategy; labeling and instructions for use; responses to agency questions | Quality system readiness for audit | — | Payer strategy and coding |
| **05 Launch** | — | Training materials | Labeling, registration, QMS readiness; post-market surveillance plan | Complaint handling and field service setup | Design transfer and manufacturing readiness; process validation (IQ, OQ, PQ) | Sales model, pricing, distribution |
| **06 Post-market** | — | Post-market clinical follow-up | Complaints, vigilance, surveillance; periodic safety and performance reporting | Design changes and CAPA inputs; change control and re-validation | Yield improvement and cost reduction | Adoption, expansion, next indication |

A dash means no work in that phase is led by that discipline, not that the discipline is idle.

The map is also the tool catalog. Once it exists, anyone can point at a cell and say *"there is no tool here,"* which is how the roadmap builds itself.

**Early roadmap:** `setup` (interviews a founder and scaffolds their context folder), then `user-needs`, then a **context health check** — a mock audit that reports whether a team's design history file is complete, current and traceable, scored on evidence rather than on how many folders exist.

**Open for debate:** the phase names, whether concept and definition should merge, and whether the six disciplines are the right cut.

## How MOS gets built

### Governance

Eric Sugalski is the architect and holds final say on the lifecycle map, the context standard and the tool format. Everything else is open. The intent is a system with a coherent spine, not a committee.

Roles people can grow into:

- **Contributor** — submits a tool, a template, an improvement or a test report
- **Maintainer** — owns one tool, reviews changes to it, and is named on it
- **Domain lead** — owns a discipline of the lifecycle map (technical, clinical, regulatory, quality, manufacturing or commercial)

### Cadence

One tool per month, built in public, demoed on a community call. That is the internal goal, not a public promise. The community measures MOS on momentum — tools shipping, testers using them — rather than against a calendar.

### Two rules that protect the project

1. **No tool without three testers.** Before a tool is built, at least three community members must commit to using it on real work and reporting back. This guarantees each tool has users at launch and keeps the founder from building into silence.
2. **Every tool starts from a real problem someone has right now.** Not from a gap on the map, and not from what would look impressive.

### Two ways to contribute

Most subject-matter experts have never opened a pull request, and that cannot be a barrier to contributing.

| Path | Who it is for | How it works |
| --- | --- | --- |
| **GitHub** | Technical contributors | Fork, edit, open a pull request |
| **Skool** | Everyone else | Post the draft or file in the community; a maintainer commits it, with the contributor credited as author |

### What contributors get

- **Named authorship** on every tool they help build — "Maintainer, MOS Risk Management tool" is a real line on a résumé
- **Review and mentorship** from experienced practitioners, which is the strongest draw for early-career members
- **A tool they needed anyway**, built faster because others helped
- **Stage time** on the monthly community call
- **A path upward**, from contributor to maintainer to domain lead

### The tool format

Each tool is a **skill package**, not a loose document: a folder holding `SKILL.md` (YAML frontmatter naming the tool and when to use it, then numbered execution steps), templates, any deterministic scripts, a statement of what context it reads and writes, and a named maintainer.

Two consequences. The tool is invocable as `/user-needs` rather than described in prose, and mirroring the same instructions to `AGENTS.md` lets other AI tools run it — which is how the AI-agnostic principle gets honored in practice rather than in theory.

Tools are self-contained and versioned. If it cannot be described in one sentence, it is two tools.

## Licensing and intellectual property

Deliberately lightweight: no lawyers, no contributor paperwork, no bureaucracy. A one-hour legal review before public launch is worth doing, but nothing here should require it.

| Item | Approach | Why |
| --- | --- | --- |
| Content (templates, guides, education) | **CC BY 4.0** | Free to use and adapt with attribution; easy for company legal teams to accept |
| Code and scripts | **MIT** | Simple and universally understood |
| Contributions | **Developer Certificate of Origin** (a one-line sign-off, as Linux uses) | No agreements to sign, no legal cost |
| Name and logo | Trademark held by the founder | The content stays open; the brand stays protected |

**Every contribution affirms three things:**

1. I wrote this myself, or I have the right to share it.
2. It contains no confidential information belonging to my employer or anyone else.
3. It reproduces no text from ISO, IEC, AAMI or other copyrighted standards. Citing clause numbers is fine; pasting clause text is not.

Two consequences worth stating plainly:

- **Anyone may use MOS commercially, including forking it.** That is what open means, and the trademark prevents a fork from passing itself off as official.
- **MOS may later offer a paid hosted version built on contributed work.** Both licenses permit this. It is stated up front so nobody is surprised.

Every output carries the same disclaimer: MOS provides no warranty, and all outputs must be reviewed and approved by qualified personnel at the user's company.

## How people get and use MOS

### Phase 1: open source, now

- **GitHub organization** (not a personal account), so the project reads as unaffiliated, maintainers can be added, and it outlives any one person
- **Download as ZIP** for non-technical users. No Git knowledge required: download, unzip, drop into the folder. Each release is a numbered GitHub Release, and every past release stays available
- **Skool** as the home of MOS: it holds the download links and the educational material, including the Classroom videos, and it is where discussion and contributions happen
- **medtechoperatingsystem.com** as a static site generated from the repository: browsable lifecycle map, tool catalog and documentation, and the way into the community. It sends people to Skool for downloads and does not host them. No accounts, no backend, essentially no hosting cost
- **LinkedIn and the newsletter** for reach and announcements. MOS stays editorially separate from the newsletter's opinions

### Phase 2: hosted, only when earned

A hosted application with accounts, connected storage and browser-based tools is deferred. Two reasons:

1. Building it now would consume the entire time budget and produce a polished shell around one or two immature tools.
2. Local execution actually gives **better** context access. An AI reading a local folder sees everything with zero integration work, while a web app must build OAuth connections to Drive, Dropbox, OneDrive and SharePoint before it can read anything.

**The real onboarding hurdle in Phase 1** is not GitHub. It is getting members set up with an AI that can read their own files. The Classroom exists to clear exactly that: set up your context folder, connect your AI, run your first tool. If members genuinely cannot get past that step with good instruction, that is the signal that Phase 2 is worth building.

## The first 90 days

Budget: roughly 4–8 hours per week. The plan is sized for that, which means the founder's hours go into architecture, review and community energy — not into writing all the content.

### Month 1 — Foundation

- [ ] Publish this charter to Skool and collect reactions
- [ ] Create the GitHub organization with licenses, contribution guide and DCO sign-off
- [ ] Publish the context standard v0.1 (folder structure, naming, file formats)
- [ ] Publish the lifecycle map v0.1 for the community to tear apart
- [ ] Recruit three testers for the setup tool

### Month 2 — First tool

- [ ] Ship the **setup** tool: it interviews a founder about their device, intended use and stage, then scaffolds a populated context folder
- [ ] Record three Classroom videos: set up your context, connect your AI, run your first tool
- [ ] Run it live with the three testers and fix what breaks
- [ ] Hold the first monthly community call, with a demo

### Month 3 — Proof it is not a solo project

- [ ] Stand up the static site at medtechoperatingsystem.com
- [ ] Ship the **user needs** tool, seeded from existing material and de-branded, with someone other than the founder as maintainer
- [ ] Name the first domain leads
- [ ] Announce publicly on LinkedIn and in the newsletter

### What success looks like at 90 days

The community defines the long-term target, but the 90-day bar is concrete:

- Two working tools, at least one maintained by someone else
- Three or more members who have used a tool on real work
- Five or more people who contributed something
- A lifecycle map the community argued over and improved

### What would say it is not working

The honest failure mode is the founder building alone into silence. Watch for: fewer than three testers willing to commit, no contributions from anyone else by month 3, or no member completing the setup without hand-holding. Any of those means the problem is engagement or onboarding, not tooling — and the response is to fix that, not to build more tools.

## Open questions for the community

1. **Is the lifecycle map right?** Are these the right phases, in the right order, with the right names? Are the six disciplines the right cut?
2. **Where does the context standard start?** What is the minimum folder structure a two-person company can adopt on day one without it feeling like bureaucracy?
3. **Which tool after user needs?** Point at the cell on the map that hurts most in your own work.
4. **What terminology fights need settling first?** User needs vs. user requirements vs. design inputs is the obvious one. What else?
5. **Who wants to maintain something?** Tools need owners, and disciplines need leads.
6. **What would make you use this on real work**, rather than read it and move on?
