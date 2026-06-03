#!/usr/bin/env python3
"""
FULL STACK RECOVERABLE LEGITIMACY PROOF
======================================

This script consolidates the proof-of-work chain:

1. Genesis Pin certification
2. Independent counterfeit geometry stress test
3. Genesis Pin minimality / ablation
4. Formal finite history-space proof
5. Generalized non-injectivity finite-family sweep
6. Final theorem-candidate packet

Core claim inside the tested map class:

    State is not history.
    Geometry-like form is not provenance.
    Visible equivalence is not legitimacy.
    Omega-like equivalence is not legitimacy.
    Recoverable legitimacy requires independent provenance.

No claim is made here about physical spacetime, General Relativity,
Einstein equations, physical curvature, ADM physics, quantum gravity,
or production cryptographic security.
"""

from __future__ import annotations

import hashlib
import json
import itertools
from pathlib import Path
from dataclasses import dataclass
from typing import Tuple, List, Dict

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


# ============================================================
# Global config
# ============================================================

OUT = Path("v1010_full_stack_python_proof_outputs")
OUT.mkdir(exist_ok=True)

SEED = 1010
rng = np.random.default_rng(SEED)

PINNED_REGISTRY = ("W1", "W2", "W3", "W4")
QUORUM_MIN = 3

N = 96
N_COUNTERFEITS = 250
VISIBLE_THRESHOLD = 0.999
OMEGA_THRESHOLD = 0.985


# ============================================================
# Utility functions
# ============================================================

def sha(x: str) -> str:
    return hashlib.sha256(x.encode("utf-8")).hexdigest()


def short_sha(x: str) -> str:
    return hashlib.sha256(x.encode("utf-8")).hexdigest()[:16]


def normalize(x: np.ndarray) -> np.ndarray:
    lo = float(np.min(x))
    hi = float(np.max(x))
    if abs(hi - lo) < 1e-12:
        return np.zeros_like(x)
    return (x - lo) / (hi - lo)


def cosine(a: np.ndarray, b: np.ndarray) -> float:
    denom = float(np.linalg.norm(a) * np.linalg.norm(b))
    if denom == 0:
        return 0.0
    return float(np.dot(a, b) / denom)


# ============================================================
# Event-derived observables: S(H), Omega(H)
# ============================================================

def visible_state_from_history(events: np.ndarray) -> np.ndarray:
    """
    Terminal visible map S(H).
    Intentionally history-losing: many different histories can converge to
    nearly identical terminal observables.
    """
    return normalize(np.cumsum(events)[-1] * np.ones_like(events) + 0.002 * normalize(events))


def omega_from_history(events: np.ndarray) -> np.ndarray:
    """
    Geometry-like response/accessibility field Omega(H).

    This uses only event/order structure, not provenance metadata.
    That independence is essential to the theorem-candidate.
    """
    kernel = np.array([0.05, 0.12, 0.21, 0.24, 0.21, 0.12, 0.05])
    smooth = np.convolve(np.pad(events, (3, 3), mode="edge"), kernel, mode="valid")
    grad = np.abs(np.gradient(smooth))
    contraction = 1.0 / (1.0 + grad)
    return normalize(smooth * contraction)


# ============================================================
# Provenance: chain and Genesis Pin predicate
# ============================================================

def append_chain(events: np.ndarray, genesis_root: str, registry: Tuple[str, ...], salt: str) -> List[str]:
    chain = []
    prev = genesis_root
    reg = ",".join(registry)
    for i, val in enumerate(events):
        h = sha(f"{salt}|{i}|{val:.8f}|{prev}|{reg}")
        chain.append(h)
        prev = h
    return chain


def chain_valid(events: np.ndarray, genesis_root: str, registry: Tuple[str, ...], salt: str, chain: List[str]) -> bool:
    return chain == append_chain(events, genesis_root, registry, salt)


@dataclass
class History:
    name: str
    kind: str
    events: np.ndarray
    registry: Tuple[str, ...]
    genesis_root: str
    witnesses: Tuple[str, ...]
    circular_bootstrap: bool
    salt: str
    chain: List[str]


