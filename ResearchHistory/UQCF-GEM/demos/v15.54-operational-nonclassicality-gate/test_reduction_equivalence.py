"""v15.54 Task 5 RED: target-blind retained reduction and structural equivalence."""
from copy import deepcopy
from pathlib import Path
import json, unittest
import nonclassicality_contract as nc
import operational_family as of
import retained_reduction as rr
import target_equivalence as te
ROOT=Path(__file__).resolve().parents[4]
class ReductionEquivalenceTests(unittest.TestCase):
 def setUp(self):
  self.c=nc.load_contract(ROOT); self.f=of.enumerate_raw_candidates(self.c)
 def test_reduction_domain_exact(self):
  keys={"object_count","lineage_incidence","dependency_incidence","recoverability_relation","composition_table","refinement_diagram","disjoint_partition"}
  for x in self.f: self.assertEqual(set(rr.reduce_to_retained(self.c,x)),keys)
 def test_reduction_id_blind(self):
  x=deepcopy(self.f[0]); a=rr.reduce_to_retained(self.c,x); x["id"]="renamed"; self.assertEqual(a,rr.reduce_to_retained(self.c,x))
 def test_operational_table_not_retained(self):
  x=deepcopy(self.f[0]); a=rr.reduce_to_retained(self.c,x); x["operational_table"]=deepcopy(self.f[-1]["operational_table"]); self.assertEqual(a,rr.reduce_to_retained(self.c,x))
 def test_all_frozen_candidates_share_retained_readout(self):
  self.assertEqual(len({json.dumps(rr.reduce_to_retained(self.c,x),sort_keys=True) for x in self.f}),1)
 def test_self_equivalence(self):
  for x in self.f: self.assertTrue(te.are_equivalent(self.c,x,x))
 def test_symmetry(self):
  for a in self.f:
   for b in self.f: self.assertEqual(te.are_equivalent(self.c,a,b),te.are_equivalent(self.c,b,a))
 def test_id_ignored(self):
  x=deepcopy(self.f[0]); x["id"]="other"; self.assertTrue(te.are_equivalent(self.c,self.f[0],x))
 def test_distinct_carrier_sizes_inequivalent(self):
  self.assertFalse(te.are_equivalent(self.c,self.f[0],self.f[-1]))
 def test_json_roundtrip_class_key(self):
  for x in self.f: self.assertEqual(te.canonical_class_key(self.c,x),te.canonical_class_key(self.c,json.loads(json.dumps(x))))
if __name__=="__main__": unittest.main()
