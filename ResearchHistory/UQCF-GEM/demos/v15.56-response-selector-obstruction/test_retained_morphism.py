"""v15.56 Task 6 RED: retained lineage/recoverability cross-carrier morphism gate."""
import unittest
import retained_morphism as rm

class RetainedMorphismTests(unittest.TestCase):
 def test_source_is_retained_structure(self):
  r=rm.classify_retained_morphism()
  self.assertEqual(r["derivation_basis"],"RETAINED_LINEAGE_RECOVERABILITY_ONLY")
 def test_no_geometric_coarse_graining(self):
  self.assertEqual(rm.classify_retained_morphism()["external_maps_used"],[])
 def test_reports_status(self):
  self.assertIn(rm.classify_retained_morphism()["primary_verdict"],(
   "CANONICAL_RETAINED_MORPHISM_FOUND",
   "RETAINED_MORPHISM_NONUNIQUE",
   "NO_RETAINED_CROSS_CARRIER_MORPHISM",
   "ILL_TYPED_RETAINED_MORPHISM"))
 def test_required_preservation(self):
  r=rm.classify_retained_morphism()
  self.assertEqual(set(r["preservation_requirements"]),{
   "LINEAGE","RECOVERABILITY_ORDER","PROVENANCE","COMPOSITION"})
 def test_no_silent_map(self):
  r=rm.classify_retained_morphism()
  if r["primary_verdict"]!="CANONICAL_RETAINED_MORPHISM_FOUND":
   self.assertIsNone(r["morphism"])
if __name__=="__main__": unittest.main()
