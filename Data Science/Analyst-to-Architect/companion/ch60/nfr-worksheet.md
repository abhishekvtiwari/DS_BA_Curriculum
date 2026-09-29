# Non-functional requirements worksheet

For each row, replace the adjective with a number and a measurement method.
See Chapter 60, section 60.3, for the full method.

| # | System / feature | Vague requirement | Precise requirement | Measured how | Owner |
|---|---|---|---|---|---|
| 1 | | "should be fast" | | | |
| 2 | | "should be reliable" | | | |
| 3 | | "should be secure" | | | |
| 4 | | "should scale" | | | |
| 5 | | "should be cheap" | | | |
| 6 | | "shouldn't lose data" | | | |
| 7 | | "should be available" | | | |
| 8 | | "should be current / fresh" | | | |

## The "nines" reference table (availability)

Computed with the availability cell in Chapter 60, section 60.3 (a year of 365 days, a month of
one twelfth of a year).

| Availability | Downtime per year | Downtime per month |
|---|---|---|
| 99% | ~87.6 hours (3.65 days) | ~7.3 hours |
| 99.5% | ~43.8 hours (1.8 days) | ~3.65 hours |
| 99.9% | ~8.76 hours | ~43.8 minutes |
| 99.95% | ~4.38 hours | ~21.9 minutes |
| 99.99% | ~52.6 minutes | ~4.4 minutes |
| 99.999% | ~5.3 minutes | ~26 seconds |

For something that happens only a few times a month (a daily job), write the target as a count
instead of a percentage: at about 30 runs a month, one failure is already 3.3%, so "99.5% of runs"
would allow none. "At most 2 failed runs a year" says what you mean.

Each additional nine costs disproportionately more to achieve. Before targeting one, ask:
what actually happens to the business during the downtime the lower tier allows? If the
answer is "nothing serious," you don't need the extra nine.
