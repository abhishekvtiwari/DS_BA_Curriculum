"""Riverstone Daily Sales Flash: SQL -> pandas -> an HTML email with KPI tiles, a chart and a table.

Usage:
    python daily_flash.py                  # today in India: build the email and write a preview to out/
    python daily_flash.py 2025-12-18       # a given day, as YYYY-MM-DD
    python daily_flash.py --send           # build it and send it (what the scheduler runs)

Settings come from a .env file in this folder (copy .env.example to .env and fill it in):
    RIVERSTONE_DB, SMTP_HOST, SMTP_PORT, SMTP_USER, SMTP_PASSWORD, FLASH_TO, FLASH_FAILURE_TO

Exit codes: 0 sent or previewed (including "no sales recorded"), 1 a check failed, 2 the job crashed.

Analyst to Architect, Chapter 20. Riverstone Supplies is fictional; every name and number is invented.
"""
from __future__ import annotations

import argparse
import base64
import logging
import mimetypes
import os
import smtplib
import sys
import time
import traceback
from datetime import date, datetime, timedelta
from email.message import EmailMessage
from io import BytesIO
from pathlib import Path
from zoneinfo import ZoneInfo

import matplotlib
matplotlib.use("Agg")                      # draw to a file, not a window
import matplotlib.pyplot as plt
import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

log = logging.getLogger("flash")

IST = ZoneInfo("Asia/Kolkata")
INK, MUTED, ACC, GOOD, BAD, LIGHT = "#1d2330", "#5b6475", "#0f5c8c", "#2f7d6d", "#b23b3b", "#dfe5ec"
LOW_SALES_THRESHOLD = 500        # units: a product selling fewer than this in a day is flagged
MEDIAN_BAND = 0.6                # today's revenue must be within 60% of the recent median
CHART_CID = "flash-chart@riverstone"

DAY_SQL = text("""
    SELECT s.order_date, s.order_id, s.customer_id, p.product_name,
           c.segment, s.quantity, s.net_revenue, s.product_cost
    FROM sales_lines s
    JOIN products  p ON p.product_id  = s.product_id
    JOIN customers c ON c.customer_id = s.customer_id
    WHERE s.order_date = :day
""")

DAILY_SQL = text("""
    SELECT s.order_date, SUM(s.net_revenue) AS net_revenue
    FROM sales_lines s
    WHERE s.order_date BETWEEN :start AND :end
    GROUP BY s.order_date ORDER BY s.order_date
""")


# ---------------------------------------------------------------- data

def daily(engine, start: date, end: date) -> pd.DataFrame:
    """Revenue per day from start to end, both included."""
    return pd.read_sql(DAILY_SQL, engine, params={"start": start, "end": end}, parse_dates=["order_date"])


def load(engine, day: date):
    """Today's lines; the 14 days before today; the 14 days ending today; the same day last year; month to date."""
    lines = pd.read_sql(DAY_SQL, engine, params={"day": day}, parse_dates=["order_date"])
    previous = daily(engine, day - timedelta(days=14), day - timedelta(days=1))
    trend = daily(engine, day - timedelta(days=13), day)
    last_year = daily(engine, day.replace(year=day.year - 1), day.replace(year=day.year - 1))
    month_to_date = daily(engine, day.replace(day=1), day)   # the 1st of the month, worked out in Python
    return lines, previous, trend, last_year, month_to_date


def checks(lines: pd.DataFrame, day: date, previous: pd.DataFrame) -> list[tuple[str, bool, str]]:
    """Return (name, passed, detail) for each check. Any failure means no email."""
    revenue = float(lines["net_revenue"].sum())
    median_recent = float(previous["net_revenue"].median())
    return [
        ("rows returned", len(lines) > 0, f"{len(lines):,} lines"),
        ("all rows are today's", bool((lines["order_date"].dt.date == day).all()), str(day)),
        ("no missing revenue", bool(lines["net_revenue"].notna().all()),
         f"{int(lines['net_revenue'].isna().sum())} missing"),
        (f"revenue within {MEDIAN_BAND:.0%} of recent median", abs(revenue / median_recent - 1) < MEDIAN_BAND,
         f"₹{revenue:,.0f} vs median ₹{median_recent:,.0f}"),
    ]


def headlines(lines: pd.DataFrame, last_year: pd.DataFrame, month_to_date: pd.DataFrame) -> dict:
    revenue = float(lines["net_revenue"].sum())
    ly = float(last_year["net_revenue"].sum()) if len(last_year) else 0.0
    return {
        "revenue": revenue,
        "orders": int(lines["order_id"].nunique()),
        "customers": int(lines["customer_id"].nunique()),
        "average_order_value": revenue / max(lines["order_id"].nunique(), 1),
        "gross_margin_pct": (1 - float(lines["product_cost"].sum()) / revenue) * 100 if revenue else 0.0,
        "vs_last_year_pct": (revenue / ly - 1) * 100 if ly else None,
        "month_to_date": float(month_to_date["net_revenue"].sum()),
    }


