// Analyst to Architect, Chapter 19 - Office Scripts (Excel on the web).
// Each script is a separate main(): paste one at a time into Automate > New Script.

function main(workbook: ExcelScript.Workbook) {
  const sheet = workbook.getWorksheet("Master");
  if (!sheet) {                                   // no such sheet: stop here
    console.log("No Master sheet");
    return;
  }
  const used = sheet.getUsedRange();
  const lastRow = used.getRowCount();
  const lastCol = used.getColumnCount();

  const header = sheet.getRangeByIndexes(0, 0, 1, lastCol);
  header.getFormat().getFont().setBold(true);
  header.getFormat().getFont().setColor("#FFFFFF");
  header.getFormat().getFill().setColor("#0F5C8C");
  sheet.getFreezePanes().freezeRows(1);           // freeze the header row
  used.getFormat().autofitColumns();

  console.log(`formatted ${lastRow} rows, ${lastCol} columns`);
}

// ---- next script ----

function main(workbook: ExcelScript.Workbook) {
  const sheet = workbook.getWorksheet("Master");
  if (!sheet) { console.log("No Master sheet"); return; }
  const rowCount = sheet.getUsedRange().getRowCount();
  const statusRange = sheet.getRangeByIndexes(1, 8, rowCount - 1, 1);  // I2 down, one column
  const values = statusRange.getValues();              // one read: a grid, one row per cell

  const map: { [key: string]: string } = {
    "delivered": "Delivered", "dlvd": "Delivered", "cancelled": "Cancelled",
    "canceled": "Cancelled", "cxl": "Cancelled", "shipped": "Shipped", "pending": "Pending"
  };

  let unmapped = 0;
  for (let r = 0; r < values.length; r++) {
    const raw = String(values[r][0]).trim().toLowerCase();
    if (map[raw]) { values[r][0] = map[raw]; } else { unmapped++; }
  }

  statusRange.setValues(values);                       // one write, of column I only
  console.log(`${values.length} rows, ${unmapped} unmapped statuses`);
}
