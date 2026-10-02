-- Chapter 15. Data Visualization Principles
-- Practice SQL for POSTGRESQL, extracted from the chapter.
--
-- Riverstone Supplies is the worked example throughout the book. Load the database
-- first (companion/riverstone_setup_mini.sql, riverstone_2025_setup.sql, or
-- companion/full/riverstone_full_setup_postgresql.sql), then run these statements in order.
--
-- Each statement keeps the chapter's explanation above it and the chapter's own
-- result below it, marked as the chapter's. Run it yourself to see your own.
-- Source: manuscript/ch15-data-visualization-principles.md


-- =============================================================================================
-- Chapter 15. Data Visualization Principles
-- =============================================================================================

-- Part 2 — The Analyst

-- > Chapter at a glance > > You will learn to: explain how people read charts, and why position
-- and length beat angle, area, and color · start from the question and pick the chart that answers
-- it · build clear bar, line, histogram, box, scatter, stacked, waterfall, heatmap, and map
-- charts, and know when each fails · use color with meaning: one highlight, sequential and
-- diverging palettes, color-blind-safe choices · write titles that state the finding and
-- annotations that explain it · remove clutter without removing information · recognize misleading
-- charts (truncated axes, dual axes, 3D, cherry-picked ranges) and avoid making them · show
-- missing and uncertain data openly · make charts accessible · build the charts in Excel and
-- Google Sheets · redesign a poor management pack. > > Before you start: Chapter 1 (levels of
-- measurement), Chapter 4 (averages (mean vs median), percentages, and the chart checks in section
-- 4.7), Chapter 10 and 11 (spreadsheets and pivot tables), and Chapter 13 (SQL aggregation).
-- Chapter 14 helps: charts of dirty data are wrong however well they're drawn. > > Time needed:
-- 12–15 hours of reading and practice, spread over two weeks. > > Tools: Excel for Windows
-- (Microsoft 365) or Google Sheets; PostgreSQL or MySQL for preparing chart data. > > Practice
-- data: companion/ch15/ch15_chart_data.xlsx, one sheet for every chart in this chapter, made from
-- the full Riverstone dataset. The same tables are in companion/ch15/chart_data/ as CSV files, and
-- every table can be rebuilt from riverstone_full with SQL like the queries in this chapter.

-- ---

-- =============================================================================================
-- Why this matters
-- =============================================================================================

-- Most people who see your analysis will never see your spreadsheet, your SQL, or your cleaning
-- log. They'll see a chart, for a few seconds, on a slide or a dashboard, often on a phone. What
-- they understand in those seconds is what your analysis says, whatever the numbers underneath.

-- A good chart makes the important thing obvious: October is the peak, Wholesale orders are
-- larger, one branch is behind. A poor chart hides it in a legend with eleven colors, or worse,
-- invents a story that isn't there: a bar that looks twice as tall because the axis starts at 90%,
-- a margin line that seems to follow revenue because someone chose two scales that make it.

-- Visualization is also one of the most visible analyst skills. Hiring managers look at portfolio
-- charts before anything else, interviewers ask "what's wrong with this chart?", and a single
-- clear chart in a review meeting does more for an analyst's reputation than a hundred correct
-- queries nobody sees.

-- The good news is that clear charts follow a small number of principles, backed by research on
-- how people see. This chapter teaches those principles with Riverstone's full three-year dataset,
-- shows each one as a before-and-after, and ends with a makeover of Riverstone's old management
-- pack.

-- ---

-- =============================================================================================
-- In plain English
-- =============================================================================================

-- Think about the display board at a railway station. Hundreds of people glance at it while
-- walking. The board's designers had one job: let each person find their train, platform, and time
-- in a couple of seconds.

-- So the board lists trains in time order (sorted, so your eye knows where to look). Every row has
-- the same layout (consistent). Platform numbers are large (the thing people need most is the most
-- visible). Cancelled trains are shown in red, and only cancelled trains (color has one meaning).
-- There's no decoration, no 3D effect, no logo in the middle.

-- A chart is the same kind of object. Its reader is busy. Your job isn't to show everything you
-- know; it's to make one message quick to find and hard to misread:

-- - Choosing a chart is choosing the layout that fits the question, like a timetable for times or
-- a map for locations. - Sorting and labeling are what let the eye find the answer without
-- searching. - Color with meaning is the red for cancellations: used for one thing, so it stands
-- out. - A title that states the finding is the announcement over the speaker: "the 18:05 to Pune
-- leaves from platform 4". - Honesty is the board showing the real platform, not the one that
-- would make the station look efficient.

-- ---

-- =============================================================================================
-- 15.1 How people read charts
-- =============================================================================================

-- When someone looks at a chart, their eyes and brain decode it: they turn shapes back into
-- numbers and comparisons. Some shapes decode quickly and accurately; others are slow and
-- misleading. Choosing a chart is mostly choosing an encoding that people decode well.

-- =============================================================================================
-- The accuracy ranking
-- =============================================================================================

-- In a famous study in 1984, William Cleveland and Robert McGill asked people to judge values
-- shown in different ways, and measured how accurate they were. Later studies have broadly
-- confirmed their ranking, from most to least accurate:

-- 1. Position along a common scale (dots or bar ends against the same axis) 2. Position along non-
-- aligned scales (the same axis repeated in separate panels) 3. Length (bars that start at the
-- same baseline), direction, and angle 4. Area (bubbles, treemaps) 5. Volume and curvature 6.
-- Color saturation and shading (lighter and darker)

-- The practical rule: encode the most important comparison with position or length. Use angle,
-- area, and color for secondary information, or when the exact value doesn't matter.

-- Figure 15.1 shows why. Riverstone's 2025 revenue by segment is drawn twice.

-- Figure 15.1 — The same three numbers. In the pie, comparing Wholesale with Hospitality means
-- judging two angles; in the bar chart, it means comparing two lengths against one axis.

