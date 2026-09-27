"""Analyst to Architect · Chapter 43 · number check.
Recomputes the numbers quoted in Chapter 43's prose and writes checks/ch43_results.json for the figures.
Run from checks/: python3 ch43_check.py   (about 30 seconds). Riverstone Supplies is fictional."""
import copy, json, math, pathlib, warnings
import numpy as np, pandas as pd, torch, torch.nn as nn
from sklearn.compose import ColumnTransformer
from sklearn.datasets import load_digits
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import log_loss, roc_auc_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
warnings.filterwarnings("ignore")
HERE = pathlib.Path(__file__).resolve().parent
COMP = HERE.parent / "companion"
fails = 0
def ok(label, got, want):
    global fails
    good = got == want; fails += not good
    print(("OK  " if good else "BAD ") + f"{label}: {got} (text: {want})")

# 43.1 neuron by hand
x = np.array([16, 5.03]); w = np.array([0.05, 0.9]); b = -1.2
z = w @ x + b
ok("neuron z", round(z, 3), 4.127); ok("neuron sigmoid", round(1 / (1 + math.exp(-z)), 3), 0.984)

# 43.2 XOR
torch.manual_seed(43)
X_xor = torch.tensor([[0.0, 0.0], [0.0, 1.0], [1.0, 0.0], [1.0, 1.0]])
y_xor = torch.tensor([[0.0], [1.0], [1.0], [0.0]])
single = nn.Sequential(nn.Linear(2, 1), nn.Sigmoid())
opt = torch.optim.SGD(single.parameters(), lr=0.5)
lf = nn.BCELoss()
for _ in range(2000):
    opt.zero_grad(); loss = lf(single(X_xor), y_xor); loss.backward(); opt.step()
ok("single neuron XOR loss", round(loss.item(), 4), 0.6931)
ok("ln2", round(math.log(2), 4), 0.6931)

torch.manual_seed(43)
two_layer = nn.Sequential(nn.Linear(2, 4), nn.Tanh(), nn.Linear(4, 1), nn.Sigmoid())
opt2 = torch.optim.SGD(two_layer.parameters(), lr=0.5)
for _ in range(3000):
    opt2.zero_grad(); pred = two_layer(X_xor); loss2 = lf(pred, y_xor); loss2.backward(); opt2.step()
ok("two-layer XOR loss", round(loss2.item(), 5), 0.00097)

# 43.3 forward pass by hand
x_t = torch.tensor([1.0, 0.5])
W1 = torch.tensor([[0.3, -0.2], [0.4, 0.1]]); b1 = torch.tensor([0.1, -0.1])
W2 = torch.tensor([[0.5, -0.6]]); b2 = torch.tensor([0.2])
z1 = W1 @ x_t + b1; a1 = torch.tanh(z1); z2 = W2 @ a1 + b2; a2 = torch.sigmoid(z2)
ok("z2", round(z2.item(), 4), 0.1438); ok("a2", round(a2.item(), 4), 0.5359)

# 43.4 autograd check
W2g = W2.clone().requires_grad_(); b1g = b1.clone().requires_grad_()
W1g = W1.clone().requires_grad_(); b2g = b2.clone().requires_grad_()
target = torch.tensor([1.0])
pred_tiny = torch.sigmoid(W2g @ torch.tanh(W1g @ x_t + b1g) + b2g)
loss_tiny = nn.functional.binary_cross_entropy(pred_tiny, target)
loss_tiny.backward()
ok("autograd grad", round(W2g.grad[0, 0].item(), 4), -0.1352)

# 43.5 tabular
accounts = pd.read_csv(COMP / "accounts" / "accounts.csv")
accounts["rep_id"] = accounts["rep_id"].astype(str)
CATS = ["segment", "city_tier", "company_size", "rep_id"]
NUMS = ["tenure_months", "orders_2024", "units_2024", "revenue_2024", "avg_discount_pct",
        "late_payment_days", "complaints_2024", "categories_bought", "days_since_last_order",
        "website_logins_2024", "catalog_downloads_2024"]
rest, test_acc = train_test_split(accounts, test_size=0.2, random_state=37, stratify=accounts["churned_2025"])
train_acc, valid_acc = train_test_split(rest, test_size=0.25, random_state=37, stratify=rest["churned_2025"])
prepare = ColumnTransformer([("cat", OneHotEncoder(handle_unknown="ignore"), CATS),
    ("num", Pipeline([("fill", SimpleImputer(strategy="median", add_indicator=True)), ("scale", StandardScaler())]), NUMS)])
X_train = prepare.fit_transform(train_acc[CATS + NUMS]).astype("float32")
X_valid = prepare.transform(valid_acc[CATS + NUMS]).astype("float32")
y_train = train_acc["churned_2025"].to_numpy().astype("float32")
y_valid = valid_acc["churned_2025"].to_numpy().astype("float32")

torch.manual_seed(43)
Xtr_t = torch.tensor(X_train); ytr_t = torch.tensor(y_train).unsqueeze(1); Xva_t = torch.tensor(X_valid)
network = nn.Sequential(nn.Linear(X_train.shape[1], 16), nn.ReLU(), nn.Linear(16, 8), nn.ReLU(), nn.Linear(8, 1))
opt3 = torch.optim.Adam(network.parameters(), lr=0.01)
lf3 = nn.BCEWithLogitsLoss()
loss_curve = []
for epoch in range(200):
    opt3.zero_grad(); logits = network(Xtr_t); loss3 = lf3(logits, ytr_t); loss3.backward(); opt3.step()
