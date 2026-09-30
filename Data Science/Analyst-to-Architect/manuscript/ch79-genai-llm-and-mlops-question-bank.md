# Chapter 79. GenAI, LLM & MLOps Question Bank

*Part 8 — Be Interview Ready*

> **Chapter at a glance**
>
> **You will learn to:** answer the LLM fundamentals, RAG design, and evaluation questions that come up in GenAI-adjacent Data Scientist, ML Engineer, and AI Engineer interviews · reason correctly about embeddings, chunking, and retrieval, not just name the components · explain how a model actually survives production (registries, serving, monitoring, retraining) · design a RAG assistant and a model-serving platform end to end, stating trade-offs out loud.
>
> **Before you start:** Chapters 54–57 (Generative AI and LLMs; RAG, agents and evaluation; MLOps; LLMOps), which teach every idea in this bank; Chapter 35, section 35.2 for the dot product and cosine similarity; Chapter 41, section 41.7 for word embeddings; Chapter 74 for the classical-ML side of monitoring; Chapter 69 for the three answer tiers and the twelve extra-point tags. This chapter tests those skills; it doesn't teach them again. When you can't answer a question, its **Learn it in** line sends you to the section that teaches it.
>
> **Time needed:** 3½–4½ hours for a first pass: about 10 minutes per core question answered aloud, 1–2 minutes per rapid-fire row, 20 minutes for each design case, and about 45 minutes to run the four code demos yourself. Plus 45 minutes for the final-week list.
>
> **How this chapter is built.** Same format as the other question banks. Every **core question** gives a memory hook ("Remember it as…"), a one-line answer you can recall under pressure, and a tier table: what **passes**, what's **strong**, and the **extra points** (Chapter 69's moves, tagged the same way: **[+Clarify]**, **[+Edge cases]**, **[+Validate]** and so on). Then come the likely follow-ups, the red flag, and where to learn it. Every **rapid-fire section** is a scan table: question, one-line answer, one extra point, level, and where to learn it (a bare number such as 54.2 means that section). The four **Run it yourself** demos (cosine similarity, chunking, a drift statistic, and a cost estimate) are complete: copy a demo's cells, in order, into a fresh notebook and they print what's shown (Python 3.11, NumPy 2.4.6, SciPy 1.17.1; NumPy is installed in Chapter 18, SciPy in Chapter 21, section 21.5). Prompting technique, agent design, and vendor behaviour can't be "run" the way a retrieval score can, so they are reasoned through, with a pointer to the chapter that measured them. Ideas no earlier chapter teaches are marked **Beyond the book** and carry their own short explanation.

**Levels and roles.** Each question carries a level and the roles that usually ask it. **Fresher:** screening calls and first-job interviews. **Mid:** one to three years in the role. **Senior:** lead or specialist rounds. **AIE** AI engineer (builds products on top of AI models) · **DS** data scientist · **MLE** machine learning engineer.

**A note on currency.** GenAI tooling and model capabilities change fast. This chapter teaches durable ideas (how RAG works, why chunking matters, what a drift statistic measures) rather than specific model names or context-window sizes, which go stale within weeks. The only prices used, in Q79-033, are Chapter 54's price tiers, checked 29 September 2026. Verify any current specifics against the providers' own pages before an actual interview.

---

## 79.1 LLM fundamentals

### Q79-001 · What's a token, and why does a model's context window get measured in tokens, not words or characters?

**Level:** Fresher · **Roles:** AIE, DS, MLE

**Remember it as:** *A token is roughly a chunk of a word, not a whole word, which is exactly why "context window" numbers look bigger than you'd expect from word count alone.*

**Answer in one line:** A **token** is the basic unit a language model actually processes, often a word, part of a word, or punctuation mark, produced by a tokenizer that breaks text into these sub-word pieces; models measure context (and pricing) in tokens because that's the model's native unit of computation, and it doesn't map cleanly to word count, since a rare or long word can split into several tokens while a common short word is one.

| Tier | What to say |
|---|---|
| Passes | "A token is basically a word" (a rough approximation, misses the sub-word splitting that actually matters for the answer) |
| Strong | Explains that a token is often a sub-word unit, and that this is precisely why token counts and word counts diverge, especially for uncommon words, code, or non-English text |
| Extra points | **[+Business]** this divergence matters practically: rough ratios are commonly cited (about four characters, or about 0.75 English words, per token; Chapter 54 prices with the four-characters rule), but they break down for code, product codes, technical jargon, or other languages, and any cost or context-length estimate built on a clean word-to-token ratio should be treated with real caution |

**Likely follow-ups:** Why does the same context window "fit less" for code than for plain English text? How does tokenization affect a model's ability to do character-level tasks, like counting letters in a word?
**Red flag:** treating "tokens" and "words" as interchangeable when estimating cost or context usage.
**Learn it in:** Chapter 54, section 54.2 (tokens, and byte-pair encoding by hand).

### Q79-002 · What's an embedding, and why does cosine similarity, not Euclidean distance, dominate as the comparison metric for them?

**Level:** Mid · **Roles:** AIE, DS, MLE

**Remember it as:** *Cosine similarity asks "do these two vectors point in the same direction," ignoring how long each vector is. For meaning-based comparison, direction is usually what actually matters, not magnitude.*

**Answer in one line:** An **embedding** is a dense numeric vector representing a piece of text (or an image, audio, etc.) such that semantically similar inputs produce vectors that are close together in that vector space; **cosine similarity** measures the angle between two vectors, ignoring their length, which tends to reflect things like text length or intensity rather than meaning, so the angle is a more reliable meaning-similarity signal than raw distance.

**Run it yourself.** A query and three tiny three-number "embeddings": a document about returns, a document about something else, and a third that points exactly the way the returns document does but is twice as long.

```python
import numpy as np

query = np.array([0.9, 0.1, 0.0])      # a question about returns
doc_a = np.array([0.85, 0.15, 0.05])   # a document about returns
doc_b = np.array([0.1, 0.2, 0.95])     # a document about something else
doc_c = np.array([1.7, 0.3, 0.1])      # doc_a's direction, twice as long


def cosine_sim(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))


for name, doc in [("doc_a", doc_a), ("doc_b", doc_b), ("doc_c", doc_c)]:
    cosine = cosine_sim(query, doc)
    distance = np.linalg.norm(query - doc)
    print(f"{name}: cosine {cosine:.3f}   distance {distance:.3f}")
```

```
doc_a: cosine 0.996   distance 0.087
doc_b: cosine 0.124   distance 1.246
doc_c: cosine 0.996   distance 0.831
```

**How it works:**

