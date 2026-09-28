"""
Analyst to Architect — Chapter 24: Requirements, Storytelling & Stakeholders
build_ch24_files.py — writes the reusable templates and the fully worked example
this chapter walks through (the December 2025 revenue fall).

Run from this folder:  python3 build_ch24_files.py   (needs pandas and pyarrow)

Every number in the worked example is computed here from the full Riverstone data
(../full/*.parquet), with the same chain-linked decomposition as Chapter 23, section 23.11:
nothing is typed by hand. dec_dip() returns the numbers; the chapter's figures
(figures/make_figs24.py) and checks (checks/ch24_check.py) use the same function.
Riverstone Supplies is fictional; every name is invented.
"""
import pathlib

HERE = pathlib.Path(__file__).resolve().parent
FULL = HERE.parent / "full"


def month_totals(lines, month):
    """Customers, orders, net revenue, orders per customer and AOV for one month ('2025-11')."""
    x = lines[lines.month == month]
    t = {"customers": x.customer_id.nunique(), "orders": x.order_id.nunique(), "revenue": x.net_revenue.sum()}
    t["opc"] = t["orders"] / t["customers"]
    t["aov"] = t["revenue"] / t["orders"]
    return t


def bridge(before, after):
    """Chain-linked decomposition of Revenue = Customers x Orders/Customer x AOV (section 23.11)."""
    customer = (after["customers"] - before["customers"]) * before["opc"] * before["aov"]
    frequency = after["customers"] * (after["opc"] - before["opc"]) * before["aov"]
    aov = after["customers"] * after["opc"] * (after["aov"] - before["aov"])
    return {"customer": customer, "frequency": frequency, "aov": aov, "total": after["revenue"] - before["revenue"]}


def dec_dip():
    """All the numbers the December example uses, computed from companion/full."""
    import pandas as pd
    orders = pd.read_parquet(FULL / "orders.parquet")
    items = pd.read_parquet(FULL / "order_items.parquet")
    customers = pd.read_parquet(FULL / "customers.parquet")
    lines = items.merge(orders, on="order_id")
    lines = lines[lines.status != "Cancelled"].copy()
    lines["net_revenue"] = lines.quantity * lines.unit_price * (1 - lines.discount_pct / 100)
    lines["month"] = lines.order_date.dt.to_period("M").astype(str)
    lines = lines.merge(customers[["customer_id", "segment"]], on="customer_id")

    n = {"nov": month_totals(lines, "2025-11"), "dec": month_totals(lines, "2025-12"),
         "may": month_totals(lines, "2025-05"), "jun": month_totals(lines, "2025-06")}
    n["bridge"] = bridge(n["nov"], n["dec"])
    n["pct"] = n["bridge"]["total"] / n["nov"]["revenue"] * 100
    n["pct_may_jun"] = (n["jun"]["revenue"] - n["may"]["revenue"]) / n["may"]["revenue"] * 100
    n["aov_share"] = n["bridge"]["aov"] / n["bridge"]["total"] * 100
    # share of orders by segment, and AOV by segment, in each month
    for key, m in (("nov", "2025-11"), ("dec", "2025-12")):
        x = lines[lines.month == m]
        first = x.drop_duplicates("order_id")
        n[key]["segment_share"] = (first.segment.value_counts(normalize=True) * 100).to_dict()
        g = x.groupby("segment").agg(revenue=("net_revenue", "sum"), orders=("order_id", "nunique"))
        n[key]["segment_aov"] = (g.revenue / g.orders).to_dict()
    # the same November -> December fall in each year of the data
    n["dec_fall_by_year"] = {}
    for y in (2023, 2024, 2025):
        a, b = month_totals(lines, f"{y}-11"), month_totals(lines, f"{y}-12")
        n["dec_fall_by_year"][y] = (b["revenue"] - a["revenue"]) / a["revenue"] * 100
    return n


def cr(v):
    """Rupees to crore with two decimals: 155985901.5 -> '15.60'."""
    return f"{abs(v) / 1e7:.2f}"


