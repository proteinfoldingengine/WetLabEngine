"""v15.56 Task 20 RED: provenance-protected structural product identity."""
import unittest
import product_identity as pi
class ProductIdentityTests(unittest.TestCase):
 def test_product(self):
  r=pi.classify(); self.assertEqual(r["identity"],"(genesis_id, provenance_root, full_lineage_address)")
 def test_complementary_roles(self):
  r=pi.classify()
  self.assertTrue(r["tamper_evident_provenance"])
  self.assertTrue(r["intrinsic_parent_child_incidence"])
 def test_localization_type(self):
  self.assertEqual(pi.classify()["source_localization_status"],"TYPED_IF_SOURCE_LEDGER_RECORD_BINDS_FULL_LINEAGE_ADDRESS")
 def test_no_amplitude(self):
  self.assertFalse(pi.classify()["source_amplitude_earned"])
 def test_no_geometry(self):
  self.assertEqual(pi.classify()["geometry_used"],[])
if __name__=="__main__": unittest.main()
