"""
Analyst to Architect · Riverstone CRM dataset (first used in Chapter 36; reused in Chapters 37, 39, 44)
generate_riverstone_crm.py: builds Riverstone's full CRM export, every enquiry from 2023 to 2025.

Run:     python3 generate_riverstone_crm.py            (writes into companion/crm/)
Writes:  crm/leads.csv, crm/activities.csv, crm/stage_history.csv
Seed:    20236 (the same seed always produces the same files)
Tested:  Python 3.12.3, NumPy 2.4.4, pandas 3.0.2 (17 September 2026)
Spec:    planning/data/riverstone-crm.md (tables, columns, planted signal, planted messiness, leakage traps)

Riverstone Supplies is fictional; every name, email and number is invented.
"""
import pathlib
import numpy as np
import pandas as pd

rng = np.random.default_rng(20236)
OUT = pathlib.Path(__file__).resolve().parent / "crm"
OUT.mkdir(exist_ok=True)
EXPORT_DATE = pd.Timestamp("2025-12-31 23:59")

# ---------------- people (same reps as the one-year database) ----------------
REPS = {3: "Neha Kulkarni", 4: "Rahul Mehta", 5: "Farah Khan", 9: "Inside Sales Desk"}

# ---------------- lead volume by month ----------------
months = pd.date_range("2023-01-01", "2025-12-01", freq="MS")
season = {1: 1.0, 2: 0.95, 3: 1.05, 4: 1.0, 5: 0.95, 6: 0.8, 7: 0.75, 8: 0.95, 9: 1.1, 10: 1.35, 11: 1.25, 12: 0.9}
growth = {2023: 280, 2024: 330, 2025: 390}           # average new enquiries per month
rows = []
for m in months:
    n = rng.poisson(growth[m.year] * season[m.month])
    days = rng.integers(0, m.days_in_month, n)
    secs = rng.integers(8 * 3600, 20 * 3600, n)
    for d, s in zip(days, secs):
        rows.append(m + pd.Timedelta(days=int(d), seconds=int(s)))
created = pd.Series(sorted(rows))
N = len(created)
year = created.dt.year.to_numpy(); month = created.dt.month.to_numpy()

# ---------------- lead attributes ----------------
def pick(options, probs, size):
    return rng.choice(options, size=size, p=np.array(probs) / np.sum(probs))

src_names = ["Marketplace", "Website", "Trade fair", "Referral", "Cold call", "Partner"]
source = np.empty(N, dtype=object)
for y, probs in {2023: [30, 30, 10, 12, 10, 8], 2024: [36, 28, 9, 11, 9, 7], 2025: [48, 24, 7, 9, 7, 5]}.items():
    idx = np.where(year == y)[0]
    source[idx] = pick(src_names, probs, len(idx))
tradefair_month = np.isin(month, [2, 9])                        # the two trade fairs Riverstone attends
source[tradefair_month & (rng.random(N) < 0.18)] = "Trade fair"

segment = pick(["Retail", "Hospitality", "Wholesale"], [45, 35, 20], N).astype(object)
size_band = pick(["1-10", "11-50", "51-200", "200+"], [38, 34, 19, 9], N).astype(object)
size_band[segment == "Wholesale"] = pick(["1-10", "11-50", "51-200", "200+"], [15, 35, 32, 18], (segment == "Wholesale").sum())
interest = pick(["Storage", "Kitchen", "Industrial", "Furniture"], [36, 34, 18, 12], N).astype(object)
interest[(segment == "Wholesale") & (rng.random(N) < 0.45)] = "Industrial"
interest[(segment == "Hospitality") & (rng.random(N) < 0.35)] = "Kitchen"
size_mult = pd.Series(size_band).map({"1-10": 0.5, "11-50": 1.0, "51-200": 2.2, "200+": 4.5}).to_numpy()
est_qty = np.round(rng.lognormal(mean=np.log(120), sigma=1.0, size=N) * size_mult).astype(float)
visits = rng.poisson(np.where(source == "Website", 3.0, 1.2))
cities = ["Mumbai", "Pune", "Delhi", "Bengaluru", "Ahmedabad", "Chennai", "Hyderabad", "Kolkata", "Jaipur", "Surat",
          "Nagpur", "Indore", "Kochi", "Lucknow", "Nashik", "Goa", "Udaipur"]
city = pick(cities, [16, 11, 11, 9, 7, 6, 6, 5, 4, 4, 3, 3, 3, 3, 3, 3, 3], N).astype(object)
free_mail = rng.random(N) < np.where(np.isin(source, ["Marketplace", "Website"]), 0.55, 0.25)

phrases_good = ["need bulk quantity", "tender requirement", "urgent requirement", "monthly supply needed", "for our new outlet"]
phrases_weak = ["send price list", "sample only", "just checking rates", "want catalogue", "price please"]
phrases_neutral = ["interested in your products", "please call back", "need quotation", "details required", "enquiry"]
text_kind = pick(["good", "weak", "neutral"], [22, 30, 48], N)
product_word = pd.Series(interest).map({"Storage": "storage boxes", "Kitchen": "food containers",
                                        "Industrial": "industrial crates", "Furniture": "garden chairs"}).to_numpy()