def build():
    n = dec_dip()
    b, nov, dec = n["bridge"], n["nov"], n["dec"]
    seg = lambda s: f"{s} {nov['segment_share'][s]:.1f}% → {dec['segment_share'][s]:.1f}%"
    years = n["dec_fall_by_year"]

    (HERE / "clarifying_questions_bank.md").write_text('''# Clarifying questions for a vague ask

Six questions that turn almost any stakeholder request into something answerable.
Questions 1, 2, 3 and 5 are Chapter 5's checks (section 5.2), asked out loud; 4 and 6 are new.
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

**To:** [who needs to act]
**Cc:** [who decides, or needs to know]
**From:** [you]
**Date:** [date]
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

    (HERE / "example_memo_dec_dip.md").write_text(f'''# Analyst to Architect — Chapter 24 worked example

**To:** Vikram Singh, Sales Manager
**Cc:** Anita Rao, Sales Head
**From:** Meera Iyer, Analytics
**Date:** 9 January 2026
**Re:** Why did December revenue fall from November?

## Bottom line
December's ₹{cr(dec["revenue"])} crore is {abs(n["pct"]):.1f}% below November's ₹{cr(nov["revenue"])} crore, but this is the
expected post-festive fall, not a new problem: two-thirds of it came from smaller orders,
one-third from fewer customers and orders, and the segment mix did not shift. No corrective
action is needed.

## What we found
- Revenue fell ₹{cr(b["total"])} crore, from ₹{cr(nov["revenue"])} crore (November) to ₹{cr(dec["revenue"])} crore (December).
- Decomposed into its three drivers: customers contributed −₹{cr(b["customer"])} crore, orders per
  customer −₹{cr(b["frequency"])} crore, and average order value −₹{cr(b["aov"])} crore — AOV drove {n["aov_share"]:.0f}% of the fall.
- Segment mix was essentially unchanged ({seg("Retail")} of orders, {seg("Wholesale")},
  {seg("Hospitality")}), so this is not a shift toward smaller-spending segments.
- The shape mirrors the May-to-June dip earlier in the year (−{abs(n["pct_may_jun"]):.1f}%), which was also led by
  smaller orders with the mix unchanged.
- December fell from November in every year of the data: by {abs(years[2023]):.1f}% in 2023,
  {abs(years[2024]):.1f}% in 2024 and {abs(years[2025]):.1f}% in 2025.

## Why
Riverstone's festive season (October–November) pulls forward large bulk and gifting orders;
December's order book reverts to routine reordering: mostly smaller orders (two-thirds of the
fall), with somewhat fewer customers and orders (one-third). Both of this year's dips (May→June
and Nov→Dec) have the same shape: led by smaller orders, with the segment mix unchanged. That
repeated shape is evidence of seasonality rather than a customer or competitive problem, though
the causes differ (the June trough; the post-festive fall in December).

## What we recommend
No corrective action for December itself. For planning: build the 2026 monthly revenue plan
around this seasonal shape rather than a flat run rate (one month's revenue repeated for every
month), so December is never compared against November as if they should look similar.

## What could change this
If January 2026 also comes in well below its usual range, the seasonal explanation would be
wrong and this should be reopened.

## Appendix
Data: `companion/full/` order lines, non-cancelled, November and December 2025 (and the same
months of 2023 and 2024 for the year-on-year check). Method: chain-linked (sequential)
decomposition of Revenue = Customers × Orders/Customer × AOV (Chapter 23, section 23.11).
Every number above is computed from the order data, not typed.
''', encoding="utf-8")

    (HERE / "three_slide_story.md").write_text(f'''# Three-slide story — the same finding, for a five-minute slot

**Slide 1 — headline**
> December revenue fell {abs(n["pct"]):.0f}%, in line with Riverstone's usual seasonal pattern — no action needed.
- December: ₹{cr(dec["revenue"])} cr · November: ₹{cr(nov["revenue"])} cr · (chart: 12 months of 2025 revenue, December and
  June's dips both circled and labelled "seasonal dip")

**Slide 2 — why**
> Two-thirds of the fall is smaller orders; the segment mix did not move.
- Waterfall: November ₹{cr(nov["revenue"])} cr → customers −₹{cr(b["customer"])} cr → frequency −₹{cr(b["frequency"])} cr → AOV −₹{cr(b["aov"])} cr → December ₹{cr(dec["revenue"])} cr
- One line: "Segment mix barely moved — Retail, Wholesale and Hospitality each kept their
  November share of orders."

**Slide 3 — what we'll do**
> Plan 2026 around this shape; re-check if January doesn't recover to the normal range.
- 2026 monthly plan sketch: a seasonal curve, not a flat line
- One checkpoint: "Review by 10 February once January actuals land."
''', encoding="utf-8")
    print("wrote 4 files")


if __name__ == "__main__":
    build()
