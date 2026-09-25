"""v15.56 Task 23 RED: projective native Poisson response."""
import unittest
import projective_poisson as pp
class PoissonTests(unittest.TestCase):
 def test_equation(self):
  self.assertEqual(pp.classify()["equation"],"Delta_lin phi = J - component_mean(J)")
 def test_solvability(self):
  self.assertTrue(pp.classify()["rhs_orthogonal_to_kernel"])
 def test_projective_covariance(self):
  r=pp.classify(); self.assertEqual(r["source_scaling_law"],"J->aJ implies phi->a phi modulo kernel")
 def test_unique_gauge(self):
  self.assertEqual(pp.classify()["gauge_fix"],"zero_mean_on_each_connected_component")
 def test_no_geometry(self):
  self.assertEqual(pp.classify()["geometry_used"],[])
if __name__=="__main__": unittest.main()
