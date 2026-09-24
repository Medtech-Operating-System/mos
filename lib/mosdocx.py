#!/usr/bin/env python3
"""mosdocx — Word documents for MOS skills.

MOS skills draft in Markdown and deliver in Word. This script is the one place
that conversion happens, so every document a company receives has the same
cover page, footer and styles regardless of which AI ran the skill. It needs Python
3.8 or later and nothing else: no packages, no network.

Commands:

  check
      Confirm Python can run this script, by building and reading back a
      document in memory. Writes nothing.

  template [--settings PATH] [--out PATH] [--force]
      Build the company's document template from its document settings: a
      cover page with the logo top left, a control table (Document Name,
      Document Number, Revision, Related SOPs / Template Files with release
      dates) and a revision history table; a footer on every page with the
      company name at the left margin, Document Name and Revision in the
      centre and the page number at the right; and, if the settings switch it
      on, a slim header on every page but the cover.
      Default --settings: context/templates/document-settings.md
      Default --out:      context/templates/document-template.docx

  inspect [--template PATH]
      Report which fields a template carries. Use it on a company's own
      controlled template before relying on it.

  render --in FILE.md --out FILE.docx --title NAME [--template PATH]
         [--settings PATH] [--set KEY=VALUE ...] [--remove-input] [--force]
      Pour a Markdown draft into the template. --title fills Document Name.
      Document Number, Revision and Related documents stay as bracketed
      placeholders unless the settings or --set give them. The draft's own # title is
      dropped, since the cover carries it, and whatever sits between that title
      and the first ## heading goes on the cover. A table of six or more
      columns is laid out landscape, and a ## heading starting "Appendix"
      starts a new page.

  read FILE.docx
      Print a Word document as text, for a skill to read. Tracked changes are
      shown as if accepted, and counted at the top so the reader knows.

Document settings are a short Markdown file of "Key: value" lines, written by
the setup skill. Every document is built from them, which is what keeps a
company's documents alike. Keys, with their defaults:

  Company:          (required)
  Logo:             path to a PNG or JPEG, or blank for the company name
  Template:         MOS, or Company when the company supplies its own
  Font:             Calibri
  Body size:        10.5  (points; everything else scales with it)
  Page size:        Letter, or A4
  Date format:      M/D/YYYY, YYYY-MM-DD, or DD-Mon-YYYY
  Document number:  [Document Number]  (the placeholder until one is assigned)
  First revision:   [Rev]
  Header:           Off, or On

The template's body is the cover page: render keeps it and starts the document
on the next page. A company's own template works the same way, provided its
cover and footer carry the tokens {{document_name}}, {{document_number}},
{{revision}} and {{related_documents}}. Tokens it lacks are reported, not
invented. Two more are optional: {{date}}, today's date, and a paragraph
holding {{front_matter}}, which marks where the draft's opening lines go.
"""

import argparse
import datetime
import io
import os
import re
import struct
import sys
import zipfile
import xml.etree.ElementTree as ET
from xml.sax.saxutils import escape

VERSION = '0.2.0'  # a shared contract: a change in behaviour is a new MOS release

DEFAULT_TEMPLATE = os.path.join('context', 'templates', 'document-template.docx')
DEFAULT_SETTINGS = os.path.join('context', 'templates', 'document-settings.md')

SETTINGS = {
    'company': '',
    'logo': '',
    'template': 'MOS',
    'font': 'Calibri',
    'body size': '10.5',
    'page size': 'Letter',
    'date format': 'M/D/YYYY',
    'document number': '[Document Number]',
    'first revision': '[Rev]',
    'header': 'Off',
}
PAGE_SIZES = {'letter': (12240, 15840), 'a4': (11906, 16838)}
MONTHS = 'Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec'.split()
DATE_FORMATS = {
    'm/d/yyyy': lambda d: '%d/%d/%d' % (d.month, d.day, d.year),
    'yyyy-mm-dd': lambda d: d.isoformat(),
    'dd-mon-yyyy': lambda d: '%02d-%s-%d' % (d.day, MONTHS[d.month - 1], d.year),
}


def load_settings(path):
    """Settings from a document-settings file, over the defaults. Only known keys are
    read, so the file can carry explanation around them. A missing file gives the
    defaults. Bad values are refused here, not discovered in a finished document."""
    out = dict(SETTINGS)
    if path and os.path.exists(path):
        with open(path, encoding='utf-8') as f:
            for line in f:
                m = re.match(r'^\s*[-*]?\s*([A-Za-z][A-Za-z ]*?)\s*:\s*(.*?)\s*$', line)
                if m and m.group(1).lower() in SETTINGS:
                    out[m.group(1).lower()] = m.group(2).strip('`').strip()
    if out['page size'].lower() not in PAGE_SIZES:
        raise MosDocxError('Page size must be Letter or A4, not "%s"' % out['page size'])
    if out['date format'].lower() not in DATE_FORMATS:
        raise MosDocxError('Date format must be M/D/YYYY, YYYY-MM-DD or DD-Mon-YYYY, not "%s"'
                           % out['date format'])
    try:
        size = float(out['body size'])
    except ValueError:
        size = 0
    if not 7 <= size <= 16:
        raise MosDocxError('Body size must be a number of points between 7 and 16, not "%s"'
                           % out['body size'])
    if out['header'].lower() not in ('on', 'off'):
        raise MosDocxError('Header must be On or Off, not "%s"' % out['header'])
    if out['template'].lower() not in ('mos', 'company'):
        raise MosDocxError('Template must be MOS or Company, not "%s"' % out['template'])
    return out


def configure(settings):
    """Set page geometry from the settings."""
    global PAGE_W, PAGE_H, TEXT_W
    PAGE_W, PAGE_H = PAGE_SIZES[settings['page size'].lower()]
    TEXT_W = PAGE_W - 2 * MARGIN


def format_date(settings, day=None):
    return DATE_FORMATS[settings['date format'].lower()](day or datetime.date.today())

TOKENS = {
    'document_name': '[Document Name]',
    'document_number': '[Document Number]',
    'revision': '[Rev]',
    'related_documents': '[Related SOPs / template files and their release dates]',
    'date': '',  # filled at render time
}
REQUIRED_TOKENS = ('document_name', 'document_number', 'revision', 'related_documents')

NS = {
    'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main',
    'r': 'http://schemas.openxmlformats.org/officeDocument/2006/relationships',
    'wp': 'http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing',
    'a': 'http://schemas.openxmlformats.org/drawingml/2006/main',
    'pic': 'http://schemas.openxmlformats.org/drawingml/2006/picture',
}
XMLNS = ' '.join('xmlns:%s="%s"' % kv for kv in NS.items())
W = '{%s}' % NS['w']

