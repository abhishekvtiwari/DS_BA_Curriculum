# Chapter 65. FinOps: The Economics of Data Platforms

*Part 7 — Architecture, Governance & Leadership*

> **Chapter at a glance**
>
> **You will learn to:** explain how cloud billing actually works — pay-as-you-go, no minimum commitment, and the handful of meters that drive almost every bill · identify the real cost drivers in a data platform: warehouse compute and storage, orchestration, and AI serving and API calls · compute unit economics — cost per report, per prediction, per AI request — for a real platform · use tagging and showback to make a shared bill honest about who's spending what · make architecture decisions with cost as an explicit input, not an afterthought discovered on next month's invoice.
>
> **Before you start:** this chapter puts a real price on the platform Chapters 60 through 64 designed, distributed, patterned, governed, and secured. It reuses numbers from earlier chapters: Chapter 49's sensor-archive estimate, Chapter 52's cloud vocabulary and its cost section, Chapter 54's LLM price tiers, the LLM costs Chapters 55 and 57 measured, Chapter 58's PO-intake review time, and Chapter 63's value table. It also returns to one specific number: Chapter 60's non-functional requirement that platform cost stay under ₹0.50 per 1,000 order lines processed — a target set before anyone had actually built a cost model to check it against.
>
> **Time needed:** 9–11 hours, spread over a week.
>
> **Tools:** `pandas` for the cost model and `psql` for one count on `riverstone_full` (tested with Python 3.11 and pandas 3.0.6).
>
> **Practice data:** `companion/ch65/`: `monthly_cost_model.csv` (Riverstone's monthly infrastructure bill, ten components, priced at AWS list prices for the Mumbai region checked on 29 September 2026) and `unit_economics.csv` (the unit costs section 65.3 computes). `build_ch65_files.py` writes both.
>
> **A note on the numbers in this chapter.** Infrastructure unit prices (database compute and storage, servers, S3 storage tiers, data transfer) are AWS's published list prices for its Mumbai region (`ap-south-1`), checked on 29 September 2026; the price sheet in the Project's Tools section gives each one and its source. Dollars become rupees at **₹87 to the dollar**, the one rate this chapter uses. Other chapters used other rates (₹83 in Chapter 49, ₹88 in Chapter 57), because exchange rates move, so every calculation here says which rate it uses. Which instance sizes Riverstone runs, and how much it stores, are a reasonable invented sizing for a company at this scale, not a disclosed fact about a real company; the volumes come from earlier chapters. Cloud pricing changes; verify current rates before building a real budget on this chapter's specific numbers.

---

## Why this matters

Every chapter in this Part has asked "does it work," "does it survive failure," "does it fit the organization," "is it governed," "is it secure." None of them asked the question that eventually lands on an architect's desk regardless of how well any of the others were answered: **what does this actually cost, and is that number acceptable?**

Cloud infrastructure makes this question deceptively easy to postpone. There's no upfront purchase order, no visible price tag on the moment you provision a database or call an API — just a bill that arrives weeks later, shaped by decisions nobody was thinking about as cost decisions at the time. An architect who designs well but never prices what they've designed is planning half a system. FinOps — the discipline of bringing financial accountability to variable cloud spend — is the other half, and it's a design skill, not an accounting afterthought: the best time to know what something costs is before you build it, not when the invoice explains it to you.

Chapter 2 warned that cloud bills grow quietly if nobody watches them. Chapter 52, section 52.7, priced one pipeline and found one lever: don't run what nothing needs. This chapter builds the whole model.

It also closes something specific, in the same spirit as Chapter 64 closing Chapter 60's access-control risk. Chapter 60's design document set a cost target — **under ₹0.50 per 1,000 order lines processed** — as a non-functional requirement, the way Chapter 60 taught every NFR should be: a number, not an adjective. Nobody, at the time, built the bottom-up model to check whether that number was realistic. This chapter builds it.

---

## In plain English

Think about the difference between a household that tracks its spending and one that only discovers what it spent when the bank statement arrives.

The second household isn't necessarily spending more — but every decision it makes is uninformed by cost until it's too late to change: they book the expensive flight because nobody checked the price against the month's budget before clicking buy, they're startled every month by how much the streaming subscriptions add up to because nobody ever listed them side by side. The first household makes exactly the same purchases sometimes — but it makes them *knowing* what they cost, and that knowledge changes some of the decisions, because seeing four subscription costs lined up next to each other is what makes "we don't need all four" obvious in a way that four separate, forgotten monthly charges never do.

**FinOps is that household budget, for cloud infrastructure.** Not spending less, necessarily — spending *knowingly*. The habit of lining every cost up, attributing it to who's actually generating it, and asking whether each one is buying what it's supposed to, before the surprise arrives rather than after.

---

## 65.1 How cloud billing actually works

Cloud billing has one property that makes it different from almost every other kind of business expense: **there's no minimum commitment, and the bill is the sum of many small, continuously-metered charges rather than one negotiated price.** A traditional software purchase is a single number agreed in advance; a cloud bill is thousands of tiny measurements — instance-hours, gigabytes stored, requests made, gigabytes transferred — added up after the fact.

**The handful of meters that drive almost every real bill:**

- **Compute**, billed by the hour or the second a resource runs, whether or not it's doing useful work. A database instance running 24/7 is billed for all 730 hours in a month (24 × 365 ÷ 12), not just the hours someone happens to query it. Riverstone's warehouse is exactly that: Chapter 45's PostgreSQL, run on Amazon RDS (the managed PostgreSQL service Chapter 52 named) since the platform moved to AWS.
- **Storage**, billed by the gigabyte-month, with the rate depending heavily on *how quickly you need to retrieve it* — a distinction section 65.2 returns to.
- **Requests and API calls**, billed per call or per unit of work — the meter that governs every LLM API call in Chapter 58's PO-intake pipeline and Chapter 55's support assistant.
- **Data transfer**, specifically data moving *out* of the cloud provider's network — usually free coming in, metered going out once a free monthly allowance is used up (100 GB a month on AWS), and the meter most commonly forgotten when estimating a new system's cost in advance.

**Two purchasing models matter for any sustained workload:** **on-demand** pricing, the default, charges the full metered rate with no commitment and no discount; **reserved** pricing (committing to a usage level for one or three years) cuts the same resource's cost substantially, in exchange for giving up the flexibility to simply stop paying if the workload disappears. For the instances in this chapter, AWS's Mumbai price list takes about 36% off for a one-year commitment paid monthly, and about 61% off for three years paid upfront. The architect's job is knowing which of a platform's components are stable enough to reserve and which are still too uncertain to commit to.

---

## 65.2 Cost drivers in a data platform

Riverstone's monthly infrastructure bill, built bottom-up: every part of Chapter 60's container diagram that runs on its own infrastructure, priced at AWS's Mumbai list prices. First, the names an AWS bill uses.

> **Reading an AWS bill: seven names you need**
>
> - **RDS** (Relational Database Service): Amazon's managed database service, here running PostgreSQL. Chapter 52 met it as an example of a platform service.
> - **EC2** (Elastic Compute Cloud): a rented virtual machine, billed for every hour it runs.
> - **Instance type:** the size of that machine. `db.m5.large` (the database) and `t3.large` (the two servers) each have 2 vCPUs (Chapter 52) and 8 GB of memory.
> - **gp3:** general-purpose SSD storage for a database, billed per GB **provisioned** (set aside in advance), whether or not it's full.
> - **Single-AZ:** the database lives in one availability zone (Chapter 52), one data centre, with no standby copy. Multi-AZ keeps a standby in a second zone and costs twice as much: $0.506 an hour for this database instead of $0.253. Single-AZ is a cost choice with a reliability price. Chapter 52 advised spreading anything that must stay up across two zones, and Chapter 60's reliability target (at most 2 pipeline runs a year needing a person) is what this choice has to be checked against.
> - **S3 Standard** and **S3 Glacier Flexible Retrieval:** hot and cold object storage. Glacier costs far less to keep and takes hours, and a fee, to read back.
> - **Egress:** data leaving AWS for the internet — dashboards, API replies, emails.

The ten lines of the bill, with the quantity and the unit price behind each:

| Component | What it is | Quantity × unit price (USD) |
|---|---|---|
| Warehouse compute (RDS) | `db.m5.large`, PostgreSQL, Single-AZ, always on | 730 hours × $0.253 |
| Warehouse storage (gp3) | 800 GB provisioned | 800 GB × $0.131 |
| Warehouse backups | automatic daily snapshots | free up to the 800 GB provisioned |
| Orchestration (Dagster) | `t3.large`, always on: the daemon and web UI that fire schedules | 730 hours × $0.0896 |
| Defect-model serving | `t3.large`, always on for line speed (Chapter 56's FastAPI service) | 730 hours × $0.0896 |
| PO-intake (LLM API) | Chapter 57's metered cost, workhorse tier | 1,120 emails × $0.000892 |
| RAG assistant (LLM API) | Chapter 55's estimate, workhorse tier | 1,000 questions × $0.00154 |
| Sensor archive, hot (S3) | the last 90 days of the archive | 68.3 GB × $0.025 |
| Sensor archive, cold (Glacier) | the rest of the year | 208.7 GB × $0.0045 |
| Data transfer out | 180 GB a month, the first 100 GB free | 80 GB × $0.1093 |

By hand, once: 730 hours × $0.253 = $184.69 a month for the warehouse, and at ₹87 to the dollar that's ₹16,068. `build_ch65_files.py` does the same multiplication for every line.

The sensor archive is Chapter 49's plant-wide rollout (1,460 sensors, one reading a second) a year in: 277 GB, of which the last 90 days (277 × 90 ÷ 365 = 68.3 GB) stay in S3 Standard. Chapter 52's Terraform moved old *versions* of files to Glacier after 90 days; the cold tier here moves the readings themselves after 90 days, which takes one more lifecycle rule of the same shape (a `transition` block instead of `noncurrent_version_transition`), with the same `GLACIER` storage class, S3 Glacier Flexible Retrieval.

Now load the bill, largest line first:

```python
import pandas as pd

costs = pd.read_csv("monthly_cost_model.csv")
costs_sorted = costs.sort_values("monthly_inr", ascending=False)
print(costs_sorted[["component", "monthly_inr"]].to_string(index=False))
```

```
                     component  monthly_inr
       Warehouse compute (RDS)        16068
       Warehouse storage (gp3)         9118
       Orchestration (Dagster)         5691
          Defect-model serving         5691
             Data transfer out          760
      Sensor archive, hot (S3)          149
       RAG assistant (LLM API)          134
           PO-intake (LLM API)           87
Sensor archive, cold (Glacier)           82
             Warehouse backups            0
```

- **`pd.read_csv(...)`** loads the bill, one row per component (Chapter 18). The file also has the owner, the unit, the unit price, the quantity, and the dollar amount of each line.
- **`sort_values("monthly_inr", ascending=False)`** orders the rows by their rupee cost; `ascending=False` puts the largest first.
- **`costs_sorted[["component", "monthly_inr"]]`**: the double brackets pick a list of two columns, so the table fits the page.
- **`.to_string(index=False)`** prints every row, without the row numbers pandas would otherwise add on the left.

Add it up:

```python
total = costs["monthly_inr"].sum()
print(f"Total monthly infrastructure cost: ₹{total:,.0f}")
print(f"In dollars: ${costs['monthly_usd'].sum():,.2f}, at ₹87 to the dollar")
```

```
Total monthly infrastructure cost: ₹37,780
In dollars: $434.24, at ₹87 to the dollar
```

- **`costs["monthly_inr"].sum()`** adds one column, like `SUM()` in SQL.
- **`:,.0f`** formats a number with a comma between thousands (`,`) and no decimals (`.0f`); `:,.2f` keeps two decimals for dollars and cents.

Each line's share of the total is one more column:

```python
costs_sorted["share_pct"] = (costs_sorted["monthly_inr"] / total * 100).round(1)
print(costs_sorted[["component", "share_pct"]].head(4).to_string(index=False))
```

```
              component  share_pct
Warehouse compute (RDS)       42.5
Warehouse storage (gp3)       24.1
Orchestration (Dagster)       15.1
   Defect-model serving       15.1
```

- The right-hand side divides the whole column by the total at once, makes it a percentage, and rounds it to one decimal; assigning it to `costs_sorted["share_pct"]` adds it as a new column.
- **`.head(4)`** shows only the first four rows, the largest four lines.

Two groups matter for the argument that follows: the warehouse's two lines, and the two LLM lines. Pick each group by its exact names:

```python
warehouse = ["Warehouse compute (RDS)", "Warehouse storage (gp3)"]
llm = ["PO-intake (LLM API)", "RAG assistant (LLM API)"]

is_warehouse = costs_sorted["component"].isin(warehouse)
is_llm = costs_sorted["component"].isin(llm)
print(f"Warehouse share: {costs_sorted.loc[is_warehouse, 'monthly_inr'].sum() / total:.1%}")
print(f"LLM API share: {costs_sorted.loc[is_llm, 'monthly_inr'].sum() / total:.1%}")
```

```
Warehouse share: 66.7%
LLM API share: 0.6%
```

- **`.isin(warehouse)`** gives `True` for each row whose component is one of the names in the list, and `False` otherwise: a mask, as in Chapter 18.
- **`costs_sorted.loc[is_warehouse, 'monthly_inr']`** keeps the rows where the mask is `True` and the one column `monthly_inr`; `.sum()` adds their rupees, and dividing by `total` gives the group's share. Adding the rupees first, rather than the rounded shares, avoids adding up rounding errors.
- **`:.1%`** prints a fraction as a percentage with one decimal: 0.667 prints as `66.7%`.

![A horizontal bar chart of Riverstone's ten monthly infrastructure costs, from warehouse compute at ₹16,068 and warehouse storage at ₹9,118 (darker, together 66.7% of the bill), through the two always-on servers at ₹5,691 each, down to the LLM API lines at ₹134 and ₹87 (0.6% together) and free backups; total ₹37,780 a month](figures/fig65-1-cost-breakdown.svg)

*Figure 65.1 — Two line items — the warehouse's compute and storage — are two-thirds of the entire bill. The AI systems everyone worries about cost less than the database everyone takes for granted.*

**Three findings, in order of how surprising they typically are to a first-time reviewer:**

1. **The warehouse dominates, not the AI.** RDS compute and storage together are two-thirds of the bill; the two LLM-powered systems (PO-intake extraction and the RAG assistant) combined are under 1%. Even counting the defect-model server, everything AI is about a sixth. This is a common and important surprise: the newest, most talked-about part of a platform is rarely its largest cost driver, and a cost review that only scrutinizes "the AI spend" while ignoring the database running underneath it is looking in the wrong place.
2. **Storage tiering works, and here it barely matters.** The sensor archive's hot tier (S3 Standard, 90 days) costs ₹149 a month for 68.3 GB; the cold tier (Glacier Flexible Retrieval, everything older) costs ₹82 for three times the data (208.7 GB). Per gigabyte, cold is about 5.6 times cheaper. Kept entirely in S3 Standard, the archive would cost about ₹602 a month, so tiering saves about ₹370 a month. That is Chapter 49's lesson in rupees: at this size, storage is almost never the problem.
3. **Compute for always-on services is a fixed cost, not a variable one.** The defect-model serving instance and the Dagster instance are billed for every hour they run, whether Taloja's line is producing parts at that moment or not — a cost that scales with *uptime*, not usage, which is exactly why the reserved-versus-on-demand decision (section 65.1) matters most for always-on lines like these. Chapter 52 found an always-on container 24 times dearer than the same container run on a schedule.

### What this bill leaves out

This is the **infrastructure** bill, not everything the platform costs. It leaves out Power BI licences for the dashboards (Chapter 16), the pipeline's own scheduled containers (Chapter 52 priced them at under $1 a month), the reverse-ETL syncs and the semantic layer's dbt runs (small jobs on the instances above), monitoring and log storage, the service that sends the Flash's emails, a staging environment, the credential vault (Chapter 64), and the servers' own disks. Above all, it leaves out people. Chapter 66 comes back to engineering time, the cost that never appears on a cloud invoice.

---

## 65.3 Unit economics — and the NFR nobody had checked

A total monthly bill tells you what a platform costs. **Unit economics** tell you what it costs *to do the thing the platform exists to do* — the number that actually lets you compare, scale, or defend a cost, because "₹37,780 a month" means nothing on its own, and "8 paise per email processed" can be judged against what processing that email is worth.

A unit cost is a cost divided by a volume, so you need both. The costs are on the bill. The volumes come from earlier chapters, and the biggest one, order lines, comes from the data itself.

### Where the volume comes from

Chapter 60's NFR is per 1,000 order lines, so count them. The last full year in `riverstone_full` is 2025:

<!-- db: riverstone_full -->

```sql
SELECT COUNT(*) AS order_lines_2025
FROM order_items AS i
JOIN orders AS o ON o.order_id = i.order_id
WHERE o.order_date >= DATE '2025-01-01'
  AND o.order_date <  DATE '2026-01-01';
```

```
 order_lines_2025 
------------------
            87011
(1 row)
```

- **`FROM order_items AS i`**: one row per order line, the table's grain (Chapter 28). `i` and `o` are short aliases for the two tables.
- **`JOIN orders AS o ON o.order_id = i.order_id`** attaches each line to its order, because the date lives on the order, not the line (Chapter 12).
- **`WHERE o.order_date >= DATE '2025-01-01' AND o.order_date < DATE '2026-01-01'`** keeps the whole of 2025 and nothing after: from the first day, up to but not including the first day of 2026. `DATE '...'` writes a date value.
- **`COUNT(*) AS order_lines_2025`** counts the rows left and names the result column.

The platform loads every line, cancelled or not, so the count takes them all: 87,011 lines in 2025, about 7,251 a month.

### A unit cost by hand, then in pandas

**By hand, once.** PO-intake's line on the bill is ₹87 a month, and Chapter 57 counted 1,120 order emails in a month (19 ordinary days of 40, and 3 month-end days of 120). ₹87 ÷ 1,120 = ₹0.078, about 8 paise an email. (Chapter 57 got ₹0.079, because it used ₹88 to the dollar.)

Every unit cost follows one **allocation rule**: which lines of the bill it carries, divided by which volume.

| Unit cost | Cost lines it carries | Volume a month |
|---|---|---|
| per 1,000 order lines | the whole bill | 87,011 ÷ 12 lines, in thousands |
| per Daily Flash send | 2 minutes of warehouse compute and orchestration | one send |
| per defect prediction | defect-model serving | 500 parts a week × 52 ÷ 12 (Chapter 56) |
| per PO-intake email | PO-intake (LLM API) | 1,120 emails (Chapter 57) |
| per RAG question | RAG assistant (LLM API) | 1,000 questions (Chapter 55's planning figure) |

The volumes, in code:

```python
volumes = {
    "order line": 87_011 / 12,            # 2025's lines, a month (the query above)
    "defect prediction": 500 * 52 / 12,   # Chapter 56: 500 parts inspected a week
    "PO-intake email": 1_120,             # Chapter 57: 19 days × 40 + 3 days × 120
    "RAG question": 1_000,                # Chapter 55's planning figure
}
for name, n in volumes.items():
    print(f"{name:<18} {n:>6,.0f} a month")
```

```
order line          7,251 a month
defect prediction   2,167 a month
PO-intake email     1,120 a month
RAG question        1,000 a month
```

- A **dictionary** maps each name to its volume (Chapter 17). `87_011 / 12` is written as the calculation, not as its answer, so anyone can check where it came from.
- **`.items()`** gives each name and its value in turn. `:<18` pads the name to 18 characters and `:>6,.0f` right-aligns the number, so the columns line up.

Now divide. Each unit cost is one line of the bill (or the whole total) over one volume:

```python
by_name = costs.set_index("component")["monthly_inr"]

unit_costs = pd.Series({
    "per 1,000 order lines": total / (volumes["order line"] / 1_000),
    "per defect prediction": by_name["Defect-model serving"] / volumes["defect prediction"],
    "per PO-intake email": by_name["PO-intake (LLM API)"] / volumes["PO-intake email"],
    "per RAG question": by_name["RAG assistant (LLM API)"] / volumes["RAG question"],
})
print(unit_costs.round(3).to_string())
```

```
per 1,000 order lines    5210.376
per defect prediction       2.627
per PO-intake email         0.078
per RAG question            0.134
```

- **`costs.set_index("component")["monthly_inr"]`** makes the component names the row labels and keeps one column, so `by_name["Defect-model serving"]` looks up a cost by its name.
- **`pd.Series({...})`** turns a dictionary into a labelled column of numbers: the keys become the labels.
- **"Per 1,000 order lines"** is the total divided by the month's lines in thousands: ₹37,780 ÷ 7.251.
- **`.round(3)`** keeps three decimals; `companion/ch65/unit_economics.csv` holds the same numbers.

The Daily Flash needs a rule of its own, because it has no line on the bill. It runs for about two minutes on the warehouse and the orchestrator (Chapter 52), on 250 working days a year (Chapter 20). Charge it for exactly those minutes:

```python
per_hour = (by_name["Warehouse compute (RDS)"] + by_name["Orchestration (Dagster)"]) / 730
per_send = per_hour * 2 / 60
unit_costs["per Daily Flash send"] = per_send
print(f"warehouse + orchestrator: ₹{per_hour:.2f} an hour")
print(f"one Flash send, 2 minutes: ₹{per_send:.2f}")
print(f"a year, 250 sends: ₹{per_send * 250:,.0f}")
```

```
warehouse + orchestrator: ₹29.81 an hour
one Flash send, 2 minutes: ₹0.99
a year, 250 sends: ₹248
```

- The two monthly costs, divided by 730 hours, are what an hour of both machines costs; two minutes is `2 / 60` of an hour.
- `unit_costs["per Daily Flash send"] = per_send` adds a fifth entry to the Series.
- Try changing `2 / 60` to `60 / 60`, as if each Flash held both machines for a whole hour: a send would cost ₹29.81, and a year of sends about ₹7,450. Still small against what the Flash saves.

About ₹1 a send, ₹250 a year, against the ₹97,500 a year of staff time the Flash saves (Chapter 20, section 20.14): trivial, and never worth optimizing. Charging the Flash a share of the hours the machines sit idle as well would be a choice, not a fact. **An allocation rule is a decision**, which is why a unit cost should always be quoted with its rule.

### Checking Chapter 60's NFR

Before you run it, predict: Chapter 60 allowed ₹0.50 per 1,000 order lines. By roughly what factor is ₹5,210 over it?

```python
ch60_target = 0.50   # Chapter 60's NFR: ₹ per 1,000 order lines
actual = unit_costs["per 1,000 order lines"]
print(f"Chapter 60's target: ₹{ch60_target:.2f} per 1,000 order lines")
print(f"This chapter's bottom-up figure: ₹{actual:,.2f} per 1,000 order lines")
print(f"Off by a factor of: {actual / ch60_target:,.0f}")
```

```
Chapter 60's target: ₹0.50 per 1,000 order lines
This chapter's bottom-up figure: ₹5,210.38 per 1,000 order lines
Off by a factor of: 10,421
```

**That gap is real, and it's worth sitting with rather than explaining away.** Chapter 60 wrote a specific, testable number, exactly as its own section on non-functional requirements taught — and that number turns out to have been about 10,000 times too optimistic (10,421 times, exactly), because it was never actually checked against a real, bottom-up cost model. This is not a failure of Chapter 60's method; it's exactly the failure Chapter 60's method exists to catch, once someone finally runs the numbers.

![Three dots on a log scale of rupees per 1,000 order lines: Chapter 60's original NFR at ₹0.50, the marginal cost at ₹12.00, and the fully-loaded cost at ₹5,210.38, about 10,000 times the target](figures/fig65-2-nfr-reality-check.svg)

*Figure 65.2 — An NFR is a hypothesis until someone prices it. This one was wrong by four orders of magnitude, and the only way to find that out was to build the model.*

**What actually went wrong with the original number, diagnosed properly rather than just corrected:** a well-specified cost target has to keep two different things apart. The **fully-loaded average cost** is this chapter's ₹5,210 per 1,000 lines, which includes the always-on warehouse and orchestration whether or not a single new order line arrives that month. The **marginal cost** is what one additional 1,000 order lines costs once the platform already exists. Chapter 60's NFR didn't say which it meant. The marginal cost is the obvious suspect, so compute it: go down the bill and ask which lines grow when more order lines arrive.

```python
emails_per_1000 = volumes["PO-intake email"] / volumes["order line"] * 1_000
marginal = {
    "LLM calls for PO emails": emails_per_1000 * unit_costs["per PO-intake email"],
    "warehouse storage": 0.0,   # 800 GB is provisioned, and paid for, already
    "compute": 0.0,             # the always-on instances have spare capacity
    "data transfer": 0.0,       # dashboards and the Flash don't grow with order lines
}
print(f"PO emails per 1,000 order lines: {emails_per_1000:.1f}")
for item, rupees in marginal.items():
    print(f"{item:<24} ₹{rupees:5.2f}")
print(f"{'marginal cost':<24} ₹{sum(marginal.values()):5.2f} per 1,000 order lines")
```

```
PO emails per 1,000 order lines: 154.5
LLM calls for PO emails  ₹12.00
warehouse storage        ₹ 0.00
compute                  ₹ 0.00
data transfer            ₹ 0.00
marginal cost            ₹12.00 per 1,000 order lines
```

- **`emails_per_1000`** assumes new order lines arrive in today's mix: 1,120 PO emails for every 7,251 lines, so about 154 emails per 1,000 lines. Each of those emails costs one LLM call.
- The zeros are the point of the exercise. Storage is paid for by the gigabyte provisioned, not used; the instances run all month anyway; nothing leaving AWS depends on how many lines there are. Each zero holds only while there's spare capacity, which is why the NFR below says so.
- **`sum(marginal.values())`** adds the four amounts.

About **₹12 per 1,000 order lines**, almost all of it PO-intake's LLM calls (people's review time isn't on an infrastructure bill). That is 434 times below the fully-loaded figure, and still 24 times Chapter 60's ₹0.50. So the original number wasn't a marginal cost either. It was never priced at all, and **the NFR, as written, didn't say which cost it meant**, which is exactly the kind of ambiguity Chapter 60's own advice about turning adjectives into numbers was supposed to prevent, and didn't quite manage to, on its own first attempt.

**The corrected NFR, written the way section 60.3's method actually demands:**

> *Fully-loaded infrastructure cost: under ₹6,000 per 1,000 order lines processed, reviewed monthly, covering the warehouse, orchestration, AI serving and LLM calls (measured: ₹5,210). Marginal cost of incremental volume: under ₹15 per 1,000 additional order lines, assuming existing infrastructure has spare capacity (measured: ₹12). Both measured from the same monthly cost model, not estimated separately.*

That's a target Riverstone's actual ₹5,210 meets with about 15% to spare, and — more importantly — it's a target that means something specific enough to be checked again next month, which the original one-line version never quite was.

**The other unit-economics figures, useful for the same reason:**

| Metric | Value | What it's good for |
|---|---:|---|
| Cost per Daily Flash send | ₹0.99 | Trivial: about ₹250 a year against ₹97,500 a year of staff time saved |
| Cost per defect-model prediction | ₹2.63 | High per prediction because the server runs all day for 2,167 parts a month — see section 65.2's third finding |
| Cost per PO-intake email processed | ₹0.078 | Compare with about ₹4.93 of reviewer time per email (below) |
| Cost per RAG assistant question | ₹0.134 | Cheap enough that usage limits should be about quality control, not cost control |

**The PO-intake comparison is the one worth pausing on.** Chapter 58, section 58.7, priced assisted mode at ₹197 a day of reviewer time: 39 minutes (about 45 seconds to confirm each of 40 emails, plus the queue of emails that need judgment), at the ₹300 an hour loaded rate the book has used since Part 2. Chapter 63's value table (section 63.2) uses the same figures. That is about ₹4.93 of review time per email (₹197 ÷ 40), against ₹0.078 of LLM cost: about 63 times as much. Counting the wrong orders a reviewer misses, Chapter 58's assisted total rises to about ₹1,530 a day. Either way, the infrastructure was never the expensive part of that decision. The human confirmation time is where nearly all the real cost sits, which matters directly for any future proposal to "automate this further to save money": the money to be saved is almost entirely in reducing human review time, and in how many errors that review catches, not in cutting an already-negligible API bill.

---

## 65.4 Budgets, tagging, and showback

None of section 65.2's cost breakdown is possible without a habit that has to be built in from the start: **every resource tagged, at creation, with who owns it.**

- **Tagging**, mechanically: every resource — a database, a storage bucket, a compute instance — carries metadata at creation time recording its owner, which container it belongs to (Chapter 60's diagram), and its environment (production, staging). Chapter 52's Terraform already did this for the sensor bucket (`tags = { ... }`). Retrofitting tags onto untagged resources months later is possible but far more work than tagging at creation, which is why it belongs in Chapter 63's automation-inventory discipline from day one, not as a cleanup project.
- **Showback** takes the tagged bill and reports each team's actual spend back to them — "your containers cost ₹25,000 this month" — without automatically charging that amount against their budget. It's the first, lower-stakes step, and the right one to start with: it makes cost visible and creates accountability through transparency alone, before any harder conversation about budgets or enforcement.
- **Chargeback** goes further, actually billing each team's cost centre for its share — appropriate once showback has run long enough that the numbers are trusted and teams have had a chance to act on what they saw before being charged for it.
- **Budgets and alerts** close the loop: a threshold per tag, with a notification (Chapter 20's alerting pattern, section 20.8, reused) when spending approaches or crosses it — catching a runaway cost within days instead of discovering it a month later on the invoice.

In `monthly_cost_model.csv`, the `owner` column plays the part of the tag. A showback report is one `groupby` (Chapter 18):

```python
showback = costs.groupby("owner")["monthly_inr"].sum().sort_values(ascending=False)
print((showback / total * 100).round(1).to_string())
```

```
owner
data platform       81.7
AI applications     15.6
shared               2.0
plant operations     0.6
```

- **`groupby("owner")["monthly_inr"].sum()`** adds the rupees for each owner, one total per tag, like `GROUP BY` in SQL.
- Dividing by `total` and multiplying by 100 turns each total into a share of the bill.

![A three-stage flow: every resource tagged at creation, one monthly bill split automatically by tag, and a showback report per owner: data platform 81.7%, AI applications 15.6%, shared 2.0%, plant operations 0.6%](figures/fig65-3-tagging-showback.svg)

*Figure 65.3 — Tagging turns one anonymous invoice into an answerable question: whose spending is this, actually?*

**Riverstone's own showback breakdown:** the data platform team's containers (the warehouse, its backups, and orchestration) are about four-fifths of the bill; the AI applications (defect-model serving and both LLM APIs) about a sixth; plant operations' sensor archive under 1%. Data transfer out, 2%, is genuinely shared: dashboards, API replies and the Flash's emails all use it, and no single team should be charged for it in full. That last category matters: **forcing every cost into a single owner's showback report, when some costs are genuinely shared, produces a number that's precise and wrong** — better to have an honest "shared" category than a falsely attributed one.

---

## 65.5 Cost-aware architecture decisions

Every architectural choice this Part has taught carries a cost dimension that's worth naming explicitly, not left implicit until the bill arrives.

- **Storage tiering** (section 65.2's second finding) is a large lever once archives reach terabytes: moving data to a colder tier as it ages costs nothing in engineering effort once a lifecycle policy exists, and Glacier Flexible Retrieval is about 5.6 times cheaper per gigabyte than S3 Standard in Mumbai. At Riverstone's 277 GB it saves about ₹370 a month, which is Chapter 49's point again: storage is rarely the problem; scanning is. What if the archive grew to 10 TB? With the same split, a quarter hot and three-quarters cold, the same rule would save about ₹13,400 a month: the lever grows with the archive.
- **Reserved versus on-demand compute** (section 65.1): the warehouse's RDS instance and the defect-model's serving instance are both stable, always-on, predictable workloads — textbook candidates for reserved pricing, once the platform's shape is stable enough to commit to. Together they cost ₹21,759 a month on demand; the calculation below prices the reservation. Reserved pricing covers instance-hours only: the 800 GB of gp3 storage costs the same either way.
- **Scheduled versus event-driven** (Chapter 63, section 63.5) has a direct cost reading, not just a latency one: an always-on event listener is a 24/7 compute cost regardless of how often it actually fires, while a scheduled job's cost scales with how often it runs. Chapter 52, section 52.7, measured the gap at 24 times for one container. That's the cost side of Chapter 63's rule: default to scheduled unless a real cost of delay justifies the always-on alternative.
- **Choosing the right model tier** (Chapter 54's landscape) is a direct cost lever for any LLM-powered system: PO-intake's extraction task doesn't need the most capable, most expensive model available — a workhorse model handles structured extraction well. Chapter 54's table puts the frontier tier at about 5 times the workhorse price, and more than 10 times the volume tier; Chapter 57 found the same 5 times per email (₹0.393 against ₹0.079) for output quality the task genuinely doesn't need.
- **Fan-out and duplication** (Chapter 12's join warning, and Chapter 28's grain discipline in section 28.8, revisited through a cost lens): a query or a pipeline that silently multiplies rows doesn't just produce wrong numbers — it also silently multiplies compute and storage cost for exactly as long as nobody notices.

**One of these, priced.** AWS's Mumbai price list (checked 29 September 2026) offers the database at $0.162 an hour and a `t3.large` at $0.0564 an hour on a one-year reservation with nothing paid upfront:

```python
on_demand = by_name["Warehouse compute (RDS)"] + by_name["Defect-model serving"]
reserved = (0.162 + 0.0564) * 730 * 87      # $ an hour × hours × ₹87 to the dollar
print(f"on demand: ₹{on_demand:,.0f} a month")
print(f"reserved:  ₹{reserved:,.0f} a month")
print(f"saving:    ₹{on_demand - reserved:,.0f} a month, {1 - reserved / on_demand:.0%}")
```

```
on demand: ₹21,759 a month
reserved:  ₹13,871 a month
saving:    ₹7,888 a month, 36%
```

- `0.162 + 0.0564` is the two reserved hourly rates added; times 730 hours and ₹87 gives rupees a month.
- `:.0%` shows a fraction as a whole percentage: 0.36 prints as `36%`.

About ₹7,900 a month, roughly ₹95,000 a year, for a promise to keep both machines for a year. Whether that's a good trade depends on whether the defect model will still run on that server in twelve months: a reservation for a workload that gets redesigned is money spent on nothing.

**The single habit that makes every one of these decisions available rather than accidental:** attach a rough cost estimate to any architecture decision record (Chapter 60, section 60.4) that involves provisioning something new or changing how often something runs. "This will cost approximately ₹X/month, based on Y usage" turns a design conversation that used to end with "we'll see what it costs" into one where cost is weighed against the other trade-offs at the same table, before the decision is made rather than after.

---

## Common mistakes

| Mistake | Symptom | Fix |
|---|---|---|
| Treating cost as an afterthought | Surprise invoices; architecture decisions made with no cost estimate at all | Attach a rough cost estimate to every ADR that provisions or scales something |
| Writing a cost NFR nobody actually costs out | A target like Chapter 60's, off by about 10,000 times once checked | Build the bottom-up model before finalizing the number |
| Confusing average cost with marginal cost | A cost target that's ambiguous about which one it means | State explicitly: fully-loaded, or the cost of the next unit of work |
| Assuming AI spend is the biggest line item | Reviewing the LLM bill while the database, at two-thirds of spend, goes unexamined | Look at the full breakdown before assuming where the money goes |
| No storage tiering on a large archive | Paying hot-tier prices for terabytes nobody's queried in a year | A lifecycle policy, several times cheaper per GB for no engineering cost |
| On-demand pricing for stable, always-on workloads | Paying full rate for a database that's been running unchanged for a year | Reserved pricing once the workload is proven stable |
| Untagged resources | A monthly bill nobody can attribute to a team or a reason | Tag at creation, not as a retrofit project |
| Jumping straight to chargeback | Teams distrust numbers they never got to see and question first | Showback first, build trust in the numbers, chargeback later if needed |
| Charging shared costs to one team's showback report | A precise-looking number that's actually wrong | An honest "shared" category |
| Using the most capable model tier by default | Paying about 5 times more than a task needs | Match model tier to task difficulty, per Chapter 54 |
| Optimizing the cheap part | Effort spent shaving 8 paise of API cost per email while about ₹4.93 of review time per email goes unexamined | Unit economics that include the whole cost, not just the infrastructure slice |

---

## In the real world: the NFR that was off by 10,000 times

When Meera's team assembled the first full monthly cost model for Riverstone's platform — the exercise behind this chapter — the number that stopped the room wasn't a runaway bill. It was Chapter 60's own NFR table, six months old by that point, sitting quietly in the design document everyone had signed off on: *"Cost ceiling: platform cost under ₹0.50 per 1,000 order lines processed."*

Nobody in the original design review had built a cost model to check that number. It had been written the way most early NFRs are written — a plausible-sounding target, stated with appropriate precision (a number, not an adjective, exactly as Chapter 60's own method demanded), and never actually tested against reality because at the time, there was no platform yet to measure.

The real, bottom-up figure came out to ₹5,210.38 per 1,000 order lines — about 10,000 times the original target. Meera's first reaction, by her own account, was to assume she'd made an arithmetic error. She hadn't. At about 7,251 order lines a month, the original NFR allowed the whole platform under ₹4 a month; the database alone — always-on, whether or not a single new order arrived that hour — cost that much in well under an hour.

What made this a genuinely useful finding rather than an embarrassing one was the diagnosis, not just the gap. Working through where the original number could have come from, the team first guessed it had been meant as a **marginal** cost — what one more thousand order lines costs once the platform already exists — rather than the **fully-loaded** figure this chapter's model computed. So they computed the marginal cost too: a few more LLM calls for the PO emails that come with more orders, and nothing else. It came to about ₹12 per 1,000 lines — far closer to ₹0.50 than the fully-loaded figure, but still 24 times over. The original number wasn't a marginal cost either. It was a guess with no stated meaning, which is exactly what an NFR is supposed to replace.

The fix, written up and taken back to the design document:

1. **Two numbers, not one**, explicitly labeled, each with what was measured and what the ceiling is: fully-loaded cost, measured at ₹5,210 per 1,000 lines against a ceiling of ₹6,000 (the number that actually appears on the monthly bill); and marginal cost, measured at ₹12 per 1,000 additional lines against a ceiling of ₹15 (the number that matters when deciding whether to take on more volume).
2. **A monthly review**, tying the cost model to the same cadence as Chapter 63's automation inventory review — cost drifts the same way ownership does, quietly, unless someone keeps checking.
3. **The original NFR's ambiguity flagged explicitly** in the design document's own change log, as a lesson rather than a correction quietly made and forgotten: *"The original cost NFR did not specify fully-loaded vs. marginal cost, and was never checked against a real model before being adopted. See Chapter 65's cost model for the corrected, dual-metric version."*

Anita Rao's reaction, when the finding reached her, was not alarm — Riverstone's actual monthly spend, ₹37,780, was entirely reasonable for what the platform did, and nobody had ever felt the bill was too high. Her question was simpler and more pointed: *"If we'd set a budget alert on the original number, would it have fired on day one?"* It would have — immediately, and every day since, quietly training everyone to ignore it as a false alarm, which is precisely how a genuinely useful budget alert dies.

What made the difference:

- **Someone actually built the model**, rather than trusting a number that had sat unchallenged since it was written.
- **The team diagnosed the ambiguity, not just corrected the number** — understanding *why* the original figure was wrong is what produced a target that will hold up the next time someone checks it.
- **The correction was documented as a lesson**, not smoothed over — a future NFR writer reading this design document's history learns to specify average versus marginal, not just to trust that this particular number is now right.
- **The finding changed a process (monthly review), not just a document** — the same discipline this book has applied to automations (Chapter 63) and models (Chapter 64), now applied to cost.

---

## Project: build and defend a cost model

**Goal:** produce a real, bottom-up monthly cost model for a system you're responsible for, with unit economics and at least one cost-aware recommendation.

### Tools you'll need

- **Python** with `pandas` for cost modelling, the same tool used throughout this book for every other kind of analysis. Tested with Python 3.11 and pandas 3.0.6.
- **Cloud cost tools:** AWS Cost Explorer and Cost and Usage Reports (or the equivalent on any cloud provider) for real tagging and showback at scale; the AWS Pricing Calculator for estimating a new system's cost before building it.
- **The price sheet behind this chapter.** All AWS prices are on-demand list prices for Asia Pacific (Mumbai), `ap-south-1`, before tax, from AWS's public price list files (`pricing.us-east-1.amazonaws.com/offers/v1.0/aws/<service>/current/ap-south-1/index.json`), checked on 29 September 2026. Rupees are at ₹87 to the dollar.

| Item | Unit price (USD) | Source |
|---|---:|---|
| RDS for PostgreSQL, `db.m5.large`, Single-AZ | $0.253 an hour | AmazonRDS price list |
| The same, Multi-AZ | $0.506 an hour | AmazonRDS price list |
| The same, 1-year reserved, no upfront | $0.162 an hour | AmazonRDS price list |
| RDS gp3 storage | $0.131 per GB-month | AmazonRDS price list |
| RDS backup storage beyond the provisioned size | $0.095 per GB-month | AmazonRDS price list |
| EC2 `t3.large`, Linux | $0.0896 an hour | AmazonEC2 price list |
| The same, 1-year reserved, no upfront | $0.0564 an hour | AmazonEC2 price list |
| S3 Standard, first 50 TB | $0.025 per GB-month | AmazonS3 price list |
| S3 Glacier Flexible Retrieval | $0.0045 per GB-month | AmazonS3 price list |
| Data transfer out to the internet, after 100 GB free | $0.1093 per GB | AWSDataTransfer price list |
| LLM, workhorse tier, per million tokens | $2 in, $10 out | Chapter 54, section 54.12 |

- **Companion files (`companion/ch65/`):**
  - `build_ch65_files.py`: builds the cost model from the unit prices above and the invented sizing and volumes stated in sections 65.2 and 65.3.
  - `monthly_cost_model.csv`: all ten cost components, with owner, unit, unit price, quantity, and the monthly cost in dollars and rupees.
  - `unit_economics.csv`: the five unit costs of section 65.3.

**Option A: your own system.** Any platform or pipeline with a real, checkable cloud bill.

**Option B: Riverstone.** Extend `monthly_cost_model.csv` with a plausible eleventh component (a staging environment, monitoring and log storage, or another item from section 65.2's list of what the bill leaves out) and recompute the totals.

**Steps**

1. **List every component** that costs money — compute, storage, requests, transfer — the same inventory discipline as Chapter 63's automation audit, applied to infrastructure.
2. **Find the real unit price for each**, from the provider's current pricing page, not memory — cloud pricing changes, and last year's number is not this year's bill. Write down the date you checked it.
3. **Compute the total monthly cost**, and rank components by share, the way section 65.2 did.
4. **Compute at least three unit-economics figures** relevant to what the system actually does (cost per report, per prediction, per transaction), each with its allocation rule.
5. **If there's an existing cost-related NFR or budget**, check it against your bottom-up model. Does it hold up? If not, diagnose why, the way this chapter's story did, rather than just replacing the number.
6. **Propose one cost-aware architecture change** (storage tiering, reserved pricing, a smaller model tier) with an estimated saving.
7. **Sketch a tagging scheme** that would let this system's cost be attributed honestly to whoever owns each part of it.

**What good looks like:** the total is built bottom-up from real unit prices, not estimated top-down from the current bill; at least one unit-economics figure is genuinely useful for a real future decision; any existing cost target is checked, not assumed correct.

**Stretch goals**

- Model the cost difference between on-demand and reserved pricing for your most stable, always-on component, using real current rates.
- Design a budget alert for your system, and check — honestly — whether it would fire immediately, the way Riverstone's original NFR would have.
- Compare your system's AI/LLM cost against its human-time cost for the same task, per unit, the way section 65.3 compared PO-intake's ₹0.078 of API cost per email against about ₹4.93 of review time per email.

---

## Recap

- **Cloud billing is pay-as-you-go**, metered by compute-hours, storage-gigabyte-months, requests, and data transfer, with reserved pricing available once a workload is stable enough to commit to.
- **The warehouse, not the AI, dominates most real data-platform bills**: Riverstone's RDS compute and storage are two-thirds of its ₹37,780 a month; its two LLM-powered systems combined are under 1%.
- **Storage tiering is a large lever once archives reach terabytes**, several times cheaper per gigabyte for a lifecycle policy that costs nothing further in engineering effort; at Riverstone's size it saves about ₹370 a month.
- **Unit economics turn a total into a decision-ready number**, once you state the allocation rule: 8 paise of LLM cost per PO-intake email, set against about ₹4.93 of review time per email, shows exactly where the real cost — and the real opportunity — actually sits.
- **A cost NFR needs to specify average versus marginal cost explicitly**, or it's not really a checkable number — Chapter 60's original ₹0.50 target was about 10,000 times too low on a fully-loaded basis and 24 times too low even as a marginal cost.
- **Tagging at creation, showback before chargeback, and budget alerts that would actually fire meaningfully** are what turn a shared, anonymous bill into an honest, actionable one.
- **Every architectural choice in this Part has a cost dimension**: storage tiering, reserved compute, scheduled versus event-driven, model tier selection — each worth a rough estimate attached to its ADR, before the decision, not after.

---

## Key terms

FinOps · cloud billing · on-demand pricing · reserved pricing · compute meter · storage meter · request/API meter · data transfer meter · egress · provisioned storage · storage tiering · lifecycle policy · unit economics · allocation rule · fully-loaded cost · marginal cost · tagging · showback · chargeback · budget alert · cost-aware architecture decision

*(All terms are defined in the Glossary, Appendix A.)*

---

## Check yourself

- [ ] You can explain how cloud billing works — the meters, on-demand versus reserved — well enough to estimate a new system's cost before building it.
- [ ] You can build a bottom-up cost model for a real platform and identify its largest cost drivers, without assuming they're the newest or most talked-about component.
- [ ] You compute unit economics that are actually useful for a decision, and you can state the allocation rule behind each one.
- [ ] You check an existing cost target against a real model rather than trusting it because it's already written down.
- [ ] You can tell the difference between average and marginal cost, and specify which one any cost target actually means.
- [ ] You tag resources at creation and use showback before reaching for chargeback.
- [ ] You attach a rough cost estimate to architecture decisions before they're made, not after the bill explains them.

---

## Exercises

Use `companion/ch65/monthly_cost_model.csv` and `unit_economics.csv`.

### Warm-up

1. Name the four meters that drive most cloud bills, and give a one-sentence example of each.
2. What's the difference between on-demand and reserved pricing, and what does an organization give up to get the reserved discount?
3. What's the difference between showback and chargeback, and why does showback usually come first?
4. In your own words, explain the difference between average (fully-loaded) cost and marginal cost, with a non-cloud example.
5. Why might tagging resources at creation be far easier than tagging them a year later?

### Core

6. Reproduce section 65.2's cost breakdown. What are the top three cost components, and what share of the total do they represent together?
7. Riverstone's sensor archive splits into a hot and cold tier. Compute the cost per GB for each tier, and explain why the ratio between them matters more than either number alone.
8. Explain, using this chapter's numbers, why "the AI is expensive" would be the wrong conclusion for anyone reviewing Riverstone's platform bill.
9. Chapter 60's original NFR was off by about 10,000 times. Walk through the diagnosis: what likely caused the gap, and how was the corrected NFR different from simply replacing the number?
10. Compare the cost per PO-intake email (₹0.078) against Chapter 58's ₹197 a day of reviewer time in assisted mode (at about 40 emails a day). What does this comparison tell you about where a future cost-reduction effort should focus?
11. Design a showback breakdown for a hypothetical new team at Riverstone (say, a "customer experience" team using the support assistant). What would you need to tag, and what share of the current bill might reasonably move to them?
12. A colleague proposes switching Riverstone's PO-intake extraction to the most capable available model "to improve accuracy." Using section 65.5 and Chapter 54's pricing, what would you ask before agreeing?

### Stretch

13. Model the reserved-pricing saving for Riverstone's RDS instance and defect-model serving instance combined (₹21,759/month on demand), assuming a 50% reserved discount. What's the annual saving, and what would you need to be confident about before committing to it?
14. Using `build_ch65_files.py` as a template, add an eleventh cost component (a staging environment, monitoring and log storage) and recompute the total and the fully-loaded cost per 1,000 order lines.
15. Design a budget alert for Riverstone's platform that would NOT have fired immediately (unlike the original NFR), using this chapter's real total as your baseline.

### Think about it

16. Is it ever right to accept a much higher cost than an original target, once you understand why the target was wrong, without treating it as a failure? What would you want documented before doing so?
17. A team consistently shows the highest cost in showback and feels unfairly singled out. How would you investigate whether that's a real signal or an artifact of how shared costs are allocated?

---

## Answers

**1.** Compute (billed per hour/second a resource runs — a database instance running continuously); storage (billed per GB-month — a data lake's total stored volume); requests/API calls (billed per call — an LLM API charging per token processed); data transfer (billed per GB leaving the provider's network — serving a dashboard's data to users outside the cloud).

**2.** On-demand charges the full metered rate with no commitment, cancellable anytime. Reserved pricing commits to a usage level for one or three years in exchange for a substantial discount (about 36% for one year and about 61% for three years paid upfront, for this chapter's instances in Mumbai) — the organization gives up the flexibility to simply stop paying if the workload disappears or shrinks.

**3.** Showback reports a team's actual cost back to them without charging it against their budget; chargeback actually bills their cost centre for it. Showback comes first because it builds trust in the numbers and gives teams a chance to act on what they see before facing a financial consequence for costs they may not have understood or agreed to.

**4.** Fully-loaded cost includes all the fixed infrastructure whether or not more work is done — like the total cost of running a restaurant's kitchen for a month, rent and staff included, divided by meals served. Marginal cost is what one more unit costs, given the fixed infrastructure already exists — the cost of the ingredients for one more meal, once the kitchen is already open and staffed for the night.

**5.** Tagging at creation is a single, automatic step built into how a resource gets provisioned. Tagging a year later means someone has to inventory every existing resource, determine its owner after the fact (potentially without documentation), and apply tags retroactively — exactly the kind of shadow-IT discovery problem Chapter 63's automation audit describes, applied to infrastructure instead of automations.

**6.** Warehouse compute (₹16,068), warehouse storage (₹9,118), and then a tie for third between orchestration and defect-model serving (₹5,691 each). The top three lines, counting one of the tied servers, come to ₹30,877, 81.7% of the ₹37,780 total; warehouse compute and storage alone are 66.7%.

**7.** Hot tier: ₹149 ÷ 68.3 GB ≈ ₹2.18 per GB. Cold tier: ₹82 ÷ 208.7 GB ≈ ₹0.39 per GB — about 5.6 times cheaper per gigabyte (the same ratio as the list prices, $0.025 ÷ $0.0045). The ratio matters more than either absolute number because it's what tells you the lifecycle policy is doing real work: every gigabyte that ages into the cold tier gets that 5.6-times saving, and here that's 75% of the archive. Multiply the ratio by the size, though: at 277 GB the whole saving is about ₹370 a month.

**8.** The two LLM-powered systems (PO-intake extraction and the RAG assistant) combine for under 1% of the total monthly bill (₹221 of ₹37,780), and all AI together, including the defect-model server, is 15.6%, while the always-on warehouse alone is 66.7%. A reviewer focused on "the AI is expensive" would be scrutinizing the smallest meaningful line items on the invoice while the largest one — the database everyone assumes is just infrastructure — goes unexamined.

**9.** The original NFR never said whether it meant the fully-loaded cost (which includes the always-on warehouse and orchestration regardless of volume) or the marginal cost of more volume, and nobody priced either. Fully-loaded, it's ₹5,210 per 1,000 lines, about 10,000 times the target; marginal, about ₹12, still 24 times the target. The corrected NFR doesn't just replace the wrong number with the right one — it states both metrics, labels which is which, records what was measured next to each ceiling, and says how often it's checked, so the ambiguity that caused the original error can't recur.

**10.** ₹197 ÷ 40 ≈ ₹4.93 of review time per email, against ₹0.078 of API cost: labour is about 63 times the infrastructure cost. Any future effort to reduce PO-intake's total cost should focus on reducing review time (better extraction confidence, a faster confirmation screen) and on the errors that review misses (Chapter 58's ₹1,530 a day), rather than further optimizing an already-negligible API bill — exactly the finding section 65.3 draws out explicitly.

**11.** Tag the support assistant's infrastructure (or the relevant share of its LLM API calls) with the new team's identifier going forward. A reasonable starting point moves the RAG assistant's line, ₹134 of ₹37,780, about 0.35% of current spend, to the new team, though the real number depends on how usage is actually attributed once the new team's specific queries can be distinguished from existing ones.

**12.** Ask what specific accuracy problem the current model tier is actually causing (a named failure rate on the golden set, not a general worry), and what the price difference is per Chapter 54's table — about 5 times for the frontier tier ($10 and $50 per million tokens against $2 and $10). At Riverstone's volume the frontier month is still small (Chapter 57: about ₹440), so cost alone won't decide it; if there's no measured accuracy problem, the proposal is changing a model that was already working, for a benefit nobody has demonstrated is needed, and it resets every evaluation Chapter 57 set up.

**13.** At a 50% reserved discount, ₹21,759 a month becomes about ₹10,880, a saving of about ₹10,880 a month, ₹1,30,554 a year (about ₹1.31 lakh). At AWS's real one-year, no-upfront rates the discount is 36%, about ₹7,900 a month (section 65.5). Reserved pricing covers the instance-hours only; the gp3 storage is billed the same either way. Before committing, you'd want confidence that both workloads (the warehouse and the defect-model service) will keep running at roughly this size for the full commitment period — reserving capacity for a workload that might be redesigned or retired within the year converts a savings opportunity into a sunk cost.

**14.** Personal/computational exercise using the provided script as a template; check that the new component uses a real, sourced and dated unit price and that the total, the per-line-item shares, and the cost per 1,000 order lines are all recomputed consistently from the updated data, not just re-typed.

**15.** For example, a budget alert set at ₹45,000 a month (about 19% above the current ₹37,780 baseline) would not fire immediately, giving genuine warning room before an actual overrun rather than firing constantly on entirely normal spend — the difference between a budget alert that teaches people to trust it and one that teaches them to ignore it, the same lesson Chapter 20 (section 20.8) taught about alert thresholds generally.

**16.** Yes — when the higher cost is genuinely justified by what was learned (as in this chapter's story, where ₹5,210 per 1,000 lines turned out to be an entirely reasonable fully-loaded figure for a ₹37,780-a-month platform), rather than an excuse to stop scrutinizing spend. What should be documented: the original target, why it was wrong, what the corrected target is and how it's defined, and what would trigger revisiting it again — exactly the change-log entry this chapter's story added to Riverstone's design document.

**17.** Check whether the team's apparent cost includes genuinely shared infrastructure (data transfer, and anything else every team uses) that's been attributed entirely to them rather than split honestly across everyone who benefits from it — Figure 65.3's "shared" category exists precisely to prevent this. Check the allocation rules too: a unit cost or a share depends on the rule chosen (section 65.3). If the shared-cost allocation is fair and the team's number is still highest, investigate whether that reflects real, justified usage (a genuinely heavier workload) before assuming either the team or the accounting is at fault.

---

## Where this leads

- **Chapter 60, Designing Whole Systems:** the NFR this chapter checks, corrects, and documents — the same design document, updated a second time.
- **Chapters 54 and 57 (Part 6):** the LLM price tiers this chapter's AI costs use, and the metered cost per email they're computed from.
- **Chapter 63, Automation Architecture & Governance:** the ownership and inventory discipline this chapter's tagging scheme directly extends to cost.
- **Chapter 66, Data Strategy, Maturity & Building Data Teams:** the business case for platform investment, now backed by a real cost model rather than an estimate.
- **Interview preparation:** the Architecture & Leadership Question Bank asks about cost-aware design directly — "how would you estimate what a proposed system will cost, and how would you check that estimate later" is this chapter's method.
