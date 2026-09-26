import unittest
try:
 import independent_hidden_geometry as m
except ModuleNotFoundError:
 m=None
class Gate(unittest.TestCase):
 def test_implementation_exists(self): self.assertIsNotNone(m)
 def test_preregistered(self):
  if m is None: self.skipTest("RED: implementation absent")
  r=m.run(); self.assertEqual(r["parameters_fit_to_response"],0)
  self.assertIn(r["verdict"],["INDEPENDENT_HIDDEN_COMPLETION_GEOMETRY_SIGNAL","NULL","INVALID_FIXTURE"])
if __name__=="__main__": unittest.main()