enquiry_text = np.array([
    f"{rng.choice(phrases_good if k == 'good' else phrases_weak if k == 'weak' else phrases_neutral)} - {w}"
    for k, w in zip(text_kind, product_word)], dtype=object)

# ---------------- planted signal: probability of being won within 90 days ----------------
logit = np.full(N, -3.05)
logit += pd.Series(source).map({"Marketplace": -0.75, "Website": 0.0, "Trade fair": 0.85, "Referral": 1.35,
                                "Cold call": 0.25, "Partner": 0.6}).to_numpy()
logit += np.where((source == "Marketplace") & (year == 2025), -0.45, 0.0)     # 2025 marketplace plan brought weaker leads
logit += pd.Series(segment).map({"Retail": 0.0, "Hospitality": 0.1, "Wholesale": 0.45}).to_numpy()
logit += np.where((segment == "Hospitality") & np.isin(month, [8, 9, 10]), 0.35, 0.0)
logit += pd.Series(size_band).map({"1-10": -0.45, "11-50": 0.0, "51-200": 0.3, "200+": 0.55}).to_numpy()
logit += 0.3 * (np.log(est_qty) - np.log(120))
logit += 0.12 * np.minimum(visits, 6)
logit += np.where(free_mail, -0.5, 0.0)
logit += pd.Series(text_kind).map({"good": 0.6, "weak": -0.55, "neutral": 0.0}).to_numpy()
owner = np.where(np.isin(source, ["Marketplace", "Website"]) & (rng.random(N) < 0.6), 9,
                 rng.choice([3, 4, 5], size=N))
logit += np.where(owner == 9, -0.2, 0.0)
p_true = 1 / (1 + np.exp(-logit))
won = rng.random(N) < p_true

# ---------------- process: response, activities, stages (this is where leakage lives) ----------------
quality = logit + rng.normal(0, 0.7, N)                  # what reps "sense" about a lead
resp_mean_h = np.exp(2.2 - 0.45 * (quality - quality.mean())) * np.where(owner == 9, 2.2, 1.0)
first_response_hours = np.round(rng.exponential(resp_mean_h) + 0.2, 1)
never_contacted = (rng.random(N) < 0.12 * np.where(won, 0.05, 1.0))
first_response_hours[never_contacted] = np.nan

stage_rows = []; act_rows = []; quote_sent = np.full(N, np.datetime64("NaT"), dtype="datetime64[ns]"); closed_at = np.full(N, np.datetime64("NaT"), dtype="datetime64[ns]")
aid = 1
for i in range(N):
    t0 = created.iloc[i]; lid = 100001 + i
    stage_rows.append((lid, "New", t0))
    if never_contacted[i]:
        closed = t0 + pd.Timedelta(days=90)
        stage_rows.append((lid, "Lost", closed)); closed_at[i] = closed
        continue
    t = t0 + pd.Timedelta(hours=float(first_response_hours[i]))
    stage_rows.append((lid, "Contacted", t))
    act_rows.append((aid, lid, t, rng.choice(["Call", "Email"], p=[0.6, 0.4]))); aid += 1
    qualified = won[i] or rng.random() < 0.28
    n_extra = rng.poisson(3.2 if won[i] else 1.1)
    horizon = 60 if won[i] else 85
    times = sorted(t + pd.Timedelta(hours=float(h)) for h in rng.uniform(2, horizon * 24, n_extra))
    for tt in times:
        act_rows.append((aid, lid, tt, rng.choice(["Call", "Email", "Meeting", "Sample sent"], p=[0.4, 0.35, 0.15, 0.10]))); aid += 1
    if qualified:
        tq = t + pd.Timedelta(days=float(rng.uniform(1, 20)))
        stage_rows.append((lid, "Qualified", tq))
        if won[i] or rng.random() < 0.45:
            tqs = tq + pd.Timedelta(days=float(rng.uniform(1, 15)))
            quote_sent[i] = tqs.to_datetime64()
            stage_rows.append((lid, "Quote sent", tqs))
            act_rows.append((aid, lid, tqs, "Quote sent")); aid += 1
    if won[i]:
        closed = t0 + pd.Timedelta(days=float(rng.uniform(12, 88)))
        stage_rows.append((lid, "Won", closed))
    else:
        closed = t0 + pd.Timedelta(days=float(rng.uniform(20, 90))) if rng.random() < 0.55 else t0 + pd.Timedelta(days=90)
        stage_rows.append((lid, "Lost", closed))
    closed_at[i] = closed.to_datetime64()

lead_id = np.arange(100001, 100001 + N)
still_open = pd.to_datetime(closed_at) > EXPORT_DATE
companies_a = ["Shree", "Metro", "Royal", "Green", "Sunrise", "Coastal", "Prime", "City", "Golden", "Everest", "Lotus", "Kaveri",
               "Silver", "Sagar", "Ganesh", "New India", "Classic", "Om", "Star", "Heritage"]
