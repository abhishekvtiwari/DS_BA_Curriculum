#!/usr/bin/env python3
"""
Analyst to Architect · Chapter 54 · Generative AI & Large Language Models
File: regression_test.py - fails (exit code 1) if extraction accuracy on the golden set drops below the floor.
How:  python regression_test.py                 (scores the WITH_EXAMPLE prompt)
      python regression_test.py --prompt NAIVE  (scores another prompt from extraction.py)
Riverstone Supplies is fictional; every name and number here is invented.
"""
import argparse
import sys

import extraction

GOLDEN = ["email_001", "email_002", "email_003", "email_004", "email_005",     # the first two emails
          "email_008", "email_010", "email_011", "email_012", "email_014"]     # of each of the five shapes
FLOOR = 0.70

parser = argparse.ArgumentParser()
parser.add_argument("--prompt", default="WITH_EXAMPLE", choices=["NAIVE", "INSTRUCTED", "WITH_EXAMPLE"])
args = parser.parse_args()

exact, fields, unparseable = extraction.evaluate(getattr(extraction, args.prompt), GOLDEN)
accuracy = exact / len(GOLDEN)
print(f"{args.prompt}: {exact} of {len(GOLDEN)} fully correct, accuracy {accuracy:.0%} "
      f"(floor {FLOOR:.0%}), unparseable {unparseable}")
sys.exit(0 if accuracy >= FLOOR and unparseable == 0 else 1)
