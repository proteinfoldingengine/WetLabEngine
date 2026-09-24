"""v15.47 Task 3 RED: quotient surviving functors by frozen target equivalence."""
from pathlib import Path
import copy, unittest
import functor_contract as fc
import functor_candidates as cand
import functor_classes as cls

class FunctorClassTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        root=Path(__file__).resolve().parents[4]
        cls.c=fc.load_contract(root)
        cls.cs=cand.enumerate_candidates(cls.c)

    def test_identity_only_keeps_120_classes(self):
        r=cls.surviving_classes(self.c,self.cs)
        self.assertEqual(r["survivor_count"],120)
        self.assertEqual(r["equivalence_class_count"],120)

    def test_every_survivor_occurs_once(self):
        r=cls.surviving_classes(self.c,self.cs)
        members=[tuple(m) for group in r["classes"] for m in group]
        self.assertEqual(len(members),120)
        self.assertEqual(len(set(members)),120)

    def test_unearned_equivalence_rejected(self):
        c=copy.deepcopy(self.c)
        c["target_category"]["equivalence"]="ALL_SITE_PERMUTATIONS"
        with self.assertRaisesRegex(ValueError,"unearned_target_equivalence"):
            cls.surviving_classes(c,self.cs)

    def test_incomplete_candidate_family_rejected(self):
        with self.assertRaisesRegex(ValueError,"incomplete_candidate_family"):
            cls.surviving_classes(self.c,self.cs[:-1])

    def test_duplicate_candidate_rejected(self):
        bad=list(self.cs); bad[-1]=bad[0]
        with self.assertRaisesRegex(ValueError,"duplicate_candidate"):
            cls.surviving_classes(self.c,bad)

if __name__=="__main__": unittest.main()
