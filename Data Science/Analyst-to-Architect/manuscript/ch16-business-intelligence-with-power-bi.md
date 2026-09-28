# Chapter 16. Business Intelligence with Power BI

*Part 2 — The Analyst*

> **Chapter at a glance**
>
> **You will learn to:** install Power BI Desktop and build a first report · explain what a BI tool does that a spreadsheet can't, and which Power BI licence buys what · load Riverstone's full dataset with Power Query and choose between Import and DirectQuery · build a star schema with a proper date table · write DAX measures from zero, and know when a measure beats a calculated column · use `CALCULATE` to change filter context deliberately · build time intelligence (year to date, same period last year, year-over-year growth) that survives slicers · design a report page with Chapter 15's principles, using cards, slicers, tooltips, drill-through, and bookmarks · publish, schedule refresh, use a gateway, and share with an app · apply row-level security so each region sees only its own customers · keep a model fast and avoid the modelling mistakes that make numbers wrong · recognize the same ideas in Tableau and Looker Studio.
>
> **Before you start:** Chapter 11 (Power Query, the Data Model, and DAX in Excel), Chapter 13 (SQL aggregation and the `sales_lines` view), Chapter 14 (cleaning: this chapter assumes clean data), and Chapter 15 (chart choice, color, titles: this chapter applies them rather than repeating them). You don't need any programming for this chapter. Python comes next, in Chapters 17 and 18.
>
> **Time needed:** 22–26 hours, spread over three weeks.
>
> **Tools:** **Power BI Desktop**, free, **Windows only**; section 16.0 installs it. On macOS or Linux you need a Windows virtual machine, a cloud Windows desktop, or a Windows computer at work or college. Publishing and sharing (sections 16.9 and 16.10) need the Power BI Service, which needs a **work or school account**. PostgreSQL or MySQL with `riverstone_full` (Chapter 14), or the CSV files, for the data.
>
> **Practice data:** the full Riverstone dataset (`companion/full/`), plus `companion/ch16/` which holds the chapter's DAX measures as text files, the expected value of every measure, the SQL that produces those values, a city-to-region table, and a `UserRegion` table for the security section.

---

## Why this matters

By the end of Chapter 15 you can clean a dataset, analyze it, and draw an honest chart. There's one thing left that separates an analyst's work from a report people rely on: **it has to stay true next month without you.**

That's what a BI tool does. You build the model once, and the report refreshes itself: new orders arrive, the numbers move, the branch heads open the same link and see today's figures. Nobody emails a workbook. Nobody asks "is this the latest version?" The 25 hours a year you'd spend rebuilding a monthly pack become 25 hours of analysis.

Power BI is the most common BI tool in Indian companies, and the one most analyst job descriptions name. The skills transfer: Tableau, Looker Studio, Qlik, and Metabase differ in syntax and menus, but every one of them asks you to model data, write measures, and design a report. Learning Power BI properly means learning that shape of work.

This chapter builds one thing: a live Riverstone sales report on the full three-year dataset, with measures that match to the rupee, security so each region sees only its own customers, and a refresh schedule. Then it shows what goes wrong, which is mostly modelling, not charting.

> **About screenshots.** Power BI's interface changes every month. This chapter describes what to click in words and explains the ideas behind it, so it stays useful when the buttons move. Where a menu name might have changed, check Microsoft's current documentation.

---

## In plain English

A spreadsheet is a **notebook**: you write the numbers in, and they stay as you left them. A BI tool is a **kitchen**: you write the recipe, and the dish gets made again with whatever arrives that morning.

Building a Power BI report is setting up that kitchen:

- **Power Query** is the prep station. Wash, chop, standardize: the cleaning steps from Chapter 14, recorded once so they repeat with every delivery.
- **The model** is how ingredients are organized: one shelf for customers, one for products, one for dates, and the big crate of order lines in the middle. Put things on the right shelves and every recipe is quick; pile them up anywhere and every dish takes an hour.
- **DAX measures** are the recipes: "net revenue" is written once and cooked correctly whether you ask for one region, one month, or the whole company.
- **The report page** is the plate: what the guest sees, arranged for them, not for you.
- **Refresh** is the standing delivery order, and **row-level security** is the rule that each table gets served only its own dish.

The most common beginner mistake is to keep working like a notebook: pasting values into the model, writing a formula for each cell, and making a new page for each region. The kitchen only pays off when the recipe is written once and the ingredients keep arriving.

---

## 16.0 Install Power BI Desktop and make your first report

This is the first chapter that uses Power BI, so start by installing it and proving it works on a small file. Allow 45–60 minutes, most of it download time.

### What you need

- **Windows 10 or Windows 11, 64-bit.** Microsoft's download page lists Windows 10, Windows 11, and Windows Server, on 64-bit (x64) machines only. Microsoft lists at least 2 GB of free memory (4 GB or more recommended) and a screen of at least 1440×900.
- **On a Mac or Linux:** Power BI Desktop doesn't run there. Pick one of three routes: a **virtual machine** (a program that runs a whole Windows computer inside a window on your own machine), a **cloud Windows desktop** you open in a browser, or a Windows computer at work or college. If none of those is possible, read the chapter and do its SQL checks, and build the report later on a borrowed Windows machine.

### Install it

There are two ways. Use one, not both: Microsoft doesn't support having the Store version and the downloaded version installed side by side, so uninstall one before installing the other.

1. **The Microsoft Store (recommended).** Open the **Microsoft Store** app (Windows' own app shop), search for **Power BI Desktop**, and click **Get** (or **Install**). Microsoft recommends this route: the Store keeps Desktop up to date by itself, downloads only the parts that changed, and doesn't need **administrator rights** (the permission to install software for every user of the computer, which work laptops often withhold).
2. **The download page.** Search the web for "Power BI Desktop download" and use the page on microsoft.com. It gives one installer, `PBIDesktopSetup_x64.exe` (about 660 MB in September 2026); run it and follow the steps. This route needs administrator rights, and you update Desktop yourself by downloading the new version each month.

**Check:** open Power BI Desktop. It may show a welcome screen asking you to sign in; close it. Desktop doesn't need an account (signing in only matters when you publish, in section 16.9). You should see an empty report canvas: a large white page in the middle.

### A tour of the screen

- **The views**, down the left edge. **Report view** is the canvas where you place visuals. **Table view** shows the rows of a loaded table, like a spreadsheet you can't type into. **Model view** shows the tables as boxes and the relationships between them. (Recent versions add more views, such as a DAX query view; this chapter doesn't need them.)
- **The panes**, down the right edge. **Filters** holds filters for a visual, a page, or the whole report. **Visualizations** holds the chart types, and under them the **wells** (the slots such as Columns, X-axis, and Values) that you fill with fields. **Data** lists every table and its columns.
- **The ribbon**, across the top: **Home** (getting data, publishing), **Insert**, **Modeling** (measures, tables, security roles), and **View**.

### Your first report in five minutes

You'll count Riverstone's customers by segment, from one CSV file.

1. **Home → Get data → Text/CSV**, choose `companion/full/customers.csv`, and click **Load** in the preview window. The Data pane now shows a table called `customers` with its five columns.
2. On the canvas, click the **Table** visual in the Visualizations pane. An empty frame appears.
3. In the Data pane, tick `segment`, then `customer_id`.

Before you look at the result, predict: what will Power BI do with `customer_id`, a column of numbers?

It adds them up. The table shows **Sum of customer_id**, which is a meaningless number: IDs are labels, not quantities. Power BI's default for any numeric column is to sum it.

4. In the **Columns** well, click the small arrow next to `Sum of customer_id` and choose **Count**. The column becomes **Count of customer_id**:

| segment | Count of customer_id |
|---|---|
| Hospitality | 1,513 |
| Retail | 2,791 |
| Wholesale | 723 |
| **Total** | **5,027** |

5. **File → Save as**, and save it as `first_report.pbix` in your working folder.

The total, 5,027, is Riverstone's number of customer records, as in Chapter 14. What happens if you change it to **Count (Distinct)**? Nothing, and that's a check in itself: every `customer_id` is different, so counting all of them and counting the distinct ones agree.

That's the whole Power BI loop in miniature: get data, choose a visual, drag fields into its wells, and check the aggregation. The rest of the chapter does the same thing on a proper model.

### If something goes wrong

| Problem | What to do |
|---|---|
| A download site offers "Power BI Desktop" with extras, or an old version | Use only the Microsoft Store or microsoft.com. Download sites that repackage installers can add unwanted software |
| The work laptop blocks installing | Try the Microsoft Store route, which needs no administrator rights. If the Store is blocked too, ask IT; a short, specific request ("Power BI Desktop from the Microsoft Store, for learning, no company data") is usually approved |
| You're on a Mac | Use a Windows virtual machine, a cloud Windows desktop, or a Windows computer at work or college (see "What you need") |
| Desktop asks you to sign in | Close the dialog. You need an account only to publish |
| A number column shows **Sum of …** | Change the aggregation in the well (step 4). Section 16.4 shows how measures avoid this for good |
| Later, connecting to MySQL asks for a "connector" | Section 16.2 covers it |

### An account for publishing, later

Desktop is free and needs no account. The **Power BI Service**, where reports are published and shared (section 16.9), is different: signing in needs a **work or school account**, meaning an email address from an employer or a college that uses Microsoft 365. Microsoft doesn't accept personal addresses such as Gmail or Outlook.com for the Service. If you don't have one, everything in this chapter up to section 16.8 works in Desktop, and so does testing security with **View as** in section 16.10; read section 16.9 as a walkthrough of what happens at work.

---

## 16.1 What Power BI is, and what it costs

### The pieces

![Power BI Desktop on Windows builds the report and publishes it to the Power BI Service in the browser, where a workspace holds the semantic model and reports, refreshes on a schedule through an on-premises gateway, and shares with readers who need a licence](figures/fig16-1-power-bi-pieces.svg)

*Figure 16.1 — Desktop builds it; the Service runs it on a schedule and shares it. Nothing you build is visible to anyone until you publish.*

