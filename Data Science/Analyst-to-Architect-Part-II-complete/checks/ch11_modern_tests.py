"""Chapter 11 (expanded): modern Excel functions evaluated with the Python `formulas` engine (an independent
Excel formula evaluator) on values taken from ch11_practice.xlsx. Functions it can't evaluate are computed with pandas.
Run from the book root:  python3 checks/ch11_modern_tests.py   (needs: pip install formulas)"""
import formulas, pandas as pd, numpy as np
S = pd.read_excel("companion/ch11/ch11_practice.xlsx", sheet_name="Sales", dtype={"customer_code": str})
C = pd.read_excel("companion/ch11/ch11_practice.xlsx", sheet_name="Customers", dtype={"customer_code": str})
def arr(values): return "{" + ";".join(f'"{v}"' if isinstance(v, str) else str(v) for v in values) + "}"
def run(label, f):
    try:
        out = formulas.Parser().ast(f)[1].compile()()
        out = out.tolist() if hasattr(out, "tolist") else out
    except Exception as e:
        out = f"ERR {type(e).__name__}"
    print(f"{label:34} -> {out}")
codes, names = arr(C.customer_code), arr(C.customer_name)
run("XMATCH 0014", f'=XMATCH("0014",{codes})')
run("XLOOKUP wildcard *Bay*", f'=XLOOKUP("*Bay*",{names},{codes},"none",2)')
run("XLOOKUP not found", f'=XLOOKUP("9999",{codes},{names},"not found")')
run("SWITCH", '=SWITCH("Pending","Delivered","Closed","Shipped","In transit","Pending","Open","Void")')
run("LET margin", '=LET(rev,4335471,gm,1137221,gm/rev)')
run("TEXTJOIN", '=TEXTJOIN(", ",TRUE,"Coastal Foods","","Northgate Distributors")')
# multi-criteria XLOOKUP on real columns (first 120 lines are enough to include order 10057)
sub = S.head(120)
run("XLOOKUP multi-criteria", f'=XLOOKUP(1,({arr(sub.customer_name)}="Harbour Traders")*({arr(sub.product_name)}="Industrial Crate"),{arr(sub.order_id)},"none")')
run("FILTER small", '=FILTER({1;2;3},{1;2;3}>1)')
# pandas for functions the engine lacks
ok = S[S.status != "Cancelled"]
cust = ok.groupby("customer_name").net_revenue.sum().sort_values(ascending=False)
print("TAKE(SORTBY) top 3               ->", cust.head(3).round(2).to_dict())
print("TEXTSPLIT Neha Kulkarni          ->", "Neha Kulkarni".split(" "))
m = ok.groupby("month_start").net_revenue.sum().round(2)
print("SCAN running total (last 3)      ->", m.cumsum().round(2).tolist()[-3:])
print("REDUCE max monthly gain          ->", round(m.diff().max(), 2), m.diff().idxmax().date())
print("BYROW grid row totals            ->", ok.pivot_table(index="segment", columns="quarter", values="net_revenue", aggfunc="sum").sum(axis=1).round(2).to_dict())
netrev = lambda q, p, d: q * p * (1 - d / 100)
print("LAMBDA NETREV(45,750,5)          ->", netrev(45, 750, 5))
print("TOCOL/UNIQUE reps (non-blank)    ->", sorted(S.sales_rep.dropna().unique().tolist()))
print("HSTACK months x revenue rows     ->", len(m))
print("Wholesale customers TEXTJOIN     ->", ", ".join(C[C.segment == "Wholesale"].customer_name))
print("TEXTBEFORE/TEXTAFTER code parts  ->", "02.01.2025|SO10001|C0002|P108x10@290-0%|DEL".split("|"))
print("GETPIVOTDATA Wholesale Q4        ->", round(ok[(ok.segment=="Wholesale")&(ok.quarter=="Q4")].net_revenue.sum(),2))
print("GETPIVOTDATA Retail total        ->", round(ok[ok.segment=="Retail"].net_revenue.sum(),2))
print("pivot % of row Wholesale Q4      ->", round(ok[(ok.segment=="Wholesale")&(ok.quarter=="Q4")].net_revenue.sum()/ok[ok.segment=="Wholesale"].net_revenue.sum()*100,1))
print("pivot rank rep Q4                ->", ok[ok.quarter=="Q4"].groupby("sales_rep").net_revenue.sum().rank(ascending=False).to_dict())
bands = pd.cut(ok.net_revenue, [0, 10000, 20000, 30000, 40000, 60000], right=False)
print("pivot group line value bands     ->", ok.groupby(bands, observed=False).net_revenue.agg(["count","sum"]).round(2).to_dict())
print("calc field avg realised price    ->", {k: round(v, 2) for k, v in (ok.groupby("product_name").net_revenue.sum()/ok.groupby("product_name").quantity.sum()).items()})
