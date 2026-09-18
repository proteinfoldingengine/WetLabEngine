import hashlib
import json
import subprocess
import unittest
from dataclasses import replace
from pathlib import Path

import torch

import p6_core as p6


class P6ContractTests(unittest.TestCase):
    def test_frozen_protocol_constants(self):
        self.assertEqual(("1VII", "1L2Y", "1UAO"), p6.TARGET_NAMES)
        self.assertEqual(
            ("physical_real_sequence", "physical_shuffled_sequence", "generic_collapse"),
            p6.MODES,
        )
        self.assertEqual(tuple(range(6)), p6.SEEDS)
        self.assertEqual(300, p6.STEPS)
        self.assertAlmostEqual(0.02, p6.LEARNING_RATE)
        self.assertEqual(4, p6.CONTACT_MIN_SEQ_SEPARATION)
        self.assertAlmostEqual(8.0, p6.NATIVE_CONTACT_CUTOFF_A)
        self.assertEqual((0.75, 1.25), p6.RG_RATIO_GATE)

    def test_exact_historical_input_provenance_is_bound(self):
        manifest = json.loads(Path("P6_SOURCE_MANIFEST.json").read_text())
        expected_full = {
            "1L2Y": "5d1bbb545a312dfff1ae1e64b6d8addecb2f561ddc4011aeb5bee9d1dfcd4438",
            "1UAO": "e827fae677f8e96d1320688694b3db96bcc73050f81c6f842efc2e0ce9937e1e",
        }
        expected_excerpt = {
            "1L2Y": (
                "inputs/1L2Y.chainA_model1_NCAC.pdb",
                "3bcf838a433d65723afd175836fd727779e872d27d1b2d20eefbd729ad009e18",
            ),
            "1UAO": (
                "inputs/1UAO.chainA_model1_NCAC.pdb",
                "2c582e51deb46bae17bc02219550c98c29aa69fab6647d828481983e8406ed3e",
            ),
        }
        for name, full_digest in expected_full.items():
            self.assertEqual(full_digest, manifest["targets"][name]["full_pdb_sha256"])
            path_text, digest = expected_excerpt[name]
            path = Path(path_text)
            self.assertTrue(path.is_file(), path)
            self.assertEqual(digest, hashlib.sha256(path.read_bytes()).hexdigest())
            self.assertEqual(digest, manifest["targets"][name]["evaluator_excerpt_sha256"])

        p5_1vii = Path("../P5/inputs/1VII.pdb")
        self.assertTrue(p5_1vii.is_file())
        actual_blob = subprocess.check_output(["git", "hash-object", str(p5_1vii)], text=True).strip()
        self.assertEqual("dc55a7f18ce79b6db592240bdb7dcee96a4c1b8b", actual_blob)
        self.assertEqual(actual_blob, manifest["targets"]["1VII"]["git_blob"])

    def test_canonical_geometry_is_target_independent(self):
        a = p6.canonical_geometry(20)
        b = p6.canonical_geometry(20)
        for field in (
            "n_ca_lengths",
            "ca_c_lengths",
            "c_n_lengths",
            "n_ca_c_angles",
            "ca_c_n_angles",
            "c_n_ca_angles",
            "omega",
        ):
            torch.testing.assert_close(
                getattr(a, field), getattr(b, field), rtol=0.0, atol=0.0
            )

    def test_initial_torsions_are_deterministic_and_target_native_blind(self):
        a = p6.initial_torsions(20, seed=3)
        b = p6.initial_torsions(20, seed=3)
        c = p6.initial_torsions(20, seed=4)
        torch.testing.assert_close(a[0], b[0], rtol=0.0, atol=0.0)
        torch.testing.assert_close(a[1], b[1], rtol=0.0, atol=0.0)
        self.assertGreater(float(torch.max(torch.abs(a[0] - c[0]))), 1e-6)

    def test_sequence_shuffles_are_frozen_composition_preserving_and_nonidentity(self):
        for name in p6.TARGET_NAMES:
            target = p6.load_target(name)
            shuffled = p6.shuffled_sequence(name)
            self.assertEqual(len(target.sequence), len(shuffled))
            self.assertEqual(sorted(target.sequence), sorted(shuffled))
            self.assertNotEqual(target.sequence, shuffled)
            self.assertEqual(shuffled, p6.shuffled_sequence(name))

    def test_objective_and_gradients_are_native_evaluator_blind(self):
        target = p6.load_target("1VII")
        pf0, ps0 = p6.initial_torsions(len(target.sequence), seed=2)
        scale = p6.generic_collapse_scale(target.sequence, pf0, ps0)

        def value_and_grad(t):
            pf = pf0.clone().requires_grad_(True)
            ps = ps0.clone().requires_grad_(True)
            e, _, _ = p6.objective(
                t, pf, ps, "physical_real_sequence", generic_scale=scale
            )
            g = torch.autograd.grad(e, (pf, ps))
            return float(e.detach()), tuple(x.detach() for x in g)

        e0, g0 = value_and_grad(target)
        moved = replace(target, native_ca=target.native_ca + 123.456)
        e1, g1 = value_and_grad(moved)
        self.assertAlmostEqual(e0, e1, places=12)
        torch.testing.assert_close(g0[0], g1[0], rtol=0.0, atol=1e-12)
        torch.testing.assert_close(g0[1], g1[1], rtol=0.0, atol=1e-12)

    def test_generic_null_initial_nonlocal_gradient_is_matched(self):
        target = p6.load_target("1VII")
        pf0, ps0 = p6.initial_torsions(len(target.sequence), seed=1)
        scale = p6.generic_collapse_scale(target.sequence, pf0, ps0)
        gp = p6.initial_nonlocal_gradient_norm(
            target.sequence, pf0, ps0, "physical_real_sequence", generic_scale=scale
        )
        gg = p6.initial_nonlocal_gradient_norm(
            target.sequence, pf0, ps0, "generic_collapse", generic_scale=scale
        )
        self.assertAlmostEqual(gp, gg, places=9)

    def test_topk_precision_uses_fixed_contact_budget(self):
        native = torch.tensor(
            [[0.,0.,0.],[3.8,0.,0.],[7.6,0.,0.],[11.4,0.,0.],[0.,4.,0.],[3.8,4.,0.]],
            dtype=torch.float64,
        )
        model = native.clone()
        precision, k = p6.topk_native_contact_precision(model, native)
        self.assertEqual(3, k)
        self.assertGreaterEqual(precision, 0.0)
        self.assertLessEqual(precision, 1.0)

    def test_exact_sign_flip_and_holm_controls(self):
        self.assertEqual(1.0, p6.exact_sign_flip_p([1.0, -1.0]))
        a, b = p6.holm_two(0.01, 0.2)
        self.assertAlmostEqual(0.02, a)
        self.assertAlmostEqual(0.2, b)

    def test_canonical_reconstruction_preserves_covalent_geometry(self):
        n_res = 20
        geom = p6.canonical_geometry(n_res)
        pf, ps = p6.initial_torsions(n_res, seed=5)
        phi = torch.cat([geom.phi[:1], pf])
        n, ca, c = p6.reconstruct_backbone(geom, phi, ps)
        dl, da = p6.covalent_drift(geom, n, ca, c)
        self.assertLess(dl, 1e-8)
        self.assertLess(da, 1e-8)


if __name__ == "__main__":
    unittest.main()
