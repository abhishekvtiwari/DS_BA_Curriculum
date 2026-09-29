# Diagrams for Chapter 61. Run: python3 make_figs61.py
# Canvas 740 px wide prints at 174 mm (493.2 pt), so 11 px text prints at 7.3 pt.
# (The old Figure 61.4, the failure-analysis table, is now a real table in section 61.7.)
import math
from make_figs import *

GREEN = "#2f7d6d"; PURPLE = "#7a4fa0"; GOLD = "#b7791f"; RED = "#b23b3b"
SOFT = "#eef2f7"; BLUE2 = "#2f6690"
W = 740


def box(x, y, w, h, title, c, lines=(), size=11.5, tag=None):
    """A card: coloured title bar, then centred lines of text."""
    o = [rect(x + 3, y + 4, w, h, fill=SOFT, rx=8), rect(x, y, w, h, fill="#fff", stroke=c, sw=1.6, rx=8)]
    o.append(f'<path d="M{x},{y+8} a8,8 0 0 1 8,-8 H{x+w-8} a8,8 0 0 1 8,8 V{y+28} H{x} Z" fill="{c}"/>')
    o.append(text(x + w / 2, y + 19, title, 12.5, "#fff", "bold", anchor="middle", family=HEAD))
    for i, l in enumerate(lines):
        o.append(text(x + w / 2, y + 48 + i * 17, l, size, INK, anchor="middle",
                      weight="bold" if (tag is not None and i == 0) else "normal"))
    return "".join(o)


def f1():  # CAP: the triangle, and Riverstone's two opposite choices
    o = [text(20, 30, "CAP: when the network partitions, pick one", 16, INK, "bold", family=HEAD)]
    cx, cy, R = 165, 215, 105
    pts = [(cx + R * math.cos(math.radians(a)), cy + R * math.sin(math.radians(a))) for a in (-90, 30, 150)]
    o.append(f'<polygon points="{" ".join(f"{x:.1f},{y:.1f}" for x, y in pts)}" fill="#f3f6fa" '
             f'stroke="{RULE}" stroke-width="1.4"/>')
    # labels sit clear of the dots: above the top vertex, below the two bottom ones
    labels = [("Consistency", ["every reader sees", "the latest write"], ACC, 0, -58),
              ("Availability", ["the system keeps", "responding"], GREEN, -20, 30),
              ("Partition tolerance", ["the network can", "drop messages"], GOLD, 25, 30)]
    for (px, py), (name, sub, c, dx, dy) in zip(pts, labels):
        o.append(f'<circle cx="{px:.1f}" cy="{py:.1f}" r="7" fill="{c}"/>')
        lx, ly = px + dx, py + dy
        o.append(text(lx, ly, name, 12.5, c, "bold", anchor="middle"))
        for i, l in enumerate(sub):
            o.append(text(lx, ly + 16 + i * 15, l, 11.5, MUTED, anchor="middle"))
    for i, l in enumerate(["P is not", "optional", "at scale"]):
        o.append(text(cx, cy - 4 + i * 15, l, 12, INK, "bold", anchor="middle"))
    # right: the two Riverstone choices
    o.append(box(340, 56, 385, 128, "Order writes (PO-intake → ERP)", ACC,
                 ["CP: choose consistency", "If the CRM check or the ERP can't be reached,",
                  "hold the order in the exception queue.", "Retrying is safe: one email, one order (Ch 58)."],
                 11.5, tag=True))
    o.append(box(340, 204, 385, 128, "Dashboard reads (warehouse → BI)", GREEN,
                 ["AP: choose availability", "If BI can't reach the warehouse, show the last",
                  "imported data under its banner, 'Data current", "to 7 January, 6:35 a.m.' (Ch 47), not an error."],
                 11.5, tag=True))
    o.append(text(20, 372, "CAP is not a menu you pick from once. Different parts of the same platform", 12, MUTED))
    o.append(text(20, 389, "make different, deliberate choices.", 12, MUTED))
    return svg(W, 404, "".join(o))


