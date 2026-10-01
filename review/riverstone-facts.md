# Riverstone Supplies: fact sheet (DRAFT for Abhishek's approval)

**Status:** draft, 28 Sep 2026. Decision D3 in `DECISIONS.md`. Every Part II–Closing fix under theme T10 is checked against this sheet once it is approved.

**How to read it**

- **Fixed** = already decided by Abhishek. Cited to the finding or decision.
- **Canon** = what the chapters, the bible and the data agree on. Cited to chapter and line (`Ch 20 L598` = `manuscript/ch20-….md`, line 598).
- **Proposal** = my suggestion where chapters disagree. It is not canon until you approve it. Section 9 lists all of them.
- Sources: `planning/chapter-writing-instructions.md` §7 (the "bible"), `planning/riverstone-bible-additions.md` ("bible+"), `planning/cross-part-issues.md` (CPI-n), `review/reader-journey/journey-findings.md` (RJ-…), `tracker/register.csv` (finding IDs).
- Line numbers are for today's manuscript. They will move as fixes land.

---

## 0. Decisions already fixed (apply everywhere)

| # | Fact | Value | Source |
|---|---|---|---|
| F1 | Loaded hourly rate (staff time) | **₹300/hour**, book-wide | 66.5. Ch 63's "~₹3.9 lakh" becomes "~₹97,500" |
| F2 | Meera Iyer's start | Ch 1 wins: she "has just joined Riverstone Supplies as a sales coordinator" (Ch 1 L356). Ch 83's "five years" and "administrative role" are adapted to fit | 83.1 |
| F3 | Daily Sales Flash timing | ERP load finishes overnight; the **06:30 Dagster run** (Ch 46) ingests it; the Flash is **sent by 07:30 IST on working days** (Ch 20). Ch 61 "as of 06:14" becomes "as of 06:35" | 60.3 (also 61.22, 63.14, 60.21) |
| F4 | Rupee digit grouping | **Indian lakh grouping** (₹2,03,775), book-wide | 67.9, V67.7, 19.8 |
| F5 | Revenue anchors | One-year database (2025): **₹43,35,471** (was printed ₹4,335,471). December 2025: **₹4,39,823.50** (printed ₹439,823.50 / ₹439,824) | CLAUDE.md §8; verified below |
| F6 | Who raised the Ch 24 ask | **Vikram Singh** (Sales Manager) raises it; memo to Vikram, cc **Anita Rao** (Sales Head), who decides | 24.5 |
| F7 | Invoicing | Ch 3 stands: the ERP raises the invoice **automatically on shipment, the same day** (order 5001: shipped and invoice 9001 on 6 Jan 2026) | 25.1 (option A); 76B.2 follows it |
| F8 | Currency in printed output and figures | **₹**, not "Rs" | V57.9, V58.9 |
| F9 | Deployment target in Ch 52 | **ECS Fargate** throughout (not Kubernetes) | 52.22 |
| F10 | Size bands (order value) | `right=False`: ₹10,000 ≤ medium < ₹25,000 … ≥ ₹50,000 "very large"; Ch 16, 18, 19 agree | 18.23 |
| F11 | Sensor datasets | Keep Ch 48's archive (25 machines, 10-second readings); fix Ch 40's four references to it | 48.5, 40.34 (a) |

> **Scale of F4.** 477 rupee amounts of ₹1 lakh or more in the prose use international grouping today (grep `₹ ?\d{3},\d{3}`). Only 9 already use lakh grouping (Ch 10, 11, 15, 26, 46, 67). Code output also needs a formatter, not hand edits. Anchors in lakh grouping: ₹43,35,471 · ₹4,39,823.50 · ₹3,23,930 · ₹5,02,775 · ₹1,00,460 · ₹2,97,710 · ₹1,14,66,41,651.25.

---

## 1. The company

