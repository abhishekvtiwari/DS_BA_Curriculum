#!/usr/bin/env bash
# Analyst to Architect - Chapter 50: re-run every printed output, including the optional Kafka broker.
# Run from the book root:  bash checks/ch50_verify_all.sh <empty scratch folder>
# Needs: the Chapter 48 sensor data (companion/ch48/sensor_readings), Java 17+, internet access to
# downloads.apache.org, and kafka-python==3.0.11 in the python3 that runs the verifier.
# Section 50.3's terminal block downloads Kafka 4.3.1 into the scratch folder, formats
# /tmp/kraft-combined-logs, starts a broker on localhost:9092, and creates the topic; the Python
# verifier then runs every cell, the Kafka producer and consumer included, against that broker.
# Riverstone Supplies is fictional; every name and number is invented.
set -u
SCRATCH="${1:?give an empty scratch folder}"
mkdir -p "$SCRATCH"
if [ -n "$(ls -A "$SCRATCH")" ]; then echo "scratch folder is not empty: $SCRATCH"; exit 2; fi
if [ -e /tmp/kraft-combined-logs ]; then echo "/tmp/kraft-combined-logs exists: stop that broker and remove it first"; exit 2; fi
export OMP_NUM_THREADS=1
status=0
env -u JAVA_TOOL_OPTIONS python3 tools/verify_shell.py manuscript/ch50-streaming-and-real-time.md --cwd "$SCRATCH" || status=1
python3 tools/verify_python.py manuscript/ch50-streaming-and-real-time.md --cwd companion/ch50 || status=1
python3 checks/ch50_check.py || status=1
( cd "$SCRATCH/kafka_2.13-4.3.1" && env -u JAVA_TOOL_OPTIONS bin/kafka-server-stop.sh )
sleep 10
rm -rf /tmp/kraft-combined-logs
( cd companion/ch50 && rm -rf stream_log events_in stream_out checkpoints delta_windows alerts_sent.duckdb spark-warehouse )
exit $status