# Page geometry, in twentieths of a point. US Letter, one-inch margins.
PAGE_W, PAGE_H, MARGIN = 12240, 15840, 1440
TEXT_W = PAGE_W - 2 * MARGIN
WIDE_TABLE = 6  # columns at which a chapter turns landscape


class MosDocxError(Exception):
    pass


# ---- images -----------------------------------------------------------------

def image_size(data):
    """(width, height, extension) of a PNG or JPEG, from its header bytes."""
    if data[:8] == b'\x89PNG\r\n\x1a\n':
        w, h = struct.unpack('>II', data[16:24])
        return w, h, 'png'
    if data[:2] == b'\xff\xd8':
        i = 2
        while i < len(data) - 9:
            if data[i] != 0xFF:
                i += 1
                continue
            marker = data[i + 1]
            if 0xC0 <= marker <= 0xCF and marker not in (0xC4, 0xC8, 0xCC):
                h, w = struct.unpack('>HH', data[i + 5:i + 9])
                return w, h, 'jpeg'
            i += 2 + struct.unpack('>H', data[i + 2:i + 4])[0]
    raise MosDocxError('the logo must be a PNG or JPEG file')


# ---- template parts ---------------------------------------------------------

CONTENT_TYPES = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
<Default Extension="xml" ContentType="application/xml"/>
<Default Extension="png" ContentType="image/png"/>
<Default Extension="jpeg" ContentType="image/jpeg"/>
<Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>
<Override PartName="/word/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.styles+xml"/>
<Override PartName="/word/settings.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.settings+xml"/>
<Override PartName="/word/footer1.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.footer+xml"/>
%s</Types>'''

ROOT_RELS = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/>
</Relationships>'''

DOC_RELS = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>
<Relationship Id="rId2" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/settings" Target="settings.xml"/>
<Relationship Id="rId4" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/footer" Target="footer1.xml"/>
%s</Relationships>'''

SETTINGS_XML = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:settings %s>
<w:defaultTabStop w:val="720"/>
<w:compat><w:compatSetting w:name="compatibilityMode" w:uri="http://schemas.microsoft.com/office/word" w:val="15"/></w:compat>
</w:settings>''' % XMLNS

def base_sect(header):
    """Section properties. With a header, the cover page (the first page of the first
    section) gets an empty header and the ordinary footer; later sections drop that
    first-page treatment in section_props()."""
    refs = '<w:footerReference w:type="default" r:id="rId4"/>'
    tail = ''
    if header:
        refs = ('<w:headerReference w:type="default" r:id="rId3"/><w:headerReference w:type="first" r:id="rId5"/>'
                + refs + '<w:footerReference w:type="first" r:id="rId6"/>')
        tail = '<w:titlePg/>'
    return ('<w:sectPr>%s<w:pgSz w:w="%d" w:h="%d"/>'
            '<w:pgMar w:top="%d" w:right="%d" w:bottom="%d" w:left="%d" w:header="576" w:footer="576" w:gutter="0"/>'
            '%s</w:sectPr>' % (refs, PAGE_W, PAGE_H, MARGIN, MARGIN, MARGIN, MARGIN, tail))


