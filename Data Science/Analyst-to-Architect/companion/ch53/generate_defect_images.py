#!/usr/bin/env python3
"""
Analyst to Architect · Chapter 53 · Deep Learning in Depth
File: generate_defect_images.py - builds the molded-part images the chapter's vision project uses.
What: writes defect_data/images.npy (N x 32 x 32 float32, values 0-1) and defect_data/labels.npy
      (0 = good, 1 = defective), plus defect_data/defect_types.npy naming the defect on each image.
      Each image is a top-down view of a molded lid on a conveyor: a bright disc on a darker belt,
      with moulding noise. Defective parts carry one of three faults Riverstone's QC team sees:
        scratch      a thin bright line across the part
        void         a dark round hole in the surface
        short_shot   a bite missing from the edge, where the cavity did not fill
How:  python3 generate_defect_images.py [--n 6000] [--defect-rate 0.08]
Seed: 53 (fixed), so every reader's images, model and confusion matrix match the book's.
Tested on: Python 3.11, numpy 2.4.6 (September 2026). No downloads, no GPU.
Riverstone Supplies is fictional; these images are generated, not photographs.
"""
import argparse, os
import numpy as np

ap = argparse.ArgumentParser()
ap.add_argument('--n', type=int, default=6000)
ap.add_argument('--defect-rate', type=float, default=0.08)
ap.add_argument('--out', default='defect_data')
a = ap.parse_args()
rng = np.random.default_rng(53)
os.makedirs(a.out, exist_ok=True)

SIZE = 32
yy, xx = np.mgrid[0:SIZE, 0:SIZE]

def blank_part():
    """A good part: a bright disc on a darker belt, with a little lighting and moulding variation."""
    image = np.full((SIZE, SIZE), 0.18, dtype=np.float32)          # the conveyor belt
    centre_y, centre_x = rng.normal(16, 0.8, 2)
    radius = rng.normal(11.5, 0.4)
    disc = (yy - centre_y) ** 2 + (xx - centre_x) ** 2 <= radius ** 2
    image[disc] = rng.normal(0.72, 0.03)                           # the moulded lid
    ring = np.abs(np.sqrt((yy - centre_y) ** 2 + (xx - centre_x) ** 2) - radius * 0.62) < 0.9
    image[ring] -= 0.10                                            # the moulded rim
    image += rng.normal(0, 0.025, image.shape)                     # sensor noise
    lighting = np.linspace(rng.uniform(-0.05, 0.05), rng.uniform(-0.05, 0.05), SIZE)
    image += lighting[None, :]
    return np.clip(image, 0, 1).astype(np.float32), (centre_y, centre_x, radius)

def add_scratch(image, centre_y, centre_x, radius):
    angle = rng.uniform(0, np.pi)
    length = rng.uniform(radius * 0.8, radius * 1.4)
    for t in np.linspace(-length / 2, length / 2, 40):
        y = int(round(centre_y + t * np.sin(angle)))
        x = int(round(centre_x + t * np.cos(angle)))
        if 0 <= y < SIZE and 0 <= x < SIZE:
            image[y, x] = min(1.0, image[y, x] + rng.uniform(0.18, 0.28))

def add_void(image, centre_y, centre_x, radius):
    void_y = centre_y + rng.uniform(-radius * 0.5, radius * 0.5)
    void_x = centre_x + rng.uniform(-radius * 0.5, radius * 0.5)
    void_r = rng.uniform(1.6, 2.8)
    hole = (yy - void_y) ** 2 + (xx - void_x) ** 2 <= void_r ** 2
    image[hole] = np.clip(image[hole] - rng.uniform(0.30, 0.42), 0, 1)

def add_short_shot(image, centre_y, centre_x, radius):
    angle = rng.uniform(0, 2 * np.pi)
    bite_y = centre_y + radius * 0.85 * np.sin(angle)
    bite_x = centre_x + radius * 0.85 * np.cos(angle)
    bite_r = rng.uniform(3.0, 4.5)
    bite = (yy - bite_y) ** 2 + (xx - bite_x) ** 2 <= bite_r ** 2
    image[bite] = 0.18 + rng.normal(0, 0.02, bite.sum())           # belt shows through

DEFECTS = {'scratch': add_scratch, 'void': add_void, 'short_shot': add_short_shot}

images, labels, kinds = [], [], []
for _ in range(a.n):
    image, (cy, cx, r) = blank_part()
    if rng.random() < a.defect_rate:
        kind = rng.choice(list(DEFECTS))
        DEFECTS[kind](image, cy, cx, r)
        labels.append(1); kinds.append(kind)
    else:
        labels.append(0); kinds.append('good')
    images.append(np.clip(image, 0, 1))

images = np.stack(images).astype(np.float32)
labels = np.array(labels, dtype=np.int8)
kinds = np.array(kinds)
np.save(f'{a.out}/images.npy', images)
np.save(f'{a.out}/labels.npy', labels)
np.save(f'{a.out}/defect_types.npy', kinds)
counts = {k: int((kinds == k).sum()) for k in ['good', 'scratch', 'void', 'short_shot']}
print(f'{len(images):,} images of {SIZE}x{SIZE} pixels')
print(f'defective {int(labels.sum()):,} ({labels.mean():.1%}) · ' + ' · '.join(f'{k} {v}' for k, v in counts.items()))
print(f'wrote {a.out}/images.npy, {a.out}/labels.npy, {a.out}/defect_types.npy')
