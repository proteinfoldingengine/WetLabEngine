"""v15.48 final RED: mechanical ill-typed adjudication."""
from pathlib import Path
import copy, unittest
import signature_contract as sc
import verify_type_obstruction as vt
import gate as g

class GateTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.root=Path(__file__).resolve().parents[4]
        cls.c=sc.load_contract(cls.root)
        cls.v=vt.verify(cls.root,cls.c)

    def test_verified_type_obstruction_adjudicates_ill_typed(self):
        r=g.adjudicate(self.c,self.v)
        self.assertEqual(r["verdict"],"RECOVERABILITY_SIGNATURE_ILL_TYPED")
        self.assertFalse(r["signature_matching_executed"])
        self.assertEqual(r["tasks_2_and_3"],"NOT_EXECUTED_BY_STOP_RULE")

    def test_unknown_verdict_rejected(self):
        r=g.adjudicate(self.c,self.v); r["verdict"]="MAYBE"
        with self.assertRaisesRegex(ValueError,"verdict"): g.verify_result(r)

    def test_physical_claim_promotion_rejected(self):
        r=g.adjudicate(self.c,self.v); r["physical_gravity"]=True
        with self.assertRaisesRegex(ValueError,"claim_boundary"): g.verify_result(r)

    def test_source_correspondence_promotion_rejected(self):
        r=g.adjudicate(self.c,self.v); r["source_correspondence"]="CERTIFIED"
        with self.assertRaisesRegex(ValueError,"claim_boundary"): g.verify_result(r)

    def test_invalid_verification_rejected(self):
        v=copy.deepcopy(self.v); v["status"]="BROKEN"
        with self.assertRaisesRegex(ValueError,"verification_status"): g.adjudicate(self.c,v)

if __name__=="__main__": unittest.main()
