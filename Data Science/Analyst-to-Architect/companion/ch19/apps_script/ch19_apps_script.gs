// Analyst to Architect, Chapter 19 - Google Apps Script for Sheets.
// Paste into Extensions > Apps Script. Set CRM_TOKEN in Project Settings > Script Properties,
// and the project's time zone to India (Asia/Kolkata) before adding timed triggers.

function formatMaster() {
  const sheet = SpreadsheetApp.getActive().getSheetByName('Master');
  const lastRow = sheet.getLastRow();
  const lastCol = sheet.getLastColumn();

  sheet.getRange(1, 1, 1, lastCol)
       .setFontWeight('bold')
       .setFontColor('#ffffff')
       .setBackground('#0f5c8c');
  sheet.setFrozenRows(1);
  sheet.autoResizeColumns(1, lastCol);

  Logger.log(`formatted ${lastRow} rows and ${lastCol} columns`);
}

function cleanStatuses() {
  const sheet = SpreadsheetApp.getActive().getSheetByName('Master');
  const lastRow = sheet.getLastRow();
  const range = sheet.getRange(2, 9, lastRow - 1, 1);    // I2 down: row 2, column 9, one column
  const values = range.getValues();                      // one read

  const map = {
    'delivered': 'Delivered', 'dlvd': 'Delivered', 'cancelled': 'Cancelled',
    'canceled': 'Cancelled', 'cxl': 'Cancelled', 'shipped': 'Shipped', 'pending': 'Pending'
  };

  let unmapped = 0;
  for (let r = 0; r < values.length; r++) {
    const raw = String(values[r][0]).trim().toLowerCase();
    if (map[raw]) values[r][0] = map[raw];
    else unmapped++;
  }

  range.setValues(values);                               // one write, of column I only
  Logger.log(`${values.length} rows cleaned, ${unmapped} unmapped`);
}

function onOpen() {
  SpreadsheetApp.getUi()
    .createMenu('Riverstone')
    .addItem('Clean statuses', 'cleanStatuses')
    .addItem('Send daily summary', 'sendDailySummary')
    .addToUi();
}

/**
 * Riverstone's loyalty rebate percentage.
 * @param {number} annualValue The customer's annual net revenue.
 * @return {number} 0, 1 or 2.
 * @customfunction
 */
function REBATEPCT(annualValue) {
  if (annualValue >= 400000) return 2;
  if (annualValue >= 250000) return 1;
  return 0;
}

function escapeHtml(text) {
  return String(text)
    .replaceAll('&', '&amp;')
    .replaceAll('<', '&lt;')
    .replaceAll('>', '&gt;')
    .replaceAll('"', '&quot;');
}

function onFormSubmit(e) {
  const answers = e.namedValues;          // {'Email address': ['x@y.com'], 'Company': [...], ...}
  const email = answers['Email address'][0];
  const company = answers['Company'][0];
  const product = answers['Product'][0];
  const quantity = answers['Quantity'][0];

  const html = `
    <p>Dear ${escapeHtml(company)},</p>
    <p>Thank you for your enquiry. We have logged it and a sales executive will reply
       within one working day.</p>
    <table style="border-collapse:collapse;font-family:Arial;font-size:13px">
      <tr><td style="padding:4px 12px;color:#5b6475">Product</td>
          <td style="padding:4px 12px"><b>${escapeHtml(product)}</b></td></tr>
      <tr><td style="padding:4px 12px;color:#5b6475">Quantity</td>
          <td style="padding:4px 12px"><b>${escapeHtml(quantity)}</b></td></tr>
    </table>
    <p style="color:#5b6475;font-size:12px">
      Riverstone Supplies · this is an automatic acknowledgement.</p>`;

  MailApp.sendEmail({
    to: email,
    subject: `Riverstone: we received your enquiry (${product})`,
    htmlBody: html,
    name: 'Riverstone Supplies'
  });

  SpreadsheetApp.getActive().getSheetByName('Enquiries')
    .appendRow([new Date(), email, company, product, Number(quantity), 'acknowledged']);
}

function readEnquiries() {
  const sheet = SpreadsheetApp.getActive().getSheetByName('Enquiries');
  const rows = sheet.getDataRange().getValues().slice(1);   // every row after the header
  Logger.log(`${rows.length} enquiries in the sheet`);
  return rows;
}

function keepSince(rows, since) {
  const recent = rows.filter(r => r[0] > since);            // column 0 holds the date received
  Logger.log(`${recent.length} arrived since the last summary`);
  return recent;
}

function unitsByProduct(rows) {
  const totals = {};
  rows.forEach(r => {
    const product = r[3];
    totals[product] = (totals[product] || 0) + Number(r[4]);
  });
  Logger.log(JSON.stringify(totals));
  return totals;
}

function buildSummaryHtml(count, totals) {
  if (count === 0) {
    return '<p style="font-family:Arial">No enquiries were received since the last summary.</p>';
  }
  let tableRows = '';
  Object.keys(totals).sort().forEach(product => {
    tableRows += `<tr><td style="padding:4px 12px">${escapeHtml(product)}</td>` +
                 `<td style="padding:4px 12px;text-align:right">${totals[product]}</td></tr>`;
  });
  return `<h3 style="font-family:Arial">Enquiries since the last summary: ${count}</h3>
    <table style="border-collapse:collapse;font-family:Arial;font-size:13px">
      <tr><th style="text-align:left;padding:4px 12px">Product</th>
          <th style="text-align:right;padding:4px 12px">Units</th></tr>
      ${tableRows}
    </table>
    <p style="color:#5b6475;font-size:12px">
      Sent automatically by the Riverstone enquiries sheet.</p>`;
}

function sendDailySummary() {
  const now = new Date();
  if (now.getDay() === 0 || now.getDay() === 6) return;      // 0 is Sunday, 6 is Saturday
  const props = PropertiesService.getScriptProperties();
  const lastSent = new Date(props.getProperty('LAST_SUMMARY') || 0);

  const rows = keepSince(readEnquiries(), lastSent);
  const html = buildSummaryHtml(rows.length, unitsByProduct(rows));
  Logger.log(html);                                           // read it before it goes out

  MailApp.sendEmail({ to: 'sales.team@riverstone.example',
                      subject: 'Riverstone enquiries — daily summary',
                      htmlBody: html, name: 'Riverstone reporting' });
  props.setProperty('LAST_SUMMARY', now.toISOString());
}

function fetchOpenEnquiries() {
  const token = PropertiesService.getScriptProperties()
                                 .getProperty('CRM_TOKEN');    // not in the code
  const response = UrlFetchApp.fetch('https://crm.example.com/api/v1/enquiries?status=open', {
    method: 'get',
    headers: { Authorization: 'Bearer ' + token },
    muteHttpExceptions: true
  });

  if (response.getResponseCode() !== 200) {
    throw new Error('CRM returned ' + response.getResponseCode() + ': ' +
                    response.getContentText().slice(0, 200));
  }

  const data = JSON.parse(response.getContentText());
  const rows = data.results.map(r => [r.id, r.company, r.product, r.quantity, r.created_at]);
  const sheet = SpreadsheetApp.getActive().getSheetByName('CRM');
  sheet.getRange(2, 1, sheet.getMaxRows() - 1, 5).clearContent();   // clear the last run
  if (rows.length === 0) {
    Logger.log('no open enquiries');
    return;
  }
  sheet.getRange(2, 1, rows.length, rows[0].length).setValues(rows);
  Logger.log(`${rows.length} enquiries written`);
}
