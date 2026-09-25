"""v15.56 Task 30 RED: executable fine-prune-coarse response comparison."""
import unittest
import pruning_response as pr
class T(unittest.TestCase):
 def test_cases(self): self.assertGreaterEqual(pr.run()["case_count"],4)
 def test_source_pushforward(self): self.assertLess(pr.run()["max_source_pushforward_error"],1e-12)
 def test_reports_commutator(self): self.assertGreaterEqual(pr.run()["max_projective_response_mismatch"],0.0)
 def test_classifies(self): self.assertIn(pr.run()["verdict"],("EXACT_NATURALITY","PROJECTIVE_NATURALITY","SYSTEMATIC_MISMATCH","UNSTRUCTURED_FAILURE"))
 def test_no_fit(self): self.assertFalse(pr.run()["fitted_parameters"])
if __name__=="__main__": unittest.main()
