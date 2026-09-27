"""Compare a cleaned Q4 2025 order-line table with the truth (companion/ch14/clean_truth_orders_q4_2025.csv).
Usage: python3 checks/ch14_compare_clean.py path/to/clean.csv path/to/issues.csv"""
import sys, pandas as pd
T = pd.read_csv("companion/ch14/clean_truth_orders_q4_2025.csv", dtype={"customer_code": str}, keep_default_na=False)
X = pd.read_csv(sys.argv[1], dtype={"customer_code": str}, keep_default_na=False)
Q = pd.read_csv(sys.argv[2])
quar = set(Q[Q.action == "quarantined"].order_item_id)
print("rows clean/truth:", len(X), len(T), "| issues:", Q.issue.value_counts().to_dict())
m = T.merge(X, on="order_item_id", suffixes=("_t", "_x"), how="outer", indicator=True)
print("row match:", m._merge.value_counts().to_dict())
m = m[m._merge == "both"]
def eq(a, b): return (pd.to_numeric(m[a], errors="coerce").round(4) == pd.to_numeric(m[b], errors="coerce").round(4))
checks = {
 "order_id": eq("order_id_t", "order_id_x"),
 "order_date": m.order_date_t.str[:10] == m.order_date_x.astype(str).str[:10],
 "customer_code": m.customer_code_t == m.customer_code_x,
 "product_id": eq("product_id_t", "product_id_x"),
 "quantity": eq("quantity_t", "quantity_x") | m.order_item_id.isin(quar),
 "unit_price": eq("unit_price_t", "unit_price_x"),
 "discount_pct": eq("discount_pct_t", "discount_pct_x"),
 "status": m.status_t == m.status_x,
 "sales_rep": m.sales_rep_t.fillna("") == m.sales_rep_x.fillna(""),
 "branch": m.branch_t == m.branch_x,
}
ok = True
for k, v in checks.items():
    bad = int((~v).sum()); ok &= bad == 0; print(f"{k:14} mismatches: {bad}")
v = X[(X.status == "Cancelled") == False]
v = X[(X.status != "Cancelled") & (~X.order_item_id.isin(quar))]
rev = (pd.to_numeric(v.quantity) * pd.to_numeric(v.unit_price) * (1 - pd.to_numeric(v.discount_pct) / 100)).sum()
tq = T[(T.status != "Cancelled") & (T.order_item_id.isin(quar))]
print("clean non-cancelled revenue excl. quarantine:", round(rev, 2))
print("truth non-cancelled revenue:", round(T[T.status != "Cancelled"].net_revenue.sum(), 2),
      "| truth value of quarantined non-cancelled lines:", round(tq.net_revenue.sum(), 2),
      "| difference explained:", round(T[T.status != "Cancelled"].net_revenue.sum() - tq.net_revenue.sum() - rev, 2) == 0)
print("ALL FIELDS MATCH" if ok else "MISMATCHES FOUND")
