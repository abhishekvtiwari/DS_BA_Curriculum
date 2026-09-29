#!/usr/bin/env python3
"""ch53_check.py - checks the numbers Chapter 53's prose quotes, and writes the data its figures draw.

Run from the book folder, after companion/ch53/generate_defect_images.py has built defect_data/:
    OMP_NUM_THREADS=1 python3 checks/ch53_check.py
It runs every Python cell of the chapter in order (as tools/verify_python.py does, from companion/ch53),
then checks each number the text states in words against the variables the cells produced, and writes
checks/ch53_results.json for figures/make_figs53.py. About four minutes on one CPU thread.
"""
import contextlib, io, json, math, os, pathlib, re

import numpy as np
import torch

torch.set_num_threads(1)           # the book's PyTorch outputs were produced on one CPU thread

BOOK = pathlib.Path(__file__).resolve().parents[1]
CHAPTER = BOOK / "manuscript" / "ch53-deep-learning-in-depth.md"
OUT = BOOK / "checks" / "ch53_results.json"

md = CHAPTER.read_text(encoding="utf-8")
os.chdir(BOOK / "companion" / "ch53")
ns = {"__name__": "__main__"}
cells, snapshots = [], []          # each cell's code, and the names it left behind (later cells reuse some names)
skip = False
for m in re.finditer(r'<!-- run: (none) -->|^```(\w*)\n(.*?)^```$', md, re.S | re.M):
    if m.group(1):
        skip = True
        continue
    if m.group(2) == "python":
        if skip:
            skip = False
            continue
        with contextlib.redirect_stdout(io.StringIO()):
            exec(compile(m.group(3), "<chapter cell>", "exec"), ns)
        cells.append(m.group(3))
        snapshots.append(dict(ns))
    elif skip:
        skip = False

from sklearn.metrics import confusion_matrix, precision_recall_curve  # noqa: E402

ok = 0


def check(label, got, want, tol=0.0):
    global ok
    if isinstance(want, (int, float)) and not isinstance(want, bool):
        assert abs(got - want) <= tol, f"{label}: {got} != {want}"
    else:
        assert got == want, f"{label}: {got} != {want}"
    ok += 1


def at(code):
    """The names as they stood right after the first cell whose code contains `code`."""
    return next(snap for cell, snap in zip(cells, snapshots) if code in cell)


