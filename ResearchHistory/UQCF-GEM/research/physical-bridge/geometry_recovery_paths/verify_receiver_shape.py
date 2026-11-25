"""Independent finite-set replay of all interventions, targets, reads and materialized paths."""
from collections import Counter, defaultdict
from copy import deepcopy
from itertools import combinations, permutations, product
import json
import lzma
from pathlib import Path
import sys


def check(value, message):
    if not value:
        raise ValueError(message)


def masks(views):
    return [sum(2 ** v for v in view) for view in views]


def smallest_covers(children, views):
    for count in range(1, len(views) + 1):
        answers = [group for group in combinations(range(len(views)), count)
                   if all(any(child in views[j] for j in group) for child in children)]
        if answers:
            return answers
    raise ValueError("uncovered child")


def model(anchor, zero, chart, leaves, owners, cut):
    p = [-1, 0, 1, 1, 1] + ([0] if anchor else [])
    S, H, R = map(chart.index, "SHR")
    a, b, c = leaves
    tips = sorted(leaves)
    g = {0: 5, 1: 3, a: 0 if zero else 2, b: 0 if zero else 2, c: 1}
    if anchor:
        g[5] = 4
    base = [{0, 1} for _ in chart]
    if anchor:
        base[H].add(5)
    initial = [set(v) for v in base]
    for j, held in ((S, leaves), (H, [a]), (R, [b])):
        initial[j].update(held)
    if anchor:
        check([len(initial[i]) for i in (S, H, R)] == [5, 4, 3], "prior chart addresses")
    target = [set(v) for v in base]
    goal = {leaf: chart.index(key) for leaf, key in zip(leaves, owners)}
    for leaf in tips:
        target[goal[leaf]].add(leaf)

    active = [set(v) for v in initial]
    drop = a if cut == "a" else b
    active[S].remove(drop)
    after = masks(active)
    union = set(range(len(p)))

    def profile(views):
        check(set.union(*views) == union and all(0 in v and all(p[i] in v for i in v if i) for v in views),
              "prefix/coverage")
        return [len(smallest_covers({i for i, up in enumerate(p) if up == v}, views)[0])
                if v in p else 0 for v in range(len(p))]

    def report(view):
        retained = sorted(view)
        projected = dict.fromkeys(retained, 0)
        for v, amount in g.items():
            x = v
            while x not in view:
                x = p[x]
            projected[x] += amount
        # All surviving descendants of p represent precisely its fine subtree.
        common = sum(amount for v, amount in projected.items() if v in set(tips) | {1})
        return dict(nodes=retained, p1=[projected[v] for v in retained], p=projected[1],
                    b_readable=b in view, positive_pair_same=b not in view, common_p=[common, common])

    q = profile(active)
    check(q == profile(target) == [1, 2, 0, 0, 0] + ([0] if anchor else []), "endpoint profile")
    free = [set(v) for v in active]
    free[S].remove(b if cut == "a" else a)
    free_tau = profile(free)[1]
    free_next = [[j, v] for j, view in enumerate(free) for v in sorted(view) if v
                 and all(p[w] != v for w in view) and any(v in other for k, other in enumerate(free) if k != j)]
    check(not free_next, "source-only continuation has a successor")
    covers = smallest_covers(tips, active)
    check(len(covers) == 1, "nonunique minimum cover")
    chosen = {}
    for v in tips:
        keeper, = (j for j in covers[0] if v in active[j])
        chosen[v] = keeper
    source_p = [report(view[S])["p"] for view in (initial, active)]
    states, profiles = [], []

    def append():
        states.append(masks(active))
        profiles.append(profile(active))
        check(sum(abs(x-y) for x, y in zip(profiles[-1], q)) <= 1, "profile width")
        if len(states) > 1:
            check(sum((x ^ y).bit_count() for x, y in zip(states[-2], states[-1])) == 1, "move size")

    append()
    for v in tips:
        for j, view in enumerate(active):
            if v in view and j != chosen[v]:
                view.remove(v)
                append()
    first_R = report(active[R])
    stop = len(states) - 1
    singleton = [2 ** chosen[v] for v in tips]
    reads = []

    def transfer(v, dest):
        old, = (j for j, view in enumerate(active) if v in view)
        check(old != dest, "identity transfer")
        reads.append([tips.index(v), 2 ** old, 2 ** dest])
        active[dest].add(v)
        append()
        active[old].remove(v)
        append()

    # Align the two participating palettes, then resolve the mismatched leaf assignments.
    original_roles, desired_roles = set(chosen.values()), set(goal.values())
    if original_roles != desired_roles:
        old, = original_roles - desired_roles
        new, = desired_roles - original_roles
        for v in tips:
            if v in active[old]:
                transfer(v, new)
    while active != target:
        used = {j for j, view in enumerate(active) if any(v in view for v in tips)}
        needed = desired_roles - used
        candidates = [v for v in tips if v not in active[goal[v]] and (not needed or goal[v] in needed)]
        v = min(candidates)
        transfer(v, goal[v])

    return dict(anchor=anchor, zero=zero, chart=chart, abc=list(leaves), owners=owners, cut=cut,
                prior=masks(initial), post=after, q=q, source_tau=[profile(initial)[1], q[1]],
                free=masks(free), free_tau=[q[1], free_tau], free_next=free_next, target=masks(target), states=states,
                profiles=profiles, source_p=source_p, prior_R=report(initial[R]), shrink_index=stop,
                assignment=singleton, reads=reads, live_list_verified=bool(reads), first_R=first_R,
                final_R=report(target[R]))


