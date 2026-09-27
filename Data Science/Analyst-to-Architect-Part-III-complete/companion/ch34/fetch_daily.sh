#!/usr/bin/env bash
# Analyst to Architect · Chapter 34 · the project: download one day's export, check it, archive it.
# Usage: ./fetch_daily.sh 2025-12-16 [base_url]
# Exit codes: 0 done, 1 bad arguments, 2 file not published yet, 3 checksum mismatch.
# Tested on: bash 5.2.21, curl 8.5, Ubuntu 24.04.
set -euo pipefail

DAY="${1:-}"
BASE_URL="${2:-http://127.0.0.1:8034}"
INCOMING="incoming"
ARCHIVE="archive"
LOG="logs/fetch_daily.log"

log() { printf '%s %s %s\n' "$(date '+%Y-%m-%d %H:%M:%S')" "$1" "$2" | tee -a "$LOG"; }

if [[ ! "$DAY" =~ ^[0-9]{4}-[0-9]{2}-[0-9]{2}$ ]]; then
    echo "usage: $0 YYYY-MM-DD [base_url]" >&2
    exit 1
fi

mkdir -p "$INCOMING" "$ARCHIVE" "$(dirname "$LOG")"
NAME="orders_${DAY}.csv"
log INFO "downloading $NAME from $BASE_URL"

if ! curl --silent --show-error --fail --max-time 30 \
        --output "$INCOMING/$NAME" "$BASE_URL/exports/$NAME"; then
    log ERROR "could not download $NAME (not published yet, or the server is unreachable)"
    rm -f "$INCOMING/$NAME"
    exit 2
fi

curl --silent --show-error --fail --max-time 30 \
     --output "$INCOMING/$NAME.sha256" "$BASE_URL/exports/$NAME.sha256"

if ! (cd "$INCOMING" && sha256sum --check --status "$NAME.sha256"); then
    log ERROR "checksum mismatch for $NAME; leaving it in $INCOMING for inspection"
    exit 3
fi

ROWS=$(( $(wc -l < "$INCOMING/$NAME") - 1 ))
REVENUE=$(awk -F, 'NR > 1 { total += $11 } END { printf "%.2f", total + 0 }' "$INCOMING/$NAME")
log INFO "$NAME passed its checksum: $ROWS order lines, revenue $REVENUE"

gzip --force "$INCOMING/$NAME"
mv "$INCOMING/$NAME.gz" "$ARCHIVE/"
rm -f "$INCOMING/$NAME.sha256"
log INFO "archived $ARCHIVE/$NAME.gz"
