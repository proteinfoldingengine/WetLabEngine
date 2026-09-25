"""v15.56 Task 5 RED: cross-carrier target-functor typing."""
import unittest
import target_functor as tf

class TargetFunctorTests(unittest.TestCase):
 def test_objects(self):
  r=tf.classify_target_functor()
  self.assertEqual(r["objects"],"CENTERED_PHI_L_FOR_ADMISSIBLE_L")
 def test_no_arbitrary_cross_size_map(self):
  r=tf.classify_target_functor()
  self.assertIsNone(r["cross_carrier_morphism"])
 def test_verdict(self):
  self.assertEqual(tf.classify_target_functor()["primary_verdict"],
                   "MISSING_CANONICAL_CROSS_CARRIER_MORPHISM")
 def test_required_naturality_square(self):
  r=tf.classify_target_functor()
  self.assertEqual(r["naturality_equation"],"T_mn B_m = B_n S_mn")
 def test_no_fit(self):
  self.assertEqual(tf.classify_target_functor()["forbidden_inputs_used"],[])
if __name__=="__main__": unittest.main()
