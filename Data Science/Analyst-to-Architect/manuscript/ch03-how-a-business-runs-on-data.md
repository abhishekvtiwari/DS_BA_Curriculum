# Chapter 3. How a Business Runs on Data

*Part 0 — First Principles: Data from Zero*

> **Chapter at a glance**
>
> **You will learn to:** name a company's departments and the data each creates · follow one order from enquiry to cash, and say which system records each step · explain what ERP, CRM, HRMS, POS, e-commerce, and support systems do · tell a transaction from a report, and bookings from billings from collections · define a KPI so two people calculate the same number · describe how dashboards, meetings, and decision rights turn data into decisions · find where people copy, re-type, and email data by hand, and estimate the cost.
>
> **Before you start:** Chapter 1 (rows, columns, grain, data quality) and Chapter 2 (files, databases, and APIs).
>
> **Time needed:** 3–4 hours, including the exercises and the project.
>
> **Tools:** a pen and a notebook. A spreadsheet or a free diagram tool is useful for the project, but optional.
>
> **Practice data:** Riverstone Supplies' first quarter of 2026: twelve orders, ten invoices, and ten payments from the mini database you'll query yourself in Chapter 12. Every number in this chapter was calculated from that database and checked by script.

---

## Why this matters

In Chapter 1 you learned what data is. In Chapter 2 you learned where it lives. This chapter answers the question that sits between those and every job in this book: **why does a business have all this data in the first place, and who uses it?**

The short answer is that a company *is* a chain of people handing work to each other. A salesperson hands an order to the warehouse. The warehouse hands a delivery to finance. Finance hands a number to the managing director. Every handover leaves a record, and those records are the data you'll clean, query, chart, and model for the rest of your career.

Analysts who understand this chain are far more useful than analysts who only know the tools. When a manager asks, *"What were sales last month?"*, the analyst who knows the chain asks one question back: *"Orders placed, invoices raised, or cash received?"* Those are three different numbers. At Riverstone Supplies in January 2026 they were ₹116,210, ₹104,210, and ₹0. By the end of this chapter you'll know exactly why, and you'll never again hand over a "sales" number without saying which one it is.

This chapter also starts the book's **automation** thread. Before you can automate anything, you have to see where people work by hand. Section 3.7 shows you how.

---

## In plain English

Think of a relay race. Four runners, one baton. Each runner takes the baton, runs their stretch, and hands it on. Races are often lost at the handovers.

A business works the same way, and **data is the baton**. The salesperson writes down what the customer wants and passes it on. The warehouse packs the goods, records what it shipped, and passes that on. Finance sends a bill, records what was paid, and passes it on to the people who write reports.

Three things follow from the picture:

- **Each runner only sees their own stretch.** The warehouse doesn't care how long the customer took to decide; sales doesn't see when the cash arrives. That's why different departments quote different numbers for the "same" thing.
- **Handovers are where things go wrong.** An order typed twice can be typed wrong once. A file emailed around can be out of date by the time it's opened.
- **Someone has to watch the whole race.** Managers need to know how the team is doing, not just each runner. That's what reports, KPIs, and dashboards are for, and it's where analysts come in.

---

## 3.1 The departments of a company and the data they create

Meet the company. **Riverstone Supplies** makes and distributes plastic storage boxes, kitchenware, industrial crates, and a small range of furniture. Its customers are retailers (like Sharma Hardware in Mumbai), hotels and caterers (like Green Leaf Hotels in Pune), and wholesalers (like Coastal Foods in Chennai). It has two plants:

- **Plant 1, Taloja** (Navi Mumbai), which makes storage boxes and kitchenware.
- **Plant 2, Chakan** (Pune), which makes industrial crates and furniture.

Finished goods go to the central warehouse, **Bhiwandi Main**, near Mumbai, and are shipped to customers from there.

Each department exists to do a job, and creates data as a side effect of doing it. Figure 3.1 shows the eight you'll meet most often.

![Eight departments of Riverstone Supplies, each listing the data it creates, all feeding management decisions](figures/fig3-1-departments-and-their-data.svg)

*Figure 3.1 — Every department creates data while doing its own job. Management needs all of it to decide.*

| Department | Its job | Data it creates | A question the data answers |
|---|---|---|---|
| **Sales** | win and keep customers | enquiries (**leads**), quotes, orders, visit notes | *Which customers are ordering less than last year?* |
| **Marketing** | make the right people aware of the products | campaigns, website visits, trade-fair contacts | *Which campaign brought in enquiries that became orders?* |
| **Purchasing** | buy raw materials and packaging | suppliers, purchase orders, goods received | *Which supplier delivers late most often?* |
| **Production** | make the goods | production plans, machine runs, output, scrap | *How much plastic did we waste last month, and on which machine?* |
| **Warehouse and dispatch** | store, pick, pack, and ship | stock levels, picking lists, **delivery challans**, proofs of delivery | *How many orders left the warehouse late?* |
| **Finance** | bill customers, collect cash, pay bills, keep the books | invoices, payments, expenses, budgets, tax records | *How much are customers overdue, and who?* |
| **HR** | hire, pay, and look after employees | employee records, attendance, payroll, hiring | *How long does it take to fill a job?* |
| **Customer support** | fix problems after the sale | complaints, **tickets**, returns, resolution times | *Which product causes the most complaints?* |

A **lead** is a possible customer who has shown interest but hasn't bought. A **delivery challan** is the document that travels with goods in India, listing what's in the truck (elsewhere, a delivery note).

Finance needs sales' orders to raise invoices. Production needs them to plan what to make. Management needs everything to decide where to spend money. **Data created in one department is almost always used in another**, and that is the root of most of the problems, and most of the jobs, in this book.

> **Try it.** Pick a company you've dealt with recently: a food delivery app, your bank, a hospital. Name three departments it must have and one record each creates about *you*.

---

## 3.2 Following one order from enquiry to cash

To see how departments depend on each other's data, follow one piece of business all the way through. This journey is called **order to cash**, or **lead to cash** when it includes winning the customer.

Here is a real order from Riverstone's database: **order 5001**, from Sharma Hardware, a retail customer in Mumbai. You'll query these exact rows in Chapter 12. The order has two lines:

