# Generates the figures for Chapter 18 (SVG, via matplotlib). Run from the book folder: python3 figures/make_figs18.py
#
# Figures 18.2, 18.3 and 18.4 are the charts the chapter's own code draws. So that each figure is exactly what a
# reader's code produces, this script runs the chapter's Python blocks in order (like tools/verify_python.py, in
# companion/ch18), and whenever a block saves one of the chart PNGs it also saves the same figure as SVG here.
# Figure 18.1 shows the chart of section 18.11 after the first step and when finished; it is drawn by make_step_figure()
# with the same data and the same calls as the chapter's cells, side by side at print width.
#
# Print size (V3): every figure prints at the full text width, 174 mm = 493.2 pt. matplotlib writes text as paths,
# which tools/pdf/fig_check.py can't read, so this script measures every figure's printed text size itself and ends
# with a report: every figure must print all its text at 7.0 pt or more.
import contextlib, io, os, pathlib, re, sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.figure
import matplotlib.pyplot as plt
import matplotlib.text as mtext
import pandas as pd

BOOK = pathlib.Path(__file__).resolve().parents[1]
FIG = BOOK / "figures"
CH = next((BOOK / "manuscript").glob("ch18-*.md"))
PRINT_PT = 493.2
SVG_OF = {"region_2025.png": "fig18-2-region-bars.svg",
          "order_values.png": "fig18-3-order-value-boxes.svg",
          "reps_highlight.png": "fig18-4-highlight-lines.svg"}
REPORT = []


def printed_sizes(fig, svg_path):
    """Smallest and largest text size (pt) as the figure prints: font pt x 493.2 / SVG width pt."""
    fig.canvas.draw()
    sizes = [(t.get_fontsize(), t.get_text()) for t in fig.findobj(mtext.Text)
             if t.get_visible() and t.get_text().strip() and t.get_window_extent().width > 0]
    W = float(re.search(r'<svg[^>]*width="([\d.]+)pt"', pathlib.Path(svg_path).read_text()).group(1))
    lo, hi = min(sizes), max(sizes)
    return W, round(lo[0] * PRINT_PT / W, 2), lo[1], round(hi[0] * PRINT_PT / W, 2)


def save_svg(fig, name):
    path = FIG / name
    with plt.rc_context({"svg.fonttype": "path"}):
        fig.savefig(path, format="svg", bbox_inches="tight", pad_inches=0.04)
    REPORT.append((name,) + printed_sizes(fig, path))


def make_step_figure(m25):
    """Figure 18.1: the actual-vs-target chart after step 1, and finished (section 18.11's cells)."""
    fig, (a, b) = plt.subplots(1, 2, figsize=(6.85, 2.7))
    for ax in (a, b):
        ax.plot(m25["month"], m25["net_revenue"] / 1e7, color="#0f5c8c", linewidth=2.5)
        ax.tick_params(labelsize=7.6)
    a.set_title("Step 1: the actual line only", loc="left", fontsize=8.6, color="#5b6475")
    b.plot(m25["month"], m25["target_revenue"] / 1e7, color="#5b6475", linewidth=1.5, linestyle="--")
    b.text(12.2, m25["net_revenue"].iloc[-1] / 1e7, "Actual", color="#0f5c8c", va="top", fontsize=7.6)
    b.text(12.2, m25["target_revenue"].iloc[-1] / 1e7, "Target", color="#5b6475", va="bottom", fontsize=7.6)
    b.set_title("2025 finished at 98.3% of target", loc="left", fontweight="bold", fontsize=8.6)
    b.set_ylabel("Net revenue (₹ crore)", fontsize=7.6)
    b.set_ylim(0, 22)
    b.set_xticks(range(1, 13))
    b.spines[["top", "right"]].set_visible(False)
    fig.subplots_adjust(wspace=0.35)
    save_svg(fig, "fig18-1-chart-steps.svg")
    plt.close(fig)


def run_chapter():
    """Run the chapter's Python blocks in order; copy the chart PNGs it saves to SVG."""
    md = CH.read_text(encoding="utf-8")
    original_savefig = matplotlib.figure.Figure.savefig

    def savefig(self, fname, *args, **kwargs):
        original_savefig(self, fname, *args, **kwargs)
        if isinstance(fname, (str, os.PathLike)) and os.path.basename(str(fname)) in SVG_OF:
            save_svg(self, SVG_OF[os.path.basename(str(fname))])

    matplotlib.figure.Figure.savefig = savefig
    os.chdir(BOOK / "companion" / "ch18")
    sys.path.insert(0, os.getcwd())
    token = re.compile(r'<!-- (py): reset -->|<!-- run: (none) -->|^```(\w*)\n(.*?)^```$', re.S | re.M)
    ns, skip = {"__name__": "__main__"}, False
    for m in token.finditer(md):
        if m.group(1):
            ns = {"__name__": "__main__"}
            continue
        if m.group(2):
            skip = True
            continue
        if m.group(3) == "python":
            if skip:
                skip = False
                continue
            with contextlib.redirect_stdout(io.StringIO()):
                exec(compile(m.group(4), "<ch18>", "exec"), ns)
        elif skip:
            skip = False
    matplotlib.figure.Figure.savefig = original_savefig
    return ns


if __name__ == "__main__":
    if not os.environ.get("RIVERSTONE_DB"):
        sys.exit("Set RIVERSTONE_DB (and start companion/ch18/api_demo.py, with API_TOKEN set) first: the chapter's "
                 "cells run in order. See checks/ch18_extra_check.py for the environment the chapter expects.")
    ns = run_chapter()
    make_step_figure(ns["m25"])
    bad = 0
    for name, W, lo, lo_txt, hi in REPORT:
        flag = "OK" if lo >= 7.0 else "TOO SMALL"
        bad += lo < 7.0
        print(f"{flag:9} {name:34} width {W:6.1f} pt  smallest {lo:5.2f} pt ({lo_txt[:30]!r})  largest {hi:5.2f} pt")
    sys.exit(1 if bad else 0)