- `np.array([...])` turns each list into a NumPy array (Chapter 18), so arithmetic works on all three numbers at once.
- `np.dot(a, b)` is the dot product: multiply matching numbers and add them up (Chapter 35, section 35.2). By hand for the query and `doc_a`: 0.9 × 0.85 + 0.1 × 0.15 + 0 × 0.05 = 0.765 + 0.015 + 0 = 0.78.
- `np.linalg.norm(v)` is the vector's length, the square root of the sum of its squares: √(0.9² + 0.1² + 0²) = 0.9055 for the query and 0.8646 for `doc_a`. Dividing the dot product by both lengths gives the cosine: 0.78 ÷ (0.9055 × 0.8646) = 0.78 ÷ 0.7829 ≈ 0.996.
- `np.linalg.norm(query - doc)` is the Euclidean distance: subtract the vectors, then take the length of the difference (Chapter 35, section 35.1). The loop stores each number under a name, then prints both.
- `:.3f` prints three decimals.

**Reading it.** `doc_a` and `doc_c` get the same cosine, 0.996, because they point the same way; only their lengths differ. Euclidean distance treats them very differently (0.087 against 0.831) purely because `doc_c` is longer. That is the case for cosine: a longer or more emphatic text shouldn't count as less similar in meaning.

| Tier | What to say |
|---|---|
| Passes | "Embeddings capture meaning as numbers" (correct, no explanation of the actual comparison mechanism) |
| Strong | The direction-versus-length distinction above, correctly identifying why cosine similarity is the standard choice for comparing embeddings |
| Extra points | **[+Validate]** the computed scores above: 0.996 for a related pair and 0.124 for an unrelated one, a large separation, and the same 0.996 for a vector twice as long<br>**[+Edge cases]** many embedding models return unit-length vectors (Chapter 54, section 54.8 scales its own to length 1); for those, cosine similarity equals the dot product, and ranking by Euclidean distance gives the same order, so the choice mostly matters when vector lengths differ<br>**[+Simple first]** it's the same cosine similarity Chapter 35, section 35.2 used to compare customers' product mixes; embeddings are one of its highest-leverage uses |

**Likely follow-ups:** What happens to retrieval quality if two genuinely different documents happen to produce very similar embeddings? How would you visualize a set of embeddings to sanity-check they're capturing meaningful structure?
**Red flag:** not knowing why cosine similarity, specifically, is the standard choice over a plain distance.
**Learn it in:** Chapter 35, section 35.2 (dot product and cosine similarity); Chapter 41, section 41.7 and Chapter 54, section 54.8 (embeddings).

### Rapid-fire, 79.1

Roles: AIE, DS and MLE for every row.

| # | Question | One-line answer | Extra point | Level · learn it in |
|---|---|---|---|---|
| Q79-003 | What's a context window, in plain terms? | The maximum amount of text (measured in tokens) a model can consider at once, including both the prompt and its own generated response | **[+Business]** a conversation or document exceeding the context window must be truncated or summarized somehow, or the model simply can't see the parts that don't fit | Fresher · 54.4 |
| Q79-004 | What's temperature, in an LLM's generation settings? | A setting controlling how random or deterministic the model's next-token choice is; low temperature favors the most likely next token consistently, high temperature allows more varied, less predictable output | **[+Business]** a factual extraction task usually wants low temperature (consistency); a creative writing task often wants it higher | Fresher · 54.5 |
| Q79-005 | What's the difference between fine-tuning and prompting (few-shot examples) as ways to adapt a model's behavior? | Fine-tuning updates the model's own weights on new examples, a heavier, more permanent change; prompting adapts behavior at inference time through instructions and examples in the prompt itself, with no weight changes at all | **[+Trade-offs]** fine-tuning can achieve a more consistent behavior change for a narrow task, at real cost and complexity; prompting is far cheaper to iterate on and is often sufficient | Mid · 54.9 |
| Q79-006 | What's a multimodal model? | A model that can process and/or generate more than one type of input or output, text and images together, for instance, rather than being restricted to text alone | **[+Business]** a scanned purchase order or a photo of a damaged delivery is exactly the input a text-only model can't read | Fresher · 54.10 |

---

## 79.2 Basic-but-tricky GenAI questions

### Q79-007 · If an LLM "hallucinates" a confident, plausible-sounding wrong answer, is that a bug in the model?

**Level:** Fresher · **Roles:** AIE, DS, MLE

**Remember it as:** *A language model is fundamentally predicting a plausible next token, not looking up a verified fact. Hallucination isn't a malfunction, it's the expected behavior of that mechanism when it has no grounding to lean on.*

**Answer in one line:** Not exactly a "bug" in the traditional sense: an LLM generates text by predicting statistically plausible continuations, and when it lacks reliable information about a specific fact, it can still generate fluent, confident-sounding text that's simply wrong, since fluency and factual accuracy are not the same thing the model is optimizing for; this is precisely why grounding techniques like RAG (section 79.3) exist, to give the model real, retrieved information to base its answer on instead of relying purely on its trained-in, sometimes-wrong "memory."

| Tier | What to say |
|---|---|
| Passes | "Hallucination means the model makes things up sometimes" (true, no explanation of the underlying mechanism) |
| Strong | The plausibility-vs-accuracy distinction above, connecting it directly to why RAG and grounding are the standard mitigation |
| Extra points | **[+Business]** a system with no grounding and no way to say "I don't know" will always eventually hallucinate on a question outside its reliable knowledge; the fix isn't a "smarter" model alone, it's an architecture (retrieval, citations, a refusal threshold) that gives the model a real alternative to guessing |

**Likely follow-ups:** How would you measure a system's hallucination rate in practice? What's the risk of a RAG system hallucinating even *with* retrieved context available?
**Red flag:** treating hallucination as a simple defect that better prompting alone fully solves.
**Learn it in:** Chapter 54, section 54.11 (limits and risks); Chapter 55, section 55.6 (grounding, citations, and refusal).

### Rapid-fire, 79.2

Roles: AIE, DS and MLE for every row.