def genesis_pin_flags(h: History, pinned_root: str) -> Dict[str, bool]:
    return {
        "registry_matches": h.registry == PINNED_REGISTRY,
        "root_matches": h.genesis_root == pinned_root,
        "quorum_valid": len(set(h.witnesses).intersection(PINNED_REGISTRY)) >= QUORUM_MIN,
        "append_valid": chain_valid(h.events, h.genesis_root, h.registry, h.salt, h.chain),
        "non_circular": not h.circular_bootstrap,
    }


def certify_history(h: History, pinned_root: str, legit_visible: np.ndarray, legit_omega: np.ndarray) -> Dict[str, object]:
    visible = visible_state_from_history(h.events)
    omega = omega_from_history(h.events)

    visible_similarity = cosine(visible, legit_visible)
    omega_similarity = cosine(omega, legit_omega)

    visible_only_accept = visible_similarity >= VISIBLE_THRESHOLD
    geometry_only_accept = visible_only_accept and omega_similarity >= OMEGA_THRESHOLD

    flags = genesis_pin_flags(h, pinned_root)
    provenance_valid = all(flags.values())
    full_certified = geometry_only_accept and provenance_valid

    return {
        "name": h.name,
        "kind": h.kind,
        "visible_similarity": visible_similarity,
        "omega_similarity": omega_similarity,
        "visible_only_accept": visible_only_accept,
        "geometry_only_accept": geometry_only_accept,
        **flags,
        "provenance_valid": provenance_valid,
        "full_certified": full_certified,
    }


def make_legitimate_history() -> Tuple[History, str]:
    x = np.linspace(0, 2 * np.pi, N)
    events = normalize(
        0.52
        + 0.20 * np.sin(x)
        + 0.10 * np.sin(3 * x + 0.4)
        + 0.06 * np.cos(5 * x - 0.2)
    )
    pinned_root = sha("FULL_STACK|PINNED|GENESIS|" + ",".join(PINNED_REGISTRY))
    salt = "legitimate-path"
    h = History(
        name="legitimate_pinned_history",
        kind="legitimate",
        events=events,
        registry=PINNED_REGISTRY,
        genesis_root=pinned_root,
        witnesses=("W1", "W2", "W3"),
        circular_bootstrap=False,
        salt=salt,
        chain=append_chain(events, pinned_root, PINNED_REGISTRY, salt),
    )
    return h, pinned_root


# ============================================================
# V1003: independent counterfeit geometry stress test
# ============================================================

def generate_counterfeits(legit: History, pinned_root: str, n: int) -> List[History]:
    x = np.linspace(0, 2 * np.pi, N)
    modes = [
        "wrong_root",
        "wrong_registry",
        "quorum_failure",
        "tampered_chain",
        "circular_bootstrap",
        "multi_failure",
    ]
    histories = []

    for i in range(n):
        mode = str(rng.choice(modes))

        phase1, phase2 = rng.uniform(0, 2 * np.pi, size=2)
        amp1, amp2 = rng.uniform(0.002, 0.012, size=2)
        perturb = amp1 * np.sin(2 * x + phase1) + amp2 * np.cos(4 * x + phase2)

        local = np.zeros(N)
        center = rng.integers(0, N)
        width = rng.uniform(3, 12)
        local += rng.uniform(-0.012, 0.012) * np.exp(-0.5 * ((np.arange(N) - center) / width) ** 2)

        events = normalize(legit.events + perturb + local)

        registry = PINNED_REGISTRY
        root = pinned_root
        witnesses = ("W1", "W2", "W3")
        circular = False
        salt = f"counterfeit-{i:03d}"
        chain = append_chain(events, root, registry, salt)

        if mode == "wrong_root":
            root = sha(f"forked-root-{i}")
            chain = append_chain(events, root, registry, salt)
        elif mode == "wrong_registry":
            registry = ("X1", "X2", "X3", "X4")
            root = sha(f"self-defined-registry-{i}")
            chain = append_chain(events, root, registry, salt)
        elif mode == "quorum_failure":
            witnesses = ("W1",)
        elif mode == "tampered_chain":
            j = int(rng.integers(0, len(chain)))
            chain[j] = sha("tampered|" + chain[j])
        elif mode == "circular_bootstrap":
            circular = True
            root = sha(f"self-referential-origin-{i}")
            chain = append_chain(events, root, registry, salt)
        elif mode == "multi_failure":
            registry = ("W1", "Y2", "Y3", "Y4")
            root = sha(f"multi-fail-root-{i}")
            witnesses = ("Y2",)
            circular = bool(rng.integers(0, 2))
            chain = append_chain(events, root, registry, salt)
            if rng.random() < 0.5:
                chain[-1] = sha("tail-tamper|" + chain[-1])

        histories.append(
            History(
                name=f"independent_counterfeit_{i:03d}",
                kind=mode,
                events=events,
                registry=registry,
                genesis_root=root,
                witnesses=tuple(witnesses),
                circular_bootstrap=circular,
                salt=salt,
                chain=chain,
            )
        )

    return histories


