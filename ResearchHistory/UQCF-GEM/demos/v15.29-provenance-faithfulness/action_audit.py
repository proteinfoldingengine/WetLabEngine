from __future__ import annotations

from dataclasses import dataclass
import numpy as np

import fiber_model as fm
import provenance_equivalence as pe


@dataclass(frozen=True)
class ActionAudit:
    status: str
    distinction_certified: bool
    action_certified: bool
    group_law_exact: bool
    projection_equivariant: bool
    representation_ready: bool
    reason: str


def audit_real_provenance_action(evidence) -> ActionAudit:
    rows = tuple(evidence)
    distinction_links = tuple(
        row for row in rows
        if getattr(row, 'certifies_q_fiber_relation', False)
    )
    action_links = tuple(
        row for row in rows
        if getattr(row, 'relation_class', None) == 'CERTIFIED_ACTION'
        and getattr(row, 'certifies_action', False)
        and getattr(row, 'certifies_q_fiber_relation', False)
    )

    distinction_certified = bool(distinction_links)
    action_certified = bool(action_links)

    if not action_certified:
        return ActionAudit(
            status=(
                'PROVENANCE_DISTINCTION_EXISTS_BUT_ACTION_NOT_CERTIFIED'
                if distinction_certified
                else 'NO_CERTIFIED_PROVENANCE_ACTION_ON_Q_FIBER'
            ),
            distinction_certified=distinction_certified,
            action_certified=False,
            group_law_exact=False,
            projection_equivariant=False,
            representation_ready=False,
            reason=(
                'NO_FROZEN_CERTIFIED_ACTION_CONNECTS_A_Q_FIBER_PROVENANCE_'
                'RELATION_TO_THE_TORUS_SOURCE_REPRESENTATION'
            ),
        )

    # The current frozen inventory has no such record. If a future frozen
    # inventory introduces one, do not infer group law/equivariance from the
    # metadata booleans alone: those require their own exact witness.
    return ActionAudit(
        status='PROVENANCE_ACTION_METADATA_PRESENT_BUT_EXACT_WITNESS_REQUIRED',
        distinction_certified=distinction_certified,
        action_certified=False,
        group_law_exact=False,
        projection_equivariant=False,
        representation_ready=False,
        reason='CERTIFIED_ACTION_METADATA_ALONE_DOES_NOT_SUPPLY_EXACT_ACTION_WITNESS',
    )


def _synthetic_group_law_exact(actions, complex_) -> bool:
    group = actions.torus_automorphisms(complex_.L)
    if len(group) != 8 * complex_.L * complex_.L:
        return False
    group_set = set(group)
    edge_actions = {g: actions.edge_action(complex_, g) for g in group}

    for g in group:
        for h in group:
            gh = g.compose(h)
            if gh not in group_set:
                return False
            if edge_actions[gh] != edge_actions[g].compose(edge_actions[h]):
                return False
    return True


def _projection_equivariant_exact(actions, complex_) -> bool:
    b1 = complex_.B1.astype(int)
    for g in actions.torus_automorphisms(complex_.L):
        p_edge = actions.edge_action(complex_, g).matrix_int()
        p_vertex = actions.vertex_action(complex_, g).matrix_int()
        if not np.array_equal(b1 @ p_edge, p_vertex @ b1):
            return False
    return True


def audit_synthetic_extension_action() -> ActionAudit:
    _exact, actions = fm._inherited_modules()
    complex_ = fm.load_frozen_complex()

    a, b, synthetic_evidence = pe.synthetic_distinct_control()
    relation = pe.classify_pair(a, b, synthetic_evidence)
    distinction_certified = relation.status == 'PROVENANCE_DISTINCT_CERTIFIED'

    group_law_exact = _synthetic_group_law_exact(actions, complex_)
    projection_equivariant = _projection_equivariant_exact(actions, complex_)

    # Synthetic carrier = the full oriented edge chain representation, with
    # exact projection B1 to the vertex-source carrier. Signed-permutation
    # matrices are a finite linear representation. No representative selector
    # or embedding is used. This is a control, not frozen UQCF evidence.
    action_certified = group_law_exact
    projection_to_q_certified = True
    finite_linear_representation = group_law_exact
    no_arbitrary_selector = True

    representation_ready = all((
        distinction_certified,
        projection_to_q_certified,
        action_certified,
        finite_linear_representation,
        projection_equivariant,
        no_arbitrary_selector,
    ))

    return ActionAudit(
        status=(
            'SYNTHETIC_PROVENANCE_REPRESENTATION_READY'
            if representation_ready
            else 'SYNTHETIC_PROVENANCE_ACTION_CONTROL_FAILED'
        ),
        distinction_certified=distinction_certified,
        action_certified=action_certified,
        group_law_exact=group_law_exact,
        projection_equivariant=projection_equivariant,
        representation_ready=representation_ready,
        reason=(
            'SYNTHETIC_CONTROL_SUPPLIES_EXACT_EDGE_ACTION_B1_PROJECTION_AND_'
            'FINITE_SIGNED_PERMUTATION_REPRESENTATION'
        ),
    )
