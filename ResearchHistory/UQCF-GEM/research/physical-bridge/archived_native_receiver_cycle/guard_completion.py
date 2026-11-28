"""A proposed incidence-based target for historical M9, and its finite controls."""
import argparse
from collections import Counter
from dataclasses import dataclass
import gzip
from hashlib import sha256
from itertools import combinations, permutations, product
import json
import os
from pathlib import Path
import sys

from remote_incidence import BASE, add_source, changed, cover, encoded, registers, suffix_size
from replay import HERE, PINS, local_history


@dataclass(frozen=True)
class Roles:
    small: frozenset
    missing: frozenset
    exact_row: int
    containing_row: int
    crossing_row: int

    def destinations(self):
        return {self.exact_row: self.small, self.containing_row: self.missing,
                self.crossing_row: self.small | self.missing}


def infer(rows, retained=None):
    """Read unordered pairs held by leaves at initialization under the M9 convention."""
    roots = [frozenset(r) for r in rows]
    if len(roots) != 6 or min(map(len, roots)) != 2:
        return None
    labels = frozenset.union(*roots)
    if labels != frozenset(range(8)):
        return None
    if retained is None:
        retained = [sorted(r)[:2] for r in roots]
    pairs = set(map(frozenset, retained))
    candidates = []
    for p, q in combinations(pairs, 2):
        if p & q or p | q not in roots:
            continue
        for s in pairs.intersection(roots):
            if s & (p | q):
                continue
            t = labels - (p | q | s)
            if t in roots:
                continue
            exact = [i for i, row in enumerate(roots) if row == s]
            containing = [i for i, row in enumerate(roots) if t <= row]
            crossing = [i for i, row in enumerate(roots) if all(row & part for part in (p, q, s, t))]
            if len(exact) == len(containing) == len(crossing) == 1:
                a, b, c = exact[0], containing[0], crossing[0]
                if len({a, b, c}) == 3:
                    candidates.append(Roles(s, t, a, b, c))
    return candidates[0] if len(candidates) == 1 else None


def build(rows, roles, source_order=None, target_order=None, dest_order=None):
    destinations = roles.destinations()
    dest = sorted(destinations, key=lambda i: sorted(destinations[i])) if dest_order is None else dest_order
    source = [i for i in range(len(rows)) if i not in dest] if source_order is None else source_order
    order = tuple(source) + tuple(dest)
    guards = sorted(sorted(r) for r in destinations.values()) if target_order is None else target_order
    goal = list(guards) + [sorted(rows[i]) for i in dest]
    return [sorted(rows[i]) for i in order], goal, order


def propose(rows):
    """Form the proposed M9 input from one preparation within the tested rank-three class.

    A returned proposal still requires historical certificate verification.
    None means that this trigger did not supply an operation.
    """
    if len(rows) != 6 or any(len(row) < 2 for row in rows):
        return None
    pattern = infer(rows)
    if pattern is None or len(cover(rows)) != 3:
        return None
    return build(rows, pattern)


def pairings(labels):
    if not labels:
        yield ()
        return
    for j in range(1, len(labels)):
        for tail in pairings(labels[1:j] + labels[j+1:]):
            yield ((labels[0], labels[j]),) + tail


