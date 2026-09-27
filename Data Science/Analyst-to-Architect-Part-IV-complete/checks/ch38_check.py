"""Analyst to Architect · Chapter 38 · number check.
Recomputes every number quoted in Chapter 38's prose and writes checks/ch38_results.json for the figures.
Run from checks/: python3 ch38_check.py   (about 1 minute on one CPU core).
Riverstone Supplies is fictional; every name and number is invented."""
import json, pathlib, warnings
import numpy as np, pandas as pd
from scipy.cluster.hierarchy import fcluster, linkage
from sklearn.cluster import DBSCAN, KMeans
from sklearn.decomposition import PCA
from sklearn.ensemble import IsolationForest
from sklearn.manifold import TSNE
from sklearn.metrics import adjusted_rand_score, roc_auc_score, silhouette_score
from sklearn.preprocessing import StandardScaler
import umap
warnings.filterwarnings("ignore")
HERE = pathlib.Path(__file__).resolve().parent
COMP = HERE.parent / "companion"
fails = 0
def ok(label, got, want):
    global fails
    good = got == want
    fails += not good
    print(("OK  " if good else "BAD ") + f"{label}: {got} (text: {want})")

acc = pd.read_csv(COMP / "accounts" / "accounts.csv")
acc["log_revenue"] = np.log(acc["revenue_2024"])
acc["late_payment_days"] = acc["late_payment_days"].fillna(acc["late_payment_days"].median())
FEATURES = ["log_revenue", "orders_2024", "categories_bought", "avg_discount_pct",
            "late_payment_days", "days_since_last_order", "tenure_months"]
X = StandardScaler().fit_transform(acc[FEATURES])

# hand k-means example
small = np.array([[1.0, 2.0], [1.5, 1.8], [5.0, 8.0], [8.0, 8.0], [1.0, 0.6], [9.0, 11.0]])
c1 = small[[0, 1, 4]].mean(axis=0); c2 = small[[2, 3, 5]].mean(axis=0)
ok("hand centroids", (list(c1.round(2)), list(c2.round(2))), ([1.17, 1.47], [7.33, 9.0]))
ok("C distance to c1 start", round(float(np.hypot(5 - 1, 8 - 2)), 2), 7.21)
ok("C distance to c2 start", round(float(np.hypot(5 - 9, 8 - 11)), 2), 5.0)
inertia1 = float(((small[[0, 1, 4]] - c1) ** 2).sum()); inertia2 = float(((small[[2, 3, 5]] - c2) ** 2).sum())
ok("cluster 1 inertia", round(inertia1, 3), 1.313); ok("cluster 2 inertia", round(inertia2, 2), 14.67)
ok("total inertia", round(inertia1 + inertia2, 2), 15.98)

res = {"k": [], }
for k in range(2, 9):
    km = KMeans(n_clusters=k, n_init=10, random_state=38).fit(X)
    res["k"].append((k, float(km.inertia_), float(silhouette_score(X, km.labels_, sample_size=2000, random_state=38))))
ok("k=2 silhouette", round(res["k"][0][2], 3), 0.277); ok("k=4 silhouette", round(res["k"][2][2], 3), 0.203)
ok("k=2 inertia", round(res["k"][0][1]), 25503); ok("k=8 inertia", round(res["k"][-1][1]), 14175)

base = KMeans(n_clusters=4, n_init=10, random_state=38).fit_predict(X)
acc["cluster"] = base
sizes = np.bincount(base)
ok("cluster sizes", sizes.tolist(), [1088, 944, 2398, 570])
med = acc.groupby("cluster")["revenue_2024"].median().round(0).astype(int).tolist()
ok("median revenue", med, [282400, 1083800, 145600, 73450])
churn = acc.groupby("cluster")["churned_2025"].mean().round(3).tolist()
ok("churn by cluster", churn, [0.026, 0.035, 0.08, 0.405])
share = (acc.groupby("cluster")["revenue_2024"].sum() / acc["revenue_2024"].sum() * 100).round(1).tolist()
ok("revenue share", share, [15.8, 62.0, 19.9, 2.3])
ok("key accounts share of base", round(sizes[1] / len(acc) * 100), 19)
ok("wholesale share of cluster 1", round((acc[acc.cluster == 1].segment == "Wholesale").mean() * 100), 69)
scored = acc["cluster"].map(acc.groupby("cluster")["churned_2025"].mean())
ok("cluster-only AUC", round(roc_auc_score(acc["churned_2025"], scored), 3), 0.759)

