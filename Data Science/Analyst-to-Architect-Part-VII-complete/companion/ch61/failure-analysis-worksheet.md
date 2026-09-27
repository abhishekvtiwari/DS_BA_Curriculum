# Failure analysis worksheet

For each container/component in your system, fill in the four columns.
See Chapter 61, section 61.7, for the method and a worked example.

| Container | Weakest link | What breaks (specifically) | How it degrades |
|---|---|---|---|
| | | | |
| | | | |
| | | | |
| | | | |
| | | | |

## Reading your own table

Once every row is filled in, answer these three questions — they're the actual
output of the exercise, not the table itself:

1. **Is there a genuine single point of failure** — a row where "how it degrades"
   is "total outage" rather than some form of graceful reduction? If so, that's
   where a reliability investment is justified first.
2. **Which rows made a deliberate CAP choice** (consistency over availability, or
   the reverse)? Can you state, for each, *why* that side was chosen — who would
   be harmed by the opposite choice?
3. **Which rows have never actually been tested** — designed to degrade a certain
   way, but never deliberately exercised to confirm it? Those are candidates for
   a chaos test (Chapter 61's real-world story).