-- In the pie, is Wholesale bigger than Hospitality? Most people can't tell: 27.3% and 24.2% are
-- angles of 98° and 87°, drawn in different orientations. In the bar chart, the difference is
-- visible at a glance, and the labels give the exact values.

-- The data for the chart comes from the full dataset (the sales_lines view from Chapter 13,
-- section 13.2, which excludes cancelled orders). Every piece of the query is from Chapters 12 and
-- 13, but it's built here in three small steps, so you can see what each piece adds.

-- Step 1: one total per segment. Join each sales line to its customer to get the segment, keep
-- 2025, and add up revenue for each segment:

-- <!-- db: riverstone_full -->

SELECT c.segment, SUM(s.net_revenue) AS net_revenue
FROM sales_lines s JOIN customers c ON c.customer_id = s.customer_id
WHERE s.order_date BETWEEN '2025-01-01' AND '2025-12-31'
GROUP BY c.segment;

/* The chapter shows:
      segment   |           net_revenue            
   -------------+----------------------------------
    Hospitality | 277476705.0000000000000000000000
    Retail      | 556436453.7500000000000000000000
    Wholesale   | 312728492.5000000000000000000000
   (3 rows)
*/


-- How it works:

-- - FROM sales_lines s JOIN customers c ON c.customer_id = s.customer_id gives each sales line its
-- customer's row, so the line knows its segment (the join from Chapter 12, section 12.10; s and c
-- are short aliases). - WHERE s.order_date BETWEEN '2025-01-01' AND '2025-12-31' keeps only 2025.
-- - GROUP BY c.segment with SUM(s.net_revenue) makes one row per segment with its total.

-- The totals are right, but the long decimals are hard to read and the rows aren't in any useful
-- order.

-- Step 2: round and sort. ROUND(...) with no second argument rounds to whole rupees, and ORDER BY
-- net_revenue DESC puts the biggest segment first, the order the bar chart needs:

SELECT c.segment, ROUND(SUM(s.net_revenue)) AS net_revenue
FROM sales_lines s JOIN customers c ON c.customer_id = s.customer_id
WHERE s.order_date BETWEEN '2025-01-01' AND '2025-12-31'
GROUP BY c.segment
ORDER BY net_revenue DESC;

/* The chapter shows:
      segment   | net_revenue 
   -------------+-------------
    Retail      |   556436454
    Wholesale   |   312728493
    Hospitality |   277476705
   (3 rows)
*/


-- Step 3: add each segment's share. A share is the segment's total divided by the total of all
-- segments. The all-segment total is a window over the grouped result:

SELECT c.segment, ROUND(SUM(s.net_revenue)) AS net_revenue,
       ROUND(100 * SUM(s.net_revenue) / SUM(SUM(s.net_revenue)) OVER (), 1) AS share_pct
FROM sales_lines s JOIN customers c ON c.customer_id = s.customer_id
WHERE s.order_date BETWEEN '2025-01-01' AND '2025-12-31'
GROUP BY c.segment
ORDER BY net_revenue DESC;

/* The chapter shows:
      segment   | net_revenue | share_pct 
   -------------+-------------+-----------
    Retail      |   556436454 |      48.5
    Wholesale   |   312728493 |      27.3
    Hospitality |   277476705 |      24.2
   (3 rows)
*/


-- How the new line works:

-- - SUM(s.net_revenue) on its own is each segment's total, as in step 1. - SUM(SUM(s.net_revenue))
-- OVER (): the inner SUM makes each segment's total (it belongs to GROUP BY); the outer SUM ...
-- OVER () adds those three totals across all rows, so every row can see the grand total of about
-- ₹1,14,66,41,651. The empty OVER () means "the window is every row". Chapter 13, section 13.3,
-- showed why a window can wrap an aggregate: grouping happens first. - 100 * ... / ... turns the
-- ratio into a percentage, and ROUND(..., 1) keeps one decimal place.

-- The three shares add up to 100.0%, and Retail's 48.5% is the "almost half" the bar chart shows.

-- =============================================================================================
-- What the eye notices first
-- =============================================================================================

-- Some visual differences are noticed before a person consciously looks for them, in a fraction of
-- a second. These pre-attentive attributes include color (one orange bar among gray ones), size,
-- position, orientation, enclosure (a box around something), and added marks (an arrow or a
-- label). They're the tools for directing attention.

-- Two consequences:

-- - One highlight works; many don't. A single orange line among gray ones pops out instantly.
-- Eleven colors don't pop out at all; the reader has to match each one to a legend, one by one
-- (section 15.10). - Every difference looks meaningful. If bars are different colors "for
-- variety", readers assume the colors mean something. Don't encode anything you don't intend to
-- communicate.

-- =============================================================================================
-- Working memory is small
-- =============================================================================================

-- People can hold only a few things in mind at once. A legend with eight entries forces readers to
-- remember eight color–name pairs while looking at the chart. That's why labeling lines and bars
-- directly (the name next to the line, the value at the end of the bar) is almost always better
-- than a legend, and why charts with more than about five or six categories in color usually need
-- a different design.

-- > Simplification note. Perception research is more nuanced than a ranked list: accuracy depends
-- on the task, the data, and the reader's familiarity with the chart type. The ranking is still
-- the most useful single guide for everyday business charts, and it explains most of the rules in
-- this chapter.

-- ---

-- =============================================================================================
-- 15.2 Start from the question
-- =============================================================================================