g = ns
# 53.0 and 53.1
check("images", g["images"].shape, (6000, 32, 32))
check("defective", int(g["labels"].sum()), 476)
check("neuron weighted sum", round(at("negative_sum =")["weighted_sum"], 2), 0.10)
check("negative case", round(at("negative_sum =")["negative_sum"], 2), -0.5)
check("float64 repr", repr(np.array([2.0, 3.0]) @ np.array([0.6, -0.4]) + 0.1), "np.float64(0.0999999999999999)")
check("parameters 1024-64-1", 1024 * 64 + 64 + 64 + 1, 65665)
# 53.2
check("neuron 1 sum", round(1.0 * -0.3 + 2.0 * 0.2 + 0.1, 3), 0.2)
check("dloss/dz2", round(at("dloss_dz2 = 2")["dloss_dz2"], 3), 0.84)
check("chain rule dW2[0]", round(0.84 * 2.1, 3), 1.764)
check("dW2[0]", round(float(at("dloss_dz2 = 2")["dW2"][0]), 3), 1.764)
check("adam m", round(0.1 * -6, 3), -0.6)
check("adam v", round(0.001 * 36, 3), 0.036)
check("adam step", round(float(at("adam_step =")["adam_step"]), 3), 0.1)
# 53.3
check("He std", round(math.sqrt(2 / 1024), 4), 0.0442)
check("batch norm std", round(float(np.array([2.0, 4, 6, 8]).std()), 3), 2.236)
# 53.5
check("conv stride 2", (32 - 3) // 2 + 1, 15)
check("pooling", at("m.reshape(2, 2, 2, 2)")["m"].reshape(2, 2, 2, 2).max(axis=(1, 3)).tolist(), [[4, 2], [2, 5]])
# 53.6
s6 = at("best_cost, best_threshold = min(results)")
ytr, yte, cvp, p = s6["ytr"], s6["yte"], s6["cv_probabilities"], s6["probabilities"]
check("training defects", int(ytr.sum()), 357)
rows = []
for t in (0.5, 0.3, 0.1, 0.05, 0.02, 0.01, 0.005, 0.002):
    tn, fp, fn, tp = confusion_matrix(ytr, cvp > t).ravel()
    rows.append({"threshold": t, "caught": int(tp), "missed": int(fn), "false_alarms": int(fp),
                 "accuracy": float((tp + tn) / len(ytr)), "cost": int(fn * 4000 + fp * 40)})
r = {row["threshold"]: row for row in rows}
check("cv 0.1 recall %", round(100 * r[0.1]["caught"] / 357), 96)
check("cv 0.1 false alarms", r[0.1]["false_alarms"], 31)
check("cv 0.1 missed", r[0.1]["missed"], 13)
check("cv 0.1 miss cost", r[0.1]["missed"] * 4000, 52000)
check("best threshold", s6["best_threshold"], 0.01)
check("best cost", int(s6["best_cost"]), 31560)
check("two thirds", round(1 - r[0.01]["cost"] / r[0.5]["cost"], 2), 0.66)
check("accuracy highest at expensive end", max(rows, key=lambda x: x["accuracy"])["threshold"] in (0.5, 0.3), True)
tn, fp, fn, tp = confusion_matrix(yte, p > 0.01).ravel()
check("test caught", int(tp), 116)
check("test false alarms", int(fp), 46)
check("test cost", int(fn * 4000 + fp * 40), 13840)
check("test recall %", round(100 * tp / (tp + fn), 1), 97.5)
tn, fp, fn, tp = confusion_matrix(yte, p > 0.5).ravel()
check("test cost at 0.5", int(fn * 4000 + fp * 40), 40080)
check("test accuracy at 0.5 %", round(100 * (tp + tn) / len(yte), 1), 99.2)
check("one in twelve", round((tp + fn) / fn), 12)
check("one in eight", round(119 / 15), 8)
check("cnn parameters", sum(q.numel() for q in at("cnn = train_cnn(seed=53)")["cnn"].parameters()), 27905)
check("cnn threshold", at("cnn = train_cnn(seed=53)")["cnn_threshold"], 0.05)
# 53.7
check("cracked-crate score", round(float(at("scaled = scores /")["scores"][3, 1]), 2), 1.24)
exps = np.exp(at("scaled = scores /")["scaled"][3])
check("exps", [round(float(e), 3) for e in exps], [1.375, 2.403, 1.128, 1.168])
check("exp total", round(float(exps.sum()), 3), 6.074)
check("attention params", 3 * 4 * 2, 24)
check("67 million", round(4 * 4096 ** 2 / 1e6), 67)
# 53.9
check("quantized flips", int(((at("after = model.predict_proba")["before"] > 0.01) != (at("after = model.predict_proba")["after"] > 0.01)).sum()), 7)
tn, fp, fn, tp = confusion_matrix(yte, at("after = model.predict_proba")["after"] > 0.01).ravel()
check("quantized caught", int(tp), 116)
check("quantized false alarms", int(fp), 53)
check("biases", sum(b.size for b in at("after = model.predict_proba")["model"].intercepts_), 49)
# Answers
check("answer 9 re-inspections", (r[0.01]["false_alarms"], r[0.005]["false_alarms"]), (189, 301))
check("answer 9 share", (round(100 * 189 / 4500), round(100 * 301 / 4500)), (4, 7))
check("answer 10 ratio", round(117 / 46, 1), 2.5)
w = g["weights_again"]
check("answer 13 weight on 'was'", (round(float(w[3, 2]), 2), round(float(w[2, 2]), 2)), (0.19, 0.24))

precision, recall, _ = precision_recall_curve(ytr, cvp)
flagged = cvp > 0.01
results = {
    "cv_table": rows,
    "pr_curve": {"recall": [round(float(v), 4) for v in recall], "precision": [round(float(v), 4) for v in precision]},
    "operating_point": {"threshold": 0.01, "recall": float(flagged[ytr == 1].mean()),
                        "precision": float(ytr[flagged].mean())},
    "attention": [[round(float(v), 3) for v in row] for row in w],
}
OUT.write_text(json.dumps(results, indent=1))
print(f"ch53_check.py: {ok} checks passed; wrote {OUT.relative_to(BOOK)}")
