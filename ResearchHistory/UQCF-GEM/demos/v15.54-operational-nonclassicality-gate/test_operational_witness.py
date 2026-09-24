"""v15.54 Task 3 RED: exact CHSH operational witness."""
from copy import deepcopy
from pathlib import Path
import unittest
import nonclassicality_contract as nc
import operational_family as of
import operational_witness as ow
ROOT=Path(__file__).resolve().parents[4]
class WitnessTests(unittest.TestCase):
 def setUp(self):
  self.c=nc.load_contract(ROOT); self.f=of.enumerate_raw_candidates(self.c)
 def byrole(self,r): return next(x for x in self.f if x["control_role"]==r)
 def test_classical_v1553_control_does_not_pass(self):
  self.assertFalse(ow.evaluate_witness(self.c,self.byrole("V1553_PERMUTATION_CLASSICAL"))["passes"])
 def test_noncommuting_classical_control_does_not_pass(self):
  self.assertFalse(ow.evaluate_witness(self.c,self.byrole("NONCOMMUTING_PERMUTATION_CLASSICAL"))["passes"])
 def test_preregistered_candidate_passes(self):
  self.assertTrue(ow.evaluate_witness(self.c,self.byrole("OPERATIONAL_CANDIDATE"))["passes"])
 def test_id_blind(self):
  x=deepcopy(self.byrole("OPERATIONAL_CANDIDATE")); a=ow.evaluate_witness(self.c,x); x["id"]="other"; self.assertEqual(a,ow.evaluate_witness(self.c,x))
 def test_internal_operation_labels_blind(self):
  x=deepcopy(self.byrole("OPERATIONAL_CANDIDATE")); a=ow.evaluate_witness(self.c,x); x["operations"]=list(reversed(x["operations"])); self.assertEqual(a,ow.evaluate_witness(self.c,x))
 def test_mutation_closes_witness(self):
  x=deepcopy(self.byrole("OPERATIONAL_CANDIDATE")); x["operational_table"]["x1y1"]={"00":[1,2],"01":[0,1],"10":[0,1],"11":[1,2]}; self.assertFalse(ow.evaluate_witness(self.c,x)["passes"])
 def test_missing_context_rejected(self):
  x=deepcopy(self.byrole("OPERATIONAL_CANDIDATE")); del x["operational_table"]["x1y1"]
  with self.assertRaises(ValueError): ow.evaluate_witness(self.c,x)
 def test_exact_score(self):
  r=ow.evaluate_witness(self.c,self.byrole("OPERATIONAL_CANDIDATE")); self.assertEqual(r["score"],[4,1]); self.assertEqual(r["bound"],[2,1])
if __name__=="__main__": unittest.main()
