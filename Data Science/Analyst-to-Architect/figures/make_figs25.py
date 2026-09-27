# Generates the SVG figures for Chapter 25. Run: python3 make_figs25.py
from make_figs import *
from make_figs01 import wrap

GREEN="#2f7d6d"; PURPLE="#7a4fa0"; ORANGE="#c0662b"; RED="#b23b3b"; TEAL="#1f6fa3"; GREY="#5b6475"


def wraplines(s, n):
    words = s.split(); lines = []; cur = ""
    for w in words:
        if len(cur + " " + w) > n:
            lines.append(cur); cur = w
        else:
            cur = (cur + " " + w).strip()
    lines.append(cur)
    return lines


def arrow_right(x, y, length, colour=MUTED, sw=2):
    return (path(f"M{x},{y} H{x+length-6}", stroke=colour, sw=sw)
            + f'<path d="M{x+length-6},{y-5} L{x+length+1},{y} L{x+length-6},{y+5} Z" fill="{colour}"/>')


# ---------- Figure 25.1: the SDLC and the BA's work in each phase ----------
def fig_sdlc():
    phases = [
        ("Requirements", ACC, "All of it: elicit, map the as-is, gap analysis, write and agree the requirements", "heaviest"),
        ("Design", TEAL, "Answer questions, defend the requirement when design quietly drops part of it", "heavy"),
        ("Build", GREEN, "Stay available. Clarify the small things that would otherwise be guessed", "light"),
        ("Test", PURPLE, "Write or review the UAT plan, prepare the business users who will run it", "medium"),
        ("Deploy", ORANGE, "Run UAT, confirm the business need is met, sign off, hand over, train", "heavy"),
        ("Maintain", GREY, "Collect what did not work, specify the changes, watch the process drift back", "medium"),
    ]
    W, H, G, x0, y0 = 196, 186, 18, 32, 74
    o = [text(x0, 34, "The software development life cycle, and what the business analyst does in each phase",
              15, INK, "bold", family=HEAD),
         text(x0, 56, "The requirements phase is not the job. It is the first sixth of it.", 12.5, MUTED, style="italic")]
    bar = {"heaviest": 1.0, "heavy": 0.72, "medium": 0.5, "light": 0.26}
    for i, (name, c, dutyline, weight) in enumerate(phases):
        x = x0 + i * (W + G)
        o.append(rect(x + 2, y0 + 3, W, H, fill="#e9eef4", rx=8))
        o.append(rect(x, y0, W, H, fill="#fff", stroke=c, sw=1.6, rx=8))
        o.append(f'<path d="M{x},{y0+8} a8,8 0 0 1 8,-8 H{x+W-8} a8,8 0 0 1 8,8 V{y0+34} H{x} Z" fill="{c}"/>')
        o.append(text(x + 12, y0 + 23, f"{i+1}  {name}", 13.5, "#fff", "bold", family=HEAD))
        o.append(wrap(x + 12, y0 + 58, wraplines(dutyline, 26), 11.5, INK, 17))
        # how much of the BA's time this phase takes
        bw = int((W - 24) * bar[weight])
        o.append(rect(x + 12, y0 + H - 34, W - 24, 10, fill="#eef2f7", rx=5))
        o.append(rect(x + 12, y0 + H - 34, bw, 10, fill=c, rx=5))
        o.append(text(x + 12, y0 + H - 12, "BA effort: " + weight, 10.5, MUTED))
        if i < len(phases) - 1:
            o.append(arrow_right(x + W + 2, y0 + H / 2, G - 2))
    ybot = y0 + H
    o.append(path(f"M{x0},{ybot+30} H{x0+6*(W+G)-G}", stroke=RULE, sw=1.2, dash="4 4"))
    o.append(text(x0, ybot + 56, "Sign-off happens at the end of phase 1. Most of the damage in this job happens in phases 2 to 6.",
                  12.5, INK, "bold"))
    return svg(x0 * 2 + 6 * W + 5 * G, ybot + 76, "".join(o))


# ---------- Figure 25.2: order-to-cash as a swimlane ----------
LANES = [("Customer", PURPLE), ("Sales", ACC), ("Warehouse", TEAL), ("Finance", GREEN)]

# (step number, short label, lane index, date)
SWIM = [
    (1, "Enquiry", 0, "22 Oct"),
    (2, "Visit, credit\ncheck, terms", 1, "4 Nov"),
    (3, "Quote", 1, "22 Dec"),
    (4, "Order typed\ninto the ERP", 1, "5 Jan"),
    (5, "Stock check\nand reserve", 2, "5 Jan"),
    (6, "Pick, pack,\nship", 2, "6 Jan"),
    (7, "Invoice 9001", 3, "6 Jan"),
    (8, "Signed POD\nscanned", 2, "8 Jan"),
    (9, "Payment\nmatched", 3, "2 Feb"),
    (10, "January\nreport", 3, "3 Feb"),
]


