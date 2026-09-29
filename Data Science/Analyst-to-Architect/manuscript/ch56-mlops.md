# Chapter 56. MLOps: Making Models Survive Production

*Part 6 — Production ML, Generative AI & MLOps*

> **Chapter at a glance**
>
> **You will learn to:** name the four ways a working model stops working · version the five things that make up "the model" · track experiments so every run can be compared instead of remembered · register a model and point a name at the version in use · package a model with the metadata that has to travel with it · serve it behind a real HTTP endpoint with validation, versioning, and a log line monitoring can read · choose between batch, online, shadow, canary, and blue-green · monitor in three layers, and know which layer sees which failure · compute drift with PSI and the KS statistic, and see why drift alarms and model decay are not the same thing · decide when to retrain, and what to check before shipping the retrain · run an incident and write the post-mortem · and judge how far up the MLOps maturity ladder your company should actually climb.
>
> **Before you start:** Chapter 53 (the defect model this chapter operates, and its threshold chosen with money), Chapter 29 (tested, packaged Python; classes, decorators, type hints, logging), Chapter 34 (the command line, background jobs, HTTP and `curl`), Chapters 26 and 32 (CI: a check on every push), Chapter 39 (evaluation: recall, precision, a threshold chosen by cost), Chapter 30 (A/B tests), and Chapter 52 (containers).
>
> **Time needed:** 18–22 hours, spread over three weeks, in three sittings: sections 56.0–56.5 (setup, versioning, tracking, packaging, and a running service), about 8 hours; sections 56.6–56.9 (deployment, monitoring, drift, and retraining), about 7 hours; sections 56.10–56.11, the project and the exercises take the rest.
>
> **Tools:** Python with NumPy, SciPy, and scikit-learn (Chapters 18, 21 and 35), plus four new packages installed in section 56.0: FastAPI, uvicorn, httpx2, and MLflow. All local; no cloud account.
>
> **Practice data:** six months of Riverstone's moulding line, built by `simulate_production.py` in `companion/ch56`: 12,000 parts over 24 weeks, with the lamps replaced in week 8 and a new mould producing an unlabeled defect from week 16. It uses Chapter 53's `defect_data` folder, which must sit beside it in `companion/ch53`.

---

## Why this matters

Chapter 53 ended with a defect model whose threshold was priced in rupees. Its cheapest point, 0.01, caught 97.5% of the test defects (116 of 119) with 46 false alarms in 1,500 parts. For the camera's first months on the line, the plant manager agreed a different point: **0.1**, which on the same test parts catches 95% of defects (113 of 119) and sends 6 good parts in 1,500 for re-inspection instead of 46, because the QC inspector had been moved to a second line (Chapter 53's story) and had little time to spare. That was the easy part. The hard part is the next six months, and it fails in four ways that have nothing to do with modeling:

- **The world moves.** New lamps, a new mould, a new supplier's resin. The model was trained on a world that no longer exists.
- **Nobody notices.** A model that has quietly got worse looks exactly like a model that is fine, unless someone is measuring.
- **Nobody can reproduce it.** Six months later, "which data was this trained on?" has no answer, so the model cannot be rebuilt, audited, or improved.
- **Nobody can roll it back.** A retrain ships, quality drops, and there is no previous version to return to.

This chapter is the discipline that fixes all four, and it is the difference between a demo and a system. It is also, in most companies, the work that goes to the person who can *both* train a model and run software, which is the ML engineer role on Chapter 8's career tree and a significant salary step.

---

## In plain English

**A model is a perishable good, and MLOps is the cold chain.**

**MLOps**, short for machine-learning operations, is the set of practices that keeps a model working, and right, after it leaves the notebook: versioning what it was built from, tracking how it was built, packaging and serving it, monitoring it, retraining it, and rolling it back. Chapter 53 named it in one line; this chapter teaches it.

A trained model is a set of numbers that encode how the world looked on the day the training data was collected. Deploy it and it starts aging immediately, because the world doesn't stand still: lighting changes, products change, customers change, and the model doesn't.

The cold chain has four parts, and you need all four:

- **Labels on the box.** Which data, which code, which parameters, which day. Without them you cannot reproduce, compare, or roll back.
- **A thermometer.** Monitoring, in layers: is the service up, does the incoming data look like what we trained on, and is the model still right? Each layer catches a different failure, and the last one is late because the truth arrives late.
- **A rule for when to throw it out.** A retraining trigger, decided in advance, so the decision isn't made by whoever shouts loudest.
- **A way to put the old one back.** Rollback, practiced before you need it.

The rest of this chapter is those four parts, on Riverstone's defect model, with real tools and measured results.

---

## 56.0 Setting up

### Step 1. Install the four new packages

Open a terminal (Chapter 26, section 26.0), activate the book's virtual environment (Chapter 17, section 17.0), and install:

<!-- run: none -->
```
# terminal
$ python -m pip install fastapi==0.141.1 uvicorn==0.54.0 httpx2==2.13.1 mlflow==3.16.1
```

- **`fastapi`** is a library for writing web services in Python: you write ordinary functions, and FastAPI turns them into HTTP endpoints (section 56.5). It brings **`pydantic`** with it, the library that checks incoming data against a schema.
- **`uvicorn`** is the web server that runs a FastAPI service and listens on a port (Chapter 34, section 34.9).
- **`httpx2`** is the newest generation of `httpx`, the HTTP client Chapter 29 mentioned beside `requests`. FastAPI's test client (section 56.5) uses it to call a service without starting a server. (Older guides say to install `httpx`; with this FastAPI version the test client still works with it, but prints a warning asking for `httpx2`.)
- **`mlflow`** records training runs, stores models, and keeps a registry of model versions (section 56.3). It is the largest of the four and takes a minute or two to install. It brings `skops`, a safer way to save scikit-learn models, which section 56.3 uses.
- `==` pins the exact version this chapter's outputs came from (Chapter 17). Add the four packages to your `requirements.txt`.

### Step 2. Build six months of production

Go to the chapter's companion folder. Chapter 53's companion folder, `companion/ch53`, must sit beside it, with the `defect_data` folder you made there, including the `features.npy` file that section 53.6 saved:

```
# terminal
$ cd companion/ch56
$ ls ../ch53/defect_data
defect_types.npy
features.npy
images.npy
labels.npy

$ python simulate_production.py
12,000 parts over 24 weeks (1,053 defective, of which 69 are the new flash defect)
mean brightness: week 0 0.392, week 23 0.448
```

- `cd companion/ch56` moves into the chapter's folder (Chapter 26, section 26.0).
- `ls ../ch53/defect_data` checks that Chapter 53's data is where this chapter expects it: `..` is the parent folder, `companion`, so `../ch53` is Chapter 53's folder. If `features.npy` is missing, run section 53.6's feature cell again.
- `python simulate_production.py` draws 12,000 more moulded lids the way Chapter 53's generator did, but in time order, 500 a week for 24 weeks, and changes the line twice along the way (section 56.1). It computes Chapter 53's 108 convolution features for every part and saves everything to `production_data/stream.npz`. It takes about two minutes. The seed is fixed (56), so your two printed lines should match these exactly.

The folders now look like this:

```text
companion/
├── ch53/
│   └── defect_data/          Chapter 53's 6,000 images, labels and features
└── ch56/
    ├── simulate_production.py
    ├── train.py              section 56.3's training runs, as one script
    ├── serve.py              section 56.5's service
    ├── ci_model_check.py     exercise 9's CI check
    └── production_data/
        └── stream.npz        the 24 weeks you just built
```

### Step 3. The notebook

Start Jupyter from `companion/ch56` (Chapter 17, section 17.0), open a new notebook, and run every cell in this chapter in order, in that one notebook: later cells use names that earlier cells made. The first cell checks the new packages:

```python
import fastapi, uvicorn, httpx2, mlflow, pydantic

for package in (fastapi, uvicorn, httpx2, mlflow, pydantic):
    print(f"{package.__name__:<9} {package.__version__}")
```

```
fastapi   0.141.1
uvicorn   0.54.0
httpx2    2.13.1
mlflow    3.16.1
pydantic  2.13.5
```

