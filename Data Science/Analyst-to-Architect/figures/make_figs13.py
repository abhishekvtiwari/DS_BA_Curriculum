# Generates the SVG figures for Chapter 13. Run from this folder: python3 make_figs13.py
# Every figure prints at the full text width (174 mm = 493.2 pt), so a font of s px on a W px canvas
# prints at s * 493.2 / W pt. The canvases here are 720 px wide: 10.5 px prints at 7.2 pt, the smallest
# size used. check_sizes() refuses to write a figure with any text under 7 pt.
import re
from make_figs import *

W = 720
PRINT_PT = 493.2

def check_sizes(name, s):
    w = float(re.search(r'viewBox="0 0 ([\d.]+)', s).group(1))
    small = [float(x) for x in re.findall(r'font-size="([\d.]+)"', s) if float(x) * PRINT_PT / w < 7.0]
    assert not small, f'{name}: text under 7 pt ({min(small)} px on {w} px)'
    return s

def table(x, y, title, headers, rows, widths, color=ACC, rowfill=None, subtitle=None, fs=11, rh=22,
          right=()):
    """A small result table. Columns listed in `right` are right-aligned (numbers)."""
    o = []
    if subtitle:
        o += [text(x, y - 24, title, 12.5, INK, "bold", family=HEAD), text(x, y - 8, subtitle, 10.5, MUTED, style="italic")]
    elif title:
        o.append(text(x, y - 8, title, 12.5, INK, "bold", family=HEAD))
    tw = sum(widths)
    o.append(rect(x, y, tw, rh, fill=color, rx=3))
    cx = x
    for j, (h_, wd) in enumerate(zip(headers, widths)):
        if j in right:
            o.append(text(cx + wd - 7, y + rh - 7, h_, fs, "#fff", "bold", anchor="end", family=MONO))
        else:
            o.append(text(cx + 7, y + rh - 7, h_, fs, "#fff", "bold", family=MONO))
        cx += wd
    yy = y + rh
    for i, r in enumerate(rows):
        f = rowfill[i] if rowfill and rowfill[i] else "#fff"
        o.append(rect(x, yy, tw, rh, fill=f, stroke=RULE, sw=0.8))
        cx = x
        for j, (v, wd) in enumerate(zip(r, widths)):
            if j in right:
                o.append(text(cx + wd - 7, yy + rh - 7, v, fs, INK, anchor="end", family=MONO))
            else:
                o.append(text(cx + 7, yy + rh - 7, v, fs, INK, family=MONO))
            cx += wd
        yy += rh
    o.append(rect(x, y, tw, yy - y, stroke=RULE, sw=1, rx=3))   # closed outer border
    return "".join(o), yy

def fig_group_vs_window():
    o = []
    rows = [["Metro Mart", "5006", "14,640"], ["Metro Mart", "5012", "26,220"], ["Sharma Hardware", "5001", "14,700"],
            ["Sharma Hardware", "5005", "14,550"], ["Sharma Hardware", "5011", "11,700"]]
    total = {"Metro Mart": "40,860", "Sharma Hardware": "40,950"}
    t, y1 = table(20, 46, "order_totals (5 rows)", ["customer", "order_id", "order_revenue"], rows, [124, 76, 106],
                  right=(2,)); o.append(t)
    t, y2 = table(380, 60, "GROUP BY customer", ["customer", "total"],
                  [["Metro Mart", "40,860"], ["Sharma Hardware", "40,950"]], [124, 80], color="#7a4fa0",
                  subtitle="2 rows: the orders are collapsed", right=(1,)); o.append(t)
    o.append(text(380, y2 + 20, "SUM(order_revenue) … GROUP BY customer", 10.5, MUTED, family=MONO))
    t, y3 = table(20, 250, "SUM(…) OVER (PARTITION BY customer)", ["customer", "order_id", "order_revenue", "customer_total"],
                  [r + [total[r[0]]] for r in rows], [124, 76, 106, 112], color="#2f7d6d",
                  subtitle="5 rows: every order kept, its customer's total added alongside", right=(2, 3)); o.append(t)
    bx, by = 460, 250
    o.append(rect(bx, by, 240, 132, fill="#f6f9fc", stroke=RULE, rx=6))
    for i, (l, wt) in enumerate([("GROUP BY answers: what is", "normal"), ("each customer's total?", "normal"),
                                 ("A window answers: what is", "normal"), ("each order, and how big is it", "normal"),
                                 ("next to its customer's total?", "normal")]):
        o.append(text(bx + 12, by + 24 + i * 19, l, 11, INK, wt))
    o.append(text(bx + 12, by + 24 + 5 * 19 + 4, "Windows add, without losing rows.", 11, INK, "bold"))
    return svg(W, max(y3, by + 132) + 16, "".join(o))

