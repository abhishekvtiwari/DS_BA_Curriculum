"""Summarize every CSV export in a folder.

Usage:  python summarize_exports.py sales_exports
"""
import csv
import sys
from pathlib import Path


def read_rows(path):
    """Return the rows of a CSV file as a list of dictionaries."""
    with open(path, encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def summarize(path):
    """Return one summary dictionary for a CSV export."""
    rows = read_rows(path)
    values, bad = [], 0
    for row in rows:
        try:
            if row["status"] != "Cancelled":
                values.append(float(row["net_revenue"]))
        except (ValueError, TypeError, KeyError):
            bad += 1
    return {
        "file": path.name,
        "rows": len(rows),
        "lines_counted": len(values),
        "unreadable": bad,
        "net_revenue": round(sum(values), 2),
    }


def main(folder):
    paths = sorted(Path(folder).glob("*.csv"))
    if not paths:
        print(f"No CSV files found in {folder}")
        return 1
    print(f"{'file':<28}{'rows':>6}{'net revenue':>16}")
    total = 0.0
    for path in paths:
        s = summarize(path)
        total += s["net_revenue"]
        print(f"{s['file']:<28}{s['rows']:>6}{s['net_revenue']:>16,.2f}")
    print(f"{'TOTAL':<28}{'':>6}{total:>16,.2f}")
    return 0


if __name__ == "__main__":
    folder = sys.argv[1] if len(sys.argv) > 1 else "sales_exports"
    raise SystemExit(main(folder))
