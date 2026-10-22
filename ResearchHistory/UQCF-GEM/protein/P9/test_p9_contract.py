from __future__ import annotations

import math
import sys
from pathlib import Path

import torch

ROOT = Path(__file__).resolve().parent
P1_DIR = ROOT.parent / "P1"
P6_DIR = ROOT.parent / "P6"
for path in (ROOT, P1_DIR, P6_DIR):
    if str(path) not in sys.path:
        sys.path.insert(0, str(path))

import p1_core as p1
import p6_core as p6
import p9_core as p9


def test_target_family_and_state_matrix_are_frozen():
    assert p9.TARGET_NAMES == ("1VII", "1L2Y", "1UAO", "1CRN")
    assert p9.SEEDS == tuple(range(6))
    assert p9.CHECKPOINTS == (50, 100, 150, 200)
    assert p9.GENERATOR_STEPS == 200
    assert p9.HANDOFF_STEPS == 100
    assert len(p9.expected_state_keys()) == 96
    assert len(set(p9.expected_state_keys())) == 96


def test_1crn_adapter_uses_pinned_input_and_p6_target_shape():
    target = p9.load_target("1CRN")
    assert isinstance(target, p6.Target)
    assert target.name == "1CRN"
    assert len(target.sequence) == 46
    assert target.native_ca.shape == (46, 3)
    assert target.native_ca.dtype == torch.float64


def test_coherence_score_reproduces_frozen_p1_v9_formula():
    target = p9.load_target("1VII")
    phi_free, psi = p6.initial_torsions(len(target.sequence), seed=0)
    _, (_, ca, _), _ = p9.p6_objective_from_state(
        target, phi_free, psi
    )
    scores = p9.coherence_scores(ca)

    ctx = p1.FoldContext(
        torch.zeros((ca.shape[0], 3), dtype=ca.dtype),
        "dummy",
    )
    obs = p1.bridge_observables(ca, ctx)

    assert abs(scores["sigma_bridge"] - float(obs["sigma_bridge"])) < 1e-12
    assert abs(scores["closure_ready"] - float(obs["closure_ready"])) < 1e-12

    r_micro = math.exp(
        -(
            0.60 * scores["dir_pen"]
            + 0.20 * scores["angle_var"]
            + 0.26 * scores["dihed_smooth"]
        )
    )
    compactness = math.exp(-0.12 * scores["rg"])
    c_meso = 1.0 / (
        1.0
        + math.exp(
            -(
                1.8 * (scores["soft_contacts"] - 0.40)
                - 0.42 * scores["density_var"]
                + 0.8 * compactness
            )
        )
    )
    flat_primary = (
        0.36 * r_micro
        + 0.24 * c_meso
        + 0.40 * scores["loop_compat"]
    )
    flat_secondary = (
        0.32 * r_micro
        + 0.20 * c_meso
        + 0.48 * scores["loop_compat"]
    )
    assert abs(scores["R_micro"] - r_micro) < 1e-12
    assert abs(scores["C_meso"] - c_meso) < 1e-12
    assert abs(scores["flat_primary"] - flat_primary) < 1e-12
    assert abs(scores["flat_secondary"] - flat_secondary) < 1e-12


def test_candidate_score_is_native_information_blind():
    target = p9.load_target("1L2Y")
    phi_free, psi = p6.initial_torsions(len(target.sequence), seed=2)
    energy0, (_, ca0, _), _ = p9.p6_objective_from_state(
        target, phi_free, psi
    )
    scores0 = p9.coherence_scores(ca0)

    changed = p6.Target(
        name=target.name,
        sequence=target.sequence,
        native_ca=target.native_ca * 11.0 + 777.0,
    )
    energy1, (_, ca1, _), _ = p9.p6_objective_from_state(
        changed, phi_free, psi
    )
    scores1 = p9.coherence_scores(ca1)

    assert abs(float(energy0) - float(energy1)) < 1e-12
    assert torch.allclose(ca0, ca1, rtol=0.0, atol=1e-12)
    for key in (
        "sigma_bridge",
        "closure_ready",
        "flat_primary",
        "flat_secondary",
    ):
        assert abs(scores0[key] - scores1[key]) < 1e-12


def test_group_spearman_and_exact_sign_flip_primitives():
    assert abs(p9.spearman_rank([1, 2, 3, 4], [10, 20, 30, 40]) - 1.0) < 1e-12
    assert abs(p9.spearman_rank([1, 2, 3, 4], [40, 30, 20, 10]) + 1.0) < 1e-12
    assert p9.exact_sign_flip_p([1.0, 1.0, 1.0, 1.0]) == 0.125


def test_state_bank_is_deterministic_and_checkpoint_complete():
    target = p9.load_target("1UAO")
    a = p9.generate_state_bank(target, seed=0)
    b = p9.generate_state_bank(target, seed=0)
    assert tuple(sorted(a)) == p9.CHECKPOINTS
    assert tuple(sorted(b)) == p9.CHECKPOINTS
    for step in p9.CHECKPOINTS:
        assert torch.equal(a[step][0], b[step][0])
        assert torch.equal(a[step][1], b[step][1])


def test_handoff_is_deterministic_and_preserves_covalent_geometry():
    target = p9.load_target("1UAO")
    state = p9.generate_state_bank(target, seed=1)[50]
    a = p9.run_handoff(target, *state)
    b = p9.run_handoff(target, *state)
    assert a["best_handoff_ca_rmsd_A"] == b["best_handoff_ca_rmsd_A"]
    assert a["final_topk_native_contact_precision"] == b["final_topk_native_contact_precision"]
    assert a["max_bond_length_drift_A"] < 1e-8
    assert a["max_bond_angle_drift_rad"] < 1e-8
    assert not a["failed"]


def test_adjudicator_requires_all_frozen_go_conditions():
    good = p9.synthetic_acceptance_fixture(go=True)
    bad = p9.synthetic_acceptance_fixture(go=False)
    assert p9.adjudicate(good)["decision"] == "GO_TRANSFERABLE_COHERENCE_HANDOFF_COORDINATE"
    assert p9.adjudicate(bad)["decision"] == "NO_GO_TRANSFERABLE_COHERENCE_HANDOFF_COORDINATE"
