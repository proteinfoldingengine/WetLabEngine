import unittest
from fractions import Fraction as F
from small_controls import graph_center, intersection_basis, canonical

class FixedChecks(unittest.TestCase):
    def test_scalar_subalgebra_retains_sum(self):
        old=[[1,0],[0,1]];new=[[1,1]]
        self.assertEqual(canonical(graph_center(old,new)), canonical(new))
    def test_linear_intersection_independently_recovers_sum(self):
        old=[[1,0],[0,1]];new=[[1,1]]
        self.assertEqual(canonical(intersection_basis(old,new)), canonical(new))
    def test_four_address_retains_merged_effect(self):
        old=[[int(i==j) for j in range(4)] for i in range(4)]
        new=[[1,0,0,0],[0,1,1,0],[0,0,0,1]]
        self.assertEqual(canonical(graph_center(old,new)),canonical(new))
        self.assertEqual(canonical(intersection_basis(old,new)),canonical(new))
    def test_incomparable_centers_have_scalar_intersection(self):
        old=[[1,0,0],[0,1,1]];new=[[1,1,0],[0,0,1]]
        expected=[[1,1,1]]
        self.assertEqual(canonical(graph_center(old,new)),canonical(expected))
        self.assertEqual(canonical(intersection_basis(old,new)),canonical(expected))
    def test_disjoint_vector_spaces_intersect_in_zero(self):
        self.assertEqual(intersection_basis([[1,0]],[[0,1]]),[])
    def test_rational_intersection_preserves_exact_values(self):
        self.assertEqual(canonical(intersection_basis([[F(1,3),F(1,2)]],[[2,3]])),canonical([[2,3]]))
if __name__=='__main__':unittest.main()
