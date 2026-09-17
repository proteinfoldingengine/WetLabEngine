import unittest


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

    def test_v9_energy_and_gradient_ignore_native_geometry_at_fixed_length(self):
        import torch
        p1 = self.p1
        p1.seed_all(11)
        n = 12
        x = p1.random_chain(n, seed=23) + 0.25 * torch.randn((n, 3))
        target_a = torch.randn((n, 3))
        target_b = 7.0 * torch.randn((n, 3)) + 31.0
        ctx_a = p1.FoldContext(target_a, "A")
        ctx_b = p1.FoldContext(target_b, "B")

        xa = x.clone().detach().requires_grad_(True)
        ea, _ = p1.energy_for_mode(xa, ctx_a, "v9")
        ga = torch.autograd.grad(ea, xa)[0]

        xb = x.clone().detach().requires_grad_(True)
        eb, _ = p1.energy_for_mode(xb, ctx_b, "v9")
        gb = torch.autograd.grad(eb, xb)[0]

        self.assertTrue(torch.equal(ea.detach(), eb.detach()))
        self.assertTrue(torch.equal(ga.detach(), gb.detach()))

    def test_reduction_control_modes_are_frozen(self):
        expected = {
            "baseline",
            "angle_only",
            "dihedral_only",
            "soft_contact_only",
            "ungated_full",
            "v9",
        }
        self.assertEqual(set(self.p1.CONTROL_MODES), expected)

    def test_ungated_full_removes_only_dynamic_gates(self):
        import torch
        p1 = self.p1
        p1.seed_all(31)
        n = 10
        target = torch.randn((n, 3))
        ctx = p1.FoldContext(target, "T")
        x = p1.random_chain(n, seed=4) + 0.1 * torch.randn((n, 3))
        e_ungated, obs = p1.energy_for_mode(x, ctx, "ungated_full")
        expected = p1.v9_energy_from_observables(obs, gate_sigma=1.0, gate_closure=1.0)
        self.assertTrue(torch.equal(e_ungated.detach(), expected.detach()))


if __name__ == "__main__":
    unittest.main()
