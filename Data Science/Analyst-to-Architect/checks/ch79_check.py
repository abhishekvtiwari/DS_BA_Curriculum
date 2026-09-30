#!/usr/bin/env python3
"""ch79_check.py - checks Chapter 79 (GenAI, LLM & MLOps Question Bank) against the chapters it cites.

Usage: python3 checks/ch79_check.py        (run from the book folder)

1. Every section number Ch 79 cites ("section 55.3", "| Mid · 54.4, 55.1", "sections 56.7-56.9")
   exists as a "## NN.M" heading in the current manuscript.
2. Every fact Ch 79 quotes from another chapter appears inside the section (or file) it is credited to.
3. Every question ID Ch 79 cites from another bank exists there, on the topic Ch 79 says.
4. The arithmetic Ch 79 does in prose (cosine by hand, cost by hand, shares) is recomputed.
5. Only Chapter 69's twelve tags are used.
Exit code 1 on any failure.
"""
import glob, math, re, sys

MS = "manuscript"
ch79 = open(glob.glob(f"{MS}/ch79-*.md")[0], encoding="utf-8").read()
fails = 0


def chapter(n):
    return open(glob.glob(f"{MS}/ch{n}-*.md")[0], encoding="utf-8").read()


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
cited = set(re.findall(r"(?:section|sections|·|;|,|and) (\d{2}\.\d{1,2})\b", ch79))
cited |= set(re.findall(r"–(\d{2}\.\d{1,2})\b", ch79))
cited = {c for c in cited if not c.startswith("79.") and c.split(".")[0] in
         {"21", "35", "36", "41", "54", "55", "56", "57", "58", "71"}}
for c in sorted(cited, key=lambda s: tuple(map(int, s.split(".")))):
    n, s = c.split(".")
    ok(section(n, s) is not None, f"cited section {c} has no heading")
print(f"sections cited and found: {len(cited)}")

# 2. quoted facts, each inside the section credited
facts = [
    (35, 2, "cosine similarity"),
    (41, 7, "bridge to LLMs"),
    (54, 2, "sub-word tokens"),
    (54, 2, "counting letters"),
    (54, 4, "middle of a very long context"),
    (54, 5, "Claude Sonnet 5.5, reject any non-default"),
    (54, 8, "scales each vector to length 1"),
    (54, 11, "Prompt injection"),
    (54, 11, "Non-determinism"),
    (54, 12, "| Workhorse | $2 / $10–12 |"),
    (54, 12, "checked 29 September 2026"),
    (55, 3, "def chunk_sentences"),
    (55, 3, "def chunk_sections"),
    (55, 5, "cross-encoder"),
    (55, 6, "the normalized top score is always 1.0"),
    (55, 8, "Every agent needs a **step limit**"),
    (55, 9, "LLM-as-judge"),
    (55, 9, "score 50 answers by hand once"),
    (55, 10, "### Injection through your own documents"),
    (55, 10, "### The superseded document"),
    (55, 11, "About 13 to 14 paise a question"),
    (56, 2, "A **model registry**"),
    (56, 7, "Monitoring, in three layers"),
    (56, 8, "PSI reaches 4.4"),
    (56, 8, "(96.8%)"),
    (56, 8, "(96.5%)"),
    (56, 8, "(84.4%)"),
    (56, 8, "Recall falls by about 12 points"),
    (56, 8, "PSI 0.006"),
    (56, 8, "PSI 0.013"),
    (56, 8, "<0.1 stable, 0.1-0.25 watch, >0.25 investigate"),
    (56, 8, "input drift is not model decay"),
    (56, 9, "retrain monthly, and immediately on any event the plant tells us about"),
    (56, 9, "the right default"),
    (56, 11, "training-serving skew"),
    (56, 11, "twenty models share features"),
    (57, 5, "(2.00, 10.00)"),
    (57, 5, '"volume-001": (0.75, 3.75)'),
    (57, 5, "USD_TO_INR = 88.0"),
    (57, 5, "cost per email: ₹0.079"),
    (57, 5, "₹ 87.93"),
    (57, 6, "corpus version"),
    (57, 8, "**A circuit breaker.**"),
    (57, 10, "A **trace**"),
    (57, 11, "The human loop"),
    (58, 5, "The human in the loop"),
    (58, 6, "circuit breaker"),
    (71, 9, "Query optimization and indexes"),
]
for n, s, text in facts:
    body = section(n, s)
    ok(body is not None and text in body, f"'{text}' not found in section {n}.{s}")
