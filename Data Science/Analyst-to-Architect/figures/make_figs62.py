# Diagrams for Chapter 62. Run: python3 make_figs62.py
# Every figure prints at the full text width (493.2 pt). All canvases are 680 px wide, so
# 1 px = 0.725 pt: the smallest text here, 10.5 px, prints at 7.6 pt (visual standard: 7 pt or more).
# Text is wrapped by measuring it with the DejaVu Sans metrics the PDF uses, so no label can
# run past its box, and every box is sized to the text it holds.
import math, os
from PIL import ImageFont
from make_figs import *

GREEN = "#2f7d6d"; PURPLE = "#7a4fa0"; ORANGE = "#b35a1f"; GOLD = "#9a6512"; RED = "#b23b3b"
GREY = "#6b7383"; SOFT = "#eef2f7"
W = 680
BODY = 10.5          # body text, px (7.6 pt printed)
LEAD = 13.6          # line spacing for body text

_FONT_DIR = "/usr/share/fonts/truetype/dejavu/"
_fonts = {}
def width(s, size, bold=False):
    """Width in px of s at this font size, measured with the font the PDF uses."""
    if bold not in _fonts:
        _fonts[bold] = ImageFont.truetype(_FONT_DIR + ("DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf"), 100)
    return _fonts[bold].getlength(s) * size / 100

def wrap(s, size, max_w, bold=False):
    """Split s into lines that each fit in max_w px at this font size."""
    lines, line = [], ""
    for word in s.split():
        trial = (line + " " + word).strip()
        if width(trial, size, bold) <= max_w or not line:
            line = trial
        else:
            lines.append(line); line = word
    if line: lines.append(line)
    for l in lines:
        assert width(l, size, bold) <= max_w + 0.5, f"too wide: {l!r}"
    return lines

def lines_at(x, y, lines, size, fill=INK, weight="normal", anchor="start", lead=None):
    lead = lead or size * 1.3
    return "".join(text(x, y + i * lead, l, size, fill, weight, anchor=anchor) for i, l in enumerate(lines))

def arrow(x1, y1, x2, y2, c=MUTED, sw=1.5, dash=None):
    a = math.atan2(y2 - y1, x2 - x1); s = 7
    p1 = (x2 - s * math.cos(a - 0.45), y2 - s * math.sin(a - 0.45))
    p2 = (x2 - s * math.cos(a + 0.45), y2 - s * math.sin(a + 0.45))
    return (path(f"M{x1},{y1} L{x2},{y2}", stroke=c, sw=sw, dash=dash)
            + f'<path d="M{x2},{y2} L{p1[0]:.1f},{p1[1]:.1f} L{p2[0]:.1f},{p2[1]:.1f} Z" fill="{c}"/>')

def box_height(w, title, paras):
    tlines = wrap(title, BODY, w - 14, bold=True)
    body = [wrap(p, BODY, w - 16) for p in paras]
    band = 8 + len(tlines) * LEAD
    return band + 8 + sum(len(b) for b in body) * LEAD + (len(body) - 1) * 4 + 6

def box(x, y, w, title, paras, c, dash=None, h=None):
    """A box with a coloured title band and wrapped body paragraphs. Returns (svg, height).
    h: force a taller box (to line up with its neighbours)."""
    tlines = wrap(title, BODY, w - 14, bold=True)
    body = [wrap(p, BODY, w - 16) for p in paras]
    band = 8 + len(tlines) * LEAD
    h = h or box_height(w, title, paras)
    o = [rect(x, y, w, h, fill="#fff", stroke=c, sw=1.4, rx=6, extra=f'stroke-dasharray="{dash}"' if dash else "")]
    o.append(f'<path d="M{x},{y+6} a6,6 0 0 1 6,-6 H{x+w-6} a6,6 0 0 1 6,6 V{y+band} H{x} Z" fill="{c}"/>')
    o.append(lines_at(x + 8, y + 4 + BODY, tlines, BODY, "#fff", "bold", lead=LEAD))
    yy = y + band + 8 + BODY - 1
    for b in body:
        o.append(lines_at(x + 8, yy, b, BODY, INK, lead=LEAD))
        yy += len(b) * LEAD + 4
    return "".join(o), h

