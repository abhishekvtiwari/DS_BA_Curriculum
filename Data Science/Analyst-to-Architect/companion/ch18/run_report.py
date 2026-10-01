"""Analyst to Architect · Chapter 18 · run_report.py
Section 18.18's entry point: the one command a scheduler runs.

Use:     python run_report.py                 # last completed month
         python run_report.py --month 2025-12 # a named month
         python run_report.py --month 2025-12 --excel
Exit:    0 if the report was written, 1 if a check failed, 2 if the month has no data.
Tested:  Python 3.12.0, pandas 3.0.2 (1 October 2026)

A scheduled job has nobody watching it, so this file does only four things: work out which
month, write the report, say what happened in the log, and hand back an exit code the
scheduler can act on.

Riverstone Supplies is fictional; every name and number is invented.
"""
from __future__ import annotations

import argparse
import logging
import sys
from pathlib import Path

import pandas as pd

from report_objects import (ExcelWriterStep, MarkdownWriterStep, MonthlyReport, ReportConfig)

log = logging.getLogger("run_report")


def last_completed_month(today: pd.Timestamp | None = None) -> str:
    """A report that runs on the 1st wants the month that just ended, not the one starting."""
    today = today or pd.Timestamp.today()
    return (today.normalize().replace(day=1) - pd.offsets.MonthBegin(1)).strftime("%Y-%m")


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(prog="run_report",
                                 description="Write Riverstone's monthly sales report.")
    ap.add_argument("--month", help="YYYY-MM. Default: the last completed month.")
    ap.add_argument("--excel", action="store_true", help="also write the Excel workbook")
    ap.add_argument("--out", default="reports", help="where to write (default: reports)")
    args = ap.parse_args(argv)

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)-7s %(name)s %(message)s",
        handlers=[logging.StreamHandler(sys.stdout),
                  logging.FileHandler(Path(args.out).parent / "run_report.log", encoding="utf-8")])

    month = args.month or last_completed_month()
    log.info("starting report for %s", month)

    writers = [MarkdownWriterStep()] + ([ExcelWriterStep()] if args.excel else [])
    report = MonthlyReport(ReportConfig(month=month, out_dir=Path(args.out)), writers=writers)

    try:
        if report.lines().empty:
            log.error("no order lines for %s: nothing written", month)
            return 2
        written = report.run()
    except ValueError as e:                      # a check failed; run() says which
        log.error("%s", e)
        return 1

    for p in written:
        log.info("wrote %s (%s bytes)", p, f"{p.stat().st_size:,}")
    h = report.headlines()
    log.info("net revenue Rs %s from %s orders", f"{h['net_revenue']:,.0f}", f"{h['orders']:,}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
