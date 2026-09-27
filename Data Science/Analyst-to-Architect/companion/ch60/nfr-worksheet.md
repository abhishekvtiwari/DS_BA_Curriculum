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

| Availability | Downtime per year | Downtime per month |
|---|---|---|
| 99% | ~3.65 days | ~7.3 hours |
| 99.5% | ~1.83 days | ~3.65 hours |
| 99.9% | ~8.76 hours | ~43.8 minutes |
| 99.95% | ~4.38 hours | ~21.9 minutes |
| 99.99% | ~52.6 minutes | ~4.4 minutes |
| 99.999% | ~5.3 minutes | ~26 seconds |

Each additional nine costs disproportionately more to achieve. Before targeting one, ask:
what actually happens to the business during the downtime the lower tier allows? If the
answer is "nothing serious," you don't need the extra nine.
