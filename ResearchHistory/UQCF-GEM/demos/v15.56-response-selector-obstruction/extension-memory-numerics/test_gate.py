import importlib.util
import pathlib
import unittest
import numpy as np

HERE=pathlib.Path(__file__).resolve().parent
G=HERE/"gate.py"

def load():
    if not G.exists():
        raise AssertionError("gate.py missing: expected RED")
    s=importlib.util.spec_from_file_location("v1572",G)
    m=importlib.util.module_from_spec(s)
    s.loader.exec_module(m)
    return m

class GateTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.g=load()

    def test_frozen_constants(self):
        self.assertEqual(self.g.MP_DPS,80)
        self.assertEqual(self.g.ETA,1e-4)
        self.assertEqual(self.g.STRENGTH,1e-3)
        self.assertEqual(len(self.g.HIDDEN),27)

    def test_high_precision_partial_trace_matches_float_reference(self):
        rho=self.g.V71.V64.ASYM.select_states()[0]["rho"]
        mr=self.g.mpcmat(rho)
        for e in self.g.EDGES:
            a=self.g.mp_to_np(self.g.mp_restrict(mr,e))
            b=self.g.V71.V70.restrict(rho,e)
            self.assertLessEqual(np.linalg.norm(a-b),1e-14)

    def test_measurement_schema_and_counts(self):
        r=self.g.run_measurement()
        self.assertEqual(r["n_float_witnesses"],52488)
        self.assertEqual(r["n_nonzero_mp_cases"],1944)
        self.assertIn(r["verdict"],[
            "EXTENSION_MEMORY_CANCELLATION_CONFIRMED",
            "EXTENSION_MEMORY_NUMERIC_DISAGREEMENT",
            "INVALID"])

    def test_adjudication_branches(self):
        self.assertEqual(self.g.adjudicate(True,True,True,True),
                         "EXTENSION_MEMORY_CANCELLATION_CONFIRMED")
        self.assertEqual(self.g.adjudicate(True,False,True,True),
                         "EXTENSION_MEMORY_NUMERIC_DISAGREEMENT")
        self.assertEqual(self.g.adjudicate(False,True,True,True),"INVALID")

if __name__=="__main__":
    unittest.main()
