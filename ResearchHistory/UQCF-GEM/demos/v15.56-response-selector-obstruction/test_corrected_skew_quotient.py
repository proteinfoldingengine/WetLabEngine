import unittest
try: import corrected_skew_quotient as q
except ModuleNotFoundError: q=None
class T(unittest.TestCase):
 def test_red(self): self.assertIsNotNone(q)
 def test_gate(self):
  if q is None: self.skipTest("RED")
  r=q.run(); self.assertEqual(r["fitted_parameters"],0)
  self.assertIn(r["verdict"],["CORRECTED_SKEW_QUOTIENT_THEOREM_VERIFIED","CORRECTED_SKEW_QUOTIENT_NONSURJECTIVE","MIXED_ORTHOGONALITY_IDENTITY_FAILS","INVALID"])
if __name__=="__main__": unittest.main()