# Styles every rendered body uses. Kept as separate definitions so they can be
# added to a company's own template when it lacks them.
STYLE_DEFS = {
    'Normal': '<w:style w:type="paragraph" w:default="1" w:styleId="Normal"><w:name w:val="Normal"/><w:qFormat/>'
              '<w:pPr><w:spacing w:after="120" w:line="264" w:lineRule="auto"/></w:pPr></w:style>',
    'Title': '<w:style w:type="paragraph" w:styleId="Title"><w:name w:val="Title"/><w:basedOn w:val="Normal"/>'
             '<w:next w:val="Normal"/><w:qFormat/><w:pPr><w:spacing w:before="0" w:after="240"/></w:pPr>'
             '<w:rPr><w:b/><w:sz w:val="36"/></w:rPr></w:style>',
    'Heading1': '<w:style w:type="paragraph" w:styleId="Heading1"><w:name w:val="heading 1"/><w:basedOn w:val="Normal"/>'
                '<w:next w:val="Normal"/><w:qFormat/><w:pPr><w:keepNext/><w:spacing w:before="360" w:after="120"/>'
                '<w:outlineLvl w:val="0"/></w:pPr><w:rPr><w:b/><w:sz w:val="28"/></w:rPr></w:style>',
    'Heading2': '<w:style w:type="paragraph" w:styleId="Heading2"><w:name w:val="heading 2"/><w:basedOn w:val="Normal"/>'
                '<w:next w:val="Normal"/><w:qFormat/><w:pPr><w:keepNext/><w:spacing w:before="240" w:after="80"/>'
                '<w:outlineLvl w:val="1"/></w:pPr><w:rPr><w:b/><w:sz w:val="24"/></w:rPr></w:style>',
    'Heading3': '<w:style w:type="paragraph" w:styleId="Heading3"><w:name w:val="heading 3"/><w:basedOn w:val="Normal"/>'
                '<w:next w:val="Normal"/><w:qFormat/><w:pPr><w:keepNext/><w:spacing w:before="200" w:after="60"/>'
                '<w:outlineLvl w:val="2"/></w:pPr><w:rPr><w:b/><w:i/><w:sz w:val="22"/></w:rPr></w:style>',
    'MOSBullet': '<w:style w:type="paragraph" w:customStyle="1" w:styleId="MOSBullet"><w:name w:val="MOS Bullet"/>'
                 '<w:basedOn w:val="Normal"/><w:pPr><w:tabs><w:tab w:val="left" w:pos="360"/></w:tabs>'
                 '<w:spacing w:after="60"/><w:ind w:left="360" w:hanging="360"/></w:pPr></w:style>',
    'MOSBullet2': '<w:style w:type="paragraph" w:customStyle="1" w:styleId="MOSBullet2"><w:name w:val="MOS Bullet 2"/>'
                  '<w:basedOn w:val="Normal"/><w:pPr><w:tabs><w:tab w:val="left" w:pos="720"/></w:tabs>'
                  '<w:spacing w:after="60"/><w:ind w:left="720" w:hanging="360"/></w:pPr></w:style>',
    'MOSQuote': '<w:style w:type="paragraph" w:customStyle="1" w:styleId="MOSQuote"><w:name w:val="MOS Quote"/>'
                '<w:basedOn w:val="Normal"/><w:pPr><w:pBdr><w:left w:val="single" w:sz="12" w:space="8" w:color="A6A6A6"/></w:pBdr>'
                '<w:ind w:left="360"/></w:pPr><w:rPr><w:color w:val="404040"/></w:rPr></w:style>',
    'MOSCode': '<w:style w:type="paragraph" w:customStyle="1" w:styleId="MOSCode"><w:name w:val="MOS Code"/>'
               '<w:basedOn w:val="Normal"/><w:pPr><w:spacing w:after="0"/><w:ind w:left="360"/></w:pPr>'
               '<w:rPr><w:rFonts w:ascii="Consolas" w:hAnsi="Consolas"/><w:sz w:val="18"/></w:rPr></w:style>',
    'MOSTableText': '<w:style w:type="paragraph" w:customStyle="1" w:styleId="MOSTableText"><w:name w:val="MOS Table Text"/>'
                    '<w:basedOn w:val="Normal"/><w:pPr><w:spacing w:before="20" w:after="20" w:line="240" w:lineRule="auto"/></w:pPr>'
                    '<w:rPr><w:sz w:val="18"/></w:rPr></w:style>',
    'MOSRule': '<w:style w:type="paragraph" w:customStyle="1" w:styleId="MOSRule"><w:name w:val="MOS Rule"/>'
               '<w:basedOn w:val="Normal"/><w:pPr><w:pBdr><w:bottom w:val="single" w:sz="4" w:space="1" w:color="BFBFBF"/></w:pBdr>'
               '<w:spacing w:after="240"/></w:pPr><w:rPr><w:sz w:val="8"/></w:rPr></w:style>',
    'MOSFooter': '<w:style w:type="paragraph" w:customStyle="1" w:styleId="MOSFooter"><w:name w:val="MOS Footer"/>'
                 '<w:basedOn w:val="Normal"/><w:pPr><w:pBdr><w:top w:val="single" w:sz="4" w:space="4" w:color="A6A6A6"/>'
                 '</w:pBdr><w:spacing w:after="0"/></w:pPr><w:rPr><w:sz w:val="17"/><w:szCs w:val="17"/></w:rPr></w:style>',
    'MOSHeader': '<w:style w:type="paragraph" w:customStyle="1" w:styleId="MOSHeader"><w:name w:val="MOS Header"/>'
                 '<w:basedOn w:val="Normal"/><w:pPr><w:pBdr><w:bottom w:val="single" w:sz="4" w:space="4" w:color="A6A6A6"/>'
                 '</w:pBdr><w:spacing w:after="0"/></w:pPr><w:rPr><w:sz w:val="17"/><w:szCs w:val="17"/></w:rPr></w:style>',
    'MOSTable': '<w:style w:type="table" w:customStyle="1" w:styleId="MOSTable"><w:name w:val="MOS Table"/>'
                '<w:tblPr><w:tblBorders>' +
                ''.join('<w:%s w:val="single" w:sz="4" w:space="0" w:color="A6A6A6"/>' % s
                        for s in ('top', 'left', 'bottom', 'right', 'insideH', 'insideV')) +
                '</w:tblBorders><w:tblCellMar><w:top w:w="40" w:type="dxa"/><w:left w:w="80" w:type="dxa"/>'
                '<w:bottom w:w="40" w:type="dxa"/><w:right w:w="80" w:type="dxa"/></w:tblCellMar></w:tblPr></w:style>',
}

def scale_sizes(xml, factor):
    """Scale every font size in a piece of XML. Sizes are written for a 10.5 pt body."""
    if factor == 1:
        return xml
    return re.sub(r'<w:(sz|szCs) w:val="(\d+)"/>',
                  lambda m: '<w:%s w:val="%d"/>' % (m.group(1), max(2, round(int(m.group(2)) * factor))), xml)


def styles_xml(font, body_pt):
    body = round(body_pt * 2)
    return scale_sizes(
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n<w:styles %s>\n'
        '<w:docDefaults><w:rPrDefault><w:rPr><w:rFonts w:ascii="%s" w:hAnsi="%s" w:eastAsia="%s" w:cs="%s"/>'
        '<w:sz w:val="21"/><w:szCs w:val="21"/><w:lang w:val="en-US"/></w:rPr></w:rPrDefault>'
        '<w:pPrDefault><w:pPr><w:spacing w:after="120"/></w:pPr></w:pPrDefault></w:docDefaults>\n%s\n</w:styles>'
        % (XMLNS, escape(font), escape(font), escape(font), escape(font), '\n'.join(STYLE_DEFS.values())),
        body / 21)


def _cell(content, width, shade=False, vmerge=None, valign='center'):
    props = '<w:tcW w:w="%d" w:type="dxa"/>' % width
    if vmerge == 'restart':
        props += '<w:vMerge w:val="restart"/>'
    elif vmerge == 'continue':
        props += '<w:vMerge/>'
    if shade:
        props += '<w:shd w:val="clear" w:color="auto" w:fill="F2F2F2"/>'
    props += '<w:vAlign w:val="%s"/>' % valign
    return '<w:tc><w:tcPr>%s</w:tcPr>%s</w:tc>' % (props, content)


def _small(text, bold=False):
    rpr = '<w:rPr>%s<w:sz w:val="20"/></w:rPr>' % ('<w:b/>' if bold else '')
    return ('<w:p><w:pPr><w:spacing w:before="20" w:after="20"/></w:pPr>'
            '<w:r>%s<w:t xml:space="preserve">%s</w:t></w:r></w:p>' % (rpr, escape(text)))