-- The most common charting mistake happens before any chart is drawn: starting from the data ("I
-- have sales by month and region, what chart can I make?") instead of the question ("Is our
-- festive peak getting bigger, and is it the same everywhere?"). The question decides the chart.

-- Figure 15.2 matches the kind of question to a chart. Three more questions sharpen the choice:

-- 1. Who is reading it, and where? A CEO scanning a slide on a phone needs one message in large
-- type. An analyst exploring data in a workbook can handle a detailed scatter plot. 2. Explore or
-- explain? Exploratory charts are for you: quick, many, rough, to find what's interesting.
-- Explanatory charts are for others: few, polished, each with one message. Most of this chapter is
-- about explanatory charts; section 15.5's distributions are also your main exploratory tools. 3.
-- What should they do next? If the chart should lead to a decision ("increase September stock"),
-- design it so that decision is the obvious conclusion, with the evidence visible.

-- Figure 15.2 — Start from the kind of question, then choose the chart. The alternatives column
-- matters: the first choice isn't always the best one for your data.

-- =============================================================================================
-- Levels of measurement decide what's allowed
-- =============================================================================================

-- Chapter 1 introduced levels of measurement. They constrain charts directly:

-- | Data | Examples | Chart implications | |---|---|---| | Nominal (categories with no order) |
-- segment, city, product | Sort bars by value, not alphabetically; don't connect categories with
-- lines | | Ordinal (ordered categories) | size band, rating, month name | Keep the natural order;
-- a line is acceptable across ordered periods | | Interval and ratio (numbers) | revenue,
-- quantity, order value | Histograms and box plots for distributions; scatter plots for
-- relationships; bars need a zero baseline (ratio) | | Time | order date, month | Time runs left
-- to right; lines show continuity; equal time gaps need equal spacing |

-- A line joining Retail, Wholesale, and Hospitality implies a trend from one to the next that
-- doesn't exist. A histogram of customer segments is really a bar chart. And a bar chart of
-- temperatures in °C with a zero baseline misleads, because 0 °C isn't "no temperature" (interval
-- data); a line or dot chart suits it better.

-- =============================================================================================
-- The table is a chart choice too
-- =============================================================================================

-- When readers need exact values (a price list, a monthly target sheet) or need to look up one
-- number among many, a well-formatted table beats a chart. Tables are also better for small
-- numbers of values with different units. Section 15.8 shows how to make a table that works like a
-- chart: aligned numbers, sensible rounding, and a heatmap-style shading.

-- ---

-- =============================================================================================
-- 15.3 Bar and column charts
-- =============================================================================================

-- Bar charts (horizontal) and column charts (vertical) compare values across categories by length.
-- They're the workhorse of business reporting, and the easiest chart to make better.

-- Figure 15.3 — Riverstone's 2025 revenue by product. Sorting, turning the bars horizontal,
-- labeling values, and using one color make the ranking readable in seconds.

-- =============================================================================================
-- Five rules for bars
-- =============================================================================================

-- 1. Start the value axis at zero. A bar's length is its value. If the axis starts at ₹10 crore, a
-- ₹20 crore bar looks twice as long as a ₹15 crore one, when it's only a third bigger. This is the
-- one rule in this chapter with no exceptions for bars. (Lines and dots are different; section
-- 15.4.) 2. Sort by value for nominal categories, so the ranking is visible. Keep the natural
-- order for ordinal ones (months, size bands). 3. Go horizontal when labels are long. Product
-- names such as "Food Container Set" fit on a horizontal bar chart without rotation; rotated text
-- is slow to read. 4. Label values directly when exact numbers matter, and then remove the value
-- axis and gridlines, which now repeat the labels. 5. Use one color, and add a second only to
-- highlight something (section 15.10).

-- In Figure 15.3's "after" version, Storage Box 25L leads at ₹23.1 crore, and the two smallest
-- products, Garden Chair (₹4.5 crore, sold only in March–May) and Water Bottle 1L (₹4.0 crore),
-- together sell less than any other single product.

-- =============================================================================================
-- Grouped and stacked bars
-- =============================================================================================

-- When each category splits into sub-groups, you have three choices:

-- - Grouped (clustered) bars put sub-groups side by side. Good for comparing sub-groups within
-- each category, with up to about three or four sub-groups. - Stacked bars put sub-groups on top
-- of each other. Good for comparing totals, and the bottom segment; hard for middle segments,
-- which don't share a baseline (section 15.7). - Small multiples: a separate small bar chart for
-- each sub-group, on the same scale. Often the clearest option once there are more than three sub-
-- groups.

-- =============================================================================================
-- Dot plots and lollipops
-- =============================================================================================

-- A dot plot replaces each bar with a dot on the value axis. Because dots encode by position, not
-- length, the axis doesn't need to start at zero, which makes dot plots ideal for comparing values
-- that are close together, such as attainment percentages between 92% and 112%. A lollipop chart
-- is a dot with a thin line back to the axis: a lighter-looking bar, with the same zero-baseline
-- rule as a bar.

-- =============================================================================================
-- In Excel and Google Sheets
-- =============================================================================================

-- Excel: select the data, Insert → Charts → Insert Column or Bar Chart → Clustered Bar. To sort,
-- sort the source data (largest at the bottom of the range for a horizontal bar chart, because
-- Excel plots the first row nearest the axis origin), or tick Format Axis → Axis Options →
-- Categories in reverse order on the category axis. Add values with Chart Elements (+) → Data
-- Labels, then delete the value axis and gridlines. Ctrl+1 opens the Format pane for whatever is
-- selected.

-- Google Sheets: Insert → Chart, then in the Chart editor → Setup → Chart type choose Bar chart.
-- Under Customize → Series, tick Data labels; under Customize → Gridlines and ticks, remove
-- gridlines. Sort the source range first (Data → Sort range).

-- > Watch out: pivot charts sort by the pivot. A pivot chart (Chapter 11) follows the pivot
-- table's order. Sort the pivot (Row Labels → More Sort Options → Descending by Sum of
-- net_revenue) rather than the chart.

-- ---

-- =============================================================================================
-- 15.4 Line charts
-- =============================================================================================

-- Line charts show change over a continuous dimension, almost always time. The line itself tells
-- the reader "these points are connected": each month follows the last.

-- Figure 15.4 — The same 36 months, two ways. The continuous line shows growth over time; one line
-- per year makes the seasonal pattern simple to compare.

-- The left chart answers "how has revenue changed over three years?": clear growth, with a yearly
-- rhythm. The right chart answers "is every year's season the same shape?": yes, weak June–July
-- and a peak in October, at a higher level each year. Same data, different question, different
-- chart.

-- The data behind the right chart is a pivot of month against year:

