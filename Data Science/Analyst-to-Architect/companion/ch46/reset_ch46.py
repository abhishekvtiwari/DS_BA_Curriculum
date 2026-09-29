"""Chapter 46 companion: reset the practice environment.
Same source as Chapter 45 (riverstone_source, a private copy of riverstone_2025), plus a fresh warehouse,
the dispatch files, an outbox folder for delivered reports, and an alerts folder.
Run: python3 reset_ch46.py     (PostgreSQL must be running; riverstone_2025 loaded)
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
                "WHERE slot_name = 'ch45_slot'")                 # Chapter 45's change-capture slot, if any
    cur.execute("SELECT pg_terminate_backend(pid) FROM pg_stat_activity "
                "WHERE datname IN ('riverstone_source', 'riverstone_2025') AND pid <> pg_backend_pid()")
    cur.execute("DROP DATABASE IF EXISTS riverstone_source")
    cur.execute("CREATE DATABASE riverstone_source TEMPLATE riverstone_2025")
    conn.close()
    for folder in ["warehouse", "exports", "outbox", "alerts"]:
        shutil.rmtree(folder, ignore_errors=True)
        os.makedirs(folder)
    make_files.write_all("exports")

if __name__ == "__main__":
    reset(); print("Chapter 46 environment reset.")
