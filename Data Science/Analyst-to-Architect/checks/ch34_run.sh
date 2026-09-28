#!/usr/bin/env bash
# ch34_run.sh - runs every terminal session in Chapter 34 for real, as the user meera, in a throwaway folder.
#
# Usage (as root, from anywhere):  checks/ch34_run.sh SCRATCH_DIR [--fill]
#
# What it builds in SCRATCH_DIR (deleted and rebuilt on every run):
#   home/     mounted over /home/meera in a private mount namespace (unshare), so the chapter's paths
#             (/home/meera/ch34/practice) are real while every file lives in SCRATCH_DIR. It holds
#             analyst-to-architect/companion/ch34, a COPY of the book's companion folder (no generated
#             practice/ folder), which the chapter's first commands copy to ~/ch34 and build.
#   run/      the verifier, ch34_check.py and a copy of the chapter, mounted at /srv for meera to read.
#   etc/      a copy of /etc/passwd and /etc/group with a user meera (uid 1500) added, mounted over the real
#             ones inside the namespace only, so `ls -l` shows meera as the owner. Nothing outside changes.
# Then it runs checks/ch34_shell_session.py on the chapter as meera (setpriv), with /home/meera as the
# working folder, and finally checks/ch34_check.py on the practice folder the session built.
# Blocks marked <!-- run: none --> (the WSL install, the SSH server, a remote server) are not run.
set -euo pipefail
BOOK=$(cd "$(dirname "$0")/.." && pwd)
SCR=$(mkdir -p "${1:?usage: ch34_run.sh SCRATCH_DIR [--fill]}" && cd "$1" && pwd); shift
CH="$BOOK/manuscript/ch34-the-command-line-linux-and-networking-basics.md"

rm -rf "${SCR:?}/home" "${SCR:?}/etc" "${SCR:?}/run"
mkdir -p "$SCR/home/analyst-to-architect/companion" "$SCR/etc" "$SCR/run"
rsync -a --exclude practice --exclude __pycache__ "$BOOK/companion/ch34/" "$SCR/home/analyst-to-architect/companion/ch34/"
cp /etc/passwd /etc/group "$SCR/etc/"
echo 'meera:x:1500:1500:Meera Iyer:/home/meera:/bin/bash' >> "$SCR/etc/passwd"
echo 'meera:x:1500:' >> "$SCR/etc/group"
chown -R 1500:1500 "$SCR/home"
cp "$BOOK/checks/ch34_shell_session.py" "$BOOK/checks/ch34_check.py" "$SCR/run/"
cp "$CH" "$SCR/run/ch34.md"; chown -R 1500:1500 "$SCR/run"

status=0
unshare --mount --propagation private bash -c '
  set -e
  mount --bind "$0/home" /home/meera
  mount --bind "$0/etc/passwd" /etc/passwd
  mount --bind "$0/etc/group" /etc/group
  mount --bind "$0/run" /srv      # the verifier and a copy of the chapter, readable by meera
  mount -t tmpfs tmpfs /tmp       # an empty /tmp for every run (the chapter writes files there)
  status=0
  umask 002    # the default on Ubuntu for a normal user, who has a group of their own
  env -i HOME=/home/meera USER=meera LOGNAME=meera TZ=Asia/Kolkata SHELL=/bin/bash \
    PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin \
    setpriv --reuid 1500 --regid 1500 --clear-groups \
    python3 /srv/ch34_shell_session.py /srv/ch34.md --cwd /home/meera "${@:2}" || status=$?
  python3 /srv/ch34_check.py /home/meera/ch34 || status=1
  exit $status' "$SCR" "$BOOK" "$@" || status=$?
if [[ " $* " == *" --fill "* ]]; then cp "$SCR/run/ch34.md" "$CH"; fi
exit $status
