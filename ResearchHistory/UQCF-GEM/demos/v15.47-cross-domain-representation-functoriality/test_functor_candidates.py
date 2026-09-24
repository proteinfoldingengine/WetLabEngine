"""v15.47 Task 2 RED: exhaustive candidate enumeration and law checks."""
from pathlib import Path
import unittest
import functor_contract as fc
import functor_candidates as cand

class FunctorCandidateTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        root=Path(__file__).resolve().parents[4]
        cls.c=fc.load_contract(root)
        cls.cs=cand.enumerate_candidates(cls.c)

    def test_all_5_site_permutations_enumerated(self):
        self.assertEqual(len(self.cs),120)
        self.assertEqual(len({tuple(x["node_site_bijection"]) for x in self.cs}),120)

    def test_no_candidate_is_scored(self):
        self.assertTrue(all("score" not in x for x in self.cs))

    def test_identity_composition_refinement_checked(self):
        checks=[cand.check_laws(self.c,x) for x in self.cs]
        self.assertTrue(all(x["identity"] for x in checks))
        self.assertTrue(all(x["composition"] for x in checks))
        self.assertTrue(all(x["refinement"] for x in checks))

    def test_weak_covariance_remains_nonselective(self):
        survivors=cand.weak_covariance_survivors(self.c,self.cs)
        self.assertGreater(len(survivors),1)

    def test_manual_dictionary_is_rejected(self):
        bad=dict(self.cs[0]); bad["manual_dictionary"]=True
        self.assertEqual(cand.check_laws(self.c,bad)["status"],"MANUAL_CROSS_DOMAIN_DICTIONARY")

    def test_dimension_mismatch_rejected(self):
        bad=dict(self.cs[0]); bad["carrier_dimension"]=125
        self.assertEqual(cand.check_laws(self.c,bad)["status"],"DIMENSION_MISMATCH")

if __name__=="__main__": unittest.main()
