"""Require complete human banner review for a future publication candidate."""
import argparse
import json
from pathlib import Path
from build_banner_review import manifest


def validate_report(report, expected, scene_ids=None):
    assert report.get('schema_version') == 1 and report.get('revision') == expected['revision'], 'Stale review: rebuild and review current images/palettes'
    entries = report.get('entries', [])
    by_key = {(e['banner_id'], e['scene_id']): e for e in entries}
    required = {(h['id'], p['id']): (h, p) for h in expected['houses'] for p in h['panels']}
    assert len(by_key) == len(entries) and by_key.keys() == required.keys(), 'Missing, extra or duplicate review decisions'
    checked=0
    for key, (house, panel) in required.items():
        entry = by_key[key]
        assert entry.get('image_sha256') == panel['sha256'] and entry.get('reference_sha256') == house['reference_sha256'], f'Stale image/reference: {key}'
        if scene_ids is not None and panel['id'] not in scene_ids:
            continue
        assert entry.get('status') in ['pass', 'not_visible'], f'Unresolved banner review: {key}'
        assert entry['status'] != 'not_visible' or isinstance(entry.get('notes'), str) and entry['notes'].strip(), f'Explain absent marking: {key}'
        checked+=1
    return checked


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('report', type=Path, help='Exported banner-review-decisions.json')
    args = parser.parse_args()
    count = validate_report(json.loads(args.report.read_text()), manifest())
    print(f'Validated {count} banner decisions against current image, reference and palette versions.')
