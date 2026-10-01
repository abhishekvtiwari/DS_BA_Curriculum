-- Chapter 16. Business Intelligence with Power BI
-- Practice SQL for POSTGRESQL, extracted from the chapter.
--
-- Riverstone Supplies is the worked example throughout the book. Load the database
-- first (companion/riverstone_setup_mini.sql, riverstone_2025_setup.sql, or
-- companion/full/riverstone_full_setup_postgresql.sql), then run these statements in order.
--
-- Each statement keeps the chapter's explanation above it and the chapter's own
-- result below it, marked as the chapter's. Run it yourself to see your own.
-- Source: manuscript/ch16-business-intelligence-with-power-bi.md


-- 2025: ₹24,735.56 (format: currency, 2 decimals).

-- All seven are in companion/ch16/measures.dax, ready to paste.

-- =============================================================================================
-- Check your measures against SQL
-- =============================================================================================

-- A measure you can't verify is a guess. Every number in this chapter has a SQL equivalent you can
-- run on riverstone_full. First, all three years:

-- <!-- db: riverstone_full -->

SELECT ROUND(SUM(net_revenue)) AS all_years
FROM sales_lines;

/* The chapter shows:
    all_years  
   ------------
    2663490235
   (1 row)
*/


-- ROUND(…) with one argument rounds to a whole number, as the card does. Then 2025, one column per
-- card:

SELECT ROUND(SUM(net_revenue)) AS revenue,
       COUNT(DISTINCT order_id) AS orders,
       COUNT(DISTINCT customer_id) AS customers,
       ROUND(SUM(net_revenue) / COUNT(DISTINCT order_id), 2) AS aov,
       ROUND(100 * (1 - SUM(product_cost) / SUM(net_revenue)), 1) AS gm_pct
FROM sales_lines
WHERE order_date >= '2025-01-01';

/* The chapter shows:
     revenue   | orders | customers |   aov    | gm_pct 
   ------------+--------+-----------+----------+--------
    1146641651 |  46356 |      4599 | 24735.56 |   27.5
   (1 row)
*/


-- For the year 2025 (a card, or the matrix total): Target ₹1,16,69,50,000, % of Target 98.3%, Gap
-- to Target −₹2,03,08,349. Riverstone finished the year just short of plan.

-- > Watch out: blank isn't zero. Revenue LY for any month of 2023 is blank, because there's no
-- 2022 data. YoY Growth % already returns blank there, because DIVIDE returns blank when the
-- denominator is blank. A plain subtraction doesn't: [Net Revenue] - [Revenue LY] would show all
-- of 2023's revenue as "growth". Where you need one, test first: > > dax > YoY Change = IF ( NOT
-- ISBLANK ( [Revenue LY] ), [Net Revenue] - [Revenue LY] ) > > > ISBLANK ( value ) is true when
-- the value is blank, NOT reverses it, and an IF with no third argument returns blank when the
-- test fails.

-- Check them against SQL. Year to date at the end of June 2025, and the same period last year:

SELECT ROUND(SUM(net_revenue) FILTER (WHERE order_date BETWEEN '2025-01-01' AND '2025-06-30')) AS ytd_jun_2025,
       ROUND(SUM(net_revenue) FILTER (WHERE order_date BETWEEN '2024-01-01' AND '2024-06-30')) AS ytd_jun_2024,
       ROUND(100.0*SUM(net_revenue) FILTER (WHERE order_date BETWEEN '2025-01-01' AND '2025-06-30')/SUM(net_revenue) FILTER (WHERE order_date BETWEEN '2024-01-01' AND '2024-06-30') - 100, 1) AS yoy_pct
FROM sales_lines;

/* The chapter shows:
    ytd_jun_2025 | ytd_jun_2024 | yoy_pct 
   --------------+--------------+---------
       499203925 |    379844027 |    31.4
   (1 row)
*/


-- How it works: FILTER (WHERE …) after an aggregate (Chapter 13) adds up only the rows that pass
-- its test, so one query can hold both periods side by side; yoy_pct divides one by the other,
-- times 100, minus 100. The first two match Revenue YTD and Revenue YTD LY in the June row.

-- And by quarter, so you can check a matrix of Net Revenue, Revenue LY, and YoY Growth % with
-- 'Date'[Quarter] on rows:

