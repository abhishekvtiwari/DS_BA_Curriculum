# Generates the SVG figures for Chapter 26. Run: python3 make_figs26.py
from make_figs import *
from make_figs01 import wrap

GREEN="#2f7d6d"; PURPLE="#7a4fa0"; ORANGE="#c0662b"; RED="#b23b3b"; TEAL="#1f6fa3"; GREY="#5b6475"


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
            + f'<path d="M{x+length-6},{y-5} L{x+length+1},{y} L{x+length-6},{y+5} Z" fill="{colour}"/>')


def arrow_left(x, y, length, colour=MUTED, sw=2):
    return (path(f"M{x+length},{y} H{x+6}", stroke=colour, sw=sw)
            + f'<path d="M{x+6},{y-5} L{x-1},{y} L{x+6},{y+5} Z" fill="{colour}"/>')


# ---------- Figure 26.1: the three places a file lives ----------
def fig_three_places():
    W, H, G, x0, y0 = 250, 210, 148, 34, 86
    places = [
        ("Working directory", ACC, "The files as your editor sees them. Edit here. Nothing is safe here.",
         ["monthly_revenue.sql", "  (edited, unsaved to Git)"]),
        ("Staging area", ORANGE, "What you have chosen to put in the next snapshot. A shopping basket.",
         ["monthly_revenue.sql", "  (selected for commit)"]),
        ("Repository (history)", GREEN, "Commits. Permanent, each with a message, a hash, and an author.",
         ["6489661 Split monthly revenue", "1bed4f9 Revert \"Limit the...\""]),
    ]
    o = [text(x0, 36, "The three places a file lives, and the commands that move it",
              15.5, INK, "bold", family=HEAD),
         text(x0, 60, "Almost every confusing Git message is Git telling you which of these three it means.",
              12.5, MUTED, style="italic")]
    for i, (name, c, blurb, sample) in enumerate(places):
        x = x0 + i * (W + G)
        o.append(rect(x + 2, y0 + 3, W, H, fill="#e9eef4", rx=8))
        o.append(rect(x, y0, W, H, fill="#fff", stroke=c, sw=1.6, rx=8))
        o.append(f'<path d="M{x},{y0+8} a8,8 0 0 1 8,-8 H{x+W-8} a8,8 0 0 1 8,8 V{y0+34} H{x} Z" fill="{c}"/>')
        o.append(text(x + 12, y0 + 23, f"{i+1}  {name}", 13, "#fff", "bold", family=HEAD))
        o.append(wrap(x + 12, y0 + 58, wraplines(blurb, 32), 11.5, INK, 17))
        o.append(rect(x + 12, y0 + H - 74, W - 24, 56, fill="#f6f9fc", stroke=RULE, sw=1, rx=5))
        for k, line in enumerate(sample):
            o.append(text(x + 20, y0 + H - 54 + k * 20, line, 10, MUTED, family=MONO))
    # forward arrows with command labels
    ymid = y0 + H / 2
    for i, (cmd, note) in enumerate([("git add", "choose"), ("git commit", "record")]):
        x = x0 + i * (W + G) + W
        o.append(arrow_right(x + 14, ymid - 16, G - 28, ACC, 2.4))
        o.append(text(x + G / 2, ymid - 26, cmd, 12, ACC, "bold", anchor="middle", family=MONO))
        o.append(text(x + G / 2, ymid + 2, note, 10.5, MUTED, anchor="middle", style="italic"))
    # backward arrows
    for i, cmd in enumerate([["git restore"], ["git restore", "--staged"]]):
        x = x0 + i * (W + G) + W
        o.append(arrow_left(x + 14, ymid + 40, G - 28, RED, 2))
        for k, line in enumerate(cmd):
            o.append(text(x + G / 2, ymid + 62 + k * 15, line, 10.5, RED, "bold", anchor="middle", family=MONO))
    yb = y0 + H + 46
    insp = [("git status", "which files differ, and in which of the three", ACC),
            ("git diff", "what changed in the working directory, line by line", ORANGE),
            ("git log", "what is already in the history", GREEN)]
    o.append(text(x0, yb, "And the three commands that only look:", 12.5, INK, "bold"))
    for k, (cmd, what, c) in enumerate(insp):
        y = yb + 26 + k * 28
        o.append(rect(x0, y - 14, 156, 22, fill="#f6f9fc", stroke=c, sw=1.2, rx=5))
        o.append(text(x0 + 10, y + 2, cmd, 11.5, c, "bold", family=MONO))
        o.append(text(x0 + 172, y + 2, what, 12, INK))
    return svg(x0 * 2 + 3 * W + 2 * G, yb + 26 + 3 * 28 + 14, "".join(o))


