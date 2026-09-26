import importlib.util
import json
import pathlib
import tempfile
import unittest
import numpy as np

HERE=pathlib.Path(__file__).resolve().parent
GATE=HERE/"gate.py"

def load_gate():
    if not GATE.exists():
        raise AssertionError("gate.py missing: expected RED before implementation")
    spec=importlib.util.spec_from_file_location("source_law_specificity_gate",GATE)
    mod=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

class T(unittest.TestCase):
    def test_01_constants_are_frozen(self):
        g=load_gate()
        self.assertEqual(g.ETA,1e-3)
        self.assertEqual(g.S,0.137)
        self.assertEqual(len(g.FIXTURES),11)
        self.assertEqual(len(g.R.HB)*len(g.R.PB),243)

    def test_02_local_unitary_update_preserves_density_properties(self):
        g=load_gate()
        rho=g.F.state(*g.FIXTURES[0]); p=g.R.PB[0]
        out=g.local_unitary_update(rho,g.S,p)
        self.assertLess(np.linalg.norm(out-out.conj().T),1e-12)
        self.assertLess(abs(np.trace(out)-1),1e-12)
        self.assertLess(np.min(np.linalg.eigvalsh(out))+1e-12, np.min(np.linalg.eigvalsh(out))+2e-12)
        self.assertAlmostEqual(float(np.min(np.linalg.eigvalsh(out))),float(np.min(np.linalg.eigvalsh(rho))),places=11)

    def test_03_hidden_marginals_close_under_unitary_sample(self):
        g=load_gate()
        rho=g.F.state(*g.FIXTURES[0]); h=g.R.HB[0]; p=g.R.PB[4]
        a=g.local_unitary_update(rho+g.ETA*h,g.S,p)
        b=g.local_unitary_update(rho-g.ETA*h,g.S,p)
        self.assertLess(g.G.marginal_diff(a,b),g.CLOSURE_TOL)

    def test_04_measure_fixture_exports_full_maps(self):
        g=load_gate()
        z=g.measure_fixture(g.FIXTURES[0])
        self.assertEqual(z["E_exp"].shape,(9,243))
        self.assertEqual(z["E_unitary"].shape,(9,243))
        self.assertEqual(z["unitary_source_change"].shape,(9,))
        self.assertEqual(z["closure_residuals"].shape,(243,))
        self.assertTrue(np.isfinite(z["E_exp"]).all())
        self.assertTrue(np.isfinite(z["E_unitary"]).all())

    def test_05_evaluator_requires_active_unitary_source(self):
        g=load_gate()
        z=g.measure_fixture(g.FIXTURES[0])
        z["unitary_source_change"][:]=0
        _,errors=g.evaluate_arrays(z,g.FIXTURES[0])
        self.assertTrue(any("source inactive" in e for e in errors))

    def test_06_evaluator_rejects_broken_closure(self):
        g=load_gate()
        z=g.measure_fixture(g.FIXTURES[0])
        z["closure_residuals"][0]=10*g.CLOSURE_TOL
        _,errors=g.evaluate_arrays(z,g.FIXTURES[0])
        self.assertTrue(any("closure" in e for e in errors))

    def test_07_controlled_contrast_is_null_vs_nonnull(self):
        g=load_gate()
        z=g.measure_fixture(g.FIXTURES[0])
        metrics,errors=g.evaluate_arrays(z,g.FIXTURES[0])
        self.assertEqual(errors,[])
        self.assertGreater(metrics["ranks"]["E_exp"]["rank"],0)
        self.assertEqual(metrics["ranks"]["E_unitary"]["rank"],0)
        self.assertLessEqual(metrics["unitary_to_exponential_norm_ratio"],g.MIXED_RATIO_TOL)

    def test_08_report_validation_fails_closed(self):
        g=load_gate()
        with tempfile.TemporaryDirectory() as td:
            out=pathlib.Path(td)/"run"
            report=g.run(out)
            self.assertEqual(report["verdict"],"SOURCE_LAW_SPECIFICITY_CONFIRMED")
            loaded=json.loads((out/"report.json").read_text())
            loaded["all_controls_pass"]=False
            (out/"report.json").write_text(json.dumps(loaded))
            with self.assertRaises(ValueError):
                g.verify(out)

if __name__=="__main__":
    unittest.main()
