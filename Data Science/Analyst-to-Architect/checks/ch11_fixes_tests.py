"""Chapter 11 (Part 2 build, 28 Sep 2026): every formula result added or changed by the review fixes,
evaluated by LibreOffice headless on the companion workbooks (ch11_practice.xlsx, the messy month-end
pack, and Chapter 4's numbers_practice.xlsx). XLOOKUP is not in LibreOffice 24.2, so its results are
checked with pandas at the end.
Run from the book root:  python3 checks/ch11_fixes_tests.py"""
import subprocess, shutil, pathlib, datetime as dt
import pandas as pd
from openpyxl import load_workbook

W = pathlib.Path("/tmp/ch11fix")  # scratch; shutil.rmtree(W, ignore_errors=True); W.mkdir()


def run(src, tests, setup=None):
    wb = load_workbook(src)
    T = wb.create_sheet("Tests")
    if setup:
        setup(wb)
    for i, (n, f) in enumerate(tests, start=1):
        T.cell(row=i, column=1, value=n); T.cell(row=i, column=2, value=f)
    name = pathlib.Path(src).stem + "_t.xlsx"
    wb.save(W / name)
    subprocess.run(["soffice", "-env:UserInstallation=file:///tmp/ch11fix_profile", "--headless", "--convert-to", "xlsx", "--outdir", str(W / "o"), str(W / name)],
                   capture_output=True)
    r = load_workbook(W / "o" / name, data_only=True)["Tests"]
    for i, (n, f) in enumerate(tests, start=1):
        print(f"  {n:52} -> {r.cell(row=i, column=2).value!r}")


S = lambda c: f"Sales!{c}2:{c}331"
print("ch11_practice.xlsx")


def grid(wb):
    # Section 11.4 two-way grid: months in A5:A16, segments in B4:D4, SUMIFS in B5:D16 (sheet Grid)
    G = wb.create_sheet("Grid")
    for j, s in enumerate(["Hospitality", "Retail", "Wholesale"]):
        G.cell(row=4, column=2 + j, value=s)
    for i in range(12):
        G.cell(row=5 + i, column=1, value=dt.datetime(2025, i + 1, 1))
        for j in range(3):
            col = "BCD"[j]
            G.cell(row=5 + i, column=2 + j,
                   value=f'=SUMIFS(Sales!$J$2:$J$331,Sales!$K$2:$K$331,$A{5+i},Sales!$N$2:$N$331,{col}$4,'
                         f'Sales!$H$2:$H$331,"<>Cancelled")')
    # Section 11.2 Report sheet: month starts F2:F13, valid revenue G2:G13
    R = wb.create_sheet("Report")
    for i in range(12):
        R.cell(row=2 + i, column=6, value=dt.datetime(2025, i + 1, 1))
        R.cell(row=2 + i, column=7,
               value=f'=SUMIFS(Sales!$J$2:$J$331,Sales!$K$2:$K$331,F{2+i},Sales!$H$2:$H$331,"<>Cancelled")')
        R.cell(row=2 + i, column=8, value=f"=G{3+i}-G{2+i}" if i < 11 else None)