| # | Question | One-line answer | Extra point | Level · learn it in |
|---|---|---|---|---|
| Q79-008 | Does a bigger context window mean you should always stuff in as much context as possible? | No: more context costs money and time, and models use information buried in the middle of a long prompt worse than information at the start or end, so answer quality can drop even when the relevant text is technically present | **[+Business]** relevant, well-curated context (via good retrieval, section 79.3) usually beats simply maximizing context volume | Mid · 54.4, 55.1 |
| Q79-009 | Is prompt engineering a durable, transferable skill, or is it fragile to the specific model? | Some general principles transfer (clarity, structure, examples), but specific prompt wording that works well on one model version can behave differently on another, an ongoing maintenance cost worth planning for | **[+Scale]** a production system built on carefully tuned prompts needs a regression test on its golden set whenever the provider ships a new model version, exactly like code needs tests when a dependency updates | Mid · 57.4 |
| Q79-010 | Can you fully prevent prompt injection in a system that takes user input and feeds it to an LLM? | Not with complete certainty using prompting alone; layered defenses (instructions separated from data, output validation, limiting what the model is allowed to actually do) reduce risk but don't eliminate it | **[+Limits]** say plainly that no defense closes it fully, then name the layer that matters most: model output never triggers an action without validation | Mid · 54.11; 55.10 (injection through your own documents); governance in Chapter 64 |
| Q79-011 | Is an LLM-based system deterministic, given the exact same input twice? | Not necessarily, even at temperature 0, due to factors like non-deterministic floating-point computation, request batching, and model versions changing under the same name; treat outputs as close-to-deterministic, not guaranteed identical | **[+Edge cases]** some current models don't accept a temperature setting at all; pin the model version, store the output you validated, and prefer rule-based or semantic checks to exact-match tests | Mid · 54.5, 54.11 |

---

## 79.3 Retrieval-Augmented Generation (RAG)

### Q79-012 · Walk through RAG end to end, and implement a simple chunking function

**Level:** Mid · **Roles:** AIE, DS, MLE

**Remember it as:** *Retrieve first, then generate. The model only answers using what was actually found, not purely from what it happened to memorize during training.*

**Answer in one line:** RAG breaks source documents into **chunks**, converts each chunk into an **embedding**, stores them in a **vector index**; at query time, the query is embedded and compared against that index to **retrieve** the most relevant chunks, which are then inserted into the model's prompt as grounding context before it **generates** an answer, ideally with **citations** back to the source chunks used.

**Run it yourself.** A fixed-size chunking function with overlap, run on one bullet of Riverstone's returns policy (`policy_returns.md` in Chapter 55's corpus):

<!-- py: reset -->
```python
def chunk_text(text, chunk_size=60, overlap=15):
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start += chunk_size - overlap
    return chunks


policy = ("Goods ordered in error may be returned within 15 days if unused "
          "and in original packaging. A restocking fee of 10% applies, "
          "and freight both ways is charged to the customer.")
print(f"{len(policy)} characters")
for i, chunk in enumerate(chunk_text(policy)):
    print(f'chunk {i}: "{chunk}"')
```

```
173 characters
chunk 0: "Goods ordered in error may be returned within 15 days if unu"
chunk 1: " 15 days if unused and in original packaging. A restocking f"
chunk 2: " A restocking fee of 10% applies, and freight both ways is c"
chunk 3: " both ways is charged to the customer."
```

**How it works:**

- `start` is where the next chunk begins. Each pass takes `text[start:end]`, 60 characters, then moves `start` on by `chunk_size - overlap` = 45, so each chunk repeats the last 15 characters of the one before.
- Slicing past the end of a string just stops at the end, which is why the last chunk is shorter (38 characters); the `while` loop ends once `start` passes the length.
- `overlap` must be smaller than `chunk_size`. If they were equal, `start` would never move and the loop would run forever. Try changing it to `overlap=0`: you get three chunks instead of four, and the word "unused" is cut into "unu" and "sed" with neither chunk holding it whole.
- Python joins strings written side by side into one, so the brackets around `policy` only let the text run over three lines. `enumerate` numbers the chunks from 0.

**Reading it.** The 15 overlapping characters, " 15 days if unu", appear at the end of chunk 0 and the start of chunk 1: that redundancy is what keeps a fact from vanishing at a cut. Notice too that the cuts land mid-word ("unu", "restocking f", "is c"): character chunking doesn't know what a word or a sentence is. And chunk 0 carries "15 days" without the 10% restocking fee, so an answer built from chunk 0 alone would be incomplete, the failure this chapter's real-world story is about.

| Tier | What to say |
|---|---|
| Passes | Names the RAG pipeline stages in the right order, can't produce working chunking logic |
| Strong | The working overlap-chunking function above, correctly explaining *why* overlap exists: without it, a sentence split exactly at a chunk boundary can lose meaning that only makes sense with the text on the other side of the cut |
| Extra points | **[+Validate]** the output above shows the overlap in action (" 15 days if unu" on both sides of the first cut), and shows its limit: chunk 0 still lacks the fee<br>**[+Edge cases]** fixed-size chunking is simple but cuts words and sentences in half; chunking by sentences or by document sections, with the document's title attached to each chunk, is the usual refinement, and Chapter 55 measures all three rather than choosing by taste |

**Likely follow-ups:** How would you choose chunk size for a specific document type (a legal contract vs. a product FAQ)? What's reranking, and why is it often added after the initial retrieval step?
**Red flag:** describing RAG's stages with no understanding of why chunking or overlap specifically matters.
**Learn it in:** Chapter 55, section 55.3 (chunking: fixed, sentence, and section strategies).

### Q79-013 · What's reranking, and why does an extra step after initial vector retrieval improve answer quality?

**Level:** Mid · **Roles:** AIE, DS, MLE

**Remember it as:** *The first retrieval pass is fast but approximate. Reranking is a slower, more careful second look at just the top candidates, worth the extra cost because there are far fewer of them to examine closely.*

**Answer in one line:** Initial retrieval (vector search, keyword search, or both) is fast but approximate, built to quickly narrow thousands or millions of chunks down to a top handful; a **reranker**, typically a more expensive model that reads the question and each candidate chunk together and scores relevance directly (a **cross-encoder**), then re-scores just that smaller candidate set more carefully, often surfacing a better final ranking than the fast first pass alone.

| Tier | What to say |
|---|---|
| Passes | "Reranking makes the results better" (true, no explanation of why a two-stage approach specifically) |
| Strong | The speed-vs-accuracy two-stage trade-off above: cheap-and-broad first pass, expensive-and-precise second pass on a much smaller set |
| Extra points | **[+Validate]** measure it before keeping it: the crude word-count reranker in Chapter 55's exercise 11 made recall@1 *worse* (0.87 to 0.82), because re-sorting by a weaker score undoes a good ranking<br>**[+Business]** this two-stage pattern (fast filter, then expensive precise scoring on a small candidate set) recurs well beyond RAG, wherever a precise method doesn't scale to the full dataset but is affordable on a pre-filtered handful |

**Likely follow-ups:** What would you check if reranking made results measurably worse on a specific query? How would you decide how many candidates to pass into the reranking stage?
**Red flag:** treating reranking as an optional polish step rather than understanding the two-stage cost/accuracy trade-off it exists to solve.
**Learn it in:** Chapter 55, section 55.5 (hybrid search, measuring it, and what a reranker adds).

