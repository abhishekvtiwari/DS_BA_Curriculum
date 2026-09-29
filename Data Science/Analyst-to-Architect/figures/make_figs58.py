# Generates the SVG figures for Chapter 58. Run: python3 make_figs58.py
# Every number shown was printed by the chapter's own code (companion/ch58): section 58.4's run
# (53 loaded, 6 awaiting approval, 1 held), section 58.7's two rates and cost table, and section 58.8's
# accuracy by email style.
# Canvas 720 px wide, printed at 493.2 pt: 10.5 px text prints at 7.2 pt, so no text is smaller than 10.5.
# Colours: blue for right or safe, orange for wrong or risky, never red against green; every coloured
# mark also carries a word, and the "wrong" bars are hatched.
from make_figs import *
ORANGE = "#c0662b"; ORANGEBG = "#fbeee4"; BLUEBG = "#e6f0f7"; PURPLE = "#7a4fa0"
W = 720


def arrow_h(x1, y, x2, c=INK):
    return path(f"M{x1},{y} H{x2 - 2}", stroke=c, sw=1.8) + path(f"M{x2 - 7},{y - 4.5} L{x2},{y} L{x2 - 7},{y + 4.5}", stroke=c, sw=1.8)


def arrow_v(x, y1, y2, c=INK, dash=None):
    return path(f"M{x},{y1} V{y2 - 2}", stroke=c, sw=1.8, dash=dash) + path(f"M{x - 4.5},{y2 - 7} L{x},{y2} L{x + 4.5},{y2 - 7}", stroke=c, sw=1.8)


def fig_pipeline():
    o = [text(20, 26, "Riverstone's purchase-order intake, end to end", 14, INK, "bold", family=HEAD),
         text(20, 44, "One run over the 60 practice emails (section 58.4)", 11, MUTED)]
    boxes = [("email", "20 to 40 a day,", "five shapes", INK), ("extract", "pinned model,", "prompt v3", ACC),
             ("parse", "comments out,", "dates fixed", ACC), ("validate", "PO, codes,", "dates, quantities", PURPLE),
             ("decide", "valid? over", "the limit?", ORANGE), ("write", "keys, one", "transaction, audit", INK)]
    bw, gap, x0, y0 = 104, 12, 20, 60
    centres = []
    for i, (title, d1, d2, c) in enumerate(boxes):
        x = x0 + i * (bw + gap)
        centres.append(x + bw / 2)
        o.append(rect(x, y0, bw, 70, fill="#fff", stroke=c, sw=1.8, rx=7))
        o.append(text(x + bw / 2, y0 + 22, title, 12.5, c, "bold", anchor="middle"))
        o.append(text(x + bw / 2, y0 + 42, d1, 10.5, INK, anchor="middle"))
        o.append(text(x + bw / 2, y0 + 57, d2, 10.5, INK, anchor="middle"))
        if i < len(boxes) - 1:
            o.append(arrow_h(x + bw, y0 + 35, x + bw + gap))
    y1 = y0 + 70
    # validate -> held for review (nothing is written): down, then left, then down
    hx, ax, lx = 250, 428, 600                         # left edges of the three outcome boxes
    o.append(path(f"M{centres[3]},{y1} V150 H{hx + 80}", stroke=PURPLE, sw=1.8, dash="5,4"))
    o.append(arrow_v(hx + 80, 150, 176, PURPLE, dash="5,4"))
    o.append(text(centres[3] - 6, 146, "fails", 10.5, PURPLE, "bold", anchor="end"))
    o.append(rect(hx, 176, 160, 46, fill="#f3eef8", stroke=PURPLE, sw=1.6, rx=7))
    o.append(text(hx + 80, 195, "held for review: 1", 12, PURPLE, "bold", anchor="middle"))
    o.append(text(hx + 80, 212, "no items; nothing written", 10.5, INK, anchor="middle"))
    # write -> two outcomes, with the status decide chose
    wx = centres[5]
    o.append(path(f"M{wx},{y1} V158 H{ax + 80}", stroke=INK, sw=1.8))
    o.append(arrow_v(ax + 80, 158, 176, ORANGE))
    o.append(arrow_v(lx + 50, 158, 176, ACC))
    o.append(rect(ax, 176, 160, 46, fill=ORANGEBG, stroke=ORANGE, sw=1.6, rx=7))
    o.append(text(ax + 80, 195, "awaiting approval: 6", 12, ORANGE, "bold", anchor="middle"))
    o.append(text(ax + 80, 212, "written; over ₹1,00,000", 10.5, INK, anchor="middle"))
    o.append(rect(lx, 176, 100, 46, fill=BLUEBG, stroke=ACC, sw=1.6, rx=7))
    o.append(text(lx + 50, 195, "loaded: 53", 12, ACC, "bold", anchor="middle"))
    o.append(text(lx + 50, 212, "88% of emails", 10.5, INK, anchor="middle"))
    o.append(rect(20, 240, W - 40, 50, fill=ROWALT, stroke=RULE, rx=7))
    o.append(text(34, 260, "The write is the part that is different: two UNIQUE keys, one transaction for an order's", 11, INK))
    o.append(text(34, 278, "header and lines, and an audit row naming the run. Replaying the morning wrote nothing twice.", 11, INK, "bold"))
    return svg(W, 304, "".join(o))


