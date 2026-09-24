"""Stage C2 RED: exact representation-family controls."""
import unittest
import stage_c_representations as sr

class StageCRepresentationTests(unittest.TestCase):
    def test_32_has_multiple_nontrivial_factorizations(self):
        fs=sr.factorizations(32)
        self.assertIn((32,),fs); self.assertIn((2,2,2,2,2),fs)
        self.assertGreater(len(fs),1)
    def test_125_has_no_five_nontrivial_factors(self):
        self.assertFalse(any(len(x)==5 for x in sr.factorizations(125)))
    def test_neutral_state_selects_no_factorization(self):
        self.assertIsNone(sr.neutral_factorization_selector(32))
    def test_rigid_sorts_do_not_create_dictionary(self):
        self.assertEqual(sr.node_site_dictionary(5,5,cross_domain_relations=[]),None)
    def test_dimension_types_not_equated(self):
        self.assertFalse(sr.same_carrier_type(32,125))
if __name__=="__main__": unittest.main()
