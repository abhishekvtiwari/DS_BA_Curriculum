# Generates the SVG figures for Chapter 57. Run: python3 make_figs57.py
# Every number is measured here by the chapter's own code (companion/ch57, companion/ch55).
# Canvas 740 px wide prints at 174 mm (493.2 pt), so 11 px text prints at 7.3 pt.
import os, random, sys
from pathlib import Path
from make_figs import *

HERE = Path(__file__).resolve().parent
COMP = HERE.parent / "companion"
sys.path.insert(0, str(COMP / "ch57")); sys.path.insert(0, str(COMP / "ch55"))
from pipeline import (PROMPTS, Cache, build_prompt, call_with_fallback, emails, evaluate, parse,
                      tolerant_parse, truth)
from provider import NEW_MODEL, PINNED_MODEL, Meter, call

GREEN = "#2f7d6d"; PURPLE = "#7a4fa0"; ORANGE = "#c0662b"; RED = "#b23b3b"
W = 740


def fig_upgrade():
    runs = [(f"pinned {PINNED_MODEL}", "Chapter 54's parse", evaluate("v3"), GREEN,
             "the system as it|ran on Friday"),
            (f"new {NEW_MODEL}", "Chapter 54's parse", evaluate("v3", model=NEW_MODEL), RED,
             "every reply unparseable:|nothing loads"),
            (f"new {NEW_MODEL}", "tolerant_parse", evaluate("v3", model=NEW_MODEL, parser=tolerant_parse),
             GREEN, "drop comment lines, fix|the date: 20 minutes")]
    o = [text(20, 28, "The day the provider changed the model", 15, INK, "bold", family=HEAD),
         text(20, 48, "Prompt v3 on the 60-email golden set", 12, MUTED)]
    y = 70; x0, bw = 220, 300
    for model, parser, r, c, note in runs:
        o.append(text(20, y + 16, model, 12, INK, "bold"))
        o.append(text(20, y + 33, parser, 11.5, MUTED))
        o.append(rect(x0, y, bw, 38, fill=ROWALT, stroke=RULE, rx=4))
        if r["unparseable"]:
            o.append(rect(x0, y, bw * r["unparseable"] / 60, 38, fill="#f6dcdc", stroke=RED, rx=4))
            o.append(text(x0 + 10, y + 24, f"0 correct: {r['unparseable']} of 60 unparseable", 12, RED, "bold"))
        else:
            o.append(rect(x0, y, bw * r["exact"] / 60, 38, fill=c, stroke=c, rx=4))
            o.append(text(x0 + 10, y + 24, f"{r['exact']} of 60 correct", 12, "#ffffff", "bold"))
        for k, part in enumerate(note.split("|")):
            o.append(text(x0 + bw + 12, y + 16 + 16 * k, part, 11.5, MUTED))
        y += 56
    o.append(rect(x0, y + 4, bw, 50, fill=PKBG, stroke=PK, rx=6))
    o.append(text(x0 + bw / 2, y + 24, "The model was not worse.", 12.5, INK, "bold", anchor="middle"))
    o.append(text(x0 + bw / 2, y + 43, "A contract nobody enforced had changed.", 12, INK, anchor="middle"))
    o.append(text(20, y + 80, "A nightly golden-set run turns this into a Saturday-night build failure.", 12, MUTED))
    o.append(text(20, y + 98, "Without it, it is a Monday morning with no orders.", 12, MUTED))
    return svg(W, y + 112, "".join(o))


def cache_day():
    rng = random.Random(57)
    day = rng.sample(list(truth), 40)
    traffic = day + [rng.choice(day) for _ in range(8)]
    rng.shuffle(traffic)
    cache, cached, plain = Cache(), Meter(), Meter()
    for name in traffic:
        p = build_prompt("v3", emails[name])
        cache.get_or_call(p, PINNED_MODEL, cached)
        call(p, model=PINNED_MODEL, meter=plain)
    return len(traffic), cache, cached.cost_rupees(), plain.cost_rupees()


