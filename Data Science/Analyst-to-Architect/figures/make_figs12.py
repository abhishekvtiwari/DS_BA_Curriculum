# Generates the SVG figures for Chapter 12 at print size. Run: python3 make_figs12.py
# Every figure prints at the full text width (493.2 pt), so a font of s px on a W px canvas prints at
# s * 493.2 / W pt. Each canvas below keeps its smallest text at 7 pt or more (checked by tools/pdf/fig_check.py).
# Shared drawing helpers and colours come from make_figs.py; the Chapter 12 figures there are the older,
# larger-canvas versions and are no longer used.
from make_figs import svg, text, rect, path, INK, MUTED, ACC, RULE, PK, PKBG, FK, FKBG, ROWALT, HEAD, MONO

RED = "#b23b3b"; GREEN = "#2f7d6d"


def min_px(w):
    """Smallest font size (px) that prints at 7 pt on a canvas w px wide, rounded up a little."""
    return round(7 * w / 493.2 + 0.05, 1)


def badge(x, y, label, size):
    c, bg = (PK, PKBG) if label == "PK" else (FK, FKBG)
    return (rect(x, y - 12, 27, 17, fill=bg, stroke=c, sw=1, rx=3)
            + text(x + 13.5, y + 1, label, size, c, "bold", anchor="middle"))


