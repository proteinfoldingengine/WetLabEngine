from __future__ import annotations

import math
import unittest

import torch

import p8b_core as p8b


class P8BContractTests(unittest.TestCase):
    def test_frozen_protocol(self):
        self.assertEqual(p8b.TARGET_NAME, "1VII")
        self.assertEqual(p8b.SEEDS, tuple(range(42, 50)))
        self.assertEqual(p8b.MODES, (
            "dynamic_622",
            "compaction_only",
            "force_gate_only",
            "all_lockin_from_start",
        ))
        self.assertEqual(p8b.STEPS, 2000)
        self.assertEqual(p8b.TORSION_LEARNING_RATE, 0.001)
        self.assertEqual(p8b.BETTI_THRESHOLD, 8)
        self.assertEqual(p8b.DAG_LIFETIME, 100)
        self.assertEqual(p8b.FORCE_LIFETIME, 50)

    def test_recovered_coefficients_are_frozen(self):
        expected = {
            "k_contact_spring_base": 1.5,
            "k_df_funnel": 6000.0,
            "k_phi_torque_base": 1.0,
            "k_lj_repulsion_base": 1.25,
            "k_hydro_base": 0.75,
            "k_electrostatic_base": 1.0,
            "k_rama": 0.05,
            "contact_dist": 8.0,
            "DEBYE_LENGTH": 5.0,
        }
        for key, value in expected.items():
            self.assertEqual(p8b.RECOVERED_CONSTANTS[key], value)

    def test_p6_backbone_geometry_is_exact(self):
        target = p8b.load_target()
        phi_free, psi = p8b.initial_torsions(len(target.sequence), 42)
        n, ca, c = p8b.reconstruct(phi_free, psi)
        length_drift, angle_drift = p8b.covalent_drift(n, ca, c)
        self.assertLess(length_drift, 1e-8)
        self.assertLess(angle_drift, 1e-8)

    def test_identical_seed_initialization_across_arms(self):
        target = p8b.load_target()
        reference = p8b.initial_torsions(len(target.sequence), 42)
        for _mode in p8b.MODES:
            candidate = p8b.initial_torsions(len(target.sequence), 42)
            self.assertTrue(torch.equal(reference[0], candidate[0]))
            self.assertTrue(torch.equal(reference[1], candidate[1]))

    def test_exact_recovered_gate_trace_on_qualifying_fixture(self):
        state = p8b.ControllerState()
        phases = []
        contact_active = []
        for step in range(100):
            phase, active = p8b.update_controller(
                state=state,
                mode="dynamic_622",
                betti1_count=8,
                step=step,
            )
            phases.append(phase)
            contact_active.append(active)
        self.assertEqual(phases[0], "Compaction")
        self.assertEqual(phases[98], "Compaction")
        self.assertEqual(phases[99], "LockIn")
        self.assertFalse(any(contact_active[:99]))
        self.assertTrue(contact_active[99])

    def test_control_semantics(self):
        for mode, expected_phase0, expected_contact0 in (
            ("compaction_only", "Compaction", False),
            ("force_gate_only", "LockIn", False),
            ("all_lockin_from_start", "LockIn", True),
        ):
            state = p8b.ControllerState()
            phase, active = p8b.update_controller(
                state=state,
                mode=mode,
                betti1_count=8,
                step=0,
            )
            self.assertEqual(phase, expected_phase0)
            self.assertEqual(active, expected_contact0)

    def test_native_firewall(self):
        target = p8b.load_target()
        phi_free, psi = p8b.initial_torsions(len(target.sequence), 42)
        phi0 = phi_free.clone().requires_grad_(True)
        psi0 = psi.clone().requires_grad_(True)
        state0 = p8b.ControllerState()
        e0, _ = p8b.coordinate_objective(
            target.sequence, phi0, psi0, state0, "dynamic_622", step=0
        )
        g0 = torch.autograd.grad(e0, (phi0, psi0))

        altered = p8b.Target(
            name=target.name,
            sequence=target.sequence,
            native_ca=target.native_ca * 7.0 + 123.456,
        )
        phi1 = phi_free.clone().requires_grad_(True)
        psi1 = psi.clone().requires_grad_(True)
        state1 = p8b.ControllerState()
        e1, _ = p8b.coordinate_objective(
            altered.sequence, phi1, psi1, state1, "dynamic_622", step=0
        )
        g1 = torch.autograd.grad(e1, (phi1, psi1))

        self.assertEqual(float(e0.detach()), float(e1.detach()))
        self.assertTrue(torch.equal(g0[0], g1[0]))
        self.assertTrue(torch.equal(g0[1], g1[1]))

    def test_no_native_argument_in_coordinate_objective(self):
        import inspect
        params = inspect.signature(p8b.coordinate_objective).parameters
        self.assertNotIn("native_ca", params)
        self.assertNotIn("native", params)


if __name__ == "__main__":
    unittest.main()
