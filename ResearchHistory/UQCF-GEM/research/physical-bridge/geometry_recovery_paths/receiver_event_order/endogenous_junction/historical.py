"""Load unchanged historical implementations and verify primitive edits independently."""
from functools import cache
from importlib.util import module_from_spec, spec_from_file_location
from itertools import groupby
import sys


def module_file(name, path):
    spec = spec_from_file_location(name, path)
    result = module_from_spec(spec)
    spec.loader.exec_module(result)
    return result


class History:
    def __init__(self, checkout):
        demos = checkout / "ResearchHistory/UQCF-GEM/demos"
        sys.path.insert(0, str(demos / "v16.53-four-child-boundary"))
        import producer
        import verifier
        self.p, self.v = producer, verifier
        self.atom = module_file("source_atom", demos / "v16.26-consistency-increment-law/engine.py")
        self.cert = module_file("source_verifier", demos / "v16.26-consistency-increment-law/verify.py")
        self.p1 = module_file("p1", demos / "v16.23-overlap-descent/engine.py")

    @cache
    def parents(self, tree):
        children = self.p.layout(tree)
        return tuple([-1] + [next(i for i, row in enumerate(children) if n in row)
                             for n in range(1, len(children))])

    def verify_cut(self, tree, state, chart, site):
        parents = self.parents(tree)
        views = [positions(m, len(parents)) for m in state]
        doc = self.atom.atomic(parents, views, chart, site)
        delta, flag = self.cert.verify_atomic(doc)
        after = tuple(sum(1 << v for v in row) for row in doc["after"])
        assert after == toggle(state, chart, site)
        return after, (doc["tau_before"], doc["tau_after"], delta, flag)

    @cache
    def moves(self, tree, state):
        parents = self.parents(tree)
        nodes = self.p.layout(tree)
        valid = {}
        for j, mask in enumerate(state):
            for i in range(1, len(nodes)):
                present = bool(mask & (1 << i))
                if present:
                    if any(mask & (1 << u) for u in nodes[i]):
                        continue
                    if not any(n != j and m & (1 << i) for n, m in enumerate(state)):
                        continue
                elif not mask & (1 << parents[i]):
                    continue
                nxt = toggle(state, j, i)
                high, low = (state, nxt) if present else (nxt, state)
                assert self.verify_cut(tree, high, j, i)[0] == low
                valid[j, i, -1 if present else 1] = nxt
        return valid

    @cache
    def profile(self, tree, state):
        return tuple(self.v.profile_check(tree, len(state), list(state)))

    @cache
    def endpoint(self, tree, k, q):
        return tuple(self.v.model(tree, q, k)[2])

    def check_path(self, tree, q, path):
        self.v.path_check(tree, len(path[0]), list(q), [list(s) for s in path],
                          list(path[0]), list(self.endpoint(tree, len(path[0]), q)))

    @cache
    def normalize(self, tree, q, state):
        path = tuple(map(tuple, self.p.normalize(list(state), tree, len(state), list(q))))
        self.check_path(tree, q, path)
        return path

    def grades(self, tree, mask):
        parents = self.parents(tree)
        row = positions(mask, len(parents))
        values = self.p1.push(parents, tuple(range(len(parents))), row, [1] * len(parents))
        return tuple(zip(row, map(int, values)))


def positions(mask, size):
    return tuple(i for i in range(size) if mask & (1 << i))


def toggle(state, chart, tip):
    result = list(state)
    result[chart] ^= 1 << tip
    return tuple(result)


def move(before, after):
    (j, delta), = [(i, x ^ y) for i, (x, y) in enumerate(zip(before, after)) if x != y]
    assert delta.bit_count() == 1
    return j, delta.bit_length()-1, 1 if after[j] > before[j] else -1


def local(path, j):
    return tuple(m for m, _ in groupby(row[j] for row in path))


def last_root_move(nodes, path):
    return next((i for i in range(len(path)-1, 0, -1)
                 if move(path[i-1], path[i])[1] in nodes[0]), None)
