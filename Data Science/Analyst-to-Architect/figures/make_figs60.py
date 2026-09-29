# Diagrams for Chapter 60. Run: python3 make_figs60.py
# Every figure prints at the full text width (493.2 pt). All canvases are 680 px wide, so
# 1 px = 0.725 pt: the smallest text here, 10.5 px, prints at 7.6 pt (visual standard: 7 pt or more).
# Text is wrapped by measuring it with the DejaVu Sans metrics the PDF uses, so no label can
# run past its box.
import math, os
from PIL import ImageFont
from make_figs import *

GREEN = "#2f7d6d"; PURPLE = "#7a4fa0"; GOLD = "#b7791f"; RED = "#b23b3b"; BLUE2 = "#2f6690"
GREY = "#8a93a3"; GREYBG = "#f1f3f6"; SOFT = "#eef2f7"
W = 680

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

def arrow(x1, y1, x2, y2, c=MUTED, sw=1.5, dash=None):
    a = math.atan2(y2 - y1, x2 - x1); s = 7
    p1 = (x2 - s * math.cos(a - 0.45), y2 - s * math.sin(a - 0.45))
    p2 = (x2 - s * math.cos(a + 0.45), y2 - s * math.sin(a + 0.45))
    return (path(f"M{x1},{y1} L{x2},{y2}", stroke=c, sw=sw, dash=dash)
            + f'<path d="M{x2},{y2} L{p1[0]:.1f},{p1[1]:.1f} L{p2[0]:.1f},{p2[1]:.1f} Z" fill="{c}"/>')

def step(x, y, n, c=INK):
    """A numbered circle that ties an arrow to a step of the section 60.5 trace."""
    return (f'<circle cx="{x}" cy="{y}" r="8.5" fill="{c}" stroke="#fff" stroke-width="1.5"/>'
            + text(x, y + 3.8, str(n), 10.5, "#fff", "bold", anchor="middle"))

def lines_at(x, y, lines, size, fill=INK, weight="normal", anchor="start", lead=None):
    lead = lead or size * 1.32
    return "".join(text(x, y + i * lead, l, size, fill, weight, anchor=anchor) for i, l in enumerate(lines))

def ext_system(x, y, w, h, lines_):
    """Another system, outside the platform: a grey box with a bold name."""
    for l in lines_:
        assert width(l, 10.5, True) <= w - 8, l
    o = [rect(x, y, w, h, fill=GREYBG, stroke=GREY, sw=1.3, rx=6)]
    o.append(lines_at(x + w / 2, y + h / 2 - (len(lines_) - 1) * 6.5 + 4, lines_, 10.5, INK, "bold", anchor="middle", lead=13))
    return "".join(o)

def person(cx, top, lines_):
    """A person or group: an icon, with the name below it (never on top of it)."""
    o = [f'<circle cx="{cx}" cy="{top+11}" r="10" fill="{MUTED}"/>',
         rect(cx - 16, top + 23, 32, 22, fill=MUTED, rx=7)]
    o.append(lines_at(cx, top + 59, lines_, 10.5, INK, "bold", anchor="middle", lead=13))
    return "".join(o)


