// Run with node scripts/test_panel_layout.cjs; no dependencies required.
const assert = require('node:assert/strict');
const {fitPanels} = require('../panel-layout.js');
for (let count = 1; count <= 7; count++) {
  for (const ratios of [[1.5], [.55, 2.8, 1, 1.8], [3, .5, .75, 2]]) {
    const panels = Array.from({length: count}, (_, i) => ({aspectRatio: ratios[i % ratios.length]}));
    const plan = fitPanels(panels, 952, 1268, (index, width) => 35 + Math.ceil((index + 1) * 140 / width) * 21);
    assert(plan, `No layout for ${count} panels`);
    assert.deepEqual(plan.boxes.map(box => box.index), panels.map((_, i) => i));
    for (const box of plan.boxes) {
      assert(box.x >= 0 && box.y >= 0 && box.width > 0 && box.height > box.copyHeight);
      assert(box.x + box.width <= 952.001 && box.y + box.height <= 1268.001);
    }
    for (let i = 0; i < count; i++) for (let j = i + 1; j < count; j++) {
      const a = plan.boxes[i], b = plan.boxes[j];
      assert(a.x + a.width <= b.x + .001 || b.x + b.width <= a.x + .001 ||
        a.y + a.height <= b.y + .001 || b.y + b.height <= a.y + .001, 'Panels overlap');
    }
  }
}
assert.throws(() => fitPanels([], 952, 1268, () => 0), /1–7/);
assert.throws(() => fitPanels(Array(8).fill({}), 952, 1268, () => 0), /1–7/);
console.log('PASS: ordered 1–7-panel layouts across mixed image ratios; canvas bounds, text space and no overlaps.');
