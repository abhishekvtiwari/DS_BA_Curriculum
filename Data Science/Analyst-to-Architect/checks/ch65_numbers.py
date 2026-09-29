"""Chapter 65: recompute every number the prose, tables, exercises and answers quote.

Run from the book folder: python3 checks/ch65_numbers.py
Reads companion/ch65/monthly_cost_model.csv (rebuild it first with build_ch65_files.py).
"""
import pathlib
import pandas as pd

BOOK = pathlib.Path(__file__).resolve().parent.parent
costs = pd.read_csv(BOOK / "companion/ch65/monthly_cost_model.csv")
unit_csv = pd.read_csv(BOOK / "companion/ch65/unit_economics.csv").set_index("metric")["value_inr"]
c = costs.set_index("component")["monthly_inr"]
total = costs["monthly_inr"].sum()
FX = 87
ok = True


def check(label, got, want, tol=0.5):
    global ok
    good = abs(got - want) <= tol
    ok &= good
    print(f"{'ok ' if good else 'BAD'} {label}: {got:,.4f} (text: {want:,})")


# Section 65.1 and the price sheet: reserved discounts, Multi-AZ
check("RDS 1-yr no upfront discount %", (1 - 0.162 / 0.253) * 100, 36, 0.5)
check("t3.large 1-yr no upfront discount %", (1 - 0.0564 / 0.0896) * 100, 37, 0.5)
check("RDS 3-yr all upfront discount %", (1 - 2606 / (3 * 8760) / 0.253) * 100, 61, 0.5)
check("t3.large 3-yr all upfront discount %", (1 - 865 / (3 * 8760) / 0.0896) * 100, 63, 0.5)
check("Multi-AZ / Single-AZ", 0.506 / 0.253, 2, 0)

# Section 65.2
check("by hand: 730 x 0.253 ($)", 730 * 0.253, 184.69, 0.005)
check("by hand: RDS in rupees", 184.69 * FX, 16068, 0.5)
check("hot GB", 277 * 90 / 365, 68.3, 0.05)
check("cold GB", 277 - 68.3, 208.7, 0.05)
check("total", total, 37780, 0)
check("total $", costs["monthly_usd"].sum(), 434.24, 0.005)
check("warehouse share %", (c["Warehouse compute (RDS)"] + c["Warehouse storage (gp3)"]) / total * 100, 66.7, 0.05)
check("LLM share %", (c["PO-intake (LLM API)"] + c["RAG assistant (LLM API)"]) / total * 100, 0.6, 0.05)
ai = c["Defect-model serving"] + c["PO-intake (LLM API)"] + c["RAG assistant (LLM API)"]
check("all AI share % (about a sixth)", ai / total * 100, 15.6, 0.05)
check("hot per GB (rupees)", c["Sensor archive, hot (S3)"] / 68.3, 2.18, 0.005)
check("cold per GB (rupees)", c["Sensor archive, cold (Glacier)"] / 208.7, 0.39, 0.005)
check("hot/cold per-GB ratio (list prices)", 0.025 / 0.0045, 5.6, 0.05)
check("cold share of archive %", 208.7 / 277 * 100, 75, 0.5)
all_standard = 277 * 0.025 * FX
check("archive all in S3 Standard (rupees)", all_standard, 602, 0.5)
tiered = c["Sensor archive, hot (S3)"] + c["Sensor archive, cold (Glacier)"]
check("tiering saving (about 370)", all_standard - tiered, 370, 5)
ten_tb_saving = (10_000 * 0.025 - (2_500 * 0.025 + 7_500 * 0.0045)) * FX
check("10 TB what-if saving (about 13,400)", ten_tb_saving, 13400, 50)
check("egress billed GB", 180 - 100, 80, 0)
check("Ch 52 always-on vs scheduled", 730 / 30, 24, 0.5)

