"""v15.56 Task 27 RED: rooted-response refinement naturality gate."""
import unittest
import refinement_naturality as rn
class T(unittest.TestCase):
 def test_object(self): self.assertEqual(rn.classify()["object"],"ROOTED_PROJECTIVE_GREEN_RESPONSE")
 def test_lawful(self): self.assertTrue(rn.classify()["requires_lineage_preserving_refinement"])
 def test_verdict(self): self.assertIn(rn.classify()["primary_verdict"],("REFINEMENT_NATURALITY_EARNED","REFINEMENT_NATURALITY_FAILS","REFINEMENT_MAP_CLASS_UNDERSPECIFIED"))
 def test_no_geometry(self): self.assertEqual(rn.classify()["geometry_used"],[])
if __name__=="__main__": unittest.main()
