#!/usr/bin/env bash
# ch26_run.sh - runs every terminal session in Chapter 26 for real, in a throwaway scratch folder.
#
# Usage (as root, from anywhere):  checks/ch26_run.sh SCRATCH_DIR [--fill]
#
# What it builds in SCRATCH_DIR (deleted and rebuilt on every run):
#   home/     mounted over /home/meera in a private mount namespace (unshare), so the chapter's paths
#             (/home/meera/riverstone-analysis) are real while every file, including the Git repository,
#             lives in SCRATCH_DIR. It holds analyst-to-architect/companion/ch26, a COPY of the book's
#             companion folder (never a link into the book, so no Git command can reach the book's own
#             repository); GIT_CEILING_DIRECTORIES stops Git from looking above /home/meera.
#   bin/git   a wrapper that gives every Git command a timestamp one minute after the previous one
#             (from Mon 2 Mar 2026 10:00 IST), so commit hashes are the same on every run
#   remote/   a bare repository standing in for https://github.com/meera/riverstone-analysis.git; exec/
#             holds a git-remote-https helper that serves that URL from remote/ (Git's own remote-ext),
#             so push and pull print exactly what Git prints for a GitHub remote
#   bin/github-*  what happens on github.com in section 26.7 (merging a pull request, a colleague's push),
#             called from the chapter's hidden session blocks
#   bin/code  stands in for VS Code's `code` command, which opens a file in the editor and prints nothing
# Then it runs checks/ch26_shell_session.py on the chapter with /home/meera as the working folder.
set -euo pipefail
BOOK=$(cd "$(dirname "$0")/.." && pwd)
SCR=$(mkdir -p "${1:?usage: ch26_run.sh SCRATCH_DIR [--fill]}" && cd "$1" && pwd); shift
CH="$BOOK/manuscript/ch26-the-professional-toolkit-git-agile-documentation-and-ai-assistants.md"

rm -rf "${SCR:?}/home" "${SCR:?}/bin" "${SCR:?}/exec" "${SCR:?}/remote" "${SCR:?}/clock" "${SCR:?}/sysconfig"
mkdir -p "$SCR/home/analyst-to-architect/companion" "$SCR/bin" "$SCR/exec" "$SCR/remote/meera"
cp -r "$BOOK/companion/ch26" "$SCR/home/analyst-to-architect/companion/ch26"
printf '#!/bin/sh\n# VS Code: opens the file in the editor; prints nothing\nexit 0\n' > "$SCR/bin/code"

cat > "$SCR/bin/git" <<EOF
#!/bin/sh
n=\$(cat "$SCR/clock" 2>/dev/null || echo 0); n=\$((n + 1)); echo "\$n" > "$SCR/clock"
t=\$((1772425800 + n * 60))
export GIT_COMMITTER_DATE="@\$t +0530"
case " \$* " in *" --amend "*) ;; *) export GIT_AUTHOR_DATE="@\$t +0530" ;; esac
exec /usr/bin/git "\$@"
EOF

for f in /usr/lib/git-core/*; do ln -s "$f" "$SCR/exec/"; done
rm "$SCR/exec/git-remote-https"
cat > "$SCR/exec/git-remote-https" <<EOF
#!/bin/sh
# stand-in for GitHub: serve https://github.com/OWNER/REPO from SCRATCH_DIR/remote/OWNER/REPO
p=\$(printf '%s' "\$2" | sed 's#^https://github.com/##; s#/\$##')
case "\$p" in *.git) ;; *) p="\$p.git" ;; esac
exec /usr/bin/git remote-ext "\$1" "%S $SCR/remote/\$p"
EOF
printf '[protocol "ext"]\n\tallow = always\n' > "$SCR/sysconfig"
/usr/bin/git init -q --bare -b main "$SCR/remote/meera/riverstone-analysis.git"

# github-merge-pr NUMBER BRANCH TITLE: what "Merge pull request" does on github.com
cat > "$SCR/bin/github-merge-pr" <<EOF
#!/bin/sh
set -e
w=\$(mktemp -d); git clone -q "$SCR/remote/meera/riverstone-analysis.git" "\$w/r"; cd "\$w/r"
GIT_AUTHOR_NAME="Meera Iyer" GIT_AUTHOR_EMAIL="meera@riverstone.example" \
GIT_COMMITTER_NAME="GitHub" GIT_COMMITTER_EMAIL="noreply@github.com" \
git merge -q --no-ff "origin/\$2" -m "Merge pull request #\$1 from meera/\$2" -m "\$3"
git push -q origin main; rm -rf "\$w"
EOF
# github-colleague-readme: Farah adds a README on github.com while Meera works
cat > "$SCR/bin/github-colleague-readme" <<EOF
#!/bin/sh
set -e
w=\$(mktemp -d); git clone -q "$SCR/remote/meera/riverstone-analysis.git" "\$w/r"; cd "\$w/r"
printf '# Riverstone analysis\n\nMonthly revenue queries for the sales team.\n' > README.md
git add README.md
GIT_AUTHOR_NAME="Farah Khan" GIT_AUTHOR_EMAIL="farah@riverstone.example" \
GIT_COMMITTER_NAME="Farah Khan" GIT_COMMITTER_EMAIL="farah@riverstone.example" \
git commit -q -m "Add a README"
git push -q origin main; rm -rf "\$w"
EOF
chmod +x "$SCR/bin/"* "$SCR/exec/git-remote-https"

export HOME=/home/meera PATH="$SCR/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin" GIT_EXEC_PATH="$SCR/exec" GIT_CONFIG_SYSTEM="$SCR/sysconfig"
unset GIT_CONFIG_GLOBAL GIT_DIR GIT_WORK_TREE
export GIT_CEILING_DIRECTORIES=/home/meera GIT_EDITOR=true GIT_MERGE_AUTOEDIT=no TZ=Asia/Kolkata
unshare --mount --propagation private bash -c '
  mount --bind "$0/home" /home/meera
  python3 "$1/checks/ch26_shell_session.py" "$2" --cwd /home/meera "${@:3}"
  exit $?' "$SCR" "$BOOK" "$CH" "$@" || status=$?
# Outside the namespace: the repository the session built is in the scratch folder, not in the book.
echo "repository: $(cd "$SCR/home/riverstone-analysis" 2>/dev/null && /usr/bin/git rev-parse --show-toplevel)"
exit ${status:-0}
