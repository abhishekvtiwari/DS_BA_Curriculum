// Analyst to Architect, Chapter 19 — Google Apps Script for Sheets.
// Paste into Extensions > Apps Script. Set CRM_TOKEN in Project Settings > Script Properties.

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

  Logger.log('formatted %s rows and %s columns', lastRow, lastCol);
}


function cleanStatuses() {
  const sheet = SpreadsheetApp.getActive().getSheetByName('Master');
  const range = sheet.getDataRange();
  const values = range.getValues();                    // one read

  const map = {
    'delivered': 'Delivered', 'dlvd': 'Delivered', 'cancelled': 'Cancelled',
    'canceled': 'Cancelled', 'cxl': 'Cancelled', 'shipped': 'Shipped', 'pending': 'Pending'
  };

  let unmapped = 0;
  for (let r = 1; r < values.length; r++) {
    const raw = String(values[r][8]).trim().toLowerCase();
    if (map[raw]) values[r][8] = map[raw];
    else unmapped++;
  }

  range.setValues(values);                             // one write
  Logger.log('%s rows cleaned, %s unmapped', values.length - 1, unmapped);
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


function onFormSubmit(e) {
  const row = e.namedValues;                          // {'Email address': ['x@y.com'], ...}
  const email = row['Email address'][0];
  const company = row['Company'][0];
  const product = row['Product'][0];
  const quantity = row['Quantity'][0];

  const html = `
    <p>Dear ${company},</p>
    <p>Thank you for your enquiry. We have logged it and a sales executive will reply within one working day.</p>
    <table style="border-collapse:collapse;font-family:Arial;font-size:13px">
      <tr><td style="padding:4px 12px;color:#5b6475">Product</td><td style="padding:4px 12px"><b>${product}</b></td></tr>
      <tr><td style="padding:4px 12px;color:#5b6475">Quantity</td><td style="padding:4px 12px"><b>${quantity}</b></td></tr>
    </table>
    <p style="color:#5b6475;font-size:12px">Riverstone Supplies · this is an automatic acknowledgement.</p>`;

  MailApp.sendEmail({
    to: email,
    subject: `Riverstone: we received your enquiry (${product})`,
    htmlBody: html,
    name: 'Riverstone Supplies'
  });

  SpreadsheetApp.getActive().getSheetByName('Enquiries')
    .appendRow([new Date(), email, company, product, quantity, 'acknowledged']);
}


function sendDailySummary() {
  const sheet = SpreadsheetApp.getActive().getSheetByName('Enquiries');
  const values = sheet.getDataRange().getValues().slice(1);

  const yesterday = new Date(); yesterday.setDate(yesterday.getDate() - 1);
  const isYesterday = (d) => new Date(d).toDateString() === yesterday.toDateString();
  const rows = values.filter(r => isYesterday(r[0]));

  const byProduct = {};
  rows.forEach(r => { byProduct[r[3]] = (byProduct[r[3]] || 0) + Number(r[4]); });

  const tableRows = Object.keys(byProduct).sort()
    .map(p => `<tr><td style="padding:4px 12px">${p}</td>
                   <td style="padding:4px 12px;text-align:right">${byProduct[p].toLocaleString('en-IN')}</td></tr>`)
    .join('');

  const html = `
    <h3 style="font-family:Arial">Enquiries yesterday: ${rows.length}</h3>
    ${rows.length === 0 ? '<p>No enquiries were received.</p>' :
      `<table style="border-collapse:collapse;font-family:Arial;font-size:13px">
         <tr><th style="text-align:left;padding:4px 12px;border-bottom:1px solid #c9d3df">Product</th>
             <th style="text-align:right;padding:4px 12px;border-bottom:1px solid #c9d3df">Units</th></tr>
         ${tableRows}
       </table>`}
    <p style="color:#5b6475;font-size:12px">Sent automatically at ${new Date().toLocaleString('en-IN')}.</p>`;

  MailApp.sendEmail({ to: 'sales.team@riverstone.example', subject: 'Riverstone enquiries — daily summary',
                      htmlBody: html, name: 'Riverstone reporting' });
}


function fetchOpenEnquiries() {
  const token = PropertiesService.getScriptProperties().getProperty('CRM_TOKEN');  // not in the code
  const response = UrlFetchApp.fetch('https://crm.example.com/api/v1/enquiries?status=open', {
    method: 'get',
    headers: { Authorization: 'Bearer ' + token },
    muteHttpExceptions: true
  });

  if (response.getResponseCode() !== 200) {
    throw new Error('CRM returned ' + response.getResponseCode() + ': ' + response.getContentText().slice(0, 200));
  }

  const data = JSON.parse(response.getContentText());
  const rows = data.results.map(r => [r.id, r.company, r.product, r.quantity, r.created_at]);
  const sheet = SpreadsheetApp.getActive().getSheetByName('CRM');
  sheet.getRange(2, 1, rows.length, rows[0].length).setValues(rows);
  Logger.log('%s enquiries written', rows.length);
}
