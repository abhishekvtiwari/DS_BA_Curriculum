"""Chapter 45 companion: reset the practice environment.
Creates riverstone_source (a private copy of riverstone_2025 that plays the ERP and CRM),
deletes the local warehouse, and writes the practice export files.
Run: python3 reset_ch45.py     (PostgreSQL must be running; riverstone_2025 loaded)
Connection: the same RIVERSTONE_SOURCE string as the chapter's notebook (default "dbname=riverstone_source");
reset() swaps its dbname for the maintenance database "postgres", because a database can't be copied or dropped
from inside itself. PostgreSQL copies a database only while nobody else is connected to it, so reset() first
closes other connections to riverstone_2025 and riverstone_source (for example an open DBeaver tab).
Riverstone Supplies is fictional; every name and number is invented."""
import os, shutil, psycopg2
import make_files

def reset():
    src = os.environ.get("RIVERSTONE_SOURCE", "dbname=riverstone_source")
    conn = psycopg2.connect(src, dbname="postgres")      # same user, password and host; other database
    conn.autocommit = True
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
