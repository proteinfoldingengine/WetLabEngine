"""v15.56 Task 9 RED: Genesis Pin + repair-history descendant correspondence."""
import unittest
import descent_correspondence as dc
class DescentTests(unittest.TestCase):
 def test_input_object(self):
  r=dc.classify_correspondence()
  self.assertEqual(r["input_object"],"GENESIS_PIN_PLUS_CERTIFIED_DESCENT_REPAIR_HISTORY")
 def test_exact_outcome(self):
  r=dc.classify_correspondence()
  self.assertIn(r["primary_verdict"],(
   "UNIQUE_DESCENDANT_CORRESPONDENCE","DESCENDANT_CORRESPONDENCE_NONUNIQUE",
   "NO_DESCENDANT_CORRESPONDENCE","ILL_TYPED_DESCENT_HISTORY"))
 def test_no_carrier_geometry(self):
  self.assertEqual(dc.classify_correspondence()["carrier_geometry_used"],[])
 def test_preserves_native_data(self):
  r=dc.classify_correspondence()
  self.assertEqual(set(r["preserves"]),{
   "GENESIS_PROVENANCE","LINEAGE_ADDRESS","REPAIR_ORDER","RECOVERABILITY_ORDER"})
 def test_unique_requires_single_equivalence_class(self):
  r=dc.classify_correspondence()
  if r["primary_verdict"]=="UNIQUE_DESCENDANT_CORRESPONDENCE":
   self.assertEqual(r["correspondence_classes"],1)
if __name__=="__main__": unittest.main()
