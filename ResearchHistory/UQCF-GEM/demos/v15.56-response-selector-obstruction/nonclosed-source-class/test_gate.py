import importlib.util,pathlib,unittest,numpy as np
HERE=pathlib.Path(__file__).resolve().parent; GATE=HERE/"gate.py"
def load():
 if not GATE.exists(): raise AssertionError("gate.py missing: expected RED")
 s=importlib.util.spec_from_file_location("v1559",GATE);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
class T(unittest.TestCase):
 @classmethod
 def setUpClass(cls):cls.g=load();cls.row=cls.g.states()[0]
 def test_01_frozen_states(self):
  self.assertEqual([x["candidate_index"] for x in self.g.states()],[13,16,22,25,27,29,37,39,46,50,66,77])
 def test_02_filter_preserves_density_matrix(self):
  g=self.g;r=self.row["rho"];z=g.filter_update(r,g.S_FILTER,g.R.PB[0])
  self.assertLess(np.linalg.norm(z-z.conj().T),1e-12);self.assertLess(abs(np.trace(z)-1),1e-12);self.assertGreater(np.linalg.eigvalsh(z).min(),-1e-12)
 def test_03_filter_measurement_shapes(self):
  g=self.g;E,a,n=g.filter_edge_map(self.row["rho"])
  self.assertEqual(E.shape,(9,243));self.assertEqual(a.shape,(9,));self.assertEqual(n.shape,(243,));self.assertTrue(np.isfinite(E).all())
 def test_04_filter_is_active_and_nonclosed(self):
  g=self.g;z=g.measure_state(self.row);m,e=g.evaluate_arrays(z)
  self.assertEqual(e,[]);self.assertEqual(m["active_source_count"],9);self.assertGreater(m["max_nonclosure"],g.NONCLOSURE_MIN)
 def test_05_second_nonclosed_law_has_nonzero_response(self):
  g=self.g;z=g.measure_state(self.row);m,e=g.evaluate_arrays(z)
  self.assertEqual(e,[]);self.assertGreater(m["ranks"]["E_filter"]["rank"],0);self.assertGreater(m["ranks"]["E_exp"]["rank"],0)
if __name__=="__main__":unittest.main()