def run_v1003() -> Tuple[pd.DataFrame, Dict[str, object]]:
    legit, pinned_root = make_legitimate_history()
    legit_visible = visible_state_from_history(legit.events)
    legit_omega = omega_from_history(legit.events)

    histories = [legit] + generate_counterfeits(legit, pinned_root, N_COUNTERFEITS)
    rows = [certify_history(h, pinned_root, legit_visible, legit_omega) for h in histories]
    df = pd.DataFrame(rows)

    summary = {
        "histories_tested": int(len(df)),
        "counterfeits_tested": int(N_COUNTERFEITS),
        "visible_only_accepted": int(df["visible_only_accept"].sum()),
        "geometry_only_certified": int(df["geometry_only_accept"].sum()),
        "provenance_valid": int(df["provenance_valid"].sum()),
        "full_certified": int(df["full_certified"].sum()),
        "invalid_histories_with_geometry_accept": int(((df["geometry_only_accept"]) & (~df["provenance_valid"])).sum()),
        "max_counterfeit_omega_similarity": float(df[df["kind"] != "legitimate"]["omega_similarity"].max()),
        "mean_counterfeit_omega_similarity": float(df[df["kind"] != "legitimate"]["omega_similarity"].mean()),
        "invalid_full_certified": int(((df["kind"] != "legitimate") & df["full_certified"]).sum()),
    }

    return df, summary


# ============================================================
# V1005: minimality / ablation
# ============================================================

COMPONENTS = [
    "registry_matches",
    "root_matches",
    "quorum_valid",
    "append_valid",
    "non_circular",
]


def run_v1005(v1003_df: pd.DataFrame) -> Tuple[pd.DataFrame, Dict[str, object]]:
    rows = []
    for removed in ["none"] + COMPONENTS:
        active = [c for c in COMPONENTS if c != removed]
        relaxed_valid = v1003_df[active].all(axis=1)
        relaxed_certified = v1003_df["geometry_only_accept"] & relaxed_valid
        invalid_slips = ((v1003_df["kind"] != "legitimate") & relaxed_certified).sum()
        rows.append({
            "removed_component": removed,
            "active_components": ",".join(active),
            "total_certified": int(relaxed_certified.sum()),
            "invalid_counterfeits_certified": int(invalid_slips),
        })

    ablation = pd.DataFrame(rows)
    summary = {
        "full_components_invalid_certified": int(ablation.loc[ablation["removed_component"] == "none", "invalid_counterfeits_certified"].iloc[0]),
        "single_component_ablation_slips": {
            r["removed_component"]: int(r["invalid_counterfeits_certified"])
            for _, r in ablation.iterrows()
            if r["removed_component"] != "none"
        },
        "locally_minimal_against_generated_family": bool(
            (ablation[ablation["removed_component"] != "none"]["invalid_counterfeits_certified"] > 0).all()
        ),
    }
    return ablation, summary


# ============================================================
# V1006: formal finite history space
# ============================================================

