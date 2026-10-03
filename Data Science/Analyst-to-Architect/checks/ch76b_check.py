#!/usr/bin/env python3
"""ch76b_check.py - checks Chapter 76B (Business Analyst Question Bank) against the chapters it cites.

Usage: python3 checks/ch76b_check.py        (run from the book folder)

1. Every section number cited in Ch 76B ("section 25.8", "Chapter 24, section 24.1", "| Mid · 25.7; 24.1 |")
   exists as a "## NN.M" heading in the current manuscript.
2. Every fact Ch 76B takes from another chapter appears inside the section it is credited to
   (requirement numbers, the rule, the lanes, Figure numbers, terms).
3. Question IDs run Q76B-001 ... Q76B-095 with no gaps or duplicates, and no old "Q76-" / "76.N" labels remain.
4. The at-risk rule's counts quoted in Q76B-013 (3 flagged, 7 too new of 24 key accounts on 31 Dec 2025)
   are recomputed from riverstone_2025 with Chapter 25's own query (skipped if PostgreSQL is unreachable).
Exit code 1 on any failure.
"""
import glob, re, subprocess, sys

MS = "manuscript"
ch = open(glob.glob(f"{MS}/ch76b-*.md")[0], encoding="utf-8").read()
fails = 0


def chapter(n):
    return open(glob.glob(f"{MS}/ch{n:0>2}-*.md")[0], encoding="utf-8").read()


def section(n, sec):
    text = chapter(n)
    m = re.search(rf"^## {n}\.{sec} .*?(?=^## )", text, re.S | re.M)
    return m.group(0) if m else None


def ok(cond, msg):
    global fails
    if not cond:
        fails += 1
        print("FAIL:", msg)


# 1. every cited section exists
cited = set()
for m in re.finditer(r"sections? ((?:\d{1,2}\.\d{1,2}(?:,? (?:and )?)?)+)", ch):
    cited.update(re.findall(r"\d{1,2}\.\d{1,2}", m.group(1)))
for m in re.finditer(r"\| (?:Fresher|Mid|Senior) · (.+?) \|$", ch, re.M):
    cited.update(re.findall(r"\b\d{1,2}\.\d{1,2}\b", m.group(1)))
for c in sorted(cited, key=lambda s: tuple(map(int, s.split(".")))):
    n, sec = c.split(".")
    ok(section(n, sec) is not None, f"section {c} not found")
print(f"sections cited: {len(cited)}: {', '.join(sorted(cited, key=lambda s: tuple(map(int, s.split('.')))))}")

# 2. facts are in the credited section
QUOTES = [
    ("3", "2", ["types the order in", "invoice 9001", "proof of delivery", "SHARMA HW JAN", "paid in two instalments"]),
    ("3", "7", ["**8. Delivery**", "**9. Payment**"]),
    ("23", "13", ["Defining a metric"]),
    ("24", "1", ["What's the scope, explicitly?", "*out* of scope"]),
    ("24", "2", ["A **business rule** is a definition", "trailing 90 days"]),
    ("24", "3", ["power–interest grid", "stakeholder register", "RACI", "Manage closely", "Monitor"]),
    ("24", "4", ["Bottom line up front", "pyramid principle"]),
    ("24", "7", ["Presenting to executives"]),
    ("24", "8", ["can you just change the number?", "Figure 24.4", "Hold the number"]),
    ("25", "1", ["Elicit.", "Analyze.", "Specify.", "Validate."]),
    ("25", "2", ["**1 Requirements**", "**2 Design**", "**3 Build**", "**4 Test**", "**5 Deploy**", "**6 Maintain**",
                 "The names of the phases vary; the sequence does not", "writes or reviews the UAT plan", "Waterfall and Agile"]),
    ("25", "3", ["The discipline, in five moves", "exception path", "Ask how often"]),
    ("25", "4", ["Figure 25.1", "Five of the nine transitions cross a lane", "4 order typed into the ERP",
                 "5 stock check and reserve", "8 signed proof of delivery scanned", "9 payment matched",
                 "the room starts talking", "BPMN", "diamonds for decisions", "As-is before to-be"]),
    ("25", "5", ["business requirement", "non-functional requirement", "no more than two hours old during working hours",
                 "reconcile to the ERP's own figure to the rupee"]),
    ("25", "6", ["FR-01", "FR-03", "1.5 times", "at least four days of orders", "NFR-01.** Data shall be no more than one working day old",
                 "Seven of the 24 key accounts are too new to judge", "only accounts where they are the assigned rep"]),
    ("25", "7", ["Business Requirements Document", "two developers reading it build the same thing",
                 "readable by someone who will never log in", "requirements traceability matrix", "Chapter 11's skills",
                 "scope and what is out of scope", "assumptions"]),
    ("25", "8", ["Figure 25.3", "AC-5", "reconciliation criterion", "Given, When, Then", "use case"]),
    ("25", "9", ["Figure 25.4", "FR-14 and NFR-09", "root cause", "scan faster", "Ranking the gaps"]),
    ("25", "10", ["QA** verifies the system works as specified", "at more than one level of aggregation",
                  "If the BA drives the mouse, the test measures the BA", "Who signs off", "triage"]),
    ("25", "11", ["Every decision that changes scope gets written down", "change request"]),
    ("25", "12", ["BR-05", "BR-06", "FR-15", "FR-16", "FR-17", "within ₹1", "named person", "audit trail",
                  "how often does the exception happen"]),
    ("26", "10", ["Scrum", "sprints", "backlog"]),
    ("63", "9", ["Change management"]),
    ("69", "3", ["Move 1: Clarify first", "Move 2: State assumptions"]),
]
for n, sec, needles in QUOTES:
    text = section(n, sec) or ""
    for s in needles:
        ok(s in text, f"'{s}' not in section {n}.{sec}")
