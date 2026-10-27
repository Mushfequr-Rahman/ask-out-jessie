const filters = [...document.querySelectorAll('[data-filter]')];
const groups = [...document.querySelectorAll('[data-ship-type]')];
const count = document.querySelector('#design-count');
const designs = [...document.querySelectorAll('.comparison-ship')];

function filterShips(type) {
  groups.forEach((item) => {
    item.hidden = type !== 'all' && item.dataset.shipType !== type;
  });
  filters.forEach((button) => {
    button.setAttribute('aria-pressed', String(button.dataset.filter === type));
  });
  const visible = designs.filter((design) => !design.hidden).length;
  count.textContent = `${visible} of ${designs.length} designs`;
}

filters.forEach((button) => {
  button.addEventListener('click', () => filterShips(button.dataset.filter));
});
// All six designs remain visible when JavaScript is unavailable.
document.querySelector('.fleet-filters').hidden = false;
