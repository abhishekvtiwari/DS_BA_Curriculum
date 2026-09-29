# Chapter 41. NLP Foundations

*Part 4 — Machine Learning & Data Science*

> **Chapter at a glance**
>
> **You will learn to:** clean and tokenize free text, and choose between stemming and lemmatization · build a bag-of-words and a TF-IDF representation by hand before using a library · measure similarity between documents · classify text with Naive Bayes and logistic regression, and read a confusion matrix for more than two classes · score sentiment with a word lexicon and know when it fails · train a sentiment classifier and compare it honestly with the lexicon · find topics in unlabelled text with LDA and NMF, and judge whether they mean anything · train word embeddings and see why they're the bridge to modern language models.
>
> **Before you start:** Chapter 35 (dot product, vector length, cosine similarity, PCA), Chapter 36 (splits, pipelines, sparse matrices), Chapter 37 (Naive Bayes, logistic regression), Chapter 38 (judging clusters), Chapter 39 (precision, recall, F1). This chapter treats text as another kind of feature, built on those foundations.
>
> **Time needed:** 12–15 hours over two weeks. Take it in two sittings: sections 41.0 to 41.4 (turning text into numbers, and classifying it), then sections 41.5 to 41.7 (sentiment, topics, and embeddings).
>
> **Tools:** Python 3 with scikit-learn (installed in Chapter 35), plus NLTK and gensim, installed in section 41.0 (all free).
>
> **Practice data:** 3,000 Riverstone support tickets from 2024–2025, with free-text bodies, a topic, a sentiment, and a satisfaction score, built by `companion/generate_riverstone_tickets.py`. Every number in this chapter was calculated, and every output shown is real.

---

## Why this matters

Chapter 1 promised that this book would eventually deal with unstructured text: emails, reviews, support tickets, free-text survey answers. That's most of the data most companies have, and almost none of the algorithms from Chapters 36–39 can touch it directly, because they all expect numbers in a table.

This chapter is the bridge. Riverstone's support inbox gets a few thousand tickets a year, and three real questions sit behind it:

- *Which team should a new ticket be routed to?* (classification)
- *Which customers are angry right now, so someone calls them today?* (sentiment)
- *What are people actually writing to us about, that our five official categories don't capture?* (topic discovery)

Every method here turns words into numbers first, and the quality of that conversion decides everything downstream. It's also where this book's foundations pay off directly: TF-IDF is an application of Chapter 35's dot products, text classification reuses Chapter 37's Naive Bayes and logistic regression, and judging discovered topics uses Chapter 38's "how do you know it's real?" discipline. Nothing in this chapter is a new kind of thinking, only a new kind of input.

---

## In plain English

**Think of a support team lead skimming a stack of tickets.**

First they'd scan past the "the", "and", and "please" to the words that carry meaning: *broken*, *invoice*, *late*. That's **tokenization** and **stop-word removal**. They'd notice that "delivered", "delivery", and "delivering" are really the same idea, wearing different endings. That's **stemming** or **lemmatization**.

To sort tickets into piles, they'd count which meaningful words each ticket uses, and notice that a word every ticket uses (like "order") tells them nothing, while a word only a few tickets use (like "GST") tells them a lot. That's the idea behind **TF-IDF**.

Some words carry an obvious mood: "furious", "disappointed", "thanks". Counting those is quick **sentiment analysis**, and it fails the moment someone writes something dry and factual that happens to include an angry-sounding word out of context.

Read enough tickets and patterns emerge that nobody wrote down as an official category: maybe there's a cluster of tickets that are really about *packaging*, cutting across "delivery" and "defect". Finding those patterns without being told what to look for is **topic modeling**.

And if you've ever noticed that a customer who says "crate" often also says "broken" or "cracked", never "refund" or "invoice", you've done in your head what a **word embedding** does with arithmetic: it learns which words keep company with which.

---

## 41.0 Setting up

### Two new libraries

This chapter needs two libraries that no earlier chapter installed. **NLTK** (the Natural Language Toolkit) splits and cleans text and scores sentiment; **gensim** trains word embeddings (section 41.7). In a terminal, activate the book's virtual environment (Chapter 17, section 17.0), then install both and record them in `requirements.txt`, as in Chapter 35, section 35.9:

<!-- run: none -->
```
# terminal
$ python -m pip install nltk gensim
$ python -m pip freeze > requirements.txt
```

- `python -m pip install nltk gensim` downloads both libraries, and the packages they need, into the active environment.
- `python -m pip freeze > requirements.txt` rewrites the list of installed packages, so the two new ones are recorded.

### The tickets

The practice data comes from a companion script, the same way Chapter 36 built its CRM export. Still in the terminal, go to the folder that holds the book's `companion` folder (Chapter 26, section 26.0 covers `cd`), then:

```
# terminal
$ cd companion
$ python generate_riverstone_tickets.py
3,000 tickets written to tickets/tickets.csv
topics: Delivery 892, Product Defect 625, Billing 560, General Enquiry 514, Order Change 409
sentiment: neutral 1,467, frustrated 988, positive 545
$ cd tickets
```

- `cd companion` moves into the companion folder, where the script lives.
- `python generate_riverstone_tickets.py` builds the tickets and saves them in a new folder, `tickets`, as `tickets.csv`. The script uses fixed random seeds, so everyone gets exactly the same 3,000 tickets, and the three lines it prints are its confirmation.
- `cd tickets` moves into that new folder. Start Jupyter (or open VS Code) from here, as in Chapter 17, section 17.0, and save this chapter's notebook here. Your notebook then sits next to `tickets.csv`, so the file name alone is enough to open it: no folder path needed.

### Checking the install

In a new notebook, the first cell imports both libraries and prints their versions:

```python
import nltk
import gensim

print(nltk.__version__, gensim.__version__)
```

```
3.10.3 4.4.0
```

- `import nltk` and `import gensim` load the two libraries. If either line fails with `ModuleNotFoundError`, the install went into a different environment: check which environment your notebook is using (Chapter 17, section 17.0).
- `__version__` confirms which version you have. This chapter's outputs were produced with the versions shown.

### NLTK's data files

`pip` installs NLTK's code, but not the word lists and small models it uses. Those are separate downloads, fetched once with `nltk.download`:

```python
for package in ["punkt_tab", "stopwords", "wordnet", "omw-1.4", "vader_lexicon"]:
    print(package, nltk.download(package, quiet=True))
```

```
punkt_tab True
stopwords True
wordnet True
omw-1.4 True
vader_lexicon True
```

- `punkt_tab` is the model NLTK's tokenizer uses to find where sentences end (section 41.2). Older guides say `punkt`; current NLTK needs `punkt_tab`, and without it the tokenizer stops with a "Resource punkt_tab not found" error.
- `stopwords` is NLTK's list of very common words, such as *the* and *is* (section 41.2).
- `wordnet` is a dictionary of English words and their base forms, used for lemmatization (section 41.2).
- `omw-1.4` (Open Multilingual WordNet) is extra WordNet data that the lemmatizer loads alongside it.
- `vader_lexicon` is the sentiment word list used in section 41.5.
- `quiet=True` hides the download progress messages. `nltk.download` returns `True` when the package is ready, either freshly downloaded or already there.

The files go into a folder called `nltk_data` in your home folder, so this is a one-time download: running the cell again only checks that they're there. If a line prints `False`, run `nltk.download` for that package without `quiet=True` to see the reason; it's usually no internet connection, or a company network that blocks the download.

---

## 41.1 Text as data

### The tickets

Load the file and see how many tickets it holds, over what dates, and what each column contains:

```python
import pandas as pd

tickets = pd.read_csv("tickets.csv")
print(
    f"{len(tickets):,} tickets, {tickets['created_at'].min()} "
    f"to {tickets['created_at'].max()}"
)
print(tickets.dtypes.to_string())
```

```
3,000 tickets, 2024-01-01 to 2025-12-30
ticket_id               int64
created_at                str
customer_name             str
subject                   str
body                      str
topic                     str
sentiment                 str
order_id                int64
resolution_hours      float64
satisfaction_score      int64
```

- `pd.read_csv("tickets.csv")` reads the file that sits next to your notebook.
- `.min()` and `.max()` on the date column give the first and last dates. The dates are stored as text in year-month-day form, so their alphabetical order is also their date order.
- `tickets.dtypes` lists every column with its type (Chapter 18, section 18.3); `.to_string()` prints the whole list.

The ten columns:

| Column | What it holds |
|---|---|
| `ticket_id` | the ticket's number |
| `created_at` | the date the ticket arrived |
| `customer_name` | who wrote it |
| `subject` | the subject line |
| `body` | the free text the customer wrote: the column this chapter is about |
| `topic` | one of five official categories, assigned when the ticket was generated |
| `sentiment` | frustrated, neutral, or positive, also assigned when generated |
| `order_id` | the order the ticket is about |
| `resolution_hours` | how long support took to resolve it |
| `satisfaction_score` | the customer's rating afterwards, 1 to 5 |

How are the tickets spread across the topics and the sentiments?

```python
print(tickets["topic"].value_counts().to_string())
print(tickets["sentiment"].value_counts().to_string())
```

```
topic
Delivery           892
Product Defect     625
Billing            560
General Enquiry    514
Order Change       409
sentiment
neutral       1467
frustrated     988
positive       545
```

Delivery is the largest category and Order Change the smallest; about half the tickets are neutral in tone. Now the text itself: how long is a ticket, and what does one look like?

```python
lengths = tickets["body"].str.len()
print(
    f"body length in characters: mean {lengths.mean():.0f}, "
    f"min {lengths.min()}, max {lengths.max()}"
)
print(tickets.loc[0, ["subject", "body", "topic", "sentiment"]].to_string())
```

```
body length in characters: mean 120, min 76, max 227
subject                                          Billing issue
body         Dear team, could you clarify the invoice for o...
topic                                                  Billing
sentiment                                              neutral
```

- `.str.len()` counts the characters in every body (Chapter 18, section 18.10).
- `tickets.loc[0, [...]]` picks row 0 and four of its columns. pandas shortens the long body with `...` when it prints a column like this; section 41.2 prints it in full.

Riverstone's tickets look like real support email: short, sometimes typo-ridden, occasionally polite ("kindly do the needful"), occasionally furious. Five official topics and three sentiment labels were assigned when each ticket was generated, which lets this chapter check machine answers against a known truth, something you rarely get with real support data.

> **A caution about this chapter's data.** These tickets come from a template generator: a handful of sentence patterns per topic and sentiment, filled in with random products and numbers. That makes the topics far more distinctive than typical human writing, and you'll see classification scores in this chapter that would be suspicious on a real inbox. Section 41.2's watch-out box and the exercises come back to this; treat the *methods* as the lesson, not the exact scores.

### Why "just read them" doesn't scale

At a few thousand tickets a year, reading every one is possible; at 30,000 it isn't, and a human reader is also inconsistent (two people label the same ticket differently) and slow to notice a trend spread across weeks. The rest of the chapter turns text into something a computer, and a consistent process, can act on.

---

## 41.2 Cleaning and tokenization

**Tokenization** splits text into units, usually words; each unit is a **token**. NLTK's `word_tokenize` also separates punctuation from words. Here it is on the first ticket, after lowercasing, so that "The" and "the" count as the same word:

```python
from nltk.tokenize import word_tokenize

raw = tickets.loc[0, "body"]
lower = raw.lower()
tokens = word_tokenize(lower)
print("raw:      ", raw)
print("lowercase:", lower)
print("tokens:   ", tokens)
```

```
raw:       Dear team, could you clarify the invoice for order #108347? The amount Rs 2570 does not match what we discussed with the sales rep.
lowercase: dear team, could you clarify the invoice for order #108347? the amount rs 2570 does not match what we discussed with the sales rep.
tokens:    ['dear', 'team', ',', 'could', 'you', 'clarify', 'the', 'invoice', 'for', 'order', '#', '108347', '?', 'the', 'amount', 'rs', '2570', 'does', 'not', 'match', 'what', 'we', 'discussed', 'with', 'the', 'sales', 'rep', '.']
```

- `.lower()` turns every capital letter into a small one.
- `word_tokenize(lower)` returns a list of tokens.

**Reading it.** `word_tokenize` split `#108347` into `#` and `108347`, and made `,`, `?` and `.` tokens of their own. It also knows the difference between a full stop that ends a sentence and a decimal point inside a number, which splitting on spaces can't:

```python
print(word_tokenize("the 2.5 kg crate arrived. thanks"))
```

```
['the', '2.5', 'kg', 'crate', 'arrived', '.', 'thanks']
```

`2.5` stays one token, while the full stop after "arrived" becomes its own.

