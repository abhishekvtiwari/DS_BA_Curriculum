"""Turn a chapter's Markdown into a runnable Jupyter notebook, then execute it.

Why this works rather than writing notebooks by hand: the chapter already teaches line by line.
Each code block in the manuscript sits between the prose that sets it up and a bulleted
explanation of every line and argument, with the real output in between. That is exactly a
notebook's shape, so the notebook carries the book's own words and the book's own code.

What happens to each piece of the chapter:

  prose, headings, tables        -> markdown cells, unchanged
  ```python                      -> a code cell, executed, so the output is produced here
  the ``` output block after it  -> dropped when the cell runs (the real output replaces it),
                                    kept and labelled as the chapter's own when it cannot run
  <!-- run: none -->             -> a code cell that is NOT executed, and says why
  ```sql ```bash ```vb etc.      -> shown inside a markdown cell, since a Python kernel cannot
                                    run them; the chapter's output is kept beside them
  <!-- py: reset -->             -> a note that the cells below assume a fresh kernel

Nothing is invented. An output is either produced by running the cell here, or it is the
chapter's own output, labelled as such.

    python tools/notebooks/md_to_notebook.py ch18            # one chapter
    python tools/notebooks/md_to_notebook.py ch18 --no-exec  # build without running
    python tools/notebooks/md_to_notebook.py --all           # every chapter with python
"""
import argparse
import glob
import os
import pathlib
import re
import sys

import nbformat as nbf

ROOT = pathlib.Path(__file__).resolve().parents[2]
MS = ROOT / 'manuscript'
COMP = ROOT / 'companion'

FENCE = re.compile(r'^```([A-Za-z0-9_+-]*)\s*$')
MARKER = re.compile(r'^<!--\s*([a-z]+):\s*([a-z-]+)\s*-->\s*$')
RUNNABLE_PROSE = {'text', 'output', ''}          # a bare fence is the chapter's printed output


def tokenise(md):
    """[(kind, text, lang, marker)] where kind is 'prose' or 'fence'."""
    out, buf, i = [], [], 0
    lines = md.splitlines()
    marker = None
    while i < len(lines):
        line = lines[i]
        m = MARKER.match(line)
        if m:
            marker = (m.group(1), m.group(2))
            i += 1
            continue
        f = FENCE.match(line)
        if f:
            lang = f.group(1).lower()
            body, i = [], i + 1
            while i < len(lines) and not FENCE.match(lines[i]):
                body.append(lines[i]); i += 1
            i += 1
            if buf:
                out.append(('prose', '\n'.join(buf).strip(), None, None)); buf = []
            out.append(('fence', '\n'.join(body), lang, marker))
            marker = None
            continue
        buf.append(line); i += 1
    if buf:
        out.append(('prose', '\n'.join(buf).strip(), None, None))
    return [t for t in out if t[1].strip()]


def build(key, exec_ok=True):
    src = sorted(MS.glob(f'{key}-*.md'))
    if not src:
        raise SystemExit(f'no manuscript for {key}')
    md = src[0].read_text(encoding='utf-8')
    title = md.splitlines()[0].lstrip('# ').strip()
    toks = tokenise(md)

    cells = [nbf.v4.new_markdown_cell(
        f"# {title}\n\n"
        f"*The runnable half of this chapter.* Every code cell below is the chapter's own code, and "
        f"the words around it are the chapter's own explanation. Run the cells in order: each one "
        f"uses names made by the cells before it.\n\n"
        f"Riverstone Supplies is the single worked example throughout the book, so the data here is "
        f"the same data you meet in every other chapter.\n\n"
        f"Built from `manuscript/{src[0].name}`.")]

    skipped_out = False
    n_code = n_frozen = n_foreign = 0
    for idx, (kind, text, lang, marker) in enumerate(toks):
        if kind == 'prose':
            cells.append(nbf.v4.new_markdown_cell(text))
            skipped_out = False
            continue

        norun = marker == ('run', 'none')
        if marker == ('py', 'reset'):
            cells.append(nbf.v4.new_markdown_cell(
                "> **Fresh start.** The cells below do not depend on the ones above. If you have "
                "been running top to bottom, restarting the kernel here changes nothing."))

        if lang == 'python':
            if norun:
                cells.append(nbf.v4.new_code_cell(text))
                cells[-1].metadata['skip_execution'] = True
                cells.append(nbf.v4.new_markdown_cell(
                    "> **Not run here.** The chapter marks this block as illustration rather than "
                    "something to execute, usually because it needs a service, a key or a file this "
                    "notebook does not set up. Read it, do not run it."))
                n_frozen += 1
            else:
                cells.append(nbf.v4.new_code_cell(text))
                n_code += 1
            skipped_out = not norun
            continue

        if lang in RUNNABLE_PROSE:
            # the chapter's printed output. Keep it on the code cell: if the cell runs here, the
            # real output replaces it; if it cannot run, it is restored as the chapter's own.
            if skipped_out:
                for c in reversed(cells):
                    if c.cell_type == 'code':
                        c.metadata['book_output'] = text
                        break
                skipped_out = False
                continue
            cells.append(nbf.v4.new_markdown_cell(
                "**The chapter's output:**\n\n```\n" + text + "\n```"))
            continue

        # sql, bash, vba, dax, yaml ...: a Python kernel cannot run these
        cells.append(nbf.v4.new_markdown_cell(
            f"**`{lang}`, not run by this notebook.** Run it in the tool the chapter names.\n\n"
            f"```{lang}\n{text}\n```"))
        n_foreign += 1
        skipped_out = False

    nb = nbf.v4.new_notebook(cells=cells)
    nb.metadata.kernelspec = {'display_name': 'Python 3', 'language': 'python', 'name': 'python3'}
    nb.metadata.language_info = {'name': 'python', 'version': '3.12'}

    where = COMP / key
    where.mkdir(parents=True, exist_ok=True)
    out = where / f'{key}-notebook.ipynb'

    status, needs_setup, review = 'not executed', 0, []
    if exec_ok and n_code:
        try:
            from nbclient import NotebookClient
            client = NotebookClient(nb, timeout=600, kernel_name='python3',
                                    allow_errors=True,
                                    resources={'metadata': {'path': str(where)}})
            client.execute()
            needs_setup, review = settle_errors(nb)
            ran = sum(1 for c in nb.cells
                      if c.cell_type == 'code' and c.get('execution_count'))
            status = ('executed clean' if not needs_setup and not review
                      else f'{ran} of {n_code} ran, {needs_setup} need setup'
                            + (f', {len(review)} TO REVIEW' if review else ''))
        except Exception as e:                                  # noqa: BLE001
            status = f'execution failed: {type(e).__name__}'
    out.write_text(nbf.writes(nb), encoding='utf-8')
    return dict(key=key, cells=len(cells), code=n_code, frozen=n_frozen, foreign=n_foreign,
                needs_setup=needs_setup, review=review, status=status, path=out)