def exceptions(lines: pd.DataFrame) -> pd.DataFrame:
    """Products whose quantity sold today is below the threshold: the 'tell me what's wrong' list."""
    by_product = lines.groupby("product_name", as_index=False)["quantity"].sum()
    low = by_product[by_product["quantity"] < LOW_SALES_THRESHOLD].sort_values("quantity")
    return low.reset_index(drop=True)


# ---------------------------------------------------------------- chart

def style_axes(ax, title, ylabel=None):
    """Chapter 18's chart rules: left-aligned action title, no top/right spines, light gridlines."""
    ax.set_title(title, loc="left", fontweight="bold", color=INK, fontsize=10)
    if ylabel:
        ax.set_ylabel(ylabel, color=MUTED)
    ax.spines[["top", "right"]].set_visible(False)
    ax.grid(axis="y", color=LIGHT, linewidth=0.8)
    ax.set_axisbelow(True)
    return ax


def trend_title(trend: pd.DataFrame, day: date) -> str:
    """An action title: where today sits in the last 14 days."""
    lakh = trend["net_revenue"].astype(float) / 1e5
    today = float(lakh[trend["order_date"].dt.date == day].sum())
    below, above = int((lakh < today).sum()), int((lakh > today).sum())
    place = {0: "the lowest", 1: "the second-lowest", 2: "the third-lowest"}.get(below)
    if place is None:
        place = {0: "the highest", 1: "the second-highest", 2: "the third-highest"}.get(above, "a middling")
    return f"{day:%d %b}, at ₹{today:.1f} lakh, was {place} day of the last 14"


def trend_chart(trend: pd.DataFrame, title: str) -> bytes:
    """Return the 14-day revenue chart as PNG bytes."""
    fig, ax = plt.subplots(figsize=(6.4, 2.3))
    ax.plot(trend["order_date"], trend["net_revenue"].astype(float) / 1e5, color=ACC, linewidth=2.2)
    style_axes(ax, title, "₹ lakh")
    ax.set_ylim(0, float(trend["net_revenue"].max()) / 1e5 * 1.2)
    ax.tick_params(labelsize=8, colors=MUTED)
    fig.autofmt_xdate(rotation=0, ha="center")
    buffer = BytesIO()                                  # a file that lives in memory
    fig.savefig(buffer, format="png", dpi=150, bbox_inches="tight")
    plt.close(fig)
    return buffer.getvalue()


# ---------------------------------------------------------------- HTML

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


def build_html(day: date, head: dict, by_segment: pd.DataFrame, low: pd.DataFrame,
               img_src: str, chart_alt: str) -> str:
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
                           f"No products sold below {LOW_SALES_THRESHOLD} units today.</p>")
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
      <img src="{img_src}" width="620" alt="{chart_alt}" style="display:block"></td></tr>
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


def no_data_email(day: date) -> tuple[str, str]:
    """The 'no data today' email: short, honest, unmistakable."""
    subject = f"Riverstone Daily Flash — {day:%d %b %Y} — no sales recorded"
    html = (f"<p style='font:14px Arial,sans-serif'>No sales were recorded on {day:%d %b %Y}.</p>"
            f"<p style='font:12px Arial,sans-serif;color:{MUTED}'>If that looks wrong, check the overnight load.</p>")
    return subject, html


# ---------------------------------------------------------------- mail

def build_message(subject: str, html: str, to: list[str], png: bytes | None = None,
                  attachments=()) -> EmailMessage:
    """A multipart email: plain text, HTML, the chart as a related image, and any attachments."""
    message = EmailMessage()
    message["Subject"] = subject
    message["From"] = os.environ["SMTP_USER"]
    message["To"] = ", ".join(to)
    message.set_content("This report needs an HTML-capable email client.")   # plain-text fallback
    message.add_alternative(html, subtype="html")
    if png is not None:
        html_part = message.get_payload()[1]
        html_part.add_related(png, maintype="image", subtype="png", cid=f"<{CHART_CID}>")
    for path in attachments:
        kind, _ = mimetypes.guess_type(path)
        maintype, subtype = (kind or "application/octet-stream").split("/")
        with open(path, "rb") as f:
            data = f.read()
        message.add_attachment(data, maintype=maintype, subtype=subtype, filename=Path(path).name)
    return message


def send_message(message: EmailMessage) -> dict:
    """Send by SMTP. With a password set, upgrade to encryption (STARTTLS) and log in first."""
    with smtplib.SMTP(os.environ["SMTP_HOST"], int(os.environ["SMTP_PORT"]), timeout=30) as smtp:
        if os.environ.get("SMTP_PASSWORD"):
            smtp.starttls()
            smtp.login(os.environ["SMTP_USER"], os.environ["SMTP_PASSWORD"])
        return smtp.send_message(message)


def alert_failure(subject: str, detail: str) -> None:
    """Tell a person when the job fails. Never fail silently."""
    to = os.environ.get("FLASH_FAILURE_TO")
    if not to:
        log.error("FLASH_FAILURE_TO is not set, so nobody was alerted")
        return
    html = f"<pre style='font:12px monospace'>{detail}</pre>"
    send_message(build_message(subject, html, [to]))


# ---------------------------------------------------------------- running it

