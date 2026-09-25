"""v15.56 Task 17 RED: native source-to-lineage bridge typing."""
import unittest
import native_source_bridge as nb
class BridgeTests(unittest.TestCase):
 def test_spaces(self):
  r=nb.classify()
  self.assertEqual(r["source"],"V1555_RESPONSE_Q4")
  self.assertEqual(r["target"],"Map(K_R,Q)")
 def test_locality_basis(self):
  self.assertEqual(nb.classify()["attachment_basis"],"RETAINED_IDENTITY_AND_INTRINSIC_LINEAGE_ONLY")
 def test_no_selector_smuggling(self):
  self.assertEqual(nb.classify()["chosen_q4_coefficients"],None)
 def test_reports_obstruction_or_family(self):
  self.assertIn(nb.classify()["primary_verdict"],(
   "CANONICAL_NATIVE_BRIDGE_FOUND","NATIVE_BRIDGE_NONUNIQUE",
   "NO_NATIVE_BRIDGE_FROM_CURRENT_DATA","ILL_TYPED_NATIVE_BRIDGE"))
 def test_no_geometry(self):
  self.assertEqual(nb.classify()["geometry_used"],[])
if __name__=="__main__": unittest.main()
