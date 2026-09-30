# Chapter 20. Automating Reports & Delivering Insights

*Part 2 — The Analyst*

> **Chapter at a glance**
>
> **You will learn to:** place any report on the automation ladder and decide how far up it should go · map a report's flow and time its manual steps before automating anything · choose between VBA, Apps Script, Python, BI subscriptions, and low-code flows · produce the right output: formatted Excel, PDF, CSV, or the email body itself · build an HTML email with KPI tiles, a table, and a chart attached so that it shows in Outlook and Gmail · send mail safely from code with SMTP or a workspace API, with credentials in a `.env` file, and test it on a mail server on your own computer · schedule with Task Scheduler, cron, or a cloud scheduler, in the business's time zone · design exception reports and alerts that people don't learn to ignore · deliver to Teams, Slack, or WhatsApp · make an automation trustworthy: logging, checks, failure alerts, "no data today", retries, idempotency · manage recipients and confidentiality · document and hand over · measure what it saved.
>
> **Before you start:** Chapter 19 (spreadsheet automation, and its box "HTML in ten minutes" in section 19.7), Chapter 13 (the SQL the report runs on), Chapter 14 (checks on data), Chapter 15 (chart design), Chapter 16 (BI subscriptions), Chapter 18 (pandas and scripts), and the terminal basics from Chapter 17, section 17.0. The scheduling section uses a few more terminal pieces, each explained where it appears; Chapters 26 and 34 teach the terminal properly.
>
> **Time needed:** 20–25 hours, spread over two to three weeks. Allow two of those hours for setting up: the `.env` file, the local test mail server, and a scheduler.
>
> **Tools:** the Python you installed in Chapter 17 (section 17.0 sets the book's rule on Python versions), with `pandas`, `matplotlib`, `SQLAlchemy`, a database driver, `python-dotenv`, `requests` and `aiosmtpd` (a test mail server), plus `tzdata` on Windows; a mail account you're allowed to send from (SMTP, Microsoft 365, or Google Workspace) when you're ready to send for real; Windows Task Scheduler or cron. Optional: Power Automate, n8n, Make, or Zapier.
>
> **Practice data:** the `riverstone_full` database, and two files in `companion/ch20/`: `daily_flash.py`, the finished Daily Sales Flash, which builds the email in this chapter, and `.env.example`, the settings file you copy and fill in.

---

## Why this matters

An analysis nobody reads has the same value as an analysis nobody did. Delivery is not the packaging around the work; it's the part where the work turns into a decision.

Most analysts discover this the hard way. The report is right, the chart is clear, and it still fails: it lands at 11 a.m. when the meeting was at 9, or in an attachment nobody opens on a phone, or in an inbox where it looks like the eleven other reports that go unread. Or it arrives faithfully for six months and then quietly stops, and nobody notices for three weeks.

This chapter is about the last mile: getting the number in front of the right person, at the right time, in a form they'll act on, reliably enough that they stop thinking about where it comes from. It's also where an analyst's time comes back. A report that takes ninety minutes a day is about 47 working days a year; automating it buys back two months, and those months are what you spend on the analysis nobody has asked for yet.

The chapter builds one thing end to end: Riverstone's **Daily Sales Flash**, a database query that becomes an email with KPI tiles, a table, and a chart, sent every morning, with an exception alert when something is wrong and a failure alert when the job itself breaks.

---

## In plain English

Think about how a newspaper reaches a doorstep.

Someone writes the story (your analysis). Someone else decides what goes on page one (what the reader needs first). It's printed in a fixed format (the same layout every day, so readers know where to look). It's delivered at the same time every morning, whether or not anyone is awake at the press. And if the van breaks down, somebody knows within minutes, because a hundred people ring up.

An automated report is the same machine:

- **The press** is the script: it runs the same way every time.
- **Page one** is your KPI tiles: three or four numbers, in the same place, every day.
- **The delivery round** is scheduling and recipients.
- **The phone calls** are the failure alerts, except you don't wait for the readers to notice. The machine tells you first.

The mistake most first automations make is building a beautiful press with no phone. It works for weeks, then a source file changes name, and the report sends yesterday's numbers, or nothing at all, and everyone keeps trusting it until a decision goes wrong.

---

## 20.1 The automation ladder

![Five rungs: manual, refreshable, scheduled, triggered, self-serve, each with how it works and what it removes](figures/fig20-1-automation-ladder.svg)

*Figure 20.1 — Each rung removes a different kind of work. Most reports should stop at rung 3.*

| Rung | What it means | Right when |
|---|---|---|
| **1 Manual** | A person does every step | It's truly one-off, or the judgment is the work |
| **2 Refreshable** | The steps are recorded: Power Query, a saved query, a model | The shape is stable; the data changes |
| **3 Scheduled** | A script runs at a fixed time | The report is regular and the audience is fixed |
| **4 Triggered** | It runs when something happens: a file lands, a form is submitted, a threshold breaks | Waiting until tomorrow morning would be too late |
| **5 Self-serve** | People answer their own questions in a model or dashboard | The questions vary, and you're the bottleneck |

Three practical rules:

1. **Every rung above 2 needs an owner, a log, and a failure alert.** Automation converts a person's attention into a machine's silence; the alert is how you buy the attention back.
2. **Don't skip rung 2.** If the manual steps aren't stable, scheduling them only makes the same mistake happen faster, at 7 a.m., without anyone watching.
3. **Rung 5 is a different job.** Self-serve is a data model and a shared definition (Chapter 16), not a script. It's the right end state for the reports people ask about constantly, and overkill for the rest.

---

## 20.2 Map the flow before you automate

![A six-step flow from ERP export to email, with four steps marked MANUAL and one marked judgment, and a box explaining what the map shows](figures/fig20-2-report-flow.svg)

*Figure 20.2 — Map every step from source to reader, mark which are manual, and time them for a week.*

Before writing any code, draw the report's flow and answer five questions:

1. **Where does the data come from**, and when is it ready? (A report scheduled for 06:00 that reads a table loaded at 06:30 is worse than no report.)
2. **What happens to it**, step by step, and how long does each step take? Time them for a week; people consistently misjudge which step is slow.
3. **Which steps are mechanical and which are judgment?** Automate the mechanical ones. Keep the judgment, and give it a place in the output: a commentary box, three sentences, written by a human.
4. **Who reads it**, on what device, and what decision do they make? A branch manager reading on a phone at 8 a.m. needs four numbers; the finance analyst needs the workbook.
5. **What happens if it's wrong or late?** That tells you how much checking and alerting the automation deserves.

For Riverstone's Daily Flash, the map came out as: ERP loads at 02:00 (automatic) → an analyst opens four files (25 minutes) → cleans and combines (30 minutes) → pivots and charts (20 minutes) → writes three sentences of commentary (judgment) → emails 14 managers (5 minutes). Eighty minutes of mechanical work, three sentences worth keeping.

---

## 20.3 Choosing the delivery tool

| If the work is… | Use | Because |
|---|---|---|
| Inside one workbook, on a desktop | **VBA** (Chapter 19) | It's already there; formatting, PDF, Outlook |
| Inside Google Sheets, with forms and triggers | **Apps Script** (Chapter 19) | Triggers and email are built in, and it runs in the cloud |
| From a database or API, or needs real transformation | **Python** (Chapter 18) | Anything else fights you |
| An existing BI report | **Power BI subscriptions and alerts** (Chapter 16) | No code, and the model is already governed |
| Gluing SaaS tools together, owned by the business | **Power Automate, n8n, Make, Zapier** | Non-developers can maintain them |
| A pipeline with dependencies and retries | **An orchestrator** (Chapter 46) | Scheduling is not the same as orchestration |

Two decision rules that save arguments:

- **Follow the data.** If the numbers live in a database, the automation belongs where the database is simple to reach, which usually means Python on a server, not a macro on a laptop.
- **Follow the maintainer.** An automation nobody but you can change is a risk. Sometimes the right answer is the slightly worse tool that the team can maintain, and that is a legitimate engineering decision, not a compromise.

> **Watch out: the laptop trap.** Task Scheduler on your own machine is the most common first home for an automation, and it fails when you're on leave, when the laptop sleeps, when IT pushes an update, and when you change jobs. It's fine for a week while you prove the value. Then ask for a server, a VM, a container, or a cloud scheduler.

---

## 20.4 Output formats: what to send

| Format | Good for | Costs the reader |
|---|---|---|
| **Email body (HTML)** | Daily numbers, alerts, anything read on a phone | Nothing: it's already open |
| **Formatted Excel** | Figures people will slice, filter, or paste into a deck | A download and an app |
| **PDF** | A fixed record: board packs, statements, anything signed off | Can't be reworked; often unread on phones |
| **CSV** | Feeding another system | Useless to humans |
| **A link to a dashboard** | Exploration, many questions | A login, and a licence (Chapter 16) |

The rule that matters more than the format: **put the answer in the body.** An attachment is a request; a body is an answer. If someone must open a file to learn whether today was good, most of them won't. Send the four numbers in the email and attach the workbook for the two people who want it.

Riverstone's Flash does exactly that: KPI tiles and a table in the body, and (in the project's stretch version) the detailed workbook attached for the finance analyst who reconciles it.

---

## 20.5 The report as an email

Email clients are not browsers. Classic Outlook for Windows renders HTML with Microsoft Word's engine (the new Outlook uses a browser engine, but design for the older one while both are in use); Gmail strips some CSS; phones are 360 pixels wide. What survives everywhere is 2005-era HTML:

- **Tables for layout**, not flexbox or grid, and a fixed width of about 600–640 pixels.
- **Inline styles** (`style="…"` on each element), because `<style>` blocks and external stylesheets are often stripped.
- **Web-safe fonts** (Arial, Segoe UI, Helvetica) with fallbacks; no web fonts.
- **Images with a `width` attribute and `alt` text**, because many clients block images by default: the email must still make sense with every image missing.
- **No JavaScript**, ever. It's stripped, and it would be a security problem if it weren't.

### What it looks like

This section and the next build one email: the finished Flash, made by `companion/ch20/daily_flash.py` and shown in Figure 20.3 as the recipients see it, with its subject line above it.

