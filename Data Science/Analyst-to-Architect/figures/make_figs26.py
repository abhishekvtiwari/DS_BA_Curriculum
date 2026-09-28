# Generates the SVG figures for Chapter 26. Run: python3 make_figs26.py
# Every figure prints at the full text width (493.2 pt). The canvases are 700 px wide, so a font of s px prints
# at s x 0.705 pt: the smallest text here, 10.5 px, prints at 7.4 pt (visual standard: 7 pt or more).
from make_figs import *
from make_figs01 import wrap

GREEN = "#2f7d6d"; PURPLE = "#7a4fa0"; ORANGE = "#c0662b"; RED = "#b23b3b"; TEAL = "#1f6fa3"; GREY = "#5b6475"
W = 700


def wraplines(s, n):
    words = s.split(); lines = []; cur = ""
    for w in words:
        if len(cur + " " + w) > n:
            lines.append(cur); cur = w
        else:
            cur = (cur + " " + w).strip()
    lines.append(cur)
    return lines


def arrow_right(x, y, length, colour=MUTED, sw=2):
    return (path(f"M{x},{y} H{x+length-6}", stroke=colour, sw=sw)
            + f'<path d="M{x+length-7},{y-5} L{x+length+1},{y} L{x+length-7},{y+5} Z" fill="{colour}"/>')


def arrow_left(x, y, length, colour=MUTED, sw=2):
    return (path(f"M{x+length},{y} H{x+6}", stroke=colour, sw=sw)
            + f'<path d="M{x+7},{y-5} L{x-1},{y} L{x+7},{y+5} Z" fill="{colour}"/>')


def card(x, y, w, h, colour, title, bar=30):
    return (rect(x + 2, y + 3, w, h, fill="#e9eef4", rx=8) + rect(x, y, w, h, fill="#fff", stroke=colour, sw=1.6, rx=8)
            + f'<path d="M{x},{y+8} a8,8 0 0 1 8,-8 H{x+w-8} a8,8 0 0 1 8,8 V{y+bar} H{x} Z" fill="{colour}"/>'
            + text(x + 10, y + 20, title, 11.5, "#fff", "bold", family=HEAD))


# ---------- Figure 26.1: reading a command (section 26.0) ----------
def fig_anatomy():
    o = [text(20, 28, "Reading a command: a program, then options, then arguments", 13.5, INK, "bold", family=HEAD)]
    o.append(rect(20, 48, 660, 50, fill="#f6f9fc", stroke=RULE, rx=6))
    x0, cw, size = 44, 10.84, 18        # DejaVu Sans Mono: 0.602 em per character
    parts = [(0, "git", INK, "the program"),
             (4, "log", ACC, "which of Git's commands"),
             (8, "--oneline", GREEN, "a long option: two dashes, a word"),
             (18, "-n 2", PURPLE, "a short option with a value: show 2")]
    for start, word, c, _ in parts:
        o.append(text(x0 + start * cw, 81, word, size, c, "bold", family=MONO))
    # labels in rows: the rightmost part takes the top row, so no leader line crosses a label
    for k, (start, word, c, label) in enumerate(parts):
        xa, xb = x0 + start * cw, x0 + (start + len(word)) * cw
        xm = (xa + xb) / 2
        row = 3 - k
        ylab = 130 + row * 22
        o.append(path(f"M{xa},104 V108 H{xb} V104", stroke=c, sw=1.4))
        o.append(path(f"M{xm},108 V{ylab-4} H{xm+8}", stroke=c, sw=1.4))
        o.append(text(xm + 12, ylab, label, 11.5, c, "bold"))
    o.append(rect(20, 214, 660, 50, fill="#fff", stroke=RULE, rx=6))
    o.append(text(32, 234, "Arguments come last and say what to work on, often a file:", 11, INK))
    o.append(text(410, 234, "git add monthly_revenue.sql", 11, INK, "bold", family=MONO))
    o.append(text(32, 254, "Text with spaces goes in quotes, as one argument:", 11, INK))
    o.append(text(345, 254, "git commit -m \"Add monthly revenue query\"", 11, INK, "bold", family=MONO))
    return svg(W, 276, "".join(o))


