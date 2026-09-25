"""v15.56 Task 2 RED: audit richer pre-existing structures for nontrivial Q4 action."""
import json, unittest
from pathlib import Path
import selector_audit as sa
HERE=Path(__file__).resolve().parent

class SelectorAuditTests(unittest.TestCase):
 def setUp(self): self.c=json.loads((HERE/"contract.json").read_text())
 def test_audit_is_preexisting_only(self):
  r=sa.audit(self.c); self.assertEqual(r["post_v1555_structures_used"],[])
 def test_each_structure_typed(self):
  r=sa.audit(self.c)
  for x in r["audited_structures"]:
   self.assertIn(x["status"],("INDUCED_ACTION_DEFINED","NO_CANONICAL_INDUCED_ACTION"))
 def test_no_identity_assumption_for_untyped_maps(self):
  r=sa.audit(self.c)
  for x in r["audited_structures"]:
   if x["status"]=="NO_CANONICAL_INDUCED_ACTION": self.assertIsNone(x["matrix"])
 def test_classification_scope(self):
  r=sa.audit(self.c)
  self.assertIn(r["primary_verdict"],("SELECTOR_NONUNIQUE","NO_EARNED_SELECTOR","CANONICAL_SELECTOR_FOUND"))
 def test_canonical_requires_defined_action_and_normalization(self):
  r=sa.audit(self.c)
  if r["primary_verdict"]=="CANONICAL_SELECTOR_FOUND":
   self.assertTrue(r["earned_normalization"])
   self.assertEqual(r["invariant_dimension"],1)
if __name__=="__main__": unittest.main()
