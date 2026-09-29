# ADR-023: Support assistant refusal and document status

**Status:** Accepted
**Date:** after the pilot's second week (Chapter 55)
**Owner:** AI applications team

## Context
Two findings from Chapter 55. First, hybrid search adds the keyword and meaning scores after
rescaling each set for the question being asked (section 55.5), so the top result always
scores 1.0: a refusal threshold on those rescaled scores can never trigger. Second, in the
pilot, the assistant told a customer that delivery was free above ₹40,000. The threshold had
been ₹25,000 since January; the answer came from `policy_delivery_rev3_superseded.md`, an old
policy still in the shared folder, which the search ranked first because it really is about
free-delivery thresholds.

## Decision
Refuse when the raw (absolute) keyword or meaning score of the best passage is below its floor,
not on rescaled scores. Give every document a status (current, superseded, draft) and an
effective date at index time, and index only current documents.

## Alternatives considered
1. **Keep rescaled scores and lower the threshold** — rejected: the top result is 1.0 whatever
   the threshold, so nothing changes.
2. **Always answer, with a confidence caveat** — rejected: a confidently worded wrong answer
   with a small caveat is not meaningfully safer; refusal is the right behavior when no
   document clears the bar.
3. **Delete the superseded file and do nothing else** — done as well, but not instead: it fixes
   this one file, not the next document nobody thinks to delete.

## Consequences
**Positive:** the assistant refuses when nothing in the corpus answers the question, and a
superseded policy can no longer be retrieved; the refusal log became a list of questions the
documents don't answer.
**Negative / costs:** the floors must be re-tuned whenever the retrieval method changes, since
raw scores aren't comparable across methods; every document now needs a status and an owner
before it can be indexed.

## Revisit when
The retrieval method changes (a new embedding model, a different search algorithm), since the
floors are calibrated to the current method's scores.