def examine(rows):
    observed = {}
    for row in rows:
        key = (row["anchor"], row["zero"], row["chart"], tuple(row["abc"]), row["owners"], row["cut"])
        check(key not in observed, "duplicate execution")
        observed[key] = row
    target_counts = defaultdict(Counter)
    fixed = []
    pairs = 0
    for anchor, zero in product((False, True), repeat=2):
        for order in permutations("SHR"):
            chart = "".join(order)
            for leaves in permutations((2, 3, 4)):
                for owners_tuple in product("SHR", repeat=3):
                    if len(set(owners_tuple)) != 2:
                        continue
                    owners = "".join(owners_tuple)
                    pair = []
                    for cut in "ab":
                        key = (anchor, zero, chart, leaves, owners, cut)
                        actual = observed.pop(key)
                        expected = model(*key)
                        if json.dumps(actual, sort_keys=True) != json.dumps(expected, sort_keys=True):
                            raise ValueError(f"{key} differing fields: {[k for k in expected if actual[k]!=expected[k]]}")
                        pair.append(actual)
                    A, B = pair
                    for field in ("prior", "prior_R", "target", "q", "free", "final_R", "source_p"):
                        check(A[field] == B[field], f"matched {field}")
                    check(A["prior"][chart.index("R")] == A["free"][chart.index("R")], "source-only alternative")
                    check([x["first_R"]["b_readable"] for x in pair] == [False, True], "fixed fine query")
                    check([x["first_R"]["p"] for x in pair] == ([4,4] if zero else [8,6]), "fork atom")
                    check(all(x["first_R"]["common_p"] == ([4,4] if zero else [8,8]) for x in pair), "common responses")
                    first = all(x["reads"] and x["reads"][0][0] == leaves[1] - 2 for x in pair)
                    silent = any(not x["reads"] for x in pair)
                    target_counts[owners]["pairs"] += 1
                    target_counts[owners]["both_first_b"] += int(first)
                    target_counts[owners]["one_no_recolor"] += int(silent)
                    if owners == "HHS":
                        check(first and all(x["shrink_index"] == 1 for x in pair), "fixed-target read")
                        for x, role in zip(pair, "SR"):
                            check(x["reads"][0][1:] == [2 ** chart.index(role), 2 ** chart.index("H")],
                                  "old owner or destination")
                        if chart == "SHR" and leaves == (2,3,4) and not zero and anchor:
                            fixed = pair
                    pairs += 1
    check(not observed and bool(fixed), "extra histories or missing named case")
    stable = sorted(k for k,v in target_counts.items() if v["both_first_b"] == v["pairs"])
    sensitive = sorted(k for k,v in target_counts.items() if 0 < v["both_first_b"] < v["pairs"])
    totals = sum(target_counts.values(), Counter())
    return dict(status="PASS", histories=2*pairs, matched_pairs=pairs, fixed_target_pairs=target_counts["HHS"]["pairs"],
                both_first_b=totals["both_first_b"], pairs_with_silent_arm=totals["one_no_recolor"],
                every_order_first_b=stable, some_orders_first_b=sensitive,
                per_target={k:dict(v) for k,v in sorted(target_counts.items())},
                anchored_fixed_example=fixed)


def rejecting_controls(rows):
    index = next(i for i, row in enumerate(rows) if not row["anchor"] and not row["zero"]
                 and row["chart"] == "SHR" and row["abc"] == [2, 3, 4]
                 and row["owners"] == "SSH" and row["cut"] == "a")
    original = rows[index]

    def changed(field, value):
        trial = rows.copy()
        trial[index] = {**original, field: value}
        return trial

    false_reads = deepcopy(original["reads"])
    false_reads[0][1] = 4 if false_reads[0][1] != 4 else 1
    broken_path = deepcopy(original["states"])
    broken_path[1][2] ^= 1
    tests = {
        "missing_history": rows[:index] + rows[index+1:],
        "duplicate_history": rows + [original],
        "substituted_target": changed("owners", "SRS"),
        "invalid_receiver_move": changed("states", broken_path),
        "wrong_old_holder": changed("reads", false_reads),
        "wrong_reading": changed("first_R", {**original["first_R"], "p": 19}),
        "false_kernel_claim": changed("first_R", {**original["first_R"], "b_readable": True}),
        "false_live_provenance": changed("live_list_verified", False),
        "wrong_boolean_type": changed("live_list_verified", 1),
        "wrong_coverage": changed("source_tau", [1, 3]),
        "wrong_source_only_control": changed("free", original["post"]),
        "wrong_observation_phase": changed("shrink_index", 0),
    }
    for name, data in tests.items():
        try:
            examine(data)
        except (ValueError, KeyError):
            continue
        raise ValueError("accepted corrupted control: " + name)
    return sorted(tests)


def main(directory):
    rows = json.loads(lzma.decompress((directory/"receiver_shape_traces.json.xz").read_bytes()))
    results = examine(rows)
    results["rejecting_controls"] = rejecting_controls(rows)
    (directory/"receiver_shape_certificate.json").write_text(json.dumps(results, indent=2, sort_keys=True) + "\n")
    print(json.dumps({k:v for k,v in results.items() if k not in ("per_target", "anchored_fixed_example")}, sort_keys=True))


if __name__ == "__main__":
    main(Path(sys.argv[1]))