def fig_two_rates():
    o = [text(20, 26, "The same system, described two ways", 14, INK, "bold", family=HEAD)]
    for x, bg, c, head, big, label, l1, l2 in [
            (20, BLUEBG, ACC, "what the business case says", "88%", "straight-through rate",
             "53 of 60 emails loaded", "without anyone touching them"),
            (370, ORANGEBG, ORANGE, "what the ground truth says", "19%", "silent error rate",
             "10 of those 53 orders are wrong:", "a quantity or a missing line")]:
        o.append(rect(x, 42, 330, 150, fill=bg, stroke=c, sw=1.8, rx=8))
        o.append(text(x + 165, 66, head, 12, c, "bold", anchor="middle"))
        o.append(text(x + 165, 108, big, 32, c, "bold", anchor="middle"))
        o.append(text(x + 165, 132, label, 12, INK, anchor="middle"))
        o.append(text(x + 165, 156, l1, 11, INK, anchor="middle"))
        o.append(text(x + 165, 174, l2, 11, INK, anchor="middle"))
    y = 220
    o.append(text(20, y, "Cost per day at 40 emails, counting labour AND the cost of being wrong", 12, INK, "bold"))
    cols = [(262, "minutes"), (352, "labour ₹"), (452, "errors/day"), (572, "error cost ₹"), (690, "total ₹/day")]
    for x, label in cols:
        o.append(text(x, y + 22, label, 10.5, MUTED, "bold", anchor="end"))
    y += 32
    rows = [("manual (today)", "120", "600", "0.00", "0", "600", MUTED),
            ("assisted: review each", "39", "197", "0.67", "1,333", "1,530", ACC),
            ("straight through", "9", "47", "6.67", "13,333", "13,380", ORANGE)]
    for label, *values, c in rows:
        o.append(rect(20, y, W - 40, 30, fill="#fff", stroke=c, sw=1.5, rx=6))
        o.append(text(32, y + 20, label, 11.5, c, "bold"))
        for (x, _), v in zip(cols, values):
            last = x == cols[-1][0]
            o.append(text(x, y + 20, v, 12 if last else 11.5, c if last else INK, "bold" if last else "normal", anchor="end"))
        y += 36
    o.append(text(20, y + 14, "Straight through saves the most labour and costs the most money. Assisted costs more than", 11, INK))
    o.append(text(20, y + 31, "typing on paper, because a reviewer misses 1 wrong draft in 10: it wins only if review catches", 11, INK))
    o.append(text(20, y + 48, "over 97%, or if typing itself gets more than 1.2% of orders wrong. Measure both in shadow mode.", 11, INK, "bold"))
    return svg(W, y + 62, "".join(o))


def fig_segments():
    hatch = ('<defs><pattern id="hatch58" width="7" height="7" patternUnits="userSpaceOnUse" '
             'patternTransform="rotate(45)"><rect width="7" height="7" fill="' + ORANGE + '"/>'
             '<line x1="0" y1="0" x2="0" y2="7" stroke="#fff" stroke-width="2.5"/></pattern></defs>')
    o = [hatch, text(20, 26, "Accuracy by email style: automate the segment you are excellent at", 14, INK, "bold", family=HEAD)]
    o.append(rect(20, 38, 14, 12, fill=ACC, stroke=ACC, rx=2)); o.append(text(40, 48, "correct", 11, INK))
    o.append(rect(110, 38, 14, 12, fill="url(#hatch58)", stroke=ORANGE, rx=2)); o.append(text(130, 48, "wrong (hatched)", 11, INK))
    rows = [("bulleted", 13, 0), ("forwarded", 14, 0), ("terse", 10, 0), ("table", 7, 4), ("prose", 3, 8)]
    y, x0, unit = 64, 100, 22
    for name, right, wrong in rows:
        o.append(text(x0 - 10, y + 17, name, 12, INK, "bold", anchor="end"))
        o.append(rect(x0, y, unit * right, 26, fill=ACC, stroke=ACC, rx=3))
        if wrong:
            o.append(rect(x0 + unit * right, y, unit * wrong, 26, fill="url(#hatch58)", stroke=ORANGE, rx=3))
        o.append(text(x0 + unit * 14 + 12, y + 17, f"{right} correct, {wrong} wrong", 11.5, INK))
        o.append(text(W - 20, y + 17, "candidate" if not wrong else "review", 11.5, ACC if not wrong else ORANGE, "bold", anchor="end"))
        y += 36
    o.append(rect(20, y + 6, W - 40, 50, fill=BLUEBG, stroke=ACC, rx=7))
    o.append(text(W / 2, y + 26, "37 of 37 correct across three styles: 62% of the volume", 12, ACC, "bold", anchor="middle"))
    o.append(text(W / 2, y + 44, "0 errors so far, but with 37 cases the true rate could be up to about 8% (rule of three)", 11, INK, anchor="middle"))
    o.append(text(20, y + 78, "Prose is hard, as expected. Tables are the second worst, because several items on one row are", 11, INK))
    o.append(text(20, y + 95, "exactly what the extraction misses. You find the segment by measuring it, not by guessing.", 11, INK))
    return svg(W, y + 108, "".join(o))


if __name__ == "__main__":
    for name, fn in [("fig58-1-intake-pipeline.svg", fig_pipeline), ("fig58-2-two-rates.svg", fig_two_rates),
                     ("fig58-3-segments.svg", fig_segments)]:
        open(name, "w").write(fn())
    print("ok58")
