import unittest
import p4_geometry_source_audit as p4

class P4GeometryGateTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.r=p4.audit()

    def test_exact_source_hashes(self):
        self.assertTrue(all(self.r["source_hash_match"].values()))

    def test_all_peptide_cn_links_fail_declared_geometry(self):
        cn=self.r["historical_initializer"]["C_N_peptide"]
        self.assertEqual(cn["n"],35)
        self.assertEqual(cn["within_0p1A"],0)
        self.assertGreater(cn["min_abs_error_to_declared"],1.0)

    def test_interior_nca_cac_geometry_constructed(self):
        self.assertEqual(self.r["historical_initializer"]["N_CA_interior"]["within_0p1A"],34)
        self.assertEqual(self.r["historical_initializer"]["CA_C_interior"]["within_0p1A"],34)

    def test_declared_cn_constant_is_not_used(self):
        c=self.r["source_contract"]
        self.assertTrue(c["generator_declares_C_N_dist_1p33"])
        self.assertFalse(c["generator_uses_C_N_dist_after_declaration"])

    def test_forcefield_cannot_enforce_n_c_covalent_geometry(self):
        c=self.r["source_contract"]
        self.assertFalse(c["forcefield_receives_N_coords"])
        self.assertFalse(c["forcefield_receives_C_coords"])
        self.assertTrue(c["main_passes_CA_as_force_coordinates"])
        self.assertTrue(c["main_computes_phi_psi_from_N_CA_C"])
        self.assertFalse(c["explicit_covalent_bond_force_function_present"])

    def test_gate_verdict(self):
        self.assertEqual(self.r["verdict"],"NO_GO_HISTORICAL_PHYSICAL_BACKBONE_INTERPRETATION")

if __name__=="__main__":
    unittest.main()