def cover_xml(company, logo):
    """The cover page: logo top left, the document's title, and the control table.
    `logo` is (width_px, height_px) or None, in which case the company name stands in."""
    if logo:
        mark = '<w:p><w:pPr><w:spacing w:after="0"/></w:pPr>%s</w:p>' % logo_xml(logo, 2.0, 1.0, 1)
    else:
        mark = ('<w:p><w:pPr><w:spacing w:after="0"/></w:pPr><w:r><w:rPr><w:b/><w:sz w:val="28"/></w:rPr>'
                '<w:t xml:space="preserve">%s</w:t></w:r></w:p>' % escape(company))
    title = ('<w:p><w:pPr><w:pStyle w:val="Title"/><w:spacing w:before="2400" w:after="480"/></w:pPr>'
             '<w:r><w:t xml:space="preserve">{{document_name}}</w:t></w:r></w:p>')
    widths = (3000, TEXT_W - 3000)
    rows = [
        ('Document Name', '{{document_name}}'),
        ('Document Number', '{{document_number}}'),
        ('Revision', '{{revision}}'),
        ('Related SOPs / Template Files (Release Date)', '{{related_documents}}'),
    ]
    body = ''.join('<w:tr><w:trPr><w:cantSplit/></w:trPr>%s%s</w:tr>' % (
        _cell(_small(label, True), widths[0], shade=True), _cell(_small(token), widths[1]))
        for label, token in rows)
    borders = ''.join('<w:%s w:val="single" w:sz="4" w:space="0" w:color="808080"/>' % side
                      for side in ('top', 'left', 'bottom', 'right', 'insideH', 'insideV'))
    table = (
        '<w:tbl><w:tblPr><w:tblW w:w="%d" w:type="dxa"/><w:tblBorders>%s</w:tblBorders>'
        '<w:tblLayout w:type="fixed"/><w:tblCellMar><w:top w:w="60" w:type="dxa"/><w:left w:w="100" w:type="dxa"/>'
        '<w:bottom w:w="60" w:type="dxa"/><w:right w:w="100" w:type="dxa"/></w:tblCellMar></w:tblPr>'
        '<w:tblGrid>%s</w:tblGrid>%s</w:tbl>'
        % (TEXT_W, borders, ''.join('<w:gridCol w:w="%d"/>' % w for w in widths), body)
    )
    front = '<w:p><w:r><w:t>{{front_matter}}</w:t></w:r></w:p>'
    return mark + title + table + '<w:p/>' + front + '<w:p/>' + revision_table_xml()


def revision_table_xml():
    """Revision history: the first row records this document; the second is left for the next."""
    widths = (2160, 5490, TEXT_W - 2160 - 5490)
    borders = ''.join('<w:%s w:val="single" w:sz="4" w:space="0" w:color="808080"/>' % side
                      for side in ('top', 'left', 'bottom', 'right', 'insideH', 'insideV'))
    row = lambda cells, head=False: '<w:tr><w:trPr><w:cantSplit/></w:trPr>%s</w:tr>' % ''.join(
        _cell(_small(c, head) if c else '<w:p/>', w, shade=head, valign='top') for c, w in zip(cells, widths))
    return (
        '<w:tbl><w:tblPr><w:tblW w:w="%d" w:type="dxa"/><w:tblBorders>%s</w:tblBorders>'
        '<w:tblLayout w:type="fixed"/><w:tblCellMar><w:top w:w="60" w:type="dxa"/><w:left w:w="100" w:type="dxa"/>'
        '<w:bottom w:w="60" w:type="dxa"/><w:right w:w="100" w:type="dxa"/></w:tblCellMar></w:tblPr>'
        '<w:tblGrid>%s</w:tblGrid>%s%s%s</w:tbl>'
        % (TEXT_W, borders, ''.join('<w:gridCol w:w="%d"/>' % w for w in widths),
           row(('Revision Number', 'Summary of Changes', 'Date'), True),
           row(('{{revision}}', 'Original', '{{date}}')), row(('', '', '')))
    )


def logo_xml(logo, max_w_in, max_h_in, pic_id):
    """An inline picture of the logo, fitted inside a box, keeping its proportions."""
    scale = min(max_w_in * 914400 / logo[0], max_h_in * 914400 / logo[1])
    cx, cy = int(logo[0] * scale), int(logo[1] * scale)
    return (
        '<w:r><w:drawing><wp:inline distT="0" distB="0" distL="0" distR="0"><wp:extent cx="%d" cy="%d"/>'
        '<wp:docPr id="%d" name="Logo"/><wp:cNvGraphicFramePr><a:graphicFrameLocks noChangeAspect="1"/>'
        '</wp:cNvGraphicFramePr><a:graphic><a:graphicData uri="http://schemas.openxmlformats.org/drawingml/2006/picture">'
        '<pic:pic><pic:nvPicPr><pic:cNvPr id="0" name="Logo"/><pic:cNvPicPr/></pic:nvPicPr>'
        '<pic:blipFill><a:blip r:embed="rIdLogo"/><a:stretch><a:fillRect/></a:stretch></pic:blipFill>'
        '<pic:spPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="%d" cy="%d"/></a:xfrm>'
        '<a:prstGeom prst="rect"><a:avLst/></a:prstGeom></pic:spPr></pic:pic></a:graphicData></a:graphic>'
        '</wp:inline></w:drawing></w:r>' % (cx, cy, pic_id, cx, cy)
    )


def header_xml(company, logo):
    """The optional slim header: logo (or company name) at the left margin, document
    number and revision at the right."""
    left = logo_xml(logo, 1.2, 0.35, 2) if logo else '<w:r><w:t xml:space="preserve">%s</w:t></w:r>' % escape(company)
    return (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?><w:hdr %s><w:p>'
        '<w:pPr><w:pStyle w:val="MOSHeader"/></w:pPr>%s'
        '<w:r><w:ptab w:relativeTo="margin" w:alignment="right" w:leader="none"/></w:r>'
        '<w:r><w:t xml:space="preserve">{{document_number}}  \u00b7  Rev. {{revision}}</w:t></w:r></w:p></w:hdr>'
        % (XMLNS, left)
    )


EMPTY_HEADER = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?><w:hdr %s><w:p><w:pPr>'
                '<w:spacing w:after="0"/></w:pPr></w:p></w:hdr>' % XMLNS)


def footer_xml(company):
    """Three parts on one line: company at the left margin, document name and revision
    centred, page number at the right margin. Positional tabs measure from the margins,
    so the parts hold their places on portrait and landscape pages alike. The size comes
    from the MOSFooter style, not from the runs, because Word rebuilds the page-number
    fields when it lays out the page and the rebuilt text takes the paragraph's size."""
    run = lambda text: '<w:r><w:t xml:space="preserve">%s</w:t></w:r>' % escape(text)
    ptab = lambda where: '<w:r><w:ptab w:relativeTo="margin" w:alignment="%s" w:leader="none"/></w:r>' % where
    field = lambda instr: '<w:fldSimple w:instr=" %s "><w:r><w:t>1</w:t></w:r></w:fldSimple>' % instr
    return (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?><w:ftr %s><w:p>'
        '<w:pPr><w:pStyle w:val="MOSFooter"/></w:pPr>'
        '%s%s%s%s%s%s%s%s</w:p></w:ftr>'
        % (XMLNS, run(company), ptab('center'), run('{{document_name}}  ·  Rev. {{revision}}'),
           ptab('right'), run('Page '), field('PAGE'), run(' of '), field('NUMPAGES'))
    )


