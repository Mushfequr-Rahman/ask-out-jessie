// Shared chapter reader. Each HTML shell declares its own data-chapter-src.
const reader = document.querySelector('#reader');
const previous = document.querySelector('#previous');
const next = document.querySelector('#next');
const status = document.querySelector('#page-status');
const pageSelect = document.querySelector('#page-select');
const message = document.querySelector('#reader-message');
const viewSelect = document.querySelector('#page-view');
const transcript = document.querySelector('#page-transcript-content');
const chapterData = [];
const CANVAS = {width: 1000, height: 1400, panelWidth: 952, panelHeight: 1268};
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
        page.panels.length < 1 || page.panels.length > 5) throw Error('Invalid page');
    if (page.footer !== undefined && typeof page.footer !== 'string') throw Error('Invalid footer');
    page.panels.forEach(panel => {
      if (!panel || typeof panel.image_src !== 'string' ||
          !/^assets\/[a-zA-Z0-9_/-]+\.(png|jpe?g|webp|svg)$/.test(panel.image_src) ||
          typeof panel.caption !== 'string') throw Error('Invalid panel');
      if (panel.lettering_mode !== undefined && !['baked', 'editable_html'].includes(panel.lettering_mode)) throw Error('Invalid lettering mode');
      if (panel.holder !== undefined && (!['x','y','width','height'].every(k => typeof panel.holder[k] === 'number' && Number.isFinite(panel.holder[k])) || panel.holder.x < 0 || panel.holder.y < 0 || panel.holder.width <= 0 || panel.holder.height <= 0 || panel.holder.x + panel.holder.width > CANVAS.panelWidth + .01 || panel.holder.y + panel.holder.height > CANVAS.panelHeight + .01)) throw Error('Invalid fixed holder');
      if (page.layout_mode === 'fixed' && !panel.holder) throw Error('Fixed page needs holders');
      if (panel.priority !== undefined && (!Number.isInteger(panel.priority) || panel.priority < 1 || panel.priority > 5)) throw Error('Priority must be 1–5');
      if (panel.image_fit !== undefined && panel.image_fit !== 'contain') throw Error('Invalid image fit');
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
    heading.className = 'canvas-title';
    article.append(heading);
    const grid = element('div', 'panel-grid');
    page.panels.forEach(panel => {
      const box = element('div', 'page-panel');
      box.dataset.priority = String(panel.priority ?? 3);
      box.dataset.lettering = panel.lettering_mode ?? 'editable_html';
      if (panel.holder) box.dataset.holder = JSON.stringify(panel.holder);
      const image = element('img', 'panel-art');
      image.src = panel.image_src;
      image.alt = panel.image_alt ?? panel.caption;
      image.style.objectFit = 'contain';
      image.loading = index === 0 ? 'eager' : 'lazy';
      image.decoding = 'async';
      image.addEventListener('load', () => {
        if (!article.hidden) layoutPage(article);
      });
      const link = element('a', 'panel-illustration');
      link.href = panel.image_src;
      link.target = '_blank';
      link.rel = 'noopener';
      link.setAttribute('aria-label', `Open full-size illustration: ${image.alt} (opens a new tab)`);
      link.append(image);
      const copy = element('div', 'panel-copy');
      copy.hidden = panel.lettering_mode === 'baked';
      if (panel.caption) copy.append(element('p', 'panel-caption', panel.caption));
      if (panel.narration) {
        const story = element('div', 'panel-story');
        panel.narration.split('\n').filter(Boolean).forEach(line => {
          const narration = element('p', 'panel-narration', line);
          if (/^[^:\n]{1,35}: [“"]/.test(line) || /^“/.test(line)) narration.classList.add('dialogue-bubble');
          story.append(narration);
        });
        copy.append(story);
      }
      box.append(link, copy);
      grid.append(box);
    });
    article.append(grid);
    const footer = element('div', 'page-foot');
    footer.append(element('span', '', page.footer ?? `${chapter.title} · ${page.Title}`),
      element('span', '', String(page['Page Number']).padStart(2, '0')));
    article.append(footer);
    const viewport = element('div', 'page-viewport');
    const frame = element('div', 'page-frame');
    frame.append(article);
    viewport.append(frame);
    viewport.hidden = true;
    fragment.append(viewport);
    chapterData.push(page);
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
  pages.forEach((page, number) => {
    page.hidden = number !== currentPage;
    page.closest('.page-viewport').hidden = number !== currentPage;
  });
  layoutPage(pages[currentPage]);
  renderTranscript(chapterData[currentPage]);
  previous.disabled = currentPage === 0;
  next.disabled = currentPage === pages.length - 1;
  pageSelect.value = String(currentPage);
  status.textContent = `PAGE ${String(currentPage + 1).padStart(2, '0')} OF ${String(pages.length).padStart(2, '0')}`;
}

function layoutPage(article) {
  if (article.hidden) return;
  const boxes = [...article.querySelectorAll('.page-panel')];
  if (boxes.every(box => box.dataset.holder)) {
    boxes.forEach(box => {
      const h = JSON.parse(box.dataset.holder);
      Object.assign(box.style, {left: `${h.x}px`, top: `${h.y}px`, width: `${h.width}px`, height: `${h.height}px`});
      fitPanelImage(box);
    });
    article.dataset.layout = 'fixed';
    scalePage(article);
    return;
  }
  const panels = boxes.map(box => {
    const img = box.querySelector('img');
    return {aspectRatio: img.naturalWidth && img.naturalHeight ? img.naturalWidth / img.naturalHeight : 1.5, priority: Number(box.dataset.priority)};
  });
  let plan;
  for (const fontSize of [16, 15, 14, 13, 12]) {
    article.style.setProperty('--copy-size', `${fontSize}px`);
    const cache = new Map();
    plan = ComicLayout.fitPanels(panels, CANVAS.panelWidth, CANVAS.panelHeight, (index, width) => {
      const key = `${index}:${width.toFixed(2)}`;
      if (!cache.has(key)) {
        const copy = boxes[index].querySelector('.panel-copy').cloneNode(true);
        copy.classList.add('copy-measure');
        copy.style.width = `${width - 28}px`;
        copy.style.maxHeight = 'none';
        article.append(copy);
        cache.set(key, Math.ceil(copy.getBoundingClientRect().height / currentScale(article)));
        copy.remove();
      }
      return cache.get(key);
    });
    if (plan) break;
  }
  if (!plan) {
    // Extremely long author text remains available in the page transcript.
    plan = ComicLayout.fitPanels(panels, CANVAS.panelWidth, CANVAS.panelHeight, () => 220);
  }
  plan.boxes.forEach(({index, x, y, width, height}) => {
    const box = boxes[index];
    Object.assign(box.style, {left: `${x}px`, top: `${y}px`, width: `${width}px`, height: `${height}px`});
    box.querySelector('.panel-copy').style.maxHeight = `${height - 28}px`;
    fitPanelImage(box);
  });
  article.dataset.rows = plan.rows.join('-');
  scalePage(article);
}

function fitPanelImage(box) {
  const image = box.querySelector('img');
  if (box.dataset.lettering === 'baked') {
    // The artwork was generated for this immutable aperture, including its lettering.
    Object.assign(image.style, {width: '100%', height: '100%', transform: 'none', objectFit: 'cover'});
    return;
  }
  const illustration = box.querySelector('.panel-illustration');
  const caption = box.querySelector('.panel-caption');
  const story = box.querySelector('.panel-story');
  // Leave the text overlays in the panel, but keep them off the actual artwork.
  const top = caption ? caption.offsetHeight + 20 : 8;
  const bottom = story ? story.offsetHeight + 24 : 8;
  const fitted = ComicLayout.fitImage(image.naturalWidth || 1500, image.naturalHeight || 1000,
    Math.max(1, illustration.clientWidth - 16), Math.max(1, illustration.clientHeight - top - bottom));
  Object.assign(image.style, {width: `${fitted.width}px`, height: `${fitted.height}px`,
    transform: `translate(${fitted.x + 8}px, ${fitted.y + top}px)`});
  image.dataset.fitScale = String(fitted.scale);
}

function currentScale(article) {
  return Number(article.dataset.scale || 1);
}

function scalePage(article) {
  const viewport = article.closest('.page-viewport');
  const scale = viewSelect.value === 'actual' ? 1 : Math.min(1, viewport.clientWidth / CANVAS.width);
  article.dataset.scale = String(scale);
  article.style.transform = `scale(${scale})`;
  const frame = article.closest('.page-frame');
  frame.style.width = `${CANVAS.width * scale}px`;
  frame.style.height = `${CANVAS.height * scale}px`;
}

function renderTranscript(page) {
  const fragment = document.createDocumentFragment();
  fragment.append(element('h3', '', `Page ${page['Page Number']}: ${page.Title}`));
  page.panels.forEach((panel, index) => {
    const entry = element('section', 'transcript-panel');
    entry.append(element('h4', '', `Panel ${index + 1}`));
    if (panel.caption) entry.append(element('p', 'transcript-caption', panel.caption));
    if (panel.narration) entry.append(element('p', '', panel.narration));
    fragment.append(entry);
  });
  transcript.replaceChildren(fragment);
}
viewSelect.addEventListener('change', () => { if (pages.length) scalePage(pages[currentPage]); });
new ResizeObserver(() => { if (pages.length) scalePage(pages[currentPage]); }).observe(document.querySelector('#chapter-pages'));

previous.addEventListener('click', () => showPage(currentPage - 1));
next.addEventListener('click', () => showPage(currentPage + 1));
pageSelect.addEventListener('change', () => {
  showPage(Number(pageSelect.value));
  reader.scrollIntoView({ block: 'start' });
});
document.addEventListener('keydown', event => {
  if (event.altKey || event.ctrlKey || event.metaKey || event.shiftKey ||
      event.target.closest('input, textarea, select, [contenteditable="true"]')) return;
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
