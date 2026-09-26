"""v15.56 Task 32 RED: positive fiber-local linear naturality no-go gate."""
import unittest
import fiber_local_nogo as fn
class T(unittest.TestCase):
 def test_cases(self): self.assertGreaterEqual(fn.run()["case_count"],4)
 def test_all_sources(self): self.assertTrue(fn.run()["operator_level_test"])
 def test_positive_local(self): self.assertTrue(fn.run()["positive_fiber_local_family"])
 def test_no_fit_claim(self): self.assertFalse(fn.run()["posthoc_parameter_fit"])
 def test_verdict(self): self.assertIn(fn.run()["verdict"],("POSITIVE_FIBER_LOCAL_NATURALITY_EXISTS","POSITIVE_FIBER_LOCAL_NATURALITY_NO_GO","DEGENERATE_OR_UNRESOLVED"))
if __name__=="__main__": unittest.main()
