"""Chapter 45 companion: reset the practice environment.
Creates riverstone_source (a private copy of riverstone_2025 that plays the ERP and CRM),
deletes the local warehouse, and writes the practice export files.
Run: python3 reset_ch45.py     (PostgreSQL must be running; riverstone_2025 loaded)
Riverstone Supplies is fictional; every name and number is invented."""
import os, shutil, psycopg2
import make_files

PG = os.environ.get("RIVERSTONE_PG", "dbname=postgres")

def reset():
    conn = psycopg2.connect(PG); conn.autocommit = True
    cur = conn.cursor()
    cur.execute("SELECT pg_drop_replication_slot(slot_name) FROM pg_replication_slots "
                "WHERE slot_name = 'ch45_slot'")
    cur.execute("SELECT pg_terminate_backend(pid) FROM pg_stat_activity "
                "WHERE datname IN ('riverstone_source', 'riverstone_2025') AND pid <> pg_backend_pid()")
    cur.execute("DROP DATABASE IF EXISTS riverstone_source")
    cur.execute("CREATE DATABASE riverstone_source TEMPLATE riverstone_2025")
    conn.close()
    shutil.rmtree("warehouse", ignore_errors=True); os.makedirs("warehouse")
    shutil.rmtree("exports", ignore_errors=True); os.makedirs("exports")
    make_files.write_all("exports")

if __name__ == "__main__":
    reset(); print("Chapter 45 environment reset.")
