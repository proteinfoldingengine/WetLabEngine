import importlib.util,pathlib,unittest
HERE=pathlib.Path(__file__).resolve().parent;G=HERE/"gate.py"
def load():
 if not G.exists():raise AssertionError("gate.py missing: expected RED")
 s=importlib.util.spec_from_file_location("v1567",G);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
class T(unittest.TestCase):
 @classmethod
 def setUpClass(cls):cls.g=load()
 def test_01_frozen_case(self):self.assertEqual(self.g.CANDIDATE,13);self.assertEqual(self.g.T,1e-3)
 def test_02_audit_returns_named_verdict(self):
  r=self.g.audit();self.assertIn(r["verdict"],["STATE_MISMATCH","MOMENT_MISMATCH","CORRELATION_MISMATCH","GRAM_MISMATCH","POLAR_MISMATCH","PATHS_IDENTICAL_AT_FROZEN_CORNER","INVALID"])
if __name__=="__main__":unittest.main()
