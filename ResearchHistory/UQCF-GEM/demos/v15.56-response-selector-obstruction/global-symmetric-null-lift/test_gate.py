import importlib.util,pathlib,unittest
HERE=pathlib.Path(__file__).resolve().parent;G=HERE/"gate.py"
def load():
 if not G.exists():raise AssertionError("gate.py missing: expected RED")
 s=importlib.util.spec_from_file_location("v1563",G);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
class T(unittest.TestCase):
 @classmethod
 def setUpClass(cls):cls.g=load()
 def test_01_global_basis_dimension(self):self.assertEqual(len(self.g.BASIS),63)
 def test_02_linear_map_shapes(self):
  row=self.g.states()[0];A1,Ap=self.g.derivative_maps(row["rho"])
  self.assertEqual(A1.shape,(9,63));self.assertEqual(Ap.shape,(27,63))
 def test_03_full_measurement_has_frozen_states(self):
  r=self.g.run_measurement();self.assertEqual(len(r["rows"]),12);self.assertIn(r["verdict"],["GLOBAL_SYMMETRIC_NULL_LIFT_EXISTS","PARTIAL_GLOBAL_LIFT_ONLY","GLOBAL_LIFT_OBSTRUCTED"])
if __name__=="__main__":unittest.main()
