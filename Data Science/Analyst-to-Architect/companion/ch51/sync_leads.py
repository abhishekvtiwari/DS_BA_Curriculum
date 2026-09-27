"""Chapter 51 companion: compute lead scores and overdue-invoice flags from Riverstone's data,
and push them into the sandbox CRM. Every write is idempotent: safe to run the sync again.
Riverstone Supplies is fictional; every name and number is invented."""
import hashlib, os
from datetime import date
import psycopg2

SRC = os.environ.get("RIVERSTONE_SOURCE", "dbname=riverstone_source")
TODAY = date(2026, 1, 6)                    # fixed "today" so every run of this chapter agrees
STAGE_POINTS = {"New": 10, "Contacted": 30, "Quoted": 55, "Won": 100, "Lost": 0}
SOURCE_POINTS = {"Referral": 15, "Website": 10, "Trade Show": 20, "Cold Call": 5}

def fetch_rows(sql, params=None):
    conn = psycopg2.connect(SRC)
    with conn, conn.cursor() as cur:
        cur.execute(sql, params)
        rows = cur.fetchall()
    conn.close()
    return rows

def lead_scores():
    """Score = latest stage points + source points + a recency bonus for stages entered in the last 14 days.
    Documented, deterministic, and small enough to check by hand (section 51.2)."""
    rows = fetch_rows("""
        SELECT l.lead_id, l.company_name, l.source,
               h.stage, h.entered_at
        FROM leads AS l
        JOIN lead_stage_history AS h ON h.lead_id = l.lead_id
        ORDER BY l.lead_id, h.entered_at""")
    latest = {}
    for lead_id, company, source, stage, entered_at in rows:
        latest[lead_id] = (company, source, stage, entered_at)   # keeps the last row per lead: latest stage
    scores = {}
    for lead_id, (company, source, stage, entered_at) in latest.items():
        base = STAGE_POINTS.get(stage, 0) + SOURCE_POINTS.get(source, 0)
        recent = (TODAY - entered_at.date()).days <= 14
        score = base + (10 if recent and stage != "Lost" else 0)
        scores[str(lead_id)] = {"company_name": company, "stage": stage, "score": min(score, 100)}
    return scores

def overdue_flags():
    """Simplification: Riverstone's finance system tracks payments separately (out of scope here).
    We approximate a 45-75 day aging bucket using each customer's most recent Delivered order,
    standing in for a real accounts-receivable feed, and flag the customer, not the order."""
    rows = fetch_rows("""
        SELECT customer_id, MAX(order_date) AS most_recent_delivery
        FROM orders
        WHERE status = 'Delivered'
        GROUP BY customer_id
        HAVING MAX(order_date) BETWEEN %s - INTERVAL '75 days' AND %s - INTERVAL '45 days'""", [TODAY, TODAY])
    out = {}
    for customer_id, most_recent in rows:
        days = (TODAY - most_recent.date()).days if hasattr(most_recent, "date") else (TODAY - most_recent).days
        out[str(customer_id)] = {"days_overdue": days}
    return out

def idempotency_key(lead_id, payload):
    """A stable key: same lead, same content, same key - so a retried request is recognized as a repeat."""
    content = f"{lead_id}:{payload.get('score')}:{payload.get('stage')}"
    return hashlib.sha256(content.encode()).hexdigest()[:16]