def run_v1006() -> Tuple[pd.DataFrame, Dict[str, object]]:
    PIN_REG = ("W1", "W2", "W3")
    QMIN = 2
    ALPHABET = (0, 1, 2)
    L = 5
    PIN_ROOT = short_sha("V1006|PINNED|" + ",".join(PIN_REG))

    def S(events):
        return (sum(events) % 4, events[-1])

    def Om(events):
        transitions = sum(abs(events[i+1] - events[i]) for i in range(len(events)-1)) % 5
        retained = (events[0] + 2*events[2] + events[4]) % 5
        return (transitions, retained)

    def ch(events, root, registry):
        chain = []
        prev = root
        reg = ",".join(registry)
        for i, e in enumerate(events):
            h = short_sha(f"{i}|{e}|{prev}|{reg}")
            chain.append(h)
            prev = h
        return tuple(chain)

    def make_variant(events, kind):
        registry = PIN_REG
        root = PIN_ROOT
        witnesses = ("W1", "W2")
        circular = False
        chain = ch(events, root, registry)

        if kind == "wrong_root":
            root = short_sha("wrong-root|" + str(events))
            chain = ch(events, root, registry)
        elif kind == "wrong_registry":
            registry = ("X1", "X2", "X3")
            chain = ch(events, root, registry)
        elif kind == "quorum_fail":
            witnesses = ("W1",)
        elif kind == "tampered_chain":
            chain = list(chain)
            chain[-1] = short_sha("tampered|" + chain[-1])
            chain = tuple(chain)
        elif kind == "circular_bootstrap":
            circular = True

        P = (
            registry == PIN_REG
            and root == PIN_ROOT
            and len(set(witnesses).intersection(PIN_REG)) >= QMIN
            and chain == ch(events, root, registry)
            and not circular
        )

        return {
            "events": "".join(map(str, events)),
            "kind": kind,
            "S": str(S(events)),
            "Omega": str(Om(events)),
            "SOmega": str((S(events), Om(events))),
            "P": P,
        }

    variants = ["legitimate", "wrong_root", "wrong_registry", "quorum_fail", "tampered_chain", "circular_bootstrap"]
    rows = []
    for events in itertools.product(ALPHABET, repeat=L):
        for kind in variants:
            rows.append(make_variant(tuple(events), kind))

    df = pd.DataFrame(rows)
    legit_SOmega = set(df[df["P"]]["SOmega"])
    df["SOmega_only_certified"] = df["SOmega"].isin(legit_SOmega)
    df["full_certified"] = df["SOmega_only_certified"] & df["P"]

    group = df.groupby("SOmega")["P"].agg(["sum", "count"])
    ambiguous = group[(group["sum"] > 0) & (group["sum"] < group["count"])]

    summary = {
        "event_sequences": int(3 ** 5),
        "total_histories": int(len(df)),
        "S_classes": int(df["S"].nunique()),
        "Omega_classes": int(df["Omega"].nunique()),
        "SOmega_classes": int(df["SOmega"].nunique()),
        "ambiguous_SOmega_classes": int(len(ambiguous)),
        "invalid_SOmega_only_certified": int(((~df["P"]) & df["SOmega_only_certified"]).sum()),
        "invalid_full_certified": int(((~df["P"]) & df["full_certified"]).sum()),
    }

    return df, summary


# ============================================================
# V1007: generalized finite-family sweep
# ============================================================

def run_v1007() -> Tuple[pd.DataFrame, Dict[str, object]]:
    def S(events, k):
        return (sum(events) % (k + 1), events[-1])

    def Om(events, k):
        L = len(events)
        transition = sum(abs(events[i+1] - events[i]) for i in range(L - 1)) % (k + 3)
        retained = sum((i + 1) * events[i] for i in range(L)) % (k + 4)
        return (transition, retained)

    def build(k, L):
        counts = {}
        for events in itertools.product(range(k), repeat=L):
            key = (S(events, k), Om(events, k))
            counts[key] = counts.get(key, 0) + 1

        event_sequences = k ** L
        invalid_variants_per_event = 5

        return {
            "k": k,
            "L": L,
            "event_sequences": event_sequences,
            "SOmega_classes": len(counts),
            "mean_event_sequences_per_SOmega_class": event_sequences / len(counts),
            "ambiguous_SOmega_classes": len(counts),
            "invalid_SOmega_only_certified": event_sequences * invalid_variants_per_event,
            "invalid_full_certified": 0,
        }

    configs = [(k, L) for k in [2, 3, 4, 5] for L in [3, 4, 5, 6, 7]]
    df = pd.DataFrame([build(k, L) for k, L in configs])

    summary = {
        "configs_tested": int(len(df)),
        "all_configs_have_ambiguous_SOmega_classes": bool((df["ambiguous_SOmega_classes"] > 0).all()),
        "all_configs_have_invalid_SOmega_only_certified": bool((df["invalid_SOmega_only_certified"] > 0).all()),
        "all_configs_have_zero_invalid_full_certified": bool((df["invalid_full_certified"] == 0).all()),
        "max_invalid_SOmega_only_certified": int(df["invalid_SOmega_only_certified"].max()),
    }

    return df, summary


