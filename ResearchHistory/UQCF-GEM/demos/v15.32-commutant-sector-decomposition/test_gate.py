import unittest

from sector_decomposition_gate import audit


class SectorDecompositionGateTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.r = audit()

    def test_macro_sector_dimensions(self):
        self.assertEqual(self.r["group_order"], 392)
        self.assertEqual(self.r["dim_Z"], 50)
        self.assertEqual(self.r["rational_macro_sector_count"], 4)
        self.assertEqual(
            self.r["rational_macro_sector_dimensions"],
            {"homology": 2, "axis": 12, "diagonal": 12, "generic": 24},
        )
        self.assertTrue(self.r["projector_checks_exact"])
        self.assertTrue(self.r["direct_sum_verified"])

    def test_sector_hom_matrix(self):
        expected = {
            "homology": {"homology": 1, "axis": 0, "diagonal": 0, "generic": 0},
            "axis": {"homology": 0, "axis": 3, "diagonal": 0, "generic": 0},
            "diagonal": {"homology": 0, "axis": 0, "diagonal": 3, "generic": 0},
            "generic": {"homology": 0, "axis": 0, "diagonal": 0, "generic": 3},
        }
        self.assertEqual(self.r["sector_hom_dimension_matrix"], expected)
        self.assertEqual(
            self.r["sector_self_end_dimensions"],
            {"homology": 1, "axis": 3, "diagonal": 3, "generic": 3},
        )
        self.assertTrue(self.r["cross_sector_hom_zero"])
        self.assertEqual(self.r["recovered_total_commutant_dimension"], 10)

    def test_momentum_orbits(self):
        self.assertEqual(self.r["nonzero_momentum_orbit_count"], 9)
        self.assertEqual(
            self.r["momentum_orbits_by_type"],
            {
                "axis": {"count": 3, "orbit_sizes": [4, 4, 4]},
                "diagonal": {"count": 3, "orbit_sizes": [4, 4, 4]},
                "generic": {"count": 3, "orbit_sizes": [8, 8, 8]},
            },
        )
        self.assertEqual(self.r["galois_groups_by_type"], {"axis": 1, "diagonal": 1, "generic": 1})
        self.assertEqual(self.r["splitting_field_sector_count"], 10)
        self.assertTrue(self.r["multiplicity_free_over_splitting_field"])

    def test_adjudication(self):
        self.assertEqual(
            self.r["status"],
            "MULTIPLICITY_FREE_SECTORS_BUT_WEIGHT_NONUNIQUENESS",
        )
        self.assertEqual(self.r["residual_weight_dimension"], 10)
        self.assertEqual(self.r["projective_relative_weight_dimension"], 9)
        self.assertEqual(self.r["mixing_freedom_dimension"], 0)
        self.assertFalse(self.r["unique_canonical_source_sector"])

    def test_firewall(self):
        for key in (
            "new_source_semantics_axiom_added",
            "coupling_solver_reopened",
            "gravity_observables_evaluated",
            "uses_holonomy_selector",
            "uses_newton_or_gr",
            "uses_metric_selector",
            "uses_pruning_as_selector",
            "uses_entropy_as_selector",
            "uses_physical_time",
            "physical_gravity_derived",
            "scientific_breakthrough",
            "signal_of_life",
        ):
            self.assertFalse(self.r[key], key)
        self.assertEqual(self.r["Pillar_3"], "OPEN")


if __name__ == "__main__":
    unittest.main()
