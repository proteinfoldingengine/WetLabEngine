import unittest, independent_hidden_fixture as f
class T(unittest.TestCase):
 def test_freeze(self):
  r=f.run(); self.assertFalse(r["hidden_response_evaluated"]); self.assertEqual(r["parameters_fit_to_response"],0)
  self.assertGreaterEqual(r["fixture"]["min_eigenvalue"],.03); self.assertGreaterEqual(r["fixture"]["pair_singular_min"],.02); self.assertGreaterEqual(r["fixture"]["holonomy_angle"],.20); self.assertLessEqual(r["fixture"]["cyclic_pair_difference"],1e-12)
 def test_deterministic(self): self.assertEqual(f.run(),f.run())
if __name__=="__main__": unittest.main()