### Rapid-fire, 79.3

Roles: AIE, DS and MLE for every row.

| # | Question | One-line answer | Extra point | Level · learn it in |
|---|---|---|---|---|
| Q79-014 | Why does a RAG system need citations, not just an answer? | Citations let a user (or an automated evaluator) verify the answer actually traces back to real, retrieved source material, rather than trusting the model's fluency alone | **[+Validate]** a citation is also a test hook: an evaluation can check that the cited source is the one that holds the answer | Fresher · 55.6 |
| Q79-015 | What happens if the retrieval step finds no genuinely relevant chunks for a query? | A well-designed system should recognize this and respond with an honest "I don't have information on that" rather than generating a plausible-sounding answer from the model's untethered training knowledge | **[+Edge cases]** the refusal needs a threshold on the absolute retrieval score (a normalized top score is always 1.0), chosen on questions the documents can and can't answer | Mid · 55.6; Q79-007 |
| Q79-016 | Why might a RAG system need to periodically re-embed and re-index its documents? | If the underlying embedding model is updated, or the source documents change meaningfully, the existing vector index can become stale or inconsistent with newly embedded content | **[+Scale]** this is a real, recurring maintenance cost of a RAG system, not a one-time setup task; a superseded document left in the index is how an assistant quotes a dead policy | Mid · 55.10, 55.11 |
| Q79-017 | What's a vector database, and how is it different from a traditional relational database for this use case? | A store built for fast approximate-nearest-neighbour search over high-dimensional vectors, a query pattern ordinary relational indexes aren't built for at scale; though extensions such as pgvector add this to PostgreSQL, keeping vectors in a table beside your data, often the right first choice | **[+Simple first]** at Riverstone's scale, a NumPy array and a dot product are enough; an approximate-nearest-neighbour index earns its place at millions of chunks | Mid · 55.4, and Chapter 55's project tools (pgvector, dedicated vector databases); relational indexes: Chapter 71, section 71.9 |

---

## 79.4 Agents and tool use

### Q79-018 · What's the difference between a simple prompt-and-response LLM call and an "agent"?

**Level:** Mid · **Roles:** AIE, DS, MLE

**Remember it as:** *A single call answers once. An agent can decide to call a tool, look at the result, and decide again, in a loop, until it's actually done.*

**Answer in one line:** A single LLM call takes a prompt and returns one response; an **agent** wraps an LLM in a loop that lets it decide to call external tools (a search, a calculator, a database query, an API), observe the result, and decide on a next action, potentially several times, before producing a final answer, giving it the ability to take multi-step actions rather than just generate text once.

| Tier | What to say |
|---|---|
| Passes | "An agent is an LLM that can use tools" (correct, no mention of the decision loop that makes multi-step behavior possible) |
| Strong | The observe-decide-act loop above, correctly distinguishing single-shot generation from iterative, tool-using behavior |
| Extra points | **[+Business]** an agent's added capability comes with added failure modes: it can call the wrong tool, misinterpret a tool's result, or loop unproductively, all failure modes a single prompt-response call simply doesn't have, which is exactly why evaluating and guardrailing agents (section 79.5) is a genuinely harder problem than evaluating a single response<br>**[+Trade-offs]** most business problems are a script with one or two tools; an agent earns its cost only when the number of steps can't be known in advance |

**Likely follow-ups:** What's the risk of an agent getting stuck in a loop, and how would you guard against it? How would you decide whether a task actually needs an agent versus a single well-designed prompt?
**Red flag:** treating "agent" as just a marketing term with no specific technical distinction from a single LLM call.
**Learn it in:** Chapter 55, sections 55.7 (tools) and 55.8 (agents, without the hype).

### Rapid-fire, 79.4

Roles: AIE and MLE for every row; DS for Q79-021.

| # | Question | One-line answer | Extra point | Level · learn it in |
|---|---|---|---|---|
| Q79-019 | Why does an agent typically need a maximum number of steps or a timeout? | Without one, a genuinely stuck agent (repeatedly calling the same tool, or oscillating between two actions) can loop indefinitely, wasting cost and never returning a result | **[+Edge cases]** give it a step limit, a token budget, and a timeout; the step limit is the same idea as a retry cap (Q78-017), while a circuit breaker (Q78-021) is the related cross-run version that stops calling a failing service for a while | Fresher · 55.8 (step limits) |
| Q79-020 | What's the risk of giving an agent access to a tool with real side effects (sending an email, modifying a database)? | An agent's decision to call that tool is itself a probabilistic model output, not a guaranteed-correct decision; a wrong or hallucinated tool call with real side effects can cause real, hard-to-undo damage | **[+Business]** make tools read-only by default, whitelist them per context, and put a human confirmation in front of any irreversible action | Mid · 55.7; Chapter 58, section 58.5 |
| Q79-021 | How would you debug an agent that's producing a wrong final answer despite calling the right tools? | Trace through the full sequence: what each tool actually returned, and how the agent interpreted that result at each step, since the failure could be in tool selection, tool execution, or the agent's interpretation of a correct tool result | **[+Edge cases]** look first for a tool that returned an error or an empty result the agent treated as an answer; it's the same "trace backward through the steps" method as data lineage in Chapter 77 (Q77-030) | Mid · Chapter 57, section 57.10 (traces) |
| Q79-022 | What's the difference between a single agent and a multi-agent system? | A single agent handles the whole task itself, looping through tool calls; a multi-agent system splits the task across several specialised agents that pass work between them, trading simplicity for narrower, better-scoped roles | **[+Trade-offs]** more agents means more coordination, more model calls, and more places for a hand-off to go wrong | Senior · Beyond the book (below) |

**Beyond the book: multi-agent systems.** Chapter 55 builds one agent: one loop, one model, a set of tools. A **multi-agent system** puts an **orchestrator** agent in charge, which splits a task and hands each part to a specialised agent with its own instructions and tools (one searches the documents, one looks up orders, one drafts the reply), then combines their results. Each specialist is easier to prompt and test on its own, but every hand-off is another model call and another place for a misunderstanding. A fair interview answer: start with one agent and a step limit, and split only when one agent's instructions or tool list have grown too large to test.

---

## 79.5 Evaluating AI applications

### Q79-023 · How do you evaluate an LLM-based application's output quality, given there's often no single "correct" answer to check against?

**Level:** Mid · **Roles:** AIE, DS, MLE

**Remember it as:** *A golden set gives you known-good answers to check against. An LLM-as-judge extends that same idea to open-ended answers a simple string match can't score.*

