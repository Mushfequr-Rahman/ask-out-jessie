// Run with node scripts/test_panel_layout.cjs; no dependencies required.
const assert = require('node:assert/strict');
const {fitPanels, fitImage} = require('../panel-layout.js');
for (let count = 1; count <= 5; count++) {
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
assert.throws(() => fitPanels([], 952, 1268, () => 0), /1–5/);
assert.throws(() => fitPanels(Array(6).fill({}), 952, 1268, () => 0), /1–5/);
console.log('PASS: ordered 1–5-panel layouts across mixed image ratios; canvas bounds, text space and no overlaps.');

// A five-image page gives its decisive beat substantially more space.
const priorities = [1, 1, 5, 2, 1];
const priorityPlan = fitPanels(priorities.map(priority => ({priority, aspectRatio: 1.5})), 952, 1268, () => 90);
const areas = priorityPlan.boxes.map(box => box.width * box.height);
assert(areas.every((area, i) => i === 2 || areas[2] > area * 1.5), 'Hero priority must visibly change area');
assert.deepEqual(priorityPlan.boxes.map(box => box.index), [0, 1, 2, 3, 4], 'Priority must preserve reading order');
const equalPlan = fitPanels(priorities.map(() => ({priority: 1, aspectRatio: 1.5})), 952, 1268, () => 90);
assert(areas[2] > equalPlan.boxes[2].width * equalPlan.boxes[2].height * 1.5, 'Increasing priority must enlarge the panel');
for (const priority of [0, 6, 1.5, '5', true]) assert.throws(() => fitPanels([{priority}], 952, 1268, () => 90), /1–5/);
console.log('PASS: five-image hero emphasis, priority-driven resizing, stable reading order and invalid priorities.');

for (const [sourceWidth, sourceHeight] of [[1536, 1024], [1024, 1536], [1000, 1000], [3000, 400]]) {
  for (const [boxWidth, boxHeight] of [[300, 700], [700, 200], [150, 150]]) {
    const image = fitImage(sourceWidth, sourceHeight, boxWidth, boxHeight);
    assert(Math.abs(image.width / image.height - sourceWidth / sourceHeight) < 1e-9, 'Image stretched');
    assert(image.x >= -1e-9 && image.y >= -1e-9);
    assert(image.x + image.width <= boxWidth + 1e-9 && image.y + image.height <= boxHeight + 1e-9, 'Image cropped');
    assert(Math.abs(image.x * 2 + image.width - boxWidth) < 1e-9);
    assert(Math.abs(image.y * 2 + image.height - boxHeight) < 1e-9);
    assert(Math.abs(image.width - boxWidth) < 1e-9 || Math.abs(image.height - boxHeight) < 1e-9, 'Image not maximally fitted');
  }
}
assert.throws(() => fitImage(0, 100, 100, 100), /positive/);
console.log('PASS: proportional image scaling and translation, portrait/landscape/square sources, no crop or distortion.');
