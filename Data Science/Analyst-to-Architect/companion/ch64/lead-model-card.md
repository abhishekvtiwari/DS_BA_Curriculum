# Model card: lead score (the Chapter 64 stand-in)

Written by `build_ch64_files.py` (Chapter 64, section 64.8), in the format of Chapter 39, section 39.10.
The model is a simplified stand-in for the Part 4 lead-scoring model. The numbers are this run's real output.

| Field | Entry |
|---|---|
| Purpose | Rank new sales leads so reps call the likeliest wins first |
| Not for | Deciding whether a lead is contacted at all; pricing; credit decisions |
| Inputs | company_size_band, days_since_signup, industry (region is **not** an input) |
| Output | lead_score: predicted chance of winning the lead, in percent (0 to 100) |
| Training data | 1,778 leads from 2024 (a 75% sample); 592 held back for testing |
| Test AUC | 0.718 |
| Owner (business) | Anita Rao, Sales Head |
| Built by | Meera Iyer, analytics |
| Approved by | (a named person who did not build it; filled in at approval) |
| Version | stand-in, file models/lead_model_standin.joblib |

## Score by region, 2025 leads

| Region | Leads | Mean score |
|---|---:|---:|
| West | 620 | 29.0 |
| South | 540 | 26.9 |
| North | 410 | 21.8 |
| East | 260 | 15.0 |

## Known limits

- The score follows company size, and company size differs by region, so East leads score lower
  on average although region is not an input (section 64.7). Use it with the response-priority
  rule, not alone.
- Trained on 2024 leads only; re-check the regional gap every quarter.