run("companion/ch11/ch11_practice.xlsx", [
    ("11.3 cell 1: --(Wholesale)", f'=SUMPRODUCT(--({S("N")}="Wholesale"))'),
    ("11.3 cell 2: Wholesale AND not cancelled", f'=SUMPRODUCT(({S("N")}="Wholesale")*({S("H")}<>"Cancelled"))'),
    ("11.3 cell 3: (W+Q)*valid", f'=SUMPRODUCT((({S("N")}="Wholesale")+({S("E")}>=50))*({S("H")}<>"Cancelled"))'),
    ("11.3 cell 3 no status", f'=SUMPRODUCT(({S("N")}="Wholesale")+({S("E")}>=50))'),
    ("11.3 cell 3b: both tests true", f'=SUMPRODUCT(({S("N")}="Wholesale")*({S("E")}>=50))'),
    ("11.3 cell 3c: qty>=50 all statuses", f'=SUMPRODUCT(--({S("E")}>=50))'),
    ("11.3 cell 4 no status: ((W)+(Q))>0", f'=SUMPRODUCT(--((({S("N")}="Wholesale")+({S("E")}>=50))>0))'),
    ("11.3 final: OR AND valid", f'=SUMPRODUCT(((({S("N")}="Wholesale")+({S("E")}>=50))>0)*({S("H")}<>"Cancelled"))'),
    ("11.3 revenue", f'=SUMPRODUCT(((({S("N")}="Wholesale")+({S("E")}>=50))>0)*({S("H")}<>"Cancelled")*{S("J")})'),
    ("11.3 cancelled lines with qty>=50", f'=COUNTIFS({S("E")},">=50",{S("H")},"Cancelled")'),
    ("11.19 weighted discount (filtered)", f'=SUMPRODUCT({S("G")},{S("E")}*{S("F")}*({S("H")}<>"Cancelled"))/SUMPRODUCT({S("E")}*{S("F")}*({S("H")}<>"Cancelled"))'),
    ("11.4 IF J5", '=IF(Sales!J5>=30000,"Large","Not large")'),
    ("11.4 IFS J2", '=_xlfn.IFS(Sales!J2>=30000,"Large",Sales!J2>=10000,"Medium",TRUE(),"Small")'),
    ("11.4 SWITCH H2", '=_xlfn.SWITCH(Sales!H2,"Delivered","Closed","Shipped","In transit","Pending","Open","Cancelled","Void")'),
    ("11.4 CHOOSE B2", '=CHOOSE(ROUNDUP(MONTH(Sales!B2)/3,0),"Q1","Q2","Q3","Q4")'),
    ("11.4 IFERROR J2/E2", "=IFERROR(Sales!J2/Sales!E2,0)"),
    ("11.4 J5 / E5 / F5 / G5", '=Sales!J5&" / "&Sales!E5&" / "&Sales!F5&" / "&Sales!G5'),
    ("11.4 NOT H2", '=NOT(Sales!H2="Cancelled")'),
    ("11.11 XOR G2>0, E2>=50", "=_xlfn.XOR(Sales!G2>0,Sales!E2>=50)"),
    ("11.11 XOR row 5 (G5>0, E5>=50)", "=_xlfn.XOR(Sales!G5>0,Sales!E5>=50)"),
    ("11.11 DATEDIF ym", '=DATEDIF(DATE(2025,1,24),DATE(2025,12,5),"ym")'),
    ("11.11 DATEDIF md", '=DATEDIF(DATE(2025,1,24),DATE(2025,12,5),"md")'),
    ("11.11 DATEDIF y", '=DATEDIF(DATE(2025,1,24),DATE(2025,12,5),"y")'),
    ("11.11 _xlfn.CEILING.MATH(45,10)", "=_xlfn.CEILING.MATH(45,10)"),
    ("11.11 LARGE 2", f"=LARGE({S('J')},2)"),
    ("11.11 RANK.EQ 51520 desc", f"=_xlfn.RANK.EQ(51520,{S('J')},0)"),
    ("11.11 RANK.EQ 51520 asc", f"=_xlfn.RANK.EQ(51520,{S('J')},1)"),
    ("11.11 QUARTILE.INC 1", f"=_xlfn.QUARTILE.INC({S('J')},1)"),
    ("11.11 PERCENTILE.INC 0.25", f"=_xlfn.PERCENTILE.INC({S('J')},0.25)"),
    ("11.11 MODE.SNGL qty all", f"=_xlfn.MODE.SNGL({S('E')})"),
    ("11.11 PMT", "=PMT(10%/12,36,-500000)"),
    ("11.11 SUBSTITUTE instance", '=SUBSTITUTE("SO-10001-A","-","",1)'),
    ("11.11 NUMBERVALUE", '=_xlfn.NUMBERVALUE("4.335.471,00",",",".")'),
    ("11.12 ROW() in this cell", "=ROW()"),
    ("11.12 ROWS(A2:A331)", "=ROWS(Sales!A2:A331)"),
    ("11.15 COUNTIF text '101' vs number", '=COUNTIF(Tests!D1:D3,101)'),
    ("11.15 SUM of mixed", "=SUM(Tests!D1:D3)"),
    ("11.13 MATCH month", "=MATCH(DATE(2025,10,1),Grid!A5:A16,0)"),
    ("11.13 MATCH segment", '=MATCH("Wholesale",Grid!B4:D4,0)'),
    ("11.13 INDEX two-way", '=INDEX(Grid!B5:D16,MATCH(DATE(2025,10,1),Grid!A5:A16,0),MATCH("Wholesale",Grid!B4:D4,0))'),
    ("11.13 ex24 Retail March", '=INDEX(Grid!B5:D16,MATCH(DATE(2025,3,1),Grid!A5:A16,0),MATCH("Retail",Grid!B4:D4,0))'),
    ("11.13 ex24 Hospitality July", '=INDEX(Grid!B5:D16,MATCH(DATE(2025,7,1),Grid!A5:A16,0),MATCH("Hospitality",Grid!B4:D4,0))'),
    ("11.20 G3:G13-G2:G12 first", "=Report!H2"),
    ("11.20 G3:G13-G2:G12 last", "=Report!H12"),
    ("11.20 max of differences", "=MAX(Report!H2:H12)"),
    ("11.20 min of differences", "=MIN(Report!H2:H12)"),
    ("11.20 Report G2 (Jan)", "=Report!G2"),
    ("11.8 ans33 old denominator W", f'=SUMPRODUCT(({S("N")}="Wholesale")*({S("H")}<>"Cancelled")/COUNTIFS({S("M")},{S("M")},{S("N")},{S("N")},{S("H")},{S("H")}))'),
    ("11.8 ans33 old denominator R", f'=SUMPRODUCT(({S("N")}="Retail")*({S("H")}<>"Cancelled")/COUNTIFS({S("M")},{S("M")},{S("N")},{S("N")},{S("H")},{S("H")}))'),
    ("11.8 ans33 old denominator H", f'=SUMPRODUCT(({S("N")}="Hospitality")*({S("H")}<>"Cancelled")/COUNTIFS({S("M")},{S("M")},{S("N")},{S("N")},{S("H")},{S("H")}))'),
    ("11.8 ans33 new W", f'=SUMPRODUCT(({S("N")}="Wholesale")*({S("H")}<>"Cancelled")/COUNTIFS({S("M")},{S("M")},{S("H")},"<>Cancelled"))'),
    ("11.8 ans33 new R", f'=SUMPRODUCT(({S("N")}="Retail")*({S("H")}<>"Cancelled")/COUNTIFS({S("M")},{S("M")},{S("H")},"<>Cancelled"))'),
    ("11.8 ans33 new H", f'=SUMPRODUCT(({S("N")}="Hospitality")*({S("H")}<>"Cancelled")/COUNTIFS({S("M")},{S("M")},{S("H")},"<>Cancelled"))'),
    ("11.8 ans33 IFERROR W", f'=SUMPRODUCT(IFERROR(({S("N")}="Wholesale")*({S("H")}<>"Cancelled")/COUNTIFS({S("M")},{S("M")},{S("H")},"<>Cancelled"),0))'),
    ("distinct valid orders", f'=SUMPRODUCT(({S("H")}<>"Cancelled")/COUNTIFS({S("A")},{S("A")}))'),
    ("Wholesale per line (denominator)", f'=SUMIFS({S("J")},{S("N")},"Wholesale",{S("H")},"<>Cancelled")/COUNTIFS({S("N")},"Wholesale",{S("H")},"<>Cancelled")'),
    ("Wholesale per customer (/6)", f'=SUMIFS({S("J")},{S("N")},"Wholesale",{S("H")},"<>Cancelled")/6'),
    ("Wholesale distinct customers", f'=SUMPRODUCT(({S("N")}="Wholesale")/COUNTIF({S("M")},{S("M")}))'),
    ("status cancelled lines", f'=COUNTIF({S("H")},"Cancelled")'),
    ("stockroom ROW trace", "=10-7"),
], setup=lambda wb: (grid(wb), wb["Tests"].__setitem__("D1", 101), wb["Tests"].__setitem__("D2", "101"),
                     wb["Tests"].__setitem__("D3", 5)))

