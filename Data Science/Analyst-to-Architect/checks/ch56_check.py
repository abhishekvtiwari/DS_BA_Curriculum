#!/usr/bin/env python3
"""ch56_check.py - checks Chapter 56's numbers against the production stream, the artifact and the service."""
import os, pathlib, sys, warnings
warnings.filterwarnings('ignore')
C = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else '/home/claude/book/companion/ch56')
os.chdir(C); sys.path.insert(0, str(C))
import joblib, numpy as np
from scipy import stats
from sklearn.metrics import confusion_matrix
ok = 0
def check(label, got, want, tol=0.0):
    global ok
    if isinstance(want, float) and isinstance(got, float):
        assert abs(got - want) <= tol + 1e-9, f'{label}: {got} != {want}'
    else:
        assert got == want, f'{label}: {got} != {want}'
    ok += 1
s = np.load('production_data/stream.npz', allow_pickle=True)
X, y, week, brightness, kind = s['features'], s['labels'], s['week'], s['brightness'], s['kind']
check('parts', len(y), 12000); check('weeks', int(week.max()) + 1, 24)
check('defective', int(y.sum()), 1053); check('flash parts', int((kind == 'flash').sum()), 69)
check('flash starts in week', int(week[kind == 'flash'].min()), 16)
check('week 0 brightness', round(float(brightness[week == 0].mean()), 3), 0.392)
check('week 23 brightness', round(float(brightness[week == 23].mean()), 3), 0.448)
bundle = joblib.load('models/defect_v1.joblib')
model, metadata = bundle['model'], bundle['metadata']
check('artifact version', metadata['version'], 'defect-v1')
check('threshold travels with the model', metadata['threshold'], 0.1)
check('metadata records the data hash', len(metadata['data_hash']), 16)
def psi(reference, recent, buckets=10):
    cuts = np.quantile(reference, np.linspace(0, 1, buckets + 1)); cuts[0], cuts[-1] = -np.inf, np.inf
    a = np.clip(np.histogram(reference, cuts)[0] / len(reference), 1e-4, None)
    b = np.clip(np.histogram(recent, cuts)[0] / len(recent), 1e-4, None)
    return float(((b - a) * np.log(b / a)).sum())
base = brightness[week < 8]
check('stable weeks are quiet', round(max(psi(base, brightness[week == w]) for w in range(8)), 2), 0.02)
check('PSI week 15', round(psi(base, brightness[week == 15]), 2), 4.41)
check('PSI week 23', round(psi(base, brightness[week == 23]), 2), 4.25)
check('KS week 15', round(float(stats.ks_2samp(base, brightness[week == 15]).statistic), 2), 0.73)
def recall(weeks, m=model, threshold=0.1):
    rows = np.isin(week, weeks)
    tn, fp, fn, tp = confusion_matrix(y[rows], m.predict_proba(X[rows])[:, 1] > threshold, labels=[0, 1]).ravel()
    return round(tp / (tp + fn), 2), int(fp)
check('recall while inputs drift (weeks 8-15)', recall(range(8, 16))[0] >= 0.94, True)
check('recall after the new mould (weeks 16-23)', recall(range(16, 24))[0], 0.84)
check('recall on the baseline weeks', recall(range(0, 8))[0], 0.98)
from sklearn.neural_network import MLPClassifier
c53X = np.load('../ch53/defect_data/features.npy'); c53y = np.load('../ch53/defect_data/labels.npy')
retrained = MLPClassifier(hidden_layer_sizes=(48,), max_iter=300, random_state=56).fit(
    np.vstack([c53X, X[np.isin(week, range(16, 20))]]),
    np.concatenate([c53y, y[np.isin(week, range(16, 20))]]))
check('retrain lifts recent recall', recall(range(20, 24), retrained)[0], 0.91, tol=0.01)
check('retrain does not forget', recall(range(0, 8), retrained)[0], 0.99)
check('retrain costs false alarms', recall(range(20, 24), retrained)[1] > recall(range(20, 24))[1], True)
import logging
logging.getLogger('defect-service').setLevel(logging.WARNING)
from fastapi.testclient import TestClient
from serve import app
client = TestClient(app)
check('health reports the version', client.get('/health').json()['model_version'], 'defect-v1')
i = int(np.where((week == 0) & (y == 1))[0][0])
check('a defective part is flagged',
      client.post('/predict', json={'part_id': 'P1', 'features': X[i].tolist()}).json()['verdict'], 'defective')
check('a short payload is rejected',
      client.post('/predict', json={'part_id': 'P2', 'features': [0.1] * 50}).status_code, 422)
print(f'ch56_check.py: {ok} checks passed')
