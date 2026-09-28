# Generates the SVG figures for Chapter 34. Run: python3 make_figs34.py
# Every figure prints at the full text width (493.2 pt). The canvases are 700 px wide, so a font of s px prints
# at s x 0.705 pt: the smallest text here, 10.5 px, prints at 7.4 pt (visual standard: 7 pt or more).
from make_figs import *
from make_figs01 import wrap

GREEN = "#2f7d6d"; PURPLE = "#7a4fa0"; ORANGE = "#c0662b"; RED = "#b23b3b"
W = 700


def arrow(x1, y1, x2, y2, colour=INK, sw=1.8):
    """A straight arrow from (x1, y1) to (x2, y2), horizontal or vertical."""
    if y1 == y2:
        d = 1 if x2 > x1 else -1
        head = f'<path d="M{x2-8*d},{y2-5} L{x2},{y2} L{x2-8*d},{y2+5} Z" fill="{colour}"/>'
        return path(f"M{x1},{y1} H{x2-7*d}", stroke=colour, sw=sw) + head
    d = 1 if y2 > y1 else -1
    head = f'<path d="M{x2-5},{y2-8*d} L{x2},{y2} L{x2+5},{y2-8*d} Z" fill="{colour}"/>'
    return path(f"M{x1},{y1} V{y2-7*d}", stroke=colour, sw=sw) + head


def box(x, y, w, h, colour, fill="#fff", sw=1.6):
    return rect(x, y, w, h, fill=fill, stroke=colour, sw=sw, rx=7)


# ---------- Figure 34.1: three channels and an exit code ----------
def fig_channels():
    o = [text(20, 28, "One command: one channel in, two channels out, and an exit code", 13.5, INK, "bold", family=HEAD)]
    # the command in the middle
    cx, cy, cw, ch = 214, 92, 272, 62
    o.append(box(cx, cy, cw, ch, INK, fill="#f6f9fc"))
    o.append(text(cx + cw / 2, cy + 25, "grep -c \"Pune\"", 12, INK, "bold", anchor="middle", family=MONO))
    o.append(text(cx + cw / 2, cy + 45, "../sales_lines_2025.csv", 12, INK, "bold", anchor="middle", family=MONO))
    # standard input, on the left
    o.append(box(20, 80, 160, 86, ACC))
    o.append(text(32, 102, "standard input", 11.5, ACC, "bold"))
    o.append(wrap(32, 122, ["the keyboard, a file", "(< file), or the output", "of a pipe (|)"], 10.5, INK, 15))
    o.append(arrow(180, cy + ch / 2, cx - 2, cy + ch / 2, ACC))
    # standard output and standard error, on the right
    o.append(box(520, 52, 160, 78, GREEN))
    o.append(text(532, 73, "standard output", 11.5, GREEN, "bold"))
    o.append(text(532, 92, "42", 12, INK, "bold", family=MONO))
    o.append(wrap(532, 110, ["the screen, a file (> file),", "or the next command (|)"], 10.5, INK, 15))
    o.append(box(520, 142, 160, 78, RED))
    o.append(text(532, 163, "standard error", 11.5, RED, "bold"))
    o.append(text(532, 182, "(nothing this time)", 10.5, INK, style="italic"))
    o.append(wrap(532, 200, ["the screen, even in a pipe,", "or a file (2> file)"], 10.5, INK, 15))
    o.append(path(f"M{cx+cw+2},{cy+20} H500 V91 H512", stroke=GREEN, sw=1.8))
    o.append(f'<path d="M512,86 L520,91 L512,96 Z" fill="{GREEN}"/>')
    o.append(path(f"M{cx+cw+2},{cy+42} H500 V181 H512", stroke=RED, sw=1.8, dash="5 3"))
    o.append(f'<path d="M512,176 L520,181 L512,186 Z" fill="{RED}"/>')
    # the exit code, below
    o.append(arrow(cx + cw / 2, cy + ch, cx + cw / 2, 196, PURPLE))
    o.append(box(cx + 16, 198, cw - 32, 56, PURPLE))
    o.append(text(cx + cw / 2, 220, "exit code:  echo $?  prints 0", 11.5, PURPLE, "bold", anchor="middle", family=MONO))
    o.append(text(cx + cw / 2, 240, "0 means it worked; anything else, it failed", 10.5, INK, anchor="middle"))
    o.append(text(20, 284, "Output and errors are separate channels, so a pipe or a file can take one and leave the other on the screen.",
                  10.5, MUTED, style="italic"))
    return svg(W, 300, "".join(o))


