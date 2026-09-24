"""v15.47 Task 5 RED: mechanical verdict and claim boundary."""
from pathlib import Path
import copy, unittest
import functor_contract as fc
import functor_candidates as cand
import functor_classes as classes
import verify_functoriality as vf
import gate as g

class GateTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        root=Path(__file__).resolve().parents[4]
        cls.c=fc.load_contract(root); cls.cs=cand.enumerate_candidates(cls.c)
        cls.cl=classes.surviving_classes(cls.c,cls.cs); cls.v=vf.verify(cls.c,cls.cs,cls.cl)
    def test_120_classes_adjudicates_nonselective(self):
        r=g.adjudicate(self.c,self.cl,self.v)
        self.assertEqual(r["verdict"],"FUNCTORIALITY_STILL_NONSELECTIVE")
        self.assertEqual(r["equivalence_class_count"],120)
    def test_unknown_verdict_rejected(self):
        r=g.adjudicate(self.c,self.cl,self.v); r["verdict"]="MAYBE"
        with self.assertRaisesRegex(ValueError,"verdict"): g.verify_result(r)
    def test_physical_claim_rejected(self):
        r=g.adjudicate(self.c,self.cl,self.v); r["physical_gravity"]=True
        with self.assertRaisesRegex(ValueError,"claim_boundary"): g.verify_result(r)
    def test_source_correspondence_promotion_rejected(self):
        r=g.adjudicate(self.c,self.cl,self.v); r["source_correspondence"]="CERTIFIED"
        with self.assertRaisesRegex(ValueError,"claim_boundary"): g.verify_result(r)
    def test_canonical_bytes(self):
        r=g.adjudicate(self.c,self.cl,self.v)
        self.assertEqual(g.canonical_bytes(r),g.canonical_bytes(r))
if __name__=="__main__": unittest.main()