| Product | Quantity | List price | Discount | Line value |
|---|---|---|---|---|
| Storage Box 10L | 20 | ₹450 | 0% | ₹9,000 |
| Water Bottle 1L | 50 | ₹120 | 5% | ₹5,700 |
| **Total** | | | | **₹14,700** |

Check it by hand: 20 × ₹450 = ₹9,000. 50 × ₹120 = ₹6,000, less 5% is ₹5,700. ₹9,000 + ₹5,700 = ₹14,700. ✓ (As in the rest of this book, tax is left out to keep numbers simple.)

The order row only says *who ordered what, when*. But it has a history before it and a future after it, and every step was recorded somewhere. Figure 3.2 shows all ten steps.

![Ten steps of order 5001, from a website enquiry in October 2025 to the January 2026 sales report, with the date, what happened, and the record created at each step](figures/fig3-2-one-order-enquiry-to-cash.svg)

*Figure 3.2 — One order, ten steps. Each box shows the date, what happened, and the record it left behind.*

**1. Enquiry (22 October 2025).** Rakesh, the buyer at Sharma Hardware, fills in the enquiry form on Riverstone's website: name, shop, city, phone, and "interested in storage boxes for our shop". The form creates a **lead** in the CRM, the sales team's system for tracking deals (section 3.3). Sharma Hardware isn't a customer yet; it's a row with a status of *New*.

**2. New customer (4 November 2025).** Neha Kulkarni, a sales executive, visits the shop. Rakesh wants to buy on credit, so finance runs a credit check and agrees **payment terms** of 30 days: Sharma Hardware can pay up to 30 days after each invoice. Finance creates the customer in the ERP, Riverstone's main business system, where it gets **customer ID 1** and a signup date of 2025-11-04. Every later order, invoice, and payment carries that ID.

**3. Quote (22 December 2025).** Rakesh asks for prices. Neha builds a quote, Q-2025-118, in a spreadsheet, emails it as a PDF, and logs it against the lead in the CRM. A **quote** is an offer: *these products, at these prices, until this date*.

**4. Order (5 January 2026).** Rakesh replies to the quote email: "Please send 20 of the 10-litre boxes and 50 bottles." Neha opens the ERP and **types the order in**: customer 1, two lines, prices, a 5% discount on the bottles that she agreed on the phone. The ERP creates **order 5001** with a status of *Pending*, dated 2026-01-05, with Neha as the sales rep.

**5. Stock check (5 January 2026).** Both products are **made to stock**: Plant 1 at Taloja makes them in advance and sends them to Bhiwandi Main. But Bhiwandi Main updates the ERP's stock figures once a day from its own spreadsheet, so Neha phones the warehouse to be sure. The stock is **reserved** for order 5001.

**6. Dispatch (6 January 2026).** The warehouse prints a **picking list**, picks and packs the boxes and bottles, and ships them with a delivery challan. The ERP marks the order *Shipped*.

**7. Invoice (6 January 2026).** When goods ship, the ERP raises **invoice 9001** for ₹14,700, dated 2026-01-06, **due** on 2026-02-05, 30 days later, because of the terms agreed in step 2. An **invoice** is the formal request for payment: the sale becomes money the customer owes.

**8. Delivery (8 January 2026).** The truck arrives. Rakesh signs a paper **proof of delivery** (POD). Someone at Bhiwandi Main scans it, emails it to finance, and updates the order to *Delivered*.

**9. Payment (2 February 2026).** Sharma Hardware pays ₹14,700 by bank transfer. The bank statement shows a short reference, "SHARMA HW JAN". A finance assistant works out that it pays invoice 9001 and records **payment 1** against it.

**10. Report (3 February 2026).** The team prepares the **January sales report**. Invoice 9001 is one of the three behind the line *"January: ₹104,210"*.

**It took a long time.** From enquiry to cash was 103 days. Once the order existed, things moved faster: order to invoice 1 day, invoice to payment 27 days, order to cash 28 days. Each gap comes from subtracting two dates recorded by two different departments.

**The data lives in several places.** The lead and quote are in the CRM; the customer, order, invoice, and payment in the ERP; the proof of delivery is a scanned image in someone's email; the report is an Excel file. To answer *"How long does it take to turn an enquiry into cash?"* you need two systems that don't share an ID for Sharma Hardware: the CRM knows it by a lead number, the ERP as customer 1.

**People carried the baton by hand at several handovers.** Neha re-typed the order and phoned about stock; someone scanned paper, matched a bank line by eye, and built the report. Section 3.7 puts a cost on these steps.

> **Simplification note.** Real processes have more branches: partial shipments, back orders, credit holds, returns, and credit notes. Order 5001 is a clean run. You'll meet messier cases in the data itself: order 5004 was cancelled, invoice 9002 was paid in two instalments, and invoice 9007 hasn't been paid at all.

---

## 3.3 Business systems: ERP, CRM, HRMS, POS, and e-commerce

A **business system** is software a department uses for its daily work, storing the records in a database (section 2.6). You'll hear these abbreviations in your first week of any data job.

| System | What it's for | Typical records | Main users | Examples of real products |
|---|---|---|---|---|
| **ERP** (enterprise resource planning) | running the core of the business: sales orders, stock, production, purchasing, invoicing, and accounts, all in one system | customers, products, orders, invoices, payments, stock movements, purchase orders | sales operations, warehouse, production, purchasing, finance | SAP, Oracle NetSuite, Microsoft Dynamics 365, Odoo; TallyPrime is common in smaller Indian firms |
| **CRM** (customer relationship management) | winning and keeping customers | leads, contacts, calls, meetings, quotes, deals and their stages | sales, marketing, customer success | Salesforce, HubSpot, Zoho CRM |
| **HRMS** (human resource management system) | managing employees | employee records, attendance, leave, payroll, hiring | HR, managers, every employee for leave and payslips | Workday, Zoho People, Keka |
| **POS** (point of sale) | recording sales at a shop counter | bills, items scanned, payment method, cashier, time | shop staff | the billing app at Sai Krupa General Store (Chapter 1); supermarket tills |
| **E-commerce platform** | selling online | product listings, carts, online orders, payments, website visits | online sales, marketing | Shopify, WooCommerce, marketplaces |
| **Support desk** (ticketing system) | tracking customer problems until they're fixed | tickets, messages, categories, status, time to resolve | customer support | Zendesk, Freshdesk |

