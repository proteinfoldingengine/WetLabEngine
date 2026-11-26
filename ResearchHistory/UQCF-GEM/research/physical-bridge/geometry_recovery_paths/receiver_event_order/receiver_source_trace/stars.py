"""Adapters to the pinned four-child producer, its verifier, the source atom and P1."""
from functools import cache
from importlib.util import module_from_spec, spec_from_file_location
from itertools import groupby, permutations
import sys


TIPS = (1, 2, 3, 4)
PARENTS = (-1, 0, 0, 0, 0)
PRIORITIES = tuple(permutations(TIPS))
PALETTES = tuple(permutations(range(3)))


def imported(name, path):
    spec = spec_from_file_location(name, path)
    module = module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def degree(mask):
    return (mask >> 1).bit_count()


def sites(mask):
    return tuple(i for i in range(5) if mask & (1 << i))


def holders(state, tip):
    return tuple(i for i, mask in enumerate(state) if mask & (1 << tip))


def compressed(values):
    return tuple(x for x, _ in groupby(values))


@cache
def encode(mask, priority):
    return 1 + sum(1 << i for i, tip in enumerate(priority, 1) if mask & (1 << tip))


@cache
def decode(mask, priority):
    return 1 + sum(1 << tip for i, tip in enumerate(priority, 1) if mask & (1 << i))


def ordered(state, priority, palette):
    return tuple(encode(state[j], priority) for j in palette)


class Archive:
    def __init__(self, checkout):
        uqcf = checkout / "ResearchHistory/UQCF-GEM"
        demos = uqcf / "demos"
        sys.path.insert(0, str(demos / "v16.53-four-child-boundary"))
        import producer
        import verifier
        self.producer = producer
        self.verifier = verifier
        self.atom = imported("ordinary_source", demos / "v16.26-consistency-increment-law/engine.py")
        self.p1 = imported("graded_projection", demos / "v16.23-overlap-descent/engine.py")
        self.geometry = imported("archive_work", uqcf / "research/physical-bridge/forced_parent_deletion/check_geometry_repair.py")

    @cache
    def height(self, state):
        h, = self.verifier.profile_check(self.producer.Q, len(state), list(state))
        assert h == self.producer.coordinate(state, TIPS)
        return h

    @cache
    def cuts(self, state):
        before = tuple(sites(mask) for mask in state)
        accepted = {}
        for chart, row in enumerate(before):
            for tip in row[1:]:
                try:
                    atom = self.atom.atomic(PARENTS, before, chart, tip)
                except ValueError as error:
                    if str(error) != "same union":
                        raise
                    continue
                end = tuple(sum(1 << i for i in view) for view in atom["after"])
                assert [self.height(state), self.height(end)] == [atom["tau_before"], atom["tau_after"]]
                accepted[chart, tip] = end
        return accepted

    @cache
    def reachable(self, state, prohibited=None):
        seen = {state}
        for command, step in self.cuts(state).items():
            if command != prohibited:
                seen.update(self.reachable(step, prohibited))
        return frozenset(seen)

    @cache
    def route(self, state):
        target = [self.height(state)]
        path = self.producer.normalize(list(state), self.producer.Q, 3, target)
        _, _, end = self.verifier.model(self.producer.Q, target, 3)
        self.verifier.path_check(self.producer.Q, 3, target, path, list(state), end)
        return tuple(tuple(row) for row in path)

    @cache
    def local(self, state, receiver):
        return compressed(x[receiver] for x in self.route(state))

    @cache
    def other_charts(self, state, source):
        return compressed(tuple(mask for j, mask in enumerate(row) if j != source)
                          for row in self.route(state))

    @cache
    def marker(self, state, receiver):
        sequence = self.local(state, receiver)
        b = degree(state[receiver])
        q = self.height(state)
        assert b <= 2 and q in (2, 3)
        expected = list(range(b, 4)) + [4 if q == 2 else 2]
        assert list(map(degree, sequence[:len(expected)])) == expected
        return sequence[len(expected) - 2], sequence[len(expected) - 1]

    @cache
    def grades(self, mask, grade):
        row = sites(mask)
        values = self.p1.push(PARENTS, tuple(range(5)), row, grade)
        return tuple(zip(row, map(int, values)))

    def work(self, state, grade):
        # The shared Pin never contributes to a pairwise cut.
        squares = [sum(grade) ** 2] + [g ** 2 for g in grade[1:]]
        return self.geometry.work_for([sites(m) for m in state], squares)