# ---------- Figure 60.1: the four C4 zoom levels ----------
def f1():
    o = [text(12, 24, "The C4 model: the same system at four levels of zoom", 13, INK, "bold", family=HEAD)]
    levels = [("Level 1: Context", "The system as one box, among the people and other systems around it", ACC),
              ("Level 2: Container", "The system opened up: its major deployable pieces (app, database, pipeline)", GREEN),
              ("Level 3: Component", "One container opened up: the modules inside it and how they call each other", GOLD),
              ("Level 4: Code", "One component's actual classes or functions; rarely drawn by hand", PURPLE)]
    cw, gap, x0, y0 = 150, 14, 12, 40
    bodies = [wrap(sub, 10.5, cw - 18) for _, sub, _ in levels]
    ch = 34 + max(len(b) for b in bodies) * 14 + 8
    for i, ((title, _, c), body) in enumerate(zip(levels, bodies)):
        x = x0 + i * (cw + gap)
        assert width(title, 11, True) <= cw - 10, title
        o.append(rect(x, y0, cw, ch, fill="#fff", stroke=c, sw=1.6, rx=8))
        o.append(f'<path d="M{x},{y0+8} a8,8 0 0 1 8,-8 H{x+cw-8} a8,8 0 0 1 8,8 V{y0+24} H{x} Z" fill="{c}"/>')
        o.append(text(x + cw / 2, y0 + 16.5, title, 11, "#fff", "bold", anchor="middle"))
        o.append(lines_at(x + 9, y0 + 42, body, 10.5, INK, lead=14))
        if i < 3:
            o.append(arrow(x + cw + 2, y0 + ch / 2, x + cw + gap - 1, y0 + ch / 2))
    note = ("Zoom in one level at a time. A context diagram with component detail crammed in helps nobody, "
            "and a component diagram of the whole company is unreadable. Pick the level the conversation needs, and stop there.")
    y = y0 + ch + 22
    nl = wrap(note, 10.5, W - 24)
    o.append(lines_at(12, y, nl, 10.5, MUTED, lead=14))
    return svg(W, y + (len(nl) - 1) * 14 + 10, "".join(o))


# ---------- Figure 60.2: context diagram ----------
def f2():
    o = [text(12, 24, "Context diagram: the Riverstone Analytics & AI Platform (level 1)", 13, INK, "bold", family=HEAD)]
    # the one system in the middle
    px, py, pw, ph = 250, 170, 180, 96
    o.append(rect(px + 3, py + 4, pw, ph, fill=SOFT, rx=9))
    o.append(rect(px, py, pw, ph, fill="#fff", stroke=ACC, sw=2, rx=9))
    o.append(f'<path d="M{px},{py+9} a9,9 0 0 1 9,-9 H{px+pw-9} a9,9 0 0 1 9,9 V{py+36} H{px} Z" fill="{ACC}"/>')
    o.append(lines_at(px + pw / 2, py + 15, ["Riverstone Analytics", "& AI Platform"], 11, "#fff", "bold", anchor="middle", lead=13))
    o.append(lines_at(px + pw / 2, py + 54, wrap("Turns orders, sensor readings and documents into reports, alerts and actions", 10.5, pw - 20),
                      10.5, INK, anchor="middle", lead=13))
    # people (icon above, name below) and other systems (grey boxes)
    o.append(person(70, 44, ["Branch", "managers"]))
    o.append(person(610, 44, ["Customers"]))
    o.append(person(70, 318, ["Sales and", "ops staff"]))
    o.append(person(610, 318, ["Data and", "analytics team"]))
    o.append(ext_system(280, 44, 120, 46, ["ERP", "(order records)"]))
    o.append(ext_system(280, 350, 120, 46, ["CRM"]))
    o.append(ext_system(12, 190, 112, 58, ["Plant sensors;", "Taloja line", "camera"]))
    o.append(ext_system(556, 196, 112, 46, ["Email inbox"]))
    # arrows: every one crosses the platform's edge
    o.append(arrow(318, 90, 318, py - 2, GOLD)); o.append(text(312, 134, "orders", 10.5, GOLD, anchor="end"))
    o.append(arrow(362, py, 362, 92, GOLD)); o.append(lines_at(368, 126, ["confirmed", "PO orders"], 10.5, GOLD, lead=12.5))
    o.append(arrow(318, 350, 318, py + ph + 2, GOLD)); o.append(lines_at(312, 304, ["leads,", "segments"], 10.5, GOLD, anchor="end", lead=12.5))
    o.append(arrow(362, py + ph, 362, 348, GOLD)); o.append(lines_at(368, 304, ["lead scores,", "follow-up flags"], 10.5, GOLD, lead=12.5))
    o.append(arrow(124, 219, px - 2, 219, GOLD)); o.append(text(130, 210, "readings, images", 10.5, GOLD))
    o.append(arrow(556, 219, px + pw + 2, 219, GOLD)); o.append(lines_at(438, 198, ["PO and support", "emails"], 10.5, GOLD, lead=12.5))
    o.append(arrow(px + 10, py - 2, 104, 104, MUTED)); o.append(lines_at(150, 92, ["dashboards,", "Daily Sales Flash"], 10.5, MUTED, lead=12.5))
    o.append(arrow(px + pw - 10, py - 2, 578, 104, MUTED)); o.append(lines_at(446, 96, ["answers to", "questions"], 10.5, MUTED, lead=12.5))
    o.append(arrow(px + 10, py + ph + 2, 104, 326, MUTED)); o.append(lines_at(160, 326, ["drafts to", "confirm, flags"], 10.5, MUTED, lead=12.5))
    o.append(arrow(578, 326, px + pw - 10, py + ph + 2, MUTED, dash="4 3")); o.append(lines_at(500, 272, ["builds and", "runs it"], 10.5, MUTED, lead=12.5))
    y = 428
    o += [f'<circle cx="20" cy="{y-4}" r="5" fill="{MUTED}"/>', text(32, y, "a person or group", 10.5, MUTED),
          rect(160, y - 11, 18, 13, fill=GREYBG, stroke=GREY, sw=1.2, rx=3), text(184, y, "another system, outside the platform", 10.5, MUTED)]
    note = "One box in the middle, and every arrow crosses its edge. Nobody here asks which orchestrator runs inside: that question belongs one level down."
    nl = wrap(note, 10.5, W - 24)
    o.append(lines_at(12, y + 22, nl, 10.5, MUTED, lead=14))
    return svg(W, y + 22 + (len(nl) - 1) * 14 + 10, "".join(o))


