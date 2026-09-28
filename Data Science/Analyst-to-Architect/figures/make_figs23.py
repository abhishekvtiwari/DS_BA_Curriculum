# Diagrams for Chapter 23. Run: python3 make_figs23.py
# Every figure prints at the full text width (493.2 pt), so a font of s px on a W px canvas prints at
# s * 493.2 / W pt. Canvases here are 640-700 px wide and the smallest text is 10.5 px, i.e. >= 7.4 pt.
# Numbers are computed from the companion files, never typed.
from make_figs import *
import math, pathlib, re
import pandas as pd

GREEN = "#2f7d6d"; PURPLE = "#7a4fa0"; ORANGE = "#c0662b"; GOLD = "#b7791f"; RED = "#b23b3b"
SOFT = "#eef2f7"
CH23 = pathlib.Path(__file__).resolve().parent.parent / "companion/ch23"
MINUS = "−"


def arrow(x1, y1, x2, y2, c=MUTED, sw=1.5):
    a = math.atan2(y2 - y1, x2 - x1); s = 7
    p1 = (x2 - s * math.cos(a - 0.45), y2 - s * math.sin(a - 0.45))
    p2 = (x2 - s * math.cos(a + 0.45), y2 - s * math.sin(a + 0.45))
    return (path(f"M{x1},{y1} L{x2},{y2}", stroke=c, sw=sw)
            + f'<path d="M{x2},{y2} L{p1[0]:.1f},{p1[1]:.1f} L{p2[0]:.1f},{p2[1]:.1f} Z" fill="{c}"/>')


def card(x, y, w, h, title, c, lines, size=11):
    o = [rect(x, y, w, h, fill="#fff", stroke=c, sw=1.5, rx=6),
         f'<path d="M{x},{y+6} a6,6 0 0 1 6,-6 H{x+w-6} a6,6 0 0 1 6,6 V{y+22} H{x} Z" fill="{c}"/>',
         text(x + w / 2, y + 16, title, 11.5, "#fff", "bold", anchor="middle", family=HEAD)]
    for i, l in enumerate(lines):
        o.append(text(x + w / 2, y + 40 + i * 16, l, size, INK, anchor="middle"))
    return "".join(o)


def statements():
    """Read the P&L and balance-sheet lines from financials_2025.md (built by the companion script)."""
    md = (CH23 / "financials_2025.md").read_text(encoding="utf-8")
    def num(label):
        m = re.search(r"\| \**" + re.escape(label) + r"\**[^|]*\| \**\(?([\d,]+)\)?\**", md)
        return int(m.group(1).replace(",", ""))
    return num, md


def f1():  # the cash cycle as a timeline
    num, md = statements()
    rev, cogs = num("Net revenue"), num("Cost of goods sold")
    dio = round(num("Inventory") / cogs * 365); dso = round(num("Trade receivables") / rev * 365)
    dpo = round(num("Trade payables") / cogs * 365); ccc = dio + dso - dpo
    W, H = 680, 300
    x0, x1 = 40, 640; k = (x1 - x0) / (dio + dso)
    X = lambda d: x0 + d * k
    o = [text(20, 26, "The cash cycle, as a timeline (Riverstone's days, worked out in section 23.3)", 13, INK, "bold", family=HEAD)]
    # events on the line
    o.append(path(f"M{x0},150 H{x1}", stroke=INK, sw=1.5))
    for d, lab1, lab2 in [(0, "Day 0", "stock arrives"), (dpo, f"Day {dpo}", "we pay supplier"),
                          (dio, f"Day {dio}", "stock is sold"), (dio + dso, f"Day {dio+dso}", "customer pays")]:
        o.append(f'<circle cx="{X(d):.1f}" cy="150" r="5" fill="{INK}"/>')
        anchor = "start" if d == 0 else ("end" if d == dio + dso else "middle")
        o.append(text(X(d), 172, lab1, 11, INK, "bold", anchor=anchor))
        o.append(text(X(d), 187, lab2, 10.5, MUTED, anchor=anchor))
    # bars above the line: DIO and DSO (the operating cycle)
    o.append(rect(X(0), 92, X(dio) - X(0), 26, fill="#fbe7da", stroke=ORANGE, sw=1.2, rx=3))
    o.append(text((X(0) + X(dio)) / 2, 109, f"DIO {dio} days: stock waits to be sold", 11, INK, anchor="middle"))
    o.append(rect(X(dio), 92, X(dio + dso) - X(dio), 26, fill="#ece3f4", stroke=PURPLE, sw=1.2, rx=3))
    o.append(text((X(dio) + X(dio + dso)) / 2, 109, f"DSO {dso} days: waiting to be paid", 11, INK, anchor="middle"))
    o.append(path(f"M{X(0)},74 V84 H{X(dio+dso)} V74", stroke=MUTED, sw=1))
    o.append(text((X(0) + X(dio + dso)) / 2, 68, f"Operating cycle = DIO + DSO = {dio+dso} days", 11, INK, "bold", anchor="middle"))
    # bars below the line: DPO, then the cash gap
    o.append(rect(X(0), 204, X(dpo) - X(0), 26, fill="#fbf0d9", stroke=GOLD, sw=1.2, rx=3))
    o.append(text((X(0) + X(dpo)) / 2, 221, f"DPO {dpo} days: supplier's credit", 11, INK, anchor="middle"))
    o.append(rect(X(dpo), 204, X(dio + dso) - X(dpo), 26, fill="#f6dede", stroke=RED, sw=1.2, rx=3,
                  extra='stroke-dasharray="5 3"'))
    o.append(text((X(dpo) + X(dio + dso)) / 2, 221, f"Cash conversion cycle {ccc} days: our own cash is tied up",
                  11, INK, "bold", anchor="middle"))
    o.append(text(20, 262, f"Cash conversion cycle = DIO + DSO {MINUS} DPO = {dio} + {dso} {MINUS} {dpo} = {ccc} days.", 11.5, INK, "bold"))
    o.append(text(20, 282, "The company can be profitable all the while: the gap is about timing, not about profit.", 11, MUTED))
    return svg(W, H, "".join(o))


