# Diagrams for Chapter 63. Run: python3 make_figs63.py (from the figures folder)
# Every figure prints at the full text width (493.2 pt). All canvases are 680 px wide, so
# 1 px = 0.725 pt: the smallest text here, 10.5 px, prints at 7.6 pt (visual standard: 7 pt or more).
# Text is wrapped by measuring it with the DejaVu Sans metrics the PDF uses, so no label can
# run past its box. Figure 63.1's scores and Figure 63.4's counts are read from
# companion/ch63/automation-inventory.csv, the file the reader works from.
import csv, math, os
from collections import Counter
from PIL import ImageFont
from make_figs import *

GREEN = "#2f7d6d"; PURPLE = "#7a4fa0"; GOLD = "#b7791f"; RED = "#b23b3b"; BLUE2 = "#2f6690"
ORANGE = "#c0662b"; GREY = "#8a93a3"; GREYBG = "#f1f3f6"; SOFT = "#eef2f7"; LIGHT = "#dfe5ec"
W = 680
MIN = 10.5                                   # smallest font size used, px
ARROW_R = "→"
HERE = os.path.dirname(os.path.abspath(__file__))
INVENTORY = os.path.join(HERE, "..", "companion", "ch63", "automation-inventory.csv")

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

def arrow(x1, y1, x2, y2, c=MUTED, sw=1.5):
    a = math.atan2(y2 - y1, x2 - x1); s = 7
    p1 = (x2 - s * math.cos(a - 0.45), y2 - s * math.sin(a - 0.45))
    p2 = (x2 - s * math.cos(a + 0.45), y2 - s * math.sin(a + 0.45))
    return (path(f"M{x1},{y1} L{x2},{y2}", stroke=c, sw=sw)
            + f'<path d="M{x2},{y2} L{p1[0]:.1f},{p1[1]:.1f} L{p2[0]:.1f},{p2[1]:.1f} Z" fill="{c}"/>')

def header_box(x, y, w, h, title, c):
    """A white box with a coloured title band."""
    return (rect(x, y, w, h, fill="#fff", stroke=c, sw=1.4, rx=6)
            + f'<path d="M{x},{y + 6} a6,6 0 0 1 6,-6 H{x + w - 6} a6,6 0 0 1 6,6 V{y + 22} H{x} Z" fill="{c}"/>'
            + text(x + 8, y + 15.5, title, 11, "#fff", "bold"))

def inventory():
    with open(INVENTORY, encoding="utf-8") as f:
        return {r["automation_name"]: r for r in csv.DictReader(f)}


