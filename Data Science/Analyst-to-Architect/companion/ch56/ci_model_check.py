#!/usr/bin/env python3
"""ci_model_check.py - fails the build if the packaged model falls below the agreed floor."""
import sys
import joblib, numpy as np
from sklearn.metrics import confusion_matrix
from sklearn.model_selection import train_test_split

FLOOR = 0.90
bundle = joblib.load("models/defect_v1.joblib")
X = np.load("../ch53/defect_data/features.npy"); y = np.load("../ch53/defect_data/labels.npy")
_, X_test, _, y_test = train_test_split(X, y, test_size=0.25, random_state=53, stratify=y)
probabilities = bundle["model"].predict_proba(X_test)[:, 1]
tn, fp, fn, tp = confusion_matrix(y_test, probabilities > bundle["metadata"]["threshold"]).ravel()
recall = tp / (tp + fn)
print(f"recall {recall:.3f} (floor {FLOOR}), false alarms {fp}, model {bundle['metadata']['version']}")
sys.exit(0 if recall >= FLOOR else 1)
