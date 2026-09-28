# Generates the SVG figures for Chapter 3. Run: python3 make_figs03.py
# Redrawn 28 Sep 2026 (visual findings V3.1-V3.4, V3.13): every canvas is 720 px wide, so a font of
# s px prints at s x 493.2 / 720 = 0.685 s pt; the smallest text here is 12 px (8.2 pt).
from make_figs import *
from make_figs01 import wrap
GREEN="#2f7d6d"; PURPLE="#7a4fa0"; ORANGE="#c0662b"; RED="#b23b3b"; DARKRED="#8f2424"; TEAL="#1f6fa3"; GREY="#5b6475"

def lakh(n) -> str:
    """Indian digit grouping for rupee amounts (option pick 67.9): 4335471 -> '43,35,471'."""
    n = str(n).replace(',', ''); i, _, d = n.partition('.')
    if len(i) <= 3: out = i
    else:
        head, tail = i[:-3], i[-3:]
        out = ','.join([head[max(0, k-2):k] for k in range(len(head), 0, -2)][::-1]) + ',' + tail
    return out + ('.' + d if d else '')

def rs(v): return "₹" + lakh(v)

W_CANVAS = 720

# ---------- Figure 3.1: departments and the data they create ----------
def dept_box(x, y, w, h, title, color, lines):
    o = [rect(x+2, y+3, w, h, fill="#e9eef4", rx=8), rect(x, y, w, h, fill="#fff", stroke=color, sw=1.6, rx=8),
         f'<path d="M{x},{y+8} a8,8 0 0 1 8,-8 H{x+w-8} a8,8 0 0 1 8,8 V{y+30} H{x} Z" fill="{color}"/>',
         text(x+12, y+21, title, 15, "#fff", "bold", family=HEAD)]
    o.append(wrap(x+12, y+51, lines, 13, INK, 18))
    return "".join(o)

def fig_departments():
    o = []
    deps = [("Sales", ACC, ["enquiries (leads), quotes,", "sales orders, customer visits"]),
            ("Marketing", PURPLE, ["campaigns, website visits,", "trade-fair contacts"]),
            ("Purchasing", ORANGE, ["suppliers, purchase orders,", "goods received"]),
            ("Production", GREEN, ["production plans, machine", "runs, output, scrap"]),
            ("Warehouse & dispatch", TEAL, ["stock levels, picking lists,", "delivery challans, deliveries"]),
            ("Finance", RED, ["invoices, payments, expenses,", "budgets, tax records"]),
            ("HR", GREY, ["employees, attendance,", "payroll, hiring"]),
            ("Customer support", ORANGE, ["complaints, tickets, returns,", "resolution times"])]
    W = 320; H = 84; GX = 40; GY = 14; x0 = 20; y0 = 20
    for i, (t, c, l) in enumerate(deps):
        r, cidx = divmod(i, 2)
        x = x0 + cidx*(W+GX); y = y0 + r*(H+GY)
        o.append(dept_box(x, y, W, H, t, c, l))
    ybot = y0 + 4*(H+GY) - GY
    bar_y = ybot + 40
    # every department feeds the management bar
    for cidx in range(2):
        x = x0 + cidx*(W+GX) + W/2
        o.append(path(f"M{x},{ybot+2} V{bar_y-6}", stroke=MUTED, sw=1.8))
        o.append(f'<path d="M{x-5},{bar_y-9} L{x},{bar_y-1} L{x+5},{bar_y-9} Z" fill="{MUTED}"/>')
    o.append(rect(x0, bar_y, 2*W+GX, 46, fill=INK, rx=23))
    o.append(text(W_CANVAS/2, bar_y+29, "Management uses all of it to decide", 16, "#fff", "bold", anchor="middle", family=HEAD))
    return svg(W_CANVAS, bar_y+46+20, "".join(o))

# ---------- Figures 3.2 and 3.4: one order from enquiry to cash ----------
# (date, step, what happened, record it leaves, colour, done by hand?)  Order 5001 and invoice 9001 as in the text.
STEPS = [("22 Oct 2025", "Enquiry", "Rakesh fills in the website form", "CRM: new lead", ACC, False),
         ("4 Nov 2025", "New customer", "Credit check; 30-day terms", "ERP: customer 1", ACC, False),
         ("22 Dec 2025", "Quote", "Neha sends prices by email", "CRM: quote Q-2025-118", ACC, True),
         ("5 Jan 2026", "Order", "Rakesh emails; Neha re-types it", "ERP: order 5001", PURPLE, True),
         ("5 Jan 2026", "Stock check", "Boxes and bottles made to stock at Taloja", "ERP: stock reserved", GREEN, True),
         ("6 Jan 2026", "Dispatch", "Bhiwandi Main picks, packs, ships", "ERP: delivery challan", TEAL, False),
         ("6 Jan 2026", "Invoice", "Raised when the order ships", "ERP: invoice 9001", RED, False),
         ("8 Jan 2026", "Delivery", "Rakesh signs the proof of delivery", "Status: Delivered", TEAL, True),
         ("2 Feb 2026", "Payment", "Bank transfer; finance matches it", "ERP: payment 1", RED, True),
         ("3 Feb 2026", "Report", "January sales report", "Report: Jan " + rs(104210), GREY, True)]

def split_words(s, n):
    lines, cur = [], ""
    for w in s.split():
        if len((cur + " " + w).strip()) > n: lines.append(cur); cur = w
        else: cur = (cur + " " + w).strip()
    lines.append(cur)
    return lines

