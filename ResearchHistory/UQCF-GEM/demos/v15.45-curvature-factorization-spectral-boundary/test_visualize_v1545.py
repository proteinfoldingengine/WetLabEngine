"""Checks that the visualization reproduces the published v15.45 exact certificates."""
import unittest
import visualize_v1545 as v
class VizTests(unittest.TestCase):
 def test_exact_certificates(self):
  for L,expected in v.CERTIFIED.items(): self.assertEqual(v.verify_exact(L),expected)
 def test_odd_conditioning(self):
  self.assertAlmostEqual(v.centered_finite_condition(5),2.61803398875,places=8)
  self.assertAlmostEqual(v.centered_finite_condition(7),5.04891733952,places=8)
if __name__=="__main__": unittest.main()
