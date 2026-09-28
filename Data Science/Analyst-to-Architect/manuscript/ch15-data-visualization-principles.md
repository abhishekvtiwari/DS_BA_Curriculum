# Chapter 15. Data Visualization Principles

*Part 2 — The Analyst*

> **Chapter at a glance**
>
> **You will learn to:** explain how people read charts, and why position and length beat angle, area, and color · start from the question and pick the chart that answers it · build clear bar, line, histogram, box, scatter, stacked, waterfall, heatmap, and map charts, and know when each fails · use color with meaning: one highlight, sequential and diverging palettes, color-blind-safe choices · write titles that state the finding and annotations that explain it · remove clutter without removing information · recognize misleading charts (truncated axes, dual axes, 3D, cherry-picked ranges) and avoid making them · show missing and uncertain data openly · make charts accessible · build the charts in Excel and Google Sheets · redesign a poor management pack.
>
> **Before you start:** Chapter 1 (levels of measurement), Chapter 4 (averages (mean vs median), percentages, and the chart checks in section 4.7), Chapter 10 and 11 (spreadsheets and pivot tables), and Chapter 13 (SQL aggregation). Chapter 14 helps: charts of dirty data are wrong however well they're drawn.
>
> **Time needed:** 12–15 hours of reading and practice, spread over two weeks.
>
> **Tools:** Excel for Windows (Microsoft 365) or Google Sheets; PostgreSQL or MySQL for preparing chart data.
>
> **Practice data:** `companion/ch15/ch15_chart_data.xlsx`, one sheet for every chart in this chapter, made from the full Riverstone dataset. The same tables are in `companion/ch15/chart_data/` as CSV files, and every table can be rebuilt from `riverstone_full` with SQL like the queries in this chapter.

---

## Why this matters

Most people who see your analysis will never see your spreadsheet, your SQL, or your cleaning log. They'll see a chart, for a few seconds, on a slide or a dashboard, often on a phone. What they understand in those seconds is what your analysis *says*, whatever the numbers underneath.

A good chart makes the important thing obvious: October is the peak, Wholesale orders are larger, one branch is behind. A poor chart hides it in a legend with eleven colors, or worse, invents a story that isn't there: a bar that looks twice as tall because the axis starts at 90%, a margin line that seems to follow revenue because someone chose two scales that make it.

Visualization is also one of the most visible analyst skills. Hiring managers look at portfolio charts before anything else, interviewers ask "what's wrong with this chart?", and a single clear chart in a review meeting does more for an analyst's reputation than a hundred correct queries nobody sees.

The good news is that clear charts follow a small number of principles, backed by research on how people see. This chapter teaches those principles with Riverstone's full three-year dataset, shows each one as a before-and-after, and ends with a makeover of Riverstone's old management pack.

---

## In plain English

Think about the display board at a railway station. Hundreds of people glance at it while walking. The board's designers had one job: let each person find their train, platform, and time in a couple of seconds.

So the board lists trains in time order (sorted, so your eye knows where to look). Every row has the same layout (consistent). Platform numbers are large (the thing people need most is the most visible). Cancelled trains are shown in red, and only cancelled trains (color has one meaning). There's no decoration, no 3D effect, no logo in the middle.

A chart is the same kind of object. Its reader is busy. Your job isn't to show everything you know; it's to make one message quick to find and hard to misread:

- **Choosing a chart** is choosing the layout that fits the question, like a timetable for times or a map for locations.
- **Sorting and labeling** are what let the eye find the answer without searching.
- **Color with meaning** is the red for cancellations: used for one thing, so it stands out.
- **A title that states the finding** is the announcement over the speaker: "the 18:05 to Pune leaves from platform 4".
- **Honesty** is the board showing the real platform, not the one that would make the station look efficient.

---

## 15.1 How people read charts

When someone looks at a chart, their eyes and brain decode it: they turn shapes back into numbers and comparisons. Some shapes decode quickly and accurately; others are slow and misleading. Choosing a chart is mostly choosing an encoding that people decode well.

### The accuracy ranking

In a famous study in 1984, William Cleveland and Robert McGill asked people to judge values shown in different ways, and measured how accurate they were. Later studies have broadly confirmed their ranking, from most to least accurate:

1. **Position along a common scale** (dots or bar ends against the same axis)
2. **Position along non-aligned scales** (the same axis repeated in separate panels)
3. **Length** (bars that start at the same baseline), **direction**, and **angle**
4. **Area** (bubbles, treemaps)
5. **Volume** and **curvature**
6. **Color saturation** and **shading** (lighter and darker)

The practical rule: **encode the most important comparison with position or length**. Use angle, area, and color for secondary information, or when the exact value doesn't matter.

Figure 15.1 shows why. Riverstone's 2025 revenue by segment is drawn twice.

