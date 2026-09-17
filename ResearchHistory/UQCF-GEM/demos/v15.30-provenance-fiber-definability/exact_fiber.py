from __future__ import annotations

from dataclasses import dataclass

import frozen_inputs as fi


@dataclass(frozen=True)
class FiberCase:
    key: str
    edge_vector: tuple[int, ...]
    q: tuple[int, ...]

    def __post_init__(self) -> None:
        if any(type(value) is not int for value in self.edge_vector):
            raise ValueError('exact fiber representative must be integral')
        if any(type(value) is not int for value in self.q):
            raise ValueError('exact coarse source must be integral')


def canonical_fiber_cases() -> tuple[FiberCase, ...]:
    fm = fi.load_v1529().fiber_model
    root = fm.root_fixture()
    face = fm.face_shift(root, face_index=0, coefficient=1)
    cycle = fm.cycle_shift(root, fm.canonical_cycle_basis()[7])
    return (
        FiberCase('root', tuple(root.edge_vector), tuple(root.q)),
        FiberCase('face-boundary-shift', tuple(face.edge_vector), tuple(face.q)),
        FiberCase('cycle-shift', tuple(cycle.edge_vector), tuple(cycle.q)),
    )


def same_q_exact(a: FiberCase, b: FiberCase) -> bool:
    return a.q == b.q


def noncycle_control_preserves_q(root: FiberCase, edge_index: int) -> bool:
    fm = fi.load_v1529().fiber_model
    if type(edge_index) is not int or not 0 <= edge_index < len(root.edge_vector):
        raise ValueError('edge index out of range')
    shifted = list(root.edge_vector)
    shifted[edge_index] += 1
    q = tuple(fm.apply_B1(tuple(shifted)))
    return q == root.q


def evaluate_labeling_on_fiber(label_fn) -> tuple[object, ...]:
    return tuple(label_fn(case) for case in canonical_fiber_cases())
