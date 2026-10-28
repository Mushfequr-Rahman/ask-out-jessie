"""Build a static side-by-side heraldry review page without changing artwork."""
import hashlib
from html import escape
import json
from pathlib import Path
from heraldry import scene_banners, validate_banner

ROOT = Path(__file__).resolve().parents[1]


def load(path):
    return json.loads((ROOT / path).read_text())


def manifest():
    objects = load('objects.json'); characters = load('character.json')
    scenes = load('scenes/prologue.json')['scenes']
    houses = []
    for banner in objects['objects']:
        if banner['kind'] != 'heraldry':
            continue
        validate_banner(banner)
        panels = []
        for scene in scenes:
            if banner['id'] not in [b['id'] for b in scene_banners(scene, characters, objects)]:
                continue
            path = ROOT / scene['output_file']
            panels.append({'id': scene['id'], 'page': scene['page_number'], 'panel': scene['panel_number'],
                           'file': scene['output_file'], 'sha256': hashlib.sha256(path.read_bytes()).hexdigest()})
        houses.append({'id': banner['id'], 'name': banner['name'], 'reference': banner['canonical_reference'],
                       'reference_sha256': hashlib.sha256((ROOT / banner['canonical_reference']).read_bytes()).hexdigest(),
                       'palette': banner['palette'], 'panels': panels})
    result = {'schema_version': 1, 'chapter': 'prologue', 'houses': houses,
              'checks': load('templates/image-request.json')['heraldry']['review_checks']}
    result['revision'] = hashlib.sha256(json.dumps(result, sort_keys=True).encode()).hexdigest()
    return result


def build():
    data = manifest()
    (ROOT / 'generation/banner-review.json').write_text(json.dumps(data, indent=2, ensure_ascii=False)+'\n')
    sections = []
    for house in data['houses']:
        swatches = ''.join(f'<li><span class="swatch" style="background:{house["palette"][part]["hex"]}"></span>{part}: {escape(house["palette"][part]["name"])} <code>{house["palette"][part]["hex"]}</code></li>' for part in ['cloth','emblem','trim'])
        for swatch in house['palette'].get('accents', []):
            swatches += f'<li><span class="swatch" style="background:{swatch["hex"]}"></span>{escape(swatch["name"])} <code>{swatch["hex"]}</code></li>'
        cards = []
        for panel in house['panels']:
            key = house['id'] + ':' + panel['id']
            cards.append(f'''<article class="review-card" data-key="{key}"><h3>Page {panel['page']}, panel {panel['panel']}</h3><a href="../{panel['file']}" target="_blank" rel="noopener"><img src="../{panel['file']}" alt="Page {panel['page']}, panel {panel['panel']}: inspect visible {escape(house['name'])} markings" loading="lazy"></a><p><a href="../prologue.html?page={panel['page']}#reader" target="_blank" rel="noopener">View in comic ↗</a> · Open image to inspect small details.</p><label>Decision <select><option value="pending">Needs review</option><option value="pass">Matches reference</option><option value="fix">Needs correction</option><option value="not_visible">No visible house marking</option></select></label><label>Notes <textarea rows="2" placeholder="Colour, emblem, trim or lighting issue"></textarea></label></article>''')
        sections.append(f'''<section id="{house['id']}"><h2>{escape(house['name'])}</h2><div class="comparison"><aside><a href="../{house['reference']}" target="_blank" rel="noopener"><img class="reference" src="../{house['reference']}" alt="Canonical {escape(house['name'])}"></a><ul>{swatches}</ul><p>Neutral-light material targets. Judge hue and emblem identity with allowance for scene lighting.</p></aside><div class="candidates">{''.join(cards) or '<p>No scenes currently name this house. The reference is ready for future chapters.</p>'}</div></div></section>''')
    html = '''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>Banner consistency review · Magneton</title><link rel="stylesheet" href="banner-review.css"><script src="banner-review.js" defer></script></head><body><main><a href="../assets.html">← Asset library</a><h1>Banner consistency review</h1><p>Compare each house reference with the candidate panels. Check cloth hue, emblem and trim separately. Panels are selected from scene character/object affiliations; a house marking may not be visible. Existing illustrations have not been corrected by this workflow.</p><p>Open full-size images for small details. Changes save in this browser. Export decisions for repository validation; this page does not publish or edit artwork.</p><div class="toolbar"><button id="export" type="button">Export review JSON</button><span id="status" role="status">Loading review…</span></div><p id="storage-message" role="status"></p>''' + ''.join(sections) + '</main></body></html>\n'
    (ROOT / 'generation/banner-review.html').write_text(html)
    print(f'Built eight-house review with {sum(len(h["panels"]) for h in data["houses"])} panel/house comparisons; decisions start pending.')


if __name__ == '__main__':
    build()
