"""
Analyst to Architect — Chapter 18: Python for Analysts (pandas & Automation)
build_ch18_files.py — for instructors: rebuilds the one data file this chapter ships. Readers don't need to run it.

Run from this folder:  python3 build_ch18_files.py    (needs pandas + pyarrow; reads companion/full/*.parquet)
Creates:
  api_response.json   a saved copy of page 1 of the demonstration API's reply for 1 December 2025
                      (the same reply api_demo.py sends for from=2025-12-01&to=2025-12-01&page=1&page_size=100)
The chapter also reads companion/full/, ch14/orders_q4_2025_export.csv, ch15/chart_data/,
ch16/city_region.csv and ch17/sales_exports/ (as ../../companion/... from work/ch18). The other files in this folder (api_demo.py,
clean_orders_pandas.py, monthly_report.py) are written by hand and are part of the chapter.
Riverstone Supplies is fictional; every name and number is invented.
"""
import json
import pathlib

from api_demo import orders_page

HERE = pathlib.Path(__file__).resolve().parent
code, payload = orders_page({"from": "2025-12-01", "to": "2025-12-01", "page": "1", "page_size": "100"})
assert code == 200
(HERE / "api_response.json").write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
old = HERE / "report_template.md"          # no longer used by the chapter
if old.exists():
    old.unlink()
print("wrote api_response.json:", payload["count"], "lines,", len(payload["results"]), "on page 1 of", payload["pages"])
