from __future__ import annotations

from dataclasses import dataclass

import fiber_model as fm
import provenance_inventory as inv

THEOREM_STATUS = 'PROVENANCE_EXTENSION_NOT_ENTAILED'


@dataclass(frozen=True)
class FrozenReduct:
    q: tuple[int, ...]
    source_role: str
    genesis_status: str
    retained_source_grade: str


@dataclass(frozen=True)
class ProvenanceExpansion:
    reduct: FrozenReduct
    representative_labels: tuple[tuple[int, ...], ...]
    provenance_classes: tuple[str, ...]

    def __post_init__(self) -> None:
        if len(self.representative_labels) != len(self.provenance_classes):
            raise ValueError('one provenance class is required per representative')
        if len(self.representative_labels) < 2:
            raise ValueError('countermodel requires at least two representatives')
        if len(set(self.representative_labels)) != len(self.representative_labels):
            raise ValueError('countermodel representatives must be distinct')
        for representative in self.representative_labels:
            if fm.apply_B1(representative) != self.reduct.q:
                raise ValueError('all representatives must lie in the frozen q-fiber')


def _frozen_reduct() -> FrozenReduct:
    rows = inv.frozen_inventory(inv.REPO_ROOT)
    source_role = inv.by_key('v923-source-role', rows)
    genesis = inv.by_key('v997-genesis-pin', rows)
    retained_grade = inv.by_key('v13.26-source-calibration', rows)

    # These fields retain only independently certified archive facts/types.
    # None contains or infers a map from torus representatives to provenance.
    return FrozenReduct(
        q=fm.root_fixture().q,
        source_role=f'{source_role.key}:{source_role.value_type}',
        genesis_status=f'{genesis.key}:{genesis.value_type}',
        retained_source_grade=f'{retained_grade.key}:{retained_grade.value_type}',
    )


def fiber_countermodels() -> tuple[ProvenanceExpansion, ProvenanceExpansion]:
    root = fm.root_fixture()
    shifted = fm.face_shift(root, face_index=0, coefficient=1)
    if not fm.same_coarse_source(root, shifted):
        raise ArithmeticError('countermodel representatives must share q exactly')

    reduct = _frozen_reduct()
    labels = (root.edge_vector, shifted.edge_vector)

    collapsed = ProvenanceExpansion(
        reduct=reduct,
        representative_labels=labels,
        provenance_classes=('P0', 'P0'),
    )
    distinguishing = ProvenanceExpansion(
        reduct=reduct,
        representative_labels=labels,
        provenance_classes=('P0', 'P1'),
    )
    return collapsed, distinguishing


def same_frozen_reduct(a: ProvenanceExpansion, b: ProvenanceExpansion) -> bool:
    return (
        a.reduct == b.reduct
        and a.representative_labels == b.representative_labels
    )


def _equivalence_signature(expansion: ProvenanceExpansion) -> tuple[tuple[bool, ...], ...]:
    classes = expansion.provenance_classes
    return tuple(
        tuple(classes[i] == classes[j] for j in range(len(classes)))
        for i in range(len(classes))
    )


def relation_disagrees(a: ProvenanceExpansion, b: ProvenanceExpansion) -> bool:
    if not same_frozen_reduct(a, b):
        raise ValueError('non-entailment comparison requires the same frozen reduct')
    return _equivalence_signature(a) != _equivalence_signature(b)


def non_entailment_status() -> str:
    collapsed, distinguishing = fiber_countermodels()
    if not same_frozen_reduct(collapsed, distinguishing):
        raise AssertionError('countermodels do not share one frozen reduct')
    if not relation_disagrees(collapsed, distinguishing):
        raise AssertionError('countermodels do not disagree on provenance relation')
    return THEOREM_STATUS