SELECT EXTRACT(MONTH FROM order_date) AS month,
       ROUND(SUM(net_revenue) FILTER (WHERE EXTRACT(YEAR FROM order_date) = 2024)) AS rev_2024,
       ROUND(SUM(net_revenue) FILTER (WHERE EXTRACT(YEAR FROM order_date) = 2025)) AS rev_2025
FROM sales_lines WHERE order_date >= '2024-01-01' GROUP BY 1 ORDER BY 1;

/* The chapter shows:
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
*/


-- How it works:

-- - EXTRACT(MONTH FROM order_date) turns each date into its month number, 1 to 12 (Chapter 12,
-- section 12.8). - SUM(net_revenue) FILTER (WHERE EXTRACT(YEAR FROM order_date) = 2024) adds up
-- only the 2024 rows; the next line does the same for 2025. This is the pivot pattern from Chapter
-- 13 (Pattern 9), with years as the columns. - WHERE order_date >= '2024-01-01' leaves out 2023,
-- which this table doesn't need. - GROUP BY 1 means "group by the first column in the SELECT list"
-- (here, the month). It saves retyping a long expression. ORDER BY 1 works the same way: sort by
-- the first column.

-- October 2025 (₹18,06,20,103) was 22.7% above October 2024 (₹14,72,21,566): the kind of
-- comparison the year-over-year chart makes visible.

-- =============================================================================================
-- Rules for lines
-- =============================================================================================

-- 1. Time runs left to right, with equal spacing for equal time. If a month is missing, leave a
-- gap or mark it; don't let the chart squeeze the axis so that a two-month jump looks like one
-- month. 2. The zero baseline is optional. A line encodes by position, not length, so the axis can
-- start near the data when change is the message. But say so with a clearly labeled axis, and
-- don't zoom in so far that noise looks like drama (section 15.12). 3. Label lines directly at
-- their right-hand end instead of using a legend. The right chart in Figure 15.4 does this. 4.
-- Limit the number of lines. Up to about four or five lines are readable. Beyond that, highlight
-- one or two and gray the rest (section 15.10), or use small multiples. 5. Use markers only when
-- the points matter. Markers on 36 monthly points add clutter; markers on 5 yearly points help. 6.
-- Don't use a line for categories. A line from Retail to Wholesale suggests a trend that doesn't
-- exist (section 15.2).

-- =============================================================================================
-- Annotate events
-- =============================================================================================

-- A line chart becomes an explanation when it says why something happened: "price increase", "new
-- Kolkata branch system", "festive season". Add a short annotation at the point, with a thin
-- leader line if needed. One to three annotations are usually enough.

-- =============================================================================================
-- Dual axes, and why to avoid them
-- =============================================================================================

-- A dual-axis chart plots two measures with different units against two vertical axes, for example
-- revenue on the left and gross margin percentage on the right. It looks efficient and misleads
-- readily, because the chart-maker chooses both scales, and so chooses where the lines cross and
-- whether they appear to move together. Section 15.12 shows a Riverstone example. Better
-- alternatives: two small charts stacked with aligned time axes; or index both measures to 100 at
-- the start and plot them on one axis; or put the second measure in labels.

-- =============================================================================================
-- Column charts for few periods, sparklines for many series
-- =============================================================================================

-- For a handful of periods (four quarters, three years), a column chart is often clearer than a
-- line, because each period is a separate, comparable total. For many series in a table (a
-- sparkline per branch), Excel's Insert → Sparklines → Line and Google Sheets' =SPARKLINE(B2:M2)
-- draw a tiny line inside a cell: no axes, only the shape.

-- ---

-- =============================================================================================
-- 15.5 Distributions: histograms and box plots
-- =============================================================================================

-- Averages hide shape. Chapter 4 showed that only 70 of Riverstone's 173 orders were above the
-- "average" order: one number hid the shape of the data. Distribution charts show the shape: where
-- most values are, how spread out they are, whether the data is skewed, and where the outliers are
-- (Chapter 14, section 14.6).

-- =============================================================================================
-- Histograms
-- =============================================================================================

-- A histogram groups a numeric variable into bins (ranges of equal width) and draws a bar for the
-- count in each bin. The bars touch, because the bins are continuous.

-- A coarse first look at Riverstone's 46,356 non-cancelled 2025 orders, in ₹25,000 bins:

WITH order_values AS (
  SELECT order_id, SUM(net_revenue) AS order_value FROM sales_lines
  WHERE order_date BETWEEN '2025-01-01' AND '2025-12-31' GROUP BY order_id
)
SELECT FLOOR(order_value / 25000) * 25000 AS bin_start, COUNT(*) AS orders
FROM order_values GROUP BY 1 ORDER BY 1;

/* The chapter shows:
    bin_start | orders 
   -----------+--------
            0 |  27627
        25000 |  14222
        50000 |   3718
        75000 |    657
       100000 |    122
       125000 |     10
   (6 rows)
*/


-- How it works:

-- - The CTE order_values (Chapter 13, section 13.2) adds up each order's lines, so there is one
-- row per order with its order_value. - FLOOR(order_value / 25000) * 25000 assigns every order to
-- the start of its bin. FLOOR rounds a number down to the whole number below it, like Chapter 11's
-- FLOOR.MATH. By hand, for an order of ₹37,480: 37,480 ÷ 25,000 = 1.4992; FLOOR makes it 1; 1 ×
-- 25,000 = 25,000, so the order falls in the ₹25,000–₹49,999 bin. - COUNT(*) with GROUP BY 1
-- counts the orders in each bin, and ORDER BY 1 lists the bins from the lowest.

-- Most orders are under ₹25,000, and the counts fall quickly after that: a right-skewed
-- distribution, common for money.

-- Six bars is only a first look. What happens if you change the bin width? Before you run the next
-- query, predict: with bins five times narrower (₹5,000), roughly how many bars will there be, and
-- will the tallest bar still be the first one? The only change is 25000 to 5000, in both places:

