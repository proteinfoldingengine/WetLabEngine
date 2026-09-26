import importlib.util,pathlib,unittest
HERE=pathlib.Path(__file__).resolve().parent;G=HERE/"gate.py"
def load():
 if not G.exists():raise AssertionError("gate.py missing: expected RED")
 s=importlib.util.spec_from_file_location("v1566",G);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
class T(unittest.TestCase):
 @classmethod
 def setUpClass(cls):cls.g=load()
 def test_01_precision_and_ladders_frozen(self):
  self.assertEqual(self.g.MP_DPS,80);self.assertEqual(self.g.FLOAT_TS,[1e-2,3e-3,1e-3,3e-4,1e-4,3e-5])
 def test_02_all_states_adjudicated(self):
  r=self.g.run_measurement();self.assertEqual(len(r["rows"]),12);self.assertIn(r["verdict"],["NUMERICAL_CANCELLATION_CONFIRMED","ANALYTIC_NUMERIC_DISAGREEMENT","ANALYTIC_FACTOR_INVALID","INVALID"])
if __name__=="__main__":unittest.main()