def fig_anatomy():
    o = []
    # (indent in characters, code, colour, label lines); SVG collapses leading spaces, so indent by x
    code = [(0, "AVG(revenue) OVER (", "#0f5c8c", ["1  What to calculate (always required)"]),
            (4, "PARTITION BY category", "#7a4fa0", ["2  Restart for each group (optional)"]),
            (4, "ORDER BY month", "#c0662b", ["3  The order of rows in each group: needed by",
                                              "    RANK, LAG and LEAD; optional for SUM and AVG"]),
            (4, "ROWS BETWEEN 2 PRECEDING AND CURRENT ROW", "#2f7d6d", ["4  Which rows count: the frame (optional)"]),
            (0, ")", "#0f5c8c", [])]
    cw = 11.5 * 0.602                      # DejaVu Sans Mono advance per character
    y = 36
    rows = []
    for ind, c, col, labs in code:
        rows.append((y, ind, c, col, labs))
        y += 22 + 16 * (len(labs) - 1 if labs else 0)
    box_h = y - 14 - 6
    o.append(rect(20, 14, 680, box_h, fill="#f6f9fc", stroke=RULE, rx=6))
    for y, ind, c, col, labs in rows:
        o.append(text(34 + ind * cw, y, c, 11.5, col, "bold", family=MONO))
        for k, lab in enumerate(labs):
            o.append(text(356 + (0 if k == 0 else 21), y + k * 16, lab.strip(), 11, col,
                          "bold" if k == 0 else "normal"))
    top = 14 + box_h + 28
    o.append(text(20, top, "The frame slides down the rows. For April, the 3-month window is February, March and April:", 11.5, INK, "bold"))
    months = [("Jan", "2,02,640"), ("Feb", "2,53,664"), ("Mar", "2,78,008"), ("Apr", "2,10,282"), ("May", "3,29,359"), ("Jun", "1,86,928")]
    labels = {1: "◄ 2 PRECEDING", 2: "◄ 1 PRECEDING", 3: "◄ CURRENT ROW"}
    bx, by, rh = 20, top + 12, 24
    for i, (mn, v) in enumerate(months):
        infr = i in (1, 2, 3)
        o.append(rect(bx, by + i * rh, 220, rh - 2, fill="#e2f3ee" if infr else "#fff",
                      stroke="#2f7d6d" if infr else RULE, sw=1.8 if infr else 0.8, rx=3))
        wt = "bold" if i == 3 else "normal"
        o.append(text(bx + 10, by + i * rh + 16, mn + " 2025", 11.5, INK, wt, family=MONO))
        o.append(text(bx + 210, by + i * rh + 16, v, 11.5, INK, wt, anchor="end", family=MONO))
        if i in labels:
            o.append(text(bx + 230, by + i * rh + 16, labels[i], 11, "#2f7d6d", "bold" if i == 3 else "normal"))
    # bracket spanning the whole frame (Feb to Apr)
    x0, y0, y1 = 352, by + rh, by + 4 * rh - 2
    o.append(path(f"M{x0},{y0} h8 V{y1} h-8", stroke="#2f7d6d", sw=1.6))
    o.append(text(x0 + 14, (y0 + y1) / 2 + 4, "frame: 3 rows", 11, "#2f7d6d", "bold"))
    cx, cy = 470, by + 6
    o.append(rect(cx, cy, 230, 118, fill="#f6f9fc", stroke=RULE, rx=6))
    o.append(text(cx + 12, cy + 22, "moving_avg_3m for April", 11.5, INK, "bold"))
    o.append(text(cx + 12, cy + 44, "(2,53,664 + 2,78,008", 11, INK, family=MONO))
    o.append(text(cx + 19, cy + 62, "+ 2,10,282) ÷ 3", 11, INK, family=MONO))
    o.append(text(cx + 12, cy + 80, "= 2,47,318", 11, INK, "bold", family=MONO))
    o.append(text(cx + 12, cy + 104, "In May, the frame moves on.", 11, MUTED))
    return svg(W, by + 6 * rh + 12, "".join(o))

