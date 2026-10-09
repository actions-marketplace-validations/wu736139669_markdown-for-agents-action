#!/usr/bin/env python3
"""Generate llms.txt (and llms-full.txt) from a directory of Markdown files.

Usage:
    python3 make_llms_txt.py ./public --base https://example.com \
        --name "Site Name" --description "One-line description" [--full]

For every *.md file found (excluding llms*.txt sources), the first `# ` heading
becomes the link title and the first `> ` blockquote becomes its description.
"""
import argparse
import pathlib
import re
import sys


def read_card(path):
    text = path.read_text(encoding='utf-8')
    title = None
    desc = ''
    for line in text.splitlines():
        line = line.strip()
        if title is None and line.startswith('# '):
            title = line[2:].strip()
            continue
        if line.startswith('> '):
            desc = line[2:].strip()
            break
    return title or path.stem, desc


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('directory')
    ap.add_argument('--base', required=True)
    ap.add_argument('--name', required=True)
    ap.add_argument('--description', default='')
    ap.add_argument('--full', action='store_true', help='also write llms-full.txt')
    args = ap.parse_args()

    root = pathlib.Path(args.directory)
    base = args.base.rstrip('/')
    md_files = sorted(p for p in root.rglob('*.md') if not p.name.startswith('llms'))
    if not md_files:
        print('no .md files found — run generate_md.py first', file=sys.stderr)
        sys.exit(1)

    out = [f'# {args.name}', '']
    if args.description:
        out += [f'> {args.description}', '']
    out += ['## Pages', '']
    for p in md_files:
        title, desc = read_card(p)
        rel = p.relative_to(root).with_suffix('').as_posix()
        url = f'{base}/{rel}.md' if rel != 'index' else f'{base}/index.md'
        line = f'- [{title}]({url})'
        if desc:
            line += f': {desc}'
        out.append(line)
    out.append('')

    (root / 'llms.txt').write_text('\n'.join(out), encoding='utf-8')
    print(f'llms.txt written: {len(md_files)} entries')

    if args.full:
        chunks = [p.read_text(encoding='utf-8') for p in md_files]
        (root / 'llms-full.txt').write_text('\n\n---\n\n'.join(chunks), encoding='utf-8')
        print('llms-full.txt written')


if __name__ == '__main__':
    main()
