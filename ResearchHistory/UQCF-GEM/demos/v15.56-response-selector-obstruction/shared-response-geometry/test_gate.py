import importlib.util,pathlib,unittest,numpy as np
HERE=pathlib.Path(__file__).resolve().parent;G=HERE/"gate.py"
def load():
 if not G.exists():raise AssertionError("gate.py missing: expected RED")
 s=importlib.util.spec_from_file_location("v1560",G);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
class T(unittest.TestCase):
 @classmethod
 def setUpClass(cls):cls.g=load();cls.row=cls.g.states()[0]
 def test_01_amplitudes_frozen(self):self.assertEqual(self.g.AMPLITUDES,[.0685,.137,.274])
 def test_02_projector_geometry_identity(self):
  g=self.g;E=g.ASYM.exponential_edge_map(self.row["rho"]);P=g.projector(E)
  self.assertLess(np.linalg.norm(P@P-P),1e-10);self.assertAlmostEqual(np.trace(P),9,places=8)
 def test_03_measure_state_has_all_amplitudes(self):
  z=self.g.measure_state(self.row)
  self.assertEqual(sorted(z["filter_maps"]),self.g.AMPLITUDES)
  self.assertEqual(z["E_exp"].shape,(9,243))
  for E in z["filter_maps"].values():self.assertEqual(E.shape,(9,243))
 def test_04_controls_and_geometry_pass_sample(self):
  m,e=self.g.evaluate(self.g.measure_state(self.row));self.assertEqual(e,[])
  self.assertEqual(m["exp_rank"],9);self.assertEqual(m["filter_ranks"],[9,9,9])
  self.assertEqual(len(m["exp_filter_min_cosines"]),3)
  self.assertEqual(len(m["filter_pair_projector_distances"]),3)
if __name__=="__main__":unittest.main()
