import importlib.util, pathlib, unittest
import numpy as np
HERE=pathlib.Path(__file__).resolve().parent
GATE=HERE/"gate.py"
def load():
    if not GATE.exists(): raise AssertionError("gate.py missing: expected RED")
    s=importlib.util.spec_from_file_location("v1558",GATE); m=importlib.util.module_from_spec(s); s.loader.exec_module(m); return m
class T(unittest.TestCase):
    @classmethod
    def setUpClass(cls): cls.g=load()
    def test_01_selector_is_deterministic_and_response_blind(self):
        g=self.g; a=g.select_states(); b=g.select_states()
        self.assertEqual([x["candidate_index"] for x in a],[x["candidate_index"] for x in b])
        self.assertEqual(len(a),12)
        forbidden={"E_exp","E_unitary","rank","response"}
        self.assertFalse(any(k in forbidden for row in a for k in row))
    def test_02_selected_states_meet_asymmetry_and_conditioning(self):
        g=self.g
        for row in g.select_states():
            d=row["diagnostics"]
            self.assertGreaterEqual(d["min_eigenvalue"],.025)
            self.assertGreaterEqual(d["min_edge_singular"],.020)
            self.assertGreaterEqual(d["holonomy_angle"],.15)
            self.assertGreaterEqual(d["pair_asymmetry"],.06)
            self.assertGreaterEqual(d["bloch_asymmetry"],.025)
    def test_03_direct_exponential_map_has_frozen_shape(self):
        g=self.g; row=g.select_states()[0]
        E=g.exponential_edge_map(row["rho"])
        self.assertEqual(E.shape,(9,243)); self.assertTrue(np.isfinite(E).all())
    def test_04_unitary_map_and_closure_have_frozen_shapes(self):
        g=self.g; row=g.select_states()[0]
        E,activity,closure=g.unitary_edge_map(row["rho"])
        self.assertEqual(E.shape,(9,243)); self.assertEqual(activity.shape,(9,)); self.assertEqual(closure.shape,(243,))
    def test_05_one_state_replicates_source_law_contrast(self):
        g=self.g; z=g.measure_state(g.select_states()[0])
        m,e=g.evaluate_arrays(z)
        self.assertEqual(e,[])
        self.assertGreater(m["ranks"]["E_exp"]["rank"],0)
        self.assertEqual(m["ranks"]["E_unitary"]["rank"],0)
        self.assertEqual(m["active_source_count"],9)
        self.assertLessEqual(m["unitary_to_exponential_norm_ratio"],g.MIXED_RATIO_TOL)
if __name__=="__main__": unittest.main()
