"""v15.56 Task 26 RED: rooted Green-response invariant diagnosis."""
import unittest
import rooted_green_invariant as rg
class RootedGreenTests(unittest.TestCase):
 def test_pair_frozen(self):
  r=rg.run(); self.assertTrue(r["cospectral_pair_frozen"])
 def test_global_spectrum_equal(self):
  self.assertLess(rg.run()["max_global_spectrum_difference"],1e-8)
 def test_rooted_spectral_measure_differs(self):
  self.assertGreater(rg.run()["rooted_spectral_measure_separation"],1e-6)
 def test_green_diagonal_differs(self):
  self.assertGreater(rg.run()["green_diagonal_separation"],1e-6)
 def test_response_explained_by_rooted_green(self):
  self.assertLess(rg.run()["response_reconstruction_error"],1e-10)
if __name__=="__main__": unittest.main()
