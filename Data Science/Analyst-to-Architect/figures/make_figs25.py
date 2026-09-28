# Generates the SVG figures for Chapter 25. Run: python3 make_figs25.py
#
# Every figure is drawn on a 600 px canvas. It prints at the full text width (493.2 pt), so
# 1 px = 0.822 pt and the smallest text used here, 9 px, prints at 7.4 pt (visual standard: >= 7 pt).
# The figures carry no in-figure title: the caption under each one says what it shows.
from make_figs import *
from PIL import ImageFont

GREEN = "#2f7d6d"; PURPLE = "#7a4fa0"; ORANGE = "#b35a1f"; RED = "#b23b3b"; TEAL = "#1f6fa3"; GREY = "#5b6475"
W = 600
FONTS = {
    ("normal", ""): "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    ("bold", ""): "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    ("normal", "italic"): "/usr/share/fonts/truetype/dejavu/DejaVuSans-Oblique.ttf",
    ("bold", "italic"): "/usr/share/fonts/truetype/dejavu/DejaVuSans-BoldOblique.ttf",
}
_cache = {}


def width(s, size, weight="normal", style=""):
    """Width in px of s set in DejaVu Sans (the figures' font) at size px."""
    key = (weight, style, size)
    if key not in _cache:
        _cache[key] = ImageFont.truetype(FONTS[(weight, style)], size=100)
    return _cache[key].getlength(s) * size / 100


def fit(s, maxw, size, weight="normal", style=""):
    """Break s into lines no wider than maxw px."""
    lines, cur = [], ""
    for w in s.split():
        trial = (cur + " " + w).strip()
        if cur and width(trial, size, weight, style) > maxw:
            lines.append(cur); cur = w
        else:
            cur = trial
    lines.append(cur)
    return lines


def para(x, y, lines, size, fill=INK, lh=None, weight="normal", style=""):
    lh = lh or size * 1.32
    return "".join(text(x, y + i * lh, l, size, fill, weight, style=style) for i, l in enumerate(lines))


def head_band(x, y, w, h, c, r=6):
    return f'<path d="M{x},{y+r} a{r},{r} 0 0 1 {r},-{r} H{x+w-r} a{r},{r} 0 0 1 {r},{r} V{y+h} H{x} Z" fill="{c}"/>'


def arrow_down(x, y1, y2, c=GREY, sw=1.6):
    return (path(f"M{x},{y1} V{y2-5}", stroke=c, sw=sw)
            + f'<path d="M{x-4},{y2-6} L{x},{y2} L{x+4},{y2-6} Z" fill="{c}"/>')


def arrow_right(x1, x2, y, c=GREY, sw=1.6):
    return (path(f"M{x1},{y} H{x2-5}", stroke=c, sw=sw)
            + f'<path d="M{x2-6},{y-4} L{x2},{y} L{x2-6},{y+4} Z" fill="{c}"/>')


# ---------- Figure 25.1: order-to-cash as a swimlane ----------
LANES = [("Customer", PURPLE), ("Sales", ACC), ("Warehouse", TEAL), ("Finance", GREEN)]
SWIM = [  # (step, label, lane, date) -- Chapter 3, section 3.2
    (1, "Enquiry", 0, "22 Oct 2025"),
    (2, "Visit and terms", 1, "4 Nov 2025"),
    (3, "Quote", 1, "22 Dec 2025"),
    (4, "Order typed in", 1, "5 Jan 2026"),
    (5, "Stock check", 2, "5 Jan 2026"),
    (6, "Pick, pack, ship", 2, "6 Jan 2026"),
    (7, "Invoice 9001", 3, "6 Jan 2026"),
    (8, "POD scanned", 2, "8 Jan 2026"),
    (9, "Payment matched", 3, "2 Feb 2026"),
    (10, "January report", 3, "3 Feb 2026"),
]


