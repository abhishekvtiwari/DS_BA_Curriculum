"""Run the book's own PDF build on Windows, with pandoc supplied from pypandoc.

The build itself is unchanged: this only fixes two things about the environment it is being run
in, so that `tools/pdf/books.py` works here exactly as it does where it was written.

1. **Pandoc.** `build.py` shells out to `pandoc`. There is no system pandoc on this machine, so
   this puts the binary that ships with the `pypandoc-binary` wheel on PATH first. Install it with
   `pip install pypandoc-binary`; pandoc 3.9 is what was used.

2. **UTF-8.** `build.py` calls `read_text()` and `write_text()` without naming an encoding. On
   Linux that is UTF-8; on Windows it is cp1252, and the manuscript has characters cp1252 cannot
   represent, so every chapter fails to read. Python's UTF-8 mode makes the defaults match.

Usage, from the repository root or anywhere:

    python tools/review-export/build_book.py book4
    python tools/review-export/build_book.py book1 book2 book3 book4 map

Output goes where books.py puts it unless BOOK_BUILD_DIR and BOOK_OUT_DIR say otherwise; both are
passed through untouched.
"""
import os
import pathlib
import subprocess
import sys


def pandoc_dir():
    """The directory holding pandoc.exe from the pypandoc-binary wheel."""
    try:
        import pypandoc
    except ImportError:
        raise SystemExit('pypandoc is not installed. Run: pip install pypandoc-binary')
    p = pathlib.Path(pypandoc.get_pandoc_path()).parent
    if not p.exists():
        raise SystemExit(f'pypandoc reports a pandoc path that does not exist: {p}')
    return p


def book_root():
    """The folder holding tools/pdf/books.py."""
    here = pathlib.Path(__file__).resolve()
    for base in [here.parents[2] / 'Data Science' / 'Analyst-to-Architect',
                 here.parents[2],
                 pathlib.Path.cwd()]:
        if (base / 'tools' / 'pdf' / 'books.py').exists():
            return base
    raise SystemExit('cannot find tools/pdf/books.py')


if __name__ == '__main__':
    if len(sys.argv) < 2:
        raise SystemExit(__doc__)

    root = book_root()
    env = dict(os.environ)
    env['PATH'] = str(pandoc_dir()) + os.pathsep + env['PATH']
    env['PYTHONUTF8'] = '1'
    env['PYTHONIOENCODING'] = 'utf-8'

    print(f'book root : {root}')
    print(f'pandoc    : {pandoc_dir()}')
    print(f'targets   : {" ".join(sys.argv[1:])}')
    print('-' * 70, flush=True)

    r = subprocess.run([sys.executable, '-X', 'utf8', 'tools/pdf/books.py', *sys.argv[1:]],
                       cwd=root, env=env)
    sys.exit(r.returncode)
