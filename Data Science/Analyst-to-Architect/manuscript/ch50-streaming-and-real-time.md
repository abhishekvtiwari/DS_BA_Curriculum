# Chapter 50. Streaming & Real-Time

*Part 5 — Data Engineering, Integration & Scale*

> **Chapter at a glance**
>
> **You will learn to:** tell the difference between "real-time" as a business word and as an engineering commitment · explain topics, partitions, offsets, consumer groups, and why order is only guaranteed inside a partition · produce and consume events, commit offsets, and handle the duplicates that at-least-once delivery creates · run a real Kafka broker on your own computer, and read and write the Kafka client code you'll meet at work · count events in tumbling, sliding, and session windows, by hand and in Spark · build a Spark Structured Streaming job with event-time windows and a watermark · show what happens to late data, both when it's accepted and when it's dropped · keep a streaming sink from drowning in small files · monitor a stream: lag, watermark, state size, and dropped rows · decide when streaming is worth its cost, using Riverstone's plant monitoring case.
>
> **Before you start:** Chapter 45 (ingestion, and its incremental-load watermark), Chapter 46 (idempotency and the delivery log), Chapter 47 (quality and alerts), Chapter 48 (Spark, and the sensor data this chapter replays), and Chapter 49 (table formats and compaction). Section 50.3's optional broker uses the terminal from Chapter 34.
>
> **Time needed:** 15–19 hours of reading and practice, spread over two to three weeks. Plan four sittings: sections 50.0–50.2; section 50.3, plus 30–45 minutes if you run the optional Kafka broker; sections 50.4–50.5, the heart of the chapter; section 50.6 onwards and the project.
>
> **Tools:** Python 3.14 in the virtual environment from Chapter 17, with `pyspark` (Chapter 48), `deltalake` (Chapter 49), `duckdb` (Chapter 45), and `pyarrow` (Chapter 18), plus Java 21 (Chapter 48). Nothing new is needed for the main thread. The optional Kafka broker in section 50.3 is a free download.
>
> **Practice data:** the Chapter 48 sensor archive, replayed as a stream of events by the companion scripts.

> **A note on Kafka.** Kafka is the industry's standard event log, and this chapter teaches its model. Kafka runs as a **broker**, a server program that stores the events and hands them out. So that every reader can run every idea, the main examples use `mini_log.py`, a small append-only log in the companion folder that works the way Kafka does: topics, partitions, keys, offsets, consumer groups, committed offsets, and at-least-once delivery. Section 50.3 then shows how to run a real single-server Kafka broker on your own computer, and runs a real producer and consumer against it. That part is optional. Every output in this chapter comes from a real run.

---

## Why this matters

Everything in Part 5 so far has been **batch**: a pipeline runs at 6:30, does a day's work, and stops. Batch is the right answer far more often than people admit. But some questions genuinely can't wait for tomorrow morning.

Riverstone's plant is one of them. A machine running 12 °C hot produces scrap continuously, and the loss is per minute, not per day. By the time the nightly pipeline notices, a shift's output is ruined. The same shape appears in fraud detection, delivery tracking, stock levels during a sale, and any alert where the value of the answer decays in minutes.

Streaming is how you answer those questions. It's also where a set of new problems arrive: events that come out of order, events that come twice, events that come late, state that has to be kept between events, and jobs that must run forever rather than finish. This chapter meets all of them on Riverstone's sensor data, and ends with the question that matters more than any of the technology: *is this worth doing in real time at all?*

---

## In plain English

Think about the order counter at a busy restaurant.

- Orders arrive one after another and go onto a **spike** (the old metal spike receipts are pushed onto). Nothing is ever removed or edited; new slips go on top. That's a **log**, and it's what Kafka is.
- The kitchen has several spikes, one per section. A table's orders always go to the same spike, so that table's courses stay in order. That's **partitioning by key**: order is guaranteed within a partition, not across the restaurant.
- Each cook remembers how far down their spike they've got. That's an **offset**. Two teams can read the same spike at their own speed: **consumer groups**.
- If a cook is interrupted before writing down where they got to, they redo the last few slips: some dishes get made twice. That's **at-least-once delivery**, and the fix is to recognize a repeat.
- "How many dishes in the last 15 minutes?" needs a **window**, and the answer depends on whether you mean when the order was *placed* or when the slip *reached* the kitchen: **event time** versus **processing time**.
- A slip found on the floor at 9pm, written at 7pm, is **late data**. You decide how long to hold a window open for stragglers: that's a **watermark**.

---

## 50.0 Setting up

Work the way Chapter 48 did. In your file manager, copy the folder `companion/ch50` and paste it inside `work`, so you have `work/ch50` next to `work/ch48`. It holds two small Python files, which this chapter imports like any library:

| File | What it does | First used |
|---|---|---|
| `sensor_events.py` | Reads the Chapter 48 sensor archive and hands readings back as events, so you can replay them as a stream | Section 50.2 |
| `mini_log.py` | A small append-only message log that works the way Kafka does, kept in ordinary files | Section 50.2 |

The events come from the sensor data you generated in Chapter 48 (section 48.0, step 4). `sensor_events.py` looks for it in `../ch48/sensor_readings`, which is where it is if your two practice folders sit side by side. If you deleted it, run `python make_sensor_data.py` in `work/ch48` again: the seed makes it identical.

There's nothing new to install for the main thread. `pyspark` came in Chapter 48, `deltalake` in Chapter 49, `duckdb` in Chapter 45, and `pyarrow` in Chapter 18. On **Windows**, run this chapter in **WSL** (Chapter 34): from section 50.4 on, Spark writes files, which on Windows needs an extra download (Chapter 48's troubleshooting box), and the optional Kafka broker in section 50.3 needs a Linux or macOS terminal anyway.

Create a notebook `ch50.ipynb` in `work/ch50`, choose the `.venv` kernel (Chapter 17, section 17.0), and run each code block as its own cell, top to bottom, without restarting the kernel.

> **Tool note.** The outputs in this chapter were produced with Python 3.11.15, PySpark 4.2.0, deltalake 1.6.6, DuckDB 1.5.6, PyArrow 25.0.1, OpenJDK 21.0.10, Apache Kafka 4.3.1, and kafka-python 3.0.11. Your Python 3.14 environment gives the same outputs.

---

## 50.1 What "real-time" actually means

"Real-time" in a business conversation usually means "sooner than now". Before building anything, turn it into a number and a consequence.

| Latency | What it takes | Example |
|---|---|---|
| **Daily** | Batch (Chapters 45–47) | Riverstone's Daily Sales Flash |
| **Hourly** | Batch, run more often | Stock levels for Riverstone's warehouse team |
| **Minutes** | Micro-batch streaming | Riverstone's machine temperature alerts |
| **Seconds** | Streaming with a short trigger interval | Flagging suspicious account activity for review |
| **Milliseconds** | Not a data pipeline at all: application code | Blocking a card transaction |

**Micro-batch** streaming, in the third row, processes a stream as a series of small batches, one every few seconds to minutes, each holding whatever has arrived since the last. It's how most streaming jobs run, including the Spark jobs in this chapter.

Three questions settle most cases.

1. **What decision changes because the answer arrives sooner?** If nobody acts until the morning meeting, minute-level data buys nothing.
2. **What's the cost of being wrong or late by an hour?** For Riverstone: a shift's worth of scrap from one machine.
3. **Who watches it?** A stream that alerts at 3 a.m. needs someone on call. Streaming moves work from the pipeline to the operations rota.

> **Watch out: "real-time dashboard" is usually a batch job with a shorter schedule.** Refreshing a dashboard every 10 minutes is far simpler than a streaming pipeline, and often indistinguishable to users. Try that first.

---

## 50.2 The log: topics, partitions, offsets, groups

An event log is an **append-only** sequence of records. **Producers** add to the end; **consumers** read forwards and remember where they've got to. Nothing is updated in place, which is what makes the model simple to reason about and safe to replay.

![A log for the topic sensor-readings, drawn as two horizontal strips, partition 0 and partition 1, each a row of six numbered slots, offsets 0 to 5, followed by an empty dashed slot marked "off 6, next". Four producer boxes on the left send readings: M-04 and M-08 go to partition 0, and M-07 and M-21 go to partition 1, so each machine's readings sit in one partition only. Arrows under the strips mark each consumer group's committed offset: in partition 0 both groups are at offset 6; in partition 1 the alerting group is at offset 3, lag 3, and scrap-monitor is at offset 6, lag 0. Boxes on the right summarize the two groups. Notes underneath say that order is guaranteed inside a partition, that there is no order across partitions, and that a committed offset is the next position the group will read.](figures/fig50-1-log-partitions-offsets.svg)

*Figure 50.1 — A topic is a log split into partitions. A key always lands in the same partition. Offsets are kept per group and per partition, which is why two teams can read the same events at different speeds.*

| Term | What it means | Why it matters |
|---|---|---|
| **Topic** | A named stream of events (`sensor-readings`) | The unit producers and consumers agree on |
| **Partition** | One append-only log within a topic | Parallelism: more partitions, more consumers |
| **Key** | A value that decides the partition (the machine id) | All events for one key stay in order |
| **Offset** | A record's position in its partition, counting from 0 | Where a consumer has got to |
| **Consumer group** | A set of consumers sharing the work of a topic | Two teams read the same data independently |
| **Lag** | How far behind the end of the log a group is | The single most important streaming metric |
| **Retention** | How long events are kept | Decides how far back you can replay |
| **Broker** | A Kafka server: it stores partitions and serves producers and consumers | Production Kafka runs as a cluster of several brokers |
| **Replica** | A copy of a partition kept on another broker | If a broker dies, a replica takes over and nothing is lost |

### The two companion helpers

The events come from `sensor_events.py`. It has two functions:

| Call | What it returns or does |
|---|---|
| `se.readings(minute_from, minute_to)` | Every reading taken on 1 December 2025 from minute `minute_from` up to, but not including, minute `minute_to`, counted in minutes after midnight, like `range()`. 25 machines send 6 readings a minute (one every 10 seconds). |
| `se.readings(…, machine="M-07")` | The same, for one machine only |
| `se.write_batch(folder, name, events)` | Writes the events into one file of JSON lines, one event per line, the way a source system would drop a file of new events into a folder (used from section 50.4) |