WITH order_values AS (
  SELECT order_id, SUM(net_revenue) AS order_value FROM sales_lines
  WHERE order_date BETWEEN '2025-01-01' AND '2025-12-31' GROUP BY order_id
)
SELECT FLOOR(order_value / 5000) * 5000 AS bin_start, COUNT(*) AS orders
FROM order_values GROUP BY 1 ORDER BY 1;

/* The chapter shows:
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
*/


-- Change "Wholesale" to "Retail" or "Hospitality" for the other segments. Rounded to whole rupees:

-- | Segment | Orders | Q1 (₹) | Median (₹) | Q3 (₹) | Largest (₹) | |---|---:|---:|---:|---:|---:|
-- | Hospitality | 12,432 | 10,212 | 19,122 | 31,000 | 1,15,550 | | Retail | 23,865 | 10,750 |
-- 19,425 | 32,275 | 1,13,430 | | Wholesale | 10,059 | 13,340 | 25,762 | 43,826 | 1,43,175 |

-- (Hospitality's Q1 is ₹10,212.50 and Wholesale's median ₹25,762.50 before rounding.)

-- =============================================================================================
-- The same numbers in SQL (optional, PostgreSQL)
-- =============================================================================================

-- PostgreSQL can calculate quartiles too, with a function you haven't met yet. This is optional:
-- the spreadsheet route above gives the same numbers.

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

/* The chapter shows:
      segment   | orders |  q1   | median |  q3   |  max   
   -------------+--------+-------+--------+-------+--------
    Hospitality |  12432 | 10212 |  19122 | 31000 | 115550
    Retail      |  23865 | 10750 |  19425 | 32275 | 113430
    Wholesale   |  10059 | 13340 |  25762 | 43826 | 143175
   (3 rows)
*/


-- How it works:

-- - The CTE order_values makes one row per order, now with the customer's segment from the join. -
-- PERCENTILE_CONT(0.25) asks for the value a quarter (0.25) of the way through the sorted values:
-- Q1. 0.5 is the median and 0.75 is Q3. "CONT" stands for continuous: like QUARTILE.INC, it
-- interpolates between two values when needed, which is why the results match the spreadsheet. -
-- WITHIN GROUP (ORDER BY order_value) says which column to sort before counting a quarter of the
-- way through. It's needed because a percentile only makes sense on sorted values. - GROUP BY
-- segment makes the calculation run once per segment, like SUM does; ROUND(...) gives whole
-- rupees, and MAX(order_value) is the largest order. - ORDER BY median sorts the segments from the
-- smallest median.

-- PERCENTILE_CONT is PostgreSQL's; MySQL doesn't have it, so in MySQL use the spreadsheet route
-- above or the window-function query in section 15.15.

-- Figure 15.6 — Box plots compare distributions across groups. Wholesale orders are larger and
-- more variable; Retail and Hospitality are nearly identical.

-- The box plots show what a bar chart of averages would hide: Retail and Hospitality orders are
-- almost identical in size (medians ₹19,425 and ₹19,122), while the middle half of Wholesale
-- orders spans ₹13,340 to ₹43,826. All three segments have a long right tail of large orders,
-- shown as dots. For money data those dots are usually real big orders, not errors: the IQR rule
-- flags unusual values, and Chapter 14's business limits decide whether they're wrong.

-- > Watch out: box plots hide the number of values and gaps. A box from 12 orders looks as solid
-- as one from 12,000, and a box plot can't show that a distribution has two peaks. Add the count
-- to the label, and look at a histogram as well when exploring.

-- =============================================================================================
-- Other distribution charts
-- =============================================================================================

-- - Strip plots and dot plots draw every value as a dot along one axis, with a little random
-- vertical jitter so dots don't hide each other. Best for small groups (up to a few hundred
-- values). - Density curves smooth a histogram into a line. Good for comparing a few overlapping
-- distributions; harder to explain to a business audience. - Violin plots mirror a density curve
-- around a center line. Common in data science, rarely needed in business reports.

-- =============================================================================================
-- In Excel and Google Sheets
-- =============================================================================================

-- Excel (2016 and later): select the order values, Insert → Insert Statistic Chart → Histogram;
-- set the bin width in Format Axis → Axis Options → Bin width. Insert → Insert Statistic Chart →
-- Box and Whisker draws box plots; with a category column next to the values, it draws one box per
-- category. Excel's box plot uses its own quartile method (Inclusive or Exclusive median, set in
-- Format Data Series), which can differ slightly from QUARTILE.INC.

-- Google Sheets: Insert → Chart → Chart type → Histogram chart, with Customize → Histogram →
-- Bucket size. Sheets has no built-in box plot; the usual workaround is a candlestick chart built
-- from Q1, median, Q3, minimum, and maximum, or QUARTILE.INC values in a table.

-- ---

-- =============================================================================================
-- 15.6 Relationships: scatter plots
-- =============================================================================================

-- A scatter plot places each record at the position of two numeric values, one on each axis. It
-- answers "do these two measures move together?", and it's the chart most likely to reveal
-- something a summary number hides.

-- The usual summary number for a relationship is the correlation: a number from −1 to +1 that says
-- how closely two measures follow a straight line together. +1 is a perfect rising line, 0 is no
-- straight-line pattern, and −1 is a perfect falling line. In a spreadsheet, =CORREL(range1,
-- range2) returns it, with the two measures in two ranges of the same length. Chapter 22, section
-- 22.5, shows how it's calculated and where it misleads; the next example shows the first warning.

-- =============================================================================================
-- Why you must look: Anscombe's quartet
-- =============================================================================================

-- In 1973 the statistician Francis Anscombe published four small datasets designed to make one
-- point. Each has 11 points. In all four, the mean of x is 9, the mean of y is 7.50, the
-- correlation between x and y is 0.82, and the best-fitting straight line is the same: y = 3.00 +
-- 0.500x. By every summary statistic, they're the same data.

-- Figure 15.7 — Anscombe's quartet. Identical summaries, four different relationships: roughly
-- linear, curved, linear with an outlier, and no relationship except one influential point.

