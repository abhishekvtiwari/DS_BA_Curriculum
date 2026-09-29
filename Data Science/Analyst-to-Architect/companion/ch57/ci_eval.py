#!/usr/bin/env python3
"""ci_eval.py - the golden set as a build step. Exits non-zero if the feature regressed."""
import argparse
import sys

from pipeline import evaluate, parse, tolerant_parse

FLOOR = 0.70
parser = argparse.ArgumentParser()
parser.add_argument("--model", default="workhorse-001")
parser.add_argument("--parser", choices=["strict", "tolerant"], default="tolerant")
args = parser.parse_args()

result = evaluate("v3", model=args.model, parser=tolerant_parse if args.parser == "tolerant" else parse)
print(f"{args.model}, {args.parser} parser: {result['exact']}/{result['of']} ({result['accuracy']:.0%}), "
      f"unparseable {result['unparseable']}, floor {FLOOR:.0%}")
sys.exit(0 if result["accuracy"] >= FLOOR and result["unparseable"] == 0 else 1)
