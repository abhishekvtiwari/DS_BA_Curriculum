// Mock of the few ExcelScript calls chapter 19 uses, over the consolidated Master grid.
const fs = require('fs');
const grid = JSON.parse(fs.readFileSync(process.env.MASTER_JSON));
function makeRange(r0, c0, nr, nc) {
  const fmt = { getFont: () => ({ setBold() {}, setColor() {} }), getFill: () => ({ setColor() {} }), autofitColumns() {} };
  return {
    getRowCount: () => nr, getColumnCount: () => nc, getFormat: () => fmt,
    getValues: () => { const out = []; for (let r = 0; r < nr; r++) { out.push(grid[r0 + r].slice(c0, c0 + nc)); } return out; },
    setValues: (v) => { for (let r = 0; r < nr; r++) for (let c = 0; c < nc; c++) grid[r0 + r][c0 + c] = v[r][c]; }
  };
}
const sheet = {
  getUsedRange: () => makeRange(0, 0, grid.length, grid[0].length),
  getRangeByIndexes: (r, c, nr, nc) => makeRange(r, c, nr, nc),
  getFreezePanes: () => ({ freezeRows(n) { sheet.frozen = n; } })
};
const workbook = { getWorksheet: (name) => name === 'Master' ? sheet : undefined };
module.exports = { workbook, sheet };
