"""check_setup.py - checks your setup for Chapter 17 of "Analyst to Architect".

Run it from your work/ch17 folder, with the book's environment active:
    python check_setup.py
You don't need to understand this code yet; by the end of Chapter 17 you will.
"""
import sys
from pathlib import Path
from importlib.metadata import version, PackageNotFoundError

problems = []

def report(item, found, fix=None):
    """Print one line of the report, and remember the fix if there is one."""
    if fix is None:
        print(f"{item:<16}{found:<12}OK")
    else:
        problems.append(fix)
        print(f"{item:<16}{found:<12}FIX {len(problems)}")

v = sys.version_info
python_found = f"{v.major}.{v.minor}.{v.micro}"
if (v.major, v.minor) >= (3, 11):
    report("Python", python_found)
else:
    report("Python", python_found, "Install Python 3.14 (section 17.0, step 2), then recreate .venv.")

in_venv = sys.prefix != sys.base_prefix
if in_venv:
    report("Environment", Path(sys.prefix).name)
else:
    report("Environment", "none", "Activate the environment (section 17.0, step 4), then run this again.")

try:
    report("JupyterLab", version("jupyterlab"))
except PackageNotFoundError:
    report("JupyterLab", "missing",
           "With the environment active, run:  python -m pip install jupyterlab")

here = Path.cwd()
csv_files = sorted(Path("sales_exports").glob("*.csv"))
if len(csv_files) == 12:
    report("Practice files", "12 CSVs")
else:
    report("Practice files", f"{len(csv_files)} CSVs",
           f"You are in {here}. Use cd to move into your work/ch17 folder (section 17.0, step 1).")

print("Python in use:", sys.executable)
if problems:
    print("Fix these, in order, then run the script again:")
    for number, fix in enumerate(problems, start=1):
        print(f"  {number}. {fix}")
else:
    print("Setup OK: you're ready for section 17.1.")
