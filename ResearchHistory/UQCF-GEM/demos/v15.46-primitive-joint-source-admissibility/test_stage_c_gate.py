"""Stage C5 RED: mechanical adjudication and claim boundary."""
import copy, unittest
from pathlib import Path
import stage_c_contract as sc
import stage_c_nonuniqueness as sn
import stage_c_verify as sv
import stage_c_gate as sg

class StageCGateTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        root=Path(__file__).resolve().parents[4]
        cls.c=sc.load_contract(root)
        cls.w=sn.find_witness(cls.c)
        cls.v=sv.verify_witness(cls.c,cls.w)

    def test_verified_pair_adjudicates_nonunique(self):
        r=sg.adjudicate(self.c,self.w,self.v)
        self.assertEqual(r["verdict"],"REPRESENTATION_NONUNIQUE")
        self.assertEqual(r["source_correspondence"],"NOT_EVALUATED")
        self.assertEqual(r["Pillar_3"],"OPEN")
        self.assertFalse(r["physical_gravity"])

    def test_unverified_witness_rejected(self):
        v=copy.deepcopy(self.v); v["status"]="BROKEN"
        with self.assertRaisesRegex(ValueError,"verification_status"):
            sg.adjudicate(self.c,self.w,v)

    def test_physical_claim_promotion_rejected(self):
        r=sg.adjudicate(self.c,self.w,self.v)
        r["physical_gravity"]=True
        with self.assertRaisesRegex(ValueError,"claim_boundary"):
            sg.verify_result(r)

    def test_unknown_verdict_rejected(self):
        r=sg.adjudicate(self.c,self.w,self.v)
        r["verdict"]="MAYBE"
        with self.assertRaisesRegex(ValueError,"verdict"):
            sg.verify_result(r)

    def test_canonical_bytes_deterministic(self):
        r=sg.adjudicate(self.c,self.w,self.v)
        self.assertEqual(sg.canonical_bytes(r),sg.canonical_bytes(r))

if __name__=="__main__": unittest.main()
