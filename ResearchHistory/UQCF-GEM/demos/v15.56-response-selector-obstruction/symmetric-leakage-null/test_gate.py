import importlib.util,pathlib,unittest
HERE=pathlib.Path(__file__).resolve().parent;G=HERE/"gate.py"
def load():
 if not G.exists():raise AssertionError("gate.py missing: expected RED")
 s=importlib.util.spec_from_file_location("v1562",G);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
class T(unittest.TestCase):
 @classmethod
 def setUpClass(cls):cls.g=load()
 def test_01_basis_sizes(self):self.assertEqual(len(self.g.SYM),6);self.assertEqual(len(self.g.SKEW),3)
 def test_02_all_frozen_states_pass(self):
  r=self.g.run_measurement();self.assertEqual(r["verdict"],"SYMMETRIC_LEAKAGE_NULL_CONFIRMED");self.assertEqual(len(r["rows"]),12)
 def test_03_null_and_positive_ranks(self):
  r=self.g.run_measurement()
  for row in r["rows"]:
   self.assertEqual(row["symmetric_ranks"],[0,0,0]);self.assertEqual(row["positive_ranks"],[3,3,3])
if __name__=="__main__":unittest.main()
