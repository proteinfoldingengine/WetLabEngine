from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path
import argparse
import json

import exact_fiber as ef
import frozen_inputs as fi
import naturality as nat
import typed_carrier_graph as tc
import uniqueness as uq

ALLOWED_STATUSES = {
    'NO_TYPED_COMMON_CARRIER',
    'PROVENANCE_FIBER_RELATION_NOT_DEFINABLE',
    'MULTIPLE_NATURAL_RELATIONS_REMAIN',
    'CANONICAL_PROVENANCE_FIBER_RELATION_CERTIFIED',
}

NEXT = {
    'NO_TYPED_COMMON_CARRIER':
        'GENUINELY_TYPED_COMMON_CARRIER_OR_EXPLICIT_NEW_AXIOM',
    'PROVENANCE_FIBER_RELATION_NOT_DEFINABLE':
        'LOCALIZED_SYMMETRY_OR_DEFINABILITY_OBSTRUCTION',
    'MULTIPLE_NATURAL_RELATIONS_REMAIN':
        'ADDITIONAL_PRIMITIVE_SELECTING_AMONG_NATURAL_RELATIONS',
    'CANONICAL_PROVENANCE_FIBER_RELATION_CERTIFIED':
        'SEPARATE_PROVENANCE_ACTION_REPRESENTATION_READINESS_GATE',
}

BASE_SHA = '6535ea69214f6661e340fe201813dfd17ddbb7e1'


@dataclass(frozen=True)
class CandidateAudit:
    key: str
    gate_a_common_carrier: bool
    gate_b_exact_fiber: bool | None
    gate_c_natural: bool | None
    gate_d_unique: bool | None
    gate_e_no_choice: bool | None
    relation_signatures: tuple[tuple[int, ...], ...]
    stop_reason: str

    def __post_init__(self) -> None:
        if not self.gate_a_common_carrier:
            if any(value is not None for value in (
                self.gate_b_exact_fiber,
                self.gate_c_natural,
                self.gate_d_unique,
                self.gate_e_no_choice,
            )):
                raise ValueError('later gates must be NOT_REACHED after Gate A failure')
        if self.gate_b_exact_fiber is False:
            if any(value is not None for value in (
                self.gate_c_natural,
                self.gate_d_unique,
                self.gate_e_no_choice,
            )):
                raise ValueError('later gates must be NOT_REACHED after Gate B failure')
        if self.gate_c_natural is False:
            if any(value is not None for value in (
                self.gate_d_unique,
                self.gate_e_no_choice,
            )):
                raise ValueError('later gates must be NOT_REACHED after Gate C failure')
        if self.gate_d_unique is False and self.gate_e_no_choice is not None:
            raise ValueError('Gate E is not reached after Gate D nonuniqueness')


@dataclass(frozen=True)
class DefinabilityAudit:
    status: str
    candidates: tuple[CandidateAudit, ...]
    countermodels_survive: bool
    canonical_relation_certified: bool

    def __post_init__(self) -> None:
        if self.status not in ALLOWED_STATUSES:
            raise ValueError(f'unregistered v15.30 status: {self.status}')
        if self.canonical_relation_certified != (
            self.status == 'CANONICAL_PROVENANCE_FIBER_RELATION_CERTIFIED'
        ):
            raise ValueError('canonical-relation flag disagrees with status')


def _nontrivial_signature(signature: tuple[int, ...]) -> bool:
    return len(set(signature)) > 1


def adjudicate(results: tuple[CandidateAudit, ...]) -> str:
    typed = [result for result in results if result.gate_a_common_carrier]
    if not typed:
        return 'NO_TYPED_COMMON_CARRIER'

    natural = [
        result for result in typed
        if result.gate_b_exact_fiber is True and result.gate_c_natural is True
    ]
    if not natural:
        return 'PROVENANCE_FIBER_RELATION_NOT_DEFINABLE'

    signatures = {
        signature
        for result in natural
        for signature in result.relation_signatures
    }
    if len(signatures) >= 2:
        return 'MULTIPLE_NATURAL_RELATIONS_REMAIN'

    if any(result.gate_d_unique is False for result in natural):
        return 'MULTIPLE_NATURAL_RELATIONS_REMAIN'

    positive = [
        result for result in natural
        if result.gate_d_unique is True and result.gate_e_no_choice is True
    ]
    if (
        len(signatures) == 1
        and positive
        and _nontrivial_signature(next(iter(signatures)))
    ):
        return 'CANONICAL_PROVENANCE_FIBER_RELATION_CERTIFIED'

    return 'PROVENANCE_FIBER_RELATION_NOT_DEFINABLE'


def _real_q_fiber_relation_records(candidate: fi.CandidateEvidence):
    modules = fi.load_v1529()
    records = modules.provenance_inventory.frozen_inventory(
        modules.provenance_inventory.REPO_ROOT
    )
    keys = set(candidate.evidence_keys)
    return tuple(
        record for record in records
        if record.key in keys and record.certifies_q_fiber_relation
    )


