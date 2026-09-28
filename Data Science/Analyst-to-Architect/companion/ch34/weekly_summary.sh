#!/usr/bin/env bash
# weekly_summary.sh 2025-12-15
set -euo pipefail

MONDAY="${1:?usage: $0 YYYY-MM-DD (a Monday)}"
TOTAL=0

for offset in 0 1 2 3 4 5 6; do
    DAY=$(date -d "$MONDAY + $offset days" +%F)      # macOS: date -j -v+"$offset"d -f %Y-%m-%d "$MONDAY" +%F
    LINE=$(./daily_summary.sh "$DAY")
    echo "$LINE"
    REVENUE=${LINE##*revenue }
    TOTAL=$(awk -v a="$TOTAL" -v b="$REVENUE" 'BEGIN { printf "%.2f", a + b }')
done

echo "week of $MONDAY: revenue $TOTAL"
