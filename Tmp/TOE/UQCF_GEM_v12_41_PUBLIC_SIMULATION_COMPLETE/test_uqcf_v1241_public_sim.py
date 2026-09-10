
import unittest
import numpy as np
from pathlib import Path
from uqcf_v1241_public_sim import (
    paulis, density_state, exact_closure_residual, broken_closure_residual,
    sweep_records
)

class TestPublicSimulation(unittest.TestCase):
    def test_density_state_is_valid(self):
        rho=density_state(0.37)
        self.assertLess(np.linalg.norm(rho-rho.conj().T),1e-12)
        self.assertLess(abs(np.trace(rho)-1.0),1e-12)
        self.assertGreaterEqual(np.linalg.eigvalsh(rho).min(),-1e-12)

    def test_exact_closure_is_numerically_zero(self):
        for lam in np.linspace(0,2*np.pi,17):
            rho=density_state(float(lam))
            self.assertLess(exact_closure_residual(rho),1e-12)

    def test_broken_control_is_nonzero_somewhere(self):
        vals=[broken_closure_residual(density_state(float(lam))) for lam in np.linspace(0,2*np.pi,17)]
        self.assertGreater(max(vals),0.05)

    def test_sweep_schema(self):
        rows=sweep_records(11)
        self.assertEqual(len(rows),11)
        required={"step","lambda","Cx","Cy","Cz","exact_bracket","exact_rhs","exact_residual","broken_rhs","broken_residual","purity"}
        self.assertTrue(required.issubset(rows[0].keys()))
        self.assertLess(max(r["exact_residual"] for r in rows),1e-12)
        self.assertGreater(max(r["broken_residual"] for r in rows),0.05)


    def test_export_helpers_create_expected_files(self):
        from uqcf_v1241_public_sim import export_csv, render_static_plot
        outdir=Path("test_outputs")
        outdir.mkdir(exist_ok=True)
        rows=sweep_records(21)
        csv_path=export_csv(rows,outdir/"diag.csv")
        png_path=render_static_plot(rows,outdir/"verify.png")
        self.assertTrue(Path(csv_path).exists())
        self.assertTrue(Path(png_path).exists())
        self.assertGreater(Path(csv_path).stat().st_size,100)
        self.assertGreater(Path(png_path).stat().st_size,1000)

if __name__=="__main__":
    unittest.main()
