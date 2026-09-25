"""v15.56 Task 22 RED: retained source-grade amplitude gate."""
import unittest
import retained_amplitude as ra
class AmpTests(unittest.TestCase):
 def test_prior_grade(self):
  r=ra.classify(); self.assertTrue(r["relative_retained_grade_earned"])
 def test_local_field(self):
  self.assertEqual(ra.classify()["localized_source_form"],"J_s = g_ret(s) delta_{k,k(s)}")
 def test_scale_status(self):
  r=ra.classify(); self.assertFalse(r["absolute_observer_scale_earned"])
  self.assertTrue(r["positive_rescaling_freedom"])
 def test_no_geometry(self):
  self.assertEqual(ra.classify()["geometry_used"],[])
if __name__=="__main__": unittest.main()
