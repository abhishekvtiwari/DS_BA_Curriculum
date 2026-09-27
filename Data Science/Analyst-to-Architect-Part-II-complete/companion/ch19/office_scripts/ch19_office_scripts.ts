// Analyst to Architect, Chapter 19 — Office Scripts (Excel on the web).
// Paste one function at a time into Automate > New Script.

function main(workbook: ExcelScript.Workbook) {
  const sheet = workbook.getWorksheet("Master");
  const used = sheet.getUsedRange();
  const lastRow = used.getRowCount();
  const lastCol = used.getColumnCount();

  const header = sheet.getRangeByIndexes(0, 0, 1, lastCol);
  header.getFormat().getFont().setBold(true);
  header.getFormat().getFont().setColor("#FFFFFF");
  header.getFormat().getFill().setColor("#0F5C8C");
  sheet.getRange("A2").getFormat().setRowHeight(18);
  used.getFormat().autofitColumns();

  console.log(`formatted ${lastRow} rows, ${lastCol} columns`);
}


function main(workbook: ExcelScript.Workbook) {
  const sheet = workbook.getWorksheet("Master");
  const range = sheet.getUsedRange();
  const values = range.getValues();                    // one read: a 2-D array

  const map: { [key: string]: string } = {
    "delivered": "Delivered", "dlvd": "Delivered", "cancelled": "Cancelled",
    "canceled": "Cancelled", "cxl": "Cancelled", "shipped": "Shipped", "pending": "Pending"
  };

  let unmapped = 0;
  for (let r = 1; r < values.length; r++) {            // row 0 is the header
    const raw = String(values[r][8]).trim().toLowerCase();   // column I
    if (map[raw]) { values[r][8] = map[raw]; } else { unmapped++; }
  }

  range.setValues(values);                             // one write
  console.log(`${values.length - 1} rows, ${unmapped} unmapped statuses`);
}
