# Diagrams for Chapter 17 (Python from Zero). Run: python3 make_figs17.py
# Every figure prints at the full text width (493.2 pt). The canvases are 640 px wide, so 1 px prints
# at 0.77 pt and the smallest text here (9.4 px) prints at 7.2 pt (visual standard: >= 7 pt).
from make_figs import *
from html import escape as _esc
GREEN="#2f7d6d"; PURPLE="#7a4fa0"; ORANGE="#c0662b"; GOLD="#8a5a12"; RED="#b23b3b"; SOFT="#eef2f7"
W = 640
MONO_ADV = 0.6021          # DejaVu Sans Mono advance width, in em


def arrow(x1,y1,x2,y2,c=MUTED,sw=1.6):
    import math
    a=math.atan2(y2-y1,x2-x1); s=8
    p1=(x2-s*math.cos(a-0.45),y2-s*math.sin(a-0.45)); p2=(x2-s*math.cos(a+0.45),y2-s*math.sin(a+0.45))
    return path(f"M{x1},{y1} L{x2},{y2}",stroke=c,sw=sw)+f'<path d="M{x2},{y2} L{p1[0]:.1f},{p1[1]:.1f} L{p2[0]:.1f},{p2[1]:.1f} Z" fill="{c}"/>'


def mono(x, y, s, size, fill=INK, weight="normal"):
    """Monospaced text that keeps its leading spaces: the indent becomes an x offset, so it survives
    any SVG renderer (plain <text> collapses runs of spaces)."""
    lead = len(s) - len(s.lstrip(" "))
    x0 = x + lead * MONO_ADV * size
    return (f'<text x="{x0:.1f}" y="{y}" font-size="{size}" fill="{fill}" font-weight="{weight}" '
            f'font-family="{MONO}">{_esc(s.lstrip(" "))}</text>')


def card(x,y,w,h,title,c,lines,size=10):
    o=[rect(x+2,y+3,w,h,fill=SOFT,rx=7),rect(x,y,w,h,fill="#fff",stroke=c,sw=1.4,rx=7),
       f'<path d="M{x},{y+7} a7,7 0 0 1 7,-7 H{x+w-7} a7,7 0 0 1 7,7 V{y+24} H{x} Z" fill="{c}"/>',
       text(x+9,y+16.5,title,11,"#fff","bold",family=HEAD)]
    for i,l in enumerate(lines):
        bold = l.startswith("Use for:")
        o.append(text(x+9,y+42+i*15.5,l,size,INK,"bold" if bold else "normal"))
    return "".join(o)


def f1():
    o=[text(12,22,"Three ways to run Python, and what each is for",13,INK,"bold",family=HEAD)]
    cw, gap, top, h = 196, 14, 36, 168
    xs = [12, 12+cw+gap, 12+2*(cw+gap)]
    o.append(card(xs[0],top,cw,h,"1. The REPL",ACC,["Type python, get >>>","Each line runs when you press Enter",
             "Shows each expression's value","Nothing is saved","","Use for: trying one thing,","checking what a function does"]))
    o.append(card(xs[1],top,cw,h,"2. A notebook (Jupyter)",GREEN,["Cells of code, output underneath","Notes and charts in between",
             "Values stay between cells","Cells can run out of order","","Use for: exploring data,","showing your working"]))
    o.append(card(xs[2],top,cw,h,"3. A script (.py file)",PURPLE,["Runs top to bottom, every time","Only print() shows anything",
             "Takes arguments, gives an exit code","Can be scheduled and versioned","","Use for: anything repeated,","shared, or run at 6 a.m."]))
    y = top+h+20
    x1 = xs[1]+cw/2; x2 = xs[2]+cw/2
    o.append(path(f"M{x1},{top+h+3} V{y}",stroke=MUTED,sw=1.6))
    o.append(arrow(x1,y,x2,y,MUTED)); o.append(path(f"M{x2},{y} V{top+h+11}",stroke=MUTED,sw=1.6))
    o.append(arrow(x2,y,x2,top+h+5,MUTED))
    o.append(text((x1+x2)/2,y+16,"when it works, move it into a script (section 17.12)",10,INK,anchor="middle"))
    return svg(W,y+26,"".join(o))


TRACE = [
    "Traceback (most recent call last):",
    '  File "/home/meera/analyst-to-architect/work/ch17/summarize_exports.py", line 51, in <module>',
    "    raise SystemExit(main(folder))",
    "                     ~~~~^^^^^^^^",
    '  File "/home/meera/analyst-to-architect/work/ch17/summarize_exports.py", line 42, in main',
    "    s = summarize(path)",
    '  File "/home/meera/analyst-to-architect/work/ch17/summarize_exports.py", line 23, in summarize',
    '    values.append(float(row["net_revenue"]))',
    "                  ~~~~~^^^^^^^^^^^^^^^^^^^^",
    "ValueError: could not convert string to float: ''",
]


def marker(x, y, n, c):
    return (f'<circle cx="{x}" cy="{y}" r="7.5" fill="{c}"/>'
            + text(x, y+3.6, str(n), 10, "#fff", "bold", anchor="middle"))


