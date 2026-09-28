# Parked: Python moved out of Chapter 15 (Part 2 build, 28 Sep 2026)

Approved decision (CLAUDE.md section 3; findings 15.1, 15.2, 15.3, 15.9, 15.10): the Python in Chapter 15
moves to **Chapter 18, section 18.11 "Charts with matplotlib and seaborn"**, because Chapter 15 comes before
Python in the reading order (10, 11, 19, 12, 13, 14, 15, 16, 17, 18). Each block below is kept **verbatim**
as it stood in Chapter 15, labelled with its destination and with a one-line note of what it depends on.
The Ch 18 build pulls a block from here, rebuilds it as Jupyter cells (finding 15.1 lists nine cells:
read + `head()`; filter 2025; attainment sum; `subplots` + one `ax.plot`; target line with
`linestyle="--"`; direct labels with `ax.text`; title/ylabel/ylim/xticks; spines; `savefig`), shows real
output (the chart image) after each, explains every argument, and points **back** ("Chapter 15 drew this
chart in a spreadsheet; here is the same chart in code").

Rupee amounts are as they stood before the lakh-grouping pass (option pick 67.9): convert prose amounts
when a block is placed; never hand-edit program output.

Chapter 15 now ends its Excel/Sheets section 15.14 without code and says in "Where this leads":
"Chapter 18 draws these charts in Python." The companion data the blocks read is unchanged:
`companion/ch15/chart_data/*.csv` (built by `companion/ch15/build_ch15_data.py`).

---

## 1. §15.14 subsection "A first look at charts in code" (text, two code blocks, their outputs, and the closing explanation)

**Landed** in Ch 18 §18.11 (the attainment cell, three drawing cells and Figure 18.1) (Part 2/3 build).

**Destination:** → Ch 18 §18.11

**Depends on:** pandas and matplotlib (Ch 17–18); run with the working folder `companion/ch15` so `chart_data/monthly_2023_2025.csv` is found; the second block uses `m25` from the first. `<!-- py: reset -->` is the verify_python marker. The last sentence names `figures/make_figs15.py`, a build script (finding 15.9): don't carry that name into reader text; if the figure code is wanted, publish it as `companion/ch18/chart_examples.ipynb` and reference that.


<!-- verbatim start -->

### A first look at charts in code

Python is taught in its own block: Chapter 17 covers the language and Chapter 18 covers pandas and charting with **matplotlib** and **seaborn**. If you haven't reached them yet, read this section as a preview and return to it afterwards. The same principles apply in code, where they're easier to repeat: once a chart function is written, every chart it draws follows the rules. This preview uses the chart data in `companion/ch15`.

<!-- py: reset -->
```python
import pandas as pd
monthly = pd.read_csv("chart_data/monthly_2023_2025.csv")
m25 = monthly[monthly["year"] == 2025]
print(m25[["month", "net_revenue", "target_revenue"]].head(3).to_string(index=False))
print(round(m25["net_revenue"].sum() / m25["target_revenue"].sum() * 100, 1))
```

```
 month  net_revenue  target_revenue
     1   85195520.0        77350000
     2   78582579.0        70000000
     3  101009066.0       108050000
98.3
```

The first three months, and the year's attainment: 98.3%. (January shows ₹85,195,520 here and ₹85,195,521 in SQL, because each tool rounded the unrounded ₹85,195,520.50 differently.)

```python
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

fig, ax = plt.subplots(figsize=(8, 4))
ax.plot(m25["month"], m25["net_revenue"] / 1e7, color="#0f5c8c", linewidth=2.5)
ax.plot(m25["month"], m25["target_revenue"] / 1e7, color="#5b6475", linewidth=1.5, linestyle="--")
ax.text(12.1, m25["net_revenue"].iloc[-1] / 1e7, "Actual", color="#0f5c8c", va="center")
ax.text(12.1, m25["target_revenue"].iloc[-1] / 1e7, "Target", color="#5b6475", va="center")
ax.set_title("2025 finished at 98.3% of target", loc="left", fontweight="bold")
ax.set_ylabel("Net revenue (₹ crore)")
ax.set_ylim(0, 22)
ax.set_xticks(range(1, 13))
ax.spines[["top", "right"]].set_visible(False)
fig.savefig("my_revenue_chart.png", dpi=150, bbox_inches="tight")
print("saved")
```

```
saved
```

Every principle from the chapter is a line of code: direct labels instead of a legend (`ax.text`), an action title, a unit in the axis title, a zero baseline, and no top or right border. `matplotlib.use("Agg")` draws without opening a window, which is what you want in a script. The full figure code for this chapter is `figures/make_figs15.py`.

<!-- verbatim end -->

---

## 2. "Chapter at a glance": the Python items

**Landed** in Ch 18's Chapter at a glance box (for the record) (Part 2/3 build).

**Destination:** → Ch 18 §18.11 (for the record; Ch 18's own Tools line already lists Python)

**Depends on:** nothing. Removed from Ch 15's "You will learn to" and Tools lines (finding 15.2). Original lines:


<!-- verbatim start -->

> **You will learn to:** explain how people read charts, and why position and length beat angle, area, and color · start from the question and pick the chart that answers it · build clear bar, line, histogram, box, scatter, stacked, waterfall, heatmap, and map charts, and know when each fails · use color with meaning: one highlight, sequential and diverging palettes, color-blind-safe choices · write titles that state the finding and annotations that explain it · remove clutter without removing information · recognize misleading charts (truncated axes, dual axes, 3D, cherry-picked ranges) and avoid making them · show missing and uncertain data openly · make charts accessible · build the charts in Excel and Google Sheets, with a first look at matplotlib · redesign a poor management pack.
>
> **Tools:** Excel for Windows (Microsoft 365) or Google Sheets; PostgreSQL or MySQL for preparing chart data; optionally Python 3.12 with pandas and matplotlib for section 15.14.

<!-- verbatim end -->

---

## 3. Project "Tools you'll need": Python and the build scripts

**Landed** (Part 2/3 build): no build-script names in Ch 18; `chart_examples.ipynb` was not created, because the chapter's own cells are the code.

**Destination:** → Ch 18 §18.11 / Ch 18 companion (finding 15.9 suggests `companion/ch18/chart_examples.ipynb`)

**Depends on:** Python 3.12, pandas 3.0.2, matplotlib 3.10; the two figure scripts live in `figures/` (build files, not reader files). The build script `companion/ch15/build_ch15_data.py` stays in the companion folder and is now described in `companion/ch15/README.md` for instructors (finding 15.10).


<!-- verbatim start -->

- **Python 3.12** with **pandas 3.0.2** and **matplotlib 3.10** (optional, section 15.14).
  - `companion/ch15/build_ch15_data.py`: rebuilds them from `companion/full/`.
  - `figures/make_figs15.py` and `make_figs15_diagrams.py`: the code for every figure in this chapter, including the project's before and after charts.

<!-- verbatim end -->

---

## 4. Project: step 4 wording and the Python stretch goal

**Landed** in Ch 18's project stretch goal (rebuild the five redesigned charts with `style_axes`) (Part 2/3 build).

**Destination:** → Ch 18 §18.11 exercises (stretch goal: "Rebuild all five redesigns in Python with one `style_chart(ax, title)` function")

**Depends on:** the five redesigns of Ch 15's project (Figure 15.16, data in `companion/ch15/ch15_chart_data.xlsx` sheets `product_2025`, `margin_by_year`, `region_2025`, `rep_month_2025`, `region_month_2025`), matplotlib `Axes`. In Ch 15, step 4 now reads "in Excel or Google Sheets".


<!-- verbatim start -->

4. **Build the redesign** in Excel, Google Sheets, or Python from the chart data. Sort, remove clutter, label directly, choose colors deliberately, and start bars at zero.

- Rebuild all five in Python with a single `style_chart(ax, title)` function that applies your rules, so every chart comes out consistent.

<!-- verbatim end -->

---

## 5. §15.9 Maps: "or Python"

**Landed** as one sentence on maps in Ch 18 §18.11 (Part 2/3 build).

**Destination:** → Ch 18 §18.11 (optional mention of map libraries); nothing else to place

**Depends on:** nothing. Ch 15 now reads "BI tools such as Power BI (Chapter 16) are better."


<!-- verbatim start -->

**Excel:** **Insert → Maps → Filled Map** shades countries, states, and districts from place names (it looks names up online, so it needs an internet connection and can misread ambiguous names). **Google Sheets:** **Chart type → Geo chart** for countries and regions. For city-level symbol maps with custom boundaries, BI tools (Power BI's map visuals, Chapter 16) or Python are better.

<!-- verbatim end -->

---

## 6. "Check yourself": the code bullet

**Landed** in Ch 18's Check yourself (Part 2/3 build).

**Destination:** → Ch 18 "Check yourself" (e.g. "You can apply Chapter 15's chart rules in matplotlib")

**Depends on:** Ch 18 §18.11. Ch 15 now reads "You can build all of this in Excel or Google Sheets."


<!-- verbatim start -->

- [ ] You can build all of this in Excel or Google Sheets, and recognize the same principles in code.

<!-- verbatim end -->

---

## 7. Exercises: the Python route in the intro and in exercise 9

**Landed** in Ch 18's exercises introduction and exercise 22 (box plots) (Part 2/3 build).

**Destination:** → Ch 18 §18.11 exercises ("Redo Chapter 15's exercise 9 box plots with `ax.boxplot` or seaborn")

**Depends on:** `companion/ch15/chart_data/order_values_2025.csv`. Ch 15 now names only Excel and Google Sheets.


<!-- verbatim start -->

Use `companion/ch15/ch15_chart_data.xlsx` (or the CSV files), the `riverstone_full` database, and Excel, Google Sheets, or Python.

9. Build box plots of order value by segment (Excel's Box and Whisker, or Python). Using the SQL output in section 15.5, what's the IQR of Wholesale orders, and what's the 1.5 × IQR upper fence?

<!-- verbatim end -->

---

## 8. Exercise 22 (Stretch) and its answer

**Landed** in Ch 18 as exercise 31 and its answer, with Figure 18.4; the signature is reconciled as `highlight_lines(ax, df, focus)` in both (Part 2/3 build).

**Destination:** → Ch 18 §18.11 exercises and answers

**Depends on:** pandas `read_csv`/`set_index`, matplotlib `Axes.plot`, `ax.text`, `ax.set_title`, `ax.spines`, f-strings; data `companion/ch15/chart_data/rep_month_2025.csv` (one column per rep, index = month 1–12); Ch 15 Figure 15.11 (the highlight idea). The answer shows no output: when placed, call it for two reps and show the two real charts. In Ch 15 the Stretch set is renumbered: old 23 (palette) is now 22. Note when placing: the exercise names `highlight_lines(df, focus)` but the answer's function also takes `ax`; make them agree.


<!-- verbatim start -->

22. In Python, write a function `highlight_lines(df, focus)` that draws every column of a month-by-rep table in light gray and the `focus` column in orange with a direct label. Use it for two different reps.

**22.** One solution:

```
def highlight_lines(df, focus, ax):
    for col in df.columns:
        if col != focus:
            ax.plot(df.index, df[col] / 1e7, color="#dfe5ec", linewidth=1)
    ax.plot(df.index, df[focus] / 1e7, color="#c0662b", linewidth=2.5)
    ax.text(df.index[-1] + 0.2, df[focus].iloc[-1] / 1e7, focus, color="#c0662b", va="center")
    ax.set_title(f"{focus} against the rest of the team", loc="left", fontweight="bold")
    ax.spines[["top", "right"]].set_visible(False)
```

Call it with `rep = pd.read_csv("chart_data/rep_month_2025.csv").set_index("month")` and, for example, `"Rahul Mehta"` and `"Simran Kaur"`.

<!-- verbatim end -->

---

## 9. Answer 13: the pandas clause

**Landed** in Ch 18 as exercise 23 (`.corr()` = 0.916) (Part 2/3 build).

**Destination:** → Ch 18 §18.11 or §18.6 exercises ("check Chapter 15's correlation of 0.916 with `.corr()`")

**Depends on:** `companion/ch15/chart_data/customers_2025.csv` read into `df`. Ch 15's answer 13 now keeps only `=CORREL`.


<!-- verbatim start -->

**13.** **0.916** (for example `=CORREL(C2:C4600, D2:D4600)` in Excel on the `customers_2025` sheet, or `df[["orders", "net_revenue"]].corr()` in pandas).

<!-- verbatim end -->
