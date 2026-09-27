"""check_setup.py - confirms your Python setup for "Analyst to Architect" (Chapter 6).
Run it from a terminal:  python check_setup.py   (on macOS/Linux: python3 check_setup.py)"""
import sys
from importlib.metadata import version, PackageNotFoundError

ok = True
v = sys.version_info
if (v.major, v.minor) >= (3, 11):
    print(f"{'python':<12} {f'{v.major}.{v.minor}.{v.micro}':<8} OK")
else:
    print(f"{'python':<12} {f'{v.major}.{v.minor}.{v.micro}':<8} TOO OLD: install Python 3.13 or newer")
    ok = False

for package in ["pandas", "openpyxl", "matplotlib", "jupyterlab"]:
    try:
        print(f"{package:<12} {version(package):<8} OK")
    except PackageNotFoundError:
        print(f"{package:<12} {'-':<8} MISSING: run  python -m pip install {package}")
        ok = False

print("All set." if ok else "Fix the lines above, then run this script again.")
