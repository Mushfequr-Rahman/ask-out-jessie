/* Priority-weighted comic rows. Panels keep their left-to-right, top-to-bottom order. */
(function (root) {
  'use strict';
  function arrangements(count, row = [], result = []) {
    if (!count) result.push(row);
    else if (row.length < 4) {
      for (let size = 1; size <= Math.min(3, count); size++) arrangements(count - size, [...row, size], result);
    }
    return result;
  }
  function distribute(total, minimums, weights) {
    if (minimums.reduce((sum, value) => sum + value, 0) > total) return null;
    const values = minimums.slice();
    let active = weights.map((_, index) => index), remaining = total;
    while (active.length) {
      const sum = active.reduce((sum, i) => sum + weights[i], 0);
      const constrained = active.filter(i => remaining * weights[i] / sum < minimums[i]);
      if (!constrained.length) {
        active.forEach(i => { values[i] = remaining * weights[i] / sum; });
        break;
      }
      constrained.forEach(i => { remaining -= values[i]; });
      active = active.filter(i => !constrained.includes(i));
    }
    return values;
  }
  function fitPanels(panels, width, height, measureText, gap = 10) {
    if (!panels.length || panels.length > 7) throw Error('A comic page needs 1–7 panels');
    const priorities = panels.map(panel => panel.priority ?? 3);
    if (priorities.some(p => !Number.isInteger(p) || p < 1 || p > 5)) throw Error('Priority must be 1–5');
    const weights = priorities.map(priority => Math.pow(priority, 1.65));
    const totalWeight = weights.reduce((sum, value) => sum + value, 0);
    let best;
    for (const rows of arrangements(panels.length)) {
      let offset = 0;
      const groups = rows.map(size => {
        const indexes = Array.from({length: size}, (_, i) => offset + i);
        const widths = distribute(width - gap * (size - 1), indexes.map(() => 215), indexes.map(i => weights[i]));
        const texts = widths.map((w, i) => measureText(offset + i, w));
        const row = {indexes, widths, texts, weight: indexes.reduce((sum, i) => sum + weights[i], 0),
          minimum: Math.max(185, ...texts.map(h => h + 92))};
        offset += size;
        return row;
      });
      const heights = distribute(height - gap * (rows.length - 1), groups.map(row => row.minimum), groups.map(row => row.weight));
      if (!heights) continue;
      const boxes = [];
      let y = 0;
      groups.forEach((row, rowIndex) => {
        let x = 0;
        row.indexes.forEach((index, column) => {
          boxes.push({index, x, y, width: row.widths[column], height: heights[rowIndex], copyHeight: row.texts[column]});
          x += row.widths[column] + gap;
        });
        y += heights[rowIndex] + gap;
      });
      const area = boxes.reduce((sum, box) => sum + box.width * box.height, 0);
      let score = 0;
      for (const box of boxes) {
        const share = box.width * box.height / area, target = weights[box.index] / totalWeight;
        // The story's priority drives area, rather than fitting every image into equal cards.
        score += 14 * (share - target) ** 2 / target;
        const aspect = panels[box.index].aspectRatio || 1.5, frame = box.width / box.height;
        score += 2.4 * target * (1 - Math.min(aspect / frame, frame / aspect));
        score += Math.max(0, 235 - box.width) / width;
        for (const other of boxes) {
          if (priorities[box.index] > priorities[other.index] && box.width * box.height < other.width * other.height) {
            score += 30 * (other.width * other.height - box.width * box.height) / area;
          }
        }
      }
      if (!best || score < best.score) best = {score, boxes, rows};
    }
    return best ?? null;
  }
  root.ComicLayout = {fitPanels};
  if (typeof module !== 'undefined' && module.exports) module.exports = {fitPanels};
})(typeof window === 'undefined' ? globalThis : window);
