"""v15.49 Task 1 RED: bridge domain/codomain contract."""
from pathlib import Path
import unittest
import bridge_contract as bc

class BridgeContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.root=Path(__file__).resolve().parents[4]
        cls.c=bc.load_contract(cls.root)
    def test_sources_are_pinned(self):
        self.assertGreaterEqual(len(self.c["sources"]),4)
        self.assertTrue(all(len(v["git_blob_sha"])==40 for v in self.c["sources"].values()))
    def test_domain_and_codomain_explicit(self):
        self.assertEqual(self.c["domain"]["sort"],"RETAINED_RECOVERABILITY")
        self.assertEqual(self.c["codomain"]["sort"],"QUANTUM_OPERATIONAL_RECOVERABILITY")
    def test_equal_cardinality_does_not_certify_typing(self):
        self.assertEqual(self.c["typing"]["status"],"NO_CROSS_DOMAIN_MORPHISM_TYPE_CERTIFIED")
        self.assertFalse(self.c["typing"]["equal_cardinality_is_sufficient"])
        self.assertIsNone(self.c["typing"]["bridge_homset"])
    def test_no_privileged_bridge(self):
        self.assertIsNone(self.c["cross_domain"]["bridge"])
        self.assertIsNone(self.c["cross_domain"]["node_site_dictionary"])
    def test_axiom_manifest_frozen(self):
        self.assertEqual(set(self.c["axioms"]),{"type_preservation","covariance","composition_order",
            "neutrality","refinement","lineage_locality","disjoint_composition","gauge_respect","no_downstream_selection"})
    def test_downstream_firewall(self):
        self.assertTrue(all(self.c["prohibited_inputs"].values()))
    def test_source_drift_fails_closed(self):
        with self.assertRaisesRegex(ValueError,"source_blob_mismatch"):
            bc.load_contract(self.root,overrides={"carrier_origin":b"drift"})
if __name__=="__main__": unittest.main()