def audit_candidate(
    candidate: fi.CandidateEvidence,
    graph: tc.CarrierGraph | None = None,
) -> CandidateAudit:
    if graph is None:
        graph, _ = tc.build_real_graph()

    connection = tc.find_typed_connection(
        graph,
        candidate.domain,
        'TORUS_EDGE_REPRESENTATIVE',
        real_only=True,
    )
    if not connection.real_certified:
        return CandidateAudit(
            key=candidate.key,
            gate_a_common_carrier=False,
            gate_b_exact_fiber=None,
            gate_c_natural=None,
            gate_d_unique=None,
            gate_e_no_choice=None,
            relation_signatures=(),
            stop_reason='GATE_A_NO_CERTIFIED_TYPED_COMMON_CARRIER',
        )

    relation_records = _real_q_fiber_relation_records(candidate)
    if not relation_records:
        return CandidateAudit(
            key=candidate.key,
            gate_a_common_carrier=True,
            gate_b_exact_fiber=False,
            gate_c_natural=None,
            gate_d_unique=None,
            gate_e_no_choice=None,
            relation_signatures=(),
            stop_reason='GATE_B_NO_CERTIFIED_Q_FIBER_RELATION_WITNESS',
        )

    return CandidateAudit(
        key=candidate.key,
        gate_a_common_carrier=True,
        gate_b_exact_fiber=False,
        gate_c_natural=None,
        gate_d_unique=None,
        gate_e_no_choice=None,
        relation_signatures=(),
        stop_reason='GATE_B_RELATION_METADATA_LACKS_EXACT_LABELING_WITNESS',
    )


def _build_audit(results: tuple[CandidateAudit, ...]) -> DefinabilityAudit:
    status = adjudicate(results)
    natural_signatures = {
        signature
        for result in results
        if result.gate_b_exact_fiber is True and result.gate_c_natural is True
        for signature in result.relation_signatures
    }
    countermodels = (
        len(natural_signatures) >= 2
        or any(
            result.gate_c_natural is True and result.gate_d_unique is False
            for result in results
        )
    )
    return DefinabilityAudit(
        status=status,
        candidates=results,
        countermodels_survive=countermodels,
        canonical_relation_certified=(
            status == 'CANONICAL_PROVENANCE_FIBER_RELATION_CERTIFIED'
        ),
    )


def audit_real_archive() -> DefinabilityAudit:
    graph, candidates = tc.build_real_graph()
    if len(candidates) != 4:
        raise AssertionError('v15.30 real audit requires exactly four candidates')
    results = tuple(audit_candidate(candidate, graph) for candidate in candidates)
    return _build_audit(results)


def _synthetic_candidate(
    key: str,
    *,
    common: bool,
    exact: bool | None,
    natural: bool | None,
    unique: bool | None,
    no_choice: bool | None,
    signatures: tuple[tuple[int, ...], ...] = (),
    reason: str,
) -> CandidateAudit:
    return CandidateAudit(
        key=key,
        gate_a_common_carrier=common,
        gate_b_exact_fiber=exact,
        gate_c_natural=natural,
        gate_d_unique=unique,
        gate_e_no_choice=no_choice,
        relation_signatures=signatures,
        stop_reason=reason,
    )


def synthetic_common_word_null_control() -> DefinabilityAudit:
    result = _synthetic_candidate(
        'common-word-null',
        common=False,
        exact=None,
        natural=None,
        unique=None,
        no_choice=None,
        reason='UNTYPED_COMMON_WORDS_DO_NOT_CREATE_A_RELATION',
    )
    return _build_audit((result,))


def synthetic_no_common_carrier_control() -> DefinabilityAudit:
    return synthetic_common_word_null_control()


def synthetic_supplied_embedding_control() -> DefinabilityAudit:
    graph = tc.synthetic_supplied_embedding_graph()
    connection = tc.find_typed_connection(
        graph,
        'SYNTHETIC_PROVENANCE',
        'TORUS_EDGE_REPRESENTATIVE',
        real_only=True,
    )
    result = _synthetic_candidate(
        'supplied-embedding',
        common=connection.real_certified,
        exact=None,
        natural=None,
        unique=None,
        no_choice=None,
        reason='SUPPLIED_EMBEDDING_IS_NOT_DERIVED_FROZEN_EVIDENCE',
    )
    return _build_audit((result,))


def synthetic_q_collapsed_control() -> DefinabilityAudit:
    signature = uq.canonical_partition_signature(('Q', 'Q', 'Q'))
    result = _synthetic_candidate(
        'q-collapsed',
        common=True,
        exact=True,
        natural=True,
        unique=True,
        no_choice=True,
        signatures=(signature,),
        reason='SYNTHETIC_RELATION_IS_ONLY_A_FUNCTION_OF_Q',
    )
    return _build_audit((result,))


