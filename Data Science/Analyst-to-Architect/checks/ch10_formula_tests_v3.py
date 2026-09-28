"""Chapter 10 v3 additions (Part 2 build, 28 Sep 2026): every formula added or changed in this build,
evaluated by LibreOffice on the companion workbooks, so no result in the chapter is typed by hand.

Run from the book root after companion/ch10/build_ch10_files.py:
    python3 checks/ch10_formula_tests_v3.py

LibreOffice 24.2 has no XLOOKUP, so the XLOOKUP results are checked with the equivalent
INDEX/MATCH (same arguments, same "not found" value) on ch10_tracker_check.xlsx."""
import subprocess, shutil, pathlib, datetime as dt
from openpyxl import load_workbook

work = pathlib.Path("/tmp/ch10v3"); shutil.rmtree(work, ignore_errors=True); work.mkdir()


def run(src, sheet_tests, setup=None):
    """Copy a workbook, add a Tests sheet with the formulas, recalculate in LibreOffice, read results."""
    wb = load_workbook(src)
    if setup: setup(wb)
    T = wb.create_sheet("Tests")
    for i, (n, f) in enumerate(sheet_tests, start=1):
        T.cell(row=i, column=1, value=n); T.cell(row=i, column=2, value=f)
    name = pathlib.Path(src).stem
    wb.save(work / f"{name}.xlsx")
    for attempt in range(6):   # LibreOffice sometimes refuses a file while another instance is busy; retry
        subprocess.run(["soffice", f"-env:UserInstallation=file:///tmp/ch10v3_profile{attempt}", "--headless",
                        "--convert-to", "xlsx", "--outdir", str(work / "out"), str(work / f"{name}.xlsx")],
                       capture_output=True)
        if (work / "out" / f"{name}.xlsx").exists(): break
    r = load_workbook(work / "out" / f"{name}.xlsx", data_only=True)
    res = {}
    for i, (n, f) in enumerate(sheet_tests, start=1):
        v = r["Tests"].cell(row=i, column=2).value
        res[n] = v
        print(f"{n:42} {f[:70]:70} -> {v!r}")
    return res, r


print("== §10.0 first run and §10.3 cell detective (ch10_practice.xlsx)")
def first_run(wb):
    ws = wb.create_sheet("First run"); ws["A1"] = 2.5; ws["B1"] = "=ROUND(A1,0)"; ws["A2"] = 2.4; ws["B2"] = "=ROUND(A2,0)"
run("companion/ch10/ch10_practice.xlsx", [
    ("ROUND(2.5,0)", "='First run'!B1"), ("ROUND(2.4,0)", "='First run'!B2"),
    ("ISNUMBER(A2)", "=ISNUMBER('Cell detective'!A2)"), ("ISTEXT(A3)", "=ISTEXT('Cell detective'!A3)"),
    ("LEN(A3)", "=LEN('Cell detective'!A3)"), ("LEN(A4)", "=LEN('Cell detective'!A4)"),
    ("ISNUMBER(A5)", "=ISNUMBER('Cell detective'!A5)"), ("ISNUMBER(A6)", "=ISNUMBER('Cell detective'!A6)"),
    ("SUM(A2:A4)", "=SUM('Cell detective'!A2:A4)"),
    ("ISTEXT(A8)", "=ISTEXT('Cell detective'!A8)"), ("LEN(A8)", "=LEN('Cell detective'!A8)"),
    ("A8 value", "='Cell detective'!A8"),
    ("=Data!B2 as a number", "=Data!B2*1"),
    ("status bar E: SUM", "=SUM(Data!E2:E331)"), ("status bar E: AVERAGE", "=AVERAGE(Data!E2:E331)"),
    ("status bar E: COUNT", "=COUNT(Data!E2:E331)"),
    ("rows in Cell detective", "=COUNTA('Cell detective'!A2:A20)"),
], setup=first_run)

