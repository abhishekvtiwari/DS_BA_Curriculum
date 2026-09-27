' Analyst to Architect, Chapter 19 — VBA modules from the chapter.
' Import with File > Import File in the VBA editor (Alt+F11), or paste into a module.
' Riverstone Supplies is fictional; every name and number is invented.

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


Sub FormatSalesSheet(ws As Worksheet)
    With ws
        .Rows(1).Font.Bold = True
        .Activate                          ' FreezePanes needs the sheet visible
        .Range("A2").Select
        ActiveWindow.FreezePanes = True
        .Cells.EntireColumn.AutoFit
    End With
End Sub


Option Explicit                       ' every variable must be declared

Sub SayHello()
    ' a comment starts with an apostrophe
    MsgBox "Hello from Riverstone"     ' shows a dialog box
    Debug.Print "this goes to the Immediate window"
End Sub


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


Sub CheckTarget(actual As Double, target As Double)
    If actual >= target Then
        Debug.Print "Above target"
    ElseIf actual >= target * 0.9 Then
        Debug.Print "Close: " & Format(actual / target, "0.0%")
    Else
        Debug.Print "Below target by " & Format(target - actual, "#,##0")
    End If
End Sub

Sub BandBySize(value As Double)
    Select Case value
        Case Is >= 50000
            Debug.Print "very large"
        Case 25000 To 49999.99
            Debug.Print "large"
        Case 10000 To 24999.99
            Debug.Print "medium"
        Case Else
            Debug.Print "small"
    End Select
End Sub


Sub LoopDemo()
    Dim i As Long, ws As Worksheet, total As Double

    For i = 1 To 5                                   ' counted loop
        Debug.Print "row " & i
    Next i

    For Each ws In ThisWorkbook.Worksheets           ' loop a collection
        Debug.Print ws.Name & " has " & ws.UsedRange.Rows.Count & " rows"
    Next ws

    i = 1
    Do While ThisWorkbook.Worksheets(1).Cells(i, 1).Value <> ""   ' loop until a condition fails
        total = total + ThisWorkbook.Worksheets(1).Cells(i, 11).Value
        i = i + 1
    Loop
    Debug.Print "total " & total
End Sub


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
    Debug.Print targets("Bengaluru"), targets.Exists("Delhi")
End Sub


Function NetLine(quantity As Long, unitPrice As Double, Optional discountPct As Double = 0) As Double
    NetLine = quantity * unitPrice * (1 - discountPct / 100)
End Function

Sub UseIt()
    Debug.Print NetLine(45, 430, 5)        ' 18382.5
    Debug.Print NetLine(10, 290)           ' 2900
End Sub


Private Const SOURCE_FOLDER As String = "C:\Riverstone\branch_files\"
Private Const MASTER_SHEET As String = "Master"


Sub ObjectBasics()
    Dim wb As Workbook, ws As Worksheet, rng As Range

    Set wb = ThisWorkbook                          ' the workbook holding this code
    Set ws = wb.Worksheets("Master")               ' by name, not by position
    Set rng = ws.Range("A1:K1")

    ws.Range("A1").Value = "order_item_id"
    ws.Cells(2, 1).Value = 184000                  ' Cells(row, column): easier in loops
    rng.Font.Bold = True
    Debug.Print ws.Name, ws.Cells(1, 1).Value, rng.Address
End Sub


Sub RangeToolkit()
    Dim ws As Worksheet, lastRow As Long, lastCol As Long
    Set ws = ThisWorkbook.Worksheets("Master")

    lastRow = ws.Cells(ws.Rows.Count, "A").End(xlUp).Row          ' last used row in column A
    lastCol = ws.Cells(1, ws.Columns.Count).End(xlToLeft).Column  ' last used column in row 1
    Debug.Print lastRow, lastCol

    Dim data As Range
    Set data = ws.Range(ws.Cells(2, 1), ws.Cells(lastRow, lastCol))   ' the data without the header
    Debug.Print data.Address, data.Rows.Count

    ws.Range("A1").CurrentRegion.Select                            ' the contiguous block, like Ctrl+A
    ws.Rows(1).Insert                                              ' insert, delete, clear
    ws.Rows(1).Delete
    ws.Range("L:L").ClearContents
End Sub


' recorded
Sheets("Master").Select
Range("A1").Select
Selection.Value = "Total"

' written
ThisWorkbook.Worksheets("Master").Range("A1").Value = "Total"


Sub FormatHeader(ws As Worksheet, lastCol As Long)
    With ws.Range(ws.Cells(1, 1), ws.Cells(1, lastCol))
        .Font.Bold = True
        .Font.Color = RGB(255, 255, 255)
        .Interior.Color = RGB(15, 92, 140)
        .HorizontalAlignment = xlCenter
        .EntireColumn.AutoFit
    End With
End Sub


Option Explicit

Private Const SOURCE_FOLDER As String = "C:\Riverstone\branch_files\"
Private Const DATA_SHEET As String = "Sales"

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
        Set src = Workbooks.Open(SOURCE_FOLDER & fileName, ReadOnly:=True)
        Set srcWs = src.Worksheets(DATA_SHEET)

        lastRow = srcWs.Cells(srcWs.Rows.Count, "A").End(xlUp).Row
        lastCol = srcWs.Cells(1, srcWs.Columns.Count).End(xlToLeft).Column

        If nextRow = 1 Then                            ' copy the header once, from the first file
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
        fileName = Dir                                  ' Dir with no argument returns the next file
    Loop

    Application.DisplayAlerts = True
    Application.ScreenUpdating = True

    MsgBox filesRead & " files consolidated, " & Format(nextRow - 2, "#,##0") & " data rows.", vbInformation