- **Power BI Desktop** is the free Windows application you installed in section 16.0. It contains Power Query (the same engine as Excel's, Chapter 11), the data model, the DAX formula language, and the report designer. Its file is a `.pbix`.
- **The Power BI Service** (`app.powerbi.com`) is the cloud side: **workspaces** hold your published content, a **semantic model** (formerly "dataset") holds the data and the DAX, **reports** hold the pages, **dashboards** pin selected visuals from several reports, and an **app** is the polished, read-only package you hand to the business.
- **The on-premises data gateway** is a small program installed on a machine inside your network so the Service can refresh from a database it can't otherwise reach.
- **Power BI is part of Microsoft Fabric**, Microsoft's wider analytics platform. For an analyst, that mostly changes the words on the pricing page and the menus around the workspace; the Desktop, model, and DAX work in this chapter is unchanged.

### Licences, as of writing

Licensing decides who can see what you build, so check the current rules before promising anything. The table gives Microsoft's published list prices at the time of writing (September 2026).

| Licence | Price (US list) | What it allows |
|---|---|---|
| **Free** | $0 | Power BI Desktop, and personal workspaces in the Service. No sharing. |
| **Pro** | $14 per user per month | Publishing to shared workspaces, sharing with other Pro users, apps, 8 scheduled refreshes a day. Included with Microsoft 365 E5. |
| **Premium Per User (PPU)** | $24 per user per month | Pro plus larger models, 48 refreshes a day, paginated reports, deployment pipelines. **Everyone who views PPU content needs PPU.** |
| **Fabric capacity (F SKUs)** | From about $263 a month (F2), pay as you go | Shared compute instead of per-user licences. From **F64** upward, viewers with free licences can read content. |

Both per-user prices rose on 1 April 2025 (Pro from $10 to $14, PPU from $20 to $24) and were unchanged through 2026. The older Premium per-capacity P SKUs are no longer sold to new customers; Microsoft directs enterprise buyers to Fabric capacity instead. Prices are US list prices before tax and vary by country and agreement.

Two practical consequences:

1. **You can learn everything in Desktop for free; publishing needs a work or school account.** Desktop costs nothing, and everything up to publishing works without a licence or an account. Only the Service needs an account, and sharing needs Pro.
2. **Count the readers, not the authors.** A report for 300 branch staff at ₹1,200 a month each is a real budget line; the F64 threshold is where organizations switch to capacity so that viewers don't need paid seats.

### When a BI tool is the right answer

| Situation | Better answer |
|---|---|
| The same report, refreshed regularly, read by several people | **Power BI** |
| Many people need to slice the same data themselves | **Power BI** |
| Numbers must be consistent across teams (one definition of revenue) | **Power BI** (a shared semantic model) |
| A one-off analysis nobody will repeat | A spreadsheet (or, after Chapter 17, a Python notebook) |
| Heavy statistics, modelling, or machine learning | Python (Chapters 17–18; statistics in Chapters 21–22; machine learning in Part 4) |
| Ad-hoc data exploration by an analyst | SQL |
| A document with commentary and exhibits | A written report (Chapter 20) |

> **Watch out: Power BI is not a database.** It reads from sources and keeps a copy for speed. It's not where data should be corrected, and a model is not a substitute for a warehouse (Chapter 28 for modelling; Part 5, Chapter 49, for warehouses and lakehouses). If the fix belongs upstream, fix it upstream (Chapter 14, section 14.11).

---

## 16.2 Getting Riverstone's data in

### Connect

**Home → Get data** lists the connectors. This chapter uses the database you loaded in Chapter 14:

- **PostgreSQL database:** server `localhost`, database `riverstone_full`, then your PostgreSQL user name and password from Chapter 12. Power BI needs the Npgsql provider on older Desktop versions; recent versions ship it.
- **MySQL database:** needs the MySQL Connector/NET package installed, which Desktop will prompt for.
- **Text/CSV:** the files in `companion/full/` work too, if you'd rather not use a database; the box at the end of this subsection shows that route.

The **Navigator** window lists the tables and views. Tick five of them:

- `sales_lines`, the view you built in Chapter 13: one row per order line, cancelled orders already excluded, with `net_revenue` and `product_cost` computed. It becomes the fact table.
- `customers`, `products`, `employees`, and `sales_targets`.

Click **Transform Data** to open Power Query (**Load** skips it, which you rarely want). In the **Queries** list on the left, rename each query by double-clicking it, so the model reads in business language: `sales_lines` → **Sales**, `customers` → **Customer**, `products` → **Product**, `employees` → **Employee**, `sales_targets` → **Targets**.

After **Home → Close & Apply**, Table view shows each table's row count at the bottom of the screen. Yours should read: Sales **200,381** rows (all three years, cancelled orders left out), Customer **5,027**, Product **8**, Employee **16**, Targets **36**.

> **No database? The CSV route.** **Get data → Text/CSV** for `order_items.csv`, `orders.csv`, `customers.csv`, `products.csv`, `employees.csv`, and `sales_targets.csv`, then **Transform Data**. In Power Query, select `order_items` (209,006 rows) and build Sales from it:
>
> 1. **Home → Merge Queries**, choose `orders`, click `order_id` in both tables, **Join Kind: Left Outer**, OK. Expand the new column (the two-arrow icon in its header), tick `order_date`, `customer_id`, `sales_rep_id`, and `status`, and untick **Use original column name as prefix**. Still 209,006 rows: each line gets its order's details.
> 2. Open the filter arrow on `status` and untick **Cancelled**: 200,381 rows, the same lines as `sales_lines`.
> 3. **Merge Queries** again with `products` on `product_id`, and expand only `unit_cost`.
> 4. **Add Column → Custom Column** named `net_revenue`: `= [quantity] * [unit_price] * (1 - [discount_pct] / 100)`. Another named `product_cost`: `= [quantity] * [unit_cost]`. Set both to **Decimal Number**.
> 5. Rename `order_items` to **Sales**, and the other queries as above. Right-click `orders` and untick **Enable load**, so it's used for the merge but not loaded as a table of its own.
>
> Every measure and number in the rest of the chapter is the same on either route.

### Import or DirectQuery

Power BI asks how to connect:

| Mode | How it works | Use it when |
|---|---|---|
| **Import** | Data is copied into the model's in-memory engine, compressed. Fastest reports; needs refresh to update. | Almost always. This chapter uses Import. |
| **DirectQuery** | Every visual sends a query to the source. Always current; as fast as your database, and many DAX features are limited. | Data too large to import, or a real-time requirement |
| **Composite / Dual** | Some tables imported, some DirectQuery | Large fact table with small dimensions |
| **Live connection** | To an existing published semantic model or Analysis Services | Reusing a model someone else owns |

Riverstone's 200,381 order lines are tiny for Import: the model compresses to a few megabytes and every visual responds instantly. Import until you have a reason not to.

### Power Query here versus Chapter 14

The Power Query in Desktop is the one you learned in Chapter 11 and used for cleaning in Chapter 14, with the same ribbon and M language. The same rules apply: profile the whole dataset (**View → Column quality**, **Column distribution**, **Column profile**, and switch profiling to the entire dataset), and transform in recorded steps.

What changes is **where cleaning belongs**. Prefer, in order:

1. **Fix it in the source system**, so everyone benefits (Chapter 14's cleaning log exists for exactly this).
2. **Fix it in a database view or a warehouse table**, so every tool sees the same clean data.
3. **Fix it in Power Query**, when you can't do either.
4. **Fix it in DAX**, only for things that must respond to filters.

Riverstone follows that order already: the `sales_lines` view does the heavy work in the database (rule 2), so Power Query only adds what the report needs and the database doesn't have: a **region** for each customer, and business names for the columns.

### Add a region to each customer

The report groups customers into four regions, and the database has only a city. `companion/ch16/city_region.csv` maps each of Riverstone's 39 cities to its region. In Power Query:

1. **Home → New Source → Text/CSV**, choose `companion/ch16/city_region.csv`. It loads as a query with two columns, `city` and `region`, and 39 rows. Right-click it and untick **Enable load**: it's a lookup, not a table for the report.
2. Select **Customer**, then **Home → Merge Queries**: choose `city_region`, click `city` in both tables, **Join Kind: Left Outer**, OK. Expand the new column and tick only `region`.
3. Customers with no city (Chapter 14 found 100 of them) have nothing to match, so their `region` is `null`. Select the `region` column, **Transform → Replace Values**, and replace `null` with `City missing`. A blank category would vanish from charts; a named one stays visible (Chapter 15's rule).
4. Rename the columns into business language: `customer_name` → **Customer**, `city` → **City**, `segment` → **Segment**, `region` → **Region**. In Product, `product_name` → **Product**; in Employee, `employee_name` → **Employee**.

Check the result with a Table visual of `Region` and Count of `customer_id`:

| Region | Customers |
|---|---|
| West | 1,660 |
| South | 1,400 |
| North | 1,224 |
| East | 643 |
| City missing | 100 |
| **Total** | **5,027** |

These count every customer record. Customers who ordered in 2025 are fewer (4,599), and 91 of the 100 customers with no city are among them, which will matter in section 16.8.

**Query folding** matters here. When Power Query can translate your steps into SQL, the database does the work and only the result travels. Right-click a step → **View Native Query**: if it's greyed out, folding stopped at that step. Filters, column removal, renames, and simple type changes usually fold; merges with a CSV file, custom M functions, and index columns usually break it. Put the folding steps first.

> **Tool note: don't import what you don't need.** Remove columns you'll never show, filter to the years you report on, and drop helper columns before loading. Every column loaded costs memory and refresh time, and a column with many distinct values (an ID, a timestamp to the second) costs the most.

---

## 16.3 The model: a star schema and a date table

A **model** is a set of tables joined by relationships. Its shape decides whether DAX is simple or painful.

![Riverstone's star schema: a central Sales fact table of 200,381 order lines joined to Date, Customer, Product, and Employee dimensions, plus a second fact table of 36 monthly targets joined to Date](figures/fig16-2-star-schema.svg)

*Figure 16.2 — A star schema: one fact table per business event, one dimension per thing you filter or group by, everything joined through keys, and both fact tables sharing the Date dimension.*

### Facts and dimensions

- A **fact table** holds events, one row per event, with keys and numbers: here, one row per order line, with `order_id`, `customer_id`, `product_id`, `sales_rep_id`, `order_date`, `status`, `quantity`, `net_revenue`, and `product_cost`. It's long and narrow, and it's where the measures aggregate.
- A **dimension table** holds the things you slice by, one row each, with descriptive columns: Customer, Product, Employee, Date. Short and wide.
- **Relationships** run one-to-many from the dimension to the fact, and filters flow **down** that arrow: filtering Customer filters Sales, not the other way around (unless you switch cross-filtering to both, which you should avoid until you know why you need it).

This shape is called a **star schema** because the fact table sits in the middle with dimensions around it. It's not a Power BI quirk: it's the standard analytical model (Chapter 28 covers the theory, and Chapter 11's Data Model section showed the Excel version).

Riverstone's model:

| Table | Role | Rows | Key |
|---|---|---|---|
| Sales (the `sales_lines` view) | Fact | 200,381 | — |
| Targets (`sales_targets`) | Fact | 36 | `target_month` |
| Date | Dimension | 1,096 | `Date` |
| Customer | Dimension | 5,027 | `customer_id` |
| Product | Dimension | 8 | `product_id` |
| Employee | Dimension | 16 | `employee_id` |

Two fact tables at different grains (order lines by day, targets by month) is normal. They connect through the shared Date dimension, which is why a date table isn't optional.

**Create the relationships** in Model view. Desktop usually finds `customer_id` and `product_id` by itself, because the names match on both sides; check each line it drew. Drag `Sales[sales_rep_id]` onto `Employee[employee_id]` yourself. The Date relationships come after the next subsection.

### The date table

A date table has one row for every day, with the columns you group by. You build it in DAX as a **calculated table**: a table whose rows come from a formula, computed when the model refreshes. Build it in five small steps, checking the result in Table view after each one.

**Step 1: one row per day.** **Modeling → New table**, and type in the formula bar:

```dax
Date = CALENDAR ( DATE ( 2023, 1, 1 ), DATE ( 2025, 12, 31 ) )
```

How it works:

- `Date =` names the new table `Date`.
- `DATE ( 2023, 1, 1 )` builds a date from three numbers: year, month, day. This one is 1 January 2023; `DATE ( 2025, 12, 31 )` is 31 December 2025.
- `CALENDAR ( start, end )` returns a table with one column, also called `Date`, holding every day from the start to the end, inclusive.

Table view shows **1,096 rows**: 365 days in 2023, 366 in 2024 (a leap year), and 365 in 2025. The first row is 1 January 2023 and the last 31 December 2025.

**Step 2: add a Year column.** Click the formula bar again and wrap the table in `ADDCOLUMNS`:

```dax
Date =
ADDCOLUMNS (
    CALENDAR ( DATE ( 2023, 1, 1 ), DATE ( 2025, 12, 31 ) ),
    "Year", YEAR ( [Date] )
)
```

How it works:

- `ADDCOLUMNS ( table, "name", expression )` takes a table and adds a column. The name comes first, in quotes; the expression after it runs once for each row.
- `[Date]` is the current row's date, and `YEAR ( [Date] )` pulls out its year: 2023 for the first row.
- Press **Shift+Enter** in the formula bar to start a new line; the line breaks only make the formula readable.

**Step 3: month number and month name.** Add two more name-and-expression pairs inside the same `ADDCOLUMNS`, after the Year line (each pair is separated from the next by a comma):

```dax
    "Month No", MONTH ( [Date] ),
    "Month", FORMAT ( [Date], "MMM" ),
    "Year Month", FORMAT ( [Date], "yyyy-MM" ),
```

How it works:

- `MONTH ( [Date] )` gives the month as a number, 1 to 12.
- `FORMAT ( value, "format" )` turns a value into **text** laid out by a format code, like a spreadsheet's number formats. The codes used in this chapter:

| Format code | Shows, for 15 January 2025 |
|---|---|
| `"MMM"` | Jan |
| `"yyyy-MM"` | 2025-01 |
| `"d MMM yyyy"` | 15 Jan 2025 |
| `"0.0%"` (for a number such as 0.983) | 98.3% |

**Step 4: the quarter.** Add:

```dax
    "Quarter", "Q" & QUARTER ( [Date] ),
```

`QUARTER ( [Date] )` returns 1 for January–March up to 4 for October–December, and `&` joins text, so "Q" & 1 becomes `Q1`, as `&` did in Chapter 10's spreadsheet formulas.

**Step 5: the financial year.** Most Indian companies report on a financial year that runs from April to March and is named after the year it ends in: FY2026 runs from 1 April 2025 to 31 March 2026. Work two dates by hand first. 15 March 2025: the month is 3, before April, so it belongs to the year ending in March 2025, **FY2025**. 15 April 2025: the month is 4, so the year ends in March 2026, **FY2026**. As a formula, add the last pair (no comma after it):

```dax
    "Financial Year", "FY" & IF ( MONTH ( [Date] ) >= 4, YEAR ( [Date] ) + 1, YEAR ( [Date] ) )
```

How it works: `IF ( test, if true, if false )` works like the spreadsheet `IF`. From April on, the financial year is the calendar year plus one; before April, it's the calendar year. `"FY" &` puts the letters in front.

The finished table, whose full text is in `companion/ch16/date_table.dax`, starts like this in Table view:

| Date | Year | Month No | Month | Year Month | Quarter | Financial Year |
|---|---|---|---|---|---|---|
| 01/01/2023 | 2023 | 1 | Jan | 2023-01 | Q1 | FY2023 |
| 02/01/2023 | 2023 | 1 | Jan | 2023-01 | Q1 | FY2023 |
| 03/01/2023 | 2023 | 1 | Jan | 2023-01 | Q1 | FY2023 |

(The dates show in your computer's date format.)

> **Watch out: quote the table name.** `Date` is also the name of a DAX function, so write the table as `'Date'` in formulas: `'Date'[Date]` means "the Date column of the Date table". Put a table name in single quotes whenever it has a space or matches a DAX function name, as Date does.

Then:

1. **Mark it as a date table:** select the table → **Table tools → Mark as date table**, pointing at `'Date'[Date]`. Time-intelligence functions need this.
2. **Join it:** in Model view, drag `'Date'[Date]` onto `Sales[order_date]`, and again onto `Targets[target_month]`.
3. **Sort month names properly:** select the `Month` column → **Column tools → Sort by column → Month No**, or every chart will run April, August, December.
4. **Include whole years.** A date table that stops mid-December breaks year-to-date calculations.
5. **Use the financial-year column** if the business reports April–March. Riverstone's targets are calendar months, so this chapter uses calendar years, but the column is there for exercises.

> **Watch out: targets are monthly.** Each target is stored on the first day of its month (`2025-01-01` holds all of January's target). A date-range slicer that starts on 2 January loses January's target entirely. Show `% of Target` by month, quarter, or year, never by a day-level range.

### Hide, rename, and format

The model is the interface everyone else uses, so treat it like one:

- **Hide** raw key columns (`customer_id`, `product_id`, `order_id`, `sales_rep_id`) from report view: right-click → **Hide in report view**. They're for relationships and formulas, not for dragging onto a page.
- **Rename** columns into business language (you did the main ones in Power Query), and hide the number columns that measures will add up: `net_revenue` and `product_cost` become measures in section 16.4, so nobody should drag the raw columns onto a page.
- **Format** measures once, in the model: currency with no decimals for rupees, one decimal for percentages. Then every visual inherits it.
- **Sort** what needs sorting, and set **Data category** for geography columns (City, Region) so map visuals work.

The field names used in the rest of this chapter:

| Table | Fields you'll use |
|---|---|
| Sales | `Sales[order_id]`, `Sales[customer_id]`, `Sales[sales_rep_id]`, `Sales[order_date]`, `Sales[status]`, `Sales[net_revenue]`, `Sales[product_cost]` (all hidden) |
| Customer | `Customer[Customer]`, `Customer[City]`, `Customer[Segment]`, `Customer[Region]` |
| Product | `Product[Product]`, `Product[unit_cost]` |
| Employee | `Employee[Employee]` |
| Date | `'Date'[Date]`, `'Date'[Year]`, `'Date'[Quarter]`, `'Date'[Month]`, `'Date'[Financial Year]` |
| Targets | `Targets[target_month]`, `Targets[target_revenue]` (hidden) |

> **Watch out: don't build a flat table.** New users often load one wide table with customer, product, and date columns repeated on every row, because it looks like a spreadsheet. It works at 200,000 rows and collapses later: filters get slow, totals get wrong when the same customer appears in two rows, and time intelligence has nothing to hang on. Build the star.

---

## 16.4 DAX from zero

**DAX** (Data Analysis Expressions) is the formula language of Power BI, Power Pivot (Chapter 11, section 11.8), and Analysis Services. It looks like Excel formulas and behaves differently in one crucial way: **a DAX formula has no cell**. It runs inside whatever filters the visual applies.

You met measures, `SUMX`, `RELATED`, `CALCULATE`, and `DIVIDE` in Chapter 11, section 11.8, on 330 order lines in Excel. Here the same ideas run on the full dataset, one measure at a time, each checked before the next.

### Measures and calculated columns

| | Calculated column | Measure |
|---|---|---|
| **Computed** | Once per row, at refresh | Once per visual cell, at view time |
| **Stored** | In the model (costs memory) | Not stored |
| **Sees** | The current row | The current filter context |
| **Use for** | Something you slice or group **by** (a band, a flag, a sorted key) | Anything you **aggregate** (revenue, margin, counts, ratios) |

The rule of thumb: **if you'd put it on an axis or in a slicer, it's a column; if you'd put it in the values area, it's a measure.** Beginners write columns for everything, which bloats the model and gives wrong totals (a column of "margin %" per row, averaged, is not the margin).

**"Sees the current row"** has a name: **row context**. A calculated column's formula runs once for each row of its table, and inside it a column name means "this row's value". Try one, to see it. Select the Sales table in Table view, choose **Table tools → New column**, and type:

```dax
Unit Cost = RELATED ( Product[unit_cost] )
```

How it works:

- The formula runs 200,381 times, once per Sales row. Each time, the row context is that one order line.
- `RELATED ( Product[unit_cost] )` follows the relationship from this Sales row to its one Product row and fetches that product's unit cost, as in Chapter 11.

Find the line of order 10001 (click the arrow on `order_id` and filter to 10001): product 108, quantity 10, **Unit Cost 190**, and `product_cost` 1,900, which is 10 × 190. The view's `product_cost` column already holds exactly this multiplication, so delete `Unit Cost` again (right-click → **Delete from model**). It was only a demonstration: a column that repeats a lookup costs memory and adds nothing.

### Somewhere to keep the measures

Before writing any measures, make them a home. **Home → Enter data**, name the table `_Measures`, and click **Load**. Each measure you create below goes in this table (select `_Measures` in the Data pane before **New measure**). Once it holds a measure, hide its empty `Column1`. All measures then sit together at the top of the Data pane, instead of scattered through the tables.

### The base measures, one at a time

Build a test page for them: a **card** visual (it shows one number) and a **slicer** of `'Date'[Year]` with **2025** ticked. After each measure, drop it on the card and compare it with the value given here.

**Net Revenue.** Select `_Measures`, then **Home → New measure**, and type:

```dax
Net Revenue = SUM ( Sales[net_revenue] )
```

How it works:

- `Net Revenue =` is the measure's name, which is how every other formula and visual will refer to it: `[Net Revenue]`.
- `SUM ( Sales[net_revenue] )` adds up the `net_revenue` column of Sales, over whatever rows the filters leave.

In Chapter 11, the Sales table had quantity, price, and discount, so net revenue needed `SUMX` to multiply row by row before adding. Here the `sales_lines` view already did that multiplication for every line in SQL (the "fix it in a view" rule from section 16.2), so a plain `SUM` of one column is enough.

With the Year slicer on 2025 the card shows **₹1,14,66,41,651**. To show it that way, select the measure and, on the **Measure tools** ribbon, set the format to **Currency** with the ₹ symbol and 0 decimal places. Set it once here, and every visual that uses the measure inherits it.

What happens if you change the slicer? Tick 2024 instead: the card shows **₹90,30,15,475**. Clear the slicer: **₹2,66,34,90,235**, all three years. The measure didn't change; the filter did. That's the whole idea of a measure.

**Product Cost** is the same pattern on the cost column:

```dax
Product Cost = SUM ( Sales[product_cost] )
```

2025: **₹83,18,03,000**.

**Gross Margin** and **Gross Margin %** call the measures you already have:

```dax
Gross Margin = [Net Revenue] - [Product Cost]
```

```dax
Gross Margin % = DIVIDE ( [Gross Margin], [Net Revenue] )
```

How it works:

- **Measures reference measures.** `[Net Revenue]` in square brackets with no table name is the measure. `Gross Margin` doesn't repeat the revenue formula; it calls it. When the definition of revenue changes, it changes in one place.
- **`DIVIDE ( numerator, denominator )`** returns blank (or a value you give as a third argument) instead of an error when the denominator is zero or blank. Use it whenever the denominator could be zero or blank, which for a measure is almost always: a filter can always leave no rows.

2025: Gross Margin **₹31,48,38,651**; Gross Margin % **27.5%** (format it as a percentage with one decimal).

**Orders** needs a new function:

```dax
Orders = DISTINCTCOUNT ( Sales[order_id] )
```

`DISTINCTCOUNT ( column )` counts the different values in a column, like SQL's `COUNT(DISTINCT …)` (Chapter 12). 2025: **46,356** orders.

> **Watch out: `COUNTROWS(Sales)` is not orders.** `COUNTROWS ( table )` counts rows, and the fact table is order **lines**: in 2025, 83,444 rows for 46,356 orders. Counting the wrong grain is the most common wrong number in a new model, and it looks plausible.

**Customers** counts the different customers who bought:

```dax
Customers = DISTINCTCOUNT ( Sales[customer_id] )
```

2025: **4,599** customers. (The Customer table has 5,027 records; 428 of them didn't order in 2025, so they have no Sales rows in that filter.)

**Average Order Value** divides two measures:

```dax
Average Order Value = DIVIDE ( [Net Revenue], [Orders] )
```

2025: **₹24,735.56** (format: currency, 2 decimals).

All seven are in `companion/ch16/measures.dax`, ready to paste.

### Check your measures against SQL

A measure you can't verify is a guess. Every number in this chapter has a SQL equivalent you can run on `riverstone_full`. First, all three years:

<!-- db: riverstone_full -->

```sql
SELECT ROUND(SUM(net_revenue)) AS all_years
FROM sales_lines;
```

```
 all_years  
------------
 2663490235
(1 row)
```

`ROUND(…)` with one argument rounds to a whole number, as the card does. Then 2025, one column per card:

```sql
SELECT ROUND(SUM(net_revenue)) AS revenue,
       COUNT(DISTINCT order_id) AS orders,
       COUNT(DISTINCT customer_id) AS customers,
       ROUND(SUM(net_revenue) / COUNT(DISTINCT order_id), 2) AS aov,
       ROUND(100 * (1 - SUM(product_cost) / SUM(net_revenue)), 1) AS gm_pct
FROM sales_lines
WHERE order_date >= '2025-01-01';
```

```
  revenue   | orders | customers |   aov    | gm_pct 
------------+--------+-----------+----------+--------
 1146641651 |  46356 |      4599 | 24735.56 |   27.5
(1 row)
```

How it works:

- `WHERE order_date >= '2025-01-01'` keeps 2025, because the data ends in December 2025. It plays the part of the Year slicer.
- `revenue` matches `Net Revenue`; `orders` and `customers` use `COUNT(DISTINCT …)`, exactly what `DISTINCTCOUNT` does.
- `aov` divides revenue by orders and rounds to 2 decimals, like `Average Order Value`.
- `gm_pct` is 100 × (1 − cost ÷ revenue): the margin as a percentage, the same as `Gross Margin %`.

So in a card filtered to 2025, your measures must read: Net Revenue **₹1,14,66,41,651**, Orders **46,356**, Customers **4,599**, Average Order Value **₹24,735.56**, Gross Margin % **27.5%**. `companion/ch16/expected_measures.md` lists these and the rest; build the card, compare, and only then move on.

### Writing DAX that people can read

- **One measure per idea**, named in business language (`Net Revenue`, not `Sum of amt2`).
- **Lay out long formulas.** Press Shift+Enter in the formula bar to start a new line; the free DAX Formatter website (daxformatter.com) lays out a whole measure for you. Team conventions matter more than which convention.
- **Keep measures in the `_Measures` table**, as above.
- **Write a description** for each measure (in the model view) so the field list explains itself.

---

## 16.5 `CALCULATE` and filter context

Everything hard about DAX is filter context. Everything good about DAX is that you can change it on purpose.

![A cell in a visual carries filters from rows, columns, slicers, and page filters; those filters are applied to the measure, which returns one number. CALCULATE changes the filters before the measure runs](figures/fig16-3-filter-context.svg)

*Figure 16.3 — A measure is evaluated once per cell, under the filters that cell carries. `CALCULATE` is how you change those filters.*

### The idea

A visual cell says "Wholesale, 2025, West region". Those filters reach the model, narrow the tables, and then the measure runs over what's left. Change the cell, and the same measure runs again over a different subset. That's why `[Net Revenue]` in a card is company revenue, and the same measure in a matrix row is that row's revenue: one definition, many answers.

### `CALCULATE`

`CALCULATE ( <expression>, <filter1>, <filter2>, … )` evaluates the expression with the filters modified. Build a **matrix** visual to watch it work: `Customer[Segment]` on Rows, `[Net Revenue]` in Values, and the Year slicer on 2025. It shows Hospitality ₹27,74,76,705 Retail ₹55,64,36,454 Wholesale ₹31,27,28,493 total ₹1,14,66,41,651. Add each measure below to the same matrix.

**A fixed filter.**

```dax
Retail Revenue = CALCULATE ( [Net Revenue], Customer[Segment] = "Retail" )
```

How it works: the first argument is what to calculate, `[Net Revenue]`; the second, `Customer[Segment] = "Retail"`, is the filter to apply first. Predict what the Wholesale row shows before you add it.

| Segment | Net Revenue | Retail Revenue |
|---|---|---|
| Hospitality | ₹27,74,76,705 | ₹55,64,36,454 |
| Retail | ₹55,64,36,454 | ₹55,64,36,454 |
| Wholesale | ₹31,27,28,493 | ₹55,64,36,454 |
| **Total** | **₹1,14,66,41,651** | **₹55,64,36,454** |

Every row shows Retail's revenue. That's rule 1 below: the filter argument **replaced** the row's segment filter. (If your Sales table still had cancelled lines, as Chapter 11's did, `CALCULATE ( [Net Revenue], Sales[status] <> "Cancelled" )` would be the way to leave them out; the `sales_lines` view has already done it.)

**Adding instead of replacing.** Wrap the filter in `KEEPFILTERS`:

```dax
Retail Only = CALCULATE ( [Net Revenue], KEEPFILTERS ( Customer[Segment] = "Retail" ) )
```

`KEEPFILTERS ( filter )` keeps the row's own filter and adds this one on top, so both must be true. The Hospitality and Wholesale rows can't be Retail as well, so they go **blank**; the Retail row and the total show ₹55,64,36,454.

**Removing a filter.**

```dax
All-Customer Revenue = CALCULATE ( [Net Revenue], REMOVEFILTERS ( Customer ) )
```

`REMOVEFILTERS ( Customer )` clears every filter on the Customer table. In the segment matrix, every row shows **₹1,14,66,41,651**: the segment filter was removed, but the year filter stayed, because it's on the Date table. The measure is "revenue for all customers", not "company revenue for all time".

**A share, using that denominator.**

```dax
Share of Segment =
DIVIDE (
    [Net Revenue],
    CALCULATE ( [Net Revenue], REMOVEFILTERS ( Customer[Customer] ) )
)
```

How it works: `REMOVEFILTERS ( Customer[Customer] )` clears only the filter on the customer-name column, and leaves the Segment filter alone. With Segment and then Customer on the matrix rows, the denominator is the whole segment's revenue, and the measure is that customer's share of its segment. Expand Wholesale: Riverstone's biggest customer of 2025, Galaxy Logistics Patna, has ₹10,73,806.50, which is **0.34%** of Wholesale's ₹31,27,28,493.

Three rules explain most surprises:

1. **A filter argument replaces the existing filter on that column.** In the Wholesale row, `Retail Revenue` shows Retail's number, not blank. Wrap the filter in `KEEPFILTERS()` to add to the existing filter instead.
2. **`REMOVEFILTERS` (or `ALL`, its older name inside `CALCULATE`) clears filters**, which is how you compute a denominator for a share. `ALLSELECTED` clears only the filters that come from inside the visual (its rows and columns), and keeps the ones the reader chose in slicers. Use it when a percentage should add up to 100% of what the user selected. For example, put a slicer of `Product[Product]` on the page, tick only Storage Box 25L and Storage Box 10L, and add a table of Product with this measure:

   ```dax
   Share of Selection = DIVIDE ( [Net Revenue], CALCULATE ( [Net Revenue], ALLSELECTED ( Product ) ) )
   ```

   In 2025 it shows Storage Box 25L **54.1%** and Storage Box 10L **45.9%**, adding to 100% of the two ticked products. `Product Share %` (below), which uses `REMOVEFILTERS`, shows 20.2% and 17.1% for the same rows: their shares of all eight products.
3. **`CALCULATE` also turns a row context into a filter context** ("context transition"). This matters inside **iterators**, functions that walk a table row by row, such as `SUMX` (Chapter 11) and its cousin `AVERAGEX`:

   ```dax
   Avg Customer Revenue = AVERAGEX ( Customer, [Net Revenue] )
   ```

   `AVERAGEX ( table, expression )` computes the expression once for each row of the table and averages the results. Each time, the row context is one customer. A measure used inside an iterator is wrapped in a hidden `CALCULATE`, which turns "this customer's row" into a filter on Customer, so `[Net Revenue]` returns that one customer's revenue. Customers who bought nothing in 2025 return blank, and `AVERAGEX` skips blanks, so in 2025 the result is the average over the 4,599 customers who ordered: **₹2,49,324.13**. Without context transition, every row would return the whole company's revenue, and the "average" would be ₹1,14,66,41,651.

### Filter functions this chapter uses

| Function | Does |
|---|---|
| `REMOVEFILTERS` / `ALL` | Clears filters from a table or columns |
| `KEEPFILTERS` | Adds a filter instead of replacing |
| `ALLSELECTED` | Clears the visual's own filters but respects slicers |
| `VALUES ( column )` | The values of a column in the current filter context, as a one-column table (section 16.10) |
| `SELECTEDVALUE ( column, default )` | The single value of a column in context, or the default when there are none or several (section 16.8) |
| `HASONEVALUE ( column )` | True when exactly one value of a column is in context: useful for showing a message instead of a meaningless total |

> **Reference: two more you'll meet.** `FILTER ( table, condition )` returns the rows of a table that pass a test, for conditions a simple filter argument can't express, such as a measure: `FILTER ( Customer, [Net Revenue] > 1000000 )`. `RANKX ( table, expression )` ranks each row by an expression, usually over `ALL ( Customer )`. Exercise 23 uses `FILTER`; this chapter doesn't need `RANKX`.

> **You've done this in SQL.** Ranking, running totals, and comparisons with an earlier period are what SQL window functions did in Chapter 13: `RANK()` and `DENSE_RANK()` in section 13.4, running totals and `LAG` for growth in section 13.6. `RANKX`, `TOTALYTD`, and `SAMEPERIODLASTYEAR` (section 16.6) are the DAX versions, with one difference: in DAX they respond to whatever the reader filters.

A worked example: the share each product takes of a filtered selection.

```dax
Product Share % =
VAR ThisProduct = [Net Revenue]
VAR AllProducts = CALCULATE ( [Net Revenue], REMOVEFILTERS ( Product ) )
RETURN DIVIDE ( ThisProduct, AllProducts )
```

In 2025, that gives Storage Box 25L **20.2%**, Food Container Set **18.7%**, Storage Box 10L **17.1%**, and Industrial Crate **13.3%**, which the SQL in section 16.8 confirms.

**`VAR` … `RETURN`** stores a value once, makes the code readable, and avoids recomputing. `VAR ThisProduct = [Net Revenue]` stores this row's revenue; `VAR AllProducts` stores the revenue with the Product filter removed; `RETURN` gives the result. Use variables freely; they're evaluated where they're declared, which is itself a useful property when filter context changes later in the formula.

> **Watch out: totals aren't the sum of the rows.** A measure is evaluated at the total row under the total row's filters, not by adding the visible rows. For ratios that's correct behavior (the total margin % is not the sum of the rows' margin %), and for some patterns it looks wrong (a "rank" total, a per-row `IF` that doesn't apply at the total). When a total looks odd, ask what filters the total row has, and use `HASONEVALUE` to blank it out when the total is meaningless.

---

## 16.6 Time intelligence

Business questions are mostly comparisons over time: how are we doing this year so far, against last year, against plan. DAX has functions for this, and they all need the marked date table from section 16.3.

Build a matrix to watch them: `'Date'[Month]` on Rows, the Year slicer on 2025, and `[Net Revenue]` in Values. Then add each measure below as a new column. The table after the measures shows what January to June must read.

**Year to date.**

```dax
Revenue YTD = TOTALYTD ( [Net Revenue], 'Date'[Date] )
```

`TOTALYTD ( measure, date column )` adds the measure from 1 January of the year up to the last date in the cell, as in Chapter 11. By June it reaches ₹49,92,03,925.

**The same period last year.**

```dax
Revenue LY = CALCULATE ( [Net Revenue], SAMEPERIODLASTYEAR ( 'Date'[Date] ) )
```

`SAMEPERIODLASTYEAR ( date column )` takes the dates in the cell and moves them back one year; `CALCULATE` uses them as the date filter. In the January 2025 row it gives January 2024's revenue.

**Year to date, last year.**

```dax
Revenue YTD LY = CALCULATE ( [Revenue YTD], SAMEPERIODLASTYEAR ( 'Date'[Date] ) )
```

The same shift, applied to a measure that is itself a year-to-date. By June: ₹37,98,44,027.

**Growth.**

```dax
YoY Growth % = DIVIDE ( [Net Revenue] - [Revenue LY], [Revenue LY] )
```

This year minus last year, divided by last year; format it as a percentage with one decimal.

**A rolling three months.**

```dax
Revenue 3M Rolling =
CALCULATE ( [Net Revenue], DATESINPERIOD ( 'Date'[Date], MAX ( 'Date'[Date] ), -3, MONTH ) )
```

How it works: `DATESINPERIOD` returns a run of dates, and has four arguments.

- `'Date'[Date]`: the date column to take the dates from.
- `MAX ( 'Date'[Date] )`: the end date, the last date in the cell (31 March in the March row).
- `-3`: how many units to go; the minus sign means backwards.
- `MONTH`: the unit. So the March row covers January to March.

January's rolling three months reach back into November and December 2024, which is why they're bigger than January alone.

With Year = 2025, the matrix must read:

| Month | Net Revenue | Revenue YTD | Revenue LY | Revenue YTD LY | YoY Growth % | Revenue 3M Rolling |
|---|---|---|---|---|---|---|
| Jan | ₹8,51,95,521 | ₹8,51,95,521 | ₹6,40,63,515 | ₹6,40,63,515 | 33.0% | ₹28,59,14,637 |
| Feb | ₹7,85,82,579 | ₹16,37,78,100 | ₹5,86,32,364 | ₹12,26,95,879 | 34.0% | ₹23,66,00,651 |
| Mar | ₹10,10,09,066 | ₹26,47,87,166 | ₹7,81,93,384 | ₹20,08,89,263 | 29.2% | ₹26,47,87,166 |
| Apr | ₹9,51,94,709 | ₹35,99,81,875 | ₹7,25,34,870 | ₹27,34,24,133 | 31.2% | ₹27,47,86,355 |
| May | ₹8,72,49,568 | ₹44,72,31,443 | ₹6,68,88,391 | ₹34,03,12,524 | 30.4% | ₹28,34,53,343 |
| Jun | ₹5,19,72,483 | ₹49,92,03,925 | ₹3,95,31,504 | ₹37,98,44,027 | 31.5% | ₹23,44,16,760 |

**Against plan.** Targets live in their own fact table, joined to Date:

```dax
Target = SUM ( Targets[target_revenue] )
```

```dax
% of Target = DIVIDE ( [Net Revenue], [Target] )
```

```dax
Gap to Target = [Net Revenue] - [Target]
```

For the year 2025 (a card, or the matrix total): Target **₹1,16,69,50,000**, % of Target **98.3%**, Gap to Target **−₹2,03,08,349**. Riverstone finished the year just short of plan.

> **Watch out: blank isn't zero.** `Revenue LY` for any month of 2023 is blank, because there's no 2022 data. `YoY Growth %` already returns blank there, because `DIVIDE` returns blank when the denominator is blank. A plain subtraction doesn't: `[Net Revenue] - [Revenue LY]` would show all of 2023's revenue as "growth". Where you need one, test first:
>
> ```dax
> YoY Change = IF ( NOT ISBLANK ( [Revenue LY] ), [Net Revenue] - [Revenue LY] )
> ```
>
> `ISBLANK ( value )` is true when the value is blank, `NOT` reverses it, and an `IF` with no third argument returns blank when the test fails.

Check them against SQL. Year to date at the end of June 2025, and the same period last year:

```sql
SELECT ROUND(SUM(net_revenue) FILTER (WHERE order_date BETWEEN '2025-01-01' AND '2025-06-30')) AS ytd_jun_2025,
       ROUND(SUM(net_revenue) FILTER (WHERE order_date BETWEEN '2024-01-01' AND '2024-06-30')) AS ytd_jun_2024,
       ROUND(100.0*SUM(net_revenue) FILTER (WHERE order_date BETWEEN '2025-01-01' AND '2025-06-30')/SUM(net_revenue) FILTER (WHERE order_date BETWEEN '2024-01-01' AND '2024-06-30') - 100, 1) AS yoy_pct
FROM sales_lines;
```

```
 ytd_jun_2025 | ytd_jun_2024 | yoy_pct 
--------------+--------------+---------
    499203925 |    379844027 |    31.4
(1 row)
```

How it works: `FILTER (WHERE …)` after an aggregate (Chapter 13) adds up only the rows that pass its test, so one query can hold both periods side by side; `yoy_pct` divides one by the other, times 100, minus 100. The first two match `Revenue YTD` and `Revenue YTD LY` in the June row.

And by quarter, so you can check a matrix of `Net Revenue`, `Revenue LY`, and `YoY Growth %` with `'Date'[Quarter]` on rows:

```sql
SELECT 'Q' || EXTRACT(QUARTER FROM order_date) AS quarter,
       ROUND(SUM(net_revenue) FILTER (WHERE EXTRACT(YEAR FROM order_date)=2025)) AS rev_2025,
       ROUND(SUM(net_revenue) FILTER (WHERE EXTRACT(YEAR FROM order_date)=2024)) AS rev_2024,
       ROUND(100.0*SUM(net_revenue) FILTER (WHERE EXTRACT(YEAR FROM order_date)=2025)/SUM(net_revenue) FILTER (WHERE EXTRACT(YEAR FROM order_date)=2024)-100,1) AS yoy_pct
FROM sales_lines WHERE order_date >= '2024-01-01' GROUP BY quarter ORDER BY quarter;
```

```
 quarter | rev_2025  | rev_2024  | yoy_pct 
---------+-----------+-----------+---------
 Q1      | 264787166 | 200889263 |    31.8
 Q2      | 234416760 | 178954764 |    31.0
 Q3      | 223564918 | 175230767 |    27.6
 Q4      | 423872808 | 347940682 |    21.8
(4 rows)
```

How it works:

- `EXTRACT(QUARTER FROM order_date)` gives the quarter as a number, 1 to 4, and `||` joins text (Chapter 13), so `'Q' || 1` gives `Q1`, the same label as the date table's `Quarter` column.
- `EXTRACT(YEAR FROM order_date)=2025` inside each `FILTER` sends each line to its year's column.
- `GROUP BY quarter` groups by the column named `quarter` in the `SELECT`; PostgreSQL lets you group by an output name like this.

Growth slowed through the year, from 31.8% in Q1 to 21.8% in Q4, which is the honest version of the story Chapter 15's management pack got wrong.

Notes that save hours:

- **Time intelligence needs a marked date table with complete years.** If `Revenue LY` is blank everywhere, that's the first thing to check.
- **`SAMEPERIODLASTYEAR` shifts whatever dates are in context**, so it works for a month, a quarter, or a custom selection. `DATEADD` is the flexible version: `DATEADD ( 'Date'[Date], -1, YEAR )` shifts by one year, and `-1, MONTH` by one month.
- **For a 4-4-5 or financial-year calendar**, the built-in functions won't match the business calendar; build the comparison with your own date columns (`Financial Year`, `Period`) and `CALCULATE` (Exercise 23).

---

## 16.7 Designing the report page

Chapter 15's principles apply unchanged: start from the question, sort bars, label directly, use one highlight color, write titles that state findings, and never truncate a bar axis. What's new is that the reader can now **interact**, so the design has to guide that too.

![A report page wireframe: a dark header with the title "Riverstone sales — 2025" and slicers, a row of four KPI cards, a revenue-and-target line chart, a sorted region bar chart including a City missing bar, a product bar chart, and a panel listing drill-through, tooltip, and bookmark actions](figures/fig16-4-report-page.svg)

*Figure 16.4 — Riverstone's monthly pack as one page: four cards answer "how are we doing?", the visuals below answer "why?", and everything else lives on drill-through pages.*

### Layout

- **Follow the reading order:** most important at the top left, supporting detail below and to the right. A reader who stops after three seconds should still have the headline.
- **Use a grid.** Align visuals to the same edges and give them the same padding (**Format → General → Properties** for exact position and size). Misalignment reads as carelessness.
- **One page, one question.** "How did we do this month?" is a page. "Which customers are slipping?" is another page, reached by drill-through.
- **Keep cards to four or five.** Each card needs a comparison, or it's a number without meaning: revenue with % of target, margin with change in points.
- **Leave white space.** A page with twelve visuals is a wall; a page with six is a report.

### The visuals

Power BI's standard visuals map directly onto Chapter 15's chart types: **column/bar**, **line**, **combo**, **scatter**, **map**, **matrix** (a pivot table), **card** and **KPI**, **gauge** (avoid: it uses angle and area to show one number), **pie** and **donut** (rarely), **treemap**, **waterfall**, **funnel**, **ribbon**, **decomposition tree**, and **key influencers**.

Three that earn their place in a sales report:

- **Matrix** for the numbers people want to read exactly: region by month, with conditional formatting as a heatmap (Chapter 15, section 15.8).
- **Waterfall** for "why did revenue change?" (Chapter 15, section 15.7): set the breakdown to Segment or Product.
- **Decomposition tree** for exploring a number down its dimensions, with the **AI split** option that suggests the dimension with the biggest difference. Useful in a meeting; not a substitute for a designed page.

**Custom visuals** from AppSource fill gaps (small multiples, better bullet charts). Before using one in a shared report, check who maintains it, whether it's certified by Microsoft, and whether it sends data anywhere.

### Interaction

- **Slicers** filter a page. Keep two or three (Year, Region, Segment), and set **Edit interactions** so that a slicer or a visual filters the visuals it should. A common design: a chart filters its neighbours (**Filter**), but cards stay on the whole selection (**None**).
- **The Filters pane** holds filters at three levels: visual, page, and all pages. Use "all pages" for a rule that never changes, such as excluding cancelled orders if your fact table hasn't already (Riverstone's has).
- **Drill-down** (the arrows on a visual) moves through a hierarchy: Year → Quarter → Month, or Region → City.
- **Drill-through** sends the reader to a detail page with the clicked context: right-click a region bar → **Drill through → Customer detail**, and that page opens filtered to the region.
- **Tooltips** can be a whole mini-page (**Page information → Allow use as tooltip**): hovering a bar shows a small trend chart for that bar's category.
- **Bookmarks** save a state (filters, which visuals are visible) and can be attached to buttons: one button for "revenue view", another for "margin view", on the same page.
- **Buttons, selection pane, and the sync-slicers pane** are how a page becomes a small application. Use them sparingly; every hidden state is something a reader can get stuck in.

### Themes and formatting

Set the **View → Themes → Customize current theme** once: colors (Chapter 15's palette, checked for color vision deficiency), fonts, and default title formatting. Export it as a JSON theme file and reuse it in every Riverstone report so charts look the same everywhere. Individual visual formatting overrides the theme, which is exactly how inconsistency creeps in; prefer changing the theme.

### Accessibility, mobile, and performance of the page

- **Alt text** on each visual (**Format → General → Alt text**), stating what it shows and its finding, as in Chapter 15.
- **Tab order** (**Selection pane → Tab order**) so keyboard and screen-reader users move through the page sensibly.
- **Mobile layout** (**View → Mobile layout**) rearranges visuals into a single column for phones: branch managers will open it on a phone.
- **Fewer visuals is faster.** Each visual is at least one query; a page with twenty visuals and five slicers can take seconds to render.

---

## 16.8 A worked example: Riverstone's monthly pack

Here's the whole build, in the order you'd actually do it. Every number below is checkable with SQL, and `companion/ch16/expected_measures.md` has the full list.

**1. Load.** Connect to `riverstone_full` and load `sales_lines` (as Sales), `customers`, `products`, `employees`, and `sales_targets`, as in section 16.2. In Power Query, rename the queries and columns, and add `Region` to Customer from `city_region.csv`, with "City missing" for customers who have no city.

**2. Model.** Build the star from section 16.3, add the DAX date table, mark it, create relationships, hide keys, rename fields.

**3. Measures.** The base set from section 16.4, then the time intelligence from section 16.6, in the `_Measures` table.

**4. Page 1, "Overview".** Four cards (Net Revenue, % of Target, Gross Margin %, Orders), a line chart of Net Revenue and Target by month, a sorted bar of revenue by region, a bar of revenue by product, and slicers for Year, Region, and Segment.

With the Year slicer on 2025, the cards must read:

| Card | Value |
|---|---|
| Net Revenue | ₹1,14,66,41,651 |
| % of Target | 98.3% |
| Gross Margin % | 27.5% |
| Orders | 46,356 |
| Average Order Value | ₹24,735.56 |
| Customers | 4,599 |

**5. Check the region bar** against SQL. The database has no region column, so the query types the city-to-region list from `city_region.csv` into a `VALUES` list (Chapter 14, section 14.3):

```sql
SELECT COALESCE(r.region, 'City missing') AS region, ROUND(SUM(s.net_revenue)) AS rev_2025, COUNT(DISTINCT s.customer_id) AS customers
FROM sales_lines s JOIN customers c ON c.customer_id=s.customer_id
LEFT JOIN (VALUES
 ('Mumbai','West'),('Pune','West'),('Ahmedabad','West'),('Surat','West'),('Nashik','West'),('Nagpur','West'),('Indore','West'),('Goa','West'),('Vadodara','West'),('Rajkot','West'),('Thane','West'),('Aurangabad','West'),
 ('Bengaluru','South'),('Chennai','South'),('Hyderabad','South'),('Kochi','South'),('Coimbatore','South'),('Mysuru','South'),('Visakhapatnam','South'),('Madurai','South'),('Mangaluru','South'),('Thiruvananthapuram','South'),
 ('Delhi','North'),('Jaipur','North'),('Lucknow','North'),('Chandigarh','North'),('Udaipur','North'),('Kanpur','North'),('Ludhiana','North'),('Dehradun','North'),('Agra','North'),('Noida','North'),('Gurugram','North'),
 ('Kolkata','East'),('Bhubaneswar','East'),('Patna','East'),('Guwahati','East'),('Ranchi','East'),('Raipur','East')) AS r(city,region) ON r.city=c.city
WHERE s.order_date >= '2025-01-01' GROUP BY r.region ORDER BY rev_2025 DESC;
```

```
    region    | rev_2025  | customers 
--------------+-----------+-----------
 West         | 383840549 |      1506
 South        | 318624642 |      1289
 North        | 279250231 |      1127
 East         | 142256284 |       586
 City missing |  22669946 |        91
(5 rows)
```

How it works:

- `(VALUES ('Mumbai','West'), …) AS r(city, region)` is a small table typed into the query: 39 rows, the same as `city_region.csv`, with its columns named `city` and `region`.
- `LEFT JOIN … ON r.city=c.city` is the SQL version of the Power Query merge: every customer keeps its row, and those with no city get a `NULL` region.
- `COALESCE(r.region, 'City missing')` replaces that `NULL` with the label, as the **Replace Values** step did (Chapter 14).
- `COUNT(DISTINCT s.customer_id)` counts the customers who ordered in 2025 in each region.

The last row is ₹2,26,69,946 from 91 of the 100 customers with no city (Chapter 14): the other 9 didn't order in 2025. Because Power Query labelled them, Power BI shows a "City missing" bar instead of a blank category. Chapter 15's rule applies: show it in gray rather than dropping it, and the five bars add up to the Net Revenue card.

**6. Check the product bar:**

```sql
SELECT p.product_name, ROUND(SUM(s.net_revenue)) AS rev_2025, ROUND(100*SUM(s.net_revenue)/SUM(SUM(s.net_revenue)) OVER (),1) AS share
FROM sales_lines s JOIN products p ON p.product_id=s.product_id WHERE s.order_date >= '2025-01-01'
GROUP BY p.product_name ORDER BY rev_2025 DESC LIMIT 4;
```

```
    product_name    | rev_2025  | share 
--------------------+-----------+-------
 Storage Box 25L    | 231104138 |  20.2
 Food Container Set | 214380655 |  18.7
 Storage Box 10L    | 196381989 |  17.1
 Industrial Crate   | 152683090 |  13.3
(4 rows)
```

How it works: `SUM(SUM(s.net_revenue)) OVER ()` is a window over the grouped rows (Chapter 13): the inner `SUM` is each product's revenue, and the outer `SUM … OVER ()` adds those across all eight products, so `share` is each product's percentage of the total, as `Product Share %` computes. `LIMIT 4` keeps the top four after sorting.

**7. Page 2, "Customer detail"**, set as a drill-through target on Region: a matrix of customers with Net Revenue, Orders, YoY Growth %, and last order date; a line of that customer's monthly revenue; and the drill-through filter card showing which region the reader came from.

**8. Titles.** Every visual gets a title that states the finding where the finding is stable (`"October is the peak in every region"`), or a plain descriptive title where the reader's slicers change the story. Dynamic titles use a measure that builds a sentence:

```dax
Overview Title =
"Riverstone sales — " & SELECTEDVALUE ( 'Date'[Year], "all years" )
    & " — ₹" & FORMAT ( [Net Revenue] / 10000000, "#,##0.0" ) & " cr at "
    & FORMAT ( [% of Target], "0.0%" ) & " of target"
```

How it works:

- `SELECTEDVALUE ( 'Date'[Year], "all years" )` returns the year when exactly one is selected, and the text "all years" when none or several are.
- `&` joins the pieces of text into one sentence.
- `[Net Revenue] / 10000000` turns rupees into crore (1 crore = ₹1,00,00,000 ten million), and the format code `"#,##0.0"` shows it with one decimal: 114.7.
- `FORMAT ( [% of Target], "0.0%" )` shows 0.983 as 98.3%.

With Year = 2025 the title reads **"Riverstone sales — 2025 — ₹114.7 cr at 98.3% of target"**. Clear the slicer and it reads **"Riverstone sales — all years — ₹266.3 cr at 99.2% of target"**.

Set the visual's title to that measure with **Format → Title → fx → Field value**.

> **Watch out: commas in a format code divide by a thousand.** In a `FORMAT` code, a comma just before the decimal point scales the number down by 1,000 per comma: `"#,##0,,.0"` shows 1,146,641,651 as 1,146.6 (millions). Commas can reach thousands, millions, and billions, but never crore, which is 10 million: that's why the title divides by 10000000 instead.

**9. Save, publish, refresh, secure** (sections 16.9 and 16.10).

---

## 16.9 Publishing, refresh, and sharing

This section needs the Power BI Service, and so a work or school account (section 16.0). Without one, read it as a walkthrough: it's what you'll do on your first BI job.

![Five steps: build in Desktop, publish to a workspace, set credentials and a refresh schedule with a gateway for on-premises data, secure with roles, and deliver through an app, plus a panel listing the four things that break most often](figures/fig16-5-publish-refresh.svg)

*Figure 16.5 — What happens after the report looks right, and what usually goes wrong.*

**Publish.** **Home → Publish**, sign in with your work or school account, and choose a workspace. A workspace is a folder with permissions; use one per team or subject area, never "My workspace" for anything shared. Publishing uploads the semantic model **and** the report, and replaces what's there.

**Credentials and refresh.** In the Service, open the semantic model's settings:

- **Data source credentials:** the account the Service uses to read the source. Personal credentials expire when people leave; ask for a service account.
- **Scheduled refresh:** up to **8 refreshes a day** on Pro, **48** on PPU or Fabric capacity. Set the time to after the source system's nightly load, not at 9:00 when everyone opens the report.
- **Failure notifications:** send them to a team address, not one person.
- **Incremental refresh** (Pro included, larger models on PPU/Fabric): refresh only recent partitions instead of the whole table. Riverstone's 200,381 rows don't need it; a 200-million-row fact table does.

**Gateway.** A database on the company network is invisible to the cloud. The **on-premises data gateway** (standard mode, installed on a server that stays on) bridges it. Personal mode exists for one user's own refreshes and shouldn't run a company report.

**Sharing.** Options, from most to least manageable:

1. **An app**: publish the workspace as an app with selected reports and an audience. Readers get a clean, navigable package. This is the default for anything with more than a few readers.
2. **Workspace roles** (Admin, Member, Contributor, Viewer) for the people who build and review.
3. **Share a report link** with specific people, for small, temporary cases.
4. **Embed** in Teams or SharePoint for where people already work.
5. **Subscriptions**: email a PDF or image on a schedule, for readers who won't open a link.

Everyone who opens the content needs a licence: Pro (or PPU, or a free licence if the workspace sits on F64 or larger capacity). Sort this out before you promise a report to 200 people.

**Version control and deployment.** Save the `.pbix` in OneDrive, SharePoint, or Git (Chapter 26): Power BI Desktop files are binary, so Git stores them without useful diffs, while the newer **`.pbip` project format** saves the model and report as text files that diff properly. PPU and Fabric add **deployment pipelines** for development → test → production. At minimum, keep a copy of the last published file and a changelog.

**Usage metrics** (**workspace → report → Usage metrics**) show who opens the report and how often. A report nobody opens is a signal, not a failure: ask them what they needed instead.

---

## 16.10 Row-level security

**Row-level security (RLS)** filters the data by who is looking. One report, one model, and the North manager sees North.

![A dynamic role on the Customer table keeps rows whose Region is in the signed-in user's regions from a small UserRegion table, and an All regions role for leaders; a table shows what each person sees: Anita Rao all ₹114.7 crore, Pooja Desai West and East ₹52.6 crore, Arjun Nair South ₹31.9 crore, Sandeep Gill North ₹27.9 crore](figures/fig16-6-row-level-security.svg)

*Figure 16.6 — Security belongs in the model. The rule filters a dimension, and the filter flows to the facts.*

A role's rule is a DAX condition written on one table. Power BI tests it on every row of that table, keeps the rows where it's true, and the relationships carry that filter to the facts.

### Static roles

In Desktop: **Modeling → Manage roles → New**, name the role `South`, choose the Customer table, and write the rule:

```dax
[Region] = "South"
```

The rule runs once for each Customer row, and `[Region]` is that row's region, so only South's customers survive.

Then **Modeling → View as**, tick **South**, and click OK. The page redraws as a South reader would see it: with the Year slicer on 2025, the Net Revenue card shows **₹31,86,24,642**, Customers shows **1,289**, and the region bar has a single South bar. Click **Stop viewing** to return.

In the Service, open the semantic model → **Security**, and add people or groups to each role.

A user with no role sees everything **if** they can edit the workspace (Admin, Member, or Contributor), and **nothing** if they're a Viewer or an app reader: once a model has roles, a reader outside every role gets an empty report. So give leaders who should see everything a role of their own. Create a role `All regions` on Customer with the rule:

```dax
TRUE ()
```

`TRUE ()` is true for every row, so the role keeps all customers, including the ones with "City missing". Map Anita Rao, the Sales Head, to it.

Static roles don't scale: 4 regions is fine, 40 sales reps is not.

### Dynamic roles

Build a small mapping table, `companion/ch16/user_region.csv`, with one row per person and region. Pooja Desai has two rows, West and East, because she covers East until a fourth regional manager is hired. Load it with **Get data → Text/CSV**, name it `UserRegion`, don't relate it to anything, and hide it from report view (right-click → **Hide in report view**): it's for the rule, not for readers.

Then one role, `Region manager`, on the Customer table:

```dax
Customer[Region]
    IN CALCULATETABLE (
        VALUES ( UserRegion[region] ),
        UserRegion[email] = USERPRINCIPALNAME ()
    )
```

How it works, from the inside out:

- `USERPRINCIPALNAME ()` returns the signed-in user's email in the Service, such as `pooja.desai@riverstone.example`.
- `CALCULATETABLE ( table, filter )` is `CALCULATE` for tables: it returns the table under the filter. Here the filter keeps the UserRegion rows with that email.
- `VALUES ( UserRegion[region] )` lists the regions in those rows: for Pooja, the two-row table {West, East}; for Arjun Nair, {South}.
- `Customer[Region] IN …` is true when this customer's region is one of them.

Add a row to the mapping table and the new manager is covered; no model change, no republish.

In Desktop, `USERPRINCIPALNAME()` returns your own account, so test with **View as**: tick **Other user**, type `pooja.desai@riverstone.example`, and tick the **Region manager** role.

Expected results on Riverstone's 2025 data, which is how you test it:

| Who | Role | Regions | Net Revenue 2025 | Customers |
|---|---|---|---|---|
| Anita Rao (Sales Head) | All regions | all | ₹1,14,66,41,651 | 4,599 |
| Pooja Desai (RSM West, also covers East) | Region manager | West, East | ₹52,60,96,833 | 2,092 |
| Arjun Nair (RSM South) | Region manager | South | ₹31,86,24,642 | 1,289 |
| Sandeep Gill (RSM North) | Region manager | North | ₹27,92,50,231 | 1,127 |

The four regions add to ₹1,12,39,71,706 which is ₹2,26,69,946 short of the company total: the customers with no city, and so no region. No region manager sees them; only the All regions role does. Decide deliberately who should see them, and say so on the page.

### Rules that keep RLS honest

- **Filter dimensions, not facts,** and let the relationship do the work. A rule on a 200,381-row fact table is slower and easier to get wrong.
- **Test every role**, in Desktop with **View as** and in the Service with **Test as role**, and check a total you know.
- **RLS hides rows, not columns.** Object-level security (column and table level) is separate, and is set outside Desktop's main UI (Tabular Editor).
- **RLS doesn't apply to workspace admins, members, and contributors**: people who can edit the model can see all of it. Viewers, and app users, get the filtered view.
- **Exported data obeys RLS**, and so do subscriptions, which are generated per user.
- **Never build "security" by making a page per region** with visual filters. Anyone can remove a filter, and every new region means a new page.

---

## 16.11 Performance and the mistakes that make numbers wrong

### Keep the model small and simple

- **Import only what you need** (section 16.2): fewer columns, fewer rows, fewer distinct values. High-cardinality columns (timestamps to the second, GUIDs, free text) cost the most memory.
- **Star schema, not snowflake.** One level of dimension is faster and simpler than dimensions joined to other dimensions.
- **Prefer measures to calculated columns**, and calculated columns to Power Query columns only when they must respond to the model; do heavy transformation upstream in SQL.
- **Avoid bidirectional relationships** unless a specific pattern needs them; they can create ambiguity and slow filtering.
- **Turn off Auto date/time** (**File → Options → Data Load → Time intelligence**), which silently creates a hidden date table per date column. You have a real one.
- **Watch the visuals per page.** Each visual is a query. A page of twenty visuals, several with complex measures, is where "the report is slow" comes from.
- **Measure it:** **View → Performance analyzer** in Desktop records how long each visual takes and shows the DAX it ran. DAX Studio (free) goes further, with server timings and a model-size analyzer (VertiPaq Analyzer).

### The mistakes that produce wrong numbers

| Mistake | Symptom | Fix |
|---|---|---|
| Counting fact rows as events | "Orders" shows 83,444 for 2025 instead of 46,356 | `DISTINCTCOUNT` on the order key |
| Averaging a percentage column | A margin that no month has | Compute the ratio with `DIVIDE` at the level shown |
| Cancelled orders left in | Revenue too high by ₹4,92,41,854 in 2025 | Filter in the source view or one page-level filter |
| No date table, or not marked | Time intelligence blank or wrong | A real date table, marked, covering whole years |
| Relationship on the wrong column | Totals repeat or collapse | Check both sides' grain in Model view |
| Bidirectional filters everywhere | Numbers change when unrelated slicers move | One-way filters from dimensions |
| Blank dimension rows | A category called "(Blank)" | Rename in Power Query ("City missing"), never hide silently |
| Measures in the fact table's context by accident | Totals don't match rows | Understand context transition; test with `HASONEVALUE` |
| Different definitions in two reports | Two "revenue" numbers in one meeting | One shared semantic model |
| Stale data presented as current | Decisions on last week's numbers | Show the data date and the refresh time on every page |

The last one deserves a measure on every report. It needs two facts: the latest date in the data, and the moment of the last refresh.

The refresh moment comes from a one-row **calculated table**. Calculated tables are computed when the model refreshes, so the time they capture is the refresh time. **Modeling → New table**:

```dax
Refresh = ROW ( "Refreshed IST", UTCNOW () + TIME ( 5, 30, 0 ) )
```

How it works:

- `ROW ( "name", expression )` builds a table with one row and one column, here called `Refreshed IST`.
- `UTCNOW ()` is the current date and time in UTC, read when the table is computed, at refresh.
- `TIME ( 5, 30, 0 )` is 5 hours 30 minutes. Adding it converts UTC to India Standard Time, as in Chapter 14, section 14.7. Starting from UTC gives the same answer on your laptop and in the Service.

Then the measure:

```dax
Last Refreshed =
"Data to " & FORMAT ( CALCULATE ( MAX ( Sales[order_date] ), REMOVEFILTERS () ), "d MMM yyyy" )
    & " · refreshed " & FORMAT ( MAX ( Refresh[Refreshed IST] ), "d MMM yyyy HH:mm" ) & " IST"
```

How it works:

- `MAX ( Sales[order_date] )` is the latest order date. `CALCULATE ( …, REMOVEFILTERS () )` with no arguments to `REMOVEFILTERS` clears every filter, so a Year slicer on 2024 doesn't make the label say the data stops in 2024.
- `MAX ( Refresh[Refreshed IST] )` reads the one value in the Refresh table; `"HH:mm"` shows hours and minutes on a 24-hour clock.

On Riverstone's data the card reads, for example, **"Data to 28 Dec 2025 · refreshed 28 Sep 2026 07:05 IST"**: the first date is the last order in the data (check it with `SELECT MAX(order_date) FROM sales_lines;`), the second is whenever you last refreshed.

Why not `NOW ()` in the measure? A measure is computed when the visual is drawn, so `NOW ()` would show the moment the reader opened the page, not when the data was refreshed: exactly the "stale data presented as current" mistake the measure exists to prevent. It would also give your computer's local time in Desktop and UTC in the Service.

---

## 16.12 The same ideas in other tools

Every BI tool asks the same four things: connect, model, define measures, design. What changes is where the work happens.

| | Power BI | Tableau | Looker Studio | Metabase / Superset |
|---|---|---|---|---|
| **Modelling** | Star schema in the model, relationships | Data source with relationships or joins | Blends and joins; heavier work belongs upstream | Mostly upstream, in SQL |
| **Measure language** | DAX | Calculated fields and LOD expressions (`{FIXED …}`) | Calculated fields; LookML in Looker (the enterprise product) | SQL, plus simple metrics |
| **Strength** | Modelling, DAX, Microsoft integration, price | Exploratory visual analysis, chart craft | Free, fast for Google-based data | Open source, SQL-first, cheap to self-host |
| **Cost** | Free Desktop; per-user or capacity to share | Per-user, higher | Free tier, Pro for governance | Free open source, paid cloud |
| **Runs on** | Desktop: Windows only | Windows and macOS | Browser | Browser |

Two things transfer completely: **the star schema** and **the discipline of one definition per measure**. The syntax is local knowledge; the modelling is the skill. An analyst who can build Riverstone's model in Power BI can rebuild it in Tableau in a week.

Analysts often meet the others in specific situations: Looker Studio when the data is in Google Analytics or BigQuery and the budget is zero; Metabase or Superset when the company runs its own stack; Tableau in organizations that standardized on it years ago; Excel, still, for the last mile (Chapter 11's Data Model is the same engine as Power BI's).

---

## 16.13 Where BI tools are heading

Three shifts matter for an analyst's work, and all three are moving fast enough that you should check the current state before relying on them.

1. **Natural-language questions.** Power BI's Q&A visual and **Copilot** answer typed questions ("revenue by region last quarter") and draft measures, DAX, and report pages. They work best on a **well-modelled, well-named** semantic model, which is the same work this chapter teaches. Treat generated DAX as a draft: verify it against SQL before it reaches a report.
2. **The semantic model as the shared definition.** Fabric, dbt's semantic layer (Chapter 32), and similar tools push toward one place where "net revenue" is defined for every tool. That's a governance win, and it makes the modelling skill more valuable, not less.
3. **BI merging with the data platform.** Fabric's OneLake, lakehouses, and direct-lake connections blur the line between "the warehouse" and "the report". Chapter 28 covers modelling, and Part 5 (Chapter 49) covers warehouses and lakehouses; for an analyst, the practical effect is fewer imports and more querying of shared tables.

What hasn't changed, and probably won't: someone has to decide what a number means, check it, and design a page that tells the truth in ten seconds.

---
## Common mistakes

| Mistake | Symptom | Fix |
|---|---|---|
| Downloading Power BI Desktop from a third-party site | Unwanted extra software; an outdated version | The Microsoft Store or microsoft.com only (section 16.0) |
| Loading one flat table instead of a star | Slow filters, wrong totals, no time intelligence | Fact and dimension tables joined by keys |
| No date table | `SAMEPERIODLASTYEAR` blank; months sort alphabetically | Build one, mark it, sort month by month number |
| Calculated columns for everything | Big model, wrong ratios at totals | Measures for anything aggregated |
| `COUNTROWS` on the fact table for "orders" | 83,444 instead of 46,356 | `DISTINCTCOUNT ( Sales[order_id] )` |
| `/` instead of `DIVIDE` | Errors or infinity in cards | `DIVIDE`, with a default if needed |
| Cleaning inside Power BI that belongs upstream | Every report repeats the same fixes | Fix in the source, a view, or the warehouse |
| Breaking query folding early | Slow refresh, whole tables pulled | Keep foldable steps first; check View Native Query |
| Bidirectional relationships by default | Numbers change when unrelated slicers move | One-way from dimensions to facts |
| Auto date/time left on | Hidden date tables bloat the model | Turn it off in Options |
| Twenty visuals on a page | Slow page, no message | Fewer visuals, drill-through pages |
| Chart defaults accepted | Unsorted bars, legends, truncated axes | Chapter 15's rules; a saved theme |
| Blank categories hidden | Totals don't match the bars | Rename to "City missing", show in gray |
| No refresh timestamp | Old data mistaken for today's | A `Last Refreshed` measure on every page |
| Personal credentials on the semantic model | Refresh fails when someone leaves | A service account |
| "My workspace" for shared content | Nobody else can maintain it | A shared workspace, with an app |
| Security by separate pages or filters | Anyone can remove a filter | Row-level security in the model |
| Untested roles | A manager sees nothing, or everything | View as, Test as role, check a known total |
| Publishing without checking numbers | The first question in the meeting is "is this right?" | Reconcile every card against SQL |
| Promising a report before checking licences | 200 readers, no Pro licences | Confirm licensing first |

---

## In the real world: the ₹2.3 crore that vanished

Meera published Riverstone's first Power BI report on a Monday in February 2026. The Overview page had four cards, a revenue-and-target line, a region bar, and a product bar; the numbers matched the ERP exactly, and she'd checked each card against SQL.

On Tuesday, Sandeep Gill added the region bars on his phone during a call and got ₹112.4 crore, while the card above them said ₹114.7 crore. He posted a screenshot in the sales group: *"Which number is wrong?"* By lunchtime three people had decided the report couldn't be trusted, and one had gone back to the old spreadsheet pack.

Both numbers were right. Ninety-one of the customers who ordered in 2025 have no city, so they have no region; the region visual dropped them, and the card counted everyone. The gap was ₹2.3 crore, exactly the amount Chapter 14 had flagged and Chapter 15 had insisted on showing.

Meera fixed it in four steps:

1. **Power Query:** replaced the null region of customers with no city with `"City missing"`, so the category exists instead of being blank.
2. **The visual:** the region bar now shows five bars, with "City missing" in gray at the bottom, and a note in the subtitle: *"₹2.3 cr from 91 customers with no city on record."*
3. **A reconciliation panel** on a hidden "About this report" page, reached by a small question-mark button: source and refresh time, row counts (200,381 order lines in the report, from 209,006 lines and 116,194 orders in the source), what's excluded (cancelled orders: 1,956 orders worth ₹4.9 crore in 2025), and the SQL used to check each card.
4. **A `Last Refreshed` measure** in the header, because the second question after "is this right?" is always "is this current?".

She also sent the list of 91 customers to the CRM owner, since the fix that matters is upstream.

The report survived. Two months later the branch heads were using drill-through to their own customers, the monthly pack had stopped being assembled by hand, and the only spreadsheet left in the process was the one the plant used for stock.

What made the difference:

- She **showed the gap instead of hiding it**, which converted a credibility problem into a data-quality request.
- She **put the checking on the report itself**: sources, exclusions, counts, refresh time.
- She **treated the first disagreement as feedback**, not an attack. Reports earn trust in the first fortnight or never.

---

## Project: replace Riverstone's monthly pack with a live report

**Goal:** one published report that answers the monthly review's questions, refreshes itself, and shows only each manager's region.

### Tools you'll need

- **Power BI Desktop** (free, Windows only), current monthly release, installed in section 16.0. macOS or Linux: a Windows virtual machine or cloud desktop.
- **Power BI Service** with a Pro licence or trial, for publishing, refresh, and apps. It needs a work or school account. Without one, everything up to publishing still works, and you can test roles with **View as** in Desktop.
- **PostgreSQL 16 or MySQL 8.0** with `riverstone_full` (tested on 16.15 and 8.0.46), or the CSV files in `companion/full/`.
- **Optional:** DAX Studio and Tabular Editor (free) for performance analysis and model editing; the DAX Formatter website.
- **Companion files (`companion/ch16/`):**
  - `measures.dax`: every measure in this chapter, ready to paste.
  - `expected_measures.md`: each measure's expected value on the full dataset, with the SQL that produces it.
  - `ch16_checks.sql`: that SQL as one runnable script (PostgreSQL; a MySQL version is included).
  - `user_region.csv`: the mapping table for dynamic row-level security.
  - `city_region.csv`: city-to-region mapping for the Customer dimension (section 16.2).
  - `date_table.dax` and `report_checklist.md`: the date table code and a page-review checklist.

**Option A: your own data.** Build the same thing on a dataset from your work (anonymized), with at least one fact table, three dimensions, and a date table.

**Option B: Riverstone.** Use `riverstone_full`.

**Steps**

1. **Model:** star schema, date table marked, keys hidden, fields renamed, formats set.
2. **Measures:** the base set and the time intelligence, in a `_Measures` table, each with a description.
3. **Check every measure against SQL** using `ch16_checks.sql`. Don't design anything until the numbers match.
4. **Overview page:** four or five cards, revenue vs target by month, revenue by region (including "City missing"), revenue by product, and slicers for Year, Region, and Segment. Chapter 15's rules throughout; a theme saved and applied.
5. **Detail page:** customers, reached by drill-through from region, with YoY growth and last order date.
6. **About page:** sources, refresh time, exclusions, row counts, and the definition of each measure in business language.
7. **Publish** to a workspace, set credentials, schedule a refresh, and (if you have the licences) publish an app. *(Needs a work or school account; without one, skip to step 8.)*
8. **Row-level security:** a dynamic role driven by `user_region.csv`, and an All regions role for leaders. Test with **View as** that West + East returns ₹52,60,96,833 and South ₹31,86,24,642 for 2025 (and, with a work or school account, with **Test as role** in the Service).
9. **Write a half-page note to the business:** what the report answers, what it excludes, how often it refreshes, who to ask when a number looks wrong.

**What good looks like:** every card matches SQL to the rupee; the region bars plus "City missing" add to the card total; the page renders in under three seconds (Performance analyzer); roles tested; a refresh timestamp visible; no visual without a title that says something.

**Stretch goals**

- Add incremental refresh on the Sales table, partitioned by year, and compare refresh times.
- Add a "what changed" page: a waterfall of 2024 → 2025 revenue by segment (Retail +₹11.3 crore, Wholesale +₹7.4 crore, Hospitality +₹5.7 crore), with a dynamic title.
- Rebuild the Overview page in Looker Studio or Tableau Public and list, in ten lines, what was easier and what was harder.

---

## Timed challenge: the Q4 branch page (45 minutes)

One page, a clock, and answers you can check. Use `riverstone_full`, a Year slicer set to 2025, and a page filtered to Q4 (October–December).

- **Level 1:** Q4 2025 net revenue, orders, and customers.
- **Level 2:** Q4 2025 average order value and gross margin %.
- **Level 3:** Q4 2025 as a percentage of the Q4 target, and the gap in rupees.
- **Level 4:** Q4 2025 growth over Q4 2024.
- **Level 5:** Q4 revenue by region, sorted, with the missing-region bar shown.
- **Level 6:** the top three products in Q4, and the share of the biggest.
- **Level 7:** clear the Q4 page filter, then find revenue with no sales rep in 2025, and what share of the year that is.
- **Bonus:** a dynamic page title that reads "Q4 2025: ₹42.4 cr, 94.7% of target, +21.8% on last year" and updates when the slicer changes.

Answers at the end of the chapter.

---

## Recap

- **Power BI Desktop** (free, Windows, from the Microsoft Store) builds; the **Service**, which needs a work or school account, refreshes and shares. Pro is $14 and PPU $24 per user per month at the time of writing, with Fabric capacity from F64 letting free users view. Check current pricing before promising anything.
- **Import** beats DirectQuery for anything that fits, and Riverstone's 200,381 order lines fit with room to spare.
- **Clean upstream where you can**; use Power Query for what's left, and keep query folding.
- **Model as a star:** facts (order lines, targets), dimensions (Date, Customer, Product, Employee), a marked date table with whole years, keys hidden, business names.
- **Measures, not calculated columns**, for anything aggregated. A calculated column has a row context; a measure has a filter context. `DISTINCTCOUNT` counts orders, not lines; `DIVIDE` protects against zero and blank; measures call measures.
- **Filter context is the whole of DAX.** `CALCULATE` replaces filters; `KEEPFILTERS` adds; `REMOVEFILTERS`/`ALL` clear; `ALLSELECTED` respects slicers; inside an iterator, context transition turns each row into a filter. Totals are computed under the total's filters, not by adding rows.
- **Time intelligence** needs the date table: `TOTALYTD`, `SAMEPERIODLASTYEAR`, `DATESINPERIOD`. Riverstone 2025: ₹1,14,66,41,651 98.3% of target, +27.0% on 2024, with growth slowing from 31.8% in Q1 to 21.8% in Q4.
- **Design the page** with Chapter 15's rules plus interaction: slicers, drill-through, tooltip pages, bookmarks, a theme, alt text, and a mobile layout.
- **Publishing is a process:** workspace, credentials, schedule, gateway, roles, app. Show the data date and the refresh time, captured at refresh, not with `NOW ()`.
- **Row-level security** lives in the model, filters dimensions, and must be tested against known totals. Once roles exist, a reader in no role sees nothing, so leaders need an All regions role.
- **Most wrong numbers are modelling mistakes**, not DAX mistakes: wrong grain, wrong relationship, blank categories, cancelled orders, or two definitions of revenue.

---

## Key terms

business intelligence · Power BI Desktop · Microsoft Store · administrator (admin) rights · virtual machine · work or school account · Power BI Service · workspace · semantic model (dataset) · report · dashboard · app · Microsoft Fabric · Pro · Premium Per User · Fabric capacity (F SKU) · on-premises data gateway · Import mode · DirectQuery · composite model · live connection · query folding · star schema · fact table · dimension table · grain · relationship · cross-filter direction · date table · mark as date table · calculated table · DAX · measure · calculated column · `DISTINCTCOUNT` · `DIVIDE` · filter context · row context · iterator (`AVERAGEX`) · context transition · `CALCULATE` · `REMOVEFILTERS` · `KEEPFILTERS` · `ALLSELECTED` · `SELECTEDVALUE` · `VAR`/`RETURN` · time intelligence · `TOTALYTD` · `SAMEPERIODLASTYEAR` · `DATESINPERIOD` · slicer · drill-down · drill-through · tooltip page · bookmark · theme · alt text · mobile layout · scheduled refresh · incremental refresh · deployment pipeline · row-level security · `USERPRINCIPALNAME` · `CALCULATETABLE` · object-level security · Performance analyzer · DAX Studio · usage metrics · Q&A · Copilot

*(All terms are defined in the Glossary, Appendix A.)*

---

## Check yourself

- [ ] You can install Power BI Desktop, and explain what Desktop, the Service, a workspace, a semantic model, and an app each are, and who needs which licence.
- [ ] You choose Import or DirectQuery for a reason, and keep query folding alive where it matters.
- [ ] You build a star schema with a marked date table, hidden keys, business names, and set formats.
- [ ] You know when to write a measure and when to write a calculated column.
- [ ] You can write `Net Revenue`, `Gross Margin %`, `Orders`, `% of Target`, `Revenue LY`, and `YoY Growth %` from memory, and check each against SQL.
- [ ] You can explain filter context and row context, and what `CALCULATE`, `REMOVEFILTERS`, `KEEPFILTERS`, and `ALLSELECTED` do to filter context.
- [ ] You design a page with a message, Chapter 15's chart rules, a saved theme, drill-through, and alt text.
- [ ] You publish, set credentials and a schedule, know when a gateway is needed, and share through an app.
- [ ] You implement and test dynamic row-level security, and know what it doesn't protect.
- [ ] You can name the five modelling mistakes most likely to make a number wrong, and check for them.

---

## Exercises

Build in Power BI Desktop where you can; check every answer against `riverstone_full` with SQL.

### Warm-up

1. Which of these needs Power BI rather than a spreadsheet, and why: (a) a one-off pricing analysis; (b) a weekly stock report for six branches; (c) a monthly sales pack read by 40 people; (d) reconciling one export against an ERP?
2. Name the piece of Power BI that does each job: transforms source data; stores the tables and DAX; holds report pages for a team; lets the cloud refresh from an on-premises database; packages reports for readers.
3. Which licence does each person need: an analyst who only builds on their laptop; an analyst who publishes to a shared workspace; 30 branch managers who only read; 400 readers when the workspace sits on F64 capacity?
4. For each, say measure or calculated column: revenue; order size band (small/medium/large); margin %; financial year; number of distinct customers; days since last order (shown per customer in a table).
5. Why is `COUNTROWS ( Sales )` the wrong measure for "orders" in Riverstone's model, and what are the two numbers for 2025?
6. What breaks if the date table stops at 15 December 2025?

### Core

7. Build the star schema and write the seven base measures from section 16.4. Check all six 2025 values in the table in section 16.8.
8. Add `% of Target`, `Gap to Target`, `Revenue LY`, and `YoY Growth %`. What are the 2025 values of each?
9. Build a matrix of quarter by year with `Net Revenue` and `YoY Growth %`. In which quarter of 2025 was growth slowest, and what was it?
10. Build the region bar chart. What is East's 2025 revenue, and how much revenue has no region?
11. Write `Product Share %` with `REMOVEFILTERS`, and check the top four products' shares for 2025.
12. Add a segment matrix with `Net Revenue`, `Revenue LY`, and `YoY Growth %` for 2025. Which segment grew fastest?
13. Write a measure for revenue from orders with no sales rep, and express it as a share of 2025 revenue.
14. What was the value of cancelled orders in 2025, and how many orders? Where in the model should this exclusion live, and why?
15. Build the Overview page from section 16.8 and apply a theme with Chapter 15's palette. List three default settings you changed and why.
16. Add a drill-through page for customers. Which filters travel with the drill-through, and how do you show the reader what they're looking at?
17. Add a `Last Refreshed` measure that shows the last order date in the data and the time of the last refresh in IST, and put it in the page header.
18. Create a static role for South and test it with **View as** in Desktop. What 2025 revenue and customer count do you see?
19. Replace it with a dynamic role driven by `user_region.csv`, tested with **View as → Other user** (and, with a work or school account, **Test as role** in the Service). What does Pooja Desai see, and why does she see two regions?
20. Run **Performance analyzer** on your Overview page. Which visual is slowest, and what would you try first to speed it up?

### Stretch

21. Turn off Auto date/time and compare the model size before and after (**Model view → Properties**, or DAX Studio's VertiPaq Analyzer). What changed?
22. Write a measure that returns the name of the highest-revenue customer in the current selection. What does it return for 2025, and with how much revenue? (Hint: `TOPN` returns a table; you need one value from it.)
23. Riverstone's finance team reports on April–March financial years. Add a `Financial Year` column and a `Revenue FYTD` measure that doesn't use `TOTALYTD`. What is FY2026 revenue to 31 December 2025?
24. Set up incremental refresh on Sales partitioned by year. What must be true of the source query for it to work?

### Think about it

25. A manager asks for "the same numbers as the ERP screen, but prettier". What questions do you ask before building?
26. Two teams publish two reports whose revenue differs by 4%. How do you find the cause, and what would you change so it doesn't happen again?
27. Your report will be read by 300 people who each need a Pro licence. Finance asks whether there's a cheaper way. What options do you present?

---

## Answers

**1.** (b) and (c) need Power BI: repeated, shared, refreshed. (a) is a one-off for a spreadsheet. (d) is a cleaning and reconciliation job for SQL or Power Query (Chapter 14), though its result may feed a report.

**2.** Power Query transforms; the semantic model stores tables and DAX; a workspace holds team content; the on-premises data gateway bridges to internal sources; an app packages reports for readers.

**3.** Free (Desktop only); Pro; Pro each (or a capacity); free licences, because F64 and above allow free users to view content in that capacity.

**4.** Measures: revenue, margin %, distinct customers. Calculated columns: order size band and financial year (you slice by them). "Days since last order" per customer can be either: a column if it's a static attribute refreshed nightly, a measure if it must respond to the date slicer, which is usually what people want.

**5.** The fact table is order **lines**. In 2025 there are **83,444** lines and **46,356** orders, so `COUNTROWS ( Sales )` overstates orders by about 80%. Use `DISTINCTCOUNT ( Sales[order_id] )`.

**6.** Year-to-date and last-year comparisons break for December (and anything after the 15th): `TOTALYTD` and `SAMEPERIODLASTYEAR` need complete periods in the date table, and the December column would silently show a partial month.

**7.** 2025: Net Revenue ₹1,14,66,41,651 · Orders 46,356 · Customers 4,599 · Average Order Value ₹24,735.56 · Gross Margin % 27.5% · all years ₹2,66,34,90,235.

**8.** 2025: `% of Target` **98.3%** (target ₹1,16,69,50,000), `Gap to Target` **−₹2,03,08,349**, `Revenue LY` **₹90,30,15,475**, `YoY Growth %` **+27.0%**.

**9.** Q4, at **+21.8%** (Q1 +31.8%, Q2 +31.0%, Q3 +27.6%). Growth slowed all year even though Q4 was the biggest quarter in rupees (₹42,38,72,808).

**10.** East **₹14,22,56,284** (586 customers). Revenue with no region: **₹2,26,69,946** from 91 customers with no city.

**11.** Storage Box 25L **20.2%**, Food Container Set **18.7%**, Storage Box 10L **17.1%**, Industrial Crate **13.3%**.

**12.** Wholesale, **+31.1%** (₹31,27,28,493 against ₹23,84,57,929). Retail grew 25.4% and Hospitality 25.7%, so Wholesale gained share.

**13.** `Revenue no rep = CALCULATE ( [Net Revenue], ISBLANK ( Sales[sales_rep_id] ) )`: the filter keeps the lines whose `sales_rep_id` is blank. 2025: **₹3,36,30,135** on 2,468 lines, **2.9%** of the year's revenue. It's why a rep-level page needs an "(unassigned)" row (Chapter 14, section 14.3).

**14.** **₹4,92,41,854** across **1,956** orders. The exclusion belongs upstream, in the view or the Power Query filter, so every report shares it; a page-level filter is acceptable in one report, but it will be forgotten in the next one.

**15.** Any three, with reasons, such as: sorted the region bar by value rather than alphabetically; removed the legend and labeled directly; set the theme's data colors to the Riverstone palette; turned off the automatic axis start on a bar chart; set number formats to crore with one decimal.

**16.** The filters on the visual you right-clicked plus the page filters travel with the drill-through (Power BI shows them in the Filters pane). Show the reader by putting a card bound to a measure such as `SELECTEDVALUE ( Customer[Region], "All regions" )` at the top of the detail page, and keep the automatic **Back** button.

**17.** Two pieces, as in section 16.11. A calculated table captured at refresh, `Refresh = ROW ( "Refreshed IST", UTCNOW () + TIME ( 5, 30, 0 ) )`, and the measure `Last Refreshed = "Data to " & FORMAT ( CALCULATE ( MAX ( Sales[order_date] ), REMOVEFILTERS () ), "d MMM yyyy" ) & " · refreshed " & FORMAT ( MAX ( Refresh[Refreshed IST] ), "d MMM yyyy HH:mm" ) & " IST"`. The data date is 28 Dec 2025. `UTCNOW ()` plus 5:30 gives IST on any machine; `NOW ()` in a measure would show the time the page was opened, not the refresh time.

**18.** South in 2025: **₹31,86,24,642** and **1,289** customers. Every visual on every page changes; cards, totals, and the region bar (now one bar) all shrink.

**19.** Pooja Desai sees **₹52,60,96,833** (West ₹38,38,40,549 + East ₹14,22,56,284) across 2,092 customers, because `user_region.csv` has two rows for her email: she is the West manager and also covers East until a fourth regional manager is hired. `VALUES ( UserRegion[region] )` returns both rows' regions, and `IN` keeps customers in either.

**20.** Typically the matrix or the map, because they produce the largest queries. First things to try: reduce the number of visuals, remove unnecessary columns from the visual, replace a complex measure with a simpler one (or a column computed at refresh), and check whether a slicer with many values is the real cost.

**21.** The model gets smaller, often noticeably, because Power BI stops creating a hidden date table for every date column. On a small model like Riverstone's the saving is a few hundred kilobytes; on a model with twenty date columns and ten years of data it can be tens of megabytes, plus faster refreshes.

**22.** One solution:

```dax
Top Customer =
MAXX (
    TOPN ( 1, VALUES ( Customer[Customer] ), [Net Revenue], DESC ),
    Customer[Customer]
)
```

How it works:

- `VALUES ( Customer[Customer] )` is the list of customer names in the current selection.
- `TOPN ( 1, table, [Net Revenue], DESC )` has four arguments: how many rows to keep (1), the table to take them from, what to sort by (each name's `[Net Revenue]`, by context transition), and the direction (`DESC`, biggest first). It returns a **table** with one row.
- A measure must return one value, not a table. `MAXX ( table, Customer[Customer] )` goes through that one-row table and returns the largest name in it, which is the only name. (`SELECTEDVALUE` can't do this job: it takes a column, not a table.)
- **Ties:** if two customers tie for first place, `TOPN` returns both rows, and `MAXX` then returns the name that sorts last alphabetically. Say so in the visual's tooltip if ties are possible.

For 2025 it returns **Galaxy Logistics Patna**, with ₹10,73,806.50 (about ₹10.7 lakh). Check it with SQL:

```sql
SELECT c.customer_name, ROUND(SUM(s.net_revenue), 2) AS revenue
FROM sales_lines s JOIN customers c ON c.customer_id = s.customer_id
WHERE s.order_date >= '2025-01-01'
GROUP BY c.customer_name ORDER BY revenue DESC LIMIT 1;
```

```
     customer_name      |  revenue   
------------------------+------------
 Galaxy Logistics Patna | 1073806.50
(1 row)
```

The query groups by name, as `VALUES ( Customer[Customer] )` does, so two customer records with the same name (the duplicate customers of Chapter 14, section 14.4) count as one.

**23.** The date table already has the `Financial Year` column (section 16.3, step 5). Then:

```dax
Revenue FYTD =
CALCULATE (
    [Net Revenue],
    FILTER (
        ALL ( 'Date' ),
        'Date'[Financial Year] = MAX ( 'Date'[Financial Year] ) && 'Date'[Date] <= MAX ( 'Date'[Date] )
    )
)
```

How it works: `ALL ( 'Date' )` starts from every date, ignoring the cell's own date filter; without it, `FILTER` could only look inside the dates already in the cell, and a December cell could never reach back to April. `FILTER` then keeps the dates in the cell's financial year (`MAX ( 'Date'[Financial Year] )`) **and** (`&&`) on or before the cell's last date. FY2026 runs from 1 April 2025, so to 31 December 2025 it is April–December 2025: **₹88,18,54,486** (verify with `SELECT ROUND(SUM(net_revenue)) FROM sales_lines WHERE order_date BETWEEN '2025-04-01' AND '2025-12-31';`).

**24.** The source must support query folding so the date filters (`RangeStart` and `RangeEnd` parameters) are pushed to the source, the partitioning column must be a date or datetime, and rows must not change in closed partitions (or you must refresh them too). A database source folds; a folder of CSVs generally doesn't.

**25.** Ask: which decisions does this support, and who makes them? Which numbers exactly, with what definition and what exclusions? How current must they be (daily, hourly)? Who may see what? Does the ERP screen agree with finance, and which is the definition of record? And what's the one question the page should answer in ten seconds? "Prettier" usually means "I can't find what I need", which is a design question, not a styling one.

**26.** Compare definitions before comparing charts: the period, the exclusions (cancelled orders, internal accounts), the grain (lines versus orders), the currency and rounding, and the refresh times. Reconcile one small slice (one branch, one month) until you find where the two diverge. Then fix it upstream: one shared semantic model, or one definition in the warehouse (Chapter 32), with the definitions written on an "About" page so the next disagreement takes five minutes.

**27.** Options: (a) Pro for everyone (300 × $14 ≈ $4,200 a month at list); (b) Fabric capacity at F64 or above, where viewers can hold free licences, which is often cheaper above roughly 350–600 viewers; (c) reduce the audience: an app for the people who need interaction, and emailed PDF subscriptions or a paginated report for those who only read one page; (d) check what's already owned, since Microsoft 365 E5 includes Pro. Present the break-even calculation, not only the options.

**Timed challenge answers.** Level 1: ₹42,38,72,808 · 13,777 orders · 4,220 customers. Level 2: AOV ₹30,766.70 · gross margin 27.6%. Level 3: 94.7% of a ₹44,75,00,000 target, a gap of −₹2,36,27,192. Level 4: +21.8% on Q4 2024's ₹34,79,40,682. Level 5: West ₹14,26,88,728 · South ₹11,77,26,527 · North ₹10,29,66,828 · East ₹5,21,20,934 · City missing ₹83,69,792. Level 6: Storage Box 25L ₹8,92,25,213 (21.0%), Food Container Set ₹8,31,56,260 (19.6%), Storage Box 10L ₹7,60,99,616 (18.0%). Level 7 (Q4 filter cleared): ₹3,36,30,135 or 2.9% of 2025 revenue. Bonus: build the title from `SELECTEDVALUE`, `[Net Revenue]`, `[% of Target]`, and `[YoY Growth %]` with `FORMAT`, as in section 16.8.

---

## Where this leads

- **Chapter 20, Automating Reports & Delivering Insights:** subscriptions, alerts, and scheduled delivery around this report, and how to present what it shows.
- **Chapter 24, Requirements, Storytelling & Stakeholders:** turning a page of visuals into a decision.
- **Chapter 28, Advanced SQL, Performance & Data Modeling:** star schemas, slowly changing dimensions, and the warehouse the model should eventually read from.
- **Chapter 32, Analytics Engineering with dbt:** defining measures once, upstream of every BI tool.
- **Chapter 46, Pipelines & Orchestration:** scheduling and orchestrating the loads that feed a BI model.
- **Interview preparation:** the Excel, Google Sheets, VBA & BI Question Bank (Chapter 70) covers DAX, filter context, star schemas, and "why don't these two numbers match?".
