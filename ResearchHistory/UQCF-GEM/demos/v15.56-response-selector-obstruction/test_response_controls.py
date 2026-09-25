"""v15.56 Task 24 RED: executable native response controls."""
import unittest
import response_controls as rc
class Controls(unittest.TestCase):
 def test_families(self):
  r=rc.run(); self.assertGreaterEqual(r["tree_count"],4)
 def test_residual(self):
  self.assertLess(r:=rc.run()["max_poisson_residual"],1e-10)
 def test_relabel(self):
  self.assertLess(rc.run()["max_relabeling_error"],1e-10)
 def test_scale(self):
  self.assertLess(rc.run()["max_projective_scale_error"],1e-10)
 def test_null(self):
  self.assertLess(rc.run()["max_null_response_norm"],1e-10)
 def test_topology_signal(self):
  self.assertGreater(rc.run()["min_nonisomorphic_shape_separation"],1e-3)
if __name__=="__main__": unittest.main()