def note(x, y, s, w, fill=MUTED, weight="normal"):
    """A wrapped line of explanatory text. Returns (svg, height)."""
    ls = wrap(s, BODY, w, bold=(weight == "bold"))
    return lines_at(x, y + BODY, ls, BODY, fill, weight, lead=LEAD), len(ls) * LEAD


# ---------- Figure 62.1: Lambda (as Chapter 50 built it) and Kappa, on the same sensor need ----------
def f1():
    o = [text(12, 22, "One need, two shapes: the plant-sensor case from Chapter 50", 13, INK, "bold", family=HEAD)]
    PW = 322; LX = 12; RX = W - 12 - PW; top = 36
    o.append(text(LX, top + 12, "LAMBDA: what Chapter 50 built", 11.5, ACC, "bold"))
    o.append(text(RX, top + 12, "KAPPA: the same need, one path", 11.5, GREEN, "bold"))
    y0 = top + 22
    # ---- Lambda
    src_l = ["Machine controllers send a reading every 10 seconds to the sensor-readings topic."]
    src_r = ["The same readings, on a topic kept for months, so any stretch of history can be replayed."]
    hsrc = max(box_height(PW, "Sources", src_l), box_height(PW, "Sources", src_r))
    s, h = box(LX, y0, PW, "Sources", src_l, GREY, h=hsrc)
    o.append(s); yl = y0 + h + 22
    cw = (PW - 10) / 2
    sp = ["Alert consumer: 2-minute average per machine; raises the line alert.",
          "Streaming job: 5-minute windows into a streaming table."]
    bt = ["Correction job: re-reads the day from the archive.",
          "Rewrites yesterday's windows into a corrected table."]
    hh = max(box_height(cw, "Speed layer (live)", sp), box_height(cw, "Batch layer (daily)", bt))
    s1, _ = box(LX, yl, cw, "Speed layer (live)", sp, ORANGE, h=hh)
    s2, _ = box(LX + cw + 10, yl, cw, "Batch layer (daily)", bt, ACC, h=hh)
    o += [s1, s2]
    o.append(arrow(LX + cw / 2, yl - 20, LX + cw / 2, yl - 2))
    o.append(arrow(LX + cw + 10 + cw / 2, yl - 20, LX + cw + 10 + cw / 2, yl - 2))
    ys = yl + hh + 22
    s, h3 = box(LX, ys, PW, "Serving layer: the dashboard query",
                ["Reads the corrected table for past days and the streaming table for today."], PURPLE)
    o.append(s)
    o.append(arrow(LX + cw / 2, yl + hh + 2, LX + cw / 2, ys - 2))
    o.append(arrow(LX + cw + 10 + cw / 2, yl + hh + 2, LX + cw + 10 + cw / 2, ys - 2))
    yend_l = ys + h3
    # ---- Kappa
    s, h = box(RX, y0, PW, "Sources", src_r, GREY, h=hsrc)
    o.append(s); yk = y0 + h + 22
    s, hk = box(RX, yk, PW, "One streaming job",
                ["Raises the line alert, and writes 5-minute windows into one table."], GREEN)
    o.append(s); o.append(arrow(RX + PW / 2, yk - 20, RX + PW / 2, yk - 2))
    ysk = yk + hk + 22
    s, h4 = box(RX, ysk, PW, "Serving: the dashboard query", ["Reads the one table."], PURPLE)
    o.append(s); o.append(arrow(RX + PW / 2, yk + hk + 2, RX + PW / 2, ysk - 2))
    yr = ysk + h4 + 22
    s, hr = box(RX, yr, PW - 14, "To correct history: replay",
                ["Only when needed: reset the job's offsets to the start of the topic and run the same code again, with a longer watermark, since nobody is waiting on it."],
                GREEN, dash="5,3")
    o.append(s)
    # dashed return line: from the replay box, up the right margin, back into the topic
    xr = W - 8; ytop = y0 + hsrc / 2
    o.append(path(f"M{RX + PW - 14},{yr + hr / 2} H{xr} V{ytop}", stroke=GREEN, sw=1.5, dash="4,3"))
    o.append(arrow(xr, ytop, RX + PW + 2, ytop, GREEN, dash="4,3"))
    ysk, h4 = yr, hr
    yend_r = ysk + h4
    yc = max(yend_l, yend_r) + 12
    s, hc1 = note(LX, yc, "Cost: the window logic lives in two jobs that must keep agreeing.", PW, INK, "bold")
    s2, hc2 = note(RX, yc, "Cost: months of retention, and a replay you must trust.", PW, INK, "bold")
    o += [s, s2]
    return svg(W, int(yc + max(hc1, hc2) + 10), "".join(o))


