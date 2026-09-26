import unittest
try:import hidden_response_theorem as h
except ModuleNotFoundError:h=None
class T(unittest.TestCase):
 def test_red(self):self.assertIsNotNone(h)
 def test_gate(self):
  if h is None:self.skipTest("RED")
  r=h.run();self.assertEqual(r["fitted_coefficients"],0);self.assertIn(r["verdict"],["ANALYTIC_MIXED_RESPONSE_THEOREM_VERIFIED","ANALYTIC_FORMULA_FAILS","DEGENERATE_STRATUM"])
if __name__=="__main__":unittest.main()
