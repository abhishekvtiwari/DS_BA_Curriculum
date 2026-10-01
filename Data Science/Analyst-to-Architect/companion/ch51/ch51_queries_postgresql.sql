-- Chapter 51. Data Activation: Reverse ETL, APIs & System Integration
-- Practice SQL for POSTGRESQL, extracted from the chapter.
--
-- Riverstone Supplies is the worked example throughout the book. Load the database
-- first (companion/riverstone_setup_mini.sql, riverstone_2025_setup.sql, or
-- companion/full/riverstone_full_setup_postgresql.sql), then run these statements in order.
--
-- Each statement keeps the chapter's explanation above it and the chapter's own
-- result below it, marked as the chapter's. Run it yourself to see your own.
-- Source: manuscript/ch51-data-activation.md


-- - start_crm() and start_receiver() start the two servers in the background of the notebook, at
-- ports 8051 and 8052 on this computer, as Chapter 45's practice API did at 8045. - seed_crm()
-- fills the sandbox from riverstone_source: all of Riverstone's leads, and an account for each
-- customer except the newest, customer 24, who signed up in November and has no CRM account yet
-- (section 51.4 creates it). It returns the two counts. - BASE is the start of every address the
-- CRM answers on. TOKEN comes from the environment; the default after it is the sandbox's public
-- token, so the notebook runs even without .env. HEADERS sends it as a bearer token.

-- > Tool note. The outputs in this chapter were produced with Python 3.11.15, requests 2.33.1,
-- psycopg2 2.9.13, python-dotenv 1.2.3, and PostgreSQL 16.13.

-- ---

-- =============================================================================================
-- 51.1 The loop nobody finishes
-- =============================================================================================

-- Chapter 7 drew the full flow from a question to an answer. Here's the piece most companies
-- build, and then stop before finishing.

-- Figure 51.1 — Most data platforms stop at the dashboard. Activation closes the loop back into
-- the systems people work in every day.

-- A dashboard is pull: someone has to open it, notice something, and act. A synced field in the
-- CRM is push: it's sitting where the action already happens, next to the customer's name, when
-- the rep is already looking. The difference in how often it gets used is not small.

-- Fields worth syncing back, and what they change:

-- | Field | Computed from | Changes what | |---|---|---| | Lead score | Stage, source, recency
-- (this chapter) | Which leads a rep calls first | | Follow-up-due flag | Order dates and delivery
-- status (this chapter) | Which quiet customers a rep calls this week | | Customer health score |
-- Order frequency, support tickets, payment history | Who account management checks in on | |
-- Credit limit or hold | Payment history, exposure | Whether an order can be placed at all | |
-- Reorder flag | Stock levels, usage rate | Whether a purchase order gets raised | | Overdue-
-- payment flag | Invoices and payments | Whether finance chases a customer this week | | Churn
-- risk | Usage decline, contract dates | Whether a renewal call gets scheduled |

-- Every one of these is a number the warehouse can compute, once it has the data. The work in this
-- chapter is getting it to land somewhere it changes a decision, safely.

-- ---

-- =============================================================================================
-- 51.2 Computing what to sync
-- =============================================================================================

-- Riverstone will sync two things into its CRM: a lead score on each lead, so reps call the right
-- leads first, and a follow-up-due flag on each customer account, so reps call the customers who
-- have gone quiet.

-- "Today" in this chapter. Throughout this chapter, today is 6 January 2026, the same simulated
-- calendar as Chapter 46: the nightly run starts at 06:30 IST that morning. Every date rule below
-- counts back from that day, which the SQL writes as DATE '2026-01-06', so every run of the
-- chapter gives the same answer.

-- =============================================================================================
-- Lead scoring
-- =============================================================================================

-- The rule is deliberately simple and fully documented, because a score nobody can explain doesn't
-- earn trust from the sales team:

-- > score = points for the lead's current stage + points for how it arrived + a recency bonus if
-- it entered that stage in the last 14 days, capped at 100. A Lost lead scores 0, whatever else is
-- true.

-- | Current stage | Points | |---|---| | New | 10 | | Contacted | 30 | | Quoted | 55 | | Won | 100
-- | | Lost | 0, and the whole score is 0 |

-- | Source | Points | |---|---| | Trade fair | 20 | | Referral | 15 | | Website | 10 | | IndiaMART
-- listing | 10 | | Cold call | 5 |

-- - Recency: +10 if the lead entered its current stage on or after 23 December 2025, 14 days
-- before today. - Lost: a lost lead should never rank above an active one, so it scores 0 whatever
-- its source or recency. - The cap: only a Won lead can pass 100 (100 plus its source points), so
-- every Won lead scores exactly 100. The highest score for a lead still in play is Quoted 55 +
-- Trade fair 20 + recency 10 = 85.