# ---------- Figure 62.2: medallion tiers, mapped to what the book already built ----------
def f2():
    o = [text(12, 22, "Medallion: bronze, silver, gold, and what sits on top", 13, INK, "bold", family=HEAD)]
    LW = 128; DX = 12 + LW + 10; DW = 262; BX = DX + DW + 10; BW = W - 12 - BX
    o.append(text(DX, 46, "What it holds", BODY, MUTED, "bold"))
    o.append(text(BX, 46, "Where this book built it", BODY, MUTED, "bold"))
    rows = [("ON TOP", "Semantic layer", "One definition per metric (revenue, active customer), reading gold tables. Not a fourth tier.",
             "Chapter 32, section 32.13 (the net_revenue macro); Chapter 16's semantic model", ACC, True),
            ("GOLD", "Modeled (marts)", "Business-ready tables built around the questions people ask: revenue by month, on-time delivery.",
             "Chapter 45's modeled layer; Chapter 32's marts, built with dbt", GOLD, False),
            ("SILVER", "Staging", "Cleaned, typed, deduplicated, and conformed to one shape, but not yet built around business questions.",
             "Chapter 45's staging schema, kept clean by Chapter 47's checks", GREY, False),
            ("BRONZE", "Raw", "Exactly as the source sent it, kept for audit and replay.",
             "Chapter 45's raw schema", ORANGE, False)]
    y = 54
    for i, (tier, name, desc, built, c, dashed) in enumerate(rows):
        d = wrap(desc, BODY, DW - 16); b = wrap(built, BODY, BW - 16)
        h = max(len(d), len(b), 2) * LEAD + 14
        extra = 'stroke-dasharray="5,3"' if dashed else ""
        fill, ink = ("#fff", c) if dashed else (c, "#fff")
        o.append(rect(12, y, LW, h, fill=fill, stroke=c, sw=1.6, rx=6, extra=extra))
        o.append(text(12 + LW / 2, y + h / 2 - 2, tier, BODY, ink, "bold", anchor="middle"))
        o.append(text(12 + LW / 2, y + h / 2 + LEAD - 2, name, BODY, ink, "bold", anchor="middle"))
        o.append(rect(DX, y, DW, h, fill="#fff", stroke=c, sw=1.2, rx=6, extra=extra))
        o.append(lines_at(DX + 8, y + 7 + BODY, d, BODY, INK, lead=LEAD))
        o.append(rect(BX, y, BW, h, fill=SOFT, rx=6))
        o.append(lines_at(BX + 8, y + 7 + BODY, b, BODY, INK, lead=LEAD))
        y += h
        if i < len(rows) - 1:
            label = "reads" if i == 0 else "built from"
            o.append(arrow(12 + LW / 2, y + 20, 12 + LW / 2, y + 3))
            o.append(text(12 + LW / 2 + 8, y + 15, label, BODY, MUTED))
            y += 22
    s, h = note(12, y + 8, "Data flows upwards: raw, then staging, then marts. The semantic layer is where 'revenue' is defined once, on top of gold.", W - 24)
    o.append(s)
    return svg(W, int(y + 8 + h + 8), "".join(o))


