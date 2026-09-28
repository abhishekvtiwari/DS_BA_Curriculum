# Terminal versions of the full-dataset setup scripts

These load the same data as `../riverstone_full_setup_postgresql.sql` and `../riverstone_full_setup_mysql.sql`,
but faster, by reading the CSV files with `\copy` (psql) or `LOAD DATA LOCAL INFILE` (mysql). They need a
terminal (Chapter 26 §26.0) and must be run from the `companion/full/` folder so the CSV paths resolve:

    cd companion/full
    psql -d riverstone_full -f terminal/riverstone_full_setup_postgresql.sql
    mysql --local-infile=1 -u root < terminal/riverstone_full_setup_mysql.sql

The scripts one folder up use plain INSERT statements, so DBeaver can run them (Chapter 14 §14.1).
Both versions were loaded side by side on 28 Sep 2026 and every table matched.
