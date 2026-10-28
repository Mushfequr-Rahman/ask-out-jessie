"""Refresh world.json asset metadata and the HTML/Markdown artwork catalogues."""
from pathlib import Path
from html import escape
import hashlib
import json
import re
import struct
from sync_chapters import sync_chapters

ROOT = Path(__file__).resolve().parents[1]
world_path = ROOT / 'world.json'
world = sync_chapters(json.loads(world_path.read_text()))
existing = {asset['id']: asset for asset in world.get('assets', [])}
ship_ids = {ship['asset_id'] for ship in world['ship_designs']}
usage = {}
for story in world['publication']['stories']:
    for page in story['pages']:
        for panel in page['panels']:
            usage.setdefault(panel['asset_id'], []).append({
                'story_id': story['id'], 'page': page['number'],
                'panel': panel['number'], 'description': panel['image_description']})
titles = {
    'fracture': 'The Fracture', 'magnetic-islands': 'Magnetic currents',
    'survivors': 'The first survivors', 'human-adaptation': 'Generations adapt',
    'ore': 'Magneton discovery', 'polarity-engine': 'Type B polarity engine',
    'city': 'A floating city', 'gravity-chamber': 'The gravity chamber',
    'city-street': 'Life in the city', 'mining-dock': 'Mining and trade',
    'ducal-assembly': 'The mining barons', 'rovan-city': 'Rovan’s island city',
    'unpaid-ledger': 'The unpaid soldiers', 'duke-resolve': 'Rovan’s resolve',
    'caravan-boarding': 'Boarding the Caravan', 'duke-seizure': 'The duke’s claim',
    'soldiers-cheer': 'The soldiers cheer', 'rovan-future': 'His own future',
    'recruit-drill': 'Training the recruits', 'single-bastion-departure': 'One Bastion departs',
    'auric-raid': 'The raid on Auric Reach', 'ships-confiscated': 'Seizing the ships',
    'city-captured': 'The captured city', 'secret-type-c-forge': 'The secret forge',
    'five-honour-guards': 'The five honour guards', 'magnetic-boarding': 'Magnetic-field drifting',
    'shattered-earth-atlas': 'Shattered Earth atlas', 'magneton-types': 'Magneton metal specimens',
}
titles.update({s['asset_id']: s['name'] for s in world['ship_designs']})
titles.update({d['banner_asset_id']: d['name'] + ' banner' for d in world['duchies']})
assets = []
for path in sorted((ROOT / 'assets').rglob('*')):
    if not path.is_file() or path.suffix.lower() not in {'.png', '.jpg', '.jpeg', '.webp', '.svg'}:
        continue
    raw = path.read_bytes()
    dimensions = None
    if raw.startswith(b'\x89PNG\r\n\x1a\n'):
        width, height = struct.unpack('>II', raw[16:24])
        dimensions = {'width': width, 'height': height}
    identifier = path.stem
    category = 'ships' if identifier in ship_ids else 'banners' if identifier.startswith('banner-') else 'comic' if identifier in usage else 'world'
    old = existing.get(identifier, {})
    assets.append({
        'id': identifier, 'file': path.relative_to(ROOT).as_posix(),
        'title': old.get('title', titles.get(identifier, identifier.replace('-', ' ').title())),
        'category': category, 'dimensions': dimensions, 'byte_size': len(raw),
        'sha256': hashlib.sha256(raw).hexdigest(), 'status': 'current',
        'origin': old.get('origin', 'Generated artwork created for this project; some designs use user-provided visual references.'),
        'comic_usage': usage.get(identifier, []),
    })
world['assets'] = assets
world['publication']['asset_catalogue'] = 'assets.html'
world['publication']['repository_asset_catalogue'] = 'ASSETS.md'
world_path.write_text(json.dumps(world, indent=2, ensure_ascii=False) + '\n')

labels = {'comic': 'Comic scenes', 'ships': 'Ships', 'world': 'World references', 'banners': 'Duchy banners'}

def size_label(asset):
    dims = asset['dimensions']
    return (f"{dims['width']} × {dims['height']} · " if dims else '') + f"{asset['byte_size'] / 1024 / 1024:.1f} MB"