# Section 65.3
lines = 87_011 / 12
check("order lines a month", lines, 7251, 0.5)
check("PO by hand", 87 / 1120, 0.078, 0.0005)
check("Ch 57 per email at 88", (10_844 * 2 + 3_184 * 10) / 1e6 / 60 * 88, 0.079, 0.0005)
check("per $ PO email", (10_844 * 2 + 3_184 * 10) / 1e6 / 60, 0.000892, 0.0000005)
check("RAG $ per question", (470 * 2 + 60 * 10) / 1e6, 0.00154, 0)
per1000 = total / (lines / 1000)
check("per 1,000 lines", per1000, 5210.38, 0.005)
check("factor vs 0.50", per1000 / 0.50, 10421, 0.5)
check("defect predictions a month", 500 * 52 / 12, 2167, 0.5)
check("per defect prediction", c["Defect-model serving"] / (500 * 52 / 12), 2.63, 0.005)
check("per RAG question", c["RAG assistant (LLM API)"] / 1000, 0.134, 0.0005)
flash_hour = (c["Warehouse compute (RDS)"] + c["Orchestration (Dagster)"]) / 730
check("Flash per hour", flash_hour, 29.81, 0.005)
check("Flash per send", flash_hour * 2 / 60, 0.99, 0.005)
check("Flash a year (about 250)", flash_hour * 2 / 60 * 250, 250, 5)
check("Flash whole-hour what-if a year", flash_hour * 250, 7450, 5)
check("NFR allows a month (under Rs 4)", 0.50 * lines / 1000, 3.63, 0.005)
emails_per_1000 = 1120 / lines * 1000
marg = emails_per_1000 * (c["PO-intake (LLM API)"] / 1120)
check("marginal per 1,000 lines", marg, 12.0, 0.005)
check("fully-loaded / marginal", per1000 / marg, 434, 0.5)
check("marginal / 0.50", marg / 0.5, 24, 0.05)
check("headroom under 6,000 %", (6000 / per1000 - 1) * 100, 15, 0.2)
check("Ch 58 review per email", 197 / 40, 4.93, 0.005)
check("review / LLM per email", (197 / 40) / (c["PO-intake (LLM API)"] / 1120), 63, 0.5)
check("Ch 58 review minutes: 40 x 45 s", 40 * 45 / 60, 30, 0)

# unit_economics.csv matches section 65.3's outputs
check("csv per 1,000 lines", unit_csv["per 1,000 order lines"], 5210.376, 0.0005)
check("csv Flash", unit_csv["per Daily Flash send"], 0.994, 0.0005)
check("csv defect", unit_csv["per defect prediction"], 2.627, 0.0005)
check("csv PO", unit_csv["per PO-intake email"], 0.078, 0.0005)
check("csv RAG", unit_csv["per RAG question"], 0.134, 0.0005)

# Section 65.4
owner = costs.groupby("owner")["monthly_inr"].sum() / total * 100
for name, want in [("data platform", 81.7), ("AI applications", 15.6), ("shared", 2.0), ("plant operations", 0.6)]:
    check(f"showback {name}", owner[name], want, 0.05)

# Section 65.5
od = c["Warehouse compute (RDS)"] + c["Defect-model serving"]
check("two instances on demand", od, 21759, 0)
res = (0.162 + 0.0564) * 730 * FX
check("reserved a month", res, 13871, 0.5)
check("reserved saving a month (about 7,900)", od - res, 7900, 15)
check("reserved saving a year (about 95,000)", (od - res) * 12, 95000, 400)
check("frontier / workhorse input", 10 / 2, 5, 0)
check("frontier / volume output (more than 10)", 50 / 4, 12.5, 0)

# Answers
check("ans 6 top three", c["Warehouse compute (RDS)"] + c["Warehouse storage (gp3)"] + c["Orchestration (Dagster)"], 30877, 0)
check("ans 6 share", 30877 / total * 100, 81.7, 0.05)
check("ans 8 LLM rupees", c["PO-intake (LLM API)"] + c["RAG assistant (LLM API)"], 221, 0)
check("ans 11 RAG share", 134 / total * 100, 0.35, 0.005)
check("ans 13 at 50% a month", od / 2, 10880, 0.5)
check("ans 13 at 50% a year", od / 2 * 12, 130554, 0)
check("ans 15 alert headroom %", (45000 / total - 1) * 100, 19, 0.2)
check("annual cost (for Ch 66/67)", total * 12, 453360, 0)

print("ALL OK" if ok else "SOME CHECKS FAILED")
