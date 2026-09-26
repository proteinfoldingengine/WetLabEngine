"""v15.56 Task 36 RED: quantitative intrinsic obstruction invariants."""
import unittest
import obstruction_invariants as oi
class T(unittest.TestCase):
 def test_rank(self): self.assertTrue(oi.classify()["rank_canonical"])
 def test_spectrum(self): self.assertTrue(oi.classify()["singular_spectrum_requires_inner_products"])
 def test_rank_formula(self): self.assertEqual(oi.classify()["connected_branch_collapse_rank"],"dim ker(P_r)")
 def test_monotonic(self): self.assertTrue(oi.classify()["kernel_dimension_monotone_under_composed_surjective_pruning"])
 def test_no_geometry(self): self.assertEqual(oi.classify()["geometry_used"],[])
if __name__=="__main__": unittest.main()
