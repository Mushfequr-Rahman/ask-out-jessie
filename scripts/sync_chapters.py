"""Validate chapter sources and refresh their derived world.json story records."""
from pathlib import Path
import json
import re

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
        for panel in page['panels']:
            assert isinstance(panel, dict), 'Panel must be an object'
            assert isinstance(panel.get('image_src'), str) and re.fullmatch(r'assets/[a-zA-Z0-9_/-]+\.(png|jpe?g|webp|svg)', panel['image_src']), 'Invalid image_src'
            assert isinstance(panel.get('caption'), str), 'Panel needs a caption string (may be empty)'
            assert 'priority' not in panel or type(panel['priority']) is int and 1 <= panel['priority'] <= 5, 'Priority must be 1–5'
            assert 'image_fit' not in panel or panel['image_fit'] == 'contain', 'Invalid image fit'
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
             'image_description': panel.get('image_alt', panel['caption'])}
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
