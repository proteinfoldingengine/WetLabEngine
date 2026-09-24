"""v15.54 Task 2 RED: exact operational candidate family."""
from copy import deepcopy
import json, unittest
import nonclassicality_contract as nc
import operational_family as of
from pathlib import Path
ROOT=Path(__file__).resolve().parents[4]
class FamilyTests(unittest.TestCase):
 def setUp(self):
  self.c=nc.load_contract(ROOT); self.family=of.enumerate_raw_candidates(self.c)
 def test_finite_deterministic_nonempty(self):
  self.assertGreaterEqual(len(self.family),3); self.assertEqual(self.family,of.enumerate_raw_candidates(self.c))
 def test_unique_records(self):
  self.assertEqual(len({of.canonical_candidate(x,ignore_id=True) for x in self.family}),len(self.family))
 def test_all_baselines_admissible(self):
  for x in self.family: self.assertTrue(of.check_admissibility(self.c,x)["admissible"])
 def test_exact_probability_normalization(self):
  for x in self.family:
   for row in x["operational_table"].values():
    self.assertEqual(sum(n/d for n,d in row.values()),1)
 def test_id_is_metadata(self):
  x=deepcopy(self.family[0]); a=of.check_admissibility(self.c,x); x["id"]="renamed"; b=of.check_admissibility(self.c,x); self.assertEqual(a,b)
 def test_forbidden_target_status_rejected(self):
  for key in ("target_class","nonclassical","E_observables"):
   x=deepcopy(self.family[0]); x[key]=True; self.assertFalse(of.check_admissibility(self.c,x)["admissible"])
 def test_negative_probability_rejected(self):
  x=deepcopy(self.family[0]); x["operational_table"]["x0y0"]["00"]=[-1,2]; self.assertFalse(of.check_admissibility(self.c,x)["admissible"])
 def test_bad_normalization_rejected(self):
  x=deepcopy(self.family[0]); x["operational_table"]["x0y0"]["00"]=[1,1]; self.assertFalse(of.check_admissibility(self.c,x)["admissible"])
 def test_zero_denominator_rejected(self):
  x=deepcopy(self.family[0]); x["operational_table"]["x0y0"]["00"]=[1,0]; self.assertFalse(of.check_admissibility(self.c,x)["admissible"])
 def test_missing_context_rejected(self):
  x=deepcopy(self.family[0]); del x["operational_table"]["x1y1"]; self.assertFalse(of.check_admissibility(self.c,x)["admissible"])
 def test_json_roundtrip(self):
  for x in self.family: self.assertEqual(of.check_admissibility(self.c,x),of.check_admissibility(self.c,json.loads(json.dumps(x))))
 def test_controls_present(self):
  roles={x["control_role"] for x in self.family}; self.assertIn("V1553_PERMUTATION_CLASSICAL",roles); self.assertIn("NONCOMMUTING_PERMUTATION_CLASSICAL",roles); self.assertIn("OPERATIONAL_CANDIDATE",roles)
if __name__=="__main__": unittest.main()