# ---------- Figure 62.3: centralized, data mesh, data fabric ----------
def f3():
    o = [text(12, 22, "Who owns the data: three organizational patterns", 13, INK, "bold", family=HEAD)]
    gap = 10; cw = (W - 24 - 2 * gap) / 3; y = 36
    cards = [("Centralized", ACC,
              ["Who owns it: one team owns ingestion, models, quality, and delivery for everyone.",
               "Gains: simple to govern; one set of standards, one place to look.",
               "Costs: every request waits in one queue as the company grows."]),
             ("Data mesh", GREEN,
              ["Who owns it: each domain team owns its data as a product, on a shared self-serve platform, under federated governance.",
               "Gains: removes the central queue.",
               "Costs: needs builders in every domain and a mature platform."]),
             ("Data fabric", PURPLE,
              ["Who owns it: no change. Tools find and query data where it already lives: a data catalog, plus a query engine that reads several sources.",
               "Gains: easier discovery, without moving data.",
               "Costs: technology, not organization; it pairs with either of the other two."])]
    hmax = max(box_height(cw, t, ps) for t, _, ps in cards)
    for i, (t, c, ps) in enumerate(cards):
        s, _ = box(12 + i * (cw + gap), y, cw, t, ps, c, h=hmax)
        o.append(s)
    s, hn = note(12, y + hmax + 10, "Riverstone today: centralized. Meera's four-person data platform team (Chapter 60) serves the whole company, which fits its size. Section 62.6 checks whether that should change.", W - 24)
    o.append(s)
    return svg(W, int(y + hmax + 10 + hn + 8), "".join(o))


# ---------- Figure 62.4: data contracts and the semantic layer as the glue ----------
def f4():
    o = [text(12, 22, "Two domains, one name: without and with an agreed definition", 13, INK, "bold", family=HEAD)]
    PW = 322; LX = 12; RX = W - 12 - PW; y0 = 36
    o.append(text(LX, y0 + 12, "WITHOUT A CONTRACT", 11.5, RED, "bold"))
    o.append(text(RX, y0 + 12, "WITH A CONTRACT", 11.5, GREEN, "bold"))
    y = y0 + 22; cw = (PW - 10) / 2
    pa = ["active_customer = a non-cancelled order in the trailing 12 months"]
    pb = ["active_customer = has a non-zero balance"]
    hh = max(box_height(cw, "Sales publishes", pa), box_height(cw, "Finance publishes", pb))
    a, _ = box(LX, y, cw, "Sales publishes", pa, RED, h=hh)
    b, _ = box(LX + cw + 10, y, cw, "Finance publishes", pb, RED, h=hh)
    o += [a, b]
    yr = y + hh + 22
    o.append(arrow(LX + cw / 2, y + hh + 2, LX + PW / 2 - 24, yr - 2, RED))
    o.append(arrow(LX + cw + 10 + cw / 2, y + hh + 2, LX + PW / 2 + 24, yr - 2, RED))
    c, hc = box(LX, yr, PW, "Result: two counts, one name",
                ["Each table is right by its own rule. Nobody notices until one report uses both and the numbers don't match."], RED)
    o.append(c); endl = yr + hc
    d, hd = box(RX, y, PW, "Semantic layer (owned by the data platform team)",
                ["active_customer = a non-cancelled order in the trailing 12 months. Written once, tested, read by everyone."], ACC)
    o.append(d)
    yr2 = y + hd + 22
    pe = ["uses active_customer as defined"]; pf = ["publishes customer_with_balance"]
    h2 = max(box_height(cw, "Sales reads it", pe), box_height(cw, "Finance names its own", pf))
    e, _ = box(RX, yr2, cw, "Sales reads it", pe, GREEN, h=h2)
    f, _ = box(RX + cw + 10, yr2, cw, "Finance names its own", pf, GREEN, h=h2)
    o += [e, f]
    o.append(arrow(RX + cw / 2, y + hd + 2, RX + cw / 2, yr2 - 2, GREEN))
    endr = yr2 + h2
    yb = max(endl, endr) + 10
    s, hn = note(12, yb, "A data contract (Chapter 47) states in writing what a dataset promises; the semantic layer (Chapter 32) is where the shared definitions live. A second meaning gets a second name.", W - 24)
    o.append(s)
    return svg(W, int(yb + hn + 8), "".join(o))