SELECT 'Q' || EXTRACT(QUARTER FROM order_date) AS quarter,
       ROUND(SUM(net_revenue) FILTER (WHERE EXTRACT(YEAR FROM order_date)=2025)) AS rev_2025,
       ROUND(SUM(net_revenue) FILTER (WHERE EXTRACT(YEAR FROM order_date)=2024)) AS rev_2024,
       ROUND(100.0*SUM(net_revenue) FILTER (WHERE EXTRACT(YEAR FROM order_date)=2025)/SUM(net_revenue) FILTER (WHERE EXTRACT(YEAR FROM order_date)=2024)-100,1) AS yoy_pct
FROM sales_lines WHERE order_date >= '2024-01-01' GROUP BY quarter ORDER BY quarter;

/* The chapter shows:
    quarter | rev_2025  | rev_2024  | yoy_pct 
   ---------+-----------+-----------+---------
    Q1      | 264787166 | 200889263 |    31.8
    Q2      | 234416760 | 178954764 |    31.0
    Q3      | 223564918 | 175230767 |    27.6
    Q4      | 423872808 | 347940682 |    21.8
   (4 rows)
*/


-- How it works:

-- - EXTRACT(QUARTER FROM order_date) gives the quarter as a number, 1 to 4, and || joins text
-- (Chapter 13), so 'Q' || 1 gives Q1, the same label as the date table's Quarter column. -
-- EXTRACT(YEAR FROM order_date)=2025 inside each FILTER sends each line to its year's column. -
-- GROUP BY quarter groups by the column named quarter in the SELECT; PostgreSQL lets you group by
-- an output name like this.

-- Growth slowed through the year, from 31.8% in Q1 to 21.8% in Q4, which is the honest version of
-- the story Chapter 15's management pack got wrong.

-- Notes that save hours:

-- - Time intelligence needs a marked date table with complete years. If Revenue LY is blank
-- everywhere, that's the first thing to check. - SAMEPERIODLASTYEAR shifts whatever dates are in
-- context, so it works for a month, a quarter, or a custom selection. DATEADD is the flexible
-- version: DATEADD ( 'Date'[Date], -1, YEAR ) shifts by one year, and -1, MONTH by one month. -
-- For a 4-4-5 or financial-year calendar, the built-in functions won't match the business
-- calendar; build the comparison with your own date columns (Financial Year, Period) and CALCULATE
-- (Exercise 23).

-- ---

-- =============================================================================================
-- 16.7 Designing the report page
-- =============================================================================================

-- Chapter 15's principles apply unchanged: start from the question, sort bars, label directly, use
-- one highlight color, write titles that state findings, and never truncate a bar axis. What's new
-- is that the reader can now interact, so the design has to guide that too.

-- Figure 16.4 — Riverstone's monthly pack as one page: four cards answer "how are we doing?", the
-- visuals below answer "why?", and everything else lives on drill-through pages.

-- =============================================================================================
-- Layout
-- =============================================================================================

-- - Follow the reading order: most important at the top left, supporting detail below and to the
-- right. A reader who stops after three seconds should still have the headline. - Use a grid.
-- Align visuals to the same edges and give them the same padding (Format → General → Properties
-- for exact position and size). Misalignment reads as carelessness. - One page, one question. "How
-- did we do this month?" is a page. "Which customers are slipping?" is another page, reached by
-- drill-through. - Keep cards to four or five. Each card needs a comparison, or it's a number
-- without meaning: revenue with % of target, margin with change in points. - Leave white space. A
-- page with twelve visuals is a wall; a page with six is a report.

-- =============================================================================================
-- The visuals
-- =============================================================================================

-- Power BI's standard visuals map directly onto Chapter 15's chart types: column/bar, line, combo,
-- scatter, map, matrix (a pivot table), card and KPI, gauge (avoid: it uses angle and area to show
-- one number), pie and donut (rarely), treemap, waterfall, funnel, ribbon, decomposition tree, and
-- key influencers.

-- Three that earn their place in a sales report:

-- - Matrix for the numbers people want to read exactly: region by month, with conditional
-- formatting as a heatmap (Chapter 15, section 15.8). - Waterfall for "why did revenue change?"
-- (Chapter 15, section 15.7): set the breakdown to Segment or Product. - Decomposition tree for
-- exploring a number down its dimensions, with the AI split option that suggests the dimension
-- with the biggest difference. Useful in a meeting; not a substitute for a designed page.

