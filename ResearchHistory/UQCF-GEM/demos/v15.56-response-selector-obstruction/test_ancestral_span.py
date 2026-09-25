"""v15.56 Task 7 RED: common ancestral refinement span."""
import unittest
import ancestral_span as asp
class SpanTests(unittest.TestCase):
 def test_shape(self):
  r=asp.classify_span(); self.assertEqual(r["shape"],"R_m <- R_* -> R_n")
 def test_basis(self):
  self.assertEqual(asp.classify_span()["derivation_basis"],"COMMON_RETAINED_LINEAGE")
 def test_no_geometry(self):
  self.assertEqual(asp.classify_span()["external_maps_used"],[])
 def test_verdict(self):
  self.assertIn(asp.classify_span()["primary_verdict"],(
   "CANONICAL_ANCESTRAL_SPAN_FOUND","ANCESTRAL_SPAN_NONUNIQUE",
   "NO_COMMON_ANCESTRAL_SPAN","ILL_TYPED_ANCESTRAL_SPAN"))
 def test_canonical_requires_universal_property(self):
  r=asp.classify_span()
  if r["primary_verdict"]=="CANONICAL_ANCESTRAL_SPAN_FOUND":
   self.assertTrue(r["universal_property_verified"])
if __name__=="__main__": unittest.main()