def fig_order_to_cash(mark_manual=False):
    o = []
    x0 = 16; y0 = 48; RH = 50; W = W_CANVAS - 2*x0
    X_NUM = x0 + 20; X_STEP = x0 + 44; X_WHAT = x0 + 196; X_REC = x0 + 462; REC_W = 184; X_BADGE = x0 + W - 20
    # column heads
    for x, s in [(X_STEP, "Step and date"), (X_WHAT, "What happened"), (X_REC, "Record it leaves")]:
        o.append(text(x, y0-14, s, 12.5, MUTED, "bold"))
    # timeline spine through the step numbers
    o.append(path(f"M{X_NUM},{y0+RH/2} V{y0+9*RH+RH/2}", stroke=RULE, sw=3))
    for i, (d, t, who, rec, c, manual) in enumerate(STEPS):
        y = y0 + i*RH
        hand = mark_manual and manual
        if hand:
            o.append(rect(x0, y+3, W, RH-6, fill="#fbe9e9", stroke=DARKRED, sw=2, rx=6))
        elif i % 2 == 0:
            o.append(rect(x0, y+3, W, RH-6, fill=ROWALT, rx=6))
        o.append(f'<circle cx="{X_NUM}" cy="{y+RH/2}" r="13" fill="{c}"/>')
        o.append(text(X_NUM, y+RH/2+5, str(i+1), 13, "#fff", "bold", anchor="middle"))
        o.append(text(X_STEP, y+22, t, 14, INK, "bold", family=HEAD))
        o.append(text(X_STEP, y+39, d, 12, MUTED))
        lines = split_words(who, 32)
        ty = y + (RH/2 + 5 if len(lines) == 1 else 21)
        o.append(wrap(X_WHAT, ty, lines, 13, INK, 16))
        o.append(rect(X_REC, y+12, REC_W, 26, fill="#fff", stroke=RULE, rx=4))
        o.append(text(X_REC+8, y+30, rec, 12, INK, family=MONO))
        if hand:
            o.append(f'<circle cx="{X_BADGE}" cy="{y+RH/2}" r="11" fill="{DARKRED}"/>')
            o.append(text(X_BADGE, y+RH/2+5, "!", 14, "#fff", "bold", anchor="middle"))
    ybot = y0 + 10*RH
    if mark_manual:
        o.append(f'<circle cx="{x0+11}" cy="{ybot+24}" r="11" fill="{DARKRED}"/>')
        o.append(text(x0+11, ybot+29, "!", 14, "#fff", "bold", anchor="middle"))
        o.append(text(x0+30, ybot+29, "A person copies, re-types, or checks data by hand at this step (6 of 10 steps)", 13, INK, "bold"))
        o.append(text(x0, ybot+52, "Source: Mini database (Jan–Mar 2026) for order 5001, invoice 9001 and payment 1.", 12, MUTED, style="italic"))
        return svg(W_CANVAS, ybot+64, "".join(o))
    o.append(text(x0, ybot+26, "Ten steps and more than three months from a website enquiry to one line in a monthly report.", 13, MUTED, style="italic"))
    o.append(text(x0, ybot+48, "Source: Mini database (Jan–Mar 2026) for order 5001, invoice 9001 and payment 1.", 12, MUTED, style="italic"))
    return svg(W_CANVAS, ybot+60, "".join(o))

# ---------- Figure 3.3: bookings, billings, collections ----------
# Horizontal bars, each labelled with its name and value, so colour carries no meaning on its own.
def fig_bbc():
    o = []
    months = ["January", "February", "March"]
    data = [("Booked (orders placed)", [116210, 161700, 58020], ACC),
            ("Billed (invoiced)", [104210, 161700, 31800], PURPLE),
            ("Collected (cash in)", [0, 64700, 132550], GREEN)]
    x0 = 16; XB = 200; BW_MAX = 400; vmax = 180000; BH = 20; y = 40
    o.append(text(x0, 24, "Riverstone, first quarter of 2026: three different numbers for “sales”", 15, INK, "bold", family=HEAD))
    for i, m in enumerate(months):
        y += 16
        o.append(text(x0, y+12, m + " 2026", 14, INK, "bold", family=HEAD))
        y += 20
        for name, vals, col in data:
            v = vals[i]; w = v/vmax*BW_MAX
            o.append(text(XB-10, y+BH-5, name, 12.5, INK, anchor="end"))
            o.append(rect(XB, y, BW_MAX, BH, fill="#f2f5f9", rx=3))
            if w: o.append(rect(XB, y, w, BH, fill=col, rx=3))
            o.append(text(XB+max(w, 0)+8, y+BH-5, rs(v), 13, INK, "bold"))
            y += BH + 7
    o.append(text(x0, y+22, "Same scale for every bar (full grey track = " + rs(180000) + "). Source: Mini database (Jan–Mar 2026).", 12, MUTED, style="italic"))
    return svg(W_CANVAS, y+36, "".join(o))

if __name__ == "__main__":
    for name, fn in [("fig3-1-departments-and-their-data.svg", fig_departments),
                     ("fig3-2-one-order-enquiry-to-cash.svg", lambda: fig_order_to_cash(False)),
                     ("fig3-4-where-manual-work-hides.svg", lambda: fig_order_to_cash(True)),
                     ("fig3-3-booked-billed-collected.svg", fig_bbc)]:
        open(name, "w").write(fn())
    print("ok")
