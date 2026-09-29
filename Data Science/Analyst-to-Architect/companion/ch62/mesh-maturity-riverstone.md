# Data mesh maturity scorecard — Riverstone (worked)

Companion to Chapter 62, section 62.6 and Figure 62.5. Full reasoning behind
each score.

**Scale:** 1 = absent · 3 = partly in place · 5 = working company-wide.
**Rule:** any question at 1, or a total under 15 out of 25, means not ready.

| Question | Score | Evidence |
|---|---|---|
| Multiple domain teams that could each own data | 1 | One data platform team (four people, Chapter 60) serves the whole company; sales, operations, and the Taloja plant have no builders of their own yet. |
| A self-serve platform domains could use independently | 2 | Dagster and the warehouse are genuinely reusable, but no domain team has ever onboarded or used them without the platform team's direct, hands-on involvement. |
| Federated governance (agreed standards, locally applied) | 2 | A data contract (Chapter 47) exists and works for the Bhiwandi dispatch feed; there's no company-wide contract standard any other team has adopted. |
| A data-product mindset (a named owner and a stated service level) | 3 | Chapter 60's container diagram gives every piece a named owner and explicit non-functional requirements: real groundwork, even though it was built by one team for its own use. |
| Organizational appetite for the cultural change a mesh requires | 1 | No domain outside the data platform team has asked to own its own data. |
| **Total** | **9 / 25** | Two questions at 1. |

## Verdict

**Not ready.** Two blockers (domain teams and appetite) and a total of 9,
well under 15. A data mesh imposed on Riverstone today would add real
organizational complexity (new roles, new governance processes, new platform
obligations) to solve a bottleneck that doesn't yet exist: one four-person
team is managing the current load without sustained queueing.

**The specific, observable trigger that would change this verdict:** a
business domain with its own builder (a person whose job includes owning that
domain's data) asks to own its data, rather than the data platform team
guessing this is wanted and building it in advance.

## Rerun, from the chapter's story

Months after the first run, the Taloja plant hired its own data analyst and
asked to own the plant's data. Rerun:

| Question | Before | After |
|---|---|---|
| Multiple domain teams that could each own data | 1 | 2 |
| A self-serve platform | 2 | 2 |
| Federated governance | 2 | 2 |
| A data-product mindset | 3 | 3 |
| Organizational appetite | 1 | 3 |
| **Total** | **9** | **12** |

Still under 15, so still not ready for a mesh. But the trigger fired and the
blockers are gone for one domain, so the verdict becomes **ready for a
specific first step**: one plant data product, owned by the plant (Chapter 62,
exercise 16).