![The Riverstone Daily Sales Flash email under its subject line: a title, four KPI tiles (net revenue ₹2,511,819 up 2.3% on last year, 118 orders from 116 customers, average order ₹21,287 at 27.3% margin, month to date ₹5.71 crore), a 14-day revenue line chart titled "18 Dec, at ₹25.1 lakh, was the second-lowest day of the last 14", a table of today's revenue by segment, and a red low-movement exception box for Industrial Crate, 345 units](figures/fig20-3-daily-flash-email.png)

*Figure 20.3 — Riverstone's Daily Sales Flash for 18 December 2025. Four numbers, a trend, a small table, one exception, and a line saying where it came from. Everything above the fold answers "was today good?".*

Design rules for the body, which are Chapter 15's rules under email constraints:

1. **Four tiles maximum**, each with a comparison. A number without a comparison is trivia.
2. **The subject line carries the headline:** `Riverstone Daily Flash — 18 Dec 2025 — ₹2,511,819 (+2.3% vs LY)`. Many readers never open it, and that's a success, not a failure.
3. **One chart**, small, with an action title or a heading that says what it shows.
4. **A small table**, three to six rows. Anything longer belongs in an attachment or a dashboard.
5. **Exceptions in a coloured box**, or a green line saying there are none. Silence is ambiguous.
6. **A footer that says where it came from, who owns it, and how to stop receiving it.**

The email writes money with Python's `,` format, which groups in thousands (₹2,511,819). This book writes rupees the Indian way (₹25,11,819); both are correct, and the email keeps Python's default.

### A KPI tile, by hand

If HTML is new to you, read Chapter 19's box "HTML in ten minutes" (section 19.7) first: tags, attributes, `style`, and the `<table>`, `<tr>`, `<td>` trio are all there. Here is the Flash's KPI tile written by hand, with today's net revenue in it:

```html
<table role="presentation" cellpadding="0" cellspacing="0" style="background:#f3f6fa;border:1px solid #dfe5ec;border-radius:6px">
  <tr><td style="padding:10px 12px">
    <div style="font:12px Arial,sans-serif;color:#5b6475">Net revenue</div>
    <div style="font:bold 20px Arial,sans-serif;color:#1d2330;padding-top:2px">₹2,511,819</div>
    <div style="font:12px Arial,sans-serif;color:#2f7d6d;padding-top:2px">+2.3% vs last year</div>
  </td></tr>
</table>
```

What each new piece does:

- **A one-cell table** (`<table>`, one `<tr>`, one `<td>`) is the box. Classic Outlook draws a table's background and border reliably; it doesn't do that for most other tags.
- **`role="presentation"`** tells screen readers that the table is layout, not data, so they don't announce "table, one row, one column".
- **`cellpadding="0" cellspacing="0"`** switch off the gaps old email clients add inside and between cells; the `padding:10px 12px` in the cell's style then sets the space exactly (10 pixels top and bottom, 12 left and right).
- **`<div>`** is a plain block: each one starts on a new line. Three of them give the label, the number, and the comparison.
- **`font:bold 20px Arial,sans-serif`** is shorthand for three settings at once: the weight (`bold`), the size, and the font, with `sans-serif` as the fallback if Arial is missing.
- **`border-radius:6px`** rounds the corners. Classic Outlook ignores it and draws square corners, which is harmless.

Figure 20.4 shows it as an email client draws it, on the left.

![Left: one KPI tile, Net revenue ₹2,511,819, +2.3% vs last year. Right: the same tile next to an Orders tile, 118, 116 customers, as a row built by the tile function](figures/fig20-4-kpi-tile.png)

*Figure 20.4 — The tile written by hand (left), and the row of two tiles that `tile()` builds below (right), rendered by a browser.*

### The same tile, from Python

Typing that for every number would be slow and easy to get wrong, so the Flash has a function that fills in the label, value, and note.

<!-- py: reset -->
```python
INK, MUTED, LIGHT, GOOD = "#1d2330", "#5b6475", "#dfe5ec", "#2f7d6d"

def tile(label, value, note="", note_color=MUTED):
    return (
        f'<td style="padding:0 8px 0 0;vertical-align:top">'
        f'<table role="presentation" cellpadding="0" cellspacing="0" width="100%" '
        f'style="background:#f3f6fa;border:1px solid {LIGHT};border-radius:6px">'
        f'<tr><td style="padding:10px 12px">'
        f'<div style="font:12px Arial,sans-serif;color:{MUTED}">{label}</div>'
        f'<div style="font:bold 20px Arial,sans-serif;color:{INK};padding-top:2px">{value}</div>'
        f'<div style="font:12px Arial,sans-serif;color:{note_color};padding-top:2px">{note}</div>'
        f"</td></tr></table></td>")

row = ("<table role='presentation'><tr>"
       + tile("Net revenue", "₹2,511,819", "+2.3% vs last year", GOOD)
       + tile("Orders", "118", "116 customers")
       + "</tr></table>")
print(len(row), "characters of HTML")
print(row)
```

```
1035 characters of HTML
<table role='presentation'><tr><td style="padding:0 8px 0 0;vertical-align:top"><table role="presentation" cellpadding="0" cellspacing="0" width="100%" style="background:#f3f6fa;border:1px solid #dfe5ec;border-radius:6px"><tr><td style="padding:10px 12px"><div style="font:12px Arial,sans-serif;color:#5b6475">Net revenue</div><div style="font:bold 20px Arial,sans-serif;color:#1d2330;padding-top:2px">₹2,511,819</div><div style="font:12px Arial,sans-serif;color:#2f7d6d;padding-top:2px">+2.3% vs last year</div></td></tr></table></td><td style="padding:0 8px 0 0;vertical-align:top"><table role="presentation" cellpadding="0" cellspacing="0" width="100%" style="background:#f3f6fa;border:1px solid #dfe5ec;border-radius:6px"><tr><td style="padding:10px 12px"><div style="font:12px Arial,sans-serif;color:#5b6475">Orders</div><div style="font:bold 20px Arial,sans-serif;color:#1d2330;padding-top:2px">118</div><div style="font:12px Arial,sans-serif;color:#5b6475;padding-top:2px">116 customers</div></td></tr></table></td></tr></table>
```

Line by line:

- **The first line** names four colours once, so every tile uses the same ones. Python can assign several names in one line when both sides have the same number of items.
- **`tile(label, value, note="", note_color=MUTED)`** takes the three texts and the note's colour, grey unless you say otherwise (Chapter 17's default values).
- **Eight f-strings in a row, inside brackets.** Python joins string literals written next to each other into one string, so this is one long string, split over lines only so a person can read it. The brackets let it run over several lines. (You may also see a `\` at the end of a line, which continues it; brackets are the cleaner way.)
- **Quotes inside quotes.** HTML attributes need quotes, so each f-string is written in single quotes `'…'` and the HTML inside uses double quotes `"…"`. The last line swaps them, which is fine as long as each string starts and ends with the same kind.
- **Each tile is its own `<td>`,** holding the one-cell table from above, with 8 pixels of space on its right. `row` puts two of them side by side in one row of an outer table: that is how you get a "card row" that works in Outlook. The printed HTML is the whole of it, 1,035 characters, and Figure 20.4 (right) is what it looks like.

### Connecting without a password in the code

The tiles above have their numbers typed in. The real ones come from the database, and a script that connects to a database needs its address and password. Those must not be in the code (Chapter 17 said why: a password in a script is a password in every copy of that script, forever). They go in **environment variables**: named settings that belong to the running program's surroundings, not to its code. Python reads them from `os.environ`, a dictionary of every variable the program was started with.

The easy way to set them for one project is a **`.env` file**: a plain-text file named `.env`, in the project folder, with one `NAME=value` per line. Copy `.env.example` from the companion folder to `.env` and fill in your own values. The Flash's looks like this:

```text
RIVERSTONE_DB=postgresql+psycopg://postgres:your-password@localhost:5432/riverstone_full
SMTP_HOST=localhost
SMTP_PORT=8025
SMTP_USER=flash@riverstone.example
SMTP_PASSWORD=
FLASH_TO=you@riverstone.example
FLASH_FAILURE_TO=you@riverstone.example
```

`RIVERSTONE_DB` is the database address in the form Chapter 18 used, with the user and password you set in Chapter 12, section 12.3. The `SMTP_` lines point at a test mail server on your own computer (section 20.6), so nothing can reach a real inbox while you learn; when you're ready for real, they become your mail service's host, port 587, and a service account's password. The two `FLASH_` lines are who gets the report and who hears about failures. **Never commit `.env` to Git**: add it to the project's `.gitignore` file (Chapter 26 shows how), and commit `.env.example`, with no real passwords in it, so a colleague knows which settings to fill in.

The `python-dotenv` package reads the file (`pip install python-dotenv` in your project's virtual environment, if it isn't there yet):

```python
import os
import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

found = load_dotenv(".env")    # read the .env file in this folder into os.environ
print("found .env:", found)
print(sorted(name for name in os.environ if name.startswith(("RIVERSTONE_", "SMTP_", "FLASH_"))))
engine = create_engine(os.environ["RIVERSTONE_DB"])
```

```
found .env: True
['FLASH_FAILURE_TO', 'FLASH_TO', 'RIVERSTONE_DB', 'SMTP_HOST', 'SMTP_PASSWORD', 'SMTP_PORT', 'SMTP_USER']
```

- **`load_dotenv(".env")`** reads the `.env` file in the current folder, adds each line to `os.environ`, and returns `True` if it found the file. It never overwrites a variable that is already set, so a server can set the real values another way and the same code still works.
- **The second `print`** lists the setting *names* only; `startswith` accepts a tuple of prefixes and is `True` if the name starts with any of them. Never print the values: a log with a password in it is as bad as a script with one.
- **`os.environ["RIVERSTONE_DB"]`** fails loudly with a `KeyError` if the setting is missing, which is what you want; a report that quietly connects to the wrong database is worse.

### The chart

A chart in an email is a PNG. There are two ways to include it, and only one works everywhere:

- **As a related image, by CID** (Content-ID): the PNG travels inside the email as a part of its own, and the HTML points at it with `<img src="cid:…">`. Outlook, Gmail, and phones all show it. This is the Flash's route.
- **As a base64 data URI** (`<img src="data:image/png;base64,…">`): the picture is written into the HTML itself as text. Gmail and classic Outlook for Windows don't display these, so use them only to preview the email in a browser.

Either way, draw the chart with matplotlib as in Chapter 18, keep it under about 620 pixels wide, and write `alt` text that states the finding, because a blocked image should still say something. First, the last 14 days of revenue, ending on the report's day:

```python
from datetime import date, timedelta

day = date(2025, 12, 18)
trend = pd.read_sql(text("""
    SELECT order_date, SUM(net_revenue) AS net_revenue
    FROM sales_lines
    WHERE order_date BETWEEN :start AND :day
    GROUP BY order_date ORDER BY order_date
"""), engine, params={"start": day - timedelta(days=13), "day": day}, parse_dates=["order_date"])
trend["lakh"] = trend["net_revenue"].astype(float) / 1e5
print(len(trend), "days")
print(trend[["order_date", "lakh"]].to_string(index=False, float_format="%.1f"))
```

```
14 days
order_date  lakh
2025-12-05  29.4
2025-12-06  33.5
2025-12-07  37.8
2025-12-08  30.0
2025-12-09  24.9
2025-12-10  31.3
2025-12-11  31.4
2025-12-12  32.8
2025-12-13  33.2
2025-12-14  35.9
2025-12-15  30.6
2025-12-16  33.5
2025-12-17  36.0
2025-12-18  25.1
```

- **`day - timedelta(days=13)`** is 5 December: with `BETWEEN`, which includes both ends, that is 14 days ending on the 18th. The dates are passed as parameters (`:start`, `:day`), never pasted into the SQL (Chapter 18, section 18.13).
- **`.astype(float)`**: the database returns exact decimal numbers, which pandas keeps as general Python objects; converting to `float` lets it divide and plot them. Dividing by `1e5` (100,000) gives lakh, and `float_format="%.1f"` prints one decimal place.

The 18th, at 25.1 lakh, is the second-lowest day of the fortnight; only 9 December (24.9) was lower. That sentence is the chart's action title. Now the chart, drawn into memory rather than into a file:

```python
from io import BytesIO
import matplotlib
matplotlib.use("Agg")                     # draw to a file, not a window
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter

ACC = "#0f5c8c"

def style_axes(ax, title, ylabel=None):
    """Chapter 18's chart rules: left-aligned action title, no top/right spines, light gridlines."""
    ax.set_title(title, loc="left", fontweight="bold", color=INK, fontsize=10)
    if ylabel:
        ax.set_ylabel(ylabel, color=MUTED)
    ax.spines[["top", "right"]].set_visible(False)
    ax.grid(axis="y", color=LIGHT, linewidth=0.8)
    ax.set_axisbelow(True)
    return ax

title = "18 Dec, at ₹25.1 lakh, was the second-lowest day of the last 14"
fig, ax = plt.subplots(figsize=(6.4, 2.3))
ax.plot(trend["order_date"], trend["lakh"], color=ACC, linewidth=2.2)
style_axes(ax, title, "₹ lakh")
ax.set_ylim(0, trend["lakh"].max() * 1.2)
ax.xaxis.set_major_formatter(DateFormatter("%d %b"))
buffer = BytesIO()
fig.savefig(buffer, format="png", dpi=150, bbox_inches="tight")
plt.close(fig)

png = buffer.getvalue()
print(type(png).__name__, len(png), "bytes, starting", png[:8])
```

```
bytes 31983 bytes, starting b'\x89PNG\r\n\x1a\n'
```

- **`style_axes`** is Chapter 18's function (section 18.11), copied in, with a smaller title font so the title fits a 620-pixel image.
- **`ax.set_ylim(0, …)`** starts the axis at zero, so a dip isn't exaggerated (Chapter 15), and leaves 20% headroom above the highest day.
- **`DateFormatter("%d %b")`** labels the dates as `05 Dec` instead of `2025-12-05`, using the same format codes as `strftime` (Chapter 17, section 17.11).
- **`BytesIO()`** is a file that lives in memory. `fig.savefig(buffer, format="png", …)` writes the picture into it exactly as it would into a file on disk; `format="png"` is needed because there's no file name to guess the format from. `dpi=150` keeps it sharp on phones.
- **`buffer.getvalue()`** hands back the whole picture as **bytes**: raw numbers from 0 to 255, not text. Every PNG starts with the same eight bytes, which is why the output shows `PNG` near the start.

The HTML then points at the picture by a name you choose, its Content-ID. The PNG itself is added to the email in section 20.6:

```python
CHART_CID = "flash-chart@riverstone"
img_tag = f'<img src="cid:{CHART_CID}" width="620" alt="{title}" style="display:block">'
print(img_tag)
```

```
<img src="cid:flash-chart@riverstone" width="620" alt="18 Dec, at ₹25.1 lakh, was the second-lowest day of the last 14" style="display:block">
```

`cid:flash-chart@riverstone` means "the picture is the part of this same email whose Content-ID is `flash-chart@riverstone`". Any name works if it is unique within the email; the `@` form is the convention. The `alt` text is the action title, so a reader with images blocked still gets the finding.

To look at the email in a browser before sending anything, swap the `cid:` link for a data URI. **Base64** turns bytes into text by writing every 3 bytes as 4 characters chosen from 64 safe ones (letters, digits, `+` and `/`), so a picture can sit inside an HTML file:

```python
import base64

encoded = base64.b64encode(png).decode("ascii")
preview_tag = img_tag.replace(f"cid:{CHART_CID}", "data:image/png;base64," + encoded)
print(len(png), "bytes became", len(encoded), "characters of text")
print(preview_tag[:70] + " …")
```

```
31983 bytes became 42644 characters of text
<img src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAA04AAAFmCAYAAA …
```

- **`base64.b64encode(png)`** returns the encoded text still as bytes; **`.decode("ascii")`** turns it into an ordinary string. It comes out about a third longer than the picture.
- **`replace`** swaps the `cid:` address for the data URI. The finished script writes this preview version to `out/daily_flash_<date>.html` and sends the `cid:` version.

---

## 20.6 Sending mail from code, safely

### SMTP: the universal route

Four ideas first, because this is the first time the book sends email:

- **SMTP** (Simple Mail Transfer Protocol) is the language mail servers speak to each other and to programs that hand them mail. Your script is a small SMTP client: it connects, says who the mail is from and to, and hands over the message.
- **Host and port.** The host is the mail server's address (`smtp.office365.com`, say); the port is the numbered door on it that the SMTP service listens at. **Port 587** is the standard door for programs submitting mail; the connection starts unencrypted and is then upgraded. **Port 465** is encrypted from the first byte, and in Python needs `smtplib.SMTP_SSL` instead of `smtplib.SMTP`.
- **STARTTLS** is that upgrade on port 587: the script asks the server to switch the connection to encryption (TLS) *before* it sends the password, so the password never crosses the network in plain text.
- **A multipart message** is one email made of several parts, each labelled with a **MIME type** (`text/plain`, `text/html`, `image/png`, `text/csv`): a plain-text version, the HTML version, the images the HTML uses, and any attachments. The mail program shows the best part it can.

Python's standard library builds the message with `email.message.EmailMessage` and sends it with `smtplib`. Build first; this part runs anywhere, with no mail server:

```python
from email.message import EmailMessage

html = f"<p style='font:14px Arial,sans-serif'>Test Flash</p>{row}{img_tag}"
message = EmailMessage()
message["Subject"] = "Riverstone Daily Flash — 18 Dec 2025 — test"
message["From"] = os.environ["SMTP_USER"]
message["To"] = os.environ["FLASH_TO"]
message.set_content("This report needs an HTML-capable email client.")   # plain-text fallback
message.add_alternative(html, subtype="html")
message.get_payload()[1].add_related(png, maintype="image", subtype="png", cid=f"<{CHART_CID}>")

print(message["From"], "→", message["To"])
for part in message.walk():
    print(part.get_content_type(), part.get("Content-ID", ""))
```

```
flash@riverstone.example → you@riverstone.example
multipart/alternative 
text/plain 
multipart/related 
text/html 
image/png <flash-chart@riverstone>
```

- **`html`** is a small test email: one line of text, the row of tiles from section 20.5, and the chart's `<img>` tag.
- **`message = EmailMessage()`** starts an empty email. **`message["Subject"] = …`** sets a header, the lines at the top of every email. `From` and `To` come from the `.env` settings, not the code.
- **`set_content(...)`** makes the plain-text part. Always set one: some clients, and most spam filters, look for it.
- **`add_alternative(html, subtype="html")`** adds the HTML version and turns the message into `multipart/alternative`: "these parts say the same thing; show the best one you can".
- **`message.get_payload()[1]`** is the second part, the HTML (the plain text is `[0]`). **`add_related(png, maintype="image", subtype="png", cid=…)`** attaches the chart *to the HTML part*, as a related image with the Content-ID the `<img src="cid:…">` tag points at. The angle brackets around the name are how Content-IDs are written in the email's headers; in the HTML you leave them off.
- **`message.walk()`** visits every part in order. The output is the email's structure: an alternative of plain text and a `multipart/related` group holding the HTML and its image.

Printing the whole message would show thousands of lines of base64 (the chart, encoded for travel), so the walk is the useful view. You'll see the raw headers when the test server receives it below.

An **attachment** is one more part. Its MIME type is written as two halves, a main type and a subtype (`text` and `csv`), and the `mimetypes` module guesses it from the file name:

```python
import mimetypes
from pathlib import Path

Path("out").mkdir(exist_ok=True)
trend[["order_date", "net_revenue"]].to_csv("out/last_14_days.csv", index=False)

path = "out/last_14_days.csv"
kind, _ = mimetypes.guess_type(path)
maintype, subtype = kind.split("/")
with open(path, "rb") as f:
    data = f.read()
message.add_attachment(data, maintype=maintype, subtype=subtype, filename=Path(path).name)
print(kind, len(data), "bytes")
print([part.get_content_type() for part in message.walk()])
```

```
text/csv 324 bytes
['multipart/mixed', 'multipart/alternative', 'text/plain', 'multipart/related', 'text/html', 'image/png', 'text/csv']
```

- **`mimetypes.guess_type(path)`** returns two things, the type and the file's compression (`None` here); `kind, _ =` keeps the first and ignores the second. For a `.xlsx` workbook it would be the long `application/vnd.openxmlformats-officedocument.spreadsheetml.sheet`; for a file type it doesn't know, it returns `None`, and the finished script falls back to `application/octet-stream` ("some bytes").
- **The first two lines after the imports** make an `out` folder (`exist_ok=True`: no error if it's already there) and save the 14-day table in it as a CSV (Chapter 18), so there's a real file to attach.
- **`with open(path, "rb") as f:`** opens the file in binary mode (`"rb"`, read bytes) and closes it afterwards, the habit from Chapter 17.
- **`add_attachment(...)`** wraps everything so far and the new file in a `multipart/mixed` message: "a message, plus files". `filename=` is the name the recipient sees; `Path(path).name` is the file's name without its folder.

### Sending, and testing it on your own computer

Don't test on real people. Python can run a small **test mail server** on your own computer that accepts mail and prints it instead of delivering it. Install it once with `pip install aiosmtpd` (Python used to have one built in, `smtpd`, but it was removed in Python 3.12), then start it in a **second terminal**, in any folder, and leave it running:

```bash
python -m aiosmtpd -n -l localhost:8025
```

`-l localhost:8025` means "listen on this computer, at port 8025"; `-n` stops it trying to switch to a different user account, which it can't do without administrator rights. The `.env` above already points `SMTP_HOST` and `SMTP_PORT` at it. Back in your notebook:

<!-- run: none -->
```python
import smtplib

def send_message(message):
    with smtplib.SMTP(os.environ["SMTP_HOST"], int(os.environ["SMTP_PORT"]), timeout=30) as smtp:
        if os.environ.get("SMTP_PASSWORD"):
            smtp.starttls()
            smtp.login(os.environ["SMTP_USER"], os.environ["SMTP_PASSWORD"])
        return smtp.send_message(message)

refused = send_message(message)
print("refused:", refused)
```

```
refused: {}
```

- **`smtplib.SMTP(host, port, timeout=30)`** opens the connection. `int(...)` is needed because every environment variable is text. `timeout=30` gives up after 30 seconds instead of hanging (Chapter 18, section 18.14). Used with `with`, the connection is closed properly even if something fails.
- **`if os.environ.get("SMTP_PASSWORD"):`** runs the two security lines only when a password is set. The test server has no encryption and no password; a real mail service on port 587 has both, and then `starttls()` upgrades the connection before `login(...)` sends the password.
- **`send_message(message)`** reads the recipients from the headers and hands the message over. It returns a dictionary of recipients the server refused; empty means every address was accepted.

The second terminal shows the email as it arrived. These are its first lines:

```text
---------- MESSAGE FOLLOWS ----------
Subject: Riverstone Daily Flash =?utf-8?q?=E2=80=94_18_Dec_2025_=E2=80=94?=
 test
From: flash@riverstone.example
To: you@riverstone.example
MIME-Version: 1.0
Content-Type: multipart/mixed; boundary="===============4515678096233146423=="
X-Peer: ('127.0.0.1', 59298)

--===============4515678096233146423==
Content-Type: multipart/alternative;
 boundary="===============2092394867852545785=="
```

The subject looks scrambled because `—` isn't a plain English character, so it travels encoded (`=?utf-8?q?…?=`) and your mail program decodes it. `X-Peer` is added by the test server: the address and port your script connected from. The long `boundary` numbers mark where each part you built starts and ends: `multipart/mixed` on the outside, because of the attachment, then the `multipart/alternative` inside it. They are random, so yours will differ. When this works, change the four `SMTP_` settings in `.env` to your service account's, and the same code sends real mail.

Points that matter:

- **Credentials come from the environment**, loaded from a `.env` file that is never committed (section 20.5, and Chapter 26 for `.gitignore`).
- **Sending as a person is fragile.** Ask for a service account or a shared mailbox, so the report doesn't stop when someone leaves or changes their password.

### Microsoft 365 and Google Workspace

Many organizations have switched off basic SMTP authentication. Then the routes are:

| Platform | Route | Notes |
|---|---|---|
| Microsoft 365 | **Microsoft Graph API** (`/users/{id}/sendMail`), app registration with `Mail.Send` | The supported way for unattended sending; IT approves the app |
| Microsoft 365 | **Power Automate** flow that sends the mail | No app registration; the flow owner sends it |
| Google Workspace | **Gmail API** with a service account, or **Apps Script `MailApp`** (Chapter 19) | Apps Script is much simpler for Sheets-based flows |
| Anywhere | A transactional provider (SendGrid, SES, Postmark) | Best deliverability for volume; needs domain setup |

Whichever you use, ask three questions first: **who does the mail appear to come from**, **who can stop it**, and **what happens to bounces**. An automation sending from a personal mailbox to 40 people is a governance problem waiting to be discovered.

### Never send from a laptop as yourself, for long

The honest progression: prove the value with your own mailbox for a week, then move to a service account and a server. The moment the report has more than a handful of recipients, it belongs on a platform that IT knows about.

---

## 20.7 Scheduling

### Let the script work out the date

A scheduled job runs the same command every morning, so the command can't contain a date: `daily_flash.py 2025-12-18` would send 18 December every day. The script has to work out "today" itself, in the business's time zone, and still accept a date when a person wants to rerun an old day. Chapter 18's monthly report (section 18.15) already reads its command line with **`argparse`**: `ArgumentParser`, a positional argument, an option written with `--`, `parse_args()`, and a free `--help` message. The Flash needs two things that script didn't: a positional argument that can be left out (the day), and an on/off switch (`--send`).

```python
import argparse
from datetime import datetime
from zoneinfo import ZoneInfo

parser = argparse.ArgumentParser()
parser.add_argument("day", nargs="?", default=None)
parser.add_argument("--send", action="store_true")

for command_line in (["--send"], ["2025-12-18"]):
    args = parser.parse_args(command_line)
    day = date.fromisoformat(args.day) if args.day else datetime.now(ZoneInfo("Asia/Kolkata")).date()
    print(command_line, "→ send:", args.send, "| day given:", args.day, "| used today's date:", args.day is None)
```

```
['--send'] → send: True | day given: None | used today's date: True
['2025-12-18'] → send: False | day given: 2025-12-18 | used today's date: False
```

- **`argparse.ArgumentParser()`** and **`add_argument`** work as in Chapter 18: `"day"` is a *positional* argument, taken from its place in the command, and `--send` is an *option*, typed by name.
- **`nargs="?"`** makes `day` optional: zero or one value. **`default=None`** is what it holds when it's left out.
- **`--send`** with **`action="store_true"`** is a switch: `True` if it's typed, `False` if not. Sending is off unless you ask, so a test run can never email anyone by accident.
- **`parser.parse_args(command_line)`** normally reads the real command line; handing it a list lets you try both cases in a notebook. `["--send"]` is what the scheduler will run; `["2025-12-18"]` is a person rerunning an old day.
- **`date.fromisoformat(args.day) if args.day else …`** uses the given date if there is one, and otherwise today. **`datetime.now(ZoneInfo("Asia/Kolkata"))`** is the current time in India, whatever the server's clock is set to, and **`.date()`** keeps just the date. The next subsection explains `ZoneInfo`. (On Windows, run `pip install tzdata` once: Windows doesn't ship the time-zone list that `zoneinfo` reads.)

So the scheduler's command is just `daily_flash.py --send`.

### Windows Task Scheduler

For a script on a Windows machine or VM:

1. **Task Scheduler → Create Task** (not "Basic Task": you need the extra options).
2. **General:** run whether the user is logged on or not; use a service account; tick "Run with highest privileges" only if you truly need it.
3. **Triggers:** weekly, Monday to Friday, at 07:00, so the Flash is in inboxes by 07:30. The time is the machine's own local time, so check which time zone the VM is set to before you trust it: cloud VMs are often set to UTC.
4. **Actions:** program `C:\riverstone\.venv\Scripts\python.exe`, arguments `daily_flash.py --send`, and **Start in** `C:\riverstone`, the script's folder. The most common cause of "it works when I run it, not when it's scheduled" is a missing working folder; it also decides where the log and the preview files are written.
5. **Settings:** "Stop the task if it runs longer than 1 hour", and "If the task fails, restart every 10 minutes, up to 3 times". Retries are safe only once the job is idempotent (section 20.11): a rerun must not send a second email. Microsoft's reference says only that the task is restarted "if the task fails", and a script that starts, runs, and exits with an error code may not count as a failed task, so the Flash also does its own waiting for the data (section 20.11) rather than relying on this setting.

### cron

On Linux or macOS, the schedule lives in a **crontab**, a text file of jobs, one per line. First find out which time zone the server's clock uses, because cron fires by that clock. On a Linux server:

```bash
timedatectl
```

Its `Time zone:` line says, for example, `Etc/UTC (UTC, +0000)`. (On a Mac, `date` prints the time with the zone's short name.) On a UTC server, 07:00 in India is 01:30 UTC; India has no daylight saving, so that never shifts. Then open the crontab. `crontab -e` opens it in a text editor; if yours opens one you can't find the way out of, run `export EDITOR=nano` first, which picks **nano** (save with Ctrl+O and Enter, leave with Ctrl+X). Add this line, with the intended local time in a comment above it:

```bash
# m  h  dom mon dow  command            07:00 India time (01:30 UTC), Monday to Friday
30 1 * * 1-5  cd /opt/riverstone && /opt/riverstone/.venv/bin/python daily_flash.py --send >> logs/cron.log 2>&1
```

`crontab -l` lists what's installed. The pieces of that line:

| Piece | What it does |
|---|---|
| `30 1 * * 1-5` | Minute 30, hour 1, any day of the month, any month, weekdays 1–5 (Monday to Friday). `0 7 * * *` would be 07:00 every day; `*/15 * * * *` every fifteen minutes |
| `cd /opt/riverstone &&` | Go to the script's folder, and run the rest only if that worked (`&&`) |
| `/opt/riverstone/.venv/bin/python` | The project's own Python, by its full path. cron runs with a minimal environment: no `PATH` you're used to and no virtual environment switched on, so give full paths |
| `daily_flash.py --send` | No date: the script works out today in India itself, and reads the `.env` file that sits next to it |
| `>> logs/cron.log` | Add (`>>`) anything the job prints to the end of this file, instead of losing it; `>` would overwrite the file each time |
| `2>&1` | Send error output (stream 2) to the same place as normal output (stream 1), so a crash is in the log too |

Two things you'll meet in other people's crontabs. `"$(date +\%F)"` pastes today's date into the command, but by the *server's* clock, and the `%` must be written `\%` because cron treats a bare `%` as a line break. And `set -a; . .env; set +a` loads a `.env` file into the environment before the command; the Flash doesn't need it, because `load_dotenv` reads the file. Chapter 26, section 26.0, teaches `&&` and that `.env` line properly, and Chapter 34, section 34.2, teaches `>>` and `2>&1`.

If the server is a Red Hat or Fedora machine, its cron (called *cronie*) also accepts a line `CRON_TZ=Asia/Kolkata` at the top of the crontab, and then the times below it are India time: `0 7 * * 1-5`. The cron on Ubuntu and Debian doesn't support this; there, the job runs by the server's clock, as above.

### Cloud schedulers

GitHub Actions (`on: schedule`), Azure Functions timers, AWS EventBridge with Lambda, Google Cloud Scheduler, and the scheduler inside any orchestrator (Chapter 46) all do the same job without a machine you maintain. For a script that runs for a minute a day and needs a database, a small VM or a container on a schedule is usually simplest; for anything with dependencies, use the orchestrator. Check each one's time-zone setting: GitHub Actions schedules, for example, always run in UTC.

### Time zones, the quiet bug

A date and time with no time zone attached is ambiguous: 02:30 where? Python lets you attach one with **`tzinfo=`**, and **`astimezone(...)`** converts a time to another zone. `ZoneInfo("Asia/Kolkata")` is India's zone by its standard name, taken from the world's time-zone list:

```python
from datetime import timezone

ist = ZoneInfo("Asia/Kolkata")
server_time = datetime(2025, 12, 18, 2, 30, tzinfo=timezone.utc)
india_time = server_time.astimezone(ist)
print("server (UTC):", server_time.strftime("%Y-%m-%d %H:%M"))
print("India (IST): ", india_time.strftime("%Y-%m-%d %H:%M"))
print("same calendar date?", server_time.date() == india_time.date())
```

```
server (UTC): 2025-12-18 02:30
India (IST):  2025-12-18 08:00
same calendar date? True
```

- **`datetime(2025, 12, 18, 2, 30, tzinfo=timezone.utc)`** is 02:30 on 18 December in UTC; `timezone.utc` is UTC itself.
- **`strftime("%Y-%m-%d %H:%M")`** formats it with the codes from Chapter 17, section 17.11: `%Y` year, `%m` month, `%d` day, `%H` hour (00–23), `%M` minute.

Five and a half hours later it's 08:00 in India, still the 18th, so nothing goes wrong. Now run a job late in the UTC evening:

```python
server_time = datetime(2025, 12, 17, 20, 0, tzinfo=timezone.utc)
india_time = server_time.astimezone(ist)
print("server (UTC):", server_time.strftime("%Y-%m-%d %H:%M"))
print("India (IST): ", india_time.strftime("%Y-%m-%d %H:%M"))
print("same calendar date?", server_time.date() == india_time.date())
print("'yesterday' by the server:", server_time.date() - timedelta(days=1),
      "| by India:", india_time.date() - timedelta(days=1))
```

```
server (UTC): 2025-12-17 20:00
India (IST):  2025-12-18 01:30
same calendar date? False
'yesterday' by the server: 2025-12-16 | by India: 2025-12-17
```

At 20:00 UTC on the 17th it's already 01:30 on the 18th in India, so a job that asks the server for "yesterday" reports the 16th while every reader's yesterday is the 17th. Nothing crashes, and the email looks normal; it's just a day out. Three habits fix it permanently:

1. **Set the schedule in the business's time zone**, knowing which clock the scheduler uses, and write the intended local time in a comment.
2. **Compute the reporting date explicitly**, in the business time zone (`datetime.now(ZoneInfo("Asia/Kolkata")).date()`), or pass it as an argument; never rely on the server's idea of today.
3. **Put the period in the subject line and the body**, so a reader can see which day they're looking at.

---

## 20.8 Alerts and exception reports

A daily report says what happened. An **alert** says something needs attention. They are different products, and mixing them is why people stop reading both.

| | Report | Alert |
|---|---|---|
| Arrives | On a schedule | When a condition is met |
| Contains | The full picture | One problem, and what to do |
| Success looks like | Read in 20 seconds | Rare, and acted on |
| Failure mode | Ignored | Ignored, which is worse |

### Designing an exception rule

The Flash's rule is simple, which is a feature: *any product that sold fewer than 500 units today*. Here it is in pandas, on the real data, with the `engine` from section 20.5:

```python
lines = pd.read_sql(text("""
    SELECT p.product_name, s.quantity, s.net_revenue
    FROM sales_lines s JOIN products p ON p.product_id = s.product_id
    WHERE s.order_date = :day
"""), engine, params={"day": day})

by_product = lines.groupby("product_name", as_index=False)["quantity"].sum().sort_values("quantity")
low = by_product[by_product["quantity"] < 500]

print(by_product.to_string(index=False))
print("\nexceptions:", len(low), "→", low["product_name"].tolist())
```

```
      product_name  quantity
  Industrial Crate       345
   Storage Box 25L       575
   Water Bottle 1L       600
     Lunch Box Set       790
Food Container Set       855
   Storage Box 10L      1005
     Stackable Bin      1240

exceptions: 1 → ['Industrial Crate']
```

One product falls below the line, so the email carries one exception box. On a day when nothing does, the email says so in green rather than showing an empty table: **silence is ambiguous, and an empty box looks like a bug.**

### Thresholds that survive contact with reality

- **Base them on history, not a round number.** "Below 500 units" is a placeholder; "below the 10th percentile of the last 90 days for that product" adapts as the business grows. The next cell shows what that means.
- **Require persistence** for noisy measures: alert when a threshold is crossed two days running, not on a single dip.
- **Add a floor for materiality:** don't alert on a ₹4,000 shortfall because it's 40% below target.
- **Say what to do.** "Industrial Crate sold 345 units (below 500). Check stock at Bhiwandi and confirm the Mumbai dispatch." An alert without an action is only anxiety.
- **Count them.** If an alert fires every day, it's a report. If it never fires, nobody will believe it when it does; test it deliberately.

A threshold from history takes one query and two pandas steps. The **10th percentile** of a product's daily sales is the level it sells below on only one day in ten; and pandas computes it with `quantile(0.10)` (Chapter 18, section 18.6):

```python
history = pd.read_sql(text("""
    SELECT s.order_date, p.product_name, SUM(s.quantity) AS quantity
    FROM sales_lines s JOIN products p ON p.product_id = s.product_id
    WHERE s.order_date BETWEEN :start AND :end
    GROUP BY s.order_date, p.product_name
"""), engine, params={"start": day - timedelta(days=90), "end": day - timedelta(days=1)})

p10 = history.groupby("product_name")["quantity"].quantile(0.10).rename("p10")
compare = by_product.merge(p10, left_on="product_name", right_index=True)
compare["below_p10"] = compare["quantity"] < compare["p10"]
print(len(history), "product-days of history")
print(compare.to_string(index=False))
```

```
607 product-days of history
      product_name  quantity    p10  below_p10
  Industrial Crate       345  267.0      False
   Storage Box 25L       575  922.5       True
   Water Bottle 1L       600  991.0       True
     Lunch Box Set       790  811.0       True
Food Container Set       855  987.0       True
   Storage Box 10L      1005 1232.0       True
     Stackable Bin      1240 1266.0       True
```

- **The query** adds up each product's units per day, for the 90 days before today (19 September to 17 December), so today can't influence its own threshold.
- **`groupby("product_name")["quantity"].quantile(0.10)`** gives one threshold per product; `.rename("p10")` names the result.
- **`merge(..., left_on="product_name", right_index=True)`** lines each product's threshold up with today's total: `p10` is a Series whose index is the product name, so the right side joins on its index (Chapter 18, section 18.7).
- **A product that sold nothing on a day has no row** for that day, so its quietest days are missing and its threshold comes out a little high. A real rule would fill those days with 0 first, with a calendar table (Chapter 13).

Read the result before you adopt it. Industrial Crate, the only product under the fixed 500, is *not* unusual for itself: it always sells little (its 10th percentile is 267). But six of the seven products sold below their own tenth percentile: 18 December was a quiet day for almost everything, which the revenue check in section 20.11 sees as well. A per-product rule on its own would have sent six alerts that morning. That is why the next two defences exist.

### Alert fatigue

The failure mode of alerting is volume. Three defences: **one rule, one owner**; **a weekly digest for anything not urgent**; and **a monthly review of every alert** asking "did anyone act on this?" Alerts nobody acted on get deleted, not tuned.

---

## 20.9 Delivering to chat

Where teams live in Teams, Slack, or WhatsApp, a message there beats an email nobody opens. The simplest route is an **incoming webhook**: the channel's owner creates a secret URL, and anything that can send an HTTP POST with JSON in it (Chapter 18, section 18.14) can post to that channel. The two big tools want different JSON:

- **Slack** incoming webhooks accept a plain message: `{"text": "…"}`.
- **Microsoft Teams** is retiring its old incoming webhooks (Office 365 Connectors). The replacement is the **Workflows** app: on the channel, choose *Workflows* and a template such as *Send webhook alerts to a channel*, save it, and copy the webhook URL it gives you. Workflows accept an **Adaptive Card**, Microsoft's JSON format for a small card of text and buttons, wrapped as a message with one attachment.

Build both payloads first; this runs anywhere:

```python
import json

summary = ("Riverstone Daily Flash, 18 Dec 2025: ₹2,511,819 (+2.3% vs LY). "
           "1 exception: Industrial Crate, 345 units.")
slack_payload = {"text": summary}
teams_payload = {
    "type": "message",
    "attachments": [{
        "contentType": "application/vnd.microsoft.card.adaptive",
        "content": {
            "$schema": "http://adaptivecards.io/schemas/adaptive-card.json",
            "type": "AdaptiveCard",
            "version": "1.2",
            "body": [{"type": "TextBlock", "text": summary}],
        },
    }],
}
print(json.dumps(slack_payload, ensure_ascii=False))
print(json.dumps(teams_payload, indent=2, ensure_ascii=False))
```

```
{"text": "Riverstone Daily Flash, 18 Dec 2025: ₹2,511,819 (+2.3% vs LY). 1 exception: Industrial Crate, 345 units."}
{
  "type": "message",
  "attachments": [
    {
      "contentType": "application/vnd.microsoft.card.adaptive",
      "content": {
        "$schema": "http://adaptivecards.io/schemas/adaptive-card.json",
        "type": "AdaptiveCard",
        "version": "1.2",
        "body": [
          {
            "type": "TextBlock",
            "text": "Riverstone Daily Flash, 18 Dec 2025: ₹2,511,819 (+2.3% vs LY). 1 exception: Industrial Crate, 345 units."
          }
        ]
      }
    }
  ]
}
```

- **`teams_payload`** is Microsoft's documented shape: a `message` whose one attachment has the card's content type, and a card whose `body` is a list of blocks. One `TextBlock` is enough for a summary; more blocks give headings or a fact list.
- **`json.dumps(..., ensure_ascii=False)`** writes the dictionary as JSON text (Chapter 17) and keeps `₹` as it is instead of an escape code; `indent=2` lays it out for reading.

Then the post itself, which needs a real channel, so test it only on one you own:

<!-- run: none -->
```python
import requests

def post_to_webhook(payload, url_env):
    """Post a payload to the webhook whose URL is in the environment variable url_env."""
    response = requests.post(os.environ[url_env], json=payload, timeout=20)
    response.raise_for_status()
    return response.status_code

post_to_webhook(slack_payload, "SLACK_WEBHOOK_URL")
post_to_webhook(teams_payload, "TEAMS_WEBHOOK_URL")
```

- **The URL comes from the environment**, like the SMTP password: anyone who has it can post to your channel. Add `SLACK_WEBHOOK_URL` or `TEAMS_WEBHOOK_URL` to `.env`.
- **`json=payload`** sends the dictionary as JSON; **`timeout=20`** stops a slow service holding the job forever.
- **`raise_for_status()`** turns an error reply into a Python error you'll see and log, as in Chapter 18, section 18.14: a `400` means the service didn't understand the JSON, and a `403` or `404` usually means the URL is wrong or the webhook was removed. Slack answers a good post with status `200` and the body `ok`.

Habits that keep chat useful:

- **Link, don't dump.** Chat is for the headline and the exception; the detail lives in the report or the dashboard. Keep the same discipline as email: a headline, a few numbers, and a link.
- **Who owns it:** a Teams workflow belongs to the person who created it, and stops if they leave. Add a co-owner, as you would a deputy for the script.
- **WhatsApp Business API** is common in Indian sales teams and is not a webhook: it needs an approved provider, pre-approved message templates, and consent. Check the rules before promising it; personal WhatsApp automation breaks the terms of service.
- **Threads and mentions:** mention a person only when you need them to act. A daily `@channel` is how a channel gets muted.

---

## 20.10 Low-code automation

| Tool | Home ground | Strengths | Watch for |
|---|---|---|---|
| **Power Automate** | Microsoft 365 | Excel, Outlook, SharePoint, Teams, approvals; runs Office Scripts | Licensing tiers; flows owned by individuals |
| **n8n** | Self-hosted or cloud | Open source, code steps when needed, cheap at volume | You maintain it |
| **Make** (formerly Integromat) | Cloud SaaS | Visual, many connectors, good error handling | Per-operation pricing |
| **Zapier** | Cloud SaaS | The widest connector list, easiest start | Costs rise quickly with volume |

Low-code is the right answer when the work is **moving things between SaaS tools** (a form response becomes a CRM record becomes a Teams message), when **the business should own it**, or when **IT won't let you run scripts**. It's the wrong answer when the logic is complex, when it needs real data transformation, or when you'd be building a pipeline one box at a time: a flow with forty steps and no version control is harder to maintain than fifty lines of Python.

A pattern that works well in practice: **Python does the data work and writes a result somewhere** (a table, a file, an API endpoint), and **a flow does the delivery** (email, Teams, approvals). Each tool does what it's good at, and the business can change the recipients without touching code.

---

## 20.11 Making an automation trustworthy

![Six cards: it says what it did, it checks before it sends, it tells you when it breaks, it handles nothing-today, it can be run twice, someone else can run it](figures/fig20-5-trustworthy.svg)

*Figure 20.5 — The six properties that separate an automation people rely on from one they quietly stop believing.*

### Checks that can stop it

Chapter 18's monthly report ran six checks before writing anything. The Flash does the same with the day's data. The recent median comes from the 14 days before the report's day, worked out from `day` so the same code works on any date:

```python
def checks(lines, day, previous_days):
    """Return (name, passed, detail) for each check. Any failure means no email."""
    revenue = float(lines["net_revenue"].sum())
    median_recent = float(previous_days["net_revenue"].median())
    return [
        ("rows returned", len(lines) > 0, f"{len(lines):,} lines"),
        ("all rows are today's", bool((lines["order_date"].dt.date == day).all()), str(day)),
        ("no missing revenue", bool(lines["net_revenue"].notna().all()),
         f"{int(lines['net_revenue'].isna().sum())} missing"),
        ("revenue within 60% of recent median", abs(revenue / median_recent - 1) < 0.6,
         f"₹{revenue:,.0f} vs median ₹{median_recent:,.0f}"),
    ]

def load_for_checks(day):
    lines = pd.read_sql(text("""
        SELECT order_date, order_id, net_revenue FROM sales_lines WHERE order_date = :day
    """), engine, params={"day": day}, parse_dates=["order_date"])
    previous = pd.read_sql(text("""
        SELECT order_date, SUM(net_revenue) AS net_revenue FROM sales_lines
        WHERE order_date BETWEEN :start AND :end GROUP BY order_date
    """), engine, params={"start": day - timedelta(days=14), "end": day - timedelta(days=1)})
    return lines, previous

lines, previous = load_for_checks(day)
for name, passed, detail in checks(lines, day, previous):
    print(f"{'PASS' if passed else 'FAIL'}  {name}  ({detail})")
```

```
PASS  rows returned  (213 lines)
PASS  all rows are today's  (2025-12-18)
PASS  no missing revenue  (0 missing)
PASS  revenue within 60% of recent median  (₹2,511,819 vs median ₹3,209,520)
```

- **Each check is a tuple** of a name, `True` or `False`, and a detail for the log, so one loop can print them all and one line can ask whether all passed.
- **`abs(revenue / median_recent - 1) < 0.6`**: today divided by the recent median is 1.0 on a typical day; subtracting 1 and taking the absolute value (`abs`) gives how far off it is, up or down. Today is 22% below, inside the 60% band.
- **`day - timedelta(days=14)` to `day - timedelta(days=1)`** is the 14 days before the report's day (4 to 17 December here), so the window moves with the date.

Now a date with no sales, 1 January 2026, which is what the Flash met on the morning the overnight load failed (the story later in this chapter). Before you run it, predict which of the four checks will fail:

```python
lines, previous = load_for_checks(date(2026, 1, 1))
for name, passed, detail in checks(lines, date(2026, 1, 1), previous):
    print(f"{'PASS' if passed else 'FAIL'}  {name}  ({detail})")
```

```
FAIL  rows returned  (0 lines)
PASS  all rows are today's  (2026-01-01)
PASS  no missing revenue  (0 missing)
FAIL  revenue within 60% of recent median  (₹0 vs median ₹2,932,108)
```

Two checks pass with nothing to check. `.all()` on an empty column is `True`, because there is no row that breaks the rule; that is why "rows returned" must come first. The row check and the median check fail, and either is enough to stop the email. A check that fails is not a disaster; a check that doesn't exist is. The rule: **if a check fails, nothing is sent, and a person is told.**

Month to date is a different window, from the 1st of the month to the report's day. In PostgreSQL:

```python
month_to_date = pd.read_sql(text("""
    SELECT SUM(net_revenue) AS net_revenue FROM sales_lines
    WHERE order_date >= DATE_TRUNC('month', CAST(:day AS date)) AND order_date <= :day
"""), engine, params={"day": day})
print(f"₹{float(month_to_date['net_revenue'].iloc[0]):,.0f}")
```

```
₹57,069,985
```

`DATE_TRUNC('month', …)` cuts a date back to the 1st of its month (Chapter 13); `CAST(:day AS date)` tells PostgreSQL the parameter is a date. MySQL has no `DATE_TRUNC`: write `order_date >= DATE_FORMAT(:day, '%Y-%m-01')` instead. The finished script avoids both by working out the 1st of the month in Python, `day.replace(day=1)`, which works on any database. Don't reuse the 14-day window for month to date: it gives the right answer only by accident, on the 14th.

### Logging and run history

Chapter 18's monthly report (section 18.15) already writes a **log** with Python's `logging` module: a named logger from `getLogger`, one `basicConfig` call that sets the level and the line format, and messages such as `log.info("loading %s", month)`. The Flash uses the same pieces and adds three things: showing the log inside a notebook, sending it to a file as well as the screen, and dating each line in the file. First the same setup, made visible in a notebook:

```python
import logging, sys

logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s", stream=sys.stdout, force=True)
log = logging.getLogger("flash")
log.debug("this detail is below INFO, so it is hidden")
log.info("starting")
log.warning("3 rows could not be read")
print("the report itself")
```

```
INFO starting
WARNING 3 rows could not be read
the report itself
```

- **`logging.getLogger("flash")`** is the Flash's named **logger**, and the four levels are Chapter 18's: `log.debug(...)` for detail, `log.info(...)` for normal progress, `log.warning(...)` for something odd but not fatal, `log.error(...)` for a failure.
- **`basicConfig(...)`** with **`level=logging.INFO`** shows INFO and above and hides DEBUG, which is why the first line never appears. This **`format=`** leaves out Chapter 18's `%(asctime)s`; the file below brings it back.
- **`stream=sys.stdout`**: every program has two output streams, **standard output** (stdout), where `print` writes, and **standard error** (stderr), meant for messages about the run. Logging writes to stderr unless told otherwise, which keeps log lines apart from the report's own output; a notebook needs stdout here for the lines to appear in its output. **`force=True`** replaces any logging set up earlier, which a notebook may already have done (without it, `basicConfig` can quietly do nothing).
- **`%s` in a message** is filled in from the values after it, as in Chapter 18: `log.info("loaded %s lines", 213)`.

A scheduled job needs its log in two places: on the screen while you test, and in a **log file**, so that next month you can read what happened this morning. Each place a log line goes is a **handler**, and each handler has its own format:

```python
Path("logs").mkdir(exist_ok=True)
screen = logging.StreamHandler(sys.stdout)
screen.setFormatter(logging.Formatter("%(levelname)s %(message)s"))
logfile = logging.FileHandler("logs/flash.log", encoding="utf-8")
logfile.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(message)s", datefmt="%Y-%m-%dT%H:%M:%S"))
logging.basicConfig(level=logging.INFO, handlers=[screen, logfile], force=True)

lines, previous = load_for_checks(day)
log.info("loaded %s lines for %s", len(lines), day)
log.warning("%s product(s) below %s units", len(low), 500)
```

```
INFO loaded 213 lines for 2025-12-18
WARNING 1 product(s) below 500 units
```

- **`StreamHandler(sys.stdout)`** writes to the screen, like `stream=sys.stdout` above; in the script, `StreamHandler()` with no argument writes to stderr.
- **`Path("logs").mkdir(exist_ok=True)`** makes the `logs` folder if it isn't there. **`setFormatter(logging.Formatter(...))`** gives a handler its own layout, in the same codes as `format=`.
- **`FileHandler("logs/flash.log")`** adds each line to the end of a file. Its format adds **`%(asctime)s`**, the date and time, which the screen doesn't need but a file read next month does; `datefmt` writes it as `2026-01-05T07:00:12`, with no space inside, and `encoding="utf-8"` lets the file hold `₹`.
- **`basicConfig(..., handlers=[screen, logfile], force=True)`** sends every log line to both. `force=True` replaces the setup from the first cell, so no line is printed twice. `log` is the same logger as before: `getLogger("flash")` always returns the one logger with that name.
- **`log.warning("%s product(s) below %s units", len(low), 500)`** builds the message from the data (`low` from section 20.8), not from typed-in text.

The file has the same lines, with the time in front. Here are the last two, without the time, which changes every run:

```python
last_two = Path("logs/flash.log").read_text(encoding="utf-8").splitlines()[-2:]
for line in last_two:
    print(line.split(" ", 1)[1])          # everything after the first space: drop the timestamp
```

```
INFO loaded 213 lines for 2025-12-18
WARNING 1 product(s) below 500 units
```

Write a log line per run with the numbers that matter: rows read, total, exceptions raised, recipients, seconds taken. Then a run that produces a strange number can be explained a month later. Keeping the log in a table (a `run_history` table, or a sheet) also gives you the previous-run comparison for the checks.

### Failure alerts, "no data today", retries, and idempotency

- **Failure alert:** wrap the job in `try/except`, and on failure email a person (`FLASH_FAILURE_TO`) with the traceback, then exit non-zero so the scheduler also knows. A job that fails silently is worse than no job.
- **"No data today":** decide deliberately. For a daily sales report, send a short "no sales were recorded" note: a missing email is indistinguishable from a broken job.
- **Retries:** transient failures (a database restarting, a mail server timing out) deserve two or three retries with a growing pause. Permanent failures (a missing column) should not be retried; they should alert.
- **Idempotency:** running the job twice must not send two emails or double-load a table. Use a run key (`flash_2025-12-18`), record it, and exit early if it's already there.
- **Timeouts:** every network call gets one (Chapter 18, section 18.14), or one slow API holds the job forever.

```python
run_key = f"flash_{day}"
already_sent = {"flash_2025-12-17"}          # in a real job this comes from a table or a file
if run_key in already_sent:
    print(f"{run_key} already sent; exiting without sending again")
else:
    print(f"{run_key} not sent yet; proceeding")
```

```
flash_2025-12-18 not sent yet; proceeding
```

### The Flash, assembled

Every piece is now on the table. Here is how `companion/ch20/daily_flash.py` puts them together: its `main()` function, exactly as it is in the file. The functions it calls (`load`, `checks`, `build_html`, `build_message`, `send_message`, and the rest) are the cells of this chapter, tidied into functions further up the same file.

<!-- run: none -->
```python
def main(argv=None) -> int:
    args = parse_args(argv)
    day = date.fromisoformat(args.day) if args.day else datetime.now(IST).date()
    setup_logging()
    load_dotenv(Path(__file__).with_name(".env"))        # the .env next to this file -> os.environ
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
```

Block by block:

- **`def main(argv=None) -> int:`** `argv=None` means "read the real command line", but a test can pass a list, as in section 20.7; `-> int` is a note for human readers that the function returns a whole number (Python doesn't check it).
- **The first three lines** read the command line (section 20.7), set the day (today in India unless one is given; `IST` is `ZoneInfo("Asia/Kolkata")`, set once at the top of the file), and set up the log (screen and file, as above). **`load_dotenv(Path(__file__).with_name(".env"))`** reads the `.env` file that sits next to the script (section 20.5): `__file__` is the script's own path, and `.with_name(".env")` is the file called `.env` in the same folder, so it works whatever folder the scheduler starts in.
- **The run key.** When sending, it first checks `runs/sent_keys.txt`; if today's key is there, it logs that and stops with exit code 0. That is what makes a retry, or a second click, safe.
- **`try:`** wraps everything that can go wrong. **`--wait-for-load`** makes it wait for the overnight load first (exercise 22 builds the `load_status` table it reads; without the switch, it trusts the clock).
- **`load(...)`** runs the five queries: today's lines, the 14 days before, the 14 days ending today, the same day last year, and month to date.
- **The "no data today" branch.** No rows means the short "no sales recorded" email, not the checks and not an empty report.
- **The checks.** If any fails, it logs which, emails `FLASH_FAILURE_TO`, and returns **1**, so the scheduler sees a failure.
- **The report.** Headlines, the segment table, the exceptions, the chart with its action title, and the HTML with the `cid:` link. The **preview** copy swaps in a data URI and is written to `out/`, so you can always open what would have been sent.
- **`if args.send:`** builds the multipart message with the chart attached, sends it, and records the run key. Without `--send`, it only prints the subject line.
- **`except Exception:`** catches anything unexpected: `log.exception` writes the error and its traceback to the log, `alert_failure` emails the traceback to a person, and it returns **2**. If even the alert fails, that is logged too.
- **`return 0`, `1`, `2`** become the program's **exit code** (Chapter 17): 0 for success, 1 for "a check stopped it", 2 for "it crashed". The last line of the file, `sys.exit(main())`, hands it to the scheduler; it does the same as Chapter 17's `raise SystemExit(...)`.

Run it the way a scheduler would, without `--send`, for the Flash's day and for a day with no data:

```python
import subprocess

for day_text in ["2025-12-18", "2026-01-01"]:
    run = subprocess.run([sys.executable, "daily_flash.py", day_text], capture_output=True, text=True)
    print("exit code", run.returncode, "|", run.stdout.strip())
    print(run.stderr.strip(), end="\n\n")
```

```
exit code 0 | Riverstone Daily Flash — 18 Dec 2025 — ₹2,511,819 (+2.3% vs LY)
INFO loaded 213 lines for 2025-12-18
INFO revenue 2511819, orders 118, exceptions 1
INFO wrote out/daily_flash_2025-12-18.html

exit code 0 | Riverstone Daily Flash — 01 Jan 2026 — no sales recorded
INFO loaded 0 lines for 2026-01-01
WARNING no sales lines for 2026-01-01
INFO wrote out/daily_flash_2026-01-01.html
```

- **`subprocess.run([...], capture_output=True, text=True)`** runs the script as a separate program, as Chapter 18's monthly report did, and collects what it printed: `run.stdout` (the subject line) and `run.stderr` (the log lines). `sys.executable` is the Python running this notebook.
- **The first run** loaded 213 lines, found one exception, wrote the preview, and printed the subject line; the preview is `out/daily_flash_2025-12-18.html`, the page in Figure 20.3. **The second** found no lines, took the "no data" branch, and still wrote an email, because silence would look like a broken job.

With the test mail server from section 20.6 running, add `--send` and the email arrives in the second terminal. Run the same command again and the log says `flash_2025-12-18 already sent; nothing to do`: one email, however many times it runs.

---

## 20.12 Recipients and confidentiality

Most reporting incidents aren't wrong numbers. They're right numbers sent to the wrong people.

- **Keep the recipient list out of the code**, in a table or a config file with an owner and a review date. Lists made of individual addresses go stale; a distribution group maintained by IT doesn't.
- **Review the list quarterly.** People leave, change roles, and stay on lists for years.
- **Think about who sees what.** If branch managers shouldn't see each other's margins, either send per-branch emails from filtered data, or move to a dashboard with row-level security (Chapter 16, section 16.10). Never rely on a reader not scrolling.
- **Use `To` for people who must act and `Cc` sparingly.** Use `Bcc` for lists of external recipients so addresses aren't shared.
- **Attach deliberately.** The classic incident is an attachment with a hidden sheet, an unfiltered pivot cache, or last month's tab still in the workbook. If you attach an Excel file, generate it fresh from the data, don't reuse a template with old numbers inside.
- **Know what's sensitive.** Customer names, prices, margins, and salaries are not equally shareable. Ask before automating a report that contains any of them, and write the answer into the handover note.
- **Have a stop switch.** A `PAUSED=true` setting, or a single `enabled` flag in the config, so anyone can stop the sending without editing code.

---

## 20.13 Documenting and handing over

An automation is not finished when it runs; it's finished when someone else can own it. One page, kept with the code:

1. **What it does, in one sentence**, and who asked for it.
2. **When it runs**, in which time zone, on which machine, under which account.
3. **Inputs:** sources, tables, credentials (where they live, not what they are), parameters.
4. **Outputs:** what is produced, where it's written, who receives it.
5. **Checks:** what must pass before anything is sent, and what a failure means.
6. **Failure playbook:** the three most likely failures, how they look, and what to do. ("Refresh failed: the ERP load ran late. Rerun after 07:30 with `python daily_flash.py <date> --send`.")
7. **Owner and deputy**, with the date of the last review.

Two more habits make handover real: **run through it with the deputy once**, and **put the code in version control** (Chapter 26) rather than in a folder called `final_v3`.

---

## 20.14 Measuring what it saved

Automation is one of the few analyst activities with a simple business case, and analysts routinely fail to make it.

```python
minutes_before, minutes_after, runs_per_year = 80, 2, 250
hours_saved = (minutes_before - minutes_after) * runs_per_year / 60
print(f"{hours_saved:,.0f} hours a year, about {hours_saved/8:,.0f} working days")
hourly_cost = 300          # Riverstone's loaded staff cost: salary plus overheads, per hour
print(f"At ₹{hourly_cost} an hour, that is ₹{hours_saved * hourly_cost:,.0f} a year")
```

```
325 hours a year, about 41 working days
At ₹300 an hour, that is ₹97,500 a year
```

At Riverstone's rate the money is modest; the forty-one working days are the point, because they go to work that wasn't getting done. Record three things when you automate something: the time it took before (measured, not guessed), the time it takes now, and the errors it prevents. Then report it once a quarter, with the same discipline you'd apply to any other number. It's how the next automation gets approved, and how the work becomes visible to people who only see the output.

And keep a list of what to automate next, ordered by (time saved × frequency) ÷ effort. The top of that list is rarely the most interesting problem, which is exactly why it's worth writing down.

---

## Common mistakes

| Mistake | Symptom | Fix |
|---|---|---|
| Automating an unstable manual process | The script breaks every month | Stabilize at rung 2 first |
| Scheduling before the source is ready | Yesterday's numbers, silently | Check the load time; validate the date range |
| The answer in an attachment | Low open rates, "can you tell me the number instead?" | Put the headline in the subject and the body |
| Modern CSS in an email | Broken layout in Outlook | Tables, inline styles, 600–640 px |
| Images without `alt` and `width` | A blank box in half the clients | Always set both; the email must work image-free |
| The chart as a base64 data URI | No chart in Gmail or classic Outlook | Attach it as a related image and use `cid:` |
| Credentials in the script | A password in Git forever | Environment variables, `.env` outside version control |
| Sending from a personal mailbox | It stops when you leave or change your password | A service account or shared mailbox |
| Scheduled on a laptop | Fails on leave, on updates, on sleep | A server, VM, container, or cloud scheduler |
| Ignoring time zones | "Yesterday" differs from the reader's yesterday | Know the scheduler's clock; compute the date in the business time zone |
| A date typed into the scheduled command | The same day's report, every day | Let the script default to today in the business time zone |
| No checks | A wrong report, delivered on time | Checks that stop the send |
| No failure alert | Nobody notices for three weeks | Alert a person, and exit non-zero |
| Silence when there's no data | Indistinguishable from a broken job | Send "no sales were recorded" |
| Not idempotent | Two emails, or double-loaded data | A run key, recorded and checked |
| Alerts that fire daily | Everyone mutes them | Tune thresholds; use persistence and materiality |
| Alerts with no action | Anxiety, no decision | Say what to do and who owns it |
| Recipient list in the code | Stale lists; wrong people | A config table with an owner and review date |
| The wrong attachment | A real confidentiality incident | Generate fresh; never reuse a template with data |
| No documentation | "Only Meera knows how it works" | The one-page handover note |
| Never measuring | The work is invisible | Time before, time after, errors prevented |

---

## In the real world: the flash that stopped

Riverstone's Daily Sales Flash went live on a Monday in February 2026: 07:30 IST, a service account, fourteen recipients, KPI tiles in the body. Vikram Singh stopped asking for the morning numbers on WhatsApp within a week, which was the point.

On 4 March, the Flash arrived showing ₹0 revenue and zero orders, with the green line saying no products were below threshold. The exception logic had nothing to look at; the checks had not been written yet; the email was technically correct and completely useless. Three managers rang the analytics team in fifteen minutes, which was the fastest feedback Meera had ever received about a report.

The cause was dull: the overnight ERP load had failed at 02:10, and the Flash read an empty table at 07:30.

She changed four things that afternoon.

1. **Checks before sending.** Rows returned, all rows are today's, no missing revenue, and revenue within 60% of the recent median. On 4 March, two of the four would have failed, and the first alone is enough.
2. **A "no data" branch.** If there are no rows, the email says *"No sales were recorded on 4 March. If that looks wrong, check the overnight load"*, and the subject says so too. It's short, honest, and unmistakable.
3. **A failure alert to a person.** Any exception, or any failed check, emails the analytics team with the traceback and exits non-zero, so the scheduler's own alerting fires as well.
4. **A dependency, not a clock.** The Flash now waits for a row in a small `load_status` table saying the ERP load finished, retrying every ten minutes until 08:30, and alerts if it never arrives.

The last change is the one that mattered most, and it's the one people skip: a report scheduled at a time is guessing; a report that waits for its input knows.

Two months later, the same mechanism caught something better. On 12 May the Flash's median check failed: revenue was 71% below the recent median. Not a broken load this time — a branch had entered a day of orders against the wrong month, which would have made May look terrible and April suspiciously good. The check held the email, the analytics team looked, the branch fixed it before 10 a.m., and nobody outside three people ever knew.

What made the difference:

- **The failure was visible to the machine first**, and the machine told a person.
- **Silence was never an option:** either the report, or a clear statement that there was nothing to report.
- **The checks encoded what "wrong" means**, so they caught a data problem the author hadn't imagined.
- **It waited for its input** instead of trusting the clock.

---

## Project: Riverstone's Daily Sales Flash

**Goal:** an email that makes the morning call unnecessary, an exception alert when something is wrong, and a failure alert when the job breaks.

### Tools you'll need

- **Python**, as installed in Chapter 17 (section 17.0), with `pandas`, `matplotlib`, `SQLAlchemy`, a database driver, `python-dotenv`, `requests`, and `aiosmtpd`; on Windows, also `tzdata`. Everything runnable in this chapter was executed on Python 3.11 with pandas 3.0.6, matplotlib 3.10.8, SQLAlchemy 2.1.1, psycopg 3.3.6, python-dotenv 1.2.3, and aiosmtpd 1.4.6.
- **A test mail server first:** `aiosmtpd` on your own computer (section 20.6). Then **a mail route you're allowed to use:** SMTP with a service account, Microsoft Graph, the Gmail API, Apps Script's `MailApp` (Chapter 19), or a transactional provider.
- **A scheduler:** Windows Task Scheduler, cron, GitHub Actions, or a cloud scheduler.
- **Optional:** Power Automate, n8n, Make, or Zapier for delivery; Teams or Slack incoming webhooks.
- **Companion files (`companion/ch20/`):** `daily_flash.py`, the complete Daily Sales Flash: queries, checks, headline calculations, exception rule, 14-day chart, HTML builder, multipart message with the chart attached by CID, SMTP sender, failure alert, "no data" branch, run key, logging, arguments, and exit codes. It writes a preview of the email to `out/daily_flash_<date>.html`, which is the page shown in Figure 20.3. `.env.example` lists the settings; copy it to `.env` and fill it in.

> **Before you send anything real.** Sending mail, posting to webhooks, and scheduling need accounts you control. Test the email with the local mail server from section 20.6, test a webhook on a channel you own, and run a scheduled job against the test server for a few days before you point it at real inboxes.

**Option A: your own report.** Take the report you produce most often and put it on rungs 2 and 3 of the ladder.

**Option B: Riverstone.** Build `daily_flash.py` yourself before reading the companion version.

**Steps**

1. **Map the flow** and time the manual steps for a week. Write down what you'll automate and what stays judgment.
2. **One query** for the day's lines, one for the last 14 days, one for the same day last year.
3. **Headline numbers:** net revenue, orders, customers, average order value, gross margin, month to date, and the comparison with last year.
4. **Four checks that can stop the send**, including one that compares today with the recent median.
5. **The exception rule:** products below a threshold, with the threshold in one named constant and a plan to base it on history later.
6. **The email:** subject line with the headline, four KPI tiles, a 14-day chart, a segment table, the exception box (or the green "none today" line), and a footer saying where it came from.
7. **Sending:** SMTP or your workspace's API, credentials from `.env`, recipients from config, the chart attached by CID, and `--send` off by default so you can look at the HTML first. Test on the local mail server.
8. **Failure handling:** try/except around everything, an alert to a person, a non-zero exit code, the "no data" branch, a run key so a second run sends nothing, and a log line per run.
9. **Schedule it** so it arrives by 07:30 business time (07:00 on weekdays), with no date in the command, and make it wait for (or check) the source load.
10. **Write the handover page** and the hours-saved calculation.

**What good looks like (18 December 2025):** net revenue **₹25,11,819**, **118** orders from **116** customers, average order **₹21,287**, gross margin **27.3%**, **+2.3%** on the same day last year, month to date **₹5.71 crore**, and **one** exception (Industrial Crate, 345 units). Your email will show the revenue as `₹2,511,819`, Python's grouping. Running it twice sends one email.

**Stretch goals**

- Add the formatted workbook from Chapter 18 as an attachment for the two people who want it, and nobody else.
- Send each branch manager only their branch's numbers, from the same script.
- Post a two-line summary to a Teams or Slack channel at the same time, linking to the Power BI report from Chapter 16.
- Store each run's headline numbers in a `run_history` table, and use it for the "versus recent median" check instead of recomputing.

---

## Timed challenge: forty minutes

Use `riverstone_full` and Python. Answers at the end of the chapter.

- **Level 1:** For 18 December 2025, compute net revenue, orders, customers, and average order value.
- **Level 2:** Compute the same day's gross margin percentage, and the comparison with 18 December 2024.
- **Level 3:** Month-to-date revenue to 18 December 2025.
- **Level 4:** The 14-day daily series ending that day: which day was highest, and which lowest?
- **Level 5:** Products selling fewer than 500 units that day.
- **Level 6:** Write the subject line your script would send, with the headline number and the comparison.
- **Level 7:** Write the four checks and run them for 18 December 2025 and for a date with no data (1 January 2026). What happens in each case?
- **Bonus:** Compute the hours saved a year if the manual version took 80 minutes and the automated one takes 2, at 250 runs a year.

---

## Recap

- **The ladder** runs manual → refreshable → scheduled → triggered → self-serve. Stabilize before scheduling; everything above rung 2 needs an owner, a log, and a failure alert.
- **Map the flow and time it** before automating. Automate the mechanical steps, keep the judgment, and give the judgment a place in the output.
- **Choose the tool** from where the data lives and who will maintain it: VBA, Apps Script, Python, BI subscriptions, or a low-code flow.
- **Put the answer in the email body**, with the headline in the subject. Attachments are for people who asked for them.
- **Email HTML is old HTML:** tables, inline styles, 600–640 px, web-safe fonts, images with `alt` and `width`, no JavaScript. Attach the chart as a related image and point at it with `cid:`; a base64 data URI is only for previewing in a browser.
- **Send from a service account**, with credentials in a `.env` file that is never committed, through SMTP, Graph, Gmail, or a provider. Build the multipart message, then test it on a local mail server before any real inbox.
- **Schedule in business time:** know which clock the scheduler uses, let the script work out today in the business time zone (`zoneinfo`), use absolute paths in cron, and prefer waiting for the source load over trusting the clock.
- **Alerts are not reports:** thresholds based on history (a per-product percentile, read before it's adopted), persistence, materiality, an action, an owner, and a periodic review of whether anyone acted.
- **Trustworthy means:** it logs to the screen and a file, it checks before sending (rows first: `.all()` of nothing is `True`), it alerts a person when it breaks, it handles "no data today", it can run twice, and someone else can run it.
- **Recipients and confidentiality** are where real incidents happen: config-driven lists, quarterly review, per-recipient filtering or row-level security, deliberate attachments, and a stop switch.
- **Document and hand over**, then **measure**: 80 minutes to 2, 250 times a year, is 325 hours.

---

## Key terms

automation ladder · refreshable · scheduled · triggered · self-serve · report flow map · delivery tool · formatted Excel · PDF · CSV extract · HTML email · KPI tile · inline styles · table layout · web-safe font · `alt` text · environment variable · `.env` file · `load_dotenv` · bytes · `BytesIO` · base64 · data URI · Content-ID (`cid:`) · related image · SMTP · host and port · STARTTLS · MIME type · multipart message · `EmailMessage` · attachment · test mail server (`aiosmtpd`) · service account · shared mailbox · Microsoft Graph · Gmail API · transactional provider · Task Scheduler · cron · crontab · `CRON_TZ` · working directory · cloud scheduler · time zone · `zoneinfo` · `astimezone` · reporting date · alert · exception report · threshold · percentile threshold · persistence · materiality · alert fatigue · incoming webhook · Teams Workflows · Adaptive Card · Block Kit · WhatsApp Business API · low-code · Power Automate · n8n · Make · Zapier · logging · logger · log level · log handler · log file · stdout and stderr · `argparse` · positional argument · option · run history · check · failure alert · exit code · "no data today" · retry · idempotency · run key · recipient list · row-level filtering · stop switch · handover note · hours saved

*(All terms are defined in the Glossary, Appendix A.)*

---

## Check yourself

- [ ] You can place a report on the ladder and say why it should stop there.
- [ ] You map a flow and time the steps before writing code.
- [ ] You choose the delivery tool from where the data and the maintainer are, not from preference.
- [ ] You put the answer in the subject line and the body, and attach only what's actually needed.
- [ ] You can build an HTML email that renders in Outlook and Gmail: tables, inline styles, 640 px, `alt` text, and the chart attached by `cid:`.
- [ ] You send mail with credentials from a `.env` file, from an account that isn't personal, and test it on a local mail server first.
- [ ] You schedule in business time, know which clock your scheduler uses, let the script work out the reporting date, and know why cron needs absolute paths.
- [ ] Your alerts have thresholds with a rationale, an action, and an owner, and you review whether anyone acts on them.
- [ ] Your automations log every run, check before sending, alert a person on failure, say "no data today", and can be run twice safely.
- [ ] Your recipient list lives in config with a review date, and you've thought about who may see what.
- [ ] There's a one-page handover note, and someone else has run the job.
- [ ] You can state the hours the automation saves and the errors it prevents.

---

## Exercises

Use `riverstone_full`, `companion/ch20/daily_flash.py`, and your own email account only where it's safe.

### Warm-up

1. Place each on the ladder and say what it would take to move it up one rung: a weekly stock count pasted into a workbook; a Power BI report with a subscription; a monthly pack built by a macro; an ad-hoc pricing analysis.
2. A report is scheduled at 06:00 and the source table loads at 06:30. What are three ways to fix it, and which is best?
3. Why does an attachment lower the chance a report is read? When is an attachment still the right choice?
4. Name four things that break HTML email layout, and the safe alternative for each.
5. Where should database and SMTP credentials live, and what's wrong with each of these: in the script; in a config file committed to Git; in the scheduler's command line?
6. What's the difference between a report and an alert, and what happens when you mix them?

### Core

7. Run `daily_flash.py` for 18 December 2025 without `--send` and open the HTML. What are the four KPI values?
8. Change the exception threshold to 800 units and rerun. How many exceptions appear, and which products?
9. Run it for 1 January 2026 (a date with no data). What does it produce, and why is that better than sending nothing?
10. Add a fifth KPI tile showing the number of order lines, and check that the row of tiles still fits at 640 px.
11. Write the four checks from section 20.11 as a function and run them for 18 December 2025. What does each report?
12. Deliberately break a check (for example, require revenue within 5% of the median) and confirm that nothing is sent and the log says why.
13. Add a `run_history` table (or a CSV) that records the date, revenue, exceptions, and run time. Use it to make the job idempotent.
14. Move section 20.8's percentile rule into `daily_flash.py` in place of the fixed 500 units. Which products would be flagged on 18 December 2025, and which on 17 December?
15. Write the subject line generator, including the "no data" case, and test it for both dates.
16. Add a plain-text alternative to the email and confirm the message has both parts.
17. Write the Task Scheduler or cron entry that runs the Flash at 07:00 India time on weekdays, on a server whose clock is UTC, including the working folder and log redirection.
18. Write a `post_to_webhook` function for Teams or Slack and a two-line summary message. (Test it only against a channel you own.)
19. Draft the one-page handover note for the Flash, using the seven headings in section 20.13.
20. Calculate the hours saved for a report in your own work, and write the two sentences you'd put in a quarterly update.

### Stretch

21. Send each branch manager only their branch's numbers from one run, and explain how you'd verify that nobody received another branch's figures.
22. Make the job wait for a `load_status` row instead of trusting the clock, with retries every ten minutes until 08:30 and an alert if it never arrives.
23. Add a weekly digest on Mondays that summarizes the week's exceptions, so daily alerts can be reserved for what needs same-day action.
24. Rebuild the delivery half in a low-code tool (Power Automate, n8n, or Make) with Python producing the data, and compare maintainability.
25. Chapter 17's `summarize_exports.py` reads its folder from `sys.argv`. Give it proper options with `argparse`: `python summarize_exports.py sales_exports --month 2025-10 --output summary.md`, where `--month` summarizes one month only. Keep the docstring, the functions, and the exit code.
26. Add `logging` at INFO level to the same script: one line when it starts, one per file processed, one warning per unreadable row, and one line with the total at the end.

### Think about it

27. Your Flash has run for six months. How would you find out whether anyone still reads it, and what would you do if the answer is "two people"?
28. A manager asks for a daily alert whenever any customer's order is 20% below their average. What do you ask before building it?
29. An automation you built emails a confidential margin report to a list that turns out to include a contractor. What do you do in the first hour, and what do you change afterwards?

---

## Answers

**1.** Weekly stock count: rung 1 → rung 2 by making the paste a Power Query refresh. Power BI subscription: rung 3 already; rung 4 would be a data-driven alert, rung 5 is self-serve, which it partly is. Monthly macro pack: rung 3 if scheduled, rung 2 if someone clicks the button; move it up by scheduling it somewhere that isn't a laptop. Ad-hoc pricing analysis: rung 1, and it should stay there.

**2.** (a) Move the schedule to 07:00 and hope; (b) check the data before reporting and fail if it's stale; (c) make the job wait for a "load finished" signal and retry. (c) is best, (b) is the minimum, and (a) is what most teams do until it bites.

**3.** An attachment needs a download, an app, and a second decision, and on a phone it's often impossible. It's right when the reader will work with the data (filter, pivot, paste into a model), or when a fixed record is needed for compliance.

**4.** Flexbox or grid → tables; `<style>` blocks or external CSS → inline styles; web fonts → web-safe fonts with fallbacks; wide layouts → 600–640 px; also images without `width`/`alt` → always set both.

**5.** In environment variables, loaded from a `.env` file that isn't committed, or a secret manager. In the script: they end up in Git and in everyone's copy. In a committed config file: the same problem with extra steps. On the scheduler's command line: visible in process lists and logs.

**6.** A report arrives on a schedule and shows the full picture; an alert arrives when something is wrong and names one problem and an action. Mixed, the alert becomes routine and gets ignored, and the report becomes noisy.

**7.** The tiles show net revenue `₹2,511,819` (+2.3% vs last year) · **118** orders from 116 customers · average order `₹21,287` with 27.3% margin · month to date `₹5.71 cr`.

**8.** At 800 units, four products are flagged: Industrial Crate (345), Storage Box 25L (575), Water Bottle 1L (600), and Lunch Box Set (790). That's the tuning problem in one experiment: the threshold decides whether the alert is useful or noise.

**9.** It writes the "No sales were recorded on 01 Jan 2026" email, with "no sales recorded" in the subject too, logs a warning, and exits with code 0. It's better than silence because a missing email is indistinguishable from a broken job, and better than an empty table because it tells the reader what to check.

**10.** Five tiles at 640 px are cramped; either drop to four, use two rows of two, or shorten the labels. The answer is a design decision, and the check is opening it on a phone.

**11.** On 18 December 2025: rows returned PASS (213 lines), all rows are today's PASS, no missing revenue PASS, revenue within 60% of the recent median PASS (₹25,11,819 against a median of ₹32,09,520 for 4–17 December).

**12.** Set `MEDIAN_BAND = 0.05`. The median check fails, the job logs `check failed: revenue within 5% of recent median (…)`, writes no email, alerts `FLASH_FAILURE_TO`, and exits with code 1. That's the behaviour you want; the lesson is that too tight a threshold turns a safety net into a blocker.

**13.** Store `run_key`, date, revenue, exception count, and duration. At the start, `SELECT 1 FROM run_history WHERE run_key = :key`: if it exists, log and exit 0 without sending.

**14.** On 18 December 2025, six of the seven products are below their own 10th percentile of the previous 90 days: Storage Box 25L (575 against 922.5), Water Bottle 1L (600 against 991), Lunch Box Set (790 against 811), Food Container Set (855 against 987), Storage Box 10L (1,005 against 1,232) and Stackable Bin (1,240 against 1,266). Industrial Crate, the only product under the fixed 500, is not flagged (345 against 267): it always sells little. On 17 December only Food Container Set is flagged (960 against 990). The relative rule stops flagging a product for being small and catches a normally busy product having a bad day, but on a generally quiet day it fires for almost everything, so pair it with persistence or a materiality floor.

**15.** `f"Riverstone Daily Flash — {day:%d %b %Y} — ₹{revenue:,.0f} ({vs_ly:+.1f}% vs LY)"`, and for the empty case `f"Riverstone Daily Flash — {day:%d %b %Y} — no sales recorded"`.

**16.** `message.set_content(...)` then `message.add_alternative(html, subtype="html")` gives a `multipart/alternative` message; check with `message.get_content_type()` and by viewing the source in the client.

**17.** cron, on a UTC server (07:00 India time is 01:30 UTC): `30 1 * * 1-5 cd /opt/riverstone && /opt/riverstone/.venv/bin/python daily_flash.py --send >> logs/cron.log 2>&1`. With cronie (Red Hat, Fedora) you can instead put `CRON_TZ=Asia/Kolkata` above `0 7 * * 1-5 …`. Task Scheduler: program = the venv's `python.exe`, arguments = `daily_flash.py --send` (no date: the script works out today in India), **Start in** = the script folder, trigger weekly on Monday to Friday at the local time that is 07:00 in India, with restart on failure. Never put a date in a scheduled command: a fixed one sends the same day forever, and `%date%` is not expanded by Task Scheduler and would be in the machine's local format in a batch file anyway.

**18.** See section 20.9. The summary should be two lines: the headline number with the comparison, and the exception count, plus a link to the dashboard.

**19.** The seven headings from section 20.13, filled in for the Flash: what and who asked; 07:00 IST on weekdays, arriving by 07:30, on the reporting VM under the `svc-analytics` account; sources and credentials; outputs and recipients; the four checks; the three likely failures with commands to rerun; owner and deputy with a review date.

**20.** For example: *"Automating the daily flash replaced 80 minutes of manual work with 2, 250 times a year: about 325 hours, or 41 working days. It has also caught two data errors before they reached managers."*

**21.** Loop the branches, filter the data, and send one email per branch, with the branch in the subject. Verify by logging, for each send, the recipient and a hash or total of the data sent, then spot-check three; and by sending the first run to yourself with the branch name in the body.

**22.** Create a small `load_status` table (`load_date`, `status`) in a database you're allowed to write to, and have the load (or you, while testing) insert a `finished` row. `daily_flash.py --wait-for-load` already polls it every ten minutes: if the row appears, it runs; if 08:30 passes without it, it raises an error naming the missing load, and the `except` block sends the failure alert. Log each attempt so a late load is visible afterwards.

**23.** A Monday job that reads `run_history` and the exception log for the previous week, groups by product and branch, and sends one digest. Daily alerts then carry only same-day actions, which is what keeps them credible.

**24.** Python writes the day's numbers to a table or a JSON file; the flow reads it, formats the message, and sends it. Maintainability improves for the business (they can change recipients and wording) and worsens for you (logic split across two places): document where the boundary is.

**25.** Replace the `sys.argv` lines with a parser: `parser.add_argument("folder", nargs="?", default="sales_exports")`, `parser.add_argument("--month")` (default `None`, meaning every month) and `parser.add_argument("--output")` (default `None`, meaning print to the screen), then `args = parser.parse_args()`. Pass `args.folder`, `args.month` and `args.output` to `main()`, when `args.month` is given, read only that month's file (the exports are named by month, so `--month 2025-10` means `riverstone_2025_10.csv`: `Path(folder).glob(f"*{args.month.replace('-', '_')}.csv")`), write the summary to `args.output` if it is given, and keep `raise SystemExit(main(...))` so the exit code still reaches the terminal. `python summarize_exports.py --help` now lists all three.

**26.** Once, at the start of `main()`: `logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")` and `log = logging.getLogger("summary")`. Then `log.info("starting: %s", folder)`, `log.info("reading %s", path)` for each file, `log.warning("row %s unreadable: %r", line_no, value)` for a bad row, and `log.info("total %s", total)` at the end. Use `%s` placeholders, not f-strings, in logging calls. Run it from the terminal: the log lines go to stderr, so `python summarize_exports.py > summary.txt` puts the summary in the file and still shows the log on the screen.

**27.** Ask the mail platform for open rates if you have them, put a tracked link to the dashboard in the footer and watch the clicks, or stop sending it for a week and see who asks. If two people read it, either narrow it to those two, fold it into a weekly digest, or replace it with an alert; a report read by two people is not a failure if those two make decisions with it.

**28.** What decision follows the alert? How many customers, and therefore how many alerts a day? What's "average": mean or median, over what period? Does a 20% drop matter for a ₹5,000 customer? Who acts, and by when? And would a weekly list of the twenty biggest declines serve better than daily alerts?

**29.** First hour: stop the schedule (the stop switch), find out exactly what was sent and to whom, tell your manager and whoever owns data protection, and don't try to recall the email quietly. Afterwards: recipient lists in config with an owner, a review date, and a check that every recipient is on an approved domain; a test send to yourself on every change; and sensitivity written into the handover note.

**Timed challenge answers.** Level 1: ₹25,11,819 · 118 orders · 116 customers · ₹21,287 average order. Level 2: 27.3% gross margin; +2.3% against 18 December 2024's ₹24,54,466. Level 3: **₹5,70,69,985** (₹5.71 crore) from 1 to 18 December. If you get ₹4.45 crore, your window started on the 5th, not the 1st: reusing the 14-day series for month to date is the most common slip, and it was a real bug in the first version of `daily_flash.py`. Level 4: highest **7 December (₹37,82,009)**, lowest **9 December (₹24,88,217)**; the 18th itself is ₹25,11,819, a little above the low. Level 5: Industrial Crate, 345 units. Level 6: `Riverstone Daily Flash — 18 Dec 2025 — ₹2,511,819 (+2.3% vs LY)`. Level 7: all four pass for 18 December 2025; for 1 January 2026 the row check and the median check fail (the other two pass because there is nothing to test), so no report is sent, and the "no data" email goes out instead. Bonus: 325 hours, about 41 working days.

---

## Where this leads

- **Chapter 21 and 22:** the statistics behind sensible thresholds, and why a single day's dip usually isn't a signal.
- **Chapter 24, Requirements, Storytelling & Stakeholders:** what to write in the three sentences of commentary you kept.
- **Chapter 26, The Professional Toolkit:** the terminal in more depth (section 26.0), versioning automations with Git, and keeping `.env` out of the repository.
- **Chapter 29, Python as Software:** packaging, tests, and configuration once a script becomes a tool several people depend on.
- **Chapter 46:** orchestration, when "run this at 7" becomes "run these eleven things in the right order, with retries".
- **Chapter 47:** data-quality testing, which is the checks in this chapter done systematically.
- **Interview preparation:** the Automation & Integration Question Bank (Chapter 78) asks how you'd automate and deliver a recurring report, and what you'd do when it fails; the Business Analyst bank (Chapter 76B, Q76B-038) asks how you'd specify the requirement for one.
