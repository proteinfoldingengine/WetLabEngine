from __future__ import annotations

from dataclasses import dataclass

import fiber_model as fm


@dataclass(frozen=True)
class RelationResult:
    status: str
    physical_distinction_certified: bool
    supporting_keys: tuple[str, ...]
    reason: str


@dataclass(frozen=True)
class SyntheticControlEvidence:
    key: str
    relation_class: str
    value_type: str
    certifies_q_fiber_relation: bool
    fiber_tag: tuple[int, ...]
    relation_mode: str
    representative_classes: tuple[tuple[tuple[int, ...], str], ...]

    def __post_init__(self) -> None:
        if self.relation_class != 'SYNTHETIC_CONTROL':
            raise ValueError('synthetic evidence must be explicitly typed SYNTHETIC_CONTROL')
        if not self.certifies_q_fiber_relation:
            raise ValueError('synthetic control must explicitly certify its test relation')
        if self.relation_mode not in {'VALUE_EQUALS_Q', 'EXACT_PARTITION'}:
            raise ValueError('unknown synthetic relation mode')


def classify_pair(a, b, evidence) -> RelationResult:
    if a.q != b.q:
        raise ValueError('pair is not in one q-fiber')
    links = tuple(r for r in evidence if getattr(r, 'certifies_q_fiber_relation', False))
    if not links:
        return RelationResult(
            'PROVENANCE_RELATION_UNSPECIFIED',
            False,
            (),
            'NO_FROZEN_TYPED_RELATION_FROM_TORUS_REPRESENTATIVE_TO_PROVENANCE',
        )
    return classify_from_certified_links(a, b, links)


def classify_from_certified_links(a, b, links) -> RelationResult:
    results = []
    unsupported = []
    for link in links:
        if getattr(link, 'relation_class', None) != 'SYNTHETIC_CONTROL':
            unsupported.append(getattr(link, 'key', 'UNKNOWN'))
            continue
        results.append(_classify_synthetic(a, b, link))

    if not results:
        return RelationResult(
            'PROVENANCE_RELATION_UNSPECIFIED',
            False,
            tuple(sorted(unsupported)),
            'CERTIFIED_LINK_METADATA_LACKS_EXACT_PAIR_EQUIVALENCE_RULE',
        )

    statuses = {r.status for r in results}
    if len(statuses) != 1:
        raise ValueError('certified q-fiber relations disagree')

    status = results[0].status
    keys = tuple(sorted(k for r in results for k in r.supporting_keys))
    # Synthetic controls test adjudication logic only; they never certify a
    # physical source distinction in the frozen UQCF ontology.
    return RelationResult(
        status,
        False,
        keys,
        results[0].reason,
    )


def _classify_synthetic(a, b, link: SyntheticControlEvidence) -> RelationResult:
    if a.q != link.fiber_tag or b.q != link.fiber_tag:
        raise ValueError('synthetic control used outside its declared q-fiber')

    if link.relation_mode == 'VALUE_EQUALS_Q':
        return RelationResult(
            'PROVENANCE_IDENTICAL',
            False,
            (link.key,),
            'SYNTHETIC_CONTROL_PROVENANCE_IS_DETERMINISTIC_FUNCTION_OF_Q',
        )

    assignments = dict(link.representative_classes)
    if a.edge_vector not in assignments or b.edge_vector not in assignments:
        raise ValueError('synthetic exact partition does not cover pair')
    status = (
        'PROVENANCE_IDENTICAL'
        if assignments[a.edge_vector] == assignments[b.edge_vector]
        else 'PROVENANCE_DISTINCT_CERTIFIED'
    )
    return RelationResult(
        status,
        False,
        (link.key,),
        'SYNTHETIC_CONTROL_EXACT_FIBER_PARTITION_ONLY',
    )


def synthetic_collapsed_control():
    a = fm.root_fixture()
    b = fm.face_shift(a, 0, 1)
    evidence = (
        SyntheticControlEvidence(
            key='synthetic-q-deterministic-provenance',
            relation_class='SYNTHETIC_CONTROL',
            value_type='Q_DETERMINISTIC_PROVENANCE_VALUE',
            certifies_q_fiber_relation=True,
            fiber_tag=a.q,
            relation_mode='VALUE_EQUALS_Q',
            representative_classes=(),
        ),
    )
    return a, b, evidence


def synthetic_distinct_control():
    a = fm.root_fixture()
    b = fm.face_shift(a, 0, 1)
    evidence = (
        SyntheticControlEvidence(
            key='synthetic-exact-distinguishing-partition',
            relation_class='SYNTHETIC_CONTROL',
            value_type='EXACT_Q_FIBER_PARTITION',
            certifies_q_fiber_relation=True,
            fiber_tag=a.q,
            relation_mode='EXACT_PARTITION',
            representative_classes=((a.edge_vector, 'A'), (b.edge_vector, 'B')),
        ),
    )
    return a, b, evidence
