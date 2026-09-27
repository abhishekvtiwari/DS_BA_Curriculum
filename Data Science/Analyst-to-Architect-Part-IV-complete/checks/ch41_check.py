"""Analyst to Architect · Chapter 41 · number check.
Recomputes the numbers quoted in Chapter 41's prose and writes checks/ch41_results.json for the figures.
Run from checks/: python3 ch41_check.py   (about 20 seconds). Riverstone Supplies is fictional."""
import json, pathlib, re, warnings
import numpy as np, pandas as pd
from sklearn.decomposition import NMF, LatentDirichletAllocation, PCA
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import f1_score
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
warnings.filterwarnings("ignore")
HERE = pathlib.Path(__file__).resolve().parent
COMP = HERE.parent / "companion"
fails = 0
def ok(label, got, want):
    global fails
    good = got == want; fails += not good
    print(("OK  " if good else "BAD ") + f"{label}: {got} (text: {want})")

tickets = pd.read_csv(COMP / "tickets" / "tickets.csv")
ok("rows", len(tickets), 3000)
ok("topics", dict(tickets.topic.value_counts()), {"Delivery": 892, "Product Defect": 625, "Billing": 560, "General Enquiry": 514, "Order Change": 409})
ok("sentiments", dict(tickets.sentiment.value_counts()), {"neutral": 1467, "frustrated": 988, "positive": 545})

train, test = train_test_split(tickets, test_size=0.25, random_state=41, stratify=tickets.topic)
def topic_pipeline(model):
    return Pipeline([("tfidf", TfidfVectorizer(stop_words="english", max_features=3000, ngram_range=(1, 2), min_df=2)), ("model", model)])
lr = topic_pipeline(LogisticRegression(max_iter=1000)).fit(train.body, train.topic)
nb = topic_pipeline(MultinomialNB()).fit(train.body, train.topic)
acc_lr = (lr.predict(test.body) == test.topic).mean(); acc_nb = (nb.predict(test.body) == test.topic).mean()
ok("lr acc", round(acc_lr, 3), 0.995); ok("nb acc", round(acc_nb, 3), 0.995)
mistakes = (lr.predict(test.body) != test.topic).sum(); ok("mistakes", int(mistakes), 4)

digits = re.compile(r"\d+")
lr_noid = topic_pipeline(LogisticRegression(max_iter=1000)).fit(train.body.str.replace(digits, "0", regex=True), train.topic)
acc_noid = (lr_noid.predict(test.body.str.replace(digits, "0", regex=True)) == test.topic).mean()
ok("no-id acc", round(acc_noid, 3), 0.995)

from nltk.sentiment import SentimentIntensityAnalyzer
sia = SentimentIntensityAnalyzer()
tickets["vader"] = tickets.body.apply(lambda b: sia.polarity_scores(b)["compound"])
means = tickets.groupby("sentiment").vader.mean().round(2)
ok("vader means", means.to_dict(), {"frustrated": -0.33, "neutral": 0.22, "positive": 0.64})
lex = pd.cut(tickets.vader, [-2, -0.05, 0.05, 2], labels=["frustrated", "neutral", "positive"])
ok("lexicon acc", round((lex.astype(str) == tickets.sentiment).mean(), 3), 0.625)
sent_lr = topic_pipeline(LogisticRegression(max_iter=1000)).fit(train.body, train.sentiment)
ok("sent lr acc", round((sent_lr.predict(test.body) == test.sentiment).mean(), 3), 0.999)

cv = CountVectorizer(stop_words="english", max_features=1000, min_df=5, token_pattern=r"\b[a-z]{3,}\b")
counts = cv.fit_transform(tickets.body.str.lower())
lda = LatentDirichletAllocation(n_components=5, random_state=41, max_iter=20).fit(counts)
words = cv.get_feature_names_out()
lda_topics = [[words[j] for j in c.argsort()[-8:][::-1]] for c in lda.components_]
tickets["lda_topic"] = lda.transform(counts).argmax(1)
cross = pd.crosstab(tickets.topic, tickets.lda_topic)
ok("lda cross shape", cross.shape, (5, 5))

from gensim.models import Word2Vec
sentences = [re.findall(r"[a-z]+", b.lower()) for b in tickets.body]
w2v = Word2Vec(sentences, vector_size=50, window=5, min_count=5, seed=41, workers=1)
broken_neighbors = [w for w, _ in w2v.wv.most_similar("broken", topn=5)]
ok("broken neighbors", broken_neighbors, ["completely", "received", "right", "down", "is"])

vocab_words = [w for w in ["broken", "crack", "damaged", "invoice", "gst", "refund", "delivery",
                          "dispatch", "tracking", "order", "cancel", "address", "bulk", "pricing", "catalogue"] if w in w2v.wv]
vectors = np.array([w2v.wv[w] for w in vocab_words])
coords = PCA(n_components=2, random_state=41).fit_transform(vectors)

json.dump({"lda_topics": lda_topics, "cross_lda": cross.to_dict(), "topics_order": sorted(tickets.topic.unique()),
           "vocab_words": vocab_words, "coords": coords.tolist(),
           "confusion_labels": sorted(tickets.topic.unique())},
          open(HERE / "ch41_results.json", "w"))
print("All checks passed." if not fails else f"FAILED: {fails}")
raise SystemExit(1 if fails else 0)