# ---------- Figure 12.1: the schema ----------
def fig_schema():
    W, Hc = 780, 660
    S = min_px(W)                       # 11.1 px: types, badges, legend
    NAME = 12; H = 32; R = 24; TW = 212

    class T:
        def __init__(s, x, y, name, cols):
            s.x, s.y, s.name, s.cols = x, y, name, cols
        def ry(s, i): return s.y + H + i * R + R / 2
        def bottom(s): return s.y + H + len(s.cols) * R + 6
        def draw(s):
            o = [rect(s.x + 2, s.y + 3, TW, s.bottom() - s.y, fill="#e9eef4", rx=6),
                 rect(s.x, s.y, TW, s.bottom() - s.y, fill="#fff", stroke=RULE, sw=1.2, rx=6),
                 f'<path d="M{s.x},{s.y+6} a6,6 0 0 1 6,-6 H{s.x+TW-6} a6,6 0 0 1 6,6 V{s.y+H} H{s.x} Z" fill="{ACC}"/>',
                 text(s.x + 10, s.y + 21.5, s.name, 14, "#fff", "bold", family=HEAD)]
            for i, (c, t, k) in enumerate(s.cols):
                yy = s.y + H + i * R
                if i % 2: o.append(rect(s.x + 1, yy, TW - 2, R, fill=ROWALT))
                cy = yy + R / 2 + 4.5
                if k: o.append(badge(s.x + 6, cy - 3.5, k, S))
                o.append(text(s.x + 38, cy, c, NAME, INK, "bold" if k == "PK" else "normal", family=MONO))
                o.append(text(s.x + TW - 8, cy, t, S, MUTED, anchor="end"))
            return "".join(o)

    X1, X2, X3 = 12, 276, 540
    cu = T(X1, 40, "customers", [("customer_id", "INTEGER", "PK"), ("customer_name", "VARCHAR", ""), ("city", "VARCHAR", ""), ("segment", "VARCHAR", ""), ("signup_date", "DATE", "")])
    pr = T(X1, 380, "products", [("product_id", "INTEGER", "PK"), ("product_name", "VARCHAR", ""), ("category", "VARCHAR", ""), ("unit_price", "NUMERIC", ""), ("unit_cost", "NUMERIC", "")])
    od = T(X2, 40, "orders", [("order_id", "INTEGER", "PK"), ("customer_id", "INTEGER", "FK"), ("order_date", "DATE", ""), ("status", "VARCHAR", ""), ("sales_rep_id", "INTEGER", "FK")])
    oi = T(X2, 380, "order_items", [("order_item_id", "INTEGER", "PK"), ("order_id", "INTEGER", "FK"), ("product_id", "INTEGER", "FK"), ("quantity", "INTEGER", ""), ("unit_price", "NUMERIC", ""), ("discount_pct", "NUMERIC", "")])
    inv = T(X3, 40, "invoices", [("invoice_id", "INTEGER", "PK"), ("order_id", "INTEGER", "FK"), ("invoice_date", "DATE", ""), ("due_date", "DATE", ""), ("amount", "NUMERIC", "")])
    pay = T(X3, 240, "payments", [("payment_id", "INTEGER", "PK"), ("invoice_id", "INTEGER", "FK"), ("payment_date", "DATE", ""), ("amount", "NUMERIC", ""), ("method", "VARCHAR", "")])
    em = T(X3, 440, "employees", [("employee_id", "INTEGER", "PK"), ("employee_name", "VARCHAR", ""), ("job_title", "VARCHAR", ""), ("manager_id", "INTEGER", "FK")])

    def one(x, y): return text(x, y, "1", 13.5, ACC, "bold")
    def many(x, y): return text(x, y, "N", 13.5, ACC, "bold")
    o = []
    gx = (X1 + TW + X2) / 2
    y0, y1 = cu.ry(0), od.ry(1); o += [path(f"M{X1+TW},{y0} H{gx} V{y1} H{X2}"), one(X1 + TW + 5, y0 - 5), many(X2 - 14, y1 - 5)]
    y0, y1 = pr.ry(0), oi.ry(2); o += [path(f"M{X1+TW},{y0} H{gx} V{y1} H{X2}"), one(X1 + TW + 5, y0 - 5), many(X2 - 14, y1 - 5)]
    xm = X2 + TW - 50
    o += [path(f"M{xm},{od.bottom()} V{oi.y}"), one(xm + 7, od.bottom() + 17), many(xm + 7, oi.y - 7),
          text(xm - 8, (od.bottom() + oi.y) / 2 + 4, "order_id", S, MUTED, anchor="end", style="italic")]
    gx2 = (X2 + TW + X3) / 2
    y0, y1 = od.ry(0), inv.ry(1); o += [path(f"M{X2+TW},{y0} H{gx2} V{y1} H{X3}"), one(X2 + TW + 5, y0 - 5), many(X3 - 14, y1 - 5)]
    xr = X3 + TW + 16
    y0, y1 = inv.ry(0), pay.ry(1); o += [path(f"M{X3+TW},{y0} H{xr} V{y1} H{X3+TW}"), one(X3 + TW + 4, y0 - 5), many(X3 + TW + 3, y1 - 5)]
    gx3 = X3 - 22
    y0, y1 = em.ry(0), od.ry(4); o += [path(f"M{X3},{y0} H{gx3} V{y1} H{X2+TW}"), one(X3 - 11, y0 - 5), many(X2 + TW + 4, y1 - 5)]
    y0, y1 = em.ry(0), em.ry(3); o += [path(f"M{X3+TW},{y1} H{xr} V{y0} H{X3+TW}", dash="5 4"), one(X3 + TW + 4, y0 - 5), many(X3 + TW + 3, y1 - 5)]
    for t in (cu, pr, od, oi, inv, pay, em): o.append(t.draw())
    ly = 610
    o.append(rect(20, ly - 18, 740, 32, fill="#f6f9fc", stroke=RULE, rx=6))
    o.append(badge(30, ly + 3, "PK", S)); o.append(text(64, ly + 3, "primary key: identifies each row", 12, INK))
    o.append(badge(290, ly + 3, "FK", S)); o.append(text(324, ly + 3, "foreign key: points to another table's row", 12, INK))
    o.append(path(f"M{612},{ly-1} H{640}")); o.append(one(600, ly + 4)); o.append(many(644, ly + 4))
    o.append(text(662, ly + 3, "one to many", 12, INK))
    o.append(text(20, 648, "Dashed line: an employee's manager is another employee in the same table.", S, MUTED, style="italic"))
    return svg(W, Hc, "".join(x for x in o if x))