# ---------- Figure 63.1: value against effort, risk as bubble size ----------
def f1():
    inv = inventory()
    def scores(name):
        r = inv[name]; return int(r["value_score"]), int(r["effort_score"]), int(r["risk_score"])
    # (label, value, effort, risk, colour, where the label goes)
    pts = [("Daily Sales Flash", *scores("Daily Sales Flash"), ACC, "right"),
           ("Branch macro (Ch 19)", *scores("Branch consolidation macro (MASTER_FINAL_v7)"), GREEN, "right"),
           ("PO intake, assisted", *scores("PO intake (assisted)"), GOLD, "right"),
           ("PO intake, straight through", 5, 3, 5, RED, "right"),      # rejected candidate, not in the inventory
           ("Dagster pipeline", *scores("Dagster ingestion pipeline"), BLUE2, "below"),
           ("CRM reverse-ETL syncs", *scores("CRM reverse-ETL syncs"), PURPLE, "right")]
    o = [text(20, 24, "Value against effort, with risk as the bubble's size", 13.5, INK, "bold", family=HEAD)]
    gx, gy, gw, gh = 62, 44, 580, 300
    o.append(rect(gx, gy, gw, gh, fill="#fff", stroke=RULE, sw=1.2))
    cx = lambda e: gx + (e - 0.5) / 5 * gw
    cy = lambda v: gy + gh - (v - 0.5) / 5 * gh
    for s in range(1, 6):
        o.append(path(f"M{cx(s)},{gy} V{gy + gh}", stroke=LIGHT, sw=1))
        o.append(path(f"M{gx},{cy(s)} H{gx + gw}", stroke=LIGHT, sw=1))
        o.append(text(cx(s), gy + gh + 15, str(s), MIN, MUTED, anchor="middle"))
        o.append(text(gx - 8, cy(s) + 4, str(s), MIN, MUTED, anchor="end"))
    o.append(path(f"M{gx + gw / 2},{gy} V{gy + gh}", stroke=GREY, sw=1, dash="4 3"))
    o.append(path(f"M{gx},{gy + gh / 2} H{gx + gw}", stroke=GREY, sw=1, dash="4 3"))
    o.append(text(gx + 6, gy + 14, "quick wins", MIN, MUTED, style="italic"))
    o.append(text(gx + gw - 6, gy + gh / 2 - 6, "big bets", MIN, MUTED, anchor="end", style="italic"))
    o.append(text(gx + 6, gy + gh - 7, "fill-ins", MIN, MUTED, style="italic"))
    o.append(text(gx + gw - 6, gy + gh - 7, "question marks", MIN, MUTED, anchor="end", style="italic"))
    o.append(text(gx + gw / 2, gy + gh + 32, "EFFORT TO BUILD AND RUN (1 = days, 5 = months) " + ARROW_R,
                  MIN, MUTED, "bold", anchor="middle"))
    ylab = text(gx - 30, gy + gh / 2, "VALUE (1 to 5) " + ARROW_R, MIN, MUTED, "bold", anchor="middle")
    o.append(f'<g transform="rotate(-90 {gx - 30} {gy + gh / 2})">' + ylab + "</g>")
    for label, v, e, k, c, where in pts:
        px, py, r = cx(e), cy(v), 9 + 4 * k
        dash = ' stroke-dasharray="4 2.5"' if k >= 4 else ""
        o.append(f'<circle cx="{px:.1f}" cy="{py:.1f}" r="{r}" fill="{c}" fill-opacity="0.25" '
                 f'stroke="{c}" stroke-width="2"{dash}/>')
        o.append(text(px, py + 4, f"R{k}", MIN, INK, "bold", anchor="middle"))
        sub = f"value {v}, effort {e}, risk {k}"
        if where == "right":
            o.append(text(px + r + 6, py - 2, label, MIN, INK, "bold"))
            o.append(text(px + r + 6, py + 12, sub, MIN, MUTED))
            assert px + r + 6 + max(width(label, MIN, True), width(sub, MIN)) < gx + gw - 4, label
        else:
            lx = min(px, gx + gw - 6 - max(width(label, MIN, True), width(sub, MIN)) / 2)
            o.append(text(lx, py + r + 13, label, MIN, INK, "bold", anchor="middle"))
            o.append(text(lx, py + r + 26, sub, MIN, MUTED, anchor="middle"))
    ly = gy + gh + 52
    legend = ("Bubble size and the R number show the risk score: 1 = a wrong result is stopped before anyone "
              "uses it, 5 = wrong results reach customers unseen. A dashed outline marks high risk (4 or 5).")
    ll = wrap(legend, MIN, W - 40)
    o.append(lines_at(20, ly, ll, MIN, MUTED, lead=14))
    return svg(W, ly + 14 * len(ll) + 4, "".join(o))


