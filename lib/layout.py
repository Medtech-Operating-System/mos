#!/usr/bin/env python3
"""layout — bring a company folder up to the current MOS layout.

Before MOS 0.3, skills wrote drafts to a separate outputs/ folder, organized by
the same eight domains as context/, and a person promoted a draft by moving it
into context/. Drafts now live in context/<domain>/ beside the records they
would revise, and the filename says which is which: product-code_draft.docx is
unreviewed, product-code_revA.docx is a record, product-code_revB_draft.docx is
a proposed next revision. This script moves an existing outputs/ folder into
that layout. It needs Python 3.8 or later and nothing else: no packages, no
network.

Commands:

  check [--root DIR]
      Show what apply would do, and write nothing. The first line says
      whether there is anything to do.

  apply [--root DIR] [--delete PATH ...] [--move PATH ...]
      Make the moves check showed, and add the local domain folders the moves
      need to the context map. Files check lists as left over stay where they
      are unless named: --delete removes one, --move moves it to the place
      check suggested. outputs/ is removed once it is empty, and kept if
      anything is left in it.

What it decides, for each file under outputs/<domain>/ (and outputs/user-needs/,
where MOS 0.1 put user needs):

  <doc>_draft.docx    moves to context/<domain>/. Where a record of the same
                      document is there, it becomes <doc>_rev<next>_draft.docx;
                      where the record is newer than the draft, the draft was
                      superseded and goes to context/<domain>/archive/.
  <doc>.md            with no Word draft beside it, the draft written where
  <doc>.source.md     Python was missing or the render never ran: moves as
                      <doc>_draft.md, by the same rules.
  subfolders          FDA summaries, guidance, CMS files: move as they are, to
                      the same place under context/<domain>/.
  other files         move as they are.
  <doc>_revA.docx     a record someone saved in outputs/: moves to
                      context/<domain>/ as it is, and drafts beside it are named
                      for the revision after it.
  ~$<doc>.docx        Word's lock file: that document is open. Nothing moves
                      until it is closed.
  left over           a render input (.source.md) beside its Word draft, a Markdown copy beside its
                      Word draft, a Word file not named <doc>_draft.docx, a file
                      outside the eight domains, or a name already taken in
                      context/. Listed, never touched without --delete or --move.

Paths printed are relative to the root, with forward slashes, so a skill can
pass them back to --delete and --move as printed.
"""

import argparse
import filecmp
import os
import re
import sys

VERSION = '0.1.2'

DOMAINS = ('product', 'users-and-needs', 'risk', 'design', 'manufacturing',
           'clinical', 'regulatory', 'commercial')
LEGACY = {'user-needs': 'users-and-needs'}  # MOS 0.1 named the folder for the skill, not the domain
MAP = os.path.join('context', 'context-map.md')
REV = re.compile(r'^(?P<base>.+)_rev(?P<rev>[A-Za-z]+|\d+)\.(docx|md)$')


class LayoutError(Exception):
    pass


def rel(path, root):
    return os.path.relpath(path, root).replace(os.sep, '/')


def rev_key(rev):
    return (0, int(rev), '') if rev.isdigit() else (1, len(rev), rev.upper())


def next_rev(rev):
    if rev.isdigit():
        return str(int(rev) + 1)
    letters = [ord(c) - 65 for c in rev.upper()]
    i = len(letters) - 1
    while i >= 0:
        if letters[i] < 25:
            letters[i] += 1
            return ''.join(chr(n + 65) for n in letters)
        letters[i] = 0
        i -= 1
    return 'A' + ''.join(chr(n + 65) for n in letters)


def newest_record(folders, base):
    """The highest revision of <base> in any of folders, outside archive/: (rev, path), or None."""
    best = None
    for folder in folders:
        if not os.path.isdir(folder):
            continue
        for name in os.listdir(folder):
            m = REV.match(name)
            if m and m.group('base') == base and os.path.isfile(os.path.join(folder, name)):
                if best is None or rev_key(m.group('rev')) > rev_key(best[0]):
                    best = (m.group('rev'), os.path.join(folder, name))
    return best


def is_lock(path):
    """Word's owner file, ~$name.docx: the document beside it is open."""
    return os.path.basename(path).startswith('~$')


