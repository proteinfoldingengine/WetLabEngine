from __future__ import annotations

from dataclasses import dataclass, replace
from pathlib import Path
import argparse
import json

import action_audit as aa
import countermodels as cm
import fiber_model as fm
import provenance_equivalence as pe
import provenance_inventory as inv


ALLOWED_STATUSES = {
    'PROVENANCE_COLLAPSES_TO_Q_EQUIVALENCE',
    'PROVENANCE_RELATION_TO_Q_FIBERS_NOT_ENTAILED',
    'PROVENANCE_DISTINGUISHES_REPRESENTATIVES_BUT_NO_NATURAL_ACTION',
    'PROVENANCE_ENHANCED_SOURCE_CARRIER_CERTIFIED',
    'PROVENANCE_SOURCE_REPRESENTATION_READY',
    'PROVENANCE_EXTENSION_REQUIRES_NEW_SOURCE_SEMANTICS_AXIOM',
}

NEXT = {
    'PROVENANCE_COLLAPSES_TO_Q_EQUIVALENCE':
        'NEW_SOURCE_SEMANTICS_OR_INDEPENDENT_CARRIER_PRIMITIVE',
    'PROVENANCE_RELATION_TO_Q_FIBERS_NOT_ENTAILED':
        'INDEPENDENTLY_MOTIVATED_PROVENANCE_FIBER_RELATION',
    'PROVENANCE_DISTINGUISHES_REPRESENTATIVES_BUT_NO_NATURAL_ACTION':
        'CERTIFIED_PROVENANCE_RELABELING_ACTION',
    'PROVENANCE_ENHANCED_SOURCE_CARRIER_CERTIFIED':
        'CANONICAL_LINEARIZATION_OR_FINITE_REPRESENTATION',
    'PROVENANCE_SOURCE_REPRESENTATION_READY':
        'SEPARATE_COUPLING_SPACE_GATE_FOR_S_PROV',
    'PROVENANCE_EXTENSION_REQUIRES_NEW_SOURCE_SEMANTICS_AXIOM':
        'EXPLICIT_AXIOM_APPROVAL_REQUIRED',
}


@dataclass(frozen=True)
class ExtensionAudit:
    status: str
    fiber_relation_status: str
    countermodels_survive: bool
    nontrivial_kernel_certified: bool
    projection_to_q_certified: bool
    natural_action_certified: bool
    representation_ready: bool
    requires_new_source_semantics_axiom: bool
    gravity_observables_evaluated: bool = False
    stop_reason: str | None = None

    def __post_init__(self) -> None:
        if self.status not in ALLOWED_STATUSES:
            raise ValueError(f'unregistered v15.29 status: {self.status}')
        if self.gravity_observables_evaluated:
            raise ValueError('v15.29 is gravity-blind')
        if self.representation_ready and not all((
            self.nontrivial_kernel_certified,
            self.projection_to_q_certified,
            self.natural_action_certified,
        )):
            raise ValueError('representation-ready state lacks prerequisite certificates')


def adjudicate(
    fiber_relation: str,
    countermodels_survive: bool,
    action: aa.ActionAudit,
    source_semantics_required: bool,
) -> str:
    if source_semantics_required:
        return 'PROVENANCE_EXTENSION_REQUIRES_NEW_SOURCE_SEMANTICS_AXIOM'
    if countermodels_survive or fiber_relation == 'PROVENANCE_RELATION_UNSPECIFIED':
        return 'PROVENANCE_RELATION_TO_Q_FIBERS_NOT_ENTAILED'
    if fiber_relation == 'PROVENANCE_IDENTICAL':
        return 'PROVENANCE_COLLAPSES_TO_Q_EQUIVALENCE'
    if fiber_relation == 'PROVENANCE_DISTINCT_CERTIFIED' and not action.action_certified:
        return 'PROVENANCE_DISTINGUISHES_REPRESENTATIVES_BUT_NO_NATURAL_ACTION'
    if action.action_certified and not action.representation_ready:
        return 'PROVENANCE_ENHANCED_SOURCE_CARRIER_CERTIFIED'
    if action.representation_ready:
        return 'PROVENANCE_SOURCE_REPRESENTATION_READY'
    raise AssertionError('unreachable provenance gate state')


def audit_real_archive() -> ExtensionAudit:
    evidence = inv.frozen_inventory(inv.REPO_ROOT)
    a = fm.root_fixture()
    b = fm.face_shift(a, face_index=0, coefficient=1)
    relation = pe.classify_pair(a, b, evidence)

    countermodels_survive = (
        cm.non_entailment_status() == 'PROVENANCE_EXTENSION_NOT_ENTAILED'
    )
    action = aa.audit_real_provenance_action(evidence)

    status = adjudicate(
        relation.status,
        countermodels_survive=countermodels_survive,
        action=action,
        source_semantics_required=False,
    )

    nontrivial_kernel_certified = (
        relation.status == 'PROVENANCE_DISTINCT_CERTIFIED'
        and relation.physical_distinction_certified
    )
    projection_to_q_certified = bool(
        nontrivial_kernel_certified and action.projection_equivariant
    )

    return ExtensionAudit(
        status=status,
        fiber_relation_status=relation.status,
        countermodels_survive=countermodels_survive,
        nontrivial_kernel_certified=nontrivial_kernel_certified,
        projection_to_q_certified=projection_to_q_certified,
        natural_action_certified=action.action_certified,
        representation_ready=action.representation_ready,
        requires_new_source_semantics_axiom=False,
        gravity_observables_evaluated=False,
        stop_reason=(
            'FROZEN_EVIDENCE_ADMITS_COLLAPSED_AND_DISTINGUISHING_'
            'PROVENANCE_EXPANSIONS_OVER_THE_SAME_Q_FIBER'
            if status == 'PROVENANCE_RELATION_TO_Q_FIBERS_NOT_ENTAILED'
            else action.reason
        ),
    )