print("\n== Formulas on the finished Data sheet (ch10_tracker_check.xlsx)")
def p_cells(wb):
    wb["Data"]["P1"] = "=DATE(2025,11,1)"; wb["Data"]["P2"] = "=DATE(2025,11,30)"
res, book = run("companion/ch10/ch10_tracker_check.xlsx", [
    ("P3 criterion from a cell", '=">="&Data!P1'),
    ("P-cells: + start", '=SUMIFS(Data!J2:J331,Data!H2:H331,"<>Cancelled",Data!B2:B331,">="&Data!P1)'),
    ("P-cells: + end", '=SUMIFS(Data!J2:J331,Data!H2:H331,"<>Cancelled",Data!B2:B331,">="&Data!P1,Data!B2:B331,"<="&Data!P2)'),
    ("I2", "=Data!I2"),
    ("FIND space in I2", '=FIND(" ",Data!I2)'), ("LEFT(I2,5-1)", "=LEFT(Data!I2,5-1)"),
    ("LEFT with FIND", '=LEFT(Data!I2,FIND(" ",Data!I2)-1)'), ("MID(I2,5+1,100)", "=MID(Data!I2,5+1,100)"),
    ("MID with FIND", '=MID(Data!I2,FIND(" ",Data!I2)+1,100)'),
    ("TIME(9,15,0)", "=TIME(9,15,0)"), ("TIME(17,30,0)", "=TIME(17,30,0)"),
    ("difference", "=TIME(17,30,0)-TIME(9,15,0)"), ("difference*24", "=(TIME(17,30,0)-TIME(9,15,0))*24"),
    ("SUMIF Delivered", '=SUMIF(Data!H2:H331,"Delivered",Data!J2:J331)'),
    ("SUMIFS Delivered", '=SUMIFS(Data!J2:J331,Data!H2:H331,"Delivered")'),
    ("DATE(2025,11,1)", "=DATE(2025,11,1)"), ("criterion text", '=">="&DATE(2025,11,1)'),
    ("SUMIFS status only", '=SUMIFS(Data!J2:J331,Data!H2:H331,"<>Cancelled")'),
    ("+ start date", '=SUMIFS(Data!J2:J331,Data!H2:H331,"<>Cancelled",Data!B2:B331,">="&DATE(2025,11,1))'),
    ("+ end date", '=SUMIFS(Data!J2:J331,Data!H2:H331,"<>Cancelled",Data!B2:B331,">="&DATE(2025,11,1),Data!B2:B331,"<="&DATE(2025,11,30))'),
    ("chapter order (sum, dates, status)", '=SUMIFS(Data!J2:J331,Data!B2:B331,">="&DATE(2025,11,1),Data!B2:B331,"<="&DATE(2025,11,30),Data!H2:H331,"<>Cancelled")'),
    ("MAXIFS not cancelled", '=_xlfn.MAXIFS(Data!J2:J331,Data!H2:H331,"<>Cancelled")'),
    ("MAXIFS Retail", '=_xlfn.MAXIFS(Data!J2:J331,Data!N2:N331,"Retail",Data!H2:H331,"<>Cancelled")'),
    ("MINIFS not cancelled", '=_xlfn.MINIFS(Data!J2:J331,Data!H2:H331,"<>Cancelled")'),
    ("lookup text 0005 (XLOOKUP equivalent)", '=IFERROR(INDEX(Customers!B2:B25,MATCH("0005",Customers!A2:A25,0)),"not found")'),
    ("lookup number 5 (XLOOKUP equivalent)", '=IFERROR(INDEX(Customers!B2:B25,MATCH(5,Customers!A2:A25,0)),"not found")'),
    ("C2 code", "=Data!C2"), ("M2 name", "=Data!M2"), ("N2 segment", "=Data!N2"),
    ("COUNTIF trace L4", "=COUNTIF(Data!$A$2:A4,Data!A4)"), ("COUNTIF trace L5", "=COUNTIF(Data!$A$2:A5,Data!A5)"),
    ("A4", "=Data!A4"), ("A5", "=Data!A5"), ("L4", "=Data!L4"), ("L5", "=Data!L5"),
    ("Farah Khan", '=SUMIFS(Data!$J$2:$J$331,Data!$I$2:$I$331,"Farah Khan",Data!$H$2:$H$331,"<>Cancelled")'),
    ("Reps!G1 default", "=Reps!G1"), ("Reps!G2", "=Reps!G2"),
    ("Wholesale orders", '=SUMIFS(Data!L2:L331,Data!N2:N331,"Wholesale",Data!H2:H331,"<>Cancelled")'),
    ("Nov wholesale lines (SUBTOTAL 103 check)", '=COUNTIFS(Data!N2:N331,"Wholesale",Data!K2:K331,DATE(2025,11,1))'),
    ("TEXTJOIN", '=_xlfn.TEXTJOIN(", ",TRUE,Customers!B2:B4)'),
    ("RIGHT", '=RIGHT("RS-2025-0418",4)'),
    ("COUNTIF order_id duplicates flagged", "=SUMPRODUCT((COUNTIF(Data!A2:A331,Data!A2:A331)>1)*1)"),
    ("COUNTIF customers duplicates flagged", "=SUMPRODUCT((COUNTIF(Customers!A2:A25,Customers!A2:A25)>1)*1)"),
    ("Tracker total D17", "=Tracker!D17"), ("Tracker check D20", "=Tracker!D20"),
    ("rounded months add to", "=SUMPRODUCT(ROUND(Tracker!D5:D16,0))"),
], setup=p_cells)
t = book["Tracker"]
print("Tracker D5:D16 (month key version):", [round(t.cell(row=r, column=4).value, 2) for r in range(5, 17)])
print("Tracker C5:C16:", [t.cell(row=r, column=3).value for r in range(5, 17)])