# ---------- Figure 12.2: one order, five tables ----------
def mini(x, y, name, headers, rows, widths, color, size):
    w = sum(widths)
    o = [rect(x, y, w, 22, fill=color, rx=4), text(x + 8, y + 15.5, name, 12.5, "#fff", "bold", family=HEAD)]
    yy = y + 22
    o.append(rect(x, yy, w, 19, fill="#eef2f6"))
    cx = x
    for h_, wd in zip(headers, widths):
        o.append(text(cx + 5, yy + 13.5, h_, size, MUTED, "bold", family=MONO)); cx += wd
    yy += 19
    for r in rows:
        o.append(rect(x, yy, w, 20, fill="#fff", stroke=RULE, sw=0.8)); cx = x
        for v, wd in zip(r, widths):
            o.append(text(cx + 5, yy + 14, v, size, INK, family=MONO)); cx += wd
        yy += 20
    o.append(rect(x, y, w, yy - y, stroke=color, sw=1.5, rx=4))
    return "".join(o), yy


def fig_one_order():
    W, Hc = 780, 492
    S = min_px(W)                       # 11.1 px
    C_ORD = "#0f5c8c"; C_CUS = "#2f7d6d"; C_EMP = "#7a4fa0"; C_ITM = "#c0662b"; C_PRD = "#5b6475"
    o = []
    sx, sy, sw, sh = 14, 14, 300, 400
    o.append(rect(sx + 3, sy + 4, sw, sh, fill="#e9eef4", rx=9)); o.append(rect(sx, sy, sw, sh, fill="#fffdf7", stroke="#d8cfb8", sw=1.2, rx=9))
    o.append(text(sx + 14, sy + 26, "RIVERSTONE SUPPLIES", 14, INK, "bold", family=HEAD))
    o.append(text(sx + 14, sy + 44, "Order slip, as a person sees it", S, MUTED, style="italic"))

    def band(y, h, c, table):
        return (rect(sx + 8, y, sw - 16, h, fill=c, rx=4, extra='fill-opacity="0.10"') + rect(sx + 8, y, 4, h, fill=c)
                + text(sx + sw - 14, y + 14, "→ " + table, S, c, "bold", anchor="end"))
    o.append(band(sy + 56, 46, C_ORD, "orders")); o.append(text(sx + 20, sy + 75, "Order no. 5001", 12.5, INK, "bold")); o.append(text(sx + 20, sy + 93, "05 Jan 2026 · Delivered", S, INK))
    o.append(band(sy + 110, 46, C_CUS, "customers")); o.append(text(sx + 20, sy + 129, "Sharma Hardware", 12.5, INK, "bold")); o.append(text(sx + 20, sy + 147, "Mumbai · Retail", S, INK))
    o.append(band(sy + 164, 30, C_EMP, "employees")); o.append(text(sx + 20, sy + 184, "Rep: Neha Kulkarni", 12, INK))
    o.append(band(sy + 202, 132, C_ITM, "order_items"))
    o.append(text(sx + sw - 14, sy + 232, "+ products", S, C_PRD, "bold", anchor="end"))
    hy = sy + 256
    o.append(text(sx + 20, hy, "Product", S, MUTED, "bold")); o.append(text(sx + 150, hy, "Qty", S, MUTED, "bold", anchor="end"))
    o.append(text(sx + 190, hy, "Price", S, MUTED, "bold", anchor="end")); o.append(text(sx + 228, hy, "Disc", S, MUTED, "bold", anchor="end")); o.append(text(sx + 280, hy, "Net ₹", S, MUTED, "bold", anchor="end"))
    for i, (p, q, pr_, d, n) in enumerate([("Storage Box 10L", "20", "450", "0%", "9,000"), ("Water Bottle 1L", "50", "120", "5%", "5,700")]):
        yy = sy + 276 + i * 20
        o.append(text(sx + 20, yy, p, 12, INK)); o.append(text(sx + 150, yy, q, 12, INK, anchor="end")); o.append(text(sx + 190, yy, pr_, 12, INK, anchor="end"))
        o.append(text(sx + 228, yy, d, 12, INK, anchor="end")); o.append(text(sx + 280, yy, n, 12, INK, anchor="end"))
    o.append(f'<line x1="{sx+20}" y1="{sy+305}" x2="{sx+280}" y2="{sy+305}" stroke="{RULE}"/>')
    o.append(text(sx + 20, sy + 323, "Total", 12.5, INK, "bold")); o.append(text(sx + 280, sy + 323, "₹14,700", 12.5, INK, "bold", anchor="end"))
    o.append(rect(sx + 8, sy + 342, sw - 16, 50, fill="#fff4d6", stroke="#e2c46b", rx=5))
    o.append(text(sx + 16, sy + 362, "Line values and the total are not stored.", S, INK, "bold"))
    o.append(text(sx + 16, sy + 381, "SQL calculates them: qty × price × (1 − disc).", S, INK))
    X = 350
    t, _ = mini(X, 14, "orders", ["order_id", "customer_id", "order_date", "status", "sales_rep_id"], [["5001", "1", "2026-01-05", "Delivered", "3"]], [66, 86, 82, 76, 96], C_ORD, S); o.append(t)
    t, _ = mini(X, 94, "customers", ["customer_id", "customer_name", "city", "segment"], [["1", "Sharma Hardware", "Mumbai", "Retail"]], [86, 114, 60, 66], C_CUS, S); o.append(t)
    t, _ = mini(X, 174, "employees", ["employee_id", "employee_name", "job_title"], [["3", "Neha Kulkarni", "Sales Executive"]], [86, 104, 116], C_EMP, S); o.append(t)
    t, _ = mini(X, 254, "order_items", ["order_id", "product_id", "quantity", "unit_price", "discount_pct"], [["5001", "101", "20", "450.00", "0.00"], ["5001", "103", "50", "120.00", "5.00"]], [66, 80, 72, 80, 96], C_ITM, S); o.append(t)
    t, _ = mini(X, 354, "products", ["product_id", "product_name", "category"], [["101", "Storage Box 10L", "Storage"], ["103", "Water Bottle 1L", "Kitchen"]], [80, 116, 72], C_PRD, S); o.append(t)

    def conn(y1, y2, c): return path(f"M{sx+sw},{y1} C{sx+sw+22},{y1} {X-22},{y2} {X},{y2}", stroke=c, sw=2)
    o += [conn(sy + 79, 50, C_ORD), conn(sy + 133, 130, C_CUS), conn(sy + 179, 210, C_EMP), conn(sy + 250, 300, C_ITM), conn(sy + 270, 400, C_PRD)]
    o.append(text(14, 462, "Keys tie the pieces together: orders.customer_id = 1 finds the customer, and sales_rep_id = 3 the rep;", S, INK))
    o.append(text(14, 481, "order_items.order_id = 5001 finds the lines, and each line's product_id finds its product.", S, INK))
    return svg(W, Hc, "".join(o))


