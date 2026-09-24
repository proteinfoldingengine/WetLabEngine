"""v15.53 Task 1 RED: frozen contract and provenance boundary."""
from pathlib import Path
import unittest
import realization_contract as rc

ROOT = Path(__file__).resolve().parents[4]
EXPECTED_SOURCES = {
    "v1546_stage_c": {"path": "ResearchHistory/UQCF-GEM/demos/v15.46-primitive-joint-source-admissibility/docs/STAGE_C_RESULTS.json", "git_blob_sha": "30e0b10c9317f81c7f7627a15919148a31583c73"},
    "v1551_results": {"path": "ResearchHistory/UQCF-GEM/demos/v15.51-minimal-quantum-origin-primitive/docs/RESULTS.json", "git_blob_sha": "e52c2d1e8330d6699f84b293ec456b375f7fc7d0"},
    "v1552_verification": {"path": "ResearchHistory/UQCF-GEM/demos/v15.52-quantum-origin-invariance-obstruction/docs/VERIFICATION.json", "git_blob_sha": "670b881a0d7db1da784caa6ec522dc4fd4465949"},
    "v1552_spec": {"path": "docs/superpowers/specs/2026-09-23-v1552-quantum-origin-invariance-obstruction.md", "git_blob_sha": "e85d252189a23fbfdd6e347e1ad605dd657ae59b"},
}
EXPECTED_OBSERVABLES = ("object_count","lineage_incidence","dependency_incidence","recoverability_relation","composition_table","refinement_diagram","disjoint_partition")
EXPECTED_VERDICTS = ("CERTIFIED_FAMILY_OBSTRUCTION_WITNESS","NO_WITNESS_IN_FROZEN_FAMILY","FAMILY_INVALID","VERIFICATION_FAILED")

class ContractTests(unittest.TestCase):
    def setUp(self):
        self.c = rc.load_contract(ROOT)
    def test_schema_and_sources_are_frozen(self):
        self.assertEqual(self.c["schema"], "uqcf-v1553-realization-contract-v1")
        self.assertEqual(self.c["sources"], EXPECTED_SOURCES)
    def test_verdicts_are_exact(self):
        self.assertEqual(tuple(self.c["primary_verdicts"]), EXPECTED_VERDICTS)
    def test_retained_domain_is_exactly_v1552_seven(self):
        self.assertEqual(tuple(self.c["retained_observables"]), EXPECTED_OBSERVABLES)
    def test_forbidden_selector_and_target_fields_are_explicit(self):
        self.assertTrue({"target_class","E_observables","node_site_dictionary","fixture_order_selector","post_result_gauge","enumeration_index"} <= set(self.c["forbidden_fields"]))
    def test_claim_firewall_is_frozen(self):
        self.assertEqual(self.c["source_correspondence"], "NOT_EVALUATED")
        self.assertEqual(self.c["Pillar_3"], "OPEN")
        for k in ("physical_source_law","geometry_or_curvature","continuum_limit","empirical_fit","fundamental_physical_time","dark_matter_primitive"):
            self.assertFalse(self.c[k])
    def test_predecessor_bytes_verify(self):
        self.assertEqual(rc.verify_sources(ROOT, self.c), EXPECTED_SOURCES)
    def test_source_drift_fails_closed(self):
        c = rc.load_contract(ROOT)
        c["sources"]["v1551_results"]["git_blob_sha"] = "0"*40
        with self.assertRaises(ValueError):
            rc.verify_sources(ROOT, c)

if __name__ == "__main__":
    unittest.main()
