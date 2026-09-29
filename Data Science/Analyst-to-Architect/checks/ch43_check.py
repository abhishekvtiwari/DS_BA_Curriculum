"""Analyst to Architect · Chapter 43 · number check.

Runs the chapter's Python cells in order (like a notebook, from companion/ch43/), then recomputes
the numbers quoted in the prose and writes checks/ch43_results.json for figures/make_figs43.py.
Run from anywhere: OMP_NUM_THREADS=1 python3 checks/ch43_check.py   (about 30 seconds).
Riverstone Supplies is fictional."""
import contextlib, io, json, math, os, pathlib, re

HERE = pathlib.Path(__file__).resolve().parent
BOOK = HERE.parent
CHAPTER = BOOK / "manuscript" / "ch43-a-first-look-at-deep-learning.md"
fails = 0


def ok(label, got, want):
    global fails
    good = got == want
    fails += not good
    print(("OK  " if good else "BAD ") + f"{label}: {got} (text: {want})")


# Run every python cell of the chapter body (not the answers) in one namespace.
md = CHAPTER.read_text(encoding="utf-8")
body, answers = md.split("\n## Answers\n")
os.chdir(BOOK / "companion" / "ch43")
import torch

torch.set_num_threads(1)
ns = {"__name__": "__main__"}
with contextlib.redirect_stdout(io.StringIO()):
    for cell in re.findall(r"^```python\n(.*?)^```$", body, re.S | re.M):
        exec(cell, ns)
g = ns.__getitem__
import numpy as np
import torch.nn as nn
from sklearn.metrics import roc_auc_score

# 43.1
ok("neuron z", round(0.05 * 16 + 0.9 * 5.03 - 1.2, 3), 4.127)
ok("0.8 + 4.527", round(0.05 * 16 + 0.9 * 5.03, 3), 5.327)
ok("0.25**10 about one millionth", f"{0.25 ** 10:.1e}", "9.5e-07")
# 43.2
ok("ln 2", round(math.log(2), 4), 0.6931)
ok("single neuron loss", round(g("loss").item(), 4), 0.6931)
ok("two-layer loss", round(g("loss2").item(), 5), 0.00097)
ok("ReLU net loss", round(g("relu_loss").item(), 4), 0.3467)
before, grad = -0.06509867310523987, 0.03870430588722229
ok("one SGD step by hand", round(before - 0.5 * grad, 6), round(-0.08445082604885101, 6))
# 43.3 / 43.4
ok("a2", round(g("a2_hand"), 4), 0.5359)
ok("loss -ln a2", round(-math.log(g("a2_hand")), 4), 0.6238)
ok("dz2", round(g("a2_hand") - 1, 4), -0.4641)
ok("dW2", [round(v, 4) for v in g("dW2")], [-0.1352, -0.1561])
ok("dz1", [round(v, 4) for v in g("dz1")], [-0.2124, 0.247])
ok("autograd = hand", torch.allclose(g("W2g").grad[0].double(), torch.tensor(g("dW2"), dtype=torch.float64), atol=1e-6), True)
ok("64-bit nudge agrees to 7 decimals", abs(g("slope_64") - g("dW2")[0]) < 1e-7, True)
ok("loss difference in 5th decimal", f"{2e-4 * 0.1352:.1e}", "2.7e-05")
# 43.5
ok("25 features = 13 one-hot + 11 + 1", 3 + 3 + 3 + 4 + 11 + 1, 25)
ok("network params", 25 * 16 + 16 + 16 * 8 + 8 + 8 + 1, 561)
ok("561 / 26 about twenty", round(561 / 26), 22)
ok("network valid AUC", round(roc_auc_score(g("y_valid"), g("final_pred")), 3), 0.773)
ok("logit valid AUC", round(roc_auc_score(g("y_valid"), g("logit_pred")), 3), 0.764)
ok("boosting valid AUC", round(roc_auc_score(g("y_valid"), g("boosting_pred")), 3), 0.786)
ok("network test AUC", round(roc_auc_score(g("y_test"), g("network_test")), 3), 0.818)
ok("churn rate", round(g("accounts")["churned_2025"].mean(), 3), 0.097)
ok("no-churn accuracy", round(1 - g("accounts")["churned_2025"].mean(), 3), 0.903)
ok("valid churners", int(g("y_valid").sum()), 97)
# 43.6
fm = g("feature_map")
ok("feature map max", round(float(fm.max()), 1), 1.3)
ok("feature map min", round(float(fm.min()), 1), -2.0)
ok("argmax of max is bottom (row 4)", int(np.unravel_index(fm.argmax(), fm.shape)[0]), 4)
ok("CNN params", 80 + 1168 + 2080 + 165, 3493)
ok("conv params", (1 * 8 * 9 + 8, 8 * 16 * 9 + 16, 64 * 32 + 32, 32 * 5 + 5), (80, 1168, 2080, 165))
ok("base accuracy", round(g("base_accuracy"), 3), 0.987)
with torch.no_grad():
    f = nn.functional.normalize(g("base_model").features(g("Xb_test_t")), dim=1)
sim, y = f @ f.T, g("yb_test_t")
same, eye = y[:, None] == y[None, :], torch.eye(len(y), dtype=torch.bool)
ok("same-digit features more similar", bool(sim[same & ~eye].mean() > sim[~same].mean()), True)
# 43.7
sweep = g("sweep")
means = {n: (np.mean(t), np.mean(s)) for n, (t, s) in sweep.items()}
ok("scratch ahead at every size", all(s > t for t, s in means.values()), True)
gaps = [round((s - t) * 100, 1) for t, s in means.values()]
ok("gaps 2 to 3 points", all(2.0 <= gp <= 3.5 for gp in gaps), True)
ok("trainable 2,245", 2080 + 165, 2245)
ok("frozen 1,248", 80 + 1168, 1248)

json.dump(
    {
        "xor_grid": [[float(v) for v in row] for row in
                     g("two_layer")(torch.tensor([[a / 40, b / 40] for b in range(-8, 49) for a in range(-8, 49)],
                                                 dtype=torch.float32)).detach().numpy().reshape(57, 57)],
        "network": {"z1": [round(v, 4) for v in g("z1").tolist()], "a1": [round(v, 4) for v in g("a1").tolist()],
                    "z2": round(g("z2").item(), 4), "a2": round(g("a2").item(), 4)},
        "image": np.round(g("images")[0], 2).tolist(),
        "feature_map": np.round(fm, 1).tolist(),
    },
    open(HERE / "ch43_results.json", "w"),
)
print("All checks passed." if not fails else f"FAILED: {fails}")
raise SystemExit(1 if fails else 0)
