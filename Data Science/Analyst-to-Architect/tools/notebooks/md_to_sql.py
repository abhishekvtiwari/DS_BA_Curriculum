"""Turn a chapter's SQL into annotated, runnable .sql files, one per dialect.

PostgreSQL is the book's primary database and MySQL is the supported alternative, so every
chapter that teaches SQL gets two files. The book already marks which blocks belong to which:

    <!-- run: pg -->      PostgreSQL only
    <!-- run: mysql -->   MySQL only
    <!-- run: both -->    both, unchanged
    <!-- out: mysql -->   the MySQL output of the block above
    (no marker)           both

Each statement keeps the chapter's own explanation above it, as SQL comments, and the chapter's
own result below it, so the file teaches rather than just executes. Nothing is invented: an output
is the chapter's, and it is labelled as the chapter's.

    python tools/notebooks/md_to_sql.py ch12
    python tools/notebooks/md_to_sql.py --all
"""
import argparse
import pathlib
import re
import sys
import textwrap

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from md_to_notebook import MS, COMP, tokenise           # noqa: E402

DIALECTS = {'postgresql': {'pg', 'both', None}, 'mysql': {'mysql', 'both', None}}
SQL_LANGS = {'sql', 'mysql', 'postgresql', 'plpgsql'}


def comment(text, width=96):
    """Prose as SQL line comments, wrapped, with markdown stripped back to plain words."""
    text = re.sub(r'!\[[^\]]*\]\([^)]*\)', '', text)             # figures
    text = re.sub(r'\*\*(.+?)\*\*', r'\1', text)                 # bold
    text = re.sub(r'(?<!\w)\*(.+?)\*(?!\w)', r'\1', text)        # italic
    text = re.sub(r'`([^`]*)`', r'\1', text)                     # inline code
    out = []
    for para in text.split('\n\n'):
        para = ' '.join(l.strip() for l in para.splitlines() if l.strip())
        if not para:
            continue
        if para.startswith('#'):
            head = para.lstrip('#').strip()
            out += ['', '-- ' + '=' * (width - 3), f'-- {head}', '-- ' + '=' * (width - 3)]
        else:
            out += [''] + ['-- ' + l for l in textwrap.wrap(para, width)]
    return '\n'.join(out)


def build(key):
    src = sorted(MS.glob(f'{key}-*.md'))
    if not src:
        raise SystemExit(f'no manuscript for {key}')
    md = src[0].read_text(encoding='utf-8')
    title = md.splitlines()[0].lstrip('# ').strip()
    toks = tokenise(md)

    # collect (prose, sql, dialect, output) in order
    items, pending_prose, last = [], [], None
    for kind, text, lang, marker in toks:
        if kind == 'prose':
            if last is not None:
                items.append(last); last = None
            pending_prose.append(text)
            continue
        mk = marker[1] if marker and marker[0] in ('run', 'out') else None
        if lang in SQL_LANGS:
            if last is not None:
                items.append(last)
            last = dict(prose='\n\n'.join(pending_prose), sql=text, dialect=mk, out=None, out_my=None)
            pending_prose = []
            continue
        if lang in ('', 'text', 'output') and last is not None:
            if marker and marker == ('out', 'mysql'):
                last['out_my'] = text
            elif last['out'] is None:
                last['out'] = text
            continue
        pending_prose = []
    if last is not None:
        items.append(last)

    where = COMP / key
    where.mkdir(parents=True, exist_ok=True)
    written = {}
    for dialect, accept in DIALECTS.items():
        chosen = [it for it in items if (it['dialect'] in accept)]
        if not chosen:
            continue
        head = [
            f'-- {title}',
            f'-- Practice SQL for {dialect.upper()}, extracted from the chapter.',
            '--',
            '-- Riverstone Supplies is the worked example throughout the book. Load the database',
            '-- first (companion/riverstone_setup_mini.sql, riverstone_2025_setup.sql, or',
            '-- companion/full/riverstone_full_setup_' + ('postgresql' if dialect == 'postgresql' else 'mysql')
            + '.sql), then run these statements in order.',
            '--',
            "-- Each statement keeps the chapter's explanation above it and the chapter's own",
            '-- result below it, marked as the chapter\'s. Run it yourself to see your own.',
            f'-- Source: manuscript/{src[0].name}',
            '',
        ]
        body = []
        for it in chosen:
            if it['prose']:
                body.append(comment(it['prose']))
            body.append('')
            body.append(it['sql'].rstrip())
            shown = it['out_my'] if (dialect == 'mysql' and it['out_my']) else it['out']
            if shown:
                body.append('')
                body.append('/* The chapter shows:')
                body += ['   ' + l for l in shown.rstrip().splitlines()]
                body.append('*/')
            body.append('')
        f = where / f'{key}_queries_{dialect}.sql'
        # Never overwrite a file the book already ships. Several chapters carry hand-written query
        # files, and an auto-extracted one is not an improvement on a curated one.
        if f.exists():
            written[dialect] = (f, 0)
            continue
        f.write_text('\n'.join(head + body) + '\n', encoding='utf-8')
        written[dialect] = (f, len(chosen))
    return title, written, len(items)


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('chapters', nargs='*')
    ap.add_argument('--all', action='store_true')
    a = ap.parse_args()
    keys = a.chapters
    if a.all:
        keys = [f.name.split('-')[0] for f in sorted(MS.glob('ch*.md'))
                if len(re.findall(r'```(?:sql|mysql)\n', f.read_text(encoding='utf-8'))) >= 3]
    if not keys:
        raise SystemExit('name a chapter, or pass --all')
    print(f"{'ch':<7}{'blocks':>7}  files written")
    for k in keys:
        title, written, total = build(k)
        bits = ', '.join(f"{d}: {n} stmts" if n else f"{d}: SKIPPED, already shipped"
                         for d, (f, n) in written.items())
        print(f"{k:<7}{total:>7}  {bits}")
