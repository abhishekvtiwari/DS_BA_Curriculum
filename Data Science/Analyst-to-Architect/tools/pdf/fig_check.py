"""Smallest text size of each figure as it prints (visual review theme V3: figure text >= 7 pt).

    python tools/pdf/fig_check.py manuscript/ch01-*.md            # every figure a chapter uses
    python tools/pdf/fig_check.py figures/fig1-2-receipt-to-table.svg

A figure is printed at the full text width (book.css: p > img { width: 100% }), which is 174 mm =
493.2 pt, however wide its SVG canvas is. So a font of s px on a canvas W px wide prints at
s * 493.2 / W pt. Figures whose text is drawn as paths (matplotlib with svg.fonttype=path) have no
<text> elements; they are reported as "paths" and must be checked by eye.
"""
import sys, re, pathlib, glob

PRINT_PT = (210 - 18 - 18) / 25.4 * 72     # text width in pt
ROOT = pathlib.Path(__file__).resolve().parents[2]


def svg_sizes(path):
    s = pathlib.Path(path).read_text(encoding='utf-8')
    m = re.search(r'viewBox="[-\d.]+ [-\d.]+ ([\d.]+) [\d.]+"', s) or re.search(r'<svg[^>]*\swidth="([\d.]+)', s)
    W = float(m.group(1))
    default = re.search(r'<svg[^>]*font-size="([\d.]+)"', s)
    sizes = [float(x) for x in re.findall(r'<text[^>]*font-size="([\d.]+)', s)]
    sizes += [float(x) for x in re.findall(r'font-size:\s*([\d.]+)px', s)]
    if not sizes and default:
        sizes = [float(default.group(1))]
    k = PRINT_PT / W
    return W, (round(min(sizes) * k, 2) if sizes else None), (round(max(sizes) * k, 2) if sizes else None), len(re.findall(r'<text', s))


def figures_of(md):
    t = pathlib.Path(md).read_text(encoding='utf-8')
    return [ROOT / m for m in re.findall(r'!\[[^\]]*\]\((figures/[^)]+\.svg)\)', t)]


if __name__ == '__main__':
    targets = []
    for a in sys.argv[1:]:
        for p in glob.glob(a):
            targets += figures_of(p) if p.endswith('.md') else [pathlib.Path(p)]
    bad = 0
    for f in targets:
        W, lo, hi, n = svg_sizes(f)
        flag = 'paths' if lo is None else ('OK' if lo >= 7 else 'SMALL')
        bad += flag == 'SMALL'
        print(f'{flag:5}  min {lo} pt  max {hi} pt  canvas {W:.0f}px  {n} text  {f.name}')
    print(f'{bad} figure(s) with text under 7 pt')
