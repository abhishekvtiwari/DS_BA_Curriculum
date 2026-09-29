#!/usr/bin/env python3
"""ch56_check.py - checks the numbers Chapter 56's prose quotes against the production stream, the packaged
artifact, and the service. Run after the chapter's notebook (it needs production_data/ and models/):

    python3 checks/ch56_check.py [companion/ch56]
"""
import os, pathlib, sys, warnings
warnings.filterwarnings('ignore')
C = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else pathlib.Path(__file__).resolve().parents[1] / 'companion' / 'ch56')
os.chdir(C); sys.path.insert(0, str(C))
import joblib, numpy as np
from scipy import stats
from sklearn.metrics import confusion_matrix
from sklearn.neural_network import MLPClassifier
ok = 0
def check(label, got, want, tol=0.0):
    global ok
    if isinstance(want, float) and isinstance(got, float):
        assert abs(got - want) <= tol + 1e-9, f'{label}: {got} != {want}'
    else:
        assert got == want, f'{label}: {got} != {want}'
    ok += 1
cost = lambda fn, fp: int(fn) * 4000 + int(fp) * 40
s = np.load('production_data/stream.npz', allow_pickle=True)
X, y, week, brightness, kind = s['features'], s['labels'], s['week'], s['brightness'], s['kind']
check('parts', len(y), 12000); check('weeks', int(week.max()) + 1, 24)
check('defective', int(y.sum()), 1053); check('flash parts', int((kind == 'flash').sum()), 69)
check('flash starts in week', int(week[kind == 'flash'].min()), 16)
bundle = joblib.load('models/defect_v1.joblib')
model, metadata = bundle['model'], bundle['metadata']
check('artifact version', metadata['version'], 'defect-v1')
check('threshold travels with the model', metadata['threshold'], 0.1)
check('data hash in figure 56.1', metadata['data_hash'][:8], '64712189')
check('artifact size in figure 56.1 and answer 9 (kB)', round(os.path.getsize('models/defect_v1.joblib') / 1024), 95)
# Why this matters: Ch 53's test parts at 0.01 and 0.1
c53X = np.load('../ch53/defect_data/features.npy'); c53y = np.load('../ch53/defect_data/labels.npy')
from sklearn.model_selection import train_test_split
Xtr, Xte, ytr, yte = train_test_split(c53X, c53y, test_size=0.25, random_state=53, stratify=c53y)
p = model.predict_proba(Xte)[:, 1]
tn, fp, fn, tp = confusion_matrix(yte, p > 0.1).ravel(); check('0.1: 113 of 119, 6 false alarms', (int(tp), int(fp)), (113, 6))
tn, fp, fn, tp = confusion_matrix(yte, p > 0.01).ravel(); check('0.01: 116 of 119, 46 false alarms, 13,840', (int(tp), int(fp), cost(fn, fp)), (116, 46, 13840))
def psi(reference, recent, buckets=10):
    cuts = np.quantile(reference, np.linspace(0, 1, buckets + 1)); cuts[0], cuts[-1] = -np.inf, np.inf
    a = np.clip(np.histogram(reference, cuts)[0] / len(reference), 1e-4, None)
    b = np.clip(np.histogram(recent, cuts)[0] / len(recent), 1e-4, None)
    return float(((b - a) * np.log(b / a)).sum())
base = brightness[week < 8]
check('PSI peak in the lamp weeks is 4.4', round(psi(base, brightness[week == 15]), 1), 4.4)
check('4.4 is seventeen times 0.25 (4.4 / 0.25 = 17.6)', int(4.4 / 0.25), 17)
check('held-out stable weeks: noise floor about 0.03', max(psi(brightness[week < 6], brightness[week == w]) for w in (6, 7)) < 0.03, True)
flagged = model.predict_proba(X)[:, 1] > 0.1
def period(weeks):
    d = np.isin(week, weeks) & (y == 1); return round(float(flagged[d].mean()), 3)
check('recall weeks 0-7 (96.8%)', period(range(0, 8)), 0.968)
check('recall weeks 8-15 (96.5%)', period(range(8, 16)), 0.965)
check('recall weeks 16-23 (84.4%)', period(range(16, 24)), 0.844)
check('about 12 points', round((period(range(0, 16)) - period(range(16, 24))) * 100), 12)
check('flash caught 18 of 69', int(flagged[kind == 'flash'].sum()), 18)
weekly = [flagged[(week == w) & (y == 1)].mean() for w in range(24)]
check('lamp weeks recall 0.93-1.00', (round(float(min(weekly[8:16])), 2), round(float(max(weekly[8:16])), 2)), (0.93, 1.0))
check('every mould week below every earlier week', max(weekly[16:]) < min(weekly[:16]), True)
gaps = [y[week == w].mean() - flagged[week == w].mean() for w in range(24)]
check('proxy gap never above one point', max(gaps) <= 0.01, True)
# shadow and retrain
mould = np.isin(week, range(16, 20))
candidate = MLPClassifier(hidden_layer_sizes=(48,), max_iter=300, random_state=56).fit(
    np.vstack([c53X, X[mould]]), np.concatenate([c53y, y[mould]]))
def score(m, weeks):
    rows = np.isin(week, weeks)
    tn, fp, fn, tp = confusion_matrix(y[rows], m.predict_proba(X[rows])[:, 1] > 0.1, labels=[0, 1]).ravel()
    return float(f'{tp / (tp + fn):.2f}'), int(fp), cost(fn, fp)      # as the chapter prints it
check('current recent', score(model, range(20, 24)), (0.88, 28, 101120))
check('retrained recent', score(candidate, range(20, 24)), (0.91, 20, 76800))
check('saving 24,320 = shadow saving', score(model, range(20, 24))[2] - score(candidate, range(20, 24))[2], 24320)
check('retrained old weeks', score(candidate, range(0, 8))[:2], (0.99, 30))
import logging
logging.getLogger('defect-service').setLevel(logging.WARNING); logging.getLogger('httpx2').setLevel(logging.WARNING)
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
