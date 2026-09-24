"""v15.54 Task 6 RED: exhaustive producer adjudication."""
from pathlib import Path
import unittest
import nonclassicality_contract as nc
import nonclassicality_search as ns
ROOT=Path(__file__).resolve().parents[4]
class SearchTests(unittest.TestCase):
 def setUp(self): self.c=nc.load_contract(ROOT)
 def test_deterministic(self): self.assertEqual(ns.search_frozen_family(self.c),ns.search_frozen_family(self.c))
 def test_allowed_verdict(self): self.assertIn(ns.search_frozen_family(self.c)["primary_verdict"],self.c["primary_verdicts"])
 def test_full_accounting(self):
  r=ns.search_frozen_family(self.c); self.assertEqual(r["candidate_count"],3); self.assertEqual(r["admissible_count"],3)
 def test_positive_requires_all_gates(self):
  r=ns.search_frozen_family(self.c)
  if r["primary_verdict"]=="CERTIFIED_OPERATIONAL_NONCLASSICAL_OBSTRUCTION":
   self.assertTrue(r["witness"]["same_retained_readout"]); self.assertTrue(r["witness"]["distinct_target_classes"]); self.assertTrue(r["witness"]["operational_witness_passes"]); self.assertEqual(r["witness"]["classical_comparator_status"],"NO_COMPARATOR_IN_FROZEN_CLASS")
 def test_controls_classical(self):
  r=ns.search_frozen_family(self.c); self.assertEqual(r["controls"]["V1553_PERMUTATION_CLASSICAL"],"CLASSICAL_COMPARATOR_FOUND"); self.assertEqual(r["controls"]["NONCOMMUTING_PERMUTATION_CLASSICAL"],"CLASSICAL_COMPARATOR_FOUND")
 def test_scope_firewall(self):
  r=ns.search_frozen_family(self.c); self.assertEqual(r["source_correspondence"],"NOT_EVALUATED"); self.assertEqual(r["Pillar_3"],"OPEN"); self.assertFalse(r["universal_quantum_derivation"]); self.assertFalse(r["physical_gravity"])
if __name__=="__main__": unittest.main()