Start with the first two minutes of the day:

```python
import sensor_events as se

first = se.readings(0, 2)
print("events:", len(first))
print(first[0])
```

```
events: 300
{'machine_id': 'M-01', 'plant': 'Bhiwandi Main', 'event_time': '2025-12-01 00:00:00', 'temperature_c': 187.28, 'units_made': 5, 'scrap': False}
```

- **`import sensor_events as se`** imports the companion file under the short name `se`, the way `pandas` becomes `pd`.
- **`se.readings(0, 2)`** returns minutes 0 and 1: every reading from 00:00:00 to 00:01:50. That's 25 machines × 6 readings × 2 minutes = 300 events.
- **`first[0]`** is the first event: a dictionary with the machine, its plant, the **event time** (when the reading was taken), the temperature, the units made in those 10 seconds, and whether the reading was flagged as scrap.

### The companion's log

`mini_log.py` defines `MessageLog`, a log kept in a folder of ordinary files: one text file per partition, one message per line, and one small JSON file per group holding its committed offsets. It's about 80 lines; open it in VS Code if you're curious. These are the calls this chapter uses, with the Kafka equivalent of each:

| Call | What it does | In Kafka |
|---|---|---|
| `MessageLog("stream_log", partitions=2, reset=True)` | Opens a log in the folder `stream_log` with 2 partitions; `reset=True` empties it first | Creating a topic with 2 partitions |
| `log.produce(key, value)` | Appends `value` to the end of the key's partition | `producer.send(topic, key=…, value=…)` |
| `log.partition_for(key)` | Which partition a key goes to: a hash of the key | Kafka's partitioner |
| `log.end_offsets()` | How many messages each partition holds | `consumer.end_offsets(…)` |
| `log.consume(group)` | Every message after the group's committed offsets, plus the offsets to commit once the work is done | `consumer.poll(…)` |
| `log.commit(group, offsets)` | Stores the group's position | `consumer.commit()` |
| `log.committed(group)` | The group's stored position, or `{}` if it has never committed | `consumer.committed(…)` |

Produce the 300 events into a log with two partitions, keyed by machine:

```python
from mini_log import MessageLog

log = MessageLog("stream_log", partitions=2, reset=True)
for e in first:
    log.produce(e["machine_id"], e)

print("end offsets:", log.end_offsets())
print("M-07 always goes to partition", log.partition_for("M-07"))
```

```
end offsets: {0: 144, 1: 156}
M-07 always goes to partition 1
```

- **`MessageLog("stream_log", partitions=2, reset=True)`** creates the folder `stream_log` inside `work/ch50`. `reset=True` means every run of the cell starts from an empty log.
- **`log.produce(e["machine_id"], e)`** sends each event with its machine id as the **key**. The key isn't stored separately from the event by accident: it's what decides the partition.
- **`log.end_offsets()`** returns `{partition: number of messages}`. The next message in a partition gets that number as its offset, because offsets count from 0.