# ---------- Figure 63.2: the reference architecture, six layers in two rows ----------
def f2():
    layers = [("1  Sources", MUTED, "ERP, CRM, plant sensors, inbound email, hand-kept spreadsheets", "the branch files it opens"),
              ("2  Ingestion", ACC, "Dagster jobs copy data in on a schedule (Ch 45, 46)", "Workbooks.Open, file by file"),
              ("3  Warehouse", BLUE2, "raw, staging and mart tables, plus the Delta sensor archive (Ch 45, 49)", "the Master sheet it rebuilds"),
              ("4  Semantic layer", GREEN, "one tested definition per metric (Ch 32)", "the one formula its author chose for revenue"),
              ("5  Delivery and activation", GOLD, "the Flash, dashboards, CRM writes, ERP orders (Ch 16, 20, 51, 58)", "the PDF it emails"),
              ("6  Monitoring", RED, "checks, run logs and failure alerts (Ch 20, 46, 47)", "its checks since Ch 19; before that, nothing")]
    o = [text(20, 24, "One shape under every automation: six layers", 13.5, INK, "bold", family=HEAD)]
    bw, gap, top = 200, 20, 42
    x0 = (W - 3 * bw - 2 * gap) / 2
    size = 10.5
    body = []
    for name, c, plat, mac in layers:
        pl = wrap("Platform: " + plat, size, bw - 16)
        ml = wrap("In a macro: " + mac, size, bw - 16)
        body.append((name, c, pl, ml))
    rows_h = []
    for row in (body[:3], body[3:]):
        rows_h.append(max(22 + 10 + (len(pl) + len(ml)) * 13.5 + 10 for _, _, pl, ml in row))
    y = top
    for ri, row in enumerate((body[:3], body[3:])):
        h = rows_h[ri]
        for i, (name, c, pl, ml) in enumerate(row):
            x = x0 + i * (bw + gap)
            o.append(header_box(x, y, bw, h, name, c))
            o.append(lines_at(x + 8, y + 38, pl, size, INK, lead=13.5))
            o.append(lines_at(x + 8, y + 38 + len(pl) * 13.5 + 4, ml, size, MUTED, lead=13.5))
            if i < 2:
                o.append(arrow(x + bw + 2, y + h / 2, x + bw + gap - 2, y + h / 2))
        if ri == 0:
            # from layer 3 (end of the first row) down and back to layer 4 (start of the second)
            xr = x0 + 2 * (bw + gap) + bw / 2; xl = x0 + bw / 2
            y1 = y + h; y2 = y + h + 26
            o.append(path(f"M{xr},{y1 + 2} V{y1 + 13} H{xl} V{y2 - 8}", stroke=MUTED, sw=1.5))
            o.append(arrow(xl, y2 - 9, xl, y2 - 2))
        y += h + 26
    y += 4
    note = ("A single macro (Ch 19) does all six jobs inside one workbook; Chapter 46's pipeline does "
            "each one in its own named piece. Same six jobs, different visibility.")
    nl = wrap(note, 11, W - 60)
    o.append(rect(20, y, W - 40, 16 + len(nl) * 15, fill=GREYBG, stroke=RULE, rx=6))
    o.append(lines_at(30, y + 19, nl, 11, INK, lead=15))
    return svg(W, y + 26 + len(nl) * 15, "".join(o))


# ---------- Figure 63.3: shared services around every automation ----------
def f3():
    o = [text(20, 24, "Four shared services, built once, used by every automation", 13.5, INK, "bold", family=HEAD)]
    sw_, sh = 196, 78
    services = [("Notification service", ACC, "one function sends email or chat for everyone", 20, 44),
                ("Credential vault", GREEN, "no password in any script; rotate without editing code", 20, 178),
                ("Run logs", GOLD, "every run: start, end, outcome, key numbers, in one place", W - 20 - sw_, 44),
                ("Alerting", RED, "a failure pages the owner, the same way every time", W - 20 - sw_, 178)]
    hx, hy, hw, hh = 250, 44, 180, 212
    o.append(header_box(hx, hy, hw, hh, "Every automation", INK))
    members = ["Daily Sales Flash", "Dagster pipeline", "CRM syncs", "PO intake", "support assistant",
               "defect model", "branch macros", "… all 24 in the inventory"]
    o.append(lines_at(hx + 12, hy + 52, members, MIN, INK, lead=19))
    for name, c, sub, x, y in services:
        o.append(header_box(x, y, sw_, sh, name, c))
        o.append(lines_at(x + 8, y + 40, wrap(sub, MIN, sw_ - 16), MIN, INK, lead=14))
        # every arrow runs from the service box's inner edge, level, to the hub box's edge
        ya = y + sh / 2
        assert hy + 24 < ya < hy + hh
        if x < hx:
            o.append(arrow(x + sw_, ya, hx - 2, ya, c))
        else:
            o.append(arrow(x, ya, hx + hw + 2, ya, c))
    y = 280
    note = ("Chapter 20 built the minimum version of each for one script: its own mail code, "
            "environment variables in a .env file instead of a vault, a log file, and a failure email.")
    nl = wrap(note, 11, W - 60)
    o.append(rect(20, y, W - 40, 16 + len(nl) * 15, fill=GREYBG, stroke=RULE, rx=6))
    o.append(lines_at(30, y + 19, nl, 11, INK, lead=15))
    return svg(W, y + 26 + len(nl) * 15, "".join(o))


