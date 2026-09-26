"""v15.56 Task 33 RED: exact intertwining obstruction theorem gate."""
import unittest
import pruning_intertwining_theorem as pt
class T(unittest.TestCase):
 def test_condition(self): self.assertEqual(pt.classify()["necessary_condition"],"ker(P) invariant under G_f modulo constants")
 def test_equiv(self): self.assertTrue(pt.classify()["quotient_factorization_equivalence"])
 def test_branch_collapse(self): self.assertIn(pt.classify()["branch_collapse_status"],("GENERALLY_VIOLATES_CONDITION","CONDITION_PRESERVED"))
 def test_scope(self): self.assertEqual(pt.classify()["scope"],"FINITE_CONNECTED_LINEAGE_GRAPHS_LINEAR_ALL_SOURCE_NATURALITY")
 def test_no_geometry(self): self.assertEqual(pt.classify()["geometry_used"],[])
if __name__=="__main__": unittest.main()
