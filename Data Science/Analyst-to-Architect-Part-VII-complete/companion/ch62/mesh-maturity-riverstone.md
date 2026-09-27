# Data mesh maturity scorecard — Riverstone (worked, 19 Sep 2026)

Companion to Chapter 62, Figure 62.4. Full reasoning behind each score.

| Dimension | Score | Evidence |
|---|---|---|
| Multiple domain teams that could each own data | 1/5 | One data platform team (4 people, Chapter 60) serves the whole company; sales, operations, and the Taloja plant have no dedicated data-owning staff of their own yet. |
| A self-serve platform domains could use independently | 2/5 | Dagster and the warehouse are genuinely reusable infrastructure, but no domain team has ever onboarded or used them without the platform team's direct, hands-on involvement. |
| Federated governance (agreed standards, locally applied) | 2/5 | Data contracts (Chapter 47) exist and work well for the Bhiwandi dispatch pipeline specifically; there's no company-wide contract standard any other team has adopted. |
| A data-product mindset (owner + stated service level) | 3/5 | Chapter 60's container diagram already gives every piece a named owner and explicit non-functional requirements — real groundwork, even though it was built by one team for its own use, not as a mesh's data products. |
| Organizational appetite for the cultural change mesh requires | 1/5 | No domain outside the data platform team has asked to own its own data pipeline; the appetite this dimension measures simply hasn't been expressed yet. |

## Verdict

**Not ready.** A data mesh imposed on Riverstone today would add real
organizational complexity — new roles, new governance processes, new
platform obligations — to solve a bottleneck that doesn't yet exist: one
four-person team is managing current load without sustained queueing.

**The specific, observable trigger that would change this verdict:** a
second domain team (plant, sales, or operations) acquiring real capacity —
a person whose job includes owning that domain's data — and asking to own
its own pipeline, rather than the data platform team guessing this is
wanted and building it preemptively.

**Update, per Chapter 62's story:** nine months after this scorecard was
first run, the Taloja plant hired its first dedicated data analyst. Rerunning
the scorecard at that point showed real movement specifically on the
"multiple domain teams" and "organizational appetite" dimensions — the exact
trigger named above, arriving for real rather than being guessed at.
