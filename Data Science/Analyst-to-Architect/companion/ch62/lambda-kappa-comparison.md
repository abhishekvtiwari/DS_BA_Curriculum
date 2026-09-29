# Lambda vs. Kappa: the full worked comparison

Companion to Chapter 62, section 62.2. Scenario: the plant's machine sensors
must raise an alert on the line within minutes, and still produce correct
daily totals. This is the plant-sensor case Chapter 50 built in section 50.8.

## What Chapter 50 built (three paths)

- **Alerting path (seconds):** a consumer group reads the `sensor-readings`
  topic and raises an alert when a machine's 2-minute average passes its
  limit. Alerts are de-duplicated by machine and window, and suppressed for
  30 minutes after firing.
- **Aggregation path (minutes):** a Spark Structured Streaming job with
  5-minute windows and a 10-minute watermark writes windows into a Delta table
  (the streaming table).
- **Correction path (daily):** a batch job re-reads the day from the archive
  and rewrites yesterday's windows (the corrected table), so late and dropped
  readings are counted once a day. "Streaming for speed, batch for truth."

## Lambda architecture: what Riverstone runs

**How it maps:** the **speed layer** is the alert consumer plus the streaming
job; the **batch layer** is the daily correction job; the **serving layer**
is the dashboard's query, which reads the corrected table for past days and
the streaming table for today.

**Cost:** the window logic (window length, what counts as a reading, how
duplicates are removed) lives in two jobs. Change it in one and forget the
other, and today's numbers stop being comparable with yesterday's. Spark
shrinks the cost, because a streaming query is almost the same code as a batch
one (Chapter 50, section 50.4), but two jobs still run, fail, and get deployed
separately.

**Why Riverstone chose it:** the team already runs Dagster batch jobs every
day (Chapter 46) and already keeps the sensor archive as a Delta table
(Chapter 49), so the correction job is one more daily asset on infrastructure
the team knows. It needs no long-retention log.

## Kappa architecture: the alternative

**How it would work at Riverstone:** drop the daily correction job. Keep one
streaming job that raises alerts and writes the 5-minute windows. To correct
history, reset the job's committed offsets to the start of the topic (Chapter
50, section 50.7: "replay is your recovery tool") and run the same code over
the whole topic again, into a fresh table. The replay run can use a much
longer watermark than the live run, because nobody is waiting on it for an
alert.

**Cost:** the topic must be retained long enough to replay the history you
might need to correct. Section 50.7's typical retention is 7 days; replaying a
quarter means keeping months of readings in the log and running a log that can
serve them. Replay must be fast and trustworthy enough to use routinely, not
just in theory.

**When it would be the better choice for Riverstone:** if the two jobs started
drifting apart often enough to cause incidents, or if Riverstone were already
running a durable, replayable log for other reasons (Chapter 50's exercise 12:
a log starts to pay for itself when several consumers need the same events).

## The case that is neither: the defect camera

The defect model (Chapter 53) looks at a camera image of each part on the
Taloja line. Chapter 56 serves it **online**: a request arrives and the answer
goes back in milliseconds, while the part is still in front of the camera.
Each prediction is also written as one structured log line (Chapter 56,
section 56.5), which monitoring reads later (section 56.7).

Lambda and Kappa are patterns for processing an event log. The defect alert
isn't a log consumer; it's a request answered on the spot. Logging the result
afterwards is a separate, asynchronous write. There is no merge step and no
stream to unify, so neither name applies.

## The general lesson

Lambda and Kappa answer one question: *when fast results and correct history
come from the same stream of events, do you keep one processing path or two?*
Start from what the organization already runs, and price the replay. When the
fast path isn't stream processing at all, use the name that fits it (online
serving) instead.