# ---------- Figure 26.2: the four undos ----------
def fig_four_undos():
    W, H, G, x0, y0 = 300, 232, 22, 34, 88
    undos = [
        ("1", "You edited a file", ACC, "The change is in the working directory only. Nothing staged, nothing committed.",
         "git restore <file>", "Destructive: the edit was never recorded, so it is gone. Run git diff first."),
        ("2", "You staged the wrong thing", ORANGE, "The change is staged. The file on disk is untouched.",
         "git restore --staged <file>", "Safe. It only removes the file from the next commit."),
        ("3", "The last commit is wrong", PURPLE, "It is in the history, but you have not pushed it.",
         "git commit --amend", "Safe while private. Never amend a commit others have pulled."),
        ("4", "A shared commit is wrong", GREEN, "It is in the history and other people already have it.",
         "git revert <hash>", "Adds a new commit that undoes it. History is never rewritten."),
    ]
    o = [text(x0, 36, "Four things go wrong. Ask where the change is before asking how to undo it.",
              15.5, INK, "bold", family=HEAD),
         text(x0, 60, "Choosing between these is the whole skill. Typing them is not.",
              12.5, MUTED, style="italic")]
    for i, (num, title, c, where, cmd, note) in enumerate(undos):
        col, row = i % 2, i // 2
        x = x0 + col * (W + G)
        y = y0 + row * (H + G)
        o.append(rect(x + 2, y + 3, W, H, fill="#e9eef4", rx=8))
        o.append(rect(x, y, W, H, fill="#fff", stroke=c, sw=1.6, rx=8))
        o.append(f'<path d="M{x},{y+8} a8,8 0 0 1 8,-8 H{x+W-8} a8,8 0 0 1 8,8 V{y+36} H{x} Z" fill="{c}"/>')
        o.append(text(x + 14, y + 25, f"{num}.  {title}", 13, "#fff", "bold", family=HEAD))
        o.append(text(x + 14, y + 60, "Where is the change?", 11, MUTED, "bold"))
        o.append(wrap(x + 14, y + 80, wraplines(where, 40), 11.5, INK, 17))
        o.append(rect(x + 14, y + H - 96, W - 28, 30, fill="#f6f9fc", stroke=c, sw=1.2, rx=5))
        o.append(text(x + 24, y + H - 76, cmd, 12.5, c, "bold", family=MONO))
        o.append(wrap(x + 14, y + H - 48, wraplines(note, 44), 11, MUTED, 16))
    yb = y0 + 2 * (H + G) + 16
    o.append(path(f"M{x0},{yb} H{x0+2*W+G}", stroke=RULE, sw=1.2, dash="4 4"))
    o.append(text(x0, yb + 28, "git reset --hard is not on this list on purpose. It is the command that loses work,",
                  12.5, INK, "bold"))
    o.append(text(x0, yb + 48, "and the four above cover almost everything you will meet in your first two years.",
                  12.5, INK, "bold"))
    return svg(x0 * 2 + 2 * W + G, yb + 68, "".join(o))