def build_template(settings, logo_bytes=None):
    """A complete template .docx, as bytes, built from document settings."""
    configure(settings)
    company = settings['company']
    header = settings['header'].lower() == 'on'
    factor = float(settings['body size']) / 10.5
    logo = ext = None
    if logo_bytes:
        w, h, ext = image_size(logo_bytes)
        logo = (w, h)
    document = scale_sizes('<?xml version="1.0" encoding="UTF-8" standalone="yes"?><w:document %s><w:body>'
                           '%s%s</w:body></w:document>' % (XMLNS, cover_xml(company, logo), base_sect(header)),
                           factor)
    image_rel = ('<Relationship Id="rIdLogo" Type="http://schemas.openxmlformats.org/officeDocument/2006/'
                 'relationships/image" Target="media/logo.%s"/>\n' % ext) if logo else ''
    rel = lambda rid, kind, target: ('<Relationship Id="%s" Type="http://schemas.openxmlformats.org/officeDocument/'
                                     '2006/relationships/%s" Target="%s"/>\n' % (rid, kind, target))
    part = lambda name, kind: ('<Override PartName="/word/%s" ContentType="application/vnd.openxmlformats-'
                               'officedocument.wordprocessingml.%s+xml"/>\n' % (name, kind))
    extra_rels = image_rel
    extra_types = ''
    if header:
        extra_rels += (rel('rId3', 'header', 'header1.xml') + rel('rId5', 'header', 'header2.xml')
                       + rel('rId6', 'footer', 'footer2.xml'))
        extra_types = part('header1.xml', 'header') + part('header2.xml', 'header') + part('footer2.xml', 'footer')
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, 'w', zipfile.ZIP_DEFLATED) as z:
        z.writestr('[Content_Types].xml', CONTENT_TYPES % extra_types)
        z.writestr('_rels/.rels', ROOT_RELS)
        z.writestr('word/document.xml', document)
        z.writestr('word/_rels/document.xml.rels', DOC_RELS % extra_rels)
        z.writestr('word/styles.xml', styles_xml(settings['font'], float(settings['body size'])))
        z.writestr('word/settings.xml', SETTINGS_XML)
        z.writestr('word/footer1.xml', footer_xml(company))
        if header:
            z.writestr('word/footer2.xml', footer_xml(company))
            z.writestr('word/header1.xml', header_xml(company, logo))
            z.writestr('word/header2.xml', EMPTY_HEADER)
            if logo:
                z.writestr('word/_rels/header1.xml.rels',
                           '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
                           '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
                           + image_rel + '</Relationships>')
        if logo:
            z.writestr('word/media/logo.%s' % ext, logo_bytes)
    return buf.getvalue()


# ---- Markdown to WordprocessingML ------------------------------------------

INLINE = re.compile(r'\*\*(.+?)\*\*|`([^`]+)`|(?<![\w*])\*(?!\s)(.+?)(?<!\s)\*(?![\w*])|\[([^\]]+)\]\(([^)]+)\)|<br\s*/?>')
ID_HYPHEN = re.compile(r'(?<=\b[A-Z]{2})-(?=\d)|(?<=\b[A-Z]{3})-(?=\d)|(?<=\b[A-Z]{4})-(?=\d)')
# "Primary users: ..." — up to five words and a colon at the start of a line.
LABEL = re.compile(r"^([A-Z][\w()/'’,.-]*(?: [\w()/'’,.-]+){0,4}:)(?= )")


def runs(text, bold=False, italic=False, mono=False):
    """Inline Markdown to runs: **bold**, *italic*, `code`, [text](url), <br>."""
    out = []
    pos = 0
    for m in INLINE.finditer(text):
        if m.start() > pos:
            out.append(_run(text[pos:m.start()], bold, italic, mono))
        if m.group(1) is not None:
            out.append(runs(m.group(1), True, italic, mono))
        elif m.group(2) is not None:
            out.append(_run(m.group(2), bold, italic, True))
        elif m.group(3) is not None:
            out.append(runs(m.group(3), bold, True, mono))
        elif m.group(4) is not None:
            out.append(runs(m.group(4), bold, italic, mono))
        else:
            out.append('<w:r><w:br/></w:r>')
        pos = m.end()
    if pos < len(text):
        out.append(_run(text[pos:], bold, italic, mono))
    return ''.join(out)


def _run(text, bold, italic, mono):
    if not text:
        return ''
    rpr = ('<w:b/>' if bold else '') + ('<w:i/>' if italic else '')
    if mono:
        rpr = '<w:rFonts w:ascii="Consolas" w:hAnsi="Consolas"/>' + rpr
    text = text.replace('\\|', '|').replace('\\*', '*')
    # IDs such as UN-001 must not break at the hyphen in a narrow column.
    parts = ID_HYPHEN.split(text)
    inner = '<w:noBreakHyphen/>'.join('<w:t xml:space="preserve">%s</w:t>' % escape(p) for p in parts)
    return '<w:r>%s%s</w:r>' % ('<w:rPr>%s</w:rPr>' % rpr if rpr else '', inner)


def _unwrap(text):
    """(text without a surrounding *...*, whether it had one)."""
    if text.startswith('*') and not text.startswith('**'):
        wrapped = text.endswith('*') and not text.endswith('**') and len(text) > 1
        return (text[1:-1] if wrapped else text[1:]), True
    return text, False


def label_para(text):
    """A paragraph, with a leading "Label:" set in bold."""
    inner, italic = _unwrap(text)
    if not (italic and text.endswith('*') and not text.endswith('**')):
        inner, italic = text, False
    m = LABEL.match(inner)
    if not m:
        return para(runs(text))
    return para(_run(m.group(1), True, italic, False) + runs(inner[m.end(1):], False, italic))


def para(inner, style=None, extra_ppr=''):
    ppr = ('<w:pStyle w:val="%s"/>' % style if style else '') + extra_ppr
    return '<w:p>%s%s</w:p>' % ('<w:pPr>%s</w:pPr>' % ppr if ppr else '', inner)


def split_row(line):
    line = line.strip()
    if line.startswith('|'):
        line = line[1:]
    if line.endswith('|') and not line.endswith('\\|'):
        line = line[:-1]
    return [c.strip() for c in re.split(r'(?<!\\)\|', line)]


