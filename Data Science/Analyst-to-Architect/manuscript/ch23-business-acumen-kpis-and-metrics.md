# Chapter 23. Business Acumen, KPIs & Metrics

*Part 2 — The Analyst*

> **Chapter at a glance**
>
> **You will learn to:** trace how a business turns cash into stock into sales and back into cash · read a P&L, a balance sheet, and a cash flow statement well enough to hold a conversation with Finance · explain why a profitable company can still run out of money · use the core metrics of sales, marketing, finance, operations, and customer teams, and compute each one correctly · build a KPI tree that decomposes revenue into numbers a team can actually act on · diagnose a revenue change with a disciplined walk down that tree instead of a guess · tell a good metric from a vanity metric, and see how targets corrupt measures · write a metric definition precise enough that two teams get the same number.
>
> **Before you start:** Chapter 3 (bookings, billings, collections, receivables, and what makes a KPI), Chapter 4 (percentages and the arithmetic of business), Chapter 13 (removing duplicate leads, Pattern 3), Chapter 18 (pandas), Chapter 21 (distributions and averages), and Chapter 22 (whether a change is real). Nothing here assumes an accounting or finance background: section 23.2 starts with the words Finance will use.
>
> **Time needed:** 17–20 hours, spread over two weeks, in two parts. Part A, "Money" (sections 23.1–23.4), takes about 8 hours and ends with a checkpoint. Part B, "Metrics that run a business" (sections 23.5–23.13), takes about 10 hours. Allow 2 more for the project.
>
> **Tools:** Python and pandas, set up in Chapters 17 and 18 (any Python from 3.11 on runs every example); this chapter's outputs were checked on Python 3.11 with pandas 3.0.6. A spreadsheet does every ratio in the chapter with one formula each. A calculator, and a willingness to read a financial statement slowly.
>
> **Practice data:** the full Riverstone dataset (`companion/full/`), Chapter 21's delivery file, and `companion/ch23/`: `financials_2025.md` (Riverstone's profit & loss, balance sheet, and cash flow statement for calendar 2025), `monthly_revenue_2025.csv`, `marketing_2025.csv`, and `working_capital_quarters_2025.csv`. Revenue, cost of goods sold, gross margin, and the customer counts come from the real order data and match Chapter 16's 2025 figures. Delivery times come from Chapter 21's delivery file, which is simulated from a documented model because the ERP has no delivery dates. Everything below gross profit on the P&L, the whole balance sheet, the cash flow statement, the quarter-end balances, and the marketing and NPS figures are invented for this chapter, because Riverstone's ERP data has no general ledger, no balance sheet, and no marketing system. Each table says which is which. Run this chapter's notebook from the `companion/ch23/` folder: `"../full/orders.parquet"` means "up one folder, to `companion/`, then into `full`".

---

## Why this matters

Every chapter so far has taught you to get a number right. This chapter teaches you to know which numbers matter, and why.

An analyst who can write a flawless query but doesn't know that a sale isn't cash until it's collected will build a beautiful chart that misses the point of the meeting. An analyst who reports "conversion is up 12%" without asking up against what, over what period, and whether anyone changed the definition halfway through, will get the number believed and the decision wrong. Business acumen is not a soft skill bolted onto the technical ones; it's the thing that tells you which query to write in the first place.

This chapter gives you four things: how to read the three financial statements that describe any company, the standard metrics of the five functions you'll work with most, a method for building and reading a KPI tree, and the judgment to know when a metric is helping and when it's being gamed. Riverstone is used throughout, with its real 2025 sales data and an invented but realistic set of financial statements, so every ratio in this chapter is something you can recompute yourself.

---

## In plain English

Imagine you take over your family's shop for a month while everyone is away. Three things worry you immediately, and they are the three financial statements in disguise.

- **"Am I making money?"** You add up what came in from customers and take away what you spent on stock, rent, and the assistant's wages. That's the **profit & loss statement**: a video of the month.
- **"What do we own, and what do we owe?"** You check the stockroom, the cash box, and the ledger of who owes you and who you owe. That's the **balance sheet**: a photograph taken at the end of the month.
- **"Do I have enough cash to pay the supplier on Friday?"** You might be profitable on paper and still short of cash, if customers haven't paid you yet and the supplier wants payment now. That's the **cash flow statement**, and it's the one that keeps shopkeepers awake at night.

A **metric** is a number you've decided to watch, the way the shopkeeper watches "cash in the box" and "stock on the shelf". A good metric tells you something you can act on. A **KPI tree** is writing down that if takings are low, it's because either fewer customers walked in, or each one bought less — which is exactly how you'd think it through standing behind the counter, just written down so a team can each own one branch.

---

## 23.1 How a business makes money: the cash cycle

Every business that makes or trades goods runs the same cycle: it turns cash into stock, stock into a sale, and a sale back into cash. Riverstone buys raw materials and packaging, turns them into boxes, crates and kitchenware at its two plants, holds them in the warehouse, sells them, and waits to be paid. Analysts who understand this cycle ask better questions than analysts who only understand the tables.

Chapter 3 followed one order from enquiry to cash, and named the money customers still owe **receivables**. The cycle below is the same journey, measured in days for the whole company at once. Three waits make it up:

- **DIO (Days Inventory Outstanding):** how long stock sits, in the plants and the warehouse, before it sells.
- **DSO (Days Sales Outstanding):** how long after a sale it takes to collect the cash. The wait for receivables.
- **DPO (Days Payable Outstanding):** how long the company takes to pay its own suppliers. This wait works *for* the company: until it pays, the supplier is lending it the stock.

Stock arrives, waits DIO days to be sold, and the customer then takes DSO days to pay. That whole stretch, **DIO + DSO**, is the **operating cycle**: from stock bought to cash collected. But the company didn't pay for the stock on day 0; the supplier gave it DPO days. So the company's *own* cash is tied up for less: **cash conversion cycle (CCC) = DIO + DSO − DPO.**