-- Only the charts show that the second relationship is a curve, the third is a perfect line
-- spoiled by one outlier, and the fourth has no relationship at all apart from a single point. You
-- can check the numbers yourself with anscombe.csv in the chart data (exercise 14).

-- =============================================================================================
-- Riverstone's customers: orders against revenue
-- =============================================================================================

-- Each dot in Figure 15.8 is one of the 4,599 customers who ordered in 2025, placed by their
-- number of orders and their 2025 net revenue.

-- Figure 15.8 — Overplotting hides how many customers sit in each area. Transparency and jitter
-- reveal density; color adds the segment.

-- The relationship is strong (a correlation of 0.916: customers who order more often spend more,
-- which is hardly surprising) but the "before" chart hides how many customers sit at each point,
-- because thousands of dots overlap. This is overplotting. The fixes:

-- - Smaller, transparent dots, so dense areas look darker. - Jitter: a small random offset when
-- one variable takes whole-number values (orders are 1, 2, 3…), so dots don't stack exactly. - A
-- heatmap of binned values (a 2D histogram) when there are tens of thousands of points. - Color
-- for a category, used sparingly: here, it shows that Wholesale customers tend to spend more per
-- order.

-- =============================================================================================
-- Rules for scatter plots
-- =============================================================================================

-- 1. Put the likely cause on the x-axis and the effect on the y-axis (orders → revenue; discount →
-- quantity). 2. Start axes where the data is, not necessarily at zero; scatter plots encode by
-- position. 3. Consider a log scale when values span several orders of magnitude (Riverstone's
-- 2025 customers range from under ₹5,000 to over ₹10 lakh). On a log scale, ₹1,000, ₹10,000,
-- ₹1,00,000, and ₹10,00,000 are equally spaced: each step is ten times the last. Label it clearly
-- ("log scale") because many readers won't notice. 4. Add a trend line only if it helps, and never
-- let it stand in for looking at the points. Anscombe's quartet has the same trend line four
-- times. 5. Correlation isn't causation. A scatter plot shows that two measures move together, not
-- why (Chapter 21 and Chapter 22 return to this).

-- Excel: Insert → Insert Scatter (X, Y) or Bubble Chart → Scatter; add a trend line with Chart
-- Elements (+) → Trendline; set transparency in Format Data Series → Marker → Fill → Transparency.
-- Google Sheets: Chart type → Scatter chart; Customize → Series → Trendline; point size under
-- Customize → Series → Point size.

-- ---

-- =============================================================================================
-- 15.7 Parts of a whole: stacked bars, pies, and waterfalls
-- =============================================================================================

-- =============================================================================================
-- Stacked and 100% stacked bars
-- =============================================================================================

-- A stacked bar shows a total and its parts. A 100% stacked bar shows only the shares, each bar
-- reaching 100%.

-- Figure 15.9 — Left: a stacked column chart shows monthly totals and the bottom segment clearly;
-- the middle segments are hard to compare. Right: a waterfall explains a change from one total to
-- another.

-- The stacked chart answers "which months are biggest, and how much of each month is Storage?"
-- well, because totals and the bottom segment (Storage) share a baseline. It answers "did
-- Industrial grow from August to October?" badly: Industrial floats on top of Kitchen, so its
-- segments start at different heights. If the middle segments matter, use small multiples or a
-- grouped bar instead.

-- Keep stacks readable:

-- - Put the most important or most stable segment at the bottom, next to the baseline. - Use no
-- more than four or five segments; group the rest into "Other". - Keep the same order in every
-- bar, and in the legend (or label segments directly on the last bar).

-- =============================================================================================
-- Pies: when they're acceptable
-- =============================================================================================

-- Pie charts are unpopular with visualization experts for the reasons in section 15.1: angles and
-- areas are hard to compare. They're still acceptable when all of these are true:

-- - the parts add up to a meaningful whole (100% of something); - there are two or three parts; -
-- the message is a simple share, such as "Retail is almost half of revenue"; - exact comparison
-- between the parts isn't the point.

-- A donut chart is a pie with a hole; it has the same weaknesses and doesn't fix them. 3D pies are
-- never acceptable: the tilt makes front slices look bigger than back slices of the same size.

-- =============================================================================================
-- Waterfall charts
-- =============================================================================================

-- A waterfall chart (bridge chart) explains how one total became another: a starting bar, floating
-- bars for each positive or negative change, and an ending bar. It's the standard way to answer
-- "why did revenue change?" in a management pack.

-- The right side of Figure 15.9 is built from the change by segment:

-- | Segment | 2024 (₹) | 2025 (₹) | Change (₹) | |---|---:|---:|---:| | Retail | 44,38,10,189 |
-- 55,64,36,454 | +11,26,26,265 | | Wholesale | 23,84,57,929 | 31,27,28,492 | +7,42,70,563 | |
-- Hospitality | 22,07,47,358 | 27,74,76,705 | +5,67,29,347 | | Total | 90,30,15,475 |
-- 1,14,66,41,651 | +24,36,26,176 |

-- (The 2025 Wholesale figure is ₹31,27,28,492.50 before rounding, which is why section 15.1's
-- query shows 312728493 and this table ₹31,27,28,492. Each figure is rounded on its own, so rows
-- can differ from the total by ₹1.) Sorting the changes from largest to smallest shows at a glance
-- that Retail contributed the most growth. Waterfalls also handle negative steps (a lost customer,
-- a price cut), which are drawn downward, usually in a contrasting color.

-- Excel (2016 and later): Insert → Insert Waterfall, Funnel, Stock, Surface, or Radar Chart →
-- Waterfall; then select the total bars and tick Set as total in Format Data Point. Google Sheets:
-- Chart type → Waterfall chart; add the totals with Customize → Series → Add subtotal, or include
-- them as rows and mark them.

-- =============================================================================================
-- Treemaps
-- =============================================================================================

