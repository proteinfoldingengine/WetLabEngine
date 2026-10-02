import unittest,copy,importlib.util

class AssertionBindings(unittest.TestCase):
    def integrity(self):
        self.assertIsNotNone(importlib.util.find_spec('bindings'),'ASSERTION_BINDING_MISSING')
        import bindings
        return bindings
    def test_assertion_hash_mutation(self):
        b=self.integrity();sources={'example':'class E:\n def test_a(self):\n  assert 1==1\n'}
        manifest=b.build(sources);self.assertTrue(b.verify(manifest,sources))
        bad=copy.deepcopy(manifest);bad['tests'][0]['ast_sha256']='0'*64
        with self.assertRaises(ValueError):b.verify(bad,sources)
    def test_assertion_source_mutation(self):
        b=self.integrity();sources={'example':'class E:\n def test_a(self):\n  assert 1==1\n'}
        manifest=b.build(sources)
        with self.assertRaises(ValueError):b.verify(manifest,{'example':sources['example'].replace('1==1','1==2')})
    def test_assertion_identity_omission(self):
        b=self.integrity();sources={'example':'class E:\n def test_a(self):\n  assert 1==1\n'}
        manifest=b.build(sources);manifest['tests']=[]
        with self.assertRaises(ValueError):b.verify(manifest,sources)
    def test_checked_in_manifest_matches_pinned_runtime(self):
        from pathlib import Path
        import json
        b=self.integrity();here=Path(__file__).resolve().parent
        modules=('test_bootstrap','test_gate','test_mechanisms','test_feasibility','test_lifting','test_integration','test_campaign','test_integrity','test_review')
        manifest=json.loads((here/'TEST_MANIFEST_CAMPAIGN.json').read_text())
        self.assertEqual(manifest['format'],'python311-ast-without-empty-type-params-v1')
        self.assertTrue(b.verify(manifest,{m:(here/(m+'.py')).read_text() for m in modules}))

if __name__=='__main__':unittest.main(verbosity=2)