| Fact | Value | Source |
|---|---|---|
| Name | Riverstone Supplies (fictional; every name and number invented) | bible §7.1; Ch 3 L47 |
| Makes and sells | Plastic storage boxes, kitchenware, industrial crates, a small range of furniture | bible §7.1; Ch 3 L47 |
| Customers | Retailers, hotels and caterers (hospitality), wholesalers, across India. Business customers only; no consumer sales | bible §7.1; Ch 3 L47 |
| Sales channels | Sales team; website (catalogue + enquiry form feeding the CRM; business customers don't order online); a B2B marketplace listing; two trade fairs a year (Feb, Sep) | bible+ (Ch 3, Ch 36) |
| Tax | Left out of examples ("net of discount; tax left out") | bible §7.1 |
| Payment terms | 30 days for credit customers (Sharma Hardware) | Ch 3 L101, L201 |
| Discount approval | ≤5% sales executive; >5–10% Sales Manager (Vikram); >10% Sales Head (Anita) after checking with the Finance Manager | bible+ (Ch 3 §3.6) |
| Departments | Sales, Marketing, Purchasing, Production, Warehouse and dispatch, Finance, HR, Customer support | bible+ (Ch 3 §3.1) |
| Financial year | **Open (C32):** Ch 16 uses the Indian FY (Apr–Mar); Ch 23 labels calendar 2025 "FY2025" | RJ-S3-17 |

### Sites

| Site | What it is | Source |
|---|---|---|
| **Plant 1, Taloja** (Navi Mumbai) | Makes storage boxes and kitchenware. Plant Manager Ramesh Patil. Defect camera trial (Ch 53) | Ch 3 L49; Ch 28 staff table; Ch 53 L803 |
| **Plant 2, Chakan** (Pune) | Makes industrial crates and furniture. Plant Manager Kiran Bhosale. Called "Chakan Plant 2" in Ch 12's lab | Ch 3 L50; bible+ |
| **Bhiwandi Main** (near Mumbai) | Central **warehouse**; all finished goods ship from here. Daily dispatch stand-up; keeps a stock spreadsheet that updates the ERP once a day; writes the daily dispatch file (Ch 45–47) | Ch 3 L52, L107, L274; Ch 45 L357 |
| Head office | Where sales, finance, HR, marketing, purchasing sit ("Head office" in the HRMS view); hybrid posting in Ch 8 | Ch 28 staff table; bible+ (Ch 8 §8.5) |
| Four branch **sales offices** | Mumbai HO, Bengaluru, Delhi, Kolkata. Not plants or warehouses. Kolkata was migrated from an older billing system and loads orders by spreadsheet upload | CPI-4 (resolved); Ch 14 §14.2; `companion/ch21/delivery_times_2025.csv` |
| Regions | West (Mumbai HO), South (Bengaluru), North (Delhi), East (Kolkata; covered by the West RSM) | Ch 16 L965; `companion/ch16/user_region.csv` |
| Lab-only sites | Sriperumbudur warehouse (Chennai, closed in the exercise); suppliers' towns | bible §7.2 (Ch 12 §12.13) |

> **Conflict C11:** Ch 48's sensor data puts machines at "Bhiwandi Main" (a warehouse) and "Chakan Pune" (`companion/ch48/make_sensor_data.py` L10; Ch 48 L177–186, L252). Ch 3 says the plants are Taloja and Chakan. See section 9.

### Size

| Measure | Value | Source |
|---|---|---|
| Company revenue, calendar 2025 | ₹1,14,66,41,651 (₹114.66 crore), non-cancelled, `riverstone_full` | Ch 23 L101; **verified** |
| Key accounts' revenue, 2025 | ₹43,35,471 (24 key accounts, `riverstone_2025`) | F5; **verified** |
| Customers (whole company) | 5,027 records = 4,979 businesses + 48 planted duplicates; 4,599 active in 2025 | `full/DATA_SPEC.md`; **verified** |
| Key accounts | 24 (one-year database) | Ch 13 L51; Ch 28 L55. **Conflict C23:** Ch 31 says "240 key accounts" |
| Cities | 39 | `full/DATA_SPEC.md`; **verified** |
| Staff in the HRMS `staff` view | 35 people (a teaching view, not the full headcount; the plants show only 3 operators) | Ch 28 L187; `companion/ch28/ch28_2025_addons.sql` |
| Sales organisation | 16 in the ERP: Sales Head, Sales Manager (Key Accounts), 3 key-account executives, 3 Regional Sales Managers, 8 regional executives | `full/employees.csv`; **verified** |
| Scale label | "a mid-sized manufacturer" | Ch 3 L47; 23.16 |

---

## 2. People and roles

### 2a. Riverstone staff (canon)

| Name | Role | ERP / HRMS id | First chapter | Notes and conflicts |
|---|---|---|---|---|
| **Meera Iyer** | Sales coordinator (Ch 1); later analyst; later "Head of Data Platform" (Ch 60) | HRMS 113, reports to Anita | Ch 1 L356 | Title and tenure conflicts: see section 3 (C2–C4). Ch 24 memo signs "Meera Iyer, Analytics" (Ch 24 L164). Ch 83 L302 "administrative role" (fixed by F2). Ch 78 L279 uses "Meera" in a generic interview story (C19) |
| **Anita Rao** | Sales Head; top of the ERP sales team (no manager); reports to the MD in the HRMS | ERP 1 / HRMS 110 | Ch 1 L356 | Ch 58 story calls the sales head "His" (RJ-S2-23). Ch 66 §66.6 "from the top" overstates her level (66.21) |
| **Vikram Singh** | Sales Manager, Key Accounts; reports to Anita | ERP 2 / HRMS 111 | Ch 3 | Title varies: "Sales Manager" (Ch 3, 5, 10, 24, 36), "key accounts sales manager" (Ch 25 L518), "Sales Manager, Key Accounts" (Ch 28 staff; Ch 27). Proposal: "Sales Manager, Key Accounts" at first mention, "Sales Manager" after (25.18) |
| **Neha Kulkarni** | Sales Executive; reports to Vikram | ERP 3 | Ch 3 | 46 orders in 2025 (**verified**) |
| **Rahul Mehta** | Sales Executive; reports to Vikram | ERP 4 | Ch 2 | 54 orders in 2025 (**verified**) |
| **Farah Khan** | Sales Executive, reports to Anita; four years in the job; hospitality expert; working toward the analyst role | ERP 5 | Ch 2 | 64 orders in 2025, the most (**verified**). Ch 68 story contradicts Ch 8–9 (68.1, 68.2). Ch 73 and Ch 76B reuse "Farah" generically (CPI-22, CPI-25, 76B.20) |
| **Imran** | Ran sales operations before Meera; the "Friday file" | — | Ch 2 L583 | Collides with **Imran Shaikh**, a machine owner in Ch 48 L283 (C19) |
| **Suresh Menon** | Finance Manager | HRMS 120 | Ch 3 | Ch 23 L630 "finance controller" and Ch 24 L222 "Finance Controller" (C14) |
| **Arvind Kapoor** | Managing Director | HRMS 100 | Ch 28 L63 (Ch 3–5, 13, 29 say "the managing director" unnamed) | Ch 54 L752 "the CEO"; Ch 67 L177 "owning family … two senior partners"; Ch 24 fig "Board / owning family" (C13) |
| Harpreet Sethi | Head of Production (Taloja) | HRMS 130 | Ch 28 | — |
| Joseph D'Souza | Purchasing Manager | HRMS 140 | Ch 28 | — |
| Mahesh Yadav | Warehouse & Dispatch Manager, Bhiwandi Main | HRMS 150 | Ch 28 | Ch 47 L568 data-contract owner is "Bhiwandi Main warehouse supervisor" (compatible: Mohan Das) |
| Lakshmi Reddy | HR Manager | HRMS 160 | Ch 28 | — |
| Zoya Mirza | Marketing Manager | HRMS 170 | Ch 28 | — |
| **Tenzin Dorji** | Customer Support Lead | HRMS 180 | Ch 28 | Ch 41 L802 names the support lead **Priya Menon** (C15) |
| Ramesh Patil | Plant Manager, Taloja | HRMS 131 | Ch 28 | Ch 53, 56 "the plant manager" unnamed (compatible) |
| Kiran Bhosale | Plant Manager, Chakan | HRMS 132 | Ch 28 | — |
| Ajay Kumar, Swati Joshi | Shift Supervisors (Taloja, Chakan) | HRMS 133, 135 | Ch 28 | — |
| Farhan Ali | Quality Inspector, Taloja | HRMS 134 | Ch 28 | Ch 8 also has a "Farhan" ML engineer (68.27) |
| Gopal Sahu, Sunita Pawar, Farid Shaikh | Machine Operators | HRMS 136–138 | Ch 28 | — |
| Mohan Das | Dispatch Supervisor, Bhiwandi Main | HRMS 151 | Ch 28 | — |
| **Priya Nambiar** | Accounts Executive (Finance) | HRMS 121 | Ch 28 | Ch 33 L727 "Priya wrote the script two years ago" (accounts team: compatible). Collides with Ch 41's Priya Menon (C15) |
| Arjun Nair | Regional Sales Manager, South | ERP 6 / HRMS 116 | Ch 14 | Part VIII reuses "Arjun" (C19) |
| Pooja Desai | RSM West; covers East until a fourth RSM is hired | ERP 7 / HRMS 117 | Ch 16 | Ch 8 L158 has an unrelated "Pooja" (day-in-the-life, not canon) |
| Sandeep Gill | RSM North | ERP 8 / HRMS 118 | Ch 14 | — |
| Kavitha Reddy, Irfan Sheikh, Meenal Joshi, Rohit Verma, Divya Menon, Aakash Jain, Simran Kaur, Tarun Bose | Regional Sales Executives | ERP 9–16 | Ch 14–16 (full dataset) | Ch 28's staff table uses eight **different** names (Divya Krishnan, Vivek Chandran, Sneha Pillai, Nisha Bhatt, Aditya Verma, Rohit Kamat, Karan Ahuja, Ritu Bansal) with null ERP ids (CPI-10, C18). ERP id 9 also means "Inside Sales Desk" in the CRM (C20) |
| Inside Sales Desk | Handles marketplace and web-form leads | CRM owner 9 | Ch 36 | C20 |
| Ayesha Qureshi | Business analyst (moved from the support desk 18 months earlier) | — | Ch 25 L520 | Not in the bible (RJ-S3-24) |
| Deepak Nair | Production planner; his demand sheet is 4 years old | — | Ch 40 L907 | Name reused in Ch 71 (C19) |
| Unnamed roles | "operations head" (Ch 21 L596), "logistics head" (Ch 22 L621), "IT manager" (Ch 54 L752), contract data engineer (Ch 45 L857, Ch 52 L667), "e-commerce contractor" (Ch 42 L614), "a newly hired VP" (Ch 67 L107), the Taloja plant analyst (Ch 62, 66), a four-person data platform team (Ch 60–66) | — | — | Proposal: keep unnamed; add to the bible as roles so later chapters reuse them |

### 2b. People outside Riverstone

| Name | Who | Source |
|---|---|---|
| Rakesh | Buyer at Sharma Hardware | Ch 1; bible |
| Kavya | College student in Mumbai (spending log) | Ch 1, 2 |
| Sai Krupa General Store (Kothrud, Pune) | Receipt example | Ch 1 |
| Swift Movers, Rapid Wheels | Delivery partners | Ch 1 L205–206. **Conflict C29:** Ch 22 L621 uses transporters SwiftLine and BlueCart |
| Suppliers | Western Polymers (Vapi), Deccan Cartons (Pune), Kaveri Steel Works (Coimbatore), Sagar Labels (Mumbai), Gujarat Pigments (Ahmedabad), Nilgiri Packaging (Ooty) | bible §7.2; Ch 28 BOM |
| Not canon | The larger hypothetical Riverstone in Ch 7 §7.6; the ten day-in-the-life people in Ch 8 §8.4 (Pooja, Sneha, Farhan…); Part VIII interview candidates | bible+ |

---

## 3. Timeline

### 3a. Data years (canon, verified)

| Period | What | Source |
|---|---|---|
| 2019–2025 | Weekly demand series, 4 categories | `generate_riverstone_demand.py` (run) |
| 2023–2025 | Full sales dataset `riverstone_full`; CRM (12,294 leads) | DATA_SPEC; generator (run) |
| 2024–2025 | Support tickets (3,000) | generator (run) |
| 1 Jan–31 Dec 2025 | One-year database `riverstone_2025`; "today" = 31 Dec 2025 | bible §7.3 |
| 1 Oct–31 Dec 2025 | Q4 export (Ch 14); sensor archive (Ch 48) | companion files |
| 1 Oct 2025 | North region raises list prices 6% | Ch 31 L694 |
| 1 Jan–31 Mar 2026 | Mini database `riverstone`; "today" = 31 Mar 2026 | bible §7.3 |
| 2–7 Jan 2026 | Part V's simulated pipeline calendar ("today" = 6 Jan 2026 in Ch 51) | Ch 45 L499; Ch 46 L603; 51.15 |

### 3b. Story events in order (as written today)

| When | Event | Chapter |
|---|---|---|
| 2017; 2020 | `MASTER_FINAL_v7_USE_THIS.xlsm` written; its author leaves | Ch 19 L1117 |
| Before Meera | Imran runs sales ops and the Friday file | Ch 2 L583 |
| 22 Oct 2025 → 3 Feb 2026 | Order 5001: enquiry 22 Oct; customer created 4 Nov (30-day terms); quote Q-2025-118 on 22 Dec; order 5 Jan; shipped and invoice 9001 on 6 Jan; delivered 8 Jan; paid 2 Feb; January report 3 Feb | Ch 3 §3.2; bible+ |
| Q4 2025 ("the quarter Meera arrived") | Meera joins; the branch macro double-counts a Kolkata file | Ch 19 L1117–1121 |
| Undated | Meera's first week (customer count) | Ch 1 L354 |
| First week Jan 2026 | Board slide check; fourth sales executive question; month-end pack rebuilt; festive stock plan kept (Suresh proposed −15%) | Ch 4 L453; Ch 5 L325; Ch 11 L1712; Ch 15 L789 |
| 6 Jan 2026 | Branch league table | Ch 14 L1322 |
| Second week Jan 2026 | "Two Januaries" tracker | Ch 10 L1100 |
| Jan 2026 | Year-end review; transporter decision; December decline meeting | Ch 13 L1524; Ch 22 L621; Ch 24 L253 |
| 3 Feb 2026 | Three numbers for January (Ch 3); "revenue zero in January" (Ch 29) | Ch 3 L365; Ch 29 L1224 |
| Feb 2026 | First Power BI report; **Daily Sales Flash goes live (07:30 IST)**; payroll-cash story; Git story; vendor lead score | Ch 16 L742; Ch 20 L598; Ch 23 L630; Ch 26 L737; Ch 35 L1060 |
| 4 Mar 2026 | Flash shows ₹0 (ERP load failed 02:10) | Ch 20 L600–602 |
| Mar 2026 | At-risk dashboard project; slow dashboard; Vikram's 98% model | Ch 25 L518; Ch 28 L2646; Ch 36 L998 |
| Mar 2026 → Aug 2026 | Defect camera runs from March; customer return in August | Ch 56 L589 |
| Apr–Oct 2026 | AutoML (Apr), segments (May), lead model live ~Apr and the rep-fairness meeting (Jun), demand planner (Jul), ticket topics (Aug), recommender (Sep), deep-learning pitch (Oct) | Ch 37–43 |
| Oct 2026; Nov 2026 | Extraction pipeline incident; PO intake live in assisted mode | Ch 57 L502; Ch 58 L513 |
| "February" (no year) | First data pipeline goes live (contract engineer; Meera business owner) | Ch 45 L857 |
| **Jan 2026** | Meera becomes **Head of Data Platform** after "four years" building the platform | **Ch 60 L267** (conflicts, C2) |
| Feb, Mar, Apr, Jun 2026 | CRM outage; mesh pitch; first automation audit ("two months into her role"); fairness audit | Ch 61 L265; Ch 62 L205; Ch 63 L268; Ch 64 L284 |
| "Late 2026" | Board review ("eighteen months" of work) | Ch 67 L177 |

### 3c. Meera's timeline

| Source | Says | Status |
|---|---|---|
| Ch 1 L356 | "has just joined … as a sales coordinator" | **Fixed (F2)** |
| Ch 2 L583, Ch 7 L382, bible+ | Inherited Imran's Friday file; Flash by hand ~40 min each morning | Canon |
| Ch 19 L1121 | Arrived in the quarter of the Nov 2025 Kolkata file (Q4 2025) | Canon (only dated anchor) |
| Ch 6 L450 | "done analyst work for months without the title" | Compatible |
| Ch 8 L415 | Still a sales coordinator at Ch 7; the work has changed, not the title | Canon |
| Ch 28 staff (2025 data) | "Sales Coordinator", reports to Anita | Canon |
| Ch 60 L267 | By Jan 2026, **four years** building the platform; becomes Head of Data Platform | **Conflict (C2, C3)** |
| Ch 63 L268 | April 2026 is "two months into her role" | Conflict (63.20: Jan → Apr is three months) |
| Ch 67 L177 | Late 2026, "eighteen months" of work | Conflict (67.10) |
| Ch 59 Case 9 | "six years of small pieces" | Conflict (59.11, RJ-S3-60) |
| Ch 83 L302–316 | "administrative role"; routine "by 2025"; rise over "five years" | **Fixed (F2):** adapt |

**Proposal P-T1 (Meera):** Meera joins as sales coordinator in **October 2025** (fits Ch 19's "quarter Meera arrived", Ch 4's January board slide, Ch 6's "for months"). She keeps the coordinator title through 2026 while doing analyst work (Ch 8). She becomes Head of Data Platform in **January 2027** (see P-T2). Ch 60's "four years" becomes "fifteen months"; Ch 83's "five years" becomes the span from October 2025 to the Ch 8 posting and Part VII (about a year to the posting, about two to the board review).

**Proposal P-T2 (book calendar):** keep Parts 0–IV and VI as dated (Oct 2025 → Nov 2026). Move Part VII forward one year: Ch 60 Jan 2027, Ch 61 Feb 2027, Ch 62 Mar 2027, Ch 63 Apr 2027 ("three months into her role"), Ch 64 Jun 2027, Ch 65 ~Jul 2027, Ch 67 late 2027 ("a year", not "eighteen months"). This is RJ-S2-26's "smallest fix". Date Part V inside 2026 (see C5).

---

## 4. Systems

### 4a. Business systems (canon)

| System | Holds | First | Notes |
|---|---|---|---|
| **ERP** (named by type, never brand) | Customers, products, employees as reps, orders, lines, invoices, payments, stock, production, purchasing. Its invoicing module is "the billing system" | Ch 3 §3.3 (Ch 2 as "billing system") | System of record. PostgreSQL in Part V (`riverstone_source`, Ch 45 L15; Ch 49 L57) |
| **CRM** | Leads, contacts, quotes, pipeline | Ch 3 §3.3 | **Not integrated** with the ERP (bible+). Ch 60 L82 and Ch 61 L265 name it **Zoho** (C27) |
| Website | Catalogue + enquiry form into the CRM | Ch 3 | Ch 30 A/B test on the form. Ch 42 L614 "customer web portal" and "e-commerce contractor" (C28) |
| Support desk | Complaints, returns; ticketing system with five fixed categories | Ch 3; Ch 41 L802 | — |
| HRMS | Employees, attendance, payroll; the 35-person `staff` view | Ch 3; Ch 28 | — |
| Spreadsheets and email | Fill the gaps; Bhiwandi stock sheet updates the ERP once a day | Ch 3 L107 | — |
| Kolkata's older billing system | Kolkata loads orders by spreadsheet upload from it | Ch 14 §14.2 (CPI-4) | Ch 17 L1118 says it was "switched off"; Ch 63 §63.3 treats it as live and screen-only (C44, 63.11) |
| Not at Riverstone | POS, e-commerce store | bible+ | C28 |

### 4b. Data and automation stack, in the order the reader meets it

| Tool / component | What Riverstone uses it for | First | Later |
|---|---|---|---|
| Excel / Google Sheets | Trackers, month-end pack (Power Query, Ch 11) | Ch 10–11 | Ch 19 macros |
| Apps Script | Farah's Monday at-risk email (09:00, time-driven trigger) | Ch 8 story; Ch 19–20 | Ch 63 inventory |
| VBA macro | Q4 branch consolidation (`MASTER_FINAL_v7_USE_THIS.xlsm`) | Ch 19 | Ch 63 audit, Ch 66 (₹5,775) |
| PostgreSQL / MySQL teaching databases | `riverstone`, `riverstone_2025`, `riverstone_full` | Ch 12–14 | Ch 28 `riverstone_perf`; Ch 32 dbt dev target is `riverstone_2025` |
| Power BI | First report Feb 2026; row-level security by region | Ch 16 L742 | Ch 28 slow dashboard |
| Python scripts | `monthly_report.py` (Ch 18); `daily_flash.py` on a "reporting VM" under `svc-analytics` (Ch 20 L821) | Ch 17–20 | Ch 29 `riverstone-report` package |
| Git | Repository for queries and scripts | Ch 26 | — |
| dbt | Models, tests; semantic layer | Ch 32 | Ch 60 "semantic layer" container |
| **Warehouse** | Raw / staging / mart layers | Ch 45 | **Disputed (4c)** |
| **Dagster** | Orchestrator; 06:30 IST daily schedule | Ch 46 | Ch 52, 56, 60 |
| Data quality checks, contracts | Freshness, reconciliation; dispatch-file contract | Ch 47 | — |
| Spark, DuckDB, Polars | Sensor archive processing | Ch 48 | — |
| **Delta Lake** on object storage | Sensor archive, partitioned by date | Ch 49 L446 | Ch 60–65 |
| Kafka-style event log (taught; local stand-in) | Sensor alerts, streaming windows | Ch 50 | Ch 62 |
| Reverse ETL | Lead scores and segments to the CRM (PATCH only after the incident) | Ch 51 | Ch 60, 61 |
| Cloud | **AWS ap-south-1 (Mumbai)**; ECS Fargate (F9); Terraform | Ch 52 L384 | Ch 65 (AWS prices) |
| Defect model | Camera on the Taloja line; FastAPI; MLflow | Ch 53, 56 | Ch 60 |
| Support assistant (RAG) | Pilot with five largest customers | Ch 55 | Ch 60 |
| PO-intake pipeline | Email orders drafted for the ERP; assisted mode; runs 06:00 weekdays | Ch 54, 57, 58 | Ch 60 |

### 4c. The warehouse story (disputed)

What each chapter says:

| Chapter | Says | Evidence |
|---|---|---|
| Ch 45 | The warehouse is a local **DuckDB file**. Framed as a simplification: "the patterns are the same on Snowflake, BigQuery, Redshift…" | L76 (simplification note), L105 `duckdb.connect("warehouse/riverstone_wh.duckdb")`, L116 |
| Ch 46, 47 | Same DuckDB file | Ch 46 L149; Ch 47 L107 |
| Ch 49 | "Orders and customers in the ERP's PostgreSQL (the system of record), **a warehouse for analytics** (raw, staging, mart), and the sensor archive as Parquet in object storage, exposed as a lakehouse table." Keep orders in the warehouse; sensors as **Delta** in object storage | L57, L446 |
| Ch 52 | AWS, ap-south-1; deploys the pipeline container; the story "the afternoon the warehouse went dark" | L384, L665 |
| Ch 60 | "Once the warehouse is **Postgres**…"; Figure 60.3 container "Warehouse (**Postgres + Delta**)" | L52, L86 |
| Ch 61 | "a single **Postgres** transaction"; Fig 61.3 "**Postgres read replicas** for BI"; Fig 61.4 "Warehouse (Postgres+…)" | L98; 61.3 |
| Ch 63 | "Chapters 45 and 49's **Postgres and Delta Lake** tables"; Fig 63.2 "WAREHOUSE Postgres + Delta" | L135; 63.3 |
| Ch 65 | Cost model: "**RDS PostgreSQL** (db.m5.large, Single-AZ) — warehouse primary"; warehouse = 66% of the bill | L77, L100, L292; `companion/ch65/monthly_cost_model.csv` |
| Ch 80 | Q80-022 starts from "today's single-database setup" | 80.2 |

Findings: 60.1 (High), 61.3 (High), 63.3 (High), 65.8, 80.2 (option a: reframe as history).

The two readings: Part V (Ch 45–47) *builds* DuckDB but calls it a stand-in. Part VII and Ch 65 *describe production* as Postgres (on RDS) + Delta. Ch 49 is neutral ("a warehouse").

**Options for Abhishek:**

| Option | Production story | Edits | Cost |
|---|---|---|---|
| **A. "Practice DuckDB, production Postgres" (proposed)** | Riverstone's production warehouse is a **PostgreSQL database on AWS RDS** (schemas raw / staging / mart), separate from the ERP's PostgreSQL. The sensor archive is a **Delta table in S3**. Part V builds the same layers in a local DuckDB file so readers can run it free. | Ch 45 simplification note names the production target once ("Riverstone runs the same layers on a PostgreSQL warehouse in the cloud; Chapter 52 deploys it"); Ch 49 L57 says which warehouse; Ch 60/61/63 keep "Postgres + Delta" but label the ERP and the warehouse as two databases; Ch 61 drops "read replicas" (none built) or labels them a proposal; Ch 65 unchanged | Smallest. Keeps Ch 65's cost model and Ch 66–67's numbers (₹4,56,168) intact |
| B. DuckDB everywhere (finding 60.1's suggestion) | Production warehouse is the DuckDB file plus the Delta archive | Ch 60 (fig, §60.1), Ch 61 (figs), Ch 63 (fig, §63.4), Ch 65 (replace RDS line, rebuild cost model) → Ch 66/67 figures change | Large ripple through the ROI chain |
| C. Managed cloud warehouse | Snowflake/BigQuery etc. | Rewrites Part V framing and Part VII | Largest; not recommended |

Also fix in any option: Ch 60 §60.1 "every later choice has to work with Postgres" must match the option; the semantic layer is Ch 32 (not Ch 23, 63.3).

---

## 5. Rates and money

### 5a. Loaded hourly rate: ₹300/hour (fixed, F1)

| Chapter | Today | After F1 |
|---|---|---|
| Ch 20 L557–562 | "fully-loaded ₹1,200 an hour … ₹390,000 a year" | ₹300 → **₹97,500 a year** (325 h × ₹300) |
| Ch 63 L74–75 | "~₹3.9 lakh at loaded cost" | **~₹97,500** |
| Ch 58 L346 | `COST_PER_HOUR = 300` | Already correct |
| Ch 66 L110, L361 | Flash ₹97,500 (implied ₹300) | Already correct; show derivation (66.5) |
| Ch 65 §65.3 | ₹198/day review cost implies ~₹396/hour (65.26) | Recompute at ₹300 or explain |
| Ch 80 L110 | `hourly_cost = 800` → ₹124,800/yr, payback 5.8 months | At ₹300: **₹46,800/yr, payback 15.4 months** (computed). The answer's "strong, easy case" wording no longer fits (C9) |

### 5b. Exchange rate (₹ per US$)

| Chapter | Rate | Where | Evidence |
|---|---|---|---|
| Ch 49 | **₹83** | Prose: "$6.40 a month, or roughly ₹530 at ₹83 to the dollar" | L427 (also 277 × $0.023 = $6.37, 49.2) |
| Ch 54 | none | Prices only in $ per million tokens ($2 / $10 workhorse) | L688 |
| Ch 55 | none stated | "a fraction of a paisa" (wrong: ≈ ₹0.13–0.14 per question) | 55.25 |
| Ch 57 | **₹88** | `USD_TO_RUPEES = 88.0` in `companion/ch57/provider.py` L33; gives ₹4.74 per 60-email run; never stated in prose | 57.4 |
| Ch 58 | ₹88 (inherited) | Uses Ch 57's `Meter` (`companion/ch58/intake.py` L18, L94) | — |
| Ch 65 | **₹87** | `USD_INR = 87.0` in `companion/ch65/build_ch65_files.py` L22; never stated in prose | 65.9 |

**Proposal P-M1: ₹87 per US$**, stated once where dollars first turn into rupees (Ch 49 §49.8) and repeated in each chapter's Tools box ("₹87 to the dollar, the rate used throughout this book; check today's rate").
- Why 87: it keeps Ch 65's cost model (₹38,014/month × 12 = **₹4,56,168**/yr, verified) and so Ch 66–67's "45%" and board speech unchanged.
- Knock-ons: Ch 49 ₹530 → **₹554** ($6.37 × 87); Ch 57 ₹4.74 → **₹4.69**, and Ch 57/58 meter outputs re-run with 87; Ch 55 "about ₹0.13 a question".
- Option B, ₹88: keeps Ch 57/58 outputs, but Ch 65's total becomes ₹4,61,409/yr and Ch 66–67 must be recomputed.
- I did not look up a current market rate; the sheet should call it "the rate used in this book", not today's rate (T13).

### 5c. Prices and costs used in more than one chapter

| Item | Value | Chapters |
|---|---|---|
| 2026 list prices (mini) | 101 Storage Box 10L ₹450 · 102 Storage Box 25L ₹780 · 103 Water Bottle 1L ₹120 · 104 Food Container Set ₹650 · 105 Industrial Crate ₹1,450 · 106 Garden Chair ₹1,200 | Ch 3, 4, 12 (**verified** in mini SQL) |
| 2025 list prices | ₹430, ₹750, ₹115, ₹620, ₹1,400, ₹1,150; 107 Lunch Box Set ₹380; 108 Stackable Bin ₹290 | Ch 10–13, 55 corpus (**verified**) |
| Older years (full) | 2023 = 92%, 2024 = 96% of current price, rounded to ₹5 | DATA_SPEC |
| Garden Chair material cost | ₹647.80 | Ch 28 |
| Annual target, key accounts 2025 | ₹42,40,000 → 102.3% attained | Ch 10–13 (**verified**) |
| Company target 2025 | ₹1,16,69,50,000 → 98.3% | DATA_SPEC (target sum **verified**) |
| Flash saving | 80 → 2 minutes, 250 runs/yr = **325 h/yr** (verified) → ₹97,500 at F1 | Ch 20, 63, 66, 67 |
| Three quantified automations | Flash ₹97,500 + branch macro ₹5,775 + PO-intake ₹1,00,500 = **₹2,03,775**; platform cost **₹4,56,168**/yr; coverage 44.7% ("about 45%") | Ch 66, 67 (**verified**) |
| PO-intake approval limit | Orders over ₹1,00,000 need a person's sign-off | Ch 58 (`intake.py` L21); Ch 60 NFR |
| Vendor prices in stories | Lead-score add-on ₹40,000/month (Ch 35); AutoML ₹6 lakh/yr (Ch 37) | single-chapter |
| Free-delivery threshold | ₹25,000 (Ch 31, Ch 55: "since January"; old ₹40,000 in the assistant's stale policy) | **Open (C24)**: Ch 31 cites Ch 3, which has no such rule (31.20) |

---

## 6. Datasets

Verified = I loaded or regenerated the data and counted it (method in the box at the end of this section).

| Dataset | Name / files | Period; "today" | Size | Chapters | Verified |
|---|---|---|---|---|---|
| Formats demo | `companion/ch02/orders_feb_2026.{csv,xlsx,json,xml,parquet}`, `api_demo.py` | Feb 2026 | 4 orders | Ch 2 | CSV has 4 data rows (wc) |
| **Mini** | DB `riverstone`; `postgresql/riverstone_setup.sql` (= root `riverstone_setup_mini.sql`, byte-identical); `mysql/riverstone_setup_mysql.sql` | Q1 2026; today 31 Mar 2026 | 8 customers, 6 products, 5 employees, **12 orders, 19 lines**, 10 invoices, 10 payments | Ch 3–5, 12, 13 §13.1–13.5 | ✓ all counts; 11 non-cancelled orders; revenue ₹3,23,930; booked Jan/Feb/Mar ₹1,16,210 / ₹1,61,700 / ₹58,020; billed ₹1,04,210 / ₹1,61,700 / ₹31,800; collected ₹0 / ₹64,700 / ₹1,32,550; invoiced ₹2,97,710, outstanding ₹1,00,460; order 5001 dates |
| **One-year** (key accounts) | DB `riverstone_2025`; `riverstone_2025_setup.sql` (seed 20251) | 2025; today 31 Dec 2025 | 24 customers, 8 products, 5 employees, **175 orders (173 non-cancelled), 330 lines (326 non-cancelled)**, 12 targets, 43 leads (30 unique emails), 89 stage rows | Ch 4–5, 10–13, 17 (330-line exports), 28–35, 45–47, 51, 82 | ✓ all; revenue ₹43,35,471 from 23 customers; Dec ₹4,39,823.50; Jan ₹2,02,640; 102.3% of ₹42,40,000; top customer Sharma Hardware ₹5,02,775; Home Plus never ordered; 11 orders with no rep (10 non-cancelled) |
| Lab | DB `riverstone_lab` (reader-built) | — | suppliers, purchase orders, warehouses | Ch 12 §12.13 | not run |
| **Full** (whole company) | DB `riverstone_full`; `companion/full/*.csv/.parquet` (seed 20230101) | 2023–2025 | 5,027 customers, 8 products, 16 employees, **116,194 orders, 209,006 lines**; 2025: 46,356 orders / 83,444 lines non-cancelled | Ch 14–16, 18, 20–23, 27 | ✓ all; 2025 revenue ₹1,14,66,41,651.25; Oct 2025 ₹18,06,20,103; 4,599 active; 39 cities; 3,414 orders with no rep |
| Q4 raw export | `companion/ch14/orders_q4_2025_export.csv` (+ clean truth) | Q4 2025 | 25,976 lines raw; 25,832 clean; 18 status spellings; branch spellings | Ch 14, 17, 19 | ✓ row counts (pandas) |
| Sales exports | `ch10/riverstone_sales_export_2025.csv`; `ch11/monthly_exports/`, `ch17/sales_exports/` | 2025 | 330 lines (12 monthly files sum to 330) | Ch 10, 11, 17 | ✓ |
| Chart data | `ch15/chart_data/*` | 2023–2025 | e.g. 46,356 order values, 4,599 customers | Ch 15, 18 | ✓ row counts |
| Deliveries (simulated) | `ch21/delivery_times_2025.csv` | 1 Jan–19 Dec 2025 | 45,040 orders; branches Mumbai HO 15,862 · Bengaluru 12,562 · Delhi 10,990 · Kolkata 5,626 | Ch 21–23 | ✓ |
| Email A/B test; transporters (simulated) | `ch22/ab_test_2026.csv`; `ch22/transporters_q4_2025.csv` | Feb 2026; Q4 2025 | 8,400; 11,600 | Ch 22 | ✓ row counts |
| Finance / marketing | `ch23/monthly_revenue_2025.csv`, `marketing_2025.csv` | 2025 | 12 months each | Ch 23 | ✓ |
| HRMS view, BOM, audit log | `ch28/ch28_2025_addons.sql` | 2025 | 35 staff; BOM for 101, 102, 104, 106, 108 | Ch 28, 33 | ✓ staff rows |
| Performance (not canon) | `riverstone_perf` (seed 28) | 2023–2025 | 714,285 orders, 1,926,847 lines | Ch 28 | not run |
| Web A/B (digital) | `ch30/generate_riverstone_web.py` (seed 30) | 2 weeks | 214,528 sessions, 622,090 events, 47,286 visitors | Ch 30 (Ch 42 planned) | not run |
| Causal | `ch31/generate_ch31_data.py` (seed 31) | 24 months | region-month panel; "240 key accounts, 68 in the programme"; ~60,000 orders near ₹25,000 | Ch 31 | not run; conflicts C23, C24 |
| Invoice match | Ch 33 data | 23 months from 2024 | 176,110 order lines; ₹4.42 bn (not canon scale, 33.8) | Ch 33 | not run |
| **CRM** | `generate_riverstone_crm.py` → `crm/` (seed 20236) | 2023–2025 | **12,294 leads** (268 duplicates), 25,682 activities, 39,275 stage rows; owners 3, 4, 5, 9 | Ch 35–39, 51, 64 | ✓ regenerated |
| Accounts (churn) | `generate_riverstone_accounts.py` | 2023–2024 features | **5,000 accounts**, churn 9.7% (484); reps 3, 4, 5, 9 | Ch 37–39, 42–44 | ✓ regenerated |
| Baskets | `generate_riverstone_baskets.py` | 2025 | 34,017 orders, 92,465 lines, 4,516 accounts, **24 products P01–P24** | Ch 38, 42 | ✓ regenerated (RJ-S2-15 quotes 33,931 / 92,359: check which the chapters print) |
| Demand | `generate_riverstone_demand.py` | 2019–2025 weekly | 365 weeks × 4 categories; 84 months | Ch 40 | ✓ regenerated |
| Sensors (small) | `generate_riverstone_sensors.py` (seed 20241) | from 3 Mar 2025 | 10,080 rows (1 machine, 1 week, 1-minute); `--full` = 12 machines × 40 weeks = 4,838,400 | Ch 40 | ✓ small run; full size computed |
| Sensor archive | `ch48/make_sensor_data.py` | 1 Oct–31 Dec 2025 | 25 machines × 92 days × 8,640 = **19,872,000** readings | Ch 48–50, 65 (F11) | ✓ computed from script constants |
| Tickets | `generate_riverstone_tickets.py` | 2024–2025 | **3,000** tickets (blueprint planned ~30k) | Ch 41 | ✓ regenerated |
| Part V source | `riverstone_source` (copy of `riverstone_2025` via `reset_ch45.py`), dispatch files, mock CRM API | simulated 2–7 Jan 2026 | first run loads 177 orders, 333 lines, 43 leads (Ch 46 L335) | Ch 45–47, 51, 52 | not run |
| Defect images | `ch53/generate_defect_images.py` | — | 6,000 simulated images | Ch 53, 56, 59 | not run |
| Support corpus | `ch55/generate_corpus.py` | — | policies, price list (2025 prices), 65 questions | Ch 55, 57 | not run |
| PO emails | Ch 54 golden set | — | 60 labelled emails | Ch 54, 57, 58 | not run |
| Fairness audit | Ch 64 dataset | — | 1,830 leads, four regions | Ch 64 | not run (RJ-S2-29) |
| Cost model | `ch65/monthly_cost_model.csv` | Aug 2026 prices | $436.94 = ₹38,014/month | Ch 65–67 | ✓ summed; implied ₹87.00/$ |

> **What I verified and how.** Started a local PostgreSQL 16 and loaded the mini, one-year and full setup scripts into scratch databases (copies in my scratchpad; nothing in the repo changed), then counted rows, statuses, revenue by month, reps, targets and invoices with SQL. Regenerated the six Part IV datasets by running copies of their generators in the scratchpad with pandas/numpy. Counted companion CSV rows with `wc`/pandas. Recomputed with Python: 325 h × ₹300; $0.053852 × 88 = ₹4.74 and × 87 = ₹4.69; 38,014 × 12 = 4,56,168; 2,03,775 ÷ 4,56,168 = 44.7%; Ch 80 at ₹300; 25 × 92 × 8,640 and 12 × 40 × 10,080; lakh-grouped forms of the anchors. Not run: `riverstone_perf`, web, causal, Ch 33, Part V pipeline, Ch 53–58 companions.

**Scope rule (canon, CPI-5; proposal to state it in Ch 13 L51):** the one-year database is **the 24 key accounts' 2025 data**; `riverstone_full` is the whole company. "Riverstone's 2025 revenue" must say which: ₹43,35,471 (key accounts) or ₹114.66 crore (company). Today Ch 11 L771 says "Riverstone has 24 customers" and Ch 13 L51 "holds all of 2025" (C10).

---

## 7. File names used in the story

| File | What it is | Chapters |
|---|---|---|
| `Weekly Sales FINAL.xlsx`, `Weekly Sales FINAL (2).xlsx` | Imran's Friday file on his laptop, emailed to 11 people | Ch 2 L583 |
| `Sales_Report_FINAL_v3.xlsx`, `…_v4.xlsx`, `report_v7_FINAL.xlsx` | Versioning examples | Ch 2 |
| `Sales_Report_final_v3_REALLY_FINAL.xlsx` | Naming example | Ch 10 |
| `riverstone_sales_tracker_2025.xlsx` | Meera's tracker | Ch 10 |
| `month_end_pack_2025_messy.xlsx` | Vikram's copy-paste pack (₹42,70,875, 100.7%) | Ch 11 L1712 |
| `MASTER_FINAL_v7_USE_THIS.xlsm`; `Riverstone_Kolkata_2025-11 (2).xlsx` | Branch consolidation macro (2017); the duplicated file | Ch 19 L1117–1121; Ch 63 |
| `orders_q4_2025_export.csv` | Q4 ERP export behind the branch league table | Ch 14 L1333 |
| `monthly_report.py` (+ `monthly_report_old.py`, `monthly_report_v2_working.py`) | Monthly sales pack script; runs 07:00 on the second working day | Ch 18 L1280; Ch 26 |
| `daily_flash.py` | The Daily Sales Flash | Ch 20 |
| `riverstone-report` package; `reports/riverstone_monthly_2026-01.xlsx`; `Monthly_Report_Dec_FINAL.xlsx` | Ch 29's packaged report and its output | Ch 29, 34 |
| `warehouse/riverstone_wh.duckdb` | Part V practice warehouse | Ch 45–47 |
| `ingest.py`, `apply_day.py`, `make_files.py`, `mock_crm_api.py`, `reset_ch45.py` | Pipeline and its simulators (reader files) | Ch 45–46, 52 |
| `failure-analysis-riverstone.md`, `mesh-maturity-riverstone.md` | Design documents | Ch 61, 62 |
| `roi_case.csv`, `monthly_cost_model.csv`, `unit_economics.csv` | Business case and cost model | Ch 65, 66 |
| `DATA_SPEC.md` | Companion spec; cited as if it were a reader document in Ch 63 (63.11, RJ-S2-27, T11) | Ch 14, 63 |

Proposal: add the story-file names above to the bible so later chapters reuse them rather than invent new ones.

---

## 8. Recurring reports and meetings

### 8a. Daily Sales Flash (fixed, F3)

| Aspect | Canon |
|---|---|
| Before automation | Built by hand each morning by Meera (Ch 7 L382, Ch 83 L310: **40 minutes**). Ch 20 L84 measures the manual process at **80 minutes** (C6) |
| Source load | ERP load runs overnight (Ch 20 L84 "02:00"; failure "at 02:10", L602) |
| Launch | A Monday in **February 2026**, script `daily_flash.py`, service account, **14 recipients**, KPI tiles in the body (Ch 20 L598) |
| Guard | Waits for a `load_status` row; retries every 10 minutes until 08:30; alerts if missing (Ch 20 L609) |
| Orchestration | Moves to the **06:30 IST Dagster run**, which builds **yesterday's** partition (Ch 46 L303; 46.5) |
| Sent | **By 07:30 IST, working days** (F3). Ch 45 L871 "went out at 7:30" agrees |
| Freshness label | "as of 06:35" (Ch 47 banner; Ch 61 fixed by F3) |
| To change | Ch 46 L41 "plate leaves at 6:30" and L808/L813/L902 "delivered by 7:00" → 07:30; Ch 60 "06:00 ERP load + 10 minutes" → F3 wording; Ch 60 "Why this matters" "6:03 a.m." (60.21); Ch 81 story suggestion aligns (81.2) |
| Content | Bookings net of cancellations (46.13), orders, customers, average order, margin, month to date, exceptions |

### 8b. Other recurring reports

| Report / job | Timing | Source |
|---|---|---|
| Friday sales file (Imran) | Friday afternoons, emailed to 11 | Ch 2 L583 |
| Monthly sales pack | 07:00 on the 2nd working day (was 3–4 h by hand) | Ch 18 L1268–1280 |
| Monthly report package | 07:00 daily/monthly run, exits non-zero on failure | Ch 29 L1243; Ch 34 L377 |
| Month-end pack (Power Query) | Month end | Ch 11 |
| Farah's Monday at-risk email | Mondays 09:00 (Apps Script) | bible+ (Ch 8) |
| Q4 branch consolidation | Quarterly (macro) | Ch 19 |
| Power BI refresh | After the nightly load | Ch 16 L558 |
| PO-intake extraction | 06:00 every weekday | Ch 57 L502 |
| Freshness / DQ checks | After the 06:30 run; weekly digest | Ch 47 |
| Sensor archive | Nightly job | Ch 49 L470 |
| NFR "daily file loaded by 07:00 IST" | BA example | Ch 25 L247 (compatible with F3) |

### 8c. Meeting rhythm (canon, bible+)

Daily dispatch stand-up at Bhiwandi Main · Monday weekly sales review (Anita, Vikram, executives) · monthly business review in the first week (MD and department heads; booked, billed and collected shown with definitions since 3 Feb 2026) · quarterly board review.

---

## 9. Open conflicts (for Abhishek to decide)

Proposals are marked **P**. "Decided" rows only need applying. IDs are register findings (CPI = cross-part issue; RJ = reader journey).

### 9a. Top priority

| # | Fact | What the chapters say | Proposal | Findings |
|---|---|---|---|---|
| C1 | Warehouse technology | DuckDB file (Ch 45–47) vs "Postgres + Delta" (Ch 60, 61, 63) vs RDS PostgreSQL warehouse (Ch 65) vs "single database" (Ch 80) | **P: Option A** in §4c (practice DuckDB; production PostgreSQL on RDS + Delta in S3) | 60.1, 61.3, 63.3, 65.8, 80.2 |
| C2 | Book calendar | Part VII starts Jan 2026 with every Part VI system live, but Part VI goes live Mar–Nov 2026 and Part II has Meera learning Power BI in Feb 2026 | **P-T2:** move Part VII one year (Jan 2027 → late 2027) | RJ-S2-25, RJ-S2-26, 63.20, 66.20, 67.10 |
| C3 | Meera's tenure | "four years" by Jan 2026 (Ch 60 L267); "five years" (Ch 83); "six years" (Ch 59 Case 9); joined Q4 2025 (Ch 19) | **P-T1:** joined Oct 2025; spans become "fifteen months" (Ch 60) / "about two years" (Ch 59, 83) | 83.1 (fixed), 59.11, RJ-S3-60 |
| C4 | Meera's title | Sales Coordinator (Ch 1, 28); "Analytics" (Ch 24 memo); Head of Data Platform (Ch 60) | **P:** coordinator until the Ch 8 posting is filled; "Data Analyst" after; Head of Data Platform from Jan 2027 (with P-T2). Ch 24's "Analytics" stays as a department label | 83.1, RJ-S1-4 |
| C5 | First pipeline go-live and the Flash's source | Ch 45 L857 "went live in February" (no year), and the Flash then came "from the warehouse instead of from Meera's spreadsheet"; Ch 20 automated it from `riverstone_full` by script in Feb 2026 | **P:** date Ch 45's go-live **June 2026**; Ch 46 "two months later" = August 2026; "instead of Chapter 20's script". Say that Part V's practice calendar (2–7 Jan 2026) is a replay | RJ-S2-18 |
| C6 | Flash manual time | 40 min (Ch 7 L127, L382; Ch 83 L310) vs 80 min (Ch 20 L84, L712, L823) | **P:** 80 min everywhere (keeps 325 h → ₹97,500 chain); Ch 7 and Ch 83 say "about 80 minutes" | none (new) |
| C8 | Exchange rate | ₹83 (Ch 49), ₹88 (Ch 57/58 code), ₹87 (Ch 65 code) | **P-M1:** ₹87, stated once, in Tools boxes | 57.4, 65.9, 49.2, 55.25 |
| C9 | Hourly rate knock-on in Ch 80 | ₹800 → at F1 the example becomes ₹46,800/yr, 15.4-month payback, so "strong, easy case" no longer fits | **P:** use ₹300 and rewrite the extra point, or keep ₹800 labelled "a senior engineer's rate, not Riverstone's" | 80.8, 66.5 (fixed) |
| C10 | What "Riverstone 2025 revenue" means | ₹43.35 lakh "all of 2025" (Ch 13 L51; Ch 11 "Riverstone has 24 customers") vs ₹114.66 crore company (Ch 14 L70, Ch 23) | **P:** Ch 13 and Ch 11 say "the 24 key accounts"; every later use names the scope | CPI-5, CPI-12, 29.31, 31.10, 33.8, 45.36, 17.40 |

### 9b. People and names

| # | Fact | What the chapters say | Proposal | Findings |
|---|---|---|---|---|
| C13 | Head of the company | MD Arvind Kapoor (Ch 28, 33); "CEO" (Ch 54 L752, L762); "owning family … two senior partners" (Ch 67 L177); "Board / owning family" (Ch 24 fig) | **P:** Riverstone is family-owned; the MD is Arvind Kapoor; the board includes two family partners. "CEO" → "the managing director" | 24.12 |
| C14 | Finance head | Suresh Menon, Finance Manager (Ch 3, 15, 28) vs "finance controller" (Ch 23 L630, Ch 24 L222) | **P:** "Suresh Menon, the Finance Manager" | none (new) |
| C15 | Support lead | Tenzin Dorji (Ch 28) vs Priya Menon (Ch 41 L802) | **P:** Tenzin Dorji in Ch 41 (also removes a third "Priya") | none (new) |
| C16 | Sales Head's gender | Anita ("she") vs Ch 58 "the sales head … His complaint" | Anita, "her" | RJ-S2-23 |
| C17 | Vikram's title | Sales Manager / key accounts sales manager / Sales Manager, Key Accounts | **P:** "Sales Manager, Key Accounts" at first mention per chapter | 25.18 |
| C18 | Regional executives | Ch 28 staff names ≠ full dataset's eight (ids 9–16) | Ch 28 adopts the dataset's names | CPI-10 |
| C19 | Reused first names | Imran (Ch 2) / Imran Shaikh (Ch 48 L283) · Arjun Nair (RSM) / Arjun (Ch 70, 77, 81) / Arjun Reddy (Ch 68) · Deepak Nair (Ch 40) / Deepak (Ch 71) · Karan Ahuja (Ch 28) / Karan (Ch 72, 72A, 75) · Sneha Pillai (Ch 28) / Sneha (Ch 8, 69) · Kavitha Reddy / Kavita (Ch 76A); Kavya (Ch 1) / Kavya Nair (Ch 68) · Priya Nambiar / Priya Menon / Priyanka (Ch 74, 79) · Farah (Ch 73, 76B) · Vikram (Ch 80) · Meera (Ch 78) · Rahul, Neha (Ch 8 exercises) · Divya Krishnan/Menon, Rohit Kamat/Verma | **P:** one rule: Riverstone names are reserved. Part VIII and non-canon examples use names from a separate list; Ch 48's machine owners get new names | 69.16, 80.16, 76B.20, 68.27, CPI-22, CPI-25, RJ-S3-7 |
| C20 | Id 9 | ERP employee 9 = Kavitha Reddy (full dataset) vs CRM/accounts owner 9 = Inside Sales Desk | **P:** give the Inside Sales Desk a non-employee id (e.g. 90) in the CRM and accounts generators, or say "owner 9 is a queue, not employee 9" | 37.4 (partly); new |
| C42 | Ayesha Qureshi | New BA in Ch 25 only | **P:** add to the bible (BA, ex-support desk), or make her Meera | RJ-S3-24 |

### 9c. Company facts and systems

| # | Fact | What the chapters say | Proposal | Findings |
|---|---|---|---|---|
| C11 | Plants in the sensor data | "Bhiwandi Main" (warehouse) and "Chakan Pune" as plants (Ch 48–50; `make_sensor_data.py` L10) vs Taloja and Chakan (Ch 3) | **P:** rename in the script to "Taloja" and "Chakan" and re-run Ch 48–50 outputs | new (touches 48.11, 50.18) |
| C12 | Two sensor datasets | Ch 40 says its generator builds Ch 48's data | Decided (F11) | 48.5, 40.34 |
| C21 | Part IV universes | 5,000 accounts vs 5,027 customers; P01–P24 products vs 101–108; reps 3, 4, 5, 9 only | **P:** one sentence at Ch 36's first use: "Part IV's datasets are simulated separately at Riverstone's scale; they do not join to `riverstone_full`" | RJ-S2-15 |
| C22 | CRM lead volume | 43 leads in 2025 (Ch 5, 13, 23, 35) vs ~400 a month (Ch 36 CRM) | **P:** "the 43 are only the leads reps logged in the ERP extract"; Ch 35's benchmark per 35.3 | 35.3, 36.22, RJ-S1-9 |
| C23 | Number of key accounts | 24 (Ch 10–13, 28) vs 240 (Ch 31 L15, L75, L300) | **P:** Ch 31 says "240 large accounts" (not "key accounts") | RJ-S3-35 |
| C24 | Free delivery | ≥ ₹25,000 (Ch 31 "Chapter 3"; Ch 55 "since January", old ₹40,000); Ch 3 has no rule | **P:** add one sentence to Ch 3's order-to-cash text (the rule since January 2025) | 31.20, RJ-S3-35 |
| C25 | Emailed-order volume | Ch 3: 40 a week × 6 min; Ch 58: 20–40 a day × 3 min; Ch 58's 60 emails are a test set | **P:** Ch 58's explanation per 58.17 ("Ch 3's numbers were for illustration") | 58.17, 58.16 |
| C26 | Invoice timing | Decided (F7); apply to Ch 25 and 76B | — | 25.1, 76B.2, 76B.3 |
| C27 | CRM brand | Bible: never by brand; Ch 60 L82 and Ch 61 L265 say Zoho | **P:** "the CRM" (and "the CRM provider's status page") | 60.22 |
| C28 | Online ordering | Bible: no e-commerce; Ch 42 "customer web portal", "e-commerce contractor" | **P:** "the website's catalogue pages" and "the web contractor" | new |
| C29 | Delivery partners | Swift Movers, Rapid Wheels (Ch 1) vs SwiftLine, BlueCart (Ch 22) | **P:** Ch 22 uses Swift Movers and Rapid Wheels | new |
| C30 | Branch managers | 4 branch sales offices vs "12 branch managers" (Ch 10 ex 27) and "30 branch managers" (Ch 16 L869) | **P:** "4 branch heads" in Ch 10; Ch 16's licence example labelled generic | new |
| C31 | Active customer | Ch 62 "last 30 days" vs Ch 23 calendar year / trailing 12 months | Use Ch 23's | 62.9 |
| C32 | Financial year | Ch 16 Indian FY vs Ch 23 "FY2025" = calendar | **P:** Riverstone reports on calendar years; Ch 23 says "calendar 2025" | RJ-S3-17 |
| C33 | Lead-scoring model | Ch 64 Tools says none exists; Part IV built one and Ch 51 syncs it | Fix Ch 64's note | RJ-S2-29 |
| C34 | ERP writes before assisted mode | Ch 57 (Oct) pipeline loads straight to the ERP; Ch 58 (Nov) launches assisted mode | **P:** Ch 57's incident is the assisted pilot's draft run | RJ-S2-21 |
| C35 | Defect incident | Ch 59 "six weeks later"; Ch 53 "three weeks"; Ch 56's August return is a different incident | Follow 59.7 | 59.7, RJ-S2-24 |
| C36 | Ch 44 memo date | Feb 2026 list uses the April 2026 model | **P:** date the memo November 2026 | RJ-S2-16 |
| C44 | Kolkata's old billing system | Still feeds a spreadsheet upload (Ch 14); "switched off" (Ch 17 L1118); screen-only, live (Ch 63) | **P:** it is still used for entry and exports a spreadsheet; Ch 17 says "exported from the old billing system before Kolkata moved its reporting to the ERP" | 63.11, 17.29 |
| C45 | Read replicas | Ch 61 fig shows BI read replicas; none built | Drop or label as proposal (with C1) | 61.3 |

### 9d. Smaller items to settle with the above

| # | Item | Proposal | Findings |
|---|---|---|---|
| C7 | Flash SLA "7:00" in Ch 46 | Apply F3 (07:30) | 60.3 |
| C37 | Kubernetes in Ch 52/56/61 | Apply F9 | 52.22 |
| C38 | Size-band edges | Apply F10 | 18.23 |
| C39 | "Rs" in output; international grouping | Apply F4, F8 | 67.9, V57.9 |
| C40 | Ch 20 "41 working days" (L561) vs "40" (L823) | 325 ÷ 8 = 40.6: say "about 41" in both | new |
| C41 | Ch 58 PO-intake ROI "~90 minutes a day" | 80 minutes | 58.19 |

**Count: 44 conflict rows** (C1–C45; C43 unused). **38 need a decision**; 6 (C7, C12, C26, C37, C38, C39) only apply a decision already taken.

---

## Questions for Abhishek

1. Warehouse: approve **Option A** (practice DuckDB, production PostgreSQL on RDS + Delta)?
2. Calendar: approve **moving Part VII to 2027** and Meera joining in **October 2025**?
3. Exchange rate: **₹87** (keeps Ch 65–67) or ₹88 (keeps Ch 57–58)?
4. Flash manual time: **80 minutes** everywhere?
5. Names: approve the rule "Riverstone names are reserved", with Part VIII using a separate name list?
6. Ch 80: at ₹300/hour the payback becomes 15.4 months. Rewrite the answer, or keep ₹800 as a stated non-Riverstone rate?