# ---------- Figure 34.2: the pipeline, stage by stage ----------
def fig_pipeline():
    o = [text(20, 28, "One question, five small tools: order lines by city", 13.5, INK, "bold", family=HEAD)]
    stages = [("cut -d, -f5", ["keep column 5", "(the city)"], "327 lines", ACC),
              ("tail -n +2", ["drop the", "header row"], "326 lines", PURPLE),
              ("sort", ["put identical", "cities together"], "326 lines", GREEN),
              ("uniq -c", ["collapse and", "count each run"], "16 lines", ORANGE),
              ("sort -nr", ["biggest", "first"], "16 lines", GREEN)]
    bw, gap, x = 116, 20, 20
    for i, (cmd, what, rows, c) in enumerate(stages):
        o.append(box(x, 50, bw, 104, c, sw=2))
        o.append(text(x + bw / 2, 74, cmd, 11.5, INK, "bold", anchor="middle", family=MONO))
        for j, line in enumerate(what):
            o.append(text(x + bw / 2, 98 + j * 16, line, 10.5, INK, anchor="middle"))
        o.append(text(x + bw / 2, 144, rows, 11, c, "bold", anchor="middle"))
        if i < 4:
            o.append(arrow(x + bw + 2, 102, x + bw + gap - 1, 102, INK, 1.8))
        x += bw + gap
    o.append(rect(20, 176, 230, 104, fill="#f6f9fc", stroke=RULE, rx=6))
    for i, line in enumerate(["74 Mumbai", "42 Pune", "34 Bengaluru", "28 Delhi", "21 Kochi"]):
        o.append(text(38, 198 + i * 18, line, 11.5, INK, family=MONO))
    o.append(wrap(276, 198, ["Each tool reads what the one before it wrote.",
                             "Nothing is saved in between, so the same command",
                             "works on a 2 GB file on a server with no Excel.",
                             "The 16 lines after uniq -c are the 16 cities;",
                             "head -5 then keeps the top five."], 11, INK, 19))
    o.append(text(20, 306, "Forgetting sort before uniq -c is the classic bug: uniq only collapses lines that are already next to each other.",
                  10.5, MUTED, style="italic"))
    return svg(W, 320, "".join(o))


