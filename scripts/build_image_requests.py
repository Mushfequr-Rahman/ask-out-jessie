"""Build deterministic, reviewable image requests from a scene and visual bibles."""
from pathlib import Path
import argparse
import hashlib
import json
import math
import re
from heraldry import scene_banners

ROOT = Path(__file__).resolve().parents[1]


def read(path):
    return json.loads(path.read_text())


def resolution(ratio):
    """Provider hint based on documented flexible-size constraints; not a tool guarantee."""
    ratio = min(3, max(1 / 3, ratio))
    width = round(math.sqrt(1048576 * ratio) / 16) * 16
    height = round(width / ratio / 16) * 16
    return {'width': width, 'height': height, 'size': f'{width}x{height}'}


def build_request(scene, world, characters, objects, template, files):
    char_map = {c['id']: c for c in characters['characters']}
    object_map = {o['id']: o for o in objects['objects']}
    selected_chars = [char_map[c] for c in scene['character_ids']]
    selected_objects = [object_map[o] for o in scene['object_ids']]
    banners = scene_banners(scene, characters, objects)
    selected_objects += [b for b in banners if b['id'] not in scene['object_ids']]
    holder = scene['holder']; ratio = holder['width'] / holder['height']
    target = resolution(ratio)
    refs = []
    def add_ref(path, role):
        assert (ROOT / path).is_file(), f'Missing reference: {path}'
        if not any(r['path'] == path for r in refs) and len(refs) < 4:
            refs.append({'path': path, 'role': role, 'index': len(refs) + 1})
    assert len(banners) <= 2, 'At most two house anchors per request; split larger casts into shots or author a combined reference sheet'
    for banner in banners:
        add_ref(banner['canonical_reference'], 'AUTHORITATIVE banner colours, emblem and trim for '+banner['duchy_id']+'. Overrides banners in ALL older scene, style and character references. Do not insert a banner unless the scene calls for it.')
    for obj in selected_objects:
        if obj['kind']=='ship' and obj.get('canonical_reference'):
            add_ref(obj['canonical_reference'], 'AUTHORITATIVE ship geometry for '+obj['id']+'. Overrides older generic ship silhouettes in scene references; preserve this design in the new pose. Do not copy its background, people or lettering.')
    for ref in scene['reference_images']:
        add_ref(ref['path'], ref['role']+' Composition/action reference only for heraldry: its banner colours and symbols are NOT authoritative; follow the canonical house anchors and palettes.')
    for c in selected_chars:
        for path in c.get('reference_images', []): add_ref(path, 'Character identity/wardrobe anchor for '+c['id']+'; not extra people to insert.')
    # House markings and ship silhouettes need stronger visual anchors than generic metal specimens.
    for obj in sorted(selected_objects, key=lambda o: 0 if o['kind'] == 'heraldry' else 1 if o['kind'] == 'ship' else 2):
        for path in obj['reference_images']: add_ref(path, obj['name']+' appearance only; include only objects required by the scene.')
    native_ratio=target['width']/target['height']
    if ratio>=native_ratio:
        visible={'x':0,'y':(1-native_ratio/ratio)/2,'width':1,'height':native_ratio/ratio}
    else:
        visible={'x':(1-ratio/native_ratio)/2,'y':0,'width':ratio/native_ratio,'height':1}
    target['visible_window']=visible
    blocks = []
    for block in scene['lettering']:
        bounds=block['bounds']
        render_text = re.sub(r'^[^:\n]{1,35}:\s*', '', block['text']) if block['type']=='speech' else block['text']
        render_text = render_text.strip('“”\"') if block['type']=='speech' else render_text
        speaker=re.match(r'^([^:\n]{1,35}):\s*',block['text']) if block['type']=='speech' else None
        speaker_name=speaker[1] if speaker else None
        speaker_id={'Rovan':'rovan-vey','Grievous':'general-grievous','Courier':'veymarch-courier','Engineer':'veymarch-engineers','Joseph':'admiral-joseph','Sailor':'auric-sailors','The ruler of Auric Reach':'auric-ruler','Ferdinand':'auric-ruler'}.get(speaker_name)
        blocks.append({**block,'speaker_name':speaker_name,'speaker_id':speaker_id,'render_text':render_text,'normalized_bounds':{k:round(bounds[k]/holder['width' if k in ['x','width'] else 'height'],4) for k in bounds}})
    for block in blocks:
        n=block['normalized_bounds']
        block['source_bounds']={'x':round(visible['x']+n['x']*visible['width'],4),'y':round(visible['y']+n['y']*visible['height'],4),'width':round(n['width']*visible['width'],4),'height':round(n['height']*visible['height'],4)}
    char_context = [{k:c[k] for k in ['id','name','title','group_id','visual_concept','uniform_standard','visual_profiles','equipment'] if k in c} for c in selected_chars]
    object_context = [{k:o[k] for k in ['id','name','description','constraints','canonical_reference','palette'] if k in o} for o in selected_objects]
    if scene['silver_guard_weapon_id']:
        for group in char_context:
            if group['id']=='honour-guard':
                group['visual_profiles']=[p for p in group.get('visual_profiles',[]) if p['weapon_id']==scene['silver_guard_weapon_id']]
    orientation='PORTRAIT / VERTICAL' if ratio < .85 else 'EXTRA WIDE HORIZONTAL STRIP' if ratio > 2.7 else 'LANDSCAPE' if ratio > 1.15 else 'NEAR SQUARE'
    camera='Re-stage the action vertically, main figure or object stacked with the setting behind, keep head, hands and entire weapon visible.' if ratio < .85 else 'Use a panoramic, low-height composition. Align all essential heads, hands, weapons and action across a central horizontal band; scenery above/below may be trimmed.' if ratio>2.7 else 'Use a clear, tightly composed shot with the important action filling the aperture; do not copy the old wide framing.'
    zones=[{'type':b['type'],'bounds':b['normalized_bounds']} for b in blocks]
    rules=list(template['constraints'])
    early_era = scene['page_number']==1 or (scene['page_number']==2 and scene['panel_number']==2)
    if early_era:rules+=['This is the Fracture/survival/discovery era: ruined land and survivors. NO airships, aircraft, powered vessels, magnetic motors, ducal heraldry or silver knights exist yet. Keep the sky free of flying vehicles.']
    if 5<=scene['page_number']<19:rules+=['Rovan commands ONE capital ship. The opposing Auric Reach force has THREE capital ships. Show only ships explicitly required by the scene; a report about them is not permission to add them to the background.']
    if scene['page_number']==19:rules+=['The three enemy Bastions surrender on page19. Rovan began with ONE Argonaut and gains THREE captured capital ships; four owned in total, not four new prizes. Damaged ships still require repairs. Show only ships explicitly required by this shot. Plain WHITE surrender flags are signals, not changed duchy colours.']
    if scene['page_number']==20:rules+=['Rovan owns FOUR capital ships: the original wedge-prowed Argonaut and THREE round-prowed prizes, Josephine, Serenity and Serendipity. Repairs and crimson repainting occur at New Frontier on page20 before the four sail for Oram. Do not show four copies of Argonaut or add a fifth ship. The three new prize captains are ordinary naval officers, not additional silver Type C knights.']
    if scene['page_number']==21:rules+=['Rovan owns FOUR capital ships: wedge-prowed Argonaut and THREE crimson repainted round-prowed Bastion prizes. Oram is now under siege, not conquered. Trading convoys are smaller transport ships, not extra capitals. City standards remain Auric GOLD/NAVY; fleet standards Veymarch CRIMSON/SILVER. Show only ships required by the shot.']
    if scene['page_number']==22:rules+=['Rovan owns FOUR capitals, one wedge Argonaut and three rounded repainted Bastion prizes. Oram’s siege ends with Duke Ferdinand and his barons surrendering the CITY on page22 after a messenger. Gold/navy Auric identities and crimson/silver Veymarch identities remain distinct. White flags are signals, not new house colours. Show only ships requested in this shot; no whole-duchy annexation.']
    if scene['page_number']>=23:rules+=['After Oram’s surrender, Rovan begins local reforms but struggles to govern and defend captured holdings. Exactly FOUR owned capital ships remain. Ironveil and Glassmere move toward exposed Auric outer territory using SMALL craft; no additional capitals or completed whole-duchy annexation. Ordinary naval captains are separate from five Type C knights.']
    if scene['page_number']==12 and scene['panel_number']==3:rules=[r for r in rules if not r.startswith('Rovan has ONE')]+['Exactly THREE Auric Reach capital ships, all fully countable, under gold/navy Auric standards. They are the opponent’s ships.']
    if scene['silver_guard_count']:
        rules += [f'Exactly {scene["silver_guard_count"]} silver Type C captain(s) visible. Do not insert other captains from the reference lineup.', 'All ordinary allied troops are BRONZE over crimson; enemy guards navy/gold with BRASS armour. Silver is exclusive to the named Type C captain(s).', 'Sealed continuous silver coverage, no open joints or gaps. Narrow brass edging, small mechanical fittings and crimson badges bearing the silver broken shield and eight-point star.']
    if scene['page_number']==9 and scene['panel_number']==1:rules+=['The standing Type C suit is empty workshop equipment, not a sixth soldier.']
    if scene['page_number']==9 and scene['panel_number']==2:rules+=['Exactly FIVE full-body captains with FIVE loadouts, left to right lance, broadsword, twin swords, hammer, scythe. All heads, feet and weapons visible.']
    rules += scene.get('visual_constraints', [])
    if not early_era:
        rules += ['All airborne vessels are rigid mechanical bronze/metal Zeppelin-like ships. ANY wooden sailing boats or cloth sails seen in an old scene reference are obsolete errors: REPLACE them with small bronze Zeppelin commuter hulls, keeping background positions.']
    duchy_ids={c.get('duchy_id') for c in selected_chars}|{o.get('duchy_id') for o in selected_objects}
    world_context={'setting':world['setting'], 'metals':[{k:m[k] for k in ['id','appearance','properties']} for m in world['metals']], 'duchies':[{k:d[k] for k in ['id','name','emblem']} for d in world['duchies'] if d['id'] in duchy_ids]}
    banner_policy = template['heraldry']
    compact=lambda value:json.dumps(value,ensure_ascii=False,separators=(',',':'))
    prompt='\n\n'.join([
      f'PURPOSE: Regenerate ONE comic illustration for FIXED holder {holder["width"]:.2f} by {holder["height"]:.2f} logical pixels, aspect {ratio:.4f}:1. {orientation}. Requested output {target["size"]}. Do NOT resize or redesign the holder. Paint a NEW composition for it, not a framed photo.',
      'SCENE: '+scene['description']+'\nCAMERA: '+camera,
      'STYLE: '+template['style'],
      'WORLD CONTEXT FROM world.json: '+compact(world_context)+' Preserve the source scene’s era and events; do not add unrelated world elements.',
      'CHARACTERS (immutable identity and costume): '+compact(char_context),
      'OBJECTS (only those belonging in this scene): '+compact(object_context),
      'REFERENCES: '+compact(refs),
      'BANNER AUTHORITY: '+compact(banner_policy)+' Dedicated objects.json palettes describe neutral-light materials. Map/UI colours from world.json are not fabric colours. Canonical banner images control heraldic geometry; palette swatches control intended material hues. Older scene/character palettes never override these. Apply the palette lighting rule, keeping each house recognisable. Palette hex values are targets, not a guarantee of identical generated pixels.',
      'LETTERING: Draw the speech balloons, cream caption/narration boxes and ALL their text directly INTO the artwork. Use a professional clear comic lettering font, dark ink on pale cream/white, readable contrast. Reproduce each render_text EXACTLY, preserving punctuation; do not print speaker labels or JSON keys. Speech tails point to the speaking person. No other words, labels, signs or gibberish. The visible crop-safe aperture in FULL SOURCE coordinates is '+compact(visible)+'. Place ALL text wholly inside it. The following bounding boxes are normalized to the FULL SOURCE image (not to the holder); use these adjusted positions exactly: '+compact([{'type':b['type'],'render_text':b['render_text'],'bounds_in_full_source_image':b['source_bounds']} for b in blocks]),
      'INVARIANTS: '+' '.join(rules),
      'DELIVERY: Edge-to-edge painted scene with finished comic lettering, no blank borders, no letterboxing, no collage. If native output ratio differs from the holder, keep ALL important content inside its central crop-safe aperture; only expendable background may extend beyond. For a wide strip, put the main figures and action in the central horizontal band, leaving substantial sky/floor outside that band.'
    ])
    return {'schema_version':2,'id':scene['id'],'parameters':{'scene':scene['id'],**files},'holder':holder,'target':target,'output_file':scene['output_file'],'reference_images':refs,'lettering':{'mode':'baked','render_in_image':True,'blocks':blocks},'resolved_context':{'world':world_context,'characters':char_context,'objects':object_context,'world_constraints':rules},'heraldry':{'banner_ids':[b['id'] for b in banners],'policy':banner_policy},'prompt':prompt,'review_checks':['Holder dimensions unchanged','Faces, costume, metals and heraldry match anchors','Correct number of ships and silver captains','No essential content cut by the holder or covered by lettering','Generated lettering matches every requested render_text exactly; transcript retains source wording',*banner_policy['review_checks']]}


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--scene',default='scenes/prologue.json')
    parser.add_argument('--world',default='world.json')
    parser.add_argument('--characters',default='character.json')
    parser.add_argument('--objects',default='objects.json')
    parser.add_argument('--template',default='templates/image-request.json')
    parser.add_argument('--output',default='generation/drafts')
    args=parser.parse_args()
    files={'world.json':args.world,'character.json':args.characters,'objects.json':args.objects}
    world,characters,objects,template=[read(ROOT/p) for p in [args.world,args.characters,args.objects,args.template]]
    data=read(ROOT/args.scene);scenes=data.get('scenes',[data])
    output=(ROOT/args.output).resolve();assert output.is_relative_to(ROOT), 'Output must stay inside repository';output.mkdir(parents=True,exist_ok=True)
    manifest=[]
    for scene in scenes:
        request=build_request(scene,world,characters,objects,template,files)
        request['source_hashes']={name:hashlib.sha256((ROOT/path).read_bytes()).hexdigest() for name,path in files.items()}
        request['source_hashes']['scene']=hashlib.sha256(json.dumps(scene,sort_keys=True,ensure_ascii=False).encode()).hexdigest()
        path=output/(scene['id']+'.json');path.write_text(json.dumps(request,indent=2,ensure_ascii=False)+'\n')
        manifest.append({'id':scene['id'],'request_file':path.relative_to(ROOT).as_posix(),'output_file':scene['output_file']})
    (output/'index.json').write_text(json.dumps({'requests':manifest},indent=2)+'\n')
    print(f'Built {len(manifest)} requests from scene + world.json + character.json + objects.json.')


if __name__=='__main__':main()