# ---------- Figures 12.3 and 12.4: small result grids ----------
def grid(x, y, title, headers, rows, widths, size, color=ACC, rowfill=None, subtitle=None):
    o = []
    if subtitle:
        o += [text(x, y - 22, title, 13, INK, "bold", family=HEAD), text(x, y - 7, subtitle, size, MUTED, style="italic")]
    else:
        o.append(text(x, y - 7, title, 13, INK, "bold", family=HEAD))
    w = sum(widths); o.append(rect(x, y, w, 21, fill=color, rx=3)); cx = x
    for h_, wd in zip(headers, widths):
        o.append(text(cx + 6, y + 14.5, h_, size, "#fff", "bold", family=MONO)); cx += wd
    yy = y + 21; centers = []
    for i, r in enumerate(rows):
        f = rowfill[i] if rowfill and rowfill[i] else "#fff"
        o.append(rect(x, yy, w, 21, fill=f, stroke=RULE, sw=0.8)); cx = x
        for v, wd in zip(r, widths):
            if v == "NULL": o.append(text(cx + 6, yy + 14.5, "NULL", size, RED, "bold", family=MONO, style="italic"))
            else: o.append(text(cx + 6, yy + 14.5, v, size, INK, family=MONO))
            cx += wd
        centers.append(yy + 10.5); yy += 21
    return "".join(o), centers, yy


