#!/usr/bin/env python3
"""
Analyst to Architect · Chapter 57 · eight weeks of questions arriving at the support assistant.
Weeks 1-4 are the questions the corpus was built for. From week 5 customers start asking about a new
product line nobody has written documentation for, which is the LLM equivalent of Chapter 56's new mould:
the inputs look like questions, the assistant looks healthy, and the answers quietly stop being useful.
Seed 57; standard library only.
"""
import json
import pathlib
import random

CH55 = pathlib.Path(__file__).resolve().parents[1] / 'ch55' / 'corpus'
NEW_TOPIC = [
    'Do you have the new stackable pallet in stock?',
    'What is the load rating of the pallet range?',
    'Can the pallets be exported to Sri Lanka?',
    'Is there a price list for the pallet range?',
    'What is the lead time on pallets?',
    'Are the pallets made from recycled material?',
    'Do pallets qualify for the bulk discount?',
    'What sizes do the new pallets come in?',
]


def build(weeks: int = 8, per_week: int = 40, seed: int = 57) -> list[dict]:
    rng = random.Random(seed)
    existing = [q['question'] for q in json.load(open(CH55 / 'questions.json', encoding='utf-8'))]
    stream = []
    for week in range(1, weeks + 1):
        new_share = 0.0 if week < 5 else min(0.35, 0.10 * (week - 4))
        for _ in range(per_week):
            if rng.random() < new_share:
                stream.append({'week': week, 'question': rng.choice(NEW_TOPIC), 'topic': 'new'})
            else:
                stream.append({'week': week, 'question': rng.choice(existing), 'topic': 'known'})
    return stream


if __name__ == '__main__':
    stream = build()
    for week in range(1, 9):
        rows = [q for q in stream if q['week'] == week]
        new = sum(1 for q in rows if q['topic'] == 'new')
        print(f'week {week}: {len(rows)} questions, {new} about the new product line')