def fig_swimlane():
    LW, LH, x0, y0 = 150, 118, 168, 92
    BW, BH = 124, 78
    o = [text(28, 36, "Riverstone order 5001, order-to-cash, by the team that owns each step",
              15, INK, "bold", family=HEAD),
         text(28, 58, "Five of the nine transitions cross a lane. Those crossings are where the delay and the errors collect.",
              12.5, MUTED, style="italic")]
    # lane bands and labels
    for li, (lname, c) in enumerate(LANES):
        y = y0 + li * LH
        if li % 2 == 1:
            o.append(rect(x0 - 140, y, 140 + 10 * LW, LH, fill="#f6f9fc"))
        o.append(path(f"M{x0-140},{y} H{x0+10*LW-26}", stroke=RULE, sw=1))
        o.append(rect(x0 - 140, y + 18, 126, LH - 36, fill="#fff", stroke=c, sw=1.6, rx=6))
        o.append(text(x0 - 77, y + LH / 2 + 5, lname, 13.5, c, "bold", anchor="middle", family=HEAD))
    ylast = y0 + len(LANES) * LH
    o.append(path(f"M{x0-140},{ylast} H{x0+10*LW-26}", stroke=RULE, sw=1))

    # step boxes
    centres = []
    for (num, label, lane, date) in SWIM:
        cx = x0 + (num - 1) * LW + BW / 2
        cy = y0 + lane * LH + LH / 2
        x = cx - BW / 2; y = cy - BH / 2
        c = LANES[lane][1]
        o.append(rect(x + 2, y + 3, BW, BH, fill="#e9eef4", rx=7))
        o.append(rect(x, y, BW, BH, fill="#fff", stroke=c, sw=1.5, rx=7))
        o.append(f'<circle cx="{x+16}" cy="{y+16}" r="11" fill="{c}"/>')
        o.append(text(x + 16, y + 20.5, str(num), 12, "#fff", "bold", anchor="middle"))
        o.append(text(x + BW - 8, y + 20, date, 10.5, MUTED, anchor="end"))
        o.append(wrap(x + 9, y + 44, label.split("\n"), 11.5, INK, 15))
        centres.append((cx, cy, lane))

    # transitions
    for i in range(len(centres) - 1):
        x1, y1, l1 = centres[i]; x2, y2, l2 = centres[i + 1]
        crossing = l1 != l2
        col = RED if crossing else MUTED
        sx = x1 + BW / 2 + 2; ex = x2 - BW / 2 - 2
        if not crossing:
            o.append(arrow_right(sx, y1, ex - sx, col, 2))
        else:
            midx = (sx + ex) / 2
            o.append(path(f"M{sx},{y1} H{midx} V{y2} H{ex-6}", stroke=col, sw=2.2))
            o.append(f'<path d="M{ex-6},{y2-5} L{ex+1},{y2} L{ex-6},{y2+5} Z" fill="{col}"/>')
            o.append(f'<circle cx="{midx}" cy="{(y1+y2)/2}" r="9" fill="{col}"/>')
            o.append(text(midx, (y1 + y2) / 2 + 4, "H", 11, "#fff", "bold", anchor="middle"))

    ybot = ylast + 26
    o.append(f'<circle cx="{x0-132}" cy="{ybot+12}" r="9" fill="{RED}"/>')
    o.append(text(x0 - 132, ybot + 16, "H", 11, "#fff", "bold", anchor="middle"))
    o.append(text(x0 - 116, ybot + 17, "a handoff: work crosses from one team to another", 12.5, INK, "bold"))
    o.append(text(x0 + 460, ybot + 17,
                  "Enquiry to cash: 103 days.  Order to invoice: 1 day.  Invoice to payment: 27 days.",
                  12.5, MUTED))
    return svg(x0 + 10 * LW + 20, ybot + 44, "".join(o))