Most tasks in this chapter care about words, not punctuation or numbers. `.isalpha()` is `True` only for a token made entirely of letters, so a comprehension (Chapter 17, section 17.6) keeps just those:

```python
words_only = [t for t in tokens if t.isalpha()]
print(words_only)
```

```
['dear', 'team', 'could', 'you', 'clarify', 'the', 'invoice', 'for', 'order', 'the', 'amount', 'rs', 'does', 'not', 'match', 'what', 'we', 'discussed', 'with', 'the', 'sales', 'rep']
```

Dropping numbers is usually right for topic and sentiment work, and usually wrong if the numbers matter (an amount, a date).

### Stop words

**Stop words** (*the*, *is*, *and*, *we*) carry grammar rather than meaning. NLTK keeps a list of them:

```python
from nltk.corpus import stopwords

stop_words = set(stopwords.words("english"))
print(len(stop_words), "stop words; the first 20:")
print(sorted(stop_words)[:20])
```

```
198 stop words; the first 20:
['a', 'about', 'above', 'after', 'again', 'against', 'ain', 'all', 'am', 'an', 'and', 'any', 'are', 'aren', "aren't", 'as', 'at', 'be', 'because', 'been']
```

- `stopwords.words("english")` returns NLTK's English list.
- `set(...)` turns the list into a set (Chapter 17, section 17.7), which checks "is this word in it?" much faster than a list.
- `sorted(stop_words)[:20]` puts the set in alphabetical order and shows the first 20.

Now remove them from the first ticket, and print what went as well as what stayed:

```python
kept = [t for t in words_only if t not in stop_words]
removed = [t for t in words_only if t in stop_words]
print(f"removed {len(removed)} stop words:", removed)
print("kept:", kept)
```

```
removed 10 stop words: ['you', 'the', 'for', 'the', 'does', 'not', 'what', 'we', 'with', 'the']
kept: ['dear', 'team', 'could', 'clarify', 'invoice', 'order', 'amount', 'rs', 'match', 'discussed', 'sales', 'rep']
```

**Reading it.** Removing stop words shrinks every ticket to the words that carry its subject: *clarify*, *invoice*, *amount*, *match*. But look at what went: **`not` is on NLTK's stop-word list**, so "does not match" became "match". For topics that hardly matters. For sentiment it can flip the meaning ("not good" becomes "good"), which exercise 3 comes back to.

### Stemming vs lemmatization

Both reduce words to a common form, so "deliver", "delivered", and "delivering" count as one feature instead of three. They do it differently:

