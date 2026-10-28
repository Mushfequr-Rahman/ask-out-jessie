// Browser-local authoring decisions; export is validated against image/reference hashes.
(async () => {
  const status = document.querySelector('#status');
  const response = await fetch('banner-review.json');
  if (!response.ok) throw Error('Cannot load banner review data');
  const data = await response.json();
  const key = `magneton-banner-review:${data.revision}`;
  let decisions = {};
  try { decisions = JSON.parse(localStorage.getItem(key) || '{}'); }
  catch { document.querySelector('#storage-message').textContent = 'Local storage unavailable. Keep this page open and export your decisions.'; }
  const cards = [...document.querySelectorAll('.review-card')];
  function update() {
    const counts = {pending: 0, pass: 0, fix: 0, not_visible: 0};
    for (const card of cards) counts[card.querySelector('select').value]++;
    status.textContent = `${counts.pending} pending · ${counts.pass} match · ${counts.fix} need correction · ${counts.not_visible} not visible`;
  }
  for (const card of cards) {
    const select = card.querySelector('select'), notes = card.querySelector('textarea');
    const saved = decisions[card.dataset.key];
    if (saved && ['pending', 'pass', 'fix', 'not_visible'].includes(saved.status)) {
      select.value = saved.status; notes.value = saved.notes || '';
    }
    card.dataset.decision = select.value;
    card.addEventListener('input', () => {
      decisions[card.dataset.key] = {status: select.value, notes: notes.value};
      card.dataset.decision = select.value;
      try { localStorage.setItem(key, JSON.stringify(decisions)); }
      catch { document.querySelector('#storage-message').textContent = 'Local storage unavailable; export before closing this page.'; }
      update();
    });
  }
  document.querySelector('#export').addEventListener('click', () => {
    const entries = data.houses.flatMap(house => house.panels.map(panel => ({
      banner_id: house.id, scene_id: panel.id, image_sha256: panel.sha256,
      reference_sha256: house.reference_sha256,
      ...(decisions[`${house.id}:${panel.id}`] || {status: 'pending', notes: ''})
    })));
    const report = {schema_version: 1, revision: data.revision, exported_at: new Date().toISOString(), entries};
    const url = URL.createObjectURL(new Blob([JSON.stringify(report, null, 2)+'\n'], {type: 'application/json'}));
    const link = document.createElement('a'); link.href = url; link.download = 'banner-review-decisions.json'; link.click();
    setTimeout(() => URL.revokeObjectURL(url), 1000);
  });
  update();
})().catch(error => { document.querySelector('#status').textContent = `Review unavailable: ${error.message}`; });
