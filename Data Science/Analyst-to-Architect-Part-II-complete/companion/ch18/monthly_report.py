"""Riverstone monthly sales report: database → checks → Excel → Markdown summary.

Usage:  python monthly_report.py 2025-12 [--out reports]
Environment: RIVERSTONE_DB (SQLAlchemy URL), e.g. postgresql+psycopg://user:pw@host:5432/riverstone_full
"""
import argparse
import logging
import os
import sys
from datetime import datetime
from pathlib import Path

import pandas as pd
from sqlalchemy import create_engine, text

log = logging.getLogger("monthly_report")

QUERY = text("""
    SELECT s.order_date, s.order_id, s.customer_id, c.segment, c.city,
           p.product_name, s.quantity, s.net_revenue, s.product_cost
    FROM sales_lines s
    JOIN customers c ON c.customer_id = s.customer_id
    JOIN products  p ON p.product_id  = s.product_id
    WHERE s.order_date >= :start AND s.order_date < :end
""")


def load(engine, month):
    """Return the month's order lines, and the month's target."""
    start = pd.Timestamp(month + "-01")
    end = start + pd.offsets.MonthBegin(1)
    lines = pd.read_sql(QUERY, engine, params={"start": start.date(), "end": end.date()}, parse_dates=["order_date"])
    target = pd.read_sql(text("SELECT target_revenue FROM sales_targets WHERE target_month = :m"),
                         engine, params={"m": start.date()})
    return lines, (float(target["target_revenue"].iloc[0]) if len(target) else None)


def check(lines, month):
    """Return a list of (name, passed, detail) checks that must all pass."""
    starts_in_month = lines["order_date"].dt.to_period("M").astype(str).eq(month).all()
    return [
        ("rows returned", len(lines) > 0, f"{len(lines):,} lines"),
        ("all dates inside the month", bool(starts_in_month), month),
        ("no missing revenue", bool(lines["net_revenue"].notna().all()), f"{int(lines['net_revenue'].isna().sum())} missing"),
        ("no negative quantities", bool((lines["quantity"] > 0).all()), f"min {int(lines['quantity'].min())}"),
        ("every line has a customer", bool(lines["customer_id"].notna().all()), f"{lines['customer_id'].nunique()} customers"),
    ]


def summarize(lines, target):
    """Return the headline numbers and the by-region table."""
    revenue = float(lines["net_revenue"].sum())
    headlines = {
        "net_revenue": round(revenue, 2),
        "orders": int(lines["order_id"].nunique()),
        "customers": int(lines["customer_id"].nunique()),
        "average_order_value": round(revenue / lines["order_id"].nunique(), 2),
        "gross_margin_pct": round((1 - lines["product_cost"].sum() / revenue) * 100, 1),
        "pct_of_target": round(revenue / target * 100, 1) if target else None,
    }
    by_segment = (lines.groupby("segment", as_index=False)
                       .agg(net_revenue=("net_revenue", "sum"), orders=("order_id", "nunique"))
                       .sort_values("net_revenue", ascending=False).round(2))
    return headlines, by_segment


def write_excel(path, headlines, by_segment, lines):
    """Write a two-sheet workbook with a formatted header row."""
    by_product = (lines.groupby("product_name", as_index=False)["net_revenue"].sum()
                       .sort_values("net_revenue", ascending=False).round(2))
    with pd.ExcelWriter(path, engine="xlsxwriter") as writer:
        pd.DataFrame([headlines]).to_excel(writer, sheet_name="Headlines", index=False)
        by_segment.to_excel(writer, sheet_name="By segment", index=False)
        by_product.to_excel(writer, sheet_name="By product", index=False)
        money = writer.book.add_format({"num_format": "#,##0.00"})
        for name in ("By segment", "By product"):
            writer.sheets[name].set_column(0, 0, 22)
            writer.sheets[name].set_column(1, 3, 16, money)
    return path


def write_markdown(path, month, headlines, by_segment, checks):
    lines_out = [f"# Riverstone sales — {month}", "",
                 f"_Generated {datetime.now():%d %b %Y %H:%M}_", "", "## Headlines", ""]
    lines_out += [f"- **{k.replace('_', ' ').title()}:** {v:,}" if isinstance(v, (int, float)) else f"- **{k}:** {v}"
                  for k, v in headlines.items()]
    lines_out += ["", "## By segment", "", by_segment.to_markdown(index=False), "", "## Checks", ""]
    lines_out += [f"- {'PASS' if ok else 'FAIL'} — {name} ({detail})" for name, ok, detail in checks]
    Path(path).write_text("\n".join(lines_out) + "\n", encoding="utf-8")
    return path


def main(month, out_dir):
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s", datefmt="%H:%M:%S")
    url = os.environ.get("RIVERSTONE_DB")
    if not url:
        log.error("RIVERSTONE_DB is not set")
        return 2
    out = Path(out_dir); out.mkdir(parents=True, exist_ok=True)
    engine = create_engine(url)

    log.info("loading %s", month)
    lines, target = load(engine, month)
    checks = check(lines, month)
    for name, ok, detail in checks:
        (log.info if ok else log.error)("check %s: %s (%s)", name, "PASS" if ok else "FAIL", detail)
    if not all(ok for _, ok, _ in checks):
        log.error("checks failed; no report written")
        return 1

    headlines, by_segment = summarize(lines, target)
    xlsx = write_excel(out / f"riverstone_{month}.xlsx", headlines, by_segment, lines)
    md = write_markdown(out / f"riverstone_{month}.md", month, headlines, by_segment, checks)
    log.info("wrote %s and %s", xlsx.name, md.name)
    print(f"{month}: net revenue {headlines['net_revenue']:,.2f} from {headlines['orders']:,} orders "
          f"({headlines['pct_of_target']}% of target)")
    return 0


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("month", help="the month to report, as YYYY-MM")
    ap.add_argument("--out", default="reports", help="output folder")
    args = ap.parse_args()
    raise SystemExit(main(args.month, args.out))
