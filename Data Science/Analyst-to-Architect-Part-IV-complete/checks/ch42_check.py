"""Analyst to Architect · Chapter 42 · number check.
Recomputes the numbers quoted in Chapter 42's prose and writes checks/ch42_results.json for the figures.
Run from checks/: python3 ch42_check.py   (about 15 seconds). Riverstone Supplies is fictional."""
import json, pathlib, sys, warnings
import numpy as np, pandas as pd
from scipy.sparse import csr_matrix
from sklearn.decomposition import TruncatedSVD
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
warnings.filterwarnings("ignore")
HERE = pathlib.Path(__file__).resolve().parent
COMP = HERE.parent / "companion"
sys.path.insert(0, str(COMP / "ch42"))
from products_text import load_products
fails = 0
def ok(label, got, want):
    global fails
    good = got == want; fails += not good
    print(("OK  " if good else "BAD ") + f"{label}: {got} (text: {want})")

lines = pd.read_csv(COMP / "baskets" / "order_lines.csv", parse_dates=["order_date"])
products = load_products()
accounts = pd.read_csv(COMP / "accounts" / "accounts.csv")
lines = lines.merge(products[["product_id", "product_name", "category"]], on="product_id")
lines = lines.merge(accounts[["account_id", "segment"]], on="account_id")
ok("lines", len(lines), 92359); ok("orders", lines.order_id.nunique(), 33931); ok("accounts", lines.account_id.nunique(), 4516)
interactions = lines.groupby(["account_id", "product_id"])["quantity"].sum().reset_index()
matrix = interactions.pivot(index="account_id", columns="product_id", values="quantity").fillna(0)
items = matrix.columns.tolist(); X = matrix.to_numpy()
ok("density", round((matrix > 0).mean().mean(), 3), 0.384)
pop_share = ((matrix > 0).sum(0) / matrix.shape[0]).sort_values(ascending=False)
ok("top product share", round(pop_share.iloc[0], 3), 0.649)

rng = np.random.default_rng(42)
n_owned = (X > 0).sum(1); eligible = np.where(n_owned >= 2)[0]
held_out = np.full(X.shape[0], -1)
for i in eligible:
    owned = np.where(X[i] > 0)[0]; held_out[i] = rng.choice(owned)
X_train = X.copy(); X_train[eligible, held_out[eligible]] = 0
ok("eligible", len(eligible), 4309)

def evaluate(score_fn, k=5):
    hits = 0; ndcg = 0.0
    for i in eligible:
        scores = score_fn(i).copy(); scores[X_train[i] > 0] = -np.inf
        topk = np.argsort(-scores)[:k]
        if held_out[i] in topk:
            hits += 1; rank = int(np.where(topk == held_out[i])[0][0]); ndcg += 1 / np.log2(rank + 2)
    return hits / len(eligible), ndcg / len(eligible)

pop_counts = (X_train > 0).sum(0).astype(float)
p_pop, n_pop = evaluate(lambda i: pop_counts)
ok("pop precision/ndcg", (round(p_pop, 3), round(n_pop, 3)), (0.614, 0.428))

item_sim = cosine_similarity(X_train.T); np.fill_diagonal(item_sim, 0)
def cf_score(i): return X_train[i] @ item_sim
p_cf, n_cf = evaluate(cf_score)
ok("cf precision/ndcg", (round(p_cf, 3), round(n_cf, 3)), (0.676, 0.510))

svd_results = []
for f in [4, 8, 12]:
    svd = TruncatedSVD(n_components=f, random_state=42).fit(X_train)
    recon = svd.transform(X_train) @ svd.components_
    p, n = evaluate(lambda i, r=recon: r[i]); svd_results.append((f, p, n))
ok("svd 4/12 precision", (round(svd_results[0][1], 3), round(svd_results[2][1], 3)), (0.662, 0.490))

import implicit
conf = csr_matrix(np.log1p(X_train))
als_results = []
for f in [8, 16]:
    m = implicit.als.AlternatingLeastSquares(factors=f, regularization=0.1, iterations=20, random_state=42)
    m.fit(conf)
    p, n = evaluate(lambda i, mm=m: mm.user_factors[i] @ mm.item_factors.T); als_results.append((f, p, n))
ok("als 8/16 precision", (round(als_results[0][1], 3), round(als_results[1][1], 3)), (0.698, 0.466))

desc = products.set_index("product_id").loc[items, "description"]
tfidf = TfidfVectorizer(stop_words="english")
content_sim = cosine_similarity(tfidf.fit_transform(desc))
def content_score(i): return X_train[i] @ content_sim
p_content, n_content = evaluate(content_score)
ok("content precision/ndcg", (round(p_content, 3), round(n_content, 3)), (0.540, 0.367))

def normalize(s):
    m = np.abs(s).max(); return s / m if m > 0 else s
def hybrid_score(i): return 0.5 * normalize(cf_score(i)) + 0.5 * normalize(content_score(i))
p_hy, n_hy = evaluate(hybrid_score)
ok("hybrid precision/ndcg", (round(p_hy, 3), round(n_hy, 3)), (0.654, 0.460))

names = products.set_index("product_id")["product_name"]
item_sim_full = cosine_similarity(X.T); np.fill_diagonal(item_sim_full, 0)
top_similar = pd.DataFrame(item_sim_full, index=items, columns=items)["P01"].sort_values(ascending=False).head(4)
ok("P01 top similar", list(top_similar.index), ["P03", "P04", "P16", "P18"])

json.dump({
    "summary": {"popularity": (p_pop, n_pop), "item_cf": (p_cf, n_cf), "svd": svd_results, "als": als_results,
               "content": (p_content, n_content), "hybrid": (p_hy, n_hy)},
    "svd_results": svd_results, "als_results": als_results,
    "top_similar_P01": {k: float(v) for k, v in top_similar.items()},
    "segment_top": {seg: (matrix[matrix.index.isin(accounts.loc[accounts.segment == seg, "account_id"])] > 0)
                   .mean().sort_values(ascending=False).head(3).to_dict() for seg in ["Retail", "Hospitality", "Wholesale"]},
    "names": names.to_dict(),
}, open(HERE / "ch42_results.json", "w"))
print("All checks passed." if not fails else f"FAILED: {fails}")
raise SystemExit(1 if fails else 0)
