// Print-layout pass, run in the page before Chromium prints it (tools/pdf/build.py).
// Everything here measures the laid-out page, so it adapts to each block's real width.
// Themes from the visual review: V7 (page breaks), V8 (code wrapping), V10 (tables), V12 (scale).
(() => {
  const PT = 96 / 72;                          // CSS px per point
  const PAGE_H = (297 - 20 - 22) * 96 / 25.4;  // printable height in px (A4 minus @page margins)
  const MIN_CODE_PT = 7.0;                     // smallest code size allowed (print minimum)
  const report = { shrunk: 0, wrappedLines: 0, kept: 0, numCols: 0, overflow: [] };

  // ---- titles: a hyphenated word in a heading never breaks at its hyphen (V61.9 "Trade-/offs")
  for (const hd of document.querySelectorAll('h1, h2, h3')) {
    const walker = document.createTreeWalker(hd, NodeFilter.SHOW_TEXT); const nodes = [];
    while (walker.nextNode()) nodes.push(walker.currentNode);
    for (const n of nodes) {
      if (!/\w-\w/.test(n.textContent) || n.parentElement.closest('code')) continue;
      const span = document.createElement('span');
      span.innerHTML = n.textContent.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/(\S*\w-\w\S*)/g, '<span class="nobr">$1</span>');
      n.replaceWith(...span.childNodes);
    }
  }

  // ---- V8: code blocks. One span per source line; shrink to fit, else hang-indent and mark.
  for (const pre of document.querySelectorAll('pre')) {
    const code = pre.querySelector('code') || pre;
    let lines = [...code.children].filter(e => e.tagName === 'SPAN' && /^cb\d+-\d+$/.test(e.id));
    if (lines.length) {                                    // highlighted block: spans are the lines
      for (const n of [...code.childNodes]) if (n.nodeType === 3) n.remove();   // drop the "\n"s
    } else {                                               // plain block: build the spans
      const text = code.textContent.replace(/\n$/, '');
      code.textContent = '';
      for (const t of text.split('\n')) {
        const s = document.createElement('span');
        s.textContent = t.length ? t : '​';
        code.appendChild(s);
      }
      lines = [...code.children];
    }
    lines.forEach(s => s.classList.add('ln'));
    pre.classList.add('lines');
    // Shrink the font (not below MIN_CODE_PT) until the longest line fits without wrapping.
    pre.style.whiteSpace = 'pre';
    let size = parseFloat(getComputedStyle(pre).fontSize) / PT;
    while (pre.scrollWidth > pre.clientWidth + 1 && size > MIN_CODE_PT) {
      size = Math.max(MIN_CODE_PT, size - 0.1);
      pre.style.fontSize = size.toFixed(2) + 'pt';
      report.shrunk++;
    }
    pre.style.whiteSpace = '';
    // Lines still too long wrap with a hanging indent (CSS) and get a continuation mark.
    const lh = parseFloat(getComputedStyle(pre).lineHeight);
    for (const s of lines) if (s.getBoundingClientRect().height > lh * 1.5) { s.classList.add('wrapped'); report.wrappedLines++; }
    // Short blocks stay whole; long ones may split across pages (avoids half-empty pages).
    pre.classList.add(pre.getBoundingClientRect().height < PAGE_H * 0.45 ? 'keep' : 'split');
  }

  // ---- V10: tables. Right-align numeric columns, keep short tables whole, no wraps in short code.
  const NUM = /^[\s(]*[-−+]?[₹$€£]?\s?[-−+]?\d[\d,]*(\.\d+)?\s?(%|pp|x|×|h|hours?|days?|ms|s|GB|MB|TB|k|K|M|L| lakh| crore)?[)\s]*$/;
  for (const table of document.querySelectorAll('table')) {
    const rows = [...table.querySelectorAll('tbody tr')];
    const ncol = Math.max(0, ...rows.map(r => r.children.length));
    for (let c = 0; c < ncol; c++) {
      const cells = rows.map(r => r.children[c]).filter(td => td && td.textContent.trim() !== '' && td.textContent.trim() !== '—');
      if (cells.length >= 2 && cells.filter(td => NUM.test(td.textContent.trim())).length / cells.length >= 0.8) {
        cells.concat(rows.map(r => r.children[c]).filter(Boolean)).forEach(td => td.classList.add('num'));
        const th = table.querySelectorAll('thead th')[c]; if (th) th.classList.add('num');
        report.numCols++;
      }
    }
    for (const cd of table.querySelectorAll('td code, th code')) if (cd.textContent.length <= 24) cd.classList.add('nowrap');
    if (table.getBoundingClientRect().height < PAGE_H * 0.4) table.classList.add('keep');
  }

  // ---- V7: keep headings, short lead-ins and answer numbers with what follows.
  const isBlock = e => e && /^(PRE|TABLE|UL|OL|BLOCKQUOTE|P|DIV|FIGURE|H[2-6])$/.test(e.tagName);
  const h = e => e.getBoundingClientRect().height;
  const leadIn = p => p && p.tagName === 'P' && (/[:：]\s*$/.test(p.textContent) || p.textContent.trim().length < 60);
  const isFig = e => e && e.tagName === 'P' && e.querySelector(':scope > img');
  const isCaption = e => e && e.tagName === 'P' && e.children.length === 1 && e.firstElementChild.tagName === 'EM' && e.textContent.trim() === e.firstElementChild.textContent.trim();
  const withCaption = els => { const last = els[els.length - 1]; if (isFig(last) && isCaption(last.nextElementSibling)) els.push(last.nextElementSibling); return els; };
  const wrap = els => { const d = document.createElement('div'); d.className = 'keep-together'; els[0].before(d); els.forEach(e => d.appendChild(e)); report.kept++; };
  // headings: take the heading, an optional lead-in paragraph, and the first block after it
  for (const hd of [...document.querySelectorAll('h2, h3, h4')]) {
    if (!hd.parentElement || hd.closest('nav')) continue;
    const group = [hd];
    let n = hd.nextElementSibling;
    if (n && leadIn(n) && isBlock(n.nextElementSibling)) { group.push(n); n = n.nextElementSibling; }
    if (isBlock(n) && !/^H/.test(n.tagName)) group.push(n);
    const total = group.reduce((a, e) => a + h(e), 0);
    withCaption(group);
    if (group.length > 1) {
      if (total < PAGE_H * 0.45) wrap(group);
      else if (group.length > 2 && h(group[0]) + h(group[1]) < PAGE_H * 0.3) wrap(group.slice(0, 2));
    }
  }
  // lead-in paragraphs and bare answer numbers elsewhere
  for (const p of [...document.querySelectorAll('p')]) {
    if (p.closest('.keep-together') || !leadIn(p)) continue;
    const n = p.nextElementSibling;
    const grp = withCaption([p, n].filter(Boolean));
    if (n && (/^(PRE|TABLE|UL|OL|BLOCKQUOTE|DIV)$/.test(n.tagName) || isFig(n)) && grp.reduce((a, e) => a + h(e), 0) < PAGE_H * 0.45) wrap(grp);
  }

  // every figure stays with its caption
  for (const f of [...document.querySelectorAll('p > img')].map(i => i.parentElement)) {
    if (!f.closest('.keep-together') && isCaption(f.nextElementSibling)) wrap([f, f.nextElementSibling]);
  }

  // a section rule directly before a heading is redundant (h2 has its own rule) and can end up
  // alone at the top of a page (V24.16, V27.14, V61.10, V75.6, V79.6): drop it
  for (const hr of [...document.querySelectorAll('hr')]) {
    const n = hr.nextElementSibling;
    if (n && (/^H[1-4]$/.test(n.tagName) || (n.classList.contains('keep-together') && /^H[1-4]$/.test(n.firstElementChild.tagName)))) hr.remove();
  }
  // empty output boxes (V46.5)
  for (const pre of [...document.querySelectorAll('pre')]) if (!pre.textContent.replace(/\u200b/g, '').trim()) pre.remove();

  // ---- V12: nothing may be wider than the text block, or Chromium shrinks the whole chapter.
  const W = document.body.clientWidth;
  for (const e of document.querySelectorAll('body *'))
    if (e.getBoundingClientRect().right > W + 2 && !e.closest('.lines .ln'))
      report.overflow.push(e.tagName + ': ' + e.textContent.trim().slice(0, 60));
  report.overflow = report.overflow.slice(0, 10);
  return report;
})();
