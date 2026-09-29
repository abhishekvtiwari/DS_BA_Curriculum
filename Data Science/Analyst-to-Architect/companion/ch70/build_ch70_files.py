"""
Analyst to Architect — Chapter 70: Excel, Google Sheets, VBA & BI Question Bank
build_ch70_files.py — writes the chapter's practice table (section 70.0).

Run from this folder:  python3 build_ch70_files.py      (needs pandas, openpyxl)
Creates:
  ch70_practice.xlsx   sheet "Orders": the 6-row practice table at A1:J7 (header in row 1),
                       sheet "Confirmations": 3 orders with an email address, for Q70-053
  ch70_practice.csv    the Orders sheet as CSV, to import into Google Sheets
Riverstone Supplies is fictional; every name and number is invented. Products and list prices are
the ones in Chapter 10 and 11's practice file.
"""
import pathlib
import pandas as pd

HERE = pathlib.Path(__file__).resolve().parent

orders = pd.DataFrame(
    [
        (1001, "2025-01-06", "Sharma Hardware", "Storage", "Storage Box 10L", 25, 430, 5, "Delivered"),
        (1002, "2025-01-07", "Metro Mart", "Kitchen", "Water Bottle 1L", 40, 115, 0, "Delivered"),
        (1003, "2025-01-09", "Sharma Hardware", "Storage", "Stackable Bin", 30, 290, 5, "Cancelled"),
        (1004, "2025-01-13", "Coastal Foods", "Industrial", "Industrial Crate", 20, 1400, 10, "Delivered"),
        (1005, "2025-01-20", "Metro Mart", "Storage", "Storage Box 25L", 8, 750, 0, "Shipped"),
        (1006, "2025-02-03", "Sharma Hardware", "Storage", "Storage Box 10L", 12, 430, 0, "Delivered"),
    ],
    columns=["order_id", "order_date", "customer_name", "category", "product_name",
             "quantity", "unit_price", "discount_pct", "status"],
)
orders["order_date"] = pd.to_datetime(orders.order_date)
orders["net_revenue"] = orders.quantity * orders.unit_price * (1 - orders.discount_pct / 100)
# column order A..J: net_revenue in I, status in J (the chapter's formulas use these letters)
orders = orders[["order_id", "order_date", "customer_name", "category", "product_name",
                 "quantity", "unit_price", "discount_pct", "net_revenue", "status"]]

confirmations = pd.DataFrame(
    [
        (1001, "Sharma Hardware", "buy@sharmahardware.example.com", ""),
        (1002, "Metro Mart", "orders@metromart.example.com", ""),
        (1004, "Coastal Foods", "purchase@coastalfoods.example.com", ""),
    ],
    columns=["order_id", "customer_name", "email", "status"],
)

with pd.ExcelWriter(HERE / "ch70_practice.xlsx", engine="openpyxl", datetime_format="yyyy-mm-dd") as xw:
    orders.to_excel(xw, sheet_name="Orders", index=False)
    confirmations.to_excel(xw, sheet_name="Confirmations", index=False)
out = orders.copy()
out["order_date"] = out.order_date.dt.strftime("%Y-%m-%d")
out.to_csv(HERE / "ch70_practice.csv", index=False)
print(out.to_string(index=False))
print("total net_revenue", orders.net_revenue.sum(), "| excluding cancelled",
      orders.loc[orders.status != "Cancelled", "net_revenue"].sum())
