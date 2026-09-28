# ADR-023: Support assistant refusal threshold

**Status:** Accepted
**Date:** (Part 6, Chapter 55)
**Owner:** AI applications team

## Context
An early version compared retrieval scores after normalizing them 0-1 per query. Because the
top-ranked chunk always normalizes to 1.0 regardless of how relevant it actually is, the
refusal logic never triggered — including on a delivery-policy question where the top-ranked
chunk was a superseded policy document, confidently cited as current.

## Decision
Use an absolute confidence floor on raw retrieval scores for the refusal decision, not a
per-query normalized score.

## Alternatives considered
1. **Keep normalized scores, lower the threshold** — rejected: doesn't fix the underlying
   problem; a bad top result still normalizes to 1.0 no matter how low the threshold is set.
2. **Always show the top result with a confidence caveat, never refuse** — rejected: a
   confidently-worded wrong answer with a small caveat is not meaningfully safer than one
   with no caveat; refusal is the correct behavior when no document clears the bar.
3. **Remove the superseded document from the corpus instead** — done in addition to, not
   instead of, this decision: fixes this one instance but not the general problem of low-
   quality top results on other future questions.

## Consequences
**Positive:** the assistant now refuses when nothing in the corpus genuinely answers the
question, instead of confidently citing whatever ranked first.
**Negative / costs:** the absolute floor must be re-tuned if the embedding or retrieval
method changes, since raw scores aren't comparable across methods.

## Revisit when
The retrieval method changes (a new embedding model, a different search algorithm), since the
absolute floor is calibrated to the current method's score distribution.