def f2():  # the consistency spectrum, with Riverstone systems on it
    o = [text(20, 30, "The consistency spectrum, with Riverstone systems on it", 16, INK, "bold", family=HEAD)]
    y = 122
    # end notes sit above the line, clear of the dashed leaders below it
    o.append(text(20, 62, "STRONG", 12.5, ACC, "bold"))
    o.append(text(20, 79, "every reader sees the", 11.5, MUTED))
    o.append(text(20, 94, "latest write, always", 11.5, MUTED))
    o.append(text(720, 62, "EVENTUAL", 12.5, GOLD, "bold", anchor="end"))
    o.append(text(720, 79, "readers may see stale data;", 11.5, MUTED, anchor="end"))
    o.append(text(720, 94, "it converges, given time", 11.5, MUTED, anchor="end"))
    o.append(path(f"M40,{y} H700", stroke=RULE, sw=2.5))
    o.append(f'<path d="M700,{y-6} L712,{y} L700,{y+6} Z" fill="{RULE}"/>')
    items = [("An order in", "the ERP database", "(one copy)", 78, ACC),
             ("Delta Lake", "reads (snapshot)", "(Ch 49)", 224, BLUE2),
             ("Warehouse vs ERP", "previous working", "day (Ch 47)", 370, GREEN),
             ("CRM reverse-", "ETL sync", "(Ch 51)", 516, GOLD),
             ("Support assistant's", "document index", "(Ch 55)", 662, RED)]
    for a, b, c_, x, c in items:
        o.append(f'<circle cx="{x}" cy="{y}" r="7" fill="{c}"/>')
        o.append(path(f"M{x},{y+8} V{y+34}", stroke=c, sw=1.2, dash="3 2"))
        o.append(text(x, y + 52, a, 11.5, INK, "bold", anchor="middle"))
        o.append(text(x, y + 67, b, 11.5, INK, anchor="middle"))
        o.append(text(x, y + 82, c_, 11.5, MUTED, anchor="middle"))
    o.append(text(20, 238, "Nothing here is a defect. Strong consistency costs latency and availability; eventual", 12, MUTED))
    o.append(text(20, 255, "consistency is a deliberate trade for scale and resilience. The judgment is choosing", 12, MUTED))
    o.append(text(20, 272, "which one each system genuinely needs, not defaulting to either.", 12, MUTED))
    return svg(W, 286, "".join(o))


def f3():  # the reliability toolkit, six cards in a 3 x 2 grid
    o = [text(20, 30, "The reliability toolkit", 16, INK, "bold", family=HEAD)]
    items = [("Partitioning & sharding", ["Partition: split one table by", "a key. Shard: put the pieces", "on different servers"], ACC,
              ["Sensor archive: partitioned by", "month (Ch 49), not sharded"]),
             ("Replication", ["Keep copies for availability", "and durability; copies of data", "can lag: a consistency cost"], GREEN,
              ["replicas: 2 keeps two copies", "of the Flash page (Ch 52)"]),
             ("Load balancing", ["Spread requests across copies", "of one service, so no single", "copy is swamped"], GOLD,
              ["A Kubernetes Service sends each", "request to a ready copy (Ch 52)"]),
             ("Caching", ["Serve repeats from memory;", "the hard part is knowing", "when an answer is stale"], PURPLE,
              ["Exact-match cache (Ch 57):", "17% saved on a normal day"]),
             ("Message queues", ["Put a log between producer", "and consumer; absorb bursts", "without losing work"], RED,
              ["MessageLog (Ch 50): topics,", "partitions, offsets, like Kafka"]),
             ("Scaling up or out", ["Up: one bigger machine.", "Out: more machines sharing", "the work"], BLUE2,
              ["Up: a bigger warehouse server.", "Out: a second defect-model copy"])]
    cw, ch, gap = 226, 108, 11
    for i, (name, desc, c, ex) in enumerate(items):
        x = 20 + (i % 3) * (cw + gap)
        y = 50 + (i // 3) * (ch + 58 + 18)
        o.append(box(x, y, cw, ch, name, c, desc, 11.5))
        o.append(rect(x, y + ch + 6, cw, 50, fill="#f3f6fa", rx=6))
        for j, l in enumerate(ex):
            o.append(text(x + cw / 2, y + ch + 26 + j * 16, l, 11, MUTED, anchor="middle"))
    yb = 50 + 2 * (ch + 58 + 18)
    o.append(text(20, yb + 6, "None of these is exotic: Parts 5 and 6 already use most of them. This chapter names", 12, MUTED))
    o.append(text(20, yb + 23, "them as a reusable kit, and each one has a cost.", 12, MUTED))
    return svg(W, yb + 38, "".join(o))


if __name__ == "__main__":
    for n, f in [("fig61-1-cap-theorem.svg", f1), ("fig61-2-consistency-spectrum.svg", f2),
                 ("fig61-3-reliability-toolkit.svg", f3)]:
        open(n, "w").write(f())
    print("ok")
