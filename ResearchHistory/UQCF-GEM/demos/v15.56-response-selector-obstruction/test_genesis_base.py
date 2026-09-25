"""v15.56 Task 8 RED: shared Genesis Pin as minimal comparison base."""
import unittest
import genesis_base as gb
class GenesisBaseTests(unittest.TestCase):
 def test_role(self):
  r=gb.classify_genesis_base(); self.assertEqual(r["candidate_role"],"COMMON_PROVENANCE_BASE")
 def test_not_assume_shared_pin(self):
  r=gb.classify_genesis_base(); self.assertFalse(r["shared_pin_assumed"])
 def test_verdict(self):
  self.assertIn(gb.classify_genesis_base()["primary_verdict"],(
   "GENESIS_PIN_CANONICAL_BASE","GENESIS_PIN_INSUFFICIENT_BASE",
   "SHARED_PIN_WITNESS_REQUIRED","ILL_TYPED_GENESIS_BASE"))
 def test_require_descent_maps(self):
  self.assertEqual(gb.classify_genesis_base()["required_maps"],["G_TO_R_m","G_TO_R_n"])
 def test_no_geometry(self):
  self.assertEqual(gb.classify_genesis_base()["external_geometry_used"],[])
if __name__=="__main__": unittest.main()