def f2():
    o=[text(12,22,"How to read a traceback: start at the bottom",13,INK,"bold",family=HEAD)]
    size, lh, top = 9.4, 15, 44
    box_h = len(TRACE)*lh + 16
    o.append(rect(34,top-4,W-46,box_h,fill="#fff",stroke=RULE,rx=6))
    marks = {9: (1, RED), 7: (2, ORANGE), 6: (3, ACC), 0: (4, MUTED)}
    for i, l in enumerate(TRACE):
        y = top + 12 + i*lh
        last = i == len(TRACE)-1
        o.append(mono(42, y, l, size, RED if last else INK, "bold" if last else "normal"))
        if i in marks:
            n, c = marks[i]
            o.append(marker(20, y-3.5, n, c))
    ky = top + box_h + 22
    key = [(1, RED, "What went wrong: the error type and its message. Read this line first."),
           (2, ORANGE, "The line of code that failed, with ~~^^ marks under the part that raised the error."),
           (3, ACC, "Where that line is: the file, the line number, and the function it is in."),
           (4, MUTED, "The chain of calls that led there, oldest at the top. Read it only if you need to.")]
    for j, (n, c, s) in enumerate(key):
        y = ky + j*19
        o.append(marker(20, y-3.5, n, c)); o.append(text(34, y, s, 10, INK))
    by = ky + len(key)*19 + 6
    o.append(rect(12,by,W-24,62,fill="#fff",stroke=GREEN,sw=1.4,rx=6)); o.append(rect(12,by,6,62,fill=GREEN))
    o.append(text(28,by+18,"What it tells you here:",10.5,INK,"bold"))
    o.append(text(28,by+35,"a blank net_revenue in a CSV file reached float(). The fix is to convert defensively and",10,INK))
    o.append(text(28,by+51,"count what failed (see “Handling errors on purpose”, below).",10,INK))
    return svg(W,by+70,"".join(o))


def f3():
    o=[text(12,22,"Which collection should I use?",13,INK,"bold",family=HEAD)]
    o.append(text(24,44,"Collection",9.6,MUTED,"bold")); o.append(text(112,44,"What it is, and a Riverstone example",9.6,MUTED,"bold"))
    o.append(text(400,44,"Typical operations",9.6,MUTED,"bold"))
    rows=[("list","Ordered, changeable","order lines in a file; the months of a year","values[0] · append() · sorted()",ACC),
          ("tuple","Fixed, unchangeable","(city, region); what a function returns","city, region = pair",GOLD),
          ("dict","Lookup: key → value","city → region; product → price; counts","d[k] · d.get(k, default) · d.items()",GREEN),
          ("set","Unique values, fast membership","distinct cities; codes in A but not B","a & b · a | b · a - b",PURPLE),
          ("DataFrame","Rows and columns (Chapter 18)","a whole CSV file, a query result","df.groupby() · df.merge()",MUTED)]
    for i,(name,what,egs,ops,c) in enumerate(rows):
        y=54+i*48
        o.append(rect(12,y,W-24,40,fill="#fff",stroke=RULE,rx=5)); o.append(rect(12,y,6,40,fill=c))
        o.append(text(24,y+25,name,11,c,"bold",family=MONO))
        o.append(text(112,y+17,what,10,INK,"bold")); o.append(text(112,y+32,egs,9.6,MUTED))
        o.append(text(400,y+25,ops,9.4,INK,family=MONO))
    return svg(W,54+5*48+6,"".join(o))


def widths_report(svgtext):
    """Warn about text that runs past the canvas (measured with matplotlib's font metrics)."""
    import re
    try:
        from matplotlib.textpath import TextPath
        from matplotlib.font_manager import FontProperties
    except ImportError:
        return []
    out = []
    for m in re.finditer(r'<text x="([\d.]+)" y="[\d.]+" font-size="([\d.]+)"[^>]*?font-weight="(\w+)"[^>]*?(font-family="([^"]+)")?[^>]*>([^<]*)</text>', svgtext):
        x, size, weight, fam, s = float(m.group(1)), float(m.group(2)), m.group(3), m.group(5) or "", m.group(6)
        if not s:
            continue
        import html
        s = html.unescape(s)
        fp = FontProperties(family="DejaVu Sans Mono" if "Mono" in fam else "DejaVu Sans", weight=weight)
        w = TextPath((0, 0), s, size=size, prop=fp).get_extents().x1
        if 'text-anchor="middle"' in m.group(0):
            x -= w / 2
        if x + w > W - 4:
            out.append(f"  overflow {x + w:.0f}px > {W}: {s[:50]}")
    return out


if __name__ == "__main__":
    for n,f in [("fig17-1-three-ways-to-run.svg",f1),("fig17-2-traceback.svg",f2),("fig17-3-collections.svg",f3)]:
        s = f()
        open(n,"w").write(s)
        for line in widths_report(s):
            print(n, line)
    print("ok")
