"""v15.56 Task 15 RED: intrinsic retained-incidence classification."""
import unittest
import retained_incidence as ri
class IncidenceTests(unittest.TestCase):
 def test_candidates(self):
  r=ri.classify()
  self.assertEqual(set(r["candidates"]),{
   "PARENT_CHILD_LINEAGE","REPAIR_SUCCESSION","RECOVERABILITY_COVER","DEPENDENCY"})
 def test_no_preferred_for_laplacian(self):
  self.assertFalse(ri.classify()["selected_by_operator_goal"])
 def test_intrinsic_status(self):
  for x in ri.classify()["relations"]:
   self.assertIn(x["status"],("INTRINSIC","CONDITIONAL","NOT_DEFINED_ON_IDENTITY_SET"))
 def test_no_geometry(self):
  self.assertEqual(ri.classify()["geometry_used"],[])
if __name__=="__main__": unittest.main()
