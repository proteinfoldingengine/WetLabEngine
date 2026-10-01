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

if __name__=='__main__':unittest.main(verbosity=2)
