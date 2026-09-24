"""v15.55 Task 2 RED: derive defect D from certified v15.54 data."""
from copy import deepcopy
from pathlib import Path
import sys, unittest
HERE=Path(__file__).resolve().parent
V54=HERE.parent/"v15.54-operational-nonclassicality-gate"
sys.path.insert(0,str(V54))
import nonclassicality_contract as nc
import operational_family as of
import defect_datum as dd

class DefectTests(unittest.TestCase):
 def setUp(self):
  self.c=nc.load_contract(HERE.parents[3])
  self.f=of.enumerate_raw_candidates(self.c)
 def role(self,r): return next(x for x in self.f if x["control_role"]==r)
 def test_candidate_defect_nonzero(self):
  d=dd.derive_defect(self.c,self.role("OPERATIONAL_CANDIDATE")); self.assertTrue(d["active"])
 def test_classical_controls_zero(self):
  for r in ("V1553_PERMUTATION_CLASSICAL","NONCOMMUTING_PERMUTATION_CLASSICAL"):
   self.assertFalse(dd.derive_defect(self.c,self.role(r))["active"])
 def test_id_blind(self):
  x=deepcopy(self.role("OPERATIONAL_CANDIDATE")); a=dd.derive_defect(self.c,x); x["id"]="renamed"; self.assertEqual(a,dd.derive_defect(self.c,x))
 def test_no_nonclassical_flag_input(self):
  x=deepcopy(self.role("OPERATIONAL_CANDIDATE")); x["nonclassical"]=True
  with self.assertRaises(ValueError): dd.derive_defect(self.c,x)
 def test_exact_score(self):
  d=dd.derive_defect(self.c,self.role("OPERATIONAL_CANDIDATE")); self.assertEqual(d["excess_over_frozen_bound"],[2,1])
 def test_no_response_encoded(self):
  d=dd.derive_defect(self.c,self.role("OPERATIONAL_CANDIDATE")); self.assertNotIn("response",d); self.assertNotIn("delta_A",d); self.assertNotIn("eta",d)
if __name__=="__main__": unittest.main()