def plan(root):
    """What apply would do: moves, map lines to add, files left over, and documents open in Word."""
    outputs = os.path.join(root, 'outputs')
    moves, leftovers, domains = [], [], set()
    if not os.path.isdir(outputs):
        return moves, leftovers, [], []
    locks = [p for p in walk(outputs) if is_lock(p)]
    taken = set()

    def leftover(src, why, suggest=None):
        leftovers.append((src, why, suggest))

    def move(src, dst, why, domain):
        if os.path.normcase(dst) in taken:
            leftover(src, 'another file in outputs/ would take the same name, %s' % rel(dst, root))
        elif os.path.exists(dst):
            same = os.path.isfile(dst) and filecmp.cmp(src, dst, shallow=False)
            leftover(src, 'an identical copy is already at %s' % rel(dst, root) if same
                     else 'a different file with this name is already at %s' % rel(dst, root))
        else:
            taken.add(os.path.normcase(dst))
            moves.append((src, dst, why))
            domains.add(domain)

    for folder in sorted(os.listdir(outputs)):
        top = os.path.join(outputs, folder)
        name = LEGACY.get(folder, folder)
        if name not in DOMAINS or not os.path.isdir(top):
            for path in [p for p in walk(top) if not is_lock(p)]:
                leftover(path, 'outside the eight domains',
                         os.path.join(root, 'context', 'inbox', os.path.basename(path)))
            continue
        target = os.path.join(root, 'context', name)
        entries = sorted(os.listdir(top))
        for entry in entries:
            src = os.path.join(top, entry)
            if is_lock(src):
                continue
            if os.path.isdir(src):
                for path in [p for p in walk(src) if not is_lock(p)]:
                    move(path, os.path.join(target, os.path.relpath(path, top)), 'reference material', name)
                continue
            if entry.endswith('.source.md'):
                base = entry[:-len('.source.md')]
                if base + '_draft.docx' in entries:
                    leftover(src, 'the input a render left behind; the Word draft beside it is the document')
                else:
                    # The render never ran, or its Word draft is gone: this is the only copy
                    draft(src, base, '.md', (target, top), name, move)
                continue
            if REV.match(entry):
                move(src, os.path.join(target, entry), 'a record saved in outputs/', name)
            elif entry.endswith('_draft.docx'):
                draft(src, entry[:-len('_draft.docx')], '.docx', (target, top), name, move)
            elif entry.endswith('.md') and entry[:-3] + '_draft.docx' in entries:
                leftover(src, 'a Markdown copy beside its Word draft; the Word draft is the document')
            elif entry.endswith('.md') and not REV.match(entry):
                draft(src, entry[:-3], '.md', (target, top), name, move)
            elif entry.endswith('.docx'):
                leftover(src, 'not named <document>_draft.docx, so its status is unclear',
                         os.path.join(target, entry))
            else:
                move(src, os.path.join(target, entry), 'moved as it is', name)

    return moves, leftovers, map_lines(root, domains), locks


def draft(src, base, ext, folders, domain, move):
    """A draft goes beside its record, named for the revision after it. Records already in
    context/<domain>/ count, and so do records saved in outputs/<domain>/, which move there too."""
    target = folders[0]
    record = newest_record(folders, base)
    if record is None:
        move(src, os.path.join(target, base + '_draft' + ext), 'a draft', domain)
    elif os.path.getmtime(record[1]) > os.path.getmtime(src):
        move(src, os.path.join(target, 'archive', os.path.basename(src)),
             'superseded: %s is newer' % os.path.basename(record[1]), domain)
    else:
        move(src, os.path.join(target, '%s_rev%s_draft%s' % (base, next_rev(record[0]), ext)),
             'a draft of the revision after %s' % os.path.basename(record[1]), domain)


def walk(path):
    if os.path.isfile(path):
        return [path]
    found = []
    for folder, _, files in os.walk(path):
        found.extend(os.path.join(folder, f) for f in sorted(files))
    return sorted(found)


# ---- the context map ----------------------------------------------------------

def sections(text):
    """{domain: (start line, end line)} for each ## section in the map."""
    lines = text.split('\n')
    found, current = {}, None
    for i, line in enumerate(lines):
        m = re.match(r'^##\s+(\S+)\s*$', line)
        if m:
            if current:
                found[current] = (found[current][0], i)
            current = m.group(1).strip().lower()
            found[current] = (i, len(lines))
        elif line.startswith('# ') and current:
            found[current] = (found[current][0], i)
            current = None
    return found, lines


def map_lines(root, domains):
    """The domains whose section in the map does not yet list ./context/<domain>/."""
    path = os.path.join(root, MAP)
    if not domains or not os.path.exists(path):
        return []
    with open(path, encoding='utf-8') as f:
        found, lines = sections(f.read())
    need = []
    for domain in DOMAINS:
        if domain not in domains:
            continue
        if domain in found:
            start, end = found[domain]
            body = [l.strip() for l in lines[start + 1:end]]
            if any(('context/%s' % domain) in l and not l.lstrip('- ').startswith(('exclude:', 'restricted:'))
                   for l in body):
                continue
        need.append(domain)
    return need


