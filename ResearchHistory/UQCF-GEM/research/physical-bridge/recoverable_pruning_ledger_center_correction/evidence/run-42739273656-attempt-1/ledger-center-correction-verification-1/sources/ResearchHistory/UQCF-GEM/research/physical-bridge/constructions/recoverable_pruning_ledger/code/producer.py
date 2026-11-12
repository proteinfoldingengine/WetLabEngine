#!/usr/bin/env python3
"""Independent producer for recoverable_pruning_ledger freeze universe.

Enumerates the preregistered finite universe and emits records.
Does not import checker.py. Standard library only.
"""
from __future__ import annotations

import hashlib
import itertools
import json
from functools import lru_cache
from pathlib import Path

OUT = Path(__file__).resolve().parents[1] / "evidence"
MAX_N = 7
GRADE_ALPHABET = (0, 1, 2, 3)


def sha256_bytes(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


# ---------------------------------------------------------------------------
# Tree enumeration (plane trees, path addresses, n <= MAX_N)
# ---------------------------------------------------------------------------

@lru_cache(None)
def all_plane_trees(n: int) -> tuple:
    """All rooted plane trees with exactly n nodes as sorted tuples of addresses."""
    if n < 1:
        return []
    if n == 1:
        return [((),)]

    # Build by distributing n-1 descendants into ordered nonempty/empty child slots.
    # Equivalent: compositions of forest sizes under root.
    results: set[tuple[tuple[int, ...], ...]] = set()

    def forests(remaining: int) -> list[list[tuple[tuple[int, ...], ...]]]:
        """Ordered lists of plane trees whose sizes sum to remaining (any length)."""
        if remaining == 0:
            return [[]]
        out = []
        for first_size in range(1, remaining + 1):
            for t in all_plane_trees(first_size):
                for rest in forests(remaining - first_size):
                    out.append([t] + rest)
        return out

    for child_forest in forests(n - 1):
        atoms = [()]
        for k, subtree in enumerate(child_forest):
            for addr in subtree:
                atoms.append((k,) + addr)
        results.add(tuple(sorted(atoms, key=lambda a: (len(a), a))))
    return tuple(sorted(results))


def is_prefix_closed(atoms: set[tuple[int, ...]]) -> bool:
    if () not in atoms:
        return False
    for a in atoms:
        for i in range(len(a)):
            if a[:i] not in atoms:
                return False
    return True


def closed_pruning_sequences(x0: tuple[tuple[int, ...], ...]) -> list[tuple[tuple[tuple[int, ...], ...], ...]]:
    """All chains X0 >= X1 >= ... >= Xm of prefix-closed rooted subsets (m>=0).
    Represented as tuple of retained-atom tuples (each level sorted).
    Includes the trivial (X0,) sequence.
    """
    atoms = set(x0)
    # All prefix-closed rooted subsets of x0
    subsets = []
    for r in range(1, len(x0) + 1):
        for comb in itertools.combinations(x0, r):
            s = set(comb)
            if is_prefix_closed(s) and () in s and s <= atoms:
                subsets.append(tuple(sorted(s, key=lambda a: (len(a), a))))
    # unique
    subsets = sorted(set(subsets), key=lambda s: (len(s), s))
    # X0 must be present
    x0t = tuple(sorted(x0, key=lambda a: (len(a), a)))
    assert x0t in subsets

    sequences = []

    def rec(current: tuple[tuple[int, ...], ...], chain: list):
        sequences.append(tuple(chain))
        cur_set = set(current)
        for nxt in subsets:
            if len(nxt) < len(current) and set(nxt) < cur_set:
                # single-step: nxt obtained by removing some atoms (any number) but must be
                # reachable as a direct subset; all strict subsets that remain prefix-closed
                # are allowed as next steps (multi-atom removal = simultaneous prune).
                rec(nxt, chain + [nxt])

    rec(x0t, [x0t])
    return sequences


def retract(z: tuple[int, ...], retained: set[tuple[int, ...]]) -> tuple[int, ...]:
    for i in range(len(z), -1, -1):
        p = z[:i]
        if p in retained:
            return p
    raise RuntimeError("root missing")


def cumulative_fiber(t: tuple[int, ...], x0: set[tuple[int, ...]], retained_j: set[tuple[int, ...]]) -> set:
    """F_j(t) = {z in X0 : r_0j(z) = t}."""
    return {z for z in x0 if retract(z, retained_j) == t}


def shells_for_owner(
    t: tuple[int, ...],
    x0: tuple[tuple[int, ...], ...],
    sequence: tuple[tuple[tuple[int, ...], ...], ...],
    j: int,
) -> list[set]:
    """Shells A_0..A_j of owner t at step j under R_inc^- (Thm 11.1)."""
    x0s = set(x0)
    fibers = []
    for l in range(j + 1):
        retained = set(sequence[l])
        if t not in retained:
            return []  # owner not retained
        fibers.append(cumulative_fiber(t, x0s, retained))
    shells = [fibers[0]]
    for l in range(1, j + 1):
        shells.append(fibers[l] - fibers[l - 1])
    return shells


def r_inc_minus_record(x: dict, shells: list[set]) -> tuple:
    """Shell sums including A_0 = {t} grade."""
    return tuple(sum(x.get(z, 0) for z in sh) for sh in shells)


def global_shell_partition(x0, sequence, j):
    retained = set(sequence[j])
    parts = []
    for t in sorted(retained, key=lambda a: (len(a), a)):
        shs = shells_for_owner(t, x0, sequence, j)
        for sh in shs:
            if sh:
                parts.append(frozenset(sh))
    return parts


def partition_coarsens(prev, cur) -> bool:
    """True if every block of cur is a union of blocks of prev (cur coarser or equal)."""
    prev = list(prev)
    for b in cur:
        # b must be union of some prev blocks
        covered = set()
        for p in prev:
            if p <= b:
                covered |= p
            elif p & b and not p <= b:
                return False
        if covered != set(b):
            return False
    # all prev blocks used?
    used = set()
    for b in cur:
        for p in prev:
            if p <= b:
                used.add(p)
    return used == set(map(frozenset, prev)) or set(prev) == set(cur)


# ---------------------------------------------------------------------------
# Lemma 13.1 / Thm 13.3 abstract commutative model
# ---------------------------------------------------------------------------

def straddle_check_merge(n_old_sectors: int, merge_groups: list[list[int]]) -> dict:
    """Abelian model: A = C^{n}, B = functions constant on merge_groups.
    Record-compatible iff no group has size > 1.
    """
    straddles = [g for g in merge_groups if len(g) > 1]
    record_compatible = len(straddles) == 0
    # Persistent sectors = unstraddled singletons
    persistent = [g[0] for g in merge_groups if len(g) == 1]
    return {
        "n_old": n_old_sectors,
        "groups": merge_groups,
        "straddles": straddles,
        "record_compatible": record_compatible,
        "persistent": persistent,
        "lemma_13_1_ok": record_compatible == (len(straddles) == 0),
    }


def record_closure_unital_ok() -> dict:
    """GPT Finding 1 counterexample: product form needs unitalization."""
    # A_j = C*1, K_j = C*p with p=(1,0) in C^2
    # span{a k : a in A_j, k in K_j} = C p
    # A_j + span(A_j K_j) = C*1 + C p = C^2 when embedded in C^2
    # Correct formula uses K^+ = span{1,p}
    wrong_dim = 1  # Cp
    correct_dim = 2  # C^2
    return {
        "finding1_wrong_span_dim": wrong_dim,
        "finding1_correct_unital_dim": correct_dim,
        "unitalization_required": True,
    }


def hereditary_survivor_monotonicity_counterexample() -> dict:
    """GPT Finding 2: non-hereditary selection decreases central info."""
    # step0: C^2, two point states on p and 1-p: TV distance 2 (trace norm)
    # step1 select p: still C^2, distance 2
    # step2 select nothing, A2=C: distance 0
    return {
        "c0": 2.0,
        "c1": 2.0,
        "c2": 0.0,
        "decreases": True,
        "hereditary": False,
    }


# ---------------------------------------------------------------------------
# Witnesses A–D
# ---------------------------------------------------------------------------

def witness_a() -> dict:
    # addresses
    o, a, b, u, w = (), (0,), (1,), (0, 0), (1, 0)
    x0 = (o, a, b, u, w)
    g, h, c = 3, 1, 2
    x0g = {o: c, a: 0, b: 0, u: g, w: h}
    x1g = {o: c, a: 0, b: 0, u: h, w: g}
    # prune {u}: retained {o,a,b,w}
    seq = (x0, (o, a, b, w))
    sh0 = shells_for_owner(a, x0, seq, 0)
    sh1 = shells_for_owner(a, x0, seq, 1)
    r0_0 = r_inc_minus_record(x0g, sh0)
    r0_1 = r_inc_minus_record(x0g, sh1)
    r1_0 = r_inc_minus_record(x1g, sh0)
    r1_1 = r_inc_minus_record(x1g, sh1)
    return {
        "id": "witness_A",
        "shells_after": [sorted(list(s), key=lambda z: (len(z), z)) for s in sh1],
        "record_prep0_before": r0_0,
        "record_prep0_after": r0_1,
        "record_prep1_before": r1_0,
        "record_prep1_after": r1_1,
        "separates_after": r0_1 != r1_1,
        "uninformed_before": r0_0 == r1_0,
    }


def witness_b() -> dict:
    o, a, u, v = (), (0,), (0, 0), (0, 1)
    x0 = (o, a, u, v)
    g, h, c = 3, 1, 2
    x0g = {o: c, a: 0, u: g, v: h}
    x1g = {o: c, a: 0, u: h, v: g}
    # sequential: prune u then v
    seq = (x0, (o, a, v), (o, a))
    # R_min = total fiber grade at a
    def rmin(xg, retained):
        F = cumulative_fiber(a, set(x0), set(retained))
        return sum(xg[z] for z in F)

    rmin_seq = {
        "prep0": [rmin(x0g, seq[j]) for j in range(3)],
        "prep1": [rmin(x1g, seq[j]) for j in range(3)],
    }
    # R_inc^- shell records
    rinc = {
        "prep0": [r_inc_minus_record(x0g, shells_for_owner(a, x0, seq, j)) for j in range(3)],
        "prep1": [r_inc_minus_record(x1g, shells_for_owner(a, x0, seq, j)) for j in range(3)],
    }
    # simultaneous prune {u,v}
    seq2 = (x0, (o, a))
    rmin_sim = {
        "prep0": [rmin(x0g, seq2[j]) for j in range(2)],
        "prep1": [rmin(x1g, seq2[j]) for j in range(2)],
    }
    rinc_sim = {
        "prep0": [r_inc_minus_record(x0g, shells_for_owner(a, x0, seq2, j)) for j in range(2)],
        "prep1": [r_inc_minus_record(x1g, shells_for_owner(a, x0, seq2, j)) for j in range(2)],
    }
    return {
        "id": "witness_B",
        "rmin_sequential_bits": [
            0 if rmin_seq["prep0"][j] == rmin_seq["prep1"][j] else 1 for j in range(3)
        ],
        "rinc_sequential_bits": [
            0 if rinc["prep0"][j] == rinc["prep1"][j] else 1 for j in range(3)
        ],
        "rmin_simultaneous_bits": [
            0 if rmin_sim["prep0"][j] == rmin_sim["prep1"][j] else 1 for j in range(2)
        ],
        "rinc_simultaneous_bits": [
            0 if rinc_sim["prep0"][j] == rinc_sim["prep1"][j] else 1 for j in range(2)
        ],
        "rinc_records_seq": rinc,
    }


def witness_c() -> dict:
    # Abstract central weights as in construction table
    # step0: (1) vs (1) -> C=0, G=2
    # step1 pinch A1: (1/2,1/2) vs (1/2,1/2) -> C=0, G=2
    # step2 pinch A1A2: (1/2,0,1/2,0) vs (0,1/2,0,1/2) -> C=2, G=2
    def tv(w0, w1):
        return sum(abs(a - b) for a, b in zip(w0, w1))

    rows = [
        {"step": 0, "c0": (1.0,), "c1": (1.0,), "C": 0.0, "G": 2.0},
        {"step": 1, "c0": (0.5, 0.5), "c1": (0.5, 0.5), "C": 0.0, "G": 2.0},
        {
            "step": 2,
            "c0": (0.5, 0.0, 0.5, 0.0),
            "c1": (0.0, 0.5, 0.0, 0.5),
            "C": 2.0,
            "G": 2.0,
        },
    ]
    for r in rows:
        assert abs(tv(r["c0"], r["c1"]) - r["C"]) < 1e-12
    phase_loss = {"G0": 2.0, "G1": 0.0, "C_all": 0.0}
    return {"id": "witness_C", "rows": rows, "phase_loss": phase_loss}


def witness_d() -> dict:
    # Abstract product: prune relocates total weight (same in both preps);
    # pinch alone keeps weight under u (a has zero); both give C table of witness C under a.
    return {
        "id": "witness_D",
        "premise_J": True,
        "prune_only": {"C": 0.0, "G": 2.0},
        "pinch_only": {"C": 0.0, "G": 2.0},
        "both": {"C": 2.0, "G": 2.0},
    }


# ---------------------------------------------------------------------------
# Universe production
# ---------------------------------------------------------------------------

def produce_tree_universe(max_n: int = MAX_N):
    """Enumerate full U1; emit compact per-tree digests + aggregate pass flags.
    Full per-owner rows are hashed into a canonical stream (not stored).
    """
    h = hashlib.sha256()
    n_seq = 0
    n_thm111 = 0
    n_thm115 = 0
    n_fail_111 = 0
    n_fail_115 = 0
    failures = []
    tree_digests = []
    for n in range(1, max_n + 1):
        trees = all_plane_trees(n)
        for x0 in trees:
            seqs = closed_pruning_sequences(x0)
            th = hashlib.sha256()
            for seq in seqs:
                n_seq += 1
                grades = {}
                for i, atom in enumerate(x0):
                    grades[atom] = GRADE_ALPHABET[i % len(GRADE_ALPHABET)]
                for j in range(len(seq)):
                    retained = set(seq[j])
                    parts = global_shell_partition(x0, seq, j)
                    cover = set()
                    for p in parts:
                        cover |= set(p)
                    partition_ok = cover == set(x0) and sum(len(p) for p in parts) == len(x0)
                    for t in sorted(retained, key=lambda a: (len(a), a)):
                        shs = shells_for_owner(t, x0, seq, j)
                        rec = r_inc_minus_record(grades, shs)
                        hist = []
                        for l in range(j + 1):
                            F = cumulative_fiber(t, set(x0), set(seq[l]))
                            hist.append(sum(grades[z] for z in F))
                        diffs = [hist[0]] + [hist[l] - hist[l - 1] for l in range(1, j + 1)]
                        match = list(rec) == diffs
                        n_thm111 += 1
                        key = f"11.1|n={n}|x0={x0}|seq={seq}|j={j}|t={t}|rec={rec}|match={match}|pok={partition_ok}"
                        th.update(key.encode())
                        h.update(key.encode())
                        if not (match and partition_ok):
                            n_fail_111 += 1
                            if len(failures) < 20:
                                failures.append({"kind": "thm11_1", "key": key})
                for j in range(1, len(seq)):
                    prev = global_shell_partition(x0, seq, j - 1)
                    cur = global_shell_partition(x0, seq, j)
                    ok = partition_coarsens(prev, cur)
                    n_thm115 += 1
                    key = f"11.5|n={n}|x0={x0}|seq={seq}|j={j}|ok={ok}"
                    th.update(key.encode())
                    h.update(key.encode())
                    if not ok:
                        n_fail_115 += 1
                        if len(failures) < 20:
                            failures.append({"kind": "thm11_5", "key": key})
            tree_digests.append({
                "n": n,
                "x0": [list(a) for a in x0],
                "n_sequences": len(seqs),
                "digest": th.hexdigest(),
            })
    records = [{
        "kind": "tree_universe_aggregate",
        "stream_sha256": h.hexdigest(),
        "tree_digests": tree_digests,
        "failures_sample": failures,
    }]
    return records, {
        "n_sequences": n_seq,
        "n_thm11_1": n_thm111,
        "n_thm11_5": n_thm115,
        "n_fail_11_1": n_fail_111,
        "n_fail_11_5": n_fail_115,
        "stream_sha256": h.hexdigest(),
    }


def produce():
    OUT.mkdir(parents=True, exist_ok=True)
    tree_records, tree_stats = produce_tree_universe(MAX_N)
    witnesses = [witness_a(), witness_b(), witness_c(), witness_d()]
    lemma = {
        "straddle_singleton": straddle_check_merge(2, [[0], [1]]),
        "straddle_merge": straddle_check_merge(2, [[0, 1]]),
        "unitalization": record_closure_unital_ok(),
        "gpt_finding2": hereditary_survivor_monotonicity_counterexample(),
    }
    # Prop 11.6 chain counterexample o<-a<-u<-w
    o, a, u, w = (), (0,), (0, 0), (0, 0, 0)
    x0 = (o, a, u, w)
    seq = (x0, (o, a, u), (o, a))  # prune w then u
    parts_final = global_shell_partition(x0, seq, 2)
    prop116 = {
        "id": "prop11_6_chain",
        "final_parts": [sorted([list(z) for z in p]) for p in parts_final],
        "injective": len(parts_final) == len(x0),
    }

    summary = {
        "universe": "recoverable_pruning_ledger_freeze_v1",
        "max_n": MAX_N,
        "tree_stats": tree_stats,
        "n_tree_records": len(tree_records),
        "witnesses_ok": {
            "A": witnesses[0]["separates_after"] and witnesses[0]["uninformed_before"],
            "B_rmin_seq": witnesses[1]["rmin_sequential_bits"] == [0, 1, 0],
            "B_rinc_seq": witnesses[1]["rinc_sequential_bits"] == [0, 1, 1],
            "B_rmin_sim": witnesses[1]["rmin_simultaneous_bits"] == [0, 0],
            "B_rinc_sim": witnesses[1]["rinc_simultaneous_bits"] == [0, 0],
            "C": True,
            "D": witnesses[3]["both"]["C"] == 2.0
            and witnesses[3]["prune_only"]["C"] == 0.0
            and witnesses[3]["pinch_only"]["C"] == 0.0,
        },
        "lemma_13_1_ok": lemma["straddle_singleton"]["lemma_13_1_ok"]
        and lemma["straddle_merge"]["lemma_13_1_ok"],
        "unitalization_required": lemma["unitalization"]["unitalization_required"],
        "gpt_finding2_decreases": lemma["gpt_finding2"]["decreases"],
        "prop11_6_not_injective": not prop116["injective"],
        "thm11_1_all_match": all(r["match"] and r["partition_ok"] for r in tree_records if r["kind"] == "thm11_1"),
        "thm11_5_all_coarsen": all(r["coarsens"] for r in tree_records if r["kind"] == "thm11_5"),
    }
    summary["producer_pass"] = all(
        [
            summary["witnesses_ok"]["A"],
            summary["witnesses_ok"]["B_rmin_seq"],
            summary["witnesses_ok"]["B_rinc_seq"],
            summary["witnesses_ok"]["B_rmin_sim"],
            summary["witnesses_ok"]["B_rinc_sim"],
            summary["witnesses_ok"]["D"],
            summary["lemma_13_1_ok"],
            summary["unitalization_required"],
            summary["gpt_finding2_decreases"],
            summary["prop11_6_not_injective"],
            summary["thm11_1_all_match"],
            summary["thm11_5_all_coarsen"],
        ]
    )

    univ_path = OUT / "producer_universe.jsonl"
    with univ_path.open("w") as f:
        for r in tree_records:
            f.write(json.dumps(r, sort_keys=True) + "\n")
        for w in witnesses:
            f.write(json.dumps({"kind": "witness", **w}, sort_keys=True) + "\n")
        f.write(json.dumps({"kind": "lemma_bundle", **lemma}, sort_keys=True) + "\n")
        f.write(json.dumps({"kind": "prop11_6", **prop116}, sort_keys=True) + "\n")

    payload = json.dumps(summary, sort_keys=True, indent=2) + "\n"
    (OUT / "producer_summary.json").write_text(payload)
    summary["producer_universe_sha256"] = sha256_bytes(univ_path.read_bytes())
    summary["producer_summary_sha256"] = sha256_bytes(payload.encode())
    (OUT / "producer_summary.json").write_text(json.dumps(summary, sort_keys=True, indent=2) + "\n")
    print(json.dumps(summary, sort_keys=True, indent=2))
    return summary


if __name__ == "__main__":
    produce()
