"""v15.55 Task 1 RED: frozen source-compatibility response contract."""
import json
import unittest
from pathlib import Path
import response_classifier as rc

HERE=Path(__file__).resolve().parent

class ContractTests(unittest.TestCase):
    def setUp(self):
        self.c=json.loads((HERE/"contract.json").read_text())

    def test_allowed_verdicts_exact(self):
        self.assertEqual(self.c["allowed_verdicts"],[
            "UNIQUE_CANONICAL_RESPONSE","RESPONSE_NONUNIQUE",
            "NO_ADMISSIBLE_RESPONSE","ILL_TYPED_RESPONSE_PROBLEM"])

    def test_exact_arithmetic_required(self):
        self.assertIs(self.c["exact_arithmetic_required"],True)

    def test_post_result_selection_forbidden(self):
        self.assertIs(self.c["post_result_selection_forbidden"],True)

    def test_axioms_exact(self):
        self.assertEqual(set(self.c["axioms"]),{
            "COVARIANCE","NEUTRALITY","REDUCTION_CONSISTENCY",
            "COMPOSITION","CONTROL_SEPARATION","NO_SPECTRAL_EDGE_SELECTION"})

    def test_classifier_interface(self):
        result=rc.classify_response_space(self.c)
        self.assertIn(result["primary_verdict"],self.c["allowed_verdicts"])

if __name__=="__main__":
    unittest.main()
