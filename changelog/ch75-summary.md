# Chapter 75 summary: Product Sense, Metrics, Case Studies & Guesstimates

**Rows:** 24 content rows (75.1–75.24) and V75.5 fixed; V75.1–V75.4, V75.6–V75.10 were already done by the style pass and are still clean; RJ-S3-57's Ch 75 part done. Nothing skipped.

## What changed
- **Pointers that teach.** Every question's "Learn it in" now names the section that teaches the idea (Ch 3, 4, 5, 15, 16, 22, 23, 24, 25, 30, 31), with "Practise it with" for bank pointers (Ch 69 moves, Ch 70 §70.8 and Q70-063, Ch 73). Broken pointers fixed: Ch 44's "revenue tree" → Ch 23 §23.10–23.11; §70.10 → Ch 16 §16.2; §70.7 → §70.8; Bayes (Ch 73 §73.1) → Ch 4 §4.9. Each heading checked against the current file.
- **Wrong answers corrected:** RICE divides by effort (worked example, "Beyond the book" note tied to Ch 25's ranking score); Q75-011 splits order count into customers × frequency; North Star matches Ch 23 §23.10; revenue growth can be price-driven; AHT paired with repeat-contact rate.
- **Guesstimates:** the gym chain now uses one geography (Greater Mumbai, census 2011: 12,442,373 people, 24 wards) → 750 gyms, about 31 per ward. The TAM is ₹18,00,00,00,000 = ₹1,800 crore, with a real bottom-up estimate from the supply side (₹1,875 crore), compared in rupees and units. All other inputs are labelled as interview assumptions.
- **Format:** Chapter at a glance (Before you start, Time needed, How this chapter is built, Levels and roles); Level (Fresher/Mid/Senior) and roles (DA, BA, PA, BI) on every question; Ch 69's twelve `[+Tag]`s; "Passes" rows rewritten as ~2-score answers; §75.6 renamed "Full cases, talked through live"; drafting notes removed; the real-world candidate is now Kabir (no clash with Karan in Ch 28, 72, 72A); Where this leads names 76A and 76B.

## Option picks
- 75.9: option (a), Greater Mumbai (BMC area). 75.23: a distinct name (Kabir). 75.19: Ch 70's Fresher/Mid/Senior scale (the bank format recorded in NOTES), not Easy/Medium/Hard; the optional move of §75.5 not done (the glance points first-job readers to §75.5 after §75.1).

## Time needed (new)
2½–3½ hours to read and drill once, out loud; 2–3 hours more for the project. (There was none before.)

## Verification
- No code blocks (check_code_teaching: 0 blocks). `checks/ch75_numbers.py` recomputes all 22 numeric claims (gyms, TAM both routes, lakh grouping, crore, units cross-check, coffee shop, open-rate points and relative change, RICE both ways) and confirms each appears in the text: all pass.
- Build: 19 pages; layout_check clean (map numbers 9/9, no stranded heads or lead-ins, no sparse pages, no small text, tofu 0); prescan clean (three line-end breaks at real hyphens); restructure --check "already in order"; no figures.

## Sources (T13)
Greater Mumbai 2011 population and wards: Census of India 2011 Primary Census Abstract, ward-level tables (collated CSV, github.com/mickeykedia/Mumbai-Population-Map), checked 30 Sep 2026. India 2011 population 1,210,854,977: district-level census CSV (github.com/nishusharma1608/India-Census-2011-Analysis), checked 30 Sep 2026. Government sites (censusindia.gov.in, pib.gov.in) are blocked by the proxy, so the household count stays an assumption, and the text says so.