def fig_resilience():
    n, cache, with_c, without_c = cache_day()
    routes = {"primary": 0, "fallback": 0, "failed": 0}; m = Meter()
    for name in truth:
        _, r = call_with_fallback(build_prompt("v3", emails[name]), m, failure_rate=0.2, backoff=0)
        routes[r] += 1
    errors = sum(m.errors.values())
    o = [text(20, 28, "Cost and failure: the work that decides the bill and the uptime", 15, INK, "bold", family=HEAD)]
    # left panel
    o.append(rect(20, 48, 340, 250, fill="#fff", stroke=GREEN, sw=1.6, rx=8))
    o.append(text(36, 74, "Exact-match cache, a normal day", 12.5, GREEN, "bold"))
    o.append(text(36, 92, f"{n} requests: 40 new emails, 8 resends", 11.5, MUTED))
    y = 110
    for label, value, share, c, fg in [("no cache", without_c, 1.0, MUTED, "#ffffff"),
                                        ("with cache", with_c, with_c / without_c, GREEN, "#ffffff")]:
        o.append(text(36, y + 14, label, 12, INK))
        o.append(rect(36, y + 22, 300, 30, fill=ROWALT, stroke=RULE, rx=4))
        o.append(rect(36, y + 22, 300 * share, 30, fill=c, stroke=c, rx=4))
        o.append(text(46, y + 42, f"₹{value:.2f}", 12, fg, "bold"))
        y += 66
    o.append(text(36, y + 16, f"hit rate {cache.hit_rate():.0%}, {1 - with_c / without_c:.0%} of the cost saved:", 12, INK, "bold"))
    o.append(text(36, y + 34, "a cache saves only what repeats.", 12, INK))
    # right panel
    o.append(rect(380, 48, 340, 250, fill="#fff", stroke=ACC, sw=1.6, rx=8))
    o.append(text(396, 74, "Fallback, provider failing 20% of calls", 12.5, ACC, "bold"))
    o.append(text(396, 92, "60 golden-set emails", 11.5, MUTED))
    y = 110
    for label, key, c in [("pinned model", "primary", GREEN), ("cheaper fallback", "fallback", ACC),
                          ("failed: to a person", "failed", RED)]:
        cnt = routes[key]
        o.append(text(396, y + 14, label, 12, INK))
        o.append(rect(396, y + 22, 250, 22, fill=ROWALT, stroke=RULE, rx=4))
        o.append(rect(396, y + 22, 250 * cnt / 60, 22, fill=c, stroke=c, rx=4))
        o.append(text(656, y + 38, f"{cnt} of 60", 12, INK, "bold"))
        y += 50
    served = (routes["primary"] + routes["fallback"]) / 60
    o.append(text(396, y + 16, f"{served:.0%} served, through {errors}", 12, INK, "bold"))
    o.append(text(396, y + 34, "provider errors.", 12, INK, "bold"))
    return svg(W, 312, "".join(o))


def fig_drift():
    from assistant import SupportAssistant
    from questions_stream import build
    a, stream = SupportAssistant(), build()
    weeks = list(range(1, 9)); refusal = []; conf = []
    for w in weeks:
        res = [a.answer(q["question"]) for q in stream if q["week"] == w]
        refusal.append(sum(1 for r in res if not r["grounded"]) / len(res))
        conf.append(sum(r["score"] for r in res) / len(res))
    o = [text(20, 28, "Monitoring a system with no accuracy", 15, INK, "bold", family=HEAD)]
    x0, x1 = 90, 700
    def px(w): return x0 + 28 + (w - 1) * (x1 - x0 - 40) / 7
    def panel(top, h, title, vals, lo, hi, ticks, fmt, colour, marker_sq):
        o.append(text(20, top - 10, title, 12.5, colour, "bold"))
        def py(v): return top + h - (v - lo) / (hi - lo) * h
        for t in ticks:
            o.append(path(f"M{x0},{py(t)} H{x1}", stroke=RULE, sw=0.7, dash="3,4"))
            o.append(text(x0 - 8, py(t) + 4, fmt(t), 11, MUTED, anchor="end"))
        o.append(path("M" + " L".join(f"{px(w)},{py(v)}" for w, v in zip(weeks, vals)), stroke=colour, sw=2.2))
        for w, v in zip(weeks, vals):
            if marker_sq:
                o.append(rect(px(w) - 4, py(v) - 4, 8, 8, fill=colour, stroke="#fff", sw=1.5))
            else:
                o.append(f'<circle cx="{px(w)}" cy="{py(v)}" r="4.5" fill="{colour}" stroke="#fff" stroke-width="1.5"/>')
            o.append(text(px(w), py(v) - 9, fmt(v), 11, INK, anchor="middle"))
        return top + h
    b1 = panel(70, 120, "Refusal rate (share of questions refused)", refusal, 0, 0.5,
               [0, 0.25, 0.5], lambda v: f"{v:.0%}", ORANGE, True)
    b2 = panel(b1 + 56, 90, "Mean retrieval confidence (0 to 1)", conf, 0.4, 0.65,
               [0.4, 0.5, 0.6], lambda v: f"{v:.2f}", PURPLE, False)
    for w in weeks:
        o.append(text(px(w), b2 + 20, f"week {w}", 11, MUTED, anchor="middle"))
    o.append(path(f"M{px(5) - 20},{64} V{b2 + 6}", stroke=RED, sw=1.4, dash="5,4"))
    o.append(text(px(5) - 12, b1 + 18, "week 5: questions about", 11.5, RED, "bold"))
    o.append(text(px(5) - 12, b1 + 33, "a new product line begin", 11.5, RED, "bold"))
    o.append(text(20, b2 + 48, "Same prompt, same model, same code. Customers started asking about something", 12, INK))
    o.append(text(20, b2 + 66, "nobody had written down. The fix is three documents, not a model change.", 12, INK))
    return svg(W, b2 + 80, "".join(o))


if __name__ == "__main__":
    os.chdir(HERE)
    for name, fn in [("fig57-1-provider-upgrade.svg", fig_upgrade), ("fig57-2-cost-and-failure.svg", fig_resilience),
                     ("fig57-3-topic-drift.svg", fig_drift)]:
        open(name, "w").write(fn())
    print("ok57")
