"""v15.48 Task 1 RED: typed recoverability-signature contract."""
from pathlib import Path
import unittest
import signature_contract as sc

class SignatureContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.root=Path(__file__).resolve().parents[4]
        cls.c=sc.load_contract(cls.root)
    def test_sources_hash_pinned(self):
        self.assertGreaterEqual(len(self.c["sources"]),4)
        self.assertTrue(all(len(v["git_blob_sha"])==40 for v in self.c["sources"].values()))
    def test_coordinate_manifests_are_explicit(self):
        self.assertGreater(len(self.c["retained_signature_schema"]),0)
        self.assertGreater(len(self.c["quantum_signature_schema"]),0)
    def test_no_cross_domain_dictionary(self):
        self.assertIsNone(self.c["cross_domain"]["node_site_dictionary"])
    def test_type_audit_is_explicit(self):
        self.assertIn(self.c["type_audit"]["status"],("COMMON_TYPE_CERTIFIED","NO_COMMON_TYPE_CERTIFIED"))
        self.assertEqual(self.c["type_audit"]["status"],"NO_COMMON_TYPE_CERTIFIED")
        self.assertIsNone(self.c["type_audit"]["equality_relation"])
    def test_downstream_firewall(self):
        self.assertTrue(all(self.c["prohibited_inputs"].values()))
    def test_source_drift_fails_closed(self):
        with self.assertRaisesRegex(ValueError,"source_blob_mismatch"):
            sc.load_contract(self.root,overrides={"carrier_origin":b"drift"})
if __name__=="__main__": unittest.main()
