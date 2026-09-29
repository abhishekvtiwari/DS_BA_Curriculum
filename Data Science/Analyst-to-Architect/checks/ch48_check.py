# Analyst to Architect - Chapter 48 checks. Run from the book root:  python3 checks/ch48_check.py
# Needs the generated dataset (companion/ch48/make_sensor_data.py). Riverstone Supplies is fictional.
import os, sys, duckdb
os.chdir('companion/ch48')
ok=True
def check(label,got,exp):
    global ok; good=(got==exp); ok&=good
    print(('OK  ' if good else 'FAIL'),label,got,'' if good else f'(expected {exp})')
con=duckdb.connect()
con.execute("CREATE VIEW r AS SELECT * FROM read_parquet('sensor_readings/*/*.parquet', hive_partitioning=true)")
check('total readings', con.execute("SELECT COUNT(*) FROM r").fetchone()[0], 19872000)
check('25 machines x 92 days x 8640', 25*92*8640, 19872000)
check('readings above 200 C', con.execute("SELECT COUNT(*) FROM r WHERE temperature_c > 200").fetchone()[0], 8143256)
check('1 Dec Bhiwandi rows', con.execute("SELECT COUNT(*) FROM r WHERE reading_date='2025-12-01' AND plant='Bhiwandi Main'").fetchone()[0], 129600)
row=con.execute("""SELECT ROUND(AVG(temperature_c),2), ROUND(AVG(CAST(scrap_flag AS INT))*100,2), SUM(units_made)::BIGINT
                   FROM r WHERE temperature_c>190 AND plant='Bhiwandi Main'""").fetchone()
check('Bhiwandi hot readings summary', row, (203.43, 1.33, 23234149))
check('supervisor rows per machine', con.execute("SELECT COUNT(*) FROM r WHERE machine_id='M-01'").fetchone()[0], 794880)
# timing ratios quoted in 48.6 and exercise 8
check('Ex8 ratio small (ms, section 48.6 table)', round(252.3/6.8), 37)
check('Ex8 ratio large (ms, section 48.6 table)', round(1211.8/213.0,1), 5.7)
check('salted/plain join rows = 3 machines x 794,880', con.execute("SELECT COUNT(*) FROM r WHERE machine_id IN ('M-01','M-02','M-03')").fetchone()[0], 2384640)
check('Bhiwandi Main machines x 8,640 x 92', con.execute("SELECT COUNT(*) FROM r WHERE plant='Bhiwandi Main'").fetchone()[0], 15*8640*92)
check('weekly summary rows (plant x ISO week)', con.execute("SELECT COUNT(*) FROM (SELECT DISTINCT plant, weekofyear(reading_date) FROM r)").fetchone()[0], 28)
check('12 M readings/week = ~200 machines at 10 s', round(12_000_000/(8640*7)), 198)
print('ALL CHECKS PASSED' if ok else 'SOME CHECKS FAILED')