print(f"quoted facts checked: {len(facts)}")

# facts credited to a chapter or file rather than a section
ok("recall@1 *worse*, 0.87 to 0.82" in chapter(55), "Ch 55 exercise 11: 0.87 to 0.82")
ok("pgvector" in chapter(55) and "approximate-nearest-neighbour (ANN) index" in chapter(55),
   "Ch 55 project tools: pgvector, ANN index")
ok("17% on a normal day" in chapter(57), "Ch 57: cache 17% on a normal day")
ok("**AI engineer**" in open(f"{MS}/part1-the-map.md", encoding="utf-8").read(), "AI engineer role (Ch 7)")
returns = open("companion/ch55/corpus/docs/policy_returns.md", encoding="utf-8").read()
ok("Goods ordered in error may be returned within 15 days if unused and in original packaging." in returns
   and "A restocking fee of 10% applies, and freight both ways is charged to the customer." in returns,
   "Q79-012's text is not Ch 55's policy_returns.md")

# 3. other banks' question IDs, and their topic
qids = {
    "Q73-031": (73, "Simpson"), "Q74-030": (74, "offline evaluation"), "Q75-014": (75, "leading and a lagging"),
    "Q77-002": (77, "Batch vs. streaming"), "Q77-030": (77, "lineage"),
    "Q78-017": (78, "retry"), "Q78-021": (78, "circuit breaker"),
}
for q, (n, topic) in qids.items():
    text = chapter(n)
    line = next((l for l in text.splitlines() if (l.startswith(f"### {q} ") or l.startswith(f"| {q} "))), "")
    ok(topic.lower() in line.lower(), f"{q} not found in Ch {n} with topic '{topic}'")
print(f"question IDs checked: {len(qids)}")

# 4. arithmetic in the prose
q, a = (0.9, 0.1, 0.0), (0.85, 0.15, 0.05)
dot = sum(x * y for x, y in zip(q, a))
lq, la = math.sqrt(sum(x * x for x in q)), math.sqrt(sum(x * x for x in a))
ok(round(dot, 2) == 0.78 and f"{lq:.4f}" == "0.9055" and f"{la:.4f}" == "0.8646"
   and f"{lq * la:.4f}" == "0.7829" and f"{dot / (lq * la):.3f}" == "0.996", "cosine by hand")
cost = 500 / 1e6 * 2 + 150 / 1e6 * 10
ok(abs(cost - 0.0025) < 1e-12 and abs(150 / 1e6 * 10 / cost - 0.60) < 1e-9, "workhorse cost and 60% output share")
ok(150 / 650 < 0.25, "output under a quarter of the tokens")
vol = 500 / 1e6 * 0.75 + 150 / 1e6 * 3.75
ok(1 - vol / cost > 0.60, "volume tier saves more than 60%")
ok(len("Goods ordered in error may be returned within 15 days if unused and in original packaging. "
       "A restocking fee of 10% applies, and freight both ways is charged to the customer.") == 173, "173 characters")
ok(173 - 3 * 45 == 38, "last chunk 38 characters")

# 5. only the twelve tags
TAGS = {"Clarify", "Assume", "Signpost", "Simple first", "Edge cases", "Trade-offs", "Validate",
        "Business", "Scale", "Limits", "Evidence", "Close"}
used = set(re.findall(r"\*\*\[\+([^\]]+)\]\*\*", ch79))
ok(used <= TAGS, f"unknown tags {used - TAGS}")
ok(not re.search(r"\[(Depth|Structure|Real evidence|Practical|Learn it in|Business|Validate)\]", ch79),
   "old-style tag left")
print(f"tags used: {len(used)} of 12")

print("OK" if not fails else f"{fails} failure(s)")
sys.exit(1 if fails else 0)
