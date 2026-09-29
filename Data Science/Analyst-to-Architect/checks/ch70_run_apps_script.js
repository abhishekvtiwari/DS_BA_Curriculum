// ch70_run_apps_script.js - runs Chapter 70's Apps Script blocks (extracted from the manuscript) in Node,
// with a small mock of SpreadsheetApp, Logger and MailApp that counts every round trip.
// Run from the book folder:  node checks/ch70_run_apps_script.js
const fs = require('fs');
const md = fs.readFileSync('manuscript/ch70-excel-google-sheets-vba-and-bi-question-bank.md', 'utf8');
const blocks = [...md.matchAll(/^```javascript\n([\s\S]*?)^```$/gm)].map(m => m[1]);
const orders = () => [
  ['order_id', 'order_date', 'customer_name', 'category', 'product_name', 'quantity', 'unit_price', 'discount_pct', 'net_revenue', 'status', ''],
  [1001, '2025-01-06', 'Sharma Hardware', 'Storage', 'Storage Box 10L', 25, 430, 5, 10212.5, 'Delivered', ''],
  [1002, '2025-01-07', 'Metro Mart', 'Kitchen', 'Water Bottle 1L', 40, 115, 0, 4600, 'Delivered', ''],
  [1003, '2025-01-09', 'Sharma Hardware', 'Storage', 'Stackable Bin', 30, 290, 5, 8265, 'Cancelled', ''],
  [1004, '2025-01-13', 'Coastal Foods', 'Industrial', 'Industrial Crate', 20, 1400, 10, 25200, 'Delivered', ''],
  [1005, '2025-01-20', 'Metro Mart', 'Storage', 'Storage Box 25L', 8, 750, 0, 6000, 'Shipped', ''],
  [1006, '2025-02-03', 'Sharma Hardware', 'Storage', 'Storage Box 10L', 12, 430, 0, 5160, 'Delivered', '']];
const confirmations = [['order_id', 'customer_name', 'email', 'status'],
  [1001, 'Sharma Hardware', 'buy@sharmahardware.example.com', ''],
  [1002, 'Metro Mart', 'orders@metromart.example.com', ''],
  [1004, 'Coastal Foods', 'purchase@coastalfoods.example.com', '']];
let calls, log, mails;
function reset() { calls = { get: 0, set: 0 }; log = []; mails = []; }
function sheetOf(g) {
  const range = (r, c, nr = 1, nc = 1) => {
    if (nr < 1) throw new Error('The number of rows in the range must be at least 1.');
    return {
      getValue: () => { calls.get++; return g[r - 1][c - 1]; },
      setValue: v => { calls.set++; g[r - 1][c - 1] = v; },
      getValues: () => { calls.get++; return g.slice(r - 1, r - 1 + nr).map(row => row.slice(c - 1, c - 1 + nc)); },
      setValues: v => { calls.set++; v.forEach((row, i) => row.forEach((x, j) => { g[r - 1 + i][c - 1 + j] = x; })); }
    };
  };
  return { getLastRow: () => g.length, getRange: range, getDataRange: () => range(1, 1, g.length, g[0].length) };
}
function load(code, sheets, names) {
  const ctx = {
    SpreadsheetApp: { getActive: () => ({ getSheetByName: n => sheets[n] }) },
    Logger: { log: x => log.push(String(x)) },
    MailApp: { sendEmail: (to, subj, body) => mails.push(to) }
  };
  return new Function(...Object.keys(ctx), code + `\nreturn {${names}};`)(...Object.values(ctx));
}
const K = g => g.slice(1).map(r => r[10]);
// Q70-052, slow then fast, each on a fresh table
let g = orders(); reset();
load(blocks[0], { Orders: sheetOf(g) }, 'markLargeSlow').markLargeSlow();
console.log('==== markLargeSlow  reads', calls.get, 'writes', calls.set, '| K:', JSON.stringify(K(g)));
g = orders(); reset();
load(blocks[1], { Orders: sheetOf(g) }, 'markLarge').markLarge();
console.log('==== markLarge      reads', calls.get, 'writes', calls.set, '| K:', JSON.stringify(K(g)), '| log:', log.join(' / '));
// the same with something already in K (row 3): the fast version must keep it, as the slow one does
for (const [i, name] of [[0, 'markLargeSlow'], [1, 'markLarge']]) {
  g = orders(); g[2][10] = 'check'; reset();
  load(blocks[i], { Orders: sheetOf(g) }, name)[name]();
  console.log(`==== ${name} with K3="check" | K:`, JSON.stringify(K(g)));
}
g = [orders()[0]]; reset();
load(blocks[1], { Orders: sheetOf(g) }, 'markLarge').markLarge();
console.log('==== markLarge on header-only sheet: ok, log', JSON.stringify(log));
// Q70-053, broken then fixed, each run twice
for (const [i, label] of [[2, 'BROKEN'], [3, 'FIXED']]) {
  const c = confirmations.map(r => r.slice());
  const f = load(blocks[i], { Confirmations: sheetOf(c) }, 'sendConfirmations');
  for (const run of [1, 2]) {
    reset(); f.sendConfirmations();
    console.log(`==== ${label} run ${run}: emails ${mails.length}`, log.length ? '| log: ' + log.join(' / ') : '');
  }
}