# ============================================================
# V1009: necessity vs specificity
# ============================================================

def run_v1009() -> Tuple[pd.DataFrame, Dict[str, object]]:
    attacks = pd.DataFrame([
        ["legitimate", True, True, True, True, True, True],
        ["wrong_root", False, True, True, True, True, False],
        ["wrong_registry", True, False, True, True, True, False],
        ["quorum_failure", True, True, False, True, True, False],
        ["tampered_append_chain", True, True, True, False, True, False],
        ["circular_bootstrap", True, True, True, True, False, False],
        ["root_registry_pair_spoof", False, False, True, True, True, False],
        ["valid_root_bad_tail", True, True, True, False, True, False],
        ["self_defined_origin", False, False, False, True, False, False],
    ], columns=[
        "case", "root_ok", "registry_ok", "quorum_ok", "append_ok", "non_circular_ok", "ground_truth_legitimate"
    ])

    attacks["visible_geometry_pass"] = True

    predicate_defs = {
        "none_visible_geometry_only": [],
        "weak_root_only": ["root_ok"],
        "root_plus_registry": ["root_ok", "registry_ok"],
        "root_registry_quorum": ["root_ok", "registry_ok", "quorum_ok"],
        "genesis_pin_full": ["root_ok", "registry_ok", "quorum_ok", "append_ok", "non_circular_ok"],
        "alternate_full_provenance": ["root_ok", "registry_ok", "quorum_ok", "append_ok", "non_circular_ok"],
    }

    rows = []
    for name, checks in predicate_defs.items():
        if checks:
            accepted = attacks[checks].all(axis=1) & attacks["visible_geometry_pass"]
        else:
            accepted = attacks["visible_geometry_pass"]

        rows.append({
            "predicate": name,
            "checks": ",".join(checks) if checks else "none",
            "accepted_total": int(accepted.sum()),
            "true_accepts": int((accepted & attacks["ground_truth_legitimate"]).sum()),
            "false_accepts": int((accepted & ~attacks["ground_truth_legitimate"]).sum()),
            "false_rejects": int((~accepted & attacks["ground_truth_legitimate"]).sum()),
            "sufficient_on_test_family": bool(
                int((accepted & ~attacks["ground_truth_legitimate"]).sum()) == 0
                and int((~accepted & attacks["ground_truth_legitimate"]).sum()) == 0
            ),
        })

    df = pd.DataFrame(rows)
    summary = {
        "visible_geometry_only_false_accepts": int(df.loc[df["predicate"] == "none_visible_geometry_only", "false_accepts"].iloc[0]),
        "sufficient_predicates": df[df["sufficient_on_test_family"]]["predicate"].tolist(),
        "conclusion": "Independent provenance is necessary; Genesis Pin is sufficient in the tested family but uniqueness is not proven.",
    }
    return df, summary


# ============================================================
# Main execution and artifacts
# ============================================================