def fig_ranks():
    o = []
    rows = [["Water Bottle 1L", "230", "1", "1", "1"], ["Industrial Crate", "125", "2", "2", "2"],
            ["Food Container Set", "85", "3", "3", "3"], ["Storage Box 10L", "85", "4", "3", "3"],
            ["Storage Box 25L", "60", "5", "5", "4"], ["Garden Chair", "0", "6", "6", "5"]]
    fills = [None, None, "#fff4d6", "#fff4d6", None, None]
    t, yy = table(20, 40, "Units sold, ranked three ways", ["product_name", "units", "ROW_NUMBER", "RANK", "DENSE_RANK"],
                  rows, [138, 52, 90, 50, 90], rowfill=fills, right=(1, 2, 3, 4)); o.append(t)
    o.append(text(20, yy + 20, "Shaded rows: the tie (85 units each).", 11, MUTED, style="italic"))
    notes = [("ROW_NUMBER", "Always 1, 2, 3, 4… Ties get different", "numbers, so add a tie-breaker to", "ORDER BY (here: product_name)."),
             ("RANK", "Ties share a number, then it skips:", "3, 3, 5. Like a race: two joint", "third places, then fifth."),
             ("DENSE_RANK", "Ties share a number, no gaps:", "3, 3, 4. Use it for 'the top 3", "distinct sales levels'.")]
    for i, (h_, a, b, c) in enumerate(notes):
        y = 22 + i * 84
        o.append(rect(452, y, 250, 76, fill="#f6f9fc", stroke=RULE, rx=6))
        o.append(text(464, y + 18, h_, 11.5, ACC, "bold", family=MONO))
        for k, l in enumerate((a, b, c)):
            o.append(text(464, y + 36 + k * 16, l, 10.5, INK))
    return svg(W, 22 + 3 * 84 + 6, "".join(o))

def fig_islands():
    o = []
    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    active = {0: "24300", 2: "24301", 3: "24301", 4: "24301", 5: "24301", 7: "24302", 10: "24304"}
    colors = {"24300": "#7a4fa0", "24301": "#2f7d6d", "24302": "#c0662b", "24304": "#0f5c8c"}
    o.append(text(20, 24, "Patel Kitchenware's order months in 2025 (dashed: no order)", 12.5, INK, "bold", family=HEAD))
    for i, m in enumerate(months):
        x = 20 + i * 57
        if i in active:
            c = colors[active[i]]
            o.append(rect(x, 36, 52, 34, fill=c, rx=4, extra='fill-opacity="0.18"'))
            o.append(rect(x, 36, 52, 34, stroke=c, sw=2, rx=4))
            o.append(text(x + 26, 58, m, 11.5, c, "bold", anchor="middle"))
            o.append(text(x + 26, 86, active[i], 10.5, c, "bold", anchor="middle", family=MONO))
        else:
            o.append(rect(x, 36, 52, 34, fill="#fff", stroke=RULE, rx=4, extra='stroke-dasharray="4 3"'))
            o.append(text(x + 26, 58, m, 11.5, "#8a93a3", anchor="middle"))
    o.append(text(20, 116, "The trick: month_number − row_number stays the same while months are consecutive.", 11.5, INK, "bold"))
    rows = [["Jan", "24301", "1", "24300"], ["Mar", "24303", "2", "24301"], ["Apr", "24304", "3", "24301"],
            ["May", "24305", "4", "24301"], ["Jun", "24306", "5", "24301"], ["Aug", "24308", "6", "24302"],
            ["Nov", "24311", "7", "24304"]]
    fills = ["#efe7f6", "#e2f3ee", "#e2f3ee", "#e2f3ee", "#e2f3ee", "#f8e8dc", "#e3eef7"]
    t, yy = table(20, 132, "", ["month", "month_number", "row_number", "island_id"], rows, [60, 110, 100, 90],
                  rowfill=fills, right=(1, 2, 3)); o.append(t)
    bx, by = 400, 132
    o.append(rect(bx, by, 300, 150, fill="#f6f9fc", stroke=RULE, rx=6))
    lines = [("Each consecutive run shares", INK, "normal"), ("one island_id. Group by it:", INK, "normal"),
             ("Mar–Jun → 4 months in a row", "#2f7d6d", "bold"), ("(island 24301, the longest)", "#2f7d6d", "bold"),
             ("Jan, Aug, Nov → 1 month each", INK, "normal"), ("Real uses: attendance streaks,", MUTED, "normal"),
             ("machine uptime runs.", MUTED, "normal")]
    for i, (l, c, wt) in enumerate(lines):
        o.append(text(bx + 12, by + 22 + i * 18, l, 11, c, wt))
    return svg(W, max(yy, by + 150) + 18, "".join(o))

if __name__ == "__main__":
    for name, fn in [("fig13-1-group-by-vs-window.svg", fig_group_vs_window),
                     ("fig13-2-window-anatomy-and-frame.svg", fig_anatomy),
                     ("fig13-3-row-number-rank-dense-rank.svg", fig_ranks),
                     ("fig13-4-gaps-and-islands.svg", fig_islands)]:
        open(name, "w").write(check_sizes(name, fn()))
    print("ok13")
