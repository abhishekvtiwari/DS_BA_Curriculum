# Chapter 19. Spreadsheet Automation: Macros, VBA, Office Scripts & Apps Script

*Part 2 — The Analyst*

> **Chapter at a glance**
>
> **You will learn to:** decide when automating inside a spreadsheet is the right answer · record a macro, save a macro-enabled workbook, and handle macro security without turning it off · read recorded code and rewrite it properly · program from zero in VBA: variables, `If`, `Select Case`, loops, arrays, collections, `Sub` and `Function` · work with Excel's object model instead of clicking · build the everyday toolkit: last row, loop the sheets, consolidate a folder of files, clean, format, pivot, PDF · send an Outlook email with the report attached or in the body · write custom worksheet functions and a simple form · debug with breakpoints and the Immediate window, and handle errors on purpose · make a macro fast with arrays and screen updating · do the same work in **Office Scripts** (Excel on the web, TypeScript) and **Google Apps Script** (Sheets, JavaScript), including triggers, HTML email, and API calls · keep macros maintainable, and know when to move the job to Power Query, Python, or a pipeline.
>
> **Before you start:** Chapters 10 and 11 (spreadsheets, formulas, lookups, pivot tables, Power Query). **No programming experience is assumed:** this is the first chapter in the book where you write code, and section 19.4 teaches the basics from zero in VBA.
>
> **Time needed:** 25–30 hours, spread over three weeks: VBA (sections 19.1–19.10) 13–16 hours, Office Scripts and Apps Script (sections 19.11–19.14) 6–8 hours, and the project about 6 hours. Take sections 19.11–19.14 as a separate sitting.
>
> **Tools:** **Excel for Windows** (Microsoft 365 or 2016+) for VBA and Outlook automation; **Excel on the web** with a Microsoft 365 business plan for Office Scripts; a **Google account** for Sheets and Apps Script. Excel for Mac runs VBA but not the Outlook or Windows-specific parts.
>
> **Practice data:** `companion/ch19/ch19_practice.xlsx`, a small workbook for your first macros (sections 19.2–19.5). `companion/ch19/branch_files/`: twelve workbooks (four branch sales offices × October, November, December 2025) built from Riverstone's Q4 2025 order lines, plus `_notes.txt` so your folder code has to filter by extension. `expected_results.md` lists every number a correct consolidation must produce. `enquiries_sample.csv` is the Google Form data for the Apps Script project.

---

## Why this matters

Walk into most Indian offices and the real reporting engine isn't a BI tool. It's a workbook with a button on it, written years ago by someone who has since left.

That's not a failure of taste. Spreadsheets are where the data already is, where the finance team is comfortable, and where a change takes minutes instead of a change request. A macro that consolidates twelve branch files and emails a PDF at 9 a.m. is worth more to the business than an elegant pipeline nobody funded.

It's also where the most common analyst horror stories live: the macro that only runs on one laptop, the one that silently skips a file, the one with a password in line 40, the one nobody can read. This chapter teaches both halves: how to automate a spreadsheet properly, and how to keep the result from becoming a liability.

There's a career angle too. "Knows VBA" still appears in analyst job descriptions across manufacturing, distribution, and finance in India, and the first automation you build at work is usually a spreadsheet one, because it needs no permission and no new software. Getting it right is how you earn the room to do the bigger things in Chapters 18 and 20.

---

## In plain English

A spreadsheet is a workshop bench. You do the job by hand: open the files, copy, paste, sort, format, save, attach, send.

A **macro** is a jig. You set it up once, and every repeat of the job clamps into the same place and comes out the same way. The first one you make is a **recording**: you do the job once with the recorder on, and the spreadsheet writes down every movement, including the clumsy ones.

Recordings are literal. If you clicked cell B7 because that's where last month's data ended, the recording clicks B7 forever, even when this month has more rows. So the second step is always the same: read what the recorder wrote, keep the useful parts, and replace the literal clicks with instructions that describe what you meant. *"Go to the last row with data"*, not *"go to B7"*. *"For every file in the folder"*, not *"open this one file"*.

That's the whole chapter. A recorder to get started, a language (VBA, TypeScript, or JavaScript) to say what you meant, and a set of habits so the jig still works when someone else picks it up.

---

## 19.1 When automating inside a spreadsheet is the right answer

| Situation | Best tool |
|---|---|
| The data already lives in workbooks, and the output must be a workbook people edit | **VBA or Office Scripts** |
| A repetitive shaping job: combine files, unpivot, clean columns | **Power Query** (Chapter 11), not a macro |
| A report several people read, refreshed on a schedule | **Power BI** (Chapter 16) |
| Data from a database or an API, or anything statistical | **Python** (Chapter 18) |
| A Google Sheets workflow: forms, emails, triggers | **Apps Script** |
| Formatting, saving as PDF, sending Outlook email, driving Excel itself | **VBA** |
| A pipeline with dependencies, retries, and monitoring | An orchestrator (Chapter 46) |

Two rules of thumb:

1. **If Power Query can do it, use Power Query.** It's recorded, refreshable, and doesn't need macro-enabled files or trust settings. Most "combine these files" macros written before 2015 would be three clicks today.
2. **Automate the boring shell, not the thinking.** Macros are excellent at opening, copying, formatting, saving, and sending. They're a poor place for business logic that changes often, and a terrible place for anything you can't explain to the person who inherits it.

### What a macro is, and what `.xlsm` means

A **macro** is code stored inside a workbook (or in your personal macro workbook) that Excel can run. Because code in a file can do anything your account can do, Excel separates file types:

| Extension | Holds macros? | Use |
|---|---|---|
| `.xlsx` | No | Normal workbooks |
| `.xlsm` | Yes | Macro-enabled workbooks |
| `.xlsb` | Yes | Binary format: faster to open for very large files |
| `.xltm` | Yes | Macro-enabled template |

Save a workbook containing code as `.xlsx` and Excel throws the code away, with one warning that everybody clicks past. It's the most common way a morning's work disappears.

### Macro security, without switching it off

**File → Options → Trust Center → Trust Center Settings → Macro Settings** offers four choices. The right one is the default: **Disable VBA macros with notification**, which lets you enable a file you trust after seeing the banner.

Two things to know in a company setting:

- **Files from the internet or email are blocked**, with a red banner rather than the yellow "Enable content" one. Since 2022 Microsoft blocks macros in files marked with the Mark of the Web by default. The fix is **not** to unblock every file: it's to put shared macro workbooks in a **trusted location** (**Trust Center → Trusted Locations**) on a network path your IT team approves.
- **Never tell colleagues to enable all macros.** That setting is how ransomware arrives. Trusted locations and, in larger companies, signed macros are the grown-up answers.

---

## 19.2 Recording your first macro

The recorder is the fastest way to learn the **object model**, Excel's names for the things you click (workbooks, sheets, cells; section 19.5): do the thing, then read what Excel wrote.

**Set up your practice workbook first.** Open `companion/ch19/ch19_practice.xlsx`. It has two sheets: **Master**, a copy of one branch file (Kolkata, December 2025: a header row and 994 order lines in columns A to K), and **Scratch**, an empty sheet for experiments. Save it straight away with **File → Save As → Excel Macro-Enabled Workbook (\*.xlsm)** as `ch19_practice.xlsm`. Every macro in sections 19.2 to 19.5 runs in this workbook.

1. **View → Macros → Record Macro** (or **Developer → Record Macro**; enable the Developer tab in **File → Options → Customize Ribbon**).
2. Name it without spaces (`Format_Sales_Sheet`), optionally give it a shortcut, and choose where to store it:
   - **This Workbook:** the macro travels with the file.
   - **Personal Macro Workbook:** a hidden workbook (`PERSONAL.XLSB`) that opens with Excel, so the macro is available in every file on your machine. This is where your personal cleanup tools belong.
3. Do the job once, carefully.
4. **Stop Recording**, then **Alt+F8** to run it, or **Alt+F11** to read it.

