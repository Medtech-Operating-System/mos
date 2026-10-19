# About the target product profile

Background for the AI running `setup`. **Do not recite this to the user.** Read it only when the
user asks what a target product profile is, why setup writes one, or whether they need it, and
answer that question in a few sentences. Most users will not ask.

## What it is

A target product profile (TPP) lists the characteristics a product must have, each at two levels:
the **minimum acceptable**, below which the product is not worth building, and the **target**, the
product the team is aiming for. A review of 120 published TPPs found nearly all use those two
levels, under names such as minimal, minimum or acceptable, and optimal, ideal, preferred or
desired.[^review] One industry account puts the minimum plainly: failing to meet the essential
parameters often means the program ends.[^biocurate]

## Why a device company writes one

- **It aligns the team.** Founders, engineers and advisors often hold different minimums without
  knowing it. Writing them down, row by row, shows where they differ while it is cheap to settle.
  The rows marked `Not set yet` are often the most useful part.
- **Others ask for it.** Investors, grant reviewers and partners commonly ask for a TPP or
  something like it. MaRS's device TPP workbook is built for communications with regulators,
  investors, partners and employees.[^mars] NIH's Blueprint MedTech program expects applicants to
  propose a TPP before larger-scale R&D.[^blueprint] CARB-X publishes a TPP with minimum
  acceptable criteria for each diagnostics funding call.[^carbx] No source found shows that a
  general SBIR application requires one, so say "commonly requested", not "required".
- **It is the reference the rest of MOS reads.** User needs, the regulatory skills and the
  commercial skills all start from it, and when they find something that bears on a row, they
  name the row.

## "Isn't that a drug thing?"

The TPP is best known from drug development. FDA's 2007 draft guidance describes it as a summary
of a drug development program written in terms of labeling concepts: the company writes the label
it wants first, and plans the studies to earn it.[^fda] The idea carries over to devices directly.
A device's version of the label is its indications for use and its claims. A device TPP adds what
a drug's does not: the engineering numbers the device must hit, whether its user can use it, and
whether it can be made at a price someone will pay.

WHO's product profiles cover diagnostics and medical devices as well as medicines, with the same
minimal and optimal structure.[^who] Device engineers may know parts of it under other names —
must-have and nice-to-have need criteria, or a product requirements document. The TPP sits above
those, and user needs and design inputs build on it.

## How MOS's TPP is organized

Sections follow the groupings device TPPs commonly use — use, population, user, setting,
technology, safety, effectiveness[^nice][^who] — with the commercial and regulatory rows investors
ask about. A value nobody has decided reads `Not set yet`, and an appendix lists where the answers
came from. Rows that
are statements, such as the intended use, have one value; rows that are numbers have both levels.

## Sources

[^review]: Target product profiles: opportunities and implications for health innovation
    development — a scoping review. https://www.sciencedirect.com/science/article/pii/S2211883726000936
[^biocurate]: Biocurate, Constructing a target product profile: industry's perspective.
    https://www.biocurate.com/resources/constructing-a-target-product-profile-industrys-perspective/
[^mars]: MaRS, Defining your target product profile: medical device products.
    https://learn.marsdd.com/article/defining-your-target-product-profile-medical-device-products/
[^blueprint]: NIBIB, Blueprint MedTech.
    https://www.nibib.nih.gov/news-events/newsroom/blueprint-medtech-continues-fuel-innovation-devices-treat-and-diagnose-conditions-affecting-nervous-system
[^carbx]: CARB-X, 2024 funding round. https://carb-x.org/carb-x-news/2024-funding-round/
[^fda]: FDA, Target Product Profile — A Strategic Development Process Tool, draft guidance,
    Federal Register, 30 March 2007. https://www.govinfo.gov/content/pkg/FR-2007-03-30/pdf/E7-5949.pdf
[^who]: WHO, Target product profiles, preferred product characteristics and target regimen
    profiles. https://www.who.int/our-work/science-division/research-for-health/optimizing-research-processes/product-profiles
[^nice]: NICE HTA Lab, Target product profiles of digital health technologies.
    https://www.nice.org.uk/Media/Default/About/what-we-do/HTA%20Lab/target-product-profiles-of-digital-health-technologies.docx

Read 2026-10-16.
