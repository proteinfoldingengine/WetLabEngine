import importlib.util,pathlib,unittest
HERE=pathlib.Path(__file__).resolve().parent;G=HERE/"gate.py"
def load():
 if not G.exists(): raise AssertionError("gate.py missing: expected RED")
 s=importlib.util.spec_from_file_location("v1569",G);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
class T(unittest.TestCase):
 @classmethod
 def setUpClass(cls): cls.g=load()
 def test_01_frozen_constants(self):
  self.assertEqual(cls:=self.g.SEED,20260969); self.assertEqual(self.g.N_FRAMES,8)
 def test_02_all_cases(self):
  r=self.g.run_measurement(); self.assertEqual(r["n_states"],12); self.assertEqual(r["n_frames"],8); self.assertIn(r["verdict"],["LOCAL_FRAME_COVARIANT_NULL_CONFIRMED","LOCAL_FRAME_COVARIANT_NULL_FALSIFIED","INVALID"])
if __name__=="__main__":unittest.main()
