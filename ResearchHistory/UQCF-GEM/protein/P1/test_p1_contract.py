import hashlib
import unittest
from pathlib import Path


class TestP1Contract(unittest.TestCase):
    def setUp(self):
        import p1_core
        self.p1 = p1_core

    def test_seed_all_controls_torch_rng(self):
        import torch
        self.p1.seed_all(1701)
        a = torch.randn(16)
        self.p1.seed_all(1701)
        b = torch.randn(16)
        self.assertTrue(torch.equal(a, b))

    def test_every_energy_mode_ignores_native_geometry_at_fixed_length(self):
        import torch
        p1 = self.p1
        p1.seed_all(11)
        n = 12
        x = p1.random_chain(n, seed=23) + 0.25 * torch.randn((n, 3))
        target_a = torch.randn((n, 3))
        target_b = 7.0 * torch.randn((n, 3)) + 31.0
        ctx_a = p1.FoldContext(target_a, "A")
        ctx_b = p1.FoldContext(target_b, "B")

        for mode in p1.CONTROL_MODES:
            with self.subTest(mode=mode):
                xa = x.clone().detach().requires_grad_(True)
                ea, _ = p1.energy_for_mode(xa, ctx_a, mode)
                ga = torch.autograd.grad(ea, xa)[0]

                xb = x.clone().detach().requires_grad_(True)
                eb, _ = p1.energy_for_mode(xb, ctx_b, mode)
                gb = torch.autograd.grad(eb, xb)[0]

                self.assertTrue(torch.equal(ea.detach(), eb.detach()))
                self.assertTrue(torch.equal(ga.detach(), gb.detach()))

    def test_reduction_control_modes_are_frozen(self):
        expected = (
            "baseline",
            "angle_only",
            "dihedral_only",
            "soft_contact_only",
            "static_combo",
            "fixed_gate",
            "v9",
        )
        self.assertEqual(self.p1.CONTROL_MODES, expected)

    def test_static_combo_removes_dynamic_gate_compression(self):
        import torch
        p1 = self.p1
        p1.seed_all(31)
        n = 10
        target = torch.randn((n, 3))
        ctx = p1.FoldContext(target, "T")
        x = p1.random_chain(n, seed=4) + 0.1 * torch.randn((n, 3))
        e_static, obs = p1.energy_for_mode(x, ctx, "static_combo")
        expected = p1.v9_energy_from_observables(
            obs, gate_sigma=1.0, gate_closure=1.0
        )
        self.assertTrue(torch.equal(e_static.detach(), expected.detach()))

    def test_fixed_gate_constants_are_frozen_from_historical_ablation(self):
        p1 = self.p1
        self.assertEqual(p1.FIXED_GATE_SIGMA, 0.1956)
        self.assertEqual(p1.FIXED_GATE_CLOSURE, 0.0393)

    def test_fixed_gate_uses_constants_not_live_gate_values(self):
        import torch
        p1 = self.p1
        p1.seed_all(37)
        n = 10
        target = torch.randn((n, 3))
        ctx = p1.FoldContext(target, "T")
        x = p1.random_chain(n, seed=9) + 0.1 * torch.randn((n, 3))
        e_fixed, obs = p1.energy_for_mode(x, ctx, "fixed_gate")
        expected = p1.v9_energy_from_observables(
            obs,
            gate_sigma=p1.FIXED_GATE_SIGMA,
            gate_closure=p1.FIXED_GATE_CLOSURE,
        )
        self.assertTrue(torch.equal(e_fixed.detach(), expected.detach()))

    def test_bound_input_payload_hashes_are_frozen(self):
        base = Path(__file__).resolve().parent / "inputs"
        expected = {
            "1UAO.ca_chainA_model1.pdb": (
                10,
                "b7cb0808f7dc0f4ed40bee9ca332696f50c2cc25d34ba53cabd7ba1ed03f468f",
            ),
            "1L2Y.ca_chainA_model1.pdb": (
                20,
                "84179b355a043df03e98f432dd2b2fbba4035b4f7df2e4928feabec8baed4378",
            ),
        }
        for name, (ca_count, expected_sha) in expected.items():
            with self.subTest(name=name):
                payload = (base / name).read_bytes()
                self.assertEqual(hashlib.sha256(payload).hexdigest(), expected_sha)
                self.assertEqual(
                    sum(
                        1
                        for line in payload.decode("ascii").splitlines()
                        if line.startswith("ATOM") and line[12:16].strip() == "CA"
                    ),
                    ca_count,
                )


if __name__ == "__main__":
    unittest.main()
