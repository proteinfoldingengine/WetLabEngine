"""Check the case-50 receiver row against the original v16.51 code and certificate."""

import gzip
import hashlib
import json
import sys
from collections import Counter, deque
from functools import lru_cache
from itertools import combinations, groupby, product
from pathlib import Path

sys.path.insert(0, str(Path(sys.argv[1]).resolve()))
import producer
import verifier


@lru_cache(maxsize=131072)
def profile(tree, state):
    return tuple(verifier.profile_check(tree, len(state), list(state)))


def excursion(tree, state, target):
    return sum(abs(a - b) for a, b in zip(profile(tree, state), target))


def reproduce_archive():
    document = producer.produce()
    raw = (json.dumps(document, sort_keys=True, separators=(",", ":")) + "\n").encode()
    compressed = gzip.compress(raw, compresslevel=9, mtime=0)
    # The original gzip used the Unix OS header byte.
    compressed = compressed[:9] + bytes([3]) + compressed[10:]
    blob = hashlib.sha1(f"blob {len(compressed)}\0".encode() + compressed).hexdigest()
    assert blob == "571d38f08006b7023a65ec64cac77fe23e0db52a"
    print("Original certificate Git blob", blob)
    return document


def primitive(before, after):
    edits = [(owner, a ^ b) for owner, (a, b) in enumerate(zip(before, after)) if a != b]
    assert len(edits) == 1
    owner, difference = edits[0]
    assert difference.bit_count() == 1
    return owner, difference.bit_length() - 1


def check_census(document):
    totals = Counter()
    for case in document["cases"]:
        assert case["failure"] is None
        spec = case["spec"]
        tree = producer.TREES[spec["tree"]]
        nodes = producer.layout(tree)
        internal = [u for u, children in enumerate(nodes) if children]
        parents = {child: u for u, children in enumerate(nodes) for child in children}
        branch = {u: r for r in nodes[0] for u in producer.vertices(nodes, r)}
        target = spec["q"]
        states = [tuple(s) for s in case["path"]]
        defects = []
        totals["cases"] += 1
        for index, state in enumerate(states):
            current = profile(tree, state)
            assert excursion(tree, state, target) <= 1
            bad = [u for u, a, b in zip(internal, target, current) if a != b]
            defects.append(bad[0] if bad else None)
            if index:
                previous = states[index - 1]
                _, site = primitive(previous, state)
                changed = {u for u, a, b in zip(internal, profile(tree, previous), current) if a != b}
                assert changed <= {parents[site]}
                assert defects[index - 1] is None or not bad or defects[index - 1] == bad[0]
        for index, (left, gap, right) in enumerate(zip(defects, defects[1:], defects[2:])):
            if left is None or right is None or gap is not None or left == right:
                continue
            totals["exact frame between distinct defects"] += 1
            if left == 0 or right == 0 or branch[left] == branch[right]:
                continue
            before, middle, after = states[index:index + 3]
            first_owner, first_site = primitive(before, middle)
            second_owner, second_site = primitive(middle, after)
            if first_owner == second_owner:
                continue
            assert parents[first_site] == left and parents[second_site] == right
            assert len(nodes[left]) == len(nodes[right]) == 2
            assert target[internal.index(left)] == target[internal.index(right)] == 2
            assert all(before[first_owner] >> j & 1 for j in nodes[left])
            assert not middle[first_owner] >> first_site & 1
            assert all(after[second_owner] >> j & 1 for j in nodes[right])
            assert not middle[second_owner] >> second_site & 1
            premature = list(before)
            premature[second_owner] ^= 1 << second_site
            assert excursion(tree, tuple(premature), target) == 2
            totals["separate top branches and label rows"] += 1
    assert tuple(totals[k] for k in ("cases", "exact frame between distinct defects",
                                     "separate top branches and label rows")) == (2592, 1412, 245)
    print("Archive windows", dict(totals))


