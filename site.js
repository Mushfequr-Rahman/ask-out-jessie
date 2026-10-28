// Keep existing published bookmarks working after the navigation cleanup.
const legacy = document.body.dataset.legacy;
if (legacy === 'metals') {
  const destination = new URL('glossary.html', window.location.href);
  destination.search = window.location.search;
  destination.hash = window.location.hash || '#metals';
  destination.searchParams.set('layout', 'holder-art-1');
  window.location.replace(destination.href);
} else if (legacy === 'home') {
  const query = new URLSearchParams(window.location.search);
  const isReader = query.has('page') || window.location.hash === '#reader';
  const isFleet = window.location.hash === '#fleet';
  if (isReader || isFleet) {
    const destination = new URL(isFleet ? 'glossary.html' : 'prologue.html', window.location.href);
    destination.search = window.location.search;
    destination.hash = isFleet ? '#ships' : '#reader';
    destination.searchParams.set('layout', 'holder-art-1');
    window.location.replace(destination.href);
  }
}