# ---------- Figure 60.3: container diagram, with the traced purchase order numbered ----------
def container(x, y, w, h, title, sub, c, kind):
    assert width(title, 10.5, True) + width(kind, 10.5) + 22 <= w, title
    o = [rect(x + 2, y + 3, w, h, fill=SOFT, rx=7), rect(x, y, w, h, fill="#fff", stroke=c, sw=1.6, rx=7),
         f'<path d="M{x},{y+7} a7,7 0 0 1 7,-7 H{x+w-7} a7,7 0 0 1 7,7 V{y+21} H{x} Z" fill="{c}"/>',
         text(x + 8, y + 15, title, 10.5, "#fff", "bold"),
         text(x + w - 8, y + 15, kind, 10.5, "#fff", anchor="end")]
    sub_lines = wrap(sub, 10.5, w - 16)
    assert 36 + (len(sub_lines) - 1) * 13.5 + 6 <= h, title
    o.append(lines_at(x + 8, y + 36, sub_lines, 10.5, INK, lead=13.5))
    return "".join(o)

def f3():
    o = [text(12, 24, "Container diagram: the platform box opened up (level 2)", 13, INK, "bold", family=HEAD)]
    LX, LW = 12, 96             # other systems, left
    C1, C2, CW = 134, 354, 196  # two columns of containers
    RX, RW = 572, 96            # other systems, right
    rows = [44, 138, 232, 326]
    CH = 64
    o.append(ext_system(LX, rows[0] + 9, LW, 46, ["Email inbox"]))
    o.append(ext_system(LX, rows[1] + 9, LW, 46, ["ERP"]))
    o.append(ext_system(LX, rows[2] + 6, LW, 52, ["Plant sensors;", "Taloja line", "camera"]))
    o.append(ext_system(RX, rows[0] + 6, RW, 52, ["Policy and", "product spec", "documents"]))
    o.append(ext_system(RX, rows[3] + 9, RW, 46, ["CRM"]))
    boxes = [(C1, rows[0], "PO-intake pipeline", "Drafts orders from emails; a person confirms each one", PURPLE, "AI"),
             (C2, rows[0], "Support assistant", "Answers from current policy and spec documents (RAG)", PURPLE, "AI"),
             (C1, rows[1], "Ingestion (Dagster)", "06:30 run: ERP orders, CRM leads, dispatch and sensor files", ACC, "data"),
             (C2, rows[1], "Warehouse", "Raw, staging and mart tables, plus the Delta sensor archive", BLUE2, "data"),
             (C1, rows[2], "Defect model service", "Scores each part's image from the line camera (FastAPI)", PURPLE, "AI"),
             (C2, rows[2], "Semantic layer", "dbt models: one definition of revenue, active customer", GREEN, "data"),
             (C1, rows[3], "BI and Flash", "Power BI dashboards; the Daily Sales Flash email", GOLD, "data"),
             (C2, rows[3], "Reverse-ETL syncs", "Lead scores, follow-up flags and segments to the CRM", ACC, "data")]
    for x, y, t, s, c, k in boxes:
        o.append(container(x, y, CW, CH, t, s, c, k))
    mid = lambda r: rows[r] + CH / 2
    # the traced purchase order (section 60.5), numbered to match its steps
    o.append(arrow(LX + LW, mid(0), C1 - 2, mid(0), INK, 1.8)); o.append(step(121, mid(0) - 12, 1))
    o.append(step(C1 + CW - 12, rows[0] + CH - 10, 2, PURPLE))
    o.append(arrow(C1 + 16, rows[0] + CH, LX + LW - 16, rows[1] + 9, INK, 1.8)); o.append(step(123, rows[0] + CH + 18, 3))
    o.append(arrow(LX + LW, mid(1) + 4, C1 - 2, mid(1) + 4, INK, 1.8)); o.append(step(121, mid(1) + 18, 4))
    o.append(arrow(C1 + CW, mid(1), C2 - 2, mid(1), INK, 1.8)); o.append(step(C1 + CW + 12, mid(1) - 12, 4))
    o.append(arrow(C2 + CW / 2, rows[1] + CH, C2 + CW / 2, rows[2] - 2, INK, 1.8)); o.append(step(C2 + CW / 2 + 14, rows[1] + CH + 15, 5))
    o.append(arrow(C2 + CW / 2, rows[2] + CH, C2 + CW / 2, rows[3] - 2, INK, 1.8)); o.append(step(C2 + CW / 2 + 14, rows[2] + CH + 15, 6))
    o.append(arrow(C2 + 14, rows[2] + CH, C1 + CW - 14, rows[3] - 2, INK, 1.8)); o.append(step(C2 - 4, rows[2] + CH + 20, 6))
    o.append(arrow(C2 + CW, mid(3), RX - 2, mid(3), INK, 1.8)); o.append(step(C2 + CW + 12, mid(3) - 12, 6))
    # other flows, not part of the trace
    o.append(arrow(LX + LW - 14, rows[2] + 9, C1 + 10, rows[1] + CH + 1, GREY, 1.4, dash="4 3"))
    o.append(arrow(LX + LW, mid(2) + 12, C1 - 2, mid(2) + 12, GREY, 1.4, dash="4 3"))
    o.append(arrow(RX, mid(0), C2 + CW + 2, mid(0), GREY, 1.4, dash="4 3"))
    # shared services band
    y = rows[3] + CH + 18
    o.append(rect(12, y, W - 24, 42, fill="#fff", stroke=RULE, rx=6))
    o.append(text(24, y + 17, "Shared services, used by every container: credential vault, run logs, alerting, monitoring", 10.5, INK, "bold"))
    o.append(text(24, y + 33, "Drawn once here instead of eight times on the diagram.", 10.5, MUTED))
    y += 64
    o += [step(20, y - 4, 1), text(34, y, "the traced purchase order, step by step (section 60.5)", 10.5, MUTED),
          path(f"M372,{y-4} L404,{y-4}", stroke=GREY, sw=1.4, dash="4 3"), text(410, y, "other flows", 10.5, MUTED),
          rect(500, y - 11, 18, 13, fill=GREYBG, stroke=GREY, sw=1.2, rx=3), text(524, y, "outside systems", 10.5, MUTED)]
    return svg(W, y + 10, "".join(o))


