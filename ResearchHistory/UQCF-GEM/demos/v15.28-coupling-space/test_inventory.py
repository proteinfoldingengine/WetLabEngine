import unittest
from pathlib import Path
import representation_inventory as inv


class InventoryTests(unittest.TestCase):
    def test_v1527_and_v1404_hashes_are_frozen(self):
        rows = {r.key: r for r in inv.frozen_inventory(Path(inv.REPO_ROOT))}
        self.assertEqual(rows['v15.27-target-origin'].git_blob,
                         '1c33232050567bf3b2bf77b19570ec2b8a1fb5e0')
        self.assertEqual(rows['v14.04-provenance-report'].git_blob,
                         'e5d9566bfc86c801d2933e63453d1800f60a675b')

    def test_missing_representation_links_fail_closed(self):
        self.assertEqual(inv.by_key('genesis-6d-field').eligibility,
                         'NO_CERTIFIED_SOURCE_TARGET_REPRESENTATION_LINK')
        self.assertEqual(inv.by_key('retained-graph-source-current').eligibility,
                         'NO_CERTIFIED_SOURCE_TARGET_REPRESENTATION_LINK')

    def test_q_baseline_is_control_not_physical_candidate(self):
        q = inv.by_key('source-quotient-q-control')
        self.assertTrue(q.eligible)
        self.assertEqual(q.role, 'BASELINE_CONTROL')

    def test_inventory_keys_are_unique_and_sorted_on_export(self):
        rows = inv.frozen_inventory(Path(inv.REPO_ROOT))
        keys = [r.key for r in rows]
        self.assertEqual(len(keys), len(set(keys)))
        self.assertEqual(keys, sorted(keys))

    def test_eligible_records_require_certified_action_and_link(self):
        for row in inv.eligible_records(inv.frozen_inventory(Path(inv.REPO_ROOT))):
            self.assertTrue(row.action_status.startswith('CERTIFIED'))
            self.assertTrue(row.label_link_status.startswith('CERTIFIED'))


if __name__ == '__main__':
    unittest.main(verbosity=2)
