import importlib.util
import pathlib
import unittest
import numpy as np

HERE=pathlib.Path(__file__).resolve().parent
G=HERE/"gate.py"

def load():
    if not G.exists():
        raise AssertionError("gate.py missing: expected RED")
    s=importlib.util.spec_from_file_location("v1571",G)
    m=importlib.util.module_from_spec(s)
    s.loader.exec_module(m)
    return m

class GateTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.g=load()

    def test_frozen_constants(self):
        self.assertEqual(self.g.ETA,1e-4)
        self.assertEqual(self.g.STRENGTH,1e-3)
        self.assertEqual(self.g.FLOW_LEVELS,[-1e-2,-3e-3,-1e-3,1e-3,3e-3,1e-2])
        self.assertEqual(self.g.REBASE_A,4e-3)
        self.assertEqual(self.g.REBASE_B,-1.5e-3)
        self.assertEqual(len(self.g.HIDDEN),27)

    def test_memory_basis_is_full_rank(self):
        m=self.g.memory_gram()
        self.assertEqual(np.linalg.matrix_rank(m),27)
        self.assertLessEqual(float(np.max(np.abs(m-np.eye(27)))),1e-12)

    def test_local_retained_lift_is_independent_construction(self):
        states=self.g.V70.V64.ASYM.select_states()
        rho=states[0]["rho"]
        y,_=self.g.V70.V64.target_Y(rho)
        for e in self.g.EDGES:
            q=self.g.V70.restrict(rho,e)
            yl=self.g.local_retained_lift(q)
            yr=self.g.V70.restrict(y,e)
            self.assertLessEqual(np.linalg.norm(yl-yr)/np.linalg.norm(yr),1e-10)

    def test_compression_control_detects_missing_coordinate(self):
        c=self.g.compression_control()
        self.assertLessEqual(c["compressed_memory_gap"],1e-12)
        self.assertGreater(c["retained_output_gap"],1e-8)

    def test_measurement_schema_and_counts(self):
        r=self.g.run_measurement()
        self.assertEqual(r["n_states"],12)
        self.assertEqual(r["n_descent_witnesses"],52488)
        self.assertIn(r["verdict"],[
            "MINIMAL_EXTENSION_MEMORY_DESCENT_CONFIRMED",
            "MINIMAL_EXTENSION_MEMORY_DESCENT_NOT_CONFIRMED",
            "INVALID"])
        self.assertIn(r["rebasing_verdict"],[
            "REBASED_NULL_INTEGRABILITY_CONFIRMED",
            "REBASED_NULL_INTEGRABILITY_NOT_CONFIRMED",
            "INVALID"])

    def test_adjudication_preserves_negative_and_invalid(self):
        self.assertEqual(self.g.adjudicate(True,False),
            "MINIMAL_EXTENSION_MEMORY_DESCENT_NOT_CONFIRMED")
        self.assertEqual(self.g.adjudicate(False,True),"INVALID")
        self.assertEqual(self.g.adjudicate_rebase(True,False),
            "REBASED_NULL_INTEGRABILITY_NOT_CONFIRMED")
        self.assertEqual(self.g.adjudicate_rebase(False,True),"INVALID")

if __name__=="__main__":
    unittest.main()
