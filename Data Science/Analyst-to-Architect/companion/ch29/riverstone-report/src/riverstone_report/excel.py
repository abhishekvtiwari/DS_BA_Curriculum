"""Writing the formatted workbook."""
from pathlib import Path

import pandas as pd
from openpyxl.styles import Font

from riverstone_report.transform import MonthSummary

RUPEES = '"₹"#,##0'


def write_report(summary: MonthSummary, categories: pd.DataFrame,
                 customers: pd.DataFrame, path: Path) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    headline = pd.DataFrame({
        "metric": ["Net revenue", "Orders", "Customers", "Target", "% of target"],
        "value": [summary.revenue, summary.orders, summary.customers,
                  summary.target, summary.pct_of_target],
    })
    sheets = [("Summary", headline), ("Categories", categories), ("Top customers", customers)]
    with pd.ExcelWriter(path, engine="openpyxl") as writer:
        for sheet, frame in sheets:
            frame.to_excel(writer, sheet_name=sheet, index=False)
            ws = writer.sheets[sheet]
            for cell in ws[1]:
                cell.font = Font(bold=True)
            ws.column_dimensions["A"].width = 26
            ws.column_dimensions["B"].width = 16
        for row in (2, 5):
            writer.sheets["Summary"].cell(row=row, column=2).number_format = RUPEES
        for sheet in ("Categories", "Top customers"):
            for cell in writer.sheets[sheet]["B"][1:]:
                cell.number_format = RUPEES
    return path
