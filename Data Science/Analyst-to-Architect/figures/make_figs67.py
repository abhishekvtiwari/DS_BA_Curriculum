# Diagrams for Chapter 67. Run from figures/: python3 make_figs67.py
# Every figure prints at the full text width (493.2 pt), so on a 660-px canvas a 10-px font prints
# at 10 x 493.2 / 660 = 7.5 pt. The smallest font used here is 10 px (visual standard: >= 7 pt).
from make_figs import *
GREEN = "#2f7d6d"; GOLD = "#b7791f"; RED = "#b23b3b"; BLUE2 = "#2f6690"; SOFT = "#eef2f7"; LIGHT = "#c9d3df"
W = 660
BODY = 10.4      # body text, px  (7.8 pt)
SMALL = 10.0     # smallest text, px (7.5 pt)


def arrow(x1, y1, x2, y2, c=MUTED, sw=1.6):
    import math
    a = math.atan2(y2 - y1, x2 - x1); s = 7
    p1 = (x2 - s * math.cos(a - 0.45), y2 - s * math.sin(a - 0.45))
    p2 = (x2 - s * math.cos(a + 0.45), y2 - s * math.sin(a + 0.45))
    return (path(f"M{x1},{y1} L{x2},{y2}", stroke=c, sw=sw)
            + f'<path d="M{x2},{y2} L{p1[0]:.1f},{p1[1]:.1f} L{p2[0]:.1f},{p2[1]:.1f} Z" fill="{c}"/>')


def box(x, y, w, title, c, lines, sub=None, step=14):
    """A card with a coloured header; returns (svg, height). An empty string in lines adds a half gap."""
    body_h = 12 + (20 if sub else 0) + sum(step if l else step * 0.5 for l in lines) + 6
    h = 26 + body_h
    o = [rect(x + 3, y + 4, w, h, fill=SOFT, rx=7), rect(x, y, w, h, fill="#fff", stroke=c, sw=1.6, rx=7),
         f'<path d="M{x},{y+8} a7,7 0 0 1 7,-7 H{x+w-7} a7,7 0 0 1 7,7 V{y+26} H{x} Z" fill="{c}"/>',
         text(x + w / 2, y + 18, title, 12, "#fff", "bold", anchor="middle", family=HEAD)]
    yy = y + 26 + 18
    if sub:
        o.append(text(x + w / 2, yy, sub, 11, c, "bold", anchor="middle")); yy += 20
    for l in lines:
        if l:
            o.append(text(x + w / 2, yy, l, BODY, INK, anchor="middle")); yy += step
        else:
            yy += step * 0.5
    return "".join(o), h


def f1():  # individual contribution -> leverage
    o = [text(12, 22, "The shift every architect eventually makes", 13, INK, "bold", family=HEAD)]
    bw = 262
    left, h = box(12, 40, bw, "Individual contribution", MUTED,
                  ["Impact: what you personally", "build, this week", "",
                   "Scales with your own hours", "",
                   "Skill: write the best query,", "the cleanest pipeline"])
    right, _ = box(W - 15 - bw, 40, bw, "Leverage", ACC,
                   ["Impact: the decisions you make", "and the people you enable", "",
                    "Scales with judgment and trust", "",
                    "Skill: make the right call, and", "get others to build it well"])
    o += [left, right]
    ym = 40 + h / 2
    o.append(arrow(12 + bw + 8, ym, W - 15 - bw - 6, ym, GOLD, 2.2))
    o.append(text(W / 2, ym - 10, "the shift", 11, GOLD, "bold", anchor="middle"))
    return svg(W, int(40 + h + 12), "".join(o))


def f2():  # first 90 days
    o = [text(6, 22, "A first-90-days plan for a new architect", 13, INK, "bold", family=HEAD)]
    phases = [("Weeks 1–4", "Listen", ACC,
               ["Read every design doc, ADR", "and postmortem that exists", "",
                "Ask every team lead: “What", "keeps you up at night?”", "",
                "Build nothing yet"]),
              ("Weeks 5–8", "Diagnose", GREEN,
               ["Draw the real C4 diagram", "(Ch 60), not the wiki’s", "",
                "Run a failure analysis (Ch 61)", "on the riskiest system", "",
                "Score maturity honestly (Ch 66)"]),
              ("Weeks 9–12", "Earn credibility", GOLD,
               ["Ship one small, visible fix,", "not a redesign", "",
                "Close one long-open risk, the", "way Ch 64 closed Ch 60’s", "access-control gap", "",
                "Write it up; let the work speak"])]
    bw, gap, x0 = 200, 24, 6
    hs = []
    for i, (wk, name, c, lines) in enumerate(phases):
        x = x0 + i * (bw + gap)
        s, h = box(x, 40, bw, wk, c, lines, sub=name, step=13.5)
        o.append(s); hs.append(h)
    for i in range(2):
        x = x0 + i * (bw + gap) + bw + 4
        o.append(arrow(x, 100, x + gap - 7, 100))
    return svg(W, int(40 + max(hs) + 12), "".join(o))


def f3():  # the arc of the book
    o = [text(6, 22, "The arc of this book, in one line", 13, INK, "bold", family=HEAD)]
    stops = [("Parts 0–1", "Ch 1–9", ["What data is,", "and where it", "can take you"], MUTED),
             ("Part 2", "Ch 10–27", ["One query (Ch 12)", "to one trusted", "automation (Ch 20)"], ACC),
             ("Parts 3–4", "Ch 28–44", ["Engineering", "discipline", "and models"], GREEN),
             ("Parts 5–6", "Ch 45–59", ["Pipelines and AI", "in production"], BLUE2),
             ("Part 7", "Ch 60–66", ["A platform designed,", "governed, secured", "and costed"], GOLD),
             ("Part 7", "Ch 67", ["Led, and someone", "else’s turn to", "learn from you"], RED)]
    col = 108; x0 = 60; yr = 84
    o.append(path(f"M{x0},{yr} H{x0 + 5 * col}", stroke=LIGHT, sw=2))
    for i, (part, ch, lines, c) in enumerate(stops):
        x = x0 + i * col
        o.append(text(x, 50, part, SMALL, MUTED, "bold", anchor="middle"))
        o.append(text(x, 64, ch, 10.6, c, "bold", anchor="middle"))
        o.append(f'<circle cx="{x}" cy="{yr}" r="7" fill="{c}"/>')
        for j, l in enumerate(lines):
            o.append(text(x, yr + 24 + j * 13, l, SMALL, INK, anchor="middle"))
    return svg(W, yr + 24 + 2 * 13 + 12, "".join(o))


if __name__ == "__main__":
    for n, f in [("fig67-1-leverage-shift.svg", f1), ("fig67-2-first-90-days.svg", f2),
                 ("fig67-3-book-arc.svg", f3)]:
        open(n, "w").write(f())
    print("ok")
