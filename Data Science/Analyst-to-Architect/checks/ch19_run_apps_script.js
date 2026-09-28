// Runs chapter 19's Apps Script blocks (extracted from the manuscript) in Node with small mocks
// of SpreadsheetApp, Logger, MailApp and PropertiesService. Run with TZ=Asia/Kolkata.
const fs = require('fs');
const md = fs.readFileSync(process.env.BOOK + '/manuscript/ch19-spreadsheet-automation.md', 'utf8');
const code = [...md.matchAll(/^```javascript\n([\s\S]*?)^```$/gm)].map(m => m[1]).join('\n');
const RealDate = Date; let fakeNow = null;
class FakeDate extends RealDate { constructor(...a) { if (a.length === 0 && fakeNow) super(fakeNow); else super(...a); } }
const grid = JSON.parse(fs.readFileSync(process.env.MASTER_JSON));
const enquiries = [['received', 'email', 'company', 'product', 'quantity', 'status']];
function sheetOf(g) {
  const range = (r, c, nr, nc) => ({
    getValues: () => g.slice(r - 1, r - 1 + nr).map(row => row.slice(c - 1, c - 1 + nc)),
    setValues: v => { v.forEach((row, i) => row.forEach((x, j) => { g[r - 1 + i][c - 1 + j] = x; })); },
    setFontWeight() { return this; }, setFontColor() { return this; }, setBackground() { return this; },
    clearContent() { return this; }
  });
  return {
    getLastRow: () => g.length, getLastColumn: () => g[0].length, getMaxRows: () => Math.max(1000, g.length),
    getRange: range, getDataRange: () => range(1, 1, g.length, g[0].length),
    setFrozenRows() {}, autoResizeColumns() {}, appendRow: row => g.push(row)
  };
}
const sheets = { Master: sheetOf(grid), Enquiries: sheetOf(enquiries) };
const log = [], mails = []; const store = {};
const ctx = {
  SpreadsheetApp: { getActive: () => ({ getSheetByName: n => sheets[n] }) },
  Logger: { log: x => log.push(String(x)) },
  MailApp: { sendEmail: o => mails.push(o) },
  PropertiesService: { getScriptProperties: () => ({ getProperty: k => (k in store ? store[k] : null), setProperty: (k, v) => { store[k] = v; } }) },
  Date: FakeDate
};
const fn = new Function(...Object.keys(ctx), code + '\nreturn {formatMaster, cleanStatuses, escapeHtml, onFormSubmit, sendDailySummary, REBATEPCT};');
const f = fn(...Object.values(ctx));
function show(title) { console.log('==== ' + title); log.forEach(l => console.log(l)); log.length = 0; }
f.formatMaster(); show('formatMaster');
f.cleanStatuses(); show('cleanStatuses');
console.log('==== escapeHtml\n' + f.escapeHtml('Tools & <Co>'));
console.log('==== REBATEPCT ' + [180000, 250000, 399999, 400000].map(f.REBATEPCT).join(' '));
// the form: submit each sample row at its own time
const csv = fs.readFileSync(process.env.BOOK + '/companion/ch19/enquiries_sample.csv', 'utf8').trim().split('\n');
const head = csv[0].split(',');
const subs = csv.slice(1).map(l => { const v = l.split(','); const o = {}; head.forEach((h, i) => o[h] = [v[i]]); return o; });
function at(s) { return new RealDate(s.replace(' ', 'T') + '+05:30'); }
// Friday's 9 a.m. summary has already gone out
store['LAST_SUMMARY'] = at('2026-01-02 09:00:00').toISOString();
subs.slice(0, 3).forEach(o => { fakeNow = at(o['Timestamp'][0]); f.onFormSubmit({ namedValues: o }); });
console.log('==== first acknowledgement'); console.log(JSON.stringify({ to: mails[0].to, subject: mails[0].subject, name: mails[0].name }));
console.log(mails[0].htmlBody);
fakeNow = at('2026-01-05 09:00:00'); mails.length = 0;
f.sendDailySummary(); show('sendDailySummary Monday 5 Jan 09:00');
console.log('==== mail to', mails[0] && mails[0].to, '| LAST_SUMMARY now', store['LAST_SUMMARY']);
subs.slice(3).forEach(o => { fakeNow = at(o['Timestamp'][0]); f.onFormSubmit({ namedValues: o }); });
console.log('==== Enquiries sheet'); enquiries.forEach(r => console.log(r.map(x => x instanceof RealDate ? x.toString() : x).join(' | ')));
fakeNow = at('2026-01-06 09:00:00'); mails.length = 0;
f.sendDailySummary(); show('sendDailySummary Tuesday 6 Jan 09:00');
fakeNow = at('2026-01-10 09:00:00'); mails.length = 0;
f.sendDailySummary(); show('sendDailySummary Saturday 10 Jan (should do nothing)'); console.log('mails sent:', mails.length);