def f2():  # P&L waterfall, horizontal bars
    num, md = statements()
    rev = num("Net revenue"); cogs = num("Cost of goods sold"); gp = rev - cogs
    sd, mk, ad, dep = num("Selling & distribution"), num("Marketing"), num("Administration"), num("Depreciation & amortisation")
    ebit = gp - sd - mk - ad - dep; interest = num("Interest expense"); tax = num("Tax (25%)"); pat = ebit - interest - tax
    steps = [("Revenue", rev, True), ("Cost of goods sold", -cogs, False), ("Gross profit", gp, True),
             ("Selling & distribution", -sd, False), ("Marketing", -mk, False), ("Administration", -ad, False),
             ("Depreciation", -dep, False), ("EBIT (operating profit)", ebit, True), ("Interest", -interest, False),
             ("Tax", -tax, False), ("Net profit (PAT)", pat, True)]
    W = 680; row = 25; top = 50
    H = top + len(steps) * row + 58
    lx = 172; x0 = 180; x1 = 560; k = (x1 - x0) / rev
    o = [text(20, 26, "Riverstone's 2025 P&L, top to bottom (₹ crore)", 13, INK, "bold", family=HEAD)]
    run = 0
    for i, (lab, v, total) in enumerate(steps):
        y = top + i * row
        if total:
            a, b = 0, v; run = v; col, fill = ACC, ACC
        else:
            a, b = run + v, run; run = run + v; col, fill = RED, "#f3d4d4"
        o.append(rect(x0 + a * k, y + 3, max((b - a) * k, 1.5), row - 7, fill=fill, stroke=col, sw=1, rx=2))
        o.append(text(lx, y + 17, lab, 11, INK, "bold" if total else "normal", anchor="end"))
        val = f"{v/1e7:,.1f}" if total else f"{MINUS}{abs(v)/1e7:,.1f}"
        o.append(text(x0 + b * k + 6, y + 17, val, 11, INK if total else RED, "bold" if total else "normal"))
    o.append(path(f"M{x0},{top} V{top + len(steps)*row}", stroke=RULE, sw=1))
    yb = top + len(steps) * row
    o.append(rect(20, yb + 12, 12, 10, fill=ACC)); o.append(text(38, yb + 21, "total or subtotal", 10.5, MUTED))
    o.append(rect(160, yb + 12, 12, 10, fill="#f3d4d4", stroke=RED)); o.append(text(178, yb + 21, f"cost ({MINUS}, taken away)", 10.5, MUTED))
    o.append(text(20, yb + 42, "Revenue and cost of goods sold come from the order data; every line below gross profit is invented for this chapter.", 10.5, MUTED))
    return svg(W, H, "".join(o))


