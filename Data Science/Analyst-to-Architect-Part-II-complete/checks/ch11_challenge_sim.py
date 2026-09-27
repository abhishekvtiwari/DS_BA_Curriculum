"""Chapter 11 championship-style challenge: reference simulation (the answer key).
Run from the book root after companion/ch11/build_ch11_files.py:  python3 checks/ch11_challenge_sim.py"""
import pandas as pd, datetime as dt, itertools
S = pd.read_excel("companion/ch11/ch11_practice.xlsx", sheet_name="Sales", dtype={"customer_code": str})
PRODUCT, OPENING = 101, 300
days = pd.date_range("2025-01-01", "2025-12-31", freq="D")
dem = S[(S.product_id == PRODUCT) & (S.status != "Cancelled")].groupby("order_date").quantity.sum()
demand = [int(dem.get(d, 0)) for d in days]

def simulate(rop, q, lead, reorder=True):
    receipts = [0] * (len(days) + 60); closing = []; pos = []; stock = OPENING
    for i, d in enumerate(days):
        if reorder and d.weekday() == 0 and i > 0 and closing[i-1] <= rop:
            receipts[i + lead] += q; pos.append(d)
        stock = stock + receipts[i] - demand[i]
        closing.append(stock)
    return closing, pos

def cost(closing, pos, hold=1, short=20, order=2000):
    return sum(c*hold for c in closing if c > 0) + sum(-c*short for c in closing if c < 0) + order*len(pos)

if __name__ == "__main__":
    lines = S[S.status != "Cancelled"]
    print("L1 total units (valid):", int(lines.quantity.sum()), " all:", int(S.quantity.sum()))
    u = lines.groupby("product_name").quantity.sum().sort_values(ascending=False); print("L1 units by product:", u.to_dict())
    cu = lines[lines.product_id==PRODUCT].groupby("customer_name").quantity.sum().sort_values(ascending=False); print("L1 top customers for product:", cu.head(3).to_dict())
    print("demand 101 total, active days:", sum(demand), sum(1 for x in demand if x))
    c, p = simulate(0, 0, 7, reorder=False)
    neg = next(i for i, x in enumerate(c) if x < 0); print("L2 first negative:", days[neg].date(), c[neg], " year-end closing:", c[-1])
    c, p = simulate(100, 250, 7)
    print("L3 PO dates:", [d.date().isoformat() for d in p])
    lo = min(c); print("L3 POs:", len(p), " first PO:", p[0].date(), " lowest:", lo, days[c.index(lo)].date(), " year-end:", c[-1])
    print("L4 negative days (100/250):", sum(1 for x in c if x < 0))
    for r in range(0, 1001, 50):
        cc, pp = simulate(r, 250, 7)
        if all(x >= 0 for x in cc): print("L4 smallest ROP (Q=250) with no negative day:", r, "POs:", len(pp), "lowest:", min(cc)); break
    for q in range(50, 2001, 50):
        cc, pp = simulate(100, q, 7)
        if all(x >= 0 for x in cc): print("L4 smallest Q (ROP=100) with no negative day:", q, "POs:", len(pp)); break
    else: print("L4 no Q up to 2000 removes negatives at ROP=100")
    print("L5 cost at 100/250:", cost(c, p), " holding/short/order parts:", sum(x for x in c if x>0), sum(-x*20 for x in c if x<0), 2000*len(p))
    best = min(((cost(*simulate(r, q, 7)), r, q) for r in range(0, 401, 50) for q in range(50, 801, 50)))
    print("L5 best (cost, rop, q):", best)
    cc, pp = simulate(best[1], best[2], 7); print("   best POs, neg days, lowest:", len(pp), sum(1 for x in cc if x < 0), min(cc))
    bestb = min(((cost(*simulate(r, q, 14)), r, q) for r in range(0, 401, 50) for q in range(50, 801, 50)))
    print("Bonus best lead 14:", bestb)
    # top few for sensitivity
    allc = sorted(((cost(*simulate(r, q, 7)), r, q) for r in range(0, 401, 50) for q in range(50, 801, 50)))[:5]; print("top5:", allc)