# facts that live in figure SVGs, not in the prose
fig254 = open("figures/fig25-4-gap-analysis.svg", encoding="utf-8").read()
for s in ["FR-14: the delivery status and date shall be recorded in the ERP within one hour of the proof of",
          "NFR-09: a delivery recorded where there is no mobile signal shall reach the ERP within one hour of",
          "the driver has no device"]:
    ok(s in fig254, f"'{s}' not in Figure 25.4")
fig253 = open("figures/fig25-3-user-story-anatomy.svg", encoding="utf-8").read()
ok("to see which of my accounts are at risk of not ordering again" in fig253, "story text not in Figure 25.3")
ok("Common mistakes" in chapter(25) and "Agreeing a scope change in a corridor" in chapter(25), "Ch 25 corridor mistake missing")

# the lane assignment quoted in Q76B-018 gives five of nine cross-lane transitions
lanes = {1: "C", 2: "S", 3: "S", 4: "S", 5: "W", 6: "W", 7: "F", 8: "W", 9: "F", 10: "F"}
crossings = sum(lanes[i] != lanes[i + 1] for i in range(1, 10))
ok(crossings == 5, f"cross-lane transitions {crossings}, expected 5")

# 3. IDs
ids = re.findall(r"\bQ76B-(\d{3})\b", ch)
heads = [int(x) for x in re.findall(r"^### Q76B-(\d{3})", ch, re.M)] + \
        [int(x) for x in re.findall(r"^\| Q76B-(\d{3}) \|", ch, re.M)]
ok(sorted(heads) == list(range(1, 96)), f"question IDs not 1..95 exactly once: {sorted(heads)}")
ok(not re.search(r"\bQ76-\d", ch), "old Q76- ID left")
ok(not re.search(r"§ ?76\.\d|section 76\.\d|^## 76\.\d", ch, re.M), "old 76.N section label left")
for m in re.findall(r"section 76B\.(\d)", ch):
    ok(re.search(rf"^## 76B\.{m} ", ch, re.M), f"section 76B.{m} cited but missing")
# tags: only Chapter 69's twelve
TAGS = {"Clarify", "Assume", "Signpost", "Simple first", "Edge cases", "Trade-offs", "Validate", "Business",
        "Scale", "Limits", "Evidence", "Close"}
for t in re.findall(r"\*\*\[\+([^\]]+)\]\*\*", ch):
    ok(t in TAGS, f"unknown tag [+{t}]")
ok(not re.search(r"\*\*\[(?!\+)[A-Z][^\]]*\]\*\*", ch), "old-style [Tag] left")
ntags = len(re.findall(r"\*\*\[\+", ch))
print(f"question IDs: {len(heads)}; tags used: {ntags}")

# 4. the at-risk counts, from Chapter 25's own query
q = re.search(r"(WITH order_days AS.*?ORDER BY verdict, customer_name;)", chapter(25), re.S).group(1)
try:
    out = subprocess.run(["su", "postgres", "-c", "psql -d riverstone_2025 -At -F '|'"], input=q,
                         capture_output=True, text=True, timeout=60).stdout
    rows = [r.split("|") for r in out.strip().splitlines()]
    if rows:
        at_risk = sum(r[-1].startswith("at risk") for r in rows)
        too_new = sum(r[-1] == "too new to judge" for r in rows)
        total = subprocess.run(["su", "postgres", "-c", "psql -d riverstone_2025 -Atc 'select count(*) from customers'"],
                               capture_output=True, text=True).stdout.strip()
        print(f"at-risk rule on 2025-12-31: {at_risk} flagged, {too_new} too new, of {total} key accounts")
        ok((at_risk, too_new, total) == (3, 7, "24"), "at-risk counts differ from the chapter (3, 7, 24)")
        ok("flags 3 of them, and 7 are too new to judge" in ch and "24 key accounts" in ch, "counts not quoted as checked")
    else:
        print("SKIP: PostgreSQL not reachable; at-risk counts not recomputed")
except Exception as e:  # noqa: BLE001
    print("SKIP: PostgreSQL not reachable:", e)

print("OK" if not fails else f"{fails} failure(s)")
sys.exit(1 if fails else 0)
