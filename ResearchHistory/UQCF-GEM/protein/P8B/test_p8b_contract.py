import unittest

import torch

import p8b_core as p8b


class P8BContractTests(unittest.TestCase):
    def test_frozen_protocol_constants(self):
        self.assertEqual(("1VII", "1L2Y", "1UAO"), p8b.TARGET_NAMES)
        self.assertEqual(tuple(range(6)), p8b.SEEDS)
        self.assertEqual(
            (
                "recovered_state_gate",
                "fixed_step99_lockin",
                "static_lockin",
                "compaction_only",
            ),
            p8b.MODES,
        )
        self.assertEqual(2000, p8b.STEPS)
        self.assertEqual(0.02, p8b.LEARNING_RATE)
        self.assertEqual(8, p8b.BETTI_PROXY_THRESHOLD)
        self.assertEqual(100, p8b.DAG_QUALIFYING_COUNT)
        self.assertEqual(50, p8b.FORCE_QUALIFYING_COUNT)
        self.assertEqual(120, p8b.BETTI_HISTORY_MAXLEN)
        self.assertEqual(99, p8b.FIXED_LOCKIN_FIRST_STEP)

    def test_historical_proxy_is_exact_contact_graph_formula(self):
        # With all 10 C-alpha sites coincident, every non-adjacent pair is
        # inside 8 A. There are C(10,2)-9 = 36 such pairs.
        # Historical proxy = 36 - (10-1) = 27.
        coords = torch.zeros((10, 3), dtype=torch.float64)
        self.assertEqual(27, p8b.historical_betti1_proxy(coords))

        # A widely separated chain has no non-adjacent contacts and clamps to 0.
        coords = torch.arange(10, dtype=torch.float64).unsqueeze(1).repeat(1, 3) * 20.0
        self.assertEqual(0, p8b.historical_betti1_proxy(coords))

    def test_history_qualifying_count_is_not_consecutive_lifetime(self):
        h = p8b.HistoricalBettiHistory()
        for i in range(99):
            h.append(8)
            if i < 20:
                h.append(0)
        # Sliding history is 119 values: 99 qualifying plus 20 nonqualifying.
        self.assertEqual(99, h.qualifying_count())
        h.append(8)
        self.assertEqual(100, h.qualifying_count())

        controller = p8b.RecoveredController()
        # Seed the controller history with the same nonconsecutive record.
        for i in range(99):
            controller.observe(8)
            if i < 20:
                controller.observe(0)
        self.assertEqual("Compaction", controller.phase)
        event = controller.observe(8)
        self.assertTrue(event["transitioned"])
        self.assertEqual("LockIn", controller.phase)

    def test_fixed_schedule_matches_earliest_possible_100th_qualifier(self):
        self.assertEqual("Compaction", p8b.fixed_schedule_phase(98))
        self.assertEqual("LockIn", p8b.fixed_schedule_phase(99))

    def test_coordinate_force_sets_are_frozen(self):
        self.assertEqual(
            {
                "lennard_jones_repulsion",
                "angular_torque_locking",
                "ramachandran_potential",
                "fractal_compaction_funnel",
                "hydrophobic_collapse",
            },
            set(p8b.COMPACTION_COORDINATE_FORCES),
        )
        self.assertEqual(
            {"screened_electrostatics", "contact_springs"},
            set(p8b.LOCKIN_ADDITIONAL_COORDINATE_FORCES),
        )
        self.assertNotIn("gamma_well", p8b.ALL_COORDINATE_FORCES)
        self.assertNotIn("torsional_incoherence_penalty", p8b.ALL_COORDINATE_FORCES)

    def test_historical_coefficients_are_untuned(self):
        self.assertEqual(6000.0, p8b.K_DF_FUNNEL)
        self.assertEqual(1.5, p8b.K_CONTACT)
        self.assertEqual(1.0, p8b.K_PHI_TORQUE)
        self.assertEqual(1.25, p8b.K_LJ)
        self.assertEqual(0.75, p8b.K_HYDRO)
        self.assertEqual(1.0, p8b.K_ELECTROSTATIC)
        self.assertEqual(0.05, p8b.K_RAMA)
        self.assertEqual(8.0, p8b.CONTACT_DIST_A)
        self.assertEqual(5.0, p8b.DEBYE_LENGTH_A)

    def test_initial_torsions_are_common_across_arms(self):
        target = p8b.load_target("1UAO")
        reference = p8b.initial_torsions(len(target.sequence), seed=3)
        for mode in p8b.MODES:
            trial = p8b.initial_torsions_for_mode(target, seed=3, mode=mode)
            self.assertTrue(torch.equal(reference[0], trial[0]))
            self.assertTrue(torch.equal(reference[1], trial[1]))

    def test_native_information_firewall(self):
        self.assertTrue(p8b.native_firewall_selfcheck())


if __name__ == "__main__":
    unittest.main()
