"""Riverstone Daily Sales Flash: SQL -> pandas -> an HTML email with KPI tiles, a table and a chart.

Usage:
    python daily_flash.py 2025-12-18                 # build the email and write it to out/
    python daily_flash.py 2025-12-18 --send          # build it and send it (needs SMTP settings)

Environment:
    RIVERSTONE_DB   SQLAlchemy URL, e.g. postgresql+psycopg://user:pw@host:5432/riverstone_full
    SMTP_HOST, SMTP_PORT, SMTP_USER, SMTP_PASSWORD, FLASH_TO, FLASH_FAILURE_TO

Analyst to Architect, Chapter 20. Riverstone Supplies is fictional; every name and number is invented.
"""
from __future__ import annotations

import argparse
import base64
import logging
import os
import smtplib
import sys
from datetime import date, timedelta
from email.message import EmailMessage
from io import BytesIO
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd
from sqlalchemy import create_engine, text

log = logging.getLogger("daily_flash")

INK, MUTED, ACC, GOOD, BAD, LIGHT = "#1d2330", "#5b6475", "#0f5c8c", "#2f7d6d", "#b23b3b", "#dfe5ec"
LOW_STOCK_THRESHOLD = 500         # units: a product selling less than this in a day is flagged

DAY_SQL = text("""
    SELECT s.order_date, s.order_id, s.customer_id, s.product_id, p.product_name,
           c.segment, c.city, s.quantity, s.net_revenue, s.product_cost
    FROM sales_lines s
    JOIN products  p ON p.product_id  = s.product_id
    JOIN customers c ON c.customer_id = s.customer_id
    WHERE s.order_date = :day
""")

RANGE_SQL = text("""
    SELECT s.order_date, SUM(s.net_revenue) AS net_revenue
    FROM sales_lines s WHERE s.order_date BETWEEN :start AND :day
    GROUP BY s.order_date ORDER BY s.order_date
""")


def load(engine, day: date):
    """Return today's lines, the last 14 days of daily revenue, the same day last year, and month to date."""
    lines = pd.read_sql(DAY_SQL, engine, params={"day": day}, parse_dates=["order_date"])
    trend = pd.read_sql(RANGE_SQL, engine, params={"start": day - timedelta(days=13), "day": day},
                        parse_dates=["order_date"])
    last_year = pd.read_sql(RANGE_SQL, engine,
                            params={"start": day.replace(year=day.year - 1), "day": day.replace(year=day.year - 1)},
                            parse_dates=["order_date"])
    mtd = pd.read_sql(RANGE_SQL, engine, params={"start": day.replace(day=1), "day": day},
                      parse_dates=["order_date"])
    return lines, trend, last_year, mtd


def headlines(lines: pd.DataFrame, last_year: pd.DataFrame, mtd_rows: pd.DataFrame) -> dict:
    revenue = float(lines["net_revenue"].sum())
    ly = float(last_year["net_revenue"].sum()) if len(last_year) else 0.0
    mtd = float(mtd_rows["net_revenue"].sum())
    return {
        "revenue": revenue,
        "orders": int(lines["order_id"].nunique()),
        "customers": int(lines["customer_id"].nunique()),
        "average_order_value": revenue / max(lines["order_id"].nunique(), 1),
        "gross_margin_pct": (1 - lines["product_cost"].sum() / revenue) * 100 if revenue else 0.0,
        "vs_last_year_pct": (revenue / ly - 1) * 100 if ly else None,
        "month_to_date": mtd,
    }


def exceptions(lines: pd.DataFrame) -> pd.DataFrame:
    """Products whose quantity sold today is below the threshold: the 'tell me what's wrong' list."""
    by_product = lines.groupby("product_name", as_index=False)["quantity"].sum()
    low = by_product[by_product["quantity"] < LOW_STOCK_THRESHOLD].sort_values("quantity")
    return low.reset_index(drop=True)


def trend_chart(trend: pd.DataFrame) -> str:
    """Return a base64 PNG of the 14-day revenue trend, for embedding in the email."""
    fig, ax = plt.subplots(figsize=(6.4, 2.1))
    ax.plot(trend["order_date"], trend["net_revenue"] / 1e5, color=ACC, linewidth=2.2)
    ax.fill_between(trend["order_date"], trend["net_revenue"] / 1e5, color=ACC, alpha=0.08)
    ax.set_ylim(0, max(trend["net_revenue"] / 1e5) * 1.25)
    ax.set_ylabel("₹ lakh", color=MUTED, fontsize=8)
    ax.tick_params(labelsize=8, colors=MUTED)
    ax.spines[["top", "right"]].set_visible(False)
    ax.grid(axis="y", color=LIGHT, linewidth=0.8)
    ax.set_axisbelow(True)
    fig.autofmt_xdate(rotation=0, ha="center")
    buffer = BytesIO()
    fig.savefig(buffer, format="png", dpi=150, bbox_inches="tight")
    plt.close(fig)
    return base64.b64encode(buffer.getvalue()).decode("ascii")