def fig_joins():
    W, Hc = 640, 430
    S = min_px(W)                       # 9.2 px; this figure uses 10.5 px or more
    Z = 10.5
    o = []
    t, cy, _ = grid(20, 34, "customers", ["customer_id", "customer_name"], [["1", "Sharma Hardware"], ["2", "Patel Kitchenware"], ["8", "Blue Bay Cafe"]], [86, 132], Z); o.append(t)
    t, oy, _ = grid(360, 34, "orders", ["order_id", "customer_id"], [["5001", "1"], ["5005", "1"], ["5011", "1"], ["5003", "2"]], [70, 88], Z); o.append(t)
    for a, b in [(0, 0), (0, 1), (0, 2), (1, 3)]:
        o.append(path(f"M238,{cy[a]} C300,{cy[a]} 300,{oy[b]} 360,{oy[b]}", stroke=GREEN, sw=2))
    o.append(text(20, 150, "Blue Bay Cafe (customer 8) has no matching order.", Z, RED, "bold"))
    o.append(text(20, 166, "Lines join rows whose customer_id values are equal.", Z, MUTED))
    t, _, _ = grid(20, 222, "INNER JOIN result", ["customer_name", "order_id"], [["Sharma Hardware", "5001"], ["Sharma Hardware", "5005"], ["Sharma Hardware", "5011"], ["Patel Kitchenware", "5003"]], [140, 76], Z, subtitle="4 rows: matches only"); o.append(t)
    t, _, _ = grid(330, 222, "LEFT JOIN result", ["customer_name", "order_id"], [["Sharma Hardware", "5001"], ["Sharma Hardware", "5005"], ["Sharma Hardware", "5011"], ["Patel Kitchenware", "5003"], ["Blue Bay Cafe", "NULL"]], [140, 76], Z, rowfill=[None, None, None, None, "#fdecec"], subtitle="5 rows: every customer kept"); o.append(t)
    o.append(rect(20, 356, 600, 64, fill="#f6f9fc", stroke=RULE, rx=5))
    for i, s_ in enumerate(["INNER JOIN keeps a row only when both sides match. LEFT JOIN keeps every row",
                            "of the left table (customers) and fills the missing right side with NULL.",
                            "Sharma Hardware appears three times: one output row per matching pair."]):
        o.append(text(30, 375 + i * 17, s_, Z, INK, "bold" if i == 2 else "normal"))
    return svg(W, Hc, "".join(o))


def fig_fanout():
    W, Hc = 640, 352
    Z = 10.5                            # min_px(640) = 9.2 px
    o = []
    o.append(text(20, 22, "✗ What goes wrong: join first, then add up", 13.5, RED, "bold", family=HEAD))
    t, _, _ = grid(20, 52, "invoices", ["invoice_id", "amount"], [["9002", "73260.00"]], [78, 72], Z); o.append(t)
    t, _, _ = grid(190, 52, "payments", ["invoice_id", "amount"], [["9002", "40000.00"], ["9002", "33260.00"]], [78, 72], Z); o.append(t)
    t, _, yy = grid(360, 52, "after the JOIN (2 rows)", ["invoice_id", "invoice_amt", "paid"], [["9002", "73260.00", "40000.00"], ["9002", "73260.00", "33260.00"]], [78, 86, 72], Z, rowfill=["#fdecec", "#fdecec"]); o.append(t)
    o.append(text(20, 150, "SUM(invoice_amt) = 1,46,520  ✗  the invoice is counted twice", 11.5, RED, "bold"))
    o.append(text(20, 168, "SUM(paid) = 73,260  ✓  payments are the finest grain, so none repeat", Z, MUTED))
    o.append(f'<line x1="20" y1="190" x2="620" y2="190" stroke="{RULE}" stroke-width="1.5"/>')
    o.append(text(20, 218, "✓ The fix: add up payments per invoice first, then join", 13.5, GREEN, "bold", family=HEAD))
    t, _, _ = grid(20, 250, "payments summed per invoice", ["invoice_id", "paid"], [["9002", "73260.00"]], [78, 72], Z, color=GREEN); o.append(t)
    t, _, yy = grid(360, 250, "after the JOIN (1 row)", ["invoice_id", "invoice_amt", "paid"], [["9002", "73260.00", "73260.00"]], [78, 86, 72], Z, color=GREEN, rowfill=["#e2f3ee"]); o.append(t)
    o.append(path("M180,271 H350", stroke=GREEN, sw=2)); o.append(f'<path d="M350,266 l7,5 l-7,5 z" fill="{GREEN}"/>')
    o.append(text(20, 318, "One row per invoice, so the totals are correct  ✓", 11.5, GREEN, "bold"))
    o.append(text(20, 336, "Rule: bring every table to the same grain (one row per invoice here) before joining.", Z, MUTED))
    return svg(W, Hc, "".join(o))


