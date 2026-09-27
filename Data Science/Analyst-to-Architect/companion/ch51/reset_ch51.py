"""Chapter 51 companion: reset the practice environment.
Creates riverstone_source (a private copy of riverstone_2025 that plays the ERP and CRM's own database),
and clears the sync log, the mock CRM's state, and the webhook inbox.
Run: python3 reset_ch51.py     (PostgreSQL must be running; riverstone_2025 loaded)
Riverstone Supplies is fictional; every name and number is invented."""
import os, shutil, psycopg2
PG = os.environ.get("RIVERSTONE_PG", "dbname=postgres")

def reset():
    conn = psycopg2.connect(PG); conn.autocommit = True
    cur = conn.cursor()
    cur.execute("SELECT pg_terminate_backend(pid) FROM pg_stat_activity "
                "WHERE datname IN ('riverstone_source', 'riverstone_2025') AND pid <> pg_backend_pid()")
    cur.execute("DROP DATABASE IF EXISTS riverstone_source")
    cur.execute("CREATE DATABASE riverstone_source TEMPLATE riverstone_2025")
    conn.close()
    for folder in ["sync_state", "webhook_inbox"]:
        shutil.rmtree(folder, ignore_errors=True); os.makedirs(folder)

if __name__ == "__main__":
    reset(); print("Chapter 51 environment reset.")
