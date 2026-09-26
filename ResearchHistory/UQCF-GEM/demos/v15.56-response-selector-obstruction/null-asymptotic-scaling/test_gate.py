import importlib.util,pathlib,unittest
HERE=pathlib.Path(__file__).resolve().parent;G=HERE/"gate.py"
def load():
 if not G.exists():raise AssertionError("gate.py missing: expected RED")
 s=importlib.util.spec_from_file_location("v1565",G);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
class T(unittest.TestCase):
 @classmethod
 def setUpClass(cls):cls.g=load()
 def test_01_amplitude_ladder(self):self.assertEqual(self.g.TS,[1e-3,5e-4,2.5e-4,1.25e-4,6.25e-5])
 def test_02_all_states_adjudicated(self):
  r=self.g.run_measurement();self.assertEqual(len(r["rows"]),12);self.assertIn(r["verdict"],["NULL_DERIVATIVE_ASYMPTOTICS_CONFIRMED","NULL_DERIVATIVE_ASYMPTOTICS_NOT_CONFIRMED"])
if __name__=="__main__":unittest.main()
