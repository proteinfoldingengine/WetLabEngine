"""v15.56 Task 34 RED: pruning defect operator and composition gate."""
import unittest
import pruning_defect_cocycle as pd
class T(unittest.TestCase):
 def test_defect(self): self.assertEqual(pd.classify()["defect_operator"],"D_r = Q_c A_r G_f - G_c P_r")
 def test_composition(self): self.assertTrue(pd.classify()["composition_identity_derived"])
 def test_no_geometry(self): self.assertEqual(pd.classify()["geometry_used"],[])
 def test_status(self): self.assertIn(pd.classify()["cocycle_status"],("CANONICAL_AFTER_RESPONSE_MAP_FIXED","NOT_CANONICAL_WITHOUT_RESPONSE_MAP","EXACT_COCYCLE_EARNED"))
if __name__=="__main__": unittest.main()
