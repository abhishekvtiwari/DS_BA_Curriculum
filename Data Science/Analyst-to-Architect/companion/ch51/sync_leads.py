"""Chapter 51 companion: the chapter's computations and keys, collected in one file for the project.
It contains exactly what sections 51.2 to 51.4 build in the notebook, and nothing else:
  lead_scores()       runs lead_scores.sql       -> {"1": {"company_name": ..., "stage": ..., "score": 45}, ...}
  follow_up_flags()   runs follow_up_due.sql     -> {"1": False, "2": True, ...} for every customer
  idempotency_key()   entity + values            (section 51.3; fails when a value goes back to an earlier one)
  run_key()           entity + values + run id   (section 51.4; the one to use)
Riverstone Supplies is fictional; every name and number is invented."""
import hashlib, json, os
import psycopg2

SRC = os.environ.get("RIVERSTONE_SOURCE", "dbname=riverstone_source")


def fetch_rows(sql, params=None):
    conn = psycopg2.connect(SRC)
    with conn, conn.cursor() as cur:
        cur.execute(sql, params)
        rows = cur.fetchall()
    conn.close()
    return rows


def lead_scores():
    with open("lead_scores.sql") as f:
        rows = fetch_rows(f.read())
    return {str(lead_id): {"company_name": name, "stage": stage, "score": score}
            for lead_id, name, source, stage, score in rows}


def follow_up_flags():
    with open("follow_up_due.sql") as f:
        due = {str(row[0]) for row in fetch_rows(f.read())}
    customers = [str(row[0]) for row in fetch_rows("SELECT customer_id FROM customers ORDER BY customer_id")]
    return {cid: cid in due for cid in customers}


def idempotency_key(record, payload):
    content = record + ":" + json.dumps(payload, sort_keys=True)
    return hashlib.sha256(content.encode()).hexdigest()[:16]


def run_key(record, payload, run_id):
    content = record + ":" + run_id + ":" + json.dumps(payload, sort_keys=True)
    return hashlib.sha256(content.encode()).hexdigest()[:16]
