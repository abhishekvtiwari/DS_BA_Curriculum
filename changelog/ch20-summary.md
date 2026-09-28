# Chapter 20, Automating Reports & Delivering Insights: summary of the Part 2 build

**Findings handled:** 26 content (20.1–20.26), 17 visual (V20.1–V20.17), 6 Reader's Journey rows.
Fixed or verified: 25 of 26 content rows (20.22 is Open and was left alone), all 17 visual rows. Reader's Journey:
Ch 20's share of RJ-S2-7 done (bare "Chapter 76" → 76B); RJ-S2-15, RJ-S3-15, RJ-S3-31 need nothing here; RJ-S1-1 Open.

## What changed

- **The techniques now work in practice.** The chart goes by CID (a related image), which Gmail and Outlook show; the
  data URI is kept only for a browser preview (20.1). The scheduled command has no date: the script works out today in
  India with `zoneinfo` (20.2). cron is set against the server's clock, with `CRON_TZ` explained as cronie-only
  (20.3). The time-zone cells now show the bug (20.4).
- **The Flash is shown whole.** "The Flash, assembled" (end of §20.11) prints the real `main()` of `daily_flash.py` and
  runs it for a normal day and a no-data day (20.5). The companion script was rewritten to match the chapter: checks
  that stop the send, the no-data branch, a run key, `--send` off by default, exit codes 0/1/2, a CID chart, a
  browser preview, logging to screen and file, and an optional wait for `load_status`.
- **Nothing is used before it's taught.** HTML (pointer to Ch 19's box, the tile by hand first, 20.6); `.env` and
  `python-dotenv` (20.9); SMTP, ports, STARTTLS, MIME and multipart, tested on a local `aiosmtpd` server (20.8); the
  shell pieces of the cron line and `crontab -e` with nano (20.10); per-product percentiles (20.18); logging and
  `argparse`, which Ch 17's rebuild now leaves to Ch 20.
- **Correct numbers and names.** Industrial Crate 345 (20.11), 47 working days (20.12), 41 days everywhere (20.13), two of
  four checks (20.14), a real 14-day chart (20.7), date-based windows and month to date ₹5,70,69,985 (20.19),
  credentials from the environment (20.20), Teams Workflows and Adaptive Cards (20.16), classic versus new Outlook
  (20.25), cross-references (20.21, 20.23), drafting leftovers removed (20.24), Ch 17 §17.0 in Before you start (20.26).
- **Facts applied:** loaded rate ₹300/hour (so ₹97,500 a year, not ₹390,000); the Flash is sent by 07:30 IST (runs
  at 07:00).
- **Figures.** 20.1, 20.2 and 20.5 redrawn at 700 px (smallest text 7.4–7.75 pt; it was 4.4–4.8), without in-figure
  titles. 20.3 (the email) re-rendered from the new script at 315 ppi, framed as an email window with its subject
  line. New Figure 20.4: the KPI tile as a browser draws it.

## Skipped or changed from the finding, and why

- **20.22 left Open** (held by Abhishek's renumbering decision).
- **20.5:** the assembled script is a `###` subsection at the end of §20.11, not "§20.11a", so §20.12–20.14 keep their
  numbers (Ch 63 cites 20.13 and 20.14). `main()` is 62 lines, not ~45, because it is the real file's function.
- **20.1:** the message's structure is shown with `walk()` rather than `print(msg)`, whose boundaries are random and
  whose image is thousands of lines of base64; the raw headers appear in the test server's real printout.
- **20.3:** `CRON_TZ` is presented as a cronie (Red Hat/Fedora) feature: Ubuntu/Debian cron doesn't support it (checked
  in both man pages). The cron line is written for a UTC server instead.
- **20.9:** the `.env` subsection sits in §20.5, not §20.6, because the chart now reads the database first.
- **20.16:** no sample webhook response is printed: none can be produced without a real channel. Slack's `200`/`ok`
  is quoted from Slack's SDK docs.
- **20.17:** kept Microsoft's restart-on-failure setting, but the text warns that a script's error exit may not count as
  a failed task (Microsoft's reference says only "if the task fails"), so the script does its own waiting.

## Option picks

20.12 and 20.13: the first option each ("47 working days… two months"; "about 41"). 67.9: lakh grouping in prose.
All other rows had one change.

## Time needed

**20–25 hours over two to three weeks** (was 18–22). About 14 new cells, the assembled script, and two hours of setup
(`.env`, the test mail server, a scheduler), as the content review estimated.

## Verification

- `tools/verify_python.py manuscript/ch20-*.md --cwd companion/ch20`: **22 blocks run, 22 outputs checked,
  0 mismatches** (needs `companion/ch20/.env`; `checks/ch20_check.py` creates it from `.env.example`).
- `checks/ch20_check.py`: **8 of 8 pass**: the `run: none` SMTP cell against a real `aiosmtpd` server, the server
  excerpt, `daily_flash.py --send` twice (one email), answer 14's numbers, and `main()` matching the file.
- MySQL month-to-date form run in MySQL: 57069985.00.
- `tools/pdf/fig_check.py`: 0 figures under 7 pt. `tools/restructure.py --check`: already in order.
- Rebuilt PDF (46 pages): `layout_check.py` clean (no stranded heads or lead-ins, no sparse pages, no small text, no
  tofu, map 20/20); `prescan.py` clean ("Draft" is exercise 19's verb).