End Sub


Sub CleanMaster()
    Dim ws As Worksheet, lastRow As Long, r As Long
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

    For r = 2 To lastRow
        Dim raw As String
        raw = LCase(Trim(ws.Cells(r, 9).Value))          ' column I = status
        If statusMap.Exists(raw) Then
            ws.Cells(r, 9).Value = statusMap(raw)
        Else
            ws.Cells(r, 9).Interior.Color = RGB(255, 235, 200)   ' flag, don't guess
        End If
        ws.Cells(r, 4).Value = Format(ws.Cells(r, 4).Value, "0000")   ' customer_code keeps its zeros
    Next r
End Sub


Sub BuildSummaryPivot()
    Dim ws As Worksheet, pvtWs As Worksheet, lastRow As Long, lastCol As Long
    Dim cache As PivotCache, pvt As PivotTable

    Set ws = ThisWorkbook.Worksheets("Master")
    lastRow = ws.Cells(ws.Rows.Count, "A").End(xlUp).Row
    lastCol = ws.Cells(1, ws.Columns.Count).End(xlToLeft).Column

    On Error Resume Next
    ThisWorkbook.Worksheets("Summary").Delete            ' start clean; DisplayAlerts already off
    On Error GoTo 0
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


Function SaveSummaryAsPdf() As String
    Dim path As String
    path = ThisWorkbook.Path & Application.PathSeparator & _
           "Riverstone_Q4_2025_summary_" & Format(Date, "yyyy-mm-dd") & ".pdf"

    ThisWorkbook.Worksheets("Summary").ExportAsFixedFormat _
        Type:=xlTypePDF, FileName:=path, Quality:=xlQualityStandard, OpenAfterPublish:=False

    SaveSummaryAsPdf = path
End Function


Sub EmailSummary(pdfPath As String, netRevenue As Double, rowCount As Long)
    Dim outlookApp As Object, mail As Object
    Dim bodyHtml As String

    Set outlookApp = CreateObject("Outlook.Application")     ' late binding: no reference needed
    Set mail = outlookApp.CreateItem(0)                      ' 0 = olMailItem

    bodyHtml = "<p>Good morning,</p>" & _
        "<p>Riverstone's Q4 2025 sales summary is attached.</p>" & _
        "<table style='border-collapse:collapse;font-family:Segoe UI,Arial;font-size:13px'>" & _
        "<tr><td style='padding:4px 12px;color:#5b6475'>Net revenue (non-cancelled)</td>" & _
        "<td style='padding:4px 12px;font-weight:bold'>" & Format(netRevenue, "₹#,##0.00") & "</td></tr>" & _
        "<tr><td style='padding:4px 12px;color:#5b6475'>Order lines consolidated</td>" & _
        "<td style='padding:4px 12px;font-weight:bold'>" & Format(rowCount, "#,##0") & "</td></tr>" & _
        "</table>" & _
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


Public Function REBATEPCT(annualValue As Double) As Double
    ' Riverstone's loyalty rebate: 0% standard, 1% from 250,000, 2% from 400,000
    Select Case annualValue
        Case Is >= 400000: REBATEPCT = 2
        Case Is >= 250000: REBATEPCT = 1
        Case Else: REBATEPCT = 0
    End Select
End Function


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


Sub RunConsolidation()
    Dim errorLog As String

    On Error GoTo Failed                       ' from here, any error jumps to the label

    Application.ScreenUpdating = False
    ConsolidateBranchFiles
    CleanMaster
    BuildSummaryPivot

CleanUp:
    Application.ScreenUpdating = True
    Application.DisplayAlerts = True
    Application.Calculation = xlCalculationAutomatic
    Exit Sub                                    ' stop before falling into the handler

Failed:
    errorLog = "Error " & Err.Number & ": " & Err.Description & " (in " & Err.Source & ")"
    Debug.Print errorLog
    MsgBox errorLog & vbCrLf & vbCrLf & "Nothing was emailed.", vbCritical, "Consolidation failed"
    Resume CleanUp                              ' always restore Excel's settings
End Sub


Sub LogLine(message As String)
    Dim f As Integer
    f = FreeFile
    Open ThisWorkbook.Path & Application.PathSeparator & "macro_log.txt" For Append As #f
    Print #f, Format(Now, "yyyy-mm-dd HH:mm:ss") & " " & message
    Close #f
End Sub


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


Sub CleanStatusFast()
    Dim ws As Worksheet, lastRow As Long, r As Long
    Dim values As Variant
    Dim statusMap As Object

    Set ws = ThisWorkbook.Worksheets("Master")
    lastRow = ws.Cells(ws.Rows.Count, "A").End(xlUp).Row

    Set statusMap = CreateObject("Scripting.Dictionary")
    statusMap("delivered") = "Delivered": statusMap("dlvd") = "Delivered"
    statusMap("cancelled") = "Cancelled": statusMap("canceled") = "Cancelled"
    statusMap("cxl") = "Cancelled": statusMap("shipped") = "Shipped"
    statusMap("pending") = "Pending"

    values = ws.Range(ws.Cells(2, 9), ws.Cells(lastRow, 9)).Value2     ' one read
    For r = 1 To UBound(values, 1)
        Dim raw As String
        raw = LCase(Trim(CStr(values(r, 1))))
        If statusMap.Exists(raw) Then values(r, 1) = statusMap(raw)
    Next r
    ws.Range(ws.Cells(2, 9), ws.Cells(lastRow, 9)).Value2 = values      ' one write
End Sub