print("\n== Back to Chapter 4 (companion/ch04/numbers_practice.xlsx)")
run("companion/ch04/numbers_practice.xlsx", [
    ("AVERAGE orders", "=AVERAGE(orders!B2:B174)"), ("MEDIAN orders", "=MEDIAN(orders!B2:B174)"),
    ("COUNT orders", "=COUNT(orders!B2:B174)"),
    ("COUNTIF above mean", '=COUNTIF(orders!B2:B174,">"&orders!E1)'),
    ("B2 Jan", "=monthly!B2"), ("B3 Feb", "=monthly!B3"), ("B13 Dec", "=monthly!B13"),
    ("pct change Jan->Feb", "=(monthly!B3-monthly!B2)/monthly!B2"),
    ("reverse pct 1276", "=1276/(1-12%)"),
    ("compound ^", "=(439824/202640)^(1/11)-1"), ("compound ^ from cells", "=(monthly!B13/monthly!B2)^(1/11)-1"),
    ("RRI 11", "=_xlfn.RRI(11,202640,439824)"), ("RRI 3", "=_xlfn.RRI(3,4335471,6000000)"),
    ("AVERAGE F3:F13", "=AVERAGE(monthly!F3:F13)"),
    ("ROUND sig figs", "=ROUND(4335471,-5)"), ("ROUND 2 sig figs", "=ROUND(4335471,-6)"),
    ("ROUND mean", "=ROUND(AVERAGE(orders!B2:B174),0)"),
    ("monthly total", "=monthly!B15"),
])

# Independent check of the damage counts (Python, not LibreOffice)
import csv
rows = list(csv.DictReader(open("companion/ch10/riverstone_sales_export_2025.csv")))
d = [(int(r["order_date"][:2]), int(r["order_date"][3:5])) for r in rows]
print("\ndates read month-first: wrong real dates", sum(1 for a, b in d if a <= 12 and a != b),
      "| right by luck", sum(1 for a, b in d if a == b), "| left as text", sum(1 for a, b in d if a > 12))
print("DATE(2025,11,1) serial:", (dt.date(2025, 11, 1) - dt.date(1899, 12, 30)).days)