def tile(label: str, value: str, note: str = "", note_color: str = MUTED) -> str:
    return (
        f'<td style="padding:0 8px 0 0;vertical-align:top">'
        f'<table role="presentation" cellpadding="0" cellspacing="0" width="100%" '
        f'style="background:#f3f6fa;border:1px solid {LIGHT};border-radius:6px">'
        f'<tr><td style="padding:10px 12px">'
        f'<div style="font:12px Arial,sans-serif;color:{MUTED}">{label}</div>'
        f'<div style="font:bold 20px Arial,sans-serif;color:{INK};padding-top:2px">{value}</div>'
        f'<div style="font:12px Arial,sans-serif;color:{note_color};padding-top:2px">{note}</div>'
        f"</td></tr></table></td>"
    )


def build_html(day: date, head: dict, by_segment: pd.DataFrame, low: pd.DataFrame, chart_b64: str) -> str:
    vs_ly = head["vs_last_year_pct"]
    vs_text = "—" if vs_ly is None else f"{vs_ly:+.1f}% vs last year"
    vs_color = GOOD if (vs_ly or 0) >= 0 else BAD

    rows = "".join(
        f'<tr><td style="padding:6px 12px;border-bottom:1px solid {LIGHT};font:13px Arial,sans-serif">{r.segment}</td>'
        f'<td style="padding:6px 12px;border-bottom:1px solid {LIGHT};font:13px Arial,sans-serif;text-align:right">'
        f'₹{r.net_revenue:,.0f}</td>'
        f'<td style="padding:6px 12px;border-bottom:1px solid {LIGHT};font:13px Arial,sans-serif;text-align:right">'
        f'{r.orders:,}</td></tr>'
        for r in by_segment.itertuples()
    )

    if low.empty:
        exception_block = (f'<p style="font:13px Arial,sans-serif;color:{GOOD}">'
                           f"No products sold below {LOW_STOCK_THRESHOLD} units today.</p>")
    else:
        items = "".join(f"<li>{r.product_name}: {int(r.quantity)} units</li>" for r in low.itertuples())
        exception_block = (
            f'<div style="border-left:4px solid {BAD};background:#fdf3f3;padding:8px 12px;margin:8px 0">'
            f'<div style="font:bold 13px Arial,sans-serif;color:{BAD}">Exception: low movement</div>'
            f'<ul style="font:13px Arial,sans-serif;color:{INK};margin:6px 0 0 18px;padding:0">{items}</ul></div>')

    return f"""<html><body style="margin:0;padding:16px;background:#ffffff">
<table role="presentation" cellpadding="0" cellspacing="0" width="640" style="width:640px">
  <tr><td style="font:bold 18px Arial,sans-serif;color:{INK};padding-bottom:2px">
      Riverstone Daily Sales Flash — {day:%d %b %Y}</td></tr>
  <tr><td style="font:12px Arial,sans-serif;color:{MUTED};padding-bottom:12px">
      Net revenue excludes cancelled orders. Generated automatically from the sales database.</td></tr>
  <tr><td>
    <table role="presentation" cellpadding="0" cellspacing="0" width="100%"><tr>
      {tile("Net revenue", f"₹{head['revenue']:,.0f}", vs_text, vs_color)}
      {tile("Orders", f"{head['orders']:,}", f"{head['customers']:,} customers")}
      {tile("Average order", f"₹{head['average_order_value']:,.0f}", f"margin {head['gross_margin_pct']:.1f}%")}
      {tile("Month to date", f"₹{head['month_to_date']/1e7:,.2f} cr", "including today")}
    </tr></table>
  </td></tr>
  <tr><td style="padding-top:16px">
      <div style="font:bold 14px Arial,sans-serif;color:{INK};padding-bottom:6px">Last 14 days</div>
      <img src="data:image/png;base64,{chart_b64}" width="620" alt="Daily net revenue, last 14 days" style="display:block"></td></tr>
  <tr><td style="padding-top:16px">
      <div style="font:bold 14px Arial,sans-serif;color:{INK};padding-bottom:6px">Today by segment</div>
      <table role="presentation" cellpadding="0" cellspacing="0" width="100%" style="border-collapse:collapse">
        <tr><th style="text-align:left;font:bold 12px Arial,sans-serif;color:{MUTED};padding:0 12px 4px">Segment</th>
            <th style="text-align:right;font:bold 12px Arial,sans-serif;color:{MUTED};padding:0 12px 4px">Net revenue</th>
            <th style="text-align:right;font:bold 12px Arial,sans-serif;color:{MUTED};padding:0 12px 4px">Orders</th></tr>
        {rows}
      </table></td></tr>
  <tr><td style="padding-top:12px">{exception_block}</td></tr>
  <tr><td style="font:11px Arial,sans-serif;color:{MUTED};padding-top:16px">
      Sent by daily_flash.py · questions to the analytics team · to stop receiving this, reply STOP.</td></tr>
</table></body></html>"""