# ---------- Figure 34.3: reading ls -l ----------
def fig_permissions():
    o = [text(20, 28, "Reading ls -l", 13.5, INK, "bold", family=HEAD)]
    o.append(rect(20, 44, 660, 36, fill="#f6f9fc", stroke=RULE, rx=6))
    line = "-rw-r--r--  1  meera  meera  877  Jan  5  2026  customers.csv"
    x0, cw = 34, 7.826      # DejaVu Sans Mono advance is 0.602 em; 13 px -> 7.83 px a character
    o.append(text(x0, 68, line, 13, INK, "bold", family=MONO))
    # the four parts of the first column; the rightmost part gets the top label row, so no leader crosses a label
    parts = [(0, 1, "type: - a file, d a folder, l a link", INK),
             (1, 4, "user (the owner): rw- read and write", GREEN),
             (4, 7, "group: r-- read only", PURPLE),
             (7, 10, "others (everyone else): r-- read only", ORANGE)]
    for k, (a, b, label, c) in enumerate(parts):
        xa, xb = x0 + a * cw + 1, x0 + b * cw - 1
        xm = (xa + xb) / 2
        row = 3 - k                                  # others -> row 0 ... type -> row 3
        ylab = 108 + row * 20
        o.append(path(f"M{xa},84 V88 H{xb} V84", stroke=c, sw=1.4))
        o.append(path(f"M{xm},88 V{ylab-4} H{xm+8}", stroke=c, sw=1.4))
        o.append(text(xm + 12, ylab, label, 11, c, "bold"))
    o.append(wrap(380, 108, ["Each set of three is read (r), write (w),", "execute (x), or - for \"not allowed\".",
                             "On a folder, x means \"can go into it\".",
                             "Then: links, owner, group, size, date, name."], 11, INK, 20))
    rows = [("644", "rw- r-- r--", "owner writes, everyone reads", "data files, documents", ACC),
            ("755", "rwx r-x r-x", "owner writes, everyone reads and runs", "scripts, folders", GREEN),
            ("600", "rw- --- ---", "owner only", "SSH keys, .env files", ORANGE),
            ("700", "rwx --- ---", "owner only, and can go in", "~/.ssh", PURPLE)]
    y = 210
    o.append(text(20, y - 9, "Each set is also a digit: read 4 + write 2 + execute 1.", 11, INK, "bold"))
    for num, bits, who, use, c in rows:
        o.append(box(20, y, 660, 32, c, sw=1.4))
        o.append(text(36, y + 21, num, 12.5, c, "bold", family=MONO))
        o.append(text(86, y + 21, bits, 11.5, INK, family=MONO))
        o.append(text(196, y + 21, who, 11, INK))
        o.append(text(480, y + 21, use, 11, MUTED))
        y += 40
    o.append(text(20, y + 14, "chmod +x script.sh adds the execute bit; chmod 600 key removes everyone else's access.", 10.5, MUTED, style="italic"))
    return svg(W, y + 28, "".join(o))


# ---------- Figure 34.4: what happens when curl asks for a file ----------
def fig_request():
    o = [text(20, 28, "What happens when curl asks for a file", 13.5, INK, "bold", family=HEAD)]
    o.append(rect(20, 44, 660, 34, fill="#f6f9fc", stroke=RULE, rx=6))
    o.append(text(32, 66, "curl --silent http://127.0.0.1:8034/exports/orders_2025-12-16.csv", 11.5, INK, "bold", family=MONO))
    parts = [("http", "the protocol: HTTP, or https for an encrypted connection", ACC),
             ("127.0.0.1", "which machine: localhost, this one", GREEN),
             ("8034", "which program on it: the port it listens on", PURPLE),
             ("/exports/orders_…", "what to ask for: the path", ORANGE)]
    for i, (lab, note, c) in enumerate(parts):
        y = 102 + i * 20
        o.append(text(32, y, lab, 11.5, c, "bold", family=MONO))
        o.append(text(180, y, note, 11, INK))
    steps = [("1. Name → address", "A name like api.example.com is looked up in DNS. 127.0.0.1 is already an address.", ACC),
             ("2. Connect to the port", "The program listening on port 8034 accepts. ss -ltn shows what is listening.", GREEN),
             ("3. Send the request", "GET /exports/orders_2025-12-16.csv, plus headers such as an API key.", PURPLE),
             ("4. Read the answer", "A status code (200 OK, 404 not found, 500 and up: the server failed), headers, the body.", ORANGE)]
    y = 188
    for title, desc, c in steps:
        o.append(box(20, y, 660, 46, c, sw=1.5))
        o.append(text(34, y + 19, title, 11.5, c, "bold"))
        o.append(text(34, y + 37, desc, 10.5, INK))
        y += 54
    return svg(W, y + 6, "".join(o))


if __name__ == "__main__":
    for name, fn in [("fig34-1-anatomy-of-a-command.svg", fig_channels), ("fig34-2-pipeline-stages.svg", fig_pipeline),
                     ("fig34-3-permissions.svg", fig_permissions), ("fig34-4-http-request.svg", fig_request)]:
        open(name, "w").write(fn())
    print("ok34")
