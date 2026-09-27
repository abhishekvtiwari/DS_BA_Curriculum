"""Chapter 45 companion (copied for Chapter 46): write the practice export files.
dispatch_2026-01-02.csv  - Bhiwandi Main's daily dispatch sheet, saved from a spreadsheet: UTF-8 with a
                           byte-order mark, dd-mm-yyyy dates, quantities with thousands separators, one bad
                           row, and a blank line at the end.
dispatch_2026-01-05.csv  - next file: a new column 'vehicle_no' added and 'qty_units' renamed 'units'.
Riverstone Supplies is fictional; every name and number is invented."""
import os
DAY1 = """dispatch_id,order_id,dispatch_date,warehouse,qty_units,remarks
D-2601,10175,02-01-2026,Bhiwandi Main,100,"Delivered to site, signed"
D-2602,10173,02-01-2026,Bhiwandi Main,"1,200",Part load
D-2603,10172,02-01-2026,Bhiwandi Main,N/A,Awaiting count
D-2604,10171,02-01-2026,Bhiwandi Main,85,
D-2605,10170,02-01-2026,Bhiwandi Main,"2,040","Two trucks; second at 4 pm"

"""
DAY2 = """dispatch_id,order_id,dispatch_date,warehouse,units,remarks,vehicle_no
D-2606,10176,05-01-2026,Bhiwandi Main,160,,MH04AB1234
D-2607,10178,05-01-2026,Bhiwandi Main,25,Urgent,MH04CD5678
"""
def write_all(folder):
    with open(os.path.join(folder, "dispatch_2026-01-02.csv"), "w", encoding="utf-8-sig", newline="") as f:
        f.write(DAY1.replace("\n", "\r\n"))
    with open(os.path.join(folder, "dispatch_2026-01-05.csv"), "w", encoding="utf-8", newline="") as f:
        f.write(DAY2)