- `import fastapi, uvicorn, httpx2, mlflow, pydantic` imports the five packages; if any is missing, this is where you find out.
- Every package keeps its version number in `__version__`, and `__name__` holds its name. `:<9` pads the name to nine characters so the versions line up (Chapter 17's format codes).

> **Tool note.** The outputs in this chapter were produced with Python 3.11.15, NumPy 2.4.6, SciPy 1.17.1, scikit-learn 1.9.1, joblib 1.6.0, FastAPI 0.141.1, pydantic 2.13.5, uvicorn 0.54.0, httpx2 2.13.1, and MLflow 3.16.1. Newer versions may print a few numbers slightly differently. MLflow writes a few `INFO` messages in red the first time it creates its database; they are messages, not errors.

---

## 56.1 What breaks after launch

```python
import numpy as np

stream = np.load("production_data/stream.npz", allow_pickle=True)
features, labels, week = stream["features"], stream["labels"], stream["week"]
brightness, kind = stream["brightness"], stream["kind"]

print(f"{len(labels):,} parts over {week.max() + 1} weeks, {labels.sum():,} defective")
counts = dict(zip(*np.unique(kind, return_counts=True)))
print("part types seen:", {str(k): int(v) for k, v in counts.items()})
print(f"mean brightness, week 0: {brightness[week == 0].mean():.3f}")
print(f"mean brightness, week 23: {brightness[week == 23].mean():.3f}")
print(f"the new 'flash' defect first appears in week {week[kind == 'flash'].min()}")
```

```
12,000 parts over 24 weeks, 1,053 defective
part types seen: {'flash': 69, 'good': 10947, 'scratch': 347, 'short_shot': 320, 'void': 317}
mean brightness, week 0: 0.392
mean brightness, week 23: 0.448
the new 'flash' defect first appears in week 16
```

**Line by line:**

- `np.load(..., allow_pickle=True)` reads the compressed archive the simulator wrote. An `.npz` file is several `.npy` arrays in one file (Chapter 53, section 53.0), and `stream["features"]` picks one out by name. `allow_pickle` is needed only because the `kind` array holds text.
- `features` has one row of 108 numbers per part, `labels` is 1 for a defective part, `week` runs 0 to 23, `brightness` is each image's mean pixel value, and `kind` names the part: good, or one of the defects.
- `np.unique(..., return_counts=True)` returns two arrays, the distinct values and how often each occurs. `zip(*...)` pairs them up, and `dict(...)` turns the pairs into a readable tally.
- `week[kind == 'flash'].min()` keeps the weeks of the flash parts and takes the earliest.

Two changes are hidden in that data, and they are the two that matter in practice:

| Change | Name | When | What a monitor sees |
|---|---|---|---|
| The lamps are replaced, so the belt looks brighter | **data drift** (the inputs change) | weeks 8–15 | a large, obvious shift in the input distribution |
| A new mould produces "flash", a defect nobody labeled | **concept drift** (the relationship changes) | weeks 16–23 | nothing, until labels arrive |

Section 56.8 measures both, and the result is not what most articles about drift will tell you.

---

## 56.2 Versioning: "the model" is five things

| What | Why it must be versioned | How |
|---|---|---|
| **Data** | "trained on last March's images" is not reproducible | a snapshot, a hash, or a query pinned to a date (Chapter 32's snapshots) |
| **Features** | the same raw image gives different features if the code changed | the feature code in Git, its version recorded with the model |
| **Code** | the training script is part of the model | the Git commit hash, recorded with the model |
| **Model artifact** | the trained weights themselves | a file in a registry, with a version number |
| **Config** | the threshold is a business decision, and it moves | in the artifact's metadata, not hard-coded in the service |

![Five boxes in a row: data, features, code, artifact and config, each with the value Riverstone records for it, and a note that one artifact carries the model and its metadata so a rollback restores both](figures/fig56-3-versioning.svg)

*Figure 56.1 — "The model" is five things, and a rollback has to restore all of them.*

A **model registry** is the index of those artifacts: for each model name, a numbered list of versions, the run that produced each one, its metrics, and an **alias**, a label such as `production` or `champion` that points at the version in use. Moving the alias is how a new version goes live, and moving it back is a rollback. (Older MLflow called these labels **stages**, with fixed names such as Staging and Production; MLflow has deprecated stages since version 2.9 in favour of aliases, and you will still meet both.) MLflow's registry, SageMaker's, Vertex AI's, and a folder with a strict naming convention are all implementations of the same idea, and the folder is a legitimate starting point for one model.

> **Watch out: the threshold is part of the model.** The plant manager agreed 0.1, from the cost of a miss against a false alarm and the inspector's time. If that number lives in the service's code and the model artifact lives in a registry, you have two things that must be changed together and are stored apart. Put the threshold in the artifact's metadata, as section 56.4 does, and have the service read it from there, as section 56.5's does; then a rollback returns both.

---

## 56.3 Experiment tracking

**Experiment tracking** means recording every training run, with what you chose (its **parameters**), what happened (its **metrics**), and the model it made, in one place you can query later. MLflow does this with a **tracking store**; here, one local file. First the data, split exactly as Chapter 53 split it:

```python
import warnings
import mlflow
from sklearn.exceptions import ConvergenceWarning
from sklearn.metrics import confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPClassifier

warnings.filterwarnings("ignore", category=ConvergenceWarning)

X = np.load("../ch53/defect_data/features.npy")
y = np.load("../ch53/defect_data/labels.npy")
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=53, stratify=y)
print(f"training rows {len(X_train):,}, test rows {len(X_test):,}, test defects {y_test.sum()}")
```

```
training rows 4,500, test rows 1,500, test defects 119
```

- `warnings.filterwarnings("ignore", category=ConvergenceWarning)` hides scikit-learn's "stopped before converging" message, and only that one, as Chapter 53 did (section 53.3): several networks here train on a fixed budget of 300 epochs, and the smallest one uses all of it. Every other warning still shows.
- `X` is Chapter 53's 6,000 × 108 feature table and `y` its labels, loaded from Chapter 53's folder with the relative path `../ch53/`.
- `train_test_split(..., test_size=0.25, random_state=53, stratify=y)` repeats Chapter 53's split (section 53.6) with the same seed, so the 1,500 test parts are the same parts, with the same 119 defects.

Now point MLflow at its store:

```python
mlflow.set_tracking_uri("sqlite:///mlflow.db")
experiment = mlflow.set_experiment("riverstone-defect")
print(f"experiment '{experiment.name}', id {experiment.experiment_id}")
```

```
experiment 'riverstone-defect', id 1
```

- `set_tracking_uri("sqlite:///mlflow.db")` puts the whole store in one SQLite database file, `mlflow.db`, next to the notebook: no server, no account. The model files themselves go in a folder called `mlruns` beside it. (MLflow 3.16 refuses the older plain-folder store unless you opt in with a setting, and asks for a database instead; a local SQLite file is the "no infrastructure" choice.)
- `set_experiment` names a group of runs, and creates it the first time, so a year of work is browsable rather than a heap. It returns the experiment, whose `name` and `experiment_id` the `print` shows.

One run, as a function:

```python
def run_one(hidden, max_iter, threshold):
    with mlflow.start_run(run_name=f"mlp-{hidden}-t{threshold}"):
        model = MLPClassifier(hidden_layer_sizes=(hidden,), max_iter=max_iter, random_state=53)
        model.fit(X_train, y_train)
        probabilities = model.predict_proba(X_test)[:, 1]
        tn, fp, fn, tp = confusion_matrix(y_test, probabilities > threshold).ravel()
        metrics = {"recall": tp / (tp + fn), "precision": tp / (tp + fp) if tp + fp else 0.0,
                   "false_alarms": float(fp), "missed": float(fn),
                   "cost_rupees": float(fn * 4000 + fp * 40)}      # Chapter 53's business metric
        mlflow.log_params({"hidden_units": hidden, "max_iter": max_iter, "threshold": threshold,
                           "features": X.shape[1], "training_rows": len(X_train)})
        mlflow.log_metrics(metrics)
        logged = mlflow.sklearn.log_model(
            model, name="model",
            skops_trusted_types=["sklearn.neural_network._stochastic_optimizers.AdamOptimizer"])
        return {"hidden": hidden, "threshold": threshold, **metrics, "model_uri": logged.model_uri}
```

**Line by line:**

- `with mlflow.start_run(run_name=...)` opens a run and closes it when the indented block ends, even if training raises an error, which is what you want: a failed run that recorded its parameters is still evidence. `run_name` is the label you will see, such as `mlp-48-t0.1`.
- The next four lines are Chapter 53's model and threshold. `MLPClassifier(hidden_layer_sizes=(hidden,), max_iter=max_iter, random_state=53)` is a network with one hidden layer of `hidden` neurons (the tuple holds one number per hidden layer), trained for at most `max_iter` epochs, with Chapter 53's seed. It is trained, then asked for probabilities, which `probabilities > threshold` turns into yes/no.
- `confusion_matrix(...).ravel()` returns the four counts in the order true negative, false positive, false negative, true positive (Chapter 39, section 39.1), which the next line needs by name.
- `metrics` is a dictionary of what happened. `tp / (tp + fp) if tp + fp else 0.0` guards precision against dividing by zero when nothing is flagged. `cost_rupees` is Chapter 53's price: ₹4,000 for each missed defect, ₹40 for each false alarm. `float(...)` makes every value a plain decimal, which is what MLflow stores.
- `log_params` records what you chose; `log_metrics` records what happened. **Log the business metric**, not only the statistical one: `cost_rupees` is what the plant manager compares, and it is the column you will sort by.
- `log_model` stores the trained model itself in the run, so the run is not just a note about a model that has since been overwritten. MLflow 3 saves scikit-learn models with `skops`, which refuses to save or load a type it doesn't recognise unless you list it in `skops_trusted_types`. `AdamOptimizer` is the part of the network that did the training (Chapter 53, section 53.2's optimizers), so it is named here in full. Section 56.4 explains why that refusal is a feature.
- The `return` line builds the result: `**metrics` copies every key and value of the `metrics` dictionary into the new one, which is how Python merges dictionaries, and `logged.model_uri` is the address MLflow gave the stored model, kept for the registry below.

Run it once, for the settings the plant manager agreed:

```python
first = run_one(48, 300, 0.1)
print(f"recall {first['recall']:.3f}, precision {first['precision']:.3f}, "
      f"false alarms {first['false_alarms']:.0f}, cost {first['cost_rupees']:,.0f} rupees")
```

```
recall 0.950, precision 0.950, false alarms 6, cost 24,240 rupees
```

The same 113 of 119 defects and 6 false alarms as the 0.1 point in "Why this matters": the run reproduces the book's model, and now it is recorded. Three more settings follow, the ones `train.py` in the companion folder runs as a script:

```python
results = [first]
for hidden, threshold in [(24, 0.1), (48, 0.05), (96, 0.1)]:
    results.append(run_one(hidden, 300, threshold))

print(f"{'hidden':>7}{'threshold':>11}{'recall':>9}{'precision':>11}{'false alarms':>14}{'cost (Rs)':>12}")
for r in results:
    print(f"{r['hidden']:>7}{r['threshold']:>11}{r['recall']:>9.3f}{r['precision']:>11.3f}"
          f"{r['false_alarms']:>14.0f}{r['cost_rupees']:>12,.0f}")
```

```
 hidden  threshold   recall  precision  false alarms   cost (Rs)
     48        0.1    0.950      0.950             6      24,240
     24        0.1    0.933      0.902            12      32,480
     48       0.05    0.958      0.884            15      20,600
     96        0.1    0.933      0.982             2      32,080
```

- `results` starts with the first run and gains one dictionary per setting.
- The two `print` lines make a table: `:>7` right-aligns in 7 characters, `.3f` keeps three decimals, and `,.0f` adds thousands separators with no decimals.
- Run the notebook twice and the store holds every run twice: MLflow never overwrites. Delete `mlflow.db` and the `mlruns` folder to start again.

And querying them afterwards, which is the entire point:

```python
runs = mlflow.search_runs(experiment_names=["riverstone-defect"], order_by=["metrics.cost_rupees ASC"])
columns = ["tags.mlflow.runName", "params.hidden_units", "params.threshold",
           "metrics.recall", "metrics.cost_rupees"]
print(runs[columns].to_string(index=False))
print(f"\ncheapest run: {runs.iloc[0]['tags.mlflow.runName']}")
```

```
tags.mlflow.runName params.hidden_units params.threshold  metrics.recall  metrics.cost_rupees
       mlp-48-t0.05                  48             0.05        0.957983              20600.0
        mlp-48-t0.1                  48              0.1        0.949580              24240.0
        mlp-96-t0.1                  96              0.1        0.932773              32080.0
        mlp-24-t0.1                  24              0.1        0.932773              32480.0

cheapest run: mlp-48-t0.05
```

- `search_runs(experiment_names=["riverstone-defect"], ...)` finds every run in the named experiments and returns a **pandas DataFrame**, one row per run (Chapter 18). Parameters appear as columns named `params.<name>`, metrics as `metrics.<name>`, and the run name as the tag `tags.mlflow.runName`. `order_by=["metrics.cost_rupees ASC"]` sorts cheapest first, the way SQL's `ORDER BY` does.
- `runs[columns]` keeps five columns, and `.to_string(index=False)` prints them without the row numbers. Parameters come back as text, which is why `0.05` and `0.1` print as typed.
- `runs.iloc[0]` is the first row, the cheapest run.

**Read the ordering.** The cheapest configuration is not the most accurate by precision, nor the biggest network. The 96-unit model has the best precision (0.982) and one of the worst costs, because it misses more defects. **Sorting by the business metric puts the right run first**, and that is why the metric belongs in the tracking store.

The cheapest run, `mlp-48-t0.05`, beats the agreed `mlp-48-t0.1` by one caught defect (114 against 113 of 119) at the price of 9 more false alarms. With 119 test defects, one part is inside the luck of the split, so version 1 keeps the plant manager's 0.1. Re-tuning the threshold belongs to the next retrain, with fresh data (section 56.9).

To browse the same runs in a web page, run `mlflow ui --backend-store-uri sqlite:///mlflow.db --port 5056` in a terminal in this folder and open `http://127.0.0.1:5056`. The page lists the experiment's runs as a table you can sort and filter, with each run's parameters, metrics and stored model one click away; `Ctrl+C` in the terminal stops it.

### The registry: a name, versions, and an alias

Register the agreed run's model under a name, point the alias `production` at it, and load it back by name:

```python
from mlflow import MlflowClient

version = mlflow.register_model(first["model_uri"], "riverstone-defect")
client = MlflowClient()
client.set_registered_model_alias("riverstone-defect", "production", version.version)

production = mlflow.sklearn.load_model("models:/riverstone-defect@production")
in_use = client.get_model_version_by_alias("riverstone-defect", "production")
print(f"riverstone-defect version {in_use.version} is @production: "
      f"{type(production).__name__} with {production.hidden_layer_sizes[0]} hidden units")
```

```
riverstone-defect version 1 is @production: MLPClassifier with 48 hidden units
```

- `mlflow.register_model(uri, name)` records the logged model in the registry under the name `riverstone-defect` and gives it the next version number. The first time, that is version 1.
- `MlflowClient()` is MLflow's lower-level interface, for jobs the one-line functions don't cover. `set_registered_model_alias(name, alias, version)` points the alias at a version; a later call with a different version moves it.
- `"models:/riverstone-defect@production"` is an address: the model named `riverstone-defect`, whichever version `@production` points at. `load_model` fetches it, so code that loads by alias never needs to know a version number.
- `get_model_version_by_alias` asks which version the alias points at, and `type(production).__name__` confirms that what came back is the trained network.
- MLflow also writes two lines to the notebook's red log area, "Successfully registered model" and "Created version '1'". Run the cell again and the registry makes version 2 of the same model, and the alias moves to it.

---

## 56.4 Packaging: what travels with the model

The registry is where the team finds versions. The service on the line should not need the tracking database to start, so the model it runs is **packaged**: one file holding the trained model and its **metadata**, the facts somebody will ask about in six months. First the metadata:

```python
import hashlib
import subprocess
import sklearn

probabilities = production.predict_proba(X_test)[:, 1]
tn, fp, fn, tp = confusion_matrix(y_test, probabilities > 0.1).ravel()
git = subprocess.run(["git", "rev-parse", "--short", "HEAD"], capture_output=True, text=True)

metadata = {
    "version": "defect-v1",
    "registry": f"riverstone-defect version {in_use.version}",
    "trained_on": "ch53 defect_data (6,000 images, seed 53)",
    "training_rows": len(X_train),
    "data_hash": hashlib.sha256(X_train.tobytes()).hexdigest()[:16],
    "features": X.shape[1],
    "feature_version": "conv108-v1",
    "code_commit": git.stdout.strip() or "none (not a Git repository)",
    "sklearn": sklearn.__version__,
    "trained_at": "2026-03-02T09:00:00",
    "threshold": 0.1,
    "metrics": {"recall": round(float(tp / (tp + fn)), 3), "precision": round(float(tp / (tp + fp)), 3)},
}
print(f"{len(metadata)} fields, data hash {metadata['data_hash']}")
```

```
12 fields, data hash 64712189dd1e70d8
```

**Line by line:**

- The first two lines score the registered model on Chapter 53's test parts at the agreed threshold, so the metadata records what the model scored when it was built.
- `subprocess.run([...], capture_output=True, text=True)` runs a terminal command from Python and keeps what it printed (Chapter 18). `git rev-parse --short HEAD` prints the short hash of the current commit (Chapter 26), which is the **code** version.
- `"version"` is the name people will say out loud; `"registry"` ties it to the registry's version number.
- `"data_hash"` is the cheap version of data versioning. `X_train.tobytes()` is the training table as raw bytes; `hashlib.sha256(...).hexdigest()` fingerprints them (Chapter 45, section 45.5); `[:16]` keeps 16 characters, plenty to tell two datasets apart. Change one number in the training data and the hash changes completely.
- `"feature_version"` names the feature code: `conv108-v1` is Chapter 53's three kernels, pooled to 108 numbers. If anyone changes a kernel, they change this name, and the service can refuse a model built on features it doesn't compute.
- `"code_commit"`: `git.stdout.strip()` is the hash, or an empty string when the folder is not in a Git repository, in which case `or` supplies the honest `"none (not a Git repository)"`. In your own project, which lives in Git (Chapter 26), this is a seven-character hash. A metadata field that says "none" is a warning worth having.
- `"sklearn"` records the library version, because a model saved by one version of scikit-learn may not load in another.
- `"trained_at"` is the story's training day, 2 March 2026, written as text so your file matches the book. A real pipeline writes `datetime.now().isoformat(timespec="seconds")` here.
- `"threshold"` is the decision boundary, **inside** the package (section 56.2), and `"metrics"` is what the model scored when it was built.

Now write the package, one file:

```python
import os
import joblib

os.makedirs("models", exist_ok=True)
joblib.dump({"model": production, "metadata": metadata}, "models/defect_v1.joblib")
print(f"models/defect_v1.joblib: {round(os.path.getsize('models/defect_v1.joblib') / 1024)} kB")
```

```
models/defect_v1.joblib: 95 kB
```

- `os.makedirs("models", exist_ok=True)` creates the `models` folder, and does nothing if it already exists.
- `joblib.dump(obj, path)` saves any Python object to a file. A Chapter 36 exercise mentioned it for a fitted pipeline; this is where it is used properly. The object here is a dictionary with two keys, the model and its metadata, so **they cannot be separated**: whoever has the model has its threshold.
- `os.path.getsize(...)` is the file's size in bytes; dividing by 1,024 gives kilobytes.

What the service will see when it loads the file:

```python
bundle = joblib.load("models/defect_v1.joblib")
model, metadata = bundle["model"], bundle["metadata"]

for key, value in metadata.items():
    print(f"  {key:<16} {value}")
```

```
  version          defect-v1
  registry         riverstone-defect version 1
  trained_on       ch53 defect_data (6,000 images, seed 53)
  training_rows    4500
  data_hash        64712189dd1e70d8
  features         108
  feature_version  conv108-v1
  code_commit      none (not a Git repository)
  sklearn          1.9.1
  trained_at       2026-03-02T09:00:00
  threshold        0.1
  metrics          {'recall': 0.95, 'precision': 0.95}
```

- `joblib.load` reads the file back into the same dictionary, and the second line unpacks its two entries.
- `metadata.items()` gives each key with its value, and `:<16` pads the keys so the values line up.

The metadata answers the questions somebody will ask in six months: what was it trained on, how many rows, with which data, which feature code, which code commit, which library version, what threshold, and what it scored.

**On pickles.** `joblib` and `pickle` store Python objects by storing instructions for rebuilding them, which means **loading a pickle can run arbitrary code**. That is fine for a file your own pipeline wrote; it is a serious vulnerability for a file that arrived from outside. MLflow 3 makes the point for you: its `skops` format refuses to load a scikit-learn model containing types it doesn't recognise until you list them as trusted, which is why section 56.3 named `AdamOptimizer` explicitly. Treat a model artifact like an executable: signed, stored where you control access, and never loaded from an untrusted source.

---

## 56.5 Serving

Three shapes, and most teams need only the first two:

| Pattern | The model runs | Latency | Fits |
|---|---|---|---|
| **Batch** | on a schedule, over many rows at once | minutes to hours | scoring yesterday's parts, churn lists, demand forecasts |
| **Online** | when a request arrives | milliseconds | a camera on a line, a fraud check, a recommendation |
| **Streaming** | as events arrive on a queue | seconds | continuous sensors, clickstreams (Chapter 50) |

Riverstone's camera needs online serving: a web service with an **endpoint**, an address such as `/predict` that answers HTTP requests (Chapter 34, section 34.9). The companion file `serve.py` is the whole service. The next four cells build it one piece at a time; `serve.py` holds exactly these definitions, without the `print` lines.

### The input contract

```python
from pydantic import BaseModel, Field, ValidationError

class Part(BaseModel):
    part_id: str = Field(min_length=1, max_length=40)
    features: list[float] = Field(min_length=108, max_length=108)

good_request = Part(part_id="demo-1", features=[0.1] * 108)
print(f"accepted {good_request.part_id} with {len(good_request.features)} features")
try:
    Part(part_id="demo-2", features=[0.1] * 50)
except ValidationError as error:
    print("rejected:", error.errors()[0]["msg"])
```

```
accepted demo-1 with 108 features
rejected: List should have at least 108 items after validation, not 50
```

**Line by line:**

- `class Part(BaseModel):` declares a **schema**: the shape a request must have. It is a class (Chapter 29, section 29.5) built on pydantic's `BaseModel`, which is what makes it check its inputs.
- Each line inside is a field with a type hint (Chapter 29, section 29.6): `part_id` must be text, `features` a list of decimals. `Field(min_length=..., max_length=...)` adds limits: an id of 1 to 40 characters, and exactly 108 features.
- `Part(part_id=..., features=[0.1] * 108)` builds one. `[0.1] * 108` is a list of 108 copies of 0.1. It passes, so nothing is raised.
- `try:` / `except ValidationError as error:` catches the failure (Chapter 29, section 29.8) when a part arrives with 50 features. `error.errors()` lists every problem found, and `[0]["msg"]` is the first one's message.

That schema is the service's **input contract**: a request with 50 features is rejected before the model sees it. FastAPI answers such a request with HTTP status **422**, "unprocessable content": the request arrived, but its content breaks the contract. That is the difference between a clear error and a wrong prediction on garbage.

### The app, its log, and its model

```python
import json
import logging
import time
from fastapi import FastAPI, HTTPException

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s %(message)s")
log = logging.getLogger("defect-service")

bundle = joblib.load("models/defect_v1.joblib")
model, metadata = bundle["model"], bundle["metadata"]
app = FastAPI(title="Riverstone defect detector", version=metadata["version"])
print(f"{app.title}: model {metadata['version']}, threshold {metadata['threshold']}")
```

```
Riverstone defect detector: model defect-v1, threshold 0.1
```

- `logging.basicConfig(...)` and `getLogger("defect-service")` set up a named logger that writes a time, a level, its name and a message per line (Chapter 29, section 29.8).
- The two `joblib` lines load the package from section 56.4 **once, when the service starts**, not on every request.
- `FastAPI(title=..., version=...)` creates the application, `app`. Everything the service answers is attached to it in the next two cells.

### The health check

```python
@app.get("/health")
def health() -> dict:
    """Liveness and readiness in one: the service is up AND the model is loaded."""
    return {"status": "ok", "model_version": metadata["version"], "threshold": metadata["threshold"]}

print(health())
```

```
{'status': 'ok', 'model_version': 'defect-v1', 'threshold': 0.1}
```

- `@app.get("/health")` is a decorator (Chapter 29, section 29.5): it registers the function below it as the answer to GET requests for the path `/health`. The function itself is unchanged, which is why the `print` can still call it directly.
- A **health check** is an endpoint that says whether the service can do its job. **Liveness** asks "is the process running?"; **readiness** asks "can it serve requests yet?", here, "is the model loaded?". Kubernetes asks exactly these questions (Chapter 52, section 52.3's `readinessProbe`).
- It returns the model version and threshold, not just "ok". A health check that passes while the wrong model is loaded has told you nothing.

### The prediction

```python
@app.post("/predict")
def predict(part: Part) -> dict:
    started = time.perf_counter()
    values = np.asarray(part.features, dtype=float)
    if not np.isfinite(values).all():
        raise HTTPException(status_code=422, detail="features contain NaN or infinity")
    probability = float(model.predict_proba(values.reshape(1, -1))[0, 1])
    verdict = "defective" if probability > metadata["threshold"] else "good"
    elapsed_ms = (time.perf_counter() - started) * 1000
    log.info(json.dumps({"part_id": part.part_id, "probability": round(probability, 4),
                         "verdict": verdict, "model_version": metadata["version"],
                         "latency_ms": round(elapsed_ms, 2), "mean_feature": round(float(values.mean()), 4)}))
    return {"part_id": part.part_id, "probability": round(probability, 4), "verdict": verdict,
            "model_version": metadata["version"], "threshold": metadata["threshold"],
            "latency_ms": round(elapsed_ms, 2)}

defective = int(np.where((week == 0) & (labels == 1))[0][0])
answer = predict(Part(part_id=f"P-{defective:05d}", features=features[defective].tolist()))
print(answer["part_id"], answer["verdict"], answer["probability"])
```

```
P-00001 defective 1.0
```

**Line by line:**

- `@app.post("/predict")` registers the function for POST requests, the method for sending data (Chapter 34). `part: Part` tells FastAPI to check the request body against the `Part` schema before the function runs.
- `time.perf_counter()` reads a precise clock (Chapter 18); the difference at the end is the time spent, in milliseconds after `* 1000`.
- `np.asarray(part.features, dtype=float)` turns the list into a NumPy array.
- `np.isfinite(values).all()` is True only if every value is an ordinary number. NaN and infinity arrive from real cameras more often than anyone expects, and scikit-learn would pass them straight into the model. `raise HTTPException(status_code=422, ...)` refuses them with a 422 and a reason. The answer is 422, "your input is wrong", not 500, "the server failed", because the fault is in the request, and the caller is the one who must fix it.
- `values.reshape(1, -1)` makes the 108 numbers one row of a table, the shape `predict_proba` expects, and `[0, 1]` takes that row's probability of class 1, defective.
- **The threshold comes from `metadata`**, so the deployed decision boundary is whatever the artifact says it is (section 56.2).
- **The log line is JSON**: `json.dumps(...)` turns a dictionary into one line of JSON text (Chapter 17), with one field per thing monitoring needs: the version, the probability, the verdict, the latency, and a cheap summary of the input (`mean_feature`). Section 56.7 builds the monitors on exactly these fields. Log structured data from day one; nobody ever regrets it.
- The `return` dictionary is the response; FastAPI sends it as JSON.
- The last three lines pick the first defective part in week 0 (`np.where(...)[0][0]` is the position of the first True) and call the function directly, the way the service will. `f"P-{defective:05d}"` writes its position as a five-digit id.

### Running it for real

That is the whole service. `serve.py` holds these definitions, so start it with uvicorn, the way Chapter 34 started its practice server in the background. First save one part as a JSON request body:

```python
with open("part.json", "w") as file:
    json.dump({"part_id": f"P-{defective:05d}", "features": features[defective].tolist()}, file)
print(f"part.json holds part P-{defective:05d}: {os.path.getsize('part.json'):,} bytes")
```

```
part.json holds part P-00001: 2,249 bytes
```

- `json.dump(obj, file)` writes the dictionary to the open file as JSON; `.tolist()` turns the NumPy row into a plain list, which JSON can hold.

Then, in a terminal in the same folder:

```
# terminal, in companion/ch56
$ uvicorn serve:app --port 8056 > uvicorn.log 2>&1 &

$ sleep 4; grep "Uvicorn running" uvicorn.log
INFO:     Uvicorn running on http://127.0.0.1:8056 (Press CTRL+C to quit)

$ curl --silent --write-out "\n" http://127.0.0.1:8056/health
{"status":"ok","model_version":"defect-v1","threshold":0.1}

$ curl --silent --output /dev/null --write-out "%{http_code}\n" -X POST -H "Content-Type: application/json" -d '{"part_id": "P-1", "features": [0.1]}' http://127.0.0.1:8056/predict
422

$ curl --silent http://127.0.0.1:8056/docs | grep -o "<title>.*</title>"
<title>Riverstone defect detector - Swagger UI</title>
```

- `uvicorn serve:app --port 8056` starts the server: `serve:app` means "the object `app` in the file `serve.py`", and `--port 8056` picks a port nothing else uses. `> uvicorn.log 2>&1 &` sends its messages to a file and runs it in the background, as in Chapter 34, section 34.9. `sleep 4` gives it time to load the model.
- `grep "Uvicorn running" uvicorn.log` finds the line that says the server is listening, and where.
- `curl --silent --write-out "\n" http://127.0.0.1:8056/health` sends a GET to the health check. The answer is the same dictionary the notebook printed, now as JSON over HTTP. The JSON arrives without a line break at the end, so `--write-out "\n"` adds one, and the prompt starts on a fresh line.
- The second `curl` sends a POST with a body that breaks the contract, one feature instead of 108. `-X POST` sets the method, `-H "Content-Type: application/json"` says the body is JSON, and `-d '...'` is the body. `--output /dev/null --write-out "%{http_code}\n"` throws the answer's body away and prints only the status code: 422.
- `/docs` is a page FastAPI writes for you. Open `http://127.0.0.1:8056/docs` in a browser and you see every endpoint with its schema, and a "Try it out" button that sends a real request; the `grep -o` here just proves the page is there by printing its title.

Now the real request, the part saved in `part.json`, and the log line it leaves behind:

<!-- run: none -->
```
# terminal, in companion/ch56
$ curl --silent --write-out "\n" -X POST -H "Content-Type: application/json" -d @part.json http://127.0.0.1:8056/predict
{"part_id":"P-00001","probability":1.0,"verdict":"defective","model_version":"defect-v1","threshold":0.1,"latency_ms":10.68}

$ grep defect-service uvicorn.log
2026-09-29 19:23:14,786 INFO defect-service {"part_id": "P-00001", "probability": 1.0, "verdict": "defective", "model_version": "defect-v1", "latency_ms": 10.68, "mean_feature": 0.2738}
```

- `-d @part.json` sends the file's contents as the body; `@` means "read it from this file".
- The answer carries the verdict, the probability, the model version, the threshold, and the time the model took. Your `latency_ms`, and the time at the start of the log line, will differ: they are measured, not computed.
- `grep defect-service uvicorn.log` finds the service's own log line: one JSON record per prediction, exactly what monitoring will read.

When you're done, stop the background server:

```
# terminal, in companion/ch56
$ kill %1
```

`kill %1` stops background job number 1, the server (Chapter 34). In a terminal where the server runs in front, `Ctrl+C` does the same.

### Testing without a server

Starting a server is how the camera will call it. For tests, FastAPI offers a **test client**: the same HTTP calls, made in-process without starting a server, which is how CI tests a service (Chapter 26, section 26.8; Chapter 29, section 29.7):

```python
from fastapi.testclient import TestClient

logging.getLogger("defect-service").setLevel(logging.WARNING)      # quiet the per-request log here
logging.getLogger("httpx2").setLevel(logging.WARNING)               # and the test client's own log
client = TestClient(app)
print(client.get("/health").json())

good = int(np.where((week == 0) & (labels == 0))[0][0])
for name, index in [("a defective part", defective), ("a good part", good)]:
    response = client.post("/predict", json={"part_id": f"P-{index:05d}",
                                             "features": features[index].tolist()})
    body = response.json()
    print(f"{name:<18} -> {body['verdict']:<10} probability {body['probability']:.4f} "
          f"(model {body['model_version']})")

bad = client.post("/predict", json={"part_id": "P-00003", "features": [0.1] * 50})
print(f"a 50-feature request -> HTTP {bad.status_code}: {bad.json()['detail'][0]['msg']}")
```

```
{'status': 'ok', 'model_version': 'defect-v1', 'threshold': 0.1}
a defective part   -> defective  probability 1.0000 (model defect-v1)
a good part        -> good       probability 0.0000 (model defect-v1)
a 50-feature request -> HTTP 422: List should have at least 108 items after validation, not 50
```

- `setLevel(logging.WARNING)` tells a logger to write only warnings and worse. The service's logger and the test client's (`httpx2`) would otherwise each write one line per call to the notebook.
- `TestClient(app)` wraps the app from the cells above; `client.get(...)` and `client.post(..., json=...)` send requests to it, and `.json()` reads the answer.
- `np.where((week == 0) & (labels == 0))[0][0]` is the first good part in week 0.
- `bad.status_code` is the HTTP status, and `bad.json()['detail'][0]['msg']` digs out pydantic's message from FastAPI's error body: a list called `detail`, one entry per problem.

How fast is it? Time 200 requests through the test client and 200 bare calls to the model:

<!-- run: none -->
```python
row = features[defective].reshape(1, -1)
request = {"part_id": "P-00001", "features": features[defective].tolist()}
model_ms, request_ms = [], []
for _ in range(200):
    started = time.perf_counter()
    model.predict_proba(row)
    model_ms.append((time.perf_counter() - started) * 1000)
    started = time.perf_counter()
    client.post("/predict", json=request)
    request_ms.append((time.perf_counter() - started) * 1000)
for name, times in [("model only", model_ms), ("whole request", request_ms)]:
    median, p95 = np.percentile(times, [50, 95])
    print(f"{name:<14} median {median:.2f} ms, 95th percentile {p95:.2f} ms")
```

```
model only     median 0.30 ms, 95th percentile 0.43 ms
whole request  median 3.62 ms, 95th percentile 5.38 ms
```

- `row` is the defective part from earlier as a one-row table, and `request` the same part as a request body, the dictionary that `client.post(..., json=request)` sends.
- Each pass of the loop times one bare `predict_proba` call and one full request through the test `client`, and appends both times, in milliseconds, to the lists `model_ms` and `request_ms`.
- `np.percentile(times, [50, 95])` returns the median and the **95th percentile**, the time that 95% of requests beat. Services are judged on the slow end, not the average, so this is the number a latency target names.

These are timings from the author's machine, and yours will differ; that is why the cell is not part of the book's checked outputs. The useful lesson is the ratio: **the model is a small fraction of the latency**, and most optimization effort in serving goes into everything around it.

---

## 56.6 Deployment patterns

| Pattern | What happens | Buys you | Costs |
|---|---|---|---|
| **Big bang** | replace the old model with the new one | nothing | everything, when it's wrong |
| **Shadow** | the new model scores every request beside the old one; only the old one's answer is used | real production data, zero risk | double compute; no feedback from real decisions |
| **Canary** | 5% of traffic uses the new model, then 25%, then all | limited blast radius, real decisions | needs traffic splitting and per-version metrics |
| **Blue-green** | two complete environments, traffic switched at once, old one kept warm | instant rollback | two environments to pay for |
| **A/B test** | versions compared as an experiment (Chapter 30) | a measured causal answer | needs enough volume and a real metric |

For a defect model on one line, the sequence that works is **shadow, then canary, then keep the previous artifact one click away**. Shadow mode is especially valuable here because the model's ground truth arrives late: run the new version silently for a few weeks, collect its disagreements with the current one, and have the QC inspector adjudicate *only the disagreements*, which is a few dozen parts rather than thousands.

```python
current = joblib.load("models/defect_v1.joblib")["model"]
mould_weeks = np.isin(week, range(16, 20))
candidate = MLPClassifier(hidden_layer_sizes=(48,), max_iter=300, random_state=56).fit(
    np.vstack([X, features[mould_weeks]]), np.concatenate([y, labels[mould_weeks]]))

shadow_weeks = np.isin(week, range(20, 24))
current_says = current.predict_proba(features[shadow_weeks])[:, 1] > 0.1
candidate_says = candidate.predict_proba(features[shadow_weeks])[:, 1] > 0.1
disagreements = current_says != candidate_says
truth = labels[shadow_weeks]

print(f"parts scored in shadow: {shadow_weeks.sum():,}")
print(f"the two models disagree on {disagreements.sum()} of them ({disagreements.mean():.1%})")
print(f"of those disagreements, the candidate is right {int((candidate_says == truth)[disagreements].sum())} times "
      f"and the current model is right {int((current_says == truth)[disagreements].sum())} times")
```

```
parts scored in shadow: 2,000
the two models disagree on 46 of them (2.3%)
of those disagreements, the candidate is right 30 times and the current model is right 16 times
```

**Line by line:**

- `mould_weeks = np.isin(week, range(16, 20))` is True for every part from weeks 16 to 19, the first four weeks of the new mould.
- The candidate is Chapter 53's network, `MLPClassifier(hidden_layer_sizes=(48,), max_iter=300, ...)`, the same 48 neurons and 300 epochs, trained again on all 6,000 of Chapter 53's parts (`X`, `y`) plus those four weeks. `np.vstack` stacks two tables one above the other, and `np.concatenate` joins two label arrays end to end. `random_state=56` fixes its starting weights, so your candidate is the book's.
- `shadow_weeks` are the four weeks after that, 20 to 23, which the candidate has never seen: 2,000 parts.
- `current_says` and `candidate_says` are each model's yes/no at the threshold 0.1. `current_says != candidate_says` is True where they disagree.
- `(candidate_says == truth)[disagreements].sum()` counts, among the disagreements only, the parts where the candidate matched the truth.

The interesting quantity is not either model's accuracy, it is **where they disagree**, because that is the only set a human needs to look at. In production, those part ids go to the inspector, and their verdicts become both the decision and next month's training data. Counted as verdicts, the candidate looks like a clear winner. But a verdict is not a rupee: split the disagreements by the kind of mistake each model avoided, and price them.

```python
cells = {
    "candidate caught a defect the current model missed": disagreements & candidate_says & (truth == 1),
    "current model caught a defect the candidate missed": disagreements & current_says & (truth == 1),
    "candidate raised a false alarm": disagreements & candidate_says & (truth == 0),
    "current model raised a false alarm": disagreements & current_says & (truth == 0),
}
for name, cell in cells.items():
    print(f"{name:<52} {cell.sum():>3}")

counts = [int(cell.sum()) for cell in cells.values()]
saving = (counts[0] - counts[1]) * 4000 - (counts[2] - counts[3]) * 40
print(f"\nthe candidate is worth {saving:,} rupees more than the current model over these four weeks")
```

```
candidate caught a defect the current model missed    10
current model caught a defect the candidate missed     4
candidate raised a false alarm                        12
current model raised a false alarm                    20

the candidate is worth 24,320 rupees more than the current model over these four weeks
```

- Each entry of `cells` combines three True/False arrays with `&`, "and": a disagreement, where a given model said "defective", and where the truth was defective (`truth == 1`) or good (`truth == 0`).
- `counts` holds the four totals in the dictionary's order. A caught defect is worth ₹4,000 and a false alarm costs ₹40, so the saving is the extra defects caught times ₹4,000, minus the extra false alarms times ₹40.

**Read the two tables together.** Counted as verdicts, the candidate wins 30 to 16, which looks decisive. But most of those wins are false alarms the current model raised and the candidate didn't (20 against 12), and each of those is worth ₹40. The money is in the first two rows: the candidate caught 10 defects the current model missed and missed 4 that it caught, a net 6 defects, ₹24,000 of the ₹24,320. A tally treats a caught defect and an avoided false alarm as equal, when one is worth a hundred times the other; with the false alarms the other way round, the same tally could have backed the wrong model. **Shadow disagreements are adjudicated and costed, not counted.** Four weeks of shadow traffic, 2,000 parts, have told Riverstone that the candidate is better where it matters, which is exactly what shadow mode is for, and exactly what a headline accuracy comparison (section 56.9) would blur.

---

## 56.7 Monitoring, in three layers

| Layer | Question | Signal | Delay |
|---|---|---|---|
| **Service** | is it up and fast? | uptime, error rate, latency percentiles, memory | seconds |
| **Input** | does the data look like the training data? | feature distributions, missing rates, ranges, drift statistics | minutes |
| **Output and outcome** | is it still right? | a fast proxy, the prediction distribution; and the slow truth, accuracy once labels arrive | hours to weeks |

![Three layers of monitoring, service, input, and output and outcome, the third split into a fast proxy stream and a slow truth stream, each with its question, signal, delay and the action it triggers](figures/fig56-2-monitoring-layers.svg)

*Figure 56.2 — Each layer sees a different failure, and only the slow stream of the third layer measures correctness.*

The first layer is ordinary software monitoring. The second is section 56.8. The third has a property that makes it hard and that most ML monitoring articles skate over: **ground truth is late.** A part flagged defective is checked within the hour, but a part passed as good is only revealed as wrong when a customer complains, weeks later. So the third layer has two streams:

- **Fast proxy**: the share of parts predicted defective, per shift. It needs no labels, and a sudden move in it is always worth a look.
- **Slow truth**: a sampled audit. Riverstone re-inspects 2% of passed parts, which is the only way a missed-defect rate is ever measured.

Here is the fast proxy week by week, beside a number production never has on the day: the true defect rate, which this simulation knows only because it drew every part.

```python
print(f"{'week':>5}{'parts':>7}{'predicted defective':>21}{'true defect rate':>18}")
for w in (0, 7, 12, 16, 20, 23):
    rows = week == w
    predicted = (model.predict_proba(features[rows])[:, 1] > 0.1).mean()
    print(f"{w:>5}{rows.sum():>7}{predicted:>20.1%}{labels[rows].mean():>17.1%}")
```

```
 week  parts  predicted defective  true defect rate
    0    500                7.8%             8.0%
    7    500                8.4%             7.2%
   12    500                7.8%             7.2%
   16    500                9.6%             9.2%
   20    500               12.6%            11.8%
   23    500                8.2%             9.0%
```

- `rows = week == w` is True for the 500 parts of week `w`.
- `(... > 0.1).mean()` is the share of those parts the model flags: the mean of True/False values is the share of Trues. `labels[rows].mean()` is the share that really were defective.
- `:>20.1%` prints a share as a percentage with one decimal, right-aligned in 20 characters.

**Read the two columns together.** They track each other closely in every week, before and after the new mould. That looks reassuring, and it is the trap. From week 16 the model misses flash parts, but it also raises a few more false alarms, and a count of parts flagged adds the two together, so the misses disappear into the total. A model that catches everything and a model that misses the new defect while flagging some good parts can show the same predicted-defective rate. **The fast proxy measures change, not correctness.** It would shout if the camera died and flagged nothing, or flagged everything; it cannot see a model quietly missing one kind of defect. And in production you would not have the right-hand column at all: only the audit of passed parts estimates it, a week or more late.

> **Watch out: alert on what you will act on.** A dashboard nobody looks at is not monitoring, and an alert that fires weekly gets muted in a fortnight. Riverstone's rule: page a human only for the service layer (down, or error rate above 1%); everything else is a daily digest with a named owner. Chapter 47's data-quality alerting makes the same argument for pipelines.

---

## 56.8 Drift, measured

Two standard statistics, each worked out in NumPy before reaching for a library.

**Population stability index (PSI)** compares a recent sample with a reference sample, bucket by bucket:

```python
from scipy import stats

def psi(reference, recent, buckets=10):
    """How far has this distribution moved? Rules of thumb: <0.1 stable, 0.1-0.25 watch, >0.25 investigate."""
    cuts = np.quantile(reference, np.linspace(0, 1, buckets + 1))
    cuts[0], cuts[-1] = -np.inf, np.inf
    reference_share = np.clip(np.histogram(reference, cuts)[0] / len(reference), 1e-4, None)
    recent_share = np.clip(np.histogram(recent, cuts)[0] / len(recent), 1e-4, None)
    return float(((recent_share - reference_share) * np.log(recent_share / reference_share)).sum())

baseline = brightness[week < 8]
print(f"{'week':>5}{'PSI':>9}{'KS':>8}   verdict")
for w in (3, 8, 10, 13, 16, 20, 23):
    recent = brightness[week == w]
    value = psi(baseline, recent)
    ks = stats.ks_2samp(baseline, recent).statistic
    verdict = "stable" if value < 0.1 else "watch" if value < 0.25 else "investigate"
    print(f"{w:>5}{value:>9.3f}{ks:>8.3f}   {verdict}")
```

```
 week      PSI      KS   verdict
    3    0.007   0.042   stable
    8    0.065   0.116   stable
   10    0.614   0.270   investigate
   13    2.959   0.562   investigate
   16    4.107   0.689   investigate
   20    3.981   0.704   investigate
   23    4.246   0.680   investigate
```

**Line by line:**

- `np.linspace(0, 1, buckets + 1)` makes 11 evenly spaced numbers from 0 to 1 (0, 0.1, … 1), and `np.quantile(reference, ...)` turns them into the 11 cut points that split the *reference* period into ten equal-sized buckets. Using the reference's own quantiles is the point: the buckets are defined by the world the model was trained on.
- `cuts[0], cuts[-1] = -np.inf, np.inf` opens the ends, so a value beyond anything seen before still lands somewhere.
- `np.histogram(values, cuts)` returns two arrays, the counts in each bucket and the bucket edges; `[0]` keeps the counts, and dividing by the sample size turns them into shares.
- `np.clip(..., 1e-4, None)` raises any share below 0.0001 to 0.0001, so an empty bucket can't cause a division by zero or an infinite logarithm. It is the standard fudge, and worth knowing about.
- The sum is over buckets of *(recent share − reference share) × log(recent share / reference share)* (Chapter 31's natural logarithm): zero when the distributions match, growing as they separate.
- `baseline` is the brightness of every part from the eight stable weeks, 0 to 7: the reference.
- **The KS statistic** (`stats.ks_2samp`, from SciPy, Chapter 21) is the Kolmogorov-Smirnov statistic, worked by hand next. It needs no buckets, which makes it a good cross-check.
- `"stable" if ... else "watch" if ... else "investigate"` chains two conditional expressions to pick one of three words.

| Setting | What it means in plain words | Value used here | What happens if you change it |
|---|---|---|---|
| `buckets` | how many slices the reference is cut into | 10 | more buckets see finer changes but get noisy with 500 parts a week; fewer miss changes in the tails |
| clip floor | the smallest share a bucket may have | 0.0001 | a bigger floor damps the effect of empty buckets, and makes PSI smaller for big shifts |
| reference period | the weeks that define "normal" | weeks 0 to 7 | a reference from a different season makes every week look drifted |
| alert threshold | the PSI that raises the alarm | 0.1 and 0.25 | set it below your noise floor and it fires every week (see calibration below) |

### The KS statistic by hand

A **cumulative distribution** says, for any value, what share of a sample is at or below it. For the five values 2, 3, 3, 5 and 8 it is 0.2 at 2, 0.6 at 3 (three of the five), 0.8 at 5, and 1.0 at 8. The **KS statistic** lines up two samples' cumulative distributions and reports the largest vertical gap between them: 0 means identical, 1 means no overlap at all.

```python
def ks_by_hand(a, b):
    grid = np.sort(np.concatenate([a, b]))
    share_a = np.searchsorted(np.sort(a), grid, side="right") / len(a)
    share_b = np.searchsorted(np.sort(b), grid, side="right") / len(b)
    return float(np.abs(share_a - share_b).max())

week10 = brightness[week == 10]
print(f"by hand {ks_by_hand(baseline, week10):.3f}, SciPy {stats.ks_2samp(baseline, week10).statistic:.3f}")
```

```
by hand 0.270, SciPy 0.270
```

- `grid` is every value from both samples, sorted: the places where either cumulative distribution can step up.
- `np.searchsorted(np.sort(a), grid, side="right")` counts, for each grid value, how many values of `a` are at or below it; dividing by `len(a)` makes that a share. The same for `b`.
- `np.abs(share_a - share_b).max()` is the largest gap, and it matches SciPy's.

**Calibrating the thresholds.** The thresholds 0.1 and 0.25 are conventions from credit scoring, not laws. Calibrate them on your own stable period, and never compare a week against a reference that contains it: the week's own parts pull the reference towards it, and its PSI comes out too small. Hold two stable weeks out of the reference:

```python
reference = brightness[week < 6]
for w in (6, 7):
    print(f"week {w} against weeks 0-5: PSI {psi(reference, brightness[week == w]):.3f}")
```

```
week 6 against weeks 0-5: PSI 0.006
week 7 against weeks 0-5: PSI 0.013
```

The two held-out stable weeks score 0.006 and 0.013: that is Riverstone's noise floor for brightness, with 500 parts a week. The conventional 0.1 sits several times above it, clear of ordinary wobble, so here the textbook threshold happens to be reasonable. On another line, with fewer parts a week or a noisier sensor, the floor could be ten times higher, and 0.1 would fire every week. Exercise 4 measures how much a reference that contains the week understates its PSI.

### The finding that matters

Now put drift next to the thing everyone assumes it predicts:

```python
print(f"{'week':>5}{'PSI':>8}{'recall':>9}{'false alarms':>14}   what is happening")
notes = {0: "baseline", 7: "baseline", 9: "new lamps, week 2", 13: "new lamps, week 6",
         15: "new lamps, week 8", 17: "new mould, week 2", 20: "new mould, week 5", 23: "new mould, week 8"}
for w in (0, 7, 9, 13, 15, 17, 20, 23):
    rows = week == w
    predicted = model.predict_proba(features[rows])[:, 1] > 0.1
    tn, fp, fn, tp = confusion_matrix(labels[rows], predicted, labels=[0, 1]).ravel()
    print(f"{w:>5}{psi(baseline, brightness[rows]):>8.2f}{tp / (tp + fn):>9.2f}{fp:>14}   {notes[w]}")
```

```
 week     PSI   recall  false alarms   what is happening
    0    0.02     0.97             0   baseline
    7    0.01     1.00             6   baseline
    9    0.33     0.97             3   new lamps, week 2
   13    2.96     0.93             9   new lamps, week 6
   15    4.41     0.98             6   new lamps, week 8
   17    4.14     0.81             7   new mould, week 2
   20    3.98     0.86            12   new mould, week 5
   23    4.25     0.87             2   new mould, week 8
```

- `notes` is a dictionary from week number to a label for the last column.
- `confusion_matrix(..., labels=[0, 1])` names both classes explicitly. Without it, a week in which the model flagged nothing and no part was defective would produce a 1 × 1 matrix, and `.ravel()` could not unpack four numbers.
- Each row prints the week's PSI against the baseline, its recall (the share of real defects caught), and its false alarms.

![Two stacked charts over 24 weeks: PSI rises past 4 after the lamps change while recall stays high, then PSI is flat while recall falls about 17 points after the new mould](figures/fig56-1-drift-vs-decay.svg)

*Figure 56.3 — The drift alarm fired when nothing was wrong, and stayed silent when something was.*

**The table above the figure is the most useful thing in the chapter, and it says the opposite of the standard advice.**

Pool the weeks into the three periods to see it without the weekly noise:

```python
flagged = model.predict_proba(features)[:, 1] > 0.1
for label, weeks in [("weeks 0-7, baseline", range(0, 8)), ("weeks 8-15, new lamps", range(8, 16)),
                     ("weeks 16-23, new mould", range(16, 24))]:
    defects = np.isin(week, weeks) & (labels == 1)
    print(f"{label:<23} caught {flagged[defects].sum()} of {defects.sum()} defects ({flagged[defects].mean():.1%})")
print(f"flash parts caught: {flagged[kind == 'flash'].sum()} of {(kind == 'flash').sum()}")
```

```
weeks 0-7, baseline     caught 301 of 311 defects (96.8%)
weeks 8-15, new lamps   caught 332 of 344 defects (96.5%)
weeks 16-23, new mould  caught 336 of 398 defects (84.4%)
flash parts caught: 18 of 69
```

- `flagged` is the model's yes/no for all 12,000 parts at once.
- `defects` is True for the defective parts of one period, so `flagged[defects]` is the model's verdict on each of them: `.sum()` counts the catches and `.mean()` is the period's recall.

- **Weeks 8 to 15: the drift alarm screams and the model is fine.** PSI reaches 4.4, seventeen times the "investigate" threshold, while weekly recall stays between 0.93 and 1.00, the same range as the stable weeks, and over the eight lamp weeks the model catches as large a share of defects as in the eight weeks before. The inputs changed enormously; the features the model relies on did not change in a way that mattered.
- **Weeks 16 to 23: the model breaks and the drift alarm says nothing new.** Recall falls by about 12 points, from about 97% to 84%, and the model catches only about a quarter of the flash parts. PSI is flat, because the incoming images look exactly like last month's. The failure is in the *relationship* between input and label, and no amount of input monitoring can see it.

The conclusion is not that drift statistics are useless: they are cheap, immediate, and they told the truth both times (the inputs *had* changed; then they *hadn't*). The conclusion is that **input drift is not model decay**. With the model trained on 2 March 2026 and week 0 starting then, week 8 is late April and week 16 late June: a monitoring plan built only on drift pages you for the wrong thing in late April and stays silent in late June. You need both layers, and you need the sampled labels.

---

## 56.9 Retraining

**Triggers**, in the order teams should adopt them:

| Trigger | When it fires | Comment |
|---|---|---|
| **Scheduled** | monthly, quarterly | the simplest thing that works, and the right default |
| **Performance** | measured accuracy falls below a floor | needs labels, so it fires late |
| **Drift** | PSI above a threshold for *n* consecutive days | fires early, and sometimes for nothing (see above) |
| **Event** | a known change: new mould, new camera, new product | the best trigger there is, and it comes from the business, not a monitor |
| **Data volume** | *n* new labeled examples available | good where labels accumulate naturally |

Riverstone's rule, written down: **retrain monthly, and immediately on any event the plant tells us about.** The new mould in week 16 is exactly such an event, and the retraining that follows should have been triggered by the production meeting, not by the model's recall falling.

The candidate from section 56.6 is that retrain. Score both models on the recent weeks and, as a regression check, on the old ones, with the cost beside each:

```python
def score(candidate_model, weeks, threshold=0.1):
    rows = np.isin(week, weeks)
    predicted = candidate_model.predict_proba(features[rows])[:, 1] > threshold
    tn, fp, fn, tp = confusion_matrix(labels[rows], predicted, labels=[0, 1]).ravel()
    return tp / (tp + fn), fp, fn * 4000 + fp * 40

for name, candidate_model in [("current (defect-v1)", model), ("retrained (defect-v2)", candidate)]:
    print(name)
    for label, weeks in [("recent weeks 20-23", range(20, 24)), ("old weeks 0-7", range(0, 8))]:
        recall, alarms, cost = score(candidate_model, weeks)
        print(f"  {label:<19} recall {recall:.2f}, false alarms {alarms:>3}, cost {cost:>7,} rupees")
```

```
current (defect-v1)
  recent weeks 20-23  recall 0.88, false alarms  28, cost 101,120 rupees
  old weeks 0-7       recall 0.97, false alarms  34, cost  41,360 rupees
retrained (defect-v2)
  recent weeks 20-23  recall 0.91, false alarms  20, cost  76,800 rupees
  old weeks 0-7       recall 0.99, false alarms  30, cost  17,200 rupees
```

- `score` returns three things for the chosen weeks: recall, the false alarms, and the cost at ₹4,000 a miss and ₹40 a false alarm.
- The loop prints each model on two lines: the recent weeks it must now handle, and the old weeks it must not have forgotten, the **regression check**.

**Read it as the shipping decision it is.** On the recent weeks the retrain catches more defects (recall 0.88 to 0.91), because it has now seen the flash defect, and raises fewer false alarms (28 to 20): the cost of those four weeks falls from ₹1,01,120 to ₹76,800, the ₹24,320 that shadow mode found. The regression check matters as much: on the old weeks it has not forgotten the original defects (recall 0.97 to 0.99, false alarms 34 to 30). Here the retrain is better on every line. That does not always happen: a retrain that gains on the new weeks and loses on the old ones is common, and only the second line of each pair would show it.

The threshold that suited `defect-v1` need not suit `defect-v2`, so **re-tuning the threshold is part of retraining**, not an afterthought. Sweep it on the retrained model's out-of-fold predictions, the way Chapter 53 chose the first one (section 53.6), so the weeks used to judge it stay unseen:

```python
from sklearn.model_selection import StratifiedKFold, cross_val_predict

X_v2 = np.vstack([X, features[mould_weeks]])
y_v2 = np.concatenate([y, labels[mould_weeks]])
folds = StratifiedKFold(n_splits=5, shuffle=True, random_state=56)
out_of_fold = cross_val_predict(MLPClassifier(hidden_layer_sizes=(48,), max_iter=300, random_state=56),
                                X_v2, y_v2, cv=folds, method="predict_proba")[:, 1]

print(f"{'threshold':>9}{'missed':>8}{'false alarms':>14}{'cost (Rs)':>11}")
sweep = []
for threshold in (0.5, 0.3, 0.1, 0.05, 0.02, 0.01):
    tn, fp, fn, tp = confusion_matrix(y_v2, out_of_fold > threshold).ravel()
    sweep.append((fn * 4000 + fp * 40, threshold))
    print(f"{threshold:>9}{fn:>8}{fp:>14}{fn * 4000 + fp * 40:>11,}")
print(f"\ncheapest threshold for defect-v2: {min(sweep)[1]}")
```

```
threshold  missed  false alarms  cost (Rs)
      0.5      56             6    224,240
      0.3      45            11    180,440
      0.1      36            34    145,360
     0.05      30            67    122,680
     0.02      22           150     94,000
     0.01      19           270     86,800

cheapest threshold for defect-v2: 0.01
```

- `X_v2` and `y_v2` are the retrain's training data, the same rows `candidate` learned from: `np.vstack` and `np.concatenate` join Chapter 53's parts and the four mould weeks, as in section 56.6.
- `StratifiedKFold(n_splits=5, shuffle=True, random_state=56)` cuts them into five shuffled folds with the same defect rate (Chapter 36), and the network is the candidate's, `hidden_layer_sizes=(48,)` and `max_iter=300`.
- `cross_val_predict(..., cv=folds, method="predict_proba")` is Chapter 53's tool: five models, each predicting the fold it didn't train on, so every training part gets an honest probability. It takes about a minute.
- Each threshold is priced, and `min(sweep)` picks the cheapest (cost, threshold) pair, as in Chapter 53.

On the retrain's own out-of-fold predictions, over its 8,000 training parts, the cheapest threshold is 0.01, the point Chapter 53 found for the first model, and the gap has widened. At 0.1 the retrain misses 36 defects and costs ₹1,45,360; at 0.01 it misses 19 and costs ₹86,800, but sends 270 good parts for re-inspection instead of 34, about eight times the inspector's workload. That is the plant manager's decision again, now with the flash defect in the numbers, and it is why **re-tuning is part of the release**: the retrain ships with whichever threshold is agreed, written into its metadata, never with the old number by default. A retrain that ships with the old threshold is a common and avoidable way to leave money on the table.

**The guardrails on any automated retrain:**

- **A held-out set the retrain never sees**, including old data, so forgetting is caught.
- **A floor**: the new model must beat the old one on the business metric, or it does not ship.
- **A regression check** on the original data, as above.
- **A human approval** for the first several retrains, until the process has earned trust.
- **The previous artifact retained**, and a rollback you have actually practiced.

> **Watch out: retraining on the model's own output is how a model eats itself.** If the training labels come from parts the model flagged, it only ever learns about defects it already catches, and its blind spots become permanent. Riverstone's 2% audit of *passed* parts exists exactly to break that loop, and it is the single most valuable data collection in the whole system.

---

## 56.10 When it goes wrong

**The runbook**, which should be one page pinned next to the dashboard:

| Step | Action |
|---|---|
| 1. Confirm | Is it the model, the data, or the service? Check the three layers in order |
| 2. Contain | Roll back to the previous model version, or switch the line to manual inspection |
| 3. Communicate | Tell the plant and QC what is happening and what they should do meanwhile |
| 4. Diagnose | Logs first: model version, input summaries, prediction distribution, per-shift metrics |
| 5. Fix | The smallest change that restores service. Retraining is rarely the fastest fix |
| 6. Learn | Post-mortem, blameless, with an action that would have caught it sooner |

**Rollback is the step people skip practising.** With the artifact-plus-metadata packaging of section 56.4, it is a file swap and a restart (or moving the registry's `production` alias back), and the threshold comes back with it. Time it once, on a quiet afternoon, and write the number in the runbook: *"rollback takes four minutes"* is a sentence that changes how a plant manager feels about the whole project.

**The post-mortem** that matters is not "the model degraded". It is the sentence that starts *"we would have caught this sooner if…"*, and its answer becomes the next monitor. For the flash defect, that sentence is: *"if the production meeting's note about the new mould had reached the ML on-call rota."* The fix is a process change, not a model change, and it is typical.

---

## 56.11 How far up the ladder to climb

| Level | What it looks like | Who should be here |
|---|---|---|
| **0. Notebook** | a model in someone's notebook, run by hand | proofs of concept only |
| **1. Reproducible** | training is a script in Git, artifacts versioned with metadata, runs tracked | **every company with one model in production** |
| **2. Served and monitored** | an endpoint or a scheduled batch, three-layer monitoring, a runbook, practiced rollback | **Riverstone, and most mid-sized companies** |
| **3. Automated pipelines** | CI/CD for models, automated retraining with guardrails, a registry with aliases | companies with several models and a team to run them |
| **4. Platform** | feature store, shared serving infrastructure, self-serve deployment, lineage across dozens of models | large organizations with many teams |

**Most companies should stop at level 2, and most articles are written from level 4.** A **feature store** (a shared service that computes each feature once and serves the same values to training and to production, so a feature can never be computed one way for training and another way in the service, the bug called **training-serving skew**) is excellent when twenty models share features and terrible when one model has 108 of them. Kubernetes is excellent at scale and an enormous tax on one service serving one camera. The honest question is: *what would break if we did this by hand once a month?* If the answer is "nothing", do it by hand and spend the time on the audit sample instead.

What does not scale down, and is worth doing at every level: **version the artifact with its metadata, track the runs, log structured predictions, monitor in three layers, and be able to roll back.** None of that needs a platform. All of it can be done in a week.

### Optional: `serve.py` in a container (Chapter 52)

Read this, or build it if you have Docker running. It is Chapter 52's Dockerfile pattern (section 52.2) with this chapter's service inside:

```dockerfile
FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY serve.py .
COPY models/ models/
CMD ["uvicorn", "serve:app", "--host", "0.0.0.0", "--port", "8056"]
```

- `FROM` starts from a small official Python image, and `WORKDIR /app` is the folder inside the container.
- `requirements.txt` is copied and installed **before** the code, so changing `serve.py` doesn't reinstall the packages (Chapter 52's layer caching).
- The service and its `models` folder come next, so the image carries the model **and** its metadata.
- `CMD` starts uvicorn. `--host 0.0.0.0` listens on every address, because requests arrive from outside the container, not from `127.0.0.1` inside it.
- In Kubernetes, the `/health` endpoint is what the `readinessProbe` of Chapter 52, section 52.3, would call before sending the pod any parts.

---

## Common mistakes

| Mistake | Symptom | Fix |
|---|---|---|
| The threshold lives in the service, the model in a registry | A rollback restores the model and not the decision boundary | Threshold in the artifact metadata |
| No data version recorded | "Which data was this trained on?" has no answer | A hash or a pinned snapshot in the metadata |
| Metrics tracked in a spreadsheet | Twelve runs nobody can compare | An experiment tracker, even a local SQLite one |
| Only statistical metrics logged | The best run by F1 is the worst by cost | Log the business metric and sort by it |
| Health check returns "ok" only | Passes while the wrong model is loaded | Return the model version too |
| Unvalidated inputs | A wrong prediction on garbage instead of a clear 422 | A schema on the request, and a finite check |
| Unstructured logs | Monitoring you cannot build | One JSON line per prediction, with version, probability, latency, input summary |
| Drift monitoring alone | Pages you for harmless input changes, silent when the model actually breaks | Three layers, including sampled ground truth |
| Treating PSI thresholds as laws | Alert fatigue within a month | Calibrate on your own stable period, with weeks held out of the reference |
| Counting shadow disagreements instead of pricing them | A clearly better model looks like a coin flip | Split the disagreements by kind of error and cost each |
| No sampled audit of passed items | Missed defects are invisible until a customer finds them | A fixed percentage of passed parts re-checked |
| Retraining on the model's own flags | Blind spots become permanent | Audit sample of passed parts feeds training |
| Shipping a retrain with the old threshold | Recall up, cost up, nobody understands why | Re-tune the threshold as part of retraining |
| No held-out regression check | The new model forgets the old defects | Evaluate on old data as well as recent |
| Rollback never practiced | A four-minute fix takes two hours during an incident | Time it on a quiet afternoon; write the number down |
| Building a platform for one model | Six months of infrastructure, one endpoint | Level 2 is the right destination for most companies |

---

## In the real world: the fortnight the line got worse and nobody knew

Riverstone's defect camera runs quietly from March. In August, a customer returns a pallet of lids with a thin tail of plastic along one edge: flash, from the new mould that started in week 16 of the log.

The post-mortem is uncomfortable, because every individual decision was defensible.

- **The drift monitor had been amber since late April**, when the plant replaced the overhead lamps. PSI went from about 0.01 to over 4, the daily digest said "investigate" for eight weeks before the mould arrived, and it never went green again. The model was fine the whole time. By June, everyone had learned that the drift alert meant nothing.
- **When the new mould arrived in late June, the drift number did not move**, because the pictures looked the same. The alert that had been crying wolf stayed silent for the real event.
- **Recall fell from about 0.97 to 0.84** and nobody could see it, because nobody was checking parts the model had passed: the camera caught about a quarter of the flash parts.
- **The production meeting knew about the new mould on the day it was installed.** That note never reached the person running the model.

The fixes are all cheap, and none of them is a better model:

1. **A 2% audit of passed parts**, which makes recall measurable within a week instead of a customer complaint.
2. **The predicted-defective rate per shift on the same chart as the audit's missed-defect rate.** On its own the predicted rate barely moved; beside the audit, a steady line of predictions and a rising line of misses is hard to ignore.
3. **The event trigger**: the production meeting's change log now goes to whoever owns the model, and any new mould, resin, or camera triggers a review.
4. **Drift thresholds recalibrated** on Riverstone's own stable period, so amber means something.
5. **A retrain including flash examples**, shipped after shadow mode, with the threshold re-tuned and the old artifact kept one click away.

**What Meera writes in the post-mortem:** *"The model didn't fail; our monitoring measured the wrong thing. Input drift told us the lamps changed, which didn't matter, and told us nothing when the parts changed, which did. We are adding a 2% audit of passed parts and a line in the production meeting's checklist. The model change is the smallest part of this fix."*

The pattern is worth carrying into any ML project: **the failures are rarely in the model, and the fixes are rarely modeling.**

---

## Project: run a model for six months in an afternoon

**Goal:** take a model you have trained and put it through a full production lifecycle, with every decision written down.

### Tools you'll need

Versions used, checked in September 2026:

- **Python** in the book's virtual environment (Chapter 17), with **NumPy**, **SciPy**, **scikit-learn 1.9.1** and **joblib**, all installed already.
- **FastAPI 0.141.1** and **uvicorn 0.54.0** for serving, and **httpx2 2.13.1**, which FastAPI's `TestClient` needs for testing the service in CI (older guides name `httpx`, which still works with a deprecation warning). Installed in section 56.0.
- **MLflow 3.16.1** for tracking and the model registry, with a local SQLite backend. In MLflow 3.16 the plain-folder store (`./mlruns` as the tracking store) is in maintenance mode and refuses to start unless you opt in, and scikit-learn models are saved with `skops`, which needs unfamiliar types declared as trusted. Registry **stages** are deprecated in favour of **aliases** (since MLflow 2.9).
- **Alternatives worth knowing:** Weights & Biases (tracking), DVC (data versioning), BentoML and Seldon (serving), Evidently and NannyML (drift and performance monitoring), SageMaker / Vertex AI / Azure ML (managed end to end), Airflow or Dagster for the scheduled parts (Chapter 46).
- **Containers and orchestration** (Docker, Kubernetes, Chapter 52) are how this runs at scale. They change the packaging and deployment steps, not the discipline; section 56.11 shows the Dockerfile.
- **Companion files** in `companion/ch56/`: `simulate_production.py` (the 24-week stream, seed 56), `train.py` (section 56.3's four tracked runs, as a script), `serve.py` (the FastAPI service), and `ci_model_check.py` (exercise 9). The notebook writes `models/defect_v1.joblib`, `mlflow.db` and the `mlruns` folder as you go.

> **Simplification note.** This is a one-machine simulation of production: no cloud, no container, no real traffic, and a "line" that is a NumPy array. The code, the metrics, and the failures are real; the scale is not. What changes at real scale: the serving layer gets containers and a load balancer, the store gets a database server, monitoring gets a time-series system, and the audit sample gets a workflow tool. What does not change: any of section 56.11's level-2 practices.

**Option A: your own model.** Any model you built in Chapters 35 to 53, with a stream of data you can replay in time order.

**Option B: Riverstone.** Use this chapter's stream.

**Steps:**

1. **Package it** with metadata: version, data hash, training rows, library versions, threshold, metrics.
2. **Track three training runs** and record the business metric alongside the statistical ones. Sort by the business metric, and register the one you ship.
3. **Serve it** behind an endpoint with input validation, a health check that returns the version, and one structured log line per prediction.
4. **Write the three-layer monitoring plan** before you look at any results: what you measure, how often, who is told, and what they do.
5. **Replay the stream week by week**, computing your monitors as you go. Record when each one first fires.
6. **Find the two events** in the data. Which monitor caught which, and how late?
7. **Retrain**, with a held-out regression check, and re-tune the threshold. Decide, in writing, whether it ships.
8. **Practise the rollback** and time it.
9. **Write the post-mortem** for the failure you found, including the sentence "we would have caught this sooner if…".

**Deliverables:** the packaged artifact, the tracked runs, the service, the monitoring plan, the week-by-week table, the retraining decision, and the post-mortem.

**Stretch goals:**

- Add shadow mode, and price the disagreements rather than counting them.
- Add a scheduled batch scorer alongside the endpoint, and compare cost per thousand predictions.
- Compute drift per feature rather than on one summary, and see which features move.
- Add a CI job (Chapter 26, section 26.8) that fails if the packaged model's metrics fall below the floor (exercise 9).
- Estimate what this would cost per month on a cloud provider, at 5,000 parts a day.

---

## Recap

- **MLOps** is the practice of keeping models working, and right, in production. A model in production fails in four ways: **the world moves, nobody notices, nobody can reproduce it, nobody can roll it back.**
- **"The model" is five things**: data, features, code, artifact, and config. A **registry** keeps numbered versions and an **alias** for the one in use; the **threshold belongs in the metadata**.
- **Track experiments** with parameters, metrics, and the artifact, and log the **business metric**: sorting by cost put a different run first than sorting by precision.
- **Package** the model with metadata that answers "what is this and what was it trained on?". Treat artifacts as executables: pickles run code.
- **Serve** batch, online, or streaming. Validate inputs with a schema, return the model version from `/health`, and log one structured line per prediction. The model is a small fraction of each request's time.
- **Deploy** with shadow and canary, and keep the old artifact one click away. By count, Riverstone's candidate won its shadow disagreements 30 to 16; priced, it was worth ₹24,320 more over four weeks, almost all of it from 6 more defects caught. **Price disagreements; don't count them.**
- **Monitor in three layers.** Ground truth is late, so pair a **fast proxy** (predicted-defective rate) with **slow truth** (a 2% audit of passed parts); only the slow truth measures correctness.
- **PSI and KS** measure input drift cheaply. In Riverstone's data, PSI hit 4.4 while recall held at 97%, then stayed flat while recall fell about 12 points. **Input drift is not model decay.**
- **Retrain** on a schedule and on events, with a held-out regression check, a business-metric floor, and a **re-tuned threshold**. Never train only on the model's own flags.
- **Practise the rollback**, write the runbook, and make the post-mortem produce a monitor.
- **Most companies should stop at level 2** of the maturity ladder and spend the saved effort on the audit sample.

---

## Key terms

MLOps · model lifecycle · data versioning · feature versioning · model artifact · model registry · model version · alias · stage (deprecated) · experiment tracking · tracking store · run · parameter · metric · business metric · packaging · metadata · data hash · pickle risk · trusted types · batch serving · online serving · streaming serving · endpoint · schema · input contract · HTTP 422 · input validation · health check · liveness · readiness · structured logging · test client · 95th percentile · big bang deployment · shadow mode · canary release · blue-green deployment · rollback · three-layer monitoring · service metrics · input monitoring · outcome monitoring · ground-truth delay · fast proxy metric · sampled audit · data drift · concept drift · population stability index · cumulative distribution · Kolmogorov-Smirnov statistic · alert fatigue · retraining trigger · regression check · threshold re-tuning · feedback loop · runbook · incident · post-mortem · MLOps maturity ladder · feature store · training-serving skew

*(All terms are defined in the Glossary, Appendix A.)*

---

## Check yourself

- [ ] I can name the five things that must be versioned, and I version all of them.
- [ ] My models are packaged with metadata, including the threshold.
- [ ] I track experiments, and I log the business metric alongside the statistical ones.
- [ ] I can register a model version and point an alias at it.
- [ ] My service validates inputs, returns its model version, and logs structured predictions.
- [ ] I can start the service, call it with `curl`, and test it without a server.
- [ ] I can choose between batch, online, shadow, canary, and blue-green, for a reason.
- [ ] I monitor in three layers and know which layer catches which failure.
- [ ] I can compute PSI and the KS statistic by hand, and I calibrate thresholds on my own data.
- [ ] I know that input drift is not model decay, and I have a sampled ground-truth stream.
- [ ] I have a retraining trigger written down, with guardrails and a regression check.
- [ ] I have practiced a rollback and know how long it takes.
- [ ] I can say where on the maturity ladder my company should stop.

---

## Exercises

Work in `companion/ch56`, in the chapter's notebook, with the stream built by `simulate_production.py`.

### Warm-up

1. How many parts are there per week, and what is the overall defect rate? How does the rate change after week 16, and why?
2. Load the packaged model and print its metadata. Which three fields would you need most in an incident, and why?
3. Call `/health` and `/predict` with one good and one defective part. What does the response tell you that a bare probability would not?
4. Compute PSI for weeks 6 and 7 against weeks 0 to 5, and for week 5 against the other stable weeks. Then compute week 5 against weeks 0 to 7, itself included. What does the difference tell you, and where should the "stable" threshold sit?

### Core

5. Compute recall per week for all 24 weeks and plot it. When does the fall begin, and how many weeks pass before it is obvious by eye?
6. Compute PSI on a *feature* rather than on brightness: take feature 0 and repeat the table. Does it tell the same story?
7. Add a monitor that compares the predicted-defective rate with the true defect rate per week, and find the first week where the gap exceeds one percentage point. Then pool four weeks at a time. What does the monitor see, and why?
8. Retrain including weeks 16 to 19, then find the threshold that minimizes Chapter 53's cost on weeks 20 to 23. How much does the optimal threshold move, and why is choosing it on those weeks optimistic?
9. Write a CI check that loads the packaged model, scores the held-out Chapter 53 test set, and exits non-zero if recall falls below 0.90. Then write the workflow file that runs it on every push.
10. Send the service a request with a NaN in the features, and one with 108 zeros. What happens in each case, and which worries you more?

### Stretch

11. Implement shadow mode as a function that scores both models on a week and returns only the disagreeing part ids, sorted by how confident the disagreement is.
12. Add a second version of the artifact (`defect_v2.joblib`), switch the service to load whichever version an environment variable names, and time a rollback.
13. Simulate a third change: the camera is moved, so every image is shifted two pixels. Which monitor catches it, and how quickly?
14. Build a weekly digest: a small text report with service metrics, drift, the fast proxy, and the audit result, written to a file by a script you could schedule.

### Think about it (no code needed)

15. Your drift monitor has been amber for eight weeks and the model is fine. What do you do?
16. Ground truth for missed defects arrives weeks late. Name three ways to shorten that loop, and what each costs.
17. The plant wants automated retraining with no human approval. What do you need in place first?
18. When would you argue *against* deploying a model at all, even one that works?

---

## Answers

**1.**

```python
parts_per_week = np.bincount(week)
print(f"parts per week: {parts_per_week.min()} to {parts_per_week.max()}, defect rate overall {labels.mean():.2%}")
print(f"weeks 0-15: {labels[week < 16].mean():.2%}")
print(f"weeks 16-23: {labels[week >= 16].mean():.2%}")
print(f"flash parts in weeks 16-23: {(kind[week >= 16] == 'flash').sum()}")
```

```
parts per week: 500 to 500, defect rate overall 8.77%
weeks 0-15: 8.19%
weeks 16-23: 9.95%
flash parts in weeks 16-23: 69
```

`np.bincount(week)` counts how many parts carry each week number, 0 to 23. The rate rises by roughly two points from week 16 because the new mould adds a defect type on top of the existing ones. That is a **change in the world**, not a change in the model, and it is the kind of thing a plant knows on the day it happens: the cheapest monitor Riverstone has is the production meeting's change log.

**2.**

```python
metadata = joblib.load("models/defect_v1.joblib")["metadata"]
for key in ("version", "threshold", "trained_on", "data_hash", "feature_version", "trained_at", "metrics"):
    print(f"  {key:<16} {metadata[key]}")
```

```
  version          defect-v1
  threshold        0.1
  trained_on       ch53 defect_data (6,000 images, seed 53)
  data_hash        64712189dd1e70d8
  feature_version  conv108-v1
  trained_at       2026-03-02T09:00:00
  metrics          {'recall': 0.95, 'precision': 0.95}
```

In an incident the three that matter are **version** (is the thing running the thing I think is running?), **threshold** (what decision boundary is in force?), and **trained_on** with its hash (does this model know about the change we just made?). Everything else is useful later; those three are useful at 2 a.m.

**3.** The response carries `model_version`, `threshold`, and `latency_ms` alongside the probability. That turns every prediction into a self-describing record: when a QC inspector disputes a verdict three days later, the logged line says which model made it, under which threshold, and how long it took. A bare probability cannot be audited, and an audit trail you have to reconstruct is one you do not have.

**4.**

```python
print(f"week 6 against weeks 0-5: PSI {psi(brightness[week < 6], brightness[week == 6]):.4f}")
print(f"week 7 against weeks 0-5: PSI {psi(brightness[week < 6], brightness[week == 7]):.4f}")
others = brightness[(week < 8) & (week != 5)]
print(f"week 5 against the other stable weeks: PSI {psi(others, brightness[week == 5]):.4f}")
print(f"week 5 against weeks 0-7, itself included: PSI {psi(brightness[week < 8], brightness[week == 5]):.4f}")
```

```
week 6 against weeks 0-5: PSI 0.0062
week 7 against weeks 0-5: PSI 0.0132
week 5 against the other stable weeks: PSI 0.0266
week 5 against weeks 0-7, itself included: PSI 0.0192
```

The held-out weeks score 0.006 and 0.013, and week 5 against the other seven stable weeks 0.027. Compared with a reference that contains it, week 5 scores 0.019, about a quarter lower: the week pulls the reference towards itself. **That is how you calibrate the threshold**: the largest value your own stable period produces, measured out of sample, is the noise floor (here about 0.03), and an alert threshold should sit meaningfully above it. Importing 0.1 and 0.25 from a credit-scoring textbook without this check is how alert fatigue starts.

**5.**

```python
import matplotlib.pyplot as plt

weekly_recall = [flagged[(week == w) & (labels == 1)].mean() for w in range(24)]
print("weeks 0-15: ", " ".join(f"{r:.2f}" for r in weekly_recall[:16]))
print("weeks 16-23:", " ".join(f"{r:.2f}" for r in weekly_recall[16:]))
plt.plot(range(24), weekly_recall, marker="o")
plt.xlabel("week"); plt.ylabel("recall"); plt.ylim(0.7, 1.0)
plt.show()
```

```
weeks 0-15:  0.97 0.92 0.97 0.98 1.00 0.95 0.95 1.00 0.94 0.97 0.98 0.96 1.00 0.93 0.98 0.98
weeks 16-23: 0.80 0.81 0.86 0.79 0.86 0.86 0.90 0.87
```

`weekly_recall` is each week's recall, from `flagged` in section 56.8, and `" ".join(...)` prints the numbers on one line. `plt.plot(..., marker="o")` draws them as a line with a dot per week (Chapter 18's matplotlib), and `plt.ylim(0.7, 1.0)` starts the axis at 0.7. Every one of the eight mould weeks (0.79 to 0.90) sits below every one of the sixteen weeks before (0.92 to 1.00). Plotted, week 16's drop is visible at once, but one week holds only about 40 defects, so weekly recall is noisy (week 1 dipped to 0.92 with nothing wrong), and most people would want two or three low weeks before swearing to it. And in production this chart needs labels that only the audit of passed parts provides, a week or more late. That lag is the argument for acting on known events, such as a new mould, without waiting for the chart.

**6.**

```python
print(f"{'week':>5}{'feature 0':>11}{'feature 7':>11}{'brightness':>12}")
for w in (3, 8, 10, 13, 16, 20, 23):
    rows = week == w
    print(f"{w:>5}{psi(features[week < 8, 0], features[rows, 0]):>11.3f}"
          f"{psi(features[week < 8, 7], features[rows, 7]):>11.3f}{psi(baseline, brightness[rows]):>12.3f}")
```

```
 week  feature 0  feature 7  brightness
    3      0.016      0.009       0.007
    8      0.019      0.047       0.065
   10      0.041      0.272       0.614
   13      0.013      1.115       2.959
   16      0.027      2.079       4.107
   20      0.018      2.064       3.981
   23      0.009      2.200       4.246
```

`features[week < 8, 0]` is column 0 for the baseline weeks: the row condition before the comma, the column after it. No, feature 0 does not tell the same story: it hardly moves. It is the blob detector's strongest response in the top-left block of the image (Chapter 53, section 53.6), which is all belt, and the blob kernel compares each pixel with its neighbours, so a belt that is evenly brighter gives the same response. Feature 7, the same detector one block further in, where the lid's rim begins, moves strongly, because a brighter belt changes the contrast at the rim. Two practical lessons: what you choose to monitor decides what you can see, and a quiet monitor on a feature that ignores the change proves nothing; so monitor one interpretable summary (mean brightness) plus the few features the model actually relies on, which you can find with permutation importance (Chapter 39, section 39.8).

**7.**

```python
predicted_share = (model.predict_proba(features)[:, 1] > 0.1).astype(float)
first_week = None
for w in range(24):
    gap = labels[week == w].mean() - predicted_share[week == w].mean()
    if first_week is None and gap > 0.01:
        first_week = w
print(f"first week where the weekly gap exceeds one point: {first_week}")
for end in (15, 19, 23):
    pooled = (week > end - 4) & (week <= end)
    gap = labels[pooled].mean() - predicted_share[pooled].mean()
    print(f"weeks {end - 3}-{end} pooled: predicted {predicted_share[pooled].mean():.1%}, "
          f"true {labels[pooled].mean():.1%}, gap {gap:+.1%}")
```

```
first week where the weekly gap exceeds one point: None
weeks 12-15 pooled: predicted 9.8%, true 8.7%, gap -1.1%
weeks 16-19 pooled: predicted 9.7%, true 9.9%, gap +0.2%
weeks 20-23 pooled: predicted 10.2%, true 10.0%, gap -0.2%
```

The monitor never fires: no single week's gap passes one point, and pooled over four weeks the gap is −1.1, +0.2 and −0.2 points. The misses the new mould causes are real, but the model's extra false alarms cancel them in the count (section 56.7). So what the monitor sees is: nothing. A predicted-rate monitor is still worth having, because it catches a camera that stops flagging or flags everything, and the gap version is useful where false alarms are rare; but for missed defects, only the audit of passed parts counts them.

**8.**

```python
later = np.isin(week, range(20, 24))
probabilities_v2 = candidate.predict_proba(features[later])[:, 1]
print(f"{'threshold':>9}{'missed':>8}{'false alarms':>14}{'cost (Rs)':>11}")
for threshold in (0.5, 0.3, 0.1, 0.05, 0.02, 0.01):
    tn, fp, fn, tp = confusion_matrix(labels[later], probabilities_v2 > threshold).ravel()
    print(f"{threshold:>9}{fn:>8}{fp:>14}{fn * 4000 + fp * 40:>11,}")
```

```
threshold  missed  false alarms  cost (Rs)
      0.5      26             6    104,240
      0.3      23             7     92,280
      0.1      19            20     76,800
     0.05      19            40     77,600
     0.02      14            79     59,160
     0.01      14           132     61,280
```

On weeks 20 to 23 the cheapest threshold is 0.02 (₹59,160), against ₹76,800 at the 0.1 the service runs, so the optimum moves down, from 0.1 to 0.02; section 56.9's out-of-fold sweep moved it further, to 0.01. Choosing it on weeks 20 to 23 is optimistic for the same reason as choosing on a test set (Chapter 53, section 53.6): the threshold is fitted to the very parts that then judge it, so its cost is the best case, not an estimate. Choose on out-of-fold predictions, and let the next weeks' audit confirm.

**9.** The check is the companion file `ci_model_check.py`:

<!-- run: none -->
```python
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
```

It repeats Chapter 53's split to get the same 1,500 test parts, scores the packaged model at the threshold in its own metadata, and prints the result. Run it in a terminal, then ask for its exit code (Chapter 26, section 26.0):

```
# terminal, in companion/ch56
$ python ci_model_check.py
recall 0.950 (floor 0.9), false alarms 6, model defect-v1

$ echo $?
0
```

`sys.exit(0 if recall >= FLOOR else 1)` ends the script with exit code 0 when the model clears the floor and 1 when it doesn't, and CI turns a non-zero exit code into a red cross. Wire it in with Chapter 26's workflow file (section 26.8), saved as `.github/workflows/model-check.yml`:

```yaml
name: model-check
on: [push, pull_request]
jobs:
  check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v7
      - uses: actions/setup-python@v7
        with:
          python-version: "3.14"
      - run: python -m pip install -r requirements.txt
      - run: python ci_model_check.py
```

Every line is Chapter 26's, except the last step, which runs the check. In a real repository the packaged model and a small, versioned copy of the test parts are committed beside the script (the model is 95 kB), so GitHub's fresh machine has everything the check reads. Run it on every change to the model or the feature code (Chapter 29's exit codes, Chapter 32's pipeline). It is the model equivalent of a unit test, and it catches the most common release accident: shipping an artifact that was never evaluated at the threshold it will run under.

**10.**

```python
nan_body = '{"part_id": "P-NaN", "features": [NaN' + ', 0.1' * 107 + ']}'
response = client.post("/predict", content=nan_body, headers={"Content-Type": "application/json"})
print(response.status_code, response.json())

response = client.post("/predict", json={"part_id": "P-zero", "features": [0.0] * 108})
print(response.status_code, response.json()["verdict"], response.json()["probability"])
```

```
422 {'detail': 'features contain NaN or infinity'}
200 good 0.0
```

Strict JSON has no NaN, so `client.post(..., json=...)` refuses to send one; the first request is written as raw text and sent with `content=`, with `headers={"Content-Type": "application/json"}` saying it is JSON, the way a sloppy client on a camera might. Python's JSON reader accepts it, the schema accepts NaN as a float, and it is the explicit `np.isfinite` check that rejects it with a 422. The 108 zeros are accepted, because they are a perfectly valid input shape, and the model returns a confident "good". **The second should worry you more.** Malformed data announces itself; *plausible* data that never occurs in reality (an all-zero frame from a camera that has lost its feed) is scored silently. Defenses: a range check per feature against the training data, and an input monitor that alerts on impossible summaries, such as a `mean_feature` of exactly zero in the log.

**11.** Return the disagreements sorted by `abs(probability_new − probability_old)`, largest first. That ordering is what makes human adjudication affordable: an inspector who can look at thirty parts should look at the thirty the two models disagree about *most*, because those carry the most information about which model is right. It is the same principle as active learning, and it turns a fixed review budget into the best possible evidence.

**12.** Name the artifact files after their versions, keep the version in an environment variable, and load it at startup. In `serve.py`, the loading lines become:

<!-- run: none -->
```python
import os
MODEL_VERSION = os.environ.get("MODEL_VERSION", "defect-v1")
bundle = joblib.load(f"models/{MODEL_VERSION.replace('-', '_')}.joblib")
model, metadata = bundle["model"], bundle["metadata"]
```

`os.environ.get(name, default)` reads the variable (Chapter 29, section 29.3), falling back to `defect-v1`. The versions are written with a hyphen, `defect-v2`, and the files with an underscore, `defect_v2.joblib`, so `.replace('-', '_')` turns one into the other. Start the service with `MODEL_VERSION=defect-v2 uvicorn serve:app --port 8056`; rollback is then `MODEL_VERSION=defect-v1` plus a restart, and the threshold returns with the artifact because it lives in the metadata. Time it. If the number is over five minutes, find out which step is slow *before* the incident, because during one the clock is being watched by people who are not reading your logs.

**13.** A two-pixel shift changes the convolution features noticeably (max-pooling absorbs some of it, which is exactly what pooling is for), so **input monitoring catches it quickly**, probably within a day. Recall may barely move, because the defects are still visible. That makes it the mirror image of the flash defect: drift high, performance fine. The right response is not to retrain but to **ask the plant what changed**, which is a phone call, and to log the answer so the next person knows.

**14.** The digest should fit on a phone screen: uptime and p95 latency (the 95th percentile of section 56.5), the PSI for one or two summaries with last week's value beside it, the predicted-defective rate, the audited recall if new audit results arrived, and the model version in force. Add one line at the top saying whether anything needs action. **A digest nobody reads is worse than no digest**, so write it for the plant manager, not for yourself, and put a name against it.

**15.** First, check whether the model is actually affected: score a recent labeled sample if you have one, or look at the audit's missed-defect rate. If performance is fine, **the alert is wrong, not the model**: recalibrate the threshold on your own stable period, and write down what changed (in Riverstone's case, new lamps) so the amber has an explanation attached. What you must not do is leave it amber, because in a month nobody will look at it, and the next alert will be the real one.

**16.** Three ways: **a sampled audit** of items the model passed (costs inspector time, and it is the one that actually measures missed defects); **a fast proxy** such as the predicted-positive rate or the distribution of predicted probabilities (costs nothing, measures change rather than correctness); and **a downstream signal** that arrives sooner than the final one, such as customer complaints logged at the depot rather than at the invoice stage (costs integration work). Most teams need all three, because each is cheap and blind in a different way.

**17.** Before automating the approval you need: an evaluation set the retrain cannot see, including old data; a **business-metric floor** that blocks the release; a regression check against the original data; automatic threshold re-tuning with its own floor; shadow or canary deployment with a rollback that has been timed; a data-quality gate so a corrupt week cannot become training data; and an audit log of what shipped, when, and on which data. Then automate, and keep a human approval for the first several releases anyway.

**18.** When the decision is rare enough that a person can make it well; when an error is catastrophic and the model's failure mode is silent; when the data needed to monitor it will never exist, so you could never tell whether it still works; when the rule is already known and writing it down is cheaper (Chapter 53's section 53.10); and when nobody will own it. That last one is the most common in practice: **a model with no owner degrades to a liability**, and the most valuable thing this chapter teaches is that the ownership, the monitoring, and the runbook are the deployment, not the extras.

---

## Where this leads

- **Chapter 57, LLMOps,** applies all of this to language models, where the monitoring is harder because there is no accuracy to measure.
- **Chapter 53, Deep Learning in Depth,** trained the model this chapter operates, and chose the threshold that section 56.9 re-tunes.
- **Chapter 46, Pipelines & Orchestration,** schedules the batch scoring, the retraining, and the monitoring jobs.
- **Chapter 47, Data Quality, Observability & Contracts,** is the same discipline one layer down, for the data feeding the model.
- **Chapters 26 and 32** are where the CI habits came from: a check on every push, and tests on every pull request. A model repository deserves the same treatment.
- **Chapter 64, Security, Privacy, Governance & Responsible AI,** covers model cards, audit trails, and who is accountable when an automated decision is wrong.
- **Chapter 74, Machine Learning Question Bank,** has the interview questions, including "how would you know your model has gone stale?"
