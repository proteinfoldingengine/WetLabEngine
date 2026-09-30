"""Diagnostic controls; abstract q graph, not a retained-tree counterexample."""
from collections import deque
from importlib.util import spec_from_file_location, module_from_spec
from pathlib import Path
import json
import unittest

ROOT = Path(__file__).resolve().parent
A = {"a": ["u", "v"], "u": ["a", "x"], "v": ["a", "x"],
     "x": ["u", "v", "w"], "w": ["x", "b"], "b": ["w"]}
Q0 = (2, 2, 2)
Q = {"a": Q0, "u": (4, 2, 2), "v": (3, 3, 3),
     "x": Q0, "w": (3, 3, 3), "b": Q0}

def cost(v):
    d = [abs(a-b) for a,b in zip(Q[v], Q0)]
    return (sum(d), max(d), sum(x != 0 for x in d))

def paths(v="a", seen=()):
    if v == "b":
        yield seen + (v,)
        return
    for w in A[v]:
        if w not in seen and w != v:
            yield from paths(w, seen + (v,))

def path_cost(path):
    return tuple(max(cost(v)[i] for v in path) for i in range(3))

def connected(bounds):
    allowed = {v for v in A if all(cost(v)[i] <= bounds[i] for i in range(3))}
    if "a" not in allowed or "b" not in allowed:
        return False
    todo = deque(["a"])
    seen = {"a"}
    while todo:
        v = todo.popleft()
        if v == "b":
            return True
        for w in A[v]:
            if w in allowed and w not in seen:
                seen.add(w)
                todo.append(w)
    return False

def threshold_oracle():
    # Independent nested reachability oracle on this explicit small graph.
    z = [max(cost(v)[i] for v in A) for i in range(3)]
    for i in range(3):
        for t in sorted({cost(v)[i] for v in A}):
            trial = z.copy()
            trial[i] = t
            if connected(trial):
                z = trial
                break
    return tuple(z)

def frozen_result(filename):
    source = ROOT.parent / "v16.36-barrier-law-closure" / filename
    spec = spec_from_file_location("frozen_" + filename.replace(".", "_"), source)
    mod = module_from_spec(spec)
    spec.loader.exec_module(mod)
    # Explicit abstract input adapter: NOT a claim about retained tau realization.
    mod.q = lambda p, state: Q[state]
    return mod.exact(None, A, "a")["b"]

class Controls(unittest.TestCase):
    def test_lexicographic_extension_reverses_preference(self):
        x, y, w = (2,2,1), (3,1,3), (3,1,3)
        self.assertLess(x,y)
        self.assertGreater(tuple(map(max,x,w)), tuple(map(max,y,w)))

    def test_all_simple_paths_and_optimum(self):
        ps = sorted(paths())
        self.assertEqual(ps, [("a","u","x","w","b"), ("a","v","x","w","b")])
        self.assertEqual([path_cost(p) for p in ps], [(3,2,3),(3,1,3)])
        self.assertEqual(min(map(path_cost,ps)), (3,1,3))

    def test_frozen_producer_discards_eventual_optimum(self):
        self.assertEqual(frozen_result("producer.py"), (3,2,3))
        self.assertNotEqual(frozen_result("producer.py"), min(map(path_cost, paths())))

    def test_frozen_verifier_has_same_limitation(self):
        self.assertEqual(frozen_result("verifier.py"), (3,2,3))
        self.assertNotEqual(frozen_result("verifier.py"), min(map(path_cost, paths())))

    def test_nested_threshold_oracle_matches_all_paths(self):
        self.assertEqual(threshold_oracle(), (3,1,3))
        self.assertEqual(threshold_oracle(), min(map(path_cost, paths())))

if __name__ == "__main__":
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(Controls)
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    if not result.wasSuccessful():
        raise SystemExit(1)
    print(json.dumps({
        "scope": "ABSTRACT_GRAPH_DIAGNOSTIC_NOT_RETAINED_CERTIFICATION",
        "simple_paths": list(paths()),
        "path_costs": [path_cost(p) for p in paths()],
        "frozen_producer": frozen_result("producer.py"),
        "frozen_verifier": frozen_result("verifier.py"),
        "exhaustive_optimum": min(map(path_cost, paths())),
        "threshold_oracle": threshold_oracle(),
        "tests": result.testsRun
    }, sort_keys=True))
