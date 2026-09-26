"""v15.56 Task 35 RED: intrinsic pruning obstruction class."""
import unittest
import intrinsic_defect_class as ic
class T(unittest.TestCase):
 def test_class(self): self.assertEqual(ic.classify()["intrinsic_class"],"O_r = (Q G_f)|_{ker(P_r)}")
 def test_A_independent(self): self.assertTrue(ic.classify()["independent_of_response_coarse_map"])
 def test_zero_iff(self): self.assertTrue(ic.classify()["vanishes_iff_factorization_possible"])
 def test_nontrivial(self): self.assertEqual(ic.classify()["branch_collapse_status"],"NONZERO_FOR_NONTRIVIAL_FIBERS_ON_CONNECTED_GRAPH")
 def test_no_geometry(self): self.assertEqual(ic.classify()["geometry_used"],[])
if __name__=="__main__": unittest.main()