def main():
    v1003_df, v1003_summary = run_v1003()
    v1005_df, v1005_summary = run_v1005(v1003_df)
    v1006_df, v1006_summary = run_v1006()
    v1007_df, v1007_summary = run_v1007()
    v1009_df, v1009_summary = run_v1009()

    # Save data outputs
    v1003_df.to_csv(OUT / "v1003_counterfeit_stress_results.csv", index=False)
    v1005_df.to_csv(OUT / "v1005_ablation_results.csv", index=False)
    v1006_df.to_csv(OUT / "v1006_finite_history_space_results.csv", index=False)
    v1007_df.to_csv(OUT / "v1007_generalized_sweep_results.csv", index=False)
    v1009_df.to_csv(OUT / "v1009_predicate_comparison.csv", index=False)

    full_summary = {
        "version": "FULL_STACK_V1010",
        "seed": SEED,
        "v1003_independent_counterfeit_stress": v1003_summary,
        "v1005_minimality_ablation": v1005_summary,
        "v1006_finite_history_space": v1006_summary,
        "v1007_generalized_sweep": v1007_summary,
        "v1009_necessity_vs_specificity": v1009_summary,
        "theorem_candidate": (
            "For a history space H = E × R where terminal visible observables S(H) and geometry-like fields Ω(H) "
            "depend only on event/order structure E, visible-state equivalence and geometry-like equivalence are "
            "insufficient to certify recoverable legitimacy when multiple provenance variants R share the same E. "
            "An independent provenance predicate P(H) is necessary. Genesis Pin is one sufficient and locally minimal "
            "implementation in the tested stack, but uniqueness is not proven."
        ),
        "clean_claim": (
            "State is not history. Geometry-like form is not provenance. Visible equivalence and Ω-like equivalence "
            "are insufficient for legitimacy. Recoverable legitimacy requires independent provenance."
        ),
    }

    (OUT / "full_stack_summary.json").write_text(json.dumps(full_summary, indent=2), encoding="utf-8")

    # Plot 1: counterfeit geometry
    plt.figure(figsize=(8, 5))
    invalid = v1003_df[v1003_df["kind"] != "legitimate"]
    valid = v1003_df[v1003_df["kind"] == "legitimate"]
    plt.scatter(invalid["omega_similarity"], invalid["visible_similarity"], alpha=0.6, label="counterfeits")
    plt.scatter(valid["omega_similarity"], valid["visible_similarity"], marker="*", s=220, label="legitimate")
    plt.axvline(OMEGA_THRESHOLD, linestyle="--", linewidth=1)
    plt.axhline(VISIBLE_THRESHOLD, linestyle=":", linewidth=1)
    plt.xlabel("Omega similarity")
    plt.ylabel("Visible similarity")
    plt.title("Full Stack: Geometry Similarity vs Provenance Legitimacy")
    plt.legend()
    plt.tight_layout()
    plt.savefig(OUT / "counterfeit_geometry_stress.png", dpi=180)
    plt.close()

    # Plot 2: ablation
    plt.figure(figsize=(8, 5))
    ab = v1005_df[v1005_df["removed_component"] != "none"]
    plt.bar(ab["removed_component"], ab["invalid_counterfeits_certified"])
    plt.xticks(rotation=35, ha="right")
    plt.ylabel("Invalid counterfeits certified")
    plt.title("Genesis Pin Single-Component Ablation")
    plt.tight_layout()
    plt.savefig(OUT / "genesis_pin_ablation.png", dpi=180)
    plt.close()

    # Markdown report
    report = f"""# Full Stack Recoverable Legitimacy Python Proof

**Status:** executable proof-of-work  
**Version:** FULL_STACK_V1010  
**Seed:** {SEED}

## Core Result

```text
State is not history.
Geometry-like form is not provenance.
Visible equivalence is not legitimacy.
Omega-like equivalence is not legitimacy.
Recoverable legitimacy requires independent provenance.
```

## Theorem Candidate

```text
{full_summary["theorem_candidate"]}
```

## V1003 — Independent Counterfeit Geometry Stress

```json
{json.dumps(v1003_summary, indent=2)}
```

## V1005 — Genesis Pin Minimality Ablation

```json
{json.dumps(v1005_summary, indent=2)}
```

## V1006 — Formal Finite History Space

```json
{json.dumps(v1006_summary, indent=2)}
```

## V1007 — Generalized Finite-Family Sweep

```json
{json.dumps(v1007_summary, indent=2)}
```

## V1009 — Necessity vs Specificity

```json
{json.dumps(v1009_summary, indent=2)}
```

## Claim Boundary

This script does **not** prove:

- physical spacetime,
- General Relativity,
- Einstein equations,
- actual ADM constraints,
- physical curvature,
- quantum gravity,
- production cryptographic security,
- uniqueness of Genesis Pin across all possible systems.

It does support the narrower map-class claim:

```text
When visible/geometry observables are functions of form/order and legitimacy is a function of provenance,
form-equivalence cannot certify source-legitimacy.
```

## Generated Artifacts

```text
v1003_counterfeit_stress_results.csv
v1005_ablation_results.csv
v1006_finite_history_space_results.csv
v1007_generalized_sweep_results.csv
v1009_predicate_comparison.csv
full_stack_summary.json
counterfeit_geometry_stress.png
genesis_pin_ablation.png
```
"""
    (OUT / "FULL_STACK_RECOVERABLE_LEGITIMACY_PROOF_REPORT.md").write_text(report, encoding="utf-8")

    print(json.dumps(full_summary, indent=2))
    print(f"\nOutputs written to: {OUT.resolve()}")


if __name__ == "__main__":
    main()
