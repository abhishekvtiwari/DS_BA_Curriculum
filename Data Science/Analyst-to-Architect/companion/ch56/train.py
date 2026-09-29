#!/usr/bin/env python3
"""
Analyst to Architect · Chapter 56 · training runs, tracked.
Every run logs its parameters, its metrics and the model itself to a local MLflow store, so every
experiment can be compared next week instead of remembered. These are section 56.3's four runs, as a
script. Run: python train.py   (needs ../ch53/defect_data from Chapter 53)
Tested on: Python 3.11.15, scikit-learn 1.9.1, MLflow 3.16.1.
"""
from __future__ import annotations

import mlflow
import numpy as np
from sklearn.metrics import confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPClassifier

mlflow.set_tracking_uri('sqlite:///mlflow.db')    # one local file: no server, no account, real tracking
mlflow.set_experiment('riverstone-defect')

X = np.load('../ch53/defect_data/features.npy')
y = np.load('../ch53/defect_data/labels.npy')
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=53, stratify=y)

SETTINGS = [
    dict(hidden=24, max_iter=300, threshold=0.1),
    dict(hidden=48, max_iter=300, threshold=0.1),
    dict(hidden=48, max_iter=300, threshold=0.05),
    dict(hidden=96, max_iter=300, threshold=0.1),
]


def run_one(hidden: int, max_iter: int, threshold: float) -> dict:
    with mlflow.start_run(run_name=f'mlp-{hidden}-t{threshold}'):
        model = MLPClassifier(hidden_layer_sizes=(hidden,), max_iter=max_iter, random_state=53)
        model.fit(X_train, y_train)
        probabilities = model.predict_proba(X_test)[:, 1]
        tn, fp, fn, tp = confusion_matrix(y_test, probabilities > threshold).ravel()
        metrics = {'recall': tp / (tp + fn), 'precision': tp / (tp + fp) if tp + fp else 0.0,
                   'false_alarms': float(fp), 'missed': float(fn),
                   'cost_rupees': float(fn * 4000 + fp * 40)}          # Chapter 53's business metric
        mlflow.log_params({'hidden_units': hidden, 'max_iter': max_iter, 'threshold': threshold,
                           'features': X.shape[1], 'training_rows': len(X_train)})
        mlflow.log_metrics(metrics)
        # MLflow 3 saves scikit-learn models with skops and refuses unknown types unless you say
        # they are trusted. That refusal is a feature: it is what stops a pickled model being a
        # remote-code-execution hole (section 56.4).
        mlflow.sklearn.log_model(
            model, name='model',
            skops_trusted_types=['sklearn.neural_network._stochastic_optimizers.AdamOptimizer'])
        return {'hidden': hidden, 'threshold': threshold, **metrics}


if __name__ == '__main__':
    results = [run_one(**setting) for setting in SETTINGS]
    print(f"{'hidden':>7}{'threshold':>11}{'recall':>9}{'precision':>11}{'false alarms':>14}{'cost (Rs)':>12}")
    for r in results:
        print(f"{r['hidden']:>7}{r['threshold']:>11}{r['recall']:>9.3f}{r['precision']:>11.3f}"
              f"{int(r['false_alarms']):>14}{int(r['cost_rupees']):>12,}")
