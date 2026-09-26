import json, pathlib, unittest
class T(unittest.TestCase):
 def test_frozen(self):
  p=json.loads(pathlib.Path("INDEPENDENT_HIDDEN_FIXTURE_FROZEN.json").read_text())
  self.assertFalse(p["hidden_response_evaluated_at_freeze"]); self.assertEqual(p["parameters_fit_to_response"],0)
  self.assertLessEqual(p["cyclic_pair_difference"],1e-12); self.assertGreater(p["holonomy_angle"],.2)
if __name__=="__main__": unittest.main()
