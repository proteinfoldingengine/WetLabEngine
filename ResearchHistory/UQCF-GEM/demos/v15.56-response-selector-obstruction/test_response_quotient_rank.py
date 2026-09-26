import unittest
try:
 import response_quotient_rank as r
except ModuleNotFoundError:
 r=None
class T(unittest.TestCase):
 def test_red(self): self.assertIsNotNone(r)
 def test_gate(self):
  if r is None: self.skipTest("RED")
  x=r.run()
  self.assertEqual(x["fitted_parameters"],0)
  self.assertIn(x["verdict"],["STRONG_COLLAPSE","PARTIAL_COLLAPSE","FULL_OUTPUT_RANK","INVALID"])
if __name__=="__main__": unittest.main()
