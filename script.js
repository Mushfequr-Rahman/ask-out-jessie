const pages = [...document.querySelectorAll('.comic-page')];
const previous = document.querySelector('#previous');
const next = document.querySelector('#next');
const status = document.querySelector('#page-status');
let currentPage = 0;

function showPage(index) {
  currentPage = Math.max(0, Math.min(index, pages.length - 1));
  pages.forEach((page, number) => { page.hidden = number !== currentPage; });
  previous.disabled = currentPage === 0;
  next.disabled = currentPage === pages.length - 1;
  status.textContent = `PAGE ${String(currentPage + 1).padStart(2, '0')} OF ${String(pages.length).padStart(2, '0')}`;
}

previous.addEventListener('click', () => showPage(currentPage - 1));
next.addEventListener('click', () => showPage(currentPage + 1));
document.addEventListener('keydown', (event) => {
  if (event.altKey || event.ctrlKey || event.metaKey || event.shiftKey ||
      event.target.closest('input, textarea, select, [contenteditable="true"]')) return;
  // Only turn pages while the reader is in view.
  const bounds = document.querySelector('#reader').getBoundingClientRect();
  if (bounds.bottom <= 0 || bounds.top >= window.innerHeight) return;
  if (event.key === 'ArrowRight' || event.key === 'ArrowLeft') {
    event.preventDefault();
    showPage(currentPage + (event.key === 'ArrowRight' ? 1 : -1));
  }
});
document.querySelector('#keyboard-hint').hidden = false;

// Chapter links open the requested page before the reader anchor is followed.
document.querySelectorAll('[data-reader-page]').forEach((link) => {
  link.addEventListener('click', () => showPage(Number(link.dataset.readerPage)));
});
const requestedPage = Number(new URLSearchParams(window.location.search).get('page'));
if (Number.isInteger(requestedPage) && requestedPage >= 1 && requestedPage <= pages.length) {
  showPage(requestedPage - 1);
}
