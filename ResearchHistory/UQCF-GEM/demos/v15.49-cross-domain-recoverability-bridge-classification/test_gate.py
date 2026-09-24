"""v15.49 final RED: mechanical ill-typed bridge adjudication."""
from pathlib import Path
import copy, unittest
import bridge_contract as bc
import verify_bridge_typing as vt
import gate as g

class GateTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.root=Path(__file__).resolve().parents[4]
        cls.c=bc.load_contract(cls.root); cls.v=vt.verify(cls.root,cls.c)
    def test_verified_obstruction_adjudicates_ill_typed(self):
        r=g.adjudicate(cls_contract:=self.c,verification:=self.v)
        self.assertEqual(r["verdict"],"BRIDGE_ILL_TYPED")
        self.assertFalse(r["bridge_enumeration_executed"])
        self.assertEqual(r["tasks_2_and_3"],"NOT_EXECUTED_BY_TYPE_GATE")
    def test_unknown_verdict_rejected(self):
        r=g.adjudicate(self.c,self.v); r["verdict"]="MAYBE"
        with self.assertRaisesRegex(ValueError,"verdict"): g.verify_result(r)
    def test_physical_claim_rejected(self):
        r=g.adjudicate(self.c,self.v); r["physical_gravity"]=True
        with self.assertRaisesRegex(ValueError,"claim_boundary"): g.verify_result(r)
    def test_invalid_verification_rejected(self):
        v=copy.deepcopy(self.v); v["status"]="BROKEN"
        with self.assertRaisesRegex(ValueError,"verification_status"): g.adjudicate(self.c,v)
if __name__=="__main__": unittest.main()
