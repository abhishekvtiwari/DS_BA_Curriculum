"""Chapter 11 challenge: run the helper-column solution workbook in LibreOffice for each level's parameters and
compare with the Python simulation. Run from the book root:  python3 checks/ch11_challenge_lo.py"""
import subprocess, shutil, pathlib
from openpyxl import load_workbook
src = "companion/ch11/challenge/riverstone_stockroom_solution.xlsx"
w = pathlib.Path("/tmp/chlo"); shutil.rmtree(w, ignore_errors=True); w.mkdir()
cases = {"L2_no_reorder": (-100000, 250, 7), "L3_L4": (100, 250, 7), "L4_rop150": (150, 250, 7), "L5_best": (50, 150, 7), "bonus_best": (50, 200, 14)}
for name, (rop, q, lead) in cases.items():
    wb = load_workbook(src)
    P = wb["Parameters"]; P["B3"] = rop; P["B4"] = q; P["B5"] = lead
    R = wb["Results"]
    R["A13"] = "first negative date"; R["B13"] = '=IF(COUNTIF(Model!F2:F366,"<0")=0,"none",TEXT(MINIFS(Model!A2:A366,Model!F2:F366,"<0"),"yyyy-mm-dd"))'.replace("MINIFS", "_xlfn.MINIFS")
    R["A14"] = "L1a via SUMPRODUCT on raw codes"; R["B14"] = '=SUMPRODUCT((RIGHT(Log!A2:A331,3)<>"CAN")*MID(Log!A2:A331,31,FIND("@",Log!A2:A331)-31))'
    R["A15"] = "L1b units per product 101..108"; R["B15"] = '=SUMIFS(Log!F2:F331,Log!E2:E331,107,Log!I2:I331,"<>CAN")&"/"&SUMIFS(Log!F2:F331,Log!E2:E331,108,Log!I2:I331,"<>CAN")'
    wb.save(w / f"{name}.xlsx")
    subprocess.run(["soffice", "--headless", "--convert-to", "xlsx", "--outdir", str(w / "o"), str(w / f"{name}.xlsx")], capture_output=True)
    r = load_workbook(w / "o" / f"{name}.xlsx", data_only=True)["Results"]
    vals = {r.cell(row=i, column=1).value: r.cell(row=i, column=2).value for i in range(1, 16)}
    print(name, {k: vals[k] for k in ["POs placed", "lowest closing", "date of lowest", "negative days", "31 Dec closing", "total cost", "first negative date"]})
    if name == "L3_L4": print("  L1:", vals["L1a total units, non-cancelled"], vals["L1a via SUMPRODUCT on raw codes"], vals["L1b units of product 101 (compare each product)"], vals["L1b units per product 101..108"], vals["L1c units of 101 bought by C0012"])