def check_completions(tree, target, start):
    admitted = set()
    for supports in product((1, 2, 3), repeat=9):
        # The shared root is always present. Each other site has 3 nonempty support choices.
        state = tuple(1 + sum(1 << i for i, m in enumerate(supports, 1) if m & label)
                      for label in (1, 2))
        try:
            cost = excursion(tree, state, target)
        except verifier.InterfaceNotPreserved:
            continue
        if cost <= 1:
            admitted.add(state)

    queue = deque([start])
    reachable = {start}
    while queue:
        state = queue.popleft()
        for owner in range(2):
            for site in range(1, 10):
                neighbor = list(state)
                neighbor[owner] ^= 1 << site
                pair = tuple(neighbor)
                if pair in admitted and pair not in reachable:
                    reachable.add(pair)
                    queue.append(pair)
    assert admitted == reachable and len(admitted) == 210
    print("Admitted states, states reachable from the archived start", len(admitted), len(reachable))
    for observed, expected_count, expected_present in [(497, 6, 1), (499, 5, 0)]:
        partners = sorted(b for a, b in admitted if a == observed)
        present = sum(bool(b & (1 << 8)) for b in partners)
        assert (len(partners), present) == (expected_count, expected_present)
        print(f"Receiver {observed}: source masks {partners}; source site 8 present in {present}")

    contrary = {a for a, b in admitted if b & (1 << 8)}
    for size in (1, 2, 3):
        certificates = []
        for sites in combinations(range(1, 10), size):
            bits = sum(1 << i for i in sites)
            if all((a ^ 499) & bits for a in contrary):
                certificates.append(sites)
        if size < 3:
            assert not certificates
    assert certificates == [(1, 2, 8), (1, 3, 8), (1, 4, 8), (1, 5, 8), (1, 6, 8)]
    print("Minimum site tests with bits set as in receiver 499", certificates)


def check_order_and_writer(tree, target, case, endpoint):
    path = [tuple(s) for s in case["path"]]
    original = path[:6]
    assert original == [(753, 399), (1009, 399), (1009, 143), (1009, 655), (497, 655), (499, 655)]
    assert verifier.path_check(tree, 2, target, case["path"], case["start"], endpoint) == [1, 1, 1]
    late = [path[0], path[1], (1009, 911), (497, 911), (499, 911), path[5]]
    for route in (original, late):
        for before, after in zip(route, route[1:]):
            primitive(before, after)
    original_costs = [excursion(tree, state, target) for state in original]
    late_costs = [excursion(tree, state, target) for state in late]
    assert original_costs == [0, 1, 1, 1, 0, 1] and late_costs == [0, 1, 1, 1, 2, 1]
    assert all(s[1] & (1 << 8) for s in late[:-1])
    assert [a for a, _ in groupby(s[0] for s in original)] == [a for a, _ in groupby(s[0] for s in late)]
    print("Original and source-late costs", original_costs, late_costs)
    try:
        verifier.path_check(tree, 2, target, [list(s) for s in late + path[6:]], case["start"], endpoint)
    except verifier.InterfaceNotPreserved as error:
        assert str(error) == "total excursion exceeds one"
        print("Verifier rejects reordered path:", error)
    else:
        raise AssertionError("historical verifier accepted two simultaneous errors")

    # One extra release and restoration are invisible to the complete receiver word.
    extra = path[:3] + [path[1], path[2]] + path[3:]
    assert verifier.path_check(tree, 2, target, [list(s) for s in extra], case["start"], endpoint) == [1, 1, 1]
    assert [a for a, _ in groupby(s[0] for s in path)] == [a for a, _ in groupby(s[0] for s in extra)]
    def releases_before_write(route):
        first_write = next(i for i, s in enumerate(route) if s[0] == 499)
        return sum(bool(a[1] & 256) and not bool(b[1] & 256)
                   for a, b in zip(route[:first_write], route[1:first_write + 1]))
    assert (releases_before_write(path), releases_before_write(extra)) == (1, 2)
    print("Accepted paths with the same full receiver word: source releases before first 499 are 1 and 2")

    # Capture the actual call and parameters at entry to the historical transport helper.
    invocations = []
    def capture(frame, event, arg):
        if event == "call" and frame.f_code is producer.transport_child.__code__:
            args = frame.f_locals
            invocations.append((tuple(args["state"]), args["child"], tuple(args["roles"]),
                                tuple(args["desired"]), tuple(args["P"])))
    sys.setprofile(capture)
    try:
        assert producer.normalize(case["start"], tree, 2, target) == case["path"]
    finally:
        sys.setprofile(None)
    state, child, roles, desired, palette = invocations[0]
    assert (state, child, roles, desired, palette) == ((497, 655), 1, (1,), (0,), (0, 1))
    for source in (655, 911):
        output = producer.transport_child([497, source], tree, child, roles, desired, palette)
        assert output[1] == [499, source]
        print(f"Original transport helper with source {source}: {output[0]} -> {output[1]}")


def main():
    document = reproduce_archive()
    case = document["cases"][50]
    tree = producer.TREES["T"]
    target = case["spec"]["q"]
    assert case["spec"] == dict(tree="T", q=[2, 1, 1, 2], k=2, permutation="reversal", mode="compact")
    endpoint = verifier.model(tree, target, 2)[2]
    check_completions(tree, target, tuple(case["start"]))
    check_order_and_writer(tree, target, case, endpoint)
    check_census(document)


if __name__ == "__main__":
    main()
