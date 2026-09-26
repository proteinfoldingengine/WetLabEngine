"""v15.56 Task 31 RED: measure-robust pruning-defect gate."""
import unittest
import pruning_measure_robustness as pm
class T(unittest.TestCase):
 def test_cases(self): self.assertGreaterEqual(pm.run()["case_count"],4)
 def test_no_fit(self): self.assertFalse(pm.run()["fitted_parameters"])
 def test_admissible(self): self.assertGreaterEqual(pm.run()["aggregation_family_count"],3)
 def test_verdict(self): self.assertIn(pm.run()["verdict"],("ROBUST_DEFECT","MEASURE_DEPENDENT_DEFECT","NATURALITY_RECOVERED_BY_ADMISSIBLE_MEASURE"))
 def test_source_exact(self): self.assertLess(pm.run()["max_source_pushforward_error"],1e-12)
if __name__=="__main__": unittest.main()
