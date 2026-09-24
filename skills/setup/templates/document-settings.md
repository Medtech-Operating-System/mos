# Document settings — {{company}}

Every Word document MOS writes for this company is built from these settings, so all of them
share one cover page, footer, font and page layout. The content differs; the format does not.

To change the format, edit a value, then rebuild the template:

```
python mos/lib/mosdocx.py template --force
```

Documents already written keep the format they were written with. The next one follows the new
settings.

## Settings

Company: {{company name as it appears on documents}}
Logo: {{context/templates/logo.png, or blank to show the company name instead}}
Template: {{MOS, or Company if the company supplied its own controlled template}}
Font: {{Calibri}}
Body size: {{10.5}}
Page size: {{Letter or A4}}
Date format: {{M/D/YYYY, YYYY-MM-DD or DD-Mon-YYYY}}
Document number: {{[Document Number], or the company's pattern, such as DOC-XXXX}}
First revision: {{[Rev], or the company's first revision, such as A or 01}}
Header: {{Off, or On for a slim header on every page but the cover}}

## What each setting does

- **Company** appears at the left of every footer, and on the cover when there is no logo.
- **Logo** sits top left on the cover, and at the left of the header when the header is on.
  PNG or JPEG.
- **Template** says whose template this is. With `Company`, MOS never rebuilds or overwrites it,
  and Font, Body size, Page size and Header are ignored — the company's template decides them.
- **Font** and **Body size** set the body text. Headings, tables, the cover and the footer scale
  with the body size.
- **Page size** is Letter or A4. Wide tables turn landscape either way.
- **Date format** is used on the cover and in the revision history, and skills write dates in the
  document body the same way.
- **Document number** and **First revision** fill the cover, footer and revision history of every
  new draft. Leave them as bracketed placeholders until the company numbers the document.
- **Header**, when on, shows the logo at the left and the document number and revision at the
  right, on every page but the cover.