def add_to_map(root, domains):
    path = os.path.join(root, MAP)
    with open(path, encoding='utf-8') as f:
        text = f.read()
    for domain in domains:
        found, lines = sections(text)
        entry = '- `./context/%s/` — MOS drafts and the files they rely on' % domain
        if domain not in found:
            text = text.rstrip('\n') + '\n\n## %s\n%s\n' % (domain, entry)
            continue
        start, end = found[domain]
        for i in range(start + 1, end):
            if lines[i].strip().lower() == '- not mapped yet':
                lines[i] = entry
                break
        else:
            last = start
            for i in range(start + 1, end):
                if lines[i].strip():
                    last = i
            lines.insert(last + 1, entry)
        text = '\n'.join(lines)
    with open(path, 'w', encoding='utf-8', newline='') as f:
        f.write(text)


# ---- command line -------------------------------------------------------------

def report(root, moves, leftovers, domains, locks):
    if locks:
        print('Open in Word: %s. Close %s before apply; nothing moves while a document is open.\n'
              % (', '.join(rel(p, root) for p in locks), 'it' if len(locks) == 1 else 'them'))
    if not moves and not leftovers:
        if os.path.isdir(os.path.join(root, 'outputs')):
            print('Old layout: outputs/ is empty. apply removes it.')
        else:
            print('Current layout: no outputs/ folder. Nothing to do.')
        return
    count = len(moves) + len(leftovers)
    print('Old layout: outputs/ holds %d file%s. Drafts now live in context/<domain>/.'
          % (count, '' if count == 1 else 's'))
    if moves:
        print('\nMoves (%d):' % len(moves))
        for src, dst, why in moves:
            print('  %s\n    -> %s  (%s)' % (rel(src, root), rel(dst, root), why))
    if domains:
        print('\nContext map: adds ./context/<domain>/ under %s, so skills can read what moved there.'
              % ', '.join(domains))
    if leftovers:
        print('\nLeft over (%d) — untouched unless named with --delete or --move:' % len(leftovers))
        for src, why, suggest in leftovers:
            line = '  %s  (%s)' % (rel(src, root), why)
            if suggest:
                line += '\n    --move puts it at %s' % rel(suggest, root)
            print(line)


def apply(root, delete, move_named):
    moves, leftovers, domains, locks = plan(root)
    if locks:
        raise LayoutError('a document is open in Word (%s). Close it, then run apply again. Nothing was moved.'
                          % ', '.join(rel(p, root) for p in locks))
    by_path = {rel(src, root): (src, suggest) for src, _, suggest in leftovers}
    for name in delete + move_named:
        if name not in by_path:
            raise LayoutError('%s is not on the left-over list. Run check, and name a path as it prints.' % name)
        if name in move_named and not by_path[name][1]:
            raise LayoutError('%s has nowhere to move; it can only be deleted or left.' % name)
    for src, dst, _ in moves:
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        os.replace(src, dst)
        print('Moved: %s -> %s' % (rel(src, root), rel(dst, root)))
    if domains:
        add_to_map(root, domains)
        print('Context map: added ./context/<domain>/ under %s.' % ', '.join(domains))
    for name in move_named:
        src, dst = by_path[name]
        if os.path.exists(dst):
            raise LayoutError('%s already exists. %s not moved.' % (rel(dst, root), name))
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        os.replace(src, dst)
        print('Moved: %s -> %s' % (name, rel(dst, root)))
    for name in delete:
        os.remove(by_path[name][0])
        print('Deleted: %s' % name)
    outputs = os.path.join(root, 'outputs')
    if os.path.isdir(outputs):
        for folder, _, _ in sorted(os.walk(outputs), key=lambda w: -len(w[0])):
            if not os.listdir(folder):
                os.rmdir(folder)
    if os.path.isdir(outputs):
        left = walk(outputs)
        print('outputs/ kept: %d file%s left in it.' % (len(left), '' if len(left) == 1 else 's'))
    else:
        print('outputs/ removed. The folder is on the current layout.')


def main(argv=None):
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')
    p = argparse.ArgumentParser(prog='layout', description='Bring a company folder up to the current MOS layout.')
    sub = p.add_subparsers(dest='cmd', required=True)
    c = sub.add_parser('check')
    c.add_argument('--root', default='.')
    a_ = sub.add_parser('apply')
    a_.add_argument('--root', default='.')
    a_.add_argument('--delete', action='append', default=[], metavar='PATH')
    a_.add_argument('--move', action='append', default=[], metavar='PATH')
    a = p.parse_args(argv)
    root = os.path.abspath(a.root)
    if not os.path.isdir(os.path.join(root, 'context')) and not os.path.isdir(os.path.join(root, 'outputs')):
        print('layout: %s has no context/ or outputs/ folder. Run it from the company root.' % root, file=sys.stderr)
        return 1
    try:
        if a.cmd == 'check':
            report(root, *plan(root))
        else:
            apply(root, a.delete, a.move)
    except (LayoutError, OSError) as e:
        print('layout: %s' % e, file=sys.stderr)
        return 1
    return 0


if __name__ == '__main__':
    sys.exit(main())
