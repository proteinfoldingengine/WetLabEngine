import unittest
import provenance_inventory as inv


class InventoryTests(unittest.TestCase):
    def test_required_blobs_are_exact(self):
        rows = inv.frozen_inventory(inv.REPO_ROOT)
        self.assertEqual(inv.by_key('v15.28-ledger', rows).blob,
                         '6d1ed9766d89c2f66d072978a8fa4b60bedccb39')
        self.assertEqual(inv.by_key('v15.08-source-semantics', rows).blob,
                         '23bbeaecdb81adfe1a39b3140569d23c367b8b55')
        self.assertEqual(inv.by_key('v997-genesis-pin', rows).blob,
                         '8f4ee48cbaf6c822b87dd5e30a5dfee4d596e26e')
        self.assertEqual(inv.by_key('v923-source-role', rows).blob,
                         '9a1523c08d2b9b2c5ba2d298dfed3d563a750bec')

    def test_genesis_pin_is_not_microscopic_incidence_relation(self):
        r = inv.by_key('v997-genesis-pin')
        self.assertEqual(r.domain, 'HISTORY_PROVENANCE')
        self.assertNotIn('TORUS_EDGE_REPRESENTATIVE', r.codomains)

    def test_source_role_is_discrete_legitimacy_not_edge_label(self):
        r = inv.by_key('v923-source-role')
        self.assertEqual(r.relation_class, 'CERTIFIED_PROVENANCE_RELATION')
        self.assertEqual(r.value_type, 'TERNARY_SOURCE_ROLE')
        self.assertFalse(r.certifies_q_fiber_relation)


if __name__ == '__main__':
    unittest.main()
