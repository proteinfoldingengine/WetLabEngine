import math
import unittest
from dataclasses import replace

import torch

import p5_core as p5


class P5ContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        torch.set_num_threads(1)
        cls.villin = p5.load_target("1VII")
        cls.crambin = p5.load_target("1CRN")

    def test_target_identities_and_sizes(self):
        self.assertEqual(36, self.villin.native_ca.shape[0])
        self.assertEqual(46, self.crambin.native_ca.shape[0])
        self.assertEqual(36, len(self.villin.sequence))
        self.assertEqual(46, len(self.crambin.sequence))
        self.assertEqual("A", self.villin.residue_ids[0].chain_id)
        self.assertEqual("A", self.crambin.residue_ids[0].chain_id)

    def test_kinematic_roundtrip_preserves_source(self):
        for target in (self.villin, self.crambin):
            n, ca, c = p5.bk.reconstruct_chain_backbone(
                target.geometry, target.geometry.phi, target.geometry.psi
            )
            self.assertLess(float(torch.max(torch.abs(n - target.native_n))), 1e-8)
            self.assertLess(float(torch.max(torch.abs(ca - target.native_ca))), 1e-8)
            self.assertLess(float(torch.max(torch.abs(c - target.native_c))), 1e-8)

    def test_random_torsion_state_preserves_covalent_geometry(self):
        for target in (self.villin, self.crambin):
            pf, ps = p5.initial_torsions(target, 3)
            phi = torch.cat([target.geometry.phi[:1], pf])
            n, ca, c = p5.bk.reconstruct_chain_backbone(target.geometry, phi, ps)
            dl, da = p5.covalent_drift(target, n, ca, c)
            self.assertLess(dl, 1e-8)
            self.assertLess(da, 1e-8)

    def test_matched_initial_states_are_deterministic(self):
        for target in (self.villin, self.crambin):
            a = p5.initial_torsions(target, 5)
            b = p5.initial_torsions(target, 5)
            torch.testing.assert_close(a[0], b[0], rtol=0.0, atol=0.0)
            torch.testing.assert_close(a[1], b[1], rtol=0.0, atol=0.0)
            c = p5.initial_torsions(target, 6)
            self.assertGreater(float(torch.max(torch.abs(a[0] - c[0]))), 1e-6)

    def test_energy_is_native_evaluator_blind(self):
        target = self.villin
        pf, ps = p5.initial_torsions(target, 2)
        scales = p5.regularizer_scales(target, pf, ps)
        e0, _, _ = p5.objective(target, pf, ps, "rama_entropy", scales)
        shifted = replace(target, native_ca=target.native_ca + 123.456)
        e1, _, _ = p5.objective(shifted, pf, ps, "rama_entropy", scales)
        self.assertAlmostEqual(float(e0), float(e1), places=12)

    def test_regularizer_initial_gradient_norms_are_matched(self):
        target = self.villin
        pf0, ps0 = p5.initial_torsions(target, 1)
        scales = p5.regularizer_scales(target, pf0, ps0)
        pf = pf0.clone().requires_grad_(True)
        ps = ps0.clone().requires_grad_(True)
        phi = torch.cat([target.geometry.phi[:1], pf])
        rama = scales["rama_scale"] * p5.ramachandran_energy(phi, ps)
        variance = scales["variance_scale"] * p5.circular_variance_energy(phi, ps)
        entropy = scales["entropy_scale"] * p5.tpo_entropy_energy(phi, ps)
        combo = scales["combo_outer_scale"] * (
            0.5 * scales["rama_scale"] * p5.ramachandran_energy(phi, ps)
            + 0.5 * scales["entropy_scale"] * p5.tpo_entropy_energy(phi, ps)
        )
        target_norm = scales["target_regularizer_gradient_norm"]
        for energy in (rama, variance, entropy, combo):
            g = p5._gradient_norm(energy, (pf, ps), retain_graph=True)
            self.assertAlmostEqual(target_norm, g, places=9)

    def test_kabsch_rmsd_is_rigid_transform_invariant(self):
        x = self.villin.native_ca[:10]
        theta = 0.713
        r = x.new_tensor([
            [math.cos(theta), -math.sin(theta), 0.0],
            [math.sin(theta), math.cos(theta), 0.0],
            [0.0, 0.0, 1.0],
        ])
        moved = x @ r.T + x.new_tensor([8.2, -3.1, 5.7])
        self.assertLess(p5.kabsch_rmsd(moved, x), 1e-9)

    def test_exact_sign_flip_and_holm_controls(self):
        self.assertEqual(1.0, p5.exact_sign_flip_p([1.0, -1.0]))
        a, b = p5.holm_two(0.01, 0.2)
        self.assertAlmostEqual(0.02, a)
        self.assertAlmostEqual(0.2, b)

    def test_frozen_modes_and_protocol(self):
        self.assertEqual(
            ("baseline", "rama", "variance", "entropy", "rama_entropy", "entropy_historical_0p02"),
            p5.MODES,
        )
        self.assertEqual(tuple(range(8)), p5.SEEDS)
        self.assertEqual(120, p5.STEPS)
        self.assertAlmostEqual(0.03, p5.LEARNING_RATE)
        self.assertAlmostEqual(0.5, p5.GRADIENT_MATCH_RATIO)
        self.assertAlmostEqual(0.02, p5.HISTORICAL_ENTROPY_K)


if __name__ == "__main__":
    unittest.main()