# ---------- Figure 25.3: the four data products ----------
def fig_four_products():
    products = [
        ("Report or dashboard", ACC, [
            "Who opens it, how often?",
            "What do they do next?",
            "What is one row?",
            "Default date range?",
            "Who may see which rows?"],
         "Fails by answering a question the reader already knew"),
        ("Pipeline", TEAL, [
            "What is the source of truth?",
            "What happens when it is late?",
            "What happens when the past changes?",
            "Rerun twice: same result?",
            "Who is alerted, and how fast?"],
         "Fails by running green and being quietly wrong"),
        ("Model", PURPLE, [
            "What decision does it serve?",
            "What does each mistake cost?",
            "What is it compared against?",
            "Who is never scored?",
            "What is written out with the score?"],
         "Fails by being accurate while nobody changes what they do"),
        ("Metric definition", GREEN, [
            "What exactly is counted?",
            "What is excluded?",
            "Which teams must agree?",
            "Where does the definition live?",
            "How is a change announced?"],
         "Fails by living inside a query, reinvented by every new report"),
    ]
    W, H, G, x0, y0 = 288, 272, 20, 30, 78
    o = [text(x0, 34, "The four things a data team is asked to build, and what each requirement must pin down",
              15, INK, "bold", family=HEAD),
         text(x0, 56, "Ask the wrong set of questions and you will build something that works and nobody uses.",
              12.5, MUTED, style="italic")]
    for i, (name, c, qs, fail) in enumerate(products):
        x = x0 + i * (W + G)
        o.append(rect(x + 2, y0 + 3, W, H, fill="#e9eef4", rx=8))
        o.append(rect(x, y0, W, H, fill="#fff", stroke=c, sw=1.6, rx=8))
        o.append(f'<path d="M{x},{y0+8} a8,8 0 0 1 8,-8 H{x+W-8} a8,8 0 0 1 8,8 V{y0+36} H{x} Z" fill="{c}"/>')
        o.append(text(x + 14, y0 + 24, name, 13.5, "#fff", "bold", family=HEAD))
        yy = y0 + 62
        for q in qs:
            o.append(f'<circle cx="{x+20}" cy="{yy-4}" r="3" fill="{c}"/>')
            for j, ln in enumerate(wraplines(q, 30)):
                o.append(text(x + 32, yy + j * 15, ln, 11.5, INK))
            yy += 15 * len(wraplines(q, 30)) + 9
        o.append(rect(x + 10, y0 + H - 80, W - 20, 68, fill="#f6f9fc", rx=6))
        o.append(text(x + 20, y0 + H - 60, "HOW IT FAILS", 10, c, "bold", family=HEAD))
        o.append(wrap(x + 20, y0 + H - 42, wraplines(fail, 32), 11, MUTED, 15))
    return svg(x0 * 2 + 4 * W + 3 * G, y0 + H + 26, "".join(o))


# ---------- Figure 25.5: a gap analysis row, worked ----------
def fig_gap():
    o = [text(30, 36, "One row of a gap analysis, from Riverstone's invoicing step",
              15, INK, "bold", family=HEAD),
         text(30, 58, "A row is not finished until it produces a numbered requirement.", 12.5, MUTED, style="italic")]
    BW, BH, y0 = 330, 150, 86
    xa, xb = 30, 30 + BW + 150
    o.append(rect(xa + 2, y0 + 3, BW, BH, fill="#e9eef4", rx=8))
    o.append(rect(xa, y0, BW, BH, fill="#fdecec", stroke=RED, sw=1.6, rx=8))
    o.append(f'<path d="M{xa},{y0+8} a8,8 0 0 1 8,-8 H{xa+BW-8} a8,8 0 0 1 8,8 V{y0+34} H{xa} Z" fill="{RED}"/>')
    o.append(text(xa + 12, y0 + 23, "AS-IS", 13.5, "#fff", "bold", family=HEAD))
    o.append(wrap(xa + 12, y0 + 58, wraplines(
        "Finance raises the invoice after the warehouse emails a shipment notification, typically one to two days after the goods leave Bhiwandi Main.", 44),
        11.5, INK, 17))

    o.append(rect(xb + 2, y0 + 3, BW, BH, fill="#e9eef4", rx=8))
    o.append(rect(xb, y0, BW, BH, fill="#e2f3ee", stroke=GREEN, sw=1.6, rx=8))
    o.append(f'<path d="M{xb},{y0+8} a8,8 0 0 1 8,-8 H{xb+BW-8} a8,8 0 0 1 8,8 V{y0+34} H{xb} Z" fill="{GREEN}"/>')
    o.append(text(xb + 12, y0 + 23, "TO-BE", 13.5, "#fff", "bold", family=HEAD))
    o.append(wrap(xb + 12, y0 + 58, wraplines(
        "The invoice is raised automatically when the warehouse marks the order Shipped in the ERP.", 44),
        11.5, INK, 17))

    # the gap, between them
    gx = xa + BW + 14; gw = 122
    o.append(rect(gx, y0 + 30, gw, 90, fill="#fff", stroke=ORANGE, sw=1.6, rx=8))
    o.append(text(gx + gw / 2, y0 + 54, "THE GAP", 12, ORANGE, "bold", anchor="middle", family=HEAD))
    o.append(wrap(gx + 10, y0 + 76, ["no link between", "shipment status", "and invoicing"], 11, INK, 15))
    o.append(arrow_right(xa + BW + 2, y0 + BH / 2, 12, ORANGE))
    o.append(arrow_right(gx + gw + 2, y0 + BH / 2, 12, ORANGE))

    # root cause and requirement stack
    y1 = y0 + BH + 28
    rows = [("ROOT CAUSE", ORANGE, "Not \"finance is slow\". The warehouse updates the ERP once a day from its own spreadsheet, so the status change is not reliable enough to trigger anything."),
            ("REQUIREMENT", ACC, "FR-11: when an order's status changes to Shipped, the system shall generate the invoice for that order within one hour."),
            ("DEPENDS ON", TEAL, "NFR-04: order status in the ERP shall be updated within fifteen minutes of dispatch.")]
    TW = xb + BW - xa
    for i, (label, c, body) in enumerate(rows):
        y = y1 + i * 82
        o.append(rect(xa + 2, y + 3, TW, 68, fill="#e9eef4", rx=8))
        o.append(rect(xa, y, TW, 68, fill="#fff", stroke=c, sw=1.5, rx=8))
        o.append(rect(xa, y, 150, 68, fill=c, rx=8))
        o.append(rect(xa + 140, y, 10, 68, fill=c))
        o.append(text(xa + 14, y + 39, label, 12.5, "#fff", "bold", family=HEAD))
        o.append(wrap(xa + 164, y + 26, wraplines(body, 76), 11.5, INK, 17))
        if i < len(rows) - 1:
            o.append(path(f"M{xa+TW/2},{y+70} V{y+80}", stroke=MUTED, sw=2))
            o.append(f'<path d="M{xa+TW/2-5},{y+78} L{xa+TW/2},{y+84} L{xa+TW/2+5},{y+78} Z" fill="{MUTED}"/>')
    return svg(xb + BW + 30, y1 + 3 * 82 + 16, "".join(o))