def nearest_boundary(rows):
    """Test all Hamming moves at each distance, including additions to other rows."""
    initial = [sum(1 << x for x in row) for row in rows]
    covers = [sum(1 << x for x in labels) for labels in combinations(range(8), 3)]
    for n in range(1, 4):
        winners = []
        for moves in combinations(range(48), n):
            candidate = initial.copy()
            for d in moves:
                i, x = divmod(d, 8)
                candidate[i] ^= 1 << x
            if min(r.bit_count() for r in candidate) < 2:
                continue
            if not any(all(r & c for r in candidate) for c in covers):
                winners.append(tuple(divmod(d, 8) for d in moves))
        if winners:
            return winners
    return []


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("demo", type=Path)
    parser.add_argument("--write-examples", type=Path)
    parser.add_argument("--full-stream", type=Path, help="optionally save every verified record in run order")
    args = parser.parse_args()
    example_path = args.write_examples.resolve() if args.write_examples else None
    full_path = args.full_stream.resolve() if args.full_stream else None
    demo = args.demo.resolve()
    for name, pin in PINS.items():
        assert sha256((demo / name).read_bytes()).hexdigest() == pin
    os.chdir(demo)
    sys.path.insert(0, str(demo))
    import mechanisms
    import universe
    import verifier

    raw_hash = sha256()
    stream = gzip.open(full_path, "wb") if full_path else None
    count = 0

    def run(initial, goal, shift=0, diagnostic=False):
        nonlocal count
        q = len(cover(initial))
        c = universe.case("M9", "native", 8, [2]*6, q, initial,
                          dict(shift=shift, reversal=0, target=goal), h=2, N=3)
        r = mechanisms.produce(c)
        errors = verifier.verify_record(c, r)
        if diagnostic and errors:
            return None, sorted(set(errors))
        assert r["status"] == "PASS" and not errors, errors
        raw = encoded(r)
        raw_hash.update(raw)
        if stream:
            stream.write(raw)
        count += 1
        return (r, []) if diagnostic else r

    def step(rows):
        # This trigger and target constructor are the new, proposed operation.
        # Returning None leaves the complete current state in place.
        proposal = propose(rows)
        if proposal is None:
            return None
        initial, goal, _ = proposal
        return run(initial, goal)

    base, plus = BASE, add_source(BASE, 4)
    inputs = (base, plus)
    roles = infer(base)
    assert roles == infer(plus) == Roles(frozenset((5, 7)), frozenset((1, 4)), 5, 3, 4)
    assert nearest_boundary(base) == [((3, 3), (3, 5))]
    assert nearest_boundary(plus) == [((0, 4), (3, 3), (3, 5))]
    example = []
    for rows in inputs:
        a, goal, order = build(rows, infer(rows))
        example.append(step(rows))
    left, right = example
    b = order.index(roles.crossing_row)
    assert changed(left["nested_path"][0], right["nested_path"][0]) == [(1, 4)]
    assert changed(left["nested_path"][-1], right["nested_path"][-1]) == [(14, 0), (14, 4), (15, 0), (15, 4)]
    suffix = suffix_size(left["path"], right["path"])
    assert suffix == 25
    for arm, rec in enumerate(example):
        edits = [e for e in local_history(rec, b) if e["slots_before"] != e["slots_after"]]
        last = edits[-1]
        assert last["x"] == 1 and last["changes"][0] == ((15, 14)[arm], 0, True)
        assert last["parent_frame"] - len(rec["path"]) == -2
        assert rec["path"][-1][b] == rec["path"][0][b]
        print(f"Constructed arm {arm}: row {order[b]}, final leaves {registers(rec, -1)[b]}, "
              f"withdraw 1 at frame {last['parent_frame']} then 0 goes to leaf {last['changes'][0][0]}")
    dormant = [list(row) for row in base]
    dormant[1] = sorted(dormant[1] + [7])
    assert changed(base, dormant) == [(1, 7)]
    assert [sorted(r)[:2] for r in base] == [sorted(r)[:2] for r in dormant]
    assert step(dormant) is None
    assert all(infer(r["path"][-1], registers(r, -1)) is None for r in example)
    print("Extra 7 at row 1 disables the proposed trigger with identical initial leaves.")
    print("The proposed trigger is absent in both terminal records using their actual retained leaves.")
    saved = b"".join(map(encoded, example))
    if example_path:
        with example_path.open("wb") as f, gzip.GzipFile(filename="", fileobj=f, mode="wb", mtime=0) as z:
            z.write(saved)
    else:
        assert gzip.decompress((HERE / "completion_examples.jsonl.gz").read_bytes()) == saved

    # Relabel row positions on input; retain the historical numeric order of palette labels.
    # Check inferred role coordinates before any M9 call.
    for perm in permutations(range(6)):
        for rows in inputs:
            permuted = [rows[i] for i in perm]
            rr = infer(permuted)
            assert (perm[rr.exact_row], perm[rr.containing_row], perm[rr.crossing_row]) == (5, 3, 4)
    print("Role identification covariant in all 720 row presentations in each arm")

    # Every ordering of source rows, every assignment of the three target guards,
    # and every assignment (including contrary assignments) of destination rows to guard slots.
    guard_orders = list(permutations(sorted(sorted(s) for s in roles.destinations().values())))
    for dest in permutations((3, 4, 5)):
        signals = 0
        for so, go in product(permutations(range(3)), guard_orders):
            rs = []
            for rows in inputs:
                aa, tt, ix = build(rows, roles, so, go, dest)
                rs.append(run(aa, tt))
            z = ix.index(roles.crossing_row)
            assert rs[0]["path"][-1] == rs[1]["path"][-1]
            aa, bb = [registers(r, -1)[z] for r in rs]
            signals += aa != bb
            if dest == (3, 4, 5):
                assert (aa, bb) == ((4, 0), (0, 4))
        assert signals == (36 if dest == (3, 4, 5) else 0)
        print("Destination-row assignment", dest, "gives", signals, "of 36 terminal distinctions at row 4")

    # Test every involutive pairing with no fixed labels, using the true stock
    # producer and stock verifier, holding each target fixed between source arms.
    for target_arm, ref in enumerate(inputs):
        for shift in range(6):
            positive = 0
            for matching in pairings(tuple(range(8))):
                image = dict(matching + tuple((y, x) for x, y in matching))
                mapped = [sorted(image[x] for x in row) for row in ref]
                goal = [mapped[(i-shift) % 6] for i in range(6)]
                out = [registers(run(rows, goal, shift), -1) for rows in inputs]
                observed = [i for i in range(1, 6) if out[0][i] != out[1][i]]
                images = [frozenset(image[x] for x in base[i]) for i in (0, 2)]
                predicts = set(images) == {roles.small, roles.missing}
                if target_arm:
                    predicts = predicts and images[0] == roles.small
                assert observed == ([roles.crossing_row] if predicts else [])
                positive += bool(observed)
            assert positive == (4 if target_arm else 8)
        print(f"Pairing census at target arm {target_arm}: {positive}/105 on each of six shifts")

    # A bounded sensitivity test. Flip every single incidence away from the
    # source, with the same change in both arms, before computing either plan.
    control = Counter()
    failures = []
    for i, x in product(range(1, 6), range(8)):
        variants = [[list(r) for r in rows] for rows in inputs]
        for rows in variants:
            rows[i] = sorted(set(rows[i]) ^ {x})
        a, b = variants
        if min(map(len, a)) < 2:
            control["below floor"] += 1
            continue
        va, vb = infer(a), infer(b)
        if va is None or vb is None or va != vb:
            control["no common unique roles"] += 1
            continue
        prepared = [build(rows, rr) for rows, rr in zip(variants, (va, vb))]
        if any(len(cover(rows)) != 3 or len(cover(rows[:3])) != 2
               or len(cover(goal)) not in (2, 3) for rows, goal, _ in prepared):
            control["guard or endpoint rank"] += 1
            continue
        assert prepared[0][1:] == prepared[1][1:]
        evaluated = [run(rows, goal, diagnostic=True) for rows, goal, _ in prepared]
        if any(errors for _, errors in evaluated):
            print("Historical verifier declined control", (i, x), [err for _, err in evaluated])
            control["historical verifier declined pair"] += 1
            continue
        rs = [r for r, _ in evaluated]
        k = prepared[0][2].index(va.crossing_row)
        signal = registers(rs[0], -1)[k] != registers(rs[1], -1)[k]
        control["terminal distinction" if signal else "same terminal tuple"] += 1
        if not signal:
            failures.append((i, x))
    print("Neighborhood of matched one-bit controls", sorted(control.items()), "admitted negatives", failures)
    assert control == Counter({"below floor": 4, "historical verifier declined pair": 2,
                               "no common unique roles": 27, "same terminal tuple": 3,
                               "terminal distinction": 4})
    if stream:
        stream.close()
    print(f"Verified {count} stock records, uncompressed stream SHA-256 {raw_hash.hexdigest()}")


if __name__ == "__main__":
    main()
