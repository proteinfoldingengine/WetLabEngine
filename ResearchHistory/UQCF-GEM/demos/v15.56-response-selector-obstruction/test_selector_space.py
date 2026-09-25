"""v15.56 Task 1 RED: exact selector-space symmetry action."""
import json, unittest
from pathlib import Path
import selector_space as ss
HERE=Path(__file__).resolve().parent

class SelectorSpaceTests(unittest.TestCase):
    def setUp(self):
        self.c=json.loads((HERE/"contract.json").read_text())

    def test_field_and_dimension(self):
        r=ss.build_selector_action(self.c)
        self.assertEqual(r["scalar_field"],"Q")
        self.assertEqual(r["response_dimension"],4)

    def test_all_preearned_structures_accounted(self):
        r=ss.build_selector_action(self.c)
        self.assertEqual(set(r["structures_checked"]),{
            "RETAINED_INCIDENCE_REFINEMENT",
            "COMPOSITION_COMPATIBILITY",
            "AUTOMORPHISM_NATURALITY",
            "V1545_RESPONSE_FACTORIZATION",
            "GENESIS_PIN_PROVENANCE_REPAIR"
        })

    def test_no_forbidden_selector(self):
        r=ss.build_selector_action(self.c)
        self.assertEqual(r["forbidden_inputs_used"],[])

    def test_exact_invariant_dimension(self):
        r=ss.classify_selector_space(self.c)
        self.assertIsInstance(r["invariant_dimension"],int)
        self.assertGreaterEqual(r["invariant_dimension"],0)

    def test_verdict_consistent(self):
        r=ss.classify_selector_space(self.c)
        self.assertIn(r["primary_verdict"],self.c["allowed_verdicts"])
        if r["primary_verdict"]=="CANONICAL_SELECTOR_FOUND":
            self.assertEqual(r["invariant_dimension"],1)
            self.assertTrue(r["earned_normalization"])
        if r["invariant_dimension"]>1:
            self.assertNotEqual(r["primary_verdict"],"CANONICAL_SELECTOR_FOUND")

if __name__=="__main__":
    unittest.main()