-- A treemap fills a rectangle with nested rectangles sized by value, for example every city within
-- its region. It shows the biggest parts of a large hierarchy at once, but compares values by
-- area, the weakest encoding for exact comparisons. Use it for "where is most of the revenue?"
-- across dozens of categories, not for ranking.

-- ---

-- =============================================================================================
-- 15.8 Heatmaps and tables
-- =============================================================================================

-- A heatmap is a table whose cells are shaded by value. It's the best chart for a two-way
-- question, such as "which months and which regions are strongest?", when there are too many
-- combinations for bars or lines.

-- Figure 15.10 — Top: a sequential palette for amounts. Bottom: a diverging palette for
-- performance against a midpoint (100% of target).

-- The top heatmap shows two patterns at once: across the rows, West is the largest region every
-- month; down the columns, October is the peak everywhere. The "City missing" row is the ₹2.3
-- crore of 2025 revenue from customers with no city (Chapter 14), kept visible instead of dropped.

-- The bottom heatmap shows attainment: revenue as a percentage of target, month by month. Because
-- the meaningful midpoint is 100%, it uses a diverging palette: red for below target, blue for
-- above, and near-white for on target. Two things stand out that a line chart of revenue would
-- hide: 2025 started well above target (110% and 112% in January and February), and every month
-- from August to December missed, with October the worst at 92%.

-- =============================================================================================
-- Rules for heatmaps
-- =============================================================================================

-- 1. Choose the palette by the data (section 15.10): sequential (light to dark) for amounts,
-- diverging for above-and-below a meaningful midpoint. 2. Put numbers in the cells when readers
-- need values, with text color that contrasts with the shade. 3. Order rows and columns
-- meaningfully: time in order; categories sorted by total, or grouped. 4. Don't compare rows with
-- very different scales in one color scale: one large region can wash out the others. Shade each
-- row separately, or show percentages, if the within-row pattern is the point.

-- =============================================================================================
-- Tables that work like charts
-- =============================================================================================

-- Chapter 10 and Chapter 11 formatted tables for reading; the same principles make a table an
-- effective visual:

-- - Right-align numbers and use the same number of decimals, so digits line up. - Round to what
-- matters. ₹18.1 crore is easier to read than ₹18,06,20,103 on a management slide; keep full
-- values in the appendix or the workbook. - Remove heavy borders; light horizontal rules or
-- alternating shading are enough. - Highlight with restraint: conditional formatting (Excel: Home
-- → Conditional Formatting → Color Scales; Sheets: Format → Conditional formatting → Color scale)
-- turns a table into a heatmap; data bars (Conditional Formatting → Data Bars) add in-cell bars. -
-- Add sparklines for a trend beside each row (section 15.4).

-- ---

-- =============================================================================================
-- 15.9 Maps
-- =============================================================================================

-- A map is the right chart when location itself is part of the answer: which areas are close to
-- each other, where the gaps are, how far customers are from a warehouse. It's often the wrong
-- chart when location is only a label: "revenue by region" is a ranking question, and a sorted bar
-- chart answers it more accurately than shaded shapes of different sizes.

-- Two common kinds:

-- - Filled (choropleth) maps shade each area (state, district) by a value. Their weakness: big
-- areas dominate visually, regardless of their values, and small, dense areas (Mumbai, Delhi)
-- almost disappear. Shade by rates or shares (revenue per customer, % of target), not raw totals,
-- which mostly reflect population. - Symbol (dot or bubble) maps place a marker at each location,
-- sized or colored by value. Better for cities, and for showing concentration; bubbles compare by
-- area, so add labels for key values.

-- For Riverstone, a map of 39 cities could show that revenue is concentrated along the west coast
-- and in the metros. But "which cities bring the most revenue?" is better as a sorted bar chart of
-- the top ten cities: Mumbai ₹9.7 crore, Delhi ₹8.6 crore, Bengaluru ₹7.0 crore, and so on.

-- Excel: Insert → Maps → Filled Map shades countries, states, and districts from place names (it
-- looks names up online, so it needs an internet connection and can misread ambiguous names).
-- Google Sheets: Chart type → Geo chart for countries and regions. For city-level symbol maps with
-- custom boundaries, BI tools such as Power BI (Chapter 16) are better.

-- > Watch out: maps and missing locations. Customers with no city don't appear on a map at all,
-- and nothing tells the reader they're missing. Say how much is missing in a note ("₹2.3 crore of
-- revenue has no city and isn't shown").

-- ---

-- =============================================================================================
-- 15.10 Color with meaning
-- =============================================================================================

-- Color is the strongest pre-attentive attribute and the most abused. The principle: color should
-- mean something, and the same thing everywhere in a report.

-- =============================================================================================
-- Three kinds of palette
-- =============================================================================================

-- | Palette | Use for | Looks like | Riverstone example | |---|---|---|---| | Categorical
-- (qualitative) | Unordered groups | Distinct hues of similar strength | Retail, Wholesale,
-- Hospitality | | Sequential | Ordered amounts, low to high | One hue from light to dark | Revenue
-- by region and month | | Diverging | Values around a meaningful midpoint | Two hues meeting at a
-- light neutral | % of target around 100 |

-- Using the wrong kind is a common, subtle error. A rainbow (red, orange, yellow, green, blue) for
-- an ordered amount has no natural "more" direction, and bright yellow in the middle draws the eye
-- to middling values. A diverging palette for plain revenue invents a midpoint that means nothing.

-- =============================================================================================
-- Highlight, don't decorate
-- =============================================================================================

-- The most effective use of color in business charts is one highlight color against gray, as
-- Figure 15.11 shows.

-- Figure 15.11 — Eleven colors force the reader to decode a legend. Gray for context and one color
-- for the story make the point immediately.

-- The "before" chart asks the reader to match eleven colors to eleven names. The "after" chart has
-- one message: Rahul Mehta leads, and every rep follows the same seasonal shape. If the next slide
-- is about a different rep, highlight that rep instead; the gray context stays the same.

-- =============================================================================================
-- Consistency across a report
-- =============================================================================================

