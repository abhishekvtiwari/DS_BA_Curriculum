#!/usr/bin/env bash
# Analyst to Architect · Chapter 34 · summarize one day's export.
# Usage: ./daily_summary.sh 2025-12-16      Exit codes: 0 done, 2 no export for that day.
set -euo pipefail

DAY="${1:?usage: $0 YYYY-MM-DD}"
FILE="exports/orders_${DAY}.csv"

if [[ ! -f "$FILE" ]]; then
    echo "no export for $DAY" >&2
    exit 2
fi

ORDER_LINES=$(( $(wc -l < "$FILE") - 1 ))
REVENUE=$(awk -F, 'FNR > 1 { total += $11 } END { printf "%.2f", total + 0 }' "$FILE")
CUSTOMERS=$(awk -F, 'FNR > 1 { seen[$4] = 1 } END { print length(seen) }' "$FILE")

echo "$DAY: order lines $ORDER_LINES, customers $CUSTOMERS, revenue $REVENUE"