# ---------- Figure 60.4: turning a vague requirement into a number ----------
def f4():
    o = [text(12, 24, "Turning a vague requirement into a number", 13, INK, "bold", family=HEAD)]
    pairs = [("“Make it fast”", "The Daily Sales Flash is sent by 07:30 IST on working days, p95 over the month (the time that 95% of the month's Flashes beat).", ACC),
             ("“Make it reliable”", "At most 2 pipeline runs a year need a person to step in; counted each month from Dagster's run history.", GREEN),
             ("“Make it secure”", "No analyst's login can read another branch's customer data; access reviewed every quarter.", RED),
             ("“Make it scale”", "At 5 times today's order volume (test data), the 06:30 run still finishes by 07:15 and the sales dashboard's first view loads in under 3 seconds, p95.", GOLD),
             ("“Keep it cheap”", "Platform cost stays under ₹0.50 per 1,000 order lines processed; reviewed every month.", PURPLE)]
    y = 40
    for vague, precise, c in pairs:
        pl = wrap(precise, 10.5, 424)
        h = max(40, 18 + len(pl) * 14)
        o.append(rect(12, y, 158, h, fill="#fff", stroke=RULE, rx=6))
        o.append(text(24, y + h / 2 + 4, vague, 11, MUTED, style="italic"))
        o.append(arrow(176, y + h / 2, 204, y + h / 2, c, 1.8))
        o.append(rect(212, y, 456, h, fill="#fff", stroke=c, sw=1.5, rx=6)); o.append(rect(212, y, 6, h, fill=c))
        o.append(lines_at(230, y + h / 2 - (len(pl) - 1) * 7 + 4, pl, 10.5, INK, lead=14))
        y += h + 10
    return svg(W, y, "".join(o))


