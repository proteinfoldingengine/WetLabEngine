"""v15.56 Task 37 RED: canonical obstruction filtration under ordered pruning."""
import unittest
import obstruction_filtration as of
class T(unittest.TestCase):
 def test_kernel_flag(self): self.assertTrue(of.classify()["kernel_flag_canonical"])
 def test_strict(self): self.assertTrue(of.classify()["strict_when_each_step_prunes_new_direction"])
 def test_graded(self): self.assertEqual(of.classify()["graded_piece"],"ker(P_{0->k}) / ker(P_{0->k-1})")
 def test_dims(self): self.assertEqual(of.classify()["graded_dimension"],"n_{k-1}-n_k")
 def test_no_geometry(self): self.assertEqual(of.classify()["geometry_used"],[])
if __name__=="__main__": unittest.main()