def f3():  # a gross-profit tree whose boxes multiply or add up exactly
    num, md = statements()
    m = re.search
    get = lambda lab: int(m(r"\| " + re.escape(lab) + r" \| ([\d,]+) \|", md).group(1).replace(",", ""))
    a24, a25, ret, churn, new = (get("Active customers, 2024"), get("Active customers, 2025"),
                                get("Retained (active both years)"), get("Churned (active 2024, not 2025)"), get("New in 2025"))
    I = pd.read_parquet(CH23.parent / "full/order_items.parquet"); O = pd.read_parquet(CH23.parent / "full/orders.parquet")
    L = I.merge(O, on="order_id")
    L = L[(L.status != "Cancelled") & (L.order_date >= "2025-01-01") & (L.order_date < "2026-01-01")]
    revenue = (L.quantity * L.unit_price * (1 - L.discount_pct / 100)).sum()
    orders = L.order_id.nunique(); units = L.quantity.sum()
    rev = num("Net revenue"); gp = rev - num("Cost of goods sold")
    W, H = 700, 360
    o = [text(20, 24, "Riverstone's 2025 profit tree: every level multiplies (×) or adds (+) to the one above", 12.5, INK, "bold", family=HEAD)]
    o.append(card(250, 38, 200, 58, "Gross profit", ACC, [f"₹{gp/1e7:.1f} cr = revenue × margin"], 11))
    o.append(card(110, 124, 220, 58, "Revenue", ACC, [f"₹{rev/1e7:.1f} cr = C × F × A"], 11))
    o.append(card(420, 124, 170, 58, "Gross margin", PURPLE, [f"{gp/rev*100:.1f}%"], 11))
    o.append(arrow(330, 96, 220, 122)); o.append(arrow(370, 96, 505, 122))
    o.append(text(372, 116, "×", 13, INK, "bold", anchor="middle"))
    boxes = [(10, "Active customers (C)", GREEN, [f"{a25:,}", f"= retained + new"]),
             (240, "Orders per customer (F)", ORANGE, [f"{orders/a25:.2f} a year"]),
             (470, "Average order value (A)", GOLD, [f"₹{revenue/orders:,.2f}", "= units × price"])]
    for x, t, c, lines in boxes:
        o.append(card(x, 214, 220, 58 if len(lines) == 1 else 72, t, c, lines, 11))
        o.append(arrow(220, 182, x + 110, 212))
    o.append(text(118, 208, "×", 13, INK, "bold")); o.append(text(318, 208, "×", 13, INK, "bold"))
    leaves = [(10, f"Retained {ret:,}", f"= active 2024 ({a24:,}) {MINUS} churned ({churn:,})", GREEN, 120),
              (10, f"New {new:,}", "first order in 2025", GREEN, 120),
              (470, f"Units per order {units/orders:.2f}", "basket size", GOLD, 580),
              (470, f"Net price per unit ₹{revenue/units:,.2f}", "list price less discount", GOLD, 580)]
    for j, (x, t1, t2, c, ax) in enumerate(leaves):
        y = 294 + (j % 2) * 34
        o.append(rect(x, y, 220, 30, fill="#fff", stroke=c, sw=1.2, rx=4))
        o.append(text(x + 8, y + 13, t1, 11, INK, "bold"))
        o.append(text(x + 8, y + 26, t2, 10.5, MUTED))
    o.append(path("M120,286 V292", stroke=MUTED, sw=1.2)); o.append(path("M580,286 V292", stroke=MUTED, sw=1.2))
    o.append(text(240, 310, "C × F × A gives revenue exactly:", 10.5, MUTED))
    o.append(text(240, 325, "orders ÷ customers and revenue ÷ orders", 10.5, MUTED))
    o.append(text(240, 340, "cancel out, leaving revenue.", 10.5, MUTED))
    return svg(W, H, "".join(o))


def f4():  # May -> June bridge, computed from the monthly file
    m = pd.read_csv(CH23 / "monthly_revenue_2025.csv", index_col="month")
    may, jun = m.loc["2025-05"], m.loc["2025-06"]
    f = lambda r: (r.customers, r.orders / r.customers, r.net_revenue / r.orders)
    c0, f0, a0 = f(may); c1, f1_, a1 = f(jun)
    effects = [(c1 - c0) * f0 * a0, c1 * (f1_ - f0) * a0, c1 * f1_ * (a1 - a0)]
    steps = [("May 2025", may.net_revenue, True), ("Fewer\ncustomers", effects[0], False),
             ("Fewer orders\nper customer", effects[1], False), ("Lower average\norder value", effects[2], False),
             ("June 2025", jun.net_revenue, True)]
    W, H = 640, 290
    o = [text(20, 26, "Diagnosing the May → June 2025 dip: a chain-linked bridge", 13, INK, "bold", family=HEAD)]
    base = 232; k = 170 / 9e7; x = 30; bw = 104; gap = 18; run = 0
    for lab, v, total in steps:
        if total:
            top, h = base - v * k, v * k; run = v; fill, col = ACC, ACC
            val = f"₹{v/1e7:.2f} cr"
        else:
            top = base - run * k; h = -v * k; run += v; fill, col = "#f3d4d4", RED
            val = f"{MINUS}₹{abs(v)/1e7:.2f} cr"
        o.append(rect(x, top, bw, h, fill=fill, stroke=col, sw=1, rx=2))
        o.append(text(x + bw / 2, top - 6, val, 11, INK if total else RED, "bold", anchor="middle"))
        for j, l in enumerate(lab.split("\n")):
            o.append(text(x + bw / 2, base + 17 + j * 14, l, 11, MUTED, anchor="middle"))
        x += bw + gap
    o.append(path(f"M20,{base} H{W-20}", stroke=RULE, sw=1))
    return svg(W, H, "".join(o))


if __name__ == "__main__":
    for n, fn in [("fig23-1-operating-cycle.svg", f1), ("fig23-2-pnl-waterfall.svg", f2),
                  ("fig23-3-kpi-tree.svg", f3), ("fig23-4-root-cause.svg", f4)]:
        open(n, "w", encoding="utf-8").write(fn())
    print("ok")