companies_b = {"Retail": ["Stores", "Mart", "Traders", "Hardware", "Kitchenware"], "Hospitality": ["Hotels", "Caterers", "Restaurants", "Cafe", "Banquets"],
               "Wholesale": ["Distributors", "Wholesale", "Packaging", "Logistics", "Agencies"]}
company = np.array([f"{rng.choice(companies_a)} {rng.choice(companies_b[s])}" for s in segment], dtype=object)
slug = [c.lower().replace(" ", "") for c in company]
email = np.array([f"{s}{rng.integers(1, 999)}@{'gmail.com' if fm else s + '.in'}" for s, fm in zip(slug, free_mail)], dtype=object)

leads = pd.DataFrame({
    "lead_id": lead_id, "created_at": created.dt.strftime("%Y-%m-%d %H:%M:%S"), "company_name": company, "email": email,
    "source": source, "segment": segment, "city": city, "company_size": size_band, "product_interest": interest,
    "est_quantity": est_qty, "website_visits": visits, "enquiry_text": enquiry_text, "owner_id": owner,
    "first_response_hours": first_response_hours,
    "quote_sent_date": pd.to_datetime(quote_sent).strftime("%Y-%m-%d"),
    "days_in_pipeline": np.round((pd.to_datetime(closed_at) - created.to_numpy()).days.to_numpy(), 0),
    "status": np.where(still_open, "Open", np.where(won, "Won", "Lost")),
})
# records not yet closed at export: no close information exists yet
leads.loc[still_open, "days_in_pipeline"] = np.nan
leads.loc[leads["quote_sent_date"].isna() | (pd.to_datetime(leads["quote_sent_date"]) > EXPORT_DATE), "quote_sent_date"] = np.nan

# ---------------- planted messiness ----------------
m = rng.random(N)
spell = {"Mumbai": ["Bombay", "mumbai", "MUMBAI ", "Mumbai."], "Bengaluru": ["Bangalore", "bengaluru", "B'lore"],
         "Delhi": ["New Delhi", "delhi", "Delhi NCR"], "Pune": ["pune", "Poona"], "Chennai": ["Madras", "chennai"],
         "Kolkata": ["Calcutta", "kolkata"], "Goa": ["Panaji", "GOA"]}
for i in np.where(m < 0.09)[0]:
    c = leads.at[i, "city"]
    if c in spell: leads.at[i, "city"] = rng.choice(spell[c])
leads.loc[rng.random(N) < 0.21, "company_size"] = np.nan
leads.loc[rng.random(N) < np.where(leads["source"] == "Marketplace", 0.28, 0.07), "est_quantity"] = np.nan   # marketplace forms often skip quantity
typo = (rng.random(N) < 0.006) & leads["est_quantity"].notna()
leads.loc[typo, "est_quantity"] = leads.loc[typo, "est_quantity"] * 1000
leads.loc[rng.random(N) < 0.05, "segment"] = np.nan
leads.loc[rng.random(N) < 0.04, "email"] = leads["email"].str.upper()

# duplicate web-form resubmissions: same enquiry again within 2 days, recorded as a new lead with no outcome of its own
dup_src = leads[(leads["source"] == "Website") & (rng.random(N) < 0.08)].copy()
dup_src["created_at"] = (pd.to_datetime(dup_src["created_at"]) + pd.to_timedelta(rng.integers(10, 2880, len(dup_src)), unit="m")).dt.strftime("%Y-%m-%d %H:%M:%S")
for col in ["first_response_hours", "quote_sent_date", "days_in_pipeline"]:
    dup_src[col] = np.nan
dup_src["status"] = "Lost"
dup_src["lead_id"] = np.arange(200001, 200001 + len(dup_src))
leads = pd.concat([leads, dup_src]).sort_values("created_at").reset_index(drop=True)

activities = pd.DataFrame(act_rows, columns=["activity_id", "lead_id", "activity_at", "activity_type"])
late = rng.random(len(activities)) < 0.10                        # some reps log activities days later
activities["logged_at"] = activities["activity_at"] + pd.to_timedelta(np.where(late, rng.uniform(1, 6, len(activities)), rng.uniform(0, 0.05, len(activities))), unit="D")
activities = activities[activities["activity_at"] <= EXPORT_DATE]
for col in ["activity_at", "logged_at"]:
    activities[col] = activities[col].dt.strftime("%Y-%m-%d %H:%M:%S")
stages = pd.DataFrame(stage_rows, columns=["lead_id", "stage", "entered_at"])
stages = stages[stages["entered_at"] <= EXPORT_DATE].copy()
stages["entered_at"] = stages["entered_at"].dt.strftime("%Y-%m-%d %H:%M:%S")

leads.to_csv(OUT / "leads.csv", index=False)
activities.to_csv(OUT / "activities.csv", index=False)
stages.to_csv(OUT / "stage_history.csv", index=False)
print(f"{len(leads):,} lead rows ({len(dup_src)} duplicates) · {len(activities):,} activities · {len(stages):,} stage rows")
