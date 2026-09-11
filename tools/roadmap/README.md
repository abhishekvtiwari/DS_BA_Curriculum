# Pathway roadmap generator

Builds an interactive roadmap of both pathways from the module contracts.

```
python tools/roadmap/build_roadmap.py          # write output/roadmap/curriculum-roadmap.html
python tools/roadmap/build_roadmap.py --check  # reconcile counts, write nothing
```

## What it is, and what it is not

The **contracts are the source of truth.** This generator reads them and injects the
module / chapter / controlled-topic tree into `roadmap-template.html`. The page it writes is a
generated view and is **not authoritative material** under authoring policy 1.9, which is why it lands
in `output/` (untracked) rather than in the controlled tree. Nothing here changes a curriculum ID,
a contract, a count, or an authoring status.

Only two files are controlled: this README, `build_roadmap.py`, and `roadmap-template.html`. Delete the
built page whenever you like; rerun the command to get it back.

## What the page shows

Each pathway is drawn as a route the reader walks end to end, laid out serpentine so it uses the page
width instead of running as one long line. The route turns back on itself at each row, and the line is
drawn in the gutters between cards so the cards read as stations sitting on it rather than hiding it.

The two pathways are **independent**. The page never combines or compares them, and carries no
cross-track links.

| Encoding | Meaning |
|---|---|
| Route order | Prerequisite order, from each contract's own `prerequisite_modules` chain |
| Stop colour | The module's position in its pathway — DS runs a cool spectrum, BA a warm one |
| Ticks | One per chapter on that stop; selecting a tick opens its controlled topics |

Contract status and authoring state are deliberately **not** shown. The page is scope, not progress.

## Colour

Hue is stepped along the pathway. Lightness is solved per hue rather than fixed, because a single HSL
lightness does not give even perceived weight — cyan reads far brighter than violet at the same value.
Two colours are derived per module:

- a **graphic** colour, vivid, held at 3:1 or better against the page ground
- an **ink** colour, darker or lighter as the theme needs, held at 4.5:1 or better against the panel

Vividness leads and contrast only clamps. Solving instead for the minimum qualifying lightness produces
muddy browns across the warm hues.

## After changing the template

The page is a single HTML file with inline CSS and JS and no build step, so a syntax error anywhere in
the script leaves a blank page that still passes every static check. **Render it before trusting it.**
A headless check is enough:

```python
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page()
    errs = []; pg.on('pageerror', lambda e: errs.append(str(e)))
    pg.goto('file:///.../output/roadmap/curriculum-roadmap.html'); pg.wait_for_timeout(1500)
    print(errs or 'none', pg.eval_on_selector_all('.stop', 'n=>n.length'))
```

Expect no errors, 18 stops on DS and 15 on BA, 96 and 75 ticks.

## Opening the template directly

`roadmap-template.html` is not a viewable page — it holds an empty data placeholder until the build
injects the contracts. Opened raw it now says so and prints the build command, rather than rendering a
header over an empty space. The page to open is always `output/roadmap/curriculum-roadmap.html`.

All counts on the page are derived from the injected data. Nothing is hand-typed, so the figures cannot
drift from the contracts.