-- Custom visuals from AppSource fill gaps (small multiples, better bullet charts). Before using
-- one in a shared report, check who maintains it, whether it's certified by Microsoft, and whether
-- it sends data anywhere.

-- =============================================================================================
-- Interaction
-- =============================================================================================

-- - Slicers filter a page. Keep two or three (Year, Region, Segment), and set Edit interactions so
-- that a slicer or a visual filters the visuals it should. A common design: a chart filters its
-- neighbours (Filter), but cards stay on the whole selection (None). - The Filters pane holds
-- filters at three levels: visual, page, and all pages. Use "all pages" for a rule that never
-- changes, such as excluding cancelled orders if your fact table hasn't already (Riverstone's
-- has). - Drill-down (the arrows on a visual) moves through a hierarchy: Year → Quarter → Month,
-- or Region → City. - Drill-through sends the reader to a detail page with the clicked context:
-- right-click a region bar → Drill through → Customer detail, and that page opens filtered to the
-- region. - Tooltips can be a whole mini-page (Page information → Allow use as tooltip): hovering
-- a bar shows a small trend chart for that bar's category. - Bookmarks save a state (filters,
-- which visuals are visible) and can be attached to buttons: one button for "revenue view",
-- another for "margin view", on the same page. - Buttons, selection pane, and the sync-slicers
-- pane are how a page becomes a small application. Use them sparingly; every hidden state is
-- something a reader can get stuck in.

-- =============================================================================================
-- Themes and formatting
-- =============================================================================================

-- Set the View → Themes → Customize current theme once: colors (Chapter 15's palette, checked for
-- color vision deficiency), fonts, and default title formatting. Export it as a JSON theme file
-- and reuse it in every Riverstone report so charts look the same everywhere. Individual visual
-- formatting overrides the theme, which is exactly how inconsistency creeps in; prefer changing
-- the theme.

-- =============================================================================================
-- Accessibility, mobile, and performance of the page
-- =============================================================================================

-- - Alt text on each visual (Format → General → Alt text), stating what it shows and its finding,
-- as in Chapter 15. - Tab order (Selection pane → Tab order) so keyboard and screen-reader users
-- move through the page sensibly. - Mobile layout (View → Mobile layout) rearranges visuals into a
-- single column for phones: branch managers will open it on a phone. - Fewer visuals is faster.
-- Each visual is at least one query; a page with twenty visuals and five slicers can take seconds
-- to render.

-- ---

-- =============================================================================================
-- 16.8 A worked example: Riverstone's monthly pack
-- =============================================================================================

-- Here's the whole build, in the order you'd actually do it. Every number below is checkable with
-- SQL, and companion/ch16/expected_measures.md has the full list.

-- 1. Load. Connect to riverstone_full and load sales_lines (as Sales), customers, products,
-- employees, and sales_targets, as in section 16.2. In Power Query, rename the queries and
-- columns, and add Region to Customer from city_region.csv, with "City missing" for customers who
-- have no city.

-- 2. Model. Build the star from section 16.3, add the DAX date table, mark it, create
-- relationships, hide keys, rename fields.

-- 3. Measures. The base set from section 16.4, then the time intelligence from section 16.6, in
-- the _Measures table.

-- 4. Page 1, "Overview". Four cards (Net Revenue, % of Target, Gross Margin %, Orders), a line
-- chart of Net Revenue and Target by month, a sorted bar of revenue by region, a bar of revenue by
-- product, and slicers for Year, Region, and Segment.

-- With the Year slicer on 2025, the cards must read:

-- | Card | Value | |---|---| | Net Revenue | ₹1,14,66,41,651 | | % of Target | 98.3% | | Gross
-- Margin % | 27.5% | | Orders | 46,356 | | Average Order Value | ₹24,735.56 | | Customers | 4,599
-- |

-- 5. Check the region bar against SQL. The database has no region column, so the query types the
-- city-to-region list from city_region.csv into a VALUES list (Chapter 14, section 14.3):

