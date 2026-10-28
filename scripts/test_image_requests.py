"""Request-contract tests using real chapter and visual-bible inputs; no model calls."""
import copy
import unittest
from build_image_requests import ROOT, read, build_request, resolution


class RequestTests(unittest.TestCase):
    def setUp(self):
        self.world=read(ROOT/'world.json')
        self.characters=read(ROOT/'character.json')
        self.objects=read(ROOT/'objects.json')
        self.template=read(ROOT/'templates/image-request.json')
        self.scenes=read(ROOT/'scenes/prologue.json')['scenes']
        self.files={'world.json':'world.json','character.json':'character.json','objects.json':'objects.json'}

    def request(self,scene):
        return build_request(scene,self.world,self.characters,self.objects,self.template,self.files)

    def test_all_three_bibles_control_the_prompt(self):
        scene=next(s for s in self.scenes if s['id']=='prologue-p11-panel01')
        self.world['setting']['test_marker']='WORLD_INPUT_MARKER'
        next(c for c in self.characters['characters'] if c['id']=='honour-guard')['uniform_standard']='CHARACTER_INPUT_MARKER'
        next(o for o in self.objects['objects'] if o['id']=='condenser-lance')['description']='OBJECT_INPUT_MARKER'
        prompt=self.request(scene)['prompt']
        for marker in ['WORLD_INPUT_MARKER','CHARACTER_INPUT_MARKER','OBJECT_INPUT_MARKER']:self.assertIn(marker,prompt)

    def test_exact_speech_and_speaker(self):
        scene=next(s for s in self.scenes if s['id']=='prologue-p05-panel02')
        q=self.request(scene)
        speech=next(b for b in q['lettering']['blocks'] if b['type']=='speech')
        self.assertEqual(speech['speaker_id'],'general-grievous')
        self.assertEqual(speech['render_text'],'The soldiers’ pay is overdue, Your Grace. The repair yards are still waiting too.')
        self.assertTrue(q['lettering']['render_in_image'])
        self.assertEqual(q['lettering']['mode'],'baked')

    def test_priority_cannot_mutate_a_locked_holder(self):
        scene=copy.deepcopy(self.scenes[0]);first=self.request(scene)
        scene['priority']=1
        self.assertEqual(first['holder'],self.request(scene)['holder'])
        self.assertEqual(first['target'],self.request(scene)['target'])

    def test_deterministic_requests_and_reference_roles(self):
        scene=self.scenes[0]
        q=self.request(scene)
        self.assertEqual(q,self.request(scene))
        self.assertTrue(all(ref['role'] and (ROOT/ref['path']).is_file() for ref in q['reference_images']))

    def test_unknown_entities_are_not_silently_invented(self):
        scene=copy.deepcopy(self.scenes[0]);scene['character_ids']=['unknown-character']
        with self.assertRaises(KeyError):self.request(scene)
        scene['character_ids']=[];scene['object_ids']=['unknown-object']
        with self.assertRaises(KeyError):self.request(scene)

    def test_size_hints_respect_documented_limits(self):
        for ratio in [.2,.534,1,1.5,2.8,4]:
            q=resolution(ratio);w,h=q['width'],q['height']
            self.assertEqual(w%16,0);self.assertEqual(h%16,0)
            self.assertLess(max(w,h),3840)
            self.assertLessEqual(max(w/h,h/w),3)
            self.assertGreaterEqual(w*h,655360)
            self.assertLessEqual(w*h,8294400)


if __name__=='__main__':unittest.main()