-- By hand first. To score a lead you need its source and its current stage, with the date it
-- entered that stage. The table lead_stage_history has one row for each stage a lead has entered.
-- This query, run in psql or DBeaver against riverstone_source (Chapter 12), picks each lead's
-- newest row:

-- <!-- db: riverstone_source -->

WITH latest AS (
    SELECT lead_id, stage, entered_at,
           ROW_NUMBER() OVER (PARTITION BY lead_id ORDER BY entered_at DESC) AS rn
    FROM lead_stage_history
)
SELECT l.lead_id, l.company_name, l.source, s.stage, s.entered_at::date AS stage_entered
FROM leads AS l
JOIN latest AS s ON s.lead_id = l.lead_id AND s.rn = 1
WHERE l.lead_id <= 7
ORDER BY l.lead_id;

/* The chapter shows:
    lead_id |   company_name    |  source   |   stage   | stage_entered 
   ---------+-------------------+-----------+-----------+---------------
          1 | Anand Stores      | Referral  | Contacted | 2025-04-13
          2 | Bright Kitchens   | Website   | Quoted    | 2025-06-29
          3 | Bright Kitchens   | Website   | New       | 2025-06-12
          4 | BRIGHT KITCHENS   | Website   | New       | 2025-06-12
          5 | Cafe Mocha Lane   | Website   | New       | 2025-01-02
          6 | Delta Hospitality | Cold call | Lost      | 2025-05-27
          7 | Elite Mart        | Referral  | Won       | 2025-07-23
   (7 rows)
*/


-- - fetch_rows() is a smaller version of Chapter 45's helper: it opens a connection, runs one
-- query, and returns the rows as a list of tuples. Its second argument, params, would fill %s
-- placeholders in the query with values, as in Chapter 45; this chapter's queries have none, so it
-- stays None. - with open("lead_scores.sql") as f: opens the file, and f.read() reads it as one
-- string: the query. - The dictionary comprehension (Chapter 17) makes one entry per row. for
-- lead_id, name, source, stage, score in score_rows unpacks each row's five columns into five
-- names. The key is str(lead_id), text, because the CRM's addresses and JSON use text ids.

-- Reading it. All 43 leads are scored, and the three agree with the table worked by hand: 65, 0,
-- and 100. Check a computed field by hand like this every time: a score nobody can rebuild from
-- its own rule is a score nobody should trust, however tidy the code looks.

-- > Simplification note. A learned lead-scoring model would use more signals, such as the number
-- of contacts, the deal size, and what happened to similar past leads. That's a classification
-- model, the kind Part 4 built on Riverstone's CRM leads (Chapters 35 to 39); its predicted
-- probability could be synced with exactly this chapter's mechanics. This score is deliberately
-- transparent: every point traces to a rule a sales manager can read in one sentence, which
-- matters more early on than a cleverer model nobody can explain.

-- =============================================================================================
-- The follow-up-due flag
-- =============================================================================================

-- Riverstone's finance system tracks invoices and payments separately, and this book doesn't have
-- that data, so the chapter doesn't pretend to compute an overdue-payment flag. It syncs a flag it
-- can compute honestly from orders:

-- > A customer is follow-up due if they ordered in the last six months (since 6 July 2025) but
-- have had no delivered order in the last 45 days (since 22 November 2025).

-- This is a recency signal, a customer who has gone quiet, not a payment status. A customer who
-- owes money but took a delivery last week isn't flagged. Any real deployment should replace or
-- sharpen it with its owner's actual definition, agreed as a Chapter 47 data contract. The query
-- is in follow_up_due.sql:

SELECT c.customer_id, c.customer_name,
       MAX(o.order_date) AS last_order,
       MAX(CASE WHEN o.status = 'Delivered' THEN o.order_date END) AS last_delivered
FROM customers AS c
JOIN orders AS o ON o.customer_id = c.customer_id
GROUP BY c.customer_id, c.customer_name
HAVING MAX(o.order_date) >= DATE '2026-01-06' - INTERVAL '6 months'
   AND COALESCE(MAX(CASE WHEN o.status = 'Delivered' THEN o.order_date END), DATE '1900-01-01')
       < DATE '2026-01-06' - 45
ORDER BY c.customer_id;

/* The chapter shows:
    customer_id |   customer_name   | last_order | last_delivered 
   -------------+-------------------+------------+----------------
              2 | Patel Kitchenware | 2025-11-09 | 2025-11-09
              8 | Blue Bay Cafe     | 2025-11-09 | 2025-11-09
              9 | Lakeview Resorts  | 2025-12-21 | 2025-10-15
             13 | Om Sai Provisions | 2025-07-22 | 2025-07-22
             20 | Tasty Tiffins     | 2025-10-26 | 2025-10-26
             22 | Festive Gifts Co  | 2025-11-19 | 2025-11-19
   (6 rows)
*/