# ---------- Figure 62.5: the data mesh maturity scorecard, scored ----------
ROWS62_5 = [("Domain teams able to own data", 1,
             "One data platform team; sales, operations, and the plant have no builders of their own."),
            ("A self-serve platform", 2,
             "Dagster and the warehouse exist, but no domain has used them without the platform team."),
            ("Federated governance", 2,
             "A data contract (Chapter 47) exists for one feed, the Bhiwandi dispatch file, not as a company standard."),
            ("A data-product mindset", 3,
             "Chapter 60's containers each have an owner and non-functional requirements: a real start."),
            ("Appetite for the change", 1,
             "No domain outside the platform team has asked to own its data.")]

def f5():
    o = [text(12, 22, "Is Riverstone ready for a data mesh? Five questions, scored 1 to 5", 13, INK, "bold", family=HEAD)]
    o.append(text(12, 42, "Scale: 1 = absent · 3 = partly in place · 5 = working company-wide", BODY, MUTED))
    LBW = 250; TX = 12 + LBW + 12; TW = 280; SX = TX + TW + 14
    y = 54
    for k in range(1, 6):
        o.append(text(TX + TW * (k - 0.5) / 5, y + 10, str(k), BODY, MUTED, "bold", anchor="middle"))
    y += 18
    for label, score, ev in ROWS62_5:
        o.append(rect(12, y, W - 24, 1, fill=RULE))
        y += 8
        lab = wrap(label, 11, LBW, bold=True)
        o.append(lines_at(12, y + 14, lab, 11, INK, "bold", lead=LEAD))
        for k in range(5):
            filled = k < score
            o.append(rect(TX + TW * k / 5 + 2, y + 3, TW / 5 - 4, 16, fill=ACC if filled else "#fff",
                          stroke=ACC if filled else RULE, sw=1, rx=3))
        o.append(text(SX, y + 16, f"{score} / 5", 11, INK, "bold"))
        if score == 1:
            o.append(text(SX + 42, y + 16, "blocker", BODY, RED, "bold"))
        ev_l = wrap(ev, BODY, W - 24 - 8)
        yy = y + max(len(lab) * LEAD, 22) + 2
        o.append(lines_at(20, yy + BODY, ev_l, BODY, MUTED, lead=LEAD))
        y = yy + len(ev_l) * LEAD + 6
    o.append(rect(12, y, W - 24, 1.5, fill=INK))
    y += 6
    total = sum(r[1] for r in ROWS62_5)
    o.append(text(12, y + 14, "Total", 11, INK, "bold"))
    o.append(text(SX, y + 14, f"{total} / 25", 11, INK, "bold"))
    y += 26
    verdict = wrap("Rule: any question at 1, or a total under 15, means not ready. Riverstone has two at 1 and a total of "
                   f"{total}: not ready, and that's fine. Revisit when a business domain with its own builder asks to own its data.",
                   BODY, W - 24 - 26)
    hv = len(verdict) * LEAD + 14
    o.append(rect(12, y, W - 24, hv, fill="#fff", stroke=RED, sw=1.4, rx=5)); o.append(rect(12, y, 6, hv, fill=RED))
    o.append(lines_at(28, y + 7 + BODY, verdict, BODY, INK, lead=LEAD))
    return svg(W, int(y + hv + 8), "".join(o))


if __name__ == "__main__":
    here = os.path.dirname(os.path.abspath(__file__))
    for n, f in [("fig62-1-lambda-kappa-riverstone.svg", f1), ("fig62-2-medallion.svg", f2),
                 ("fig62-3-org-patterns.svg", f3), ("fig62-4-contracts-glue.svg", f4),
                 ("fig62-5-mesh-maturity.svg", f5)]:
        with open(os.path.join(here, n), "w") as fh:
            fh.write(f())
    print("ok")
