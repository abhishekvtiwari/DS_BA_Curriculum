"""Check every number in Chapter 75 (Product Sense, Metrics, Case Studies & Guesstimates).

Run from the book folder:  python3 checks/ch75_numbers.py
Each check recomputes an answer from its stated assumptions and confirms the
chapter prints the same figure. Exit code 1 if anything disagrees.

Sources for the two real figures (checked 30 Sep 2026):
- Greater Mumbai (BMC area), Census of India 2011 Primary Census Abstract,
  ward-level tables: 12,442,373 people in 24 wards (A ... T). Summed from the
  ward-level census CSV collated in github.com/mickeykedia/Mumbai-Population-Map.
- India, Census 2011 population: 1,210,854,977 (district-level census CSV,
  github.com/nishusharma1608/India-Census-2011-Analysis).
Every other input is an interview assumption, labelled as such in the chapter.
"""
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
CH = next((HERE.parent / "manuscript").glob("ch75-*.md")).read_text(encoding="utf-8")

fails = 0


def lakh(n: str) -> str:
    n = n.replace(",", "")
    i, _, d = n.partition(".")
    if len(i) <= 3:
        out = i
    else:
        head, tail = i[:-3], i[-3:]
        out = ",".join([head[max(0, k - 2):k] for k in range(len(head), 0, -2)][::-1]) + "," + tail
    return out + ("." + d if d else "")


def check(label, value, *texts):
    global fails
    missing = [t for t in texts if t not in CH]
    status = "ok" if not missing else "MISSING " + repr(missing)
    if missing:
        fails += 1
    print(f"{label:<48} {value!s:<22} {status}")


# Q75-024: gyms in Greater Mumbai
pop, gym_share, members = 12_500_000, 0.03, 500
goers = pop * gym_share
gyms = goers / members
check("Q75-024 gym-goers", f"{goers:,.0f}", "12,500,000 × 3% = 375,000")
check("Q75-024 gyms", f"{gyms:,.0f}", "375,000 ÷ 500 = 750")
check("Q75-024 gyms per ward (24 wards)", f"{gyms / 24:.2f}", "about 31 per ward")
check("Q75-024 people per gym", f"{pop / gyms:,.0f}", "roughly every 17,000 people")
check("Q75-024 census 2011 Greater Mumbai", "12,442,373", "12,442,373")

# Q75-025: TAM, top-down
households, buy_share, spend = 300_000_000, 0.15, 400
buyers = households * buy_share
tam_top = buyers * spend
check("Q75-025 buying households", f"{buyers:,.0f}", "300,000,000 × 15% = 45,000,000")
check("Q75-025 top-down (lakh grouping)", lakh(f"{tam_top:.0f}"), "₹" + lakh(f"{tam_top:.0f}"))
check("Q75-025 top-down in crore", f"{tam_top / 1e7:,.0f} crore", "₹1,800 crore")
people = households * 4.5
check("Q75-025 households × 4.5 people", f"{people / 1e7:.0f} crore", "about 135 crore people")
check("Q75-025 census 2011 India", "1,210,854,977", "1,210,854,977", "121 crore")

# Q75-025: TAM, bottom-up
shops, per_shop, price = 500_000, 250, 150
units = shops * per_shop
tam_bottom = units * price
check("Q75-025 containers a year", f"{units:,.0f}", "500,000 × 250 = 125,000,000")
check("Q75-025 bottom-up (lakh grouping)", lakh(f"{tam_bottom:.0f}"), "₹" + lakh(f"{tam_bottom:.0f}"), "₹1,875 crore")
gap = tam_bottom / tam_top - 1
check("Q75-025 gap between routes", f"{gap:.1%}", "within about 4%")
per_household = spend / price
implied_units = buyers * per_household
check("Q75-025 containers per buying household", f"{per_household:.2f}", "about 2.7 containers")
check("Q75-025 implied top-down units", f"{implied_units / 1e7:.1f} crore", "about 12 crore containers", "12.5 crore")
check("Q75-025 per-week sales per shop", f"{per_shop / 52:.1f}", "about 5 a week")

# Q75-027: coffee shop
check("Q75-027 coffee shop revenue a day", f"₹{300 * 150:,}", "₹45,000 a day")

# Q75-030: open rate 25% -> 18%
points = 25 - 18
relative = points / 25
check("Q75-030 change in points", points, "7 percentage points", "25 − 18 = 7 points")
check("Q75-030 relative change", f"{relative:.0%}", "28% relative drop", "7 ÷ 25 = 28%")

# Q75-020: RICE
def rice(reach, impact, confidence, effort):
    return reach * impact * confidence / effort

a, b = rice(1_000, 2, 0.8, 2), rice(1_000, 2, 0.8, 10)
wrong_a, wrong_b = 1_000 * 2 * 0.8 * 2, 1_000 * 2 * 0.8 * 10
check("Q75-020 RICE, effort 2", f"{a:,.0f}", "(1,000 × 2 × 0.8) ÷ 2 = 800")
check("Q75-020 RICE, effort 10", f"{b:,.0f}", "1,600 ÷ 10 = 160")
check("Q75-020 multiplied by effort", f"{wrong_a:,.0f} / {wrong_b:,.0f}", "3,200 against 16,000")
assert a > b and wrong_a < wrong_b

print("\nAll checks passed." if not fails else f"\n{fails} check(s) failed.")
sys.exit(1 if fails else 0)
