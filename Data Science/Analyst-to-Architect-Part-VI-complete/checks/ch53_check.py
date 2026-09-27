#!/usr/bin/env python3
"""ch53_check.py - checks the numbers quoted in Chapter 53 against the generated images and the models."""
import numpy as np, pathlib, sys
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import confusion_matrix
D = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else '/home/claude/book/companion/ch53') / 'defect_data'
ok = 0
def check(label, got, want, tol=0.0):
    global ok
    assert (abs(got - want) <= tol) if isinstance(want, (int, float)) else got == want, f'{label}: {got} != {want}'
    ok += 1
images = np.load(D / 'images.npy'); labels = np.load(D / 'labels.npy'); kinds = np.load(D / 'defect_types.npy')
check('images', images.shape, (6000, 32, 32)); check('defective', int(labels.sum()), 476)
check('defect rate %', round(100 * labels.mean(), 2), 7.93)
check('always-good accuracy %', round(100 * (labels == 0).mean(), 2), 92.07)
for kind, n in (('scratch', 162), ('void', 157), ('short_shot', 157), ('good', 5524)):
    check(f'{kind} count', int((kinds == kind).sum()), n)
# section 53.1 and 53.2 arithmetic
check('neuron weighted sum', round(2.0 * 0.6 + 3.0 * -0.4 + 0.1, 2), 0.10)
z1 = np.array([1.0, 2.0]) @ np.array([[0.5, -0.3], [0.8, 0.2]]) + np.array([0.0, 0.1])
check('hidden sums', list(np.round(z1, 3)), [2.1, 0.2])
z2 = float(np.maximum(0, z1) @ np.array([0.7, -0.5]) + 0.05)
check('prediction', round(z2, 3), 1.42); check('loss', round((z2 - 1.0) ** 2, 3), 0.176)
check('parameters 1024-128-1', 1024 * 128 + 128 + 128 + 1, 131329)
# section 53.5 convolution
patch = np.full((5, 5), 0.2); patch[1:4, 1:4] = 0.7
kernel = np.array([[-1., 0, 1], [-2, 0, 2], [-1, 0, 1]])
check('convolution at (0,0)', round(float((patch[0:3, 0:3] * kernel).sum()), 2), 1.5)
# section 53.6 model
X = np.load(D / 'features.npy')
check('features per image', X.shape[1], 108)
Xtr, Xte, ytr, yte = train_test_split(X, labels, test_size=0.25, random_state=53, stratify=labels)
model = MLPClassifier(hidden_layer_sizes=(48,), max_iter=300, random_state=53).fit(Xtr, ytr)
p = model.predict_proba(Xte)[:, 1]
tn, fp, fn, tp = confusion_matrix(yte, p > 0.5).ravel()
check('recall at 0.5 %', round(100 * tp / (tp + fn), 1), 91.6)
check('precision at 0.5 %', round(100 * tp / (tp + fp), 1), 98.2)
tn, fp, fn, tp = confusion_matrix(yte, p > 0.01).ravel()
check('recall at 0.01 %', round(100 * tp / (tp + fn), 1), 97.5)
check('cheapest cost', fn * 4000 + fp * 40, 13840)
check('cost at 0.5', 10 * 4000 + 2 * 40, 40080)
# section 53.7 attention
emb = np.eye(4)
Q = emb @ np.array([[1.0, 0.0], [0.9, 0.3], [0.2, 0.1], [0.4, 0.9]])
K = emb @ np.array([[0.9, 0.1], [0.4, 1.2], [0.2, 0.1], [0.1, 0.2]])
scores = (Q @ K.T) / np.sqrt(2)
w = np.exp(scores - scores.max(axis=1, keepdims=True))
w = w / w.sum(axis=1, keepdims=True)
check('cracked attends to crate', int(np.argmax(w[3])), 1)
check('cracked-crate weight', round(float(w[3, 1]), 3), 0.396)
check('rows sum to one', round(float(w.sum(axis=1).min()), 6), 1.0)
# section 53.9 quantization
weights = model.coefs_[0]
scale = np.abs(weights).max() / 127
restored = np.round(weights / scale).astype(np.int8).astype(np.float32) * scale
check('quantization is 4x smaller', weights.nbytes // np.round(weights / scale).astype(np.int8).nbytes, 4)
check('largest quantization error', round(float(np.abs(weights - restored).max()), 4) <= 0.0051, True)
print(f'ch53_check.py: {ok} checks passed')