# ---------- Figure 60.5: an ADR, filled in ----------
def f5():
    o = [text(12, 24, "An architecture decision record, filled in", 13, INK, "bold", family=HEAD)]
    rows = [("ADR-014", "Table format for the sensor archive"),
            ("Status and date", "Accepted, the week after the M-07 correction failed (Chapter 49's story)."),
            ("Context", "The sensor archive adds 216,000 readings a day (25 machines at two plants, one reading every 10 seconds); three months is 19.87 million. A job rewriting six weeks of machine M-07's readings failed partway under plain Parquet files, leaving the archive partly corrected (11 days fixed, 8 missing, 23 uncorrected). Recovery took two days."),
            ("Decision", "Store the sensor archive as a Delta Lake table (the deltalake Python package), not as plain Parquet files."),
            ("Alternatives considered", ["(1) Plain Parquet, versioned by folder name: rejected, because it is exactly what failed.",
                                         "(2) Apache Iceberg (PyIceberg): comparable guarantees; rejected because it needs a catalog to track each table, while deltalake needs nothing extra, and our readers (DuckDB, Spark) already read Delta.",
                                         "(3) An ordinary warehouse table: rejected, because millions of rows a month, read mostly in bulk, are far cheaper as files in object storage (Chapter 49, section 49.8)."]),
            ("Consequences", "Atomic overwrites and time travel (Chapter 49); one more format for the team to operate; the deltalake package must be pinned and retested on every upgrade."),
            ("Owner and revisit", "Data platform team. Revisit if the company standardizes on Iceberg.")]
    y = 40
    body = []
    yy = y + 20
    for label, val in rows:
        first = label == "ADR-014"
        paras = val if isinstance(val, list) else [val]
        vl = [val] if first else [l for p in paras for l in wrap(p, 10.5, W - 24 - 172)]
        body.append(text(26, yy, label, 11 if first else 10.5, ACC if first else MUTED, "bold"))
        body.append(lines_at(180, yy, vl, 11 if first else 10.5, INK, "bold" if first else "normal", lead=14))
        yy += (len(vl) - 1) * 14 + 22
    o.append(rect(12, y, W - 24, yy - y - 6, fill="#fff", stroke=RULE, sw=1.4, rx=8))
    o.extend(body)
    return svg(W, yy + 2, "".join(o))


if __name__ == "__main__":
    here = os.path.dirname(os.path.abspath(__file__))
    for n, f in [("fig60-1-c4-levels.svg", f1), ("fig60-2-context-diagram.svg", f2),
                 ("fig60-3-container-diagram.svg", f3), ("fig60-4-nfr-precision.svg", f4),
                 ("fig60-5-adr-example.svg", f5)]:
        open(os.path.join(here, n), "w").write(f())
    print("ok")
