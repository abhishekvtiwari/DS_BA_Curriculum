"""
Analyst to Architect — Chapter 19: Spreadsheet Automation
build_ch19_files.py — builds the twelve branch workbooks the chapter's macro consolidates,
and writes expected_results.md with every number the finished macro must produce.

Run from this folder:  python3 build_ch19_files.py      (needs pandas, openpyxl)
Reads ../ch14/clean_truth_orders_q4_2025.csv (the clean Q4 2025 order lines, from the full dataset).
Creates:
  branch_files/Riverstone_<Branch>_2025-10.xlsx … one file per branch per month (4 branches x 3 months)
  branch_files/_notes.txt               a non-Excel file, so the macro has to filter by extension
  expected_results.md                   what the consolidation must produce, to check your macro
  enquiries_sample.csv                  sample Google Form responses for the Apps Script project
  ch19_practice.xlsx                    the practice workbook for sections 19.2-19.5: a Master sheet
                                        (a copy of Kolkata, December 2025) and an empty Scratch sheet
Riverstone Supplies is fictional; every name and number is invented.
"""
import pathlib
import pandas as pd

HERE = pathlib.Path(__file__).resolve().parent
OUT = HERE / "branch_files"; OUT.mkdir(exist_ok=True)
truth = pd.read_csv(HERE.parent / "ch14" / "clean_truth_orders_q4_2025.csv", dtype={"customer_code": str},
                    parse_dates=["order_date"])
truth["month"] = truth.order_date.dt.strftime("%Y-%m")
cols = ["order_item_id", "order_id", "order_date", "customer_code", "product_id", "quantity",
        "unit_price", "discount_pct", "status", "sales_rep", "net_revenue"]

def lakh(v: float) -> str:
    """Indian digit grouping, as used in the book: 423872808.0 -> '42,38,72,808.00'."""
    i, _, d = f"{v:.2f}".partition(".")
    if len(i) > 3:
        head, tail = i[:-3], i[-3:]
        i = ",".join([head[max(0, k - 2):k] for k in range(len(head), 0, -2)][::-1]) + "," + tail
    return f"₹{i}.{d}"


rows = []
for (branch, month), part in truth.groupby(["branch", "month"]):
    name = f"Riverstone_{branch.replace(' ', '_')}_{month}.xlsx"
    part = part.sort_values(["order_date", "order_id", "order_item_id"])[cols]
    with pd.ExcelWriter(OUT / name, engine="openpyxl") as writer:
        part.to_excel(writer, sheet_name="Sales", index=False)
    ok = part[part.status != "Cancelled"]
    rows.append({"file": name, "branch": branch, "month": month, "rows": len(part),
                 "non_cancelled": len(ok), "net_revenue": round(ok.net_revenue.sum(), 2)})
(OUT / "_notes.txt").write_text("Branch sales extracts, Q4 2025. One row per order line.\n", encoding="utf-8")

files = pd.DataFrame(rows).sort_values(["branch", "month"])
files["net_revenue"] = files["net_revenue"].map(lakh)
ok_all = truth[truth.status != "Cancelled"]
by_branch = ok_all.groupby("branch").net_revenue.agg(["count", "sum"])
by_branch["sum"] = by_branch["sum"].map(lakh)
by_month = ok_all.groupby("month").net_revenue.agg(["count", "sum"])
by_month["sum"] = by_month["sum"].map(lakh)
by_status = truth.status.value_counts()

lines = ["# Chapter 19 — what the consolidation must produce", "",
         "Built by `build_ch19_files.py` from Riverstone's Q4 2025 order lines. Rupee amounts use Indian grouping (₹42,38,72,808.00).",
         "Riverstone Supplies is fictional; every name and number is invented.", "",
         "## The twelve files", "", files.to_markdown(index=False), "",
         "## After consolidating all twelve", "",
         f"- Data rows: **{len(truth):,}** (plus one header row per file, which the macro must not copy)",
         f"- Non-cancelled rows: **{len(ok_all):,}**",
         f"- Net revenue, non-cancelled: **{lakh(ok_all.net_revenue.sum())}**",
         f"- Net revenue, all rows including cancelled: **{lakh(truth.net_revenue.sum())}**",
         f"- Distinct orders: **{truth.order_id.nunique():,}**  ·  distinct customers: **{truth.customer_code.nunique():,}**",
         "", "### By branch (non-cancelled)", "", by_branch.rename(columns={"count": "rows", "sum": "net_revenue"}).to_markdown(), "",
         "### By month (non-cancelled)", "", by_month.rename(columns={"count": "rows", "sum": "net_revenue"}).to_markdown(), "",
         "### Rows by status (all rows)", "", by_status.to_frame("rows").to_markdown(), ""]
(HERE / "expected_results.md").write_text("\n".join(lines) + "\n", encoding="utf-8")

enq = pd.DataFrame({
    "Timestamp": ["2026-01-02 14:40:10", "2026-01-03 11:05:37", "2026-01-05 08:20:02",
                  "2026-01-05 09:14:22", "2026-01-05 10:02:47", "2026-01-05 11:31:05"],
    "Email address": ["stores@kaveritraders.example.com", "admin@sunriseschool.example.com",
                      "purchase@deccanfoods.example.com", "orders@metromart.example.com",
                      "purchase@greenleafhotels.example.com", "buy@sharmahardware.example.com"],
    "Company": ["Kaveri Traders", "Sunrise School", "Deccan Foods", "Metro Mart", "Green Leaf Hotels", "Sharma Hardware"],
    "City": ["Mysuru", "Kolkata", "Hyderabad", "Mumbai", "Pune", "Nagpur"],
    "Product": ["Industrial Crate", "Storage Box 25L", "Storage Box 25L", "Storage Box 25L", "Lunch Box Set", "Industrial Crate"],
    "Quantity": [30, 60, 40, 120, 300, 45],
    "Needed by": ["2026-01-16", "2026-01-12", "2026-01-19", "2026-01-20", "2026-01-15", "2026-02-02"],
    "Notes": ["Warehouse racking", "Classroom storage", "", "Repeat order", "New outlet opening", "Please quote freight"]})
enq.to_csv(HERE / "enquiries_sample.csv", index=False)
# The practice workbook for sections 19.2-19.5: Master holds one branch file, Scratch is empty.
practice = truth[(truth.branch == "Kolkata") & (truth.month == "2025-12")]
practice = practice.sort_values(["order_date", "order_id", "order_item_id"])[cols]
with pd.ExcelWriter(HERE / "ch19_practice.xlsx", engine="openpyxl") as writer:
    practice.to_excel(writer, sheet_name="Master", index=False)
    pd.DataFrame().to_excel(writer, sheet_name="Scratch", index=False)

print(f"{len(files)} workbooks; {len(truth):,} rows; net revenue {lakh(ok_all.net_revenue.sum())}")