# ---------- Figure 63.4: what the first audit found ----------
def f4():
    counts = Counter(r["audit_category"] for r in inventory().values())
    rows = [("Documented, owned, monitored", counts["documented and owned"], "Keep: the model to copy", GREEN,
             "Flash (Ch 20), Dagster pipeline (Ch 46), CRM syncs (Ch 51), support assistant (Ch 55), defect model (Ch 56), PO intake (Ch 58)"),
            ("Working, but no owner on record", counts["working but no owner"], "Urgent: name an owner", GOLD,
             "Branch macros, personal Apps Script projects, a Power Automate flow nobody remembers building"),
            ("Duplicated logic, disagreeing outputs", counts["duplicated logic"], "Merge each pair", ORANGE,
             "Two pairs: Delhi and Kolkata consolidation macros; Bengaluru and Mumbai HO stock-report reformatters"),
            ("Business-critical, single point of failure", counts["single point of failure"], "Confirm the fix held", RED,
             "MASTER_FINAL_v7 (Ch 19): rewritten and owned since Ch 19; the audit confirmed its checks still run"),
            ("Actively broken, nobody had noticed", counts["actively broken"], "Fix now", RED,
             "An Apps Script trigger that stopped firing five months earlier; a macro saving to a moved folder")]
    o = [text(20, 24, "The first automation audit: 24 automations, five categories", 13.5, INK, "bold", family=HEAD)]
    cols = [(20, "Category", 150), (178, "Count", 40), (226, "Action", 104), (338, "Examples", W - 20 - 338 - 6)]
    y = 40
    o.append(rect(20, y, W - 40, 24, fill=INK, rx=4))
    for x, h, w in cols:
        if h == "Count":
            o.append(text(x + w - 4, y + 16, h, 11, "#fff", "bold", anchor="end"))
        else:
            o.append(text(x + 8, y + 16, h, 11, "#fff", "bold"))
    y += 24
    for i, (cat, n, action, c, ex) in enumerate(rows):
        cl = wrap(cat, MIN, cols[0][2] - 12, True)
        al = wrap(action, MIN, cols[2][2] - 8, True)
        el = wrap(ex, MIN, cols[3][2] - 8)
        h = max(len(cl), len(al), len(el)) * 14 + 12
        o.append(rect(20, y, W - 40, h, fill="#fff" if i % 2 == 0 else ROWALT))
        o.append(rect(20, y, 5, h, fill=c))
        o.append(lines_at(cols[0][0] + 10, y + 17, cl, MIN, INK, "bold", lead=14))
        o.append(text(cols[1][0] + cols[1][2] - 4, y + 17, str(n), 12, INK, "bold", anchor="end"))
        o.append(lines_at(cols[2][0] + 8, y + 17, al, MIN, c, "bold", lead=14))
        o.append(lines_at(cols[3][0] + 8, y + 17, el, MIN, MUTED, lead=14))
        y += h
    o.append(path(f"M20,{y} H{W - 20}", stroke=RULE, sw=1))
    total = sum(r[1] for r in rows)
    assert total == 24
    o.append(text(cols[0][0] + 10, y + 17, "Total", MIN, INK, "bold"))
    o.append(text(cols[1][0] + cols[1][2] - 4, y + 17, str(total), 12, INK, "bold", anchor="end"))
    o.append(text(cols[2][0] + 8, y + 17, "17 had no owner, no monitoring and no written failure plan", MIN, MUTED))
    return svg(W, y + 28, "".join(o))


if __name__ == "__main__":
    os.chdir(HERE)
    for n, f in [("fig63-1-prioritization.svg", f1), ("fig63-2-reference-architecture.svg", f2),
                 ("fig63-3-shared-services.svg", f3), ("fig63-4-audit-findings.svg", f4)]:
        open(n, "w", encoding="utf-8").write(f())
    print("ok")