# ---------- Figure 25.4: anatomy of a user story ----------
def fig_story():
    o = [text(30, 36, "A user story, and the acceptance criteria that make it testable",
              15, INK, "bold", family=HEAD),
         text(30, 58, "Without criteria a story cannot be tested, so it can never be finished.", 12.5, MUTED, style="italic")]
    x0, y0, W = 30, 84, 900
    o.append(rect(x0 + 2, y0 + 3, W, 112, fill="#e9eef4", rx=8))
    o.append(rect(x0, y0, W, 112, fill="#fff", stroke=ACC, sw=1.8, rx=8))
    parts = [("As a", "sales rep", PURPLE, "who wants it"),
             ("I want", "to see which of my accounts are at risk of not ordering again", ACC, "what they want"),
             ("so that", "I can call them before they go quiet", GREEN, "why it is worth building")]
    yy = y0 + 30
    for kw, body, c, note in parts:
        o.append(text(x0 + 18, yy, kw, 13, c, "bold", family=MONO))
        o.append(text(x0 + 92, yy, body, 13, INK))
        o.append(text(x0 + W - 16, yy, note, 11, MUTED, anchor="end", style="italic"))
        yy += 30
    o.append(text(x0 + 18, y0 + 104, "The \"so that\" clause is the one people drop, and the one that stops you building something correct and useless.",
                  11.5, MUTED, style="italic"))

    y1 = y0 + 132
    acs = [("AC-1", "Given I am a logged-in sales rep, when I open the at-risk list, then I see only accounts where I am the rep.", "scope", TEAL),
           ("AC-2", "Given an account whose last order was more than 1.5 times its own average gap, when the list is generated, then it appears.", "the actual rule, not the word \"recently\"", ACC),
           ("AC-3", "Given an account with no orders at all, when the list is generated, then it does not appear.", "the edge case", ORANGE),
           ("AC-4", "Given the list is open, when I sort by value at risk, then accounts order by last twelve months' revenue, highest first.", "behavior the user can check", GREEN)]
    for i, (tag, body, note, c) in enumerate(acs):
        y = y1 + i * 62
        o.append(rect(x0 + 2, y + 3, W, 52, fill="#e9eef4", rx=7))
        o.append(rect(x0, y, W, 52, fill="#fff", stroke=RULE, sw=1.2, rx=7))
        o.append(rect(x0, y, 74, 52, fill=c, rx=7))
        o.append(rect(x0 + 64, y, 10, 52, fill=c))
        o.append(text(x0 + 16, y + 31, tag, 12.5, "#fff", "bold", family=MONO))
        o.append(text(x0 + 88, y + 22, body, 11.5, INK))
        o.append(text(x0 + 88, y + 41, note, 11, c, style="italic"))
    return svg(x0 * 2 + W, y1 + 4 * 62 + 16, "".join(o))


if __name__ == "__main__":
    for name, fn in [("fig25-1-sdlc-and-the-ba.svg", fig_sdlc),
                     ("fig25-2-order-to-cash-swimlane.svg", fig_swimlane),
                     ("fig25-3-four-data-products.svg", fig_four_products),
                     ("fig25-4-user-story-anatomy.svg", fig_story),
                     ("fig25-5-gap-analysis.svg", fig_gap)]:
        open(name, "w").write(fn())
    print("ok")
