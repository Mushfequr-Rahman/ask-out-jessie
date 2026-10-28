"""Review decisions must cover current image/reference versions; no automatic approval."""
import copy
import unittest
from build_banner_review import manifest
from validate_banner_review import validate_report


class BannerReviewTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.expected=manifest()

    def report(self):
        return {'schema_version':1,'revision':self.expected['revision'],'entries':[
            {'banner_id':h['id'],'scene_id':p['id'],'image_sha256':p['sha256'],
             'reference_sha256':h['reference_sha256'],'status':'pass','notes':''}
            for h in self.expected['houses'] for p in h['panels']]}

    def test_complete_review(self):
        self.assertEqual(len(self.expected['houses']),8)
        self.assertGreater(validate_report(self.report(),self.expected),0)

    def test_pending_or_correction_cannot_pass(self):
        for status in ['pending','fix']:
            report=self.report();report['entries'][0]['status']=status
            with self.assertRaises(AssertionError):validate_report(report,self.expected)

    def test_missing_or_duplicate_decision_cannot_pass(self):
        for duplicate in [False,True]:
            report=self.report()
            if duplicate:report['entries'].append(copy.deepcopy(report['entries'][0]))
            else:report['entries'].pop()
            with self.assertRaises(AssertionError):validate_report(report,self.expected)

    def test_changed_art_reference_or_palette_invalidates_review(self):
        report=self.report()
        for field in ['image_sha256','reference_sha256']:
            altered=copy.deepcopy(report);altered['entries'][0][field]='changed'
            with self.assertRaises(AssertionError):validate_report(altered,self.expected)
        altered=copy.deepcopy(report);altered['revision']='old-palette-version'
        with self.assertRaises(AssertionError):validate_report(altered,self.expected)

    def test_absent_marking_needs_explanation(self):
        report=self.report();report['entries'][0]['status']='not_visible'
        with self.assertRaises(AssertionError):validate_report(report,self.expected)
        report['entries'][0]['notes']='No banner or house badge visible in this shot.'
        validate_report(report,self.expected)


if __name__=='__main__':unittest.main()