sections, markdown = [], [
    '# Asset catalogue', '',
    f"All **{len(assets)} current illustrations** in the repository, grouped below. The comic uses {len(usage)} unique panel images, generated for fixed holders with lettering inside the artwork. Earlier visual anchors live separately in references/.", '',
    '[Browse the hosted asset library](https://mushfequr-rahman.github.io/ask-out-jessie/assets.html) · [World reference JSON](world.json) · [Banner comparison review](generation/banner-review.html)', '',
    'Select a preview or filename to open the original. Dimensions and sizes refer to the full-resolution files. All artwork was generated for this project; the original user-supplied inspiration images are not included in this catalogue.', '',
]
for category, label in labels.items():
    items = [asset for asset in assets if asset['category'] == category]
    if category == 'comic':
        items.sort(key=lambda asset: (asset['comic_usage'][0]['page'], asset['comic_usage'][0]['panel']))
    elif category == 'ships':
        ship_order = {ship['asset_id']: i for i, ship in enumerate(world['ship_designs'])}
        items.sort(key=lambda asset: ship_order[asset['id']])
    elif category == 'banners':
        banner_order = {duchy['banner_asset_id']: i for i, duchy in enumerate(world['duchies'])}
        items.sort(key=lambda asset: banner_order[asset['id']])
    cards = []
    markdown += [f'## {label}', '', '| Preview | Asset | Size | Used in the comic |', '| --- | --- | --- | --- |']
    for asset in items:
        file, title = asset['file'], asset['title']
        used = ', '.join(f"Page {u['page']}, panel {u['panel']}" for u in asset['comic_usage']) or 'Reference artwork'
        cards.append(f'''<article class="asset-card" data-asset-id="{escape(asset['id'])}"><a href="{escape(file)}" target="_blank" rel="noopener" aria-label="Open {escape(title)} original (opens a new tab)"><img src="{escape(file)}?v={asset['sha256'][:12]}" alt="{escape(title)}" loading="lazy" decoding="async"></a><div><h3>{escape(title)}</h3><p>{escape(size_label(asset))}</p><p>{escape(used)}</p><a class="text-link" href="{escape(file)}" download>Download original ↓</a></div></article>''')
        markdown.append(f'| [<img src="{file}" alt="{escape(title)}" width="110">]({file}) | **{title}**<br>[{file}]({file}) | {size_label(asset)} | {used} |')
    markdown.append('')
    sections.append(f'<section id="assets-{category}" class="reference-section" aria-labelledby="assets-{category}-title"><h2 id="assets-{category}-title">{label} <span class="asset-count">{len(items)}</span></h2><div class="asset-grid">'+''.join(cards)+'</div></section>')
markdown += ['## Keeping the catalogue current', '', 'World facts live in [world.json](world.json). Asset metadata there includes paths, dimensions, byte sizes, SHA-256 hashes, and comic panel usage.', '', 'After adding, replacing, or removing artwork, run:', '', '```sh', 'python3 scripts/build_assets.py', 'python3 scripts/sync_layout.py', '```', '', 'The script reads image metadata without modifying image files and refreshes `world.json`, `assets.html`, and this page. All generated pages are checked in; no build is required to serve the site.', '']
(ROOT / 'ASSETS.md').write_text('\n'.join(markdown))
contents = ''.join(f'<a href="#assets-{key}">{value}</a>' for key, value in labels.items())
html = f'''<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="description" content="Browse all {len(assets)} Magneton illustrations, ship designs, world references, and duchy banners.">
  <title>Magneton · Asset Library</title>
  <link rel="stylesheet" href="styles.css?v=holder-art-1">
  <script src="site.js?v=holder-art-1" defer></script>
</head>
<body>
<!-- site-header --><!-- /site-header -->
  <main class="glossary-main asset-library"><section class="page-intro" aria-labelledby="page-title"><a class="text-link" href="glossary.html?v=holder-art-1">← Glossary</a><h1 id="page-title">Asset library<span>.</span></h1><p>{len(assets)} illustrations from the fractured world.</p><p class="glossary-note">Browse the original artwork, see where each image appears in the comic, and download full-resolution files.</p><div class="data-links"><a class="primary-link" href="world.json" download>Download world.json ↓</a><a class="text-link" href="character.json" download>Download character.json ↓</a><a class="text-link" href="objects.json" download>Download objects.json ↓</a><a class="text-link" href="world.json">View world reference ↗</a><a class="text-link" href="generation/banner-review.html">Banner comparison review →</a><a class="text-link" href="https://github.com/Mushfequr-Rahman/ask-out-jessie/blob/master/ASSETS.md" target="_blank" rel="noopener">Repository catalogue ↗</a></div><div class="section-index" aria-label="Asset categories">{contents}</div></section>{''.join(sections)}</main>
<!-- site-footer --><!-- /site-footer -->
</body>
</html>
'''
(ROOT / 'assets.html').write_text(html)
print(f'Refreshed {len(assets)} assets in world.json, ASSETS.md, and assets.html.')
