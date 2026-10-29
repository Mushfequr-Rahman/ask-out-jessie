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
    assert (ship.get('commander_id') is None or ship['commander_id'] in character_ids) and ship['duchy_id'] in {d['id'] for d in duchies}, 'Unknown named ship commander/house'
    if ship.get('fleet_commander_id'):
        assert ship['fleet_commander_id'] in character_ids, 'Unknown fleet commander'
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
if 'enemy_ship_ids' in conflict:
    assert len(set(conflict['enemy_ship_ids']))==len(conflict['enemy_ship_ids'])==conflict['capital_ships_dispatched'], 'Enemy ship count mismatch'
    assert set(conflict['enemy_ship_ids']) <= named_ship_ids, 'Unknown enemy ship'
if 'captured_ship_ids' in conflict:
    captured=conflict['captured_ship_ids']
    assert len(set(captured))==len(captured)==conflict['captured_capital_ship_count'], 'Captured ship count mismatch'
    assert set(captured)==set(conflict['enemy_ship_ids']), 'The surrendered prizes must be the three engaged Bastions'
    rovan=next(c for c in characters if c['id']=='rovan-vey')
    owned={s['id'] for s in named_ships if s['duchy_id']==rovan['duchy_id'] and s['class_id']=='capital'}
    assert set(captured)<=owned and len(owned)==conflict['owned_capital_ships_after_battle']==rovan['military']['current_owned_capital_ship_count'], 'Owned fleet count differs after surrender'
    assert rovan['military']['initial_capital_ship_count']+len(captured)==len(owned), 'Keep original and captured capital counts distinct'
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
    if weapon.get('captain_id'):
        assert weapon['captain_id'] in character_ids, 'Unknown weapon captain'
for character in characters:
    if 'source_asset_id' in character:
        assert character['source_asset_id'] in assets, 'Unknown character illustration'
    if 'duchy_id' in character:
        assert character['duchy_id'] in {duchy['id'] for duchy in duchies}, 'Unknown character duchy'
    for weapon_id in character.get('equipment', {}).get('weapon_ids', []):
        assert weapon_id in weapons, 'Unknown character weapon'
    if character.get('group_id'):
        assert character['group_id'] in character_ids, 'Unknown character group'
    if character.get('current_assignment'):
        assert character['current_assignment'] in named_ship_ids, 'Unknown captain assignment'
groups={c['id']:c for c in characters if c.get('member_ids')}
for group in groups.values():
    members=group['member_ids']
    assert len(set(members))==len(members)==group['member_count'], 'Captain membership count mismatch'
    individuals=[next(c for c in characters if c['id']==id) for id in members]
    assert all(c['group_id']==group['id'] and c.get('personal_name') is None and c.get('title') for c in individuals), 'Captains need titles and group membership'
    assert {w for c in individuals for w in c['equipment']['weapon_ids']}==set(group['equipment']['weapon_ids']), 'Captain weapon assignments differ from the five sets'
if 'captain_assignments' in conflict:
    assignments=conflict['captain_assignments'];assigned=[id for ids in assignments.values() for id in ids]
    assert set(assignments)<=named_ship_ids, 'Unknown captain target ship'
    assert len(set(assigned))==len(assigned)==5 and set(assigned)==set(groups['honour-guard']['member_ids']), 'Captain assignments must partition the same five people'
    by_weapon={weapon:character['id'] for character in characters if character.get('group_id')=='honour-guard' for weapon in character['equipment']['weapon_ids']}
    expected={'argonaut':{by_weapon['shield-warhammer']},'serenity':{by_weapon['condenser-lance'],by_weapon['wind-twin-swords']},'serendipity':{by_weapon['point-scythe'],by_weapon['field-broadsword']}}
    assert {ship:set(ids) for ship,ids in assignments.items()}==expected, 'Boarding teams must match the established 2+2+1 plan'
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