def column_shares(rows, ncols):
    """Each column's share of the table width, in fiftieths of a percent (5000 = all of it).

    Word's autofit hands a long unbreakable string, such as a URL, the whole table and
    crushes its neighbours until even their headers break mid-word. Instead, every column
    gets room for its longest word, up to a cap, and the rest of the width goes where the
    text is."""
    char = 90                          # twips per character of 9 pt table text, roughly
    pad = 230                          # cell margins
    words, text = [0] * ncols, [0] * ncols
    for row in rows:
        for c, cell in enumerate(row[:ncols]):
            plain = re.sub(r'[*`]', '', cell)
            words[c] = max([words[c]] + [min(len(w), 16) for w in plain.split()])
            text[c] = max(text[c], min(len(plain), 90))
    # Every column needs room for its longest word. Beyond that, a short column (a count, a
    # code, a class) wants its entries on one line, and a prose column wants most of the
    # spare width, so that its rows stay short.
    need = [w * char + pad for w in words]
    want = [max(n, t * char + pad if t <= 24 else t * char / 1.5 + pad)
            for n, t in zip(need, text)]
    room = PAGE_H - 2 * MARGIN if ncols >= WIDE_TABLE else TEXT_W  # wide tables go landscape
    if sum(need) >= room:
        widths = [room * n / sum(need) for n in need]
    else:
        spare = room - sum(need)
        extra = [w - n for w, n in zip(want, need)]
        widths = [n + (spare * e / sum(extra) if sum(extra) else spare / ncols)
                  for n, e in zip(need, extra)]
    shares = [int(5000 * w / sum(widths)) for w in widths]
    shares[-1] += 5000 - sum(shares)
    return shares


