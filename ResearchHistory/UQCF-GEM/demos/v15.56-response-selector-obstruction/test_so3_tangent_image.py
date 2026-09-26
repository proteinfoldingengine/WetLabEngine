import unittest
try: import so3_tangent_image as s
except ModuleNotFoundError: s=None
class T(unittest.TestCase):
 def test_red(self): self.assertIsNotNone(s)
 def test_gate(self):
  if s is None: self.skipTest("RED")
  r=s.run(); self.assertEqual(r["fitted_parameters"],0)
  self.assertIn(r["verdict"],["SO3_TANGENT_IMAGE_SURJECTIVE","SO3_TANGENT_IMAGE_NONSURJECTIVE","SO3_TANGENCY_FAILS","INVALID"])
if __name__=="__main__": unittest.main()