def recipients() -> list[str]:
    return [address.strip() for address in os.environ["FLASH_TO"].split(",") if address.strip()]


def already_sent(run_key: str, path: Path = Path("runs/sent_keys.txt")) -> bool:
    return path.exists() and run_key in path.read_text(encoding="utf-8").split()


def record_sent(run_key: str, path: Path = Path("runs/sent_keys.txt")) -> None:
    path.parent.mkdir(exist_ok=True)
    with open(path, "a", encoding="utf-8") as f:
        f.write(run_key + "\n")


def wait_for_load(engine, day: date, until: str = "08:30", pause_minutes: int = 10) -> None:
    """Wait until the load_status table says the overnight load for `day` finished."""
    deadline = datetime.combine(datetime.now(IST).date(), datetime.strptime(until, "%H:%M").time(), IST)
    query = text("SELECT 1 FROM load_status WHERE load_date = :day AND status = 'finished'")
    while True:
        with engine.connect() as conn:
            if conn.execute(query, {"day": day}).first():
                return
        if datetime.now(IST) >= deadline:
            raise RuntimeError(f"the overnight load for {day} had not finished by {until}")
        log.info("load for %s not finished; waiting %s minutes", day, pause_minutes)
        time.sleep(pause_minutes * 60)


def setup_logging() -> None:
    """Log lines go to the screen (stderr) without times, and to logs/flash.log with times."""
    Path("logs").mkdir(exist_ok=True)
    screen = logging.StreamHandler()
    screen.setFormatter(logging.Formatter("%(levelname)s %(message)s"))
    logfile = logging.FileHandler("logs/flash.log", encoding="utf-8")
    logfile.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(message)s", datefmt="%Y-%m-%dT%H:%M:%S"))
    logging.basicConfig(level=logging.INFO, handlers=[screen, logfile], force=True)


def parse_args(argv=None):
    parser = argparse.ArgumentParser(description="Riverstone Daily Sales Flash")
    parser.add_argument("day", nargs="?", default=None, help="the day to report, YYYY-MM-DD (default: today in India)")
    parser.add_argument("--send", action="store_true", help="actually send the email")
    parser.add_argument("--wait-for-load", action="store_true", help="wait for the load_status row first")
    return parser.parse_args(argv)


def main(argv=None) -> int:
    args = parse_args(argv)
    day = date.fromisoformat(args.day) if args.day else datetime.now(IST).date()
    setup_logging()
    load_dotenv()                                        # .env in this folder -> os.environ
    run_key = f"flash_{day}"
    if args.send and already_sent(run_key):
        log.info("%s already sent; nothing to do", run_key)
        return 0
    try:
        engine = create_engine(os.environ["RIVERSTONE_DB"])
        if args.wait_for_load:
            wait_for_load(engine, day)
        lines, previous, trend, last_year, month_to_date = load(engine, day)
        log.info("loaded %s lines for %s", len(lines), day)
        png = None
        if lines.empty:                                  # the "no data today" branch
            log.warning("no sales lines for %s", day)
            subject, html = no_data_email(day)
            preview = html
        else:
            results = checks(lines, day, previous)
            failed = [f"{name} ({detail})" for name, passed, detail in results if not passed]
            if failed:
                log.error("check failed: %s", "; ".join(failed))
                alert_failure(f"Riverstone Daily Flash {day} NOT sent: a check failed", "\n".join(failed))
                return 1
            head = headlines(lines, last_year, month_to_date)
            by_segment = (lines.groupby("segment", as_index=False)
                               .agg(net_revenue=("net_revenue", "sum"), orders=("order_id", "nunique"))
                               .sort_values("net_revenue", ascending=False))
            low = exceptions(lines)
            title = trend_title(trend, day)
            png = trend_chart(trend, title)
            html = build_html(day, head, by_segment, low, f"cid:{CHART_CID}", title)
            data_uri = "data:image/png;base64," + base64.b64encode(png).decode("ascii")
            preview = html.replace(f"cid:{CHART_CID}", data_uri)       # a browser can't see cid: images
            subject = f"Riverstone Daily Flash — {day:%d %b %Y} — ₹{head['revenue']:,.0f}"
            if head["vs_last_year_pct"] is not None:
                subject += f" ({head['vs_last_year_pct']:+.1f}% vs LY)"
            log.info("revenue %.0f, orders %s, exceptions %s", head["revenue"], head["orders"], len(low))

        Path("out").mkdir(exist_ok=True)
        path = Path("out") / f"daily_flash_{day}.html"
        path.write_text(preview, encoding="utf-8")
        log.info("wrote %s", path)
        if args.send:
            to = recipients()
            send_message(build_message(subject, html, to, png))
            record_sent(run_key)
            log.info("sent to %s recipient(s)", len(to))
        else:
            print(subject)
        return 0

    except Exception:                                     # the job must alert a person, then fail
        log.exception("daily flash failed")
        try:
            alert_failure(f"FAILED: Riverstone Daily Flash {day}", traceback.format_exc())
        except Exception:
            log.error("the failure alert could not be sent either")
        return 2


if __name__ == "__main__":
    sys.exit(main())