def table_xml(rows):
    ncols = max(len(r) for r in rows)
    shares = column_shares(rows, ncols)
    grid = ''.join('<w:gridCol w:w="%d"/>' % (TEXT_W * s // 5000) for s in shares)
    out = []
    for i, row in enumerate(rows):
        row = row + [''] * (ncols - len(row))
        cells = []
        for cell, share in zip(row, shares):
            props = '<w:tcW w:w="%d" w:type="pct"/>' % share
            if i == 0:
                props += '<w:shd w:val="clear" w:color="auto" w:fill="E7E6E6"/>'
            cells.append('<w:tc><w:tcPr>%s</w:tcPr>%s</w:tc>' % (
                props, para(runs(cell, bold=(i == 0)), 'MOSTableText')))
        trpr = '<w:trPr><w:cantSplit/>%s</w:trPr>' % ('<w:tblHeader/>' if i == 0 else '')
        out.append('<w:tr>%s%s</w:tr>' % (trpr, ''.join(cells)))
    return ('<w:tbl><w:tblPr><w:tblStyle w:val="MOSTable"/><w:tblW w:w="5000" w:type="pct"/>'
            '<w:tblLayout w:type="fixed"/><w:tblLook w:val="04A0" w:firstRow="1" w:lastRow="0" '
            'w:firstColumn="0" w:lastColumn="0" w:noHBand="0" w:noVBand="1"/></w:tblPr>'
            '<w:tblGrid>%s</w:tblGrid>%s</w:tbl>' % (grid, ''.join(out)))


def parse_blocks(md):
    """Markdown to a list of (kind, xml, meta). kind is 'heading', 'table' or 'block'."""
    lines = md.replace('\r\n', '\n').split('\n')
    blocks = []
    i = 0
    while i < len(lines):
        line = lines[i]
        s = line.strip()
        if not s:
            i += 1
            continue
        m = re.match(r'^(#{1,6})\s+(.*)$', s)
        if m:
            level = len(m.group(1))
            style = 'Title' if level == 1 else 'Heading%d' % min(level - 1, 3)
            text = m.group(2).strip()
            extra = '<w:pageBreakBefore/>' if level == 2 and text.lower().startswith('appendix') else ''
            blocks.append(('heading', para(runs(text), style, extra), level))
            i += 1
            continue
        if re.match(r'^(-{3,}|\*{3,}|_{3,})$', s):
            blocks.append(('block', para('', 'MOSRule'), None))
            i += 1
            continue
        if s.startswith('```'):
            i += 1
            code = []
            while i < len(lines) and not lines[i].strip().startswith('```'):
                code.append(lines[i])
                i += 1
            i += 1
            blocks.append(('block', ''.join(para(_run(c, False, False, False), 'MOSCode') for c in code), None))
            continue
        if s.startswith('|') and i + 1 < len(lines) and re.match(r'^\s*\|?\s*:?-{2,}', lines[i + 1]):
            rows = [split_row(s)]
            i += 2
            while i < len(lines) and lines[i].strip().startswith('|'):
                rows.append(split_row(lines[i]))
                i += 1
            blocks.append(('table', table_xml(rows), max(len(r) for r in rows)))
            continue
        if s.startswith('>'):
            quote = []
            while i < len(lines) and lines[i].strip().startswith('>'):
                quote.append(lines[i].strip()[1:].strip())
                i += 1
            blocks.append(('block', para(runs(' '.join(q for q in quote if q)), 'MOSQuote'), None))
            continue
        lm = re.match(r'^(\s*)([-*+]|\d+[.)])\s+(.*)$', line)
        if lm:
            items = []
            while i < len(lines):
                lm = re.match(r'^(\s*)([-*+]|\d+[.)])\s+(.*)$', lines[i])
                if lm:
                    items.append([len(lm.group(1).expandtabs(4)), lm.group(2), lm.group(3).strip()])
                elif lines[i].strip() and items and lines[i].startswith(' '):
                    items[-1][2] += ' ' + lines[i].strip()  # wrapped continuation of an item
                else:
                    break
                i += 1
            xml = ''
            for indent, marker, text in items:
                bullet = '•' if marker in '-*+' else marker
                style = 'MOSBullet2' if indent >= 2 else 'MOSBullet'
                xml += para('<w:r><w:t xml:space="preserve">%s</w:t></w:r><w:r><w:tab/></w:r>%s'
                            % (escape(bullet), runs(text)), style)
            blocks.append(('block', xml, None))
            continue
        # A paragraph: consecutive lines, joined. A line shaped like "Label: value"
        # starts a new line in the same paragraph rather than being run in.
        chunk = []
        while i < len(lines) and lines[i].strip() and not re.match(
                r'^(#{1,6}\s|```|>|\||\s*([-*+]|\d+[.)])\s|(-{3,}|\*{3,}|_{3,})\s*$)', lines[i].strip() + ' '):
            chunk.append(lines[i].strip())
            i += 1
        if not chunk:  # a line no rule claims; keep it as text rather than loop
            chunk = [s]
            i += 1
        # A line that opens with a label starts its own paragraph. Lines are joined
        # before inline parsing, so *emphasis* that wraps a line still closes.
        groups = []
        for c in chunk:
            if not groups or LABEL.match(_unwrap(c)[0]):
                groups.append([c])
            else:
                groups[-1].append(c)
        blocks.append(('block', ''.join(label_para(' '.join(g)) for g in groups), None))
    return blocks


def section_props(base, landscape, first=True):
    """base sectPr, turned landscape if asked. Only the first section keeps the
    first-page (cover) header and footer; a later section's first page is an ordinary page."""
    if not first:
        base = re.sub(r'<w:(header|footer)Reference w:type="first"[^>]*/>|<w:titlePg/>', '', base)
    m = re.search(r'<w:pgSz\b[^>]*/>', base)
    if not m or not landscape:
        return base
    w = int(re.search(r'w:w="(\d+)"', m.group(0)).group(1))
    h = int(re.search(r'w:h="(\d+)"', m.group(0)).group(1))
    size = '<w:pgSz w:w="%d" w:h="%d" w:orient="landscape"/>' % (max(w, h), min(w, h))
    return base[:m.start()] + size + base[m.end():]


def body_xml(md, base_sect, cover=''):
    """The cover, then the content from a new page.

    With a cover, the draft's # title is dropped and its opening lines — up to
    the first ## heading — go on the cover, at {{front_matter}}. A wide table is
    laid out landscape from the table itself, or from its heading when at most
    one paragraph sits between them, through to the next ## heading."""
    blocks = parse_blocks(md)
    if cover:
        if blocks and blocks[0][0] == 'heading' and blocks[0][2] == 1:
            blocks = blocks[1:]
        n = next((i for i, b in enumerate(blocks) if b[0] == 'heading' and b[2] <= 2), len(blocks))
        front, blocks = ''.join(b[1] for b in blocks[:n]), blocks[n:]
        slot = re.search(r'<w:p\b(?:(?!<w:p\b).)*?\{\{front_matter\}\}.*?</w:p>', cover, re.S)
        cover = cover[:slot.start()] + front + cover[slot.end():] if slot else cover + front

    wide = [False] * len(blocks)
    for t, b in enumerate(blocks):
        if b[0] == 'table' and b[2] >= WIDE_TABLE:
            # The heading goes with its table when at most one paragraph sits between them.
            first = t
            if t >= 1 and blocks[t - 1][0] == 'heading':
                first = t - 1
            elif t >= 2 and blocks[t - 2][0] == 'heading' and blocks[t - 1][0] == 'block':
                first = t - 2
            last = next((i for i in range(t + 1, len(blocks))
                         if blocks[i][0] == 'heading' and blocks[i][2] <= 2), len(blocks))
            for i in range(first, last):
                wide[i] = True

    out = [cover]
    current = False if cover else None  # the cover is portrait
    sections = 0
    for i, b in enumerate(blocks):
        if current is not None and wide[i] != current:
            out.append('<w:p><w:pPr>%s</w:pPr></w:p>' % section_props(base_sect, current, sections == 0))
            sections += 1
        elif i == 0 and cover:
            out.append('<w:p><w:r><w:br w:type="page"/></w:r></w:p>')
        current = wide[i]
        if i and blocks[i - 1][0] == 'table' and b[0] == 'block':
            out.append('<w:p><w:pPr><w:spacing w:after="0"/></w:pPr></w:p>')  # air after a table
        out.append(b[1])
    return ''.join(out) + section_props(base_sect, bool(current), sections == 0)


# ---- render -----------------------------------------------------------------

def render(md, template_bytes, values):
    """Markdown into the template. Returns (docx bytes, tokens the template lacked)."""
    zin = zipfile.ZipFile(io.BytesIO(template_bytes))
    doc = zin.read('word/document.xml').decode('utf-8')
    sects = re.findall(r'<w:sectPr\b.*?</w:sectPr>', doc, re.S)
    if not sects:
        raise MosDocxError('the template has no section properties; is it a Word document?')
    body_open = re.search(r'<w:body>', doc)
    body_close = doc.rfind('</w:body>')
    cover = doc[body_open.end():doc.rfind('<w:sectPr')].strip()
    new_doc = doc[:body_open.end()] + body_xml(md, sects[-1], cover) + doc[body_close:]

    found = set()
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, 'w', zipfile.ZIP_DEFLATED) as zout:
        for item in zin.infolist():
            data = zin.read(item.filename)
            name = item.filename
            if name == 'word/document.xml':
                data = new_doc.encode('utf-8')
            if name == 'word/styles.xml':
                styles = data.decode('utf-8')
                missing = [d for sid, d in STYLE_DEFS.items() if 'w:styleId="%s"' % sid not in styles]
                if missing:
                    styles = styles.replace('</w:styles>', ''.join(missing) + '</w:styles>')
                data = styles.encode('utf-8')
            if re.match(r'word/(header|footer)\d*\.xml$', name) or name == 'word/document.xml':
                text = data.decode('utf-8')
                for key in TOKENS:
                    token = '{{%s}}' % key
                    if token in text:
                        found.add(key)
                        text = text.replace(token, escape(values.get(key, TOKENS[key])))
                data = text.encode('utf-8')
            zout.writestr(item, data)
    return buf.getvalue(), [k for k in REQUIRED_TOKENS if k not in found]


def inspect(template_bytes):
    """Which fields a template carries, and where."""
    z = zipfile.ZipFile(io.BytesIO(template_bytes))
    where = {}
    for name in z.namelist():
        if name == 'word/document.xml' or re.match(r'word/(header|footer)\d*\.xml$', name):
            text = z.read(name).decode('utf-8')
            for key in list(TOKENS) + ['front_matter']:
                if '{{%s}}' % key in text:
                    where.setdefault(key, []).append(name.split('/')[-1].replace('.xml', ''))
    return where


# ---- read -------------------------------------------------------------------

def _text(el):
    parts = []
    for node in el.iter():
        if node.tag == W + 't':
            parts.append(node.text or '')
        elif node.tag == W + 'noBreakHyphen':
            parts.append('-')
        elif node.tag in (W + 'tab', W + 'ptab'):
            parts.append('\t')
        elif node.tag in (W + 'br', W + 'cr'):
            parts.append('\n')
    return ''.join(parts)


def _block_text(el):
    if el.tag == W + 'p':
        style = el.find('w:pPr/w:pStyle', NS)
        sid = style.get(W + 'val') if style is not None else ''
        text = _text(el).strip()
        m = re.match(r'Heading(\d)', sid or '')
        if m and text:
            return '#' * (int(m.group(1)) + 1) + ' ' + text
        if sid == 'Title' and text:
            return '# ' + text
        return text
    if el.tag == W + 'tbl':
        rows = []
        for tr in el.findall('w:tr', NS):
            cells = [' '.join(_text(tc).split()).replace('|', '\\|') for tc in tr.findall('w:tc', NS)]
            rows.append('| ' + ' | '.join(cells) + ' |')
            if len(rows) == 1:
                rows.append('|' + '---|' * len(cells))
        return '\n'.join(rows)
    return ''


def read(docx_bytes):
    z = zipfile.ZipFile(io.BytesIO(docx_bytes))
    names = z.namelist()
    xml = z.read('word/document.xml')
    root = ET.fromstring(xml)
    ins = len(root.findall('.//w:ins', NS))
    dels = len(root.findall('.//w:del', NS))
    comments = 0
    if 'word/comments.xml' in names:
        comments = len(ET.fromstring(z.read('word/comments.xml')).findall('w:comment', NS))
    out = []
    if ins or dels:
        out.append('> Tracked changes: %d insertions, %d deletions, not accepted in the file. '
                   'Shown here as if accepted.' % (ins, dels))
    if comments:
        out.append('> Review comments: %d. Not shown.' % comments)
    for name in sorted(n for n in names if re.match(r'word/header\d*\.xml$', n)):
        htext = [_block_text(el) for el in ET.fromstring(z.read(name))]
        htext = [t for t in htext if t.strip()]
        if htext:
            out.append('Header:\n' + '\n'.join(htext))
    body = root.find('w:body', NS)
    for el in body:
        t = _block_text(el)
        if t.strip():
            out.append(t)
    return '\n\n'.join(out) + '\n'


# ---- command line -----------------------------------------------------------

def _write(path, data, force):
    if os.path.exists(path) and not force:
        raise MosDocxError('%s already exists. Not overwritten.' % path)
    folder = os.path.dirname(path)
    if folder:
        os.makedirs(folder, exist_ok=True)
    with open(path, 'wb') as f:
        f.write(data)


def main(argv=None):
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')
    p = argparse.ArgumentParser(prog='mosdocx', description='Word documents for MOS skills.')
    sub = p.add_subparsers(dest='cmd', required=True)
    sub.add_parser('check')
    t = sub.add_parser('template')
    t.add_argument('--settings', default=DEFAULT_SETTINGS)
    t.add_argument('--out', default=DEFAULT_TEMPLATE)
    t.add_argument('--force', action='store_true')
    i = sub.add_parser('inspect')
    i.add_argument('--template', default=DEFAULT_TEMPLATE)
    r = sub.add_parser('render')
    r.add_argument('--in', dest='src', required=True)
    r.add_argument('--out', required=True)
    r.add_argument('--title', required=True)
    r.add_argument('--template', default=DEFAULT_TEMPLATE)
    r.add_argument('--settings', default=DEFAULT_SETTINGS)
    r.add_argument('--set', action='append', default=[], metavar='KEY=VALUE')
    r.add_argument('--remove-input', action='store_true')
    r.add_argument('--force', action='store_true')
    rd = sub.add_parser('read')
    rd.add_argument('file')
    a = p.parse_args(argv)

    try:
        if a.cmd == 'check':
            tpl = build_template(dict(SETTINGS, company='Check', header='On'))
            doc, _ = render('# Check\n\n| a | b |\n|---|---|\n| 1 | 2 |\n', tpl, {'document_name': 'Check'})
            assert '| 1 | 2 |' in read(doc)
            print('mosdocx %s ok: Python %d.%d can write and read Word documents.'
                  % ((VERSION,) + sys.version_info[:2]))
        elif a.cmd == 'template':
            if not os.path.exists(a.settings):
                raise MosDocxError('no document settings at %s. The setup skill writes them.' % a.settings)
            settings = load_settings(a.settings)
            if not settings['company']:
                raise MosDocxError('the document settings have no Company.')
            if settings['template'].lower() == 'company':
                raise MosDocxError('the settings say this company uses its own template. Not overwritten.')
            logo = None
            if settings['logo']:
                with open(settings['logo'], 'rb') as f:
                    logo = f.read()
            _write(a.out, build_template(settings, logo), a.force)
            print('Template written: %s%s' % (a.out, '' if logo else ' (no logo; company name in its place)'))
        elif a.cmd == 'inspect':
            with open(a.template, 'rb') as f:
                where = inspect(f.read())
            for key in REQUIRED_TOKENS + ('date', 'front_matter'):
                need = 'required' if key in REQUIRED_TOKENS else 'optional'
                print('%-18s %-9s %s' % (key, need, ', '.join(where[key]) if key in where else 'MISSING'))
        elif a.cmd == 'render':
            with open(a.src, encoding='utf-8') as f:
                md = f.read()
            settings = load_settings(a.settings)
            configure(settings)
            note = ''
            if os.path.exists(a.template):
                with open(a.template, 'rb') as f:
                    tpl = f.read()
                if (settings['template'].lower() == 'mos' and os.path.exists(a.settings)
                        and os.path.getmtime(a.settings) > os.path.getmtime(a.template)):
                    note = (' The document settings changed after the template was built; rebuild it '
                            '(template --force) so the next document follows them.')
            else:
                tpl = build_template(dict(settings, company=settings['company'] or ''))
                note = ' No company template at %s; used a plain one. Run setup to make one.' % a.template
            values = {'document_name': a.title, 'date': format_date(settings),
                      'document_number': settings['document number'], 'revision': settings['first revision']}
            for kv in a.set:
                key, _, value = kv.partition('=')
                if key not in TOKENS:
                    raise MosDocxError('unknown field "%s". Known: %s' % (key, ', '.join(TOKENS)))
                values[key] = value
            doc, missing = render(md, tpl, values)
            _write(a.out, doc, a.force)
            if a.remove_input:
                os.remove(a.src)
            print('Written: %s.%s' % (a.out, note))
            if missing and os.path.exists(a.template):
                print('The template has no place for: %s. Those fields are not in the document.'
                      % ', '.join(missing))
        elif a.cmd == 'read':
            with open(a.file, 'rb') as f:
                sys.stdout.write(read(f.read()))
    except (MosDocxError, OSError, zipfile.BadZipFile, KeyError) as e:
        print('mosdocx: %s' % e, file=sys.stderr)
        return 1
    return 0


if __name__ == '__main__':
    sys.exit(main())