# ---------- Figure 26.3: the pull request flow ----------
def fig_pull_request():
    x0, y0, W = 40, 92, 1180
    o = [text(x0, 38, "From a branch to merged: the loop you will run every working day",
              15.5, INK, "bold", family=HEAD),
         text(x0, 62, "The unit of work on a team is not a commit. It is a pull request.",
              12.5, MUTED, style="italic")]
    ymain = y0 + 44
    ybr = y0 + 150
    o.append(path(f"M{x0+40},{ymain} H{x0+W-40}", stroke=GREY, sw=3))
    o.append(text(x0, ymain + 5, "main", 13, GREY, "bold", family=MONO))
    o.append(text(x0, ybr + 5, "branch", 13, ACC, "bold", family=MONO))
    xa, xb = x0 + 210, x0 + W - 150
    o.append(path(f"M{xa},{ymain} C{xa+40},{ymain} {xa+40},{ybr} {xa+90},{ybr}", stroke=ACC, sw=3))
    o.append(path(f"M{xa+90},{ybr} H{xb-90}", stroke=ACC, sw=3))
    o.append(path(f"M{xb-90},{ybr} C{xb-40},{ybr} {xb-40},{ymain} {xb},{ymain}", stroke=ACC, sw=3))
    for x in (x0 + 100, xa, xb, x0 + W - 70):
        o.append(f'<circle cx="{x}" cy="{ymain}" r="8" fill="#fff" stroke="{GREY}" stroke-width="2.6"/>')
    for x in (xa + 150, xa + 290, xa + 430):
        o.append(f'<circle cx="{x}" cy="{ybr}" r="8" fill="#fff" stroke="{ACC}" stroke-width="2.6"/>')
    steps = [
        (xa + 6, ymain - 44, ["git switch -c", "fix-cancelled-orders"], ACC, "start"),
        (xa + 290, ymain + 38, ["commit, commit, commit", "small and reviewable"], ACC, "middle"),
        (xa + 570, ymain + 38, ["git push -u origin", "<branch>"], TEAL, "middle"),
        (xb + 6, ymain - 44, ["git merge", "(via the pull request)"], GREEN, "start"),
    ]
    for x, y, lines, c, anch in steps:
        for k, line in enumerate(lines):
            o.append(text(x, y + k * 17, line, 11, c, "bold" if k == 0 else "normal",
                          anchor=anch, family=MONO))
    bx, by, bw, bh = xa + 400, ybr + 56, 340, 150
    o.append(rect(bx + 2, by + 3, bw, bh, fill="#e9eef4", rx=8))
    o.append(rect(bx, by, bw, bh, fill="#fff", stroke=PURPLE, sw=1.8, rx=8))
    o.append(f'<path d="M{bx},{by+8} a8,8 0 0 1 8,-8 H{bx+bw-8} a8,8 0 0 1 8,8 V{by+36} H{bx} Z" fill="{PURPLE}"/>')
    o.append(text(bx + 14, by + 25, "The pull request", 13, "#fff", "bold", family=HEAD))
    rows = [("Title", "says what changed, not \"fix query\"", INK),
            ("Description", "what, why, and how you checked", INK),
            ("Review", "questions before demands", PURPLE),
            ("Check", "green before it can merge", GREEN)]
    for k, (lab, body, c) in enumerate(rows):
        y = by + 60 + k * 24
        o.append(text(bx + 14, y, lab, 11, MUTED, "bold"))
        o.append(text(bx + 106, y, body, 11, c))
    o.append(path(f"M{bx+bw/2},{by} V{ybr+8}", stroke=PURPLE, sw=1.6, dash="4 4"))
    o.append(f'<circle cx="{bx+bw/2}" cy="{ybr}" r="5" fill="{PURPLE}"/>')
    yb = by + bh + 34
    o.append(path(f"M{x0},{yb} H{x0+W}", stroke=RULE, sw=1.2, dash="4 4"))
    o.append(text(x0, yb + 28,
                  "Nothing here is optional at work. Even a one-line change goes round this loop, which is why the loop has to be cheap.",
                  12.5, INK, "bold"))
    return svg(x0 * 2 + W, yb + 48, "".join(o))


if __name__ == "__main__":
    for name, fn in [("fig26-1-three-places.svg", fig_three_places),
                     ("fig26-2-four-undos.svg", fig_four_undos),
                     ("fig26-3-pull-request-flow.svg", fig_pull_request)]:
        open(name, "w").write(fn())
    print("ok")
