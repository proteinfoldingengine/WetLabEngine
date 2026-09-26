import unittest
try: import rank3_image_decomposition as r
except ModuleNotFoundError: r=None
class T(unittest.TestCase):
 def test_red(self): self.assertIsNotNone(r)
 def test_gate(self):
  if r is None: self.skipTest("RED")
  x=r.run(); self.assertEqual(x["fitted_parameters"],0)
  self.assertIn(x["verdict"],["PURE_SKEW","PURE_SYMMETRIC_TRACELESS","MIXED_INVARIANT_DECOMPOSITION","IRREDUCIBLY_MIXED_IMAGE","INVALID"])
if __name__=="__main__": unittest.main()
