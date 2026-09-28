# Chapter 10. Spreadsheet Fundamentals: Excel & Google Sheets

*Part 2 — The Analyst*

> **Chapter at a glance**
>
> **You will learn to:** find your way around Excel and Google Sheets, create and save workbooks, and manage rows, columns, and sheets · copy, paste values, find and replace · tell what a cell really contains, not only what it shows · import a CSV file without losing leading zeros or scrambling dates · format numbers, dates, and currency · write formulas with relative, absolute, and mixed references · use the essential functions (`SUM`, `AVERAGE`, `COUNT`, `IF`, `COUNTIFS`, `SUMIFS`, text and date functions) · fetch a value from another sheet with a first lookup · sort, filter, and turn a range into a table · guard your data with validation and highlight it with conditional formatting · read error values and name ranges · split and fill data with Flash Fill and Smart Fill · remove duplicates · build a clear chart · print and save as PDF · share, protect, and track versions of a workbook · build a monthly sales tracker from a raw export.
>
> **Before you start:** Chapter 1 (data types, levels of measurement, data quality) and Chapter 2 (files and formats, especially CSV). Chapter 3 (how a business runs on data) helps but isn't required.
>
> **Time needed:** 14–17 hours of reading and practice, spread over two weeks.
>
> **Tools:** Microsoft Excel (Microsoft 365 on Windows is the main version shown; Mac differences are noted) and Google Sheets (free with a Google account). You can follow the whole chapter with only one of them, and section 10.1 shows how to get both at no cost.
>
> **Practice data:** Riverstone Supplies' 2025 sales export (`companion/ch10/riverstone_sales_export_2025.csv`, 330 order lines) and the practice workbook `ch10_practice.xlsx`. They hold the same data as the `riverstone_2025` database you'll query in Chapter 13, so every total here matches. Every formula result in this chapter was calculated on these files and checked independently in Python.

---

## Why this matters

On your first day as an analyst, someone will send you a spreadsheet. It might be a sales export, a list of overdue invoices, or a budget with forty tabs. Before anyone asks you about SQL or Python, they'll ask you to make sense of that file, and they'll judge you on whether your numbers are right.

Spreadsheets are where most business data is first looked at, checked, argued over, and presented. Finance closes the month in them. Sales teams track targets in them. Operations managers plan production in them. Even companies with large data warehouses usually pull the final numbers into Excel or Google Sheets before a meeting. Knowing a spreadsheet well is not a beginner skill you grow out of. It stays in your toolkit for your whole career.

Spreadsheets are also where quiet mistakes happen. A CSV file opened with the wrong settings can turn 2 January into 1 February without any warning. A formula copied one row down can divide by the wrong total and still look reasonable. A total can include cancelled orders nobody meant to count. This chapter teaches both halves: how to get work done quickly, and how to prove that the numbers are right.

You'll learn every technique in **both Excel and Google Sheets**, side by side, because you'll meet both at work. Many Indian companies run on Microsoft 365, many startups and schools run on Google Workspace, and plenty of teams use both. By the end, you'll have turned Riverstone's raw 2025 sales export into a clean monthly tracker that reconciles to the rupee.

---

## In plain English

Picture a large sheet of **graph paper** in a school notebook. Each small square holds one thing: a number, a word, or a date. The columns are labeled with letters across the top and the rows are numbered down the side, so you can say "the square in column B, row 3" and anyone can find it.

Now imagine the notebook has a **helpful assistant** sitting inside it. In any square you can write an instruction instead of a value, such as "add up the squares above me". The assistant does the arithmetic, writes the answer in the square, and redoes it the moment any of those squares change. The instruction stays hidden underneath; you see the answer.

The notebook has **several pages**, one for sales, one for the customer list, one for targets, and an instruction on one page can read squares on another. It has **rubber stamps** that change how an answer looks (₹ signs, commas, dates) without changing the answer itself. And it has **rules taped to some squares**, like "only a whole number goes here", plus **colored markers** that highlight anything unusual.

Here's the mapping:

- The notebook is a **workbook** (the file). Each page is a **worksheet**, or **sheet**.
- Each square is a **cell**, named by its **cell address** (column letter, then row number, such as `B3`). A block of squares is a **range** (`A1:I331`).
- A hidden instruction is a **formula**. It always starts with `=`. Ready-made instructions such as "add up" are **functions** (`SUM`).
- The rubber stamps are **number formats**. They change what you see, not what is stored.
- Rules taped to squares are **data validation**. Colored markers are **conditional formatting**.
- **Excel** and **Google Sheets** are two brands of the same notebook. The pages, squares, and most instructions work the same way; the menus and a few features differ, and this chapter flags each difference.

---

## 10.1 Excel and Google Sheets: what they are and how to get them

A **spreadsheet application** is a program for storing data in a grid and calculating with it. Two dominate business use.

**Microsoft Excel** is part of Microsoft 365. It comes in three forms: the **desktop app** for Windows and Mac (the most complete), **Excel for the web** (runs in a browser, free with a Microsoft account, with fewer features), and mobile apps. Companies usually license it through a Microsoft 365 business plan. Older perpetual versions such as Excel 2019 are still found in offices and lack some newer functions; this chapter notes when a function needs Microsoft 365 or Excel 2021 or later.

**Google Sheets** runs in a web browser and is part of Google Workspace. It's free with a personal Google account, and companies pay for Workspace to get admin controls and more storage. Your files live in Google Drive, save automatically, and can be edited by several people at once.

| Question | Excel (Microsoft 365) | Google Sheets |
|---|---|---|
| Where it runs | Desktop app (Windows, Mac), browser, mobile | Browser, mobile apps |
| Cost to start learning | Free Excel for the web with a Microsoft account; full desktop app needs a subscription | Free with a Google account |
| Where files live | Your computer, OneDrive, or SharePoint | Google Drive |
| File format | `.xlsx` | Google's own format; imports and exports `.xlsx` and `.csv` |
| Size limit | 1,048,576 rows and 16,384 columns per sheet | 10 million cells per spreadsheet, across all sheets |
| Strongest at | Heavy analysis, large workbooks, Power Query and Power Pivot (Chapter 11), VBA macros (Chapter 19) | Real-time collaboration, sharing, version history, Google Forms, Apps Script (Chapter 19) |

> **Tool note.** The limits in this table are the documented limits at the time of writing. Google counts blank cells toward its 10 million, and both apps slow down well before their limits. If a file is heading toward hundreds of thousands of rows, that's a sign it belongs in a database (Chapter 12).

**Getting set up.** For Excel, sign in at office.com with a free Microsoft account to use Excel for the web, or install the desktop app if your employer or college provides Microsoft 365. For Google Sheets, sign in at sheets.google.com. Download the companion folder `companion/ch10/` (Appendix E) so you have the practice files.

### A tour of the screen

Open `ch10_practice.xlsx` in both apps. In Excel, double-click the file. In Google Sheets, go to **File → Import → Upload**, choose the file, and pick **Create new spreadsheet**. Figure 10.1 shows the same workbook in each.

![Two side-by-side sketches of the same workbook open in Excel and in Google Sheets, labeling the menu, ribbon or toolbar, name box, formula bar, grid, and sheet tabs](figures/fig10-1-spreadsheet-anatomy.svg)

*Figure 10.1 — The same workbook in Excel and Google Sheets. The grid, name box, formula bar, and sheet tabs behave the same way; Excel groups commands on a ribbon, while Sheets keeps most of them in menus.*

The parts you'll use constantly:

- **The grid.** Columns are lettered `A`, `B`, `C` … `Z`, `AA`, `AB` …; rows are numbered from `1`.
- **The name box** (top left) shows the address of the selected cell. You can also type an address there, such as `J331`, and press Enter to jump to it.
- **The formula bar** (next to *fx*) shows what the selected cell really contains. This is the single most important habit in this chapter: when a number looks odd, look at the formula bar.
- **Sheet tabs** (bottom) switch between sheets. Right-click a tab to rename, move, copy, color, or hide it.
- **The ribbon** (Excel) groups commands into tabs such as Home, Insert, Formulas, and Data. **Menus** (Sheets) hold the same commands under File, Edit, View, Insert, Format, Data, Tools, and Extensions.