# ---------- Figure 26.2: the three places a file lives ----------
def fig_three_places():
    cw, gap, x0, y0, h = 172, 72, 20, 70, 196
    places = [
        ("1  Working directory", ACC, "The files as your editor sees them. Edit here. Nothing is safe here yet.",
         ["monthly_revenue.sql", "(edited)"]),
        ("2  Staging area", ORANGE, "What you have chosen for the next snapshot. A shopping basket.",
         ["monthly_revenue.sql", "(chosen)"]),
        ("3  Repository", GREEN, "The history: commits, each with a message, a hash, and an author.",
         ["a2a9885 Split…", "75b063a Revert…"]),
    ]
    o = [text(20, 28, "The three places a file lives, and the commands that move it", 13.5, INK, "bold", family=HEAD),
         text(20, 50, "Almost every confusing Git message is Git telling you which of these three it means.", 11, MUTED, style="italic")]
    for i, (name, c, blurb, sample) in enumerate(places):
        x = x0 + i * (cw + gap)
        o.append(card(x, y0, cw, h, c, name))
        o.append(wrap(x + 10, y0 + 52, wraplines(blurb, 27), 10.5, INK, 16))
        o.append(rect(x + 10, y0 + h - 58, cw - 20, 46, fill="#f6f9fc", stroke=RULE, sw=1, rx=5))
        for k, line in enumerate(sample):
            o.append(text(x + 18, y0 + h - 38 + k * 17, line, 10.5, MUTED, family=MONO))
    ymid = y0 + h / 2
    for i, (cmd, note) in enumerate([("git add", "choose"), ("git commit", "record")]):
        x = x0 + i * (cw + gap) + cw
        o.append(text(x + gap / 2, ymid - 30, cmd, 11, ACC, "bold", anchor="middle", family=MONO))
        o.append(arrow_right(x + 6, ymid - 20, gap - 14, ACC, 2.2))
        o.append(text(x + gap / 2, ymid - 4, note, 10.5, MUTED, anchor="middle", style="italic"))
    for i, cmd in enumerate([["git", "restore"], ["git restore", "--staged"]]):
        x = x0 + i * (cw + gap) + cw
        o.append(arrow_left(x + 8, ymid + 20, gap - 14, RED, 2))
        for k, line in enumerate(cmd):
            o.append(text(x + gap / 2, ymid + 40 + k * 14, line, 10.5, RED, "bold", anchor="middle", family=MONO))
    yb = y0 + h + 34
    o.append(text(20, yb, "And the three commands that only look:", 11.5, INK, "bold"))
    insp = [("git status", "which files differ, and in which of the three places", ACC),
            ("git diff", "what changed in the working directory, line by line (--staged: in the staging area)", ORANGE),
            ("git log", "what is already in the history", GREEN)]
    for k, (cmd, what, c) in enumerate(insp):
        y = yb + 24 + k * 26
        o.append(rect(20, y - 15, 104, 22, fill="#f6f9fc", stroke=c, sw=1.2, rx=5))
        o.append(text(30, y + 1, cmd, 11, c, "bold", family=MONO))
        o.append(text(136, y + 1, what, 10.5, INK))
    return svg(W, yb + 24 + 3 * 26 + 2, "".join(o))


