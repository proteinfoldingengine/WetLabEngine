import unittest
try: import independent_hidden_ensemble as e
except ModuleNotFoundError: e=None
class T(unittest.TestCase):
 def test_red(self): self.assertIsNotNone(e)
 def test_verdict(self):
  if e is None:self.skipTest("RED")
  r=e.run();self.assertEqual(r["parameters_fit_to_verdict"],0);self.assertIn(r["verdict"],["ROBUST_LINEAR_HIDDEN_GEOMETRY_RESPONSE","ROBUST_NONLINEAR_HIDDEN_GEOMETRY_RESPONSE","ENSEMBLE_NULL","INVALID_ENSEMBLE"])
if __name__=="__main__":unittest.main()