# ---------- Figure 12.5: written order versus running order ----------
def fig_order():
    W, Hc = 640, 346
    Z = 10.5                            # min_px(640) = 9.2 px
    o = []
    written = ["SELECT", "FROM", "JOIN", "WHERE", "GROUP BY", "HAVING", "ORDER BY", "LIMIT"]
    run = [("FROM / JOIN", "gather and combine tables"), ("WHERE", "drop rows"), ("GROUP BY", "make groups"), ("HAVING", "drop groups"),
           ("SELECT", "compute columns and aliases"), ("DISTINCT", "remove duplicate rows"), ("ORDER BY", "sort (aliases exist now)"), ("LIMIT", "keep the first n")]
    o.append(text(20, 22, "You write it in this order", 13, MUTED, "bold", family=HEAD))
    x = 20; wd = 70; gap = 5
    for w_ in written:
        o.append(rect(x, 32, wd, 26, fill="#eef2f6", stroke=RULE, rx=13)); o.append(text(x + wd / 2, 49.5, w_, Z, INK, "bold", anchor="middle", family=MONO)); x += wd + gap
    o.append(text(20, 90, "The database runs it in this order", 13, ACC, "bold", family=HEAD))
    bw, bh, bg = 134, 66, 21
    for i, (k, d) in enumerate(run):
        row, col = divmod(i, 4)
        x = 20 + col * (bw + bg); y = 108 + row * (bh + 34)
        o.append(rect(x, y, bw, bh, fill="#fff", stroke=ACC, sw=1.5, rx=7))
        o.append(f'<circle cx="{x+14}" cy="{y+15}" r="10" fill="{ACC}"/>'); o.append(text(x + 14, y + 19, str(i + 1), Z, "#fff", "bold", anchor="middle"))
        o.append(text(x + 30, y + 19.5, k, 11.5, INK, "bold", family=MONO))
        words = d.split(" "); lines = []; cur = ""
        for w_ in words:
            if len((cur + " " + w_).strip()) > 20: lines.append(cur); cur = w_
            else: cur = (cur + " " + w_).strip()
        lines.append(cur)
        for j, l in enumerate(lines): o.append(text(x + 10, y + 39 + j * 14, l, Z, MUTED))
        if col < 3:
            o.append(path(f"M{x+bw+2},{y+bh/2} H{x+bw+bg-6}", sw=2)); o.append(f'<path d="M{x+bw+bg-6},{y+bh/2-5} l6,5 l-6,5 z" fill="{ACC}"/>')
        elif row == 0:
            yb = y + bh + 17; xa = 20 + bw / 2
            o.append(path(f"M{x+bw/2},{y+bh+2} V{yb} H{xa} V{y+bh+34-6}", sw=2)); o.append(f'<path d="M{xa-5},{y+bh+34-6} l5,6 l5,-6 z" fill="{ACC}"/>')
    o.append(rect(20, 288, 600, 48, fill="#fff4d6", stroke="#e2c46b", rx=5))
    o.append(text(30, 307, "This is why WHERE can't use COUNT(*) or a SELECT alias (step 2 runs before", Z, INK))
    o.append(text(30, 324, "steps 3 and 5), and why ORDER BY can use an alias (step 7 runs after step 5).", Z, INK))
    return svg(W, Hc, "".join(o))


if __name__ == "__main__":
    import os
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    for name, fn in [("fig12-1-riverstone-schema.svg", fig_schema), ("fig12-2-one-order-many-tables.svg", fig_one_order),
                     ("fig12-3-inner-vs-left-join.svg", fig_joins), ("fig12-4-fan-out.svg", fig_fanout), ("fig12-5-execution-order.svg", fig_order)]:
        open(name, "w").write(fn())
    print("ok")