-- - Assign colors to things, not positions. If Wholesale is green on one chart, it's green on
-- every chart, even when it's the first bar instead of the second. - Keep "good" and "bad" colors
-- consistent and don't reuse them for categories. If red means "below target", don't also use red
-- for the East region. - Use your organization's palette where one exists, but check it against
-- the rules below; brand colors aren't always readable.

-- =============================================================================================
-- Color vision deficiency
-- =============================================================================================

-- About 1 in 12 men and 1 in 200 women have some form of color vision deficiency, most often
-- difficulty distinguishing red from green. In a management team of twelve men, the odds are good
-- that at least one reader can't tell your red "missed" from your green "achieved".

-- - Avoid red–green as the only distinction. Use blue–orange or blue–red diverging palettes
-- (Figure 15.10 uses red–blue). - Use color-blind-safe categorical palettes, such as the Okabe–Ito
-- palette, designed to stay distinct for common types of color vision deficiency. - Don't rely on
-- color alone. Add direct labels, patterns, markers, or position, so the chart still works in
-- grayscale. Printing it in black and white is a quick test. - Simulate: tools such as Coblis (a
-- free web-based color-blindness simulator) and the accessibility checks in design tools show how
-- a chart looks to people with different types of color vision.

-- =============================================================================================
-- Contrast
-- =============================================================================================

-- Text and important marks need enough contrast with the background. The Web Content Accessibility
-- Guidelines (WCAG) ask for a contrast ratio of at least 4.5:1 for normal text and 3:1 for large
-- text and essential graphical elements such as lines and bars. Pale yellow on white fails; dark
-- gray on white passes. Free contrast checkers (for example WebAIM's) calculate the ratio from two
-- color codes.

-- Excel: Page Layout → Colors sets a workbook color theme; Format Data Series → Fill colors one
-- series, and clicking a single bar twice selects only that bar. Google Sheets: Customize → Series
-- → Format data point colors one bar; Format → Theme sets chart colors for the spreadsheet.

-- ---

-- =============================================================================================
-- 15.11 Titles, labels, annotations, and clutter
-- =============================================================================================

-- =============================================================================================
-- Titles that state the finding
-- =============================================================================================

-- Most business charts have a label for a title: "Monthly Revenue vs Target 2025". It tells
-- readers what they're looking at, and leaves them to work out what it means. An action title (or
-- headline) states the finding, so the chart supports a sentence instead of starting a puzzle.

-- Figure 15.12 — The same data. The top chart describes; the bottom chart explains, with a finding
-- in the title, direct labels, and one annotation.

-- The data behind it takes two steps: first each month's revenue, then the join to the targets.
-- Step 1 is a CTE (Chapter 13, section 13.2) that totals revenue by month; the LIMIT 3 is only
-- there to check the first rows:

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

/* The chapter shows:
        m      | net_revenue 
   ------------+-------------
    2025-01-01 |    85195521
    2025-02-01 |    78582579
    2025-03-01 |   101009066
   (3 rows)
*/


-- How it works: DATE_TRUNC('month', order_date) rounds each date down to the first day of its
-- month, and ::date turns the result into a plain date (both from Chapter 12, section 12.8), so
-- every order in January 2025 gets 2025-01-01. GROUP BY 1 adds up the revenue for each of those
-- month starts. The dates look like 2025-01-01 because that's how sales_targets stores its months,
-- which is what lets step 2 match them.

-- Step 2 keeps the CTE and replaces the final SELECT with a join to sales_targets:

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

/* The chapter shows:
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
*/


-- TEXT(B14,"0.0%") turns the number into text with a percentage format of one decimal place, and &
-- joins the pieces into one sentence. Then select the chart title, type = in the formula bar,
-- click C14, and press Enter. When next month's data arrives, the title changes with it.

-- Google Sheets. Insert → Chart opens the Chart editor: Setup for the chart type and ranges,
-- Customize for titles, series colors, labels, gridlines, and axes. Sheets has no chart templates;
-- copy a finished chart (⋮ → Copy chart) and change its data range instead. =SPARKLINE(range,
-- {"charttype","bar"}) draws in-cell bars; the braces hold an option name and its value.

-- In both tools, it's common to add a new month of data and not notice that the chart's range
-- didn't grow to include it. Base charts on a table (Excel, Ctrl+T) or a named range that grows,
-- as Chapter 11 recommended for formulas.

-- ---

-- =============================================================================================
-- 15.15 Running this chapter's SQL in MySQL
-- =============================================================================================

-- Most of this chapter's SQL runs unchanged in MySQL 8.0: the segment shares in section 15.1
-- (MySQL has the same window over an aggregate) and both histogram queries in section 15.5 (FLOOR
-- is the same) return exactly the same rows. Three PostgreSQL features don't exist in MySQL. The
-- companion file companion/ch15/ch15_queries_mysql.sql has every query in its MySQL form.

-- <!-- db: riverstone_full -->

-- FILTER and EXTRACT (section 15.4). MySQL has no FILTER clause. Use SUM(CASE WHEN … THEN … END),
-- the form Chapter 13, section 13.9, showed; MONTH() and YEAR() replace EXTRACT:

SELECT MONTH(order_date) AS month,
       ROUND(SUM(CASE WHEN YEAR(order_date) = 2024 THEN net_revenue END)) AS rev_2024,
       ROUND(SUM(CASE WHEN YEAR(order_date) = 2025 THEN net_revenue END)) AS rev_2025
FROM sales_lines WHERE order_date >= '2024-01-01' GROUP BY 1 ORDER BY 1;

/* The chapter shows:
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
*/


-- CASE WHEN YEAR(order_date) = 2024 THEN net_revenue END gives the revenue on 2024 rows and
-- nothing (NULL) on the others, and SUM skips the NULLs, so the column adds up 2024 only. The
-- numbers match section 15.4.

-- DATE_TRUNC and ::date (section 15.11). MySQL builds the first day of the month with DATE_FORMAT
-- and converts it with CAST(... AS DATE), as Chapter 12, section 12.16, showed:

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

/* The chapter shows:
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
*/

