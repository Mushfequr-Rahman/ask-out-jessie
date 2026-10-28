"""Validate chapter sources and refresh their derived world.json story records."""
from pathlib import Path
import json
import re
import math

ROOT = Path(__file__).resolve().parents[1]


def validate_chapter(chapter):
    assert isinstance(chapter, dict), 'Chapter must be an object'
    assert isinstance(chapter.get('title'), str) and chapter['title'].strip(), 'Chapter needs a title'
    assert isinstance(chapter.get('pages'), list) and chapter['pages'], 'Chapter needs pages'
    for number, page in enumerate(chapter['pages'], 1):
        assert isinstance(page, dict), 'Page must be an object'
        assert type(page.get('Page Number')) is int and page['Page Number'] == number, 'Page numbers must start at 1 and be consecutive'
        assert isinstance(page.get('Title'), str) and page['Title'].strip(), 'Page needs a Title'
        assert isinstance(page.get('panels'), list) and 1 <= len(page['panels']) <= 5, 'Each page needs 1–5 panels'
        assert 'footer' not in page or isinstance(page['footer'], str), 'Invalid footer'
        holders=[]
        for panel in page['panels']:
            assert isinstance(panel, dict), 'Panel must be an object'
            assert isinstance(panel.get('image_src'), str) and re.fullmatch(r'assets/[a-zA-Z0-9_/-]+\.(png|jpe?g|webp|svg)', panel['image_src']), 'Invalid image_src'
            assert isinstance(panel.get('caption'), str), 'Panel needs a caption string (may be empty)'
            if 'holder' in panel:
                h=panel['holder']
                assert isinstance(h, dict) and all(type(h.get(k)) in [int,float] and math.isfinite(h[k]) for k in ['x','y','width','height']), 'Invalid holder dimensions'
                assert h['x']>=0 and h['y']>=0 and h['width']>0 and h['height']>0 and h['x']+h['width']<=952.01 and h['y']+h['height']<=1268.01, 'Holder outside canvas'
                for other in holders:
                    assert h['x']+h['width']<=other['x']+.01 or other['x']+other['width']<=h['x']+.01 or h['y']+h['height']<=other['y']+.01 or other['y']+other['height']<=h['y']+.01, 'Fixed holders overlap'
                holders.append(h)
            assert page.get('layout_mode')!='fixed' or 'holder' in panel, 'Missing fixed holder'
            assert 'lettering_mode' not in panel or panel['lettering_mode'] in ['baked','editable_html'], 'Invalid lettering mode'
            assert 'priority' not in panel or type(panel['priority']) is int and 1 <= panel['priority'] <= 5, 'Priority must be 1–5'
            assert 'image_fit' not in panel or panel['image_fit'] == 'contain', 'Invalid image fit'
            assert 'image_revision' not in panel or isinstance(panel['image_revision'], str) and re.fullmatch(r'[a-fA-F0-9]{8,64}', panel['image_revision']), 'Invalid image revision'
            for field in ['narration', 'image_alt']:
                assert field not in panel or isinstance(panel[field], str), f'Invalid {field}'
            if 'layout' in panel:
                assert isinstance(panel['layout'], list) and all(isinstance(c, str) and re.fullmatch(r'[a-z][a-z0-9-]*', c) for c in panel['layout']), 'Invalid layout'
            assert 'full_size_link' not in panel or type(panel['full_size_link']) is bool, 'Invalid full_size_link'


def chapter_pages(chapter):
    """Keep the world reference format compatible with asset catalogue consumers."""
    validate_chapter(chapter)
    return [
        {'number': page['Page Number'], 'title': page['Title'], 'panels': [
            {'number': number, 'asset_id': Path(panel['image_src']).stem,
             'caption': panel['caption'], 'narration': panel.get('narration', ''),
             'priority': panel.get('priority', 3),
             'image_description': panel.get('image_alt', panel['caption']),
             **{key: panel[key] for key in ['holder','scene_id','lettering_mode'] if key in panel}}
            for number, panel in enumerate(page['panels'], 1)]}
        for page in chapter['pages']]


def sync_chapters(world):
    for story in world['publication']['stories']:
        source = (ROOT / story['json_file']).resolve()
        assert source.is_relative_to(ROOT / 'chapters') and source.suffix == '.json', 'Chapter JSON must be inside chapters/'
        chapter = json.loads(source.read_text())
        pages = chapter_pages(chapter)
        for page in chapter['pages']:
            for panel in page['panels']:
                assert (ROOT / panel['image_src']).is_file(), f"Missing image: {panel['image_src']}"
        story.update(pages=pages, page_count=len(pages),
                     panel_count=sum(len(page['panels']) for page in pages))
    return world


if __name__ == '__main__':
    path = ROOT / 'world.json'
    world = sync_chapters(json.loads(path.read_text()))
    path.write_text(json.dumps(world, indent=2, ensure_ascii=False) + '\n')
    print(f"Synced {len(world['publication']['stories'])} chapter(s) into world.json.")
