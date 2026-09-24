"""v15.47 Task 1 RED: finite functor contract."""
from pathlib import Path
import unittest
import functor_contract as fc

class FunctorContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.root=Path(__file__).resolve().parents[4]
        cls.c=fc.load_contract(cls.root)

    def test_sources_are_hash_pinned(self):
        self.assertGreaterEqual(len(self.c["sources"]),3)
        self.assertTrue(all(len(x["git_blob_sha"])==40 for x in self.c["sources"].values()))

    def test_source_category_has_nonidentity_composition(self):
        comp=self.c["source_category"]["composition"]
        self.assertTrue(any(a!="id" and b!="id" and c!="id" for a,b,c in comp))

    def test_refinement_square_is_nontrivial(self):
        sq=self.c["source_category"]["refinement_square"]
        self.assertNotEqual(sq["left_path"],sq["right_path"])
        self.assertEqual(sq["common_composite"],sq["left_composite"])
        self.assertEqual(sq["common_composite"],sq["right_composite"])

    def test_target_equivalence_is_declared_before_enumeration(self):
        self.assertEqual(self.c["target_category"]["equivalence"],"IDENTITY_ONLY")

    def test_no_downstream_selector_fields(self):
        p=self.c["prohibited_inputs"]
        for k in ("curvature","gravity","source_response","entropy","spectral_edge","physical_time"):
            self.assertTrue(p[k])

    def test_no_privileged_dictionary(self):
        self.assertIsNone(self.c["cross_domain"]["node_site_dictionary"])

    def test_source_drift_fails_closed(self):
        with self.assertRaisesRegex(ValueError,"source_blob_mismatch"):
            fc.load_contract(self.root,overrides={"carrier_origin":b"drift"})

if __name__=="__main__": unittest.main()