def send_email(subject: str, html: str, to: list[str]) -> None:
    """Send the flash by SMTP. Credentials come from the environment, never from the code."""
    message = EmailMessage()
    message["Subject"] = subject
    message["From"] = os.environ["SMTP_USER"]
    message["To"] = ", ".join(to)
    message.set_content("This report needs an HTML-capable email client.")
    message.add_alternative(html, subtype="html")

    with smtplib.SMTP(os.environ["SMTP_HOST"], int(os.environ.get("SMTP_PORT", 587))) as smtp:
        smtp.starttls()
        smtp.login(os.environ["SMTP_USER"], os.environ["SMTP_PASSWORD"])
        smtp.send_message(message)


def alert_failure(subject: str, detail: str) -> None:
    """Tell the owner when the job fails. Never fail silently."""
    to = os.environ.get("FLASH_FAILURE_TO")
    if not to:
        log.error("no FLASH_FAILURE_TO set; failure not alerted: %s", detail)
        return
    send_email(subject, f"<pre style='font:12px monospace'>{detail}</pre>", [to])


def main(day_text: str, out_dir: str, send: bool) -> int:
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s", datefmt="%H:%M:%S")
    day = date.fromisoformat(day_text)
    url = os.environ.get("RIVERSTONE_DB")
    if not url:
        log.error("RIVERSTONE_DB is not set")
        return 2

    try:
        engine = create_engine(url)
        lines, trend, last_year, mtd_rows = load(engine, day)

        if lines.empty:                                   # the "no data today" case
            log.warning("no sales lines for %s", day)
            html = (f"<p style='font:14px Arial'>No sales were recorded on {day:%d %b %Y}.</p>"
                    f"<p style='font:12px Arial;color:{MUTED}'>If that looks wrong, check the overnight load.</p>")
            subject = f"Riverstone Daily Flash — {day:%d %b %Y} — no sales recorded"
        else:
            head = headlines(lines, last_year, mtd_rows)
            by_segment = (lines.groupby("segment", as_index=False)
                               .agg(net_revenue=("net_revenue", "sum"), orders=("order_id", "nunique"))
                               .sort_values("net_revenue", ascending=False))
            low = exceptions(lines)
            html = build_html(day, head, by_segment, low, trend_chart(trend))
            subject = (f"Riverstone Daily Flash — {day:%d %b %Y} — ₹{head['revenue']:,.0f}"
                       + (f" ({head['vs_last_year_pct']:+.1f}% vs LY)" if head["vs_last_year_pct"] is not None else ""))
            log.info("revenue %.2f, orders %s, exceptions %s", head["revenue"], head["orders"], len(low))

        out = Path(out_dir); out.mkdir(parents=True, exist_ok=True)
        path = out / f"daily_flash_{day}.html"
        path.write_text(html, encoding="utf-8")
        log.info("wrote %s", path)

        if send:
            recipients = [address.strip() for address in os.environ["FLASH_TO"].split(",") if address.strip()]
            send_email(subject, html, recipients)
            log.info("sent to %s recipient(s)", len(recipients))
        else:
            print(subject)
        return 0

    except Exception as error:                            # noqa: BLE001 - the job must alert, then fail
        log.exception("daily flash failed")
        try:
            alert_failure(f"FAILED: Riverstone Daily Flash {day_text}", repr(error))
        except Exception:                                 # noqa: BLE001
            log.error("failure alert could not be sent either")
        return 1


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("day", help="the day to report, as YYYY-MM-DD")
    parser.add_argument("--out", default="out", help="folder for the rendered HTML")
    parser.add_argument("--send", action="store_true", help="actually send the email")
    args = parser.parse_args()
    raise SystemExit(main(args.day, args.out, args.send))
