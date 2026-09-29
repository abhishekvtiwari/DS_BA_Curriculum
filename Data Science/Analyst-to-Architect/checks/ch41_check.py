"""Analyst to Architect · Chapter 41 · number check.
Recomputes the numbers quoted in Chapter 41's prose (the by-hand working, and the figures' data) and writes
checks/ch41_results.json for figures/make_figs41.py. The code outputs themselves are checked by
tools/verify_python.py (run from companion/tickets/).
Run from checks/: python3 ch41_check.py   (about 30 seconds; build the tickets first with
companion/generate_riverstone_tickets.py). Riverstone Supplies is fictional."""
import json, math, pathlib, re
import numpy as np, pandas as pd
from sklearn.decomposition import NMF, LatentDirichletAllocation, PCA
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import confusion_matrix, f1_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline

HERE = pathlib.Path(__file__).resolve().parent
COMP = HERE.parent / "companion"
fails = 0


def ok(label, got, want):
    global fails
    good = got == want
    fails += not good
    print(("OK  " if good else "BAD ") + f"{label}: {got} (text: {want})")


# ---- 41.3 by hand ----
idf = lambda df, n=3: math.log((1 + n) / (1 + df)) + 1
ok("idf crate/the/broken", [round(idf(3), 3), round(idf(2), 3), round(idf(1), 3)], [1.0, 1.288, 1.693])
ok("ln(4/3), ln(4/2)", [round(math.log(4 / 3), 3), round(math.log(2), 3)], [0.288, 0.693])
sq = [round(v * v, 3) for v in (1.288, 1.693, 1.0, 1.288)]
ok("squares", sq, [1.659, 2.866, 1.0, 1.659])
ok("sum of squares", round(sum(sq), 3), 7.184)
ok("length", round(math.sqrt(7.184), 3), 2.680)
ok("normalized", [round(v / 2.680, 3) for v in (1.288, 1.693, 1.0)], [0.481, 0.632, 0.373])  # the library's unrounded value is 0.480
ok("cos(1,2) by hand", [round(0.480 * 0.406, 3), round(0.373 * 0.315, 3), round(2 * 0.480 * 0.406 + 0.373 * 0.315, 3)], [0.195, 0.117, 0.507])
ok("cos(1,3) by hand", round(0.373 * 0.323, 3), 0.120)

# ---- 41.4 Naive Bayes by hand ----
ok("likelihoods", [round(3 / 19, 3), round(2 / 15, 3), round(2 / 19, 3), round(1 / 15, 3), round(1 / 19, 3)], [0.158, 0.133, 0.105, 0.067, 0.053])
defect, delivery = 2 / 3 * 3 / 19 * 2 / 19, 1 / 3 * 2 / 15 * 1 / 15
ok("NB scores", [round(defect, 4), round(delivery, 4)], [0.0111, 0.0030])
ok("NB share", round(defect / (defect + delivery), 2), 0.79)
ok("NB share from rounded", round(0.0111 / (0.0111 + 0.0030), 2), 0.79)

# ---- Ex 2, Ex 3 ----
ok("ex2", [round(math.log(11 / 3) + 1, 3), round(math.log(11 / 3), 3), round(math.log(1.1) + 1, 3)], [2.299, 1.299, 1.095])
a, b = np.array([1, 1, 1, 2, 1]), np.array([1, 1, 1, 0, 1])
ok("ex3 cosine", round(float(a @ b / np.linalg.norm(a) / np.linalg.norm(b)), 2), 0.71)
ok("ex3 parts", [int(a @ b), round(math.sqrt(8) * 2, 3)], [4, 5.657])

# ---- the tickets ----
tickets = pd.read_csv(COMP / "tickets" / "tickets.csv")
ok("rows", len(tickets), 3000)
ok("Delivery share", round(892 / 3000 * 100, 1), 29.7)
train, test = train_test_split(tickets, test_size=0.25, random_state=41, stratify=tickets.topic)
pipe = Pipeline([("tfidf", TfidfVectorizer(stop_words="english", max_features=3000, ngram_range=(1, 2), min_df=2)),
                 ("model", LogisticRegression(max_iter=1000))]).fit(train.body, train.topic)
