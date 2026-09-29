#!/usr/bin/env python3
"""
Analyst to Architect · Chapter 56 · MLOps: Making Models Survive Production
File: simulate_production.py - six months of Riverstone's moulding line, week by week.
What: writes production_data/stream.npz holding, for 24 weeks of 500 parts each:
        features  (12000 x 108)  the same convolution features Chapter 53's model was trained on
        labels    (12000,)       1 = defective
        week      (12000,)       0 to 23
        brightness(12000,)       the mean pixel value of each image, the cheapest input monitor there is
        kind      (12000,)       good, scratch, void, short_shot, or flash
      What happens to the line, which is what the chapter detects rather than assumes:
        weeks 0-7    nothing changes. This is the baseline the model was trained for.
        weeks 8-15   the overhead lamps are replaced and the belt slowly looks brighter (input drift).
        weeks 16-23  a new mould starts producing "flash": a thin protrusion at the part's edge that
                     nobody has ever labelled, so the model has never seen it (concept drift).
How:  python3 simulate_production.py [--weeks 24] [--per-week 500]
Seed: 56 (fixed). NumPy only; no downloads, no GPU. Takes about two minutes.
Tested on: Python 3.11.15, numpy 2.4.6 (Ubuntu 24.04).
Riverstone Supplies is fictional; these images are generated, not photographs.
"""
import argparse
import os
import numpy as np

ap = argparse.ArgumentParser()
ap.add_argument('--weeks', type=int, default=24)
ap.add_argument('--per-week', type=int, default=500)
ap.add_argument('--out', default='production_data')
a = ap.parse_args()
rng = np.random.default_rng(56)

SIZE = 32
yy, xx = np.mgrid[0:SIZE, 0:SIZE]
KERNELS = [np.array([[-1, -1, -1], [-1, 8, -1], [-1, -1, -1]], dtype=float) / 8,
           np.array([[-1, -2, -1], [0, 0, 0], [1, 2, 1]], dtype=float) / 4,
           np.array([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]], dtype=float) / 4]


def blank_part(belt: float):
    """A good part. `belt` is the background brightness, which is what the new lamps change."""
    image = np.full((SIZE, SIZE), belt, dtype=np.float32)
    centre_y, centre_x = rng.normal(16, 0.8, 2)
    radius = rng.normal(11.5, 0.4)
    disc = (yy - centre_y) ** 2 + (xx - centre_x) ** 2 <= radius ** 2
    image[disc] = rng.normal(0.72, 0.03)
    ring = np.abs(np.sqrt((yy - centre_y) ** 2 + (xx - centre_x) ** 2) - radius * 0.62) < 0.9
    image[ring] -= 0.10
    image += rng.normal(0, 0.025, image.shape)
    lighting = np.linspace(rng.uniform(-0.05, 0.05), rng.uniform(-0.05, 0.05), SIZE)
    return np.clip(image + lighting[None, :], 0, 1).astype(np.float32), (centre_y, centre_x, radius)


def add_scratch(image, cy, cx, r):
    angle, length = rng.uniform(0, np.pi), rng.uniform(r * 0.8, r * 1.4)
    for t in np.linspace(-length / 2, length / 2, 40):
        y, x = int(round(cy + t * np.sin(angle))), int(round(cx + t * np.cos(angle)))
        if 0 <= y < SIZE and 0 <= x < SIZE:
            image[y, x] = min(1.0, image[y, x] + rng.uniform(0.18, 0.28))


def add_void(image, cy, cx, r):
    vy, vx = cy + rng.uniform(-r * 0.5, r * 0.5), cx + rng.uniform(-r * 0.5, r * 0.5)
    hole = (yy - vy) ** 2 + (xx - vx) ** 2 <= rng.uniform(1.6, 2.8) ** 2
    image[hole] = np.clip(image[hole] - rng.uniform(0.30, 0.42), 0, 1)


def add_short_shot(image, cy, cx, r, belt):
    angle = rng.uniform(0, 2 * np.pi)
    by, bx = cy + r * 0.85 * np.sin(angle), cx + r * 0.85 * np.cos(angle)
    bite = (yy - by) ** 2 + (xx - bx) ** 2 <= rng.uniform(3.0, 4.5) ** 2
    image[bite] = belt + rng.normal(0, 0.02, bite.sum())


def add_flash(image, cy, cx, r):
    """The new defect: a thin tail of plastic squeezed out at the edge. Faint, and never labelled."""
    angle = rng.uniform(0, 2 * np.pi)
    for t in np.linspace(r, r + rng.uniform(2.5, 4.0), 25):
        y, x = int(round(cy + t * np.sin(angle))), int(round(cx + t * np.cos(angle)))
        if 0 <= y < SIZE and 0 <= x < SIZE:
            image[y, x] = min(1.0, image[y, x] + rng.uniform(0.22, 0.34))


def convolve(image, kernel):
    kh, kw = kernel.shape
    out = np.zeros((image.shape[0] - kh + 1, image.shape[1] - kw + 1), dtype=np.float32)
    for i in range(out.shape[0]):
        for j in range(out.shape[1]):
            out[i, j] = np.sum(image[i:i + kh, j:j + kw] * kernel)
    return out


def features(image):
    """Chapter 53's features: three kernels, absolute response, max-pooled to 6x6 each."""
    maps = []
    for kernel in KERNELS:
        response = np.abs(convolve(image, kernel))
        maps.append(response[:30, :30].reshape(6, 5, 6, 5).max(axis=(1, 3)).ravel())
    return np.concatenate(maps)


rows, labels, weeks, brightness, kinds = [], [], [], [], []
for week in range(a.weeks):
    belt = 0.18 + (0.10 * (week - 7) / 8 if week >= 8 else 0.0)     # the lamps, replaced in week 8
    belt = min(belt, 0.28)
    flash_rate = 0.02 if week >= 16 else 0.0                        # the new mould, from week 16
    for _ in range(a.per_week):
        image, (cy, cx, r) = blank_part(belt)
        draw = rng.random()
        if draw < flash_rate:
            add_flash(image, cy, cx, r); label, kind = 1, 'flash'
        elif draw < flash_rate + 0.08:
            which = rng.choice(['scratch', 'void', 'short_shot'])
            {'scratch': lambda: add_scratch(image, cy, cx, r),
             'void': lambda: add_void(image, cy, cx, r),
             'short_shot': lambda: add_short_shot(image, cy, cx, r, belt)}[which]()
            label, kind = 1, which
        else:
            label, kind = 0, 'good'
        image = np.clip(image, 0, 1)
        rows.append(features(image)); labels.append(label); weeks.append(week)
        brightness.append(float(image.mean())); kinds.append(kind)

os.makedirs(a.out, exist_ok=True)
np.savez_compressed(f'{a.out}/stream.npz',
                    features=np.stack(rows).astype(np.float32), labels=np.array(labels, dtype=np.int8),
                    week=np.array(weeks, dtype=np.int16), brightness=np.array(brightness, dtype=np.float32),
                    kind=np.array(kinds))
print(f'{len(rows):,} parts over {a.weeks} weeks '
      f'({sum(labels):,} defective, of which {kinds.count("flash"):,} are the new flash defect)')
print(f'mean brightness: week 0 {np.mean([b for b, w in zip(brightness, weeks) if w == 0]):.3f}, '
      f'week 23 {np.mean([b for b, w in zip(brightness, weeks) if w == 23]):.3f}')
