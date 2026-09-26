import importlib.util,pathlib,unittest,numpy as np
HERE=pathlib.Path(__file__).resolve().parent;G=HERE/"gate.py"
def load():
 if not G.exists():raise AssertionError("gate.py missing: expected RED")
 s=importlib.util.spec_from_file_location("v1564",G);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
class T(unittest.TestCase):
 @classmethod
 def setUpClass(cls):cls.g=load()
 def test_01_hidden_has_zero_retained_marginals(self):self.assertLess(self.g.hidden_marginal_norm(),1e-12)
 def test_02_all_states_realize_vector_field_null(self):
  r=self.g.run_measurement();self.assertEqual(r["verdict"],"SOURCE_VECTOR_FIELD_NULL_REALIZED");self.assertEqual(len(r["rows"]),12)
 def test_03_finite_states_positive(self):
  r=self.g.run_measurement()
  self.assertGreaterEqual(min(x["min_finite_eigenvalue"] for x in r["rows"]),-1e-12)
if __name__=="__main__":unittest.main()
