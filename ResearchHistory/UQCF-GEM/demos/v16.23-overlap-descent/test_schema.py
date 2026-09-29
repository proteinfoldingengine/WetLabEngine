"""Substantive regression: a variant label cannot replace a metamorphic test."""
import unittest
import engine
import verify

class SchemaTests(unittest.TestCase):
    def test_original_cannot_masquerade_as_relabelled(self):
        p=(-1,0,1)
        d=engine.case(p,'U1:'+engine.code(p));d['variant']='relabeled'
        with self.assertRaisesRegex(ValueError,'declared relabel'):
            verify.verify_case(d)

    def test_omitted_storage_reversal_rejected(self):
        p=(-1,0,0)
        d=engine.case(engine.relabel(p),'U1:'+engine.code(p),reverse=False);d['variant']='relabeled'
        with self.assertRaisesRegex(ValueError,'declared storage'):
            verify.verify_case(d)

    def test_real_metamorphic_case_accepted(self):
        p=(-1,0,1)
        for var,q,rev in [('original',p,False),('relabeled',engine.relabel(p),True)]:
            d=engine.case(q,'U1:'+engine.code(p),reverse=rev);d['variant']=var
            self.assertGreater(verify.verify_case(d)['pairs'],0)

if __name__=='__main__':unittest.main(verbosity=2)
