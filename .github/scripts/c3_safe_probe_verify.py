#!/usr/bin/env python3
"""Bounded executable controls for C3 safe-probe theorem (NOT a universal proof)."""
import itertools
import json

CORE = frozenset("abcde")
TRIANGLE = (frozenset("ab"), frozenset("bc"), frozenset("ac"))
SPECTATORS = ("u", "v", "w")

def state(z):
    return TRIANGLE + (frozenset(("d", "e")) | frozenset(z),)

def hitting_number(roots):
    palette = set().union(*roots)
    for n in range(1, len(palette) + 1):
        if any(all(set(h) & root for root in roots)
               for h in itertools.combinations(sorted(palette), n)):
            return n
    raise AssertionError("no hitting set")

def observation(z):
    roots = state(z)
    core_roots = tuple(root & CORE for root in roots)
    # Every nonempty core H of size at most four; use fixed residual family {r4}.
    miss = []
    for n in range(1, 5):
        for h in itertools.combinations(sorted(CORE), n):
            miss.append(int(not (roots[3] & set(h))))
    return (core_roots, tuple(miss), hitting_number(roots),
            tuple(len(root) >= 2 for root in roots))

def valid(z, sign, label):
    return label not in z if sign == "+" else label in z

def apply(z, sign, label):
    assert valid(z, sign, label)
    return frozenset(set(z) | {label}) if sign == "+" else frozenset(set(z) - {label})

def main():
    initial_a, initial_b = frozenset(), frozenset(("u",))
    baseline = observation(initial_a)
    tested_states = 0
    for n in range(len(SPECTATORS) + 1):
        for group in itertools.combinations(SPECTATORS, n):
            z = frozenset(group)
            assert observation(z) == baseline
            assert hitting_number(state(z)) == 3
            assert all(len(root) >= 2 for root in state(z))
            tested_states += 1

    # Enumerate all common uniformly valid labelled toggles to depth four.
    frontier = [(initial_a, initial_b, ())]
    prefixes = 0
    for depth in range(5):
        next_frontier = []
        for a, b, transcript in frontier:
            prefixes += 1
            assert observation(a) == observation(b)
            assert len(b) - len(a) == 1
            assert len(transcript) == depth
            if depth == 4:
                continue
            for label in SPECTATORS:
                for sign in ("+", "-"):
                    if valid(a, sign, label) and valid(b, sign, label):
                        aa, bb = apply(a, sign, label), apply(b, sign, label)
                        assert observation(aa) == observation(bb)
                        next_frontier.append((aa, bb, transcript + ((sign, label),)))
        frontier = next_frontier

    # Rejecting controls: an unsafe legality query WOULD distinguish the worlds.
    assert not valid(initial_a, "-", "u")
    assert valid(initial_b, "-", "u")
    assert len(state(initial_a)[3]) != len(state(initial_b)[3])
    assert int("u" not in state(initial_a)[3]) != int("u" not in state(initial_b)[3])
    # The current positivity bit can converge without revealing initial occupancy.
    assert apply(initial_a, "+", "v") and apply(initial_b, "+", "v")
    assert bool(apply(initial_a, "+", "v")) == bool(apply(initial_b, "+", "v"))
    print(json.dumps({"status": "PASS", "spectator_states": tested_states,
                      "safe_prefixes_checked": prefixes,
                      "max_depth": 4, "rejecting_controls": 4,
                      "scope": "finite bounded exhaustive controls only"}, sort_keys=True))

if __name__ == "__main__":
    main()