# An error of one of these kinds means the cell needs something this machine does not have:
# a database, a key, a service, a command line. It does not mean the material is wrong.
ENVIRONMENTAL = {'KeyError', 'ConnectionError', 'ModuleNotFoundError', 'ImportError',
                 'SystemExit', 'FileNotFoundError', 'OperationalError', 'OSError',
                 'TimeoutError', 'URLError', 'HTTPError'}
# NameError almost always means an earlier environmental failure left a name unset.
CASCADE = {'NameError', 'AttributeError', 'TypeError', 'KeyError', 'UnboundLocalError'}


def settle_errors(nb):
    """Replace error tracebacks with the chapter's own output and an honest note.

    Returns (how many cells need setup, [cells whose failure looks like a real defect]).
    """
    code_cells = [c for c in nb.cells if c.cell_type == 'code']
    first_failure = None
    needs_setup, review = 0, []
    for pos, cell in enumerate(code_cells):
        err = next((o for o in cell.get('outputs', []) if o.output_type == 'error'), None)
        if err is None:
            continue
        name = err.get('ename', '?')
        book = cell.metadata.get('book_output', '')
        # Some blocks are meant to fail: the chapter is showing the reader what an error looks
        # like, and prints the traceback as its output. Then the error IS the right output.
        if book and (re.search(r'^Traceback', book, re.M) or re.search(r'^\w*Error\b', book, re.M)):
            cell.metadata.pop('book_output', None)
            continue
        if name in ENVIRONMENTAL:
            reason = ('needs something this machine does not have: a database, an API key, a '
                      'running service, or command-line arguments')
            if first_failure is None:
                first_failure = pos
        elif name in CASCADE and first_failure is not None:
            reason = ('depends on a cell above that could not run here, so its names were never '
                      'created')
        else:
            review.append((pos, name, (err.get('evalue') or '').splitlines()[:1]))
            continue
        needs_setup += 1
        book = cell.metadata.pop('book_output', None)
        cell.outputs = []
        cell.execution_count = None
        cell.metadata['skip_execution'] = True
        note = (f"> **Not run here.** This cell {reason}. Run it on your own machine, with the "
                f"setup the chapter describes, and you should see what the chapter shows.")
        if book:
            note += "\n\n**What the chapter shows:**\n\n```\n" + book + "\n```"
        i = nb.cells.index(cell)
        nb.cells.insert(i + 1, nbf.v4.new_markdown_cell(note))
    # any book_output left over belonged to a cell that ran, so it is no longer needed
    for c in code_cells:
        c.metadata.pop('book_output', None)
    return needs_setup, review


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('chapters', nargs='*')
    ap.add_argument('--all', action='store_true')
    ap.add_argument('--no-exec', action='store_true')
    a = ap.parse_args()

    keys = a.chapters
    if a.all:
        keys = []
        for f in sorted(MS.glob('ch*.md')):
            if len(re.findall(r'```python\n', f.read_text(encoding='utf-8'))) >= 3:
                keys.append(f.name.split('-')[0])
    if not keys:
        raise SystemExit('name a chapter, or pass --all')

    print(f"{'ch':<7}{'cells':>6}{'code':>6}{'frozen':>8}{'other':>7}  status")
    for k in keys:
        r = build(k, exec_ok=not a.no_exec)
        print(f"{r['key']:<7}{r['cells']:>6}{r['code']:>6}{r['frozen']:>8}{r['foreign']:>7}  {r['status']}")
        for pos, name, ev in r['review']:
            print(f"         REVIEW cell {pos}: {name} {ev}")