**Reading it.** 300 events went into two partitions, 144 and 156, split by a hash of the machine id. Every M-07 event lands in partition 1, so M-07's readings are in order relative to each other; readings from *different* machines have no guaranteed order between them. That's the trade every log makes: order within a key, parallelism across keys. (The hash here is simple: the sum of the key's bytes. Kafka uses a stronger one, so the same machine can land in a different partition there, but the rule is the same.)

### Consuming, and committing

A **committed offset** is a group's saved position: the offset of the **next** message it will read, in each partition. Committing `{0: 144, 1: 156}` means "everything before these has been handled". A group that has never committed starts from the beginning.

```python
def hot_readings(messages, limit=205.0):
    return sum(1 for m in messages if m["value"]["temperature_c"] > limit)

print("committed:", log.committed("scrap-monitor") or "nothing yet")
messages, new_offsets = log.consume("scrap-monitor")
print("read     :", len(messages), "messages")
print(messages[0])
```

```
committed: nothing yet
read     : 300 messages
{'partition': 0, 'offset': 0, 'key': 'M-02', 'value': {'machine_id': 'M-02', 'plant': 'Bhiwandi Main', 'event_time': '2025-12-01 00:00:00', 'temperature_c': 198.4, 'units_made': 6, 'scrap': False}}
```

- **`hot_readings`** counts the messages whose temperature is above a limit, 205 °C by default. **`sum(1 for m in messages if …)`** adds up a 1 for every message that passes the test, which is a count.
- **`log.committed("scrap-monitor") or "nothing yet"`**: `committed` returns `{}` for a group that has never committed, and **`or`** gives back its right-hand side when the left is empty. So the line prints the offsets, or "nothing yet".
- **`log.consume("scrap-monitor")`** returns two things, which the line unpacks into two names (Chapter 17): the messages, and the offsets to commit once the work has succeeded. It doesn't commit anything itself.
- **`messages[0]`** shows what a message looks like: its partition, its offset, its key, and the event as its **value**. The first message is from partition 0, because `consume` reads partition 0 first.

Now do the work, commit, and read again:

```python
print("above 205 C:", hot_readings(messages))
log.commit("scrap-monitor", new_offsets)
print("committed  :", log.committed("scrap-monitor"))

again, _ = log.consume("scrap-monitor")
print("read again :", len(again), "- a committed group does not re-read")
```

```
above 205 C: 82
committed  : {0: 144, 1: 156}
read again : 0 - a committed group does not re-read
```

- **`log.commit("scrap-monitor", new_offsets)`** saves the group's position, *after* the work (the count) has been done.
- **`again, _ = …`** keeps the messages and throws the offsets away: **`_`** is the usual Python name for "a value I don't need".

**Reading it.** The consumer counted 82 readings above 205 °C, and then **committed** its offsets. A second read returns nothing, because the group's position is stored. A different group, with its own committed offsets, would read the same 300 events again: that's how an alerting service and a reporting service share one topic without interfering.

---

## 50.3 Delivery guarantees, and the duplicates you will get

Three guarantees are worth naming.

- **At-most-once:** commit the offset first, then do the work. If you crash in between, the event is never processed. Nothing is duplicated, some things are lost.
- **At-least-once:** do the work, then commit. If you crash in between, the event is processed again. Nothing is lost, some things are duplicated. **This is the default in practice.**
- **Exactly-once:** achieved only when the processing and the offset commit happen in one transaction, which requires support on both sides: Kafka transactions, or Spark's checkpoint (section 50.4) plus an idempotent sink. A **sink** is wherever a stream's results are written: files, a table, an alert channel. **Idempotent** means what it meant in Chapter 46: writing the same batch twice leaves the same result as writing it once. Exactly-once is real, it's narrower than it sounds, and it's slower.

### By hand first: a crash at the wrong moment

Take a log with five messages, offsets 0 to 4, where the readings at offsets 1 and 3 are hot and should each send one alert. The consumer reads all five, and crashes at the worst possible moment. Follow both orders:

| Step | At-least-once: work, then commit | At-most-once: commit, then work |
|---|---|---|
| 1 | Read offsets 0–4 | Read offsets 0–4 |
| 2 | Send the alerts for offsets 1 and 3 | Commit offset 5 |
| 3 | **Crash** before committing | **Crash** before sending |
| 4 | Restart from the committed offset: 0 | Restart from the committed offset: 5 |
| 5 | Read 0–4 again, send alerts 1 and 3 again, commit 5 | Nothing left to read |
| **Result** | Nothing lost; 2 alerts **duplicated** | Nothing duplicated; 2 alerts **lost** |

For alerts, a lost one is worse than a repeated one, so choose at-least-once and make the repeat harmless. Here's the duplicate happening for real. A second group, `alerting`, has never committed, so it starts at the beginning:

```python
messages, new_offsets = log.consume("alerting")
print("alerts sent      :", hot_readings(messages))
print("... crash before committing")

messages, new_offsets = log.consume("alerting")
print("re-read          :", len(messages), "messages")
print("alerts sent again:", hot_readings(messages), "- the same alerts go out twice")
```

```
alerts sent      : 82
... crash before committing
re-read          : 300 messages
alerts sent again: 82 - the same alerts go out twice
```

- The first `consume` reads all 300 messages and "sends" 82 alerts (here, `hot_readings` counts them instead of sending them).
- The crash is only a printed line: the point is that **`log.commit` never ran**.
- The second `consume` is the restarted consumer. With no committed offsets, it starts from the beginning again.

**Reading it.** The crash before committing meant all 82 alerts were sent a second time. A plant supervisor's phone buzzing twice for the same reading is exactly how people learn to ignore alerts (Chapter 47).

### Remembering what was sent

The fix is Chapter 46's delivery log (section 46.3): before sending, check a record of what has already been sent. The record must be kept **on disk**, not in a Python variable, because a real crash ends the Python process and empties its memory. Here it's a one-column DuckDB table in a file, keyed by a **de-duplication key**: the machine plus the event time, which names one reading exactly.

```python
import duckdb

sent_log = duckdb.connect("alerts_sent.duckdb")
sent_log.execute("CREATE OR REPLACE TABLE sent (alert_key VARCHAR PRIMARY KEY)")

def send_once(messages):
    sent = 0
    for m in messages:
        if m["value"]["temperature_c"] > 205.0:
            key = m["key"] + " " + m["value"]["event_time"]
            found = sent_log.execute("SELECT count(*) FROM sent WHERE alert_key = ?",
                                     [key]).fetchone()[0]
            if found == 0:
                sent += 1                                   # send the alert here
                sent_log.execute("INSERT INTO sent VALUES (?)", [key])
    return sent

print("first pass:", send_once(messages))
```

```
first pass: 82
```

- **`duckdb.connect("alerts_sent.duckdb")`** opens (or creates) a DuckDB database in a file, as in Chapter 45. **`CREATE OR REPLACE TABLE`** starts the table empty each time you run the cell; in production you'd create it once and keep it.
- **`PRIMARY KEY`** makes the database refuse a second row with the same key, a safety net under the check.
- **`key = m["key"] + " " + …`** builds the de-duplication key, for example `M-07 2025-12-01 00:00:10`.
- **`SELECT count(*) … WHERE alert_key = ?`** asks whether this key was sent before; `?` is filled from the list `[key]` (Chapter 45). **`.fetchone()[0]`** takes the single number out of the one-row result.
- Only a key that isn't there yet is sent, then recorded with **`INSERT`**. Sending and recording are two steps: a crash exactly between them can still repeat one alert. Systems that must never repeat one also give the receiving system an **idempotency key** it checks itself (Chapter 51).

Now a real restart: close the database, as a crashing consumer would, and open it again, as the restarted one would.

```python
sent_log.close()
sent_log = duckdb.connect("alerts_sent.duckdb")
print("after a restart, second pass:", send_once(messages))
log.commit("alerting", new_offsets)
```

```
after a restart, second pass: 0
```

- **`sent_log.close()`** drops the connection; the table survives in the file.
- The new connection sees all 82 keys, so the second pass sends nothing. Then, at last, the consumer commits.

**Reading it.** The first pass sent 82 alerts; after the restart, the same 300 messages sent none, because the keys were on disk. A Python `set()` of sent keys would have printed 0 here too, but only because nothing really restarted: in a real crash it would be empty again and all 82 alerts would go out twice.

Why machine plus event time, and not the message's partition plus offset? Partition and offset catch a consumer re-reading the same record. They don't catch a producer sending the same reading twice, as two records with two offsets. A **business key** like machine plus event time catches both.

**The rule to remember: assume duplicates, and make the effect of a repeat harmless.** Upserts (Chapter 45), delivery logs (Chapter 46), and idempotency keys (Chapter 51) are the three tools.

### Optional: a real Kafka broker on your computer

Everything above works the same way against real Kafka. If you want to see it, you can run a single Kafka broker on your own computer in about half an hour. It's optional: if you skip it, read the two Kafka cells after it as the code you'll meet at work, and carry on at section 50.4.

You need Java 17 or later (Java 21 from Chapter 48 is fine) and a Linux or macOS terminal; on Windows, use WSL (Chapter 34). Kafka's download page, kafka.apache.org/downloads, lists the current release; this chapter used 4.3.1. In the terminal, in `work/ch50`:

```
# terminal
$ curl --silent --remote-name https://downloads.apache.org/kafka/4.3.1/kafka_2.13-4.3.1.tgz
$ tar -xzf kafka_2.13-4.3.1.tgz
$ cd kafka_2.13-4.3.1
$ KAFKA_CLUSTER_ID="$(bin/kafka-storage.sh random-uuid)"
$ bin/kafka-storage.sh format --standalone -t "$KAFKA_CLUSTER_ID" -c config/server.properties | tail -n 1
Formatting dynamic metadata voter directory /tmp/kraft-combined-logs with metadata.version 4.3-IV0.
$ bin/kafka-server-start.sh config/server.properties > kafka.log 2>&1 &
$ sleep 10
$ bin/kafka-topics.sh --create --topic sensor-readings --partitions 2 --bootstrap-server localhost:9092
Created topic sensor-readings.
```

- **`curl --silent --remote-name URL`** downloads the file and saves it under its own name (Chapter 34). Older releases move to archive.apache.org/dist/kafka/, so if this link stops working, take the newest release from the download page and change the version in the next two lines.
- **`tar -xzf file.tgz`** unpacks a compressed archive: `x` extract, `z` it's gzip-compressed, `f` the file name follows. It makes the folder `kafka_2.13-4.3.1` (2.13 is the version of Scala, the language Kafka is built with).
- **`KAFKA_CLUSTER_ID="$(…)"`** runs Kafka's tool to make a random cluster id and stores it in a shell variable (`$( )` from Chapter 34).
- **`kafka-storage.sh format`** prepares the folder where the broker will keep its log, named in `config/server.properties`: `/tmp/kraft-combined-logs`. `--standalone` means one server acting as both broker and controller, the part that keeps track of the cluster. You run this once. `/tmp` may be emptied when your computer restarts, which is fine for practice: format again if it is.
- **`kafka-server-start.sh … > kafka.log 2>&1 &`** starts the broker in the background, with its messages going to `kafka.log`, exactly like Chapter 34's file server. `sleep 10` gives it time to start.
- **`kafka-topics.sh --create`** creates the topic `sensor-readings` with 2 partitions. **`--bootstrap-server localhost:9092`** is the broker's address: this computer, port 9092.

Then install the Python client, with the book's virtual environment active, and add `kafka-python` to your `requirements.txt`:

<!-- run: none -->
```
# terminal
$ cd ..
$ python -m pip install kafka-python==3.0.11
```

When you've finished with this section, stop the broker from inside its folder with `bin/kafka-server-stop.sh`. To start it again another day, repeat only the `kafka-server-start.sh` and `sleep` lines.

### The same thing in Kafka

These two cells are the producer and consumer from section 50.2, against the real broker. They need the broker above to be running; without one, the first cell waits about a minute and then stops with `KafkaTimeoutError: Unable to bootstrap`. First the producer, sending the same 300 events:

```python
from kafka import KafkaProducer
from kafka.serializer import DefaultSerializer, JsonSerializer

producer = KafkaProducer(
    bootstrap_servers=["localhost:9092"],
    key_serializer=DefaultSerializer(),
    value_serializer=JsonSerializer(),
    acks="all",
    retries=5,
    enable_idempotence=True,
)
events = first
for event in events:
    producer.send("sensor-readings", key=event["machine_id"], value=event)
producer.flush()
print("sent:", len(events))
```

```
sent: 300
```

| Argument | Value here | What it does | If you change it |
|---|---|---|---|
| `bootstrap_servers` | `["localhost:9092"]` | Where to find the cluster. One broker's address is enough; the client learns the rest from it | A wrong address: the client can't connect and stops with `KafkaTimeoutError` |
| `key_serializer` | `DefaultSerializer()` | Turns the text key into bytes, which is all Kafka stores | Leave it out and `send` needs bytes: a text key fails |
| `value_serializer` | `JsonSerializer()` | Turns the dictionary into JSON text, then bytes | Leave it out and a dictionary can't be sent |
| `acks` | `"all"` | The broker confirms a record only when every in-sync replica has it: durability over speed | `1`: faster, but a record can be lost if a broker dies before copying it; `0`: no confirmation at all |
| `retries` | `5` | Resends up to 5 times after a temporary failure | `0`: one network blip loses the record |
| `enable_idempotence` | `True` | The broker drops copies created by this producer's own retries | `False`: a retry can store the same record twice |

- **`events = first`** reuses the 300 readings from section 50.2.
- **`producer.send("sensor-readings", key=…, value=…)`** hands one event to the producer, which sends it in the background, grouped with others for speed. `send` returns at once.
- **`producer.flush()`** waits until everything handed over has been sent and confirmed.

Now the consumer. Creating it only connects; nothing is read yet:

```python
from kafka import KafkaConsumer

consumer = KafkaConsumer(
    "sensor-readings",
    bootstrap_servers=["localhost:9092"],
    group_id="scrap-monitor",
    auto_offset_reset="earliest",
    enable_auto_commit=False,
    key_deserializer=DefaultSerializer(),
    value_deserializer=JsonSerializer(),
    max_poll_records=500,
)
```

| Argument | Value here | What it does | If you change it |
|---|---|---|---|
| `"sensor-readings"` | the topic | Which topic to read | |
| `group_id` | `"scrap-monitor"` | The consumer group; Kafka keeps its committed offsets on the broker | A new group name starts again, as a second team would |
| `auto_offset_reset` | `"earliest"` | Where to start when the group has no committed offset: the oldest event kept | `"latest"`: only events that arrive from now on |
| `enable_auto_commit` | `False` | Offsets move only when the code calls `commit()`, after the work succeeded: at-least-once | `True`: offsets are committed every few seconds, whether the work is done or not (see Common mistakes) |
| `key_deserializer`, `value_deserializer` | the same two helpers | Turn the stored bytes back into text and a dictionary | Leave them out and you get raw bytes |
| `max_poll_records` | `500` | At most 500 records per `poll` | Smaller: more, smaller batches |

Then the reading loop:

```python
def handle(value):
    return 1 if value["temperature_c"] > 205.0 else 0

read, hot = {0: 0, 1: 0}, 0
while True:
    batch = consumer.poll(timeout_ms=5000)
    if not batch:
        break
    for partition, records in batch.items():
        read[partition.partition] += len(records)
        for record in records:
            hot += handle(record.value)
    consumer.commit()
consumer.close()

print("read per partition:", read)
print("above 205 C       :", hot)
```

```
read per partition: {0: 96, 1: 204}
above 205 C       : 82
```

- **`handle`** is the work done for each event; here it returns 1 for a hot reading, so `hot` counts them. At work it would send an alert or write a row.
- **`consumer.poll(timeout_ms=5000)`** waits up to 5 seconds for new records and returns a dictionary, `{partition: [records]}`. It's empty if nothing arrived. The first poll can take a few seconds while the broker registers the group.
- **`if not batch: break`** stops the loop when nothing new arrived for 5 seconds. A real consumer is a service that never stops: it would leave this line out and keep polling.
- Each key of `batch` describes a partition; **`partition.partition`** is its number. Each **`record`** has `.key`, `.value`, `.partition`, and `.offset`.
- **`consumer.commit()`** comes only after every record in the batch was handled: at-least-once. **`consumer.close()`** leaves the group cleanly.

**Reading it.** The consumer read the same 300 readings and found the same 82 hot ones. The split between partitions differs from `mini_log`'s 144 and 156, because Kafka's partitioner uses a different hash, but each machine still sits in exactly one partition. Run the loop cell again and it reads nothing: the group's offsets are committed on the broker.

The settings that matter most are `acks`, `enable_idempotence`, `auto_offset_reset`, and turning **off** auto-commit so offsets move only after the work has succeeded. Managed services (Amazon MSK, Confluent Cloud, Azure Event Hubs, Google Pub/Sub) differ in operations, not in this model.

---

## 50.4 Streaming with Spark: the same code, running forever

A streaming query in Spark looks almost identical to a batch one. The difference is that it never finishes: it processes what has arrived, records where it got to, and waits. Spark's picture of a stream is a table that keeps growing, an **unbounded table**: each micro-batch processes the rows that arrived since the last one.

Start a Spark session as in Chapter 48 (section 48.0, step 5):

```python
from pyspark.sql import SparkSession, functions as F, types as T

spark = (SparkSession.builder
         .appName("riverstone-stream")
         .master("local[2]")
         .config("spark.sql.shuffle.partitions", "4")
         .config("spark.ui.showConsoleProgress", "false")
         .config("spark.sql.streaming.schemaInference", "false")
         .getOrCreate())
spark.sparkContext.setLogLevel("ERROR")
print("Spark", spark.version, "is running")
```

```
Spark 4.2.0 is running
```

`appName`, `master("local[2]")`, `showConsoleProgress`, `getOrCreate()`, and `setLogLevel("ERROR")` are Chapter 48's. Two settings are new here, and one import:

| Setting | Value here | What it does |
|---|---|---|
| `spark.sql.shuffle.partitions` | `4` | How many pieces Spark cuts the data into after a shuffle (Chapter 48, section 48.3). Grouping by window is a shuffle, and each piece becomes an output file, so it matters for section 50.6 |
| `spark.sql.streaming.schemaInference` | `false` | Never guess a stream's columns from its files. It's already Spark's default; setting it says so on purpose |

- **`types as T`** imports Spark's data types under the short name `T`, the way `functions` became `F`.

A stream must be told its columns in advance, as a **schema**. A schema is a `StructType`, a list of columns; each column is a `StructField` with a name and a type:

```python
SCHEMA = T.StructType([
    T.StructField("machine_id", T.StringType()),
    T.StructField("plant", T.StringType()),
    T.StructField("event_time", T.TimestampType()),
    T.StructField("temperature_c", T.DoubleType()),
    T.StructField("units_made", T.IntegerType()),
    T.StructField("scrap", T.BooleanType()),
])
print(SCHEMA.fieldNames())
```

```
['machine_id', 'plant', 'event_time', 'temperature_c', 'units_made', 'scrap']
```

- **`StringType`**, **`DoubleType`** (a decimal number), **`IntegerType`**, and **`BooleanType`** match the event's text, temperature, count, and True/False values.
- **`TimestampType`** turns the text `"2025-12-01 00:00:00"` into a real date and time. Windows need it: Spark can't cut text into 5-minute windows.
- Why not let Spark guess? On a stream, a later file with different columns would silently change the meaning of the job. Declaring the schema makes that file fail loudly instead.

Now the source. A folder of JSON-lines files is the simplest streaming source, and enough to teach every idea in this chapter: the job reads each new file that appears. Write the first file, ten minutes of readings, and point a stream at the folder:

```python
import os, shutil

for folder in ["events_in", "stream_out", "checkpoints"]:
    shutil.rmtree(folder, ignore_errors=True)
os.makedirs("events_in")

se.write_batch("events_in", "batch-01.json", se.readings(0, 10))
stream = spark.readStream.schema(SCHEMA).json("events_in")
print("streaming?", stream.isStreaming)
stream.printSchema()
```

```
streaming? True
root
 |-- machine_id: string (nullable = true)
 |-- plant: string (nullable = true)
 |-- event_time: timestamp (nullable = true)
 |-- temperature_c: double (nullable = true)
 |-- units_made: integer (nullable = true)
 |-- scrap: boolean (nullable = true)
```

- The loop deletes the three folders this section uses, so every run of the notebook starts clean. **`shutil.rmtree`** deletes a folder and everything in it; **`ignore_errors=True`** means "don't complain if it isn't there". **`os.makedirs`** creates the input folder again.
- **`se.write_batch(…, se.readings(0, 10))`** drops a file with minutes 0 to 9, 00:00:00 to 00:09:50: 25 × 6 × 10 = 1,500 readings.
- **`spark.readStream`** is `spark.read` for streams. **`.schema(SCHEMA)`** declares the columns; **`.json("events_in")`** reads JSON-lines files from the folder. In production this would be `.format("kafka")` with the broker's address and a topic; the rest of the code is unchanged.
- **`isStreaming`** confirms Spark treats this as an unbounded table. **`printSchema()`** (Chapter 48) shows the declared columns: `event_time` is a timestamp.

Nothing has been read yet. A streaming DataFrame is a plan, like Chapter 48's lazy DataFrames, until a query starts it. Two more ideas decide how the query runs:

**Triggers** decide when Spark runs a micro-batch: `processingTime="30 seconds"` for a steady job, `availableNow=True` to process everything waiting and stop (used here, so each step of the chapter is one run you can look at), or continuous mode for the lowest latency at some cost in features.

**Checkpoints** are how a streaming job survives restarts: Spark writes the files and offsets it has processed, and its running state, to the folder named in `checkpointLocation`. The next run reads the checkpoint and carries on where the last one stopped. Delete the checkpoint, or point the job at a new location, and it re-processes everything from the start; change the query's aggregation and the old checkpoint may no longer be usable. Treat it as part of the job's data.

---

## 50.5 Event time, windows, and watermarks

Two clocks matter.

- **Event time:** when the thing happened (the reading was taken at 00:02:10).
- **Processing time:** when your pipeline saw it (the file arrived at 00:14).

They differ, and the gap is where the hard problems live: a machine loses its network for ten minutes, a phone app syncs when it reconnects, a batch of events is retried. **Always aggregate on event time**, or your numbers change depending on how fast your pipeline happened to be.

### Three kinds of window, by hand

A **window** groups events by event time. Take eight readings, taken at 00:01, 00:03, 00:04, 00:07, 00:13, 00:14, 00:21, and 00:22, and count them three ways.

**Tumbling windows** of 5 minutes sit one after another with no overlap, so each event is counted once. Window 00:00–00:05 includes 00:00 but not 00:05:

| Window | Readings | Count |
|---|---|---|
| 00:00–00:05 | 00:01, 00:03, 00:04 | 3 |
| 00:05–00:10 | 00:07 | 1 |
| 00:10–00:15 | 00:13, 00:14 | 2 |
| 00:15–00:20 | none | no row |
| 00:20–00:25 | 00:21, 00:22 | 2 |

**Sliding windows** of 10 minutes, starting every 5 minutes, overlap, so each event is counted twice: 23:55–00:05 has 3, 00:00–00:10 has 4, 00:05–00:15 has 3, 00:10–00:20 has 2, 00:15–00:25 has 2, and 00:20–00:30 has 2. That's 16 counts for 8 readings. Use them for "the last 10 minutes, updated every 5".

**Session windows** with a gap of 5 minutes group activity separated by quiet spells. A session starts at an event and stays open until 5 minutes pass with no new event: {00:01, 00:03, 00:04, 00:07} is one session, from 00:01 to 00:12 (the last event plus the gap), with 4 readings; {00:13, 00:14} runs from 00:13 to 00:19, with 2; {00:21, 00:22} from 00:21 to 00:27, with 2. Use them for "how long was this machine busy?"

Now check the hand counts in Spark. This cell makes a tiny DataFrame of the eight times, and a helper that counts rows per window and shows each window's start and end:

```python
times = ["00:01", "00:03", "00:04", "00:07", "00:13", "00:14", "00:21", "00:22"]
toy = spark.createDataFrame([("2025-12-01 " + t + ":00",) for t in times], ["event_time"])
toy = toy.withColumn("event_time", F.to_timestamp("event_time"))

def count_windows(window):
    counts = toy.groupBy(window.alias("w")).count().orderBy("w")
    counts.select(F.date_format("w.start", "HH:mm").alias("start"),
                  F.date_format("w.end", "HH:mm").alias("end"),
                  "count").show()

count_windows(F.window("event_time", "5 minutes"))
```

```
+-----+-----+-----+
|start|  end|count|
+-----+-----+-----+
|00:00|00:05|    3|
|00:05|00:10|    1|
|00:10|00:15|    2|
|00:20|00:25|    2|
+-----+-----+-----+
```

- **`createDataFrame`** (Chapter 48) builds the DataFrame from a list of rows. Each row is a **tuple** with one item, written `(value,)`: the comma is what makes it a tuple. **`F.to_timestamp`** turns the text into a timestamp.
- **`F.window("event_time", "5 minutes")`** is a tumbling window: it gives each row the 5-minute window its event time falls in. Grouping by it and counting gives one row per window that has events.
- A window is one column holding **two values**, a `start` and an `end`. **`.alias("w")`** names it `w`, so `"w.start"` and `"w.end"` reach inside it.
- **`F.date_format(…, "HH:mm")`** prints a timestamp as hours and minutes. **`orderBy("w")`** sorts by window, earliest first.

**Reading it.** 3, 1, 2, 2, as by hand, and there's no row for 00:15–00:20: Spark never writes a row for a window with no events. The other two kinds are one argument away:

```python
count_windows(F.window("event_time", "10 minutes", "5 minutes"))
```

```
+-----+-----+-----+
|start|  end|count|
+-----+-----+-----+
|23:55|00:05|    3|
|00:00|00:10|    4|
|00:05|00:15|    3|
|00:10|00:20|    2|
|00:15|00:25|    2|
|00:20|00:30|    2|
+-----+-----+-----+
```

- The third argument, **`"5 minutes"`**, is the slide: a new 10-minute window starts every 5 minutes. Without it, the window is tumbling.

```python
count_windows(F.session_window("event_time", "5 minutes"))
```

```
+-----+-----+-----+
|start|  end|count|
+-----+-----+-----+
|00:01|00:12|    4|
|00:13|00:19|    2|
|00:21|00:27|    2|
+-----+-----+-----+
```

- **`F.session_window("event_time", "5 minutes")`** closes a session after 5 minutes without an event.

Both match the hand counts. The rest of this chapter uses **tumbling** windows of 5 minutes.

### Watermarks: how long to wait for late events

A reading taken at 00:02 can arrive at 00:15. Should it still count in the 00:00–00:05 window? A streaming job can't wait forever, or it would hold every window open and never publish anything. A **watermark** is the promise: *"I will wait this long for late events, and then I'll close the window."* It's the knob that trades completeness for latency, and it also bounds how much the job must keep in memory.

> **The watermark rule.** After each run, the watermark is the newest event time seen so far, minus the delay you chose (10 minutes here). During the next run, a reading older than that watermark is dropped. A window is final, and append mode writes it, once the watermark has passed its end.

> **Watch out: same word, different job.** In Chapter 45 a watermark was the highest ID or timestamp a batch load had already read, so the next load could start after it. In streaming it's a moving cut-off in event time: "I've seen events up to 00:19:50, and I'll wait 10 more minutes for stragglers." Both mean "how far we've got", but a streaming watermark decides what gets dropped.

Here is what the rule does over three runs of the job. Each run brings a new file: ten minutes of readings on time, and in runs 2 and 3, six readings taken at 00:02 that arrive late. Work it out before looking at the code:

| Run | Events arriving | Watermark in force | Six late readings (00:02) | Watermark after the run | Windows written |
|---|---|---|---|---|---|
| 1 | 00:00 to 00:09:50 | none yet | none | 00:09:50 − 10 min = 23:59:50 | none |
| 2 | 00:10 to 00:19:50, plus six M-07 at 00:02 | 23:59:50 | **kept**: 00:02 is later than 23:59:50 | 00:19:50 − 10 min = 00:09:50 | 00:00–00:05 |
| 3 | 00:20 to 00:29:50, plus six M-09 at 00:02 | 00:09:50 | **dropped**: 00:02 is earlier than 00:09:50 | 00:29:50 − 10 min = 00:19:50 | 00:05–00:10, 00:10–00:15 |

After run 2, window 00:05–00:10 isn't written yet: it ends at 00:10:00, which the watermark, 00:09:50, hasn't passed. It waits for run 3. Figure 50.2 draws the same three runs.

![A timeline of event time from 00:00 to 00:30, with six 5-minute windows drawn above it as boxes. The first three boxes show Bhiwandi Main's readings after all three runs: 456 = 450 + 6, then 450, then 450; the last three are still open. A red dot at 00:02 marks the late readings: six from M-07 arrive in run 2 and six from M-09 in run 3. Three dashed vertical lines mark the watermark after each run: 23:59:50, 00:09:50, and 00:19:50, each labelled in text. Below, three cards describe the runs. Run 1, events 00:00 to 00:09:50: no watermark in force yet, 23:59:50 after the run, so nothing is written. Run 2, events 00:10 to 00:19:50 plus six M-07 readings from 00:02: watermark in force 23:59:50, so the six are kept and the window counts 456; afterwards the watermark is 00:09:50, so 00:00–00:05 is written and 00:05–00:10, which ends at 00:10:00, waits. Run 3, events 00:20 to 00:29:50 plus six M-09 readings from 00:02: watermark in force 00:09:50, so the six are dropped and 456 stays 456; afterwards the watermark is 00:19:50, so 00:05–00:10 and 00:10–00:15 are written. A closing line states the rule: a window is final once the watermark passes its end, and a reading older than the watermark in force is dropped.](figures/fig50-2-event-time-watermark.svg)

*Figure 50.2 — The watermark decides which late events still count, and when a window is final. Same late readings, different arrival times, different answers.*

### The windowed query, one step at a time

First the calculation: readings, average temperature, and scrap readings per 5-minute window and plant, with a 10-minute watermark:

```python
windowed = (stream
    .withWatermark("event_time", "10 minutes")
    .groupBy(F.window("event_time", "5 minutes"), "plant")
    .agg(F.count("*").alias("readings"),
         F.round(F.avg("temperature_c"), 2).alias("avg_temp_c"),
         F.sum(F.col("scrap").cast("int")).alias("scrap_readings")))
windowed.printSchema()
```

```
root
 |-- window: struct (nullable = false)
 |    |-- start: timestamp (nullable = true)
 |    |-- end: timestamp (nullable = true)
 |-- plant: string (nullable = true)
 |-- readings: long (nullable = false)
 |-- avg_temp_c: double (nullable = true)
 |-- scrap_readings: long (nullable = true)
```

- **`.withWatermark("event_time", "10 minutes")`** sets the watermark: the newest `event_time` seen, minus 10 minutes. It must come before the `groupBy` it applies to.
- **`.groupBy(F.window("event_time", "5 minutes"), "plant")`** makes one group per 5-minute window and plant, like the toy example with a second grouping column.
- **`F.count("*")`**, **`F.avg`**, and **`F.round(…, 2)`** are Chapter 48's. **`F.col("scrap").cast("int")`** turns True and False into 1 and 0 (Chapter 48), so **`F.sum`** counts the scrap readings.
- The schema shows the `window` column holding a `start` and an `end`, as in the toy example.

Next, a helper that runs the query once. Each run of the job will call it:

```python
def run_once():
    query = (windowed.writeStream
             .format("parquet")
             .option("path", "stream_out/windows")
             .option("checkpointLocation", "checkpoints/windows")
             .outputMode("append")
             .trigger(availableNow=True)
             .start())
    query.awaitTermination()
    return query
```

- **`writeStream`** is `write` for streams. **`.format("parquet")`** makes the sink a folder of Parquet files, and **`.option("path", …)`** names it.
- **`.option("checkpointLocation", "checkpoints/windows")`** is where Spark keeps its place. Because every run uses the same checkpoint, run 2 carries on from where run 1 stopped: it reads only the new file, and it remembers the open windows and the watermark.
- **`.outputMode("append")`** writes a window only once it's final (the table after this list).
- **`.trigger(availableNow=True)`** processes whatever has arrived, then stops.
- **`.start()`** starts the query and returns at once, while Spark works in the background. **`query.awaitTermination()`** waits until the run is finished. The function returns the query, so you can ask it afterwards what it did.

Output modes decide what a sink receives:

| Mode | Emits | Use for |
|---|---|---|
| **append** | Rows that are final (past the watermark) | Files, tables, downstream pipelines |
| **update** | Rows that changed in this micro-batch | Dashboards and alerting where "so far" is fine |
| **complete** | The whole result each time | Small aggregates only; the state grows forever |

Last, a helper to look at what the sink holds so far:

```python
def show_windows():
    result = spark.read.parquet("stream_out/windows")
    print("windows written so far:", result.count())
    (result.orderBy("window", "plant")
           .select(F.date_format("window.start", "HH:mm").alias("window_start"),
                   F.date_format("window.end", "HH:mm").alias("window_end"),
                   "plant", "readings", "avg_temp_c", "scrap_readings")
           .show(truncate=False))
```

- **`spark.read.parquet`** reads the sink as an ordinary batch table (Chapter 48). The whole chain is in round brackets so it can run over several lines.
- **`show(truncate=False)`** prints full values (Chapter 48).

Before you run the first run, predict from the hand table: how many windows will it write?

```python
query = run_once()
show_windows()
```

```
windows written so far: 0
+------------+----------+-----+--------+----------+--------------+
|window_start|window_end|plant|readings|avg_temp_c|scrap_readings|
+------------+----------+-----+--------+----------+--------------+
+------------+----------+-----+--------+----------+--------------+
```

**Reading it.** The first run wrote **nothing at all**, and that's correct. In **append** mode a window is written only once the watermark has passed its end, so that the result never has to change. The first file's events end at 00:09:50, the watermark after the run is 10 minutes earlier, 23:59:50, and no window ends that early. This surprises everyone once.

### Late data that still counts

Run 2 drops the next ten minutes into the folder, plus six M-07 readings taken at 00:02 that arrive only now:

```python
on_time = se.readings(10, 20)
late = se.readings(2, 3, machine="M-07")
se.write_batch("events_in", "batch-02.json", on_time + late)
print("run 2:", len(on_time), "on time,", len(late), "late (event time 00:02)")

query = run_once()
show_windows()
```

```
run 2: 1500 on time, 6 late (event time 00:02)
windows written so far: 2
+------------+----------+-------------+--------+----------+--------------+
|window_start|window_end|plant        |readings|avg_temp_c|scrap_readings|
+------------+----------+-------------+--------+----------+--------------+
|00:00       |00:05     |Bhiwandi Main|456     |196.04    |4             |
|00:00       |00:05     |Chakan Pune  |300     |195.76    |4             |
+------------+----------+-------------+--------+----------+--------------+
```

- **`se.readings(10, 20)`** is 00:10:00 to 00:19:50: 1,500 readings. **`se.readings(2, 3, machine="M-07")`** is M-07's six readings from minute 2, 00:02:00 to 00:02:50.
- **`on_time + late`** joins the two lists, so the late readings sit in the same file as the new ones, as they would if a machine's network came back.

**Reading it.** The six readings from 00:02 arrived well after their window's end. The watermark in force was 23:59:50, and 00:02 is later than that, so they were **still counted**: Bhiwandi Main's 00:00–00:05 window shows **456 readings**, not the 450 that arrived on time (15 machines × 6 readings × 5 minutes = 450; M-07 is at Bhiwandi Main). Chakan Pune's 10 machines give 10 × 30 = 300. After the run the watermark moved to 00:09:50, which passed the end of 00:00–00:05, so that window was written. 00:05–00:10 ends at 00:10:00 and is still open.

### Late data that doesn't

Run 3 does the same with six readings from M-09, also taken at 00:02:

```python
very_late = se.readings(2, 3, machine="M-09")
se.write_batch("events_in", "batch-03.json", se.readings(20, 30) + very_late)

query = run_once()
show_windows()
```

```
windows written so far: 6
+------------+----------+-------------+--------+----------+--------------+
|window_start|window_end|plant        |readings|avg_temp_c|scrap_readings|
+------------+----------+-------------+--------+----------+--------------+
|00:00       |00:05     |Bhiwandi Main|456     |196.04    |4             |
|00:00       |00:05     |Chakan Pune  |300     |195.76    |4             |
|00:05       |00:10     |Bhiwandi Main|450     |195.88    |4             |
|00:05       |00:10     |Chakan Pune  |300     |195.87    |3             |
|00:10       |00:15     |Bhiwandi Main|450     |196.01    |5             |
|00:10       |00:15     |Chakan Pune  |300     |195.94    |6             |
+------------+----------+-------------+--------+----------+--------------+
```

**Reading it.** This time the watermark in force was 00:09:50, and the six M-09 readings from 00:02 are older than that, so they were **dropped**: the 00:00–00:05 window is unchanged at 456. Nothing failed, nothing was logged as an error, and the published numbers stayed stable. After the run the watermark moved to 00:19:50, so the windows 00:05–00:10 and 00:10–00:15 were written. That's the deal a watermark makes on your behalf, which is why it should be a deliberate decision rather than a default.

### What the query reports

A query keeps a progress report for each micro-batch of its run in **`query.recentProgress`**: a list of dictionaries. Look at the keys of the first one:

```python
progress = query.recentProgress
print(len(progress), "reports in this run")
print(list(progress[0].keys()))
```

```
2 reports in this run
['id', 'runId', 'name', 'timestamp', 'batchId', 'batchDuration', 'durationMs', 'eventTime', 'stateOperators', 'sources', 'sink', 'numInputRows', 'inputRowsPerSecond', 'processedRowsPerSecond', 'observedMetrics']
```

Four keys matter here. **`batchId`** numbers the micro-batches. **`numInputRows`** is how many new rows the micro-batch read. **`eventTime`** holds the watermark the micro-batch used. **`stateOperators`** is a list with one entry per step that keeps state; its first entry holds **`numRowsTotal`**, the rows kept in state, and **`numRowsDroppedByWatermark`**, the rows dropped as too late. Print those for each report:

```python
for p in progress:
    state = p["stateOperators"][0]
    print(f"batch {p['batchId']}: rows {p['numInputRows']:>4}, "
          f"watermark {p['eventTime']['watermark'][11:19]}, "
          f"dropped {state['numRowsDroppedByWatermark']}, "
          f"windows in state {state['numRowsTotal']}")
```

```
batch 4: rows 1506, watermark 00:09:50, dropped 1, windows in state 10
batch 5: rows    0, watermark 00:19:50, dropped 0, windows in state 6
```

- The watermark is text like `2025-12-01T00:09:50.000Z`; **`[11:19]`** slices out the time (Chapter 17). **`:>4`** right-aligns the number in 4 characters.

**Reading it.** Batch ids count every micro-batch since the checkpoint was created, across all three runs: run 1 was batches 0 and 1, run 2 was 2 and 3, and run 3, this one, was **4 and 5**. Each run's second micro-batch reads no rows: Spark adds it to move the watermark forward and write the windows that have just become final.

- **Batch 4** read 1,506 rows, the 1,500 on-time readings plus the six M-09 stragglers, using the watermark 00:09:50 set at the end of run 2. That's why the six were too late. The metric says **1** row dropped, not 6, because it counts *state rows*, not events. All six were M-09 readings from 00:02, so they fell in the same group: window 00:00–00:05, plant Bhiwandi Main (M-09 is one of Bhiwandi's machines M-01 to M-15). Spark had already combined them into one partial row before the watermark check, and that one row was dropped. After batch 4, state held 10 rows: 5 open windows × 2 plants.
- **Batch 5** read nothing, used the new watermark 00:19:50, and wrote the two windows it had passed, 00:05–00:10 and 00:10–00:15, for both plants. State shrank to 6 rows: the windows starting 00:15, 00:20, and 00:25, for both plants.

**How to choose a watermark.** Measure the gap between event time and arrival time for a week, and pick a value that covers the great majority of it (a high percentile), then decide what to do with the rest: drop them, route them to a "late" table for a daily correction (Chapter 46's backfill, section 46.5), or widen the watermark and accept the delay. Tell the people using the numbers which you chose.

---

## 50.6 Writing a stream into a table

Streaming sinks produce many small files, because each micro-batch writes its own. Chapter 49's problem, at speed. First count the files the three runs wrote, and the rows in each:

```python
import pyarrow.parquet as pq

out = "stream_out/windows"
files = sorted(f for f in os.listdir(out) if f.endswith(".parquet"))
rows = [pq.read_table(os.path.join(out, f)).num_rows for f in files]
print("parquet files written by the stream:", len(files))
print("rows in each file, smallest first:", sorted(rows))
```

```
parquet files written by the stream: 9
rows in each file, smallest first: [0, 0, 0, 0, 0, 1, 1, 2, 2]
```

- **`sorted(f for f in os.listdir(out) if f.endswith(".parquet"))`** lists the Parquet files in the sink's folder, leaving out Spark's bookkeeping files.
- **`pq.read_table(…).num_rows`** reads one file with PyArrow (Chapter 49) and counts its rows. The files' names are random, so **`sorted(rows)`** puts the counts in order, smallest first, to make them easy to read.

**Reading it.** Nine files for six rows, and five of the nine are **empty**: Spark writes a file for every micro-batch, including those with no final windows to write, such as run 1's.

Now load them into a Delta table the way a stream would, one append per file, and count the table's data files. The table's log (Chapter 49) knows every data file and its size, so ask it rather than the folder, which also works the same on Windows, on a Mac, and on object storage:

```python
import pyarrow as pa
from deltalake import DeltaTable, write_deltalake

shutil.rmtree("delta_windows", ignore_errors=True)
for f in files:
    write_deltalake("delta_windows", pq.read_table(os.path.join(out, f)), mode="append")

def data_files(path):
    added = pa.table(DeltaTable(path).get_add_actions(flatten=True))
    sizes = added.column("size_bytes").to_pylist()
    return f"data files {len(sizes)}, average {sum(sizes) / len(sizes) / 1e3:.1f} KB"

print("delta table now :", data_files("delta_windows"))
```

```
delta table now : data files 4, average 2.2 KB
```

- **`write_deltalake(…, mode="append")`** adds each file's rows to the table (Chapter 49); the first append creates it.
- **`data_files`** is a shorter version of Chapter 49's `file_report` (section 49.5): **`get_add_actions(flatten=True)`** returns one row per data file in the table's current version, read from its log, and **`pa.table(…)`** turns that into a PyArrow table whose **`size_bytes`** column holds each file's size.

**Reading it.** Nine appends made four data files: appending an empty table adds no data file. Now compact:

```python
DeltaTable("delta_windows").optimize.compact()
print("after compaction:", data_files("delta_windows"))
```

```
after compaction: data files 1, average 2.4 KB
```

**Reading it.** Compaction (Chapter 49) merged the four files into one. At real volumes this is a maintenance job that must run: a stream writing every 30 seconds makes at least 2,880 files a day per table partition, times the number of files each trigger writes (up to `spark.sql.shuffle.partitions`, 4 here). By the end of a month, reads are crawling.

That's the last Spark cell of the chapter, so stop Spark:

```python
spark.stop()
```

- **`spark.stop()`** shuts the Spark session down and frees the memory Java was holding. A later `getOrCreate()` would start a new session.

**The pattern that works in production:**

1. Stream into a table format (Delta, Iceberg, Hudi) rather than loose files, so readers get consistent snapshots while writes continue.
2. Use a trigger interval that balances latency against file count: 30 seconds to a few minutes is common.
3. Run **compaction** and **vacuum** on a schedule (Chapter 49), and monitor the file count.
4. Make the sink **idempotent** (upsert by key, or exactly-once via checkpoints plus a transactional sink), so a replayed batch doesn't double anything.
5. Apply Chapter 47's checks to the stream's output table, not only to batch tables.

---

## 50.7 Operating a stream

A batch job either ran or didn't. A stream is always running, so you monitor its health instead.

| Signal | What it tells you | Alert when |
|---|---|---|
| **Consumer lag** | How far behind the end of the log you are | Lag grows steadily rather than fluctuating |
| **Watermark age** | How far behind wall-clock time your event time is | It stalls, which means a source stopped sending |
| **Rows dropped as late** | Events arriving outside the watermark | Any sustained increase |
| **State size** | Memory held for open windows | It grows without bound: usually a missing watermark |
| **Batch duration versus trigger** | Whether processing keeps up | Duration approaches the trigger interval |
| **Failed restarts** | The job died and couldn't resume | Immediately: a stream that isn't running is silent |

Three habits save most incidents.

- **Replay is your recovery tool.** Retention on the log (often 7 days) means you can reset a group's offsets and re-process, provided your sink is idempotent.
- **A dead-letter path beats a crashing job.** Events that can't be parsed go to a side table with the error, rather than stopping the pipeline at 3 a.m.
- **Schema changes are the usual cause of outages.** A producer adds a field: fine. A producer renames one: your job breaks. This is Chapter 47's data contract, applied to events. Teams enforce it with a **schema registry**: a shared service that stores each topic's agreed schema and refuses events from a producer that breaks it.

---

## 50.8 Riverstone's plant monitoring case

Put the pieces together, as the plant team actually needs them.

**The need.** A machine drifting hot produces scrap continuously. The supervisor wants to know within minutes, not the next morning, and wants the day's totals to be correct even if a machine's network drops for a while.

**The design.**

- **Producer:** each machine's controller sends a reading every 10 seconds to a `sensor-readings` topic, keyed by machine id, so one machine's readings stay in order.
- **Alerting path (seconds):** a small consumer group reads the topic, holds the last few minutes per machine, and raises an alert when the average over 2 minutes exceeds the machine's limit. Alerts are de-duplicated by machine and window, and suppressed for 30 minutes after firing, so one drifting machine doesn't send twelve messages.
- **Aggregation path (minutes):** a Spark Structured Streaming job with 5-minute windows and a 10-minute watermark writes per-plant summaries into the Delta table from Chapter 49, as in section 50.5. For per-machine rows, add `machine_id` to the `groupBy`: the state grows 25 times larger, one row per machine instead of per plant.
- **Correction path (daily):** a batch job re-reads the day from the archive and rewrites yesterday's windows, so late and dropped events are corrected once a day. Streaming for speed, batch for truth. Chapter 62 names this design, a fast streaming path plus a batch path that corrects it, the **Lambda architecture**.
- **Quality:** Chapter 47's checks run on the daily corrected table, and a freshness check on the streaming table alerts if no window has been written for 15 minutes.

**What this costs.** A broker or a managed equivalent, a streaming job that must be watched, an on-call rota, and the batch pipeline that still exists. That's the honest price, and it's why the last part of this section is about whether to pay it.

**When Riverstone would not build this.** If the plant already has an alarm on the machine controller, the streaming alert adds nothing. If nobody is on the floor at night to act on it, the alert is decoration. If the scrap cost is small, a 10-minute batch job is the better answer. Chapter 58 covers the automation-and-AI version of this same decision.

---

## Common mistakes

| Mistake | Symptom | Fix |
|---|---|---|
| Building a stream because "real-time" was asked for | Complexity with no decision changed | Turn it into latency, consequence, and who acts (50.1) |
| Aggregating on processing time | Numbers change if the pipeline is slow | Aggregate on event time (50.5) |
| No watermark on a windowed job | State grows until the job dies | Set a watermark; monitor state size |
| A watermark chosen by default | Silent drops, or hours of delay | Measure the lateness distribution and choose (50.5) |
| Assuming exactly-once | Duplicate alerts and double counts | Assume at-least-once; de-duplicate (50.3) |
| Keeping the de-duplication record in memory | Duplicates come back after every real restart | Store sent keys on disk, in a table (50.3) |
| Auto-committing offsets | Events lost if the consumer dies after an auto-commit but before the work; duplicates if it dies after the work but before the next auto-commit (the story below) | Turn auto-commit off; commit after the work succeeds (50.3) |
| Ordering assumed across a topic | "Impossible" sequences in the data | Order holds within a partition; key by the entity |
| Schema inference on a stream | A new file changes the job's behaviour | Declare the schema; use a registry (50.4, 50.7) |
| Deleting or moving checkpoints | Everything re-processed, or state lost | Treat checkpoints as data (50.4) |
| Never compacting the sink | Reads slow down week by week | Scheduled compaction and vacuum (50.6) |
| No dead-letter path | One malformed event stops the pipeline | Route bad events aside with their error |
| Monitoring only "is it running?" | Silent lag and stalled watermarks | Lag, watermark age, state size, drops (50.7) |
| No batch correction path | Dropped late events are wrong forever | Reprocess the day in batch (50.8) |

---

## In the real world: the alert that cried wolf

Riverstone's first streaming alert went live on a Tuesday, watching machine temperatures against a fixed limit of 205 °C.

By Thursday, the plant supervisors had muted the channel. In two days it had sent 1,900 messages. Three things were wrong, and each is in this chapter.

**It alerted on single readings.** A reading every 10 seconds means a machine hovering near the limit trips the alert dozens of times an hour, and a single noisy reading fires it too. The fix was a 2-minute window: alert on the average, not the instant.

**It re-sent everything after every restart.** The consumer committed offsets automatically every few seconds, but the deployment restarted the job several times, and each restart re-read from a slightly older offset and re-sent alerts that had already gone. The fix was a de-duplication key of machine plus window, kept for an hour, and committing only after alerts were delivered.

**It treated all machines alike.** The extrusion lines run hotter by design, so their normal operation looked like an emergency. The fix was a per-machine limit read from a small table, with the plant team owning the values.

After the changes, the same two days would have produced 11 alerts, all of them real, and one of them caught a heater that was failing gradually.

The plant manager's verdict, at the review, was the sentence Meera kept: "The system was right every time and useful none of the time."

**What made this work.**

- **They counted the alerts** instead of arguing about whether it was noisy.
- **Every fix was about the design, not the threshold:** windows instead of readings, de-duplication instead of hope, per-machine limits instead of one number.
- **The owners of the limits were the people who understood the machines.**

---

## Project: minute-level machine monitoring

**Goal:** build the plant monitoring design from section 50.8 end to end, on the practice data, and decide whether it's worth running.

### Tools you'll need

- **Python 3.14** in the book's virtual environment, with `pyspark`, `deltalake`, `duckdb`, and `pyarrow`, and **Java 21**.
- **The Chapter 50 companion folder** (`companion/ch50/`): `mini_log.py` (the local message log) and `sensor_events.py` (replays the Chapter 48 archive as events). Generate the Chapter 48 dataset first.
- **Versions used for the outputs shown:** Python 3.11.15, PySpark 4.2.0, deltalake 1.6.6, DuckDB 1.5.6, PyArrow 25.0.1, OpenJDK 21.0.10, Apache Kafka 4.3.1, kafka-python 3.0.11.
- **For real Kafka:** the single broker from section 50.3, with `kafka-python` (or `confluent-kafka`) as the client; managed services include Amazon MSK, Confluent Cloud, Azure Event Hubs, and Google Pub/Sub. Spark connects with `format("kafka")`.
- **Other engines worth knowing:** Apache Flink (the strongest event-time engine), Kafka Streams, and cloud streaming services.

**Option A: Riverstone.** Use the companion scripts.

**Option B: your own events.** Any event-like data you have permission to use: web logs, IoT readings, transactions.

**Steps**

1. **Produce a stream:** replay one day of readings into the message log, keyed by machine, in batches of a few minutes.
2. **Write a consumer** that keeps a 2-minute average per machine and raises alerts above a per-machine limit held in a small table.
3. **Make it survive a crash:** stop the consumer mid-batch, restart it, and show that no alert is sent twice. Say which guarantee you implemented, and where the record of sent alerts lives.
4. **Build the aggregation job** in Structured Streaming: 5-minute windows, a watermark you justify, written to a Delta table.
5. **Demonstrate late data** twice: once accepted within the watermark, once dropped outside it. Record both counts.
6. **Add the correction path:** a batch job that rewrites yesterday's windows from the archive, and a check that compares streaming totals with corrected totals.
7. **Compact the sink** and record the file count before and after.
8. **Write the monitoring plan:** which signals, what thresholds, who is alerted, and what the runbook says.
9. **Write the decision memo,** one page: the latency the business needs, what it costs to run, and your recommendation, including the batch-only alternative.

**Stretch goals**

- Add a session window per machine (activity separated by gaps of more than 15 minutes) and describe what it tells the plant team.
- Replay the same day with a 1-minute watermark and compare dropped counts.
- Run the producer and the alerting consumer against the real broker from section 50.3, changing only the client code.

---

## Recap

- **Streaming is for decisions whose value decays in minutes.** Most "real-time" requests are answered better by a shorter batch schedule.
- An event log is **append-only**, split into **partitions**; a **key** decides the partition, so order holds within a key, not across a topic.
- **Consumer groups** track their own **offsets**; a committed offset is the next position to read, and **lag** is the first metric to watch.
- Delivery is **at-least-once** in practice: expect duplicates and de-duplicate by a key kept on disk. Here a crash re-sent all 82 alerts until a stored key stopped them.
- **Event time** is what you aggregate on; **processing time** is when you happened to see it.
- **Tumbling** windows count each event once, **sliding** windows overlap, and **session** windows end after a quiet gap.
- **Windows** need a **watermark**: it sets how long you wait for stragglers and bounds state. Six late readings were counted inside a 10-minute watermark (456 readings instead of 450), and six more were dropped once the watermark had moved on.
- **Append mode emits only final windows**, which is why the first run produced nothing.
- Streaming sinks make **small files**: stream into a table format and compact on a schedule.
- Operate a stream by watching **lag, watermark age, dropped rows, state size, batch duration, and restarts**, with a **dead-letter path** and a **schema contract**.
- Pair streaming with a **daily batch correction**: speed from the stream, truth from the batch.

---

## Key terms

batch · streaming · latency · micro-batch · event log · topic · partition · key · offset · committed offset · consumer group · lag · retention · replay · producer · consumer · broker · replica · at-most-once · at-least-once · exactly-once · sink · de-duplication key · business key · idempotency key · Kafka · schema registry · Structured Streaming · unbounded table · schema · trigger · checkpoint · event time · processing time · window (tumbling, sliding, session) · watermark · lateness · output mode (append, update, complete) · state · no-data batch · dead-letter path · small files · compaction · dashboard refresh

*(All terms are defined in the Glossary, Appendix A.)*

---

## Check yourself

- [ ] You can turn "real-time" into a latency, a decision, and an owner.
- [ ] You can explain topics, partitions, keys, offsets, consumer groups, lag, and retention.
- [ ] You can say exactly what order guarantees a log gives, and what it doesn't.
- [ ] You can explain at-most-once, at-least-once, and exactly-once, and say which you'd get by default.
- [ ] You can show a duplicate happening and fix it with a de-duplication key that survives a restart.
- [ ] You can read Kafka producer and consumer code and name the settings that matter.
- [ ] You can count events in tumbling, sliding, and session windows by hand.
- [ ] You can write a Structured Streaming job with a declared schema and a checkpoint.
- [ ] You can explain event time versus processing time and why aggregations use event time.
- [ ] You can trace a watermark run by run, and say what happens to data outside it.
- [ ] You can explain why an append-mode window produced no output in the first run.
- [ ] You can keep a streaming sink healthy with compaction and idempotent writes.
- [ ] You can list the signals to monitor on a running stream.
- [ ] You can argue both sides of "should this be streaming?" for a real case.

---

## Exercises

### Warm-up

1. For each, say whether you'd build streaming, a frequent batch job, or nothing: (a) a dashboard the sales head opens each morning; (b) blocking a fraudulent payment; (c) telling a supervisor a machine is running hot; (d) a weekly scrap report; (e) showing a customer where their delivery is.
2. A topic has 4 partitions and events are keyed by machine id. Which of these are guaranteed: (a) all events for M-07 are read in order; (b) all events across all machines are read in order; (c) two consumers in one group can each read a different partition; (d) two different groups can read the same partition independently?
3. Explain at-most-once and at-least-once in terms of *when the offset is committed*, and say which one produces duplicates.

### Core

4. In section 50.2, the 300 events split 144 and 156 across two partitions. Explain why the split isn't exactly even, and what would happen to ordering if the producer used a random key instead of the machine id.
5. Section 50.3 sent the same 82 alerts twice. Write the de-duplication rule you'd use in production, say where you'd store it, and how long you'd keep it.
6. The first windowed run emitted nothing. Explain why, in terms of the watermark and append mode, and say what output mode you'd use for a live dashboard that's allowed to show "so far" numbers.
7. Six readings with event time 00:02 arrived in run 2 and were counted; six more from 00:02 arrived in run 3 and were dropped. Give the watermark in force during each run and show the arithmetic that decides each outcome.
8. Section 50.5's progress output says 1 row was dropped as too late, although 6 events were late. Explain the difference between events and state rows here.
9. A streaming job writes every 30 seconds into a table partitioned by day. How many files a day does that produce, and what two things would you schedule to keep reads fast? (Chapter 49.)

### Stretch

10. Design the alerting consumer from section 50.8: window length, per-machine limits, de-duplication, suppression after firing, what the alert message says, and what happens when the consumer falls behind by an hour.
11. Riverstone's plant network drops for 25 minutes and then delivers all the missing readings at once. Trace what happens with a 10-minute watermark: which windows are correct, which are wrong, what the monitoring shows, and how the daily correction fixes it.
12. Compare Kafka with the file source used in this chapter for Riverstone's case, on: latency, replay, ordering, operational cost, and what would have to change in the Spark job. Then say what you'd recommend for a company Riverstone's size.

### Think about it (no code needed)

13. The plant manager said the alerting system was "right every time and useful none of the time". Explain what that means for how you'd measure an alerting system's success, and what you'd report monthly.
14. Streaming makes numbers arrive sooner but also makes them provisional, since late data can change them. How would you explain that to a sales head who sees a revenue figure change between 9 a.m. and 10 a.m., and what design choices would you offer?

---

## Answers

**1.** (a) **Nothing**, or a nightly batch: it's read once a day. (b) **Neither**: blocking a payment happens in the application's own request path, in milliseconds; a data pipeline is too slow, though it can score risk in advance. (c) **Streaming**, or a frequent batch if minutes are acceptable and the scrap cost is low. (d) **Batch**, weekly. (e) **Streaming** (or frequent updates from the courier's feed), because the customer is watching it change.

**2.** Guaranteed: **(a)**, because one key always maps to one partition and a partition is read in order; **(c)**, partitions are the unit of parallelism within a group; **(d)**, groups track offsets independently. **Not guaranteed: (b)** — there's no global order across partitions, only within each one.

**3.** **At-most-once** commits the offset *before* doing the work, so a crash in between loses the event: no duplicates, possible loss. **At-least-once** commits *after* the work succeeds, so a crash in between re-reads the event: no loss, **duplicates possible**. At-least-once is the default in practice, which is why de-duplication belongs in the design.

**4.** The partition is chosen by a hash of the key, and a hash spreads 25 machine ids unevenly across 2 partitions: 12 machines hashed to partition 0 and 13 to partition 1. Each machine sent exactly 12 readings (2 minutes × 6), so the partitions hold 12 × 12 = 144 and 13 × 12 = 156. With a **random key**, events for one machine would scatter across partitions, and their relative order would be lost: a later reading could be processed before an earlier one, which breaks any per-machine logic such as "temperature rising for 2 minutes".

**5.** A business key: **machine id + window start** (or machine id + event time for single-event alerts, as in section 50.3). Store it where the consumer can check it after a restart: a small table, as in section 50.3, or a key-value store with expiry, keyed as `alert:M-07:2025-12-01T00:05`. Keep it at least as long as the maximum replay you'd ever do, plus your suppression window; an hour is fine for alerts fired per 5-minute window, a day is safer if you re-process the stream. The same key doubles as the suppression record.

**6.** In **append** mode a windowed result is emitted only when it can no longer change, which means when the **watermark** has passed the window's end. After run 1 the newest event time was 00:09:50, so the watermark (10 minutes behind) was 23:59:50 of the previous day: no window's end had been passed, so nothing was final and nothing was written. For a live dashboard that may show partial numbers, use **update** mode, which emits windows whose values changed in this micro-batch, and mark the latest window as provisional in the interface.

**7.** After run 1, the newest event time was 00:09:50, so the watermark in force during run 2 was **23:59:50** (00:09:50 minus 10 minutes). The late M-07 readings had event time 00:02, which is later than 23:59:50, so they were accepted and folded into the 00:00–00:05 window, which had not yet been emitted: 450 on time plus 6 late equals **456**. After run 2, the newest event time was 00:19:50, so the watermark in force during run 3 was **00:09:50**. The M-09 readings in run 3 again had event time 00:02, which is **earlier** than 00:09:50, so they were dropped, and the window stayed at 456.

**8.** The metric counts rows removed from the **aggregation's state**, not raw input events. The query groups by window and plant, and all six late readings were M-09's from 00:02: the same window (00:00–00:05) and the same plant (Bhiwandi Main). Spark had combined them into a single partial row before the watermark check applied, and that one row was dropped. Six events, one row. It matters when reading the metric: a spike of 1 can represent thousands of events, so pair it with input counts.

**9.** Every 30 seconds is 2 per minute, 120 per hour, **2,880 files a day** per partition, and more if each micro-batch writes several files (up to `spark.sql.shuffle.partitions`). Schedule (1) **compaction** (OPTIMIZE) to merge them into files of 128–512 MB, and (2) **vacuum** to remove the files compaction replaced, with a retention that still allows your rollback window. Increasing the trigger interval is a third, cheaper lever.

**10.** A defensible design: **2-minute tumbling windows per machine** (long enough to smooth noise, short enough to act); **per-machine limits** in a small table owned by the plant team, with a default for new machines; alert when the window's average exceeds the machine's limit **and** the previous window also did, so a single spike doesn't fire; **de-duplication** by machine plus window start, stored on disk for an hour; **suppression** of 30 minutes per machine after an alert, with a reminder if still hot at the end of it; the message says machine, line, plant, the window's average and limit, how long it has been high, and a link to the dashboard and runbook. If the consumer **falls behind by an hour**, the right behaviour is to skip to the latest offsets for *alerting* (an hour-old alert is worse than useless) while recording the gap, and to let the aggregation path process the backlog normally. That decision should be written down, because it's a trade-off, not an obvious truth.

**11.** With a 10-minute watermark: readings arriving 25 minutes late are **outside** it. Other machines keep sending, so the watermark keeps moving and the windows covering the outage are written with the readings that did arrive: for the affected machines they either have no row at all or a partial count. When the missing readings land, they're **dropped**, so those windows are permanently wrong in the streaming table: they under-report output and scrap. Monitoring shows it: during the outage, the **freshness** check on those machines' readings fires, and if the whole plant's network is down the **watermark stalls**; when the backlog lands, **lag** spikes briefly and **rows dropped as too late** jumps. The **daily correction** fixes it: the batch job re-reads the full archive for the day, recomputes every window, and rewrites them with an atomic partition overwrite (Chapters 46 and 49), so by the next morning the table is right. If the plant team needs the intraday numbers to survive outages, widen the watermark (more delay, more state) or route dropped events to a late table processed hourly.

**12.** **Latency:** Kafka delivers in milliseconds; a file source depends on how often files are written, so seconds to minutes. **Replay:** Kafka replays from retained offsets without the producer's involvement; files replay only if you kept them. **Ordering:** Kafka guarantees order within a partition, and keys give you per-machine order; a folder of files has no ordering guarantee beyond what's inside each file. **Operational cost:** Kafka means a cluster (or a managed service), monitoring, and upgrades; files mean object storage. **Changes to the Spark job:** the source (`format("kafka")` with brokers, topic, and starting offsets), parsing the value from bytes, and offsets living in Kafka rather than in the file source's checkpoint tracking; the windowing, watermark, and sink code are unchanged. **Recommendation for Riverstone:** start with the file or micro-batch route and a managed service only if second-level latency is genuinely needed; a company of this size gets most of the value from 1–5 minute latency, and avoids running a broker. Revisit when there are several consumers of the same events, which is where a log starts to pay for itself.

**13.** It means correctness isn't the measure; **action** is. Measure an alerting system by: how many alerts fired, how many led to someone doing something (the useful ones), how many were ignored or muted, how long from the underlying event to the alert, and how many real events were **missed**. Report monthly: alerts per machine per week, the share acted on, median time to acknowledge, false-positive causes grouped, and any incident the system missed. A rising alert count with a falling action rate is the signal to change the design, exactly as in the story.

**14.** Explain it in their terms: *"The 9 a.m. figure is what we know so far; some orders reach the system a few minutes late, so the number can still move. By 10 a.m. it's settled, and the end-of-day figure is final and reconciled with the ERP."* Then offer design choices: (1) label the live figure as provisional, with a "final at" time, which costs nothing; (2) delay the live figure by the watermark so it never changes, at the cost of being older; (3) show both a live and a confirmed number side by side; (4) keep the live number for direction only and put decisions on the daily corrected table. The choice depends on whether they act on the intraday number or only watch it.

---

## Where this leads

- **Chapter 51, Data Activation,** sends results into business systems, where at-least-once delivery becomes idempotency keys against a CRM or ERP.
- **Chapter 52, The Cloud, Containers & Infrastructure as Code,** covers running a stream somewhere it can stay up: containers, restarts, secrets, and cost.
- **Chapter 47** applies to streams: freshness on the sink, quality checks on the corrected table, and alerting that doesn't cry wolf.
- **Chapter 49** is where the sink lives: table formats, compaction, and time travel.
- **Chapter 58, Intelligent Automation,** revisits the alerting decision with AI in the loop, and this chapter's rule stands: the design matters more than the model.
- **Chapter 61, Distributed Systems & Trade-offs,** explains what ordering and delivery guarantees cost when the log runs across many machines.
- **Chapter 62, Data Architecture Patterns,** names section 50.8's design, a fast streaming path plus a batch path that corrects it, as the Lambda architecture, and compares it with Kappa, which treats everything as a stream.
- **Part 8:** streaming questions appear in the data engineering interview chapters, and "design a real-time alerting system" is a common case in Chapter 77.
