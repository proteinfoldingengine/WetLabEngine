import unittest
import action_audit as aa
import provenance_inventory as inv


class ActionAuditTests(unittest.TestCase):
    def test_real_archive_has_no_certified_torus_provenance_action(self):
        r = aa.audit_real_provenance_action(inv.frozen_inventory(inv.REPO_ROOT))
        self.assertFalse(r.action_certified)
        self.assertEqual(r.status,
                         'PROVENANCE_DISTINCTION_EXISTS_BUT_ACTION_NOT_CERTIFIED'
                         if r.distinction_certified else
                         'NO_CERTIFIED_PROVENANCE_ACTION_ON_Q_FIBER')

    def test_synthetic_extension_has_exact_group_action(self):
        r = aa.audit_synthetic_extension_action()
        self.assertTrue(r.action_certified)
        self.assertTrue(r.group_law_exact)
        self.assertTrue(r.projection_equivariant)


if __name__ == '__main__':
    unittest.main()