**Answer in one line:** Build a **golden set** of representative queries with known-good expected answers (or key facts that must appear) to check against systematically; for genuinely open-ended output where an exact match doesn't make sense, use **LLM-as-judge** (a separate model call scoring the output against a written rubric) alongside sampled **human review**, since no single method alone reliably catches every failure mode.

| Tier | What to say |
|---|---|
| Passes | Suggests a fixed test set of questions, but scores it only by exact match against one expected answer |
| Strong | The golden-set-plus-LLM-as-judge-plus-human-review combination above, correctly noting no single method is sufficient alone |
| Extra points | **[+Edge cases]** an LLM-as-judge has its own failure modes (it can be fooled by fluent-but-wrong answers, or have its own biases about what "good" looks like), so it needs calibration against human judgment: score about 50 answers by hand once, check the judge agrees, and re-check after any model change<br>**[+Scale]** a golden set needs to be actively maintained and expanded as new failure modes are discovered in production, and run as a build step on every prompt or model change, not built once and left static |

**Likely follow-ups:** How would you build an initial golden set with no existing production data to draw from? What's the risk of over-optimizing a system specifically to score well on its own golden set?
**Red flag:** relying entirely on spot-checking outputs by eye, with no systematic, repeatable evaluation method.
**Learn it in:** Chapter 55, section 55.9 (evaluating the whole application); Chapter 57, section 57.3 (the golden set as a build step).

### Rapid-fire, 79.5

Roles: AIE, DS and MLE for every row.

| # | Question | One-line answer | Extra point | Level · learn it in |
|---|---|---|---|---|
| Q79-024 | What's a guardrail, in the context of an LLM application? | A check (before or after the model's generation) that catches and blocks unsafe, off-topic, or otherwise unacceptable input or output before it does harm | **[+Business]** guardrails are a defense layer separate from prompting; relying on prompting alone to prevent bad output is fragile, the same lesson as Q79-010's prompt-injection limits | Fresher · 55.10 |
| Q79-025 | Why might an evaluation metric that looks good in aggregate still hide a real problem? | The same Simpson's-paradox-style risk (Chapter 73, Q73-031): an overall-good average score can mask a specific query type or user segment the system handles consistently poorly | **[+Edge cases]** break the golden-set score out by question type before trusting the average | Mid · 55.9; Q73-031 |
| Q79-026 | What's a regression test for an LLM-based system, specifically? | A saved set of prompts and their previously-acceptable outputs, re-run whenever the underlying model, prompt, or retrieval logic changes, to catch a quality regression before it reaches production | **[+Validate]** it only works if prompts are versioned like code, so a failing run points at exactly what changed | Mid · 57.2–57.4 |
| Q79-027 | Why is human review still necessary even with a good automated evaluation pipeline in place? | Automated methods (golden sets, LLM-as-judge) can miss failure modes nobody anticipated when designing them; sampled human review is what catches the genuinely novel problem the automated system wasn't built to look for | **[+Close]** close the loop: every problem a reviewer or a customer finds becomes a new golden-set case | Mid · 55.9; Chapter 57, section 57.11 |

---

## 79.6 MLOps: making models survive production

### Q79-028 · How do you detect whether a production model's input data has drifted from its training data, and what does drift tell you?

**Level:** Mid · **Roles:** MLE, DS

**Remember it as:** *"It looks a little different" isn't drift detection. A distance between two distributions (PSI, or the KS statistic D), with a threshold calibrated on a stable period, is. And drift says the world changed, not that the model got worse.*

