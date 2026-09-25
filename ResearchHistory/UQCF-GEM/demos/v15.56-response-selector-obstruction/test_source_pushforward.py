"""v15.56 Task 29 RED: extensive source pushforward under pruning."""
import unittest
import source_pushforward as sp
class T(unittest.TestCase):
 def test_rule(self): self.assertEqual(sp.classify()["rule"],"J_c(v)=sum_{k:r(k)=v} J_f(k)")
 def test_extensive(self): self.assertTrue(sp.classify()["forced_by_finite_additivity"])
 def test_total(self): self.assertTrue(sp.classify()["preserves_total_retained_grade"])
 def test_composition(self): self.assertTrue(sp.classify()["functorial_under_composed_retractions"])
 def test_no_geometry(self): self.assertEqual(sp.classify()["geometry_used"],[])
if __name__=="__main__": unittest.main()
