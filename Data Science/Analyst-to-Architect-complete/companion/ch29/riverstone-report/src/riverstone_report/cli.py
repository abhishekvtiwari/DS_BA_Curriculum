"""Command-line entry point: riverstone-report --month 2025-12"""
from __future__ import annotations

import argparse
import logging
import sys

from sqlalchemy import create_engine

from riverstone_report import db, excel, transform
from riverstone_report.config import ReportConfig
from riverstone_report.errors import ReportError

log = logging.getLogger("riverstone_report")


def run(config: ReportConfig) -> None:
    engine = create_engine(config.database_url)
    lines = db.fetch_sales_lines(engine, config.month, config.next_month)
    log.info("read %d sales lines for %s", len(lines), f"{config.month:%Y-%m}")
    summary = transform.summarize(lines, db.fetch_target(engine, config.month))
    path = excel.write_report(summary, transform.revenue_by_category(lines),
                              transform.top_customers(lines, config.top_n), config.output_path)
    log.info("net revenue %.2f from %d orders; wrote %s", summary.revenue, summary.orders, path)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="riverstone-report", description="Build Riverstone's monthly sales report.")
    parser.add_argument("--month", required=True, help="the month to report, as YYYY-MM")
    parser.add_argument("--verbose", action="store_true", help="show debug messages")
    args = parser.parse_args(argv)
    logging.basicConfig(level=logging.DEBUG if args.verbose else logging.INFO,
                        format="%(asctime)s %(levelname)s %(name)s: %(message)s")
    try:
        run(ReportConfig.from_env(args.month))
    except ReportError as exc:
        log.error("%s", exc)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
