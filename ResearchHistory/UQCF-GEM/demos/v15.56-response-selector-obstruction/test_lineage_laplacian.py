"""v15.56 Task 16 RED: native lineage Laplacian theorem gate."""
import unittest
import lineage_laplacian as ll
class LaplacianTests(unittest.TestCase):
 def test_definition(self):
  self.assertEqual(ll.classify()["operator"],"Delta_lin = B_lin^T B_lin")
 def test_properties(self):
  r=ll.classify()
  for k in ("symmetric","positive_semidefinite","constants_in_kernel","relabeling_covariant"):
   self.assertTrue(r[k])
 def test_nullity(self):
  self.assertEqual(ll.classify()["nullity_theorem"],"nullity(Delta_lin)=connected_components")
 def test_no_v1545_equivalence(self):
  self.assertFalse(ll.classify()["equals_v1545_operator_claimed"])
 def test_no_geometry(self):
  self.assertEqual(ll.classify()["geometry_used"],[])
if __name__=="__main__": unittest.main()
