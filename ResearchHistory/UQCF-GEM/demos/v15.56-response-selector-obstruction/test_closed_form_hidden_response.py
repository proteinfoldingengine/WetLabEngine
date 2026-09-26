import unittest
try:import closed_form_hidden_response as c
except ModuleNotFoundError:c=None
class T(unittest.TestCase):
 def test_red(self):self.assertIsNotNone(c)
 def test_gate(self):
  if c is None:self.skipTest("RED")
  r=c.run();self.assertEqual(r["fitted_coefficients"],0);self.assertFalse(r["numerical_derivative_inside_closed_form"]);self.assertIn(r["verdict"],["CLOSED_FORM_MIXED_RESPONSE_THEOREM_VERIFIED","CLOSED_FORM_FORMULA_FAILS","DEGENERATE_STRATUM"])
if __name__=="__main__":unittest.main()