def _synthetic_extension(action: aa.ActionAudit) -> ExtensionAudit:
    a, b, evidence = pe.synthetic_distinct_control()
    relation = pe.classify_pair(a, b, evidence)
    if relation.status != 'PROVENANCE_DISTINCT_CERTIFIED':
        raise AssertionError('synthetic distinguishing control failed')

    status = adjudicate(
        relation.status,
        countermodels_survive=False,
        action=action,
        source_semantics_required=False,
    )
    return ExtensionAudit(
        status=status,
        fiber_relation_status=relation.status,
        countermodels_survive=False,
        nontrivial_kernel_certified=True,
        projection_to_q_certified=action.projection_equivariant,
        natural_action_certified=action.action_certified,
        representation_ready=action.representation_ready,
        requires_new_source_semantics_axiom=False,
        gravity_observables_evaluated=False,
        stop_reason='SYNTHETIC_CONTROL_ONLY',
    )


def synthetic_carrier_vs_ready_controls() -> tuple[ExtensionAudit, ExtensionAudit]:
    ready_action = aa.audit_synthetic_extension_action()
    if not ready_action.representation_ready:
        raise AssertionError('synthetic representation-ready control failed')

    carrier_action = replace(
        ready_action,
        representation_ready=False,
        status='SYNTHETIC_ENHANCED_CARRIER_WITH_LINEARIZATION_WITHHELD',
        reason='SYNTHETIC_CONTROL_WITHHOLDS_LINEAR_REPRESENTATION_CERTIFICATE',
    )
    carrier = _synthetic_extension(carrier_action)
    ready = _synthetic_extension(ready_action)
    return carrier, ready


def audit_synthetic_controls() -> tuple[ExtensionAudit, ...]:
    carrier, ready = synthetic_carrier_vs_ready_controls()
    return carrier, ready, audit_raw_representative_control()


def audit_raw_representative_control() -> ExtensionAudit:
    # This negative control intentionally asks whether raw microscopic edge
    # incidence may simply be *declared* to be provenance. That declaration is
    # exactly a new source-semantics axiom, not a consequence of frozen theory.
    inert_action = aa.ActionAudit(
        status='NO_CERTIFIED_PROVENANCE_ACTION_ON_Q_FIBER',
        distinction_certified=False,
        action_certified=False,
        group_law_exact=False,
        projection_equivariant=False,
        representation_ready=False,
        reason='RAW_EDGE_DIFFERENCE_HAS_NO_FROZEN_PROVENANCE_SEMANTICS',
    )
    status = adjudicate(
        'RAW_MICROSCOPIC_INCIDENCE_DIFFERENCE',
        countermodels_survive=False,
        action=inert_action,
        source_semantics_required=True,
    )
    return ExtensionAudit(
        status=status,
        fiber_relation_status='RAW_MICROSCOPIC_INCIDENCE_DIFFERENCE',
        countermodels_survive=False,
        nontrivial_kernel_certified=False,
        projection_to_q_certified=False,
        natural_action_certified=False,
        representation_ready=False,
        requires_new_source_semantics_axiom=True,
        gravity_observables_evaluated=False,
        stop_reason='RAW_REPRESENTATIVE_IDENTITY_REQUIRES_NEW_SOURCE_SEMANTICS_AXIOM',
    )


def audit() -> dict:
    result = audit_real_archive()
    evidence = inv.frozen_inventory(inv.REPO_ROOT)
    scientific_breakthrough = (
        result.status == 'PROVENANCE_SOURCE_REPRESENTATION_READY'
    )
    extension_kernel_status = (
        'CERTIFIED_NONTRIVIAL'
        if result.nontrivial_kernel_certified
        else 'NOT_CERTIFIED'
    )

    return {
        'version': 'v15.29',
        'status': result.status,
        'base_sha': inv.BASE_SCIENTIFIC_HEAD,
        'inventory_hash': inv.inventory_digest(evidence),
        'fiber_fixture_count': 2,
        'fiber_relation_counts': {result.fiber_relation_status: 1},
        'countermodels_survive': result.countermodels_survive,
        'extension_kernel_status': extension_kernel_status,
        'projection_to_q_certified': result.projection_to_q_certified,
        'natural_action_certified': result.natural_action_certified,
        'representation_ready': result.representation_ready,
        'coupling_solver_reopened': False,
        'new_source_semantics_axiom_added': False,
        'gravity_observables_evaluated': False,
        'uses_holonomy_selector': False,
        'uses_newton_or_gr': False,
        'uses_metric_selector': False,
        'uses_pruning': False,
        'uses_entropy': False,
        'uses_physical_time': False,
        'scientific_breakthrough': scientific_breakthrough,
        'signal_of_life': False,
        'gravity_canary_certified': False,
        'physical_gravity_derived': False,
        'Pillar_3': 'OPEN',
        'next_required_object': NEXT[result.status],
    }


def write_audit(out_dir: Path) -> Path:
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    path = out_dir / 'verification.json'
    path.write_text(json.dumps(audit(), indent=2, sort_keys=True) + '\n')
    return path


def main() -> None:
    parser = argparse.ArgumentParser(
        description='Run the gravity-blind v15.29 provenance source-extension gate.'
    )
    parser.add_argument('--out', type=Path, default=Path(__file__).with_name('outputs'))
    args = parser.parse_args()
    path = write_audit(args.out)
    print(path)
    print(json.dumps(audit(), sort_keys=True))


if __name__ == '__main__':
    main()