![A timeline from day 0, when stock arrives, to day 97, when the customer pays. Above the line, DIO of 55 days then DSO of 42 days make the 97-day operating cycle. Below it, DPO of 38 days is the supplier's credit, and the remaining 59 days, dashed, are the cash conversion cycle](figures/fig23-1-operating-cycle.svg)

*Figure 23.1 — The cash cycle as a timeline. The day counts are Riverstone's; section 23.3 works them out from its balance sheet. For 59 days the company's own cash sits in stock and unpaid invoices, even though it is profitable.*

A business that's growing fast needs *more* cash tied up in this cycle every month, not less, because next month's stock and receivables are bigger than this month's. That's why "we're profitable but we need a loan" is a completely ordinary sentence, and why an analyst who only looks at the P&L will misread it as a contradiction.

---

## 23.2 The profit & loss statement

The **P&L** (also income statement) covers a period — a month, a quarter, a year — and answers "did we make money, and on what?"

Riverstone's statements in this chapter cover **calendar 2025**, 1 January to 31 December, so that they line up with the order data. (Chapter 16 met India's April–March financial year; these statements don't use it, so this chapter never calls them "FY".)

### Words Finance will use

Finance speaks its own language. These are the words this chapter uses; each gets a Riverstone example.

| Word | Plain meaning | Riverstone example |
|---|---|---|
| **Revenue** (net sales) | What customers are charged for what was sold, after discounts | ₹114.66 crore of non-cancelled 2025 orders |
| **COGS** (cost of goods sold) | What the goods that were sold cost to make or buy | Materials, packaging and factory costs of those boxes |
| **Expense** | Any other cost of running the business; **opex** (operating expenses) is the total | Freight, salaries, rent, marketing |
| **Depreciation** | Spreading the cost of a long-lived asset over its useful years, as a yearly expense | A ₹50 lakh moulding machine expected to last 10 years costs ₹5 lakh a year |
| **Amortisation** | The same idea for assets you can't touch | A software licence bought for five years |
| **Accrual** | Recording a sale when it's made, not when it's paid; costs likewise | A December invoice counts in December's revenue even if paid in February |
| **Asset** | Something the company owns that has value | Cash, stock, machines, money customers owe |
| **Liability** | Something the company owes | Supplier bills, bank loans |
| **Equity** | What's left for the owners: assets − liabilities | The family's stake in Riverstone |
| **Capex** (capital expenditure) | Spending on long-lived assets; it is depreciated over later years, not expensed at once | New warehouse racking |
| **Dividend** | Profit paid out to the owners in cash | The family's share of the year's profit |
| **Leverage** | Using borrowed money to run or grow the business | Riverstone's bank loans |

Accrual is why Chapter 3 kept **booked**, **billed**, and **collected** apart. Revenue on a P&L is billings: a sale counts once it is invoiced, whether or not the cash has been collected. (Riverstone's order data has no invoice dates, so this chapter, like Chapter 16, uses non-cancelled orders as the stand-in for revenue.)

### Reading the P&L by hand

Here is Riverstone's 2025 P&L, top to bottom. Revenue and COGS are real; every line below gross profit is invented for this chapter.

| Line | What it means | Riverstone 2025 |
|---|---|---:|
| **Revenue** (net sales) | What customers were charged, after discounts | ₹114.66 crore |
| **COGS** (cost of goods sold) | What the goods themselves cost | ₹83.18 crore |
| **Gross profit** | Revenue minus COGS; the profit on the product itself | ₹31.48 crore |
| **Gross margin** | Gross profit ÷ revenue | 27.5% |
| **Operating expenses (opex)** | Selling, marketing, admin, depreciation: running the business | ₹14.33 crore |
| **EBIT** (operating profit) | Earnings before interest and tax: profit from operations | ₹17.15 crore |
| **EBIT margin** | EBIT ÷ revenue | 15.0% |
| **Interest** | Cost of borrowed money | ₹1.03 crore |
| **Tax** | Tax on profit (modelled here as a flat 25%) | ₹4.03 crore |
| **PAT** (profit after tax, net profit, "the bottom line") | What's left for the owners | ₹12.09 crore |
| **Net margin** | PAT ÷ revenue | 10.5% |

Walk the first three lines with a calculator, in rupees:

- Revenue ₹1,14,66,41,651 − COGS ₹83,18,03,000 = gross profit **₹31,48,38,651**.
- Gross margin = 31,48,38,651 ÷ 1,14,66,41,651 = 0.2746, or **27.5%**: of every ₹100 a customer pays, ₹27.50 is left after paying for the goods.
- Every line below works the same way: take the next cost away, and divide by revenue to get a margin.

In a spreadsheet it's a two-column sheet: labels in A, amounts in B, and `=B1-B2` for gross profit, `=B3/B1` for gross margin, and so on down.

### The same P&L in Python

A reminder before the code: Python's `,` format groups digits in threes (1,146,641,651), while this book's text writes rupees the Indian way (₹1,14,66,41,651), as Chapter 17 said. Same number. This first cell uses no pandas, just arithmetic.

<!-- py: reset -->
```python
revenue = 1_146_641_651     # net sales, from the order data
cogs = 831_803_000          # cost of the goods sold, from the order data
gross_profit = revenue - cogs
print(f"gross profit ₹{gross_profit:,} = {gross_profit / revenue * 100:.1f}% of revenue")
```

```
gross profit ₹314,838,651 = 27.5% of revenue
```

- **`1_146_641_651`** is how Python lets you write a long number readably: the underscores are ignored, so it's the same as `1146641651`. You can't type commas inside a number (Python would read `1,146` as two numbers).
- **`gross_profit / revenue * 100`** turns the fraction 0.2746 into a percentage, and `:.1f` shows it with one decimal, as in Chapter 17.

The rest of the P&L is one subtraction per line:

```python
selling_dist = 59_625_366    # freight, warehousing, sales salaries and commission
marketing = 20_639_550
admin = 47_012_308           # office, IT, finance and HR
depreciation = 16_052_983    # this year's share of machines, racking and vehicles
opex = selling_dist + marketing + admin + depreciation

ebit = gross_profit - opex
interest = 10_319_775
pbt = ebit - interest        # profit before tax
# tax modelled at a flat 25% of profit, a simplification for this invented P&L
tax = round(pbt * 0.25)
pat = pbt - tax              # profit after tax
print(f"opex ₹{opex:,}   EBIT ₹{ebit:,}   tax ₹{tax:,}   PAT ₹{pat:,}")
```

```
opex ₹143,330,207   EBIT ₹171,508,444   tax ₹40,297,167   PAT ₹120,891,502
```

- The four expense lines add up to **opex**; EBIT is gross profit minus opex.
- **`round(pbt * 0.25)`** is 25% of profit before tax, rounded to whole rupees. Real tax rules are more involved; the comment says the rate is a modelling choice, which is what a comment is for.

Now print the whole statement as a table, each line with its share of revenue:

```python
for label, value in [("Revenue", revenue), ("COGS", -cogs), ("Gross profit", gross_profit),
                     ("Operating expenses", -opex), ("EBIT", ebit), ("Interest", -interest),
                     ("Profit before tax", pbt), ("Tax", -tax), ("Profit after tax", pat)]:
    print(f"{label:<20} ₹{value:>15,}   ({value / revenue * 100:>5.1f}% of revenue)")
```

```
Revenue              ₹  1,146,641,651   (100.0% of revenue)
COGS                 ₹   -831,803,000   (-72.5% of revenue)
Gross profit         ₹    314,838,651   ( 27.5% of revenue)
Operating expenses   ₹   -143,330,207   (-12.5% of revenue)
EBIT                 ₹    171,508,444   ( 15.0% of revenue)
Interest             ₹    -10,319,775   ( -0.9% of revenue)
Profit before tax    ₹    161,188,669   ( 14.1% of revenue)
Tax                  ₹    -40,297,167   ( -3.5% of revenue)
Profit after tax     ₹    120,891,502   ( 10.5% of revenue)
```

- The list holds **(label, value) pairs**, and `for label, value in …` unpacks each pair (Chapter 17). Costs are stored as negative numbers so they print with a minus sign.
- **`{label:<20}`** left-aligns the label in 20 characters. **`{value:>15,}`** right-aligns the number in 15 characters (`>`), with thousands commas (`,`), so the column lines up. **`{…:>5.1f}`** does the same for the percentage, with one decimal.

![A horizontal waterfall of Riverstone's 2025 P&L in rupees crore: revenue 114.7, cost of goods sold minus 83.2, gross profit 31.5, then selling and distribution minus 6.0, marketing minus 2.1, administration minus 4.7, depreciation minus 1.6, EBIT 17.2, interest minus 1.0, tax minus 4.0, and net profit 12.1](figures/fig23-2-pnl-waterfall.svg)

*Figure 23.2 — Riverstone's 2025 P&L. Revenue and COGS are real; everything below gross profit is modelled for this chapter, sized to a plausible mid-sized manufacturer and distributor.*

Three distinctions worth knowing cold:

- **Gross margin versus net margin.** Gross margin (27.5%) is about the product; net margin (10.5%) is about the whole business. A retailer and a software company can have wildly different gross margins and similar net margins, because they spend differently below the line.
- **EBIT versus EBITDA.** **EBITDA** = EBIT + depreciation + amortisation. Like EBIT, it ignores interest and tax; it also ignores how fast assets are written down, which makes it popular for comparing companies with different asset bases. It is not cash profit, and treating it as such is how heavily borrowed, unprofitable companies get described as "healthy". Riverstone's:

```python
ebitda = ebit + depreciation   # Riverstone's depreciation line includes amortisation
print(f"EBITDA ₹{ebitda:,} = {ebitda / revenue * 100:.1f}% of revenue")
```

```
EBITDA ₹187,561,427 = 16.4% of revenue
```

- **Revenue is not cash.** A sale is booked when it's made, not when it's paid for (accrual accounting, the standard for anyone but the smallest business). That single fact is why the next two sections exist.

> **Watch out: percentages of revenue hide absolute size.** "Marketing is 1.8% of revenue" sounds small; it is ₹2.06 crore, hired-analysts'-salaries money. Always look at both the percentage and the rupee figure before deciding something is immaterial.

---

## 23.3 The balance sheet

The **balance sheet** is a snapshot at a single date, here 31 December 2025: what the company owns (**assets**), what it owes (**liabilities**), and the difference, which belongs to the owners (**equity**). It always balances, by definition: **Assets = Liabilities + Equity**.

Assets and liabilities are each split in two. **Current** means cash, or turning into cash (or falling due) within a year; **non-current** means longer-lived, like machines and long-term loans.

```python
# assets
cash = 69_945_141
receivables = 131_942_327              # invoices customers haven't paid yet
inventory = 125_340_178                # stock: materials and finished goods
other_current_assets = 17_199_625
current_assets = cash + receivables + inventory + other_current_assets
property_plant_equipment = 355_458_912   # plants, warehouse, vehicles, after depreciation
other_non_current_assets = 22_932_833
total_assets = current_assets + property_plant_equipment + other_non_current_assets

# liabilities
payables = 86_598_668                  # supplier bills not yet paid
short_term_debt = 97_464_540
other_current_liabilities = 34_399_250
current_liabilities = payables + short_term_debt + other_current_liabilities
long_term_debt = 126_130_582
total_liabilities = current_liabilities + long_term_debt

equity = total_assets - total_liabilities
print(f"total assets       ₹{total_assets:,}")
print(f"total liabilities  ₹{total_liabilities:,}")
print(f"equity             ₹{equity:,}")
print(f"check: liabilities + equity = ₹{total_liabilities + equity:,}  (must equal total assets)")
```

```
total assets       ₹722,819,016
total liabilities  ₹344,593,040
equity             ₹378,225,976
check: liabilities + equity = ₹722,819,016  (must equal total assets)
```

- Each line is one balance-sheet amount; the comments say what the less obvious ones hold. The names are long on purpose: `property_plant_equipment` reads better in six months than `ppe`.
- The totals are plain additions, current items first, then the rest.

Equity is worked out as assets − liabilities, so the check is bound to pass here. In a real balance sheet each side is added up from its own accounts, and the check is how you catch a missing line.

Three ratios read the balance sheet's health:

```python
working_capital = current_assets - current_liabilities
current_ratio = current_assets / current_liabilities
liabilities_to_equity = total_liabilities / equity
print(f"working capital       = current assets − current liabilities = ₹{working_capital:,}")
print(f"current ratio         = current assets ÷ current liabilities = {current_ratio:.2f}")
print(f"liabilities-to-equity = total liabilities ÷ equity = {liabilities_to_equity:.2f}")
```

```
working capital       = current assets − current liabilities = ₹125,964,813
current ratio         = current assets ÷ current liabilities = 1.58
liabilities-to-equity = total liabilities ÷ equity = 0.91
```

| Term | Meaning | Riverstone |
|---|---|---:|
| **Current assets** | Cash, or convertible to cash within a year: cash, receivables, inventory | ₹34.44 crore |
| **Current liabilities** | Due within a year: payables, short-term debt | ₹21.85 crore |
| **Working capital** | Current assets − current liabilities: the cushion for day-to-day operations | ₹12.60 crore |
| **Current ratio** | Current assets ÷ current liabilities: can short-term obligations be met? | 1.58 |
| **Liabilities-to-equity** | Total liabilities ÷ equity: how much of the business is funded by what it owes rather than by the owners | 0.91 |

Why an analyst should care: **receivables and inventory are analyst territory.** Both sit on the balance sheet, both are driven by the operational decisions Chapters 13 and 21 analyze (who gets credit terms, how much stock to hold, how fast orders ship), and both are exactly where a growth story turns into a cash problem. If receivables are growing faster than revenue, customers are being allowed more time to pay, or some of them aren't paying at all (Chapter 14's territory, applied to money owed rather than money already booked).

### Putting days on the cycle

Now the numbers in Figure 23.1 can be worked out. Each "days" measure compares a balance-sheet amount with a year's flow:

> - **DIO = inventory ÷ COGS × 365**
> - **DSO = receivables ÷ revenue × 365**
> - **DPO = payables ÷ COGS × 365**
> - **CCC = DIO + DSO − DPO**
>
> *Inventory, receivables, payables:* year-end balance-sheet amounts. *COGS, revenue:* the year's P&L totals. *365:* days in the year.

Why these pairings? Stock and supplier bills are recorded **at cost**, so they're compared with COGS. Customer invoices are at **selling price**, so receivables are compared with revenue. Dividing a balance by a year's flow gives "the fraction of a year's flow that's sitting there"; multiplying by 365 turns that fraction into days. Strictly, the formulas want the *average* balance over the year; with only a year-end balance sheet, the year-end amount stands in for it.

By hand, for Riverstone:

- DIO = 12,53,40,178 ÷ 83,18,03,000 × 365 = 0.1507 × 365 = **55.0 days**
- DSO = 13,19,42,327 ÷ 1,14,66,41,651 × 365 = 0.1151 × 365 = **42.0 days**
- DPO = 8,65,98,668 ÷ 83,18,03,000 × 365 = 0.1041 × 365 = **38.0 days**
- CCC = 55 + 42 − 38 = **59 days**. The operating cycle, DIO + DSO, is 97 days (stock bought to cash collected); subtract the 38 days suppliers give Riverstone and 59 days is how long *its own* cash is tied up.

In a spreadsheet with the balance sheet in column B, each is one formula, for example `=B_inventory/B_cogs*365` with your own cell addresses. In Python, the variables are already there:

```python
dio = inventory / cogs * 365
dso = receivables / revenue * 365
dpo = payables / cogs * 365
ccc = dio + dso - dpo
print(f"DIO {dio:.1f}   DSO {dso:.1f}   DPO {dpo:.1f} days")
print(f"operating cycle {dio + dso:.1f} days   CCC {ccc:.1f} days")
```

```
DIO 55.0   DSO 42.0   DPO 38.0 days
operating cycle 97.0 days   CCC 59.0 days
```

---

## 23.4 Cash flow: why profit isn't cash

The **cash flow statement** reconciles profit (an accounting figure) with the actual change in the cash balance, in three sections: **operations** (CFO), **investing** (CFI), and **financing** (CFF).

The operations section starts from profit and corrects it, line by line, for everything that moved profit and cash differently. Work it by hand first; the signs are the whole lesson.

| Line | Amount | Sign | Why this sign |
|---|---:|:---:|---|
| Profit after tax | ₹12.09 cr | start | The accounting profit from section 23.2 |
| Depreciation | ₹1.61 cr | + | It was subtracted to get profit, but no cash left this year: the machines were paid for when bought |
| Increase in receivables | ₹0.46 cr | − | Sales were booked in profit but not yet collected |
| Increase in inventory | ₹0.69 cr | − | Cash went into stock that hasn't been sold yet |
| Increase in payables | ₹0.34 cr | + | Supplier bills not yet paid: suppliers are funding us |
| **Cash flow from operations** | **₹12.89 cr** | | 12.09 + 1.61 − 0.46 − 0.69 + 0.34 |

The same in Python, reusing `pat` and `depreciation` from section 23.2:

```python
receivables_increase = 4_586_567      # receivables grew by this much during the year
inventory_increase = 6_879_850
payables_increase = 3_439_925
cfo = pat + depreciation - receivables_increase - inventory_increase + payables_increase

capex = 51_598_874                    # new warehouse racking and plant equipment
cfi = -capex

debt_drawn, dividend, loan_repayment = 22_932_833, 42_312_026, 9_173_133
cff = debt_drawn - dividend - loan_repayment

net_change = cfo + cfi + cff
print(f"Cash flow from operations (CFO): ₹{cfo:,}")
print(f"Cash flow from investing  (CFI): ₹{cfi:,}")
print(f"Cash flow from financing  (CFF): ₹{cff:,}")
print(f"Net change in cash:              ₹{net_change:,}")
print(f"Opening cash = closing cash − net change = ₹{cash - net_change:,}")
```

```
Cash flow from operations (CFO): ₹128,917,993
Cash flow from investing  (CFI): ₹-51,598,874
Cash flow from financing  (CFF): ₹-28,552,326
Net change in cash:              ₹48,766,793
Opening cash = closing cash − net change = ₹21,178,348
```

- `debt_drawn, dividend, loan_repayment = …` gives three variables three values in one line (unpacking, Chapter 17).
- The last line ties the statement to the balance sheet: **opening cash ₹2.12 crore + net change ₹4.88 crore = closing cash ₹6.99 crore**, the `cash` figure in section 23.3. The cash flow statement explains, rupee for rupee, how one balance sheet became the next.

What the three sections hold:

- **CFO (operations):** profit, adjusted for non-cash items (add back depreciation) and for money tied up in working capital (growing receivables and inventory *use* cash; growing payables *frees* it). Riverstone's CFO of ₹12.89 crore is healthily above its PAT of ₹12.09 crore.
- **CFI (investing):** money spent on or raised from long-lived assets — plant machinery, warehouses, vehicles. Almost always negative for a growing company, and that's fine.
- **CFF (financing):** money from or to lenders and owners — loans drawn or repaid, dividends paid. Riverstone's is −₹2.86 crore: it drew a new loan but paid out more in dividend and repayments.

Profit after tax was ₹12.09 crore; cash rose by ₹4.88 crore. The difference is mostly capital spending (₹5.16 crore) and the dividend (₹4.23 crore).

**The single most important habit this section can give you:** when someone says "we made ₹12 crore profit", ask "and how much of that is in the bank?" A company can report a profit and still fail, if that profit is sitting in unpaid invoices and a growing stockroom. A company can report a loss and still be safe, if it's investing heavily in growth that hasn't billed yet. Profit is an opinion; cash is a fact, delayed by exactly the cycle in section 23.1.

### Checkpoint: the end of Part A

Before Part B, check that the statements are yours. Take twenty minutes with a pencil and a calculator. A small invented hardware shop had, for last year: revenue ₹36,50,000; COGS ₹25,55,000; profit after tax ₹2,40,000; depreciation ₹60,000. At the year-end it held inventory ₹3,50,000, receivables ₹3,00,000, and payables ₹2,10,000. During the year receivables rose by ₹50,000, inventory by ₹30,000, and payables by ₹20,000.

1. Work out gross margin, DIO, DSO, DPO, and the cash conversion cycle.
2. Work out cash flow from operations, and say in one sentence why it differs from profit.
3. Check both in Python or a spreadsheet. (Answers at the end of the chapter.)

---

## 23.5 Sales metrics

Sales metrics describe the **pipeline**: the journey from a lead to a paying customer. Riverstone's CRM has real, if small, pipeline data for 2025: one table of leads and one of every stage each lead reached. Start by loading both and looking at them.

```python
import pandas as pd

leads = pd.read_parquet("../full/leads.parquet")
hist = pd.read_parquet("../full/lead_stage_history.parquet")
print(len(leads), "lead rows")
print(hist.head())
print(hist["stage"].value_counts())
```

```
43 lead rows
   lead_id      stage          entered_at
0        1        New 2025-04-07 15:20:00
1        1  Contacted 2025-04-13 19:20:00
2        2        New 2025-06-12 14:20:00
3        2  Contacted 2025-06-22 18:20:00
4        2     Quoted 2025-06-29 19:20:00
stage
New          43
Contacted    22
Quoted       14
Won           6
Lost          4
Name: count, dtype: int64
```

- **`.head()`** shows the first five rows, and **`value_counts()`** counts each stage (Chapter 18).
- `hist` has one row per lead per stage reached, with the date it got there (`entered_at`). Lead 2 reached New, then Contacted, then Quoted.
- The counts say 43 leads were New. But Chapter 13 (Pattern 3) found that 13 of those rows are the same enquiry submitted again from the website. Count them before counting anything else.

Remove the duplicates the way Chapter 13 did: match on the email address in lower case, and keep each email's first submission.

```python
leads["email_key"] = leads["email"].str.lower()
first = leads.sort_values(["created_at", "lead_id"]).drop_duplicates("email_key")
print(len(leads), "rows,", len(first), "real enquiries")
```

```
43 rows, 30 real enquiries
```

- **`.str.lower()`** makes a lower-case copy of every email, so `Ravi@Example.com` and `ravi@example.com` match (Chapter 18).
- **`.sort_values(["created_at", "lead_id"])`** puts the earliest submission first; **`.drop_duplicates("email_key")`** then keeps the first row for each email and drops the rest. It's the pandas version of Chapter 13's `ROW_NUMBER() … = 1`.

Now count how many real enquiries reached each stage:

```python
real = hist[hist["lead_id"].isin(first["lead_id"])]
reached = real.groupby("stage")["lead_id"].nunique()
reached = reached.reindex(["New", "Contacted", "Quoted", "Won", "Lost"])
print(reached)
```

```
stage
New          30
Contacted    22
Quoted       14
Won           6
Lost          4
Name: lead_id, dtype: int64
```

- **`isin(first["lead_id"])`** keeps only the stage rows of real enquiries.
- **`groupby("stage")["lead_id"].nunique()`** counts distinct leads at each stage, so a lead quoted twice would still count once.
- **`.reindex([...])`** puts the rows in the order you list, here the funnel's order, instead of alphabetical order. (Lost isn't a step down the funnel; it's where a quoted deal ends when the customer says no.)

Two win rates, and they answer different questions:

```python
won, lost, new = reached["Won"], reached["Lost"], reached["New"]
print(f"win rate (won ÷ (won + lost))  = {won / (won + lost) * 100:.1f}%")
print(f"win rate (won ÷ all enquiries) = {won / new * 100:.1f}%")
```

```
win rate (won ÷ (won + lost))  = 60.0%
win rate (won ÷ all enquiries) = 20.0%
```

The first says how often Riverstone wins a deal that reaches a decision; the second, how many enquiries end as customers. Neither is wrong. Say which one you mean.

The **sales cycle** is the days from a lead's creation (its New date) to its Won date. Build it in small steps: one small table of Won dates, one of New dates, then join them.

```python
won_dates = real[real["stage"] == "Won"][["lead_id", "entered_at"]]
won_dates = won_dates.rename(columns={"entered_at": "won_at"})
new_dates = real[real["stage"] == "New"][["lead_id", "entered_at"]]
new_dates = new_dates.rename(columns={"entered_at": "created"})
cycle = won_dates.merge(new_dates, on="lead_id")
cycle["days"] = (cycle["won_at"] - cycle["created"]).dt.days
print(cycle)
print(f"won deals {len(cycle)}   mean {cycle['days'].mean():.1f} days", end="   ")
print(f"median {cycle['days'].median():.1f} days")
```

```
   lead_id              won_at             created  days
0        7 2025-07-23 23:50:00 2025-06-17 17:50:00    36
1       12 2025-12-04 19:50:00 2025-11-02 09:50:00    32
2       13 2025-04-29 18:05:00 2025-04-03 11:05:00    26
3       23 2025-07-26 14:35:00 2025-07-04 09:35:00    22
4       25 2025-09-29 20:20:00 2025-09-13 12:20:00    16
5       39 2025-10-25 18:50:00 2025-10-04 14:50:00    21
won deals 6   mean 25.5 days   median 24.0 days
```

- **`.rename(columns={...})`** gives the two date columns different names, so they don't clash after the join.
- **`merge(..., on="lead_id")`** lines each Won date up with the same lead's New date (Chapter 18).
- Subtracting two dates gives a time difference; **`.dt.days`** turns it into whole days.
- **`end="   "`** makes `print` finish with three spaces instead of a new line, so the next `print` continues the same line. It keeps each line of code short.
- With only six won deals, 25.5 days is **indicative**, not a firm figure (Chapter 22): one more slow deal would move it a lot.

Last, where the real enquiries came from:

```python
print(first["source"].value_counts())
```

```
source
Website              14
Trade fair            5
Referral              5
Cold call             3
IndiaMART listing     3
Name: count, dtype: int64
```

| Metric | Formula | Riverstone 2025 | Watch for |
|---|---|---|---|
| **Pipeline value** | Sum of open deals' expected value | — (not tracked yet) | Stale deals inflate it; age the pipeline |
| **Win rate** | Won ÷ (Won + Lost) | **60%** (6 of 10 decided) | Won ÷ *all* enquiries (20%) is a different, also-useful number — say which one |
| **Sales cycle** | Days from lead created (New) to Won | **25.5 days** mean, 24 median (6 deals) | Skewed by a few very slow deals; report the median and the count too |
| **Conversion by stage** | Share of enquiries reaching each stage | New 100% → Contacted 73% → Quoted 47% → Won 20% | The stage with the biggest drop is where to invest |
| **Average order value (AOV)** | Revenue ÷ orders | ₹24,735.56 (Chapter 16) | Mean is pulled up by large Wholesale orders (Chapters 15 and 21) |
| **Quota attainment** | Actual ÷ target, per rep or team | 98.3% company-wide (Chapter 16) | An average hides reps far above and far below target |

Why is Chapter 21's mean order value (₹24,839.53) not the AOV above? Chapter 16's AOV counts all 46,356 non-cancelled 2025 orders; Chapter 21's delivery file keeps only the 45,040 that were delivered. Same business, different populations: always state which one you used.

Nearly half of Riverstone's 30 real enquiries (14) came through the website. In the raw table the website looks bigger, 27 of 43 rows, because all 13 duplicates were website resubmissions: counting rows would have credited the website with 13 enquiries that never happened, and cut the all-enquiries win rate from 20% to 14%. That is a small, informal pipeline, where the "sales cycle" for a self-serve reorder from an existing account (which never touches this CRM at all) is a completely different, much shorter process. **A metric only describes what it measures**, and most of Riverstone's revenue comes from repeat orders that never enter a pipeline stage.

---

## 23.6 Marketing metrics

The marketing file is invented for this chapter (Riverstone's ERP has no marketing system): one row per month of 2025.

```python
mk = pd.read_csv("marketing_2025.csv")
print(mk[["month", "leads", "marketing_spend", "new_customers", "cac", "roas"]])
print(f"\ntotal leads      {mk['leads'].sum():,}")
print(f"total spend      ₹{mk['marketing_spend'].sum():,}")
print(f"new customers    {mk['new_customers'].sum():,}")
print(f"blended CAC      ₹{mk['marketing_spend'].sum() / mk['new_customers'].sum():,.0f}")
print(f"average ROAS     {mk['attributed_revenue'].sum() / mk['marketing_spend'].sum():.1f}x")
```

```
      month  leads  marketing_spend  new_customers      cac  roas
0   2025-01    420           518896             49  10590.0  4.36
1   2025-02    390           484256             53   9137.0  5.56
2   2025-03    470           525922             75   7012.0  7.37
3   2025-04    510           554956             65   8538.0  5.52
4   2025-05    480           522505             74   7061.0  5.42
5   2025-06    340           377585             39   9682.0  4.80
6   2025-07    300           341529             46   7425.0  5.18
7   2025-08    410           485093             64   7580.0  5.80
8   2025-09    560           661445             77   8590.0  5.53
9   2025-10    690           693425             84   8255.0  5.51
10  2025-11    640           669940             90   7444.0  6.35
11  2025-12    460           449210             56   8022.0  6.22

total leads      5,670
total spend      ₹6,284,762
new customers    772
blended CAC      ₹8,141
average ROAS     5.7x
```

- **`cac`** in each row is that month's spend ÷ new customers; **`roas`** is the revenue marketing is credited with ÷ spend. The totals below the table recompute both for the whole year.
- **Blended CAC** divides the year's total spend by the year's total new customers. It is not the average of the twelve monthly CACs, for the reason Chapter 21 gave about averaging averages.

Where does 5,670 "leads" come from, when section 23.5 counted 30? The marketing file's leads are **enquiries captured by campaigns**: form fills, calls to the campaign number, cards from the trade fair. Only 30 real enquiries were ever entered into the sales CRM. The gap between the two systems is itself a finding: most enquiries never reach a sales stage, and nobody can say what happened to them. (The 772 new customers are real, though: they're the customers who first ordered in 2025, counted in section 23.9.)

| Metric | Formula | Riverstone 2025 | Watch for |
|---|---|---|---|
| **The funnel** | Impressions → clicks → leads → customers | 5,670 campaign leads → 772 new customers | Report the rate *between* each stage, not just the ends |
| **CAC** (customer acquisition cost) | Marketing spend ÷ new customers | **₹8,141** | Excludes sales salaries and time; a "fully loaded" CAC includes them and is always higher |
| **ROAS** (return on ad spend) | Attributed revenue ÷ spend | **5.7x**, monthly range 4.4–7.4x | Revenue attributed to marketing is a judgment call, not a fact (next paragraph) |
| **Payback period** | CAC ÷ monthly gross profit per new customer | 2.3 months (section 23.9) | Long paybacks strain cash even when the unit economics work |

**Attribution is the honest weak point of every marketing metric.** When a customer sees an ad, visits the website, gets a call from a rep, and orders three months later, which channel "caused" the sale? Common models — **last-touch** (credit the final interaction), **first-touch** (credit the first), and **multi-touch** (split credit across all of them) — can each tell a defensibly different story from the same data, and none is simply correct in an absolute sense. State the model whenever you report CAC or ROAS, the way you'd state units.

> **Watch out: CAC and LTV need the same population.** CAC is measured on the customers marketing actually brought in *this year*. Comparing it against the lifetime value of the whole customer base — which includes decades-old accounts marketing never touched — silently compares two different populations. Section 23.9 shows the fix.

---

## 23.7 Finance metrics

Most of these appeared already; here they're gathered as the vocabulary Finance will use with you. The variables from sections 23.2 and 23.3 are still in the notebook, so nothing is typed twice. (If you restarted, run those cells again first.)

```python
print(f"gross margin          {gross_profit / revenue * 100:.1f}%")
print(f"EBIT margin           {ebit / revenue * 100:.1f}%")
print(f"net margin            {pat / revenue * 100:.1f}%")
print(f"cash conversion cycle {ccc:.0f} days")
print(f"return on assets      {pat / total_assets * 100:.1f}%")
print(f"return on equity      {pat / equity * 100:.1f}%")
```

```
gross margin          27.5%
EBIT margin           15.0%
net margin            10.5%
cash conversion cycle 59 days
return on assets      16.7%
return on equity      32.0%
```

| Metric | Formula | Meaning |
|---|---|---|
| **Gross margin** | Gross profit ÷ revenue | How much of each rupee survives the cost of the product |
| **Contribution margin** | (Revenue − all variable costs) ÷ revenue | What's left to cover fixed costs and profit, per unit sold |
| **EBIT / net margin** | Explained in section 23.2 | Operating and overall profitability |
| **DSO / DPO / DIO / CCC** | Section 23.3 | How long cash is tied up |
| **Return on assets (ROA)** | Net profit ÷ total assets | How efficiently assets generate profit |
| **Return on equity (ROE)** | Net profit ÷ equity | The return the owners are earning on their stake |

**Fixed versus variable costs** is worth a moment. A **fixed cost** (rent, most salaries) doesn't change with volume in the short run; a **variable cost** (materials, packaging, commission) scales with each unit. Contribution margin, not gross margin, is what tells you whether taking one more order is worth it. Usually contribution margin is *lower* than gross margin, because variable selling costs like freight and commission come off too. But it can be higher, when COGS includes fixed costs (like factory overhead allocated per unit) that don't actually change if you make one more crate.

---

## 23.8 Operations metrics

Chapter 21's delivery file (simulated from a documented model, since the ERP has no delivery dates) already contains the standard logistics metrics.

```python
deliveries = pd.read_csv("../ch21/delivery_times_2025.csv")

# "in full" is assumed here: the file has no partial-shipment data
otif = deliveries["on_time"].mean()
print(f"On-Time In Full (OTIF), proxy         : {otif*100:.1f}%")
print(deliveries.groupby("branch")["on_time"].mean().mul(100).round(1))
print(f"\nmedian delivery time                  : {deliveries['delivery_days'].median():.1f} days")
print(f"orders delivered                      : {len(deliveries):,}")
```

```
On-Time In Full (OTIF), proxy         : 81.8%
branch
Bengaluru    78.0
Delhi        80.0
Kolkata      68.1
Mumbai HO    90.8
Name: on_time, dtype: float64

median delivery time                  : 3.8 days
orders delivered                      : 45,040
```

| Metric | Formula | Riverstone 2025 | Notes |
|---|---|---|---|
| **OTIF** (on-time, in-full) | Orders delivered on time and complete ÷ total | **81.8%** (on-time only; "in full" isn't tracked) | The two failure modes are different problems; measure both if you can |
| **Inventory turns** | COGS ÷ inventory (year-end, as a proxy for the average) | ₹83.18 cr ÷ ₹12.53 cr ≈ **6.6 times a year** | Turns and DIO are the same idea: 365 ÷ 6.6 = 55 days. Too high risks stockouts; too low ties up cash (section 23.1) |
| **Fill rate** | Units shipped ÷ units ordered | — (not tracked) | Distinct from OTIF: a full but late order fails OTIF, not fill rate |
| **OEE** (Overall Equipment Effectiveness) | Availability × performance × quality | — (plant data not in this dataset; applies to the Taloja and Chakan plants) | The standard machine measure in manufacturing; each of the three factors is itself worth decomposing |

Kolkata's 68.1% OTIF against Mumbai HO's 90.8% is the same finding as Chapter 21, restated in the vocabulary operations teams use in every industry. That repetition is the point: **the underlying skill — profile the distribution, don't just report the average — is the same whether you call the measure "delivery time" or "OTIF".**

---

## 23.9 Customer metrics

Customer metrics start from one question: which customers bought in each year? Read the order lines once and look at the dates they cover.

```python
items = pd.read_parquet("../full/order_items.parquet")
orders = pd.read_parquet("../full/orders.parquet")
lines = items.merge(orders, on="order_id")
lines["net_revenue"] = lines["quantity"] * lines["unit_price"] * (1 - lines["discount_pct"] / 100)
first_day, last_day = lines["order_date"].min().date(), lines["order_date"].max().date()
print(len(lines), "order lines, from", first_day, "to", last_day)
```

```
209006 order lines, from 2023-01-01 to 2025-12-28
```

- The merge gives each order line its order's date, status and customer. `net_revenue` is quantity × price, less the discount, as in Chapter 18.
- **`.min()`** and **`.max()`** find the earliest and latest order dates; **`.date()`** drops the time of day, which is always midnight here.
- The data runs from 2023 to the end of 2025, so every year needs **both** a start and an end date.

Now the two years' non-cancelled sales, each with a start date and an end date:

```python
not_cancelled = lines[lines["status"] != "Cancelled"]
dates = not_cancelled["order_date"]
in_2024 = (dates >= "2024-01-01") & (dates < "2025-01-01")
in_2025 = (dates >= "2025-01-01") & (dates < "2026-01-01")
sales_2024 = not_cancelled[in_2024]
sales_2025 = not_cancelled[in_2025]
print(len(sales_2024), "lines in 2024;", len(sales_2025), "lines in 2025")
```

```
68498 lines in 2024; 83444 lines in 2025
```

- Each year is **`>=` its first day and `<` the next year's first day**. That catches every moment of 31 December, whether dates carry times or not, and would keep any 2026 rows out if the file grew.
- `dates` is just a short name for the date column, so the two mask lines stay readable.
- The two masks `in_2024` and `in_2025` are Boolean Series (Chapter 18), combined with `&`.

Sets of customers answer the retention questions directly (Chapter 17: `&` is "in both", `-` is "in the first but not the second"):

```python
customers_2024 = set(sales_2024["customer_id"])
customers_2025 = set(sales_2025["customer_id"])
retained = customers_2024 & customers_2025   # bought in both years
churned = customers_2024 - customers_2025    # bought in 2024, not in 2025
new = customers_2025 - customers_2024        # bought in 2025, not in 2024
retention = len(retained) / len(customers_2024)
print(f"active 2024: {len(customers_2024):,}   active 2025: {len(customers_2025):,}")
print(f"retained: {len(retained):,}   churned: {len(churned):,}   new: {len(new):,}")
print(f"retention rate: {retention*100:.1f}%   churn rate: {(1-retention)*100:.1f}%")
```

```
active 2024: 4,104   active 2025: 4,599
retained: 3,827   churned: 277   new: 772
retention rate: 93.3%   churn rate: 6.7%
```

The counts reconcile both ways: 3,827 retained + 277 churned = 4,104 active in 2024, and 3,827 retained + 772 new = 4,599 active in 2025.

What is a new customer worth in their first year? Filter to new customers' 2025 sales, add up each customer's revenue, then average:

```python
new_sales = sales_2025[sales_2025["customer_id"].isin(new)]
revenue_per_new = new_sales.groupby("customer_id")["net_revenue"].sum()
print(revenue_per_new.head(3))
first_year_revenue = revenue_per_new.mean()
print(f"average first-year revenue of {len(revenue_per_new):,} new customers:", end=" ")
print(f"₹{first_year_revenue:,.0f}")
```

```
customer_id
2    174147.50
6     47673.75
7    353088.50
Name: net_revenue, dtype: float64
average first-year revenue of 772 new customers: ₹157,617
```

Now lifetime value and its comparison with CAC. CAC comes from the marketing file in section 23.6, not typed in:

```python
gross_margin = 0.275        # section 23.2's gross margin, rounded to 27.5%
horizon_years = 5           # capped lifetime: see the Watch out below
churn_rate = 1 - retention
cac = mk["marketing_spend"].sum() / mk["new_customers"].sum()

ltv = first_year_revenue * gross_margin * horizon_years
naive_ltv = first_year_revenue * gross_margin / churn_rate   # 1 ÷ churn = years of "lifetime"
print(f"LTV ({horizon_years}-year horizon, {gross_margin*100:.1f}% margin): ₹{ltv:,.0f}")
print(f"naive LTV (1 ÷ churn = {1/churn_rate:.1f} years):   ₹{naive_ltv:,.0f}")
print(f"CAC: ₹{cac:,.0f}   LTV:CAC = {ltv/cac:.1f} : 1   (naive {naive_ltv/cac:.1f} : 1)")
```

```
LTV (5-year horizon, 27.5% margin): ₹216,723
naive LTV (1 ÷ churn = 14.8 years):   ₹642,189
CAC: ₹8,141   LTV:CAC = 26.6 : 1   (naive 78.9 : 1)
```

And the **payback period**: how many months of a new customer's gross profit it takes to earn back their CAC.

```python
monthly_gross_profit = first_year_revenue * gross_margin / 12
print(f"monthly gross profit per new customer: ₹{monthly_gross_profit:,.0f}")
print(f"payback = CAC ÷ monthly gross profit = {cac / monthly_gross_profit:.1f} months")
```

```
monthly gross profit per new customer: ₹3,612
payback = CAC ÷ monthly gross profit = 2.3 months
```

| Metric | Formula | Riverstone 2025 | Watch for |
|---|---|---|---|
| **Retention rate** | Customers active in both periods ÷ active in the first | **93.3%** | High for B2B supply: switching suppliers has real friction |
| **Churn rate** | 1 − retention | **6.7%** | Small percentages compound: 1 − 0.933⁵ = 0.29, so 6.7% a year loses nearly a third (29%) of the base in five years |
| **LTV** (customer lifetime value) | Annual revenue × gross margin × customer lifetime | **₹2.17 lakh** (5-year horizon) | Never use the uncapped 1/churn lifetime (14.8 years here) — see below |
| **LTV : CAC** | LTV ÷ CAC | **26.6 : 1** | A widely quoted rule of thumb calls 3:1 or more healthy; this one is unusually high (next paragraph) |
| **Payback period** | CAC ÷ monthly gross profit per new customer | **2.3 months** | Long paybacks strain cash even when LTV:CAC looks good |
| **NPS** (Net Promoter Score) | % promoters (score 9–10) − % detractors (0–6), from a 0–10 "would you recommend us?" question | **+34** (quarterly survey, invented) | A single number from one question; see the caution below |

One caveat on the LTV: new customers arrived all through 2025, so "first-year revenue" covers about six and a half months on average, not twelve. That understates a full year's value, so the true LTV is probably higher. A cohort view (exercise 22) fixes it by following each quarter's new customers for a full year.

> **Watch out: the naive LTV formula overclaims.** "LTV = annual value × margin × (1 ÷ churn rate)" gives Riverstone a 14.8-year customer lifetime and an LTV of ₹6.42 lakh — nobody should plan around fourteen years of an unproven assumption holding. **Cap the horizon** and say so; this chapter uses five years. The 5-year-capped LTV here (₹2.17 lakh) is a third of the naive figure, and it's the one to defend in a meeting.

Riverstone's LTV:CAC of 26.6:1 is far above the "3:1 is healthy" rule of thumb (it comes from subscription software, where it's used to judge whether acquisition spending pays back), and a good analyst treats a suspiciously good number the same way as a suspiciously bad one (Chapter 22): check it before repeating it. Here it holds up, and it has a real explanation — B2B supply relationships are sticky, switching costs are high, and a customer's *first* order is small relative to what they buy once trust is established — but it also suggests Riverstone could profitably spend far more on acquiring customers than it currently does. Not every extreme number is an error; some are the actual finding.

**NPS's blind spot:** it collapses ten points of opinion, from many different customers, into one number. A promoter (9–10) and a detractor (0–6) each disappear into a bucket that says nothing about *why*, and identical NPS scores can hide completely different underlying distributions (a company with everyone at 7 versus a company split evenly between 10s and 3s can score similarly). Use it as a trend, watch the *comments* that come with it, and never let it stand alone as "customer health".

---

## 23.10 KPI trees and the North Star

A **KPI tree** decomposes one headline number into the factors that multiply or add together to produce it, until each branch is small enough that one team can own it. Chapter 3 drew a small one for collections; here is a full one for Riverstone's profit.

![A tree with gross profit (₹31.5 crore) at the top, equal to revenue times gross margin (27.5%). Revenue (₹114.7 crore) splits into active customers (4,599), orders per customer (10.08 a year) and average order value (₹24,735.56), multiplied. Active customers is retained (3,827, which is 4,104 active in 2024 minus 277 churned) plus new (772); average order value is units per order (53.75) times net price per unit (₹460.16)](figures/fig23-3-kpi-tree.svg)

*Figure 23.3 — Riverstone's 2025 profit tree. Each box multiplies or adds to give the box above it, exactly; each first-level branch is owned by a different function, and the second level is where a diagnosis (section 23.11) usually lands.*

Check the revenue branch on the real data, with every factor computed rather than typed:

```python
active_customers = len(customers_2025)
orders_2025 = sales_2025["order_id"].nunique()
revenue_2025 = sales_2025["net_revenue"].sum()
orders_per_customer = orders_2025 / active_customers
aov = revenue_2025 / orders_2025
print(f"active customers        {active_customers:,}")
print(f"orders per customer     {orders_per_customer:.2f}")
print(f"average order value     ₹{aov:,.2f}")
print(f"customers × freq × AOV  ₹{active_customers * orders_per_customer * aov:,.2f}")
print(f"actual 2025 revenue     ₹{revenue_2025:,.2f}")
```

```
active customers        4,599
orders per customer     10.08
average order value     ₹24,735.56
customers × freq × AOV  ₹1,146,641,651.25
actual 2025 revenue     ₹1,146,641,651.25
```

The identity **Revenue = Active customers × Orders per customer × Average order value** holds exactly, and it's worth seeing why: orders per customer is orders ÷ customers, and AOV is revenue ÷ orders, so C × (O ÷ C) × (R ÷ O) = R — the customers and orders cancel. (Round AOV to the paisa first and the product drifts by a few rupees; compute from the totals.) That's what makes the tree useful: every rupee of revenue change must show up as a change in one or more of those three factors. Each of those, in turn, decomposes further: active customers this year are the retained customers plus the new ones (and retained customers are last year's active customers minus the churned ones); average order value is units per order times the average net price per unit. Put gross margin on top and the same tree explains gross profit: gross profit = revenue × gross margin.

**Choosing a North Star metric.** Some companies also name one **North Star metric**: a single number, upstream of revenue, that captures whether the business is delivering value (a marketplace might track completed transactions; Riverstone might track active customers, since a customer who orders at all tends to become a repeat one). A North Star is a communication tool, not a replacement for the tree — it's the one branch senior leadership watches weekly, while the rest of the tree stays with the teams that own it.

**Building one for your own business**, in order:
1. Write the headline number as a **product or sum** of measurable factors — not a vague list, an actual formula that reconstructs the total.
2. Check the identity holds on real data, as above. If it doesn't, a factor is missing or miscounted.
3. Decompose each factor one more level, stopping when a branch is something one team can move without needing another team's help.
4. Name an owner for each branch. A branch with no owner is a fact, not a KPI.

---

## 23.11 Diagnosing a change

Riverstone's revenue fell from ₹8.72 crore in May 2025 to ₹5.20 crore in June — a genuine, well-documented seasonal trough (Chapters 11 and 15). Rather than reporting "revenue fell 40%", walk it down the tree.

Write C for customers, F for orders per customer, and A for average order value, with 0 for May and 1 for June. Revenue is C × F × A. Change one factor at a time, in order, keeping the ones already changed at their June value:

> - **Customer effect** = (C₁ − C₀) × F₀ × A₀
> - **Frequency effect** = C₁ × (F₁ − F₀) × A₀
> - **AOV effect** = C₁ × F₁ × (A₁ − A₀)

Add the three and the terms cancel, leaving C₁F₁A₁ − C₀F₀A₀: June's revenue minus May's, exactly. Work the first one by hand, with May's F₀ = 3,658 ÷ 2,885 = 1.268 orders per customer and A₀ = ₹23,851.71:

- Customer effect = (2,723 − 2,885) × 1.268 × ₹23,851.71 = −162 × 1.268 × ₹23,851.71 ≈ **−₹49.0 lakh**.

Now all three in Python, from the monthly file:

```python
monthly = pd.read_csv("monthly_revenue_2025.csv", index_col="month")
may, jun = monthly.loc["2025-05"], monthly.loc["2025-06"]
c0 = int(may["customers"])                  # C: customers
f0 = may["orders"] / c0                     # F: orders per customer
a0 = may["net_revenue"] / may["orders"]     # A: average order value
c1 = int(jun["customers"])
f1 = jun["orders"] / c1
a1 = jun["net_revenue"] / jun["orders"]

customer_effect = (c1 - c0) * f0 * a0
frequency_effect = c1 * (f1 - f0) * a0
aov_effect = c1 * f1 * (a1 - a0)
print(f"May:  {c0:,} customers × {f0:.3f} orders/cust × ₹{a0:,.2f} AOV", end=" ")
print(f"= ₹{may['net_revenue']:,.0f}")
print(f"June: {c1:,} customers × {f1:.3f} orders/cust × ₹{a1:,.2f} AOV", end=" ")
print(f"= ₹{jun['net_revenue']:,.0f}")
print(f"\nEffect of fewer customers:        ₹{customer_effect:,.0f}")
print(f"Effect of fewer orders/customer:  ₹{frequency_effect:,.0f}")
print(f"Effect of lower average order:    ₹{aov_effect:,.0f}")
print(f"Sum of effects:                   ₹{customer_effect + frequency_effect + aov_effect:,.0f}")
print(f"Actual change:                    ₹{jun['net_revenue'] - may['net_revenue']:,.0f}")
```

```
May:  2,885 customers × 1.268 orders/cust × ₹23,851.71 AOV = ₹87,249,568
June: 2,723 customers × 1.190 orders/cust × ₹16,040.89 AOV = ₹51,972,483

Effect of fewer customers:        ₹-4,899,282
Effect of fewer orders/customer:  ₹-5,070,734
Effect of lower average order:    ₹-25,307,069
Sum of effects:                   ₹-35,277,085
Actual change:                    ₹-35,277,085
```

- The six lines set C, F and A for May (`0`) and June (`1`), exactly as in the formulas above.
- **`index_col="month"`** makes the month the row label, so **`monthly.loc["2025-05"]`** picks May's row by name (Chapter 18). Each of `may` and `jun` is then one row, read by column name. Because the row mixes whole numbers and decimals, pandas stores them all as decimals; **`int()`** turns the customer count back into a whole number (Chapter 17), so it prints as 2,885 rather than 2,885.0.

![A chain-linked bridge from May 2025's ₹8.72 crore down through three effects to June's ₹5.20 crore: fewer customers minus ₹0.49 crore, fewer orders per customer minus ₹0.51 crore, and lower average order value minus ₹2.53 crore, the largest bar](figures/fig23-4-root-cause.svg)

*Figure 23.4 — The May → June revenue bridge. Fewer customers and fewer orders each cost a little; a lower average order value cost the most.*

This is a **chain-linked (sequential) decomposition**: each effect is measured holding the factors already accounted for at their new value and the rest at the old value, so the three effects sum to the total change exactly, with no leftover residual to explain away. The order you substitute in changes each individual effect. Try it the other way round, AOV first:

```python
aov_first = c0 * f0 * (a1 - a0)
frequency_second = c0 * (f1 - f0) * a1
customer_last = (c1 - c0) * f1 * a1
print(f"AOV ₹{aov_first:,.0f}   frequency ₹{frequency_second:,.0f}", end="   ")
print(f"customers ₹{customer_last:,.0f}")
print(f"sum ₹{aov_first + frequency_second + customer_last:,.0f}")
```

```
AOV ₹-28,571,993   frequency ₹-3,613,082   customers ₹-3,092,010
sum ₹-35,277,085
```

Each effect moves, but the total doesn't. AOV is still by far the largest effect: 72% of the fall one way, 81% the other. So the story doesn't depend on the order here. When it does, say which order you used. In a spreadsheet the bridge is three rows, one per formula above, and a fourth that adds them.

Before believing "the same customers placed smaller orders", check whether the *mix* changed: did June's orders come from a different blend of segments? Count May's and June's orders by customer segment:

```python
customers = pd.read_parquet("../full/customers.parquet")
may_june = orders[(orders["status"] != "Cancelled")
                  & (orders["order_date"] >= "2025-05-01") & (orders["order_date"] < "2025-07-01")]
may_june = may_june.merge(customers[["customer_id", "segment"]], on="customer_id")
month = may_june["order_date"].dt.strftime("%Y-%m")
print((pd.crosstab(month, may_june["segment"], normalize="index") * 100).round(1))
```

```
segment     Hospitality  Retail  Wholesale
order_date                                
2025-05            26.2    51.8       22.0
2025-06            26.1    52.6       21.3
```

- `orders` is the order table read in section 23.9: one row per order, so these are shares of orders, not of order lines.
- **`.dt.strftime("%Y-%m")`** writes each date as its year and month, like `2025-05` (Chapter 18), so all of May's orders share one label.
- **`pd.crosstab(month, segment)`** counts orders for every month-and-segment pair (Chapter 21). **`normalize="index"`** turns each row's counts into shares of that row, so each month's row sums to 1 (100% after `* 100`).

Each segment kept almost exactly its May share of orders (no segment moved by more than a point), so this wasn't "we sold to smaller customers".

**The finding:** of the ₹3.53 crore decline, ₹0.49 crore came from fewer customers, ₹0.51 crore from fewer orders per customer, and **₹2.53 crore — 72% of the fall — from a lower average order value.** The segment mix barely moved, which rules out a mix shift: it was "the same mix of customers placed smaller orders", consistent with the well-established seasonal trough rather than any operational failure.

**A general method for diagnosing a KPI move:**

1. **Confirm it's real** (Chapter 22): is the change bigger than normal month-to-month noise?
2. **Walk down the tree** one level, and decompose that change the way this section just did.
3. **Check for a mix effect** (Chapter 22, section 22.6) before believing a within-group story: has the *composition* of what you're measuring changed, or has behaviour genuinely changed?
4. **Compare with a benchmark that isn't your own history**: last year's same month, a similar company, a plan. A seasonal trough looks alarming against last month and unremarkable against last June.
5. **Stop at the level where you have an explanation someone can act on.** "AOV fell because it's the seasonal trough" is an answer; if it weren't seasonal, the next question would be which segment, which branch, which product — one more level down the tree.

---

## 23.12 Good metrics, vanity metrics, and gaming

A **vanity metric** goes up reliably and means little: total signups ever, page views, app downloads. It's not dishonest to report; it's just usually the wrong thing to *manage*, because it can rise while the business gets worse.

| Vanity metric | Sounds good because | What it hides | Better metric |
|---|---|---|---|
| Total customers ever acquired | Always goes up | Says nothing about who's still active | Active customers this period |
| Website visits | Big, round, easy to chart | Says nothing about intent or revenue | Leads or conversion rate |
| Total leads generated | Marketing looks busy | Says nothing about quality | Win rate, or revenue per lead |
| Features shipped | Feels like progress | Says nothing about whether anyone uses them | Adoption, retention |
| Gross merchandise value (for a marketplace) | A huge, headline-friendly number | Includes cancelled and returned orders | Net revenue after cancellations |

**Goodhart's law**, informally: *when a measure becomes a target, it stops being a good measure.* The moment a number is tied to a bonus or a promotion, people optimize the number, not necessarily the thing it was meant to represent. This isn't cynicism about people; it's a structural fact about incentives, and Riverstone's own data has an example ready-made:

```python
messy = pd.read_csv("../ch14/orders_q4_2025_export.csv", dtype=str, keep_default_na=False)
by_status = messy["status"].str.strip().str.lower().value_counts()
print(by_status)
```

```
status
delivered    21857
pending       1174
shipped       1144
cancelled     1040
dlvd           694
cxl             32
canceled        28
status           6
                 1
Name: count, dtype: int64
```

- **`dtype=str, keep_default_na=False`** read every value as text, exactly as typed, as in Chapter 14. If you leave out `keep_default_na=False`, pandas turns the blank status into a missing value (`NaN`), and `value_counts()` quietly leaves it out of the list.
- **`.str.strip().str.lower()`** removes stray spaces and capital letters, so `Delivered` and `delivered ` count together.

These are order *lines*, not orders: Chapter 14's export has one row per line. The rows reading `status` are repeated header rows and the blank is a missing value; Chapter 14 cleaned both. Even so, five spellings for two statuses show how loosely a status gets typed.

If a branch's bonus depended on "orders delivered", and Chapter 14's Delhi branch had discovered that marking a delayed order "Shipped" rather than leaving it "Pending" moved it out of the bucket anyone was checking, the metric would improve without a single delivery going faster. Nobody has to be dishonest for this to happen; a metric that's easy to move on paper and hard to move in reality *will* get moved on paper, given enough time and enough pressure.

**A checklist for spotting a metric at risk of being gamed:**

- **Can it be moved without moving the outcome it stands for?** (Marking an order shipped, without shipping it.)
- **Is it a count, when a rate would show the real story?** (Total sales calls made, versus calls that led to a meeting.)
- **Does improving it for one team make it worse somewhere else?** (A "reduce average handling time" target in support can produce rushed, unresolved calls that generate repeat contacts.)
- **Is there a paired metric that would catch the gaming?** (Pair "orders shipped on time" with "orders returned" or "repeat complaints", so gaming one makes the other visible.)

The fix is rarely "stop using metrics." It's to **pair a leading metric with a guardrail metric**, to **audit the definition periodically against the underlying reality** (exactly Chapter 14's reconciliation habit), and to **remember that the number is a proxy, not the goal.**

---

## 23.13 Defining a metric so two teams get the same number

Most "our numbers don't match" meetings are not about data quality. They're about two people who never agreed on the definition.

Take "active customer." Reasonable, defensible definitions include: placed an order in the last calendar year; placed an order in the trailing 12 months from today; placed a non-cancelled order; has a non-zero account balance. Each produces a different count from the same database, and none is wrong — they just answer subtly different questions.

Chapter 3 gave six questions every KPI definition must answer. Written up as an entry in a data dictionary, the same idea becomes six parts. **A metric definition worth writing down has:**

1. **Name.** "Active customer", not "actives".
2. **Formula.** The exact calculation, ideally as pseudocode or SQL, not a sentence that can be read two ways.
3. **Grain and population.** One row per what, over which customers, in Riverstone's case usually excluding the mini-database's Q1 2026 test data.
4. **Time window.** Calendar year, trailing 12 months, or as-of a specific date — and whether it's inclusive of the boundary dates.
5. **What's excluded.** Cancelled orders, internal test accounts, a specific customer segment.
6. **Owner and last-reviewed date.** Someone who can answer questions about it, and evidence it hasn't silently drifted.

Here is the formula part for "active customer, 2025", in PostgreSQL (Chapter 12's dialect), on the full three-year `riverstone_full` database:

<!-- db: riverstone_full -->
```sql
-- "Active customer, 2025": a documented definition, ready to paste into a data dictionary
-- Owner: Analytics team. Last reviewed: 2026-01-15.
SELECT COUNT(DISTINCT customer_id) AS active_customers_2025
FROM orders
WHERE status <> 'Cancelled'
  AND order_date >= '2025-01-01'
  AND order_date <  '2026-01-01';
```

```
 active_customers_2025 
-----------------------
                  4599
(1 row)
```

- 4,599, the same as the Python count in section 23.9. Two tools, one definition, one number.
- The date window is **half-open**: `>=` the first day, `<` the first day *after* the window. It works whether `order_date` is a date or a timestamp. `BETWEEN '2025-01-01' AND '2025-12-31'` would silently drop everything after midnight on 31 December if the column ever held times.
- No join to `customers` is needed: `orders` already holds `customer_id`, and a join adds only a chance to get it wrong.

Write the definition once, put it where both teams can see it (a data dictionary, a semantic layer, a pinned page — Chapter 16's shared semantic model is exactly this idea applied to a BI tool), and change it only with a note explaining why and from when. The alternative — every analyst quietly making their own reasonable choice — is how a company ends up with three different "revenue" figures in one meeting, all defensible, all disagreeing.

---

## Common mistakes

| Mistake | Symptom | Fix |
|---|---|---|
| Treating profit and cash as the same thing | "We made money, why can't we pay the supplier?" | Read the cash flow statement; check the cash conversion cycle |
| Quoting a margin with no rupee figure | "Only 1.8% of revenue" sounds trivial | Give the percentage and the absolute amount together |
| Reporting EBITDA as if it were cash profit | A heavily borrowed, loss-making company looks "healthy" | State which profit line you mean, and why |
| Using gross margin to decide whether to take one more order | The decision ignores which costs are actually variable | Contribution margin, not gross margin |
| Comparing CAC and LTV from different populations | A ratio that looks better or worse than reality | Measure LTV on the customers CAC actually bought |
| Using the naive 1/churn lifetime for LTV | A years-long assumption nobody would sign off on | Cap the horizon, and say so |
| Counting duplicate leads as enquiries | A win rate that blames sales for a website glitch | Deduplicate before counting (Chapter 13, Pattern 3) |
| Reporting NPS with no distribution behind it | Two very different customer bases can score the same | Show the distribution, or at least promoters/passives/detractors separately |
| A vanity metric on the headline slide | "Total signups" always goes up | Pick the metric that can also go down |
| A KPI tied to a bonus with no guardrail | The number improves; the outcome doesn't | Pair it with a metric that would catch gaming |
| No agreed definition of a shared metric | Two teams' "revenue" figures disagree | Write the six-part definition and put it where both can see it |
| Explaining a KPI move without checking mix | A within-group story for what's really a mix shift | Check the mix before believing the story (Chapter 22) |
| Stopping the diagnosis at the first plausible cause | "Sales fell because of the season" without checking the number | Decompose the tree and quantify each effect |
| Averaging a ratio across groups of different sizes | The company figure doesn't match any branch | Recompute from the totals, weighted properly (Chapter 21) |
| Presenting quota attainment as one company average | Hides reps far above and far below target | Show the distribution, not just the mean |

---

## In the real world: the profitable company that almost missed payroll

In February 2026, Riverstone's finance controller brought a single sentence to the Monday leadership meeting: *"We are profitable, and next month we may not be able to make payroll."* The room did not immediately believe both halves of that sentence could be true.

Meera had the numbers already, because she'd been asked to explain a smaller, related question the week before: why was the company's cash balance falling even though the P&L showed a healthy year? She walked the room through three facts, in order.

**First, the P&L was, on its own terms, good.** 2025 closed at ₹114.7 crore revenue, 27.5% gross margin, and ₹12.1 crore net profit — 10.5% net margin, a respectable result for a mid-sized manufacturer. Nobody in the room doubted the year had gone well.

**Second, the cash flow statement told a different, narrower story.** Operating cash flow was ₹12.9 crore, slightly ahead of profit — normal, even good. But investing activities had used ₹5.2 crore (a new warehouse racking system, approved back in Q2), and financing activities had used a further ₹2.9 crore, mostly the dividend the family had approved based on the profit figure, before anyone had checked what the cash position could actually support. Net cash had risen for the year as a whole, but the *timing* mattered: the dividend and the warehouse capex had both landed in the same eight-week window, right when receivables were also at their seasonal peak.

**Third, and this was the number that changed the meeting, the cash cycle itself had quietly lengthened.** Meera pulled DSO, DIO, and DPO at each quarter-end of 2025, instead of the year-end snapshot everyone had been looking at. Each is worked out as in section 23.3, but on the twelve months of sales (or cost of sales) up to that quarter-end, so the four rows compare fairly:

| Quarter end | DSO | DIO | DPO | Cash conversion cycle |
|---|---:|---:|---:|---:|
| 31 March 2025 | 36 | 52 | 37 | 51 |
| 30 June 2025 | 38 | 53 | 37 | 54 |
| 30 September 2025 | 40 | 54 | 38 | 56 |
| 31 December 2025 | 42 | 55 | 38 | 59 |

*The balances behind this table are invented (`working_capital_quarters_2025.csv`); the sales and cost figures they're divided by are real. The December row is section 23.3's balance sheet.*

Days sales outstanding had crept up every quarter, from 36 days at the end of March to 42 by December, as the sales team — rewarded, reasonably, on revenue booked — had quietly extended payment terms to close bigger Wholesale deals near quarter-end. Inventory days had risen too, as the warehouse stocked up ahead of the festive season. The cash conversion cycle had gone from 51 days to 59 in nine months, and nobody owned that number or was watching it move. The year-end snapshot showed a normal-looking 59; only the quarter-by-quarter view showed it growing.

Two decisions came out of the meeting. The dividend timing moved to align with the low point of the cash cycle rather than the announcement of annual results. And DSO joined the monthly management pack as its own tracked metric, with an owner in Finance and a simple rule: any customer whose payment terms exceeded 45 days needed sign-off from someone other than the rep booking the sale.

Payroll was never actually at risk that particular month — a short-term credit line covered the gap comfortably — but the near-miss was real, and it was caused by exactly the gap this chapter opened with: a profit-only view of a cash problem.

What made the difference:

- **She read the cash flow statement, not just the P&L**, when the P&L said everything was fine.
- **She looked at the trend in DSO and DIO**, not the year-end snapshot, and found a business decision (extended terms to close deals) hiding inside a ratio.
- **She connected an incentive (revenue-based commission) to an outcome (lengthening receivables)** — Goodhart's law, spotted before it became a crisis rather than after.
- **She turned the finding into an owned, monitored metric**, not just a one-time explanation.

---

## Project: build Riverstone's KPI tree and diagnose a revenue dip

**Goal:** one page that shows how Riverstone's revenue decomposes, and a second page that diagnoses a real change using that decomposition.

### Tools you'll need

- **Python and pandas** (Chapters 17 and 18). This chapter's outputs were checked on Python 3.11 with pandas 3.0.6. Every calculation in this chapter is arithmetic simple enough for a spreadsheet, too.
- **A spreadsheet:** every ratio here is one formula; a KPI tree is a natural fit for a linked set of cells, and Chapter 11's pivot tables handle the segment and monthly breakdowns.
- **Companion files (`companion/ch23/`):**
  - `financials_2025.md`: Riverstone's full 2025 P&L, balance sheet, cash flow statement, quarter-end working capital, and customer/marketing metrics, with every figure labelled real or invented.
  - `monthly_revenue_2025.csv`: the real monthly revenue, orders, customers, and AOV series.
  - `marketing_2025.csv`: monthly marketing spend, campaign leads, new customers, CAC, and ROAS (invented).
  - `working_capital_quarters_2025.csv`: quarter-end receivables, inventory, payables, and the days ratios (invented balances on real sales).
  - The folder also holds the script that built these files from the real dataset plus documented, invented assumptions; you never need to run it.
- Also used: `companion/full/` (leads and lead-stage history, orders, customers), `companion/ch21/delivery_times_2025.csv`, and `companion/ch14/orders_q4_2025_export.csv`.

**Option A: your own business.** Build the tree for a metric you actually own, using your own data.

**Option B: Riverstone.** Use `companion/full/`, `companion/ch23/`, and `companion/ch21/`.

**Steps**

1. **Build the top level of the tree:** Revenue = Active customers × Orders per customer × Average order value. Verify the identity reconstructs 2025's actual revenue.
2. **Decompose each branch one level:** active customers into retained + new (and retained into last year's active customers − churned); AOV into units per order × net price per unit.
3. **Attach a real 2025 number to every box**, and name the team that owns each one.
4. **Pick a KPI mentioned elsewhere in this book and place it on the tree** (Chapter 21's on-time delivery rate, Chapter 20's exception rate) — not everything belongs on the revenue tree, and saying why a metric doesn't fit is itself useful.
5. **Diagnose the May → June 2025 dip** using the chain-linked method in section 23.11. Reconstruct the three effects and confirm they sum to the total change.
6. **Check for a mix effect** before concluding: has the segment or branch mix shifted, or is this a within-group change?
7. **Write the one-paragraph diagnosis**, the way section 23.11 does, ending in a sentence someone could act on (or a sentence explaining why no action is needed, if it's a seasonal pattern and nothing more).
8. **Stress-test one metric for gaming:** pick a metric from your tree, and using the section 23.12 checklist, say how it could be moved without moving the underlying outcome, and what guardrail metric would catch it.

**What good looks like:** the tree's identity reconstructs ₹1,14,66,41,651.25 exactly from 4,599 customers × 10.08 orders per customer × ₹24,735.56 (with AOV computed from the totals, not rounded); the second level reads 3,827 retained + 772 new = 4,599, and 53.75 units per order × ₹460.16 per unit = the AOV; the May→June bridge attributes ₹49 lakh to fewer customers, ₹51 lakh to fewer orders per customer, and ₹2.53 crore to lower average order value, summing to the full ₹3.53 crore fall; the segment mix check shows no meaningful shift; and the guardrail exercise names a specific, checkable pairing (for example, "orders shipped" paired with "orders returned within 14 days").

**Stretch goals**

- Extend the diagnosis to the full year: which month-to-month change was the largest, and does the same three-factor decomposition explain the October festive peak as well as the June trough?
- Build a simple LTV:CAC cohort view: for customers acquired in each quarter of 2025, track their revenue in the following two quarters.
- Draft the six-part definition (section 23.13) for three metrics your own team reports, and check whether a colleague would define any of them differently.

---

## Timed challenge: forty minutes

Use `companion/ch23/financials_2025.md`, `monthly_revenue_2025.csv`, and the full dataset. Answers at the end.

- **Level 1:** From the P&L, compute gross margin, EBIT margin, and net margin as percentages.
- **Level 2:** From the balance sheet, compute working capital, the current ratio, and liabilities-to-equity.
- **Level 3:** From the balance sheet and the P&L, compute DIO, DSO, and DPO, then the cash conversion cycle.
- **Level 4:** From the cash flow statement, explain in one sentence why cash rose by less than profit after tax.
- **Level 5:** Using `monthly_revenue_2025.csv`, find the two consecutive months with the largest percentage *rise* in revenue, and compute it.
- **Level 6:** Decompose that rise into customer, frequency, and AOV effects using the chain-linked method.
- **Level 7:** State Riverstone's retention rate, churn rate, and 5-year-capped LTV, and compare LTV:CAC against the 3:1 rule of thumb.
- **Bonus:** Using the real leads data, after removing duplicates, compute the funnel conversion rate from "Contacted" to "Won" (not from "New").

---

## Recap

- **The cash cycle** turns cash into stock into sales into cash again. DIO = inventory ÷ COGS × 365, DSO = receivables ÷ revenue × 365, DPO = payables ÷ COGS × 365. Riverstone's operating cycle is 97 days (55 DIO + 42 DSO) and its cash conversion cycle 59 days (97 − 38 DPO): profit and cash are not the same thing, and the gap between them is exactly this cycle.
- **The P&L** shows revenue (₹114.7 cr) minus COGS gives gross profit (27.5% margin); minus operating expenses gives EBIT (15.0%); minus interest and tax gives net profit (10.5%).
- **The balance sheet** balances by definition (assets = liabilities + equity) and is where receivables and inventory — both analyst territory — live.
- **The cash flow statement** reconciles profit with the actual change in cash, across operating, investing, and financing activities, and ties one balance sheet's cash to the next.
- **Sales metrics** (win rate, sales cycle, AOV, quota attainment) describe the path from lead to revenue; after removing duplicate leads, Riverstone's real pipeline shows a 60% win rate on decided deals and a 25.5-day mean cycle over only six deals.
- **Marketing metrics** (CAC, ROAS, the funnel) always depend on an attribution model — state it.
- **Finance metrics** add contribution margin, ROA, and ROE to the vocabulary from the statements.
- **Operations metrics** (OTIF, inventory turns, fill rate) are the same "profile the distribution" skill from Chapter 21, in industry language.
- **Customer metrics** (retention, churn, LTV, LTV:CAC, payback, NPS) need a capped time horizon and a matched population; Riverstone's 93.3% retention and 26.6:1 LTV:CAC are both explainable, not automatically suspicious.
- **A KPI tree** decomposes a headline number into an exact identity, each branch owned by a team; diagnosing a change means walking the tree and quantifying each effect, checking for a mix shift before trusting a within-group story.
- **Vanity metrics** always rise and mean little; a metric tied to an incentive will be gamed unless paired with a guardrail.
- **A metric definition** needs a name, formula, grain, time window, exclusions, and owner — written down once, not reinvented by every analyst who touches it.

---

## Key terms

operating cycle · DIO · DSO · DPO · cash conversion cycle · profit & loss (P&L) · income statement · revenue · cost of goods sold (COGS) · expense · gross profit / margin · operating expenses (opex) · depreciation · amortisation · EBIT · EBITDA · net profit (PAT) · net margin · accrual accounting · balance sheet · assets · liabilities · equity · current assets / liabilities · working capital · current ratio · liabilities-to-equity · leverage · capital expenditure (capex) · dividend · cash flow statement · CFO / CFI / CFF · fixed cost · variable cost · contribution margin · pipeline · win rate · sales cycle · quota attainment · funnel · CAC · blended CAC · ROAS · attribution (first-touch, last-touch, multi-touch) · payback period · return on assets (ROA) · return on equity (ROE) · OTIF · inventory turns · fill rate · OEE · retention rate · churn rate · customer lifetime value (LTV) · LTV:CAC · Net Promoter Score (NPS) · KPI tree · North Star metric · chain-linked (sequential) decomposition · mix effect · vanity metric · Goodhart's law · guardrail metric · metric definition · half-open date window · data dictionary

*(All terms are defined in the Glossary, Appendix A.)*

---

## Check yourself

- [ ] You can explain the cash cycle and why a profitable company can run out of cash.
- [ ] You can compute DIO, DSO, DPO, and the cash conversion cycle from a balance sheet and a P&L.
- [ ] You can read a P&L, a balance sheet, and a cash flow statement and say what each answers.
- [ ] You know the difference between gross, EBIT, and net margin, and between EBIT and EBITDA.
- [ ] You can compute and interpret the core metrics of sales, marketing, finance, operations, and customer teams.
- [ ] You never quote CAC or LTV without saying which population and which time horizon.
- [ ] You can build a KPI tree that reconstructs a real total exactly, with each branch owned by a team.
- [ ] You diagnose a metric change by decomposing it, not by guessing, and you check for a mix effect first.
- [ ] You can name a vanity metric and its better replacement.
- [ ] You can predict how a metric would be gamed if a bonus depended on it, and propose a guardrail.
- [ ] You write metric definitions with a formula, a population, a time window, exclusions, and an owner.

---

## Exercises

Use `companion/ch23/`, `companion/full/`, and `companion/ch21/delivery_times_2025.csv`.

### Warm-up

1. A friend says "the business made a profit this year, so it must have more cash than last year." Explain why that isn't guaranteed, using the three financial statements.
2. What's the difference between gross margin and net margin? Give a one-sentence business reason a company might have high gross margin and low net margin.
3. Riverstone's DIO is 55 days, DSO is 42, DPO is 38. Compute the cash conversion cycle, and explain in one sentence what a *negative* CCC would mean for a company.
4. Name the three sections of a cash flow statement and one Riverstone example of an item in each.
5. Why is "total leads generated" a vanity metric for a sales team, and what would you track instead?
6. Write a six-part definition for "active customer" as section 23.13 does.

### Core

7. Compute Riverstone's EBITDA (EBIT + depreciation) and its margin. Why might a lender care about EBITDA more than net profit?
8. Compute the current ratio and liabilities-to-equity from the balance sheet. Would you describe Riverstone as conservatively or aggressively financed?
9. Using the real leads data, after removing duplicates, compute the conversion rate at each stage of the funnel (New→Contacted, Contacted→Quoted, Quoted→Won). Which stage loses the most leads?
10. Compute Riverstone's blended CAC and average ROAS from `marketing_2025.csv`. In which month was ROAS highest, and does that month's lead volume explain it?
11. Compute the naive (1/churn) and 5-year-capped LTV, and the resulting LTV:CAC for each. Which would you present to a board, and why?
12. Verify the KPI tree identity for 2025: active customers × orders per customer × AOV. Confirm it reconstructs the real revenue figure.
13. The summer trough didn't end in June: revenue fell again from June to July 2025. Decompose the June → July fall into customer, frequency, and AOV effects, with the chain-linked method of section 23.11.
14. For the change in exercise 13, check whether the segment mix shifted meaningfully between the two months.
15. Compute inventory turns (COGS ÷ inventory, using the year-end inventory figure as a simple proxy for the average). What would doubling inventory turns imply about DIO?
16. Using Chapter 21's delivery data, compute OTIF by branch and rank the branches. Propose one guardrail metric that would catch a branch gaming OTIF by relabelling status.
17. Using the messy Q4 export from Chapter 14, count how many rows are some variant of "Shipped". If a branch's bonus depended on minimizing "Pending" orders, what behavior would you watch for?
18. Write the SQL (or pandas) for a second, differently-scoped definition of "active customer": the trailing 12 months to 30 September 2025, instead of calendar 2025. Show that it gives a different count, and say which customers make the difference.
19. Compute return on equity and return on assets. Which is higher, and what does the gap tell you about how the business is financed?
20. Draft a one-paragraph answer, in the style of section 23.11, diagnosing October 2025's revenue peak instead of the June trough.

### Stretch

21. Build the full second level of the KPI tree (retained, churned, and new customers; units per order and net price per unit for AOV) with real 2025 numbers in every box.
22. Compute a cohort LTV: for customers whose first order was in Q1 2025, what was their total revenue through Q4 2025? Compare it with the chapter's blended LTV estimate.
23. Propose Riverstone's North Star metric, with a one-paragraph justification, and explain what it would and wouldn't tell leadership that revenue doesn't.
24. Using `marketing_2025.csv` and section 23.9, compute the payback period (CAC ÷ monthly gross profit per new customer) and say whether Riverstone's marketing spend is cash-efficient.

### Think about it

25. Riverstone's board asks why the company should invest more in marketing when it's already profitable. Using this chapter's numbers, make the case for and against.
26. A regional sales manager's bonus depends entirely on quarterly revenue booked. Predict two ways this could distort the numbers you'd see in the data, and propose a guardrail for each.
27. Two departments each report "customer retention" and get different numbers from the same underlying data. What's your first question, and what would you do about it going forward?

---

## Answers

**Checkpoint (end of Part A, section 23.4).** (1) Gross margin = (36,50,000 − 25,55,000) ÷ 36,50,000 = 10,95,000 ÷ 36,50,000 = **30.0%**. DIO = 3,50,000 ÷ 25,55,000 × 365 = **50 days**; DSO = 3,00,000 ÷ 36,50,000 × 365 = **30 days**; DPO = 2,10,000 ÷ 25,55,000 × 365 = **30 days**; CCC = 50 + 30 − 30 = **50 days**. (2) CFO = 2,40,000 + 60,000 − 50,000 − 30,000 + 20,000 = **₹2,40,000**: the same as profit this time, because adding back depreciation (₹60,000) exactly offsets the net ₹60,000 that went into receivables and stock. (3) In Python, `350000 / 2555000 * 365` gives 50.0, and so on; in a spreadsheet, one formula per line.

**1.** Profit is booked when a sale is made, not when it's paid for; a company can be profitable while its cash is tied up in growing receivables and inventory (the cash cycle), or while it spends heavily on capex or dividends. Only the cash flow statement shows what actually happened to the bank balance.

**2.** Gross margin is revenue minus the cost of the product itself; net margin is what's left after every other cost, including overhead, marketing, interest, and tax. A software company can have very high gross margin (little "cost of goods") and low net margin if it spends heavily on sales, marketing, and R&D.

**3.** CCC = 55 + 42 − 38 = **59 days**. A negative CCC (common in retail and e-commerce) means the company collects from customers before it has to pay its own suppliers — effectively financing its inventory with someone else's money.

**4.** Operations: profit adjusted for depreciation and working-capital changes. Investing: the ₹5.16 crore capital expenditure (warehouse racking, in the story). Financing: the ₹4.23 crore dividend, debt drawn, and loan repayment.

**5.** It rises whenever marketing runs any campaign, regardless of whether those leads ever buy anything or fit the business, and, as section 23.5 showed, even when the "leads" are duplicate submissions. Track win rate, or revenue per lead, which can go down even while lead count goes up.

**6.** Name: Active customer, 2025. Formula: `COUNT(DISTINCT customer_id)` from `orders` with `status <> 'Cancelled'`. Grain/population: one row per customer, Riverstone's full customer base, excluding the mini-database's test data. Time window: calendar year 2025, `order_date >= '2025-01-01' AND order_date < '2026-01-01'` (every moment of both boundary days included). Exclusions: cancelled orders. Owner: Analytics team, last reviewed [date].

**7.** EBITDA = EBIT + depreciation = ₹17.15 cr + ₹1.61 cr = **₹18.76 crore**, margin **16.4%**. A lender cares about EBITDA because it approximates cash available to service debt, independent of how assets happen to be depreciated or financed — closer to "can this business make its loan payments" than net profit is.

**8.** Current ratio 1.58, liabilities-to-equity 0.91: for every ₹1 the owners have in the business, it owes ₹0.91 to suppliers, lenders and others. A current ratio comfortably above 1, and total obligations a bit below equity, describe a moderately, not aggressively, financed balance sheet — enough borrowing to grow, enough cushion to survive a bad quarter.

**9.** After removing the 13 duplicates: New→Contacted: 22/30 ≈ 73%. Contacted→Quoted: 14/22 ≈ 64%. Quoted→Won: 6/14 ≈ 43% (with 4 of 14 Lost and the rest still open). The New→Contacted stage loses the most leads in absolute terms (8 of 30 never get contacted), as Chapter 13's funnel found.

**10.** Blended CAC ≈ ₹8,141; average ROAS ≈ 5.7x. The highest ROAS month is March (7.37x), which had solid lead volume (470) and an above-average conversion that month — not simply the month with the most leads (October had more leads, 690, but a lower ROAS, 5.51x).

**11.** Naive LTV (14.8-year lifetime): ₹6.42 lakh, LTV:CAC ≈ 79:1. 5-year-capped: ₹2.17 lakh, LTV:CAC ≈ 27:1. Present the capped figure to a board: it rests on an assumption (5 years of continued purchasing) that's far easier to defend than fourteen years of extrapolation from one year of churn data.

**12.** 4,599 × (46,356 ÷ 4,599) × (₹1,14,66,41,651.25 ÷ 46,356) = 4,599 × 10.08 × ₹24,735.56 = **₹1,14,66,41,651.25**, matching the real 2025 revenue exactly (the identity is definitional, so it always will, as long as AOV isn't rounded first).

**13.** June ₹5.20 crore → July ₹4.00 crore, a fall of 23.0% (₹1.19 crore). Customers fell from 2,723 to 2,573, orders per customer from 1.190 to 1.173, and AOV from ₹16,040.89 to ₹13,263.12. Decomposed: customer effect ≈ −₹28.6 lakh, frequency effect ≈ −₹7.0 lakh, AOV effect ≈ −₹83.8 lakh, summing to the full −₹1.19 crore — AOV is again the dominant driver, at 70% of the decline.

**14.** For June→July, segment order-share is almost unchanged (Hospitality 26.1%→26.5%, Retail 52.6%→52.5%, Wholesale 21.3%→21.0%), so the AOV decline is again a broad, within-segment effect (the deepening seasonal trough) rather than a shift toward smaller-spending segments.

**15.** COGS ÷ inventory = 83,18,03,000 ÷ 12,53,40,178 ≈ **6.6 times a year**. Doubling turns to about 13.2 would imply DIO falling from 55 days to roughly 27.5 days — much less cash tied up in stock, but a higher risk of stockouts unless replenishment also gets faster.

**16.** OTIF by branch: Mumbai HO 90.8%, Delhi 80.0%, Bengaluru 78.0%, Kolkata 68.1%. A guardrail: pair "on-time rate" with "customer-reported late deliveries" or "orders relabelled after the promised date", so relabelling an order's status without it actually arriving would show up as a gap between the two.

**17.** 1,144 rows are some spelling of "Shipped" (plus 21,857 Delivered, 1,174 Pending, and cancelled variants). If a bonus depended on minimizing Pending orders, watch for orders moved to "Shipped" status without a corresponding dispatch record or tracking update — exactly the gap a paired metric (dispatch confirmations, or actual delivery dates) would expose.

**18.** Trailing 12 months to 30 September 2025, in PostgreSQL: `SELECT COUNT(DISTINCT customer_id) FROM orders WHERE status <> 'Cancelled' AND order_date > DATE '2025-09-30' - INTERVAL '12 months' AND order_date <= DATE '2025-09-30';` gives **4,509**, against 4,599 for calendar 2025. The difference is customers who ordered only in October–December 2025 (in the calendar year, not the trailing window) set against those who ordered only in October–December 2024 (in the trailing window, not the calendar year). Small in percentage terms, but enough to produce "different" numbers in a meeting if nobody states which definition they used. (A trailing window that ends on 31 December is simply the calendar year, so the as-of date matters.)

**19.** ROE = 12,08,91,502 ÷ 37,82,25,976 ≈ **32.0%**; ROA = 12,08,91,502 ÷ 72,28,19,016 ≈ **16.7%**. ROE well above ROA indicates the company is using borrowed money (leverage) to boost the return to equity holders above what the assets alone generate.

**20.** *October 2025 revenue rose to ₹18.06 crore from September's ₹11.17 crore, a ₹6.89 crore increase. Decomposing the same way as the June dip: more active customers, more orders per customer, and a higher average order value all contributed, consistent with the well-documented festive-season peak (Chapters 11 and 15) rather than any one-off event. The segment mix shows Wholesale's share of orders rising slightly, consistent with bulk festive restocking.*

**21.** Active 2025 = retained 3,827 + new 772 = **4,599** ✓. Retained = active 2024 (4,104) − churned (277) = 3,827 ✓. Churned describes 2024's base, so it is already inside "retained"; subtracting it again would double-count. For AOV, compute both factors from the 2025 non-cancelled order lines: units per order = 24,91,830 units ÷ 46,356 orders = **53.75**; net price per unit = ₹1,14,66,41,651.25 ÷ 24,91,830 = **₹460.16**; and 53.75 × ₹460.16 = ₹24,735.56 = AOV ✓.

**22.** A cohort LTV (actual revenue from a specific quarter's new customers, tracked forward) is always more trustworthy than a blended, formula-based estimate, because it has no assumptions baked in — only the risk that the cohort isn't yet finished generating revenue. Expect it to run somewhat below the 5-year-capped estimate, since it only covers nine months rather than five years.

**23.** A reasonable choice is **active customers**, because it sits upstream of both revenue (via frequency and order size) and retention, and it's a number every function can influence. It would tell leadership whether the customer base is growing or shrinking *before* that shows up in a revenue number that can be temporarily flattered by a few large orders; it would not, on its own, say anything about profitability.

**24.** Payback period = CAC ÷ (monthly gross profit per new customer). With average first-year revenue of ₹1,57,617 and 27.5% margin, monthly gross profit per new customer ≈ ₹3,612, giving a payback of roughly **2.3 months** on a CAC of ₹8,141 — a fast payback that supports the case for spending more, not less, on acquisition.

**25.** For: LTV:CAC of 26.6:1 is far above the 3:1 rule of thumb, payback is under three months, and the company is already profitable with cash to deploy — textbook conditions for investing more in acquisition while it's working. Against: the 26.6:1 ratio rests on assumptions (the 5-year horizon, the attribution model) that haven't been stress-tested at higher spend, and past a point, additional marketing spend usually raises CAC (the easiest customers are acquired first) faster than revenue grows to match.

**26.** (a) Revenue could be pulled forward by discounting or extending payment terms near quarter-end (exactly the DSO story in this chapter's real-world example) — a guardrail would track DSO and discount rates by rep alongside revenue. (b) Deals could be booked before they're actually won, or split to appear as multiple smaller wins — a guardrail would track the rate of cancelled or reversed orders shortly after being recorded.

**27.** First question: "what's your exact definition — formula, time window, and what's excluded?" Very often the discrepancy is entirely explained by one team using calendar year and the other trailing twelve months, or one excluding cancelled orders and the other not. Going forward: write the six-part definition once, in a shared location, with an owner, so the next disagreement takes five minutes instead of a meeting.

**Timed challenge answers.** Level 1: gross margin 27.5%, EBIT margin 15.0%, net margin 10.5%. Level 2: working capital ₹12.60 crore, current ratio 1.58, liabilities-to-equity 0.91. Level 3: DIO = 12,53,40,178 ÷ 83,18,03,000 × 365 = 55.0; DSO = 13,19,42,327 ÷ 1,14,66,41,651 × 365 = 42.0; DPO = 8,65,98,668 ÷ 83,18,03,000 × 365 = 38.0; CCC = 55 + 42 − 38 = 59 days. Level 4: cash rose by less than PAT because ₹5.16 crore was spent on capex (investing) and ₹4.23 crore paid out as dividend (financing), outflows that don't appear in profit. Level 5: July→August, a rise from ₹4.00 crore to ₹7.18 crore, about 79.5% (ahead of September→October at 61.7% and August→September at 55.5%). Level 6: customer effect ≈ +₹49.6 lakh, frequency effect ≈ +₹30.5 lakh, AOV effect ≈ +₹2.38 crore, summing to the full +₹3.18 crore rise; AOV is 75% of it. Level 7: retention 93.3%, churn 6.7%, 5-year-capped LTV ≈ ₹2.17 lakh, LTV:CAC ≈ 26.6:1 — well above the 3:1 rule of thumb. Bonus: Contacted→Won using the deduplicated funnel (6 Won of 22 that reached Contacted) ≈ 27%.

---

## Where this leads

- **Chapter 24, Requirements, Storytelling & Stakeholders:** turning a diagnosis like section 23.11's into a memo and a three-slide story someone will act on.
- **Chapter 25, The Business Analyst Track:** process mapping and requirements gathering, which is how a KPI tree gets built collaboratively rather than assumed.
- **Part 4:** LTV modelling, churn prediction, and marketing mix modelling all extend the ideas in sections 23.6 and 23.9 with statistical machinery.
- **Interview preparation:** the Business Analyst Question Bank (Chapter 76B) and Product Sense, Metrics, Case Studies & Guesstimates (Chapter 75) both lean heavily on exactly this chapter — "walk me through how you'd diagnose a revenue drop" is one of the most common analyst interview questions there is.
- **Looking back:** Chapter 16's shared semantic model is where section 23.13's metric definitions are enforced in a BI tool, and Chapter 22's tests confirm a KPI move is real, and rule out confounders and mix effects, before you diagnose it.