Riverstone's set-up is typical for a mid-sized manufacturer. This book names its systems by type, because the lessons don't depend on the brand:

- **The ERP** holds customers, products, employees (as sales reps), orders, order lines, invoices, and payments, plus stock, production, and purchasing. People at Riverstone still call its invoicing module "the billing system"; that's where Imran exported his Friday file from in Chapter 2. **The mini database you'll use from Chapter 12 onward is a small copy of the ERP's sales tables.**
- **The CRM** holds leads, contacts, quotes, and the sales pipeline.
- **The website** shows the catalog and feeds enquiries to the CRM (customers don't order online). **The support desk** records complaints and returns. **The HRMS** holds employees and payroll.
- **Spreadsheets and email** fill every gap between them: quotes, the warehouse's stock sheet, the monthly report.

Riverstone has no POS, because it sells to businesses. But Sharma Hardware's POS knows exactly which Riverstone boxes sell on a Saturday afternoon, and Riverstone never sees that unless Sharma shares it: **the most useful data about your products often sits in someone else's system.**

### Systems of record and the gaps between systems

Every important fact should have one official source, its **system of record** (or **source of truth**). At Riverstone, that's the ERP for orders and invoices, the CRM for leads, and the HRMS for employees. When the CRM and the ERP disagree about what Sharma Hardware bought, the ERP wins.

The trouble is the gaps. Riverstone's CRM and ERP aren't connected: when a quote becomes an order, someone must mark the deal *Won* in the CRM, and a cancellation in the ERP never reaches the CRM unless someone remembers. Connecting systems so data flows between them automatically is **integration** (Chapters 45 and 51).

> **Spreadsheet link.** A spreadsheet can become a system of record by accident. If the warehouse's stock sheet is more current than the ERP, the sheet is now the source of truth for stock, with no access control or history (section 2.9).

---

## 3.4 Transactions and reports: booked, billed, and collected

Everything recorded in Figure 3.2 is a **transaction**: a record of one business event, written when it happens. *Invoice 9001 was raised for ₹14,700.* Transactions are the rows in a business system's database.

A **report** summarizes many transactions to answer a question (*"How much did we invoice in January?"*), at a point in time, using rules someone chose.

| | Transaction | Report |
|---|---|---|
| **What it is** | one event | a summary of many events |
| **Grain** (Chapter 1) | one order, one invoice, one payment | one month, one customer, one product |
| **Created** | by the business system, as work happens | by a person or a scheduled job, after the fact |
| **Changes?** | should be corrected, not rewritten; a cancellation is a new status or a new record | changes whenever the data or the rules change |
| **Example** | invoice 9001: ₹14,700, due 2026-02-05 | "January billings: ₹104,210" |

Systems for transactions are tuned to write one record quickly and safely; reporting needs to read millions and add them up. That's why growing companies move reporting into a separate **data warehouse** (Chapter 49).

### Three numbers called "sales"

Because reports apply rules, **two reports built from correct transactions can give different answers to the same question.** The classic case is "sales", which can mean three things, each counted at a different step of Figure 3.2:

- **Bookings**: the value of orders placed (step 4). The earliest sign of sales work.
- **Billings**: the value of invoices raised (step 7). Money customers owe.
- **Collections**: cash that arrived (step 9). What pays salaries and suppliers.

Here are all three for Riverstone's first quarter of 2026:

| Month | Booked (orders placed) | Billed (invoiced) | Collected (cash in) |
|---|---|---|---|
| January | ₹116,210 | ₹104,210 | ₹0 |
| February | ₹161,700 | ₹161,700 | ₹64,700 |
| March | ₹58,020 | ₹31,800 | ₹132,550 |
| **Quarter** | **₹335,930** | **₹297,710** | **₹197,250** |

![Grouped bars for January, February, and March 2026 showing booked, billed, and collected amounts](figures/fig3-3-booked-billed-collected.svg)

*Figure 3.3 — Same company, same quarter, three honest answers to "what were sales?"*

Every gap traces to specific transactions:

- **January booked ₹116,210 but billed ₹104,210.** The difference, ₹12,000, is order 5004 from Green Leaf Hotels: 100 water bottles, placed on 20 January and cancelled. Figure 3.3 and the table count bookings the way Riverstone's sales team reports them from the CRM, as every order placed, so the cancelled order is in. It was never shipped or invoiced.
- **January collected ₹0.** Every January invoice had 30-day terms, so none was due until February. Sharma Hardware's ₹14,700 arrived on 2 February.
- **February's three numbers.** All five February orders shipped and were invoiced in February, so bookings and billings match at ₹161,700. The ₹64,700 collected was for *January's* invoices: ₹14,700 from Sharma Hardware, ₹40,000 of Coastal Foods' ₹73,260, and ₹10,000 of Patel Kitchenware's ₹16,250.
- **March booked ₹58,020 but billed ₹31,800.** Order 5012 from Metro Mart, worth ₹26,220, is still *Pending* on 31 March: booked, not yet shipped, so not invoiced. ₹58,020 − ₹26,220 = ₹31,800. ✓
- **March collected more than it billed**, mostly February's invoices being paid. Cash lags billings by about the payment terms.

And the quarter reconciles:

- Bookings ₹335,930 − cancelled ₹12,000 − pending ₹26,220 = billings ₹297,710. ✓
- Billings ₹297,710 − collected ₹197,250 = **₹100,460 still owed by customers**, which finance calls **receivables** (or accounts receivable). ✓

> **Watch out: "sales" without a definition.** If you don't know which of the three is meant, ask. If you can't, give the name and rule with the number: *"Billed sales (invoices raised) in January: ₹104,210."* Otherwise two departments argue about who is wrong when both are right.

> **Simplification note.** Accountants recognize **revenue** under formal accounting standards, which decide exactly when a sale counts. This book uses invoices as a stand-in for revenue, as Chapters 12 and 13 do. In a real company, ask finance which rule applies before publishing a revenue number; this is general information, not accounting advice.

### When a report runs matters too

**Timing** also makes reports differ. Run on 31 March, a report shows order 5012 as *Pending*; run on 10 April, after it ships, it shows the order billed in April. Good reports state their run date and **cut-off** ("orders placed up to 31 March 2026"), which is why this book fixes "today" for each dataset.

---

## 3.5 What a KPI is

Managers can't read thousands of transactions or dozens of reports. They need a few numbers that show at a glance whether the business is on track.

A **metric** is any number you measure. A **KPI** (key performance indicator) is a metric chosen as one of the few that matter most, with a target, an owner, and a regular review.

Here are nine KPIs Riverstone's management could track, calculated for the first quarter of 2026 as of 31 March:

| KPI | Definition | Q1 2026 | Owner |
|---|---|---|---|
| **Bookings** | value of orders placed, excluding cancelled orders | ₹323,930 (includes ₹26,220 pending) | Sales Head |
| **Billings** | value of invoices raised | ₹297,710 | Finance Manager |
| **Collections** | cash received from customers | ₹197,250 (66.3% of billings) | Finance Manager |
| **Gross margin** | (billings − cost of the products sold) ÷ billings | 22.6% | Finance Manager |
| **Average order value (AOV)** | billings ÷ number of invoiced orders | ₹29,771 | Sales Head |
| **Cancellation rate** | cancelled orders ÷ all orders placed | 8.3% (1 of 12) | Sales Head |
| **Overdue receivables** | unpaid amounts on invoices past their due date | ₹88,760 of ₹100,460 owed | Finance Manager |
| **Average days to collect** | days from invoice to final payment, for fully paid invoices | 31.6 days | Finance Manager |
| **Active customers** | customers with at least one non-cancelled order in the period | 7 of 8 | Sales Head |

Check two of them by hand. **Gross margin:** the products on invoiced orders cost Riverstone ₹230,450 to make, so the margin is ₹297,710 − ₹230,450 = ₹67,260, and ₹67,260 ÷ ₹297,710 = 22.6%. ✓ **Average days to collect:** five invoices are fully paid, taking 27, 51, 26, 33, and 21 days; they add up to 158, and 158 ÷ 5 = 31.6 days. ✓ (Invoice 9001, the one from Figure 3.2, is the 27.)

### A KPI needs a definition, not just a name

"Average order value" sounds precise. It isn't. Divide bookings by orders and you get ₹323,930 ÷ 11 non-cancelled orders = ₹29,448. Divide billings by invoiced orders and you get ₹29,771. Both are reasonable; they're different KPIs with the same name. You've already met the same problem with bookings: the table in section 3.4 counts the cancelled order (₹335,930 for the quarter), and the KPI table above leaves it out (₹323,930). A usable KPI definition answers six questions:

1. **Formula:** exactly what's divided by what?
2. **Inclusions and exclusions:** are cancelled orders in? Pending? Returns? Tax?
3. **Time:** which date decides the month: order date, invoice date, or payment date?
4. **Source:** which system and table? (The ERP's `invoices` table, not the CRM.)
5. **Owner:** who decides when the definition changes?
6. **Target and review:** what's good, and who looks at it how often?

Together, those answers are a **KPI definition**: Chapter 1's data dictionary one level up, saying what a number on a dashboard means.

> **Watch out: a KPI that can be improved without improving the business.** If reps earn a bonus on bookings, a large order booked at quarter-end and later cancelled raises bookings and gains nothing. Pair KPIs that keep each other honest: bookings *with* cancellation rate, billings *with* collections.

### Leading and lagging

**Lagging indicators**, like collections and gross margin, report what already happened: accurate, but too late to change. **Leading indicators**, like new leads, quotes, and bookings, move first: less certain, but early enough to act on. In Figure 3.2, steps on the left lead and steps on the right lag. A sales head who watches only collections learns about a bad quarter three months late.

---

## 3.6 Dashboards, meetings, and who decides what

Data changes nothing until someone uses it to decide, usually on **dashboards** and in **meetings**.

A **dashboard** is a screen of a few KPIs and charts, usually refreshed automatically from the systems of record, that answers the questions its viewer asks every week (Chapters 15 and 16 build them).

Companies look at their numbers on a rhythm. Riverstone's is typical:

| When | Meeting | Who attends | What they look at | Decisions made |
|---|---|---|---|---|
| **Every morning** | dispatch stand-up at Bhiwandi Main | warehouse supervisor, dispatch team | orders to ship today, stock shortfalls | which orders ship first; what to chase from the plants |
| **Every Monday** | weekly sales review | Anita Rao (Sales Head), Vikram Singh (Sales Manager), sales executives | bookings, quotes sent, top open deals | which deals to push; which customers to visit |
| **First week of each month** | monthly business review | managing director, department heads | booked, billed, and collected; margin; overdue receivables | where to spend; which problems to fix; whether to change prices |
| **Every quarter** | board review | managing director, board of directors | results against the annual plan | strategy, investment, targets for next year |

The closer a meeting is to daily work, the more detailed its data; the more senior, the more summarized and lagging. A common first analyst job is building the monthly business review pack.

### Decision rights: who decides what

Written rules for who owns which decision are called **decision rights**. Riverstone's discount rules are an example: the bigger the discount, the more senior the approver.

| Discount on an order line | Who approves | Data they need to decide |
|---|---|---|
| up to 5% | the sales executive | the customer's order history |
| over 5% and up to 10% | the Sales Manager (Vikram Singh) | order history, the margin on the product at that price |
| over 10% | the Sales Head (Anita Rao), after checking with the Finance Manager (Suresh Menon) | margin at that price, the customer's payment record, overdue amounts |

The data follows the rules: Neha's 5% on order 5001 needed no approval. Rahul's 10% on Coastal Foods' orders 5002 and 5007 went to Vikram. Farah's 12% on Northgate Distributors' 60 industrial crates (order 5009) needed Anita.

Anita needed margin and payment data from finance and order history from the ERP. **The person who decides is rarely the person who holds the data.** Getting the right data to them, in time, in a form they can read in a minute, is the job this book trains you for.

---

## 3.7 Where manual work hides

Go back to Figure 3.2 and ask one question at every step: *did a person copy, re-type, check, or carry data by hand here?* Figure 3.4 marks the answers.

![The same ten steps of order 5001, with six steps highlighted in red where a person copies, re-types, or checks data by hand](figures/fig3-4-where-manual-work-hides.svg)

*Figure 3.4 — Six of the ten steps depend on someone moving data by hand.*

| Step | What a person does by hand | What can go wrong |
|---|---|---|
| **3. Quote** | builds the quote in a spreadsheet, saves a PDF, emails it, and logs it in the CRM | old price list used; quote never logged, so the CRM undercounts |
| **4. Order** | reads the customer's email and re-types the order into the ERP | wrong quantity, wrong product code, discount forgotten |
| **5. Stock check** | phones the warehouse, because the ERP's stock figures are updated once a day from a spreadsheet | promises stock that's already gone |
| **8. Delivery** | scans a signed paper POD, emails it to finance, updates the order status | lost paper; order left as *Shipped* for weeks |
| **9. Payment** | reads the bank statement and matches each payment to an invoice | payment matched to the wrong invoice; customer chased for money they've paid |
| **10. Report** | exports data, pastes it into Excel, fixes formulas, emails the file | the Friday file problems from Chapter 2: wrong version, broken formulas, a report on one laptop |

These steps have names:

- **Re-keying**: typing data that already exists in one place into another (step 4), inviting the typing errors from Chapter 1.
- **Copy-paste integration**: moving data between spreadsheets or systems by copying it (step 10).
- **Emailing files around** (steps 3, 8, and 10): the data stops updating the moment it's attached.
- **Manual matching**, or **reconciliation**: pairing up two sets of records by eye (step 9).
- **Shadow systems**: personal spreadsheets that hold data the official system should hold, like the warehouse's stock sheet (step 5).

### Why it matters

**Time.** Manual work is small per item and large in total. Suppose a sales team re-types 40 emailed orders a week at about 6 minutes each: 240 minutes, or 4 hours a week, which over a 50-week year is 200 hours, about five working weeks of one person's time. (Round numbers for illustration; exercise 9 works a similar estimate.)

**Errors, delay, and people.** Mistyped orders are found when the customer receives the wrong goods. A report built by hand on the third of the month can't be seen on the first. And when only one person knows how the report is put together, like Imran and his Friday file in Chapter 2, it stops when they're on leave.

### How to find manual work in any process

Ask five questions at every step:

1. **Where does this data first enter a system?** Ideally once, at the source (Chapter 1).
2. **Is it typed again anywhere later?** If yes, that's re-keying.
3. **Does it travel by email, chat, phone, or paper?** Each of those is a handover with no record in a system.
4. **Does anyone keep their own spreadsheet of it?** That's a shadow system.
5. **Does someone check or match things by eye?** That's reconciliation, and usually the slowest step.

Then estimate *how many times a week, how many minutes each*. A list of manual steps with hours attached is where every automation project starts.

### Not every manual step should be automated

Anita approving a 12% discount is a judgment, and it should stay with a person; what can be automated is sending her the margin and payment data. And automating a broken process gives you a fast broken process: fix the process first. The book returns to each of Riverstone's manual steps: reports in Chapters 19 and 20, emailed orders in Chapter 58, disconnected systems in Chapters 45 and 51, and the full process map in Chapter 25.

> **Interview extra point.** When an interviewer asks, *"What were sales last month?"*, or gives you a case with a "revenue" figure, say which definition you're using (booked, billed, or collected) before you calculate. It shows in one sentence that you understand the business, not only the tools. Chapters 75 and 76 have practice questions.

---

## Common mistakes and how to spot them

| Mistake | Symptom | Fix |
|---|---|---|
| Quoting "sales" without saying which | two managers argue about a ₹12,000 difference | Name the number: booked, billed, or collected, with its rule |
| Treating a difference between reports as an error | hours spent hunting for a bug that isn't there | Reconcile first: cancellations, pending orders, timing, and payment terms explain most gaps |
| Assuming systems agree | CRM "won deals" total doesn't match ERP orders | Find the system of record for each fact and use it |
| Reporting a KPI without a written definition | the same KPI name gives different values in different files | Write the formula, inclusions, date rule, source, and owner |
| Rewarding a single KPI | bookings rise while cancellations rise too | Pair KPIs that keep each other honest |
| Ignoring the report's run date | the same report shows a different March on 10 April | State the cut-off and the date the report was run |
| Automating before fixing | wrong numbers delivered faster | Fix the process and the data, then automate |
| Automating away a judgment | a discount approved by a rule nobody questions | Keep decisions with people; automate getting them the data |

---

## In the real world: three numbers for January

It's Tuesday, 3 February 2026. The managing director's monthly business review is on Thursday, and two numbers for January have just reached the MD's inbox. Anita's weekly sales summary, pulled from the CRM's pipeline, says **January sales: ₹116,210**. Suresh Menon, the Finance Manager, sent his month-end report from the ERP: **January sales: ₹104,210**, and underneath it, **cash received in January: ₹0**.

The MD replies to both: *"Which one is right? And why did we collect nothing?"*

Anita asks Meera Iyer to find out. Meera doesn't start by deciding who's wrong. She asks: *which step of the order does each report count?*

**1. What does each report count?** Anita's summary adds up deals marked *Won* in the CRM, which happens when an order is placed: that's **bookings**. Suresh's report adds up invoices in the ERP: **billings**. His second line is **collections**.

**2. What's in one and not the other?** Meera lists January's orders from the ERP and January's won deals from the CRM side by side:

| Order | Customer | ERP status | Value | In CRM "won"? | Invoiced? |
|---|---|---|---|---|---|
| 5001 | Sharma Hardware | Delivered | ₹14,700 | yes | yes, 9001 |
| 5002 | Coastal Foods | Delivered | ₹73,260 | yes | yes, 9002 |
| 5003 | Patel Kitchenware | Delivered | ₹16,250 | yes | yes, 9003 |
| 5004 | Green Leaf Hotels | Cancelled | ₹12,000 | yes | no |

The CRM total is ₹116,210. The invoiced total is ₹104,210. The difference is exactly order 5004: Green Leaf Hotels cancelled its 100 water bottles in the ERP, and nobody updated the deal in the CRM, because the systems aren't connected.

**3. Why no cash?** All three invoices had 30-day terms. The earliest, 9001, was due on 5 February. Sharma Hardware paid ₹14,700 yesterday, 2 February, three days early. Coastal Foods' due date is 9 February and Patel Kitchenware's is 14 February. Every invoice raised in January falls due in February, and no older invoices were waiting to be paid, so zero cash in January is exactly what 30-day terms predict.

**4. Does it reconcile?** ₹116,210 − ₹12,000 = ₹104,210. ✓

On Wednesday afternoon, Meera sends Anita and Suresh a half-page note:

> *"Both reports are correct; they count different steps. **Booked** in January (orders placed, per the CRM): ₹116,210. **Billed** (invoices raised, per the ERP): ₹104,210. The ₹12,000 difference is Green Leaf Hotels' order 5004, cancelled in the ERP but still marked Won in the CRM; I've asked Neha's team to update it. **Collected**: ₹0, because January's invoices aren't due until 5–14 February; ₹14,700 has already arrived. Suggestion: the monthly pack shows all three lines with a one-line definition under each, and the ERP is the source for billed and collected."*

On Thursday the pack has three lines instead of one, and the meeting discusses what the numbers mean instead of which is true.

Meera used no tool or formula, only the order's journey, systems of record, three definitions of "sales", and a reconciliation to the rupee. She also found a failed manual handover and fixed it. That's this chapter, applied in an afternoon.

---

## Tools

- **A notebook and pen.** Enough for every exercise, and the best way to draw your first process map.
- **A spreadsheet** (Excel or Google Sheets, optional). Useful for the project's step table and time estimates. Chapter 10 teaches both from the beginning.
- **A diagram tool** (optional). diagrams.net (also called draw.io) is free and runs in a browser; PowerPoint, Google Slides, and Google Drawings work too. Boxes and arrows are all you need.
- **The Riverstone mini database.** Not needed yet; Chapter 6 installs it and Chapter 12 queries the orders, invoices, and payments you followed here.

---

## The project: map the data flow of one process

**Goal:** map one real process the way Figure 3.2 maps order 5001, find its manual work, and propose one improvement.

**Step 1. Choose a process** you can observe or ask about: an expense claim, a customer return, a monthly report, or outside work, how a local shop restocks or a clinic books appointments.

**Step 2. List 6 to 12 steps** in order, recording six things for each:

| Column | What to write |
|---|---|
| `step` | a number and a two-word name |
| `who` | the role (not a person's name) |
| `what_happens` | one sentence |
| `data_created_or_used` | the record: a form, a bill, a row in a system |
| `where_it_lives` | system, spreadsheet, paper, email, someone's memory |
| `how_it_moves_on` | automatic, typed again, emailed, phoned, carried |

**Step 3. Draw it.** Boxes for steps, arrows for handovers, the record written under each box, as in Figure 3.2.

**Step 4. Mark the manual work.** Ask the five questions from section 3.7 at every step. Mark each manual handover in red, as in Figure 3.4.

**Step 5. Put a number on it:** hours per month for each manual step, with your assumptions.

**Step 6. Name one KPI** that shows whether the process works (for example, "days from return request to refund"), defined with section 3.5's six questions.

**Step 7. Propose one improvement** in three sentences: what changes, what it saves, and what could go wrong.

Here is a short worked start, for the restocking process at Sai Krupa General Store from Chapter 1:

| step | who | what_happens | data_created_or_used | where_it_lives | how_it_moves_on |
|---|---|---|---|---|---|
| 1 Spot low stock | shop assistant | notices a shelf is nearly empty | item name | memory | told to the owner |
| 2 Write list | owner | writes items and quantities to reorder | reorder list | paper notebook | photographed and sent by chat |
| 3 Place order | distributor's salesperson | types the list into the distributor's app | purchase order | distributor's system | automatic |
| 4 Receive goods | shop assistant | checks delivered items against the paper bill | delivery bill | paper | carried to the owner |
| 5 Update stock | owner | adds received quantities in the billing app | stock levels | billing app (POS) | typed again |

Steps 1, 2, and 5 are manual, and step 5 re-keys what the bill already says. If the billing app flagged low stock, step 1 wouldn't depend on someone noticing.

**Deliverable:** the table, drawing, hours estimate, KPI definition, and proposal. Keep it for Chapter 25.

---

## You've got it when…

- [ ] I can name the main departments of a company and one kind of data each creates.
- [ ] I can walk through lead to cash for one order and say what record each step leaves, and in which system.
- [ ] I can explain what an ERP, CRM, HRMS, POS, e-commerce platform, and support desk are for.
- [ ] I can tell a transaction from a report, and I know what a system of record is.
- [ ] I never say "sales" without saying booked, billed, or collected, and I can reconcile the three.
- [ ] I can write a KPI definition that two people would calculate the same way.
- [ ] I can find re-keying, copy-paste, emailed files, manual matching, and shadow systems in a process, and estimate their cost in hours.
- [ ] I've mapped the data flow of one real process and proposed one improvement.

---

## Recap

- A company is a chain of departments handing work to each other. **Every handover leaves data**, and data created in one department is almost always used in another.
- **Lead to cash** follows one piece of business from enquiry to payment. Riverstone's order 5001 took ten steps: 103 days from enquiry to cash, 28 from order to cash.
- **Business systems** record daily work: **ERP** (orders, stock, invoices, accounts), **CRM** (leads, quotes, deals), **HRMS** (employees, payroll), **POS** (shop sales), **e-commerce** (online orders), and **support desks** (tickets). Spreadsheets and email fill the gaps between them.
- Each fact should have one **system of record**. Systems that aren't **integrated** drift apart.
- A **transaction** records one event; a **report** summarizes many, using rules, at a point in time.
- "Sales" can mean **bookings** (orders placed), **billings** (invoices raised), or **collections** (cash received). For Riverstone's January: ₹116,210, ₹104,210, and ₹0, all correct. Reconcile them with cancellations, pending orders, and payment terms.
- A **KPI** is a chosen metric with a **definition**, an owner, a target, and a review. Pair KPIs so none can be gamed alone; watch **leading** as well as **lagging** indicators.
- **Dashboards and meetings** turn data into decisions on a rhythm. **Decision rights** say who decides; the decider rarely holds the data.
- **Manual work hides** in re-keying, copy-paste, emailed files, manual matching, and shadow systems. Find it with five questions, count it in hours, fix the process first, and keep judgment with people.

---

## Practice exercises

### Warm-up

1. Match each record to the department that creates it: (a) a delivery challan, (b) a purchase order to Western Polymers for plastic granules, (c) a payslip, (d) a complaint about a cracked crate, (e) a quote, (f) a record of how much plastic was scrapped on a machine, (g) a list of people who visited Riverstone's stall at a trade fair.
2. Transaction or report? (a) Payment 3: ₹33,260 against invoice 9002 on 2026-03-02. (b) "Overdue receivables by customer, as of 31 March 2026." (c) Order 5012, placed 2026-03-15, status Pending. (d) "Average days to collect in Q1: 31.6." (e) Ticket 208: "lid doesn't fit", opened 2026-03-18.
3. Which Riverstone system would you look in first to answer each question? (a) How many enquiries came through the website last week? (b) Has invoice 9007 been paid? (c) How many days of leave does Neha have left? (d) How many storage boxes are in stock at Bhiwandi Main? (e) Which quotes are still waiting for a customer's reply?
4. For each event, say whether it changes bookings, billings, collections, or none of them: (a) Metro Mart places an order. (b) Coastal Foods pays ₹20,000 against invoice 9006. (c) A customer asks for a quote. (d) Order 5011 ships and the ERP raises an invoice. (e) Order 5004 is cancelled before shipping. (f) A lead is marked *Qualified* in the CRM.

### Core

5. February 2026 at Riverstone: orders 5005 to 5009 were placed (₹14,550, ₹14,640, ₹32,625, ₹23,325, ₹76,560), all shipped and invoiced in February, and none was cancelled. Payments received in February: ₹14,700 (invoice 9001), ₹40,000 (invoice 9002), ₹10,000 (invoice 9003). Calculate February's booked, billed, and collected amounts, and explain in two sentences why collections are so much lower than billings.
6. A department head writes this KPI definition: *"Sales growth: sales this month compared with last month."* List at least four things that are missing or ambiguous, then rewrite it as a complete definition using the six questions in section 3.5.
7. In March 2026, three orders were placed: 5010 (₹20,100, Delivered), 5011 (₹11,700, Shipped), and 5012 (₹26,220, Pending). Only 5010 and 5011 were invoiced. Calculate (a) the cancellation rate for March, (b) average order value on billings, and (c) average order value on bookings. Explain why (b) and (c) differ.
8. List every manual handover in this process and name its type (re-keying, copy-paste, emailed file, manual matching, or shadow system): *"An employee fills in a paper expense form with receipts, and their manager signs it. The employee scans and emails it to finance. A finance assistant types each line into the ERP and checks the total against the receipts. Every Friday, the assistant copies the week's claims into the Finance Manager's budget spreadsheet."*
9. Riverstone's finance team types 25 supplier invoices a day into the ERP, taking about 3 minutes each, on 22 working days a month. How many hours a month is that? Show your working, and name two costs of this work that the hours don't capture.

### Stretch

10. It's 31 March 2026. Northgate Distributors placed order 5009 on 25 February: 60 industrial crates at ₹1,450 with a 12% discount. Invoice 9008 was raised on 26 February with 30-day terms, due 28 March. Northgate paid ₹30,000 on 20 March. The order's status is *Shipped*. Answer: (a) Check the order value by hand. (b) How much is booked, billed, and collected for this order? (c) How much does Northgate still owe, and is it overdue? By how many days? (d) What would you check before calling Northgate about the balance?
11. Build a simple **KPI tree** for collections: write "Collections" at the top and break it into the two or three things that drive it, then break each of those down one more level. For each box at the bottom, name the department that can influence it.
12. Farah wants to offer Northgate Distributors 15% off another order of industrial crates, which cost ₹1,100 to make and list at ₹1,450. (a) Who approves it? (b) Calculate the gross margin per crate at list price, 12% off, and 15% off. (c) What other data should the approver look at, and what should they ask before agreeing?

### Think about it (no calculation needed)

13. Riverstone is considering paying sales executives a commission of 1% of the bookings they bring in. Describe two ways this could reward the wrong behavior, and suggest a better basis for the commission, or a second KPI to pair with it.
14. At the monthly business review, the Sales Head wants "sales" to mean bookings and the Finance Manager wants it to mean billings. Who should decide, and how would you present the numbers so that the meeting can move on?
15. The Sales Manager makes ten CRM fields mandatory before a lead can be saved, including the customer's annual turnover. What will happen to the quality of those fields, and what would you suggest instead?

---

## Key terms

department · lead · quote / quotation · order · delivery challan / delivery note · picking list · proof of delivery (POD) · invoice · due date · payment terms · payment · made to stock · lead to cash · order to cash · business system · ERP · CRM · HRMS · POS · e-commerce platform · support desk / ticketing system · ticket · system of record / source of truth · integration · transaction · report · data warehouse · bookings · billings · collections · receivables / accounts receivable · revenue · cut-off · metric · KPI · KPI definition · leading indicator · lagging indicator · gross margin · average order value (AOV) · cancellation rate · overdue · dashboard · decision rights · re-keying · copy-paste integration · reconciliation / manual matching · shadow system · KPI tree

*(All terms are defined in the Glossary, Appendix A.)*

---

## Where this leads

- **Chapter 4, Numbers Without Fear,** teaches the percentages, averages, and growth rates behind every KPI in section 3.5.
- **Chapter 5, Thinking Like an Analyst,** turns vague questions like "why is January low?" into precise ones, the way Meera did.
- **Chapters 10 and 12** put the order-to-cash records into tools: a spreadsheet sales tracker, then the ERP's `orders`, `invoices`, and `payments` tables in SQL, where you'll calculate booked, billed, and collected yourself.
- **Chapters 19 and 20** automate the monthly report: macros and Apps Script first, then scheduled email reports and alerts.
- **Chapter 23, Business Acumen, KPIs & Metrics,** builds a full KPI tree for Riverstone and adds finance and operations metrics such as days sales outstanding.
- **Chapter 25, The Business Analyst Track,** maps Riverstone's order-to-cash process formally and writes requirements for an improvement.
- **Chapters 45 and 51** connect the systems: moving data from the ERP and CRM into a warehouse, and sending results back into them.
- **Chapter 58** automates the re-typing of emailed purchase orders with AI, with a person checking uncertain cases.
- **Interview preparation:** metric definitions, KPI trees, and business-process questions appear in Chapter 75 (product sense, metrics, and case studies) and Chapter 76 (the Business Analyst question bank), with model answers.

---

## Answers to practice exercises

*(In the finished book these move to Appendix G.)*

**1.** (a) Warehouse and dispatch. (b) Purchasing. (c) HR (payroll). (d) Customer support. (e) Sales. (f) Production. (g) Marketing.

**2.** (a) Transaction: one payment event. (b) Report: a summary of many invoices and payments at a cut-off date. (c) Transaction: one order. (d) Report: an average over several invoices. (e) Transaction: one support ticket.

**3.** (a) The CRM, where the website form creates leads. (b) The ERP, where payments are recorded against invoices. (c) The HRMS. (d) The ERP, but its stock is updated once a day (section 3.2), so for an urgent answer also check with Bhiwandi Main. (e) The CRM.

**4.** (a) Bookings. (b) Collections. (c) None: a quote isn't a sale. (d) Billings. (e) Bookings go down if you count bookings net of cancellations (the KPI definition in section 3.5); nothing is billed or collected. (f) None: it's a leading indicator, not a sale.

**5.** Booked: ₹14,550 + ₹14,640 + ₹32,625 + ₹23,325 + ₹76,560 = **₹161,700**. Billed: all five were invoiced in February, so also **₹161,700**. Collected: ₹14,700 + ₹40,000 + ₹10,000 = **₹64,700**. Collections are lower because all three payments were for January's invoices; February's invoices have 30-day terms and weren't due until March.

**6.** Missing: which "sales" (booked, billed, or collected); whether cancellations, returns, and tax count; whether "compared" means rupees or percent; which date decides the month; the source system; the owner and target. One good rewrite:

| Question | Answer |
|---|---|
| Name | Monthly billings growth |
| Formula | (billings this month − billings last month) ÷ billings last month, as a percentage to one decimal |
| Inclusions and exclusions | invoices raised; net of discount; tax excluded; credit notes subtracted in the month they're raised |
| Time | invoice date decides the month; calendar months |
| Source | ERP, `invoices` table |
| Owner, target, review | Finance Manager; target set in the annual plan; reviewed at the monthly business review |

**7.** (a) 0 cancelled out of 3 placed: **0%**. (b) ₹20,100 + ₹11,700 = ₹31,800, divided by 2 invoiced orders = **₹15,900**. (c) ₹58,020 ÷ 3 orders placed = **₹19,340**. They differ because order 5012 (₹26,220), the largest of the three, is booked but not yet invoiced. Neither is wrong; a report must say which it uses.

**8.** (1) Paper form and receipts: data created on paper instead of in a system. (2) Scanning and emailing the form to finance: **emailed file**. (3) Typing each line into the ERP: **re-keying**. (4) Checking totals against receipts: **manual matching**. (5) Copying the week's claims into the Finance Manager's spreadsheet: **copy-paste** into a **shadow system** (the budget tracker lives outside the ERP).

**9.** 25 × 3 = 75 minutes a day. 75 × 22 = 1,650 minutes a month. 1,650 ÷ 60 = **27.5 hours a month**, more than three working days. Costs the hours don't show: typing errors (paying a supplier the wrong amount), delay (untyped invoices make reports of what Riverstone owes out of date), and dependence on the people who do it.

**10.** (a) 60 × ₹1,450 = ₹87,000; 12% off is ₹10,440; ₹87,000 − ₹10,440 = **₹76,560**. ✓ (b) Booked ₹76,560 (in February); billed ₹76,560 (in February); collected ₹30,000 (in March). (c) ₹76,560 − ₹30,000 = **₹46,560** owed. It was due on 28 March, so on 31 March it's **3 days overdue**. (d) Whether the goods were delivered (the status is still *Shipped*, so Northgate may be waiting for them), whether a payment arrived but isn't recorded, and whether there's an open complaint. Three days overdue after a part-payment calls for a polite reminder, not an escalation.

**11.** One good tree (other sensible splits are fine):

- **Collections**
  - **Billings**: orders shipped (sales, warehouse) · average order value (sales) · invoicing accuracy (finance)
  - **Share paid on time**: payment terms and credit checks (sales, finance) · disputes from wrong deliveries or missing proof of delivery (warehouse, support)
  - **Overdue recovered**: reminders and escalation (finance, sales)

When collections drop, you can ask which branch moved, and each branch has an owner.

**12.** (a) Over 10%, so the Sales Head, Anita Rao, after checking with the Finance Manager, Suresh Menon. (b) At list price: (₹1,450 − ₹1,100) ÷ ₹1,450 = **24.1%**. At 12% off: price ₹1,276; (₹1,276 − ₹1,100) ÷ ₹1,276 = **13.8%**. At 15% off: price ₹1,232.50; (₹1,232.50 − ₹1,100) ÷ ₹1,232.50 = **10.8%**. 15% off leaves less than half the list-price margin. (c) Northgate's payment record (₹46,560 overdue, exercise 10), the volume the discount would win, and competitors' prices. A sensible question before agreeing: *"Can we settle the overdue balance first, or tie the discount to paying on time?"*

**13.** (1) Reps can book large orders that are later cancelled: bookings rise, no cash arrives. (2) Reps are pushed toward customers who pay late, or heavy discounts at poor margins. Better: pay on **collections**, or on billings less cancellations and long-unpaid invoices; or pair bookings with **cancellation rate** and **gross margin**.

**14.** The managing director, because the definition affects everyone who reads the pack (often finance proposes and management approves). Meanwhile, don't pick a winner: show **booked, billed, and collected** as labeled lines with definitions and sources, reconciled, as Meera did.

**15.** People fill mandatory fields with anything that gets past the screen: "0", "NA", or a guess at turnover. The fields become full but untrustworthy, which is worse than blank (Chapter 1 lists this problem for data typed by people). Better: require only what's known at that stage (name, contact, interest), collect the rest later, use pick-lists, and offer an "unknown" option.
