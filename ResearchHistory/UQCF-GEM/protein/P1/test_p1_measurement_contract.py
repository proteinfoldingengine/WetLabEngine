import unittest
from pathlib import Path

import torch

import p1_core as p1
import p1_measurement as m


class TestP1MeasurementContract(unittest.TestCase):
    def test_bound_inputs_verify_and_have_frozen_lengths(self):
        base = Path(__file__).resolve().parent
        verified = m.verify_bound_inputs(base)
        self.assertEqual(verified["1UAO"]["ca_count"], 10)
        self.assertEqual(verified["1L2Y"]["ca_count"], 20)

    def test_common_random_packet_is_repeatable(self):
        a = m.make_trial_inputs(10, 0, 4)
        b = m.make_trial_inputs(10, 0, 4)
        for xa, xb in zip(a, b):
            self.assertTrue(torch.equal(xa, xb))

    def test_common_random_packet_changes_with_seed(self):
        a = m.make_trial_inputs(10, 0, 4)
        b = m.make_trial_inputs(10, 0, 5)
        self.assertFalse(torch.equal(a[0], b[0]))
        self.assertFalse(torch.equal(a[1], b[1]))
        self.assertFalse(torch.equal(a[2], b[2]))

    def test_exact_sign_flip_known_case(self):
        self.assertEqual(m.exact_sign_flip_pvalue([1.0, 1.0, 1.0]), 0.25)

    def test_holm_adjustment(self):
        adjusted = m.holm_adjust({"static_combo": 0.01, "fixed_gate": 0.04})
        self.assertAlmostEqual(adjusted["static_combo"], 0.02)
        self.assertAlmostEqual(adjusted["fixed_gate"], 0.04)

    def test_short_stage_is_deterministic_with_frozen_noise(self):
        base = Path(__file__).resolve().parent
        target = m.load_ca_coords(base / "inputs/1UAO.ca_chainA_model1.pdb")
        ctx = p1.FoldContext(target, "1UAO")
        init, pre_noise, _ = m.make_trial_inputs(10, 0, 2)
        noise = pre_noise[:3]

        a = m.optimize_stage(
            init, ctx, target, "v9", noise, "test", 0
        )
        b = m.optimize_stage(
            init, ctx, target, "v9", noise, "test", 0
        )
        self.assertTrue(torch.equal(a[0], b[0]))
        self.assertTrue(torch.equal(a[1], b[1]))
        self.assertEqual(a[2], b[2])


if __name__ == "__main__":
    unittest.main()
