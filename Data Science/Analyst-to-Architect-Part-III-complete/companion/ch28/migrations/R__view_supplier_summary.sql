-- A repeatable migration (Flyway convention). migrate.py skips R__ files; Flyway re-applies them when they change.
CREATE OR REPLACE VIEW supplier_summary AS
SELECT supplier_city, COUNT(*) AS suppliers FROM suppliers GROUP BY supplier_city;