print("month_end_pack_2025_messy.xlsx")


def summ(wb):
    wb["Summary"]["G4"] = "=\"'\"&A4&\"'!J2:J100\""


run("companion/ch11/month_end_pack_2025_messy.xlsx", [
    ("11.14 B4 text", "=Summary!G4"),
    ("11.14 SUM(INDIRECT) Jan", "=SUM(INDIRECT(Summary!G4))"),
    ("11.14 SUMIFS(INDIRECT) Jan", "=SUMIFS(INDIRECT(\"'\"&Summary!A4&\"'!J2:J100\"),INDIRECT(\"'\"&Summary!A4&\"'!H2:H100\"),\"<>Cancelled\")"),
    ("11.14 SUMIFS(INDIRECT) Oct", "=SUMIFS(INDIRECT(\"'\"&Summary!A13&\"'!J2:J100\"),INDIRECT(\"'\"&Summary!A13&\"'!H2:H100\"),\"<>Cancelled\")"),
    ("11.14 SUMIFS(INDIRECT) Dec", "=SUMIFS(INDIRECT(\"'\"&Summary!A15&\"'!J2:J100\"),INDIRECT(\"'\"&Summary!A15&\"'!H2:H100\"),\"<>Cancelled\")"),
    ("Summary total", "=Summary!B16"),
], setup=summ)

