"""Riverstone monthly sales report: database, checks, Excel workbook, Markdown summary.

Usage:  python monthly_report.py 2025-12 [--out reports]
Needs:  RIVERSTONE_DB, a SQLAlchemy database URL, in the environment or in a .env file.
"""
import argparse
import logging
import os
from datetime import datetime
from pathlib import Path

import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

log = logging.getLogger("monthly_report")

QUERY = text("""
    SELECT s.order_date, s.order_id, s.customer_id, c.segment, p.product_name,
           s.quantity, s.net_revenue, s.product_cost
    FROM sales_lines s
    JOIN customers c ON c.customer_id = s.customer_id
    JOIN products  p ON p.product_id  = s.product_id
    WHERE s.order_date >= :start AND s.order_date < :end
""")
TARGET_QUERY = text("SELECT target_revenue FROM sales_targets WHERE target_month = :month")


def month_range(month):
    """Return the first day of the month, and the first day of the next month."""
    start = pd.Timestamp(month + "-01")
    end = start + pd.offsets.MonthBegin(1)
    return start.date(), end.date()


def load(engine, month):
    """Return the month's order lines, the same month last year, and the month's target (or None)."""
    start, end = month_range(month)
    lines = pd.read_sql(QUERY, engine, params={"start": start, "end": end}, parse_dates=["order_date"])
    last_start, last_end = month_range(f"{start.year - 1}-{start.month:02d}")
    last_year = pd.read_sql(QUERY, engine, params={"start": last_start, "end": last_end})
    target = pd.read_sql(TARGET_QUERY, engine, params={"month": start})
    target_value = float(target["target_revenue"].iloc[0]) if len(target) > 0 else None
    return lines, last_year, target_value


def check(lines, last_year, month):
    """Return a list of (name, passed, detail) checks. The report is written only if all pass."""
    if len(lines) == 0:
        return [("rows returned", False, "0 lines")]
    revenue = lines["net_revenue"].sum()
    last = last_year["net_revenue"].sum()
    change = (revenue / last - 1) * 100 if last > 0 else None
    months_found = list(lines["order_date"].dt.strftime("%Y-%m").unique())
    return [
        ("rows returned", True, f"{len(lines):,} lines"),
        ("all dates inside the month", months_found == [month], ", ".join(months_found)),
        ("no missing revenue", bool(lines["net_revenue"].notna().all()), f"{lines['net_revenue'].isna().sum()} missing"),
        ("all quantities positive", bool((lines["quantity"] > 0).all()), f"smallest {lines['quantity'].min()}"),
        ("every line has a customer", bool(lines["customer_id"].notna().all()), f"{lines['customer_id'].nunique():,} customers"),
        ("within 50% of last year", change is not None and abs(change) <= 50,
         "no sales last year" if change is None else f"{change:+.1f}%"),
    ]


def summarize(lines, target):
    """Return the headline numbers (a dictionary) and revenue by segment (a table)."""
    revenue = float(lines["net_revenue"].sum())
    orders = int(lines["order_id"].nunique())
    headlines = {
        "Net revenue (₹)": round(revenue, 2),
        "Orders": orders,
        "Customers": int(lines["customer_id"].nunique()),
        "Average order value (₹)": round(revenue / orders, 2),
        "Gross margin (%)": round((1 - float(lines["product_cost"].sum()) / revenue) * 100, 1),
        "Share of target (%)": round(revenue / target * 100, 1) if target else None,
    }
    by_segment = (lines.groupby("segment", as_index=False)
                       .agg(net_revenue=("net_revenue", "sum"), orders=("order_id", "nunique"))
                       .sort_values("net_revenue", ascending=False))
    return headlines, by_segment


def write_excel(path, headlines, by_segment, lines):
    """Write a three-sheet workbook: headlines, revenue by segment, and revenue by product."""
    by_product = (lines.groupby("product_name", as_index=False)["net_revenue"].sum()
                       .sort_values("net_revenue", ascending=False))
    headline_table = pd.DataFrame({"measure": list(headlines), "value": list(headlines.values())})
    with pd.ExcelWriter(path, engine="xlsxwriter") as writer:
        headline_table.to_excel(writer, sheet_name="Headlines", index=False)
        by_segment.to_excel(writer, sheet_name="By segment", index=False)
        by_product.to_excel(writer, sheet_name="By product", index=False)
        money = writer.book.add_format({"num_format": "#,##0.00"})
        writer.sheets["Headlines"].set_column(0, 1, 26)
        for name in ("By segment", "By product"):
            writer.sheets[name].set_column(0, 0, 22)
            writer.sheets[name].set_column(1, 1, 18, money)
    return path


def write_markdown(path, month, headlines, by_segment, checks):
    """Write a short Markdown summary that a person can read in an email."""
    out = [f"# Riverstone sales, {month}", "", f"_Generated {datetime.now():%d %b %Y %H:%M}_", "", "## Headlines", ""]
    for name, value in headlines.items():
        shown = "not available" if value is None else f"{value:,}"
        out.append(f"- **{name}:** {shown}")
    out += ["", "## By segment", "", by_segment.to_markdown(index=False, floatfmt=",.2f"), "", "## Checks", ""]
    for name, ok, detail in checks:
        out.append(f"- {'PASS' if ok else 'FAIL'}: {name} ({detail})")
    Path(path).write_text("\n".join(out) + "\n", encoding="utf-8")
    return path


def main(month, out_dir):
    """Run the report for one month. Return 0 if it worked, 1 if a check failed, 2 if it isn't set up."""
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s", datefmt="%H:%M:%S")
    load_dotenv()
    url = os.environ.get("RIVERSTONE_DB")
    if not url:
        log.error("RIVERSTONE_DB is not set")
        return 2
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    engine = create_engine(url)

    log.info("loading %s", month)
    lines, last_year, target = load(engine, month)
    checks = check(lines, last_year, month)
    for name, ok, detail in checks:
        if ok:
            log.info("check passed: %s (%s)", name, detail)
        else:
            log.error("check FAILED: %s (%s)", name, detail)
    if not all([ok for name, ok, detail in checks]):
        log.error("checks failed; no report written")
        return 1

    headlines, by_segment = summarize(lines, target)
    xlsx = write_excel(out / f"riverstone_{month}.xlsx", headlines, by_segment, lines)
    md = write_markdown(out / f"riverstone_{month}.md", month, headlines, by_segment, checks)
    log.info("wrote %s and %s", xlsx.name, md.name)
    print(f"{month}: net revenue {headlines['Net revenue (₹)']:,.2f} from {headlines['Orders']:,} orders")
    return 0


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Riverstone monthly sales report")
    parser.add_argument("month", help="the month to report, as YYYY-MM")
    parser.add_argument("--out", default="reports", help="the folder to write the files to")
    args = parser.parse_args()
    raise SystemExit(main(args.month, args.out))
