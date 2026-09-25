"""v15.56 Task 14 RED: native scalar carrier on retained identities."""
import unittest
import native_scalar_carrier as ns
class NativeCarrierTests(unittest.TestCase):
 def test_definition(self):
  r=ns.classify(); self.assertEqual(r["carrier"],"Map(K_R,Q)")
 def test_key(self):
  self.assertEqual(ns.classify()["identity_key"],["genesis_id","child_branch_address"])
 def test_pullback_canonical(self):
  self.assertTrue(ns.classify()["shared_key_pullback_canonical"])
 def test_no_geometry(self):
  self.assertEqual(ns.classify()["geometry_used"],[])
 def test_operator_not_imported(self):
  self.assertFalse(ns.classify()["v1545_operator_native_on_carrier"])
if __name__=="__main__": unittest.main()
