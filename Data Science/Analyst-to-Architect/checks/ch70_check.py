"""ch70_check.py - Chapter 70 answers that LibreOffice 24.2 can't evaluate (see checks/ch70_lo.py for the rest).

- XLOOKUP and UNIQUE(FILTER(...)) with the Python `formulas` engine (pip install formulas), on the values of
  companion/ch70/ch70_practice.xlsx.
- Google Sheets QUERY and ARRAYFORMULA (Sheets-only) recomputed with pandas: same rows, same rule.
- Q70-060's DAX numbers (Chapter 16's model) recomputed in SQL on riverstone_full.sales_lines.
Run from the book folder:  python3 checks/ch70_check.py
"""
import subprocess
import formulas
import pandas as pd

O = pd.read_excel("companion/ch70/ch70_practice.xlsx", sheet_name="Orders")
def arr(v): return "{" + ";".join(f'"{x}"' if isinstance(x, str) else str(x) for x in v) + "}"
def run(label, f):
    out = formulas.Parser().ast(f)[1].compile()()
    out = out.tolist() if hasattr(out, "tolist") else out
    print(f"{label:28} -> {out}")

run("Q70-002 XLOOKUP", f'=XLOOKUP("Storage Box 25L",{arr(O.product_name)},{arr(O.unit_price)})')
try:
    run("Q70-009 UNIQUE(FILTER)", f'=UNIQUE(FILTER({arr(O.customer_name)},{arr(O.category)}="Storage"))')
except Exception as e:
    print("Q70-009 UNIQUE(FILTER)       -> engine:", type(e).__name__, "| pandas:",
          O.loc[O.category == "Storage", "customer_name"].drop_duplicates().tolist())
q = (O[O.status != "Cancelled"].groupby("category").net_revenue.sum().sort_values(ascending=False))
print("Q70-034 QUERY (pandas)       ->", q.to_dict())
print("Q70-035 ARRAYFORMULA (pandas)->", ["Yes" if c == "Storage" else "No" for c in O.category])
print("Q70-001 hand check           ->", O[(O.customer_name == "Sharma Hardware") & (O.quantity >= 20)
                                            & (O.status != "Cancelled")].net_revenue.sum())
sql = ("select to_char(order_date,'YYYY-MM') m, round(sum(net_revenue)) from sales_lines "
       "where order_date between '2024-01-01' and '2024-01-31' or order_date between '2025-01-01' and '2025-01-31' "
       "group by 1 order by 1")
r = subprocess.run(["su", "postgres", "-c", f'psql -d riverstone_full -Atc "{sql}"'], capture_output=True, text=True).stdout.split()
ly, ty = (float(x.split("|")[1]) for x in r)
print("Q70-060 Jan 2024 / Jan 2025  ->", r, f"YoY {100 * (ty - ly) / ly:.1f}%")