with torch.no_grad():
    final_pred = torch.sigmoid(network(Xva_t)).numpy().ravel()
ok("nn AUC", round(roc_auc_score(y_valid, final_pred), 3), 0.773)

logit_model = LogisticRegression(max_iter=2000).fit(X_train, y_train)
logit_pred = logit_model.predict_proba(X_valid)[:, 1]
ok("logit AUC", round(roc_auc_score(y_valid, logit_pred), 3), 0.764)
boosting_model = HistGradientBoostingClassifier(learning_rate=0.05, max_depth=3, min_samples_leaf=40, max_iter=300, random_state=37).fit(X_train, y_train)
boosting_pred = boosting_model.predict_proba(X_valid)[:, 1]
ok("boosting AUC", round(roc_auc_score(y_valid, boosting_pred), 3), 0.788)

# 43.6/43.7 digits and transfer
digits = load_digits(); images = digits.images.astype("float32") / 16.0; labels = digits.target
base_mask = labels < 5
X_base, y_base = images[base_mask], labels[base_mask]
Xb_train, Xb_test, yb_train, yb_test = train_test_split(X_base, y_base, test_size=0.25, random_state=43, stratify=y_base)
def to_tensors(im, lb): return torch.tensor(im).unsqueeze(1), torch.tensor(lb).long()
Xb_train_t, yb_train_t = to_tensors(Xb_train, yb_train)
Xb_test_t, yb_test_t = to_tensors(Xb_test, yb_test)

class SmallCNN(nn.Module):
    def __init__(self, n_classes):
        super().__init__()
        self.conv1 = nn.Conv2d(1, 8, 3, padding=1); self.conv2 = nn.Conv2d(8, 16, 3, padding=1)
        self.pool = nn.MaxPool2d(2); self.fc1 = nn.Linear(16 * 2 * 2, 32); self.fc2 = nn.Linear(32, n_classes)
    def features(self, x):
        x = self.pool(torch.relu(self.conv1(x))); x = self.pool(torch.relu(self.conv2(x)))
        return torch.relu(self.fc1(x.flatten(1)))
    def forward(self, x): return self.fc2(self.features(x))

torch.manual_seed(43)
base_model = SmallCNN(5)
opt4 = torch.optim.Adam(base_model.parameters(), lr=0.01)
lf4 = nn.CrossEntropyLoss()
for _ in range(60):
    opt4.zero_grad(); loss4 = lf4(base_model(Xb_train_t), yb_train_t); loss4.backward(); opt4.step()
with torch.no_grad():
    base_accuracy = (base_model(Xb_test_t).argmax(1) == yb_test_t).float().mean().item()
ok("base CNN accuracy", round(base_accuracy, 3), 0.987)

new_mask = labels >= 5
X_new, y_new = images[new_mask], labels[new_mask] - 5
Xn_train, Xn_test, yn_train, yn_test = train_test_split(X_new, y_new, test_size=0.25, random_state=43, stratify=y_new)
Xn_test_t, yn_test_t = to_tensors(Xn_test, yn_test)
rng = np.random.default_rng(43)
def small_training_set(n):
    chosen = []
    for c in range(5):
        cand = np.where(yn_train == c)[0]; chosen.extend(rng.choice(cand, n, replace=False))
    return to_tensors(Xn_train[chosen], yn_train[chosen])
def train_transfer(n, epochs=80):
    Xs, ys = small_training_set(n)
    model = copy.deepcopy(base_model)
    for p in model.conv1.parameters(): p.requires_grad = False
    for p in model.conv2.parameters(): p.requires_grad = False
    model.fc1 = nn.Linear(16 * 2 * 2, 32); model.fc2 = nn.Linear(32, 5)
    o = torch.optim.Adam(filter(lambda p: p.requires_grad, model.parameters()), lr=0.01)
    for _ in range(epochs):
        o.zero_grad(); l = lf4(model(Xs), ys); l.backward(); o.step()
    with torch.no_grad(): return (model(Xn_test_t).argmax(1) == yn_test_t).float().mean().item()
def train_scratch(n, epochs=80):
    Xs, ys = small_training_set(n)
    model = SmallCNN(5)
    o = torch.optim.Adam(model.parameters(), lr=0.01)
    for _ in range(epochs):
        o.zero_grad(); l = lf4(model(Xs), ys); l.backward(); o.step()
    with torch.no_grad(): return (model(Xn_test_t).argmax(1) == yn_test_t).float().mean().item()

results = {}
for n in [3, 5, 10, 15, 30]:
    results[n] = (train_transfer(n), train_scratch(n))
ok("transfer/scratch n=3", tuple(round(v, 3) for v in results[3]), (0.844, 0.754))
ok("transfer/scratch n=30", tuple(round(v, 3) for v in results[30]), (0.929, 0.982))

json.dump({"transfer_scratch": {str(k): v for k, v in results.items()},
           "tabular_comparison": {"logistic": float(roc_auc_score(y_valid, logit_pred)),
                                  "network": float(roc_auc_score(y_valid, final_pred)),
                                  "boosting": float(roc_auc_score(y_valid, boosting_pred))},
           "xor": {"single_loss": loss.item(), "two_layer_loss": loss2.item()}},
          open(HERE / "ch43_results.json", "w"))
print("All checks passed." if not fails else f"FAILED: {fails}")
raise SystemExit(1 if fails else 0)
