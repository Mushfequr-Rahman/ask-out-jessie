/* Ordered row packing for a fixed comic canvas. No image cropping or content reordering. */
(function (root) {
  'use strict';
  function arrangements(count, row = [], result = []) {
    if (!count) result.push(row);
    else if (row.length < 4) {
      for (let size = 1; size <= Math.min(3, count); size++) arrangements(count - size, [...row, size], result);
    }
    return result;
  }

  function fitPanels(panels, width, height, measureText, gap = 12) {
    if (!panels.length || panels.length > 7) throw Error('A comic page needs 1–7 panels');
    let best;
    for (const rows of arrangements(panels.length)) {
      let offset = 0;
      const groups = rows.map(size => {
        const items = panels.slice(offset, offset + size);
        const weights = items.map(p => Math.sqrt(Math.max(.6, Math.min(2.4, p.aspectRatio || 1.5))));
        const totalWeight = weights.reduce((sum, weight) => sum + weight, 0);
        const widths = weights.map(weight => (width - gap * (size - 1)) * weight / totalWeight);
        const texts = widths.map((w, i) => measureText(offset + i, w));
        const copy = Math.max(...texts);
        const idealImage = widths.reduce((sum, w, i) => sum + w / (items[i].aspectRatio || 1.5), 0) / size;
        const group = {offset, size, items, widths, texts, copy, idealImage, minimum: copy + 104};
        offset += size;
        return group;
      });
      const usable = height - gap * (rows.length - 1);
      const minimum = groups.reduce((sum, row) => sum + row.minimum, 0);
      if (minimum > usable) continue;
      const ideal = groups.reduce((sum, row) => sum + row.idealImage, 0);
      let y = 0, score = 0;
      const boxes = [];
      groups.forEach(row => {
        const h = row.minimum + (usable - minimum) * row.idealImage / ideal;
        let x = 0;
        row.items.forEach((panel, i) => {
          const w = row.widths[i], imageHeight = h - row.texts[i] - 4;
          const aspect = panel.aspectRatio || 1.5;
          const boxAspect = (w - 4) / imageHeight;
          const fill = Math.min(aspect / boxAspect, boxAspect / aspect);
          score += (1 - fill) * w * imageHeight;
          // Reward usable images; discourage very narrow, text-heavy columns.
          score += Math.max(0, 240 - w) * 500 + Math.max(0, 170 - imageHeight) * 350;
          boxes.push({index: row.offset + i, x, y, width: w, height: h, copyHeight: row.texts[i]});
          x += w + gap;
        });
        y += h + gap;
      });
      if (!best || score < best.score) best = {score, boxes, rows};
    }
    return best ?? null;
  }
  root.ComicLayout = {fitPanels};
  if (typeof module !== 'undefined' && module.exports) module.exports = {fitPanels};
})(typeof window === 'undefined' ? globalThis : window);