sample = np.random.default_rng(38).choice(len(X), size=800, replace=False)
tree = linkage(X[sample], method="ward")
lab4 = fcluster(tree, t=4, criterion="maxclust")
ok("hierarchical sizes", np.bincount(lab4)[1:].tolist(), [147, 287, 50, 316])
ok("hierarchical ARI", round(adjusted_rand_score(base[sample], lab4), 3), 0.413)
noise = {eps: int((DBSCAN(eps=eps, min_samples=10).fit_predict(X) == -1).sum()) for eps in [0.5, 1.2]}
ok("DBSCAN noise", noise, {0.5: 4678, 1.2: 313})

pca = PCA().fit(X)
ok("PCA two components", f"{pca.explained_variance_ratio_[:2].sum():.1%}", "54.1%")
forest = IsolationForest(contamination=0.02, random_state=38).fit(X)
acc["outlier_score"] = forest.decision_function(X)
ok("outlier churn", f"{acc.nsmallest(100, 'outlier_score')['churned_2025'].mean():.1%}", "21.0%")
ok("overall churn", f"{acc['churned_2025'].mean():.1%}", "9.7%")

lines = pd.read_csv(COMP / "baskets" / "order_lines.csv").merge(
    pd.read_csv(COMP / "baskets" / "products.csv")[["product_id", "product_name"]], on="product_id")
baskets = lines.groupby("order_id")["product_name"].apply(set)
ok("orders", len(baskets), 33931); ok("order lines", len(lines), 92359)
crate = baskets.apply(lambda s: "Storage Crate 50L" in s); lid = baskets.apply(lambda s: "Crate Lid (50L)" in s)
ok("crate orders", int(crate.sum()), 4170); ok("lid orders", int(lid.sum()), 6500); ok("both", int((crate & lid).sum()), 2785)
ok("support crate", round(crate.mean(), 4), 0.1229); ok("support lid", round(lid.mean(), 4), 0.1916)
conf = (crate & lid).mean() / crate.mean()
ok("confidence", round(conf, 3), 0.668); ok("lift", round(conf / lid.mean(), 2), 3.49)
drum = set(lines.loc[lines.product_name == "Drum 60L", "order_id"]); tap = set(lines.loc[lines.product_name == "Drum Tap Fitting", "order_id"])
ok("drum orders", len(drum), 3412); ok("drum without tap", len(drum - tap), 1001)
ok("share without tap", f"{len(drum - tap) / len(drum):.1%}", "29.3%")

plot_rows = np.random.default_rng(38).choice(len(X), size=1500, replace=False)
res["coords"] = {"pca": pca.transform(X)[plot_rows][:, :2].tolist(),
                 "tsne": TSNE(n_components=2, perplexity=30, random_state=38).fit_transform(X[plot_rows]).tolist(),
                 "umap": umap.UMAP(n_components=2, random_state=38).fit_transform(X[plot_rows]).tolist(),
                 "labels": base[plot_rows].tolist()}
res["profile"] = acc.groupby("cluster").agg(size=("account_id", "size"), revenue=("revenue_2024", "median"),
    orders=("orders_2024", "median"), categories=("categories_bought", "mean"),
    recency=("days_since_last_order", "median"), churn=("churned_2025", "mean"),
    revenue_share=("revenue_2024", lambda s: s.sum() / acc["revenue_2024"].sum())).round(3).to_dict("index")
res["linkage"] = tree.tolist()
(HERE / "ch38_results.json").write_text(json.dumps(res))
print("All checks passed." if not fails else f"FAILED: {fails}")
raise SystemExit(1 if fails else 0)