SELECT COALESCE(r.region, 'City missing') AS region, ROUND(SUM(s.net_revenue)) AS rev_2025, COUNT(DISTINCT s.customer_id) AS customers
FROM sales_lines s JOIN customers c ON c.customer_id=s.customer_id
LEFT JOIN (VALUES
 ('Mumbai','West'),('Pune','West'),('Ahmedabad','West'),('Surat','West'),('Nashik','West'),('Nagpur','West'),('Indore','West'),('Goa','West'),('Vadodara','West'),('Rajkot','West'),('Thane','West'),('Aurangabad','West'),
 ('Bengaluru','South'),('Chennai','South'),('Hyderabad','South'),('Kochi','South'),('Coimbatore','South'),('Mysuru','South'),('Visakhapatnam','South'),('Madurai','South'),('Mangaluru','South'),('Thiruvananthapuram','South'),
 ('Delhi','North'),('Jaipur','North'),('Lucknow','North'),('Chandigarh','North'),('Udaipur','North'),('Kanpur','North'),('Ludhiana','North'),('Dehradun','North'),('Agra','North'),('Noida','North'),('Gurugram','North'),
 ('Kolkata','East'),('Bhubaneswar','East'),('Patna','East'),('Guwahati','East'),('Ranchi','East'),('Raipur','East')) AS r(city,region) ON r.city=c.city
WHERE s.order_date >= '2025-01-01' GROUP BY r.region ORDER BY rev_2025 DESC;

/* The chapter shows:
       region    | rev_2025  | customers 
   --------------+-----------+-----------
    West         | 383840549 |      1506
    South        | 318624642 |      1289
    North        | 279250231 |      1127
    East         | 142256284 |       586
    City missing |  22669946 |        91
   (5 rows)
*/


-- How it works:

-- - (VALUES ('Mumbai','West'), …) AS r(city, region) is a small table typed into the query: 39
-- rows, the same as city_region.csv, with its columns named city and region. - LEFT JOIN … ON
-- r.city=c.city is the SQL version of the Power Query merge: every customer keeps its row, and
-- those with no city get a NULL region. - COALESCE(r.region, 'City missing') replaces that NULL
-- with the label, as the Replace Values step did (Chapter 14). - COUNT(DISTINCT s.customer_id)
-- counts the customers who ordered in 2025 in each region.

-- The last row is ₹2,26,69,946 from 91 of the 100 customers with no city (Chapter 14): the other 9
-- didn't order in 2025. Because Power Query labelled them, Power BI shows a "City missing" bar
-- instead of a blank category. Chapter 15's rule applies: show it in gray rather than dropping it,
-- and the five bars add up to the Net Revenue card.

-- 6. Check the product bar:

SELECT p.product_name, ROUND(SUM(s.net_revenue)) AS rev_2025, ROUND(100*SUM(s.net_revenue)/SUM(SUM(s.net_revenue)) OVER (),1) AS share
FROM sales_lines s JOIN products p ON p.product_id=s.product_id WHERE s.order_date >= '2025-01-01'
GROUP BY p.product_name ORDER BY rev_2025 DESC LIMIT 4;

/* The chapter shows:
       product_name    | rev_2025  | share 
   --------------------+-----------+-------
    Storage Box 25L    | 231104138 |  20.2
    Food Container Set | 214380655 |  18.7
    Storage Box 10L    | 196381989 |  17.1
    Industrial Crate   | 152683090 |  13.3
   (4 rows)
*/


-- How it works:

-- - VALUES ( Customer[Customer] ) is the list of customer names in the current selection. - TOPN (
-- 1, table, [Net Revenue], DESC ) has four arguments: how many rows to keep (1), the table to take
-- them from, what to sort by (each name's [Net Revenue], by context transition), and the direction
-- (DESC, biggest first). It returns a table with one row. - A measure must return one value, not a
-- table. MAXX ( table, Customer[Customer] ) goes through that one-row table and returns the
-- largest name in it, which is the only name. (SELECTEDVALUE can't do this job: it takes a column,
-- not a table.) - Ties: if two customers tie for first place, TOPN returns both rows, and MAXX
-- then returns the name that sorts last alphabetically. Say so in the visual's tooltip if ties are
-- possible.

-- For 2025 it returns Galaxy Logistics Patna, with ₹10,73,806.50 (about ₹10.7 lakh). Check it with
-- SQL:

SELECT c.customer_name, ROUND(SUM(s.net_revenue), 2) AS revenue
FROM sales_lines s JOIN customers c ON c.customer_id = s.customer_id
WHERE s.order_date >= '2025-01-01'
GROUP BY c.customer_name ORDER BY revenue DESC LIMIT 1;

/* The chapter shows:
        customer_name      |  revenue   
   ------------------------+------------
    Galaxy Logistics Patna | 1073806.50
   (1 row)
*/

