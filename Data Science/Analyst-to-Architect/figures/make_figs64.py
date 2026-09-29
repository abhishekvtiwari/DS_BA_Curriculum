# Diagrams for Chapter 64. Run: python3 make_figs64.py (from the figures folder)
# Every figure prints at the full text width (493.2 pt). All canvases are 680 px wide, so
# 1 px = 0.725 pt: the smallest text here, 10.5 px, prints at 7.6 pt (visual standard: 7 pt or more).
# Text is wrapped by measuring it with the DejaVu Sans metrics the PDF uses, so no label can run
# past its box. Figure 64.1's cells are read from the same table as companion/ch64/access-control-matrix.md.
import math, os
from PIL import ImageFont
from make_figs import *

GREEN = "#2f7d6d"; PURPLE = "#7a4fa0"; GOLD = "#b7791f"; RED = "#b23b3b"; BLUE2 = "#2f6690"
ORANGE = "#c0662b"; GREY = "#8a93a3"; GREYBG = "#f1f3f6"; SOFT = "#eef2f7"
W = 680
MIN = 10.5                                   # smallest font size used, px

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

def header_box(x, y, w, h, title_lines, c, band=22):
    """A white box with a coloured title band holding one or two lines of bold white text."""
    o = [rect(x, y, w, h, fill="#fff", stroke=c, sw=1.4, rx=6),
         f'<path d="M{x},{y + 6} a6,6 0 0 1 6,-6 H{x + w - 6} a6,6 0 0 1 6,6 V{y + band} H{x} Z" fill="{c}"/>']
    for i, t in enumerate(title_lines):
        o.append(text(x + w / 2, y + 15.5 + i * 14, t, 11, "#fff", "bold", anchor="middle"))
    return "".join(o)


# ---------- Figure 64.1: the access-control matrix ----------
RESOURCES = ["Own-branch orders", "All-branch revenue", "Customer PII", "Model training data", "Credential vault"]
MATRIX = [  # the same cells as companion/ch64/access-control-matrix.md
    ("Branch staff",       ["full, own branch", "none", "none", "none", "none"]),
    ("Regional manager",   ["full, own region", "read", "masked", "none", "none"]),
    ("Analytics team",     ["read", "read", "masked", "read", "none"]),
    ("Data platform team", ["read", "read", "break-glass", "full", "admin, logged"]),
    ("Pipelines (service accounts)", ["load", "load", "load", "load", "own secret"]),
    ("External auditor",   ["audit only", "audit only", "audit only", "none", "none"]),
]
LEVEL = {"full": GREEN, "read": ACC, "masked": PURPLE, "break-glass": ORANGE, "load": BLUE2,
         "admin": GOLD, "own": GOLD, "audit": GOLD, "none": GREY}

def f1():
    lx, x0, top = 14, 138, 8
    cw = (W - 8 - x0) / len(RESOURCES)
    o = []
    hl = [wrap(r, MIN, cw - 8, True) for r in RESOURCES]
    hh = 14 * max(len(h) for h in hl)
    for i, h in enumerate(hl):
        o.append(lines_at(x0 + i * cw + cw / 2, top + 12, h, MIN, INK, "bold", anchor="middle", lead=14))
    y0, rh = top + hh + 8, 36
    for j, (role, cells) in enumerate(MATRIX):
        cy = y0 + j * rh + rh / 2
        rl = wrap(role, MIN, x0 - lx - 8, True)
        o.append(lines_at(lx, cy + 4 - (len(rl) - 1) * 7, rl, MIN, INK, "bold", lead=14))
        for i, lab in enumerate(cells):
            c = LEVEL[lab.split(",")[0].split()[0]]
            none = lab == "none"
            o.append(rect(x0 + i * cw + 3, y0 + j * rh + 3, cw - 6, rh - 6,
                          fill=GREYBG if none else "#fff", stroke=c, sw=1.3, rx=5))
            ll = wrap(lab, MIN, cw - 14, not none)
            o.append(lines_at(x0 + i * cw + cw / 2, cy + 4 - (len(ll) - 1) * 6.5, ll, MIN,
                              MUTED if none else c, "normal" if none else "bold", anchor="middle", lead=13))
    y = y0 + len(MATRIX) * rh + 16
    note = ("Every cell is written out in words; the colours only group the same level. "
            "Masked = customers appear as a code, no contact details. Break-glass = no one day to day; "
            "logged, approved access for an incident. Load = a pipeline copies data in, with no login a person can use.")
    nl = wrap(note, MIN, W - 2 * lx)
    o.append(lines_at(lx, y, nl, MIN, MUTED, lead=14))
    return svg(W, y + 14 * len(nl) - 4, "".join(o))


