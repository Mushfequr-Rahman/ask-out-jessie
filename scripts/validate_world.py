"""Check structured lore references and artwork metadata using only Python stdlib."""
from pathlib import Path
import hashlib
import json
import re
from sync_chapters import chapter_pages

ROOT = Path(__file__).resolve().parents[1]
world = json.loads((ROOT / 'world.json').read_text())
assets = {asset['id']: asset for asset in world['assets']}
assert len(assets) == len(world['assets']), 'Duplicate asset IDs'
actual_files = {path.relative_to(ROOT).as_posix() for path in (ROOT / 'assets').rglob('*')
                if path.is_file() and path.suffix.lower() in {'.png', '.jpg', '.jpeg', '.webp', '.svg'}}
assert actual_files == {asset['file'] for asset in assets.values()}, 'Asset inventory differs from files'
for asset in assets.values():
    path = (ROOT / asset['file']).resolve()
    assert path.is_relative_to((ROOT / 'assets').resolve()), 'Asset outside artwork folder'
    raw = path.read_bytes()
    assert len(raw) == asset['byte_size'], f"Stale file size: {asset['id']}"
    assert hashlib.sha256(raw).hexdigest() == asset['sha256'], f"Stale hash: {asset['id']}"

duchies = world['duchies']
assert len(duchies) == world['setting']['geography']['duchy_count'] == world['society']['duchy_count']
assert len({d['id'] for d in duchies}) == len(duchies), 'Duplicate duchy IDs'
assert len({d['color'].upper() for d in duchies}) == len(duchies), 'Duplicate duchy colours'
for duchy in duchies:
    assert re.fullmatch(r'#[0-9A-Fa-f]{6}', duchy['color']), 'Invalid duchy colour'
    assert assets[duchy['banner_asset_id']]['file'] == duchy['banner_path'], 'Banner mismatch'
palette = json.loads((ROOT / 'data/duchies.json').read_text())
assert [{key: d[key] for key in palette[0]} for d in duchies] == palette, 'Duchy palette reference drifted'

classes = {c['id'] for c in world['ship_classes']}
for ship in world['ship_designs']:
    assert ship['class_id'] in classes and ship['asset_id'] in assets, 'Broken ship reference'
    assert assets[ship['asset_id']]['file'].startswith('assets/')
assert world['objects_file'] == 'objects.json' and (ROOT / 'objects.json').is_file()
assert 'characters' not in world, 'Character records belong in character.json'
assert world['characters_file'] == 'character.json', 'Wrong character source'
characters = json.loads((ROOT / world['characters_file']).read_text())['characters']
assert isinstance(characters, list) and characters, 'Character source must contain records'
character_ids = {character['id'] for character in characters}
assert len(character_ids) == len(characters), 'Duplicate character IDs'
assert all(isinstance(identifier, str) and identifier for identifier in character_ids), 'Invalid character ID'
named_ships=world.get('named_ships', [])
named_ship_ids={ship['id'] for ship in named_ships}
assert len(named_ship_ids)==len(named_ships), 'Duplicate named ships'
designs={ship['id']:ship for ship in world['ship_designs']}
for ship in named_ships:
    assert ship['design_id'] in designs and ship['class_id']==designs[ship['design_id']]['class_id'], 'Unknown named ship design/class'
    assert ship['commander_id'] in character_ids and ship['duchy_id'] in {d['id'] for d in duchies}, 'Unknown named ship commander/house'
    if 'refit_asset_id' in ship:
        assert ship['refit_asset_id'] in assets, 'Missing named ship refit illustration'
for character in characters:
    if 'flagship_id' in character.get('military', {}):
        assert character['military']['flagship_id'] in named_ship_ids, 'Unknown flagship'
location_ids={location['id'] for location in world['locations']}
assert len(location_ids)==len(world['locations']), 'Duplicate location IDs'
for duchy in duchies:
    if duchy.get('ruler_id') is not None:
        assert duchy['ruler_id'] in character_ids, 'Unknown duchy ruler'
conflict = world['society'].get('current_conflict', {})
if 'target_character_id' in conflict:
    assert conflict['target_character_id'] in character_ids, 'Unknown conflict target'
if 'opponent_commander_id' in conflict:
    assert conflict['opponent_commander_id'] in character_ids, 'Unknown opposing commander'
if 'planned_battlefield_id' in conflict:
    assert conflict['planned_battlefield_id'] in location_ids, 'Unknown battlefield'
if 'friendly_capital_ship_id' in conflict:
    assert conflict['friendly_capital_ship_id'] in named_ship_ids, 'Unknown friendly capital ship'
for metal in world['metals']:
    for field in ['specimen_asset_id', 'core_asset_id']:
        if field in metal:
            assert metal[field] in assets, 'Broken metal illustration reference'
    if 'known_crafting' in metal:
        assert metal['known_crafting']['exclusive_expert_id'] in character_ids
assert world['setting']['geography']['atlas_asset_id'] in assets
weapons = {weapon['id']: weapon for weapon in world.get('weapons', [])}
for weapon in weapons.values():
    assert weapon['asset_id'] in assets and weapon['ability'], 'Broken weapon reference'
for character in characters:
    if 'source_asset_id' in character:
        assert character['source_asset_id'] in assets, 'Unknown character illustration'
    if 'duchy_id' in character:
        assert character['duchy_id'] in {duchy['id'] for duchy in duchies}, 'Unknown character duchy'
    for weapon_id in character.get('equipment', {}).get('weapon_ids', []):
        assert weapon_id in weapons, 'Unknown character weapon'
for metal in world['metals']:
    for weapon_id in metal.get('known_crafting', {}).get('weapon_ids', []):
        assert weapon_id in weapons, 'Unknown crafted weapon'

stories = world['publication']['stories']
assert len(stories) == world['publication']['story_count'], 'Wrong story count'
for story in stories:
    assert story['page_count'] == len(story['pages'])
    panels = [panel for page in story['pages'] for panel in page['panels']]
    assert len(panels) == story['panel_count']
    assert len({p['asset_id'] for p in panels}) == len(panels), 'Comic repeats an asset'
    assert all(panel['asset_id'] in assets for panel in panels), 'Unknown comic asset'
    assert len({assets[p['asset_id']]['sha256'] for p in panels}) == len(panels), 'Comic repeats image contents'
    reader = (ROOT / story['reader']).read_text()
    chapter = json.loads((ROOT / story['json_file']).read_text())
    assert chapter_pages(chapter) == story['pages'], 'Chapter JSON and world.json differ; run scripts/build_assets.py'
    assert f'data-chapter-src="{story["json_file"]}"' in reader, 'Reader does not load chapter source'
    assert 'class="comic-page"' not in reader, 'Reader contains hardcoded story pages'
    sources = [panel['image_src'] for page in chapter['pages'] for panel in page['panels']]
    assert sources == [assets[p['asset_id']]['file'] for p in panels], 'Chapter and world image paths differ'

for page in ROOT.glob('*.html'):
    for target in re.findall(r'(?:href|src)="([^"#]+)', page.read_text()):
        if target.startswith(('http:', 'https:', 'mailto:', 'data:')):
            continue
        local=target.split('#')[0].split('?')[0]
        assert not local or (ROOT / local).is_file(), f'Broken local link in {page.name}: {local}'
print(f"Validated {len(characters)} character records, {len(stories)} story, {len(duchies)} duchies, {len(world['ship_designs'])} ship designs and {len(assets)} assets.")
