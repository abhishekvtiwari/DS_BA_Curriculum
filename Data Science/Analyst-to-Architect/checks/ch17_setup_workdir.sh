#!/usr/bin/env bash
# Builds the reader's folder that Chapter 17's terminal sessions and notebook cells run in:
#   /home/meera/analyst-to-architect/{companion/ch17, work/ch17, notes}
# work/ch17 is the reader's copy of companion/ch17 (section 17.0, step 1). The maintainer script
# build_ch17_files.py is left out, as it is not a reader file.
# Usage (from the book folder):  bash checks/ch17_setup_workdir.sh [path/to/python3.14]
# Needs Python 3.14 for the environment (uv: `uv python install 3.14`) and network access for pip.
set -euo pipefail
BOOK="$(cd "$(dirname "$0")/.." && pwd)"
PY314="${1:-$(ls /root/.local/share/uv/python/cpython-3.14*/bin/python3 2>/dev/null | head -1)}"
ROOT=/home/meera/analyst-to-architect
if [ -e "$ROOT" ]; then mv "$ROOT" "/tmp/ch17-workdir-old.$(date +%s)"; echo "moved the previous copy aside"; fi
mkdir -p "$ROOT/companion" "$ROOT/work" "$ROOT/notes"
for dest in "$ROOT/companion/ch17" "$ROOT/work/ch17"; do
  mkdir -p "$dest"
  (cd "$BOOK/companion/ch17" && cp -r check_setup.py products.json targets_2025.csv broken_export.csv sales_exports "$dest/")
done
cp "$BOOK/companion/ch17/summarize_exports.py" "$ROOT/companion/ch17/"
# Files the reader writes in work/ch17 by section 17.12 (checks/ch17_check.py confirms they match the chapter):
cp "$BOOK/companion/ch17/summarize_exports.py" "$ROOT/work/ch17/"
printf 'import sys\nprint(sys.argv)\n' > "$ROOT/work/ch17/show_args.py"
# The book's environment, as section 17.0 builds it (so later sessions find JupyterLab installed)
"$PY314" -m venv "$ROOT/.venv"
"$ROOT/.venv/bin/python" -m pip install -q jupyterlab
echo "ready: $ROOT (python $("$ROOT/.venv/bin/python" --version))"
