"""Compose native duplicate-tip cuts with the archived P1 update of the receiver's own grade."""
from itertools import product
import json
import lzma
from pathlib import Path
import sys

from check_fixed_pair import HIST, PINS, integer_tuple, modules, require, wire
from check_fixed_pair_match import FIELDS


def event(ops, parents, family, chart, vertex):
    cert = ops["cut"].atomic(parents, family, chart, vertex)
    ops["gate"].verify_atomic(cert)
    return tuple(map(tuple, cert["after"])), [cert[k] for k in FIELDS]


def options(ops, parents, family, chart, candidates):
    trials, successful = {}, {}
    for v in candidates:
        try:
            cert = ops["cut"].atomic(parents, family, chart, v)
        except ValueError as err:
            trials[str(v)] = str(err)
            continue
        ops["gate"].verify_atomic(cert)
        trials[str(v)] = "legal"
        successful[v] = (tuple(map(tuple, cert["after"])), [cert[k] for k in FIELDS])
    return trials, successful


def local(ops, parents, start, end, grade):
    values = ops["overlap"].push(parents, start, end, grade)
    return [[v, n] for v, n in zip(end, integer_tuple(values))]


def histories(ops, p, leaves, grade, source):
    receiver = 1 - source
    full = tuple(range(len(p)))
    prior = (full, full)
    out = {}
    for i, a in enumerate(leaves):
        b = leaves[1 - i]
        post, first = event(ops, p, prior, source, a)
        tested, choices = options(ops, p, post, receiver, full)
        reverse, reverse_choices = options(ops, p, post, receiver, reversed(full))
        require(choices == reverse_choices and tested == reverse and set(choices) == {b}, "ambiguous R turn")
        end, second = choices[b]
        prior_r = local(ops, p, full, post[receiver], grade)
        after_r = local(ops, p, post[receiver], end[receiver], tuple(n for _, n in prior_r))
        source_after = local(ops, p, prior[source], post[source], grade)
        require(sum(g for _, g in after_r) == sum(grade) and end[source] == post[source], "receiver update")
        # A different legal actor order in the same unmodified full-family validator.
        pass_to_source, _ = event(ops, p, post, source, b)
        stationary = local(ops, p, prior[receiver], pass_to_source[receiver], grade)
        # An additional initially complete chart keeps another copy of either candidate.
        augmented, _ = event(ops, p, prior + (full,), source, a)
        _, spare_options = options(ops, p, augmented, receiver, full)
        out[str(a)] = dict(receiver=receiver, source_fields=first, source_payload=source_after,
                           receiver_before=prior_r, candidate_status=tested, executed=b, receiver_fields=second,
                           receiver_after=after_r, other_order=stationary, third_chart_choices=sorted(spare_options))
    return out


def main(history, out):
    ops = modules(history)
    trees = {}
    for n in range(2, 7):
        for t in product(*(range(v) for v in range(1, n))):
            p = (-1,) + t
            leaves = tuple(v for v in range(1, n) if v not in t)
            if len(leaves) != 2:
                continue
            g = tuple(3 if v == 0 else 2 if v in leaves else 4 for v in range(n))
            trees["/".join(map(str, p))] = {str(s): histories(ops, p, leaves, g, s) for s in (0, 1)}
    p, g, leaves = (-1, 0, 0, 2, 1, 3), (3, 4, 1, 4, 2, 2), (4, 5)
    witness = histories(ops, p, leaves, g, 1)
    all_arms = [arm for tree in trees.values() for pair in tree.values() for arm in pair.values()]
    different = siblings = numeric = matched = 0
    for key, record in trees.items():
        parents = list(map(int, key.split("/")))
        for pair in record.values():
            (a, x), (b, y) = sorted((int(v), row) for v, row in pair.items())
            distinct = parents[a] != parents[b]
            different += distinct
            siblings += not distinct
            measured = parents[a]
            numeric += dict(x["receiver_after"])[measured] != dict(y["receiver_after"])[measured]
            matched += all(x[k] == y[k] for k in ("source_fields", "receiver_fields"))
    counts = dict(parent_arrays=len(trees), source_role_pairs=different + siblings, histories=len(all_arms),
                  distinct_parent_pairs=different, sibling_pairs=siblings, distinguished_receiver_parent=numeric,
                  matched_source_and_receiver_cover=matched, candidate_trials=sum(len(r["candidate_status"]) for r in all_arms),
                  positive_receiver_moves=sum(sum(x == "legal" for x in r["candidate_status"].values()) for r in all_arms))
    content = dict(trees=trees, witness=witness, counts=counts)
    raw = wire(content)
    out.mkdir(exist_ok=True, parents=True)
    (out / "receiver_turn_universe.json.xz").write_bytes(lzma.compress(raw, preset=6))
    from hashlib import sha256
    cert = dict(counts=counts, witness=witness, historical_sha=HIST, raw_sha256=sha256(raw).hexdigest(),
                historical_blobs={key: sha for key, (_, sha) in PINS.items()})
    (out / "receiver_turn_certificate.json").write_text(json.dumps(cert, indent=2, sort_keys=True) + "\n")
    print(json.dumps(counts, sort_keys=True))


if __name__ == "__main__":
    main(Path(sys.argv[1]), Path(sys.argv[2]))