# ---------- Figure 64.2: privacy by design, four habits ----------
def f2():
    items = [("Data minimization", ACC, "Collect only what the feature actually needs.",
              "The lead score uses company size, industry and recency, never browsing data."),
             ("Purpose limitation", GREEN, "Data collected for one reason is not reused for another without a fresh reason.",
              "Support tickets are not fed into marketing scoring."),
             ("Sensible retention", GOLD, "Keep data only as long as it is needed, then delete it on purpose.",
              "Raw PO emails deleted 90 days after the order is confirmed."),
             ("Pseudonymize or anonymize", PURPLE, "Mask identity when the analysis doesn't need it.",
              "Assistant logs keep a hash of the question for a year, the words for 30 days (Ch 57).")]
    gap, top, pad = 10, 6, 8
    bw = (W - 12 - 3 * gap) / 4
    blocks = []
    for name, c, desc, ex in items:
        tl = wrap(name, 11, bw - 10, True)
        dl = wrap(desc, MIN, bw - 2 * pad)
        el = wrap("Riverstone: " + ex, MIN, bw - 2 * pad)
        blocks.append((tl, c, dl, el))
    band = 8 + 14 * max(len(b[0]) for b in blocks)
    dh = 13.5 * max(len(b[2]) for b in blocks)
    eh = 13.5 * max(len(b[3]) for b in blocks)
    h = band + 10 + dh + 8 + eh + 8
    o = []
    for i, (tl, c, dl, el) in enumerate(blocks):
        x = 6 + i * (bw + gap)
        o.append(header_box(x, top, bw, h, tl, c, band=band))
        o.append(lines_at(x + pad, top + band + 16, dl, MIN, INK, lead=13.5))
        ey = top + band + 10 + dh + 4
        o.append(rect(x + 4, ey, bw - 8, eh + 8, fill=SOFT, rx=4))
        o.append(lines_at(x + pad, ey + 14, el, MIN, MUTED, lead=13.5))
    return svg(W, top + h + 6, "".join(o))


# ---------- Figure 64.4: the model governance loop ----------
def f3():
    stages = [("Version and register", ACC, "Record: model ID, training-data snapshot, code version"),
              ("Approve for production", GOLD, "Record: approver's name, not the builder, and date"),
              ("Monitor in production", GREEN, "Record: drift, performance and fairness checks, dated"),
              ("Audit trail", PURPLE, "Record: every prediction linked to its model version"),
              ("Retrain or retire", RED, "Record: the decision and who made it (Ch 63)")]
    gap, top, pad = 16, 30, 7
    bw = (W - 12 - 4 * gap) / 5
    blocks = [(wrap(n, 11, bw - 8, True), c, wrap(d, MIN, bw - 2 * pad)) for n, c, d in stages]
    band = 8 + 14 * max(len(b[0]) for b in blocks)
    h = band + 10 + 13.5 * max(len(b[2]) for b in blocks) + 4
    o = [text(W / 2, 16, "Chapter 56's MLOps loop, governed: every stage leaves a record", 11.5, INK, "bold",
              anchor="middle", family=HEAD)]
    for i, (tl, c, dl) in enumerate(blocks):
        x = 6 + i * (bw + gap)
        o.append(header_box(x, top, bw, h, tl, c, band=band))
        o.append(lines_at(x + pad, top + band + 16, dl, MIN, INK, lead=13.5))
        if i < 4:
            o.append(arrow(x + bw + 2, top + h / 2, x + bw + gap - 2, top + h / 2))
    # the return path: from the last box back to the first, under the row
    x_first, x_last = 6 + bw / 2, 6 + 4 * (bw + gap) + bw / 2
    yb, yl = top + h, top + h + 22
    o.append(path(f"M{x_last},{yb + 2} V{yl} H{x_first}", stroke=MUTED, sw=1.5))
    o.append(arrow(x_first, yl, x_first, yb + 2))
    o.append(text(W / 2, yl + 16, "a retrained model starts the loop again as a new version", MIN, MUTED,
                  anchor="middle", style="italic"))
    return svg(W, yl + 24, "".join(o))


if __name__ == "__main__":
    here = os.path.dirname(os.path.abspath(__file__))
    for n, f in [("fig64-1-access-model.svg", f1), ("fig64-2-privacy-by-design.svg", f2),
                 ("fig64-4-model-governance.svg", f3)]:
        open(os.path.join(here, n), "w").write(f())
    print("ok")
