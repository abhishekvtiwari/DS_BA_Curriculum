"""Ch 81: recompute every number the chapter states (no code in the chapter itself)."""
# Q81-001: Chapter 44's call list (section 44.4 output): value-ranked vs probability-only, 40 calls
by_value, by_prob = 1_200_524, 386_008
assert round(by_value / 1e5, 1) == 12.0 and round(by_prob / 1e5, 1) == 3.9
print(f"Q81-001: {by_value/1e5:.1f} lakh vs {by_prob/1e5:.1f} lakh, ratio {by_value/by_prob:.2f} (about three times)")

# Q81-006 / Q81-034: Chapter 73's sample-ratio mismatch, 5,340 control vs 4,660 treatment
from scipy.stats import chisquare
stat, p = chisquare([5340, 4660])
print(f"SRM: chi-square {stat:.2f}, p = {p:.1e}")

# Q81-012: illustrative duplicate count
print(f"Q81-012: 37 / 1,200 = {37/1200:.1%}")

# Q81-024: illustrative CTC breakup
parts = {"fixed": 510_000, "variable": 60_000, "employer PF": 21_600, "gratuity": 8_400}
assert sum(parts.values()) == 600_000
print(f"Q81-024: parts sum to {sum(parts.values()):,}; monthly fixed gross {parts['fixed']/12:,.0f}")
print(f"Q81-024: counter 5.6 lakh fixed is {560_000/parts['fixed']-1:.1%} above 5.1 lakh")
