"""Complete the one-edit return census on the frozen symmetric grade-two orbit."""
from collections import Counter
from contextlib import redirect_stdout
from fractions import Fraction
from io import StringIO
import json
from pathlib import Path
import runpy
import sys

here = Path(__file__).resolve().parent
demos = Path(sys.argv[1]).resolve()
with redirect_stdout(StringIO()):
    prev = runpy.run_path(str(here.parent / "symmetric_matched_event/probe.py"))
P, A, base, mu, nbr = (prev[k] for k in ("P", "A", "base", "mu", "nbr"))
change, build = prev["change"], prev["build"]
leaves = Counter(prev["leaf_list"])
assert all(n == 2 for n in leaves.values())


def census():
    ledger = []
    for first, count in sorted(leaves.items()):
        if not first & 1:
            continue
        cut = change(base, A, first, -1)
        after_mask = first ^ 1
        available = leaves.copy()
        available[first] -= 1
        available[after_mask] += 1
        source_min = {k for k in P[1:] if cut[A][k] == mu}
        below = {k for k in P[1:] if cut[A][k] < mu}
        # Ignore the mutual entry until the second edit; both edits can change it.
        destinations = [j for j in P[1:] if j not in nbr[A] and not nbr[j] & nbr[A]
                        and not (below - {j}) and source_min - {j} == nbr[j]]
        answers = []
        for j in [A, *destinations]:
            goal = nbr[A]
            if j != A:
                assert {base[j][k] - mu for k in goal} == {4}
            for m, multiplicity in sorted(available.items()):
                sign = -1 if (m >> j) & 1 else 1
                def new(k):
                    return cut[j][k] + 4 * sign * (1 - 2 * ((m >> k) & 1))
                if any(new(k) != mu for k in goal):
                    continue
                if any(new(k) <= mu for k in P if k != j and k not in goal):
                    continue
                nxt = change(cut, j, m, sign)
                if j == A and nxt == base:
                    status = "prior carrier"
                else:
                    try:
                        build(nxt)
                        status = "admitted"
                    except ValueError as error:
                        status = str(error)
                answers.append([j, hex(m), sign, multiplicity, status])
        ledger.append(dict(mask=hex(first), multiplicity=count, possible_remote=destinations,
                           answers=answers))
    return ledger


def traced(call):
    seen = set()
    def profile(frame, event, arg):
        if event == "call":
            seen.add((frame.f_globals.get("__name__"), frame.f_code.co_name))
    previous = sys.getprofile()
    sys.setprofile(profile)
    try:
        value = call()
    finally:
        sys.setprofile(previous)
    return value, seen


def consumer_check():
    sys.path.insert(0, str(demos / "v15.40-global-balance-geometry-specificity"))
    import geometry_specificity_gate as comparator
    import evaluate
    from incidence_target import construct_incidence_target
    from projection import Payload, Projection
    from response_geometry import ResponseGeometry
    original_edges = sorted((j, k) for j in P for k in nbr[j] if j < k)
    target = construct_incidence_target(tuple(tuple(int(i == j) - int(i == k) for i in P)
                                             for j, k in original_edges))
    readings = []
    for label, w in (("prior", base), ("cut36", change(base, A, prev["mB"], -1)),
                     ("cut41", change(base, A, prev["mC"], -1))):
        pairs = prev["pairs"]
        minimum = min(w[j][k] for j, k in pairs)
        edges = tuple((j, k) for j, k in pairs if w[j][k] == minimum)
        mat = tuple(tuple(map(Fraction, row)) for row in w)
        # Sufficient triangle test for these specific positive off-diagonals.
        assert 0 < minimum and max(w[j][k] for j, k in pairs) < 2 * minimum
        assert all(w[j][j] == 0 and all(w[j][k] == w[k][j] for k in P) for j in P)
        geom = ResponseGeometry(P, mat, minimum, frozenset(map(frozenset, edges)),
                                True, True, True, True, len(pairs), len(P)**3)
        comp, trace = traced(lambda: comparator.compare_geometry(geom, target))
        bfs = (comparator.__name__, "_distances") in trace
        assert bfs == comp.distances_equal == comp.neighbors_equal == (label == "prior")
        if label != "prior":
            payload = Payload(11, Fraction(1), P, mat, edges, ())
            def evaluate_cut():
                try:
                    evaluate.evaluate_projection(Projection("", (), (payload,), ()))
                except ValueError as error:
                    return str(error)
                raise AssertionError("irregular payload accepted")
            stop, active = traced(evaluate_cut)
            assert stop == "degree_not_four"
            assert ("operational_complex", "construct_operational_complex") in active
            assert ("application", "evaluate_field") not in active
        else:
            stop = None
        readings.append([label, comp.metric_passes, bfs, stop])
    return readings


rows = census()
print(json.dumps({"starts": rows, "consumer": consumer_check()}, sort_keys=True))
