# Chapter 4. Numbers Without Fear

*Part 0 — First Principles: Data from Zero*

> **Chapter at a glance**
>
> **You will learn to:** calculate percentages forward and backward, and see why a rise and an equal fall don't cancel · tell percentage points from percent change · choose the right denominator for a ratio or rate · measure growth month by month and year by year, and calculate compound growth and CAGR · choose between mean, median, and mode, and use weighted averages · round without changing the story · read tables and charts without being fooled · think about probability as "how often, out of how many" · estimate quickly and sanity-check any number · spot the number tricks in business news.
>
> **Before you start:** Chapter 1 (especially section 1.6, levels of measurement) and Chapter 3 (bookings, billings, KPIs).
>
> **Time needed:** 4–5 hours, including the exercises and the project.
>
> **Tools:** a calculator (your phone's is fine), a pen, and a notebook. A spreadsheet is optional; the *Spreadsheet link* notes show each calculation in Excel and Google Sheets.
>
> **Practice data:** Riverstone's 2025 sales from the one-year database: monthly revenue, targets, and margins, and 173 orders. The companion workbook `numbers_practice.xlsx` (Appendix E) holds the same numbers with every formula from this chapter. Every number was checked by script.

---

## Why this matters

Data work is mostly arithmetic. Not advanced math: percentages, averages, growth rates, and a little probability. The difficulty isn't the calculation. It's knowing *which* calculation answers the question, and noticing when a number that looks right is wrong.

Here are three sentences a manager at Riverstone could say in a meeting, each built on a real 2025 number:

- *"Revenue grew 13.1% a month on average."* True arithmetic, badly misleading. The steady monthly rate that gets from January to December is 7.3%.
- *"Margin fell 3.9% in November."* It fell 3.9 percentage points, which is a 14.0% fall.
- *"Our average order is ₹24,243."* That's an average of monthly averages. The real average order is ₹25,061, and half of all orders are below ₹21,375.

None of these is a lie. Each is a small slip that changes what people decide. By the end of this chapter you'll catch all three on sight, and you'll never be the person who makes them.

This chapter has no code. Every idea is worked by hand with real numbers, because being able to check a number on the back of an envelope is what makes you trustworthy when the tools do the work later.

---

## In plain English

A shop has a sign: **"50% off, and an extra 20% off at the till!"** How much do you save?

It's tempting to add them: 70%. But the second discount is taken from the *already reduced* price. On a ₹1,000 item, 50% off leaves ₹500. Then 20% off ₹500 is ₹100 off, leaving ₹400. You pay 40% of the original price, so you save **60%**, not 70%.

That one example holds the most important idea in this chapter: **every percentage is a percentage *of* something.** When the "something" changes, the same percentage means a different amount. Most number mistakes in business, and most number tricks in the news, come from losing track of what the percentage is *of*.

Keep asking two questions and you'll be right far more often than wrong:

1. **Of what?** What's the base, the denominator, the starting point?
2. **Compared with what?** Last month, last year, the target, another group?

---

## 4.1 Percentages: of, back, and change

A **percentage** is a fraction out of 100. 12% means 12 out of every 100, or 0.12. There are three everyday calculations, and it helps to name them.

**1. A percentage *of* a number.** Multiply by the percentage as a decimal.

*"What is a 12% discount on an Industrial Crate listed at ₹1,450?"* 0.12 × ₹1,450 = **₹174**. The crate sells for ₹1,450 − ₹174 = ₹1,276, which is the same as ₹1,450 × 0.88. (That's order 5009's price per crate, from Chapter 3.)

**2. What percentage one number is *of* another.** Divide the part by the whole.

*"What share of 2025 revenue came from Sharma Hardware?"* ₹502,775 ÷ ₹4,335,471 = 0.116, or **11.6%**.

**3. Percent change.** The change, divided by the *starting* value:

> percent change = (new − old) ÷ old

*"How did November's revenue compare with October's?"* October was ₹681,071, November ₹633,408. (₹633,408 − ₹681,071) ÷ ₹681,071 = −0.070, or **−7.0%**.

### Working backward

*"Northgate paid ₹1,276 per crate after a 12% discount. What was the list price?"*

The tempting wrong answer is to add 12% back: ₹1,276 × 1.12 = ₹1,429.12. That's wrong because the 12% was taken off ₹1,450, not off ₹1,276. The right way: ₹1,276 is 88% of the list price, so the list price is ₹1,276 ÷ 0.88 = **₹1,450**. ✓

> **Watch out: undoing a percentage.** To reverse "*x* % off", divide by (1 − *x* %). To reverse "*x* % added", divide by (1 + *x* %). Never add or subtract the same percentage again.

### Rises and falls don't cancel

![Two bar charts: 100 rises 50% to 150 then falls 50% to 75; 100 falls 20% to 80 then rises 20% to 96](figures/fig4-1-percent-changes-dont-cancel.svg)

*Figure 4.1 — A 50% rise followed by a 50% fall leaves you at 75, not 100.*

Figure 4.1 shows why. Up 50% takes ₹100 to ₹150. Down 50% is half of ₹150, which is ₹75. Down 20% then up 20% leaves ₹96. The fall and the rise are each calculated on a different base.

Two consequences come up all the time:

- **Recovering from a fall needs a bigger rise.** After a 50% fall, you need a 100% rise to get back. After a 20% fall, you need 25%.
- **Discounts stack by multiplying.** A 10% trade discount followed by an extra 5% for early payment is 0.90 × 0.95 = 0.855 of the price, a total of **14.5%** off, not 15%.

> **Spreadsheet link.** In Excel and Google Sheets, with the old value in B2 and the new value in C2: percent change is `=(C2-B2)/B2`, formatted as a percentage. A list price from a discounted price in B2 is `=B2/(1-12%)`. The `monthly` sheet of `numbers_practice.xlsx` calculates every month's percent change this way.

---

## 4.2 Percentage points and percent change

When the thing that changes is *itself* a percentage, there are two different ways to describe the change, and mixing them up is one of the most common errors in business writing.

Riverstone's gross margin (Chapter 3, section 3.5) was **27.9%** in October 2025 and **24.0%** in November.

- The difference is 27.9 − 24.0 = **3.9 percentage points**. A **percentage point** is the unit for the plain difference between two percentages.
- The **percent change** is (24.0 − 27.9) ÷ 27.9 = **−14.0%**. The margin is 14.0% smaller than it was.

Both are correct. They answer different questions, and they sound very different. *"Margin fell 3.9%"* is wrong: it mixes the size of one with the unit of the other, and it makes the fall sound less than a third as big as it was.

Here are three more from Riverstone's data:

| Measure | Before | After | Change in points | Percent change |
|---|---|---|---|---|
| Gross margin, January → February 2025 | 29.2% | 26.0% | −3.1 points | −10.8% |
| Revenue as % of target, August → September 2025 | 102.9% | 146.9% | +44.0 points | +42.8% |
| Win rate, clean leads → duplicated leads (Chapter 13) | 20.0% | 14.0% | −6.0 points | −30.2% |

(The first row shows −3.1 points, not 29.2 − 26.0 = 3.2, because it's calculated from the unrounded margins, 29.18% and 26.04%. Section 4.6 is about exactly this kind of rounding.)

**Which should you report?** Use **points** when you talk about the level of a rate: *"conversion fell 6 points, from 20% to 14%"*. Use **percent change** when you want the relative size: *"a 30% drop in conversion"*. Whenever you can, give the before and after values too, and the reader can see both.

> **Watch out: "percent" for a change in a percentage.** When a rate, share, margin, or interest rate moves, say "percentage points" (or "points") for the difference. If a loan's interest rate goes from 8% to 9%, it rose 1 point, which is a 12.5% increase in what you pay in interest.

---

## 4.3 Ratios and rates: always ask about the denominator

A **ratio** compares two quantities by dividing one by the other. A **rate** is a ratio where the bottom is a unit of something else: per day, per customer, per 1,000 people. The bottom number is the **denominator**, and choosing it is the whole skill.

Here are Riverstone's three customer segments in 2025:

| Segment | Revenue | Orders | Customers | Revenue per customer | Average order value |
|---|---|---|---|---|---|
| Wholesale | ₹1,702,658 | 55 | 6 | ₹283,776 | ₹30,957 |
| Retail | ₹1,488,774 | 59 | 8 | ₹186,097 | ₹25,233 |
| Hospitality | ₹1,144,039 | 59 | 9 | ₹127,115 | ₹19,390 |
| **Total** | **₹4,335,471** | **173** | **23** | **₹188,499** | **₹25,061** |

Hospitality has the most customers and ties for the most orders, but the least revenue. Which segment is "biggest" depends entirely on the denominator you pick:

- **By customers:** Hospitality (9).
- **By revenue:** Wholesale (₹1,702,658).
- **Per customer:** Wholesale again, and by a lot. A wholesale customer brings in ₹283,776 ÷ ₹127,115 = **2.23 times** as much as a hospitality customer.

Rates also make different-sized periods comparable. ₹4,335,471 in a year is about **₹11,878 per day** (÷ 365), and 173 orders is about **3.3 orders per week** (÷ 52). Neither is a number anyone at Riverstone reports, but both are useful sanity checks: if someone claims a single ordinary day brought in ₹2 lakh, you know to ask what happened that day.

A **share** (or proportion) is a ratio where the part is inside the whole, like Sharma Hardware's 11.6%. Shares of a whole add up to 100%. Ratios between separate groups, like 2.23 times, don't add up to anything.

> **Try it.** Riverstone collected ₹197,250 of ₹297,710 billed in the first quarter of 2026 (Chapter 3). What's the collection rate? If next quarter it's 75.0%, how many points is that up, and what percent change?

---

## 4.4 Growth, compounding, and CAGR

### Month-over-month growth

Here is Riverstone's revenue for every month of 2025, with the percent change from the month before. (Chapter 13 calculates this same table in SQL.)

| Month | Revenue | Change from previous month |
|---|---|---|
| January | ₹202,640 | |
| February | ₹253,664 | +25.2% |
| March | ₹278,008 | +9.6% |
| April | ₹210,282 | −24.4% |
| May | ₹329,359 | +56.6% |
| June | ₹186,928 | −43.2% |
| July | ₹232,692 | +24.5% |
| August | ₹329,282 | +41.5% |
| September | ₹558,315 | +69.6% |
| October | ₹681,071 | +22.0% |
| November | ₹633,408 | −7.0% |
| December | ₹439,824 | −30.6% |
| **Year** | **₹4,335,471** | |

The monthly changes swing wildly, from −43.2% to +69.6%. Most of that is the calendar: monsoon months are slow and the festive season is busy. Month-over-month percentages exaggerate seasonal patterns, which is why businesses with more than a year of data also compare each month with the same month last year.

### The average of growth rates is a trap

*"What was the typical monthly growth in 2025?"*

The tempting method is to average the eleven monthly changes. They add up to 143.8, and 143.8 ÷ 11 = **13.1%**. It sounds reasonable. It's wrong, and you can prove it: start with January's ₹202,640 and grow it by 13.1% eleven times. You get **₹782,621** for December. The real December was ₹439,824.

The problem is Figure 4.1 again. A +56.6% month and a −43.2% month don't cancel, because each is a percentage of a different base. Averaging percentages that compound on each other always overstates growth when the numbers bounce around.

The right question is: *what single, steady monthly rate would take ₹202,640 to ₹439,824 in eleven steps?* That's the **compound growth rate**:

> compound growth rate = (end ÷ start)^(1 ÷ number of periods) − 1

₹439,824 ÷ ₹202,640 = 2.17. The eleventh root of 2.17 is 1.073. So the compound monthly growth rate is **7.3%**. Grow ₹202,640 by 7.3% eleven times and you land exactly on December.

![Line chart of Riverstone's monthly revenue in 2025, with a steady 7.3% compound path ending at December's actual value and a 13.1% path overshooting to 782,621](figures/fig4-2-average-growth-vs-compound.svg)

*Figure 4.2 — The average of the monthly changes (red) overshoots December by ₹342,797. The compound rate (green) connects the real start and end.*

"The eleventh root" sounds hard. You won't do it by hand; any calculator with a power key does it as `2.17 ^ (1/11)`, and the spreadsheet functions are below.

> **Watch out: start and end points drive compound growth.** The compound rate only uses the first and last values. From June (₹186,928, the lowest month) to October (₹681,071, the highest), revenue grew **264.3%**, a number that's true and tells you almost nothing about the year. Always ask why a growth figure starts and ends where it does.

### Compounding

**Compounding** means growth that builds on previous growth. ₹100 growing 10% a year becomes ₹110, then ₹121, then ₹133.10 after three years. Simple growth, adding ₹10 a year, would give ₹130. The extra ₹3.10 is growth on growth. Over short periods the gap is small. Over long periods it dominates: that's why a loan's interest and a company's growth rate both matter so much over ten years.

A handy shortcut is the **rule of 72**: a quantity growing at *r*% a year doubles in about 72 ÷ *r* years. At 12%, about 6 years (the exact answer is 6.12). At 8%, about 9 years (exactly 9.01). It's for quick thinking in meetings, not for reports.

### CAGR

**CAGR** (compound annual growth rate) is the compound growth rate when the periods are years. It's the standard way to describe growth over several years in company reports, investor decks, and interviews.

*"Anita wants the business in the one-year database to reach ₹60 lakh (₹6,000,000) of revenue by 2028, three years after 2025's ₹4,335,471. What growth rate does she need each year?"*

1. Ratio of end to start: ₹6,000,000 ÷ ₹4,335,471 = 1.384.
2. Three years, so take the cube root: 1.384^(1/3) = 1.1144.
3. Subtract 1: **CAGR = 11.4% a year.**

Check it by growing forward: ₹4,335,471 × 1.1144 = ₹4,831,418 in 2026, ₹5,384,098 in 2027, and ₹6,000,000 in 2028. ✓

Two tempting shortcuts both get the plan wrong:

- **Splitting the gap evenly.** ₹6,000,000 − ₹4,335,471 = ₹1,664,529, or ₹554,843 a year. That's 12.8% of 2025's revenue, but a fixed rupee amount is a smaller percentage each year, so it isn't a growth rate at all.
- **Rounding down to a nice number.** 10% a year for three years reaches ₹5,770,512, which is ₹229,488 short. Over several years, one percentage point matters.

> **Spreadsheet link.** Compound growth in both Excel and Google Sheets: `=(end/start)^(1/periods)-1`, or the built-in `=RRI(periods, start, end)`. `=RRI(3, 4335471, 6000000)` returns 0.1144, and `=RRI(11, 202640, 439824)` returns 0.0730. The plain average of monthly changes is `=AVERAGE(F3:F13)` on the `monthly` sheet, which returns the misleading 0.1307.

---
## 4.5 Averages: mean, median, mode, and weighted

An **average** is one number that stands for many. There are three common kinds, and Chapter 1 (section 1.6) showed that the level of measurement decides which ones make sense. This section shows how to choose between them for amounts, like order values, where all three are allowed.

- The **mean** adds up the values and divides by how many there are. It's what most people mean by "average".
- The **median** is the middle value when the values are sorted. Half are below it, half above.
- The **mode** is the most common value.

Riverstone received 173 orders in 2025 (not counting the two that were cancelled), worth ₹4,335,471 in total.

- **Mean:** ₹4,335,471 ÷ 173 = **₹25,061**.
- **Median:** sort the 173 order values; the 87th is **₹21,375**.
- **Mode:** order values are almost never exactly equal, so the mode of the values themselves is useless here. The mode is useful for categories and repeated counts instead: the most commonly ordered product is the Storage Box 10L (on 76 order lines), the most common quantity on a line is 15, and the most common discount is 0% (140 of 326 lines).

![Histogram of 173 order values in 10,000-rupee bands, most between 0 and 40,000, with a long tail to 100,278; the median line at 21,375 sits left of the mean line at 25,061](figures/fig4-3-order-values-mean-vs-median.svg)

*Figure 4.3 — Most orders are small; a few large ones stretch the tail to the right and pull the mean above the median.*

Why is the mean higher than the median? Look at Figure 4.3. Most orders are under ₹40,000, but a handful are much larger: the biggest five are ₹65,818, ₹68,875, ₹74,218, ₹82,250, and ₹100,278. Large values pull the mean toward them; they don't move the median at all, because the median only cares about which value is in the middle. Data with a long tail on the high side is called **right-skewed**, and it's everywhere in business: order values, salaries, house prices, time to resolve a ticket.

The result: only **70 of the 173 orders (40.5%)** are above the "average" order. If a sales executive is told the average order is ₹25,061, most of their orders will feel below average.

**Which to use?**

| Situation | Use | Why |
|---|---|---|
| Amounts that add up to a total you care about (revenue, cost, hours) | mean | mean × count = total, so it connects to budgets and plans |
| Amounts with a long tail (order values, salaries, delivery times) | median, alongside the mean | tells you what's *typical*; the gap between them shows the skew |
| Categories (products, payment methods, segments) | mode | the only average that works for nominal data (Chapter 1) |
| Ratings and ranks (ordinal data) | median, plus the count in each category | the gaps between ratings aren't equal (Chapter 1) |

Chapter 21 adds measures of spread, like percentiles and the standard deviation, which tell you how far values stray from the average.

### Weighted averages

*"What's Riverstone's average discount?"*

Every order line has a discount of 0%, 5%, 8%, 10%, or 12%. The simple average of the discount on all 326 lines is **4.06%**. But a 12% discount on a ₹50,000 line costs far more than 12% on a ₹1,000 line. To know how much discounting costs the business, each line's discount must count in proportion to its value. That's a **weighted average**:

> weighted average = sum of (value × weight) ÷ sum of weights

Weighted by each line's value before discount, the average discount is **4.69%**. You can check it without a formula: the lines were worth ₹4,548,725 at list price and ₹4,335,471 after discounts, so discounts took ₹213,254, and ₹213,254 ÷ ₹4,548,725 = 4.69%. ✓ Larger lines tend to get larger discounts (5.3% on average for lines worth ₹20,000 or more, 3.8% for smaller ones), which is why the weighted figure is higher.

The same trap appears with prices. Riverstone's four product categories sold at average net prices of ₹435 (Storage), ₹341 (Kitchen), ₹1,273 (Industrial), and ₹1,121 (Furniture) per unit. The simple average of those four prices is ₹793. But the company sold 9,475 units for ₹4,335,471, an average of **₹458 per unit**, because Storage and Kitchen sold thousands of units and Furniture sold 30. **An average of averages ignores how many items stand behind each one.**

### The average of averages

The monthly business review pack often shows a row of monthly averages. Averaging that row gives the wrong annual figure:

- Average of the twelve monthly average order values: **₹24,243**.
- Actual average order value for the year: ₹4,335,471 ÷ 173 orders = **₹25,061**.

The busy months (September to November, with 18 to 21 orders each and high order values) count the same as quiet January with 8 orders. To combine averages, go back to the totals: add up all the revenue, add up all the orders, then divide.

> **Spreadsheet link.** `=AVERAGE(B2:B174)` and `=MEDIAN(B2:B174)` on the `orders` sheet give ₹25,061 and ₹21,375; `=COUNTIF(B2:B174,">"&E1)` counts the 70 orders above the mean. A weighted average is `=SUMPRODUCT(values, weights)/SUM(weights)`, which is how the `discounts` sheet gets 4.69%. The functions have the same names in Excel and Google Sheets.

---

## 4.6 Rounding and significant figures

Rounding makes numbers readable. It also creates small puzzles that make careful readers distrust a report.

### Shares that don't add up to 100%

Riverstone's 2025 revenue by segment, rounded to whole percentages:

| Segment | Share (whole %) | Share (one decimal) |
|---|---|---|
| Wholesale | 39% | 39.3% |
| Retail | 34% | 34.3% |
| Hospitality | 26% | 26.4% |
| **Total** | **99%** | **100.0%** |

Nothing is missing. The unrounded shares are 39.27%, 34.34%, and 26.39%, and each one rounded down a little. Rounding to one decimal happens to fix it here, but not always: the same thing can happen at any precision (exercise 8). You have three honest options: show one more decimal place, add a note ("shares may not add to 100% because of rounding"), or leave it and expect the question. Never quietly change one number to force the total, because then the table no longer matches the data.

### Round at the end, not in the middle

Rounding in the middle of a calculation carries the error forward. Section 4.2's margin example showed it: from rounded margins, the January to February fall looks like 3.2 points; from the real ones, it's 3.1. Keep full precision in the spreadsheet or calculator, and round only what you show.

### Significant figures and false precision

The **significant figures** of a number are the digits that carry meaning. ₹4,335,471 has seven. Does the reader need all seven? In a finance reconciliation, yes. In a meeting, "about ₹43 lakh" or "₹4.3 million" says the same thing and is easier to remember.

The opposite mistake is **false precision**: more digits than the data can support. *"Customers take an average of 31.6 days to pay"* (Chapter 3) is correct arithmetic from five invoices. With five invoices, "about a month" is more honest. The number of digits you write is a claim about how sure you are.

A rough guide for reports:

- **Money in tables:** whole rupees in detail tables; thousands or lakhs in summaries, with the unit stated in the header.
- **Percentages:** one decimal place, unless the numbers are small samples (then whole numbers or "about").
- **Averages of small counts:** round more, and give the count: "31.6 days (5 invoices)".

---

## 4.7 Reading tables and charts correctly

Before you read any number in a table or chart, read the frame around it. Five checks catch most misreadings:

1. **Units.** Rupees, thousands, lakhs, crores, or millions? Percent or percentage points? A column headed "Revenue (₹ lakh)" with a value of 43.4 means ₹4,340,000.
2. **Period and cut-off.** A month, a quarter, year to date? Chapter 3 showed that the same report run on different dates gives different numbers.
3. **Per-period or cumulative.** A **cumulative** (running total) line always goes up as long as the values are positive, even in a terrible month. December 2025's revenue fell 30.6%, but the year-to-date line still rose.
4. **Definition.** Booked, billed, or collected? With or without cancellations? (Chapter 3.)
5. **The axis.** Where does it start?

The last one deserves a picture.

![Two bar charts of the same twelve monthly gross margins; with the axis starting at 23% November's bar looks tiny, with the axis starting at 0% it looks like a modest dip](figures/fig4-4-same-numbers-two-axes.svg)

*Figure 4.4 — The same twelve numbers. A bar chart whose axis doesn't start at zero turns a 3.9-point dip into what looks like a collapse.*

In the left chart of Figure 4.4, the axis starts at 23%, so November's 24.0% bar is about a fifth the height of October's 27.9%. The eye reads "November's margin was a fifth of October's". In the right chart, starting at zero, the bars are 24 and 28 units tall, and the dip looks like what it is.

The rule: **bar charts must start at zero**, because readers compare bar *lengths*. Line charts can start elsewhere, because readers compare *positions* and *slopes*, but the axis should be labeled clearly. Chapter 15 covers chart choice and design in depth.

> **Watch out: one chart, two axes.** A chart with revenue on a left axis and margin on a right axis lets the designer stretch either line to make them appear to move together. When you see two vertical axes, read each line against its own axis before believing the pattern.

---

## 4.8 Probability: how often, out of how many

A **probability** is how often something happens, out of how many chances. Written as a fraction, a decimal, or a percentage, it's always between 0 (never) and 1 (always), or 0% and 100%. You don't need formulas to use it well; you need to keep asking "out of how many?"

### Counting what happened

In 2025, **2 of 175 orders** were cancelled. As a rate: 2 ÷ 175 = **1.1%**, or about 1 order in 88. In the first quarter of 2026 (the mini database), 1 of 12 orders was cancelled: **8.3%**.

Did Riverstone's customers get seven times more likely to cancel? Almost certainly not. With 12 orders, a single cancellation moves the rate by 8.3 points. **Small counts make rates jumpy.** Before comparing two rates, look at how many cases each is based on; Chapter 22 shows how to judge whether a difference is bigger than chance.

### "At least one"

*"If each order has a 1.1% chance of being cancelled, what's the chance that at least one of the next 20 orders is cancelled?"*

It's easier to work out the chance that *none* is cancelled and subtract from 1. The chance one order goes through is 1 − 0.0114 = 0.9886. The chance all 20 go through is 0.9886 multiplied by itself 20 times, which is 0.795. So the chance of at least one cancellation is 1 − 0.795 = **20.5%**. Using the first quarter's 8.3% rate instead gives **82.5%**. The rate you assume changes the answer completely.

(This assumes one order's cancellation doesn't affect another's, which is called **independence**. If one big customer cancels several orders at once, the assumption breaks.)

### Chaining stages

Chapter 13's sales funnel took 30 unique leads to 22 contacted, 14 quoted, and 6 won. Each step has its own rate: 22 of 30 (73.3%), 14 of 22 (63.6%), and 6 of 14 (42.9%). The chance that a new lead is eventually won is the rates multiplied: 0.733 × 0.636 × 0.429 = **0.200**, or 20%, which matches 6 of 30. ✓

That makes planning concrete. To win 10 new customers at a 20% win rate, the sales team needs about 10 ÷ 0.20 = **50 leads**. To win more with the same number of leads, improve the weakest step.

### The order of "given" matters

Of the 173 orders, 16 were worth more than ₹50,000, and 10 of those came from wholesale customers, who placed 55 orders in all.

- Chance an order is over ₹50,000: 16 ÷ 173 = **9.2%**.
- Chance a **wholesale** order is over ₹50,000: 10 ÷ 55 = **18.2%**. This is a **conditional probability**: the chance of one thing *given* another. The denominator shrinks to wholesale orders only.
- Chance a large order is **from wholesale**: 10 ÷ 16 = **62.5%**.

The last two sound alike and differ by a factor of more than three, because the denominators differ. Mixing them up is one of the most common errors in medicine, law, and business alike: "most large orders are wholesale" is not the same as "most wholesale orders are large". Chapter 21 treats conditional probability and Bayes' rule properly.

---

## 4.9 Orders of magnitude and quick estimation

The **order of magnitude** of a number is its rough size in powers of ten: thousands, lakhs, millions, crores. Getting the order of magnitude right catches more errors than any formula, because the most damaging mistakes are the ones that are off by a factor of 10 or 100: a misplaced decimal, a figure in thousands read as rupees, an extra zero.

### Indian and international units

Indian business writing uses lakhs and crores; international writing uses thousands, millions, and billions. You'll switch between them constantly.

| Indian | Digits | International |
|---|---|---|
| 1 lakh | 100,000 | 100 thousand |
| 10 lakh | 1,000,000 | 1 million |
| 1 crore (100 lakh) | 10,000,000 | 10 million |
| 100 crore | 1,000,000,000 | 1 billion |

Riverstone's 2025 revenue in the one-year database, ₹4,335,471, is about ₹43.4 lakh, ₹0.43 crore, or ₹4.3 million. This book writes rupees with international grouping (₹4,335,471), and mentions lakhs now and then for readers who think in them.

### Sanity checks: does the number fit?

When a number arrives, check it against another number you already trust. Two examples from Riverstone:

- **Revenue per day.** ₹43 lakh a year is about ₹11,878 a day. Separately, 3.3 orders a week at ₹25,061 each is about ₹11,911 a day. Two different routes land within ₹50 of each other, so both numbers are probably sound.
- **Units from revenue.** October's revenue was ₹681,071, and the year's average price was ₹458 a unit. So October probably shipped about 681,071 ÷ 457.57 ≈ **1,488 units**. The database says **1,625**. The estimate is 8.4% low, because October sold relatively more low-priced kitchen items and fewer ₹1,450 industrial crates than the year as a whole, but it's the right order of magnitude. If the database had said 16,250 or 162, you'd know something was wrong before looking at a single row.

### Estimating from nothing

Sometimes there's no data yet: *"Is it worth building a report for this?"* or, in interviews, *"How many plastic storage boxes are sold in Mumbai each year?"* These are called **Fermi estimates** or **guesstimates**. The method is always the same:

1. Break the unknown into smaller pieces you can guess: households, share that buy boxes, boxes per purchase, purchases per year.
2. Write each assumption down with a round number.
3. Multiply, and round the answer to one or two significant figures.
4. Sanity-check the answer against anything you know, and say which assumption matters most.

Being close matters less than being clear. A reader can replace a bad assumption; they can't fix reasoning they can't see. Chapter 75 has worked guesstimates for interviews.

---

## 4.10 Number tricks in business news

Most misleading numbers in headlines, press releases, and sales decks are true. They mislead through what they leave out. Here are the common tricks, with invented examples, and the question that exposes each one.

| Trick | Example | Question to ask |
|---|---|---|
| **Tiny base** | "Profits up 300%!" (from ₹2 lakh to ₹8 lakh) | *300% of what?* |
| **Relative without absolute** | "New process doubles the risk of a defect" (from 1 in 10,000 to 2 in 10,000) | *What are the actual numbers before and after?* |
| **Cherry-picked period** | "Revenue up 264% since June" (the slowest month to the busiest) | *Why start and end there? What about the same period last year?* |
| **"Up to"** | "Up to 70% off" (on one item) | *How many items, and what's the typical discount?* |
| **Percent for points** | "Interest rates rise 1%" (from 8% to 9%) | *Points or percent?* |
| **Average hiding the spread** | "Average order ₹25,061" (most orders are smaller) | *What's the median?* |
| **Truncated axis** | a bar chart starting at 23% (Figure 4.4) | *Where does the axis start?* |
| **Mixed units** | "₹43 lakh" next to "₹4.3 million" in the same slide | *Are these in the same unit?* |
| **Record without context** | "Our best month ever!" (October, in a seasonal business) | *Best compared with the same month last year?* |
| **Survivors only** | "Our customers grew 40% on average" (counting only customers who stayed) | *Who was left out?* |

A good habit is to rewrite a headline number into a plain sentence with both numbers and the base: *"Profit rose from ₹2 lakh to ₹8 lakh, a fourfold increase from a small base."* If the rewritten sentence sounds much less exciting, the original was relying on a trick.

> **Interview extra point.** When a case interview gives you a growth figure or a percentage, restate it with its base and period before you use it: *"So revenue went from ₹20 lakh to ₹32 lakh over four years, which is about 12.5% a year compounded."* It shows you check numbers before trusting them, which is what interviewers for analyst roles are testing. Chapter 73 (statistics and probability) and Chapter 75 (metrics, case studies, and guesstimates) have practice questions.

---
## Common mistakes and how to spot them

| Mistake | Symptom | Fix |
|---|---|---|
| Adding percentages that apply one after another | "50% + 20% off = 70% off" | Multiply what remains: 0.5 × 0.8 = 0.4, so 60% off |
| Reversing a percentage by adding it back | list price from a discounted price comes out too low | Divide by (1 − discount) |
| Saying "percent" for a change in a percentage | "margin fell 3.9%" when it fell 3.9 points | Use points for the difference; give before and after |
| Averaging growth rates that compound | typical monthly growth of 13.1% when the steady rate is 7.3% | Use (end ÷ start)^(1/periods) − 1, or `RRI` |
| Quoting growth between hand-picked months | "up 264%" from the slowest to the busiest month | Compare like with like: full years, or same month last year |
| Reporting only the mean for skewed data | most orders feel "below average" | Report the median too |
| Averaging averages | ₹24,243 instead of ₹25,061 | Go back to the totals and divide once |
| Using a simple average when items differ in size | average discount 4.06% instead of 4.69% | Weight by value, units, or count |
| Rounding in the middle of a calculation | small errors that grow, points that don't match | Keep full precision; round only what you show |
| Too many digits | "31.6 days" from five invoices | Match the digits to how sure you are; give the count |
| Bar charts with a truncated axis | a small dip looks like a collapse | Start bars at zero |
| Comparing rates from very different sample sizes | 1.1% vs 8.3% cancellation read as a real change | Give the counts; be cautious with small samples |
| Confusing "A given B" with "B given A" | "most large orders are wholesale" read as "most wholesale orders are large" | Say the denominator out loud |

---

## In the real world: the board slide

It's the first week of January 2026. The managing director is presenting Riverstone's year to the board, and Vikram Singh's team has drafted the sales slide. Before it goes to the MD, Anita asks Meera Iyer to check the numbers. "Nothing fancy. Make sure nothing on it will embarrass us."

The draft slide has six claims. Meera takes them one at a time, and for each one asks: *of what, and compared with what?*

**1. "2025 revenue up 117%."** Meera finds where it comes from: December's ₹439,824 against January's ₹202,640. That's true, but it compares two single months of a seasonal business, and it isn't "2025 revenue" at all. The slide has no 2024 figures to compare with, so it can't support any year-on-year growth claim. What the board can use: *full-year revenue ₹43.4 lakh (₹4,335,471), 102.3% of the annual target.*

**2. "Average monthly growth: 13.1%."** The average of the eleven monthly changes. Meera grows January by 13.1% eleven times and gets ₹782,621 for December, almost double the real figure. The compound rate is 7.3%, but she recommends dropping the line entirely: in a year that peaks in October and dips in the monsoon, a "monthly growth rate" describes nothing real.

**3. "Gross margin down 3.9% in November."** It was 27.9% in October and 24.0% in November: down 3.9 *points*, a 14.0% fall. More useful for a board: *full-year gross margin 26.2%; November was the lowest month.*

**4. "Average order value: ₹24,243."** Meera recognizes the number from the monthly pack: it's the average of the twelve monthly averages. The real figure is ₹4,335,471 ÷ 173 = **₹25,061**. She adds the median, **₹21,375**, because the MD is likely to be asked what a typical order looks like.

**5. The segment pie chart: Wholesale 39%, Retail 34%, Hospitality 26%.** They add to 99%. A board member will notice. One decimal fixes it: 39.3%, 34.3%, 26.4%.

**6. The margin bar chart.** Its axis starts at 23%, so November's bar is a stub. Meera redraws it from zero (Figure 4.4).

There's also a note under the slide's goal for 2028, ₹60 lakh: *"That's about ₹5.5 lakh more each year."* Meera adds the growth rate that the plan really needs, **11.4% a year**, because the board will think in percentages and "₹5.5 lakh a year" gets harder every year as a percentage.

She sends the corrected slide back with a four-line note explaining each change and the check behind it. Vikram's reply: "The 117% was the best number on the slide." Anita's: "It was also the one the board would have questioned first."

Nothing Meera did needed more than a calculator and two questions. What it needed was the habit of never passing a number on without knowing what it's a percentage *of*.

---

## Tools

- **A calculator.** Your phone's calculator in landscape (scientific) mode has a power key (`xʸ` or `^`) for compound growth.
- **A spreadsheet** (optional). Excel and Google Sheets both have every function used here: `AVERAGE`, `MEDIAN`, `MODE`, `SUMPRODUCT`, `ROUND`, `COUNTIF`, and `RRI`. Chapter 10 teaches them from the beginning.
- **The companion workbook** `numbers_practice.xlsx` (Appendix E). Its `monthly`, `orders`, `discounts`, and `segments` sheets hold the 2025 numbers from this chapter with the formulas already in place, so you can check every figure and try your own. It was generated from the one-year database, and its formulas were recalculated and compared with this chapter's numbers.

---

## The project: check five statistics

**Goal:** take five numbers from the real world and check each one the way Meera checked the board slide.

**Step 1. Collect five statistics.** Find them in news articles, company annual reports or investor presentations, advertisements, or presentations at your workplace. Aim for variety: at least one growth figure, one percentage or share, one average, one chart, and one comparison between two groups. Copy the exact wording and note the source and date.

**Step 2. Record each one in a table.**

| Column | What to write |
|---|---|
| `claim` | the exact words, e.g. "Sales up 40% in three years" |
| `source_and_date` | where and when it was published |
| `base` | what the number is a percentage *of*, or an average *of* |
| `comparison` | what it's compared with: which period, group, or target |
| `type` | percent change, points, share, ratio, average, probability, chart |
| `check` | your recalculation, or the missing information you'd need |
| `trick_found` | none, or which trick from section 4.10 |
| `rewrite` | an honest one-sentence version with both numbers and the base |

**Step 3. Recalculate** whatever you can from the numbers given. For growth over several years, work out the CAGR. For a percentage, find both the part and the whole. For a chart, check the axis and the units.

**Step 4. Name what's missing.** Many claims can't be checked because the base, the period, or the sample size isn't given. Saying exactly what's missing is a result.

**Step 5. Rewrite each claim** as one honest sentence.

**Step 6. Write a three-line summary:** how many of the five held up, the most common problem, and the one question you'll ask next time you see a number like it.

**Deliverable:** your table and summary. Keep it; Chapter 5 asks you to turn one of these claims into an analyst's question.

---

## You've got it when…

- [ ] I can calculate a percentage of a number, a share, a percent change, and a list price from a discounted price.
- [ ] I know that a rise and an equal fall don't cancel, and that discounts stack by multiplying.
- [ ] I say "percentage points" for the difference between two percentages.
- [ ] I ask what the denominator is before comparing ratios or rates.
- [ ] I calculate compound growth and CAGR, and I never average growth rates that compound.
- [ ] I choose between mean, median, and mode for a purpose, and use weighted averages when items differ in size.
- [ ] I don't average averages.
- [ ] I round only at the end, and I don't write more digits than the data supports.
- [ ] I check a chart's units, period, and axis before reading its bars.
- [ ] I can work out "at least one" and conditional probabilities by counting.
- [ ] I sanity-check numbers by estimating them another way.
- [ ] I've checked five real statistics and rewritten each one fairly.

---

## Recap

- **Every percentage is a percentage of something.** Ask *of what?* and *compared with what?*
- Percent change is (new − old) ÷ old. Reverse a discount by dividing by (1 − discount). Rises and falls don't cancel, and discounts stack by multiplying.
- The difference between two percentages is measured in **percentage points**. Riverstone's margin fell from 27.9% to 24.0%: 3.9 points, a 14.0% fall.
- **Ratios and rates** depend on the denominator. Wholesale earned 2.23 times as much per customer as Hospitality, though Hospitality had more customers.
- **Compound growth** = (end ÷ start)^(1/periods) − 1. Riverstone's 2025 compound monthly rate was 7.3%; averaging the monthly changes gives a misleading 13.1%. **CAGR** is the yearly version: ₹43.4 lakh to ₹60 lakh in three years needs 11.4% a year. The **rule of 72** estimates doubling time.
- The **mean** (₹25,061 per order) is pulled up by large values; the **median** (₹21,375) shows what's typical; the **mode** suits categories. Use **weighted averages** when items differ in size (average discount 4.69%, not 4.06%), and never average averages.
- **Round at the end.** Shares may not add to 100%; say so or add a decimal. Don't claim more precision than the data has.
- **Read the frame first:** units, period, cumulative or not, definition, and where the axis starts. Bar charts start at zero.
- **Probability** is how often, out of how many. Small counts make rates jumpy. "At least one" = 1 − chance of none. Chained stages multiply. "A given B" isn't "B given A".
- **Estimate** to catch errors of 10× or 100×, and convert confidently between lakhs, crores, and millions.
- **Number tricks** leave out the base, the absolute numbers, the period, or the spread. Rewrite the claim with both numbers and the base.

---

## Practice exercises

### Warm-up

1. Calculate: (a) a 5% discount on an order worth ₹14,550; (b) what percentage ₹26,220 is of ₹58,020 (order 5012's share of March 2026 bookings, Chapter 3); (c) the price of a ₹780 Storage Box 25L after 8% off.
2. From Chapter 13's quarterly table: Kitchen revenue was ₹133,888 in the first quarter of 2025 and ₹461,146 in the fourth; Industrial was ₹275,450 in the third quarter and ₹292,040 in the fourth. Calculate each percent change.
3. Wholesale's share of revenue was 39.3% in 2025. If it's 42.0% next year, what's the change in percentage points, and what's the percent change? Write one correct sentence for each.
4. The 11 non-cancelled orders in the mini database (first quarter of 2026) were worth: ₹14,700, ₹73,260, ₹16,250, ₹14,550, ₹14,640, ₹32,625, ₹23,325, ₹76,560, ₹20,100, ₹11,700, ₹26,220. Find the mean, the median, and the mode. Which better describes a typical order, and why?

### Core

5. (a) Northgate paid ₹76,560 for an order after a 12% discount. What was the order worth at list price? (b) Riverstone raises a price by 8%, then gives a customer 8% off the new price. Is the customer paying more or less than before, and by what percent?
6. A distributor's revenue grew from ₹25 lakh to ₹40 lakh over five years. (a) What was its CAGR? (b) Using the rule of 72, roughly how long would it take to double at that rate? (c) Why is "it grew 12% a year" (60% ÷ 5) wrong?
7. Riverstone's 2025 gross margin by category was: Storage 26.9% on ₹2,297,974 of revenue; Kitchen 33.2% on ₹1,208,030; Industrial 13.6% on ₹795,830; Furniture 24.2% on ₹33,638. (a) What's the simple average of the four margins? (b) What's the margin weighted by revenue? (c) Which one is the company's gross margin, and why are they different?
8. The categories' shares of 2025 revenue, to one decimal place, are Storage 53.0%, Kitchen 27.9%, Industrial 18.4%, and Furniture 0.8%. A manager says the table is wrong. Explain what's happening and write the note you'd put under the table.
9. Riverstone wins 20% of its unique leads. (a) How many leads does it need to win 15 new customers? (b) If three new leads arrive this week and each has a 20% chance of being won, what's the chance at least one is won? (c) What assumption does (b) make, and when might it be false?

### Stretch

10. A local newspaper profile of Riverstone runs the headline *"Riverstone revenue soars 264%"*, based on June 2025 (₹186,928) and October 2025 (₹681,071). Explain in two sentences why the headline misleads, and write an honest replacement using numbers from this chapter.
11. November 2025's revenue was ₹633,408. Using the year's average price of ₹458 per unit, estimate how many units Riverstone shipped in November. The database says 1,355. How far off is your estimate, in percent? Is that good enough for a sanity check, and why?
12. In 2025, Riverstone received 29 orders worth ₹734,312 in the first quarter and 59 orders worth ₹1,754,302 in the fourth. (a) Calculate each quarter's average order value. (b) Calculate the average order value for the two quarters combined. (c) Explain why the average of your two answers in (a) isn't the answer to (b).

### Think about it (no calculation needed)

13. A company's press release says, "Our employees earn an average of ₹18 lakh a year." What else would you want to know before believing that this describes a typical employee?
14. A sales dashboard shows only a year-to-date revenue line, and it has gone up every month. Explain how this chart could hide a bad month, and suggest a better chart to put next to it.
15. A sales manager announces, "Our win rate went up 50% this quarter!" Write the two questions you'd ask before sharing the news.

---

## Key terms

percentage · percent of · share / proportion · percent change · reverse percentage · percentage point · ratio · rate · denominator · month-over-month growth · compound growth rate · compounding · rule of 72 · CAGR (compound annual growth rate) · average · mean · median · mode · right-skewed · weighted average · average of averages · rounding · significant figures · false precision · cumulative / running total · truncated axis · probability · independence · conditional probability · order of magnitude · lakh · crore · sanity check · Fermi estimate / guesstimate · base effect · relative vs absolute change

*(All terms are defined in the Glossary, Appendix A.)*

---

## Where this leads

- **Chapter 5, Thinking Like an Analyst,** turns the questions *of what?* and *compared with what?* into a method for breaking down any business question.
- **Chapters 10 and 11** build these calculations into spreadsheets: percentages, `SUMPRODUCT`, pivot tables of shares and averages.
- **Chapter 13** calculates month-over-month growth, running totals, and moving averages in SQL on the same 2025 data you used here.
- **Chapter 15, Data Visualization Principles,** goes deeper into honest charts: axes, chart choice, and the visual tricks from section 4.7.
- **Chapter 21, Descriptive Statistics & Probability,** adds spread, percentiles, distributions, and Bayes' rule.
- **Chapter 22, Statistics Without Fooling Yourself,** shows how to tell whether a difference between two rates is real or chance.
- **Chapter 23, Business Acumen, KPIs & Metrics,** applies growth rates, margins, and ratios to reading a company's financial statements.
- **Interview preparation:** percentage, growth, averages, and probability questions appear in Chapter 73 (statistics, probability, and experimentation), and guesstimates and metric questions in Chapter 75, with model answers.

---

## Answers to practice exercises

*(In the finished book these move to Appendix G.)*

**1.** (a) 0.05 × ₹14,550 = **₹727.50**. (b) ₹26,220 ÷ ₹58,020 = 0.452, so **45.2%**. (c) ₹780 × 0.92 = **₹717.60**.

**2.** Kitchen: (₹461,146 − ₹133,888) ÷ ₹133,888 = **+244.4%**; revenue more than tripled. Industrial: (₹292,040 − ₹275,450) ÷ ₹275,450 = **+6.0%**.

**3.** 42.0 − 39.3 = **2.7 percentage points**: "Wholesale's share rose 2.7 points, from 39.3% to 42.0%." (42.0 − 39.3) ÷ 39.3 = **6.9%**: "Wholesale's share of revenue grew by 6.9%." The first is clearer for most readers.

**4.** Total ₹323,930 ÷ 11 = **mean ₹29,448**. Sorted: ₹11,700, ₹14,550, ₹14,640, ₹14,700, ₹16,250, **₹20,100**, ₹23,325, ₹26,220, ₹32,625, ₹73,260, ₹76,560; the sixth value is the **median, ₹20,100**. No value repeats, so there's **no mode**. The median describes a typical order better: two large wholesale orders (₹73,260 and ₹76,560) pull the mean up, and 8 of the 11 orders are below it.

**5.** (a) ₹76,560 ÷ 0.88 = **₹87,000**. (Check: 12% of ₹87,000 is ₹10,440, and ₹87,000 − ₹10,440 = ₹76,560. ✓) (b) 1.08 × 0.92 = 0.9936. The customer pays **0.64% less** than the original price, because the 8% discount is taken from a bigger number than the 8% rise was.

**6.** (a) ₹40 lakh ÷ ₹25 lakh = 1.6. 1.6^(1/5) = 1.0986, so the CAGR is **9.9% a year**. (b) 72 ÷ 9.9 ≈ **7.3 years** (the exact answer is 7.4). (c) 60% ÷ 5 = 12% ignores compounding: each year's growth is calculated on a bigger base, so a steady 9.9% a year is enough to add 60% in five years. Growing ₹25 lakh by 12% a year for five years would reach about ₹44 lakh, not ₹40 lakh.

**7.** (a) (26.9 + 33.2 + 13.6 + 24.2) ÷ 4 = **24.5%**. (b) Weighted by revenue, the margin is **26.2%**: total revenue ₹4,335,471 minus total product cost ₹3,198,250, divided by revenue. (c) The weighted figure is the company's gross margin. The simple average gives tiny Furniture (under 1% of revenue) the same say as Storage (more than half), and it gives low-margin Industrial (18.4% of revenue) a quarter of the weight, which drags the simple average down.

**8.** Nothing is wrong. The unrounded shares (53.00%, 27.86%, 18.36%, 0.78%) add up to 100%, but three of them rounded up, so the rounded shares add to 100.1%. Note: *"Shares are rounded to one decimal place and may not add to exactly 100%."* Don't adjust one share to force the total.

**9.** (a) 15 ÷ 0.20 = **75 leads**. (b) Chance none is won: 0.8 × 0.8 × 0.8 = 0.512. Chance at least one is won: 1 − 0.512 = **48.8%**. (c) It assumes the leads are **independent** and each has the same 20% chance. It's false if, for example, all three come from the same company or from a trade fair where one bad impression affects everyone, or if one lead is far warmer than the others.

**10.** It compares the slowest month with the busiest month of a seasonal business, so most of the "growth" is the calendar, and it says nothing about the year. A single-month comparison can't be called revenue growth for the company. Honest replacement: *"Riverstone's 2025 revenue was ₹43.4 lakh, 2.3% above its annual target, with a festive-season peak of ₹6.8 lakh in October."*

**11.** ₹633,408 ÷ ₹458 ≈ **1,383 units** (using the unrounded ₹457.57, about 1,384). Against the actual 1,355, that's about **2.1% too high**. That's good enough: a sanity check is looking for errors of 10 times or 100 times, and an estimate within a few percent confirms the order of magnitude. Differences in the product mix explain the rest.

**12.** (a) First quarter: ₹734,312 ÷ 29 = **₹25,321**. Fourth quarter: ₹1,754,302 ÷ 59 = **₹29,734**. (b) (₹734,312 + ₹1,754,302) ÷ (29 + 59) = ₹2,488,614 ÷ 88 = **₹28,280**. (c) The average of the two quarterly figures, ₹27,528, gives each quarter equal weight, but the fourth quarter had twice as many orders. The combined figure must come from the totals.

**13.** Whether "average" is the mean or the median (a few very high salaries, such as senior leaders', pull the mean up); the median and the range; who is included (full-time only? contractors? leaders?); whether it's salary alone or includes bonuses and benefits; and the date and location. The median, with the number of employees, describes a typical employee far better.

**14.** A cumulative line rises whenever a month's revenue is positive, so a month that fell sharply (like December 2025, down 30.6%) still shows as the line going up, only less steeply. Put a monthly bar chart next to it (starting at zero), ideally with each month's target or the same month last year, so a bad month is visible as a short bar.

**15.** (1) *From what to what?* A rise from 10% to 15% is "up 50%" but only 5 points; a rise from 2% to 3% is also "up 50%". (2) *Out of how many leads, and were they counted the same way?* With a small number of leads, one or two extra wins can move the rate a lot, and a change such as removing duplicate leads (Chapter 13) raises the win rate without any change in selling.