![Left: a pie chart of Riverstone's 2025 revenue by segment, where the Wholesale and Hospitality slices look almost the same. Right: the same data as a horizontal bar chart, sorted, with values: Retail ₹55.6 crore (48.5%), Wholesale ₹31.3 crore (27.3%), Hospitality ₹27.7 crore (24.2%)](figures/fig15-1-pie-vs-bar.svg)

*Figure 15.1 — The same three numbers. In the pie, comparing Wholesale with Hospitality means judging two angles; in the bar chart, it means comparing two lengths against one axis.*

In the pie, is Wholesale bigger than Hospitality? Most people can't tell: 27.3% and 24.2% are angles of 98° and 87°, drawn in different orientations. In the bar chart, the difference is visible at a glance, and the labels give the exact values.

The data for the chart comes from the full dataset (the `sales_lines` view from Chapter 13, section 13.2, which excludes cancelled orders). Every piece of the query is from Chapters 12 and 13, but it's built here in three small steps, so you can see what each piece adds.

**Step 1: one total per segment.** Join each sales line to its customer to get the segment, keep 2025, and add up revenue for each segment:

<!-- db: riverstone_full -->

```sql
SELECT c.segment, SUM(s.net_revenue) AS net_revenue
FROM sales_lines s JOIN customers c ON c.customer_id = s.customer_id
WHERE s.order_date BETWEEN '2025-01-01' AND '2025-12-31'
GROUP BY c.segment;
```

```
   segment   |           net_revenue            
-------------+----------------------------------
 Hospitality | 277476705.0000000000000000000000
 Retail      | 556436453.7500000000000000000000
 Wholesale   | 312728492.5000000000000000000000
(3 rows)
```

How it works:

- `FROM sales_lines s JOIN customers c ON c.customer_id = s.customer_id` gives each sales line its customer's row, so the line knows its `segment` (the join from Chapter 12, section 12.10; `s` and `c` are short aliases).
- `WHERE s.order_date BETWEEN '2025-01-01' AND '2025-12-31'` keeps only 2025.
- `GROUP BY c.segment` with `SUM(s.net_revenue)` makes one row per segment with its total.

The totals are right, but the long decimals are hard to read and the rows aren't in any useful order.

**Step 2: round and sort.** `ROUND(...)` with no second argument rounds to whole rupees, and `ORDER BY net_revenue DESC` puts the biggest segment first, the order the bar chart needs:

```sql
SELECT c.segment, ROUND(SUM(s.net_revenue)) AS net_revenue
FROM sales_lines s JOIN customers c ON c.customer_id = s.customer_id
WHERE s.order_date BETWEEN '2025-01-01' AND '2025-12-31'
GROUP BY c.segment
ORDER BY net_revenue DESC;
```

```
   segment   | net_revenue 
-------------+-------------
 Retail      |   556436454
 Wholesale   |   312728493
 Hospitality |   277476705
(3 rows)
```

**Step 3: add each segment's share.** A share is the segment's total divided by the total of all segments. The all-segment total is a window over the grouped result:

```sql
SELECT c.segment, ROUND(SUM(s.net_revenue)) AS net_revenue,
       ROUND(100 * SUM(s.net_revenue) / SUM(SUM(s.net_revenue)) OVER (), 1) AS share_pct
FROM sales_lines s JOIN customers c ON c.customer_id = s.customer_id
WHERE s.order_date BETWEEN '2025-01-01' AND '2025-12-31'
GROUP BY c.segment
ORDER BY net_revenue DESC;
```

```
   segment   | net_revenue | share_pct 
-------------+-------------+-----------
 Retail      |   556436454 |      48.5
 Wholesale   |   312728493 |      27.3
 Hospitality |   277476705 |      24.2
(3 rows)
```

How the new line works:

- `SUM(s.net_revenue)` on its own is each segment's total, as in step 1.
- `SUM(SUM(s.net_revenue)) OVER ()`: the inner `SUM` makes each segment's total (it belongs to `GROUP BY`); the outer `SUM ... OVER ()` adds those three totals across all rows, so every row can see the grand total of about ₹1,14,66,41,651. The empty `OVER ()` means "the window is every row". Chapter 13, section 13.3, showed why a window can wrap an aggregate: grouping happens first.
- `100 * ... / ...` turns the ratio into a percentage, and `ROUND(..., 1)` keeps one decimal place.

The three shares add up to 100.0%, and Retail's 48.5% is the "almost half" the bar chart shows.

### What the eye notices first

Some visual differences are noticed before a person consciously looks for them, in a fraction of a second. These **pre-attentive attributes** include **color** (one orange bar among gray ones), **size**, **position**, **orientation**, **enclosure** (a box around something), and **added marks** (an arrow or a label). They're the tools for directing attention.

Two consequences:

- **One highlight works; many don't.** A single orange line among gray ones pops out instantly. Eleven colors don't pop out at all; the reader has to match each one to a legend, one by one (section 15.10).
- **Every difference looks meaningful.** If bars are different colors "for variety", readers assume the colors mean something. Don't encode anything you don't intend to communicate.

### Working memory is small

People can hold only a few things in mind at once. A legend with eight entries forces readers to remember eight color–name pairs while looking at the chart. That's why labeling lines and bars directly (the name next to the line, the value at the end of the bar) is almost always better than a legend, and why charts with more than about five or six categories in color usually need a different design.

> **Simplification note.** Perception research is more nuanced than a ranked list: accuracy depends on the task, the data, and the reader's familiarity with the chart type. The ranking is still the most useful single guide for everyday business charts, and it explains most of the rules in this chapter.

---

## 15.2 Start from the question

The most common charting mistake happens before any chart is drawn: starting from the data ("I have sales by month and region, what chart can I make?") instead of the question ("Is our festive peak getting bigger, and is it the same everywhere?"). The question decides the chart.

Figure 15.2 matches the kind of question to a chart. Three more questions sharpen the choice:

1. **Who is reading it, and where?** A CEO scanning a slide on a phone needs one message in large type. An analyst exploring data in a workbook can handle a detailed scatter plot.
2. **Explore or explain?** **Exploratory** charts are for you: quick, many, rough, to find what's interesting. **Explanatory** charts are for others: few, polished, each with one message. Most of this chapter is about explanatory charts; section 15.5's distributions are also your main exploratory tools.
3. **What should they do next?** If the chart should lead to a decision ("increase September stock"), design it so that decision is the obvious conclusion, with the evidence visible.

![A chart chooser with six rows. Compare categories: sorted bar chart. Show change over time: line chart. Show a distribution: histogram or box plot. Show a relationship: scatter plot. Show parts of a whole: stacked or 100% bar. Show where: map. Each row lists alternatives](figures/fig15-2-chart-chooser.svg)

*Figure 15.2 — Start from the kind of question, then choose the chart. The alternatives column matters: the first choice isn't always the best one for your data.*

### Levels of measurement decide what's allowed

Chapter 1 introduced **levels of measurement**. They constrain charts directly:

| Data | Examples | Chart implications |
|---|---|---|
| **Nominal** (categories with no order) | segment, city, product | Sort bars by value, not alphabetically; don't connect categories with lines |
| **Ordinal** (ordered categories) | size band, rating, month name | Keep the natural order; a line is acceptable across ordered periods |
| **Interval and ratio** (numbers) | revenue, quantity, order value | Histograms and box plots for distributions; scatter plots for relationships; bars need a zero baseline (ratio) |
| **Time** | order date, month | Time runs left to right; lines show continuity; equal time gaps need equal spacing |

A line joining Retail, Wholesale, and Hospitality implies a trend from one to the next that doesn't exist. A histogram of customer segments is really a bar chart. And a bar chart of temperatures in °C with a zero baseline misleads, because 0 °C isn't "no temperature" (interval data); a line or dot chart suits it better.

### The table is a chart choice too

When readers need **exact values** (a price list, a monthly target sheet) or need to **look up** one number among many, a well-formatted table beats a chart. Tables are also better for small numbers of values with different units. Section 15.8 shows how to make a table that works like a chart: aligned numbers, sensible rounding, and a heatmap-style shading.

---

## 15.3 Bar and column charts

**Bar charts** (horizontal) and **column charts** (vertical) compare values across categories by length. They're the workhorse of business reporting, and the easiest chart to make better.

![Left, before: a column chart of 2025 revenue for eight products in alphabetical order, with rotated labels and a different color for each column. Right, after: the same data as horizontal bars sorted from largest to smallest, in one gray, with values at the end of each bar](figures/fig15-3-sorted-bars.svg)

*Figure 15.3 — Riverstone's 2025 revenue by product. Sorting, turning the bars horizontal, labeling values, and using one color make the ranking readable in seconds.*

### Five rules for bars

1. **Start the value axis at zero.** A bar's length *is* its value. If the axis starts at ₹10 crore, a ₹20 crore bar looks twice as long as a ₹15 crore one, when it's only a third bigger. This is the one rule in this chapter with no exceptions for bars. (Lines and dots are different; section 15.4.)
2. **Sort by value** for nominal categories, so the ranking is visible. Keep the natural order for ordinal ones (months, size bands).
3. **Go horizontal when labels are long.** Product names such as "Food Container Set" fit on a horizontal bar chart without rotation; rotated text is slow to read.
4. **Label values directly** when exact numbers matter, and then remove the value axis and gridlines, which now repeat the labels.
5. **Use one color**, and add a second only to highlight something (section 15.10).

In Figure 15.3's "after" version, Storage Box 25L leads at ₹23.1 crore, and the two smallest products, Garden Chair (₹4.5 crore, sold only in March–May) and Water Bottle 1L (₹4.0 crore), together sell less than any other single product.

### Grouped and stacked bars

When each category splits into sub-groups, you have three choices:

- **Grouped (clustered) bars** put sub-groups side by side. Good for comparing sub-groups **within** each category, with up to about three or four sub-groups.
- **Stacked bars** put sub-groups on top of each other. Good for comparing **totals**, and the bottom segment; hard for middle segments, which don't share a baseline (section 15.7).
- **Small multiples**: a separate small bar chart for each sub-group, on the same scale. Often the clearest option once there are more than three sub-groups.

### Dot plots and lollipops

A **dot plot** replaces each bar with a dot on the value axis. Because dots encode by position, not length, the axis **doesn't need to start at zero**, which makes dot plots ideal for comparing values that are close together, such as attainment percentages between 92% and 112%. A **lollipop chart** is a dot with a thin line back to the axis: a lighter-looking bar, with the same zero-baseline rule as a bar.

### In Excel and Google Sheets

**Excel:** select the data, **Insert → Charts → Insert Column or Bar Chart → Clustered Bar**. To sort, sort the source data (largest at the bottom of the range for a horizontal bar chart, because Excel plots the first row nearest the axis origin), or tick **Format Axis → Axis Options → Categories in reverse order** on the category axis. Add values with **Chart Elements (+) → Data Labels**, then delete the value axis and gridlines. **Ctrl+1** opens the Format pane for whatever is selected.

**Google Sheets:** **Insert → Chart**, then in the **Chart editor → Setup → Chart type** choose **Bar chart**. Under **Customize → Series**, tick **Data labels**; under **Customize → Gridlines and ticks**, remove gridlines. Sort the source range first (**Data → Sort range**).

> **Watch out: pivot charts sort by the pivot.** A pivot chart (Chapter 11) follows the pivot table's order. Sort the pivot (**Row Labels → More Sort Options → Descending by Sum of net_revenue**) rather than the chart.

---

## 15.4 Line charts

**Line charts** show change over a continuous dimension, almost always time. The line itself tells the reader "these points are connected": each month follows the last.

![Left: one line through 36 months of Riverstone revenue from January 2023 to December 2025, rising overall with a peak every October, annotated at October 2025, ₹18.1 crore. Right: one line per year across January to December, labeled 2023, 2024, 2025, showing the same October peak each year at a higher level](figures/fig15-4-lines.svg)

*Figure 15.4 — The same 36 months, two ways. The continuous line shows growth over time; one line per year makes the seasonal pattern simple to compare.*

The left chart answers "how has revenue changed over three years?": clear growth, with a yearly rhythm. The right chart answers "is every year's season the same shape?": yes, weak June–July and a peak in October, at a higher level each year. Same data, different question, different chart.

The data behind the right chart is a pivot of month against year:

```sql
SELECT EXTRACT(MONTH FROM order_date) AS month,
       ROUND(SUM(net_revenue) FILTER (WHERE EXTRACT(YEAR FROM order_date) = 2024)) AS rev_2024,
       ROUND(SUM(net_revenue) FILTER (WHERE EXTRACT(YEAR FROM order_date) = 2025)) AS rev_2025
FROM sales_lines WHERE order_date >= '2024-01-01' GROUP BY 1 ORDER BY 1;
```

```
 month | rev_2024  | rev_2025  
-------+-----------+-----------
     1 |  64063515 |  85195521
     2 |  58632364 |  78582579
     3 |  78193384 | 101009066
     4 |  72534870 |  95194709
     5 |  66888391 |  87249568
     6 |  39531504 |  51972483
     7 |  30515645 |  40028093
     8 |  57166214 |  71835346
     9 |  87548908 | 111701479
    10 | 147221566 | 180620103
    11 | 127896564 | 155985902
    12 |  72822552 |  87266804
(12 rows)
```

How it works:

- `EXTRACT(MONTH FROM order_date)` turns each date into its month number, 1 to 12 (Chapter 12, section 12.8).
- `SUM(net_revenue) FILTER (WHERE EXTRACT(YEAR FROM order_date) = 2024)` adds up only the 2024 rows; the next line does the same for 2025. This is the pivot pattern from Chapter 13 (Pattern 9), with years as the columns.
- `WHERE order_date >= '2024-01-01'` leaves out 2023, which this table doesn't need.
- `GROUP BY 1` means "group by the first column in the `SELECT` list" (here, the month). It saves retyping a long expression. `ORDER BY 1` works the same way: sort by the first column.

October 2025 (₹18,06,20,103) was 22.7% above October 2024 (₹14,72,21,566): the kind of comparison the year-over-year chart makes visible.

### Rules for lines

1. **Time runs left to right, with equal spacing for equal time.** If a month is missing, leave a gap or mark it; don't let the chart squeeze the axis so that a two-month jump looks like one month.
2. **The zero baseline is optional.** A line encodes by position, not length, so the axis can start near the data when **change** is the message. But say so with a clearly labeled axis, and don't zoom in so far that noise looks like drama (section 15.12).
3. **Label lines directly** at their right-hand end instead of using a legend. The right chart in Figure 15.4 does this.
4. **Limit the number of lines.** Up to about four or five lines are readable. Beyond that, highlight one or two and gray the rest (section 15.10), or use small multiples.
5. **Use markers only when the points matter.** Markers on 36 monthly points add clutter; markers on 5 yearly points help.
6. **Don't use a line for categories.** A line from Retail to Wholesale suggests a trend that doesn't exist (section 15.2).

### Annotate events

A line chart becomes an explanation when it says *why* something happened: "price increase", "new Kolkata branch system", "festive season". Add a short annotation at the point, with a thin leader line if needed. One to three annotations are usually enough.

### Dual axes, and why to avoid them

A **dual-axis chart** plots two measures with different units against two vertical axes, for example revenue on the left and gross margin percentage on the right. It looks efficient and misleads readily, because **the chart-maker chooses both scales**, and so chooses where the lines cross and whether they appear to move together. Section 15.12 shows a Riverstone example. Better alternatives: two small charts stacked with aligned time axes; or index both measures to 100 at the start and plot them on one axis; or put the second measure in labels.

### Column charts for few periods, sparklines for many series

For a handful of periods (four quarters, three years), a **column chart** is often clearer than a line, because each period is a separate, comparable total. For many series in a table (a sparkline per branch), Excel's **Insert → Sparklines → Line** and Google Sheets' `=SPARKLINE(B2:M2)` draw a tiny line inside a cell: no axes, only the shape.

---

## 15.5 Distributions: histograms and box plots

Averages hide shape. Chapter 4 showed that only 70 of Riverstone's 173 orders were above the "average" order: one number hid the shape of the data. **Distribution charts** show the shape: where most values are, how spread out they are, whether the data is skewed, and where the outliers are (Chapter 14, section 14.6).

### Histograms

A **histogram** groups a numeric variable into **bins** (ranges of equal width) and draws a bar for the count in each bin. The bars touch, because the bins are continuous.

A coarse first look at Riverstone's 46,356 non-cancelled 2025 orders, in ₹25,000 bins:

```sql
WITH order_values AS (
  SELECT order_id, SUM(net_revenue) AS order_value FROM sales_lines
  WHERE order_date BETWEEN '2025-01-01' AND '2025-12-31' GROUP BY order_id
)
SELECT FLOOR(order_value / 25000) * 25000 AS bin_start, COUNT(*) AS orders
FROM order_values GROUP BY 1 ORDER BY 1;
```

```
 bin_start | orders 
-----------+--------
         0 |  27627
     25000 |  14222
     50000 |   3718
     75000 |    657
    100000 |    122
    125000 |     10
(6 rows)
```

How it works:

- The CTE `order_values` (Chapter 13, section 13.2) adds up each order's lines, so there is one row per order with its `order_value`.
- `FLOOR(order_value / 25000) * 25000` assigns every order to the start of its bin. `FLOOR` rounds a number **down** to the whole number below it, like Chapter 11's `FLOOR.MATH`. By hand, for an order of ₹37,480: 37,480 ÷ 25,000 = 1.4992; `FLOOR` makes it 1; 1 × 25,000 = 25,000, so the order falls in the ₹25,000–₹49,999 bin.
- `COUNT(*)` with `GROUP BY 1` counts the orders in each bin, and `ORDER BY 1` lists the bins from the lowest.

Most orders are under ₹25,000, and the counts fall quickly after that: a **right-skewed** distribution, common for money.

Six bars is only a first look. What happens if you change the bin width? **Before you run the next query, predict:** with bins five times narrower (₹5,000), roughly how many bars will there be, and will the tallest bar still be the first one? The only change is `25000` to `5000`, in both places:

```sql
WITH order_values AS (
  SELECT order_id, SUM(net_revenue) AS order_value FROM sales_lines
  WHERE order_date BETWEEN '2025-01-01' AND '2025-12-31' GROUP BY order_id
)
SELECT FLOOR(order_value / 5000) * 5000 AS bin_start, COUNT(*) AS orders
FROM order_values GROUP BY 1 ORDER BY 1;
```

```
 bin_start | orders 
-----------+--------
         0 |   4005
      5000 |   6146
     10000 |   6210
     15000 |   6239
     20000 |   5027
     25000 |   4107
     30000 |   3648
     35000 |   2700
     40000 |   2117
     45000 |   1650
     50000 |   1227
     55000 |    936
     60000 |    669
     65000 |    512
     70000 |    374
     75000 |    244
     80000 |    167
     85000 |    119
     90000 |     73
     95000 |     54
    100000 |     49
    105000 |     31
    110000 |     21
    115000 |     14
    120000 |      7
    125000 |      5
    130000 |      1
    135000 |      3
    140000 |      1
(29 rows)
```

Twenty-nine bars, and the tallest is no longer the first. Orders under ₹5,000 (4,005) are fewer than those in each ₹5,000 band from ₹5,000 to ₹20,000 (about 6,200 each): the typical order is ₹5,000–₹20,000, and the ₹25,000 bins hid that. This is the histogram to show; the six-bin version was only a quick look.

The **bin width** changes what you see:

![Three histograms of 2025 order values. With ₹1,000 bins the bars are jagged. With ₹5,000 bins a clear shape appears: a peak around ₹10,000–20,000 and a long tail to the right. With ₹25,000 bins there are only six bars and the shape is hidden](figures/fig15-5-histogram-bins.svg)

*Figure 15.5 — The same 46,356 orders in three bin widths. Too narrow shows noise; too wide hides the shape.*

There's no single right bin width. Start with a round number that gives roughly 20–40 bins over the range (₹5,000 gives 29 here), then try a narrower and a wider one. If the story changes, say which one you're showing and why.

### Box plots

A **box plot** (box-and-whisker plot) summarizes a distribution in five numbers, so several groups can be compared side by side:

- The **box** spans the **first quartile (Q1)** to the **third quartile (Q3)**: the middle 50% of values. Its length along the value axis is the **interquartile range (IQR)**.
- The line inside is the **median**.
- The **whiskers** reach to the most extreme values within 1.5 × IQR of the box (the most common convention).
- Points beyond the whiskers are drawn individually: potential outliers.

### Quartiles by hand

**Quartiles** split sorted values into four equal parts: a quarter of the values are below Q1, half below the median, and three quarters below Q3. Work one small example by hand before letting a tool do it. Palm Trading Co, a Wholesale customer in Mangaluru, placed nine orders in 2025. Sorted from smallest to largest:

| Position | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 |
|---|---|---|---|---|---|---|---|---|---|
| Order value (₹) | 9,678 | 15,136 | 19,292 | 20,520 | 25,865 | 27,960 | 39,975 | 62,335 | 99,680 |

1. **Median:** the middle value, the 5th of 9: **₹25,865**.
2. **Q1:** the middle of the lower half. The lower half is positions 1 to 5 (up to and including the median), and its middle is the 3rd value: **₹19,292**.
3. **Q3:** the middle of the upper half, positions 5 to 9: the 7th value, **₹39,975**.
4. **IQR** = Q3 − Q1 = 39,975 − 19,292 = **₹20,683**.
5. **Upper fence** = Q3 + 1.5 × IQR = 39,975 + 1.5 × 20,683 = 39,975 + 31,024.50 = **₹70,999.50**. The ₹99,680 order is above it, so a box plot draws it as a separate dot, and the upper whisker stops at ₹62,335, the largest order inside the fence. The lower fence, 19,292 − 31,024.50, is below zero, so no order is unusually small; the lower whisker reaches ₹9,678.

The spreadsheet does the same with functions you met in Chapter 11, section 11.3. With the nine values in `A2:A10`:

```excel
=MEDIAN(A2:A10)          → 25865
=QUARTILE.INC(A2:A10,1)  → 19292
=QUARTILE.INC(A2:A10,3)  → 39975
```

The second argument of `QUARTILE.INC` says which quartile: 1 for Q1, 3 for Q3 (2 would be the median). With nine values, the hand method and `QUARTILE.INC` agree exactly. With other counts they can differ slightly, because `QUARTILE.INC` **interpolates**: when a quartile falls between two values, it takes a point part of the way between them. Report the tool's answer, and say which tool you used. Chapter 21 treats quartiles and percentiles properly.

### Box plots for the three segments

For all 46,356 orders of 2025, the `order_values_2025` sheet of the practice workbook has one row per order: `order_id` in column A, `segment` in B, and `order_value` in C. `FILTER` (Chapter 11, section 11.6) hands `QUARTILE.INC` only one segment's orders. For Wholesale:

```excel
=QUARTILE.INC(FILTER(C2:C46357, B2:B46357="Wholesale"), 1)   → 13340
=MEDIAN(FILTER(C2:C46357, B2:B46357="Wholesale"))            → 25762.5
=QUARTILE.INC(FILTER(C2:C46357, B2:B46357="Wholesale"), 3)   → 43826.25
```

Change `"Wholesale"` to `"Retail"` or `"Hospitality"` for the other segments. Rounded to whole rupees:

| Segment | Orders | Q1 (₹) | Median (₹) | Q3 (₹) | Largest (₹) |
|---|---:|---:|---:|---:|---:|
| Hospitality | 12,432 | 10,212 | 19,122 | 31,000 | 1,15,550 |
| Retail | 23,865 | 10,750 | 19,425 | 32,275 | 1,13,430 |
| Wholesale | 10,059 | 13,340 | 25,762 | 43,826 | 1,43,175 |

(Hospitality's Q1 is ₹10,212.50 and Wholesale's median ₹25,762.50 before rounding.)

### The same numbers in SQL (optional, PostgreSQL)

PostgreSQL can calculate quartiles too, with a function you haven't met yet. This is optional: the spreadsheet route above gives the same numbers.

```sql
WITH order_values AS (
  SELECT s.order_id, c.segment, SUM(s.net_revenue) AS order_value
  FROM sales_lines s JOIN customers c ON c.customer_id = s.customer_id
  WHERE s.order_date BETWEEN '2025-01-01' AND '2025-12-31'
  GROUP BY s.order_id, c.segment
)
SELECT segment, COUNT(*) AS orders,
       ROUND(PERCENTILE_CONT(0.25) WITHIN GROUP (ORDER BY order_value)) AS q1,
       ROUND(PERCENTILE_CONT(0.5)  WITHIN GROUP (ORDER BY order_value)) AS median,
       ROUND(PERCENTILE_CONT(0.75) WITHIN GROUP (ORDER BY order_value)) AS q3,
       ROUND(MAX(order_value)) AS max
FROM order_values GROUP BY segment ORDER BY median;
```

```
   segment   | orders |  q1   | median |  q3   |  max   
-------------+--------+-------+--------+-------+--------
 Hospitality |  12432 | 10212 |  19122 | 31000 | 115550
 Retail      |  23865 | 10750 |  19425 | 32275 | 113430
 Wholesale   |  10059 | 13340 |  25762 | 43826 | 143175
(3 rows)
```

How it works:

- The CTE `order_values` makes one row per order, now with the customer's `segment` from the join.
- `PERCENTILE_CONT(0.25)` asks for the value a quarter (0.25) of the way through the sorted values: Q1. `0.5` is the median and `0.75` is Q3. "CONT" stands for continuous: like `QUARTILE.INC`, it interpolates between two values when needed, which is why the results match the spreadsheet.
- `WITHIN GROUP (ORDER BY order_value)` says which column to sort before counting a quarter of the way through. It's needed because a percentile only makes sense on sorted values.
- `GROUP BY segment` makes the calculation run once per segment, like `SUM` does; `ROUND(...)` gives whole rupees, and `MAX(order_value)` is the largest order.
- `ORDER BY median` sorts the segments from the smallest median.

`PERCENTILE_CONT` is PostgreSQL's; MySQL doesn't have it, so in MySQL use the spreadsheet route above or the window-function query in section 15.15.

![Horizontal box plots of 2025 order values for Hospitality, Retail, and Wholesale. Wholesale's box is further right and wider, with median ₹25,762; Retail's median is ₹19,425 and Hospitality's ₹19,122. All three have many individual dots to the right of the whiskers](figures/fig15-6-box-plots.svg)

*Figure 15.6 — Box plots compare distributions across groups. Wholesale orders are larger and more variable; Retail and Hospitality are nearly identical.*

The box plots show what a bar chart of averages would hide: Retail and Hospitality orders are almost identical in size (medians ₹19,425 and ₹19,122), while the middle half of Wholesale orders spans ₹13,340 to ₹43,826. All three segments have a long right tail of large orders, shown as dots. For money data those dots are usually real big orders, not errors: the IQR rule flags *unusual* values, and Chapter 14's business limits decide whether they're wrong.

> **Watch out: box plots hide the number of values and gaps.** A box from 12 orders looks as solid as one from 12,000, and a box plot can't show that a distribution has two peaks. Add the count to the label, and look at a histogram as well when exploring.

### Other distribution charts

- **Strip plots and dot plots** draw every value as a dot along one axis, with a little random vertical **jitter** so dots don't hide each other. Best for small groups (up to a few hundred values).
- **Density curves** smooth a histogram into a line. Good for comparing a few overlapping distributions; harder to explain to a business audience.
- **Violin plots** mirror a density curve around a center line. Common in data science, rarely needed in business reports.

### In Excel and Google Sheets

**Excel** (2016 and later): select the order values, **Insert → Insert Statistic Chart → Histogram**; set the bin width in **Format Axis → Axis Options → Bin width**. **Insert → Insert Statistic Chart → Box and Whisker** draws box plots; with a category column next to the values, it draws one box per category. Excel's box plot uses its own quartile method (**Inclusive** or **Exclusive median**, set in **Format Data Series**), which can differ slightly from `QUARTILE.INC`.

**Google Sheets:** **Insert → Chart → Chart type → Histogram chart**, with **Customize → Histogram → Bucket size**. Sheets has no built-in box plot; the usual workaround is a candlestick chart built from Q1, median, Q3, minimum, and maximum, or `QUARTILE.INC` values in a table.

---

## 15.6 Relationships: scatter plots

A **scatter plot** places each record at the position of two numeric values, one on each axis. It answers "do these two measures move together?", and it's the chart most likely to reveal something a summary number hides.

The usual summary number for a relationship is the **correlation**: a number from −1 to +1 that says how closely two measures follow a straight line together. +1 is a perfect rising line, 0 is no straight-line pattern, and −1 is a perfect falling line. In a spreadsheet, `=CORREL(range1, range2)` returns it, with the two measures in two ranges of the same length. Chapter 21 shows how it's calculated and where it misleads; the next example shows the first warning.

### Why you must look: Anscombe's quartet

In 1973 the statistician Francis Anscombe published four small datasets designed to make one point. Each has 11 points. In all four, the mean of x is 9, the mean of y is 7.50, the correlation between x and y is 0.82, and the best-fitting straight line is the same: y = 3.00 + 0.500x. By every summary statistic, they're the same data.

![Four scatter plots with identical trend lines. Dataset 1 is a loose linear cloud. Dataset 2 is a smooth curve. Dataset 3 is a tight straight line with one outlier. Dataset 4 is a vertical column of points at x = 8 with one far point at x = 19](figures/fig15-7-anscombe.svg)

*Figure 15.7 — Anscombe's quartet. Identical summaries, four different relationships: roughly linear, curved, linear with an outlier, and no relationship except one influential point.*

Only the charts show that the second relationship is a curve, the third is a perfect line spoiled by one outlier, and the fourth has no relationship at all apart from a single point. You can check the numbers yourself with `anscombe.csv` in the chart data (exercise 14).

### Riverstone's customers: orders against revenue

Each dot in Figure 15.8 is one of the 4,599 customers who ordered in 2025, placed by their number of orders and their 2025 net revenue.

![Left: a scatter plot of 4,599 customers, orders in 2025 against net revenue, where dots form solid vertical stripes at each whole number of orders and hide each other. Right: the same data with small, transparent dots, slight horizontal jitter, and a color per segment, showing that Wholesale customers tend to sit higher for the same number of orders](figures/fig15-8-scatter.svg)

*Figure 15.8 — Overplotting hides how many customers sit in each area. Transparency and jitter reveal density; color adds the segment.*

The relationship is strong (a correlation of 0.916: customers who order more often spend more, which is hardly surprising) but the "before" chart hides **how many** customers sit at each point, because thousands of dots overlap. This is **overplotting**. The fixes:

- **Smaller, transparent dots**, so dense areas look darker.
- **Jitter**: a small random offset when one variable takes whole-number values (orders are 1, 2, 3…), so dots don't stack exactly.
- **A heatmap of binned values** (a 2D histogram) when there are tens of thousands of points.
- **Color for a category**, used sparingly: here, it shows that Wholesale customers tend to spend more per order.

### Rules for scatter plots

1. **Put the likely cause on the x-axis** and the effect on the y-axis (orders → revenue; discount → quantity).
2. **Start axes where the data is**, not necessarily at zero; scatter plots encode by position.
3. **Consider a log scale** when values span several orders of magnitude (Riverstone's 2025 customers range from under ₹5,000 to over ₹10 lakh). On a log scale, ₹1,000, ₹10,000, ₹1,00,000, and ₹10,00,000 are equally spaced: each step is ten times the last. Label it clearly ("log scale") because many readers won't notice.
4. **Add a trend line only if it helps**, and never let it stand in for looking at the points. Anscombe's quartet has the same trend line four times.
5. **Correlation isn't causation.** A scatter plot shows that two measures move together, not why (Chapter 21 and Chapter 22 return to this).

**Excel:** **Insert → Insert Scatter (X, Y) or Bubble Chart → Scatter**; add a trend line with **Chart Elements (+) → Trendline**; set transparency in **Format Data Series → Marker → Fill → Transparency**. **Google Sheets:** **Chart type → Scatter chart**; **Customize → Series → Trendline**; point size under **Customize → Series → Point size**.

---

## 15.7 Parts of a whole: stacked bars, pies, and waterfalls

### Stacked and 100% stacked bars

A **stacked bar** shows a total and its parts. A **100% stacked bar** shows only the shares, each bar reaching 100%.

![Left: stacked columns of Riverstone's 2025 revenue by month, split into Storage, Kitchen, Industrial, and Furniture, with the October total highest and Furniture present only in March to May. Right: a waterfall chart from 2024 revenue of ₹90.3 crore, adding Retail +₹11.3 crore, Wholesale +₹7.4 crore, and Hospitality +₹5.7 crore to reach ₹114.7 crore in 2025](figures/fig15-9-composition.svg)

*Figure 15.9 — Left: a stacked column chart shows monthly totals and the bottom segment clearly; the middle segments are hard to compare. Right: a waterfall explains a change from one total to another.*

The stacked chart answers "which months are biggest, and how much of each month is Storage?" well, because totals and the bottom segment (Storage) share a baseline. It answers "did Industrial grow from August to October?" badly: Industrial floats on top of Kitchen, so its segments start at different heights. If the middle segments matter, use small multiples or a grouped bar instead.

Keep stacks readable:

- **Put the most important or most stable segment at the bottom**, next to the baseline.
- **Use no more than four or five segments**; group the rest into "Other".
- **Keep the same order** in every bar, and in the legend (or label segments directly on the last bar).

### Pies: when they're acceptable

Pie charts are unpopular with visualization experts for the reasons in section 15.1: angles and areas are hard to compare. They're still acceptable when **all** of these are true:

- the parts add up to a meaningful whole (100% of something);
- there are **two or three** parts;
- the message is a simple share, such as "Retail is almost half of revenue";
- exact comparison between the parts isn't the point.

A **donut chart** is a pie with a hole; it has the same weaknesses and doesn't fix them. **3D pies** are never acceptable: the tilt makes front slices look bigger than back slices of the same size.

### Waterfall charts

A **waterfall chart** (bridge chart) explains how one total became another: a starting bar, floating bars for each positive or negative change, and an ending bar. It's the standard way to answer "why did revenue change?" in a management pack.

The right side of Figure 15.9 is built from the change by segment:

| Segment | 2024 (₹) | 2025 (₹) | Change (₹) |
|---|---:|---:|---:|
| Retail | 44,38,10,189 | 55,64,36,454 | +11,26,26,265 |
| Wholesale | 23,84,57,929 | 31,27,28,492 | +7,42,70,563 |
| Hospitality | 22,07,47,358 | 27,74,76,705 | +5,67,29,347 |
| **Total** | **90,30,15,475** | **1,14,66,41,651** | **+24,36,26,176** |

(The 2025 Wholesale figure is ₹31,27,28,492.50 before rounding, which is why section 15.1's query shows 312728493 and this table ₹31,27,28,492. Each figure is rounded on its own, so rows can differ from the total by ₹1.) Sorting the changes from largest to smallest shows at a glance that Retail contributed the most growth. Waterfalls also handle negative steps (a lost customer, a price cut), which are drawn downward, usually in a contrasting color.

**Excel** (2016 and later): **Insert → Insert Waterfall, Funnel, Stock, Surface, or Radar Chart → Waterfall**; then select the total bars and tick **Set as total** in **Format Data Point**. **Google Sheets:** **Chart type → Waterfall chart**; add the totals with **Customize → Series → Add subtotal**, or include them as rows and mark them.

### Treemaps

A **treemap** fills a rectangle with nested rectangles sized by value, for example every city within its region. It shows the biggest parts of a large hierarchy at once, but compares values by area, the weakest encoding for exact comparisons. Use it for "where is most of the revenue?" across dozens of categories, not for ranking.

---

## 15.8 Heatmaps and tables

A **heatmap** is a table whose cells are shaded by value. It's the best chart for a **two-way** question, such as "which months and which regions are strongest?", when there are too many combinations for bars or lines.

![Top: a heatmap of 2025 revenue by region (West, South, North, East, and City missing) and month, in shades of blue with values in each cell, darkest in West October at ₹6.0 crore. Bottom: a heatmap of monthly percentage of target for 2023 to 2025, from red below 100 to blue above 100, with 2025 January at 110 and February at 112 in blue and October at 92 in red](figures/fig15-10-heatmaps.svg)

*Figure 15.10 — Top: a sequential palette for amounts. Bottom: a diverging palette for performance against a midpoint (100% of target).*

The top heatmap shows two patterns at once: across the rows, West is the largest region every month; down the columns, October is the peak everywhere. The "City missing" row is the ₹2.3 crore of 2025 revenue from customers with no city (Chapter 14), kept visible instead of dropped.

The bottom heatmap shows **attainment**: revenue as a percentage of target, month by month. Because the meaningful midpoint is 100%, it uses a **diverging** palette: red for below target, blue for above, and near-white for on target. Two things stand out that a line chart of revenue would hide: 2025 started well above target (110% and 112% in January and February), and every month from August to December missed, with October the worst at 92%.

### Rules for heatmaps

1. **Choose the palette by the data** (section 15.10): sequential (light to dark) for amounts, diverging for above-and-below a meaningful midpoint.
2. **Put numbers in the cells** when readers need values, with text color that contrasts with the shade.
3. **Order rows and columns meaningfully:** time in order; categories sorted by total, or grouped.
4. **Don't compare rows with very different scales** in one color scale: one large region can wash out the others. Shade each row separately, or show percentages, if the within-row pattern is the point.

### Tables that work like charts

Chapter 10 and Chapter 11 formatted tables for reading; the same principles make a table an effective visual:

- **Right-align numbers** and use the same number of decimals, so digits line up.
- **Round to what matters.** ₹18.1 crore is easier to read than ₹18,06,20,103 on a management slide; keep full values in the appendix or the workbook.
- **Remove heavy borders**; light horizontal rules or alternating shading are enough.
- **Highlight with restraint:** conditional formatting (Excel: **Home → Conditional Formatting → Color Scales**; Sheets: **Format → Conditional formatting → Color scale**) turns a table into a heatmap; data bars (**Conditional Formatting → Data Bars**) add in-cell bars.
- **Add sparklines** for a trend beside each row (section 15.4).

---

## 15.9 Maps

A map is the right chart when **location itself** is part of the answer: which areas are close to each other, where the gaps are, how far customers are from a warehouse. It's often the wrong chart when location is only a label: "revenue by region" is a ranking question, and a sorted bar chart answers it more accurately than shaded shapes of different sizes.

Two common kinds:

- **Filled (choropleth) maps** shade each area (state, district) by a value. Their weakness: **big areas dominate visually**, regardless of their values, and small, dense areas (Mumbai, Delhi) almost disappear. Shade by rates or shares (revenue per customer, % of target), not raw totals, which mostly reflect population.
- **Symbol (dot or bubble) maps** place a marker at each location, sized or colored by value. Better for cities, and for showing concentration; bubbles compare by area, so add labels for key values.

For Riverstone, a map of 39 cities could show that revenue is concentrated along the west coast and in the metros. But "which cities bring the most revenue?" is better as a sorted bar chart of the top ten cities: Mumbai ₹9.7 crore, Delhi ₹8.6 crore, Bengaluru ₹7.0 crore, and so on.

**Excel:** **Insert → Maps → Filled Map** shades countries, states, and districts from place names (it looks names up online, so it needs an internet connection and can misread ambiguous names). **Google Sheets:** **Chart type → Geo chart** for countries and regions. For city-level symbol maps with custom boundaries, BI tools such as Power BI (Chapter 16) are better.

> **Watch out: maps and missing locations.** Customers with no city don't appear on a map at all, and nothing tells the reader they're missing. Say how much is missing in a note ("₹2.3 crore of revenue has no city and isn't shown").

---

## 15.10 Color with meaning

Color is the strongest pre-attentive attribute and the most abused. The principle: **color should mean something, and the same thing everywhere in a report.**

### Three kinds of palette

| Palette | Use for | Looks like | Riverstone example |
|---|---|---|---|
| **Categorical (qualitative)** | Unordered groups | Distinct hues of similar strength | Retail, Wholesale, Hospitality |
| **Sequential** | Ordered amounts, low to high | One hue from light to dark | Revenue by region and month |
| **Diverging** | Values around a meaningful midpoint | Two hues meeting at a light neutral | % of target around 100 |

Using the wrong kind is a common, subtle error. A rainbow (red, orange, yellow, green, blue) for an ordered amount has no natural "more" direction, and bright yellow in the middle draws the eye to middling values. A diverging palette for plain revenue invents a midpoint that means nothing.

### Highlight, don't decorate

The most effective use of color in business charts is **one highlight color against gray**, as Figure 15.11 shows.

![Left, before: eleven lines of monthly revenue per sales rep in eleven colors with a legend. Right, after: ten lines in light gray and one line, Rahul Mehta, in orange with a direct label, and a label for the ten other reps](figures/fig15-11-highlight.svg)

*Figure 15.11 — Eleven colors force the reader to decode a legend. Gray for context and one color for the story make the point immediately.*

The "before" chart asks the reader to match eleven colors to eleven names. The "after" chart has one message: Rahul Mehta leads, and every rep follows the same seasonal shape. If the next slide is about a different rep, highlight that rep instead; the gray context stays the same.

### Consistency across a report

- **Assign colors to things, not positions.** If Wholesale is green on one chart, it's green on every chart, even when it's the first bar instead of the second.
- **Keep "good" and "bad" colors consistent** and don't reuse them for categories. If red means "below target", don't also use red for the East region.
- **Use your organization's palette** where one exists, but check it against the rules below; brand colors aren't always readable.

### Color vision deficiency

About **1 in 12 men and 1 in 200 women** have some form of color vision deficiency, most often difficulty distinguishing red from green. In a management team of twelve men, the odds are good that at least one reader can't tell your red "missed" from your green "achieved".

- **Avoid red–green as the only distinction.** Use blue–orange or blue–red diverging palettes (Figure 15.10 uses red–blue).
- **Use color-blind-safe categorical palettes**, such as the **Okabe–Ito** palette, designed to stay distinct for common types of color vision deficiency.
- **Don't rely on color alone.** Add direct labels, patterns, markers, or position, so the chart still works in grayscale. Printing it in black and white is a quick test.
- **Simulate:** tools such as Coblis (a free web-based color-blindness simulator) and the accessibility checks in design tools show how a chart looks to people with different types of color vision.

### Contrast

Text and important marks need enough **contrast** with the background. The Web Content Accessibility Guidelines (WCAG) ask for a contrast ratio of at least **4.5:1** for normal text and **3:1** for large text and essential graphical elements such as lines and bars. Pale yellow on white fails; dark gray on white passes. Free contrast checkers (for example WebAIM's) calculate the ratio from two color codes.

**Excel:** **Page Layout → Colors** sets a workbook color theme; **Format Data Series → Fill** colors one series, and clicking a single bar twice selects only that bar. **Google Sheets:** **Customize → Series → Format data point** colors one bar; **Format → Theme** sets chart colors for the spreadsheet.

---

## 15.11 Titles, labels, annotations, and clutter

### Titles that state the finding

Most business charts have a **label** for a title: "Monthly Revenue vs Target 2025". It tells readers what they're looking at, and leaves them to work out what it means. An **action title** (or headline) states the finding, so the chart supports a sentence instead of starting a puzzle.

![Top: a line chart of 2025 monthly actual revenue and target titled Monthly Revenue vs Target 2025, with a legend. Bottom: the same chart titled 2025 finished at 98.3% of target: a strong January–February, then a Q4 short of an ambitious plan, with direct labels for Actual and Target and an annotation at October: ₹18.1 crore, a record month, but 92% of its ₹19.6 crore target](figures/fig15-12-titles.svg)

*Figure 15.12 — The same data. The top chart describes; the bottom chart explains, with a finding in the title, direct labels, and one annotation.*

The data behind it takes two steps: first each month's revenue, then the join to the targets. Step 1 is a CTE (Chapter 13, section 13.2) that totals revenue by month; the `LIMIT 3` is only there to check the first rows:

```sql
WITH monthly AS (
  SELECT DATE_TRUNC('month', order_date)::date AS m, SUM(net_revenue) AS revenue
  FROM sales_lines
  GROUP BY 1
)
SELECT m, ROUND(revenue) AS net_revenue
FROM monthly
WHERE m >= '2025-01-01'
ORDER BY m
LIMIT 3;
```

```
     m      | net_revenue 
------------+-------------
 2025-01-01 |    85195521
 2025-02-01 |    78582579
 2025-03-01 |   101009066
(3 rows)
```

How it works: `DATE_TRUNC('month', order_date)` rounds each date down to the first day of its month, and `::date` turns the result into a plain date (both from Chapter 12, section 12.8), so every order in January 2025 gets `2025-01-01`. `GROUP BY 1` adds up the revenue for each of those month starts. The dates look like `2025-01-01` because that's how `sales_targets` stores its months, which is what lets step 2 match them.

Step 2 keeps the CTE and replaces the final `SELECT` with a join to `sales_targets`:

```sql
WITH monthly AS (
  SELECT DATE_TRUNC('month', order_date)::date AS m, SUM(net_revenue) AS revenue
  FROM sales_lines
  GROUP BY 1
)
SELECT t.target_month, ROUND(a.revenue) AS net_revenue, t.target_revenue,
       ROUND(100 * a.revenue / t.target_revenue, 1) AS pct_of_target
FROM sales_targets t
JOIN monthly a ON a.m = t.target_month
WHERE t.target_month >= '2025-01-01'
ORDER BY t.target_month;
```

```
 target_month | net_revenue | target_revenue | pct_of_target 
--------------+-------------+----------------+---------------
 2025-01-01   |    85195521 |    77350000.00 |         110.1
 2025-02-01   |    78582579 |    70000000.00 |         112.3
 2025-03-01   |   101009066 |   108050000.00 |          93.5
 2025-04-01   |    95194709 |    96900000.00 |          98.2
 2025-05-01   |    87249568 |    85900000.00 |         101.6
 2025-06-01   |    51972483 |    50400000.00 |         103.1
 2025-07-01   |    40028093 |    36500000.00 |         109.7
 2025-08-01   |    71835346 |    76050000.00 |          94.5
 2025-09-01   |   111701479 |   118300000.00 |          94.4
 2025-10-01   |   180620103 |   196150000.00 |          92.1
 2025-11-01   |   155985902 |   158950000.00 |          98.1
 2025-12-01   |    87266804 |    92400000.00 |          94.4
(12 rows)
```

How it works:

- `JOIN monthly a ON a.m = t.target_month` puts each month's revenue next to that month's target (`a` is a short alias for the CTE, `t` for the targets table).
- `ROUND(100 * a.revenue / t.target_revenue, 1)` is the **attainment**: revenue as a percentage of target, to one decimal place.
- `WHERE t.target_month >= '2025-01-01'` keeps 2025, and `ORDER BY t.target_month` lists the months in order.

Over the whole year, revenue was 98.3% of target: ₹1,14,66,41,651 against ₹1,16,69,50,000. Five months beat their target: January, February, May, June, and July.

A good action title:

- **states one finding** in a full sentence or a strong phrase;
- **is true for the whole chart**, not only its most dramatic point;
- **uses numbers** where they carry the message (98.3%, ₹18.1 crore);
- **doesn't overclaim.** "Q4 short of an ambitious plan" is supported (October's target was ₹19.6 crore, 33% above October 2024's revenue); "Q4 collapsed" isn't (October was a record month).

Keep a smaller **subtitle** or axis title for the facts readers need to read the chart correctly: the measure, the unit, the period, and what's excluded ("Net revenue, ₹ crore, excluding cancelled orders").

> **Watch out: a headline is a claim.** An action title makes your interpretation the first thing people read. That's the point, and it's also a responsibility: check that someone who disagrees with you would still accept the title as a fair description of the data.

### Labels

- **Label lines and bars directly** instead of using a legend (section 15.1).
- **Label axes with units** (₹ crore, orders, %) and format numbers for reading: ₹18.1 crore or ₹18.1 cr, not 180620103.
- **Use Indian or international units consistently.** In India, lakh (₹1,00,000) and crore (₹1,00,00,000) are standard in business; international audiences expect millions. Say which, once, and never mix them in one chart.
- **Show only as many axis ticks as needed**: 0, 5, 10, 15, 20 is enough.

### Annotations

An **annotation** is a short note on the chart that explains a point: "record month", "new price list from April", "Kolkata data incomplete". Annotations turn an exploratory chart into an explanatory one. Use one to three, place them close to what they explain, and keep them short.

### Remove clutter

Edward Tufte's idea of the **data-ink ratio** (1983) is a useful discipline: the share of the ink on a chart that shows data. Remove anything that doesn't help the reader, then check that nothing useful went with it:

| Remove or reduce | Why |
|---|---|
| Heavy gridlines | Light gridlines, or none when values are labeled |
| Borders and chart backgrounds | They frame nothing |
| 3D effects, shadows, gradients | They distort lengths and add noise |
| Legends | Label directly |
| Redundant axis when values are labeled | The labels already give the numbers |
| Decimal places nobody needs | ₹18.1 crore, not ₹18.06201 crore |
| Tick marks and axis lines where they add nothing | Especially on bar charts with labels |
| Bold, italics, and several fonts | One font, two sizes, bold for the title |

> **Simplification note: minimalism has limits.** Stripping a chart to the bare minimum can make it harder to read for people who aren't used to charts, and a chart with no context can be misread. Gridlines help readers estimate values; a light background can separate a chart from surrounding text. Remove what distracts, not everything.

---

## 15.12 Misleading charts, and how not to make them

Most misleading charts aren't made by people trying to deceive. They come from software defaults, from zooming in "to see the detail", and from wanting a chart to look impressive. Chapter 4, section 4.7, introduced several tricks; this section shows them on Riverstone data, with the honest alternative.

![Three charts. Top left: Delhi and Bengaluru revenue bars with a y-axis from 10.175 to 10.183 crore, making Delhi's bar look far taller. Top right: the same two bars from zero, almost identical, titled the gap is 0.04%. Bottom: revenue bars for 2023 to 2025 on a left axis starting at 55 and gross margin as a red line on a right axis from 20 to 28.5, so the line appears to track the bars](figures/fig15-13-misleading.svg)

*Figure 15.13 — Top: a truncated axis turns a 0.04% difference into a visual landslide. Bottom: a dual-axis chart whose two scales were chosen so that margin seems to follow revenue.*

### Truncated axes on bars

The top-left chart uses the quick (and wrong) Q4 branch numbers from Chapter 14's story: Delhi ₹10,18,31,086 and Bengaluru ₹10,17,88,506. With the axis starting at ₹10.175 crore, Delhi's bar looks about twice as tall. From zero, the bars are indistinguishable, which is the truth: a difference of ₹42,580, or 0.04%. (And the clean numbers put Bengaluru ahead by ₹1.47 crore, which a correct chart of clean data would show.)

**The rule:** bars always start at zero. If the differences you care about are small relative to the values, show the **differences** (a bar chart of change, or a dot plot of attainment) instead of truncating.

### Dual axes chosen to agree

The bottom chart puts revenue (bars, left axis) and gross margin (line, right axis) together. With the left axis starting at ₹55 crore and the right at 20%, the margin line climbs in step with revenue, and a reader concludes "as we grew, margins grew with volume". But the chart-maker could as readily have chosen scales that made margin look flat, or falling behind. In Riverstone's case, margin rose mainly because prices rose while unit costs were held constant in the data (the dataset's documented simplification), not because of volume.

**The alternative:** two aligned charts, or one chart with margin labeled on the bars (the project's makeover B in the answers), so no scale choice creates a relationship.

### Other common distortions

| Distortion | What it does | Honest alternative |
|---|---|---|
| **3D charts** | Perspective makes near bars and slices look bigger | 2D, always |
| **Area or icon scaling** | A coin twice as tall is four times the area, so it looks four times bigger | Bars, or scale icons by area, not height |
| **Cherry-picked time range** | Starting a line at a low point exaggerates growth; ending before a drop hides it | Show a full, standard period; say why a shorter one is used |
| **Inconsistent intervals** | 2019, 2021, 2024, 2025 spaced evenly look like steady years | Space by time; mark gaps |
| **Cumulative totals presented as growth** | A running total always rises, even when monthly sales fall | Show the monthly values, or both |
| **Percentages without the base** | "Kolkata +40%" from ₹1 lakh to ₹1.4 lakh | Show absolute values alongside |
| **Different scales in small multiples** | Each panel auto-scales, so a small branch looks as big as a large one | Share axes, or say clearly that they differ |
| **Averages without spread** | An average order of ₹24,736 hides that most orders are under ₹25,000 | Box plot or histogram (section 15.5) |
| **Omitted context** | A 5% drop shown without the fact that the whole market fell 12% | Add a benchmark line or annotation |

### A test for honesty

Before a chart leaves your hands, ask three questions:

1. **Would the conclusion change** if the axis started at zero, the range were longer, or the other scale were used?
2. **Would someone who disagrees** accept this chart as a fair picture of the data?
3. **Could a reader with only this chart** repeat an accurate sentence about the data?

If any answer is "no", change the chart.

---

## 15.13 Missing data, uncertainty, and accessibility

### Show what's missing

Charts make missing data invisible: a bar that isn't drawn doesn't look like a gap. Chapter 14 showed how much missing and quarantined data a real export contains. A chart should show it, or at least say how much there is.

![Left, before: horizontal bars of 2025 revenue for West, South, North, and East only. Right, after: the same four regions sorted, plus a gray bar at the bottom labeled City missing, ₹2.3 crore, with values on every bar](figures/fig15-14-missing-data.svg)

*Figure 15.14 — The "before" chart silently drops ₹2.3 crore of revenue from customers with no city. The "after" chart shows it, in gray, so the total is honest and the data gap is visible.*

- **Keep an explicit "Unknown" or "Not recorded" category** when a grouping column has gaps, in a neutral color, usually last.
- **Break lines at missing periods** instead of connecting across them, or draw the missing stretch dotted and label it.
- **Say what's excluded** in a note: "Excludes cancelled orders and 20 order lines under review."
- **Never fill gaps with zeros** to make a chart continuous; a zero is a value (Chapter 14, section 14.3).

### Show uncertainty

Some numbers in business charts are estimates: a forecast, a survey result, a figure based on incomplete data. Mark them:

- **Different line style** for forecasts (dashed) or provisional values (lighter).
- **Ranges** for estimates: a shaded band for a forecast range, or error bars for survey margins (Chapter 21 and Chapter 22 explain how they're calculated).
- **Labels** such as "provisional", "estimate", or "as of 5 January".

### Accessibility

An **accessible** chart can be understood by people with different abilities, including readers who use screen readers, have low vision, or have color vision deficiency. Most accessibility practices also make charts better for everyone.

1. **Alt text.** Add a short text alternative that states what the chart shows and its main finding: *"Line chart of Riverstone's monthly revenue in 2025 against target. Revenue beat target in January, February, and May to July, and fell short in March, April, and August to December; October was the highest month at ₹18.1 crore, 92% of target."* In Excel and PowerPoint, right-click the chart → **Edit Alt Text**; in Google Sheets, click the chart's **⋮ → Alt text**.
2. **Don't rely on color alone** (section 15.10): add labels, markers, or patterns.
3. **Contrast** of at least 4.5:1 for text and 3:1 for chart elements.
4. **Readable text size.** On a slide, chart text should be at least as large as the slide's body text; axis labels of 8 points are unreadable when projected.
5. **Provide the data.** A table next to the chart, or the underlying data in an appendix, lets anyone read exact values, including screen-reader users.
6. **Check.** Excel and PowerPoint: **Review → Check Accessibility** flags charts without alt text and low-contrast elements.

The figures in this chapter have alt text, and none relies on color alone for its message.

---

## 15.14 Building charts in Excel and Google Sheets

### A repeatable workflow in any tool

1. **Prepare the data first**, in the shape the chart needs: one row per bar or point, already summarized and sorted (SQL, a pivot table, or Power Query). Charting raw rows makes tools summarize in ways you didn't choose.
2. **Insert the simplest suitable chart**, then change the defaults: sort, remove clutter, label directly, set the colors.
3. **Write the action title and axis titles.**
4. **Check it** against sections 15.11–15.13: honest axes, visible missing data, alt text, contrast.
5. **Save the design** so the next chart starts right.

**Excel.** **Insert → Recommended Charts** suggests chart types for the selected data; treat the suggestions as a starting point. After formatting one chart the way you want, right-click it → **Save as Template**, and later choose it under **Insert → Recommended Charts → All Charts → Templates**. A **combo chart** (**Insert → Insert Combo Chart**) combines columns and lines; its **Secondary Axis** checkbox creates the dual axis that section 15.12 warns about, so leave it unticked unless you've considered the alternatives. To turn a chart title into a **dynamic action title**, first put the number in a cell. In the `monthly_2023_2025` sheet, with the 2025 revenue cells named `Revenue` and the 2025 target cells named `Target`, put the attainment in `B14`:

```excel
B14:  =SUM(Revenue)/SUM(Target)                              → 0.9826 (98.3%)
C14:  ="2025 finished at "&TEXT(B14,"0.0%")&" of target"     → 2025 finished at 98.3% of target
```

`TEXT(B14,"0.0%")` turns the number into text with a percentage format of one decimal place, and `&` joins the pieces into one sentence. Then select the chart title, type `=` in the formula bar, click `C14`, and press **Enter**. When next month's data arrives, the title changes with it.

**Google Sheets.** **Insert → Chart** opens the **Chart editor**: **Setup** for the chart type and ranges, **Customize** for titles, series colors, labels, gridlines, and axes. Sheets has no chart templates; copy a finished chart (**⋮ → Copy chart**) and change its data range instead. `=SPARKLINE(range, {"charttype","bar"})` draws in-cell bars; the braces hold an option name and its value.

In both tools, it's common to add a new month of data and not notice that the chart's range didn't grow to include it. Base charts on a **table** (Excel, **Ctrl+T**) or a named range that grows, as Chapter 11 recommended for formulas.

---

## 15.15 Running this chapter's SQL in MySQL

Most of this chapter's SQL runs unchanged in MySQL 8.0: the segment shares in section 15.1 (MySQL has the same window over an aggregate) and both histogram queries in section 15.5 (`FLOOR` is the same) return exactly the same rows. Three PostgreSQL features don't exist in MySQL. The companion file `companion/ch15/ch15_queries_mysql.sql` has every query in its MySQL form.

<!-- db: riverstone_full -->

**`FILTER` and `EXTRACT` (section 15.4).** MySQL has no `FILTER` clause. Use `SUM(CASE WHEN … THEN … END)`, the form Chapter 13, section 13.8, showed; `MONTH()` and `YEAR()` replace `EXTRACT`:

```mysql
SELECT MONTH(order_date) AS month,
       ROUND(SUM(CASE WHEN YEAR(order_date) = 2024 THEN net_revenue END)) AS rev_2024,
       ROUND(SUM(CASE WHEN YEAR(order_date) = 2025 THEN net_revenue END)) AS rev_2025
FROM sales_lines WHERE order_date >= '2024-01-01' GROUP BY 1 ORDER BY 1;
```

```
+-------+-----------+-----------+
| month | rev_2024  | rev_2025  |
+-------+-----------+-----------+
|     1 |  64063515 |  85195521 |
|     2 |  58632364 |  78582579 |
|     3 |  78193384 | 101009066 |
|     4 |  72534870 |  95194709 |
|     5 |  66888391 |  87249568 |
|     6 |  39531504 |  51972483 |
|     7 |  30515645 |  40028093 |
|     8 |  57166214 |  71835346 |
|     9 |  87548908 | 111701479 |
|    10 | 147221566 | 180620103 |
|    11 | 127896564 | 155985902 |
|    12 |  72822552 |  87266804 |
+-------+-----------+-----------+
```

`CASE WHEN YEAR(order_date) = 2024 THEN net_revenue END` gives the revenue on 2024 rows and nothing (NULL) on the others, and `SUM` skips the NULLs, so the column adds up 2024 only. The numbers match section 15.4.

**`DATE_TRUNC` and `::date` (section 15.11).** MySQL builds the first day of the month with `DATE_FORMAT` and converts it with `CAST(... AS DATE)`, as Chapter 12, section 12.16, showed:

```mysql
WITH monthly AS (
  SELECT CAST(DATE_FORMAT(order_date, '%Y-%m-01') AS DATE) AS m, SUM(net_revenue) AS revenue
  FROM sales_lines
  GROUP BY 1
)
SELECT t.target_month, ROUND(a.revenue) AS net_revenue, t.target_revenue,
       ROUND(100 * a.revenue / t.target_revenue, 1) AS pct_of_target
FROM sales_targets t
JOIN monthly a ON a.m = t.target_month
WHERE t.target_month >= '2025-01-01'
ORDER BY t.target_month;
```

```
+--------------+-------------+----------------+---------------+
| target_month | net_revenue | target_revenue | pct_of_target |
+--------------+-------------+----------------+---------------+
| 2025-01-01   |    85195521 |    77350000.00 |         110.1 |
| 2025-02-01   |    78582579 |    70000000.00 |         112.3 |
| 2025-03-01   |   101009066 |   108050000.00 |          93.5 |
| 2025-04-01   |    95194709 |    96900000.00 |          98.2 |
| 2025-05-01   |    87249568 |    85900000.00 |         101.6 |
| 2025-06-01   |    51972483 |    50400000.00 |         103.1 |
| 2025-07-01   |    40028093 |    36500000.00 |         109.7 |
| 2025-08-01   |    71835346 |    76050000.00 |          94.5 |
| 2025-09-01   |   111701479 |   118300000.00 |          94.4 |
| 2025-10-01   |   180620103 |   196150000.00 |          92.1 |
| 2025-11-01   |   155985902 |   158950000.00 |          98.1 |
| 2025-12-01   |    87266804 |    92400000.00 |          94.4 |
+--------------+-------------+----------------+---------------+
```

`DATE_FORMAT(order_date, '%Y-%m-01')` writes the date's year and month and a fixed day `01`, as text such as `2025-01-01`; `CAST(... AS DATE)` turns that text back into a date so it can be joined to `target_month`. The rest of the query is unchanged, and so are the results.

**`PERCENTILE_CONT` (section 15.5).** MySQL has no percentile function. Use the spreadsheet route in section 15.5, or build the median from window functions: exercise 21 asks you to, and its answer is the MySQL query.

---

## Common mistakes

| Mistake | Symptom | Fix |
|---|---|---|
| Starting from the data, not the question | A chart that shows everything and says nothing | Write the question first; choose the chart for it |
| Pie charts for more than three parts or close values | Readers can't rank the slices | Sorted bar chart |
| Bars that don't start at zero | Small differences look huge | Zero baseline; chart the differences or use a dot plot |
| Categories in alphabetical order | The ranking is hard to see | Sort by value (keep natural order for ordinal data) |
| Rotated or overlapping labels | Readers tilt their heads | Horizontal bars; shorter labels |
| A line across categories | Implies a trend that doesn't exist | Bars or dots |
| Too many lines or colors | A legend puzzle | Highlight one or two; gray the rest; small multiples |
| A rainbow palette for amounts | No clear "more" direction | Sequential palette |
| Red–green as the only distinction | Unreadable for about 1 in 12 men | Blue–orange or blue–red; add labels |
| Dual axes | Scales chosen to create or hide a relationship | Aligned separate charts; index to 100 |
| 3D effects | Distorted lengths and areas | 2D |
| Label titles ("Sales by Month") | Readers must find the message | Action title stating the finding |
| Legends instead of direct labels | Eye travels back and forth | Label lines and bars directly |
| Wrong histogram bins | Noise or hidden shape | Try several bin widths; say which you show |
| Averages without spread | A typical value that isn't typical | Box plot, histogram, or median and quartiles |
| Overplotted scatter plots | Density hidden | Transparency, jitter, binning |
| Missing categories silently dropped | Totals don't match other reports | Show "City missing" (or "Unknown") in gray; add a note |
| Gaps filled with zeros | A fake collapse in a line | Break the line; label missing periods |
| Cherry-picked time ranges | Exaggerated growth or decline | Standard full periods; justify exceptions |
| Tiny text on slides | Unreadable when projected | Chart text at least as large as body text |
| No alt text | Screen-reader users get nothing | State the chart type and finding in alt text |

---

## In the real world: the October that looked like a collapse

In the first week of January 2026, Riverstone's leadership team met to set the stock plan for the 2026 festive season. Every year the plants build inventory from July for the October peak, and the decision about how much to build is one of the company's biggest.

The monthly management pack opened with a column chart titled **"Monthly Target Achievement 2025"**. It showed twelve columns of attainment percentage, colored red below 100 and green above. The vertical axis ran from 90% to 115%, the software's automatic choice for values between 92.1 and 112.3. On that axis, October's column, at 92.1%, was a stub barely above the bottom, surrounded by tall green columns from January and February. Anyone glancing at the slide saw a year that started brilliantly and fell apart in the festive season.

Suresh Menon, the Finance Manager, suggested building 15% less festive stock for 2026: "We missed October badly. We shouldn't tie up cash in inventory that didn't sell." Heads nodded. Anita Rao asked Meera Iyer to "check the October story" before the decision was minuted the following week.

Meera didn't start by redrawing the chart. She wrote down the question the meeting was really answering: *Did festive-season demand weaken in 2025?* The attainment chart couldn't answer that, because attainment depends on the target as much as on sales. She pulled three numbers:

- **October 2025 revenue: ₹18,06,20,103**, the highest month in Riverstone's history.
- **October 2024 revenue: ₹14,72,21,566**, so October grew **22.7%** year over year.
- **October 2025 target: ₹19,61,50,000**, which had required growth of **33%** over October 2024.

Q4 as a whole told the same story: revenue of ₹42.4 crore, up 21.8% on Q4 2024, but 94.7% of a ₹44.75 crore target.

She built two charts for the follow-up meeting.

The first was Figure 15.12's redesign: 2025 revenue and target as two lines from a zero baseline, titled *"2025 finished at 98.3% of target: a strong January–February, then a Q4 short of an ambitious plan"*, with one annotation at October: *"₹18.1 crore, a record month, but 92% of its ₹19.6 crore target."*

The second answered the question directly: one line per year from Figure 15.4, titled *"Festive demand grew again: October 2025 was 22.7% above October 2024."* The three Octobers stood out clearly, each higher than the last.

She added a short note under both charts: *"Attainment compares sales with the plan. October's plan assumed 33% growth and actual growth was 22.7%; across Q4 the plan assumed 29% and actual growth was 21.8%. The shortfall is in the plan, not in demand."*

At the follow-up meeting, nobody argued with the numbers, because the charts made the difference between "missed target" and "weaker demand" visible. The team kept the festive stock build at the planned level and asked Finance and Sales to review how October targets are set. Vikram Singh asked for one more change to the monthly pack: every chart title would state its finding, and every attainment chart would show revenue and the previous year next to it.

What made the difference:

- **She started from the decision**, not the chart, and asked whether the chart could answer the question at all.
- **She separated the measure from the benchmark**: attainment mixes sales performance with target setting.
- **She used honest axes**: a zero baseline for revenue, and no automatic 90–115% scale for percentages that makes a 92 look like a collapse.
- **Her titles stated findings** that both sides of the argument could accept.

---

## Project: redesign Riverstone's old management pack

**Goal:** turn five poor charts into clear, honest charts that each deliver one message, and explain every change.

### Tools you'll need

- **Excel for Windows** (Microsoft 365). Histogram, box-and-whisker, waterfall, treemap, and filled map charts need Excel 2016 or later; the filled map needs an internet connection.
- **Google Sheets:** most chart types; no native box plot.
- **PostgreSQL 16 or MySQL 8.0** for preparing chart data (tested on PostgreSQL 16.15 and MySQL 8.0.46 with `riverstone_full`).
- **Companion files:**
  - `companion/ch15/ch15_chart_data.xlsx`: one sheet per chart (segment shares, monthly revenue and targets 2023–2025, 2025 order values, customers, the 2024–2025 bridge, region by month, category by month, cities, regions, margin by year, reps by month, products, Anscombe's quartet).
  - `companion/ch15/chart_data/*.csv`: the same tables as CSV.
  - `companion/ch15/ch15_queries_mysql.sql`: the chapter's queries in their MySQL form (section 15.15).
  - Every table can be rebuilt from `riverstone_full` with SQL like the queries in this chapter.
- **Free helpers:** a color-blindness simulator (such as Coblis), a contrast checker (such as WebAIM's), and ColorBrewer for sequential and diverging palettes.

**Option A: your own charts.** Take five charts from a report, dashboard, or presentation you've received or made (remove confidential numbers, or rebuild them with invented data). Redesign each one using this chapter's principles.

**Option B: Riverstone's data.** Figure 15.15 shows five charts from Riverstone's old monthly management pack. The data for each is in `ch15_chart_data.xlsx` (sheets `product_2025`, `margin_by_year`, `region_2025`, `rep_month_2025`, and `region_month_2025`).

**Steps**

1. **For each chart, write down its question** and the one message the reader should take away. If you can't find a message, decide what question the data could answer for a manager.
2. **List every problem** you see, using the mistakes table.
3. **Choose a better chart type** with the chart chooser (Figure 15.2). Explain the choice in one sentence.
4. **Build the redesign** in Excel or Google Sheets from the chart data. Sort, remove clutter, label directly, choose colors deliberately, and start bars at zero.
5. **Write an action title** for each chart, and check it against the data.
6. **Add alt text** to each chart, and check it in grayscale.
7. **Put the before-and-after pairs on five slides** (or one page each), with three bullet points under each explaining what you changed and why.
8. **Test it:** show only the "after" charts to someone who hasn't seen the data, give them ten seconds per chart, and ask what each one says. If their answer doesn't match your title, revise.

![Five poor charts. A: an exploded, shadowed pie of eight products in rainbow colors. B: revenue columns for 2023–2025 on an axis starting at 55 with a gross margin line on a second axis. C: region columns on an axis starting at 13, in four colors, with heavy gridlines. D: a rainbow stacked area chart of eleven sales reps by month with a legend. E: clustered columns for four regions across twelve months with crowded, rotated data labels and heavy gridlines](figures/fig15-15-project-before.svg)

*Figure 15.15 — Five charts from Riverstone's old management pack, each with several of this chapter's mistakes.*

**What good looks like:** each redesign answers one question in under ten seconds; every bar chart starts at zero; no chart needs a legend with more than three entries; titles state findings with numbers; missing data (the ₹2.3 crore with no city) is visible; the charts work in grayscale. One set of solutions is in Figure 15.16 in the answers, but many good redesigns exist.

**Stretch goals**

- Build the five redesigns as a one-page dashboard in Excel with a shared color theme, and make every title dynamic (section 15.14).
- Write a one-page "chart style guide" for Riverstone: fonts, colors (with codes and a color-blind check), number formats (lakh and crore), title rules, and which chart to use for the ten most common questions.

---

## Recap

- **Perception:** people judge position and length most accurately, then angle, then area and color. Put the key comparison on position or length. One highlight color is noticed instantly; many colors aren't.
- **Start from the question:** compare categories (sorted bars), change over time (lines), distribution (histograms and box plots), relationship (scatter), parts of a whole (stacked bars, waterfalls, rarely pies), location (maps). Levels of measurement constrain the choice; sometimes a table is best.
- **Bars** start at zero, are sorted, horizontal when labels are long, labeled directly, one color. **Lines** show time left to right, can zoom the axis carefully, and should be labeled directly; avoid dual axes.
- **Distributions:** histogram bin width changes the story; box plots compare groups by median and quartiles (Riverstone's Wholesale orders: median ₹25,762 against about ₹19,000 for the others). **Scatter plots** reveal what summaries hide (Anscombe's quartet); fix overplotting with transparency and jitter.
- **Composition:** stacked bars show totals and the bottom segment; waterfalls explain changes (2024 ₹90.3 crore to 2025 ₹114.7 crore, led by Retail's +₹11.3 crore). **Heatmaps** answer two-way questions; **maps** only when location matters.
- **Color:** categorical, sequential, and diverging palettes for different data; consistent meanings; color-blind-safe choices; contrast of 4.5:1 for text and 3:1 for graphics.
- **Titles state findings;** labels carry units; annotations explain; clutter goes.
- **Honesty:** no truncated bars, 3D, or scales chosen to agree; show full periods, missing data, and uncertainty. Ask whether someone who disagrees would accept the chart as fair.
- **Accessibility:** alt text, labels as well as color, readable text, and the data available as a table.

---

## Key terms

data visualization · encoding · graphical perception · pre-attentive attributes · working memory · exploratory chart · explanatory chart · bar chart · column chart · grouped (clustered) bar · stacked bar · 100% stacked bar · small multiples · dot plot · lollipop chart · line chart · dual-axis chart · sparkline · distribution · histogram · bin · skew · box plot · quartile · interquartile range (IQR) · whisker · strip plot · jitter · density curve · violin plot · scatter plot · overplotting · correlation · log scale · Anscombe's quartet · pie chart · donut chart · waterfall (bridge) chart · treemap · heatmap · choropleth map · symbol map · categorical palette · sequential palette · diverging palette · highlight color · color vision deficiency · Okabe–Ito palette · contrast ratio · WCAG · action title · annotation · data-ink ratio · clutter · truncated axis · cherry-picking · alt text · accessibility

*(All terms are defined in the Glossary, Appendix A.)*

---

## Check yourself

- [ ] You can explain why position and length beat angle, area, and color, and use that to choose an encoding.
- [ ] You write the question and the message before choosing a chart.
- [ ] You choose correctly between bar, line, histogram, box plot, scatter, stacked bar, waterfall, heatmap, map, and table for a given question.
- [ ] Your bar charts start at zero, are sorted, and are labeled directly.
- [ ] You can read and explain a box plot and a histogram, and choose sensible bins.
- [ ] You use sequential, diverging, and categorical palettes appropriately, highlight with one color, and check for color vision deficiency.
- [ ] Your chart titles state findings that are true, supported by numbers, and fair.
- [ ] You spot truncated axes, dual axes, 3D, cherry-picked ranges, and averages without spread, and replace them with honest alternatives.
- [ ] You show missing data and uncertainty instead of hiding them.
- [ ] Your charts have alt text, sufficient contrast, readable text, and don't rely on color alone.
- [ ] You can build all of this in Excel or Google Sheets.

---

## Exercises

Use `companion/ch15/ch15_chart_data.xlsx` (or the CSV files), the `riverstone_full` database, and Excel or Google Sheets.

### Warm-up

1. Rank these encodings from most to least accurate for comparing values: bubble area, bar length on a common baseline, pie slice angle, color saturation, dot position on a common scale.
2. For each question, name the best first-choice chart: (a) How did monthly revenue change over 2025? (b) Which of 39 cities brought the most revenue? (c) How are order values spread out, and are there outliers? (d) Do customers with more orders spend more? (e) What made revenue grow from 2024 to 2025? (f) Which months are strong in which regions?
3. What's wrong with each: (a) a line chart joining Retail, Wholesale, and Hospitality; (b) a pie chart of 11 sales reps' revenue; (c) a column chart of attainment with an axis from 90% to 115%; (d) a rainbow heatmap of revenue.
4. Rewrite each label title as an action title, using the numbers given: (a) "Revenue by Segment 2025" (Retail 48.5%, Wholesale 27.3%, Hospitality 24.2%); (b) "Order Values by Segment" (medians: Wholesale ₹25,762, Retail ₹19,425, Hospitality ₹19,122); (c) "Revenue 2024 vs 2025" (+₹24.4 crore; Retail +₹11.3 crore).
5. When is a pie chart acceptable? Give the conditions and one Riverstone example that meets them.
6. Name the kind of palette (categorical, sequential, diverging) for: (a) revenue by region; (b) year-over-year growth, which can be negative or positive; (c) product categories; (d) number of orders per customer.

### Core

7. Build Figure 15.3's "after" chart from `product_2025` in Excel or Google Sheets. Which two products together sell less than any other single product, and what's their combined revenue?
8. From `order_values_2025`, build a histogram with ₹10,000 bins. How many orders fall in each of the first three bins? Then try ₹2,000 and ₹50,000 bins and describe what changes.
9. Build box plots of order value by segment (Excel's Box and Whisker). Using the quartiles in section 15.5, what's the IQR of Wholesale orders, and what's the 1.5 × IQR upper fence?
10. From `monthly_2023_2025`, in how many months of each year was revenue above target? Which 2025 month had the lowest attainment, and which the highest?
11. Using `region_month_2025`, which region and month had the highest revenue, and which region and month the lowest (excluding City missing)? Build the heatmap with a sequential palette.
12. Build the waterfall from `bridge_2024_2025`. What was the total change, and what share of it came from Retail?
13. From `customers_2025`, build a scatter plot of orders against revenue with transparency. What's the correlation between the two columns? (Use `=CORREL`, section 15.6.)
14. Using `anscombe.csv`, calculate the mean of each y column (`=AVERAGE`) and the correlation of each pair (`=CORREL`). Then draw the four scatter plots. What do the charts show that the numbers don't?
15. What share of 2025 revenue has no city? Redraw a region bar chart that shows it, and write a one-sentence note for the chart.
16. Chart C in Figure 15.15 starts its axis at ₹13 crore. How many times longer does West's column look than East's, compared with the true ratio? (Use `region_2025`.)
17. Write alt text (two sentences at most) for Figure 15.6.
18. Using the query in section 15.4, calculate Q4 revenue for 2024 and 2025 and the growth rate. Build a chart that shows the three Octobers and write its action title.
19. Take the 11-rep line chart (Figure 15.11, before). Redesign it as small multiples: one small chart per rep on a shared axis. When is this better than highlighting one rep?
20. In Excel, make a chart title that updates from a cell: "2025 finished at X% of target", where X is calculated from the data. Write the formula.

### Stretch

21. MySQL has no `PERCENTILE_CONT`. Write a MySQL query that returns the median order value per segment for 2025 using window functions. Do the results match PostgreSQL exactly?
22. Design a color palette of five colors for Riverstone's charts: one highlight, one neutral, a sequential scale, and a diverging pair. Give the color codes, and check the highlight and text colors for contrast against white.

### Think about it

24. The Sales Head likes 3D pie charts "because they look professional" and asks for one on the first slide. How do you respond?
25. A manager wants a dashboard with 20 KPIs on one screen "so everything is in one place". What would you suggest, and why?

---

## Answers

**Project (Option B): one set of redesigns, shown in Figure 15.16.**

- **A (exploded pie → sorted bars):** eight slices can't be ranked by angle, and the shadow and explosion distort them. Sorted bars with values, one highlight. Title: *"Storage Box 25L led 2025"*.
- **B (dual axis → one chart with labels):** the two scales were chosen so margin appears to follow revenue. Revenue bars from zero with margin written in each bar; no second axis. Title: *"Revenue up 87% since 2023; margin up 6.4 points"*.
- **C (truncated, multicolored columns → sorted bars from zero, missing data shown):** an axis starting at ₹13 crore made East look about a twentieth of West. Title: *"West brings 33% of 2025 revenue"*.
- **D (rainbow stacked area → highlight lines):** the middle layers of a stacked area can't be read, and eleven colors need a legend. Gray lines and one highlight (or small multiples). Title: *"Every rep follows the same season; Rahul Mehta leads"*.
- **E (48 clustered columns with crowded labels → heatmap):** a two-way question with too many bars. A sequential heatmap with values. Title: *"October is the peak in every region"*.

![Five redesigned charts. A: sorted horizontal bars of product revenue in gray with Storage Box 25L highlighted in blue and values labeled. B: revenue columns for 2023 to 2025 from a zero baseline with revenue labels above and gross margin percentages inside each column. C: sorted horizontal bars of region revenue with a gray City missing bar at the bottom. D: eleven rep lines in light gray with Rahul Mehta in orange. E: a blue heatmap of revenue by region and month](figures/fig15-16-project-after.svg)

*Figure 15.16 — One set of redesigns for the old management pack. Each chart has one message in its title.*

**1.** Dot position on a common scale; bar length on a common baseline; pie slice angle; bubble area; color saturation.

**2.** (a) Line chart. (b) Sorted horizontal bar chart (top 10, or all 39 if the reader needs them). (c) Histogram, or box plot if comparing groups. (d) Scatter plot. (e) Waterfall chart. (f) Heatmap.

**3.** (a) Segments are nominal; a line implies a trend or order between them that doesn't exist. Use bars. (b) Eleven slices can't be compared by angle, and the colors need an eleven-entry legend. Use a sorted bar chart. (c) A truncated axis on columns exaggerates differences: 92% looks like a fraction of 110%. Use a zero baseline, a dot plot, or bars of the difference from 100%. (d) A rainbow has no natural order and bright middle colors draw attention to middling values; use a sequential palette.

**4.** Examples: (a) "Retail brought almost half of 2025 revenue (48.5%)". (b) "Wholesale orders are about a third larger: median ₹25,762 against about ₹19,000 for Retail and Hospitality". (c) "Revenue grew ₹24.4 crore in 2025, with Retail contributing ₹11.3 crore". Other wordings are fine if they're accurate and state one finding.

**5.** When the parts add up to a meaningful whole, there are only two or three parts, the message is a simple share, and exact comparison between parts isn't the point. Riverstone example: the 2025 segment split, if the message is only "Retail is almost half" (but not if the reader must compare Wholesale with Hospitality, as Figure 15.1 shows).

**6.** (a) Sequential (or one color for bars). (b) Diverging, centered on 0%. (c) Categorical. (d) Sequential.

**7.** **Garden Chair (₹4,50,75,400)** and **Water Bottle 1L (₹4,03,19,029)**: together **₹8,53,94,429** (₹8.5 crore), less than Lunch Box Set, the next smallest at ₹13,11,02,660.

**8.** With ₹10,000 bins starting at 0: **10,151** orders under ₹10,000; **12,449** from ₹10,000 to under ₹20,000; **9,134** from ₹20,000 to under ₹30,000. Narrower (₹2,000) bins show a jagged, noisy shape; wider (₹50,000) bins collapse the data into three or four bars and hide that most orders cluster between about ₹5,000 and ₹30,000. (Excel's histogram labels bins as ranges and may place the boundary value in the lower bin; the counts can differ by a few orders at the edges.)

**9.** Wholesale Q1 ₹13,340, Q3 ₹43,826: **IQR = ₹30,486**. Upper fence = Q3 + 1.5 × IQR = 43,826 + 45,729 = **₹89,555**. Orders above that are drawn as individual points.

**10.** Months above target: **2023: 5**, **2024: 6**, **2025: 5**. In 2025, the lowest attainment was **October (92.1%)** and the highest **February (112.3%)**.

**11.** Highest: **West in October (₹6,03,25,631)**. Lowest (excluding City missing): **East in July (₹47,02,844)**.

**12.** Total change **₹24,36,26,176** (from ₹90,30,15,475 to ₹1,14,66,41,651). Retail's +₹11,26,26,265 is **46.2%** of the growth.

**13.** **0.916**, for example with `=CORREL(C2:C4600, D2:D4600)` on the `customers_2025` sheet (orders in column C, revenue in column D).

**14.** Every y column has a mean of **7.50** (to two decimals), and every pair has a correlation of **0.82** (0.816 or 0.817 at three decimals); the x columns all have a mean of 9. The charts show four different patterns: a loose linear relationship, a smooth curve, a perfect line with one outlier, and no relationship except one extreme point that creates the correlation on its own. Summary statistics can't distinguish them.

**15.** ₹2,26,69,946 of ₹1,14,66,41,651: **2.0%**. Note: *"₹2.3 crore (2.0%) of 2025 revenue comes from customers with no city recorded and is shown separately."*

**16.** Values: West ₹38.4 crore, East ₹14.2 crore, a true ratio of **2.7**. With the axis starting at 13, the visible columns are 38.4 − 13 = 25.4 and 14.2 − 13 = 1.2, so West looks about **21 times** as long as East.

**17.** Example: *"Box plots of 2025 order values by segment. Wholesale orders are larger and more spread out (median ₹25,762) than Retail (₹19,425) and Hospitality (₹19,122), and all three have a long tail of large orders."*

**18.** Q4 2024: 14,72,21,566 + 12,78,96,564 + 7,28,22,552 = **₹34,79,40,682**. Q4 2025: 18,06,20,103 + 15,59,85,902 + 8,72,66,804 = **₹42,38,72,809** (₹42,38,72,808 before rounding each month). Growth **21.8%**. A line chart of January–December for 2023, 2024, and 2025 with direct labels; title such as *"Festive demand grew again: October 2025 was 22.7% above October 2024"*.

**19.** Small multiples show each rep's full pattern on its own panel without overlap, with a shared axis so sizes stay comparable. They're better when the reader needs to look at **every** rep (a sales manager reviewing the team); highlighting is better when the story is about **one** rep or one comparison.

**20.** Put the attainment in a cell, for example `B14` = `=SUM(Revenue)/SUM(Target)`. In another cell, `C14` = `="2025 finished at "&TEXT(B14,"0.0%")&" of target"`. Select the chart title, type `=` in the formula bar, click `C14`, and press **Enter**. The title now changes whenever the data does.

**21.** One solution:

```
WITH order_values AS (
  SELECT s.order_id, c.segment, SUM(s.net_revenue) AS order_value
  FROM sales_lines s JOIN customers c ON c.customer_id = s.customer_id
  WHERE s.order_date BETWEEN '2025-01-01' AND '2025-12-31'
  GROUP BY s.order_id, c.segment
), ranked AS (
  SELECT segment, order_value,
         ROW_NUMBER() OVER (PARTITION BY segment ORDER BY order_value) AS rn,
         COUNT(*) OVER (PARTITION BY segment) AS n
  FROM order_values
)
SELECT segment, ROUND(AVG(order_value)) AS median
FROM ranked WHERE rn IN (FLOOR((n + 1) / 2), CEIL((n + 1) / 2))
GROUP BY segment ORDER BY median;
```

It returns Hospitality **19,122**, Retail **19,425**, Wholesale **25,763**. For odd counts the two row numbers are the same row; for even counts it averages the middle two, which is what `PERCENTILE_CONT(0.5)` does. The exact Wholesale median is ₹25,762.50. PostgreSQL rounded it down and MySQL rounded it up, because the two databases break ties differently. Round only for display.

**22.** Many good answers. An example: highlight orange `#c0662b`, neutral gray `#b8c0cc`, text dark `#1d2330`, sequential blues from `#e3edf5` to `#0f5c8c`, diverging red `#b23b3b` and blue `#0f5c8c` through white. Check with a contrast checker: `#1d2330` on white is far above 4.5:1; the orange `#c0662b` on white is about 4.1:1, enough for bars, lines, and large text but slightly below the 4.5:1 needed for small text, so use the dark text color for labels. Test the palette in a color-blindness simulator; red–blue stays distinguishable, unlike red–green.

**24.** Acknowledge the goal (a professional look) and explain the cost with evidence: in a 3D pie, near slices look bigger than far ones, so the chart shows the wrong sizes, and pies can't show close shares (Figure 15.1). Offer a design that looks polished and is accurate: a sorted bar chart in the company's colors, with an action title and clean labels. If a pie is still wanted for a simple two- or three-part share, make it flat, with labels on the slices.

**25.** Ask what decisions the dashboard supports and who uses it. Suggest a top level of three to five KPIs that answer the most important question ("are we on track this month?"), each with a comparison (target or last year), and move the other KPIs to drill-down pages by topic. Twenty KPIs on one screen means small text, no context for any of them, and no clear place to look; people end up reading none of them. Chapter 16 shows how to design the pages in Power BI.

---

## Where this leads

- **Chapter 16, Business Intelligence with Power BI:** these principles applied to interactive dashboards: visual choice, themes, tooltips, and report layout.
- **Chapter 18, Python for Analysts:** Chapter 18 draws these charts in Python, with matplotlib and seaborn, including reusable chart styles.
- **Chapter 20, Automating Reports & Delivering Insights:** charts in automated reports and emails, and presenting findings to stakeholders.
- **Chapter 21, Descriptive Statistics & Probability:** the statistics behind histograms, box plots, percentiles, correlation, and uncertainty bands.
- **Chapter 22, Statistics Without Fooling Yourself:** correlation versus causation, and how to show uncertainty clearly.
- **Interview preparation:** the Excel, Google Sheets, VBA & BI Question Bank (Chapter 70) includes "critique this chart" and "which chart would you use?" questions, and the Business Analyst Question Bank (Chapter 76B) covers presenting findings.
