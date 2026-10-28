"""Validate visual bibles, fixed holders, request references and generated outputs."""
from pathlib import Path
import argparse
import hashlib
import json
import math
import struct
from sync_chapters import validate_chapter
from heraldry import validate_banner

ROOT=Path(__file__).resolve().parents[1]


def load(path):return json.loads((ROOT/path).read_text())

def local_file(path):
    resolved=(ROOT/path).resolve()
    assert resolved.is_relative_to(ROOT) and resolved.is_file(), f'Missing/unsafe reference: {path}'
    return resolved


def pointer(document,path):
    value=document
    for part in path.lstrip('/').split('/'):
        part=part.replace('~1','/').replace('~0','~')
        value=value[int(part)] if isinstance(value,list) else value[part]
    return value


def validate(require_outputs=False, banner_review=None):
    world=load('world.json');chars=load('character.json')['characters'];objects=load('objects.json')['objects']
    assert world['objects_file']=='objects.json'
    char_ids={c['id'] for c in chars};object_ids={o['id'] for o in objects}
    assert len(object_ids)==len(objects), 'Duplicate visual object IDs'
    for record in [*chars,*objects]:
        if record.get('kind')=='heraldry':validate_banner(record)
        for ref in record.get('reference_images',[]):local_file(ref)
        if 'world_reference' in record:assert pointer(world,record['world_reference']) is not None
    chapter=load('chapters/prologue.json');validate_chapter(chapter)
    panels={p['scene_id']:p for page in chapter['pages'] for p in page['panels']}
    scenes=load('scenes/prologue.json')['scenes'];lock=load('generation/layout-lock.json')['holders']
    assert len({s['id'] for s in scenes})==len(scenes)==len(panels)==len(lock)
    for scene in scenes:
        id=scene['id'];panel=panels[id]
        assert scene['holder']==panel['holder']==lock[id], f'Changed pre-generation holder: {id}'
        assert set(scene['character_ids'])<=char_ids and set(scene['object_ids'])<=object_ids
        for ref in scene['reference_images']:local_file(ref['path'])
        q=load('generation/requests/'+id+'.json')
        assert q['holder']==lock[id] and q['parameters']['scene']==id
        assert q['lettering']['mode']=='baked' and q['lettering']['render_in_image']
        assert [b['text'] for b in q['lettering']['blocks']]==[b['text'] for b in scene['lettering']], 'Lettering text drift'
        for ref in q['reference_images']:local_file(ref['path'])
        t=q['target'];assert t['width']%16==t['height']%16==0
        assert max(t['width'],t['height'])<3840 and max(t['width']/t['height'],t['height']/t['width'])<=3
        assert 655360<=t['width']*t['height']<=8294400
        visible=t['visible_window']
        for block in q['lettering']['blocks']:
            b=block['source_bounds'];assert all(math.isfinite(v) for v in b.values())
            assert b['x']>=visible['x']-.002 and b['y']>=visible['y']-.002
            assert b['x']+b['width']<=visible['x']+visible['width']+.002 and b['y']+b['height']<=visible['y']+visible['height']+.002
        if require_outputs:
            path=local_file(scene['output_file']);raw=path.read_bytes();assert raw.startswith(b'\x89PNG\r\n\x1a\n')
            width,height=struct.unpack('>II',raw[16:24]);assert width>0 and height>0
            assert panel['image_src']==scene['output_file'] and panel['lettering_mode']=='baked'
    if require_outputs:
        assert len({hashlib.sha256(local_file(s['output_file']).read_bytes()).hexdigest() for s in scenes})==len(scenes), 'Repeated generated image'
        reviewed=load('generation/review.json')['selected_outputs']
        assert {r['id'] for r in reviewed}=={s['id'] for s in scenes}, 'Incomplete publication review'
        new_banner_review_required=False
        for record in reviewed:
            raw=local_file(record['output_file']).read_bytes()
            assert hashlib.sha256(raw).hexdigest()==record['sha256'], 'Changed artwork after review'
            assert struct.unpack('>II',raw[16:24])==(record['dimensions']['width'],record['dimensions']['height'])
            selected=load(record['selected_run'])
            assert selected['status']=='visually_reviewed' and selected['output_file']==record['output_file']
            selected_request=load(selected['request_file'])
            if selected_request.get('schema_version',1)>=2 and selected_request.get('heraldry',{}).get('banner_ids'):
                new_banner_review_required=True
        assert not new_banner_review_required or banner_review, 'New heraldry-aware artwork requires --banner-review with exported decisions'
    if banner_review:
        from build_banner_review import manifest
        from validate_banner_review import validate_report
        validate_report(json.loads(Path(banner_review).read_text()),manifest())
    print(f'Validated {len(objects)} visual objects, {len(scenes)} locked holders and baked-lettering requests'+(' with selected outputs.' if require_outputs else '.'))


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--require-outputs',action='store_true')
    p.add_argument('--banner-review',help='Exported decisions for current artwork/palette versions')
    args=p.parse_args();validate(args.require_outputs,args.banner_review)