Attach it to a button so other people can run it: **Developer → Insert → Form Controls → Button**, draw it, assign the macro. (Form controls, not ActiveX; they're simpler and survive being emailed.)

### What the recorder gives you

Recording "select the data, make the header bold, freeze the top row, autofit" produces something like this:

```vb
Sub Format_Sales_Sheet()
'
' Format_Sales_Sheet Macro
'
    Range("A1:K1").Select
    Selection.Font.Bold = True
    Rows("2:2").Select
    ActiveWindow.FreezePanes = True
    Cells.Select
    Cells.EntireColumn.AutoFit
    Range("A1").Select
End Sub
```

It works, and it has three problems that every recorded macro has:

- **It selects things.** Selecting is what a human does because a human needs to see the cell. Code doesn't.
- **It's literal.** `A1:K1` is this sheet's header today; next month's file has twelve columns.
- **It depends on what's active.** `ActiveWindow` and `Cells` mean "whatever is in front of me", so running it with the wrong sheet in view formats the wrong thing.

The rewritten version says what you meant:

```vb
Sub FormatSalesSheet(ws As Worksheet)
    With ws
        .Rows(1).Font.Bold = True
        .Activate                          ' FreezePanes needs the sheet visible
        .Range("A2").Select
        ActiveWindow.FreezePanes = True
        .Cells.EntireColumn.AutoFit
    End With
End Sub
```

Now it takes the sheet as an argument, touches only that sheet, and works whatever the width of the data. (`FreezePanes` is one of the few things that really does need a selection, which is worth knowing so you don't hunt for a cleaner way.) A macro that takes an argument doesn't appear in the **Alt+F8** list, because Excel wouldn't know which sheet to give it; section 19.4 shows how to run it.

> **Watch out: the recorder can't record everything.** Loops, conditions, folder handling, and error handling never appear in a recording, because you can't click them. The recorder teaches you object names; section 19.4 onward teaches you the rest.

---

## 19.3 The VBA editor

**Alt+F11** opens the Visual Basic Editor (VBE). Four panes matter:

- **Project Explorer** (**Ctrl+R**): the tree of open workbooks, their sheets, `ThisWorkbook`, and **Modules**. Your code goes in a module (**Insert → Module**), not in a sheet, unless it's an event handler.
- **Code window:** where you type. Two drop-downs at the top navigate objects and their events.
- **Immediate window** (**Ctrl+G**): a box where you type one line and see the answer at once. Type `?ActiveSheet.Name` and press **Enter**, and it prints the name of the sheet in front of you (`?` means "print"). `Debug.Print` in your code writes here too.
- **Locals and Watch windows:** variable values while the code is paused.

Set two options once, in **Tools → Options**:

- **Require Variable Declaration** (ticked). It puts `Option Explicit` at the top of every new module, which forces you to declare variables and catches every typo. Without it, a misspelled variable is silently a new empty one, which is the single most common source of wrong answers in VBA.
- **Auto Syntax Check** (unticked, if the pop-ups annoy you; the red text still marks errors).

---

## 19.4 Programming from zero, in VBA

This section assumes you have never written code. Each example is a short procedure: type it into a module (**Insert → Module** in the editor), run it, and compare what you see with the output printed under it. Keep the Immediate window open (**Ctrl+G**), because that's where most of the output appears.

### Statements, comments, and structure

Code lives in a **procedure**. There are two kinds: a **`Sub`** does something, a **`Function`** works out a value and hands it back. Each line inside is a **statement**, one instruction.

```vb
Option Explicit                       ' every variable must be declared

Sub SayHello()
    ' a comment starts with an apostrophe
    MsgBox "Hello from Riverstone"     ' shows a dialog box
    Debug.Print "this goes to the Immediate window"
End Sub
```

Click anywhere inside `SayHello` and press **F5** (or run it from Excel with **Alt+F8**). A dialog box appears with the text *Hello from Riverstone* and an **OK** button. When you click **OK**, the Immediate window shows:

```
this goes to the Immediate window
```

What each line does:

- **`Option Explicit`** sits once at the top of the module, above every procedure. It makes VBA refuse to run code that uses a name you haven't declared (section 19.3 set the editor to add it for you).
- **`Sub SayHello()` … `End Sub`** is the procedure: its name, a pair of empty brackets (it needs nothing from you), and the line that closes it. Everything between runs from top to bottom.
- **`'`** starts a comment: VBA ignores the rest of the line. Comments can sit on their own line or after a statement.
- **`MsgBox "Hello from Riverstone"`** shows a dialog box with that text, and waits for a click. Text in code always goes inside double quotes.
- **`Debug.Print`** writes a line to the Immediate window instead.

Use `Debug.Print` while developing, not `MsgBox`: a message box in a loop of 12 files means 12 clicks.

### Variables and types

A **variable** is a name for a value. `Dim` declares it, and the type after `As` says what it can hold.

```vb
Sub VariableDemo()
    Dim branch As String
    Dim rowCount As Long
    Dim netRevenue As Double
    Dim isFinal As Boolean
    Dim orderDate As Date

    branch = "Mumbai HO"
    rowCount = 25832
    netRevenue = 423872808#
    isFinal = True
    orderDate = DateSerial(2025, 12, 31)

    Debug.Print branch & ": " & Format(rowCount, "#,##0") & " rows, " & Format(netRevenue, "#,##0.00")
    Debug.Print "Final? " & isFinal & "; period ends " & Format(orderDate, "dd mmm yyyy")
End Sub
```

<<OUT:VariableDemo>>

- **`Dim branch As String`** makes a variable called `branch` that holds text. The next four lines do the same for a whole number, a decimal number, a true/false value, and a date.
- **`branch = "Mumbai HO"`** puts a value into the variable. The `=` here means "store", not "is equal to".
- **`423872808#`**: the `#` on the end marks the number as a `Double`. You don't need to type it; the editor adds it itself to large numbers when you press Enter, so don't be surprised to see it.
- **`DateSerial(2025, 12, 31)`** builds a date from a year, a month, and a day, so you never depend on how a computer reads "31/12/2025".
- **`&`** joins pieces of text into one, like `&` in an Excel formula (Chapter 10). Numbers, `True`, and dates are turned into text as they're joined.
- **`Format(value, "pattern")`** turns a number or date into text using a pattern, like a cell's number format (Chapter 10): `"#,##0"` adds thousands separators, `"#,##0.00"` also shows two decimals, and `"dd mmm yyyy"` writes a date as *31 Dec 2025*. The separators and month names follow your computer's regional settings.

| Type | Holds | Notes |
|---|---|---|
| `String` | Text | Join with `&` (not `+`) |
| `Long` | Whole numbers | Use instead of `Integer`, which stops at 32,767. Many files pass that, and `Long` costs nothing extra |
| `Double` | Decimals | The usual numeric type |
| `Boolean` | `True` / `False` | |
| `Date` | Dates and times | `DateSerial(y, m, d)`, `Now`, `Date` |
| `Variant` | Anything | The default when you don't say; flexible, slower, and hides mistakes |
| Object types | `Workbook`, `Worksheet`, `Range` | Assign with `Set` |

Two VBA-specific rules that catch everyone:

- **Objects need `Set`:** `Set ws = ThisWorkbook.Worksheets("Master")` (a sheet is an object; section 19.5), but `total = 0` for a plain value.
- **`Option Explicit` at the top of every module.** Without it, `netRevene = 100` creates a new variable and your total stays zero.

### Conditions

A condition lets the code choose. **Before you run it, predict** which line each call below prints.

```vb
Sub CheckTarget(ByVal actual As Double, ByVal target As Double)
    If actual >= target Then
        Debug.Print "Above target"
    ElseIf actual >= target * 0.9 Then
        Debug.Print "Close: " & Format(actual / target, "0.0%")
    Else
        Debug.Print "Below target by " & Format(target - actual, "#,##0")
    End If
End Sub
```

- **`(ByVal actual As Double, ByVal target As Double)`**: the names in the brackets are the Sub's **arguments**, values you hand it each time you run it, each with a type. `ByVal` means the Sub gets its own copy of the value; "Procedures with arguments" below shows why that's the safe choice.
- **`If … Then`** tests a condition; if it's true, the lines under it run. **`ElseIf`** tests another condition only if the first was false, and **`Else`** catches everything left. **`End If`** closes the block, like `IFS` in Chapter 11 written as lines instead of one formula.
- **`Format(actual / target, "0.0%")`** shows the ratio as a percentage with one decimal.

### Running a Sub that takes arguments

`CheckTarget` needs two numbers, so **F5** and **Alt+F8** can't run it: they wouldn't know what to give it. There are two ways.

In the Immediate window, type the name, a space, and the values, then press Enter:

```vb
CheckTarget 95, 100
```

```
Close: 95.0%
```

Or write a small test `Sub` with no arguments, which you *can* run with **F5**:

```vb
Sub TestCheckTarget()
    CheckTarget 105, 100
    CheckTarget 95, 100
    CheckTarget 80, 100
End Sub
```

<<OUT:TestCheckTarget>>

Notice there are **no brackets** around `105, 100`. That's VBA's rule: when you call a `Sub`, list the values after its name without brackets; when you use a `Function`'s answer (below), put them in brackets. The same works for section 19.2's `FormatSalesSheet`: type `FormatSalesSheet ThisWorkbook.Worksheets("Master")` in the Immediate window, and the Master sheet gets a bold, frozen header.

### Banding a value with `Select Case`

`Select Case` is VBA's cleanest way to write a banding rule, the job Chapter 11 did with an approximate-match lookup on a band table.

```vb
Sub BandBySize(ByVal value As Double)
    Select Case value
        Case Is >= 50000
            Debug.Print value & " is very large"
        Case Is >= 25000
            Debug.Print value & " is large"
        Case Is >= 10000
            Debug.Print value & " is medium"
        Case Else
            Debug.Print value & " is small"
    End Select
End Sub

Sub TestBandBySize()
    BandBySize 50000
    BandBySize 49999.995
    BandBySize 25000
    BandBySize 12000
    BandBySize 9999.5
End Sub
```

<<OUT:TestBandBySize>>

- **`Select Case value`** names the value to test once; each **`Case`** below is one possibility, checked from the top, and only the first that fits runs.
- **`Case Is >= 50000`**: `Is` stands for the value being tested, so this reads "value is at least 50,000".
- **`Case Else`** catches anything no other `Case` matched, and **`End Select`** closes the block.
- The bands go **from the top down**, each with only a lower edge, so no value can fall into a gap: 49,999.995 is "large", and exactly 25,000 is "large" too. A rule written as `Case 25000 To 49999.99` would miss 49,999.995 and send it to "small". Riverstone's size bands always include the lower edge: from ₹10,000 is medium, from ₹25,000 large, from ₹50,000 very large.

**What happens if you change the order** and put `Case Is >= 10000` first? Then 50,000, 49,999.995 and 25,000 all print "medium", because the first `Case` that fits wins. Order the bands from the top down.

Comparisons are `=`, `<>` (not equal), `<`, `<=`, `>`, `>=`, and you can combine them with `And`, `Or`, `Not`.

### Loops

A **loop** repeats lines. This one uses the practice workbook's **Master** sheet. Two new pieces appear here and get a full section next (19.5): `ThisWorkbook.Worksheets("Master")` is "the sheet called Master in this workbook", and `ws.Cells(i, 11)` is the cell in row `i`, column 11 of that sheet.

```vb
Sub LoopDemo()
    Dim i As Long, ws As Worksheet, total As Double

    For i = 1 To 5                                   ' counted loop
        Debug.Print "row " & i
    Next i

    For Each ws In ThisWorkbook.Worksheets           ' loop a collection
        Debug.Print "sheet: " & ws.Name
    Next ws

    Set ws = ThisWorkbook.Worksheets("Master")
    i = 2                                            ' row 1 is the header
    Do While ws.Cells(i, 1).Value <> ""              ' stop at the first empty cell in column A
        total = total + ws.Cells(i, 11).Value        ' column 11 (K) is net_revenue
        i = i + 1
    Loop
    Debug.Print "total " & Format(total, "#,##0.00") & " over " & (i - 2) & " rows"
End Sub
```

<<OUT:LoopDemo>>

- **`Dim i As Long, ws As Worksheet, total As Double`** declares three variables on one line, separated by commas. A `Double` starts at 0.
- **`For i = 1 To 5` … `Next i`** runs the lines between five times, with `i` = 1, 2, 3, 4, 5. Use it when you know how many times (rows 2 to the last row).
- **`For Each ws In ThisWorkbook.Worksheets` … `Next ws`** visits every sheet in the workbook in turn, putting each one in `ws`. Use it for any collection: sheets, cells in a range, files.
- **`Do While … Loop`** repeats as long as the condition is true, so it suits "until the data runs out". It starts at row 2, because row 1 holds the header text `net_revenue`, and adding text to a number stops the macro with a **Type mismatch** error.
- **`i = i + 1`** moves to the next row. Always make sure something changes inside a `Do` loop, or it never ends (**Ctrl+Break** stops a runaway macro).
- **`Exit For`** and **`Exit Do`** leave a loop early, for example as soon as you've found what you were looking for.
- **`Step -1`** (`For r = lastRow To 2 Step -1`) counts backwards, which is what you need when deleting rows: deleting row 5 moves row 6 up, so a forward loop skips it.

### Arrays and collections

An **array** is one variable holding a numbered list of values. A **`Dictionary`** holds pairs: a key and its value.

```vb
Sub ArrayDemo()
    Dim branches As Variant, i As Long
    branches = Array("Mumbai HO", "Bengaluru", "Delhi", "Kolkata")

    For i = LBound(branches) To UBound(branches)
        Debug.Print i & ": " & branches(i)
    Next i

    Dim targets As Object
    Set targets = CreateObject("Scripting.Dictionary")     ' a lookup table
    targets("Mumbai HO") = 150000000#
    targets("Bengaluru") = 120000000#
    Debug.Print targets("Bengaluru") & " " & targets.Exists("Delhi")
End Sub
```

<<OUT:ArrayDemo>>

- **`Array(…)`** builds a list, and **`branches(i)`** reads item number `i`. The first item is number **0**, not 1: VBA counts positions in an `Array` from zero, which is why the output starts `0: Mumbai HO`.
- **`LBound`** and **`UBound`** give the first and last position numbers (0 and 3 here), so the loop fits the list whatever its length.
- **`CreateObject("Scripting.Dictionary")`** makes a new dictionary. It's an object, so it needs **`Set`**, and its variable is declared `As Object`.
- **`targets("Mumbai HO") = 150000000#`** stores a value under a key; **`targets("Bengaluru")`** reads it back. **`.Exists("Delhi")`** answers `True` or `False`, and it's `False` here because no target was stored for Delhi.

A dictionary works like the two-column lookup table of Chapter 10's first lookup (section 10.10): look up a key, get its value, and check with `.Exists()` before you look up. It's the right tool for "map branch spelling to standard name" and for counting.

### Procedures with arguments and return values

```vb
Function NetLine(ByVal quantity As Long, ByVal unitPrice As Double, _
                 Optional ByVal discountPct As Double = 0) As Double
    NetLine = quantity * unitPrice * (1 - discountPct / 100)
End Function

Sub UseIt()
    Debug.Print "45 at 430, 5% off: " & NetLine(45, 430, 5)
    Debug.Print "10 at 290, no discount: " & NetLine(10, 290)
End Sub
```

<<OUT:UseIt>>

- **`_`** at the end of a line (a space, then an underscore) says "this statement continues on the next line". It keeps long lines readable.
- **`Function NetLine(…) As Double`**: a `Function` returns a value, and `As Double` after the brackets says what type. It returns it **by assigning to its own name**: `NetLine = …`.
- **`Optional ByVal discountPct As Double = 0`** is an argument the caller may leave out; then it's 0. That's why `NetLine(10, 290)` works with only two values.
- **`NetLine(45, 430, 5)`** has brackets because `UseIt` uses the answer, following the rule you met with `CheckTarget`.

**Why `ByVal`?** Without it, VBA passes arguments **by reference** (`ByRef`, the default): the procedure works on the caller's own variable and can change it. `ByVal` hands over a copy. Watch the difference:

```vb
Sub DoubleIt(n As Long)                  ' no ByVal: works on the caller's variable
    n = n * 2
End Sub

Sub DoubleCopy(ByVal n As Long)          ' ByVal: works on a copy
    n = n * 2
End Sub

Sub ByRefDemo()
    Dim x As Long
    x = 5
    DoubleCopy x
    Debug.Print "after DoubleCopy: " & x
    DoubleIt x
    Debug.Print "after DoubleIt: " & x
End Sub
```

<<OUT:ByRefDemo>>

`DoubleCopy` doubled its own copy and left `x` alone; `DoubleIt` changed `x` itself. Write `ByVal` unless you really want the procedure to change the caller's variable, which is rare. (By reference also means the types must match exactly: passing a `Variant` to `DoubleIt` stops with "ByRef argument type mismatch".)

Two habits from here on: **one procedure, one job**, and **no magic numbers** — put the folder path, the sheet name, and the thresholds in **`Const`** declarations (named values that never change) at the top of the module, where the next person can find them.

```vb
Private Const SOURCE_FOLDER As String = "C:\Riverstone\branch_files\"
Private Const MASTER_SHEET As String = "Master"
```

`Private` means only procedures in this module can see the name.

---

## 19.5 Excel's object model

VBA drives Excel by talking to **objects** arranged in a hierarchy: `Application` (Excel itself) → `Workbook` → `Worksheet` → `Range` (one cell or a block of cells). Each has **properties** (things it is: `.Name`, `.Value`, `.Font.Bold`) and **methods** (things it does: `.Copy`, `.Delete`, `.SaveAs`). A dot joins an object to its property or method, and to the objects inside it.

Experiments that change cells belong on the **Scratch** sheet, never on your real data:

```vb
Sub ObjectBasics()
    Dim wb As Workbook, ws As Worksheet, rng As Range

    Set wb = ThisWorkbook                          ' the workbook holding this code
    Set ws = wb.Worksheets("Scratch")              ' by name, not by position
    Set rng = ws.Range("A1:K1")

    ws.Range("A1").Value = "order_item_id"
    ws.Cells(2, 1).Value = 184000                  ' Cells(row, column): easier in loops
    rng.Font.Bold = True
    Debug.Print ws.Name & " | " & ws.Cells(1, 1).Value & " | " & ws.Cells(2, 1).Value & " | " & rng.Address
End Sub
```

<<OUT:ObjectBasics>>

- **`ThisWorkbook`** is the workbook the code is stored in, whichever workbook happens to be in front of the user.
- **`wb.Worksheets("Scratch")`** picks a sheet by its name. `Worksheets(1)` would pick the first sheet, whichever that is today, so names are safer.
- **`ws.Range("A1:K1")`** is a block of cells by address; **`ws.Cells(2, 1)`** is one cell by row and column number (row 2, column 1 = A2), which is easier when the row is a variable in a loop.
- **`.Value = …`** writes into a cell; reading `.Value` gives what's in it. **`rng.Font.Bold = True`** sets a property of the range's font.
- **`rng.Address`** is the range's address as text, with `$` signs like an absolute reference in a formula (Chapter 10).

### The five things you'll write constantly

This one reads from **Master** but changes only **Scratch**:

```vb
Sub RangeToolkit()
    Dim ws As Worksheet, lastRow As Long, lastCol As Long
    Set ws = ThisWorkbook.Worksheets("Master")

    lastRow = ws.Cells(ws.Rows.Count, "A").End(xlUp).Row          ' last used row in column A
    lastCol = ws.Cells(1, ws.Columns.Count).End(xlToLeft).Column  ' last used column in row 1
    Debug.Print "last row " & lastRow & ", last column " & lastCol

    Dim data As Range
    Set data = ws.Range(ws.Cells(2, 1), ws.Cells(lastRow, lastCol))   ' the data without the header
    Debug.Print data.Address & " holds " & data.Rows.Count & " rows"
    Debug.Print "the block around A1 is " & ws.Range("A1").CurrentRegion.Address

    Dim scratch As Worksheet
    Set scratch = ThisWorkbook.Worksheets("Scratch")
    scratch.Rows(1).Insert                                         ' insert, delete, clear
    scratch.Rows(1).Delete
    scratch.Range("L:L").ClearContents
End Sub
```

<<OUT:RangeToolkit>>

- **`ws.Cells(ws.Rows.Count, "A").End(xlUp).Row`** is the most useful line in VBA. `ws.Rows.Count` is the number of the sheet's last row (1,048,576); `Cells(…, "A")` is that cell in column A; `.End(xlUp)` is "press Ctrl+Up from there"; and `.Row` is the row number where it lands. It finds the last row whatever the size of this month's file.
- **`.End(xlToLeft).Column`** does the same along row 1, from the far right, and gives the last column number: 11 is column K.
- **`ws.Range(ws.Cells(2, 1), ws.Cells(lastRow, lastCol))`** is the block from its top-left cell to its bottom-right cell: every data row, without the header.
- **`.CurrentRegion`** is the block of filled cells around A1, the same block **Ctrl+A** selects.
- **`.Rows(1).Insert`**, **`.Rows(1).Delete`** and **`.Range("L:L").ClearContents`** insert a row, delete it, and empty column L. Run these only where it's safe, which is why they point at Scratch.

Use `UsedRange` only when you must: it can include formatted-but-empty cells and lie to you.

### Avoid `Select` and `Activate`

Recorded code selects because you did. Written code shouldn't: it's slower, it depends on what's in front of the user, and it breaks when a dialog steals focus.

```vb
' recorded
Sheets("Master").Select
Range("A1").Select
Selection.Value = "Total"

' written
ThisWorkbook.Worksheets("Master").Range("A1").Value = "Total"
```

The same for `ActiveWorkbook` and `ActiveSheet`: use them only when you really do mean "whatever the user has open", and assign them to a variable straight away.

### `With`, for readability

```vb
Sub FormatHeader(ByVal ws As Worksheet, ByVal lastCol As Long)
    With ws.Range(ws.Cells(1, 1), ws.Cells(1, lastCol))
        .Font.Bold = True
        .Font.Color = RGB(255, 255, 255)
        .Interior.Color = RGB(15, 92, 140)
        .HorizontalAlignment = xlCenter
        .EntireColumn.AutoFit
    End With
End Sub
```

`With` names an object once; every line inside that starts with a dot belongs to it. It saves repetition and makes the block clearly about one thing, the closest VBA gets to a paragraph. `RGB(red, green, blue)` mixes a colour from three numbers between 0 and 255; `.Interior` is the cell's fill. To try it, type `FormatHeader ThisWorkbook.Worksheets("Master"), 11` in the Immediate window: Master's header row turns white on blue.

---

## 19.6 The everyday toolkit

Here is the work an analyst actually automates, in the order it usually happens. All of it runs against `companion/ch19/branch_files/`: twelve workbooks, four branch sales offices × three months of Q4 2025, named `Riverstone_<branch>_<month>.xlsx`, from `Riverstone_Bengaluru_2025-10.xlsx` to `Riverstone_Mumbai_HO_2025-12.xlsx`. Copy the folder to `C:\Riverstone\branch_files\` (or change the path in the code). Each file has one sheet, **Sales**, with the same eleven columns:

| Column | 1 (A) | 2 (B) | 3 (C) | 4 (D) | 5 (E) | 6 (F) |
|---|---|---|---|---|---|---|
| Header | `order_item_id` | `order_id` | `order_date` | `customer_code` | `product_id` | `quantity` |

| Column | 7 (G) | 8 (H) | 9 (I) | 10 (J) | 11 (K) | 12 (L) |
|---|---|---|---|---|---|---|
| Header | `unit_price` | `discount_pct` | `status` | `sales_rep` | `net_revenue` | `source_file` (added by the macro) |

The code below refers to columns by these numbers: 4 for `customer_code`, 9 for `status`, 11 for `net_revenue`. The branch and the month aren't columns; they're in the file name, which the macro keeps in column 12.

### Consolidate every file in a folder

This goes in a new module of your practice workbook. Its **Master** sheet is emptied and refilled with all twelve files.

```vb
Option Explicit

Private Const SOURCE_FOLDER As String = "C:\Riverstone\branch_files\"
Private Const DATA_SHEET As String = "Sales"
Private Const EXPECTED_FILES As Long = 12

Sub ConsolidateBranchFiles()
    Dim master As Worksheet, src As Workbook, srcWs As Worksheet
    Dim fileName As String, nextRow As Long, lastRow As Long, lastCol As Long
    Dim filesRead As Long

    Application.ScreenUpdating = False
    Application.DisplayAlerts = False

    Set master = ThisWorkbook.Worksheets("Master")
    master.Cells.ClearContents
    nextRow = 1

    fileName = Dir(SOURCE_FOLDER & "*.xlsx")           ' Dir lists files one at a time
    Do While fileName <> ""
        If Left(fileName, 2) <> "~$" Then              ' skip Excel's lock files
            Set src = Workbooks.Open(SOURCE_FOLDER & fileName, ReadOnly:=True)
            Set srcWs = src.Worksheets(DATA_SHEET)

            lastRow = srcWs.Cells(srcWs.Rows.Count, "A").End(xlUp).Row
            lastCol = srcWs.Cells(1, srcWs.Columns.Count).End(xlToLeft).Column
            Debug.Print fileName & ": " & (lastRow - 1) & " rows"

            If nextRow = 1 Then                        ' copy the header once, from the first file
                srcWs.Range(srcWs.Cells(1, 1), srcWs.Cells(1, lastCol)).Copy master.Cells(1, 1)
                master.Cells(1, lastCol + 1).Value = "source_file"
                nextRow = 2
            End If

            If lastRow >= 2 Then
                srcWs.Range(srcWs.Cells(2, 1), srcWs.Cells(lastRow, lastCol)).Copy master.Cells(nextRow, 1)
                master.Range(master.Cells(nextRow, lastCol + 1), _
                             master.Cells(nextRow + lastRow - 2, lastCol + 1)).Value = fileName
                nextRow = nextRow + lastRow - 1
            End If

            src.Close SaveChanges:=False
            filesRead = filesRead + 1
        End If
        fileName = Dir                                  ' Dir with no argument returns the next file
    Loop

    Application.DisplayAlerts = True
    Application.ScreenUpdating = True

    If filesRead <> EXPECTED_FILES Then                 ' fail loudly: never total the wrong files
        Err.Raise 513, "ConsolidateBranchFiles", _
                  "Expected " & EXPECTED_FILES & " files, read " & filesRead
    End If
    MsgBox filesRead & " files consolidated, " & Format(nextRow - 2, "#,##0") & " data rows.", vbInformation
End Sub
```

The Immediate window lists each file as it's read. Windows returns the names in alphabetical order:

<<OUT:Consolidate>>

Then a message box says **12 files consolidated, 25,832 data rows.** with an information icon.

Line by line, the parts you haven't met:

- **`Application.ScreenUpdating = False`** stops Excel redrawing the screen while the macro works: on twelve files this is the difference between four seconds and forty. **`Application.DisplayAlerts = False`** stops Excel asking questions (such as "save changes?") in the middle of the run. Both are switched back to `True` near the end.
- **`master.Cells.ClearContents`** empties every cell of Master, so a second run doesn't add to the first.
- **`Dir(SOURCE_FOLDER & "*.xlsx")`** returns the name of the first file in the folder that matches the pattern (`*` means "anything", as in Chapter 10's wildcards), so `_notes.txt` is ignored. **`Dir`** with no argument, at the bottom of the loop, returns the next name, and `""` when there are no more. (`Dir` is old but everywhere; `FileSystemObject`, via `CreateObject("Scripting.FileSystemObject")`, is the richer alternative.)
- **`If Left(fileName, 2) <> "~$" Then`**: while someone has a workbook open, Excel keeps a small **lock file** beside it, named `~$` plus the file's name. `Dir` skips hidden files, and Excel normally hides lock files, but this one line makes the macro safe even when a lock file isn't hidden: opening one as a workbook would stop the macro.
- **`Workbooks.Open(…, ReadOnly:=True)`** opens a file without being able to change it, so the macro can't accidentally modify a branch's file, and it opens even if someone else has it open. **`ReadOnly:=True`** is a **named argument**: `name:=value` sets one setting by name, so you don't have to count positions. `SaveChanges:=False` in `src.Close` works the same way.
- **`Debug.Print fileName & ": " & (lastRow - 1) & " rows"`** logs each file's row count (the last row minus the header), so you can check it against `expected_results.md` and see at once if a file was skipped or read twice.
- **The header is copied once**, from the first file; after that, data starts at row 2 in every file. **`.Copy master.Cells(nextRow, 1)`** copies a block and pastes it with its top-left corner at that cell.
- **A `source_file` column** records where each row came from: the second `If` writes the file name into column 12 of every row just pasted. Without it, you can't trace a wrong number back, and you can't tell whether a file was consolidated twice.
- **`nextRow = nextRow + lastRow - 1`** moves the paste point down by the number of data rows just added.
- **`Err.Raise 513, "ConsolidateBranchFiles", "…"`** stops the macro with your own error if it didn't read exactly twelve files. `513` is the error's number (VBA leaves 513 and above for your own errors), the second value names where it happened, and the third is the message. Section 19.9 shows how a calling procedure catches it.

**What happens if you change it** by saving a copy of one file into the folder as `Riverstone_Kolkata_2025-11 (2).xlsx`? The loop reads thirteen files, and instead of the message box the macro stops with **Expected 12 files, read 13**. That's exactly the check the macro in this chapter's "In the real world" story didn't have.

On the companion files, this produces **25,832 data rows**. `expected_results.md` lists each file's row count so you can check the macro didn't skip one, and the complete set: **24,738 non-cancelled rows**, net revenue **₹42,38,72,808.00**.

### Clean and standardize while you're there

```vb
Sub CleanMaster()
    Dim ws As Worksheet, lastRow As Long, r As Long
    Dim statusMap As Object, raw As String, unmapped As Long

    Set ws = ThisWorkbook.Worksheets("Master")
    lastRow = ws.Cells(ws.Rows.Count, "A").End(xlUp).Row

    Set statusMap = CreateObject("Scripting.Dictionary")
    statusMap("delivered") = "Delivered"
    statusMap("dlvd") = "Delivered"
    statusMap("cancelled") = "Cancelled"
    statusMap("canceled") = "Cancelled"
    statusMap("cxl") = "Cancelled"
    statusMap("shipped") = "Shipped"
    statusMap("pending") = "Pending"

    ws.Columns(4).NumberFormat = "@"                     ' column D holds text, so codes keep their zeros
    For r = 2 To lastRow
        raw = LCase(Trim(ws.Cells(r, 9).Value))          ' column I = status
        If statusMap.Exists(raw) Then
            ws.Cells(r, 9).Value = statusMap(raw)
        Else
            ws.Cells(r, 9).Interior.Color = RGB(255, 235, 200)   ' flag, don't guess
            unmapped = unmapped + 1
        End If
        ws.Cells(r, 4).Value = Format(ws.Cells(r, 4).Value, "0000")   ' customer_code as four digits
    Next r
    Debug.Print (lastRow - 1) & " rows cleaned, " & unmapped & " statuses not in the map"
End Sub
```

<<OUT:CleanMaster>>

- **`LCase(Trim(…))`** removes spaces at both ends and lower-cases the text, like `TRIM` and `LOWER` in Chapter 10, so `" Delivered "` and `"DELIVERED"` both become `delivered` before the lookup.
- **`statusMap.Exists(raw)`**: if the cleaned value is a known spelling, the standard name replaces it; if not, the cell is coloured and counted instead of guessed. On these files every status is already standard, so the count is 0; the check is how you find the day a branch starts writing something new.
- **`ws.Columns(4).NumberFormat = "@"`** formats column D as **Text** before anything is written to it. This matters because of Chapter 10's lesson (section 10.3) that what a cell *contains* and what it *shows* are different things. `Format(…, "0000")` produces the text `"0237"`, but writing that text into a General cell makes Excel read it as the number 237, and the zero is gone. In a Text cell it stays `0237`.

This is normalize-then-map: tidy the value, look it up, and **flag what isn't in the map** rather than passing it through. Section 19.10 shows how to do the same thing much faster with an array.

### Summarize, with a pivot table

```vb
Sub BuildSummaryPivot()
    Dim ws As Worksheet, pvtWs As Worksheet, lastRow As Long, lastCol As Long
    Dim cache As PivotCache, pvt As PivotTable

    Set ws = ThisWorkbook.Worksheets("Master")
    lastRow = ws.Cells(ws.Rows.Count, "A").End(xlUp).Row
    lastCol = ws.Cells(1, ws.Columns.Count).End(xlToLeft).Column

    Application.DisplayAlerts = False                    ' no "delete this sheet?" question
    On Error Resume Next                                 ' the sheet may not exist yet...
    ThisWorkbook.Worksheets("Summary").Delete
    On Error GoTo 0                                      ' ...from here, errors stop the macro again
    Application.DisplayAlerts = True
    Set pvtWs = ThisWorkbook.Worksheets.Add
    pvtWs.Name = "Summary"

    Set cache = ThisWorkbook.PivotCaches.Create( _
        SourceType:=xlDatabase, _
        SourceData:=ws.Range(ws.Cells(1, 1), ws.Cells(lastRow, lastCol)))
    Set pvt = cache.CreatePivotTable(TableDestination:=pvtWs.Range("A3"), TableName:="SalesPivot")

    With pvt
        .PivotFields("source_file").Orientation = xlRowField
        .PivotFields("status").Orientation = xlColumnField
        .AddDataField .PivotFields("net_revenue"), "Net revenue", xlSum
        .DataBodyRange.NumberFormat = "#,##0"
    End With

    pvtWs.Range("A1").Value = "Riverstone Q4 2025 — net revenue by file and status"
    pvtWs.Range("A1").Font.Bold = True
End Sub
```

- **Deleting a sheet** normally makes Excel ask "delete this sheet?" and wait for a click. **`Application.DisplayAlerts = False`** just before the delete answers for you; it's switched back on straight after.
- **`On Error Resume Next`** tells VBA to ignore an error and carry on with the next line. The first time the macro runs there's no Summary sheet to delete, and that error doesn't matter. **`On Error GoTo 0`** switches normal error handling back on at once, so a real problem later still stops the macro. Keep the two lines this close together (more in section 19.9).
- **`Worksheets.Add`** adds a new sheet, and **`.Name = "Summary"`** names it.
- **`PivotCaches.Create(…)`** stores the Master data for a pivot table (Chapter 11's pivot tables, built by code), and **`CreatePivotTable`** places the table at A3 of Summary. The `With` block then does what you'd drag by hand: `source_file` to **Rows**, `status` to **Columns**, and the sum of `net_revenue` to **Values**, shown as whole rupees with separators.

The result on Summary is one row per branch file (twelve rows) and one column per status (Cancelled, Delivered, Pending, Shipped), with a grand total of **44,25,77,334** across all statuses; take the Cancelled column out and it's the ₹42,38,72,808 of non-cancelled revenue. (Excel's `#,##0` format groups digits in threes, so on screen it shows 442,577,334.)

Pivot tables in VBA are fiddly and worth it: the alternative is `SUMIFS` formulas that someone has to drag. If the summary needs to look a specific way every month, build it once by hand, record the formatting, and paste the useful parts in here.

### Save as PDF

```vb
Function SaveSummaryAsPdf() As String
    Dim path As String
    path = ThisWorkbook.Path & Application.PathSeparator & _
           "Riverstone_Q4_2025_summary_" & Format(Date, "yyyy-mm-dd") & ".pdf"

    ThisWorkbook.Worksheets("Summary").ExportAsFixedFormat _
        Type:=xlTypePDF, FileName:=path, Quality:=xlQualityStandard, OpenAfterPublish:=False

    SaveSummaryAsPdf = path
End Function
```

- **`ThisWorkbook.Path`** is the folder the workbook is saved in, and **`Application.PathSeparator`** is `\` on Windows, so the PDF lands beside the workbook.
- **`Format(Date, "yyyy-mm-dd")`** puts today's date in the name. Run on 5 January 2026 from a workbook saved in `C:\Riverstone`, the function returns `C:\Riverstone\Riverstone_Q4_2025_summary_2026-01-05.pdf`.
- **`ExportAsFixedFormat`** writes the PDF; its named arguments say the type (PDF), the file name, the quality, and not to open it afterwards.

`ExportAsFixedFormat` on a sheet exports that sheet; on the workbook, everything. Set the print area, orientation, and `FitToPagesWide` first (`ws.PageSetup.…`, as in Chapter 10's print settings), or the PDF arrives as nine pages of columns.

---

## 19.7 Sending the report by Outlook

The email this section builds carries its numbers in the body, not only in an attachment, and the body of an email is written in HTML. This is the first HTML in the book, so here is what you need.

> **HTML in ten minutes.** **HTML** is the plain-text language web pages and formatted emails are written in. Text is wrapped in **tags**: a tag in angle brackets starts something, and the same tag with a slash ends it. `<p>Good morning,</p>` is one paragraph; `<b>12</b>` shows 12 in bold; `<h3>Enquiries</h3>` is a small heading; `<br>` is a line break and has no closing tag. A tag can carry **attributes** inside its opening angle brackets, as `name='value'` pairs. The one you'll use most is `style`, which holds display settings separated by semicolons: `<p style='color:#5b6475;font-size:12px'>` is a grey paragraph in 12-pixel text (`#5b6475` is a colour code for that grey: six characters, two each for red, green and blue). A table is three tags nested inside each other: `<table>` around the whole table, `<tr>` (table row) around each row, and `<td>` (table data) around each cell, with `<th>` for a header cell. This fragment:
>
> ```
> <table>
>   <tr><td>Net revenue</td><td><b>₹42,38,72,808.00</b></td></tr>
>   <tr><td>Order lines</td><td><b>25,832</b></td></tr>
> </table>
> ```
>
> shows in the email as a two-row, two-column table:
>
> | | |
> |---|---|
> | Net revenue | **₹42,38,72,808.00** |
> | Order lines | **25,832** |
>
> In VBA, the HTML is a text value, so it sits inside double quotes. That's why the attributes use **single** quotes (`style='…'`): a double quote would end the VBA text too early.

```vb
Sub EmailSummary(ByVal pdfPath As String, ByVal netRevenue As Double, ByVal rowCount As Long)
    Dim outlookApp As Object, mail As Object
    Dim rupee As String, bodyHtml As String

    Set outlookApp = CreateObject("Outlook.Application")     ' late binding: no reference needed
    Set mail = outlookApp.CreateItem(0)                      ' 0 = olMailItem, a new email
    rupee = ChrW(8377)                                       ' the rupee sign, by its Unicode number

    ' 1. the greeting
    bodyHtml = "<p>Good morning,</p>" & _
        "<p>Riverstone's Q4 2025 sales summary is attached.</p>"

    ' 2. the table of headline numbers
    bodyHtml = bodyHtml & _
        "<table style='border-collapse:collapse;font-family:Segoe UI,Arial;font-size:13px'>" & _
        "<tr><td style='padding:4px 12px;color:#5b6475'>Net revenue (non-cancelled)</td>" & _
        "<td style='padding:4px 12px;font-weight:bold'>" & rupee & Format(netRevenue, "#,##0.00") & "</td></tr>" & _
        "<tr><td style='padding:4px 12px;color:#5b6475'>Order lines consolidated</td>" & _
        "<td style='padding:4px 12px;font-weight:bold'>" & Format(rowCount, "#,##0") & "</td></tr>" & _
        "</table>"

    ' 3. the footer
    bodyHtml = bodyHtml & _
        "<p style='color:#5b6475;font-size:12px'>Generated automatically from the twelve branch files on " & _
        Format(Now, "dd mmm yyyy HH:mm") & ".</p>"

    With mail
        .To = "sales.managers@riverstone.example"
        .Subject = "Riverstone Q4 2025 sales summary"
        .HTMLBody = bodyHtml
        .Attachments.Add pdfPath
        .Display                      ' .Send sends it immediately; .Display lets a human look first
    End With
End Sub
```

Called with the consolidation's results (section 19.9 does this), it opens a draft email to `sales.managers@riverstone.example`, subject *Riverstone Q4 2025 sales summary*, with the PDF attached and this in the body: "Good morning," and a line saying the summary is attached; a small table reading **Net revenue (non-cancelled) ₹423,872,808.00** and **Order lines consolidated 25,832**; and a grey footer with the date and time it was generated.

- **Late binding** (`CreateObject("Outlook.Application")`, with the variable declared `As Object`) starts or connects to Outlook without adding a reference to a specific Outlook version, so the file works on other machines. **`CreateItem(0)`** makes a new, empty email.
- **`ChrW(8377)`** is the character with Unicode number 8377, the rupee sign (Chapter 2's Unicode table). Typing `₹` straight into the VBA editor doesn't work: the editor stores only a limited set of characters, and `₹` turns into `?`. Building it with `ChrW` avoids that.
- **`bodyHtml = bodyHtml & …`** adds the next piece to the end of the text built so far, so the body grows in three steps: greeting, table, footer.
- **`Format(netRevenue, "#,##0.00")`** groups digits in threes, so the email shows 423,872,808.00. VBA's `Format` patterns have no Indian lakh grouping; this book writes the same amount as ₹42,38,72,808.00.
- **`.To`, `.Subject`, `.HTMLBody`** fill in the email; **`.Attachments.Add pdfPath`** attaches the file at that path.
- **`.Display` while developing, `.Send` when you trust it.** An automation that emails the wrong list is worse than no automation.
- **HTML in the body** beats an attachment nobody opens (Chapter 20 goes further). Keep it to inline styles and tables: Outlook's rendering engine ignores most modern styling.
- **`.CC`, `.BCC`, and `.SentOnBehalfOfName`** cover the rest. For a shared mailbox, ask IT rather than storing someone's credentials.

> **Watch out: this drives the Outlook installed on your machine.** It needs Outlook open (or it starts it), it won't run on a server without Outlook, and modern security tooling may prompt. For unattended sending, use the Microsoft 365 route in Chapter 20 instead.

---

## 19.8 Custom functions and a simple form

### A UDF: your own worksheet function

A **UDF** (user-defined function) is a VBA `Function` you can use in a cell like `SUM`.

```vb
Public Function REBATEPCT(ByVal annualValue As Double) As Double
    ' Riverstone's loyalty rebate: 0% standard, 1% from 2,50,000, 2% from 4,00,000
    Select Case annualValue
        Case Is >= 400000
            REBATEPCT = 2
        Case Is >= 250000
            REBATEPCT = 1
        Case Else
            REBATEPCT = 0
    End Select
End Function

Sub TestRebate()
    Debug.Print "1,80,000 -> " & REBATEPCT(180000)
    Debug.Print "2,50,000 -> " & REBATEPCT(250000)
    Debug.Print "3,99,999 -> " & REBATEPCT(399999)
    Debug.Print "4,00,000 -> " & REBATEPCT(400000)
End Sub
```

<<OUT:TestRebate>>

**`Public`** makes the function visible outside its module, which is what lets Excel find it. Put it in a normal module and it appears in Excel as `=REBATEPCT(B2)`: type `=REBATEPCT(250000)` in a cell and it shows 1. UDFs are a good way to give the business one blessed version of a rule, instead of the same nested `IF` copied into forty workbooks. (Chapter 11's `LAMBDA` does a similar job without VBA, in Excel versions that have it.)

Limits worth knowing: a UDF can read cells but shouldn't change them; it recalculates whenever Excel wants, so it must be fast; it isn't available in Excel on the web; and a workbook full of UDFs is slower than the same logic in Power Query or as a helper column. `Application.Volatile` forces recalculation on every change, and is almost always a mistake.

### A UserForm, when a dialog is the better answer

For a macro that needs a choice ("which month?"), start with the built-in dialogs:

```vb
Sub AskForMonth()
    Dim answer As String
    answer = InputBox("Which month? (YYYY-MM)", "Riverstone consolidation", Format(Date, "yyyy-mm"))
    If answer = "" Then Exit Sub                  ' the user pressed Cancel
    If Not answer Like "####-##" Then
        MsgBox "Please use the format 2025-12.", vbExclamation
        Exit Sub
    End If
    Debug.Print "running for " & answer
End Sub

Sub PickFolder()
    With Application.FileDialog(msoFileDialogFolderPicker)
        .Title = "Choose the folder with the branch files"
        If .Show = -1 Then Debug.Print .SelectedItems(1)
    End With
End Sub
```

Run `AskForMonth` and type `2025-12`: the Immediate window shows `running for 2025-12`. Type `Dec 2025` instead and a warning box says *Please use the format 2025-12.*

- **`InputBox(prompt, title, default)`** shows a box with a text field and returns what the user typed, or `""` if they pressed **Cancel**. The third value fills the field in advance with this month.
- **`Exit Sub`** leaves the procedure at once.
- **`answer Like "####-##"`** checks text against a pattern: `#` is any digit, `?` any single character, and `*` any run of characters. `Not` turns the answer around, so the warning shows when the text *doesn't* fit.
- **`vbExclamation`** is one of VBA's built-in named numbers, called **constants**: it tells `MsgBox` to show a warning icon. `vbInformation` shows an "i", `vbCritical` a red cross, and `vbCrLf` (section 19.9) is a line break inside text.
- **`Application.FileDialog(msoFileDialogFolderPicker)`** is Windows' own "choose a folder" dialog. **`.Show`** opens it and returns **-1** when the user clicks OK (0 for Cancel), and **`.SelectedItems(1)`** is the folder they chose.

`InputBox`, `MsgBox`, and `Application.FileDialog` cover most needs and cost one line each. A **UserForm** (**Insert → UserForm** in the editor, then drag labels, text boxes, combo boxes, and buttons) is worth it when there are several inputs at once: a month, a branch, and a checkbox for "email it". Name the controls properly (`cmbBranch`, `txtMonth`, `btnRun`), write the code in the form's `btnRun_Click` event, and keep the actual work in a module the form calls, so the logic can be tested without the form.

---

## 19.9 Debugging and error handling

### Debugging

| Tool | How | Use |
|---|---|---|
| **Breakpoint** | Click the gray margin, or **F9** | Pause on a line |
| **Step Into / Over / Out** | **F8** / **Shift+F8** / **Ctrl+Shift+F8** | Walk through line by line |
| **Immediate window** | **Ctrl+G**, then `?expression` | Ask what a value is right now |
| **Locals window** | **View → Locals** | See every variable in scope |
| **Watch** | Right-click a variable → Add Watch | Stop when a value changes or meets a condition |
| **`Debug.Print`** | In the code | A log of what happened, without dialogs |
| **`Stop`** | In the code | A breakpoint that travels with the file |

The routine when a macro misbehaves: set a breakpoint before the suspect line, run, then step with **F8** while watching Locals. Nine times out of ten the problem is a variable that isn't what you assumed: the wrong sheet, an empty string, a number stored as text.

### Error handling

This is the one procedure that runs the whole job: consolidate, clean, summarize, save the PDF, and email it. If any step fails, nothing is sent.

```vb
Sub RunConsolidation()
    Dim errorLog As String, calcMode As XlCalculation
    Dim ws As Worksheet, rowCount As Long, netRevenue As Double, pdfPath As String

    calcMode = Application.Calculation         ' remember the user's calculation setting
    On Error GoTo Failed                       ' from here, any error jumps to the label

    Application.ScreenUpdating = False
    Application.Calculation = xlCalculationManual
    ConsolidateBranchFiles                     ' stops with an error unless it read 12 files
    CleanMaster
    BuildSummaryPivot

    Set ws = ThisWorkbook.Worksheets("Master")
    rowCount = ws.Cells(ws.Rows.Count, "A").End(xlUp).Row - 1
    netRevenue = Application.WorksheetFunction.SumIfs(ws.Range("K:K"), ws.Range("I:I"), "<>Cancelled")
    pdfPath = SaveSummaryAsPdf()
    EmailSummary pdfPath, netRevenue, rowCount ' reached only if every step above worked
    LogLine "sent: " & rowCount & " rows, net revenue " & Format(netRevenue, "0.00")

CleanUp:
    Application.ScreenUpdating = True
    Application.DisplayAlerts = True
    Application.Calculation = calcMode         ' put back what the user had
    Exit Sub                                    ' stop before falling into the handler

Failed:
    errorLog = "Error " & Err.Number & ": " & Err.Description & " (in " & Err.Source & ")"
    Debug.Print errorLog
    LogLine errorLog
    MsgBox errorLog & vbCrLf & vbCrLf & "Nothing was sent.", vbCritical, "Consolidation failed"
    Resume CleanUp                              ' always restore Excel's settings
End Sub
```

On the twelve companion files it runs to the end: Master fills, Summary is rebuilt, the PDF is saved, the draft email opens with ₹423,872,808.00 and 25,832 rows, and one line is added to the log (below). With the extra `(2)` file in the folder, it stops at the first step instead, and the Immediate window shows:

```
Error 513: Expected 12 files, read 13 (in ConsolidateBranchFiles)
```

A red-cross message box titled *Consolidation failed* says the same, then *Nothing was sent.* on its own line.

- **`calcMode = Application.Calculation`** saves the user's calculation setting (automatic or manual, Chapter 10's calculation mode) before the macro switches it to manual for speed; **`CleanUp`** puts back exactly what was there.
- **`On Error GoTo Failed`** sends control to the line labelled `Failed:` as soon as any error happens. A **label** is a name followed by a colon on its own line. **`Err.Number`**, **`Err.Description`** and **`Err.Source`** say what happened and where; for the check in `ConsolidateBranchFiles`, they're the three values given to `Err.Raise`.
- **`Application.WorksheetFunction.SumIfs(…)`** runs the worksheet's own `SUMIFS` (Chapter 10) from VBA: the sum of column K where column I isn't `Cancelled`.
- **`Resume CleanUp`** leaves the error handler and continues at the `CleanUp:` label, which is how you guarantee `ScreenUpdating` gets switched back on. A macro that fails with screen updating off leaves Excel looking frozen, and that's how users learn to fear macros.
- **`Exit Sub`** above `Failed:` stops a successful run from falling into the handler.
- **`vbCrLf`** is a line break inside text, so `vbCrLf & vbCrLf` leaves a blank line in the message.
- **`On Error Resume Next`** ignores errors and continues. It has exactly two legitimate uses: deleting something that may not exist (as in `BuildSummaryPivot`), and testing whether an object exists. Turn it off immediately afterwards with `On Error GoTo 0`.
- **Fail loudly, not silently.** If the consolidation read eleven files instead of twelve, the macro says so and refuses to email.

A simple log file is worth the ten lines:

```vb
Sub LogLine(ByVal message As String)
    Dim f As Integer
    f = FreeFile
    Open ThisWorkbook.Path & Application.PathSeparator & "macro_log.txt" For Append As #f
    Print #f, Format(Now, "yyyy-mm-dd HH:mm:ss") & " " & message
    Close #f
End Sub
```

- **`FreeFile`** gives a file number that isn't in use; VBA refers to open text files by number.
- **`Open … For Append As #f`** opens `macro_log.txt` beside the workbook for adding lines at the end, and creates it if it doesn't exist yet.
- **`Print #f, …`** writes one line: the date and time, then the message.
- **`Close #f`** closes the file, so the line is saved and the number is free again.

After a successful run, the last line of `macro_log.txt` reads like this (with your own date and time):

<<OUT:LogLine>>

---

## 19.10 Making macros fast

A macro that takes four minutes gets switched off. Three changes usually take it under ten seconds.

### 1. Stop Excel redrawing and recalculating

```vb
Sub FastWrapper()
    Dim calcMode As XlCalculation
    calcMode = Application.Calculation

    Application.ScreenUpdating = False
    Application.Calculation = xlCalculationManual
    Application.EnableEvents = False
    Application.DisplayStatusBar = False

    ' ... the work ...

    Application.DisplayStatusBar = True
    Application.EnableEvents = True
    Application.Calculation = calcMode
    Application.ScreenUpdating = True
End Sub
```

Always restore them (see the error handler above). `EnableEvents = False` also stops your own `Worksheet_Change` code (a procedure Excel runs by itself whenever a cell changes) from firing on every write.

### 2. Work in arrays, not cell by cell

Every read or write to a cell crosses the boundary between VBA and Excel, and that crossing is the expensive part. Read once into an array, work in memory, write once.

```vb
Sub CleanStatusFast()
    Dim ws As Worksheet, lastRow As Long, r As Long
    Dim values As Variant, raw As String
    Dim statusMap As Object

    Set ws = ThisWorkbook.Worksheets("Master")
    lastRow = ws.Cells(ws.Rows.Count, "A").End(xlUp).Row

    Set statusMap = CreateObject("Scripting.Dictionary")
    statusMap("delivered") = "Delivered"
    statusMap("dlvd") = "Delivered"
    statusMap("cancelled") = "Cancelled"
    statusMap("canceled") = "Cancelled"
    statusMap("cxl") = "Cancelled"
    statusMap("shipped") = "Shipped"
    statusMap("pending") = "Pending"

    values = ws.Range(ws.Cells(2, 9), ws.Cells(lastRow, 9)).Value2     ' one read
    For r = 1 To UBound(values, 1)
        raw = LCase(Trim(CStr(values(r, 1))))
        If statusMap.Exists(raw) Then values(r, 1) = statusMap(raw)
    Next r
    ws.Range(ws.Cells(2, 9), ws.Cells(lastRow, 9)).Value2 = values      ' one write
End Sub
```

- **`values = ….Value2`** copies the whole block I2:I25833 into memory in one go. A block read from a sheet always becomes a **grid** with two position numbers, row then column, and both start at **1** (unlike `Array()`, which starts at 0): `values(1, 1)` is I2, `values(2, 1)` is I3, and so on.
- **`UBound(values, 1)`** is the last position in the first dimension, the rows: 25,832 here. (`UBound(values, 2)` would give the columns: 1.)
- **`CStr(…)`** turns whatever is in the cell into text before `Trim` and `LCase`.
- **`If … Then …` on one line** needs no `End If` when the whole action fits on the same line.
- **Writing `.Value2 = values`** puts the whole grid back in one go.

On 25,832 rows, the cell-by-cell version in section 19.6 takes several seconds; this one is effectively instant. `.Value2` is slightly faster than `.Value` and doesn't convert dates and currency, which is usually what you want when moving data around.

To measure it yourself, use **`Timer`**, the number of seconds since midnight:

```vb
Sub TimeBoth()
    Dim t0 As Double
    t0 = Timer
    CleanMaster
    Debug.Print "cell by cell: " & Format(Timer - t0, "0.00") & " seconds"
    t0 = Timer
    CleanStatusFast
    Debug.Print "array: " & Format(Timer - t0, "0.00") & " seconds"
End Sub
```

`Timer - t0` is the time the step took. Your two numbers depend on your computer, so run it and write them down; exercise 20 asks for them.

### 3. Don't do what Excel can do in one line

| Instead of looping to… | Use |
|---|---|
| Copy a range | `src.Copy dest` |
| Find a value | `Range.Find` |
| Filter rows | `AutoFilter` + `SpecialCells(xlCellTypeVisible)` |
| Remove duplicates | `Range.RemoveDuplicates` |
| Sum by a key | A pivot table, or `Application.WorksheetFunction.SumIfs` |
| Sort | `Range.Sort` |
| Delete matching rows | `AutoFilter`, then delete the visible rows in one go |

And the honest version of all of this: **if the job is "combine these files and reshape them", Power Query does it with no code at all** (Chapter 11), refreshes on demand, and doesn't need a macro-enabled file. Reach for VBA when you need the things Power Query can't do: formatting, PDFs, email, and driving Excel itself.

---

## 19.11 Office Scripts: Excel on the web

> **A separate sitting.** Sections 19.11 to 19.14 move the same ideas to two other languages. Take them as your third week. Office Scripts need a Microsoft 365 **business** plan; if you don't have one, read section 19.11 for the ideas, skip the exercises that use it on a first pass, and go on to Apps Script, which any Google account can run.

VBA doesn't run in Excel on the web. **Office Scripts** do: **TypeScript** (JavaScript with types) recorded or written in the browser, stored with your account, and runnable from **Automate → All Scripts** or from a **Power Automate** flow.

| | VBA | Office Scripts |
|---|---|---|
| Runs in | Excel for Windows/Mac (desktop) | Excel on the web (and desktop, by running the cloud script) |
| Language | VBA | TypeScript |
| Stored in | The workbook, or PERSONAL.XLSB | Your OneDrive / SharePoint, with the workbook |
| Can open other files | Yes | No: one workbook per run (Power Automate passes data between steps) |
| Can send email | Yes, via Outlook on the machine | Not directly: Power Automate does it |
| Runs unattended | Only with the machine on and Excel open | Yes, through Power Automate in the cloud |
| Availability | Any Excel with macros enabled | Microsoft 365 business plans (not personal accounts); check your plan |

### Reading TypeScript when you know VBA

The ideas are the ones you just learned; only the spelling changes.

| VBA | TypeScript and JavaScript |
|---|---|
| `Sub Name()` … `End Sub` | `function name() {` … `}`: curly brackets mark where a block starts and ends |
| `If x Then` … `End If` | `if (x) {` … `}`; the condition sits in round brackets |
| `' a comment` | `// a comment` |
| `Dim total As Double` | `let total = 0;` (a value you'll change) or `const sheet = …;` (a name you won't point anywhere else) |
| `Not x`, `<>`, `=` in a test | `!x`, `!==`, `===` |
| `For r = 0 To n - 1` … `Next r` | `for (let r = 0; r < n; r++) {` … `}`: start; keep going while; step (`r++` adds 1) |
| `total = total + 1` | `total++` |
| `"Rows: " & n` | `` `Rows: ${n}` ``: text in back-quotes, with each value inside `${ }` |
| `Exit Sub` | `return;` |
| `Debug.Print` | `console.log(…)` in Office Scripts, `Logger.log(…)` in Apps Script |
| `As Worksheet` | `: ExcelScript.Worksheet`: the type comes after a colon |

A **semicolon** ends each statement, and **positions count from 0**: the first row is row 0 and the first column is column 0.

The same header formatting as section 19.2:

```ts
function main(workbook: ExcelScript.Workbook) {
  const sheet = workbook.getWorksheet("Master");
  if (!sheet) {                                   // no such sheet: stop here
    console.log("No Master sheet");
    return;
  }
  const used = sheet.getUsedRange();
  const lastRow = used.getRowCount();
  const lastCol = used.getColumnCount();

  const header = sheet.getRangeByIndexes(0, 0, 1, lastCol);
  header.getFormat().getFont().setBold(true);
  header.getFormat().getFont().setColor("#FFFFFF");
  header.getFormat().getFill().setColor("#0F5C8C");
  sheet.getFreezePanes().freezeRows(1);           // freeze the header row
  used.getFormat().autofitColumns();

  console.log(`formatted ${lastRow} rows, ${lastCol} columns`);
}
```

Run on the consolidated Master sheet (25,832 data rows plus the header, 12 columns), the script's output pane shows:

<<OUT:os_format>>

- **`function main(workbook: ExcelScript.Workbook)`**: every Office Script starts in a function called `main`, and Excel hands it the open workbook as its argument.
- **`workbook.getWorksheet("Master")`** is `ThisWorkbook.Worksheets("Master")`. If there's no such sheet, it gives back **`undefined`** ("nothing") instead of stopping, so **`if (!sheet)`** checks for that, logs a message, and **`return`**s.
- **`getUsedRange()`**, **`getRowCount()`**, **`getColumnCount()`** give the filled block and its size.
- **`getRangeByIndexes(0, 0, 1, lastCol)`** is the range starting at row 0, column 0 (cell A1), one row tall and `lastCol` columns wide: the header row.
- **`getFormat().getFont().setBold(true)`**: Office Scripts reach a property through `get…()` calls and change it with `set…()`, where VBA writes `.Font.Bold = True`. `"#FFFFFF"` is white and `"#0F5C8C"` the same blue as `RGB(15, 92, 140)`.
- **`getFreezePanes().freezeRows(1)`** freezes the top row, the job `ActiveWindow.FreezePanes` did in VBA.
- **`console.log(…)`** writes to the output pane, with the two numbers placed into the text by `${ }`.

Reading and writing in bulk matters even more here than in VBA, because every call crosses the network. This one reads and writes **only the status column**:

```ts
function main(workbook: ExcelScript.Workbook) {
  const sheet = workbook.getWorksheet("Master");
  if (!sheet) { console.log("No Master sheet"); return; }
  const rowCount = sheet.getUsedRange().getRowCount();
  const statusRange = sheet.getRangeByIndexes(1, 8, rowCount - 1, 1);  // from I2 down, one column
  const values = statusRange.getValues();              // one read: a grid, one row per cell

  const map: { [key: string]: string } = {
    "delivered": "Delivered", "dlvd": "Delivered", "cancelled": "Cancelled",
    "canceled": "Cancelled", "cxl": "Cancelled", "shipped": "Shipped", "pending": "Pending"
  };

  let unmapped = 0;
  for (let r = 0; r < values.length; r++) {
    const raw = String(values[r][0]).trim().toLowerCase();
    if (map[raw]) { values[r][0] = map[raw]; } else { unmapped++; }
  }

  statusRange.setValues(values);                       // one write, of column I only
  console.log(`${values.length} rows, ${unmapped} unmapped statuses`);
}
```

<<OUT:os_clean>>

- **`getRangeByIndexes(1, 8, rowCount - 1, 1)`** starts at row 1 and column 8, counting from 0, which is cell **I2**, and takes every data row of that one column.
- **`getValues()`** reads the block into a grid; **`values[r][0]`** is row `r`, column 0 of the grid, and **`values.length`** is its number of rows.
- **`const map: { [key: string]: string } = { … }`** is a lookup table like the `Scripting.Dictionary`: each `"key": "value"` pair maps a spelling to its standard name. The part after the colon is TypeScript's type label: "keys are text, values are text".
- **`String(…).trim().toLowerCase()`** is `LCase(Trim(CStr(…)))`, written as a chain of steps from left to right.
- **`if (map[raw])`** is true when the spelling is in the map, like `.Exists`.
- **`setValues(values)`** writes the grid back, to the same one column.

Why only one column? Writing a value back into a cell makes Excel read it again, just as typing does. Write the whole sheet back and a code like `0237` in a General cell turns into the number 237, and any formulas in the range become plain values. Write only the cells you changed.

**Power Automate** is where Office Scripts become an automation rather than a button: a flow can run on a schedule or a trigger (a new file in SharePoint, a form response), run the script, and then email the result, post to Teams, or write to another system. That combination replaces most of what VBA did, for organizations that live in SharePoint and Teams. It's also the honest answer when IT won't allow macros.

---

## 19.12 Google Sheets: macros and Apps Script

Google Sheets has a recorder (**Extensions → Macros → Record macro**) that writes **Apps Script**, which is JavaScript running on Google's servers. **Extensions → Apps Script** opens the editor. JavaScript reads like the TypeScript above without the type labels. To follow along, copy the consolidated Master sheet into a new workbook, save it as `.xlsx`, and bring it into a Google Sheet with **File → Import**.

```javascript
function formatMaster() {
  const sheet = SpreadsheetApp.getActive().getSheetByName('Master');
  const lastRow = sheet.getLastRow();
  const lastCol = sheet.getLastColumn();

  sheet.getRange(1, 1, 1, lastCol)
       .setFontWeight('bold')
       .setFontColor('#ffffff')
       .setBackground('#0f5c8c');
  sheet.setFrozenRows(1);
  sheet.autoResizeColumns(1, lastCol);

  Logger.log(`formatted ${lastRow} rows and ${lastCol} columns`);
}
```

Choose `formatMaster` in the editor's toolbar and click **Run**. The first time, Google asks you to authorize the script to edit your spreadsheets. Then the **Execution log** shows (without its time stamps):

<<OUT:gs_format>>

- **`SpreadsheetApp.getActive()`** is the spreadsheet the script belongs to (`ThisWorkbook`), and **`.getSheetByName('Master')`** picks the sheet. JavaScript accepts single or double quotes for text.
- **`getLastRow()`** and **`getLastColumn()`** give the last filled row and column, like the VBA last-row line.
- **`sheet.getRange(1, 1, 1, lastCol)`**: start row, start column, number of rows, number of columns, **counting from 1**, as in the sheet itself. So this is row 1, from column A across.
- **`.setFontWeight('bold')` … `.setBackground(…)`**: each `set…` returns the same range, so the calls can be **chained**, one per line.
- **`setFrozenRows(1)`** freezes the header, and **`autoResizeColumns(1, lastCol)`** autofits columns 1 to `lastCol`.

### Read and write in batches

Apps Script has quotas and a six-minute limit per execution, and every call to the spreadsheet is a round trip. The single most important habit is the same as VBA's arrays:

```javascript
function cleanStatuses() {
  const sheet = SpreadsheetApp.getActive().getSheetByName('Master');
  const lastRow = sheet.getLastRow();
  const range = sheet.getRange(2, 9, lastRow - 1, 1);    // I2 down: row 2, column 9, one column
  const values = range.getValues();                      // one read

  const map = {
    'delivered': 'Delivered', 'dlvd': 'Delivered', 'cancelled': 'Cancelled',
    'canceled': 'Cancelled', 'cxl': 'Cancelled', 'shipped': 'Shipped', 'pending': 'Pending'
  };

  let unmapped = 0;
  for (let r = 0; r < values.length; r++) {
    const raw = String(values[r][0]).trim().toLowerCase();
    if (map[raw]) values[r][0] = map[raw];
    else unmapped++;
  }

  range.setValues(values);                               // one write, of column I only
  Logger.log(`${values.length} rows cleaned, ${unmapped} unmapped`);
}
```

<<OUT:gs_clean>>

Two ways of counting sit side by side here. **`sheet.getRange(2, 9, …)`** counts rows and columns **from 1**, like the sheet (row 2, column 9 = I2), but the grid that **`getValues()`** returns counts **from 0**: its first row is `values[0]`. Office Scripts' `getRangeByIndexes(1, 8, …)` counts from 0 for the same cell. When a column comes out one place wrong, this is usually why. As in Office Scripts, the script writes back only column I, so nothing else is re-read and changed.

A loop that calls `getRange().setValue()` per cell on 25,000 rows will hit the six-minute limit. The batch version finishes in seconds.

### A custom menu, so colleagues can run it

```javascript
function onOpen() {
  SpreadsheetApp.getUi()
    .createMenu('Riverstone')
    .addItem('Clean statuses', 'cleanStatuses')
    .addItem('Send daily summary', 'sendDailySummary')
    .addToUi();
}
```

`onOpen` is a **simple trigger**: Google runs it when the sheet opens, and a **Riverstone** menu appears next to Help. **`getUi()`** is the spreadsheet's menus and dialogs; **`.addItem(label, functionName)`** adds a menu item that runs the function with that name; **`.addToUi()`** puts the finished menu on screen.

### Custom functions

```javascript
/**
 * Riverstone's loyalty rebate percentage.
 * @param {number} annualValue The customer's annual net revenue.
 * @return {number} 0, 1 or 2.
 * @customfunction
 */
function REBATEPCT(annualValue) {
  if (annualValue >= 400000) return 2;
  if (annualValue >= 250000) return 1;
  return 0;
}
```

The comment between `/**` and `*/` is a **doc comment**: Sheets shows its first line, `@param` (the argument) and `@return` (the answer) as help while you type the formula. The `@customfunction` tag makes it available as `=REBATEPCT(B2)`, and it gives the same answers as the VBA version: 0, 1, 1 and 2 for 1,80,000, 2,50,000, 3,99,999 and 4,00,000. The function itself reads from the top: the first `return` that's reached hands back its value and ends the function. Custom functions can't call services that need authorization (no email, no external API with credentials), and they're cached, so they're for calculations only.

---

## 19.13 Triggers, email, and APIs in Apps Script

### Triggers

| Trigger | Fires when | Set up |
|---|---|---|
| `onOpen`, `onEdit` | The sheet is opened or edited | Simple triggers: name the function and Google runs it |
| Time-driven | Every hour, every day at 9 a.m., every Monday | **Triggers** page in the editor, or `ScriptApp.newTrigger(...)` |
| On form submit | A linked Google Form is submitted | Installable trigger on the sheet or the form |
| On change | Structure changes (rows added, sheet renamed) | Installable trigger |

Installable triggers run as **you**, with your permissions, even when you're asleep. That's the power and the risk: a trigger that emails customers is sending mail from your account.

Set the project's time zone before you add any timed trigger: **Project Settings** (the gear icon in the editor) → **Time zone**, India (Asia/Kolkata). Otherwise "9 a.m." may be 9 a.m. somewhere else.

### An acknowledgement email on form submit

This continues the enquiry form of Chapter 10 (section 10.14): each time a customer submits it, the script thanks them by email and records the enquiry. It uses a sheet called **Enquiries** in the form's spreadsheet, with the headers `received`, `email`, `company`, `product`, `quantity`, `status` in row 1.

Anything a customer types goes into the email's HTML, and a company name containing `<` or `&` would break it, or worse, add a link you didn't write. So the first function makes text safe for HTML. **Never trust form input.**

```javascript
function escapeHtml(text) {
  return String(text)
    .replaceAll('&', '&amp;')
    .replaceAll('<', '&lt;')
    .replaceAll('>', '&gt;')
    .replaceAll('"', '&quot;');
}
```

**`.replaceAll(a, b)`** swaps every `a` in the text for `b`. `&lt;` and `&gt;` are HTML's way of writing `<` and `>` as ordinary characters, `&quot;` is a double quote, and `&amp;` is `&` itself (replaced first, so the others aren't changed twice). `escapeHtml('Tools & <Co>')` returns `Tools &amp; &lt;Co&gt;`, which the email shows as *Tools & <Co>*.

```javascript
function onFormSubmit(e) {
  const answers = e.namedValues;                     // {'Email address': ['x@y.com'], 'Company': [...], ...}
  const email = answers['Email address'][0];
  const company = answers['Company'][0];
  const product = answers['Product'][0];
  const quantity = answers['Quantity'][0];

  const html = `
    <p>Dear ${escapeHtml(company)},</p>
    <p>Thank you for your enquiry. We have logged it and a sales executive will reply within one working day.</p>
    <table style="border-collapse:collapse;font-family:Arial;font-size:13px">
      <tr><td style="padding:4px 12px;color:#5b6475">Product</td><td style="padding:4px 12px"><b>${escapeHtml(product)}</b></td></tr>
      <tr><td style="padding:4px 12px;color:#5b6475">Quantity</td><td style="padding:4px 12px"><b>${escapeHtml(quantity)}</b></td></tr>
    </table>
    <p style="color:#5b6475;font-size:12px">Riverstone Supplies · this is an automatic acknowledgement.</p>`;

  MailApp.sendEmail({
    to: email,
    subject: `Riverstone: we received your enquiry (${product})`,
    htmlBody: html,
    name: 'Riverstone Supplies'
  });

  SpreadsheetApp.getActive().getSheetByName('Enquiries')
    .appendRow([new Date(), email, company, product, Number(quantity), 'acknowledged']);
}
```

- **`e`** is the **event**: Google fills it with details of the submission. **`e.namedValues`** maps each question's title to a list of answers, so **`answers['Email address'][0]`** is the first (and only) answer to the question titled *Email address*. The titles in your form must match these keys exactly, including capitals: they're the column headers of `enquiries_sample.csv`.
- **The HTML** is one text value in back-quotes, which may run over several lines; each `${ }` puts in a value, passed through `escapeHtml` first. Inside back-quotes the attributes can use double quotes.
- **`MailApp.sendEmail({ … })`** sends the email. Its settings go in curly brackets as `name: value` pairs: the address, the subject, the HTML body, and the sender name people see.
- **`appendRow([ … ])`** adds one row under the last filled row of Enquiries. The square brackets hold the row's six values in column order; **`new Date()`** is the date and time now, and **`Number(quantity)`** stores the quantity as a number, not text.

A function named `onFormSubmit` doesn't run by itself: it needs an installable trigger. In the editor, open **Triggers → Add Trigger**, choose `onFormSubmit`, event source **From spreadsheet**, event type **On form submit**, and save. Google asks you to authorize sending email as you.

Submitting the six enquiries in `enquiries_sample.csv` through the form sends six emails. The first goes to `stores@kaveritraders.example.com` with the subject *Riverstone: we received your enquiry (Industrial Crate)*, and its body begins *Dear Kaveri Traders,*. Enquiries then has six rows, from Kaveri Traders (Friday 2 January 2026, 2:40 p.m.) to Sharma Hardware (Monday 5 January, 11:31 a.m.).

### A 9 a.m. summary in the email body

Every weekday at 9 a.m., the sales team gets one email listing the enquiries that arrived since the last summary, totalled by product. "Since the last summary", not "yesterday": on Monday, "yesterday" is Sunday, and Friday afternoon's and Saturday's enquiries would never be reported. The script remembers when it last sent, using **`PropertiesService`**, a small store of named text values that belongs to the script.

It's built in four steps, and each one logs what it did, so you can check it before anything is sent.

**Step 1: read the rows.**

```javascript
function readEnquiries() {
  const sheet = SpreadsheetApp.getActive().getSheetByName('Enquiries');
  const rows = sheet.getDataRange().getValues().slice(1);   // every row after the header
  Logger.log(`${rows.length} enquiries in the sheet`);
  return rows;
}
```

**`getDataRange()`** is the whole filled block and **`getValues()`** reads it as a grid. **`.slice(1)`** keeps everything from position 1 onward, which drops row 0, the header. **`return rows`** hands the grid back to whoever called the function.

**Step 2: keep the rows since the last summary.**

```javascript
function keepSince(rows, since) {
  const recent = rows.filter(r => r[0] > since);            // column 0 holds the date received
  Logger.log(`${recent.length} arrived since the last summary`);
  return recent;
}
```

**`rows.filter(…)`** keeps the rows for which a test is true, like Chapter 11's `FILTER`. The test is written **`r => r[0] > since`**: a small function without a name, read "for each row `r`, is its date later than `since`?". Dates compare by time, later is bigger.

**Step 3: total the units by product.**

```javascript
function unitsByProduct(rows) {
  const totals = {};
  rows.forEach(r => {
    const product = r[3];
    totals[product] = (totals[product] || 0) + Number(r[4]);
  });
  Logger.log(JSON.stringify(totals));
  return totals;
}
```

- **`const totals = {}`** is an empty lookup table, filled as it goes: product name → units.
- **`rows.forEach(r => { … })`** runs the lines in the curly brackets once for each row, like `For Each`.
- **`totals[product] || 0`** reads the running total, or 0 the first time a product appears (`||` means "or, if that's empty, this"). Then the row's quantity is added.
- **`JSON.stringify(totals)`** turns the table into text in JSON, the format of Chapter 2, so the log shows it all on one line.

**Step 4: build the email body.**

```javascript
function buildSummaryHtml(count, totals) {
  if (count === 0) {
    return '<p style="font-family:Arial">No enquiries were received since the last summary.</p>';
  }
  let tableRows = '';
  Object.keys(totals).sort().forEach(product => {
    tableRows += `<tr><td style="padding:4px 12px">${escapeHtml(product)}</td>` +
                 `<td style="padding:4px 12px;text-align:right">${totals[product]}</td></tr>`;
  });
  return `<h3 style="font-family:Arial">Enquiries since the last summary: ${count}</h3>
    <table style="border-collapse:collapse;font-family:Arial;font-size:13px">
      <tr><th style="text-align:left;padding:4px 12px">Product</th>
          <th style="text-align:right;padding:4px 12px">Units</th></tr>
      ${tableRows}
    </table>
    <p style="color:#5b6475;font-size:12px">Sent automatically by the Riverstone enquiries sheet.</p>`;
}
```

- **The "no data" branch comes first.** An automation that says *"no enquiries were received"* is trustworthy; one that sends an empty table looks broken, and one that sends nothing at all leaves people wondering (Chapter 20).
- **`Object.keys(totals).sort()`** is the list of product names, in A-to-Z order; **`.forEach`** adds one table row for each.
- **`tableRows += …`** adds text to the end, like `bodyHtml = bodyHtml & …` in VBA; a **`+`** between two pieces of text joins them.

**Putting it together.**

```javascript
function sendDailySummary() {
  const now = new Date();
  if (now.getDay() === 0 || now.getDay() === 6) return;      // 0 is Sunday, 6 is Saturday
  const props = PropertiesService.getScriptProperties();
  const lastSent = new Date(props.getProperty('LAST_SUMMARY') || 0);

  const rows = keepSince(readEnquiries(), lastSent);
  const html = buildSummaryHtml(rows.length, unitsByProduct(rows));
  Logger.log(html);                                           // read it before it goes out

  MailApp.sendEmail({ to: 'sales.team@riverstone.example',
                      subject: 'Riverstone enquiries — daily summary',
                      htmlBody: html, name: 'Riverstone reporting' });
  props.setProperty('LAST_SUMMARY', now.toISOString());
}
```

- **`now.getDay()`** is the day of the week as a number. On Saturday and Sunday the function returns at once, so a trigger that runs every day sends only on weekdays.
- **`props.getProperty('LAST_SUMMARY')`** reads the time of the last summary. The very first time there isn't one, so **`|| 0`** gives 0, and `new Date(0)` is 1 January 1970: every enquiry counts as new.
- **`props.setProperty('LAST_SUMMARY', now.toISOString())`** stores this run's time as text, *after* the email has gone, so a failed send doesn't skip any enquiries next time.
- While you test, put `//` in front of the `MailApp.sendEmail` line, run it, and read the log first.

Run at 9 a.m. on Monday 5 January 2026, after Friday's summary went out at 9 a.m. on 2 January, the sheet holds the three enquiries from Friday afternoon, Saturday and early Monday, and the log shows:

<<OUT:gs_summary>>

To run it every morning: **Triggers → Add Trigger**, choose `sendDailySummary`, event source **Time-driven**, **Day timer**, **9am to 10am**. Google picks a moment within that hour.

### Calling an API

Chapter 2 introduced **APIs**: a program sends a **request** to a web address and gets a **response** back, often in **JSON**, with a **status code** that says whether it worked (200 means OK). Apps Script can call one with `UrlFetchApp`. Here it asks Riverstone's CRM (the customer system) for the open enquiries and writes them to a sheet called **CRM**:

```javascript
function fetchOpenEnquiries() {
  const token = PropertiesService.getScriptProperties().getProperty('CRM_TOKEN');  // not in the code
  const response = UrlFetchApp.fetch('https://crm.example.com/api/v1/enquiries?status=open', {
    method: 'get',
    headers: { Authorization: 'Bearer ' + token },
    muteHttpExceptions: true
  });

  if (response.getResponseCode() !== 200) {
    throw new Error('CRM returned ' + response.getResponseCode() + ': ' + response.getContentText().slice(0, 200));
  }

  const data = JSON.parse(response.getContentText());
  const rows = data.results.map(r => [r.id, r.company, r.product, r.quantity, r.created_at]);
  const sheet = SpreadsheetApp.getActive().getSheetByName('CRM');
  sheet.getRange(2, 1, sheet.getMaxRows() - 1, 5).clearContent();   // remove the last run's rows
  if (rows.length === 0) {
    Logger.log('no open enquiries');
    return;
  }
  sheet.getRange(2, 1, rows.length, rows[0].length).setValues(rows);
  Logger.log(`${rows.length} enquiries written`);
}
```

`crm.example.com` is a placeholder, so this block has no output to show: point it at your CRM's real address and the log shows how many enquiries were written, or *no open enquiries*.

- **`PropertiesService`** stores the token (the CRM's API key) outside the code, which matters because Apps Script files are visible to anyone who can edit the sheet. Add it once in **Project Settings → Script Properties**. **`'Bearer ' + token`** is the usual way to hand an API key over in a request header.
- **`UrlFetchApp.fetch(address, { … })`** sends the request; the settings say it's a `get` (read) request and which headers to send. **`muteHttpExceptions: true`** lets you read the status code and message instead of the script dying with a generic error.
- **`throw new Error(…)`** stops the script with your own message, the JavaScript version of `Err.Raise`. `.slice(0, 200)` keeps the first 200 characters of the reply.
- **`JSON.parse(…)`** turns the JSON text into objects the script can use; **`data.results.map(r => [ … ])`** turns each enquiry into a row of five values, like `filter` but changing each item instead of choosing.
- **`clearContent()`** empties columns A to E below the header first, so rows left over from a longer earlier run don't linger. **`getMaxRows()`** is the sheet's number of rows.
- **`if (rows.length === 0)`** stops before writing when there's nothing to write: with no rows, `rows[0]` doesn't exist and the next line would fail.
- **Paging:** most APIs return a limited number of results per request, in **pages**, and say how to ask for the next one. This function reads only the first page. Chapter 18 (section 18.14) shows how to follow the pages to the end.
- **Quotas** apply per account per day: `MailApp` is limited (100 recipients a day on consumer accounts, 1,500 on Workspace at the time of writing), `UrlFetchApp` has a daily call limit, and each execution must finish within six minutes. Check the current quota page before promising a volume.

---

## 19.14 The same job in three languages

Consolidating and cleaning, as it appears in each environment:

| Task | VBA | Office Scripts | Apps Script |
|---|---|---|---|
| Get the sheet | `Set ws = ThisWorkbook.Worksheets("Master")` | `const sheet = workbook.getWorksheet("Master")` | `const sheet = SpreadsheetApp.getActive().getSheetByName('Master')` |
| Last row | `ws.Cells(ws.Rows.Count, "A").End(xlUp).Row` | `sheet.getUsedRange().getRowCount()` | `sheet.getLastRow()` |
| Read a block | `v = rng.Value2` | `const v = range.getValues()` | `const v = range.getValues()` |
| Write a block | `rng.Value2 = v` | `range.setValues(v)` | `range.setValues(v)` |
| Loop | `For r = 1 To UBound(v, 1)` | `for (let r = 0; r < v.length; r++)` | `for (let r = 0; r < v.length; r++)` |
| Lookup table | `Scripting.Dictionary` | object literal `{}` or `Map` | object literal `{}` or `Map` |
| Bold the header | `.Font.Bold = True` | `.getFormat().getFont().setBold(true)` | `.setFontWeight('bold')` |
| Log | `Debug.Print` | `console.log` | `Logger.log` |
| Open other files | `Workbooks.Open` | not available | `SpreadsheetApp.openById` |
| Email | Outlook object | via Power Automate | `MailApp` / `GmailApp` |
| Schedule | Task Scheduler plus a launcher script (fragile; see Chapter 20's laptop trap) | Power Automate | Time-driven trigger |

The shapes are identical: get a range, read once, loop in memory, write once, log what happened. Learn the pattern and the syntax is a lookup.

---

## 19.15 Living with macros responsibly

A macro becomes a liability the day its author leaves. These habits prevent that.

**Write it so someone else can read it**

- `Option Explicit` at the top; meaningful names; one procedure, one job.
- A comment block at the top of the module: what it does, what it expects (folder, sheet names, columns), what it produces, who owns it, when it was last changed.
- No magic numbers: `Const` for paths, sheet names, column positions, and thresholds. Better still, find columns by header name rather than by position, so an inserted column doesn't silently break the totals.

**Never hard-code secrets or personal paths**

- `C:\Users\meera\Desktop\` works on exactly one machine. Use `ThisWorkbook.Path`, a folder picker, or a named cell in a settings sheet.
- Passwords and tokens don't belong in a module. Apps Script has `PropertiesService`; VBA has no good answer, which is itself a reason to move that job to Python (Chapter 18) or Power Automate.
- A settings sheet (`Config`) with named cells for folder, recipients, and month is the simplest way to let the business change what it should change without touching code.

**Version control**

VBA lives inside a binary file, so Git can't diff it. Two workable answers: export the modules (`.bas`, `.cls`, `.frm`) to a folder and commit those files (right-click the module → **Export File**), or keep dated copies of the workbook with a changelog sheet. Apps Script has built-in version history and a Git-friendly command-line tool (`clasp`). Office Scripts keep versions in OneDrive. Chapter 26 covers Git properly.

**The single-owner risk**

If one person understands the macro, the business has a dependency, not an asset. Fix it with: a one-page document (what it does, how to run it, what to do when it fails), a colleague who has run it once, and code readable enough that a competent analyst could pick it up. Ask yourself the honest question: *if I'm on leave and it fails on the 2nd, what happens?*

**When to stop using macros**

| Sign | Move to |
|---|---|
| The macro is mostly combining and reshaping files | Power Query (Chapter 11) |
| It needs data from a database or an API | Python (Chapter 18) |
| It must run when nobody is logged in | Python plus a scheduler, or Power Automate (Chapter 20) |
| Several people need the output, interactively | Power BI (Chapter 16) |
| It's over about 500 lines, or nobody dares change it | Rewrite, in whatever tool fits, with tests |
| It handles personal or financial data with emails | A reviewed process, not a macro on one laptop |

None of that makes VBA a waste of time. It makes it what it is: the fastest way to automate the workbook in front of you, and a skill that pays for itself the first month you use it.

---

## Common mistakes

| Mistake | Symptom | Fix |
|---|---|---|
| Saving a macro workbook as `.xlsx` | The code is gone next time | Save as `.xlsm`; check the title bar |
| Telling users to enable all macros | A security incident waiting to happen | Trusted locations, signed macros |
| Keeping recorded code as-is | Breaks when the data changes size | Rewrite with variables and the last-row pattern |
| `Select` and `Activate` everywhere | Slow; breaks when focus changes | Address objects directly |
| No `Option Explicit` | A typo silently creates an empty variable | Turn on Require Variable Declaration |
| `Integer` for row counts | Overflow above 32,767 rows | `Long` |
| Hard-coded paths and sheet names | Runs on one laptop only | `Const`, a settings sheet, or a folder picker |
| Hard-coded column positions | An inserted column breaks the totals silently | Find columns by header text |
| Cell-by-cell loops | Minutes instead of seconds | Read into an array, work, write back |
| `ScreenUpdating` left off after an error | Excel looks frozen; users panic | Error handler with `Resume CleanUp` |
| `On Error Resume Next` across whole procedures | Errors hidden; wrong results shipped | Handle specific cases; `On Error GoTo 0` |
| Emailing with `.Send` while developing | The wrong draft reaches the sales team | `.Display` until you trust it |
| No source-file column when consolidating | You can't trace a wrong number or spot a double-count | Add `source_file` |
| Copying the header from every file | Header rows scattered through the data | Copy the header once, data from row 2 |
| Opening every file `Dir` returns | The macro stops on a `~$` lock file while someone has a branch file open | Skip names starting with `~$` |
| Writing text codes into General cells | `0237` becomes 237 | Format the column as Text (`NumberFormat = "@"`) first, and write back only the cells you changed |
| Cell-by-cell calls in Apps Script | Six-minute timeout | `getValues()` / `setValues()` once |
| Tokens in the script file | Anyone who can edit the sheet can read them | `PropertiesService`, or move the job |
| One person understands it | The business depends on a person, not a process | Document, share, simplify |
| A macro that should be Power Query | Hundreds of lines doing a refreshable job | Rebuild it in Power Query |

---

## In the real world: the macro that ran for nine years

When Meera joined Riverstone, the Q4 branch consolidation ran on a workbook called `MASTER_FINAL_v7_USE_THIS.xlsm`, written in 2017 by an analyst who had left in 2020. Every quarter, someone opened it, clicked a gray button labeled "RUN", waited about four minutes while the screen flickered, and emailed the PDF it produced.

It mostly worked. Three things about it were quietly expensive.

**It counted whatever files it found.** The macro looped `Dir("*.xls*")` over a shared folder. In the quarter Meera arrived, that folder had thirteen files: the twelve branch extracts and one called `Riverstone_Kolkata_2025-11 (2).xlsx`, a copy someone had saved when the network dropped. The total was ₹1.88 crore too high, and nobody noticed, because the macro reported nothing but "Done!".

**It stopped at row 5,000.** The loop ran `For r = 2 To 5000`, a number the original author had picked as "plenty". October 2025's Mumbai file had 3,297 rows, so it was fine, but the consolidated sheet was silently truncated the first time a branch grew past the limit.

**Nobody could read it.** 740 lines, no `Option Explicit`, variables called `x`, `x2`, and `temp3`, and a hard-coded path to a laptop that no longer existed, worked around by a mapped drive that IT wanted to remove.

She rewrote it in two afternoons, not as a heroic act but as a set of ordinary decisions:

- The folder comes from a `Config` sheet, and the macro **lists the files it read** in the summary, with row counts per file.
- Rows come from `Cells(Rows.Count, "A").End(xlUp).Row`, not from a guess.
- Each row carries its `source_file`, so a suspicious number can be traced in ten seconds.
- Three checks run before anything is emailed: twelve files found, no duplicate file names after normalizing, and the consolidated total within 25% of the same quarter last year. If a check fails, the macro writes to a log, shows what failed, and refuses to send.
- The reading loop became an array read, and the macro went from four minutes to nine seconds.
- A one-page note lives in the workbook's first sheet: what it does, how to run it, what each check means, and who to call.

The first run after the rewrite failed the duplicate check and named the file. That, in Meera's report to Anita Rao, was the entire business case: *"The old macro would have added ₹1.88 crore of a branch's November sales twice, as it probably has before. The new one won't send a report it can't stand behind."*

What made the difference:

- **It reports what it did**, not merely that it finished.
- **It checks before it sends**, and fails loudly.
- **It has no secrets**: no hidden paths, no assumptions about size, no cleverness.
- **Someone else can run it**, which is the only real test of an automation.

---

## Project: two automations, end to end

### Tools you'll need

- **Excel for Windows** (Microsoft 365 or 2016+) with the **Developer** tab enabled, for VBA, Outlook email, and PDF export. Excel for Mac runs VBA but not the Outlook automation.
- **Excel on the web** with a Microsoft 365 **business** plan, for Office Scripts and Power Automate. Personal Microsoft accounts don't have Office Scripts.
- **A Google account** for Sheets, Apps Script, Forms, and triggers. Workspace accounts have much higher email quotas than consumer ones.
- **Companion files (`companion/ch19/`):**
  - `ch19_practice.xlsx`: the practice workbook for sections 19.2–19.5 (a **Master** sheet with Kolkata's December 2025 lines and an empty **Scratch** sheet).
  - `branch_files/`: twelve workbooks (four branch sales offices × three months of Q4 2025), plus `_notes.txt`.
  - `expected_results.md`: the row count and net revenue of every file, and the totals a correct consolidation must produce.
  - `enquiries_sample.csv`: sample Google Form responses for the Apps Script project.
  - `vba/`: the chapter's VBA modules as `.bas` files, ready to import (**File → Import File** in the editor).
  - `office_scripts/` and `apps_script/`: the TypeScript and JavaScript versions.
  - `build_ch19_files.py`: rebuilds the workbooks, the sample data, and `expected_results.md` (not needed for the exercises).

> **Checking your results.** `expected_results.md` is the yardstick for every number in this project: each file's row count and net revenue, and the totals by branch, month, and status. If your macro disagrees, compare file by file: the per-file lines in the Immediate window show where the difference starts.

### Part 1: the Excel consolidation (VBA)

**Goal:** one button that turns twelve branch files into a summary, a PDF, and an email.

1. **Set up** a new `.xlsm` workbook with sheets `Config`, `Master`, and `Summary`. Put the folder path, the recipient list, and the quarter in named cells on `Config`.
2. **Consolidate** every `.xlsx` in the folder into `Master`, with a `source_file` column, ignoring `_notes.txt`.
3. **Clean:** standardize `status` through a dictionary, keep `customer_code` as four digits, and flag anything unmapped.
4. **Check, before anything else happens:** twelve files read; no duplicate file names; row count matches the sum of the per-file counts; net revenue within a sensible range. Write the results to a log sheet.
5. **Summarize:** a pivot of net revenue by branch (from `source_file`) and month, plus the headline numbers.
6. **Export** the summary as a PDF named with the quarter and today's date.
7. **Email** it with an HTML body containing the headline numbers, using `.Display` until you're sure, then `.Send`.
8. **Wrap** the whole thing in one `RunConsolidation` procedure with error handling that restores Excel's settings and refuses to email if a check failed.

**What good looks like:** **25,832** data rows, **24,738** non-cancelled, net revenue **₹42,38,72,808.00**; by branch, Mumbai HO ₹15,10,58,519.25 · Bengaluru ₹11,77,26,527.00 · Delhi ₹10,29,66,828.00 · Kolkata ₹5,21,20,933.75; by month, October ₹18,06,20,103.00 · November ₹15,59,85,902.00 · December ₹8,72,66,803.75. The whole run should take under 15 seconds.

### Part 2: the Google Sheets workflow (Apps Script)

**Goal:** an enquiry form that answers itself, and a daily summary that sends itself.

1. **Create a Google Form** with one question for each column of `enquiries_sample.csv` after the timestamp, titled exactly as the headers are (*Email address*, *Company*, *City*, *Product*, *Quantity*, *Needed by*, *Notes*), and link it to a sheet (Chapter 10, section 10.14).
2. **On submit:** send the customer an HTML acknowledgement, and append a row to an `Enquiries` sheet with a status of `acknowledged`.
3. **Validate:** if the quantity isn't a number or the email looks wrong, write the row to an `Exceptions` sheet and notify the sales team instead of the customer.
4. **At 9 a.m. every weekday:** email the sales team the enquiries received since the last summary (so Monday's covers Friday after 9 a.m., the weekend, and Monday morning) as an HTML table in the body, grouped by product, with a "no enquiries were received" branch.
5. **Add a menu** so someone can run the summary by hand.
6. **Protect it:** no addresses or tokens in the code, a log sheet of what was sent and when, and a note in the sheet explaining who owns it.

**Stretch goals**

- Rebuild Part 1's consolidation in Power Query and compare: lines of code, time to run, and what each can't do.
- Rewrite Part 1's cleaning step as an Office Script and run it from Power Automate on a schedule.
- Add a quarter-on-quarter comparison to the PDF, using last quarter's saved summary.

---

## Timed challenge: forty-five minutes in the editor

Use `companion/ch19/branch_files/` and a blank `.xlsm`. Answers at the end of the chapter.

- **Level 1:** Write a macro that counts the `.xlsx` files in the folder and prints the count and each file name to the Immediate window. How many files, and how many does `*.xls*` match?
- **Level 2:** Open each file and print its row count (excluding the header). What's the total?
- **Level 3:** Consolidate all twelve into one sheet with a `source_file` column. How many data rows?
- **Level 4:** Total `net_revenue` for rows whose status is not `Cancelled`.
- **Level 5:** Produce the total per branch, using the file name to derive the branch.
- **Level 6:** Produce the total per month, the same way.
- **Level 7:** Rewrite your row loop to read the data into an array and time both versions with `Timer`.
- **Bonus:** Add a check that fails if fewer than twelve files were read, and make the macro refuse to continue.

---

## Recap

- **Spreadsheet automation is worth doing** when the data and the audience already live in workbooks; Power Query, Power BI, and Python are better for everything else.
- **Macros live in `.xlsm`**, run under macro security, and belong in a trusted location rather than behind "enable everything".
- **Record to learn, then rewrite:** recordings select, are literal, and depend on what's active.
- **VBA basics:** `Option Explicit`, `Dim` with real types (`Long`, not `Integer`), `If`/`Select Case`, `For`/`For Each`/`Do`, arrays, `Scripting.Dictionary`, `Sub` and `Function` with arguments.
- **The object model** is `Application → Workbook → Worksheet → Range`. The last-row pattern, `Cells(row, col)`, and `With` cover most of what you write. Avoid `Select` and `ActiveSheet`.
- **The toolkit:** consolidate a folder with `Dir`, add a `source_file` column, clean through a dictionary, build a pivot, export a PDF, email through Outlook with `.Display` first.
- **Debug** with breakpoints, `Debug.Print`, the Immediate window; **handle errors** with `On Error GoTo` and a `Resume CleanUp` that restores settings.
- **Make it fast** with `ScreenUpdating = False`, manual calculation, and arrays instead of cell-by-cell access: 25,832 rows go from seconds to instant.
- **Office Scripts** bring the same ideas to Excel on the web in TypeScript, and run unattended through Power Automate; **Apps Script** does it for Sheets in JavaScript, with triggers, `MailApp`, `UrlFetchApp`, and quotas to respect.
- **Responsibility:** settings not hard-coded, secrets not in code, checks before sending, a log, version control for exported modules, and a plan for the day you're not there.

---

## Key terms

macro · macro recorder · `.xlsm` · `.xlsb` · macro security · trusted location · Mark of the Web · Personal Macro Workbook · form control · VBA · Visual Basic Editor · Immediate window · procedure · statement · argument · module · `Option Explicit` · `Dim` · `Set` · `Long` versus `Integer` · `Select Case` · `For Each` · `Do While` · array · `Scripting.Dictionary` · `Sub` · `Function` · `ByVal` / `ByRef` · object model · `Application` · `Workbook` · `Worksheet` · `Range` · `Cells` · `End(xlUp)` · `CurrentRegion` · `With` · `Value2` · `Dir` · lock file · named argument · `Err.Raise` · `FileSystemObject` · `PivotCache` · `ExportAsFixedFormat` · late binding · `CreateObject` · HTML · tag · attribute · `ChrW` · `HTMLBody` · UDF · UserForm · `InputBox` · `Like` · `FileDialog` · breakpoint · `Debug.Print` · `On Error GoTo` · `Resume` · `Err` · `FreeFile` · `Timer` · `ScreenUpdating` · `Calculation` · `EnableEvents` · Office Scripts · TypeScript · Power Automate · Apps Script · `SpreadsheetApp` · `getValues` / `setValues` · simple and installable triggers · event object · `namedValues` · escaping · `MailApp` · `GmailApp` · `UrlFetchApp` · `PropertiesService` · quota · `clasp`

*(All terms are defined in the Glossary, Appendix A.)*

---

## Check yourself

- [ ] You can record a macro, read what it wrote, and rewrite it without `Select`.
- [ ] You know which file types hold macros, and how to handle macro security without disabling it.
- [ ] You declare variables with sensible types, use `Option Explicit`, and can write `If`, `Select Case`, and all three loops from memory.
- [ ] You use the last-row pattern instead of fixed ranges, and address objects instead of activating them.
- [ ] You can consolidate a folder of files, with a source column and a per-file row count.
- [ ] You can clean a column through a dictionary and flag what isn't in the map.
- [ ] You can build a pivot, export a PDF, and send an Outlook email with an HTML body.
- [ ] You debug with breakpoints, the Immediate window, and Locals, and handle errors with a handler that restores Excel's settings.
- [ ] You make a slow macro fast with arrays and `ScreenUpdating`.
- [ ] You can do the same job in Office Scripts and Apps Script, and say when each is the right home.
- [ ] Your automations carry a settings sheet, a log, checks that can stop them, and a note for whoever inherits them.

---

## Exercises

Use `companion/ch19/branch_files/` and `expected_results.md`.

### Warm-up

1. Which file extensions can hold macros, and what happens if you save a macro workbook as `.xlsx`?
2. What are the three problems with almost every recorded macro? Rewrite this recording properly: `Sheets("Master").Select` / `Range("A1").Select` / `ActiveCell.FormulaR1C1 = "Total"`.
3. Why is `Option Explicit` worth turning on, and what exactly goes wrong without it?
4. Why is `Dim rowCount As Integer` a bug waiting to happen in a data macro?
5. Write the one line that finds the last used row in column A of a worksheet `ws`, and explain each part.
6. When would you use `For Each` rather than `For … Next`? Give a Riverstone example of each.

### Core

7. Record a macro that bolds row 1, freezes it, and autofits the columns of a branch file. Then rewrite it as a `Sub` that takes a `Worksheet` argument.
8. Write a macro that prints the name and row count of every `.xlsx` in the branch folder. How many files are there, and what is the total row count?
9. Consolidate the twelve files into a `Master` sheet with a `source_file` column. How many data rows, and does it match `expected_results.md`?
10. Add the headline calculations: non-cancelled rows and their net revenue. What are they?
11. Produce net revenue per branch, deriving the branch from the file name. Which branch is largest, and by how much over the smallest?
12. Produce net revenue per month, and state October's share of the quarter.
13. Standardize the `status` column with a `Scripting.Dictionary`, and count how many values weren't in the map.
14. Write a macro that formats the `Master` sheet: header style, number format on `net_revenue`, frozen header, autofit, and a filter.
15. Build a pivot table of net revenue by `source_file` and `status` in VBA.
16. Export the summary sheet to PDF with a file name that includes today's date, in landscape, fitted to one page wide.
17. Write the email procedure with `.Display`, including an HTML body with the headline numbers. What would you change before switching to `.Send`?
18. Write `REBATEPCT` as a UDF and check it on 180,000, 250,000, 399,999, and 400,000.
19. Add error handling to your main procedure that restores `ScreenUpdating` and `Calculation`, logs the error, and prevents the email.
20. Time your cleaning loop with `Timer`, then rewrite it with an array read and write. What's the difference on 25,832 rows?
21. Write the Apps Script version of the cleaning step for a Google Sheets copy of `Master`, using one `getValues()` and one `setValues()`.
22. Write an Apps Script `onOpen` menu with two items, and a time-driven trigger that runs a summary at 9 a.m.

### Stretch

23. Rewrite the consolidation so it finds columns by header name rather than position, and still works if a branch adds a column.
24. Add three checks that must pass before the email is sent, including one that compares the total with a previous run stored on a `History` sheet.
25. Rebuild the consolidation in Power Query and write ten lines comparing it with the macro: effort, speed, maintainability, and what each can't do.
26. Export your modules as `.bas` files and put them under Git. What does the diff of a small change look like, and why is that better than versioning the `.xlsm`?

### Think about it

27. Your predecessor's macro sends a report to 40 people every Monday, and you can't read the code. What do you do first, second, and third?
28. When is it right to keep a working macro rather than rewrite it in Python, even though Python would be "better"?

---

## Answers

**1.** `.xlsm`, `.xlsb`, and `.xltm` (and the legacy `.xls`). Saving as `.xlsx` strips the code, with a single warning: the macro is gone when the file reopens.

**2.** They select things, they're literal about ranges and sheets, and they depend on what's active. Rewritten: `ThisWorkbook.Worksheets("Master").Range("A1").Value = "Total"`.

**3.** It forces `Dim` for every variable, so a misspelling is a compile error instead of a new, empty variable. Without it, `netRevene = total` silently creates a second variable and your reported total stays zero.

**4.** `Integer` overflows above 32,767. Excel has 1,048,576 rows, and the consolidated sheet here has 25,833 including the header, so a row counter will eventually raise "Overflow". Use `Long`.

**5.** `lastRow = ws.Cells(ws.Rows.Count, "A").End(xlUp).Row` — start at the bottom of the sheet in column A (`ws.Rows.Count` is the last row number), press Ctrl+Up (`End(xlUp)`), and take that cell's row number.

**6.** `For Each` when looping a collection whose size you don't care about: every worksheet in the workbook, every file in a folder collection. `For … Next` when you need the index: rows 2 to `lastRow`, or counting backwards while deleting rows.

**7.** See section 19.2. The rewritten version takes `ws As Worksheet`, uses `With ws`, and never touches `ActiveSheet`.

**8.** **12** files. Total data rows **25,832**: Bengaluru 2,631 + 2,481 + 2,073; Delhi 2,211 + 2,220 + 1,843; Kolkata 1,117 + 1,099 + 994; Mumbai HO 3,297 + 3,167 + 2,699.

**9.** 25,832 data rows in `Master` (25,833 including the header). If Master has 25,844 used rows (11 more than expected), you copied every file's header row; if you get fewer, a file was skipped or a last-row calculation is wrong.

**10.** **24,738** non-cancelled rows, net revenue **₹42,38,72,808.00**. (All rows, including cancelled: ₹44,25,77,334.00.)

**11.** Mumbai HO **₹15,10,58,519.25**, Bengaluru ₹11,77,26,527.00, Delhi ₹10,29,66,828.00, Kolkata **₹5,21,20,933.75**. Mumbai HO is ₹9,89,37,585.50 above Kolkata, close to three times its size.

**12.** October ₹18,06,20,103.00 · November ₹15,59,85,902.00 · December ₹8,72,66,803.75. October is **42.6%** of the quarter.

**13.** On this clean data every status maps, so the count of unmapped values is **0**. That's the point of the check: it's how you find the day a branch starts writing something new.

**14.** Any correct formatting macro. Test it by adding a column to one branch file and rerunning: if your code uses fixed column letters, it now formats the wrong column.

**15.** See section 19.6. The pivot's grand total must equal ₹44,25,77,334.00 across all statuses, or ₹42,38,72,808.00 if you filter Cancelled out.

**16.** `ws.PageSetup.Orientation = xlLandscape`, `ws.PageSetup.Zoom = False`, `ws.PageSetup.FitToPagesWide = 1`, `ws.PageSetup.FitToPagesTall = False`, then `ExportAsFixedFormat` with a name built from `Format(Date, "yyyy-mm-dd")`.

**17.** Before switching to `.Send`: check the recipient list comes from the `Config` sheet and not from a hard-coded string, that the checks passed, that the PDF exists and isn't zero bytes, and that the subject and body contain the right period. Send it to yourself first.

**18.** 1,80,000 → 0; 2,50,000 → 1; 3,99,999 → 1; 4,00,000 → 2 (section 19.8's `TestRebate`).

**19.** See section 19.9. The key line is `Resume CleanUp`, so `ScreenUpdating`, `Calculation`, and `DisplayAlerts` are restored whatever happened, and the email procedure is called only after the checks.

**20.** The cell-by-cell version takes a few seconds on 25,832 rows (longer with screen updating on); the array version is effectively instant. Measure both with section 19.10's `TimeBoth`; your exact numbers depend on your computer.

**21.** See section 19.12: `getRange(2, 9, lastRow - 1, 1).getValues()` for the status column only, loop the array, map the status, `setValues()` once on the same range. A per-cell version on 25,832 rows will hit the six-minute limit.

**22.** `onOpen` builds the menu with `SpreadsheetApp.getUi().createMenu(...)`. The 9 a.m. job is an installable time-driven trigger: **Triggers → Add Trigger → Time-driven → Day timer → 9am to 10am**, or `ScriptApp.newTrigger('sendDailySummary').timeBased().atHour(9).everyDays(1).create()`. A day timer runs every day, weekends included, so the function itself must skip Saturday and Sunday: `if (now.getDay() === 0 || now.getDay() === 6) return;` (`getDay()` is 0 for Sunday and 6 for Saturday). Set the project's time zone to India first, so 9 a.m. is Indian time.

**23.** Read the header row into a dictionary of `name → column index` for each file, then address columns by name. If a branch adds a column, the macro still finds `net_revenue`; if a column is missing, it can say which one instead of silently summing the wrong data.

**24.** For example: twelve files read; the sum of per-file row counts equals the `Master` row count; and the quarter's total within 25% of the previous run stored on `History`. Each check writes PASS or FAIL with its numbers to a log sheet, and any FAIL stops the email.

**25.** Power Query wins on effort and maintainability (a few clicks, no macro security, refreshable) and can't do the PDF, the email, or the formatting. The macro wins on those and loses on everything else. The realistic answer for many teams is both: Power Query to build `Master`, a short macro to format, export, and send.

**26.** Exported `.bas` files are plain text, so Git shows exactly which lines changed; the `.xlsm` is a binary blob where Git can only say "the file changed". Commit the exports, keep the workbook as a build artifact, and note the version in a `Config` cell.

**27.** First, **make it safe**: take a copy, and find out who receives it and what they do with it. Second, **make it visible**: run it once yourself in a test copy of the folder with `.Display` instead of `.Send`, and read the log; add `Debug.Print` lines if there are none. Third, **make it explainable**: write the one-page note (inputs, outputs, schedule, failure modes), then decide whether to refactor or rewrite. Don't start by rewriting it; start by being able to describe it.

**28.** When it works, the owner understands it, the data and audience are already in Excel, and the rewrite would buy nothing but elegance. A working automation with a documented owner and a check that stops it when the data is wrong is a good outcome, whatever language it's in. Rewrite when it's fragile, unreadable, unowned, or needs data and scheduling that a spreadsheet can't reach.

**Timed challenge answers.** Level 1: **12** `.xlsx` files; `*.xls*` matches the same twelve here, but would also pick up `.xlsb` and legacy `.xls` files, which is a reason to be specific. Level 2: **25,832** rows. Level 3: 25,832 data rows plus one header. Level 4: **₹42,38,72,808.00**. Level 5: Mumbai HO ₹15,10,58,519.25 · Bengaluru ₹11,77,26,527.00 · Delhi ₹10,29,66,828.00 · Kolkata ₹5,21,20,933.75. Level 6: Oct ₹18,06,20,103.00 · Nov ₹15,59,85,902.00 · Dec ₹8,72,66,803.75. Level 7: seconds versus effectively instant. Bonus: the `EXPECTED_FILES` check in section 19.6's `ConsolidateBranchFiles`, which stops the macro with `Err.Raise` if `filesRead <> 12`.

---

## Where this leads

- **Chapter 12, Databases & SQL Foundations:** where Riverstone's data lives before it reaches a workbook, and how to ask it questions directly.
- **Chapter 20, Automating Reports & Delivering Insights:** scheduling, HTML email at scale, alerts, failure handling, and choosing between VBA, Apps Script, Python, and low-code flows.
- **Chapter 11** remains the first answer for refreshable data shaping; **Chapter 16** for shared, interactive reporting.
- **Chapter 18, Python for Analysts:** the same automations when the data comes from a database or an API, or must run unattended.
- **Chapter 26, Git:** versioning exported modules and scripts.
- **Chapter 46:** orchestration, when an automation grows into a pipeline with dependencies and retries.
- **Interview preparation:** the Excel, Google Sheets, VBA & BI Question Bank (Chapter 70) covers the object model, the last-row pattern, and "how would you make this macro faster?".