- **Stemming** (Porter's algorithm) chops suffixes with fixed rules, fast and crude. It doesn't know grammar, so it can produce non-words.
- **Lemmatization** looks up the dictionary base form (the **lemma**), and needs to be told the part of speech. Asked for the adjective, WordNet turns *better* into *good*; asked for a verb or a noun, it leaves *better* alone.

> **Porter's rules, a taste.** The Porter stemmer applies its rules in steps. Step 1 removes *-ed* and *-ing* if a vowel is left in what remains: *delivering* → *deliver*. Another step turns a final *y* into *i*: *delivery* → *deliveri*. A later step removes *-er* from a long enough word: *deliver* → *deliv*. That's why *delivered* and *delivering* both end as `deliv`, while *delivery* stops at `deliveri`. The full algorithm has about 60 such rules.

The same seven words through the stemmer and through the lemmatizer, asked for each part of speech in turn:

```python
from nltk.stem import PorterStemmer, WordNetLemmatizer

stemmer = PorterStemmer()
lemmatizer = WordNetLemmatizer()
examples = [
    "delivered", "delivery", "delivering", "crates", "broken", "running", "better"
]
print(f"{'word':<12}{'stem':<10}{'verb':<10}{'noun':<12}adjective")
for word in examples:
    stem = stemmer.stem(word)
    verb = lemmatizer.lemmatize(word, pos="v")
    noun = lemmatizer.lemmatize(word, pos="n")
    adjective = lemmatizer.lemmatize(word, pos="a")
    print(f"{word:<12}{stem:<10}{verb:<10}{noun:<12}{adjective}")
```

```
word        stem      verb      noun        adjective
delivered   deliv     deliver   delivered   delivered
delivery    deliveri  delivery  delivery    delivery
delivering  deliv     deliver   delivering  delivering
crates      crate     crate     crate       crates
broken      broken    break     broken      broken
running     run       run       running     running
better      better    better    better      good
```

- `PorterStemmer()` and `WordNetLemmatizer()` create the two tools; `.stem(word)` and `.lemmatize(word, pos=...)` apply them to one word.
- `pos` is the part of speech: `"v"` for verb, `"n"` for noun, `"a"` for adjective. Without it, `lemmatize` assumes a noun.
- `:<12` and `:<10` pad each value to 12 or 10 characters, lined up on the left, so the output forms columns: the f-string widths from Chapter 17, section 17.7.

**Reading it.** Stemming turns *delivery* into `deliveri`, not a real word, but a consistent bucket. Lemmatization gives real words, but only for the right part of speech: as a verb, *broken* becomes *break* and *running* becomes *run*; as a noun, both stay as they are; as an adjective, *better* becomes *good*. For search and topic modeling, stemming's crudeness rarely matters and it's faster; for anything a human will read afterward (a word cloud, a report), lemmatization looks less broken.

> **Watch out: cleaning choices are invisible in the output but change everything downstream.** Whether you keep numbers, remove stop words, stem, or lemmatize is a modeling decision like any hyperparameter, and different choices can move a classifier's accuracy by several points. Try more than one and compare (exercises 5 and 6), the same discipline as Chapter 36's feature engineering.

---

## 41.3 Bag of words and TF-IDF

### Bag of words, by hand

The simplest representation: for a fixed vocabulary, count how many times each word appears in each document, ignoring order entirely (hence "bag"). Take three tiny documents:

1. "the crate arrived broken"
2. "the crate arrived on time"
3. "please send a replacement crate"

On paper: list every different word once, in alphabetical order (that's the **vocabulary**, 10 words here), then read each sentence and write how many times it uses each word:

| | a | arrived | broken | crate | on | please | replacement | send | the | time |
|---|---|---|---|---|---|---|---|---|---|---|
| doc 1 | 0 | 1 | 1 | 1 | 0 | 0 | 0 | 0 | 1 | 0 |
| doc 2 | 0 | 1 | 0 | 1 | 1 | 0 | 0 | 0 | 1 | 1 |
| doc 3 | 1 | 0 | 0 | 1 | 0 | 1 | 1 | 1 | 0 | 0 |

Now the same steps in code. First the vocabulary:

```python
mini = [
    "the crate arrived broken",
    "the crate arrived on time",
    "please send a replacement crate",
]
all_words = " ".join(mini).split()
vocab = sorted(set(all_words))
print(vocab)
```

```
['a', 'arrived', 'broken', 'crate', 'on', 'please', 'replacement', 'send', 'the', 'time']
```

- `" ".join(mini)` glues the three sentences into one string with spaces between them (Chapter 17, section 17.3), and `.split()` cuts it into words: 14 words, with repeats.
- `set(all_words)` keeps one copy of each word, and `sorted(...)` puts them in alphabetical order as a list.

Next, one row of the table, for document 1 only:

```python
row = [mini[0].split().count(word) for word in vocab]
print(row)
```

```
[0, 1, 1, 1, 0, 0, 0, 0, 1, 0]
```

`mini[0].split()` is document 1 as a list of words, and `.count(word)` counts how many times a word appears in that list, once for each vocabulary word in turn. The row matches the paper table's first row. The same for all three documents, collected into a DataFrame:

```python
rows = []
for doc in mini:
    rows.append([doc.split().count(word) for word in vocab])
bow = pd.DataFrame(rows, columns=vocab)
print(bow.to_string())
```

```
   a  arrived  broken  crate  on  please  replacement  send  the  time
0  0        1       1      1   0       0            0     0    1     0
1  0        1       0      1   1       0            0     0    1     1
2  1        0       0      1   0       1            1     1    0     0
```

**Reading it.** Each row is a document, each column a vocabulary word, each cell a count; pandas numbers the rows from 0, so row 0 is document 1. "Crate" appears in all three; "arrived" and "the" in the first two. Order is completely gone: "the crate arrived broken" and "broken arrived the crate" would produce an identical row. That's the bag-of-words trade: simple and fast, blind to word order and negation ("not broken" looks like "broken" plus a stop word).

### TF-IDF, by hand

Raw counts overweight common words. **TF-IDF** (term frequency–inverse document frequency) discounts a word by how many documents contain it:

> tf-idf(word, doc) = tf(word, doc) × idf(word), where idf(word) = ln((1 + N) ÷ (1 + df)) + 1

Here **tf** is how many times the word appears in the document, **N** is the number of documents, **df** (document frequency) is how many documents contain the word, and ln is the natural logarithm (Chapter 31, section 31.0, and Chapter 35, section 35.8). This is scikit-learn's version of the formula. The +1 inside the fraction acts as if one extra document contained every word, so a word with df = 0 never divides by zero; the trailing +1 keeps a word found in every document (ln 1 = 0) from getting zero weight.

With N = 3, by hand:

- **crate** is in all 3 documents: idf = ln(4 ÷ 4) + 1 = 0 + 1 = **1.000**
- **the** and **arrived** are in 2: idf = ln(4 ÷ 3) + 1 = 0.288 + 1 = **1.288**
- **broken** is in 1: idf = ln(4 ÷ 2) + 1 = 0.693 + 1 = **1.693**

Each of these words appears once in document 1, so its tf-idf there equals its idf. Before you run the next cell, predict which of the four words gets the highest score in document 1. The code checks the hand numbers:

```python
import numpy as np

n_docs = len(mini)


def idf(word):
    docs_with_word = sum(word in doc.split() for doc in mini)
    return np.log((1 + n_docs) / (1 + docs_with_word)) + 1


for word in ["crate", "broken", "arrived", "the"]:
    tf = mini[0].split().count(word)
    tf_idf = tf * idf(word)
    print(f"{word:<8} tf(doc 1)={tf}   idf={idf(word):.3f}   tf-idf={tf_idf:.3f}")
```

```
crate    tf(doc 1)=1   idf=1.000   tf-idf=1.000
broken   tf(doc 1)=1   idf=1.693   tf-idf=1.693
arrived  tf(doc 1)=1   idf=1.288   tf-idf=1.288
the      tf(doc 1)=1   idf=1.288   tf-idf=1.288
```

- `word in doc.split()` is `True` or `False` for each document; `sum(...)` counts the `True`s, which is df.
- `np.log` is the natural logarithm, ln.
- `idf(word)` is a function (Chapter 17, section 17.8), so the formula is written once and used for every word.

**Reading it.** "Crate" appears in all three mini-documents, so its idf is a bare 1.0, the smallest possible: common within this collection, not distinctive. "Broken" appears in only one, so it gets the highest idf and the highest tf-idf score in that document: a word that appears rarely across the collection but stands out where it does appear is exactly what TF-IDF is built to find.

scikit-learn's `TfidfVectorizer` does the counting and the weighting in one step:

```python
from sklearn.feature_extraction.text import TfidfVectorizer

vectorizer = TfidfVectorizer()
matrix = vectorizer.fit_transform(mini)
print("vocabulary:", vectorizer.get_feature_names_out())
scores = pd.DataFrame(matrix.toarray(), columns=vectorizer.get_feature_names_out())
print(scores.round(3).to_string())
```

```
vocabulary: ['arrived' 'broken' 'crate' 'on' 'please' 'replacement' 'send' 'the'
 'time']
   arrived  broken  crate     on  please  replacement   send    the   time
0    0.480   0.632  0.373  0.000   0.000        0.000  0.000  0.480  0.000
1    0.406   0.000  0.315  0.534   0.000        0.000  0.000  0.406  0.534
2    0.000   0.000  0.323  0.000   0.546        0.546  0.546  0.000  0.000
```

- `TfidfVectorizer()` creates the vectorizer with its default settings.
- `.fit_transform(mini)` does two things: *fit* learns the vocabulary and each word's idf from the documents; *transform* turns each document into its row of tf-idf numbers.
- The result is a sparse matrix, as in Chapter 36, section 36.4: it stores only the non-zero cells. `.toarray()` turns it into a normal grid so pandas can print it.
- `.get_feature_names_out()` gives the vocabulary, in column order.

**Where did "a" go?** `TfidfVectorizer` lowercases the text and, by default, keeps only tokens of two or more letters or digits (its `token_pattern` setting), so the one-letter word "a" is dropped. The other idf values don't change.

**One more step: rows of length 1.** The numbers don't match the hand ones, and that's deliberate. After weighting, `TfidfVectorizer` rescales each document's row to length 1 (setting `norm="l2"`, the default), so that a long document and a short one on the same topic get comparable rows. That's Chapter 35's vector normalization, applied to text. By hand, for document 1:

> raw tf-idf: arrived 1.288, broken 1.693, crate 1.000, the 1.288
>
> length = √(1.288² + 1.693² + 1.000² + 1.288²) = √(1.659 + 2.866 + 1.000 + 1.659) = √7.184 = 2.680
>
> arrived 1.288 ÷ 2.680 = **0.481** · broken 1.693 ÷ 2.680 = **0.632** · crate 1.000 ÷ 2.680 = **0.373** · the 1.288 ÷ 2.680 = **0.481**

These are the numbers in row 0. The last digit of 0.481 differs from the table's 0.480 only because the hand working rounds as it goes.

### Documents as vectors, again

Once every document is a row of length 1, Chapter 35's cosine similarity is just the dot product of two rows: multiply the matching cells and add. By hand, from the table above:

> cos(doc 1, doc 2) = arrived 0.480 × 0.406 + crate 0.373 × 0.315 + the 0.480 × 0.406 = 0.195 + 0.117 + 0.195 = **0.507**
>
> cos(doc 1, doc 3) = crate 0.373 × 0.323 = **0.120**

Documents 1 and 2 share three words; documents 1 and 3 share only "crate", the least distinctive word. scikit-learn's `cosine_similarity` computes every pair at once:

```python
from sklearn.metrics.pairwise import cosine_similarity

print(cosine_similarity(matrix).round(3))
```

```
[[1.    0.508 0.12 ]
 [0.508 1.    0.102]
 [0.12  0.102 1.   ]]
```

Row 1, column 2 (counting from 1) is 0.508, the hand answer; the last digit differs only because the hand version used rounded numbers. The diagonal is 1: every document is identical to itself.

Now the same on all 3,000 tickets, with three settings that matter for real text:

```python
full_tfidf = TfidfVectorizer(stop_words="english", max_features=3000, min_df=2)
X_all = full_tfidf.fit_transform(tickets["body"])
print(f"{len(full_tfidf.vocabulary_):,} words in the vocabulary")
print("108347" in full_tfidf.vocabulary_, "2570" in full_tfidf.vocabulary_)
```

```
807 words in the vocabulary
False False
```

- `stop_words="english"` removes scikit-learn's own list of 318 English stop words, which is slightly different from NLTK's 198.
- `max_features=3000` would keep only the 3,000 most frequent words. These tickets have fewer than that, so here it changes nothing; on a large collection it keeps the table a manageable size.
- `min_df=2` drops any word found in fewer than 2 tickets.
- `.vocabulary_` is the learned vocabulary (a dictionary from word to column number), so `len(...)` counts it.
- The last line checks whether ticket 0's order number, 108347, and its amount, 2570, made it into the vocabulary. Both are `False`: each appears in only one ticket, so `min_df=2` dropped them.

Which tickets read most like ticket 0?

```python
sim = cosine_similarity(X_all[0], X_all)[0]
nearest = np.argsort(-sim)[1:4]
print(f"ticket 0: {tickets.loc[0, 'topic']} / {tickets.loc[0, 'sentiment']}")
print(tickets.loc[0, "body"])
for i in nearest:
    print(
        f"\nsimilarity {sim[i]:.3f} -- ticket {i} "
        f"({tickets.loc[i, 'topic']} / {tickets.loc[i, 'sentiment']}):"
    )
    print(tickets.loc[i, "body"])
```

```
ticket 0: Billing / neutral
Dear team, could you clarify the invoice for order #108347? The amount Rs 2570 does not match what we discussed with the sales rep.

similarity 1.000 -- ticket 639 (Billing / neutral):
Dear team, could you clarify the invoice for order #105476? The amount Rs 8760 does not match what we discussed with the sales rep.

similarity 1.000 -- ticket 2926 (Billing / neutral):
Dear team, could you clarify the invoice for order #105980? The amount Rs 8250 does not match what we discussed with the sales rep.

similarity 1.000 -- ticket 143 (Billing / neutral):
Dear team, could you clarify the invoice for order #109547? The amount Rs 9160 does not match what we discussed with the sales rep.
```

- `cosine_similarity(X_all[0], X_all)` compares ticket 0 with every ticket; it returns a table with one row, and `[0]` takes that row as 3,000 numbers.
- `np.argsort(...)` returns the positions that would sort the numbers from smallest to largest. The minus sign in `-sim` flips that, so the most similar come first.
- `[1:4]` skips position 0, which is ticket 0 itself (similarity 1 with itself), and keeps the next three.

**Reading it.** The three most similar tickets score a cosine similarity of exactly 1.000: the same sentence template with a different order number and amount swapped in. Order numbers and amounts that appear in only one ticket each were dropped from the vocabulary by `min_df=2`; what's left is the identical template, so the vectors are identical and the similarity is exactly 1. On real support tickets, this same calculation is what powers "find similar past tickets" and duplicate-ticket detection.

---

## 41.4 Text classification

### Setting up, and a caution about scores

We use a stratified random split for simplicity: 75% of the tickets to train on, 25% held back to test, with each topic in the same proportion on both sides (`stratify`, as in Chapter 36, section 36.3). In production you'd split by date (Chapter 36), and keep all the tickets about one order on the same side, because repeat contacts about the same order share wording.

```python
from sklearn.model_selection import train_test_split

train, test = train_test_split(
    tickets, test_size=0.25, random_state=41, stratify=tickets["topic"]
)
print(f"{len(train):,} training tickets, {len(test):,} test tickets")
print((train["topic"].value_counts(normalize=True) * 100).round(1).to_string())
```

```
2,250 training tickets, 750 test tickets
topic
Delivery           29.7
Product Defect     20.8
Billing            18.7
General Enquiry    17.1
Order Change       13.6
```

- `test_size=0.25` holds back a quarter of the tickets for testing; `random_state=41` fixes the shuffle, so you get the same split.
- `value_counts(normalize=True)` gives each topic's share instead of its count; `* 100` turns the shares into percentages.

The training shares match the full data's (892 of 3,000 Delivery tickets is 29.7%), which is what `stratify` promises.

### Naive Bayes for words, by hand

Chapter 37, section 37.5 built Naive Bayes on numeric features, using Bayes' rule: a class's score is its prior times the likelihood of what you see. For text, the "features" are word counts, and the likelihood of a word in a class comes from counting. This version is called **multinomial Naive Bayes**.

Label the three mini-documents: document 1 ("the crate arrived broken") and document 3 ("please send a replacement crate") are **Defect**; document 2 ("the crate arrived on time") is **Delivery**. Then:

- **Priors:** 2 of 3 documents are Defect, so P(Defect) = 2/3; P(Delivery) = 1/3.
- **Word counts per class:** Defect's documents hold 4 + 5 = 9 words; Delivery's holds 5. The vocabulary has 10 words.
- **Word likelihoods**, P(word | class) = (count of the word in the class + 1) ÷ (words in the class + vocabulary size):

| Word | Defect | Delivery |
|---|---|---|
| crate | (2 + 1) ÷ (9 + 10) = 3/19 = 0.158 | (1 + 1) ÷ (5 + 10) = 2/15 = 0.133 |
| broken | (1 + 1) ÷ 19 = 2/19 = 0.105 | (0 + 1) ÷ 15 = 1/15 = 0.067 |
| time | (0 + 1) ÷ 19 = 1/19 = 0.053 | (1 + 1) ÷ 15 = 2/15 = 0.133 |

The **+1** is **Laplace smoothing**: without it, "broken" would have probability 0 for Delivery, and a single unseen word would wipe out a class's whole score.

Now score a new ticket, "crate broken": prior × the likelihood of each word.

> Defect: 2/3 × 3/19 × 2/19 = 0.667 × 0.158 × 0.105 = **0.0111**
>
> Delivery: 1/3 × 2/15 × 1/15 = 0.333 × 0.133 × 0.067 = **0.0030**

Defect wins. As probabilities that add up to 1: 0.0111 ÷ (0.0111 + 0.0030) = **0.79** Defect, 0.21 Delivery. scikit-learn's `MultinomialNB`, trained on the bag-of-words table from earlier in this section, gives the same:

```python
from sklearn.naive_bayes import MultinomialNB

labels = ["Defect", "Delivery", "Defect"]
nb_mini = MultinomialNB().fit(bow, labels)
new_row = ["crate broken".split().count(word) for word in vocab]
new = pd.DataFrame([new_row], columns=vocab)
print(nb_mini.classes_, nb_mini.predict_proba(new).round(3))
```

```
['Defect' 'Delivery'] [[0.789 0.211]]
```

- `MultinomialNB()` uses the +1 by default (its setting `alpha=1.0`).
- `.fit(bow, labels)` counts the words per class, exactly as the table did.
- `new_row` counts the new ticket's words over the same 10-word vocabulary, and `new` wraps that one row in a DataFrame with the same columns as `bow`.
- `.predict_proba(new)` gives one probability per class, in the order of `.classes_` (Chapter 36, section 36.4).

On the real tickets, `MultinomialNB` does exactly this for every word in the vocabulary. The pipeline below feeds it TF-IDF weights rather than whole counts, so it works with weighted counts. That's common in practice and works well, though the theory assumes counts.

### Adding word pairs (n-grams)

Bag of words loses word order, but you can keep a little of it by counting pairs of neighbouring words as features too. A sequence of *n* neighbouring words is an **n-gram**; a pair is a **bigram**. `CountVectorizer`, the counting half of `TfidfVectorizer`, shows what `ngram_range=(1, 2)` adds on one sentence:

```python
from sklearn.feature_extraction.text import CountVectorizer

pairs = CountVectorizer(ngram_range=(1, 2)).fit(["the crate arrived broken"])
print(pairs.get_feature_names_out())
```

```
['arrived' 'arrived broken' 'broken' 'crate' 'crate arrived' 'the'
 'the crate']
```

`ngram_range=(1, 2)` means "single words (1) up to pairs (2)": the four words, plus the three adjacent pairs. This is how "not good" can survive as one feature, instead of splitting into a "not" and a "good" that bag of words can't connect. What happens if you change it to `(2, 2)`? Only the pairs are kept; exercise 11 tries that on the tickets.

### Two classifiers

Both models get the same preparation, so a small function builds a pipeline around whichever model you pass in:

```python
from sklearn.pipeline import Pipeline


def text_pipeline(model):
    vectorizer = TfidfVectorizer(
        stop_words="english", max_features=3000, ngram_range=(1, 2), min_df=2
    )
    return Pipeline([("tfidf", vectorizer), ("model", model)])
```

- The vectorizer uses section 41.3's settings, plus word pairs.
- `Pipeline([...])` chains the steps, as in Chapter 36, section 36.4. Each step is a pair: a name you choose (`"tfidf"`, `"model"`) and the object that does the work.
- Because the vectorizer sits inside the pipeline, `.fit` learns the vocabulary and idf from the training tickets only, so no test-set words leak into training (Chapter 36, section 36.9).
- The function returns a new, unfitted pipeline each time it's called. The same function serves every text model in this chapter.

Now train Naive Bayes and logistic regression to predict each ticket's topic from its body, and score them on the test tickets:

```python
from sklearn.linear_model import LogisticRegression

nb_topic = text_pipeline(MultinomialNB()).fit(train["body"], train["topic"])
lr_topic = text_pipeline(LogisticRegression(max_iter=1000)).fit(
    train["body"], train["topic"]
)
for name, model in [("Naive Bayes", nb_topic), ("logistic regression", lr_topic)]:
    pred = model.predict(test["body"])
    print(f"{name:<22} accuracy {(pred == test['topic']).mean():.3f}")
```

```
Naive Bayes            accuracy 0.991
logistic regression    accuracy 0.991
```

- `.fit(train["body"], train["topic"])` passes the raw text in; the pipeline turns it into TF-IDF features and trains the model on them.
- `(pred == test['topic']).mean()` is accuracy: the share of test tickets whose predicted topic matches the true one.

Chapter 37, section 37.3 used logistic regression for two classes. With five, scikit-learn fits one set of weights per class, turns the five scores into five probabilities that add up to 1 (with the **softmax** function, which Chapter 53, section 53.7 builds by hand), and predicts the class with the highest probability. `max_iter=1000` lets the solver take more steps; without it, you may see a `ConvergenceWarning`, which means it stopped before it finished.

**Reading it.** Both models score about 99% accuracy. That is a suspiciously good result, and section 41.1's caution explains why: this generator uses only two or three sentence templates per topic, so the vocabulary is nearly a fingerprint for the category. **Real support tickets, written by hundreds of different people in their own words, would not classify this cleanly**; a well-tuned production system on genuine free text typically lands in the 80s or low 90s for accuracy on a five-way problem like this. Treat this score as a demonstration that the method works, not as a benchmark to expect elsewhere.

### The confusion matrix for five classes

Chapter 39, section 39.1 read a two-by-two confusion matrix. With five topics it grows to five by five, and the layout is the same: **rows are the true topic, columns are the predicted topic, and the diagonal counts the correct answers**. Everything off the diagonal is a mistake.

```python
from sklearn.metrics import confusion_matrix

topics = sorted(tickets["topic"].unique())
test_pred = lr_topic.predict(test["body"])
cm = confusion_matrix(test["topic"], test_pred, labels=topics)
print(pd.DataFrame(cm, index=topics, columns=topics).to_string())
```

```
                 Billing  Delivery  General Enquiry  Order Change  Product Defect
Billing              140         0                0             0               0
Delivery               0       223                0             0               0
General Enquiry        0         4              125             0               0
Order Change           0         1                0           101               0
Product Defect         0         2                0             0             154
```

- `labels=topics` fixes the order of the rows and columns (alphabetical here), and the same list names them in the DataFrame.
- `test_pred` keeps the test predictions, so the next cells don't have to predict again.

### Precision, recall, and F1 for five classes

Each class is scored **one-vs-rest**: treat it as "positive" and the other four together as "negative", then use Chapter 39's formulas. For Delivery, read its column and its row:

- **Precision** = correct Delivery predictions ÷ all Delivery predictions (the Delivery column).
- **Recall** = correct Delivery predictions ÷ all true Delivery tickets (the Delivery row).

The Delivery column holds 223 correct predictions plus 7 tickets from other topics, so precision = 223 ÷ 230 = **0.970**. The Delivery row has 223 tickets, all predicted correctly, so recall = 223 ÷ 223 = **1.000**. F1 = 2 × 0.970 × 1.000 ÷ (0.970 + 1.000) = **0.985**.

That gives five F1 scores, one per topic. Two ways to combine them into one number:

- **Macro average:** the plain mean of the five, so every class counts equally, however small. It's the one to watch when a small class matters.
- **Weighted average:** the mean weighted by **support**, the number of true tickets in each class, so large classes count more.

`classification_report` prints all of it:

```python
from sklearn.metrics import classification_report, f1_score

print(classification_report(test["topic"], test_pred))
print(f"macro F1: {f1_score(test['topic'], test_pred, average='macro'):.3f}")
```

```
                 precision    recall  f1-score   support

        Billing       1.00      1.00      1.00       140
       Delivery       0.97      1.00      0.98       223
General Enquiry       1.00      0.97      0.98       129
   Order Change       1.00      0.99      1.00       102
 Product Defect       1.00      0.99      0.99       156

       accuracy                           0.99       750
      macro avg       0.99      0.99      0.99       750
   weighted avg       0.99      0.99      0.99       750

macro F1: 0.991
```

- `classification_report` gives precision, recall, F1, and support for each class, then accuracy, the macro average, and the weighted average. It rounds to two decimals: Delivery's 0.970 shows as 0.97.
- `f1_score(..., average="macro")` computes the macro F1 on its own, to three decimals.

### The errors, and one thing a matrix can't explain

The matrix counts the mistakes; reading them tells you why they happened:

```python
wrong = test_pred != test["topic"]
mistakes = test[wrong]
print(f"{len(mistakes)} misclassified tickets out of {len(test)}")
side_by_side = pd.DataFrame({"true": mistakes["topic"], "predicted": test_pred[wrong]})
print(side_by_side.to_string())
print(mistakes["body"].iloc[0])
```

```
7 misclassified tickets out of 750
                 true predicted
2647  General Enquiry  Delivery
450    Product Defect  Delivery
454      Order Change  Delivery
2797  General Enquiry  Delivery
1210  General Enquiry  Delivery
2145  General Enquiry  Delivery
1153   Product Defect  Delivery
The chopping board was fine but the delivery was late and the invoice amount looks off, please check.
```

- `wrong` is `True` for every test ticket whose prediction differs from the truth; `test[wrong]` keeps those rows.
- `test_pred[wrong]` picks the matching predictions, so the table shows each mistake's true and predicted topic side by side.
- `.iloc[0]` prints the first mistake's text in full.

**Reading it.** Every mistake has the same wording: a "mixed" ticket, deliberately planted by the generator, that mentions a late delivery and an invoice problem in the same message. "Delivery" and "late" pull it toward Delivery, whatever label it carries. The generator kept each planted ticket's original label, so a ticket whose words are all about delivery and billing can be labeled General Enquiry or Product Defect. Even humans disagree on tickets like this; a classification system needs a rule for them (route to the topic mentioned first, or to a "mixed issue" queue) rather than pretending every ticket has one true label.

### Checking the score isn't an accident of IDs

Could the model be keying on numbers instead of words? Numbers that occur in only one ticket were already dropped by `min_df=2`, but numbers that recur (a common amount, or an order that two tickets are about) are still features:

```python
vocabulary = lr_topic.named_steps["tfidf"].get_feature_names_out()
with_digits = [term for term in vocabulary if any(ch.isdigit() for ch in term)]
print(f"{len(with_digits)} of {len(vocabulary):,} terms contain a digit")
print("for example:", with_digits[:3])
```

```
579 of 1,543 terms contain a digit
for example: ['10', '10 days', '100044']
```

- `named_steps["tfidf"]` reaches the fitted vectorizer inside the pipeline (Chapter 36, section 36.9).
- `ch.isdigit()` is `True` for a digit character, and `any(...)` is `True` if at least one character of the term is a digit.

So the test is worth running: replace every run of digits with a placeholder, retrain, and compare.

```python
train_no_ids = train["body"].str.replace(r"\d+", "0", regex=True)
test_no_ids = test["body"].str.replace(r"\d+", "0", regex=True)
lr_no_ids = text_pipeline(LogisticRegression(max_iter=1000)).fit(
    train_no_ids, train["topic"]
)
pred_no_ids = lr_no_ids.predict(test_no_ids)
print(f"numbers replaced by 0: accuracy {(pred_no_ids == test['topic']).mean():.3f}")
print(f"original (numbers kept): accuracy {(test_pred == test['topic']).mean():.3f}")
```

```
numbers replaced by 0: accuracy 0.991
original (numbers kept): accuracy 0.991
```

- `.str.replace(r"\d+", "0", regex=True)` is Chapter 18's pattern replace (section 18.10): `\d` is any digit and `+` means "one or more", so `\d+` matches a whole number, and each one becomes `0`.
- The retrained pipeline sees the same text with every number made identical, so numbers can no longer tell the topics apart.

**Reading it.** The unchanged score says the model relies on words, not on which amounts or repeated order numbers happened to fall in which category. This is the text-classification version of Chapter 36's leakage check (section 36.7): before trusting a score, ask what the model could be secretly keying on.

> **When Naive Bayes and logistic regression are the right choice for text:** both are fast to train even with a huge vocabulary, both work well on sparse TF-IDF features, and both are still standard first choices for text classification at moderate scale. Naive Bayes is faster and simpler to explain; logistic regression usually edges it on accuracy and gives probabilities that are easier to calibrate (Chapter 39).

---

## 41.5 Sentiment analysis

### The lexicon approach

A **sentiment lexicon** is a dictionary of words with a polarity score, built by human annotation once and reused everywhere. **VADER** (Valence Aware Dictionary and sEntiment Reasoner) is tuned for informal text and handles negation ("not good") and intensifiers ("very good") with simple rules, needing no training data at all. It comes with NLTK, using the `vader_lexicon` file downloaded in section 41.0. First, one short sentence:

```python
from nltk.sentiment import SentimentIntensityAnalyzer

sia = SentimentIntensityAnalyzer()
print(sia.polarity_scores("the crate arrived broken"))
```

```
{'neg': 0.508, 'neu': 0.492, 'pos': 0.0, 'compound': -0.4767}
```

- `SentimentIntensityAnalyzer()` loads VADER's word list; `.polarity_scores(text)` scores one text and returns a dictionary.
- `neg`, `neu`, and `pos` are the shares of the text that read as negative, neutral, and positive; they add up to 1. Here "broken" makes about half the sentence negative.
- `compound` combines them into one score from −1 (most negative) to +1 (most positive). It's the one to use for a single verdict.

Now score every ticket, and compare the average score with the sentiment each ticket was labeled with:

```python
tickets["vader_score"] = tickets["body"].apply(
    lambda b: sia.polarity_scores(b)["compound"]
)
by_label = tickets.groupby("sentiment")["vader_score"].agg(["mean", "std"])
print(by_label.round(3).to_string())
```

```
             mean    std
sentiment
frustrated -0.345  0.325
neutral     0.218  0.286
positive    0.659  0.144
```

- `.apply(lambda b: ...)` runs the small function on every body (Chapter 18, section 18.6) and keeps the compound score.
- The `groupby` gives the mean and standard deviation of the score for each labeled sentiment.

The averages point the right way. To turn a score into a verdict, VADER's authors suggest a cut-off of ±0.05: below −0.05 is negative, above +0.05 positive, and in between neutral:

```python
lexicon_pred = pd.cut(
    tickets["vader_score"],
    bins=[-2, -0.05, 0.05, 2],
    labels=["frustrated", "neutral", "positive"],
)
agreement = (lexicon_pred.astype(str) == tickets["sentiment"]).mean()
print(f"lexicon-rule accuracy against the labeled sentiment: {agreement:.1%}")
```

```
lexicon-rule accuracy against the labeled sentiment: 62.6%
```

- `pd.cut` puts each score into a band (Chapter 18, section 18.5). `bins=[-2, -0.05, 0.05, 2]` lists the four edges, which make three bands: −2 to −0.05, −0.05 to 0.05, and 0.05 to 2. The outer edges, −2 and 2, are just edges wider than any possible score.
- `labels=[...]` names the three bands, in order, with the same words the tickets are labeled with.
- `.astype(str)` turns the bands into plain text so they can be compared with the labels.

Where does it go wrong? A cross-tabulation (`pd.crosstab`, Chapter 21, section 21.6) counts every combination of label and verdict; `rownames` and `colnames` just label its two sides:

```python
table = pd.crosstab(
    tickets["sentiment"], lexicon_pred, rownames=["labeled"], colnames=["lexicon says"]
)
print(table.to_string())
```

```
lexicon says  frustrated  neutral  positive
labeled
frustrated           774       92       122
neutral               87      564       816
positive               0        6       539
```

**Reading it.** The average VADER score does separate the three labeled sentiments in the right direction (−0.35, 0.22, 0.66), but turning that continuous score into a hard three-way call gets it right only **62.6%** of the time. The cross-tabulation shows why: 816 tickets labeled "neutral" get called "positive" by the lexicon, more than the 564 neutral tickets it gets right.

```python
worst = (tickets["sentiment"] == "neutral") & (lexicon_pred == "positive")
example = tickets[worst].iloc[0]
print(f"labeled: {example['sentiment']}   VADER score: {example['vader_score']:.2f}")
print(example["body"])
```

```
labeled: neutral   VADER score: 0.38
Dear team, could you clarify the invoice for order #108347? The amount Rs 2570 does not match what we discussed with the sales rep.
```

`worst` marks the tickets labeled neutral that the lexicon calls positive, and `.iloc[0]` takes the first of them.

**Reading it.** A routine billing query ("could you clarify the invoice... does not match...") scores +0.38, "positive", because VADER doesn't know that a mismatched invoice is a problem; it just doesn't contain any word its dictionary flags as negative, and dry, polite business language reads as mildly positive by VADER's general-purpose calibration. **A lexicon has no idea what your business considers bad news.** It also can't learn from your data.

### A trained classifier

The trained version needs nothing new: section 41.4's `text_pipeline`, with sentiment as the target instead of topic. One check first. The split was stratified by topic, not sentiment, so are the sentiments spread evenly between training and test?

```python
print(train["sentiment"].value_counts(normalize=True).round(3).to_string())
print(test["sentiment"].value_counts(normalize=True).round(3).to_string())
```

```
sentiment
neutral       0.490
frustrated    0.327
positive      0.183
sentiment
neutral       0.487
frustrated    0.336
positive      0.177
```

`normalize=True` gives shares again. The proportions are within a point of each other, so the split is fair for this task too.

```python
lr_sent = text_pipeline(LogisticRegression(max_iter=1000)).fit(
    train["body"], train["sentiment"]
)
pred_sent = lr_sent.predict(test["body"])
print(
    f"trained classifier accuracy: {(pred_sent == test['sentiment']).mean():.3f}   "
    f"macro F1 {f1_score(test['sentiment'], pred_sent, average='macro'):.3f}"
)
lexicon_test = lexicon_pred.loc[test.index].astype(str)
lexicon_accuracy = (lexicon_test == test["sentiment"]).mean()
print(f"lexicon rule accuracy (same test rows): {lexicon_accuracy:.3f}")
```

```
trained classifier accuracy: 0.996   macro F1 0.997
lexicon rule accuracy (same test rows): 0.615
```

- `train["sentiment"]` is the new target; everything else is the topic model's recipe.
- `lexicon_pred.loc[test.index]` picks the lexicon's verdicts for the same 750 test tickets, so the two scores are compared on the same rows.

**Reading it.** A logistic regression trained directly on labeled tickets reaches 99.6% accuracy, again inflated by the templated data (section 41.1), but the *comparison* is the honest and durable lesson: **a model trained on your own labels beats a generic lexicon by a wide margin**, because it learns which words and phrases mean trouble specifically in your context ("twice", "unacceptable", "immediately") rather than relying on a dictionary built for restaurant reviews and tweets.

> **When to use which.** A lexicon needs zero labeled data and works today; use it for a quick first pass or when you truly have no training examples. The moment you have even a few hundred labeled examples of your own text, a trained classifier is worth building, and it will keep improving as you label more.

---

## 41.6 Topic modeling

### Finding structure with no labels

**Topic modeling** discovers groups of words that tend to appear together, without being told any categories: the text equivalent of Chapter 38's clustering. The picture behind it is a factorization: one big table written, approximately, as two small tables multiplied together.

### Topics by hand

Add a fourth mini-document, "invoice amount wrong", and keep six words. The counts:

| | crate | arrived | broken | invoice | amount | wrong |
|---|---|---|---|---|---|---|
| doc 1 | 1 | 1 | 1 | 0 | 0 | 0 |
| doc 2 | 1 | 1 | 0 | 0 | 0 | 0 |
| doc 3 | 1 | 0 | 0 | 0 | 0 | 0 |
| doc 4 | 0 | 0 | 0 | 1 | 1 | 1 |

Now suppose there are two topics, "parcel" and "billing". A **topic–word table** says how strongly each topic uses each word, and a **document–topic table** says how much of each topic each document contains. First the topic–word table:

| Topic | crate | arrived | broken | invoice | amount | wrong |
|---|---|---|---|---|---|---|
| parcel | 1.0 | 0.7 | 0.3 | 0 | 0 | 0 |
| billing | 0 | 0 | 0 | 1.0 | 1.0 | 1.0 |

And the document–topic table:

| | parcel | billing |
|---|---|---|
| doc 1 | 1.0 | 0 |
| doc 2 | 1.0 | 0 |
| doc 3 | 0.8 | 0 |
| doc 4 | 0 | 1.0 |

Multiply them back, one cell at a time: doc 1's "arrived" ≈ parcel share × parcel's "arrived" + billing share × billing's "arrived" = 1.0 × 0.7 + 0 × 0 = **0.7**, against a real count of 1. Doc 4's "amount" ≈ 0 × 0 + 1.0 × 1.0 = **1.0**, exactly right. Two small tables (4 × 2 and 2 × 6, 20 numbers) stand in, approximately, for the 4 × 6 table of 24 counts. On 3,000 tickets and a thousand words the saving is enormous, and the two small tables are what you read: each topic's strongest words, and each document's mix of topics. A ticket such as "crate arrived broken, invoice wrong" would be about half parcel, half billing.

Two methods find such tables:

- **Latent Dirichlet Allocation (LDA)** treats each document as a mixture of topics (70% "damage" and 30% "delivery", say) and each topic as a list of word probabilities, fitted so the real word counts look as likely as possible. "Dirichlet" is just the name of the probability distribution LDA uses for those mixtures; you don't need its formula.
- **NMF** (non-negative matrix factorization) is the same picture with plain non-negative numbers instead of probabilities, fitted directly to the TF-IDF table. Chapter 42, section 42.4 uses the same factorization idea to recommend products.

### LDA

LDA models word counts, so it gets `CountVectorizer`, which counts without weighting:

```python
topic_vectorizer = CountVectorizer(
    stop_words="english", max_features=1000, min_df=5, token_pattern=r"\b[a-z]{3,}\b"
)
counts = topic_vectorizer.fit_transform(tickets["body"].str.lower())
words = topic_vectorizer.get_feature_names_out()
print(counts.shape)
```

```
(3000, 192)
```

- `token_pattern=r"\b[a-z]{3,}\b"` says what counts as a word: `\b` is a word boundary, and `[a-z]{3,}` is three or more lowercase letters. So numbers, and short scraps like "rs", are never counted.
- `max_features=1000` keeps at most the 1,000 most frequent words; `min_df=5` drops any word found in fewer than 5 tickets. The other settings are as in section 41.3.
- `counts.shape` is (tickets, words): 3,000 rows and a column for each of 192 words.

Fit five topics and print each topic's eight strongest words:

```python
from sklearn.decomposition import LatentDirichletAllocation

lda = LatentDirichletAllocation(n_components=5, random_state=41, max_iter=20)
lda.fit(counts)
for i, component in enumerate(lda.components_):
    top_words = [words[j] for j in component.argsort()[-8:][::-1]]
    print(f"LDA topic {i}: {', '.join(top_words)}")
```

```
LDA topic 0: order, late, days, need, update, shop, extremely, courier
LDA topic 1: order, invoice, team, gst, called, twice, dear, thanks
LDA topic 2: order, days, delivery, check, update, wanted, dispatch, share
LDA topic 3: order, disappointed, time, team, dear, board, container, unusable
LDA topic 4: order, units, bulk, just, page, tracking, reach, checking
```

- `n_components=5` asks for five topics; `random_state=41` fixes LDA's random start, so you get the same topics; `max_iter=20` is the number of passes over the data.
- `lda.fit(counts)` finds the two tables from the counts.
- `lda.components_` is the topic–word table: one row per topic, one column per word, a bigger number meaning the word is more typical of that topic.
- `component.argsort()` gives the word positions from the smallest number to the largest; `[-8:]` keeps the last eight, the largest; `[::-1]` reverses them so the strongest comes first.

Then give each ticket its most likely topic and cross-tabulate against the real categories:

```python
tickets["lda_topic"] = lda.transform(counts).argmax(axis=1)
print(pd.crosstab(tickets["topic"], tickets["lda_topic"]).to_string())
```

```
lda_topic          0    1    2    3    4
topic
Billing            0  558    2    0    0
Delivery         241  117  269  116  149
General Enquiry    0    3    2  281  228
Order Change      86  129  105   89    0
Product Defect   103    2  109  218  193
```

- `lda.transform(counts)` is the document–topic table: for every ticket, its share of each of the five topics.
- `.argmax(axis=1)` picks, for each ticket (each row), the position of its largest share: its most likely topic.

### NMF

NMF works on any table of non-negative numbers, and TF-IDF usually gives it cleaner topics than raw counts, so it gets `TfidfVectorizer` with the same settings:

```python
from sklearn.decomposition import NMF

nmf_vectorizer = TfidfVectorizer(
    stop_words="english", max_features=1000, min_df=5, token_pattern=r"\b[a-z]{3,}\b"
)
tfidf_counts = nmf_vectorizer.fit_transform(tickets["body"].str.lower())
nmf = NMF(n_components=5, random_state=41, max_iter=400).fit(tfidf_counts)
nmf_words = nmf_vectorizer.get_feature_names_out()
for i, component in enumerate(nmf.components_):
    top_words = [nmf_words[j] for j in component.argsort()[-8:][::-1]]
    print(f"NMF topic {i}: {', '.join(top_words)}")

tickets["nmf_topic"] = nmf.transform(tfidf_counts).argmax(axis=1)
print(pd.crosstab(tickets["topic"], tickets["nmf_topic"]).to_string())
```

```
NMF topic 0: order, units, bulk, dear, team, disappointed, quantity, drum
NMF topic 1: check, dispatch, share, status, update, wanted, days, order
NMF topic 2: invoice, gst, team, copy, accounts, requesting, extra, shows
NMF topic 3: reach, page, tracking, checking, updated, just, days, order
NMF topic 4: called, twice, delivered, acceptable, account, times, charged, deducted
nmf_topic          0    1    2    3    4
topic
Billing            0    3  449    0  108
Delivery         205  316    0  255  116
General Enquiry  406    5   26   77    0
Order Change     401    8    0    0    0
Product Defect   527   61    0    0   37
```

Every line has an LDA twin above; `max_iter=400` gives NMF's fitting more steps.

![Two heat maps side by side, LDA on the left and NMF on the right, each crossing the five real ticket categories (rows) against five discovered topics (columns), with each cell showing the share of that category's tickets in the topic, and each topic's strongest words listed underneath. Neither method matches the five categories one to one](figures/fig41-1-topic-models.svg)

*Figure 41.1 — LDA and NMF topics, and how each maps onto the five real categories. Each row shows where one category's tickets went. Neither method rediscovers the official five: both split and merge them by wording and tone.*

**Reading it, honestly, as Chapter 38 taught.** Neither method's five topics line up with the five real categories. LDA topic 1 ("invoice, team, gst, called, twice") is the nearest to a match: it takes 558 of the 560 Billing tickets, but also 129 Order Change and 117 Delivery tickets, wherever customers wrote "called twice" or "dear team". NMF topic 4 ("called, twice, delivered, acceptable, charged, deducted") is angry Billing *and* angry Delivery tickets bundled together by their frustrated vocabulary, not by subject. And NMF topic 0 swallows 1,539 of the 3,000 tickets, including 527 of the 625 Product Defect and 401 of the 409 Order Change tickets. A **catch-all topic** like that is a common sign that the vocabulary or the number of topics needs work.

**The topics found are real** (there genuinely is a cluster of "curt, angry, wants action now" language cutting across categories), **but they aren't the five categories a support manager already has**, and no amount of tuning would necessarily make them line up, because nothing told the algorithm those five categories exist. This is the exact caution from Chapter 38, section 38.2: an internal, algorithm-driven grouping is not automatically the grouping a business already uses.

### Checking a topic against something it never saw

Chapter 38's other habit: test a discovered group against information the algorithm didn't use. NMF topic 4 reads like customers who are writing again. The topic model never saw `order_id`, so check it: how many tickets in each topic follow an earlier ticket about the same order?

```python
in_date_order = tickets.sort_values(["created_at", "ticket_id"])
tickets["second_contact"] = in_date_order["order_id"].duplicated()
summary = tickets.groupby("nmf_topic")["second_contact"].agg(["sum", "count", "mean"])
print(summary.round(2).to_string())
print(f"all tickets: {tickets['second_contact'].mean():.0%} are second contacts")
```

```
           sum  count  mean
nmf_topic
0          290   1539  0.19
1           34    393  0.09
2          137    475  0.29
3           40    332  0.12
4          139    261  0.53
all tickets: 21% are second contacts
```

- `sort_values(["created_at", "ticket_id"])` puts the tickets in the order they arrived.
- `.duplicated()` (Chapter 18, section 18.10) is `True` for a ticket whose `order_id` already appeared on an earlier row: a second (or later) contact about the same order.
- Assigning the result back to `tickets` lines the rows up by their index labels, so each ticket gets its own flag even though the sorted table is in a different order.
- In the summary, `sum` counts the second contacts in each topic, `count` counts its tickets, and `mean` is the share.

**Reading it.** More than half of NMF topic 4's tickets are second contacts, against about one in five across all tickets. The topic found a real pattern, and a check on data it never saw confirms it. The real-world story at the end of this chapter shows what a support team can do with that.

**What topic modeling is actually good for**, given all this: discovering categories nobody has named yet ("a cluster of angry, repeat-contact language" is itself useful information for staffing an escalations queue), a first pass on genuinely unlabelled data before anyone builds a taxonomy, and a sanity check on whether your existing categories capture what people are actually writing about. It's a poor substitute for labeled classification when good labels already exist, as they do here.

---

## 41.7 Word embeddings: the bridge to LLMs

### From counting words to placing them

TF-IDF treats every word as an unrelated column: "broken" and "damaged" share no similarity at all unless they appear in the same documents. A **word embedding** instead gives every word a short list of numbers (a vector) such that words used in similar places end up with similar numbers, whether or not they ever appear in the same document.

> **Neighbours by hand.** Four tiny sentences: "crate arrived broken", "crate arrived damaged", "invoice amount wrong", "invoice amount incorrect". For each word, count its **context**: the words right next to it (one word either side).
>
> | Word | crate | arrived | invoice | amount |
> |---|---|---|---|---|
> | broken | 0 | 1 | 0 | 0 |
> | damaged | 0 | 1 | 0 | 0 |
> | wrong | 0 | 0 | 0 | 1 |
> | incorrect | 0 | 0 | 0 | 1 |
>
> "Broken" and "damaged" never appear in the same sentence, yet their rows are identical, so their cosine similarity is 1. "Broken" and "wrong" share no neighbour: cosine 0. Words are known by the company they keep.

**Word2vec** learns a compressed version of this neighbour table. It gives every word a short list of numbers, starts them at random, and nudges them, pass after pass, so that each word's numbers get better at predicting the words around it. After many passes, words used in similar places end up with similar numbers. (The nudging is done by a very small neural network; Chapter 43 introduces neural networks.)

Word2vec reads each ticket as a list of words. Python's `re` module (short for *regular expressions*, the patterns from Chapter 18, section 18.10) splits a ticket into its runs of letters:

```python
import re

sentences = [re.findall(r"[a-z]+", body.lower()) for body in tickets["body"]]
print(len(sentences), "tickets; the first as words:")
print(sentences[0])
```

```
3000 tickets; the first as words:
['dear', 'team', 'could', 'you', 'clarify', 'the', 'invoice', 'for', 'order', 'the', 'amount', 'rs', 'does', 'not', 'match', 'what', 'we', 'discussed', 'with', 'the', 'sales', 'rep']
```

- `import re` loads the module; it comes with Python, so there's nothing to install.
- `re.findall(pattern, text)` returns every piece of the text that matches the pattern. `[a-z]+` is "one or more lowercase letters in a row", so each word becomes one item and numbers and punctuation are skipped.

Now train a model on the 3,000 tickets:

```python
from gensim.models import Word2Vec

model = Word2Vec(sentences, vector_size=50, window=5, min_count=5, seed=41, workers=1)
print(f"vocabulary size: {len(model.wv):,} words")
```

```
vocabulary size: 283 words
```

- `vector_size=50`: how many numbers each word gets.
- `window=5`: how many words either side count as a word's context (the by-hand table used 1).
- `min_count=5`: words that appear fewer than 5 times are ignored; there's too little evidence to place them.
- `seed=41` and `workers=1`: the same random start, and one worker thread doing the passes in a fixed order, so you get the same result every run. With more workers the training is faster but the order, and so the result, changes a little from run to run.
- `model.wv` is the trained word-vector table, and `len(model.wv)` counts the words in it.

Which words sit closest to "broken", "invoice", and "order"?

```python
for word in ["broken", "invoice", "order"]:
    print(f"\nwords used most like '{word}':")
    for neighbor, score in model.wv.most_similar(word, topn=5):
        print(f"  {neighbor:<14} {score:.3f}")
```

```

words used most like 'broken':
  completely     0.990
  right          0.941
  received       0.939
  is             0.897
  down           0.890

words used most like 'invoice':
  shows          0.933
  amount         0.927
  rs             0.900
  accounts       0.899
  wrong          0.863

words used most like 'order':
  orer           0.624
  could          0.617
  for            0.595
  t              0.587
  invoice        0.575
```

`most_similar(word, topn=5)` returns the five words whose vectors have the highest cosine similarity with the word's vector, with those similarities.

**Reading it.** With only 3,000 short tickets, this is a small, illustrative model, not a production one (real word2vec models train on billions of words). Even so, the neighbors it finds for "broken" (*completely*, *right*, *received*, *down*, and even *is*, a sign of how small the model is) and for "invoice" (*shows*, *amount*, *rs*, *accounts*, *wrong*) are words that genuinely keep company with those ideas in this dataset: "completely broken, there is a crack right down the middle" is one of the templates. "Order"'s neighbors are weaker and noisier, including typos like *orer*, because "order" appears in nearly every ticket regardless of topic and so has less distinctive context to learn from.

### Seeing the space

Fifty numbers per word can't be drawn, but Chapter 35's PCA (section 35.10) can squeeze them down to two, the two directions that keep the most of the spread:

```python
from sklearn.decomposition import PCA

vocab_words = [
    "broken", "crack", "damaged", "invoice", "gst", "refund", "delivery", "dispatch",
    "tracking", "order", "cancel", "address", "bulk", "pricing", "catalogue",
]
vectors = np.array([model.wv[w] for w in vocab_words])
coords = PCA(n_components=2, random_state=41).fit_transform(vectors)
for word, (x, y) in zip(vocab_words, coords):
    print(f"{word:<12} {x:>6.2f} {y:>6.2f}")
```

```
broken         2.54   2.99
crack          3.62   2.51
damaged        2.52  -2.64
invoice       -3.30  -1.10
gst           -3.48  -1.64
refund         2.93  -3.04
delivery      -1.08   1.96
dispatch       0.50  -3.36
tracking       0.76  -1.49
order         -0.69  -0.63
cancel        -1.06   1.26
address       -1.85   3.14
bulk          -1.03   0.35
pricing       -2.15   0.38
catalogue      1.78   1.33
```

- `model.wv[w]` is one word's 50 numbers; `np.array([...])` stacks the fifteen into a 15 × 50 table.
- `PCA(n_components=2)` finds the two directions, and `.fit_transform` gives each word its two coordinates.
- `zip(vocab_words, coords)` pairs each word with its coordinates, and `(x, y)` unpacks the pair.
- The list spells "catalogue" the way the tickets do; a word the model never saw, such as "catalog", would raise a `KeyError`.

![A scatter of fifteen ticket words placed by the first two principal components of their word2vec vectors, with defect words, billing words and delivery words marked by different shapes and a legend, and each group lying in its own region](figures/fig41-2-word-embeddings.svg)

*Figure 41.2 — Fifteen ticket words, placed by the first two principal components of their embeddings. Shape and colour mark each word's group by meaning (see the key); the model was never told the groups. Words used in the same kind of sentence land near each other.*

**Reading it, with Chapter 38's caution firmly in mind.** The key groups the words by meaning, and the model was never told those groups. Most of them hold together: *broken* and *crack* land side by side, as do *invoice* and *gst*. Where a word strays, the templates explain it. *Refund* sits next to *damaged*, because the tickets that use it say "arrived damaged and unusable. Please refund"; *delivery* sits with *address* and *cancel*, because it mostly appears in "change the delivery address"; and *dispatch* and *tracking* are not especially close. Word2vec learns how words are *used* in this dataset, not what a dictionary says they mean. It's still a PCA plot of a small model: don't read exact distances, and expect a bigger corpus to sharpen these clusters further.

This is precisely the idea, scaled up enormously and made contextual (so "crate" gets a different vector depending on whether it's near "broken" or near "delivered"), behind the embeddings inside every modern large language model. Chapter 54 picks this up directly: the dot product between two length-1 embeddings is exactly the cosine similarity from section 41.3, and it's the mechanism behind both this chapter's "find similar tickets" and an LLM's attention.

---

## Common mistakes

| Mistake | Symptom | Fix |
|---|---|---|
| Not deciding on a cleaning pipeline deliberately | Different results every time someone reruns it | Fix and document tokenization, stop words, and stemming/lemmatization choices |
| Removing stop words before checking the task | Sentiment or negation breaks ("not good" loses "not") | Check what the task needs; some stop words carry meaning |
| Cleaning new text differently from training text | Model accuracy drops on live data; words unseen | Put all cleaning inside the pipeline so fit and predict share it |
| Trusting near-perfect classification scores | 99%+ accuracy on messy real-world text | Check for templated or duplicated text; expect real text to score lower |
| Reading a confusion matrix without reading the errors | Missing the pattern in what's misclassified | Read a sample of the actual misclassified documents |
| Using a lexicon for domain-specific sentiment | "Positive" score on a billing complaint | Train a classifier on your own labeled examples once you have some |
| Assuming discovered topics match known categories | Confusion when LDA topics "don't make sense" | Cross-tabulate against known labels; report what was actually found |
| Picking the number of topics arbitrarily | Topics that are too broad or too fragmented | Try several counts; judge by whether a person can name each topic |
| Treating TF-IDF or word2vec vectors as ground truth similarity | Overconfident "these two tickets are duplicates" claims | Use similarity as a ranking signal, not a certainty |
| Training word embeddings on too little text | Noisy, unstable neighbor words | Use pretrained embeddings for small corpora, or expect noise |
| Forgetting to fit the vectorizer only on training data | Leakage of test vocabulary into training | Fit `TfidfVectorizer` inside a pipeline, same as any other transformer (Chapter 36) |

---

## In the real world: the topics nobody had named

In August 2026, Riverstone's support lead, Priya Menon, asks Meera for "a report on what customers are actually complaining about", beyond the five categories the ticketing system forces every agent to pick from.

Meera runs both approaches from this chapter. The classification model into the five official topics works fine and isn't the interesting part; Priya already has that dashboard. The topic model is what she was actually asking for, and Meera is careful with how she presents it, because Chapter 38's lesson applies directly here too: an unsupervised result is a hypothesis, not a finding, until it's checked against something real.

The topic model's most distinct cluster isn't about any product category. It's a cluster of short, curt, action-demanding language, "called", "twice", "acceptable", "charged", "deducted", cutting across Delivery, Billing, and Product Defect tickets alike. Meera pulls fifty of those tickets and reads them by hand (the check no algorithm replaces). Many of them *are* a real pattern: customers who have already contacted support about the same order and are writing again. Others are complaints about being charged twice, pulled in by the same word.

That's not one of the five topics. It's a **repeat-contact rate**, hiding inside every category. Meera checks it against something the topic model never saw, whether the ticket's `order_id` already appeared on an earlier ticket, exactly as section 41.6 did: in that cluster, 139 of 261 tickets (53%) are second contacts, against 21% across all tickets.

Her report to Priya doesn't recommend a sixth category in the ticketing system. It recommends a repeat-contact flag, shown to agents the moment a second ticket comes in on the same order, and a weekly count of how many tickets are second contacts, as a service-quality metric in its own right. The topic model didn't answer Priya's question by handing her clean labels; it pointed at a question worth asking with a much simpler, more reliable check.

---

## Project: classify and summarize Riverstone support tickets by topic

**Goal:** a working ticket classifier, an honest sentiment comparison, and a topic-discovery pass that finds something the official categories miss.

### Tools you'll need

- **NLTK** 3.10.3 (`python -m pip install nltk`, then `nltk.download(...)` once for `punkt_tab`, `stopwords`, `wordnet`, `omw-1.4`, and `vader_lexicon`, as in section 41.0): tokenization, stop words, stemming, lemmatization, VADER sentiment.
- **scikit-learn** 1.9.1: `CountVectorizer`, `TfidfVectorizer`, `MultinomialNB`, `LogisticRegression`, `LatentDirichletAllocation`, `NMF`, `cosine_similarity`, `PCA`; the same library used in Chapters 36–39, now applied to text.
- **gensim** 4.4.0 (`python -m pip install gensim`): `Word2Vec`.
- Not used here but worth knowing for production text work: **spaCy** (faster, more modern tokenization and lemmatization, named-entity recognition), **sentence-transformers** (pretrained sentence embeddings, far stronger than a word2vec model trained on 3,000 tickets), and **Hugging Face transformers** (pretrained classifiers and modern language models, Chapter 54).
- The outputs in this chapter were produced on one CPU core with Python 3.11, pandas 3.0.6, NumPy 2.4.6, scikit-learn 1.9.1, NLTK 3.10.3, and gensim 4.4.0, on 29 September 2026.
- **Companion files:** `companion/generate_riverstone_tickets.py` builds `companion/tickets/tickets.csv` (seeds 20241 and 20242). Run the chapter's code from `companion/tickets/`, as set up in section 41.0.

**Option A: your own text.** Any collection of short documents with at least one label you can check against: emails, reviews, survey responses.

**Option B: Riverstone.** The support tickets.

**Steps:**

1. **Clean deliberately.** Choose and justify your tokenization, stop-word, and stemming/lemmatization settings in two sentences.
2. **Build TF-IDF** and show, by hand, the tf, idf, and tf-idf for two words in one document.
3. **Classify** the topic with Naive Bayes and logistic regression. Report accuracy, macro F1, and the confusion matrix, and read three misclassified examples aloud (on paper) — what do they have in common?
4. **Check for an inflated score** the way section 41.4 did: does the result survive removing an obvious shortcut (IDs, a distinctive template phrase, whatever your data's version is)?
5. **Sentiment, two ways:** score every document with a lexicon and with a classifier trained on your own labels (or a proxy, like a star rating). Compare accuracy and read two disagreements.
6. **Topic model** with LDA or NMF at two or three different numbers of topics. For each, name every topic in five words or fewer, and say whether a person could actually use the result.
7. **Cross-tabulate** discovered topics against any known label and report the honest match, good or bad.
8. **Word vectors:** train a small word2vec model (or load a pretrained one if your corpus is small) and show five word-neighbor examples that make sense and one that doesn't.
9. **Write a one-page summary** for a non-technical reader: what the classifier does, how reliable the sentiment score is, and one thing the topic model found that a fixed category list would have missed.

**Stretch goals:**

- Compare the classifier with and without **bigrams** (`ngram_range=(1, 1)` against `(1, 2)`) and see whether phrases like "not good" or "second time" change accuracy or the confusion matrix.
- Try **spaCy** for lemmatization and compare its output with NLTK's on five tricky words.
- Use `sentence-transformers` to embed whole tickets (not just words) and compare its nearest-neighbor tickets with section 41.3's TF-IDF ones.
- Fit LDA with 3, 5, 8, and 12 topics and plot a simple coherence or perplexity curve alongside your own judgment of which count gives the most nameable topics.

---

## Recap

- Text becomes usable data through **cleaning**: lowercasing, **tokenization**, optional stop-word removal, and **stemming** or **lemmatization**. Every choice is a modeling decision.
- **Bag of words** counts words per document, ignoring order; **TF-IDF** reweights those counts by how distinctive each word is across the collection, and documents become comparable with **cosine similarity**.
- **Text classification** reuses Naive Bayes and logistic regression, fed TF-IDF features; evaluate it with the same confusion-matrix habits as any classifier, scoring each class one-vs-rest and averaging with **macro F1**, and be suspicious of scores that look too good.
- **Lexicon-based sentiment** (VADER) needs no training data and doesn't know your business; a **trained sentiment classifier** learns your specific language and beats a generic lexicon once you have labels.
- **Topic modeling** (LDA, NMF) factorizes the document–word table into topics with no labels; check discovered topics against real categories, and against data they never saw, before trusting them, and expect them to find something different, not confirm what you already know.
- **Word embeddings** place words in space so that similar usage means nearby vectors, extending TF-IDF's simple co-occurrence counting; this idea, scaled up, underlies modern language models.

---

## Key terms

unstructured text · token · tokenization · stop words · stemming · Porter stemmer · lemmatization · lemma · part of speech · bag of words · vocabulary · term frequency (TF) · document frequency · inverse document frequency (IDF) · TF-IDF · row normalization · cosine similarity (text) · n-gram · bigram · multinomial Naive Bayes · Laplace smoothing · text classification · softmax · confusion matrix (multi-class) · one-vs-rest · macro average · weighted average · support · macro F1 · sentiment analysis · sentiment lexicon · VADER · polarity score · compound score · trained sentiment classifier · topic modeling · factorization · Latent Dirichlet Allocation (LDA) · non-negative matrix factorization (NMF) · document-topic distribution · topic-word distribution · catch-all topic · repeat contact · word embedding · word2vec · context window · nearest neighbors (embedding space) · pretrained embeddings

*(All terms are defined in the Glossary, Appendix A.)*

---

## Check yourself

- [ ] I can tokenize text and explain what stop-word removal, stemming, and lemmatization each do and don't do.
- [ ] I can build a bag-of-words table and a TF-IDF table by hand for a handful of short documents.
- [ ] I can explain in one sentence why TF-IDF downweights common words.
- [ ] I can score a short text with multinomial Naive Bayes by hand, including the +1 smoothing.
- [ ] I train a text classifier with the same evaluation habits as any other model: confusion matrix, per-class metrics, macro and weighted averages, and a look at the actual errors.
- [ ] I'm suspicious of near-perfect text classification scores and know what to check.
- [ ] I know a sentiment lexicon needs no training data and no idea what my business considers bad news, and I know when a trained classifier is worth the labelling effort.
- [ ] I can run LDA or NMF, and I check discovered topics against known labels before claiming they mean something.
- [ ] I can explain what a word embedding captures that TF-IDF can't, and I don't over-read a small model's results.
- [ ] I see the line from cosine similarity (Chapter 35) through TF-IDF and word2vec to what an LLM does with text (Chapter 54).

---

## Exercises

Code exercises run in the chapter's notebook, from `companion/tickets/`, after the chapter's code (they use `tickets`, `train`, `test`, `text_pipeline`, `lr_topic`, `test_pred`, `lexicon_pred`, `pred_sent`, `counts`, `words`, `lda`, `sentences`, `model` [the word2vec model], and the rest). Predict each answer before running it.

### Warm-up

1. *(hand)* Tokenize and lowercase: "Order #4471 hasn't arrived — 3 days late!" List the tokens, then list what remains after removing punctuation and stop words.
2. *(hand)* A word appears in 2 of 10 documents. Using scikit-learn's formula, idf = ln((1 + N) ÷ (1 + df)) + 1, compute its idf. Now compute it for a word in 9 of 10 documents. Which word gets more weight in a document where both appear once?
3. *(hand)* Two short reviews: "not good, would not buy again" and "good, would buy again". As bag-of-words with no stop-word removal, are their vectors identical, similar, or very different? What changes if you remove NLTK's stop words first? What does that reveal about bag-of-words and negation?
4. Which tool fits each job: (a) you have 200 labeled examples of spam and not-spam; (b) you have 50,000 unlabelled product reviews and want to know what people write about; (c) you need a same-day sentiment score with zero labeled data; (d) you want to find tickets similar to one a customer just sent?

### Core

5. Rebuild the classifier using **stemmed** text (apply the Porter stemmer to every ticket before vectorizing) instead of raw words. Does accuracy change? Does the vocabulary size?
6. Rebuild the TF-IDF vectorizer **without** removing stop words and **without** limiting `max_features`. Compare vocabulary size and accuracy with the original. Is bigger always better here?
7. For the sentiment task, compute precision and recall **per class** (frustrated, neutral, positive) for both the lexicon rule and the trained classifier. Which class does the lexicon fail hardest on, and why does that match what section 41.5 found?
8. Fit LDA with 3 topics and with 8 topics instead of 5. For each, read the top words of every topic and say in one sentence whether the topics are more or less nameable than at 5.
9. Find the ticket with the **lowest** maximum topic probability from the LDA model (the one LDA is least sure how to categorize). Read it. Does it read as genuinely ambiguous?
10. Using the word2vec model, find the five nearest neighbors of "late" and "refund". Are they more or less coherent than "order"'s neighbors from the chapter? Why might that be?

### Stretch

11. Build a classifier using **only bigrams** (`ngram_range=(2, 2)`) instead of single words plus bigrams. Compare accuracy with the original `(1, 2)` version.
12. Train the word2vec model with `vector_size=10` and with `vector_size=100`, keeping everything else fixed. Compare the neighbors of "broken" for each. What trade-off does vector size control?
13. Combine TF-IDF features with two numeric features (`resolution_hours`, ticket length) using `ColumnTransformer`, and see whether sentiment classification improves.

### Think about it

14. A manager sees your topic model's five topics and asks, "why doesn't this match our five support categories?" Answer in three sentences.
15. Your sentiment classifier scores 99% on held-out tickets from the same period it was trained on. Six months later, on new tickets, it performs much worse. Give two explanations rooted in this chapter and Chapter 36.
16. Someone proposes using cosine similarity between TF-IDF vectors to automatically merge "duplicate" support tickets above a threshold. What could go wrong, and what would you check before turning it on?

---

## Answers

*(Every calculation was checked, and every code output shown is real.)*

**1.** Tokens (lowercased): `order`, `#`, `4471`, `has`, `n't`, `arrived`, `—`, `3`, `days`, `late`, `!`. (NLTK's tokenizer splits contractions like "hasn't" into `has` and `n't`.) After removing punctuation, numbers, and stop words: `order`, `arrived`, `days`, `late` — "hasn't" is lost entirely, which is exactly the negation problem section 41.3 flags: the sentence went from "hasn't arrived" (bad) to a bag of words that reads neutral.

**2.** idf for the word in 2 of 10: ln(11 ÷ 3) + 1 = ln(3.667) + 1 = 1.299 + 1 = **2.299**. For the word in 9 of 10: ln(11 ÷ 10) + 1 = ln(1.1) + 1 = 0.095 + 1 = **1.095**. The rarer word gets more than twice the weight of the common one for the same single occurrence — TF-IDF is doing exactly what it's meant to.

**3.** Without stop-word removal, the vocabulary is *again, buy, good, not, would*, and the two reviews' counts are [1, 1, 1, 2, 1] and [1, 1, 1, 0, 1]: they differ only in "not" (2 against 0). Cosine similarity = (1 + 1 + 1 + 0 + 1) ÷ (√8 × √4) = 4 ÷ 5.657 = **0.71**, "fairly similar" for opposite meanings. Remove NLTK's stop words and "not" disappears (so does "again", also on the list): both reviews become *good, would, buy*, and their vectors are **identical**. Bag-of-words can't attach "not" to "good"; bigrams ("not good" as its own feature, section 41.4) or models that read sequences (Chapter 54) can.

**4.** (a) **A trained classifier** (Naive Bayes or logistic regression on TF-IDF): you have labels, so use them. (b) **Topic modeling** (LDA or NMF): no labels, and the goal is discovery, not prediction. (c) **A sentiment lexicon** like VADER: zero labeled data and speed are the priority; accept the accuracy trade-off from section 41.5. (d) **TF-IDF plus cosine similarity** (section 41.3): a direct similarity search needs no training at all.

**5.** The stemming function reuses section 41.2's cleaning: tokenize, keep only words, stem each one.

```python
def stem_text(text):
    tokens = word_tokenize(text.lower())
    return " ".join(stemmer.stem(t) for t in tokens if t.isalpha())


print(stem_text(tickets.loc[0, "body"]))
train_stemmed = train["body"].apply(stem_text)
test_stemmed = test["body"].apply(stem_text)
lr_stemmed = text_pipeline(LogisticRegression(max_iter=1000)).fit(
    train_stemmed, train["topic"]
)
pred_stemmed = lr_stemmed.predict(test_stemmed)
vocab_stemmed = lr_stemmed.named_steps["tfidf"].vocabulary_
vocab_original = lr_topic.named_steps["tfidf"].vocabulary_
stemmed_accuracy = (pred_stemmed == test["topic"]).mean()
original_accuracy = (test_pred == test["topic"]).mean()
print(f"stemmed:  accuracy {stemmed_accuracy:.3f}   vocabulary {len(vocab_stemmed):,}")
print(f"original: accuracy {original_accuracy:.3f}   vocabulary {len(vocab_original):,}")
```

```
dear team could you clarifi the invoic for order the amount rs doe not match what we discuss with the sale rep
stemmed:  accuracy 0.991   vocabulary 1,022
original: accuracy 0.991   vocabulary 1,543
```

This time the vocabulary **shrinks**, from 1,543 terms to 1,022, because stemming folds related word forms together (*clarify* becomes `clarifi`, *invoice* `invoic`, *discussed* `discuss`). Accuracy doesn't move: this data's topics are already easy to separate, so there's no room to improve. On a harder, less templated problem, that folding usually helps more, by letting the model generalize from a form it saw in training ("delivered") to one it didn't ("delivering"). Note that the stemmed stop words (`doe` for *does*) no longer match the vectorizer's stop-word list, so a few of them survive as features; a careful pipeline removes stop words before stemming.

**6.** Only the two settings the question names change: the stop-word list and the `max_features` cap are removed, while word pairs and `min_df=2` stay.

```python
wide_pipeline = Pipeline(
    [
        ("tfidf", TfidfVectorizer(ngram_range=(1, 2), min_df=2)),
        ("model", LogisticRegression(max_iter=1000)),
    ]
)
wide_pipeline.fit(train["body"], train["topic"])
wide_pred = wide_pipeline.predict(test["body"])
wide_vocab = wide_pipeline.named_steps["tfidf"].vocabulary_
wide_accuracy = (wide_pred == test["topic"]).mean()
print(f"no stop-word list, no cap: vocabulary {len(wide_vocab):,}   accuracy {wide_accuracy:.3f}")
print(f"original:                  vocabulary {len(vocab_original):,}   accuracy {original_accuracy:.3f}")
```

```
no stop-word list, no cap: vocabulary 1,823   accuracy 0.991
original:                  vocabulary 1,543   accuracy 0.991
```

Without the stop-word list and the cap, the vocabulary grows by about a fifth (1,823 terms against 1,543), because every stop word, and every pair containing one, becomes a feature. Accuracy doesn't improve: those extra features are noise for this task, not signal. Bigger isn't automatically better: more features mean more chances to fit noise and a slower, harder-to-explain model, so stop-word removal and a sensible cap are usually worth keeping unless a specific test shows they're costing you accuracy.

**7.** Each class is scored one-vs-rest, as in section 41.4: `said` marks the tickets given that label, `true` the tickets that really have it, and `precision_score(true, said)` and `recall_score(true, said)` apply Chapter 39's formulas to the two sets of `True`/`False` values. The lexicon is scored on all 3,000 tickets (it learned nothing from them); the classifier on the 750 test tickets.

```python
from sklearn.metrics import precision_score, recall_score

for label in ["frustrated", "neutral", "positive"]:
    said = lexicon_pred.astype(str) == label
    true = tickets["sentiment"] == label
    print(
        f"{label:<12} lexicon    precision {precision_score(true, said):.3f}   "
        f"recall {recall_score(true, said):.3f}"
    )
for label in ["frustrated", "neutral", "positive"]:
    said = pred_sent == label
    true = test["sentiment"] == label
    print(
        f"{label:<12} classifier precision {precision_score(true, said):.3f}   "
        f"recall {recall_score(true, said):.3f}"
    )
```

```
frustrated   lexicon    precision 0.899   recall 0.783
neutral      lexicon    precision 0.852   recall 0.384
positive     lexicon    precision 0.365   recall 0.989
frustrated   classifier precision 1.000   recall 0.988
neutral      classifier precision 0.992   recall 1.000
positive     classifier precision 1.000   recall 1.000
```

The lexicon's worst class is **neutral**: its recall is only 0.384, because, as section 41.5 showed, polite factual language reads as mildly positive to a general-purpose dictionary, so most truly neutral tickets get called positive instead. That's also why the lexicon's *positive* precision is so low (0.365): its positive pile is mostly neutral tickets. The trained classifier's precision and recall are all near 1.0 across every class, again inflated by the templated data, but the *pattern* — the lexicon struggling specifically on neutral — matches the cross-tabulation exactly and would likely persist on real, less templated text.

**8.**

```python
for k in [3, 8]:
    lda_k = LatentDirichletAllocation(n_components=k, random_state=41, max_iter=20)
    lda_k.fit(counts)
    print(f"\n--- LDA with {k} topics ---")
    for i, component in enumerate(lda_k.components_):
        top = [words[j] for j in component.argsort()[-8:][::-1]]
        print(f"topic {i}: {', '.join(top)}")
```

```

--- LDA with 3 topics ---
topic 0: order, days, just, extremely, dear, team, want, good
topic 1: order, invoice, team, gst, days, dear, called, twice
topic 2: order, update, bulk, team, dear, check, quantity, units

--- LDA with 8 topics ---
topic 0: order, good, time, say, piece, came, appreciate, wanted
topic 1: order, invoice, called, twice, days, team, dear, shows
topic 2: order, days, check, update, wanted, dispatch, share, status
topic 3: order, units, dear, team, soon, range, steps, really
topic 4: bin, storage, order, just, days, page, tracking, reach
topic 5: order, late, need, update, shop, extremely, courier, escalate
topic 6: order, gst, team, quantity, bulk, invoice, accounts, copy
topic 7: order, placing, want, variants, catalogue, sizes, compare, new
```

At 3 topics, the categories are squeezed into three broad buckets: topic 1 is billing with the "called twice" complaints mixed in, and topics 0 and 2 are vague blends ("days, just, extremely"; "update, bulk, check, quantity") that no support manager could name as one thing. At 8, some topics become sharper and nameable — topic 5 is angry late-delivery tickets ("late, courier, escalate"), topic 7 is catalogue requests ("variants, catalogue, sizes, compare") — but others split on accidents of wording: topic 4 is held together by "storage bin", one product name. 5, as used in the chapter, isn't obviously "correct" either; the right number is a judgment call, made by reading the topics, not a number a formula hands you.

**9.**

```python
topic_probs = lda.transform(counts)
least_confident = topic_probs.max(axis=1).argmin()
print(f"max topic probability: {topic_probs[least_confident].max():.3f}")
print(f"true topic: {tickets.loc[least_confident, 'topic']}")
print(tickets.loc[least_confident, "body"])
```

```
max topic probability: 0.355
true topic: Delivery
The chopping board was fine but the delivery was late and the invoice amount looks off, please check.
```

The least-confident ticket (its top topic gets only 0.355) is one of the planted mixed tickets from section 41.4: it talks about a product, a late delivery, and an invoice at once, so LDA spreads it across several topics. LDA's uncertainty here reflects a document that genuinely belongs to more than one topic — the same conclusion a human reading it would reach. Tickets like this are the ones to route to a person.

**10.**

```python
for word in ["late", "refund"]:
    print(f"\nneighbors of '{word}':")
    for neighbor, score in model.wv.most_similar(word, topn=5):
        print(f"  {neighbor:<14} {score:.3f}")
```

```

neighbors of 'late':
  unhappy        0.969
  courier        0.853
  no             0.840
  update         0.810
  extremely      0.794

neighbors of 'refund':
  account        0.914
  unacceptable   0.883
  immediately    0.862
  unusable       0.849
  arived         0.827
```

"Late" and "refund" each appear in a narrower set of contexts than the near-universal "order", so their neighbor lists are more topically coherent: "late" surrounds itself with delivery-frustration words (*unhappy*, *courier*, *extremely*), and "refund" with defect-and-billing complaint words (*unacceptable*, *immediately*, *unusable*), plus *arived*, a typo of a word it keeps company with. "Order" appears in almost every template regardless of topic, giving it a broad, low-signal context that produces noisier, less thematic neighbors, exactly as the chapter noted.

**11.** The same pipeline as `text_pipeline`, written out so the vectorizer can take `ngram_range=(2, 2)`.

```python
bigram_only = Pipeline(
    [
        (
            "tfidf",
            TfidfVectorizer(
                stop_words="english", max_features=3000, ngram_range=(2, 2), min_df=2
            ),
        ),
        ("model", LogisticRegression(max_iter=1000)),
    ]
)
bigram_only.fit(train["body"], train["topic"])
bigram_accuracy = (bigram_only.predict(test["body"]) == test["topic"]).mean()
print(f"bigrams only:                  accuracy {bigram_accuracy:.3f}")
print(f"unigrams + bigrams (original): accuracy {original_accuracy:.3f}")
```

```
bigrams only:                  accuracy 0.989
unigrams + bigrams (original): accuracy 0.991
```

Bigrams alone classify almost as well here (98.9% against 99.1%), because this data's fixed templates produce very consistent two-word phrases ("invoice order", "called twice" once stop words are removed) that carry nearly as much signal as single words. On less templated real text, single distinctive words are usually cheaper to estimate reliably and just as informative, which is why the standard choice is single words plus pairs together rather than either alone.

**12.** The same `Word2Vec` call as section 41.7, once for each `vector_size`.

```python
for size in [10, 100]:
    sized = Word2Vec(
        sentences, vector_size=size, window=5, min_count=5, seed=41, workers=1
    )
    print(f"\nvector_size={size}, neighbors of 'broken':")
    for neighbor, score in sized.wv.most_similar("broken", topn=5):
        print(f"  {neighbor:<14} {score:.3f}")
```

```

vector_size=10, neighbors of 'broken':
  completely     0.985
  right          0.931
  received       0.905
  there          0.905
  is             0.894

vector_size=100, neighbors of 'broken':
  completely     0.992
  received       0.936
  right          0.929
  is             0.895
  there          0.881
```

The two sizes give nearly the same top neighbors for "broken" (*completely*, *right*, *received*, *there*, and *is* appear in both lists, just reordered), because with only 3,000 short tickets there isn't enough data to make good use of 100 dimensions: most of the extra room in the larger model goes unused rather than capturing genuine nuance. A smaller vector size forces meaning into fewer numbers and can blur real distinctions on a large corpus; a larger size needs more data to fill its extra room usefully. This is a case where the corpus size, not the vector size, is the real bottleneck (section 41.7's caution).

**13.** `ColumnTransformer` (Chapter 36, section 36.4) sends the text column through the vectorizer and the two numeric columns through `StandardScaler`, then puts the results side by side for the model.

```python
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler

tickets["body_length"] = tickets["body"].str.len()
train2 = tickets.loc[train.index]
test2 = tickets.loc[test.index]
combined = ColumnTransformer(
    [
        (
            "text",
            TfidfVectorizer(
                stop_words="english", max_features=3000, ngram_range=(1, 2), min_df=2
            ),
            "body",
        ),
        ("numeric", StandardScaler(), ["resolution_hours", "body_length"]),
    ]
)
combined_pipeline = Pipeline(
    [("features", combined), ("model", LogisticRegression(max_iter=1000))]
)
combined_pipeline.fit(train2, train2["sentiment"])
combined_pred = combined_pipeline.predict(test2)
combined_accuracy = (combined_pred == test2["sentiment"]).mean()
text_only_accuracy = (pred_sent == test["sentiment"]).mean()
print(f"text + numeric features:  accuracy {combined_accuracy:.3f}")
print(f"text only (section 41.5): accuracy {text_only_accuracy:.3f}")
```

```
text + numeric features:  accuracy 0.996
text only (section 41.5): accuracy 0.996
```

Note that `"body"` is a string, not `["body"]`: a text vectorizer needs one column of strings, not a table, and a one-column list would hand it a table and fail. `train2` and `test2` are the same rows as `train` and `test`, taken again from `tickets` so that they include the new `body_length` column. Adding `resolution_hours` and ticket length changes nothing here (99.6% either way), because the generator ties sentiment to word choice directly and only loosely to resolution time; the text already carries essentially all the signal. On real data, response-time and length features often do add value for sentiment or urgency prediction, so this combination pattern (mixing a `TfidfVectorizer` column with numeric columns inside one `ColumnTransformer`) is worth having ready even when, as here, it doesn't move the needle.

**14.** "Your five categories were designed by people, for a purpose — routing tickets to the right team — and they mix several different things people care about: which product, which stage of the order, and how urgent the tone is. The topic model only sees which words appear together, so it found a pattern in *tone* (urgent, repeat-contact language) that cuts across your categories rather than matching them. That's not the model failing; it's the model finding a different, real pattern your category list wasn't built to capture."

**15.** First, **the language itself may have drifted** (Chapter 36's idea of drift, applied to text): new products, new complaint types, or seasonal issues introduce words and phrasings the classifier never saw in training, and a model trained on last year's vocabulary has no way to handle them. Second, the near-99% training-period score may itself have been inflated by **something specific to that period** the model quietly learned — a promotion that generated a wave of similarly worded tickets, or a support-team habit of using stock phrases that later changed — rather than the underlying sentiment signal being that clean everywhere. Both point to the same fix: retrain regularly on recent labeled data and monitor accuracy on a rolling basis, as Chapter 39's model card (section 39.9) and Chapter 56 (MLOps) recommend.

**16.** The main risk is treating **high textual similarity as proof the tickets are about the same issue**, when two customers can describe unrelated problems in nearly identical boilerplate language (this chapter's ticket 0 and its three "duplicates" in section 41.3 are different customers, different order numbers, different actual invoices — similar only because they used the same template). Merging on text alone could hide a second customer's genuine, distinct complaint inside a closed ticket. Before turning it on: check that a matched pair also shares something that should be shared for a true duplicate (same customer, same order ID, tickets close together in time), read a sample of pairs above the proposed threshold by hand, and make the system suggest a merge for a human to confirm rather than merging automatically.

---

## Where this leads

- **Chapter 38, Unsupervised Learning,** supplied the judgment habits (stability, external checks, "is this real?") this chapter applied to topic models.
- **Chapter 42, Recommender Systems & Ranking,** reuses TF-IDF and cosine similarity directly for content-based recommendations, and the factorization idea from section 41.6 for collaborative filtering.
- **Chapter 43, A First Look at Deep Learning,** builds the neural networks that sit inside word2vec and every model after it.
- **Chapter 54, Generative AI & Large Language Models,** picks up word embeddings exactly where this chapter leaves them: contextual, much larger, and wired into attention and generation.
- **Chapter 55, Building AI Applications,** searches documents by their embeddings (section 55.4), a whole-document version of section 41.7's word vectors.
- **Interview preparation:** the Machine Learning Question Bank (Chapter 74) covers TF-IDF versus embeddings, bag-of-words limitations, when to use a lexicon versus a trained model, and "how would you find the topics in a pile of customer feedback?"
