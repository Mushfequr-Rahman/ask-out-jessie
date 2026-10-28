"""Shared banner selection and palette validation for generation and review."""
import re


def validate_banner(banner):
    assert banner.get('canonical_reference') in banner.get('reference_images', []), 'Banner needs its canonical reference'
    palette = banner.get('palette', {})
    assert palette.get('color_space') == 'sRGB', 'Banner palette needs sRGB'
    assert palette.get('basis') == 'neutral-light art direction', 'Palette must describe material colours'
    for part in ['cloth', 'emblem', 'trim']:
        swatch = palette.get(part, {})
        assert swatch.get('name') and re.fullmatch(r'#[0-9A-Fa-f]{6}', swatch.get('hex', '')), f'Invalid banner {part} swatch'
    assert palette.get('lighting_rule'), 'Banner needs a lighting rule'


def scene_banners(scene, characters, objects):
    chars = {c['id']: c for c in characters['characters']}
    items = {o['id']: o for o in objects['objects']}
    selected = [chars[i] for i in scene['character_ids']] + [items[i] for i in scene['object_ids']]
    duchies = {x.get('duchy_id') for x in selected}
    banners = [o for o in objects['objects'] if o['kind'] == 'heraldry' and
               (o['id'] in scene['object_ids'] or o['duchy_id'] in duchies)]
    for banner in banners:
        validate_banner(banner)
    return banners
