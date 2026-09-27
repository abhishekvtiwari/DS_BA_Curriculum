"""
Analyst to Architect — Chapter 24: Requirements, Storytelling & Stakeholders
build_ch24_files.py — writes the reusable templates and the fully worked example
this chapter walks through (the Dec 2025 revenue-drop request).

Run from this folder:  python3 build_ch24_files.py
Numbers in the worked example come straight from companion/ch23/monthly_revenue_2025.csv
(itself built from the real order data). Riverstone Supplies is fictional.
"""
import pathlib
HERE = pathlib.Path(__file__).resolve().parent

(HERE / "clarifying_questions_bank.md").write_text('''# Clarifying questions for a vague ask

Six questions that turn almost any stakeholder request into something answerable.
Riverstone Supplies is fictional; every name is invented.

1. **What decision will this answer inform?** ("So I know what to cut, or what to defend")
2. **What does the number need to be compared against?** (last month, last year, a target, a competitor)
3. **What's the scope?** (which branches, segments, products, time period — and what's explicitly out)
4. **How will you use the answer?** (a slide, a one-line reply, a deep-dive deck — this decides the format)
5. **When do you need it, and would a rough answer sooner beat an exact one later?**
6. **Has anyone looked at this before?** (avoids redoing analysis, and surfaces the last agreed definition)

## Turning an ask into a question: worked examples

| The ask | The clarifying question | The answered question |
|---|---|---|
| "Can you pull the sales numbers?" | Which sales — orders, revenue, which period, compared to what? | "What was net revenue by region for Q4 2025, versus Q4 2024?" |
| "Why is revenue down?" | Down versus what period? Is this about one month or a trend? | "Why did December 2025 revenue fall from November, and is it a one-off or a pattern?" |
| "I need a report on customers." | A report for whom, to support what decision, refreshed how often? | "A monthly one-page summary for the Sales Head, showing active customers, retention, and churn." |
| "Can you check if the new pricing worked?" | Worked how — more orders, more revenue, or more margin? Compared to what baseline? | "Did average order value rise for orders placed after the 1 March price change, versus the same customers' orders before it?" |
''', encoding="utf-8")

(HERE / "memo_template.md").write_text('''# One-page analysis memo — template

**To:** [who needs to act]  **From:** [you]  **Date:** [date]
**Re:** [the question in one line]

## Bottom line
[The answer, in one or two sentences, with the key number. A reader who stops here should
still know what happened and what you recommend.]

## What we found
- [Finding 1, with its number]
- [Finding 2, with its number]
- [Finding 3, with its number]

## Why
[The explanation — the mechanism, not just the description. One paragraph.]

## What we recommend
[One clear action, or an explicit "no action needed, here's why."]

## What could change this
[The main assumption or risk that would overturn the recommendation.]

## Appendix
[Method, data sources, period covered, exclusions — for anyone who wants to check the work.]
''', encoding="utf-8")

(HERE / "example_memo_dec_dip.md").write_text('''# Analyst to Architect — Chapter 24 worked example

**To:** Anita Rao, Sales Head   **From:** Meera Iyer, Analytics   **Date:** 8 January 2026
**Re:** Why did December revenue fall from November?

## Bottom line
December's ₹8.73 crore is 44.1% below November's ₹15.60 crore, but this is the expected
post-festive normalisation, not a new problem: order values fell broadly across every
segment, with no drop in active customers or orders per customer beyond the usual seasonal
pattern. No corrective action is needed; December's figure is in line with January and
February's typical range.

## What we found
- Revenue fell ₹6.87 crore, from ₹15.60 crore (November) to ₹8.73 crore (December).
- Decomposed into its three drivers: customers contributed −₹1.26 crore, orders per
  customer −₹1.06 crore, and average order value −₹4.55 crore — AOV drove 66% of the fall.
- Segment mix was essentially unchanged (Retail 50.5% → 52.0% of orders, Wholesale 22.0% →
  21.1%, Hospitality 27.5% → 26.8%), so this is not a shift toward smaller-spending segments.
- The same pattern — a large AOV-led fall — repeated the May-to-June dip earlier in the year
  (−40.4%), which is the known seasonal trough after Q1's stocking cycle.

## Why
Riverstone's festive season (October–November) pulls forward large bulk and gifting orders;
December's order book reverts to routine reordering, which is smaller per order but not
fewer in number. This is the same mechanism in both dips this year, which is itself evidence
it's structural seasonality rather than a customer or competitive problem.

## What we recommend
No corrective action for December itself. For planning: build the FY2026 monthly revenue
plan around this seasonal shape rather than a flat run rate, so December is never compared
against November as if they should look similar.

## What could change this
If January 2026 also comes in well below its typical range, the seasonal explanation would
be wrong and this would need re-opening — the two-month test proposed at the end of this memo.

## Appendix
Data: `companion/full/` order lines, non-cancelled, 1 Jan – 31 Dec 2025. Method: chain-linked
(sequential) decomposition of Revenue = Customers × Orders/Customer × AOV (Chapter 23,
section 23.11). Compared months: November 2025 and December 2025.
''', encoding="utf-8")

(HERE / "three_slide_story.md").write_text('''# Three-slide story — the same finding, for a five-minute slot

**Slide 1 — headline**
> December revenue fell 44%, in line with Riverstone's usual seasonal pattern — no action needed.
- December: ₹8.73 cr · November: ₹15.60 cr · (chart: 12 months of 2025 revenue, December and
  June's dips both circled and labelled "seasonal trough")

**Slide 2 — why**
> The fall is broad-based order-value normalisation, not fewer customers or a weaker segment.
- Waterfall: November ₹15.60 cr → customers −₹1.26 cr → frequency −₹1.06 cr → AOV −₹4.55 cr → December ₹8.73 cr
- One line: "Segment mix barely moved — Retail, Wholesale and Hospitality each kept their
  November share of orders."

**Slide 3 — what we'll do**
> Plan FY2026 around this shape; re-check if January doesn't recover to the normal range.
- FY2026 monthly plan sketch: a seasonal curve, not a flat line
- One checkpoint: "Review by 10 February once January actuals land."
''', encoding="utf-8")

print("wrote 4 files")