def synthetic_explicit_distinguishing_control() -> DefinabilityAudit:
    signature = uq.canonical_partition_signature(('A', 'B', 'B'))
    result = _synthetic_candidate(
        'explicit-distinguishing',
        common=True,
        exact=True,
        natural=True,
        unique=True,
        no_choice=False,
        signatures=(signature,),
        reason='EXPLICIT_PARTITION_IS_SUPPLIED_NOT_DERIVED',
    )
    return _build_audit((result,))


def synthetic_automorphism_rejection_control() -> DefinabilityAudit:
    relation, action = nat.synthetic_swap_counterexample()
    naturality = nat.audit_relation_naturality(relation, action)
    result = _synthetic_candidate(
        'automorphism-rejection',
        common=True,
        exact=True,
        natural=naturality.certified,
        unique=None,
        no_choice=None,
        reason=naturality.reason,
    )
    return _build_audit((result,))


def synthetic_unique_natural_control() -> DefinabilityAudit:
    relation, action = nat.synthetic_equivariant_control()
    naturality = nat.audit_relation_naturality(relation, action)
    uniqueness = uq.classify_relation_family((('A', 'B'), ('X', 'Y')))
    signature = uniqueness.signatures[0]
    result = _synthetic_candidate(
        'unique-natural',
        common=True,
        exact=True,
        natural=naturality.certified,
        unique=(uniqueness.status == 'UNIQUE'),
        no_choice=True,
        signatures=(signature,),
        reason='SYNTHETIC_UNIQUE_NATURAL_RELATION_CONTROL',
    )
    return _build_audit((result,))


def synthetic_cross_candidate_multiple_control() -> DefinabilityAudit:
    first = _synthetic_candidate(
        'natural-a',
        common=True,
        exact=True,
        natural=True,
        unique=True,
        no_choice=True,
        signatures=(uq.canonical_partition_signature(('A', 'A', 'B')),),
        reason='FIRST_NATURAL_RELATION',
    )
    second = _synthetic_candidate(
        'natural-b',
        common=True,
        exact=True,
        natural=True,
        unique=True,
        no_choice=True,
        signatures=(uq.canonical_partition_signature(('A', 'B', 'B')),),
        reason='SECOND_INEQUIVALENT_NATURAL_RELATION',
    )
    return _build_audit((first, second))


def audit_synthetic_controls() -> tuple[DefinabilityAudit, ...]:
    return (
        synthetic_common_word_null_control(),
        synthetic_supplied_embedding_control(),
        synthetic_q_collapsed_control(),
        synthetic_explicit_distinguishing_control(),
        synthetic_automorphism_rejection_control(),
        synthetic_unique_natural_control(),
    )


def audit() -> dict:
    result = audit_real_archive()
    candidates = tuple(result.candidates)
    natural_signatures = {
        signature
        for candidate in candidates
        if candidate.gate_c_natural is True
        for signature in candidate.relation_signatures
    }
    status = result.status
    return {
        'version': 'v15.30',
        'base_sha': BASE_SHA,
        'status': status,
        'candidate_count': len(candidates),
        'candidate_results': [asdict(candidate) for candidate in candidates],
        'common_carrier_count': sum(
            candidate.gate_a_common_carrier for candidate in candidates
        ),
        'exact_fiber_relation_count': sum(
            candidate.gate_b_exact_fiber is True for candidate in candidates
        ),
        'natural_relation_count': len(natural_signatures),
        'countermodels_survive': result.countermodels_survive,
        'canonical_relation_certified': result.canonical_relation_certified,
        'new_source_semantics_axiom_added': False,
        'coupling_solver_reopened': False,
        'gravity_observables_evaluated': False,
        'uses_holonomy_selector': False,
        'uses_newton_or_gr': False,
        'uses_metric_selector': False,
        'uses_pruning_as_selector': False,
        'uses_entropy_as_selector': False,
        'uses_physical_time': False,
        'scientific_breakthrough': (
            status == 'CANONICAL_PROVENANCE_FIBER_RELATION_CERTIFIED'
        ),
        'signal_of_life': False,
        'gravity_canary_certified': False,
        'physical_gravity_derived': False,
        'Pillar_3': 'OPEN',
        'next_required_object': NEXT[status],
    }


def write_audit(out_dir: Path) -> Path:
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    path = out_dir / 'verification.json'
    path.write_text(json.dumps(audit(), indent=2, sort_keys=True) + '\n')
    return path


def main() -> None:
    parser = argparse.ArgumentParser(
        description='Run the gravity-blind v15.30 provenance-fiber definability gate.'
    )
    parser.add_argument(
        '--out', type=Path, default=Path(__file__).with_name('outputs')
    )
    args = parser.parse_args()
    path = write_audit(args.out)
    print(path)
    print(json.dumps(audit(), sort_keys=True))


if __name__ == '__main__':
    main()