**Answer in one line:** Compare the training-time distribution of each important feature with its recent production distribution using a distance: the **population stability index (PSI)** on bucketed values (Chapter 56's main metric, with rules of thumb of 0.1 for "watch" and 0.25 for "investigate", checked against a stable period) or the **Kolmogorov-Smirnov statistic D** for a continuous feature; alert on the size of the distance, not on a p-value, and treat drift as an early warning, with outcomes as the verdict.

**Run it yourself.** First, a training sample and two production samples of 1,000 values each, one with no real change and one whose mean has moved from 50 to 58:

<!-- py: reset -->
```python
import numpy as np
from scipy import stats

rng = np.random.default_rng(79)
training = rng.normal(50, 10, 1000)
prod_same = rng.normal(50, 10, 1000)      # no real shift
prod_drifted = rng.normal(58, 10, 1000)   # the mean has moved from 50 to 58

for name, recent in [("no shift", prod_same), ("mean 50 -> 58", prod_drifted)]:
    result = stats.ks_2samp(training, recent)
    print(f"{name:<14} D = {result.statistic:.3f}, p = {result.pvalue:.1e}")
```

```
no shift       D = 0.029, p = 7.9e-01
mean 50 -> 58  D = 0.317, p = 8.3e-45
```

**How it works:**

- `np.random.default_rng(79)` is a random generator with a **seed**, 79: the same seed always draws the same numbers, so your output matches this one (Chapter 21).
- `rng.normal(50, 10, 1000)` draws 1,000 values from a normal distribution with mean 50 and standard deviation 10 (Chapter 21).
- `stats.ks_2samp(a, b)` compares two samples. `.statistic` is **D**, the largest vertical gap between the two samples' cumulative distributions: 0 means identical, 1 means no overlap (Chapter 56, section 56.8 works it out by hand). `.pvalue` is the test's p-value (Chapter 22).
- `:.1e` prints a number in scientific notation with one decimal (Chapter 35): 7.9e-01 is 0.79, and 8.3e-45 is 0.000…083 with 44 zeros after the point.

With 1,000 values each, D separates the cases clearly: 0.029 against 0.317. Now the trap. Two samples of 200,000 values whose means differ by 0.3, three hundredths of a standard deviation, a difference no model would notice. Before you run the cell, predict: which of D and p will call this a big difference?

```python
big_training = rng.normal(50, 10, 200_000)
big_recent = rng.normal(50.3, 10, 200_000)   # a shift of 0.03 standard deviations
result = stats.ks_2samp(big_training, big_recent)
print(f"D = {result.statistic:.3f}, p = {result.pvalue:.1e}")
```

```
D = 0.016, p = 3.2e-23
```

`big_training` and `big_recent` come from the same `rng.normal` as before, now 200,000 values each (`200_000`; the underscore only makes it readable), and `stats.ks_2samp` and the `print` line work exactly as in the first cell: `result.statistic` is D and `result.pvalue` is p. The p-value calls this tiny shift overwhelmingly "significant", because with enough rows almost any difference is. D stays small, 0.016, below even the no-shift sample's 0.029 above. **With thousands of rows, alert on the size of D or PSI, never on the p-value**, which is what Chapter 56, section 56.8 does.

| Tier | What to say |
|---|---|
| Passes | Watches only the model's accuracy, which needs labels and arrives late |
| Strong | Monitors input drift (PSI or the KS statistic) as the early warning, and outcomes (or a cheap proxy, with a sampled audit for the truth) as the verdict: drift says the world changed, not that the model got worse |
| Extra points | **[+Evidence]** drift and decay are different things: in Chapter 56, Riverstone's new lamps pushed brightness PSI up to 4.4 while recall held (96.8% before, 96.5% during), and the new mould then cut recall to 84.4%, about 12 points, with no new drift signal; that's why you need both layers<br>**[+Validate]** calibrate the threshold on held-out stable weeks (Riverstone's noise floor for brightness was PSI 0.006–0.013) rather than trusting 0.1 blindly<br>**[+Limits]** drift is a *leading* signal of change (Chapter 75, Q75-014), not of harm: it can't see a model quietly missing one kind of defect, so outcome monitoring, the lagging signal, still decides whether it mattered |

**Likely follow-ups:** What would you do once drift is detected: retrain immediately, or investigate first? How would you monitor drift for a categorical feature instead of a continuous one?
**Red flag:** treating a drift alarm (or a tiny p-value) as proof the model is broken, or monitoring only one of the two layers.
**Learn it in:** Chapter 56, sections 56.7 (monitoring, in three layers) and 56.8 (drift, measured).

### Rapid-fire, 79.6

Roles: MLE and DS for every row.

| # | Question | One-line answer | Extra point | Level · learn it in |
|---|---|---|---|---|
| Q79-029 | What's a model registry, and why does a team need one? | A central index of every trained model version, the run that produced it, its metrics, and an alias such as `production` pointing at the version in use, so "which exact model is live right now" always has one clear answer | **[+Business]** without one, a team can lose track of which model version produced a specific prediction; with one, a rollback is moving the alias back | Fresher · 56.2, 56.3 |
| Q79-030 | What's a feature store, and what problem does it solve? | A shared service that computes each feature once and serves the same values to training and to production, so a feature can't be computed one way in training and another in the service (**training-serving skew**: the same feature computed differently in training and in production) | **[+Trade-offs]** excellent when many models share features; for one or two models, a scikit-learn pipeline packaged with the model applies the same fitted steps at serving time and does the same job | Mid · Chapter 36, section 36.9 (one pipeline for training and serving); 56.4, 56.11; Q74-030 |
| Q79-031 | How should you decide when to retrain a model? | A schedule is the simplest default; add a performance-floor trigger (late, because it needs labels), treat drift as a prompt to investigate rather than an automatic retrain, and above all retrain on known business events (a new product, supplier, or machine) | **[+Business]** the best trigger comes from the business, not a monitor: Riverstone's rule is "retrain monthly, and immediately on any event the plant tells us about" | Mid · 56.9 |
| Q79-032 | What's the difference between online and batch model serving? | Online serving responds to individual requests in real time (a single prediction per API call); batch serving scores a large dataset all at once on a schedule, with no per-request latency requirement | **[+Business]** the choice depends on whether a downstream decision genuinely needs a fresh, on-demand prediction or can work from a periodically refreshed batch of scores, the same freshness-driven logic as Q77-002's batch-vs-streaming decision | Fresher · 56.5 |

---

## 79.7 LLMOps

### Q79-033 · Estimate the daily cost of an LLM-powered feature, and explain what levers you'd pull if it's too expensive

**Level:** Mid · **Roles:** AIE, MLE

**Remember it as:** *Cost scales with tokens in, tokens out, and calls per day, so any lever that reduces one of those three reduces cost proportionally.*

**Answer in one line:** Cost per call is input tokens times the input price plus output tokens times the output price (output is usually several times dearer), multiplied by the number of calls per day; to reduce cost, shrink the prompt (better retrieval, less unnecessary context), shrink the expected output length, cache repeated queries, or route simpler queries to a cheaper, smaller model.

**Run it yourself.** Prices are quoted in US dollars per million tokens, as in Chapters 54 and 57. This uses Chapter 54's workhorse tier ($2 in, $10 out) and the volume-tier prices Chapter 57 uses ($0.75 in, $3.75 out), both from price tiers checked on 29 September 2026, for a call with 500 tokens in and 150 out, 2,000 times a day:

<!-- py: reset -->
```python
USD_TO_INR = 88.0   # rupees per US dollar, as in Chapter 57; check today's rate


def estimate_cost(tokens_in, tokens_out, price_in_per_m, price_out_per_m):
    cost_in = tokens_in / 1_000_000 * price_in_per_m
    cost_out = tokens_out / 1_000_000 * price_out_per_m
    return cost_in + cost_out


tiers = [("workhorse", 2.00, 10.00), ("volume", 0.75, 3.75)]
for tier, price_in, price_out in tiers:
    per_call = estimate_cost(500, 150, price_in, price_out)
    per_day = per_call * 2000
    rupees = per_day * USD_TO_INR
    print(f"{tier:<9} per call ${per_call:.6f};",
          f"per day ${per_day:.2f} (₹{rupees:,.0f})")
```

```
workhorse per call $0.002500; per day $5.00 (₹440)
volume    per call $0.000937; per day $1.88 (₹165)
```

**How it works:**

- `USD_TO_INR` holds the exchange rate in one named place, as Chapter 57 does; it is the only rupee assumption.
- `estimate_cost` divides each token count by a million (`1_000_000`), multiplies by the price per million, and adds the input and output costs. By hand for the workhorse tier: 500 ÷ 1,000,000 × $2 = $0.001 in, plus 150 ÷ 1,000,000 × $10 = $0.0015 out, is $0.0025 a call.
- `tiers` lists each tier's name and prices, and the loop unpacks each (tier, input price, output price) triple; `rupees` converts the day's dollars. `print` given two strings prints them with a space between. `:.6f` prints six decimals, because a single call costs a fraction of a cent; `:,.0f` prints whole rupees.

Output is under a quarter of the tokens and 60% of the workhorse cost. Routing to the volume tier cuts the bill by more than 60%, *if* its answers pass the same evaluation (Q79-036).

| Tier | What to say |
|---|---|
| Passes | Knows cost is per token, but multiplies one blended price by an average length and ignores the input/output price split |
| Strong | The token-based cost formula above, correctly separating input and output token pricing, and naming at least two concrete cost-reduction levers |
| Extra points | **[+Evidence]** Riverstone's own order-email pipeline, metered in Chapter 57, costs about ₹0.08 (₹0.079) per email, under ₹90 a month, and Chapter 55's support assistant about 13–14 paise a question: at this scale the staff time around the model costs far more than the model<br>**[+Business]** **caching** deserves special mention: a cache hit costs nothing, and for a feature with real repetition it can be the highest-leverage lever, but it saves only the share of traffic that repeats (17% on a normal day of Riverstone's order emails), so measure the hit rate on your own logs |

**Likely follow-ups:** How would you decide which queries are safe to route to a cheaper model versus which need the more capable one? What's the trade-off of caching for a use case where answers need to reflect very current information?
**Red flag:** no structured cost model at all, or ignoring caching as a lever entirely.
**Learn it in:** Chapter 54, section 54.12 (price tiers); Chapter 57, sections 57.5 (tokens, cost, and the meter) and 57.6 (caching).

### Rapid-fire, 79.7

Roles: AIE and MLE for every row.

| # | Question | One-line answer | Extra point | Level · learn it in |
|---|---|---|---|---|
| Q79-034 | Why does an LLM application need prompt versioning, the same way code needs version control? | A prompt change can meaningfully change output quality or behavior; without versioning, there's no way to know exactly which prompt produced a given historical output, or to safely roll back a change that made things worse | **[+Validate]** pair every prompt version with its golden-set score, as Q79-026's regression test does | Mid · 57.2–57.4 |
| Q79-035 | What's tracing, in an LLM application context? | Recording the full sequence of steps (retrieval, tool calls, model calls, intermediate outputs) behind a single final response, so a specific bad output can be debugged step by step instead of treated as an unexplainable black box | **[+Edge cases]** log the IDs of the retrieved chunks with each answer, or you can't tell a retrieval failure from a generation failure (the same trace-the-steps discipline as Q79-021) | Mid · 57.10; Chapter 55 (retrieved chunks carry their document name as the citation) |
| Q79-036 | What's the risk of routing a query to a cheaper, smaller model purely based on cost, with no quality check? | The cheaper model may produce a meaningfully worse answer for that specific query's complexity, silently degrading the user's experience in exchange for a cost saving that may not be worth it | **[+Business]** any routing strategy, including a fallback to a cheaper model when the main one fails, needs its own evaluation (section 79.5) proving the quality trade-off is acceptable | Mid · 57.8 (fallback model) |
| Q79-037 | Why is prompt injection a genuinely different security problem from a traditional SQL injection? | Traditional injection exploits a rigid parser with a fixable grammar; prompt injection exploits a model's flexible, natural-language interpretation, which has no equally rigid, fully closeable boundary between "instructions" and "data" the way a parameterized SQL query does | **[+Limits]** so the defense is containment, not a fix: validate output, keep tools read-only, and monitor injection attempts | Senior · 54.11; 55.10; 57.10; Q79-010 |

---

## 79.8 Full design cases

### Q79-038 · Design a RAG-based product-support assistant for Riverstone, end to end

**Level:** Senior · **Roles:** AIE, MLE, DS

**What they're really testing:** whether a complete RAG system design comes out under time pressure, covering ingestion, retrieval, generation, and evaluation, not just the retrieval step alone.

**Talked through live, start to finish:**

> "Source content: product manuals, past support tickets, and the returns policy, ingested and chunked (Q79-012), each chunk embedded and stored in a vector index. At query time: a customer's question is embedded, the index returns the top-k most similar chunks, and a reranker (Q79-013) narrows those to the genuinely most relevant few before they're inserted into the prompt as grounding context. The model generates an answer citing which source chunks it used, and if retrieval finds nothing sufficiently relevant, the system explicitly says it doesn't have a confident answer rather than guessing (Q79-015), routing to a human agent instead. For evaluation, I'd build a golden set from real historical support tickets with known-good resolutions, checked with LLM-as-judge plus sampled human review (Q79-023), and I'd add a guardrail blocking any generated answer that promises something outside Riverstone's actual policies, like an unauthorized discount. For cost, I'd cache answers to genuinely repeated common questions (Q79-033), keyed on the normalised question plus the policy-document version, and never for questions that depend on the customer's own order; the cache is cleared when a source document changes."

**Extra-points moves demonstrated:** **[+Signpost]** covered ingestion through evaluation and cost, in order, not just the retrieval mechanics. **[+Edge cases]** explicitly handled the no-good-retrieval case with a human handoff rather than letting the model guess, and kept live order data out of the cache. **[+Business]** named a guardrail tied to a real business risk (an unauthorized discount promise), not a generic safety placeholder.

**Likely follow-ups:** How would you handle a question that spans multiple product manuals? What would make you decide this needs an agent (able to look something up dynamically) rather than pure RAG?
**Red flag:** a design that only covers retrieval and generation, with no mention of evaluation, guardrails, or the no-good-answer case.
**Learn it in:** sections 79.3 and 79.5 above, pulled together; Chapter 55 builds this assistant, and Chapter 57, section 57.6 covers caching and its limits.

### Q79-039 · Design a model-serving platform that supports both real-time and batch predictions for multiple models

**Level:** Senior · **Roles:** MLE, DS

**What they're really testing:** whether the online-vs-batch distinction (Q79-032) gets applied to a genuine shared-infrastructure design, not treated as two unrelated systems.

**Talked through live, start to finish:**

> "A model registry (Q79-029) is the shared source of truth for every model version and its deployment status, used by both serving paths. Each model is packaged with its preprocessing pipeline and its metadata, such as its threshold, so the feature logic used in training is the logic used at serving time, avoiding training-serving skew; a feature store (Q79-030) takes over that job if several models share features, but for one or two models the packaged pipeline does the same job. For real-time serving: models loaded behind a low-latency API. For batch serving: a scheduled job scores a full dataset on a cadence appropriate to that model's use case (Chapter 77's batch pipeline pattern applies directly here). Both paths log predictions with the exact model version used, feeding the monitoring (Q79-028): input drift as the early warning, and outcomes, a proxy plus a sampled audit, as the verdict. A retraining trigger (Q79-031) fires on a baseline schedule and on known business events; a drift alarm opens an investigation, and a confirmed drop in performance triggers the retrain."

**Extra-points moves demonstrated:** **[+Signpost]** laid out the shared pieces first (registry, packaged feature logic, monitoring), then each serving path, rather than designing two disconnected systems. **[+Trade-offs]** chose a packaged pipeline over a feature store until several models share features. **[+Business]** connected monitoring directly to concrete retraining triggers, including business events, closing the loop rather than leaving monitoring as a dashboard nobody acts on.

**Likely follow-ups:** How would you handle two models needing genuinely different feature computation logic within the same shared feature store? What would you monitor differently for the batch path versus the real-time path?
**Red flag:** designing the two serving paths as entirely separate systems with no shared registry, feature logic, or monitoring.
**Learn it in:** Chapter 56, sections 56.4 (packaging), 56.5 (serving), 56.7–56.9 (monitoring, drift, retraining) and 56.11 (how far up the ladder to climb); Chapter 77 (the batch pipeline pattern this design's batch path reuses).

---

## Common mistakes

| Mistake | Symptom | Fix |
|---|---|---|
| Assuming a bigger context window means "always add more context" | Higher cost and latency, and sometimes worse answers despite more information present | Curate relevant context via good retrieval, don't maximize volume |
| No grounding, relying purely on the model's trained-in knowledge | Confident, fluent, sometimes wrong answers (hallucination) | Use RAG to ground answers in real, retrieved, current information |
| Chunking with no overlap | Meaning split across a chunk boundary gets lost | Use overlapping chunks, or chunk by sentences or sections |
| Monitoring only one layer: accuracy alone, or drift alone | Accuracy alone finds problems weeks late; drift alone alarms on harmless change and stays silent on real decay | Watch inputs as the early warning and outcomes (a proxy plus a sampled audit) as the verdict (Q79-028) |
| Alerting on a drift test's p-value | With thousands of rows, every tiny shift is "significant" and the alert fires daily | Alert on the size of PSI or D, with a threshold calibrated on a stable period |
| No cost model for an LLM feature before shipping it | An unpleasant cost surprise once usage scales up | Estimate cost per call from prices per million tokens, and multiply by expected volume before launch |
| An agent given side-effect tools with no human-in-the-loop check | A wrong or hallucinated tool call causes real, hard-to-undo damage | Read-only tools by default; require confirmation for high-stakes, irreversible actions |
| Evaluating only on an aggregate score | A real, segment-specific failure mode hides behind a good average | Check performance broken out by query type or user segment |

---

## In the real world: the RAG assistant that confidently cited a document that didn't say what it claimed

Priyanka, a Data Scientist, is asked in an interview to describe debugging a real RAG system issue. She describes a customer-support assistant that had started giving customers an incorrect return window, and the response even included a citation to a real, correctly retrieved policy document, which made the error harder to spot at first: the citation looked legitimate, so nobody initially suspected the retrieved content itself.

She traces it to the chunking boundary: the policy document's actual text read "returns are accepted within 30 days, except for electronics, which have a 14-day window," and a fixed-size chunk had split exactly between those two clauses, so the retrieved chunk for an electronics question contained only "returns are accepted within 30 days," the exception clause landing entirely in the next chunk, which wasn't retrieved for that specific query. The citation was technically accurate, that chunk really did come from the real policy document, but the chunk itself no longer contained the complete, correct information.

The interviewer's follow-up: how did she fix it, and how did she make sure it wouldn't happen again the same way? Her answer: she moved to chunking on sentence and paragraph boundaries instead of a fixed character count, so a chunk wouldn't split a sentence's meaning apart from its own exception clause, and she added a golden-set test case specifically covering the electronics exception, so a future chunking or retrieval change that reintroduced this exact failure would be caught automatically before shipping, not discovered again by a customer complaint.

The interviewer's note: *"A citation being real doesn't mean the retrieved content is complete. She caught a failure mode a simpler 'is this grounded' check would have completely missed."* That's the deeper lesson this whole chapter is built around: grounding and citations reduce hallucination risk, but they don't eliminate every way a RAG system can still confidently produce a wrong answer.

---

## Project

**Goal:** apply this chapter's verifiable pieces to a real or realistic scenario.

### Tools you'll need

**Python** with **NumPy** (Chapter 18) and **SciPy** (Chapter 21, section 21.5), used for every computable claim in this chapter (cosine similarity, chunking, the KS drift statistic, the cost estimate); the outputs shown came from Python 3.11, NumPy 2.4.6 and SciPy 1.17.1. For step 3, Chapter 56's `psi` function (section 56.8). In real GenAI and MLOps work: a vector store (pgvector or a dedicated vector database), an orchestration framework for agents, MLflow or a similar tool for the model registry and tracking, and an LLM observability or tracing platform. Vendor and model specifics change quickly; verify current details before relying on them in an actual interview.

1. Run the chunking function from Q79-012 on a real document of your own, and inspect every chunk boundary to check whether it splits a fact from its condition, the way this chapter's real-world story describes.
2. Compute cosine similarity between a real query and a few candidate documents (using Chapter 54's embeddings, or any embedding source available to you) and confirm the ranking matches your own judgment of relevance.
3. Run Q79-028's drift check on two real or simulated datasets of your own, one with a genuine shift and one without. Report D and PSI for each, then repeat with ten times the rows and watch what happens to the p-value while D and PSI stay put.
4. Estimate the daily cost of a hypothetical LLM feature for your own context with Q79-033's formula and prices per million tokens, and name the one cost lever you'd pull first if it came in too expensive.

---

## Key terms

token · context window · temperature · fine-tuning vs. prompting · embedding · cosine similarity · unit-length vector · hallucination · RAG (Retrieval-Augmented Generation) · chunking (fixed-size, sentence, section) · overlap · vector database · reranking · cross-encoder · citation/grounding · refusal · agent · tool use · step limit · multi-agent system · orchestrator · golden set · LLM-as-judge · guardrail · regression test (LLM) · model registry · feature store · training-serving skew · drift detection · population stability index (PSI) · KS statistic (D) · retraining trigger · online vs. batch serving · prompt versioning · tracing (LLM) · prompt injection · caching (LLM cost)

---

## Final-week revision list

Q79-001, Q79-002, Q79-007, Q79-012, Q79-013, Q79-018, Q79-023, Q79-028, Q79-033, Q79-038, Q79-039.

---

## Where this leads

- **Chapter 69, The Extra-Points Method,** is the rubric and move set every answer above is written against.
- **Chapter 74, Machine Learning Question Bank,** already covers training-serving skew and drift-adjacent concepts (Q74-030) from the classical-ML angle; this chapter extends the same discipline to LLM-based systems.
- **Chapter 77, Data Engineering & Data System Design Bank,** supplies the batch pipeline pattern Q79-039's batch-serving path reuses; **Chapter 78** (Q78-021) and **Chapter 57, section 57.8** describe the circuit breaker, and Chapter 58, section 58.6 builds one for a whole batch.
- **Chapters 54–57 of this book** teach every technique this bank draws on, in full; this chapter tests it, it doesn't re-teach it from scratch.
- **Chapter 80, Architecture & Leadership Question Bank,** comes next: the same interview discipline, applied to whole-platform design and to leading the people who build it.
