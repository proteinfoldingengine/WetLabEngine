from __future__ import annotations

from dataclasses import dataclass, replace


@dataclass(frozen=True)
class FiniteRelation:
    rep_keys: tuple[str, ...]
    labels: tuple[str, ...]

    def __post_init__(self) -> None:
        if len(self.rep_keys) != len(self.labels):
            raise ValueError('one label is required per representative')
        if len(set(self.rep_keys)) != len(self.rep_keys):
            raise ValueError('representative keys must be unique')


@dataclass(frozen=True)
class FiniteAction:
    elements: tuple[str, ...]
    rep_permutations: dict[str, tuple[int, ...]]
    label_permutations: dict[str, tuple[int, ...]]
    multiplication: dict[tuple[str, str], str]


@dataclass(frozen=True)
class NaturalityResult:
    certified: bool
    group_law_exact: bool
    equivariant: bool
    reason: str


def _is_permutation(values: tuple[int, ...], size: int) -> bool:
    return len(values) == size and tuple(sorted(values)) == tuple(range(size))


def _compose(g: tuple[int, ...], h: tuple[int, ...]) -> tuple[int, ...]:
    if len(g) != len(h):
        raise ValueError('permutation dimensions disagree')
    return tuple(g[h[i]] for i in range(len(g)))


def check_group_law(action: FiniteAction) -> bool:
    elements = tuple(action.elements)
    if not elements or len(set(elements)) != len(elements):
        return False
    if set(action.rep_permutations) != set(elements):
        return False
    if set(action.label_permutations) != set(elements):
        return False

    rep_size = len(action.rep_permutations[elements[0]])
    label_size = len(action.label_permutations[elements[0]])
    for element in elements:
        if not _is_permutation(action.rep_permutations[element], rep_size):
            return False
        if not _is_permutation(action.label_permutations[element], label_size):
            return False

    for g in elements:
        for h in elements:
            product = action.multiplication.get((g, h))
            if product not in elements:
                return False
            if action.rep_permutations[product] != _compose(
                action.rep_permutations[g], action.rep_permutations[h]
            ):
                return False
            if action.label_permutations[product] != _compose(
                action.label_permutations[g], action.label_permutations[h]
            ):
                return False
    return True


def check_equivariance(relation: FiniteRelation, action: FiniteAction) -> bool:
    labels = tuple(sorted(set(relation.labels)))
    label_index = {label: i for i, label in enumerate(labels)}
    rep_size = len(relation.rep_keys)
    label_size = len(labels)

    for element in action.elements:
        rep_perm = action.rep_permutations.get(element)
        label_perm = action.label_permutations.get(element)
        if rep_perm is None or label_perm is None:
            return False
        if not _is_permutation(rep_perm, rep_size):
            return False
        if not _is_permutation(label_perm, label_size):
            return False
        for i, label in enumerate(relation.labels):
            lhs = relation.labels[rep_perm[i]]
            rhs = labels[label_perm[label_index[label]]]
            if lhs != rhs:
                return False
    return True


def audit_relation_naturality(
    relation: FiniteRelation, certified_action: FiniteAction | None
) -> NaturalityResult:
    if certified_action is None:
        return NaturalityResult(
            certified=False,
            group_law_exact=False,
            equivariant=False,
            reason='NO_CERTIFIED_ACTION_FOR_DEFINABILITY',
        )

    group_law = check_group_law(certified_action)
    if not group_law:
        return NaturalityResult(
            certified=False,
            group_law_exact=False,
            equivariant=False,
            reason='CERTIFIED_ACTION_GROUP_LAW_FAILED',
        )

    equivariant = check_equivariance(relation, certified_action)
    if not equivariant:
        return NaturalityResult(
            certified=False,
            group_law_exact=True,
            equivariant=False,
            reason='FROZEN_AUTOMORPHISM_CHANGES_PROPOSED_RELATION',
        )

    return NaturalityResult(
        certified=True,
        group_law_exact=True,
        equivariant=True,
        reason='EXACT_FINITE_NATURALITY_CERTIFIED',
    )


def _z2_multiplication() -> dict[tuple[str, str], str]:
    return {
        ('e', 'e'): 'e',
        ('e', 's'): 's',
        ('s', 'e'): 's',
        ('s', 's'): 'e',
    }


def synthetic_swap_counterexample() -> tuple[FiniteRelation, FiniteAction]:
    relation = FiniteRelation(
        rep_keys=('r0', 'r1'),
        labels=('A', 'B'),
    )
    action = FiniteAction(
        elements=('e', 's'),
        rep_permutations={
            'e': (0, 1),
            's': (1, 0),
        },
        # The frozen provenance values remain unchanged while the two
        # representatives are swapped. A relation that distinguishes them is
        # therefore not definable from that frozen reduct.
        label_permutations={
            'e': (0, 1),
            's': (0, 1),
        },
        multiplication=_z2_multiplication(),
    )
    return relation, action


def synthetic_equivariant_control() -> tuple[FiniteRelation, FiniteAction]:
    relation = FiniteRelation(
        rep_keys=('r0', 'r1'),
        labels=('A', 'B'),
    )
    action = FiniteAction(
        elements=('e', 's'),
        rep_permutations={
            'e': (0, 1),
            's': (1, 0),
        },
        label_permutations={
            'e': (0, 1),
            's': (1, 0),
        },
        multiplication=_z2_multiplication(),
    )
    return relation, action


def break_multiplication_table(action: FiniteAction) -> FiniteAction:
    broken = dict(action.multiplication)
    if 's' not in action.elements or 'e' not in action.elements:
        raise ValueError('control requires e and s elements')
    broken[('s', 's')] = 's'
    return replace(action, multiplication=broken)
