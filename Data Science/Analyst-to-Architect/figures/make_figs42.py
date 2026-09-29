# Generates the SVG figures for Chapter 42. Run from figures/ after checks/ch42_check.py has written ch42_results.json.
# Every text element prints at 7 pt or more: on a 1000 px canvas printed 493.2 pt wide, that needs 14.2 px or more.
# (Neither figure is placed in the chapter at present; the scoreboard table in section 42.7 carries the same numbers.)
import json, pathlib
from make_figs import *
GREEN = "#2f7d6d"; RED = "#b23b3b"; ORANGE = "#c0662b"; PURPLE = "#7a4fa0"; PALE = "#eef1f5"
R = json.loads((pathlib.Path(__file__).resolve().parent.parent / "checks" / "ch42_results.json").read_text())


def line(x1, y1, x2, y2, c=RULE, sw=1, dash=None):
    return path(f"M{x1:.1f},{y1:.1f} L{x2:.1f},{y2:.1f}", stroke=c, sw=sw, dash=dash)


def fig_compare():
    """Horizontal bars: hit rate@5 for every method, best first, with NDCG@5 written beside each bar."""
    o = []; board = R["scoreboard"]
    X0 = 260; W = 560; Y0 = 80; ROW = 40
    X = lambda v: X0 + v / 0.8 * W
    o.append(text(20, 40, "Hit rate@5, leave-one-out, every method", 22, INK, "bold", family=HEAD))
    for v in [0, 0.2, 0.4, 0.6, 0.8]:
        o.append(line(X(v), Y0 - 10, X(v), Y0 + ROW * len(board), PALE))
        o.append(text(X(v), Y0 + ROW * len(board) + 22, f"{v:.0%}", 15, MUTED, anchor="middle"))
    for i, (method, (hit, ndcg, mrr)) in enumerate(board.items()):
        y = Y0 + i * ROW
        colour = GREEN if method == "segment popularity" else (MUTED if method == "popularity" else ACC)
        o.append(text(X0 - 12, y + 20, method, 16, INK, anchor="end"))
        o.append(rect(X0, y + 5, X(hit) - X0, 22, fill=colour, rx=3))
        o.append(text(X(hit) + 8, y + 21, f"{hit:.1%}  (NDCG {ndcg:.3f})", 15, INK))
    return svg(1000, Y0 + ROW * len(board) + 40, "".join(o))


def fig_segment():
    """Each segment's three most-bought products, as the share of the segment's accounts that bought them."""
    o = []; segs = R["segment_top"]; names = R["names"]
    X0 = 40; Y0 = 50; rowh = 110
    for i, (seg, items) in enumerate(segs.items()):
        y = Y0 + i * rowh
        o.append(text(X0, y, seg, 20, INK, "bold", family=HEAD))
        for j, (pid, share) in enumerate(items.items()):
            bx = X0 + j * 320
            w = share * 260
            o.append(rect(bx, y + 14, w, 24, fill=[ACC, GREEN, ORANGE][i], rx=3))
            o.append(text(bx + w + 8, y + 32, f"{share:.0%}", 16, INK, "bold"))
            o.append(text(bx, y + 62, names[pid], 16, INK))
    return svg(1000, Y0 + 3 * rowh, "".join(o))


if __name__ == "__main__":
    for name, fn in [("fig42-1-method-comparison.svg", fig_compare), ("fig42-2-segment-preferences.svg", fig_segment)]:
        open(name, "w").write(fn())
    print("ok")
