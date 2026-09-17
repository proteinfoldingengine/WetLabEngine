import unittest
import frozen_inputs as fi


class FrozenInputTests(unittest.TestCase):
    def test_v1529_result_pin_and_stop_object(self):
        mods = fi.load_v1529()
        self.assertEqual(mods.v1529_results['status'],
                         'PROVENANCE_RELATION_TO_Q_FIBERS_NOT_ENTAILED')
        self.assertEqual(mods.v1529_results['next_required_object'],
                         'INDEPENDENTLY_MOTIVATED_PROVENANCE_FIBER_RELATION')

    def test_inherited_module_blobs_are_exact(self):
        mods = fi.load_v1529()
        self.assertIsNotNone(mods.provenance_inventory)
        self.assertIsNotNone(mods.fiber_model)
        self.assertIsNotNone(mods.source_extension_gate)

    def test_exact_four_candidate_origins(self):
        rows = fi.candidate_inventory(fi.REPO_ROOT)
        self.assertEqual(tuple(row.key for row in rows), (
            'genesis-6d-carrier',
            'genesis-history-lineage',
            'retained-source-current',
            'ternary-source-role',
        ))

    def test_candidate_artifact_pins_are_exact(self):
        for row in fi.candidate_inventory(fi.REPO_ROOT):
            fi.verify_candidate(row, fi.REPO_ROOT)


if __name__ == '__main__':
    unittest.main()