> **Tool note: finding a command you can't see.** Both apps have a search box for commands. In Excel it's the search bar at the top of the window (or **Alt+Q**). In Google Sheets, press **Alt+/** (Windows) or **Option+/** (Mac) to search the menus. When this chapter gives a menu path you can't find, search for the command's name.

---

### Creating, opening, and saving a workbook

**Excel.** Start Excel and choose **Blank workbook**, or **File → New** for a template. Open an existing file with **File → Open** (**Ctrl+O**). Save with **File → Save** (**Ctrl+S**); the first time, Excel asks where. **File → Save As** saves a copy under a new name, in a new place, or in another format. If the file is on OneDrive or SharePoint, the **AutoSave** switch (top left) saves every change as you go; for files on your own computer, press **Ctrl+S** often.

**Google Sheets.** Go to sheets.google.com and click **Blank spreadsheet** (or **Template gallery**), or in Google Drive choose **New → Google Sheets**. There's no Save button: every change is saved automatically to Drive, and the "Saved to Drive" note at the top confirms it. Rename the file by clicking its name (top left). **File → Make a copy** is Sheets' version of Save As.

The Excel file formats you'll meet:

| Extension | What it is | When you'll see it |
|---|---|---|
| `.xlsx` | The standard Excel workbook | Almost always |
| `.xlsm` | A workbook that contains macros (Chapter 19) | Automated workbooks; Excel warns before running macros |
| `.xls` | The pre-2007 format | Old files and old systems; save as `.xlsx` when you can |
| `.csv` | Plain text, one sheet, values only (section 10.4) | Exports from other systems |

> **Tool note: name files so the next person can find them.** A name such as `riverstone_sales_tracker_2025.xlsx` (what, whose, which period) beats `Book1.xlsx` or `final_v3.xlsx`. Avoid spaces and special characters if the file will be read by scripts later (Chapters 17 and 20).

## 10.2 Workbooks, sheets, cells, and ranges

The practice workbook has five sheets:

| Sheet | Contents | Rows of data |
|---|---|---|
| Data | Riverstone's 2025 sales export: one row per **order line** | 330 |
| Customers | Customer code, name, city, segment, signup date | 24 |
| Products | Product ID, name, category, list price, unit cost | 8 |
| Targets | Monthly revenue target for 2025 | 12 |
| Cell detective | Six cells that look alike but aren't (section 10.3) | 6 |

Click the **Data** sheet. Row 1 holds the **headers** (column names), and each row below is one line of an order: which product, how many, at what price and discount. An order with three products has three rows. This is the **grain** of the data from Chapter 1: one row per order line, not one row per order. Keeping the grain in mind will stop you from counting 330 "orders" when Riverstone received 175.

A **range** is a rectangular block of cells, written as its top-left and bottom-right corners joined by a colon. The whole export, headers included, is `A1:I331`: nine columns (`A` to `I`) and 331 rows. The quantities alone are `E2:E331`.

A few ways to refer to cells:

| You write | It means |
|---|---|
| `B3` | One cell: column B, row 3 |
| `A2:I331` | The data rows of the export |
| `E:E` | All of column E |
| `2:2` | All of row 2 |
| `Customers!B2:B25` | Cells on another sheet (sheet name, `!`, range) |
| `'Cell detective'!A2` | A sheet name with a space must be wrapped in single quotes |

> **Try it.** Click the name box, type `I331`, and press Enter. You land on the last row of the export: order 10175, sold by Neha Kulkarni. Now press **Ctrl+Home** to jump back to `A1` (on a Mac laptop without a Home key, Excel uses **Fn+Ctrl+Left arrow**).

**Moving around fast.** Press **Ctrl+Arrow** (Mac Excel: **Cmd+Arrow**) to jump to the edge of the data in that direction; add **Shift** to select as you go. **Ctrl+Shift+End** selects from the current cell to the last used cell. These shortcuts work in both apps, and section 10.15 lists more.

### Quick answers from the status bar

*"What's the total of these cells?"* You don't always need a formula. Select `J2:J331` after you've added the net revenue column in section 10.6 (or any column of numbers now), and look at the bottom of the window.

- **Excel** shows **Average**, **Count**, and **Sum** in the **status bar** (bottom right). Right-click the status bar to add **Numerical Count**, **Minimum**, and **Maximum**.
- **Google Sheets** shows **Sum** in the bottom-right corner; click it to switch to Average, Min, Max, Count, and Count Numbers.

For the net revenue column, the status bar reads Sum **4,398,121**, Average **13,327.64**, and Count **330**, the same values `SUM`, `AVERAGE`, and `COUNT` return in section 10.7. It's the fastest way to sanity-check a number someone quotes to you in a meeting.

### Rows, columns, and sheets

| To do this | Excel | Google Sheets |
|---|---|---|
| Insert a row or column | Right-click the row number or column letter → **Insert** (**Ctrl+Shift+=**) | Right-click → **Insert 1 row above** / **Insert 1 column left** |
| Delete a row or column | Right-click → **Delete** (**Ctrl+-**) | Right-click → **Delete row** / **Delete column** |
| Change column width | Drag the border between column letters; double-click it to fit the contents | Same; or right-click → **Resize column → Fit to data** |
| Hide and unhide | Right-click → **Hide**; select the neighbors, right-click → **Unhide** | Right-click → **Hide column**; click the arrows that appear to unhide |
| Add a sheet | The **+** next to the sheet tabs (**Shift+F11**) | The **+** at the bottom left |
| Rename, move, copy, color a sheet | Right-click the tab | Right-click the tab (or its arrow) |

> **Watch out: `#####` isn't an error in your data.** A cell full of `#####` means the column is too narrow to show the number or date. Widen the column and the value appears. (A negative number formatted as a date also shows `#####`, because a date can't be negative.)

When you **insert** a row inside a range that a formula uses, the formula grows to include it: `=SUM(J2:J331)` becomes `=SUM(J2:J332)`. When you **delete** a cell that a formula points at directly, the formula shows `#REF!` (section 10.6), because the thing it referred to no longer exists.

### Copy, cut, and paste

Select cells, then **Ctrl+C** (copy) or **Ctrl+X** (cut), click the destination, and **Ctrl+V** (paste). On a Mac, use **Cmd** in both apps. The difference matters for formulas:

- **Copying** a formula shifts its relative references by the distance moved (section 10.6 shows why that's useful and when it goes wrong).
- **Cutting** (moving) a formula keeps its references pointing at the **same cells**. So does moving a block of cells by dragging its border.

Paste doesn't have to paste everything. **Paste special** lets you choose:

| Paste only… | Excel | Google Sheets |
|---|---|---|
| Values (formula results, no formulas) | **Home → Paste → Paste Values** (**Ctrl+Alt+V**, then **V**) | **Edit → Paste special → Values only** (**Ctrl+Shift+V**) |
| Formats | **Home → Paste → Formatting** | **Edit → Paste special → Format only** |
| Column widths | **Paste Special → Column widths** | **Edit → Paste special → Column width only** |
| Rows turned into columns | **Paste Special → Transpose** | **Edit → Paste special → Transposed** |

**Paste values** is the one you'll use daily: to freeze a result before sending a file, to turn repaired codes into real text (section 10.8), or to stop a pasted table from carrying broken references into another workbook.

### Find and replace, and undo

**Find** (**Ctrl+F**) jumps to a value. **Find and replace** (**Ctrl+H** in both apps; on a Mac, **Ctrl+H** in Excel and **Cmd+Shift+H** in Sheets) changes it everywhere. In the dialog you can limit the search to a sheet or the whole workbook, match case, match the entire cell, and, in Excel, choose whether to look inside **Formulas** or **Values**.

> **Watch out: replace can reach further than you meant.** Replacing `Box` with `Bin` also changes `Lunch Box Set` and any formula text containing "Box". Tick **Match entire cell contents** when you mean whole values, select the range first, and check the count the dialog reports before you save.

**Undo** (**Ctrl+Z**) reverses the last action, and pressing it again goes further back; **Redo** is **Ctrl+Y**. Undo history is lost when an Excel file is closed. Google Sheets keeps version history instead (section 10.13).

---

## 10.3 What a cell really contains

Chapter 1 promised that this chapter would show you how to check what a cell really contains. It matters because **what a cell shows and what it holds can be different things**, and formulas use what it holds.

A cell can hold one of four kinds of content:

- a **number** (dates and times are numbers too, as you'll see);
- **text** (also called a *string*): letters, or digits that the app has been told to treat as characters;
- a **logical value**: `TRUE` or `FALSE`;
- a **formula**, which produces one of the above, or an **error** such as `#N/A` or `#DIV/0!`.

Open the **Cell detective** sheet. Cells `A2` to `A7` look ordinary. Figure 10.2 shows what four of them really contain.

![A four-row diagram contrasting what a cell displays with what it stores: 32,063 stores 32062.5, a date stores 45659, 0005 is text, and 2900 with a trailing space is text](figures/fig10-2-value-vs-display.svg)

*Figure 10.2 — What you see versus what the cell contains. Display formats round numbers and dress day counts up as dates; text can look exactly like a number.*

### Four ways to investigate a cell

1. **Look at the formula bar.** Click `A7`. The cell shows `32,063`; the formula bar shows `32062.5`. A number format is rounding the display. Any formula that uses `A7` uses 32062.5.
2. **Look at the alignment.** By default, numbers line up on the right of a cell and text lines up on the left. `A2` (2900, a number) sits on the right; `A3` (`2900` stored as text) sits on the left. Excel also marks numbers stored as text with a small green triangle in the corner; hover over the warning icon to convert them.
3. **Ask with a function.** `ISNUMBER` returns `TRUE` for numbers, `ISTEXT` for text, and `LEN` counts characters.
4. **Show every formula.** Press **Ctrl+\`** (the key above Tab) in either app to switch between showing results and showing formulas. Press it again to switch back. In Excel the command is also at **Formulas → Formula Auditing → Show Formulas**; in Sheets, **View → Show → Formulas**.

Try these formulas in column C of the Cell detective sheet. The results are the same in Excel and Google Sheets:

```excel
=ISNUMBER('Cell detective'!A2)      → TRUE
=ISTEXT('Cell detective'!A3)        → TRUE
=LEN('Cell detective'!A3)           → 4
=LEN('Cell detective'!A4)           → 5
=ISNUMBER('Cell detective'!A5)      → TRUE
=ISNUMBER('Cell detective'!A6)      → FALSE
=SUM('Cell detective'!A2:A4)        → 2900
```

How it works:

- `A3` and `A4` both display `2900`, but `LEN` reveals that `A4` has five characters: the digits plus a **trailing space**, invisible on screen. Text copied from websites, PDFs, and other systems often carries spaces like this.
- `A5` displays `2025-01-02` and `ISNUMBER` says it's a number. `A6` displays `02-01-2025` and is text. Only `A5` can be sorted by date, filtered by month, or used in date arithmetic.
- `SUM(A2:A4)` returns 2900, not 8700. **`SUM` silently skips text in a range.** Nothing warns you. If a column of amounts contains some numbers stored as text, the total comes out smaller than it should be, which is the most common way a spreadsheet total goes wrong without anyone noticing.

> **Watch out: SUM ignores text without telling you.** Before you trust a total, compare `=COUNT(range)` (how many numbers) with `=COUNTA(range)` (how many non-empty cells). On a column of amounts they should match. If `COUNTA` is bigger, some amounts are text.

### Dates are numbers in disguise

Both apps store a date as the **number of days** since a starting point, and a date format makes that number look like a date. In the Windows Excel date system, day 1 is 1 January 1900; Google Sheets counts from 30 December 1899, which gives the same numbers for any modern date. Order 10001's date, 2 January 2025, is stored as **45659**:

```excel
=Data!B2*1        → 45659
```

Because dates are numbers, you can subtract them to get days, add 30 to get a due date, and compare them with `>` and `<`. Because they're only numbers underneath, a date that arrives as *text* can't do any of that. Section 10.4 shows how dates become text by accident, and section 10.8 shows how to rescue them.

> **Watch out: a date result that looks like 1900.** Subtract two dates, such as `=EOMONTH(B2,0)-B2` (days from an order to the end of its month), and the answer may display as `29-01-1900` because the cell picked up a date format. The value is 29. Change the cell's format to **Number** or **General** and the 29 appears.

---

## 10.4 Importing a CSV file without damage

Chapter 2 showed that a CSV file is plain text: values separated by commas, with no information about which columns are numbers, dates, or codes. When a spreadsheet opens a CSV, it **guesses** each column's type. Those guesses cause two of the most common data disasters in business: **leading zeros vanish** and **dates get scrambled**.

Open `riverstone_sales_export_2025.csv` in a text editor (Notepad on Windows, TextEdit on Mac). The first lines are:

```
order_id,order_date,customer_code,product_id,quantity,unit_price,discount_pct,status,sales_rep
10001,02-01-2025,0002,108,10,290,0,Delivered,Neha Kulkarni
10002,05-01-2025,0003,107,55,380,0,Delivered,Farah Khan
10003,12-01-2025,0005,101,25,430,0,Delivered,Rahul Mehta
```

Riverstone's ERP writes dates **day first** (`02-01-2025` is 2 January 2025, the Indian convention) and pads customer codes to four digits (`0002`). Both details are about to cause trouble.

### What goes wrong

We opened this file in a spreadsheet app that read the dates month first, as a computer with United States regional settings does, and counted the damage. Figure 10.3 shows the result.

![Three panels: the raw CSV text, the file opened with month-first dates showing swapped dates and codes without zeros, and the file imported with column types set correctly](figures/fig10-3-csv-import-damage.svg)

*Figure 10.3 — The same 330 lines imported two ways. Nothing warned about the damage in the middle panel; the numbers are measured on Riverstone's export.*

- **Customer codes lost their zeros in all 330 lines.** `0002` became the number `2`. A code is a label, not a quantity (Chapter 1's levels of measurement), so the zeros were part of it. Every lookup against the Customers sheet, where the code is `0002`, now fails.
- **135 dates became the wrong real dates.** Any date whose day is 12 or less could be read month first, so `02-01-2025` became 1 February 2025 and `12-01-2025` became 1 December 2025. Ten of them survived by luck because the day equals the month (`03-03-2025`).
- **195 dates stayed as text**, because a month-first reading of `13-01-2025` would need a 13th month.

The dangerous part is the middle group. The 135 wrong dates are real dates, they sort and filter normally, and nothing looks broken. On the damaged file, a formula for January revenue returns **₹91,649**. The correct figure is **₹202,640**.

### Importing correctly in Excel

Don't double-click the CSV. Import it so you can tell Excel what each column is.

1. Open a blank workbook. Go to **Data → Get & Transform Data → From Text/CSV**, choose the file, and click **Import**.
2. In the preview window, set **Data Type Detection** to **Do not detect data types**, then click **Transform Data**. The Power Query Editor opens (Chapter 11 covers it in depth).
3. Right-click the `order_date` header and choose **Change Type → Using Locale…**. Set **Data Type** to **Date** and **Locale** to **English (India)**, then click **OK**. Power Query now reads `02-01-2025` as 2 January.
4. Leave `customer_code`, `status`, and `sales_rep` as **Text** (the **ABC** icon). Set `order_id`, `product_id`, `quantity`, `unit_price`, and `discount_pct` to **Whole Number** or **Decimal Number** with the type icon at the left of each header.
5. Click **Home → Close & Load**. The data arrives as a table on a new sheet, with codes intact and real dates.

You can also stop Excel from stripping zeros when you type or open files: **File → Options → Data → Automatic Data Conversion**, then clear **Remove leading zeros and convert to a number**. These options don't affect Power Query imports, which use the types you set in step 4.

### Importing correctly in Google Sheets

1. Set the spreadsheet's locale first: **File → Settings → General → Locale → India**, then **Save settings**. The locale decides how Sheets reads dates and which date and currency formats it offers.
2. Go to **File → Import → Upload** and choose the CSV. Set **Import location** to **Insert new sheet(s)** and **Separator type** to **Comma**.
3. Decide on **Convert text to numbers, dates, and formulas**. If you leave it checked, Sheets converts quantities and prices to numbers, reads dates using the India locale, and strips the zeros from codes. If you clear it, every column arrives as text, codes included.
4. With the box checked, repair the codes afterward with `=TEXT(C2,"0000")` (section 10.8). This works only because every code has exactly four digits. When codes vary in length, clear the box instead and convert the numeric and date columns yourself.

> **Watch out: check the import, don't assume it.** After any import, run three quick checks. The row count should match the source (`=COUNTA(A2:A331)` → 330). A code column should still show its zeros. A date column should be all real dates: `=COUNT(B2:B331)` should equal the number of rows, because `COUNT` counts only numbers and real dates are numbers. On the damaged file, that formula returns 135.

> **Spreadsheet link.** The same problem exists in every tool that reads CSV files: Python's pandas (Chapter 18) and database loaders (section 12.13) guess types too. The fix is always the same: tell the tool the type of each column instead of letting it guess.

---

## 10.5 Entering and formatting data

### Typing data

Click a cell, type, and press **Enter** (move down) or **Tab** (move right). Press **F2** (Mac Excel: **Ctrl+U**; Sheets: **Enter** or **F2**) to edit a cell without retyping it. Press **Esc** to cancel an edit.

Both apps guess the type of what you type, in the same way they do with CSV files. `0005` becomes 5. `1-2` may become a date. `12345678901234567890` becomes a rounded number in scientific notation, because both apps keep only 15 significant digits. To type something as text on purpose, start with an apostrophe: `'0005`. The apostrophe doesn't appear in the cell; it only tells the app "this is text". Or format the column as text *before* typing (below).

> **Watch out: long ID numbers.** Phone numbers with country codes, 16-digit card numbers, and long order references must be stored as text. Once a 16-digit number has been converted, the digits past the 15th are gone and can't be recovered.

**Fill handle.** Select a cell and drag the small square at its bottom-right corner. Dragging a formula copies it (section 10.6). Dragging `Jan` gives `Feb`, `Mar` … Double-clicking the fill handle copies a formula down as far as the column next to it has data, which is how you fill 330 rows in one move.

### Filling a series

The fill handle (above) does more than copy. Type `1` and `2` in two cells, select both, and drag: you get 3, 4, 5 … Type `2025-01-01`, drag, and you get one day per row. To step by month, type `2025-01-01` and `2025-02-01`, select both, and drag. In Excel, **Home → Editing → Fill → Series** gives exact control (step value, stop value, months or years); in Sheets, the two-cell pattern works the same way.

### Letting the app spot a pattern: Flash Fill and Smart Fill

*"Split each sales rep's name into first name and last name."* Next to `sales_rep`, type `Neha` against the first *Neha Kulkarni* row and start typing the next first name.

- **Excel** suggests the rest in grey; press **Enter** to accept, or use **Data → Data Tools → Flash Fill** (**Ctrl+E**).
- **Google Sheets** offers **Smart Fill** suggestions in the same way; press the tick to accept (**Ctrl+Shift+Y** opens the suggestion).

These tools write **fixed values**, not formulas, so they don't update if the names change. When the data will change, use a formula instead: `=LEFT(D1,FIND(" ",D1)-1)` returns `Neha` from `Neha Kulkarni`, and `=MID(D1,FIND(" ",D1)+1,100)` returns `Kulkarni`. (`FIND` gives the position of the space; section 10.8 covers `LEFT` and `MID`.)

### Splitting one column into several

**Excel: Data → Data Tools → Text to Columns → Delimited → Space → Finish.** **Google Sheets: Data → Split text to columns**, then choose the **Separator** (Space). Both split `Neha Kulkarni` into two cells. Insert empty columns to the right first, because the split overwrites whatever is there.

> **Watch out: splitting names is rarely clean.** "Farah Khan" splits into two parts, but a name with three words or a single-word name won't. Check the results, and keep the original column.

### Styling cells

Styling is for readers: it shows where headers are, which cells are inputs, and what to look at. It never changes values.

| To do this | Excel (Home tab) | Google Sheets |
|---|---|---|
| Bold, italic, font, size, color | **Font** group (**Ctrl+B**, **Ctrl+I**) | Toolbar (**Ctrl+B**, **Ctrl+I**) |
| Fill color | **Font → Fill Color** | Toolbar paint bucket |
| Borders | **Font → Borders** | Toolbar **Borders** |
| Align left, center, right, top | **Alignment** group | Toolbar align buttons, or **Format → Alignment** |
| Wrap long text inside a cell | **Alignment → Wrap Text** | **Format → Wrapping → Wrap** |
| Copy formatting to other cells | **Clipboard → Format Painter** (double-click to reuse) | Toolbar **Paint format** (double-click to reuse) |
| Clear formatting but keep values | **Editing → Clear → Clear Formats** | **Format → Clear formatting** (**Ctrl+\\**) |
| Ready-made styles | **Styles → Cell Styles** | **Format → Alternating colors** |

A simple, professional convention: bold headers with a fill, numbers right-aligned with consistent decimals, a light fill on cells people are meant to type into, and nothing else. **Merge & Center** looks tidy in titles but breaks sorting, filtering, and copying inside data; for a title spread across columns, use **Excel: Format Cells → Alignment → Horizontal: Center Across Selection** instead.

### Number formats

A **number format** controls how a value is displayed. It never changes the stored value (section 10.3).

| To do this | Excel | Google Sheets |
|---|---|---|
| Open all format options | **Home → Number** group, or **Ctrl+1** (Mac: **Cmd+1**) | **Format → Number** |
| Comma separators | **Home → Number → Comma Style** | **Format → Number → Number** |
| Currency ₹ | **Ctrl+1 → Currency → Symbol: ₹ English (India)** | **Format → Number → Custom currency** → search "Indian rupee" |
| Percentage | **Home → Number → %** | **Format → Number → Percent** |
| Date | **Ctrl+1 → Date**, or **Custom** and type `yyyy-mm-dd` | **Format → Number → Custom date and time** |
| Text (before typing) | **Ctrl+1 → Text** | **Format → Number → Plain text** |
| More or fewer decimals | **Home → Number → Increase/Decrease Decimal** | toolbar **.0** and **.00** buttons |

**Custom formats** use codes. The ones analysts use every week:

| Code | 32062.5 shows as | Use for |
|---|---|---|
| `#,##0` | 32,063 | Whole rupees in reports |
| `#,##0.00` | 32,062.50 | Exact amounts |
| `0.0%` | (for 0.675) 67.5% | Percentages |
| `+0.0%;-0.0%` | (for 0.252) +25.2% | Changes, with a sign |
| `0000` | (for 5) 0005 | Display padding (the value stays 5) |
| `yyyy-mm-dd` | (for 45659) 2025-01-02 | Unambiguous dates |
| `mmm yyyy` | (for 45659) Jan 2025 | Month labels |

> **Tool note: Indian digit grouping.** This book writes numbers with international grouping (₹4,335,471). If your team prefers lakh and crore grouping (₹43,35,471), choosing **English (India)** as the locale in Sheets, or the ₹ English (India) currency symbol in Excel, applies it to currency formats. Pick one style for a report and use it everywhere.

> **Watch out: `0000` formatting doesn't fix a code.** A custom format of `0000` makes the number 5 *look like* `0005`, but the cell still holds 5, so a lookup for the text `0005` still fails. To create real text, use `=TEXT(C2,"0000")`.

**Tidy layout habits** that make a sheet easier to read and harder to break: one header row, no blank rows or columns inside the data, no merged cells in data areas, units in the header (`net_revenue_inr` or a note above the table), and dates in `yyyy-mm-dd` wherever other people will read them.

### Times are fractions of a day

If dates are whole days (section 10.3), a time is the **fraction of a day** that has passed. `9:30 AM` is stored as 0.3958333 (9.5 hours ÷ 24). Type times with a colon (`9:30`, `17:30`) and both apps recognize them.

That's why a time difference needs `× 24` to become hours:

```excel
=(TIME(17,30,0)-TIME(9,15,0))*24     → 8.25
```

A shift from 9:15 AM to 5:30 PM is 8.25 hours. Without `*24`, the cell would show `8:15` in a time format, or 0.34375 as a plain number. Format hour totals as **Number**, and use a format like `[h]:mm` if you want totals above 24 hours to display as hours rather than wrapping around.

---

## 10.6 Formulas and cell references

### Your first formula

*"What is each order line worth after its discount?"* Riverstone's rule for **net revenue**, the same rule you'll write in SQL in Chapter 12, is quantity × unit price × (1 − discount % ÷ 100).

On the **Data** sheet, type `net_revenue` in `J1`. In `J2`, type:

```excel
=E2*F2*(1-G2/100)
```

Press Enter. `J2` shows **2900**. Double-click the fill handle to copy the formula down to row 331.

How it works:

- Every formula starts with `=`. Without it, the app stores the characters as text.
- `E2`, `F2`, and `G2` are **cell references**: the formula reads whatever those cells hold, and recalculates if they change.
- The operators are `+` `-` `*` (multiply) `/` (divide) `^` (power) and `&` (join text). The order of operations is the one from school: brackets first, then `^`, then `*` and `/`, then `+` and `-`. `(1-G2/100)` divides first, then subtracts.

Check row 5 by hand. Order 10003 has a second line: 45 Storage Box 25L at ₹750 with a 5% discount. 45 × ₹750 = ₹33,750, and 95% of ₹33,750 is **₹32,062.50**. `J5` shows 32062.5. ✓

Click `J3` and look at the formula bar: `=E3*F3*(1-G3/100)`. You typed the formula once, yet each row refers to its own row. That's a relative reference at work.

### AutoSum and inserting functions

For a quick total, click the cell below a column of numbers and use **AutoSum**: **Excel: Home → Editing → AutoSum** (**Alt+=**; Mac: **Cmd+Shift+T**). Excel guesses the range above and writes `=SUM(…)`; check the highlighted range before pressing Enter. In **Google Sheets**, use the toolbar's **Σ Functions** button (**→ SUM**) or type the formula.

To browse functions with help on each argument, use **Excel: Formulas → Insert Function** (the *fx* button beside the formula bar) and **Sheets: Insert → Function**. While you type a function name, both apps show its arguments; in Sheets, press **F1** in the formula to expand the help card.

### Relative, absolute, and mixed references

When you copy a formula, the app adjusts its references by the same distance you moved it. A reference that shifts like this is a **relative reference**. Most of the time it's exactly what you want. Sometimes it's a silent disaster.

*"What share of the export total does each line represent?"* In scratch column `O`, type in `O2`:

```excel
=J2/SUM(J2:J331)
```

Format it as a percentage and fill it down. The first rows look sensible: 0.066%, 0.476% … Now scroll to row 331. It says **100.000%**. Figure 10.4 shows why.

![Two panels comparing a share-of-total formula copied down with a relative range, where the total shrinks each row and shares add to 656.8 percent, and with an absolute range, where shares add to 100 percent](figures/fig10-4-relative-vs-absolute.svg)

*Figure 10.4 — Copying a share-of-total formula down 330 rows. With a relative range, the denominator slides down and shrinks; with `$` signs, every row divides by the same total.*

Copied to row 3, the formula became `=J3/SUM(J3:J332)`: the *range* moved down one row too, so it no longer includes row 2. By row 331 the "total" is a single line divided by itself. Row 3's wrong share (0.476%) is so close to the right one (0.475%) that nobody would spot it, yet the column adds up to **656.8%**.

The fix is an **absolute reference**, which stays fixed when copied. Add a `$` before the column letter and before the row number:

```excel
=J2/SUM($J$2:$J$331)
```

Now every row divides by the same total, and the column adds up to **100.0%**. ✓

A **mixed reference** fixes only one part: `$J2` fixes the column and lets the row move; `J$2` fixes the row and lets the column move. You'll use them for grids that combine a row input with a column input. On a blank area of the sheet, put three prices down a column and three discounts across a row:

| | **B** | **C** | **D** |
|---|---|---|---|
| **11** | | 0.05 | 0.10 |
| **12** | 430 | | |
| **13** | 750 | | |
| **14** | 1400 | | |

In `C12`, type `=$B12*(1-C$11)` and copy it across to `D12` and down to row 14. `$B12` always reads column B (the price) while its row moves; `C$11` always reads row 11 (the discount) while its column moves. `C13` shows 712.5 (₹750 less 5%) and `D14` shows 1260 (₹1,400 less 10%). ✓

**Switching quickly.** Click inside a reference in the formula bar and press **F4** (Mac Excel: **Cmd+T**). Each press cycles `J2` → `$J$2` → `J$2` → `$J2` → `J2`. Google Sheets supports F4 in the same way.

> **Watch out: a total that includes itself.** If you put `=SUM(J2:J332)` in `J332`, the formula refers to its own cell. That's a **circular reference**. Excel shows a warning and usually returns 0; Google Sheets shows `#REF!`. Put totals outside the range they add up, or above the data.

### Error values and what they mean

When a formula can't produce a result, it shows an **error value**. Each one tells you what kind of problem to look for:

| Error | Meaning | Riverstone example | Typical fix |
|---|---|---|---|
| `#DIV/0!` | Dividing by zero or by an empty cell | `=J2/0` | Check the denominator; `=IF(B5=0,"",D5/B5)` for months with no target |
| `#VALUE!` | The wrong type of value, such as text in arithmetic | `="abc"*2` | Find the text cell (section 10.3); convert it with `VALUE` |
| `#NAME?` | A misspelled function, an unquoted text value, or an unknown named range | `=SUMM(J2:J5)` | Correct the spelling; put text in quotes |
| `#N/A` | A lookup didn't find what it was looking for | Looking up customer code `9999` | Check the code and its type (section 10.9); add an "if not found" value |
| `#REF!` | A reference points at cells that were deleted | A formula using a deleted row | Undo, or rewrite the reference |
| `#NUM!` | An impossible number, such as `=SQRT(-1)` | — | Check the inputs |
| `#SPILL!` (Excel) | A formula that returns several cells is blocked by existing data (Chapter 11) | — | Clear the cells in its way |
| `#ERROR!` (Sheets) | Sheets couldn't read the formula at all, such as a missing bracket | — | Check brackets, commas, and quotes |
| `#####` | Not an error: the column is too narrow | A date in a narrow column | Widen the column |

> **Try it.** Type each of `=J2/0`, `="abc"*2`, and `=SUMM(J2:J5)` into spare cells. Hover over (Excel: click the warning icon beside) each error to read the explanation both apps give, then delete the cells.

### Named ranges

A **named range** gives a range a meaningful name, so `=SUM(net_revenue)` replaces `=SUM(Data!$J$2:$J$331)`.

- **Excel:** select `J2:J331`, click the **name box**, type `net_revenue`, and press Enter. Manage names with **Formulas → Defined Names → Name Manager**.
- **Google Sheets:** select the range, then **Data → Named ranges → Add a range**, and type the name.

```excel
=SUM(net_revenue)     → 4398121
```

Names are always absolute, so they don't slide when copied, and they make formulas readable to the next person. Tables (section 10.10) do the same job and also grow with the data, which is why many analysts prefer them for data columns and keep names for single input cells such as `as_of_date` or `vat_rate`.

### Checking a formula's inputs

In long workbooks you'll want to see which cells feed a formula.

- **Excel: Formulas → Formula Auditing → Trace Precedents** draws arrows from the cells a formula uses; **Trace Dependents** draws arrows to the formulas that use the selected cell; **Remove Arrows** clears them. **Evaluate Formula** steps through a formula one calculation at a time, which is the best way to find where a long formula goes wrong.
- **Google Sheets** has no tracing arrows. Click into a formula and each referenced range is outlined in color on the sheet; press **Ctrl+\`** to show all formulas at once.

> **Watch out: calculation set to Manual.** If Excel stops updating results when you change inputs, someone has switched **Formulas → Calculation → Calculation Options** to **Manual** (it's a workbook setting that can travel with a file you open). Set it back to **Automatic**, or press **F9** to recalculate. A report printed while calculation was manual can show stale numbers.

### Referring to another sheet

To use a cell on another sheet, type `=` and click across to that sheet, or type the sheet name followed by `!`: `=Targets!B2` returns January's target, 300,000. Sheet names with spaces need quotes: `='Cell detective'!A2`. The references update if the sheet is renamed.

> **Spreadsheet link.** You'll meet the same idea in SQL (Chapter 12) and Python (Chapter 18), but there the formula is written once for a whole column instead of copied row by row. That's one reason large datasets move to those tools.

---

## 10.7 Essential functions

A **function** is a named calculation that takes **arguments** inside brackets, separated by commas: `=SUM(J2:J331)`. Start typing `=SU` and both apps suggest matching functions and show the arguments as you type. Everything in this section works identically in Excel and Google Sheets unless a note says otherwise.

> **Tool note: argument separators.** Some regional settings (much of Europe, for example) use semicolons: `=SUM(J2;J331)`. Indian and United States settings use commas, as this book does.

### Totals and averages: SUM, AVERAGE, MIN, MAX, ROUND

```excel
=SUM(Data!J2:J331)          → 4398121
=AVERAGE(Data!J2:J331)      → 13327.6393939394
=MIN(Data!J2:J331)          → 546.25
=MAX(Data!J2:J331)          → 56700
=ROUND(Data!J5,0)           → 32063
```

The export totals ₹4,398,121. But Chapter 13 reported Riverstone's 2025 net revenue as **₹4,335,471**, and it was right. The difference is **₹62,650**: the lines of the two **cancelled** orders, 10034 and 10131, which `SUM` happily included. You'll fix that with `SUMIFS` in a moment.

The **median** is the middle value when the numbers are sorted, so a few very large lines don't pull it up the way they pull up the average:

```excel
=MEDIAN(Data!J2:J331)     → 10212.5
```

Half the order lines are worth ₹10,212.50 or less, while the average is ₹13,327.64. When an average and a median are far apart, a few big values are doing the work. Chapter 21 explains which average to report, and why the choice depends on the level of measurement from Chapter 1.

`ROUND(value, digits)` changes the stored value, unlike a number format. `ROUND(32062.5, 0)` gives 32063. Its relatives round in one direction: `=ROUNDUP(Data!J5,-2)` gives **32100** and `=ROUNDDOWN(Data!J5,-2)` gives **32000** (a negative number of digits rounds to tens, hundreds, and so on), and `=INT(Data!J5)` drops the decimals to give **32062**. Use `ROUND` when a rounded number feeds further calculations (for example, invoice amounts to the paisa: `ROUND(x, 2)`); use a number format when you only want a tidy display.

### Counting: COUNT, COUNTA, COUNTBLANK

```excel
=COUNT(Data!A2:A331)          → 330
=COUNTA(Data!I2:I331)         → 311
=COUNTBLANK(Data!I2:I331)     → 19
```

- `COUNT` counts cells that hold **numbers** (including dates). 330 order-line IDs.
- `COUNTA` counts **non-empty** cells of any type. 311 lines have a sales rep.
- `COUNTBLANK` counts empty cells. 19 lines have no sales rep. 311 + 19 = 330. ✓

That gap is worth a question to the sales team later: which orders came in without a rep, and who gets credit for them?

### Decisions: IF, IFS, AND, OR, IFERROR

`IF(test, value_if_true, value_if_false)` returns one of two results:

```excel
=IF(Data!J5>=50000,"Big","Normal")     → Normal
```

A **test** (also called a **condition**) is anything that is TRUE or FALSE: `J5>=50000`, `H5="Delivered"`, `G5>0`. The comparison operators are `=` `<>` (not equal) `>` `<` `>=` `<=`. Text in a formula goes inside double quotes.

For more than two outcomes, `IFS` checks conditions in order and returns the result for the first one that's TRUE (Excel 2019 or later, and Google Sheets):

```excel
=IFS(Data!J5>=50000,"Large",Data!J5>=10000,"Medium",TRUE,"Small")     → Medium
```

The final `TRUE,"Small"` is the catch-all, like `ELSE` in SQL's `CASE` (Chapter 12). In older Excel versions you'd nest `IF`s instead: `=IF(J5>=50000,"Large",IF(J5>=10000,"Medium","Small"))`.

`AND` is TRUE only when every test is TRUE; `OR` is TRUE when at least one is:

```excel
=AND(Data!H5="Delivered",Data!G5>0)     → TRUE
=OR(Data!G2>=10,Data!E2>=50)            → FALSE
```

Row 5 was delivered *and* discounted. Row 2 had neither a discount of 10% or more nor a quantity of 50 or more.

`IFERROR(value, value_if_error)` replaces an error with something readable:

```excel
=IFERROR(1/0,"n/a")     → n/a
```

> **Watch out: IFERROR hides problems too.** Wrapping every formula in `IFERROR(…,0)` turns real mistakes (a misspelled sheet name, a broken lookup) into zeros that look like real results. Use it where you expect a specific, harmless error, and prefer a visible label such as `"not found"` over 0.

### Counting and adding with conditions: COUNTIF(S), SUMIF(S), AVERAGEIF(S)

These are the workhorse functions of business spreadsheets. The **S** versions take one or more pairs of *range, criterion*:

```excel
=COUNTIF(Data!G2:G331,">0")                                   → 186
=COUNTIFS(Data!H2:H331,"Delivered",Data!G2:G331,">0")          → 185
=SUMIFS(Data!J2:J331,Data!H2:H331,"<>Cancelled")               → 4335471
=AVERAGEIFS(Data!J2:J331,Data!H2:H331,"<>Cancelled")           → 13298.990797546
```

How it works:

- `COUNTIF(range, criterion)` counts cells in one range that meet one criterion. 186 lines had a discount.
- `COUNTIFS` takes several pairs and counts rows where **all** of them are true. 185 lines were delivered *and* discounted.
- `SUMIFS(sum_range, criteria_range1, criterion1, …)` adds up the first range on the rows where every criterion holds. The **sum range comes first** in `SUMIFS`. `"<>Cancelled"` means "not equal to Cancelled", so the total is **₹4,335,471**, matching Chapter 13. ✓
- `AVERAGEIFS` averages the non-cancelled lines: ₹13,298.99 per line.
- `MAXIFS` and `MINIFS` (Excel 2019 or later, and Sheets) return the largest or smallest value that meets the criteria: `=MAXIFS(Data!J2:J331,Data!N2:N331,"Retail",Data!H2:H331,"<>Cancelled")` returns **49875**, the biggest Retail line (column N holds the segment you'll add in section 10.9).

Criteria are written as text: `">0"`, `"Delivered"`, `"<>Cancelled"`. To compare with a cell's value, join the operator to the cell with `&`:

```excel
=SUMIFS(Data!J2:J331,Data!B2:B331,">="&DATE(2025,11,1),Data!B2:B331,"<="&DATE(2025,11,30),Data!H2:H331,"<>Cancelled")     → 633408
```

November's net revenue was **₹633,408**: every non-cancelled line dated on or after 1 November and on or before 30 November. The same date range can appear in two criteria, one for each end.

Two more criterion tricks:

- **Wildcards**: `*` matches any run of characters and `?` any single character. `=COUNTIF(Customers!B2:B25,"*Hotel*")` counts 2 customers with "Hotel" in the name.
- **Blank**: `""` matches empty cells. `=SUMIFS(Data!J2:J331,Data!I2:I331,"",Data!H2:H331,"<>Cancelled")` returns 204502.5, the revenue from lines with no sales rep.

> **Watch out: the row ranges must line up.** Every range in a `SUMIFS` must be the same size and start on the same row: `J2:J331` with `H2:H331`, not `H1:H330`. Excel returns `#VALUE!` for different sizes, but ranges of the same size that are offset by one row give a wrong answer with no error at all.

> **SQL link.** `SUMIFS(J, H, "<>Cancelled")` is the spreadsheet version of `SELECT SUM(net_revenue) FROM … WHERE status <> 'Cancelled'`. When you build a table of `SUMIFS` with one row per month, you're doing by hand what `GROUP BY` does in one line (section 12.9).

### A reconciliation habit

Whenever you break a total into parts, add the parts back up and compare. The sales reps' non-cancelled revenue, from four `SUMIFS` (three names and the blank):

| Sales rep | Net revenue (₹) |
|---|---|
| Rahul Mehta | 1,494,000.50 |
| Farah Khan | 1,489,073.00 |
| Neha Kulkarni | 1,147,895.00 |
| (no rep) | 204,502.50 |
| **Total** | **4,335,471.00** |

The four parts add to exactly the non-cancelled total. ✓ If they didn't, a name would be misspelled somewhere (`Farah  Khan` with two spaces is a different criterion), or a line would have a rep who isn't on your list.

> **Interview extra point.** When an interviewer hands you a spreadsheet task, finish by reconciling out loud: *"The segment totals add to ₹4,335,471, which matches the non-cancelled total, and I excluded the two cancelled orders worth ₹62,650."* Checking your own work unprompted is one of the moves Chapter 69 teaches, and Chapter 70 has spreadsheet questions that reward it.

---

## 10.8 Text and date functions

Real data arrives with codes that need padding, names in the wrong case, and dates stored as text. These functions fix them. They work the same in both apps.

### Text functions

| Function | Example | Result | What it does |
|---|---|---|---|
| `LEN` | `=LEN("2900 ")` | 5 | Counts characters, spaces included |
| `TRIM` | `=VALUE(TRIM('Cell detective'!A4))` | 2900 | Removes extra spaces; `VALUE` then turns the text into a number |
| `UPPER`, `LOWER`, `PROPER` | `=PROPER("METRO MART")` | Metro Mart | Change case |
| `LEFT`, `RIGHT` | `=LEFT("0005",2)` | 00 | First or last *n* characters |
| `MID` | `=MID("RS-2025-0418",4,4)` | 2025 | *n* characters starting at a position |
| `SUBSTITUTE` | `=SUBSTITUTE("Storage Box 10L","Box","Bin")` | Storage Bin 10L | Replace text |
| `TEXT` | `=TEXT(5,"0000")` | 0005 | Turn a number into formatted **text** |
| `FIND` | `=FIND(" ","Neha Kulkarni")` | 5 | Position of one text inside another (`SEARCH` ignores case) |
| `&`, `CONCAT` | `=Customers!B3&" ("&Customers!A3&")"` | Patel Kitchenware (0002) | Join text; `=CONCAT("RS-",Data!A2)` gives RS-10001 |

`TEXT` is the one to remember from this table. It takes a number and a format code (the same codes as section 10.5) and returns text:

```excel
=TEXT(5,"0000")               → 0005
=TEXT(Data!B2,"mmm yyyy")     → Jan 2025
```

That's how you repair customer codes that lost their zeros on import (section 10.4): in a new column, `=TEXT(C2,"0000")`, then copy the column and paste it back **as values** (**Excel: Home → Paste → Paste Values**, or **Ctrl+Alt+V**, then **V**; **Sheets: Edit → Paste special → Values only**, or **Ctrl+Shift+V**).

To join many values with a separator, `TEXTJOIN(", ",TRUE,range)` (Excel 2019 or later, and Sheets) skips blanks when its second argument is `TRUE`. Chapter 14 goes much further with messy text.

> **Watch out: text results can't be summed.** `TEXT(J2,"#,##0")` looks like a number but is text, and `SUM` skips it (section 10.3). Format numbers for *display* with number formats; use `TEXT` only when you're building a label or a code.

### Date functions

| Function | Example | Result | What it does |
|---|---|---|---|
| `DATE` | `=DATE(2025,11,1)` | 2025-11-01 | Builds a date from year, month, day |
| `YEAR`, `MONTH`, `DAY` | `=MONTH(Data!B2)` | 1 | Takes a date apart |
| `EOMONTH` | `=EOMONTH(Data!B4,0)` | 2025-01-31 | End of the month, *n* months away |
| `WEEKDAY` | `=WEEKDAY(Data!B2,2)` | 4 | Day of week; type 2 means Monday = 1, so 4 is Thursday |
| `NETWORKDAYS` | `=NETWORKDAYS(DATE(2025,12,1),DATE(2025,12,31))` | 23 | Working days (Monday to Friday) between two dates, inclusive |
| `TODAY` | `=TODAY()` | today's date | Changes every day the file is opened |

A common need is a **month key**, a single value that says which month a row belongs to. Type `month_start` in `K1` and in `K2`:

```excel
=DATE(YEAR(B2),MONTH(B2),1)
```

Every January order gets 2025-01-01, every February order 2025-02-01, and so on. Month keys like this are what the monthly tracker in this chapter's project groups by.

`NETWORKDAYS` has an optional third argument, a range of holiday dates to exclude. Riverstone would list its declared holidays on a sheet and use `=NETWORKDAYS(start,end,Holidays!A2:A20)`.

> **Watch out: TODAY() makes reports drift.** A formula such as `=TODAY()-B2` for "days since order" gives a different answer every day, which is what you want in a live receivables report and a problem in a report someone will check next week. This chapter's examples use fixed dates (Riverstone's "today" for 2025 data is 31 December 2025), and a live report would use `TODAY()`. When you send a report, write the as-of date on it.

### Rescuing dates stored as text

When a date column arrives as text (`13-01-2025`), build a real date from its pieces:

```excel
=DATE(RIGHT(B2,4),MID(B2,4,2),LEFT(B2,2))
```

`RIGHT(B2,4)` takes the year, `MID(B2,4,2)` the month, and `LEFT(B2,2)` the day. `DATE` accepts those text pieces and returns a real date, 2025-01-13. This only works when every text date has the same pattern; Chapter 14 handles columns with mixed patterns.

> **Try it.** Type `13-01-2025` into a cell formatted as Plain text or Text, and put the formula above next to it (pointing at that cell). Check the result with `=ISNUMBER()`: it should say TRUE.

---

## 10.9 A first lookup: fetching values from another sheet

The export has `customer_code` but not the customer's name or segment. Those live on the **Customers** sheet. A **lookup** finds a value in one list and returns the matching value from another column, one row at a time. Chapter 11 covers lookups in depth; this section gives you the one you'll use most.

*"Which customer placed each order line?"* Type `customer_name` in `M1` and, in `M2`:

```excel
=XLOOKUP(C2,Customers!$A$2:$A$25,Customers!$B$2:$B$25,"not found")
```

Row 2 shows **Patel Kitchenware**. Fill it down. In `N2`, fetch the segment the same way from column D:

```excel
=XLOOKUP(C2,Customers!$A$2:$A$25,Customers!$D$2:$D$25,"not found")
```

How it works:

- **Argument 1**, `C2`: what to look for (this line's customer code, `0002`).
- **Argument 2**, `Customers!$A$2:$A$25`: where to look for it (the list of codes).
- **Argument 3**, `Customers!$B$2:$B$25`: what to return from the same position (the names).
- **Argument 4**, `"not found"`: what to show if the code isn't in the list. Without it, a missing code shows `#N/A`.
- The ranges are **absolute** so they stay on rows 2 to 25 as the formula is copied down 330 rows (section 10.6).

`XLOOKUP` looks for an **exact match** by default. It's available in Microsoft 365, Excel 2021 and later, Excel for the web, and Google Sheets. With older Excel, use `INDEX` and `MATCH`, which give the same result:

```excel
=IFERROR(INDEX(Customers!$B$2:$B$25,MATCH(C2,Customers!$A$2:$A$25,0)),"not found")
```

Chapter 11 explains how `INDEX` and `MATCH` work. You'll also see an older function, `VLOOKUP`, in inherited workbooks: `=VLOOKUP(C2,Customers!$A$2:$D$25,2,FALSE)` returns the second column of the block. Its last argument must be `FALSE` for an exact match; leaving it out gives approximate matches and wrong names. Recognize it, and prefer `XLOOKUP` in new work.

### Why the import in section 10.4 mattered

Try the lookup against the number 5 instead of the text `0005`:

```excel
=IFERROR(INDEX(Customers!B2:B25,MATCH("0005",Customers!A2:A25,0)),"not found")     → Metro Mart
=IFERROR(INDEX(Customers!B2:B25,MATCH(5,Customers!A2:A25,0)),"not found")          → not found
```

A lookup matches on the stored value *and its type*. The number 5 and the text `0005` are different values. If the codes lost their zeros on import, every one of the 330 lookups says "not found", and any report by customer or segment comes out empty.

Once the segment column is filled, `SUMIFS` can use it. Non-cancelled net revenue by segment:

| Segment | Orders | Net revenue (₹) | Share |
|---|---|---|---|
| Wholesale | 55 | 1,702,658.50 | 39.3% |
| Retail | 59 | 1,488,773.75 | 34.3% |
| Hospitality | 59 | 1,144,038.75 | 26.4% |
| **Total** | **173** | **4,335,471.00** | **100.0%** |

Wholesale brought in the most revenue from the fewest orders: its orders are bigger. The three segments add back to the total. ✓

> **SQL link.** A lookup is a join done one cell at a time. In Chapter 12 you'll write `JOIN customers ON …` and fetch every name in one statement, and in Chapter 18 you'll do it in Python with `pandas.merge`.

---

## 10.10 Sorting, filtering, and tables

### Freeze the header row first

With 330 rows, the headers scroll out of sight. **Excel: View → Freeze Panes → Freeze Top Row. Sheets: View → Freeze → 1 row.** Row 1 now stays visible.

### Sorting

*"Which order lines were the biggest?"* Click any cell in the `net_revenue` column, then:

- **Excel: Data → Sort & Filter → Sort Z to A** (or **Home → Sort & Filter → Sort Largest to Smallest**).
- **Sheets: Data → Sort sheet → Sort sheet (Z to A)** for the whole sheet, or select the data and use **Data → Sort range → Advanced range sorting options**, with **Data has header row** ticked.

The top three lines are all Industrial Crates:

| order_id | Customer | Quantity | Discount | Net revenue (₹) |
|---|---|---|---|---|
| 10107 | Deccan Packaging | 45 | 10% | 56,700 |
| 10126 | Harbour Traders | 40 | 8% | 51,520 |
| 10162 | Northgate Distributors | 40 | 8% | 51,520 |

For a sort on several columns (for example, by `sales_rep`, then by `net_revenue` largest first), use **Excel: Data → Sort** and **Add Level**; in **Sheets: Data → Sort range → Advanced range sorting options → Add another sort column**.

> **Watch out: sort the whole table, not one column.** If you select only the `net_revenue` column and sort it, the amounts move and the rest of each row stays put, so every amount ends up next to the wrong order. Excel warns you with a *Sort Warning* dialog (choose **Expand the selection**); Google Sheets sorts only what you selected. Click one cell inside the data, not a whole column, and let the app find the table's edges. If it goes wrong, undo immediately with **Ctrl+Z**.

### Filtering

A **filter** hides the rows that don't match a condition, without deleting anything.

- **Excel: Data → Sort & Filter → Filter** (**Ctrl+Shift+L**). Arrows appear in the header row.
- **Sheets: Data → Create a filter.** Filter icons appear in the header row.

*"Show November's wholesale orders."* Filter `segment` to **Wholesale**, then filter `order_date` to November 2025 (**Excel:** in the date list, expand 2025 and tick only November; **Sheets:** **Filter by condition → Date is between**, 2025-11-01 and 2025-11-30). 15 lines remain.

Now watch what totals do. A plain `=SUM(J2:J331)` still says 4,398,121, because `SUM` includes hidden rows. `SUBTOTAL` with function number 109 adds **visible rows only**:

```excel
=SUBTOTAL(109,J2:J331)
```

With the November wholesale filter on, it returns **343,685.5**, the same as the matching `SUMIFS`. Clear the filter and it returns the full total again. `SUBTOTAL` works the same way in both apps.

> **Tool note: filters on shared files.** In Google Sheets, a normal filter changes the view for **everyone** who has the file open. Use **Data → Filter views → Create new filter view** to filter only your own view, and name it so colleagues can reuse it. Excel offers **View → Sheet View → New** for the same purpose when the workbook is stored on OneDrive or SharePoint.

### Removing duplicates

*"How many different orders are in the export?"* Copy the `order_id` column (`A1:A331`) to a blank sheet, then:

- **Excel: Data → Data Tools → Remove Duplicates**, tick **My data has headers**, and click **OK**. Excel reports how many duplicate values it removed and how many unique values remain.
- **Google Sheets: Data → Data cleanup → Remove duplicates**, tick **Data has header row**, and click **Remove duplicates**.

175 unique order IDs remain: the number of orders, as opposed to 330 order lines. ✓

> **Watch out: remove duplicates deletes rows for good.** It keeps the first row of each duplicate group and deletes the others, including anything else on those rows. Run it on a copy, as here, and decide first which columns define a duplicate. Chapter 14 covers near-duplicates such as `Metro Mart` and `METRO MART`, which this tool doesn't catch.

### Grouping and hiding detail

To collapse detail rows or columns under a clickable **+/−**, select them and use **Excel: Data → Outline → Group** or **Sheets: right-click → View more row actions → Group rows** (or **View → Group**). It's a tidier alternative to hiding, because readers can see that something is collapsed.

### Tables

A **table** turns a plain range into a named, structured object: it keeps its header row, applies banded formatting, adds filter buttons, and **grows automatically** when you add rows. Formulas can refer to its columns by name.

| | Excel | Google Sheets |
|---|---|---|
| Create | Click in the data, **Insert → Table** (**Ctrl+T**), tick **My table has headers** | Select the data, **Format → Convert to table** (**Ctrl+Alt+T**) |
| Rename | **Table Design → Table Name** | Click the table name above the table |
| Column types | Not part of the table; set number formats | Choose a type per column (Number, Date, Text, Dropdown, and more) |
| Totals | **Table Design → Total Row** (uses `SUBTOTAL`, so it respects filters) | No built-in total row; add `SUBTOTAL` formulas below or beside the table |
| Refer to a column | `=SUM(Sales[net_revenue])` | `=SUM(Sales[net_revenue])` |

Convert the Data sheet's range to a table and name it `Sales`. Then:

```excel
=SUM(Sales[net_revenue])     → 4398121
```

A **table reference** such as `Sales[net_revenue]` is easier to read than `J2:J331`, and it doesn't break when next month's rows are added below: the table expands and every formula that uses it includes the new rows. Inside the table, Excel writes a calculated column as `=[@quantity]*[@unit_price]*(1-[@discount_pct]/100)`, where `@` means "this row", and fills it down for you.

> **Tool note.** Tables arrived in Google Sheets in 2024 and are still gaining features; if your menus look different, search Google's help for "use tables in Google Sheets". Table references are also usable in Sheets formulas. This book's workbooks use plain ranges wherever a formula has to work in both apps and in older Excel versions.

---

## 10.11 Data validation and conditional formatting

### Data validation: stop bad data at the door

**Data validation** limits what can be typed into a cell. It's the cheapest data-quality control there is (Chapter 1, section 1.10): an error prevented at entry never reaches a report.

*"Only allow the four real order statuses."* Select `H2:H331`, then:

- **Excel: Data → Data Tools → Data Validation → Settings → Allow: List**, and in **Source** type `Delivered,Shipped,Pending,Cancelled`. On the **Error Alert** tab keep **Style: Stop**.
- **Sheets: Data → Data validation → Add rule → Criteria: Dropdown**, add the four options, and under **Advanced options** choose **Reject the input**.

Each cell now has a drop-down, and typing `Deliverd` is refused.

*"Quantity must be a whole number from 1 to 1,000."*

- **Excel: Data Validation → Allow: Whole number → between 1 and 1000.** Add a message on the **Input Message** tab, such as "Units, not cartons".
- **Sheets: Add rule → Criteria: Is between → 1 and 1000**, and **Reject the input**. (Sheets' "is between" allows decimals; to require whole numbers use **Custom formula is** `=AND(E2>=1,E2<=1000,INT(E2)=E2)`.)

Type `0` into a quantity cell and both apps refuse it. The current data passes: quantities run from 5 to 85.

> **Watch out: validation doesn't check what's already there, or what's pasted.** Rules apply when someone types into a cell. Values that were in the cells before the rule, and values pasted over the cells, can slip through. To find existing violations in Excel, use **Data → Data Validation → Circle Invalid Data**; in Sheets, invalid cells show a red corner marker. Chapter 14 builds proper validation checks.

A drop-down can also read its options from a range, such as the names on the Customers sheet (**Excel: Source** `=Customers!$B$2:$B$25`; **Sheets: Dropdown (from a range)**). Then updating the list updates every drop-down.

### Conditional formatting: make the important cells stand out

**Conditional formatting** changes a cell's appearance when its value meets a rule. The value itself doesn't change.

*"Highlight order lines worth ₹50,000 or more."* Select `J2:J331`, then:

- **Excel: Home → Styles → Conditional Formatting → New Rule → Format only cells that contain**, then **Cell Value → greater than or equal to → 50000**, and choose a fill with **Format…**.
- **Sheets: Format → Conditional formatting → Format cells if… → Greater than or equal to → 50000**, and choose a fill.

Three cells light up, the same three lines as the sort showed.

*"Shade every cancelled order's whole row."* This needs a **formula rule**, which is TRUE or FALSE for each row. Select `A2:N331` (the whole table, starting at row 2), then:

- **Excel: Conditional Formatting → New Rule → Use a formula to determine which cells to format**, formula `=$H2="Cancelled"`.
- **Sheets: Format → Conditional formatting → Format cells if… → Custom formula is**, formula `=$H2="Cancelled"`.

Four rows turn grey: one line of order 10034 and three lines of order 10131.

How it works: the formula is written for the top-left cell of the selection (`A2`) and applied to every other cell as if copied. `$H` is absolute, so every cell in a row checks that row's column H; `2` is relative, so each row checks its own row. It's the mixed reference from section 10.6 doing real work.

Other rule types worth knowing: **data bars** and **color scales** (Excel: **Conditional Formatting → Data Bars / Color Scales**; Sheets: **Color scale** tab) for a quick visual of size, **duplicate values** (Excel: **Highlight Cells Rules → Duplicate Values**; Sheets: custom formula `=COUNTIF($A:$A,$A2)>1`), and **dates** ("in the last 7 days").

> **Watch out: color is not the message.** Some readers can't tell red from green, and colors disappear when a report is printed in black and white. Pair color with something readable, such as a status column that says "Below target". Chapter 15 covers color in charts and reports.

---

## 10.12 Charts

A chart shows the shape of numbers faster than a table does. Chapter 15 teaches how to choose and design charts properly; this section covers building one in each app.

*"How did monthly revenue compare with target in 2025?"* Put the monthly figures in a small summary table (you'll build it with `SUMIFS` in the project; the numbers are in Figure 10.5), then select the `month`, `target`, and `net_revenue` columns.

- **Excel: Insert → Charts → Recommended Charts → All Charts → Combo.** Set `net_revenue` to **Clustered Column** and `target` to **Line**, then **OK**.
- **Sheets: Insert → Chart.** In the **Chart editor**, under **Setup → Chart type**, choose **Combo chart**. Check that `net_revenue` is drawn as columns and `target` as a line (**Customize → Series**).

Then finish it:

1. **Write a title that states the finding**, not the topic. Instead of "Revenue vs target 2025", write "Riverstone beat its monthly target in six of the last eight months of 2025". Excel: click the title and type. Sheets: **Customize → Chart & axis titles**.
2. **Label the axis units**: "Net revenue (₹)".
3. **Remove clutter**: heavy gridlines, 3-D effects, and a legend you don't need.
4. **Start the value axis at zero** for column charts, so a small difference doesn't look huge.

The chart shows a weak first half (₹1,460,880 against a target of ₹1,860,000, or 78.5%) and a strong second half (₹2,874,591 against ₹2,380,000, or 120.8%), with the peak in October.

| Chart | Use it when the question is… | Riverstone example |
|---|---|---|
| Column or bar | How do categories compare? | Revenue by segment |
| Line | How did something change over time? | Revenue by month |
| Combo (column + line) | How does an actual compare with a target? | Revenue vs target |
| Scatter | Do two measures move together? | Quantity vs discount per line |
| Pie | What share does each part take, with very few parts? | Rarely; a bar chart is usually clearer |

> **Tool note: charts that update.** A chart based on a range updates when the numbers in that range change. If the chart's range is an Excel table or a whole-column summary that grows, new months appear automatically. If it points at a fixed range such as `A5:D16`, a thirteenth month won't appear until you edit the range.

---

## 10.13 Working together: sharing, protection, and version history

Spreadsheets are team tools. This is where Google Sheets was built to be strong, and where Excel has caught up for files stored in the cloud.

### Sharing and permissions

**Google Sheets.** Click **Share** (top right). Add people by email and choose a role:

- **Viewer** can see the file.
- **Commenter** can see it and add comments.
- **Editor** can change anything, including sharing it further (unless you turn that off).

Under **General access**, choose **Restricted** (only people you added) or **Anyone with the link**. The settings gear in the Share dialog lets you stop editors from changing permissions and stop viewers from downloading, printing, or copying.

**Excel.** Save the workbook to **OneDrive** or **SharePoint**, then click **Share** and choose **Can edit** or **Can view** for the people or link. Files stored only on your own computer can't be edited by several people at once.

> **Watch out: "Anyone with the link" means anyone.** A link forwarded once is out of your control. For anything with customer names, prices, salaries, or personal data (Chapter 2, section 2.9), share with named people only, and review access when someone changes role.

### Editing at the same time

Both apps support **co-authoring**: several people editing at once, with each person's cursor shown in a different color. In Sheets this always happens. In Excel it works in Excel for the web and in the desktop app when **AutoSave** (top left) is on for a file on OneDrive or SharePoint.

Use **comments** for questions rather than typing notes into cells. **Excel: Review → New Comment. Sheets: Insert → Comment.** In both, typing `@` and a name in a comment notifies that person.

### Protecting formulas

When others will type into a workbook, protect the parts they shouldn't change.

- **Excel:** select the input cells, open **Format Cells** (**Ctrl+1**) **→ Protection** and clear **Locked**. Then **Review → Protect Sheet**. Locked cells (everything else) can no longer be edited.
- **Sheets: Data → Protect sheets and ranges → Add a sheet or range**, then **Set permissions** to restrict who can edit, or choose **Show a warning when editing this range** for a gentler reminder.

> **Simplification note.** Sheet protection prevents accidents, not determined people. An Excel sheet password is not strong security, and anyone who can open a file can copy its data. Keep confidential data out of widely shared files instead of relying on protection.

### Version history

Mistakes happen: a column deleted, a formula overwritten. Version history lets you see and restore earlier versions.

- **Sheets: File → Version history → See version history** (**Ctrl+Alt+Shift+H**). Each version shows who changed what, highlighted. Click **Restore this version** to go back, or **File → Version history → Name current version** to mark a milestone such as "March close, sent to CEO". Right-click a single cell and choose **Show edit history** to see that cell's changes.
- **Excel:** for files on OneDrive or SharePoint, **File → Info → Version History**. Open an earlier version to compare, then **Restore** it.

Version history replaces the old habit of saving `Sales_Report_final_v3_REALLY_FINAL.xlsx` (Chapter 2). For SQL queries and code, Git does the same job more precisely (Chapter 26).

### Google Forms feeding a sheet

A **Google Form** is a web form whose answers can land in a Google Sheet as rows, one per submission, with a timestamp. It's a common, free way to collect structured data without anyone retyping it.

*"Let branch staff log customer enquiries in a consistent format."*

1. Go to **forms.google.com** and create a form with questions such as *Company name* (short answer), *City* (short answer), *Product interest* (dropdown: Storage, Kitchen, Industrial, Furniture), and *Expected quantity* (short answer with **Response validation → Number → Whole number**).
2. In the form, open the **Responses** tab and click **Link to Sheets**, then **Create a new spreadsheet**. (From a sheet, **Tools → Create a new form** does the reverse.)
3. Each submission appears as a new row in the linked sheet's responses tab, with a **Timestamp** column first.

The form does the validation for you: dropdowns keep categories consistent, and number rules stop "about fifty". Chapter 19 goes one step further with Google Apps Script, sending each enquirer an acknowledgement email automatically.

> **Watch out: don't edit the responses sheet.** Inserting columns, sorting, or typing inside the responses tab can misalign future submissions. Build your analysis on a separate sheet that refers to the responses, for example with `=COUNTIF('Form Responses 1'!D:D,"Industrial")`. Microsoft Forms offers a similar link to Excel for work and school accounts.

---

## 10.14 Moving between apps, printing, and saving as PDF

You'll often receive an Excel file and want it in Sheets, or build in Sheets and send an Excel file to finance.

**Excel to Sheets.** Upload the `.xlsx` to Google Drive and open it. Sheets can edit it in place as an Excel file (a green `.XLSX` label appears next to the name), or you can convert it with **File → Save as Google Sheets** to get every Sheets feature.

**Sheets to Excel.** **File → Download → Microsoft Excel (.xlsx).**

What survives the trip:

| Feature | Excel → Sheets | Sheets → Excel |
|---|---|---|
| Values, number formats, most formulas (`SUMIFS`, `XLOOKUP`, `TEXT`, dates) | Yes | Yes |
| Conditional formatting and data validation | Mostly | Mostly |
| Charts | Usually, with some styling changes | Usually, with some styling changes |
| Excel tables | Usually kept as formatted ranges; check the result | Sheets tables arrive as formatted ranges; check the result |
| Pivot tables (Chapter 11) | Usually converted; check the result | Usually converted; check the result |
| App-only functions: `QUERY`, `IMPORTRANGE`, `GOOGLEFINANCE` (Sheets); Power Query, Power Pivot (Excel) | Excel-only features don't run | Sheets-only functions become fixed values or errors |
| Macros: VBA (Excel), Apps Script (Sheets) (Chapter 19) | VBA doesn't run in Sheets | Apps Script isn't exported |
| Comments and version history | Comments yes; history no | Comments yes; history no |

**CSV is the lowest common denominator.** Saving as CSV (**Excel: File → Save As → CSV UTF-8**; **Sheets: File → Download → Comma-separated values**) keeps **one sheet**, **values only**: no formulas, formatting, or other sheets. Choose **CSV UTF-8** in Excel so names in Hindi, Tamil, or with accents survive (Chapter 2, section 2.1).

> **Try it.** Download your finished tracker from Sheets as `.xlsx` and open it in Excel (or the reverse). Run the check from the project: the tracker total and the data total should still match, with a difference of 0. If a total changed, a function didn't survive.

**Portable habits** when a file will live in both apps: use functions both apps share, keep one table per sheet with one header row, avoid merged cells, write dates as real dates in `yyyy-mm-dd` format, and put a note on the first sheet saying which app the file was built in.

### Printing and saving as PDF

Many reports still end up printed or sent as a PDF. Set them up so every page is readable.

| To do this | Excel | Google Sheets |
|---|---|---|
| Preview and print | **File → Print** (**Ctrl+P**) | **File → Print** (**Ctrl+P**) |
| Print only part of a sheet | Select it, **Page Layout → Print Area → Set Print Area** | Select it, then in print settings choose **Print: Selected cells** |
| Fit all columns on one page | **File → Print → Scaling → Fit All Columns on One Page** | **Scale → Fit to width** |
| Landscape | **Page Layout → Orientation → Landscape** | **Page orientation → Landscape** |
| Repeat the header row on every page | **Page Layout → Print Titles → Rows to repeat at top**: `$1:$1` | Freeze row 1, then **Headers & footers → Repeat frozen rows** |
| Page numbers and a title | **Insert → Header & Footer** | **Headers & footers → Page numbers**, **Workbook title** |
| Save as PDF | **File → Export → Create PDF/XPS**, or **File → Save As → PDF** | **File → Download → PDF** (choose sheet or workbook, then the print settings) |

> **Try it.** Print-preview the Data sheet with no settings: 330 rows and 14 columns split across many pages, most without headers. Then set landscape, fit all columns to one page, and repeat row 1. The preview becomes readable pages, each with its header row.

---

## 10.15 Keyboard shortcuts for both apps

Shortcuts save hours over a year. Learn five at a time. In Google Sheets on a Mac, use **Cmd** where the table says **Ctrl** unless noted. Press **Ctrl+/** in Sheets to see its full list; in Excel, press **Alt** to see ribbon key tips.

| Action | Excel (Windows) | Excel (Mac) | Google Sheets |
|---|---|---|---|
| Edit the active cell | F2 | Ctrl+U | F2 or Enter |
| Cycle `$` in a reference | F4 | Cmd+T | F4 |
| Show formulas / results | Ctrl+\` | Ctrl+\` | Ctrl+\` |
| Save | Ctrl+S | Cmd+S | Saves automatically |
| AutoSum | Alt+= | Cmd+Shift+T | Σ toolbar button |
| Insert / delete row or column | Ctrl+Shift+= / Ctrl+- | Ctrl+Shift+= / Cmd+- | Right-click menu |
| Fill down | Ctrl+D | Cmd+D | Ctrl+D |
| Jump to edge of data | Ctrl+Arrow | Cmd+Arrow | Ctrl+Arrow |
| Select to edge of data | Ctrl+Shift+Arrow | Cmd+Shift+Arrow | Ctrl+Shift+Arrow |
| Format cells | Ctrl+1 | Cmd+1 | Format menu |
| Insert today's date | Ctrl+; | Ctrl+; | Ctrl+; |
| Paste values only | Ctrl+Alt+V, then V | Ctrl+Cmd+V | Ctrl+Shift+V |
| Create a table | Ctrl+T | Ctrl+T | Ctrl+Alt+T |
| Turn filter on or off | Ctrl+Shift+L | Cmd+Shift+F | Data → Create a filter |
| Find | Ctrl+F | Cmd+F | Ctrl+F |
| Find and replace | Ctrl+H | Ctrl+H | Ctrl+H (Mac: Cmd+Shift+H) |
| Flash Fill / Smart Fill | Ctrl+E | Ctrl+E | Ctrl+Shift+Y |
| Recalculate now | F9 | Cmd+= | Automatic |
| Undo / redo | Ctrl+Z / Ctrl+Y | Cmd+Z / Cmd+Y | Ctrl+Z / Ctrl+Y |
| Version history | File → Info → Version History | File → Browse Version History | Ctrl+Alt+Shift+H |

> **Tool note.** Shortcuts vary with keyboard layout, operating system version, and browser, and Mac laptops often need **Fn** for function keys. If a shortcut doesn't work, check the app's own shortcut list.

---

## Common mistakes

| Mistake | Symptom | Fix |
|---|---|---|
| Double-clicking a CSV to open it | Codes like `0002` show as `2`; some dates are wrong, others left-aligned as text | Import with column types set (section 10.4); check `COUNT` on the date column equals the row count |
| Trusting what a cell displays | A total is off by a little; `32,063` is really 32062.5 | Look at the formula bar; use `ROUND` when a rounded value must feed calculations |
| Numbers stored as text | `SUM` is too small; `COUNT` is less than `COUNTA`; green triangles in Excel | Convert with `VALUE`, `VALUE(TRIM())`, or Excel's **Convert to Number** |
| Forgetting `$` in a copied total | Shares add to far more than 100%; the last row shows 100% | Lock the range: `SUM($J$2:$J$331)`; press F4 |
| Adding every row, including cancelled orders | Your total doesn't match finance or the database | `SUMIFS(…, status, "<>Cancelled")`; ask what the report's rules are |
| Counting lines as orders | "330 orders" when the business received 175 | Know the grain; count first lines per order or unique order IDs |
| `SUMIFS` ranges that don't line up | No error, but numbers look slightly off | Make every range start and end on the same rows |
| Using a number format to "fix" codes | Lookups still return `#N/A` or "not found" | Create real text with `TEXT(C2,"0000")` and paste as values |
| Lookup without an exact match | `VLOOKUP` returns a plausible but wrong name | Use `XLOOKUP`, or `VLOOKUP(…, FALSE)` |
| `IFERROR(…,0)` everywhere | Broken formulas quietly show 0 | Catch only the error you expect, and show a visible label |
| Sorting one column instead of the table | Amounts sit next to the wrong orders | Click one cell in the data, not a column; undo at once if it goes wrong |
| Totals with `SUM` on a filtered list | The total ignores your filter | Use `SUBTOTAL(109, range)` or a table's total row |
| Deleting rows or cells a formula points at | `#REF!` appears in totals | Undo; point formulas at whole ranges or tables rather than single cells |
| Excel calculation left on Manual | Results don't change when inputs change | **Formulas → Calculation Options → Automatic**, or F9 |
| Remove Duplicates on the original data | Rows disappear, including their other columns | Work on a copy; decide which columns define a duplicate |
| Find and replace without Match entire cell | Unintended changes inside longer values and formulas | Select the range, tick **Match entire cell contents**, check the count |
| Printing without page setup | Columns split across pages, no headers after page 1 | Fit columns to one page, landscape, repeat header row |
| `TODAY()` in a report someone will check later | Numbers change between two people opening the file | Use a fixed as-of date cell and print it on the report |
| Merged cells and blank rows inside data | Sorting fails; filters stop halfway; tables break | One header row, no merges, no blank rows in data areas |
| Sharing with "Anyone with the link" | Confidential data ends up with people outside the company | Share with named people; review access regularly |
| Typing into a Google Forms responses sheet | New submissions land in the wrong columns | Analyze on a separate sheet that refers to the responses |

---

## In the real world: Meera's two Januaries

It was the second week of January 2026, and Riverstone's sales review was on Thursday. Vikram Singh, the Sales Manager, forwarded Meera Iyer a spreadsheet with one line: *"Anita says January 2025 was our worst month ever. Finance says it wasn't. Which is it?"*

The file was a monthly revenue tracker that a new trainee had put together from the ERP's 2025 export. Its January row said **₹91,649**. The finance team's figure for January 2025 was **₹202,640**. December looked odd too: ₹172,039 in the tracker, against the ₹439,824 Meera remembered from the year-end review.

Meera didn't start by rebuilding anything. She started by checking what the cells contained.

**Step 1: check the row count.** The export had 330 order lines, and `=COUNTA(A2:A331)` on the trainee's Data sheet also gave 330. No rows were missing, so the problem wasn't a failed download.

**Step 2: check the dates.** She typed `=COUNT(B2:B331)` next to the data. It returned **135**. If every date had been a real date, it would have said 330. So 195 "dates" were text. She clicked `B4`: it held the text `13-01-2025`, left-aligned. Then she clicked `B2`. It displayed a proper date, but the formula bar said **2025-02-01**, and the raw CSV in Notepad said `02-01-2025`: 2 January. The trainee's laptop was set to United States regional settings, so the app had read every date month first. Where that was impossible, it had given up and left text.

That explained both numbers at once. A month-first reading puts a line in "January" only if its real date fell on the 1st of some month, so the January row held seven lines really dated 1 June and 1 December, and none of January's own. And the tracker's total for the year, ₹1,739,092, was barely 40% of the real figure, because 195 lines had no usable date at all.

**Step 3: check the codes.** The trainee had added a customer name column with a lookup, and it said "not found" on every row. `=COUNTIF(M2:M331,"not found")` returned 330. The customer codes had become the numbers 2, 3, and 5, and the Customers sheet held the text `0002`, `0003`, `0005`.

**Step 4: fix at the source, not in the tracker.** Meera could have patched the damaged file with `DATE(RIGHT(),MID(),LEFT())` for the text dates and `TEXT(C2,"0000")` for the codes, but the 135 dates that had turned into *wrong real dates* couldn't be repaired from the file itself: nothing in the cell said which ones had been swapped. So she went back to the original CSV and imported it properly with **Data → From Text/CSV**, setting `order_date` to **Date** with the **English (India)** locale and `customer_code` to **Text**.

**Step 5: reconcile.** With the clean import, the tracker's January row showed ₹202,640, matching finance. She added the check rows she always used: the monthly revenues summed to **₹4,335,471**, which equaled `SUMIFS` on the whole Data sheet excluding cancelled orders, with a difference of 0. The two cancelled orders, worth ₹62,650, were excluded on purpose, and she wrote that rule in the note at the top of the tracker.

**Step 6: answer the question.** Her reply to Vikram was four sentences:

> *January 2025 was ₹202,640, 67.5% of target. It was weak, but not the worst month: June was lower at ₹186,928 (62.3%). The ₹91,649 figure came from a CSV opened with US date settings, which swapped days and months and dropped 195 lines. I've rebuilt the tracker from the original export and it now matches finance to the rupee.*

Then she did the part that stops it happening again. She saved the import steps (Power Query remembers them, so next year's file is one **Refresh**), moved the tracker to the team's shared drive with version history on, and added a line to the tracker's first sheet: *"Import the ERP export with Data → From Text/CSV. Never open the CSV directly."*

What Meera did that the trainee didn't:

- She **looked at what the cells contained** (`COUNT` versus `COUNTA`, the formula bar) before trusting any total.
- She **compared against an independent number** (finance's January figure) instead of assuming the spreadsheet was right.
- She **fixed the cause**, not the symptom, and **reconciled** the result to the total.
- She **wrote down the rule** (cancelled orders excluded) and **the procedure** (how to import), so the next person gets the same answer.

---

## Project: a monthly sales tracker from a raw export

**Goal:** turn a raw sales export into a monthly tracker that a sales head can read in a minute, that reconciles to the rupee, and that the next person can update without breaking it.

### Tools you'll need

- **Microsoft Excel**, Microsoft 365 for Windows (main version in this chapter). Excel for the web is free with a Microsoft account; Excel for Mac differences are noted in the text. `XLOOKUP` needs Microsoft 365, Excel 2021 or later, or Excel for the web; `IFS` and `TEXTJOIN` need Excel 2019 or later.
- **Google Sheets**, free at sheets.google.com with a Google account. **Google Forms** at forms.google.com.
- **A plain text editor** (Notepad, TextEdit, or VS Code) for looking inside CSV files.
- **Free alternative:** LibreOffice Calc opens and edits `.xlsx` files; most classic functions work, but some newer Excel functions such as `XLOOKUP` may not, depending on the version.
- **Companion files** (`companion/ch10/`, Appendix E):
  - `riverstone_sales_export_2025.csv`: the raw ERP export, 330 order lines, day-first dates, zero-padded codes.
  - `ch10_practice.xlsx`: Data, Customers, Products, Targets, and Cell detective sheets, with no formulas, for you to work in.
  - `ch10_tracker_solution.xlsx`: the finished tracker from the project, with every formula.
  - `build_ch10_files.py`: the Python script that builds all of the above from Riverstone's data (seed 20251), so the files can be regenerated.

**Option A: your own data.** Use an export you work with, such as sales, expenses, or support tickets. Remove or replace customer names, employee names, phone numbers, and anything confidential before you practice on it or show it to anyone. Follow the same steps with your own columns.

**Option B: Riverstone's data.** Use `riverstone_sales_export_2025.csv`.

**Steps**

1. **Import properly.** In Excel, **Data → From Text/CSV** with `order_date` as a Date (English (India) locale) and `customer_code` as Text. In Sheets, set the locale to India, import, and repair codes with `TEXT`. Name the sheet `Data`. Check: 330 rows, `COUNT` of dates = 330, row 2's code shows `0002`.
2. **Bring in the reference sheets.** Copy the Customers and Targets sheets from `ch10_practice.xlsx` into your workbook.
3. **Add calculated columns** to Data, filled down to row 331:
   - `J` `net_revenue`: `=E2*F2*(1-G2/100)`
   - `K` `month_start`: `=DATE(YEAR(B2),MONTH(B2),1)`
   - `L` `first_line_of_order`: `=IF(COUNTIF($A$2:A2,A2)=1,1,0)`, which is 1 on the first line of each order and 0 on the others, so adding it up counts orders instead of lines. Notice the mixed range `$A$2:A2`: its start is locked and its end grows as the formula moves down.
   - `M` `customer_name` and `N` `segment`: `XLOOKUP` from the Customers sheet (section 10.9).
4. **Build the Tracker sheet.** A title in `A1`, a one-line note in `A2` stating the rules (*"Net revenue = quantity × unit price × (1 − discount %). Cancelled orders excluded. Source: ERP export."*), and headers in row 4: `month`, `target`, `orders`, `net_revenue`, `pct_of_target`, `vs_prev_month`, `status`. In rows 5 to 16:
   - `A5`: `=Targets!A2` (format `mmm yyyy`), `B5`: `=Targets!B2`, both filled down.
   - `C5`: `=SUMIFS(Data!$L$2:$L$331,Data!$K$2:$K$331,A5,Data!$H$2:$H$331,"<>Cancelled")`
   - `D5`: `=SUMIFS(Data!$J$2:$J$331,Data!$B$2:$B$331,">="&A5,Data!$B$2:$B$331,"<="&EOMONTH(A5,0),Data!$H$2:$H$331,"<>Cancelled")`
   - `E5`: `=D5/B5` (format `0.0%`); `F6`: `=D6/D5-1` (format `+0.0%;-0.0%`), starting in February; `G5`: `=IF(D5>=B5,"On target","Below target")`.
5. **Add totals and a check.** Row 17: `=SUM()` of target, orders, and net revenue, and `=D17/B17`. Row 19: `=SUMIFS(Data!$J$2:$J$331,Data!$H$2:$H$331,"<>Cancelled")`. Row 20: `=D17-D19`, which must be **0**.
6. **Format for reading.** Freeze the header row, apply `#,##0` to money, and add conditional formatting to `pct_of_target`: green for 100% or more, red for below 80%.
7. **Add a combo chart** of net revenue (columns) and target (line), with a title that states the finding.
8. **Add a Reps sheet** with revenue and orders per sales rep (including a "(no rep)" row using the `""` criterion), a segment breakdown, and a drop-down (data validation) that picks a rep and shows their revenue.
9. **Protect and share.** Protect the formula cells, share with named people as viewers or commenters, and name the version "2025 tracker, first release".

Your tracker should match Figure 10.5.

![Diagram of the tracker workbook: the CSV feeds the Data sheet with five calculated columns, which feeds the Tracker and Reps sheets, beside the finished monthly table with conditional formatting](figures/fig10-5-monthly-tracker.svg)

*Figure 10.5 — The tracker's structure and result. Every number on the Tracker sheet comes from the Data sheet by formula, and the check row proves the months add back to the total.*

The finished Tracker sheet (numbers rounded to whole rupees here; `ch10_tracker_solution.xlsx` has the full values):

| month | target | orders | net_revenue | pct_of_target | vs_prev_month | status |
|---|---|---|---|---|---|---|
| Jan 2025 | 300,000 | 8 | 202,640 | 67.5% | | Below target |
| Feb 2025 | 300,000 | 10 | 253,664 | 84.6% | +25.2% | Below target |
| Mar 2025 | 320,000 | 11 | 278,008 | 86.9% | +9.6% | Below target |
| Apr 2025 | 320,000 | 12 | 210,282 | 65.7% | -24.4% | Below target |
| May 2025 | 320,000 | 15 | 329,359 | 102.9% | +56.6% | On target |
| Jun 2025 | 300,000 | 13 | 186,928 | 62.3% | -43.2% | Below target |
| Jul 2025 | 280,000 | 13 | 232,692 | 83.1% | +24.5% | Below target |
| Aug 2025 | 320,000 | 14 | 329,282 | 102.9% | +41.5% | On target |
| Sep 2025 | 380,000 | 18 | 558,315 | 146.9% | +69.6% | On target |
| Oct 2025 | 520,000 | 20 | 681,071 | 131.0% | +22.0% | On target |
| Nov 2025 | 500,000 | 21 | 633,408 | 126.7% | -7.0% | On target |
| Dec 2025 | 380,000 | 18 | 439,824 | 115.7% | -30.6% | On target |
| **Total** | **4,240,000** | **173** | **4,335,471** | **102.3%** | | |

The check: the Data sheet's non-cancelled total is ₹4,335,471; difference **0**. ✓ The 173 orders and ₹4,335,471 match Chapter 13's figures for the same year. ✓

**What to tell Anita:** Riverstone finished 2025 at 102.3% of its annual target, but the year had two halves. January to June reached only 78.5% of target, with June the weakest month (62.3%). From August onward, every month beat its target, and October's ₹681,071 was the best month of the year. Q4 alone brought in 40.5% of the year's revenue, so a slow Q4 would put the whole year at risk.

**Stretch goals**

- Add a `Segments` section to the Tracker that shows each month's revenue by segment (a grid of `SUMIFS` with mixed references: month down the side, segment across the top).
- Add a cell for the **as-of date** and a status that says "Month in progress" for months after it.
- Rebuild the tracker in the other app (Sheets if you used Excel, or the reverse) and confirm the check row is still 0.
- Add a Google Form for monthly target changes, feeding a sheet that the Targets sheet reads from.

---

## Recap

- A **workbook** holds **sheets**; each **cell** has an **address**, and a block of cells is a **range**. Excel and Google Sheets share this model; their menus and a few features differ.
- **What a cell shows isn't always what it contains.** Number formats round and dress up values; text can look like a number; dates are day counts. Check with the formula bar, `ISNUMBER`, `ISTEXT`, and `LEN`, and compare `COUNT` with `COUNTA`.
- **CSV imports guess types.** Opening a day-first CSV with month-first settings scrambled 135 of Riverstone's 330 dates silently, left 195 as text, and stripped the zeros from every customer code. Import with column types set.
- **Everyday handling** matters: save and name files clearly, insert and delete rows knowing what formulas will do, **paste values** to freeze results, and use **find and replace** with care. The **status bar** gives an instant sum, average, and count.
- **Error values** name the problem: `#N/A` (not found), `#REF!` (deleted reference), `#VALUE!` (wrong type), `#DIV/0!`, `#NAME?`; `#####` means a narrow column.
- **Formulas** start with `=`. **Relative references** shift when copied, **absolute references** (`$J$2`) don't, and **mixed references** lock one part.
- `SUM`, `AVERAGE`, `COUNT`, and `IF` handle the basics; **`COUNTIFS`, `SUMIFS`, and `AVERAGEIFS`** answer most business questions with conditions.
- **Text functions** (`TRIM`, `TEXT`, `LEFT`, `MID`) and **date functions** (`DATE`, `EOMONTH`, `NETWORKDAYS`) fix and reshape messy values.
- **`XLOOKUP`** fetches values from another sheet; a lookup matches type as well as value.
- **Sort** the whole table, **filter** without deleting, and use **tables** so ranges grow with the data.
- **Data validation** prevents bad entries; **conditional formatting** highlights what matters, with a readable label alongside color.
- Google Sheets leads on **sharing, co-editing, version history, and Forms**; Excel leads on heavy analysis. Files move between them, but app-only features don't.
- **Reconcile every breakdown**: the parts must add back to the total.

---

## Key terms

spreadsheet application · workbook · worksheet (sheet) · cell · cell address · range · formula · function · argument · number format · data validation · conditional formatting · name box · formula bar · ribbon · headers · grain · number · text (string) · logical value · error · trailing space · date serial number · leading zeros · locale · fill handle · custom format · operator · relative reference · absolute reference · mixed reference · circular reference · test (condition) · criterion · wildcard · reconciliation · month key · lookup · exact match · sort · filter · filter view · `SUBTOTAL` · table · table reference · formula rule · co-authoring · comment · sheet protection · version history · Google Form · CSV UTF-8 · AutoSave · status bar · paste special · paste values · find and replace · series · Flash Fill · Smart Fill · Text to Columns · Format Painter · error value · named range · AutoSum · trace precedents · calculation mode · median · remove duplicates · print area · print titles

*(All terms are defined in the Glossary, Appendix A.)*

---

## Check yourself

- [ ] You can create, save, rename, and copy a workbook in both apps, and insert, delete, hide, and resize rows and columns.
- [ ] You know when to paste values, how to find and replace safely, and what each error value (`#N/A`, `#REF!`, `#VALUE!`, `#DIV/0!`, `#NAME?`) is telling you.
- [ ] You can open the formula bar on a suspicious number and say whether it's a number, text, a date, or a formula.
- [ ] You import CSV files with column types set, and check the row count, a code column, and `COUNT` of the dates afterward.
- [ ] You know without thinking whether a formula needs `J2`, `$J$2`, `$J2`, or `J$2` before you copy it.
- [ ] You can write `COUNTIFS`, `SUMIFS`, and `AVERAGEIFS` with several criteria, including dates, "not equal", wildcards, and blanks.
- [ ] You can explain the difference between a number format and `ROUND`, and between a number format and `TEXT`.
- [ ] You can fetch a value from another sheet with `XLOOKUP` (or `INDEX`/`MATCH`) and explain why a lookup says "not found".
- [ ] You sort and filter without scrambling rows, and use `SUBTOTAL` when a filter is on.
- [ ] You use data validation to prevent bad entries and conditional formatting to point at the cells that matter.
- [ ] You can share a workbook safely, protect its formulas, and restore an earlier version.
- [ ] You can set up a sheet to print or save as a readable PDF.
- [ ] You can move a file between Excel and Google Sheets and know what might break.
- [ ] Every breakdown you build has a check that adds the parts back to the total.

---

## Exercises

Use `ch10_practice.xlsx` in Excel or Google Sheets unless an exercise says otherwise. The Data sheet's rows 2 to 331 hold the 330 order lines.

### Warm-up

1. Cell `A1` displays `32,063`. The formula bar shows `32062.5`. What does `=A1*2` return, and why?
2. Which of these cells hold text: (a) `0005` in a cell formatted as Plain text, (b) a cell that displays `2025-01-02` and returns TRUE for `ISNUMBER`, (c) `2900 ` with a trailing space?
3. Write the range that covers columns A to I and rows 1 to 331 of the Data sheet, and the reference to cell `B2` on a sheet named `Cell detective`.
4. *Predict the result.* `O2` contains `=J2/SUM(J2:J331)`. You copy it to `O3`. What formula is now in `O3`? What formula should it contain?
5. On the Data sheet, `COUNT(I2:I331)` returns 0 and `COUNTA(I2:I331)` returns 311. What does each tell you?
6. Give the menu path to import a CSV with control over column types in Excel, and the setting to change in Google Sheets before importing a file with day-first dates.
7. *Match each error to its most likely cause:* `#N/A`, `#REF!`, `#VALUE!`, `#DIV/0!`, `#NAME?`, `#####`. Causes: (a) a column too narrow, (b) a misspelled function, (c) a lookup value not in the list, (d) a deleted row a formula pointed at, (e) text used in arithmetic, (f) a month with a target of 0.

### Core

8. Add the `net_revenue` column to the Data sheet. What does row 5 show? Check it by hand.
9. Calculate total net revenue (a) for all 330 lines and (b) excluding cancelled orders. What's the difference, and which orders explain it?
10. How many lines were *Delivered* and had a discount?
11. What's the average net revenue per non-cancelled order line, to the paisa?
12. How many order lines are worth ₹50,000 or more? Which is the largest, and what did the customer buy?
13. Add `customer_name` and `segment` with `XLOOKUP`. Then use `SUMIFS` to calculate non-cancelled net revenue per segment, and reconcile to the total.
14. What was non-cancelled net revenue in November 2025? And from Wholesale customers only in November?
15. Add `month_start` with `DATE(YEAR(B2),MONTH(B2),1)`. What does `=EOMONTH(B4,0)` return, and what would a report use it for?
16. Calculate non-cancelled revenue and orders for lines with **no** sales rep. How many lines have no rep in total?
17. Add data validation so `status` only accepts the four statuses and `quantity` only accepts whole numbers from 1 to 1,000. What happens when you type `0` in a quantity cell? Does the existing data pass?
18. Build the monthly revenue table from the project and apply conditional formatting to `pct_of_target`. Which months turn red (below 80%), and how many turn green?
19. Import `riverstone_sales_export_2025.csv` into a new workbook in your app with column types set. Show three checks that prove the import worked.
20. Copy the `order_id` column to a new sheet and remove duplicates. How many values remain, and what do they represent? Then select `J2:J331` and read the sum, average, and count from the status bar.
21. Set up the Data sheet to print on readable landscape pages with the header row on every page, and save it as a PDF. List the settings you used in your app.
22. Add the `first_line_of_order` column. What does its total return for non-cancelled lines, and for all lines? Why not count lines with `COUNTIFS`?

### Stretch

23. Add `vs_prev_month` to your monthly table. Which month had the biggest percentage rise over the month before, and which the biggest fall?
24. What share of 2025's non-cancelled revenue came in October to December?
25. A colleague's damaged copy has customer codes as numbers (`2`, `5`) and some dates as text (`13-01-2025`). Write the formulas that repair each, and explain which kind of date damage *can't* be repaired from the damaged file.
26. Build a combo chart of monthly revenue and target. Write two titles for it, one that names the topic and one that states the finding, using this chapter's numbers.

### Think about it (no spreadsheet needed)

27. Anita wants the tracker shared with 12 branch managers. They should see everything, filter it for their own region, and change nothing. How would you set this up in Google Sheets, and in Excel?
28. A colleague built a tracker in Google Sheets using `QUERY` and `IMPORTRANGE`, and finance wants it as an Excel file. What will happen when they download it, and what would you do?
29. Your total matches the database to the rupee, but the sales head's own figure is ₹62,650 higher. Before you tell anyone they're wrong, what's the most likely explanation, and what question would you ask?

---

## Answers

*(In the finished book these move to Appendix G.)*

**1.** `=A1*2` returns **64125**. Formulas use the stored value, 32062.5, not the displayed 32,063. The number format only rounds the display. If you expected 64,126 (2 × 32,063), you were calculating with what you saw.

**2.** **(a) and (c)** are text. (a) is formatted as Plain text, so `0005` is stored as characters. (c) has a trailing space, which makes it text even though it looks like a number; `LEN` returns 5 and `ISTEXT` returns TRUE. (b) is a real date: `ISNUMBER` is TRUE because a date is a day count (45659) in a date format.

**3.** `Data!A1:I331` (or `A1:I331` on the Data sheet itself), and `'Cell detective'!B2`. The quotes are needed because the sheet name contains a space; without them the reference fails.

**4.** `O3` contains `=J3/SUM(J3:J332)`. Both the cell and the range moved down one row, so the total no longer includes row 2. It should contain `=J3/SUM($J$2:$J$331)`. The wrong version gives 0.476% for row 3 against the correct 0.475%, so it looks fine, but by row 331 it shows 100% and the column adds to 656.8%.

**5.** `COUNT` counts numbers, and the sales rep column holds names (text), so it returns 0. `COUNTA` counts non-empty cells: 311 lines have a rep, which means 330 − 311 = 19 lines have none (`COUNTBLANK` confirms 19). The common wrong reading is "`COUNT` returned 0, so the column is empty".

**6.** Excel: **Data → Get & Transform Data → From Text/CSV**, then **Transform Data** to set each column's type (date with the English (India) locale, codes as text). Google Sheets: **File → Settings → General → Locale → India** before **File → Import**, so day-first dates are read correctly; then repair any codes that lost their zeros.

**7.** `#N/A` → (c), a lookup value not in the list. `#REF!` → (d), a deleted row the formula pointed at. `#VALUE!` → (e), text used in arithmetic. `#DIV/0!` → (f), dividing by a target of 0. `#NAME?` → (b), a misspelled function such as `=SUMM(J2:J5)`. `#####` → (a), a column too narrow to show the value; it isn't an error in the data at all.

**8.** `=E5*F5*(1-G5/100)` returns **32062.5**. By hand: order 10003's second line is 45 × ₹750 = ₹33,750, less 5% (₹1,687.50) = ₹32,062.50. ✓

**9.**

```excel
=SUM(J2:J331)                              → 4398121
=SUMIFS(J2:J331,H2:H331,"<>Cancelled")     → 4335471
```

The difference is **₹62,650**: the four lines of the two cancelled orders, **10034** (Rahul Mehta, ₹24,800) and **10131** (Festive Gifts Co, three lines, ₹37,850). The non-cancelled total matches the database in Chapter 13.

**10.** `=COUNTIFS(H2:H331,"Delivered",G2:G331,">0")` returns **185**. (186 lines had a discount in total; the other one is order 10174's Pending line.)

**11.** `=AVERAGEIFS(J2:J331,H2:H331,"<>Cancelled")` returns 13298.990797546, which is **₹13,298.99**. A plain `AVERAGE` gives ₹13,327.64 because it includes the cancelled lines.

**12.** `=COUNTIF(J2:J331,">=50000")` returns **3**. Sorting largest first shows the biggest: order **10107**, Deccan Packaging, 45 Industrial Crates at ₹1,400 with a 10% discount, **₹56,700** (45 × 1,400 = 63,000; less 10% = 56,700 ✓). The other two are orders 10126 and 10162, both ₹51,520.

**13.** `=XLOOKUP(C2,Customers!$A$2:$A$25,Customers!$B$2:$B$25,"not found")` in `M2` and the same with column D in `N2`. Then:

```excel
=SUMIFS($J$2:$J$331,$N$2:$N$331,"Wholesale",$H$2:$H$331,"<>Cancelled")     → 1702658.5
```

Wholesale ₹1,702,658.50, Retail ₹1,488,773.75, Hospitality ₹1,144,038.75. They add to **₹4,335,471.00**. ✓ If any lookup says "not found", the codes are numbers instead of text (section 10.9).

**14.** `=SUMIFS(J2:J331,B2:B331,">="&DATE(2025,11,1),B2:B331,"<="&DATE(2025,11,30),H2:H331,"<>Cancelled")` returns **₹633,408**. Adding `N2:N331,"Wholesale"` as a fourth pair returns **₹343,685.50**, from 15 lines. A common mistake is `"<=30-11-2025"` typed as text, which some locales misread; building the date with `DATE` avoids that.

**15.** `=EOMONTH(B4,0)` returns **2025-01-31** (order 10003 was placed on 12 January). Reports use end-of-month dates for "orders up to and including this month" criteria, for due dates such as "end of next month" (`EOMONTH(date,1)`), and for month labels.

**16.**

```excel
=SUMIFS(J2:J331,I2:I331,"",H2:H331,"<>Cancelled")     → 204502.5
=SUMIFS(L2:L331,I2:I331,"",H2:H331,"<>Cancelled")     → 10
=COUNTBLANK(I2:I331)                                   → 19
```

₹204,502.50 from 10 orders had no rep. In total 19 lines have no rep: 16 non-cancelled lines plus the 3 lines of cancelled order 10131.

**17.** Status: **Data Validation → List** (Excel) or **Dropdown** (Sheets) with `Delivered,Shipped,Pending,Cancelled`. Quantity: **Whole number between 1 and 1000** (Excel), or **Custom formula** `=AND(E2>=1,E2<=1000,INT(E2)=E2)` with **Reject the input** (Sheets). Typing `0` is refused with an error message. The existing data passes: quantities run from 5 to 85, and every status is one of the four. Excel's **Circle Invalid Data** finds no cells to circle.

**18.** Red (below 80%): **January (67.5%), April (65.7%), and June (62.3%)**. Green (100% or more): **6 months**: May, August, September, October, November, and December. February, March, and July stay uncolored.

**19.** Three checks: `=COUNTA(A2:A331)` returns 330 (no rows lost); `C2` shows `0002` and `=ISTEXT(C2)` is TRUE (codes kept); `=COUNT(B2:B331)` returns 330 (every date is a real date). A fourth, stronger check: January's non-cancelled revenue is ₹202,640.

**20.** **175** values remain: one per order, compared with 330 order lines (2 of the 175 orders were cancelled, which is why the tracker counts 173). Excel's message reports 155 duplicate values removed. For `J2:J331`, the status bar shows Sum **4,398,121**, Average **13,327.64**, and Count **330**. The sum includes the cancelled lines, so it's ₹62,650 higher than the non-cancelled total; the status bar has no criteria.

**21.** Excel: **Page Layout → Orientation → Landscape**; **File → Print → Scaling → Fit All Columns on One Page**; **Page Layout → Print Titles → Rows to repeat at top** `$1:$1`; optionally **Insert → Header & Footer** for page numbers; then **File → Export → Create PDF/XPS**. Google Sheets: freeze row 1 (**View → Freeze → 1 row**), then **File → Download → PDF** (or **File → Print**) with **Page orientation: Landscape**, **Scale: Fit to width**, and **Headers & footers → Repeat frozen rows** ticked, plus page numbers. Check the preview: every page should start with the header row, and no column should spill onto its own page.

**22.** For non-cancelled lines, `=SUMIFS(L2:L331,H2:H331,"<>Cancelled")` returns **173**; for all lines, `=SUM(L2:L331)` returns **175**. `COUNTIFS(H2:H331,"<>Cancelled")` would return 326, the number of *lines*, because an order with three products has three rows. The flag works because `COUNTIF($A$2:A2,A2)` counts how many times this order ID has appeared *so far*; it's 1 only on the first line.

**23.** With `=D6/D5-1` filled down: the biggest rise was **September, +69.6%** (₹329,282 to ₹558,315); the biggest fall was **June, −43.2%** (₹329,359 to ₹186,928). Note that a big percentage fall after a big month isn't automatically bad news: December fell 30.6% from November and still beat its target.

**24.** October to December: ₹681,070.75 + ₹633,408.00 + ₹439,823.50 = **₹1,754,302.25**, which is 1,754,302.25 ÷ 4,335,471 = **40.5%** of the year.

**25.** Codes: `=TEXT(C2,"0000")`, then paste as values over the original column (this works because every code has four digits). Text dates: `=DATE(RIGHT(B2,4),MID(B2,4,2),LEFT(B2,2))`. What can't be repaired: dates that were read month first and **became valid wrong dates**, such as 2 January stored as 1 February. The cell holds a real date, and nothing in the damaged file says which of those were swapped. The only reliable fix is to re-import from the original CSV, as Meera did.

**26.** Build it as in section 10.12 (Excel: **Insert → Combo**; Sheets: **Chart editor → Combo chart**). A topic title: *"Monthly revenue vs target, 2025"*. A finding title, for example: *"Riverstone beat its target in six of the last eight months of 2025"* or *"A weak first half (78.5% of target) was rescued by a strong second half (120.8%)"*. The finding title tells the reader what to see before they study the bars.

**27.** Google Sheets: **Share** with the 12 managers by name as **Viewers**; in the Share settings, decide whether viewers may download or copy; ask each manager to use **Data → Filter views → Create new filter view** (viewers can create temporary filter views that don't affect anyone else), or create a named filter view per region for them. Excel: store the file on OneDrive or SharePoint, **Share → Can view**; viewers can sort and filter in Excel for the web without saving changes to the file. In both, protect formula cells anyway in case someone is later given edit access. The common wrong answer is "share as editors and ask them not to change anything".

**28.** `QUERY` and `IMPORTRANGE` are Google Sheets–only functions. In the downloaded `.xlsx`, those cells arrive as fixed values (or errors) and stop updating, so the Excel file is a snapshot. Tell finance it's a snapshot as of the download date, or rebuild those parts with functions both apps share (`SUMIFS`, lookups) or with Power Query in Excel (Chapter 11). Then check the totals in the Excel copy against the Sheets original.

**29.** ₹62,650 is exactly the value of the two cancelled orders. The most likely explanation is that the sales head's figure *includes* cancelled orders and yours excludes them. Neither number is "wrong" until the rule is agreed. Ask: *"Should cancelled orders count in this report?"* Then write the agreed rule on the report, as Meera did. Chapter 24 covers how to have that conversation.

---

## Where this leads

- **Chapter 11, The Spreadsheet, Mastered:** lookups in depth (`XLOOKUP` options, `INDEX`/`MATCH`), pivot tables, dynamic arrays (`FILTER`, `UNIQUE`, `SORT`), Power Query for refreshable imports, and Google Sheets' `QUERY` and `IMPORTRANGE`. The tracker you built becomes a one-click refresh.
- **Chapter 12, Databases & SQL Foundations:** the same questions (net revenue, excluding cancelled orders, revenue by segment) answered with `WHERE`, `GROUP BY`, and `JOIN`, on data too large for a spreadsheet.
- **Chapter 14, Data Cleaning & Preparation:** messy text, duplicates, mixed date formats, and missing values at scale, in spreadsheets, SQL, and pandas.
- **Chapter 15, Data Visualization Principles:** choosing the right chart, titles that state the finding, and color with meaning.
- **Chapter 19, Spreadsheet Automation:** macros, VBA, Office Scripts, and Google Apps Script, including the form-to-email workflow started in section 10.13.
- **Interview preparation:** the Excel, Google Sheets, VBA & BI Question Bank (Chapter 70) tests this chapter's skills, from "what's the difference between `COUNT` and `COUNTA`?" to live `SUMIFS` and lookup tasks.
