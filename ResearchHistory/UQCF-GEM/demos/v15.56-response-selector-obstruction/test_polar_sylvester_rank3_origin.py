import unittest
try: import polar_sylvester_rank3_origin as r
except ModuleNotFoundError: r=None
class T(unittest.TestCase):
 def test_red(self): self.assertIsNotNone(r)
 def test_gate(self):
  if r is None:self.skipTest("RED")
  x=r.run();self.assertEqual(x["fitted_parameters"],0)
  self.assertIn(x["verdict"],["LOCAL_SYLVESTER_RANK3","LOOP_CANCELLATION_RANK3","HYBRID_POLAR_LOOP_REDUCTION","NO_STABLE_ORIGIN","INVALID"])
if __name__=="__main__":unittest.main()