# ---------- Figure 26.3: the four undos ----------
def fig_four_undos():
    cw, h, gap, x0, y0 = 324, 196, 12, 20, 66
    undos = [
        ("1.  You edited a file", ACC, "The change is in the working directory only. Nothing staged, nothing committed.",
         "git restore <file>", "Destructive: the edit was never recorded, so it is gone. Run git diff first."),
        ("2.  You staged the wrong thing", ORANGE, "The change is staged. The file on disk is untouched.",
         "git restore --staged <file>", "Safe. It only takes the file out of the next commit."),
        ("3.  The last commit is wrong", PURPLE, "It is in the history, but you have not pushed it.",
         "git commit --amend", "Safe while private. Never amend a commit others have pulled."),
        ("4.  A shared commit is wrong", GREEN, "It is in the history and other people already have it.",
         "git revert <hash>", "Adds a new commit that undoes it. History is never rewritten."),
    ]
    o = [text(20, 28, "Four things go wrong. Ask where the change is before asking how to undo it.", 13.5, INK, "bold", family=HEAD),
         text(20, 50, "Choosing between these is the whole skill. Typing them is not.", 11, MUTED, style="italic")]
    for i, (title, c, where, cmd, note) in enumerate(undos):
        x = x0 + (i % 2) * (cw + gap)
        y = y0 + (i // 2) * (h + gap)
        o.append(card(x, y, cw, h, c, title))
        o.append(text(x + 12, y + 52, "Where is the change?", 10.5, MUTED, "bold"))
        o.append(wrap(x + 12, y + 70, wraplines(where, 50), 10.5, INK, 16))
        o.append(rect(x + 12, y + h - 86, cw - 24, 28, fill="#f6f9fc", stroke=c, sw=1.2, rx=5))
        o.append(text(x + 22, y + h - 67, cmd, 11.5, c, "bold", family=MONO))
        o.append(wrap(x + 12, y + h - 38, wraplines(note, 52), 10.5, MUTED, 16))
    yb = y0 + 2 * (h + gap) + 8
    o.append(path(f"M20,{yb} H680", stroke=RULE, sw=1.2, dash="4 4"))
    o.append(text(20, yb + 24, "git reset --hard", 11.5, INK, "bold", family=MONO))
    o.append(text(140, yb + 24, "is not on this list on purpose. It is the command that loses work,", 11, INK, "bold"))
    o.append(text(20, yb + 43, "and the four above cover almost everything you will meet in your first two years.", 11, INK, "bold"))
    return svg(W, yb + 56, "".join(o))


# ---------- Figure 26.4: the pull request flow ----------
def fig_pull_request():
    o = [text(20, 28, "From a branch to merged: the loop you will run every working day", 13.5, INK, "bold", family=HEAD),
         text(20, 50, "Branch, commit, push, open a pull request, review, merge. Then pull main and delete the branch.", 11, MUTED, style="italic")]
    ymain, ybr = 104, 184
    o.append(path(f"M70,{ymain} H672", stroke=GREY, sw=3))
    o.append(text(20, ymain + 5, "main", 12, GREY, "bold", family=MONO))
    o.append(text(20, ybr + 5, "branch", 12, ACC, "bold", family=MONO))
    xa, xb = 150, 600
    o.append(path(f"M{xa},{ymain} C{xa+30},{ymain} {xa+30},{ybr} {xa+70},{ybr}", stroke=ACC, sw=3))
    o.append(path(f"M{xa+70},{ybr} H{xb-70}", stroke=ACC, sw=3))
    o.append(path(f"M{xb-70},{ybr} C{xb-30},{ybr} {xb-30},{ymain} {xb},{ymain}", stroke=ACC, sw=3))
    for x in (90, xa, xb, 660):
        o.append(f'<circle cx="{x}" cy="{ymain}" r="7" fill="#fff" stroke="{GREY}" stroke-width="2.6"/>')
    for x in (xa + 110, xa + 190):
        o.append(f'<circle cx="{x}" cy="{ybr}" r="7" fill="#fff" stroke="{ACC}" stroke-width="2.6"/>')
    labels = [(xa - 4, ymain - 34, ["1  git switch -c", "add-order-count"], ACC, "start"),
              (xa + 150, ybr + 30, ["2  commit, then", "git push -u origin", "add-order-count"], TEAL, "middle"),
              (xb + 4, ymain - 34, ["4  merge on GitHub,", "then git pull"], GREEN, "end")]
    for x, y, lines, c, anch in labels:
        for k, line in enumerate(lines):
            o.append(text(x, y + k * 15, line, 10.5, c, "bold" if k == 0 else "normal", anchor=anch, family=MONO))
    bx, by, bw, bh = 384, ybr + 22, 290, 134
    o.append(card(bx, by, bw, bh, PURPLE, "3  The pull request"))
    rows = [("Title", "says what changed, not \"fix query\"", INK),
            ("Description", "what, why, and how you checked", INK),
            ("Review", "questions before demands", PURPLE),
            ("Check", "green before it can merge", GREEN)]
    for k, (lab, body, c) in enumerate(rows):
        y = by + 52 + k * 21
        o.append(text(bx + 12, y, lab, 10.5, MUTED, "bold"))
        o.append(text(bx + 96, y, body, 10.5, c))
    o.append(path(f"M{bx+bw/2},{by} V{ybr+7}", stroke=PURPLE, sw=1.6, dash="4 4"))
    yb = by + bh + 28
    o.append(path(f"M20,{yb} H680", stroke=RULE, sw=1.2, dash="4 4"))
    o.append(text(20, yb + 22, "Nothing here is optional at work. Even a one-line change goes round this loop,", 11, INK, "bold"))
    o.append(text(20, yb + 40, "which is why the loop has to be cheap.", 11, INK, "bold"))
    return svg(W, yb + 52, "".join(o))


if __name__ == "__main__":
    for name, fn in [("fig26-1-anatomy-of-a-command.svg", fig_anatomy),
                     ("fig26-2-three-places.svg", fig_three_places),
                     ("fig26-3-four-undos.svg", fig_four_undos),
                     ("fig26-4-pull-request-flow.svg", fig_pull_request)]:
        open(name, "w").write(fn())
    print("ok")
