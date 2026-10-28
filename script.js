// Shared chapter reader. Each HTML shell declares its own data-chapter-src.
const reader = document.querySelector('#reader');
const previous = document.querySelector('#previous');
const next = document.querySelector('#next');
const status = document.querySelector('#page-status');
const pageSelect = document.querySelector('#page-select');
const message = document.querySelector('#reader-message');
let pages = [];
let currentPage = 0;

function element(tag, className, text) {
  const node = document.createElement(tag);
  if (className) node.className = className;
  if (text !== undefined) node.textContent = text;
  return node;
}

function validateChapter(chapter) {
  if (!chapter || typeof chapter.title !== 'string' || !chapter.title.trim() ||
      !Array.isArray(chapter.pages) || !chapter.pages.length) throw Error('Invalid chapter');
  chapter.pages.forEach((page, index) => {
    if (!page || page['Page Number'] !== index + 1 || typeof page.Title !== 'string' ||
        !page.Title.trim() || !Array.isArray(page.panels) ||
        page.panels.length < 1 || page.panels.length > 7) throw Error('Invalid page');
    if (page.footer !== undefined && typeof page.footer !== 'string') throw Error('Invalid footer');
    page.panels.forEach(panel => {
      if (!panel || typeof panel.image_src !== 'string' ||
          !/^assets\/[a-zA-Z0-9_/-]+\.(png|jpe?g|webp|svg)$/.test(panel.image_src) ||
          typeof panel.caption !== 'string') throw Error('Invalid panel');
      for (const field of ['narration', 'image_alt']) {
        if (panel[field] !== undefined && typeof panel[field] !== 'string') throw Error('Invalid panel text');
      }
      if (panel.layout !== undefined && (!Array.isArray(panel.layout) ||
          panel.layout.some(name => typeof name !== 'string' || !/^[a-z][a-z0-9-]*$/.test(name)))) throw Error('Invalid panel layout');
      if (panel.full_size_link !== undefined && typeof panel.full_size_link !== 'boolean') throw Error('Invalid image link');
    });
  });
}

function renderChapter(chapter) {
  validateChapter(chapter);
  const fragment = document.createDocumentFragment();
  const options = document.createDocumentFragment();
  chapter.pages.forEach((page, index) => {
    const article = element('article', 'comic-page');
    article.id = `page-${page['Page Number']}`;
    article.hidden = true;
    article.setAttribute('aria-labelledby', `${article.id}-title`);
    const heading = element('h2', 'sr-only', `Page ${page['Page Number']}: ${page.Title}`);
    heading.id = `${article.id}-title`;
    article.append(heading);
    page.panels.forEach((panel, panelIndex) => {
      const layout = panel.layout ?? (page.panels.length % 2 && panelIndex === 0 ? ['wide'] : []);
      const box = element('div', ['panel', 'world-panel', ...layout].join(' '));
      const image = element('img', 'panel-art');
      // Paths are relative to the HTML shell, not the chapter JSON directory.
      image.src = panel.image_src;
      image.alt = panel.image_alt ?? panel.caption;
      image.loading = index === 0 ? 'eager' : 'lazy';
      image.decoding = 'async';
      if (panel.full_size_link) {
        const link = element('a', 'guard-art-link');
        link.href = panel.image_src;
        link.target = '_blank';
        link.rel = 'noopener';
        link.setAttribute('aria-label', `Open full-size illustration: ${image.alt} (opens a new tab)`);
        link.append(image);
        box.append(link);
      } else box.append(image);
      box.append(element('p', 'caption', panel.caption));
      if (panel.narration) box.append(element('p', 'world-note', panel.narration));
      article.append(box);
    });
    const footer = element('div', 'page-foot');
    footer.append(element('span', '', page.footer ?? `${chapter.title} · ${page.Title}`),
      element('span', '', String(page['Page Number']).padStart(2, '0')));
    article.append(footer);
    fragment.append(article);
    const option = element('option', '', `${page['Page Number']} — ${page.Title}`);
    option.value = String(index);
    options.append(option);
  });
  document.querySelector('#chapter-pages').replaceChildren(fragment);
  pageSelect.replaceChildren(options);
  pages = [...reader.querySelectorAll('.comic-page')];
  reader.querySelector('.reader-heading > span').textContent = chapter.title.toUpperCase();
  reader.querySelector('.edition').textContent = `${pages.length} PAGES · READ AT YOUR OWN PACE`;
  pageSelect.disabled = false;
  document.querySelector('#keyboard-hint').hidden = false;
  message.hidden = true;
  const requested = Number(new URLSearchParams(window.location.search).get('page'));
  showPage(Number.isInteger(requested) && requested >= 1 && requested <= pages.length ? requested - 1 : 0);
  if (window.location.hash === '#reader') reader.scrollIntoView({ block: 'start' });
}

function showPage(index) {
  if (!pages.length) return;
  currentPage = Math.max(0, Math.min(index, pages.length - 1));
  pages.forEach((page, number) => { page.hidden = number !== currentPage; });
  previous.disabled = currentPage === 0;
  next.disabled = currentPage === pages.length - 1;
  pageSelect.value = String(currentPage);
  status.textContent = `PAGE ${String(currentPage + 1).padStart(2, '0')} OF ${String(pages.length).padStart(2, '0')}`;
}

previous.addEventListener('click', () => showPage(currentPage - 1));
next.addEventListener('click', () => showPage(currentPage + 1));
pageSelect.addEventListener('change', () => {
  showPage(Number(pageSelect.value));
  reader.scrollIntoView({ block: 'start' });
});
document.addEventListener('keydown', event => {
  if (event.altKey || event.ctrlKey || event.metaKey || event.shiftKey ||
      event.target.closest('input, textarea, select, button, [contenteditable="true"]')) return;
  const bounds = reader.getBoundingClientRect();
  if (bounds.bottom <= 0 || bounds.top >= window.innerHeight) return;
  if (event.key === 'ArrowRight' || event.key === 'ArrowLeft') {
    event.preventDefault();
    showPage(currentPage + (event.key === 'ArrowRight' ? 1 : -1));
  }
});

async function loadChapter() {
  try {
    const response = await fetch(reader.dataset.chapterSrc, { cache: 'no-cache' });
    if (!response.ok) throw Error(`Chapter request failed: ${response.status}`);
    renderChapter(await response.json());
  } catch (error) {
    console.error('Unable to load chapter:', error);
    message.hidden = false;
    message.setAttribute('role', 'alert');
    message.textContent = 'This chapter could not be loaded. Please reload the page to try again.';
    status.textContent = 'CHAPTER UNAVAILABLE';
  } finally {
    reader.setAttribute('aria-busy', 'false');
  }
}
loadChapter();