print("numbers_practice.xlsx (Chapter 4)")
run("companion/ch04/numbers_practice.xlsx", [
    ("11.19 weighted discount (discounts sheet)", "=SUMPRODUCT(discounts!A2:A6,discounts!C2:C6)/SUM(discounts!C2:C6)"),
    ("11.19 simple (per line) discount", "=SUMPRODUCT(discounts!A2:A6,discounts!B2:B6)/SUM(discounts!B2:B6)"),
    ("11.19 Oct margin", "=monthly!E11"),
    ("11.19 Nov margin", "=monthly!E12"),
    ("11.19 points (E12-E11)*100", "=(monthly!E12-monthly!E11)*100"),
    ("11.19 percent change (E12-E11)/E11", "=(monthly!E12-monthly!E11)/monthly!E11"),
    ("11.19 rounded shares", "=segments!D2&\" \"&segments!D3&\" \"&segments!D4"),
    ("11.19 rounded shares sum", "=segments!D5"),
    ("11.19 unrounded shares sum", "=segments!C5"),
])

print("pandas checks (XLOOKUP and data facts)")
s = pd.read_excel("companion/ch11/ch11_practice.xlsx", sheet_name="Sales", dtype={"customer_code": str})
c = pd.read_excel("companion/ch11/ch11_practice.xlsx", sheet_name="Customers", dtype={"customer_code": str})
v = s[s.status != "Cancelled"]
print("  every order has one status:", (s.groupby("order_id").status.nunique() == 1).all())
print("  IFNA(XLOOKUP('9999')) ->", "not found" if "9999" not in set(c.customer_code) else "found")
print("  rows 2-4 tests (Wholesale, qty>=50):")
for i, r in s.head(40).iterrows():
    pass
w = (s.segment == "Wholesale").astype(int); q = (s.quantity >= 50).astype(int)
ex = s.assign(W=w, Q=q, sum_=w + q, or_=(w + q > 0).astype(int))
for kind in [(1, 0), (0, 1), (1, 1)]:
    r = ex[(ex.W == kind[0]) & (ex.Q == kind[1])].iloc[0]
    print(f"    sheet row {r.name + 2}: order {r.order_id} {r.segment} qty {r.quantity} -> W {r.W} Q {r.Q} sum {r.sum_} >0 {r.or_}")
print("  cancelled distinct customers per segment:", v.groupby("segment").customer_name.nunique().to_dict())
m = v.groupby("month_start").net_revenue.sum()
print("  month diffs:", m.diff().dropna().round(2).tolist())
print("  Wholesale Oct:", v[(v.segment == "Wholesale") & (v.month_start == "2025-10-01")].net_revenue.sum())
print("  profile of status (all 330):", s.status.value_counts().to_dict())
