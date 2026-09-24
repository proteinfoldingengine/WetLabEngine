"""v15.54 Task 4 RED: exact Bell-local classical comparator."""
from pathlib import Path
import unittest
import nonclassicality_contract as nc
import operational_family as of
import classical_comparator as cc
ROOT=Path(__file__).resolve().parents[4]
class ComparatorTests(unittest.TestCase):
 def setUp(self):
  self.c=nc.load_contract(ROOT); self.f=of.enumerate_raw_candidates(self.c)
 def role(self,r): return next(x for x in self.f if x["control_role"]==r)
 def test_extremal_count_complete(self):
  self.assertEqual(len(cc.enumerate_extremal_models(self.c)),16)
 def test_v1553_control_has_comparator(self):
  r=cc.find_classical_comparator(self.c,self.role("V1553_PERMUTATION_CLASSICAL")["operational_table"]); self.assertEqual(r["status"],"CLASSICAL_COMPARATOR_FOUND")
 def test_noncommuting_control_has_comparator(self):
  r=cc.find_classical_comparator(self.c,self.role("NONCOMMUTING_PERMUTATION_CLASSICAL")["operational_table"]); self.assertEqual(r["status"],"CLASSICAL_COMPARATOR_FOUND")
 def test_chsh_candidate_has_no_comparator(self):
  r=cc.find_classical_comparator(self.c,self.role("OPERATIONAL_CANDIDATE")["operational_table"]); self.assertEqual(r["status"],"NO_COMPARATOR_IN_FROZEN_CLASS")
 def test_bad_normalization_rejected(self):
  t={k:{o:list(v) for o,v in row.items()} for k,row in self.role("V1553_PERMUTATION_CLASSICAL")["operational_table"].items()}; t["x0y0"]["00"]=[1,1]
  with self.assertRaises(ValueError): cc.find_classical_comparator(self.c,t)
 def test_negative_rejected(self):
  t={k:{o:list(v) for o,v in row.items()} for k,row in self.role("V1553_PERMUTATION_CLASSICAL")["operational_table"].items()}; t["x0y0"]["00"]=[-1,2]
  with self.assertRaises(ValueError): cc.find_classical_comparator(self.c,t)
 def test_bound_recorded(self):
  r=cc.find_classical_comparator(self.c,self.role("OPERATIONAL_CANDIDATE")["operational_table"]); self.assertEqual(r["ontic_bound"],self.c["classical_ontic_bound"])
if __name__=="__main__": unittest.main()