pred = pipe.predict(test.body)
topics = sorted(tickets.topic.unique())
cm = confusion_matrix(test.topic, pred, labels=topics)
d = topics.index("Delivery")
ok("Delivery column", [int(cm[d, d]), int(cm[:, d].sum() - cm[d, d])], [223, 7])
prec, rec = cm[d, d] / cm[:, d].sum(), cm[d, d] / cm[d, :].sum()
ok("Delivery P/R/F1", [round(prec, 3), round(rec, 3), round(2 * prec * rec / (prec + rec), 3)], [0.970, 1.0, 0.985])
ok("mistakes are all planted mixed tickets", int((test.body[pred != test.topic].str.contains("was fine but")).sum()), 7)

# ---- 41.6 topic models (for Figure 41.1) and the repeat-contact check ----
cv = CountVectorizer(stop_words="english", max_features=1000, min_df=5, token_pattern=r"\b[a-z]{3,}\b")
counts = cv.fit_transform(tickets.body.str.lower())
lda = LatentDirichletAllocation(n_components=5, random_state=41, max_iter=20).fit(counts)
words = cv.get_feature_names_out()
lda_topics = [[words[j] for j in c.argsort()[-8:][::-1]] for c in lda.components_]
tickets["lda_topic"] = lda.transform(counts).argmax(1)
cross_lda = pd.crosstab(tickets.topic, tickets.lda_topic)
ok("LDA topic 1 Billing", [int(cross_lda.loc["Billing", 1]), int(cross_lda.loc["Order Change", 1]), int(cross_lda.loc["Delivery", 1])], [558, 129, 117])

tv = TfidfVectorizer(stop_words="english", max_features=1000, min_df=5, token_pattern=r"\b[a-z]{3,}\b")
tf = tv.fit_transform(tickets.body.str.lower())
nmf = NMF(n_components=5, random_state=41, max_iter=400).fit(tf)
nwords = tv.get_feature_names_out()
nmf_topics = [[nwords[j] for j in c.argsort()[-8:][::-1]] for c in nmf.components_]
tickets["nmf_topic"] = nmf.transform(tf).argmax(1)
cross_nmf = pd.crosstab(tickets.topic, tickets.nmf_topic)
ok("NMF topic 0", [int(cross_nmf[0].sum()), int(cross_nmf.loc["Product Defect", 0]), int(cross_nmf.loc["Order Change", 0])], [1539, 527, 401])
order = tickets.sort_values(["created_at", "ticket_id"])
tickets["second"] = order.order_id.duplicated()
t4 = tickets[tickets.nmf_topic == 4]
ok("topic 4 second contacts", [int(t4.second.sum()), len(t4), round(t4.second.mean() * 100)], [139, 261, 53])
ok("all second contacts", round(tickets.second.mean() * 100), 21)
ok("topic 4 double-charge tickets", int(t4.body.str.contains("charged twice").sum()), 103)

# ---- 41.7 word2vec (for Figure 41.2) ----
from gensim.models import Word2Vec
sentences = [re.findall(r"[a-z]+", b.lower()) for b in tickets.body]
w2v = Word2Vec(sentences, vector_size=50, window=5, min_count=5, seed=41, workers=1)
vocab_words = ["broken", "crack", "damaged", "invoice", "gst", "refund", "delivery", "dispatch",
               "tracking", "order", "cancel", "address", "bulk", "pricing", "catalogue"]
coords = PCA(n_components=2, random_state=41).fit_transform(np.array([w2v.wv[w] for w in vocab_words]))
ok("catalog absent, catalogue present", ["catalog" in w2v.wv, "catalogue" in w2v.wv], [False, True])

json.dump({"lda_topics": lda_topics, "nmf_topics": nmf_topics, "topics_order": topics,
           "cross_lda": cross_lda.values.tolist(), "cross_nmf": cross_nmf.values.tolist(),
           "vocab_words": vocab_words, "coords": coords.round(4).tolist()},
          open(HERE / "ch41_results.json", "w"), indent=1)
print("All checks passed." if not fails else f"FAILED: {fails}")
raise SystemExit(1 if fails else 0)