def fig_swimlane():
    DX, LX = 6, 82                     # date column, first lane
    LW = (W - 6 - LX) / 4              # lane width
    BW, BH, P, Y0 = LW - 16, 18, 28, 42  # box, row pitch, first row
    o = []
    ybot = Y0 + len(SWIM) * P - 4
    # lane bands (clipped to the lane edges) and headers
    for i, (name, c) in enumerate(LANES):
        x = LX + i * LW
        if i % 2 == 0:
            o.append(rect(x, 30, LW, ybot - 30, fill="#f4f7fb"))
        o.append(head_band(x + 3, 6, LW - 6, 20, c, r=5))
        o.append(text(x + LW / 2, 20, name, 10.5, "#fff", "bold", anchor="middle"))
    for i in range(5):
        x = LX + i * LW
        o.append(path(f"M{x},{30} V{ybot}", stroke=RULE, sw=1))
    o.append(text(DX, 20, "Date", 10, INK, "bold"))
    o.append(path(f"M{DX},{ybot} H{LX + 4*LW}", stroke=RULE, sw=1))
    # boxes
    boxes = []
    for r, (num, label, lane, date) in enumerate(SWIM):
        y = Y0 + r * P
        x = LX + lane * LW + (LW - BW) / 2
        c = LANES[lane][1]
        o.append(text(DX, y + 13, date, 9.5, GREY))
        o.append(rect(x, y, BW, BH, fill="#fff", stroke=c, sw=1.4, rx=4))
        o.append(f'<circle cx="{x+10}" cy="{y+BH/2}" r="7" fill="{c}"/>')
        o.append(text(x + 10, y + BH / 2 + 3.3, str(num), 9 if num < 10 else 8.6, "#fff", "bold", anchor="middle"))
        o.append(text(x + 21, y + 13, label, 9.5, INK))
        boxes.append((x + BW / 2, y, lane))
    # transitions; a crossing between lanes is red and carries an H badge
    for i in range(len(boxes) - 1):
        cx1, y1, l1 = boxes[i]; cx2, y2, l2 = boxes[i + 1]
        yb, yt = y1 + BH, y2
        if l1 == l2:
            o.append(arrow_down(cx1, yb, yt, GREY, 1.4))
        else:
            ym = (yb + yt) / 2
            o.append(path(f"M{cx1},{yb} V{ym} H{cx2} V{yt-4}", stroke=RED, sw=1.8))
            o.append(f'<path d="M{cx2-4},{yt-5} L{cx2},{yt} L{cx2+4},{yt-5} Z" fill="{RED}"/>')
            hx = LX + max(l1, l2) * LW          # the lane boundary it crosses
            o.append(f'<circle cx="{hx}" cy="{ym}" r="6.5" fill="{RED}" stroke="#fff" stroke-width="1"/>')
            o.append(text(hx, ym + 3.3, "H", 9, "#fff", "bold", anchor="middle"))
    # legend
    ly = ybot + 18
    o.append(f'<circle cx="{DX+7}" cy="{ly-3.5}" r="6.5" fill="{RED}"/>')
    o.append(text(DX + 7, ly - 0.2, "H", 9, "#fff", "bold", anchor="middle"))
    o.append(text(DX + 19, ly, "A handoff: work crosses from one lane to another (red arrow). Five of the nine transitions do.", 9.5, INK))
    o.append(text(DX, ly + 17, "Enquiry to cash: 103 days.  Order to invoice: 1 day.  Invoice to payment: 27 days.  Order to cash: 28 days.", 9.5, GREY))
    return svg(W, ly + 26, "".join(o))


