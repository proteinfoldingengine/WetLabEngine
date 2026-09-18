import unittest
import fiber_model as fm
import provenance_equivalence as pe
import provenance_inventory as inv


class EquivalenceTests(unittest.TestCase):
    def test_raw_edge_difference_is_not_provenance_evidence(self):
        a = fm.root_fixture()
        b = fm.face_shift(a, 0, 1)
        r = pe.classify_pair(a, b, inv.frozen_inventory(inv.REPO_ROOT))
        self.assertEqual(r.status, 'PROVENANCE_RELATION_UNSPECIFIED')
        self.assertFalse(r.physical_distinction_certified)

    def test_synthetic_collapsed_control_is_identical(self):
        a, b, evidence = pe.synthetic_collapsed_control()
        r = pe.classify_pair(a, b, evidence)
        self.assertEqual(r.status, 'PROVENANCE_IDENTICAL')

    def test_synthetic_distinct_control_is_certified(self):
        a, b, evidence = pe.synthetic_distinct_control()
        r = pe.classify_pair(a, b, evidence)
        self.assertEqual(r.status, 'PROVENANCE_DISTINCT_CERTIFIED')


if __name__ == '__main__':
    unittest.main()