# ---------- Figure 25.2: the four data products ----------
def fig_four_products():
    products = [
        ("Report or dashboard", ACC, ["Who opens it, and how often?", "What do they do next?", "What is one row?",
                                      "What date range is the default?", "Who may see which rows?"],
         "Answers a question the reader already knew the answer to."),
        ("Pipeline", TEAL, ["What is the source of truth?", "What happens when it is late?",
                            "What happens when the past changes?", "Run twice: the same result?",
                            "Who is alerted, and how fast?"],
         "Keeps running, shows a green tick, and is quietly wrong."),
        ("Model", PURPLE, ["What decision does it serve?", "What does each kind of mistake cost?",
                           "What baseline must it beat?", "Which accounts are never scored?",
                           "What is written out with each score?"],
         "Is accurate, and nobody changes what they do."),
        ("Metric definition", GREEN, ["What exactly is counted?", "What is excluded?", "Which teams must agree?",
                                      "Where does the definition live?", "How is a change announced?"],
         "Lives inside one query and is reinvented by every new report."),
    ]
    G, M = 12, 4
    CW = (W - 2 * M - G) / 2
    QL = 13
    fails = [fit(f, CW - 28, 9.5) for *_, f in products]
    FH = 16 + max(len(f) for f in fails) * QL + 6
    CH = 24 + 8 + 5 * QL + 8 + FH + 8
    o = []
    for i, (name, c, qs, fail) in enumerate(products):
        x = M + (i % 2) * (CW + G); y = M + (i // 2) * (CH + G)
        o.append(rect(x, y, CW, CH, fill="#fff", stroke=c, sw=1.5, rx=6))
        o.append(head_band(x, y, CW, 24, c))
        o.append(text(x + 10, y + 16.5, name, 11, "#fff", "bold"))
        yy = y + 24 + 8 + 10
        for q in qs:
            o.append(f'<circle cx="{x+14}" cy="{yy-3.3}" r="2.4" fill="{c}"/>')
            o.append(text(x + 22, yy, q, 9.5, INK))
            yy += QL
        fy = y + CH - 8 - FH
        o.append(rect(x + 8, fy, CW - 16, FH, fill="#f1f4f8", stroke=c, sw=0.8, rx=4))
        o.append(text(x + 14, fy + 12, "HOW IT FAILS", 9, c, "bold"))
        o.append(para(x + 14, fy + 12 + QL, fails[i], 9.5, INK, QL))
    return svg(W, 2 * M + 2 * CH + G, "".join(o))


# ---------- Figure 25.3: anatomy of a user story ----------
def fig_story():
    o = []
    M = 4; BWd = W - 2 * M
    parts = [("As a", "sales rep", PURPLE, "who wants it"),
             ("I want", "to see which of my accounts are at risk of not ordering again", ACC, "what they want"),
             ("so that", "I can call them before they go quiet", GREEN, "why it is worth building")]
    note = fit("The \"so that\" clause is the one people drop, and the one that stops you building something "
               "correct and useless.", BWd - 24, 9, style="italic")
    SH = 12 + 3 * 18 + 6 + len(note) * 12 + 6
    o.append(rect(M, M, BWd, SH, fill="#fff", stroke=ACC, sw=1.6, rx=6))
    yy = M + 20
    for kw, body, c, what in parts:
        o.append(text(M + 12, yy, kw, 10, c, "bold", family=MONO))
        o.append(text(M + 70, yy, body, 10, INK))
        o.append(text(M + BWd - 10, yy, what, 9, GREY, anchor="end", style="italic"))
        yy += 18
    yy += 2
    o.append(path(f"M{M+12},{yy-10} H{M+BWd-12}", stroke=RULE, sw=0.8))
    o.append(para(M + 12, yy + 3, note, 9, GREY, 12, style="italic"))

    acs = [("AC-1", "Given I am a logged-in sales rep, when I open the at-risk list, then I see only accounts where "
                    "I am the assigned rep.", "scope", TEAL),
           ("AC-2", "Given an account with at least four days of orders whose time since its last order is more than "
                    "1.5 times its own average gap between orders, when the list is generated, then that account "
                    "appears on it.", "the actual rule, not the word \"recently\"", ACC),
           ("AC-3", "Given an account with fewer than four days of orders, including one with a single order or none, "
                    "when the list is generated, then it does not appear on the at-risk list and is counted separately "
                    "as \"too new to judge\", because there is no rhythm to compare against.", "the edge case", ORANGE),
           ("AC-4", "Given the list is open, when I sort by value at risk, then accounts are ordered by their last "
                    "twelve months' revenue, highest first.", "behavior the user can check", GREEN)]
    y = M + SH + 10
    TX = M + 52; TW = BWd - 52 - 10; LH = 12.5
    for tag, body, what, c in acs:
        lines = fit(body, TW, 9.5)
        h = 8 + len(lines) * LH + LH + 4
        o.append(rect(M, y, BWd, h, fill="#fff", stroke=RULE, sw=1, rx=5))
        o.append(f'<path d="M{M},{y+5} a5,5 0 0 1 5,-5 H{M+44} V{y+h} H{M+5} a5,5 0 0 1 -5,-5 Z" fill="{c}"/>')
        o.append(text(M + 22, y + h / 2 + 3.5, tag, 10, "#fff", "bold", anchor="middle", family=MONO))
        o.append(para(TX, y + 16, lines, 9.5, INK, LH))
        o.append(text(TX, y + 16 + len(lines) * LH, what, 9, c, "bold", style="italic"))
        y += h + 6
    return svg(W, y - 6 + M, "".join(o))


# ---------- Figure 25.4: a gap analysis row, worked (Riverstone's delivery step) ----------
def fig_gap():
    o = []
    M = 4; LH = 12.5
    SW, GW = 206, 136
    AG = (W - 2 * M - 2 * SW - GW) / 2           # room for each arrow
    xa, xg, xb = M, M + SW + AG, M + SW + AG + GW + AG
    asis = fit("A driver brings back a paper proof of delivery. Someone at Bhiwandi Main scans it, emails it to "
               "finance, and changes the order to Delivered by hand, days later or not at all. The ERP holds no "
               "delivery date.", SW - 16, 9.5)
    tobe = fit("The delivery is recorded in the ERP when the customer signs, with the date and time, and the "
               "signed proof of delivery is attached to the order.", SW - 16, 9.5)
    gap = fit("Nothing records the delivery when it happens. The ERP hears about it later, from a scanned "
              "email.", GW - 16, 9.5)
    TH = 22 + 10 + max(len(asis), len(tobe), len(gap)) * LH + 4
    for x, w, title, c, fill, lines in [(xa, SW, "AS-IS", RED, "#fdf1f1", asis), (xg, GW, "THE GAP", ORANGE, "#fdf5ee", gap),
                                        (xb, SW, "TO-BE", GREEN, "#eef7f4", tobe)]:
        o.append(rect(x, M, w, TH, fill=fill, stroke=c, sw=1.4, rx=6))
        o.append(head_band(x, M, w, 22, c))
        o.append(text(x + 10, M + 15.5, title, 10.5, "#fff", "bold"))
        o.append(para(x + 8, M + 22 + 16, lines, 9.5, INK, LH))
    o.append(arrow_right(xa + SW + 2, xg - 2, M + TH / 2, ORANGE, 1.8))
    o.append(arrow_right(xg + GW + 2, xb - 2, M + TH / 2, ORANGE, 1.8))

    rows = [("ROOT CAUSE", ORANGE, "Not \"the warehouse is slow\". The only record of the delivery is a piece of paper at "
                                   "the customer's site: the driver has no device, so the fact travels back on the truck "
                                   "before anyone can type it in."),
            ("REQUIREMENT", ACC, "FR-14: the delivery status and date shall be recorded in the ERP within one hour of "
                                 "the proof of delivery being signed."),
            ("DEPENDS ON", TEAL, "NFR-09: a delivery recorded where there is no mobile signal shall reach the ERP within "
                                 "one hour of the signal returning, and none shall be lost.")]
    LW = 100; BW2 = W - 2 * M
    y = M + TH + 22
    o.append(arrow_down(W / 2, M + TH + 2, y - 1, GREY, 1.8))
    for i, (label, c, body) in enumerate(rows):
        lines = fit(body, BW2 - LW - 20, 9.5)
        h = 10 + len(lines) * LH + 2
        o.append(rect(M, y, BW2, h, fill="#fff", stroke=c, sw=1.4, rx=6))
        o.append(f'<path d="M{M},{y+6} a6,6 0 0 1 6,-6 H{M+LW} V{y+h} H{M+6} a6,6 0 0 1 -6,-6 Z" fill="{c}"/>')
        o.append(text(M + 10, y + h / 2 + 3.5, label, 10, "#fff", "bold"))
        o.append(para(M + LW + 10, y + 16, lines, 9.5, INK, LH))
        y += h
        if i < len(rows) - 1:
            o.append(arrow_down(W / 2, y + 2, y + 20, GREY, 1.8))
            y += 22
    return svg(W, y + M, "".join(o))


if __name__ == "__main__":
    for name, fn in [("fig25-1-order-to-cash-swimlane.svg", fig_swimlane),
                     ("fig25-2-four-data-products.svg", fig_four_products),
                     ("fig25-3-user-story-anatomy.svg", fig_story),
                     ("fig25-4-gap-analysis.svg", fig_gap)]:
        open(name, "w").write(fn())
    print("ok")
