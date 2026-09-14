from __future__ import annotations
from dataclasses import dataclass, asdict
from pathlib import Path
import hashlib
import json

REPO_ROOT = Path(__file__).resolve().parents[4]

ELIGIBLE = 'ELIGIBLE_EXACT_COUPLING_AUDIT'
NO_LINK = 'NO_CERTIFIED_SOURCE_TARGET_REPRESENTATION_LINK'
CONDITIONAL_LINK = 'CONDITIONAL_ON_SUPPLIED_INTERTWINER'
ARCHIVE_ONLY = 'ARCHIVE_EVIDENCE_ONLY'

@dataclass(frozen=True)
class CarrierRecord:
    key: str
    artifact_path: str
    git_blob: str
    carrier_type: str
    carrier_dimension: int | None
    action_status: str
    quotient_status: str
    composition_status: str
    label_link_status: str
    eligibility: str
    role: str

    @property
    def eligible(self) -> bool:
        return self.eligibility == ELIGIBLE


def git_blob_hash(path: Path) -> str:
    raw = path.read_bytes()
    return hashlib.sha1(f'blob {len(raw)}\0'.encode() + raw).hexdigest()


_SPECS = (
    dict(key='source-quotient-q-control', artifact_path='ResearchHistory/UQCF-GEM/demos/v15.27-target-origin/target_origin.py', git_blob='1c33232050567bf3b2bf77b19570ec2b8a1fb5e0', carrier_type='balanced_vertex_source_quotient', carrier_dimension=48, action_status='CERTIFIED_TORUS_CHAIN_AUTOMORPHISM_ACTION', quotient_status='CERTIFIED_CONSTANT_VERTEX_MODE_QUOTIENT', composition_status='NOT_REQUIRED_FOR_BASELINE_CONTROL', label_link_status='CERTIFIED_SHARED_TORUS_CHAIN_LABELS', eligibility=ELIGIBLE, role='BASELINE_CONTROL'),
    dict(key='v15.27-target-origin', artifact_path='ResearchHistory/UQCF-GEM/demos/v15.27-target-origin/target_origin.py', git_blob='1c33232050567bf3b2bf77b19570ec2b8a1fb5e0', carrier_type='target_origin_audit', carrier_dimension=None, action_status='CERTIFIED_AUDIT_EVIDENCE', quotient_status='CERTIFIED_SOURCE_QUOTIENT_NO_GO', composition_status='NOT_APPLICABLE', label_link_status='CERTIFIED_SAME_PRETIME_CHAIN_COMPLEX', eligibility=ARCHIVE_ONLY, role='FROZEN_EVIDENCE'),
    dict(key='v15.26-response-selector-rank', artifact_path='ResearchHistory/UQCF-GEM/demos/v15.27-target-origin/baseline/selector_rank.py', git_blob='623defd0d8284e5d9cba6d8f8679de698e5202bc', carrier_type='metric_free_cycle_response_coordinates', carrier_dimension=50, action_status='CERTIFIED_TORUS_CHAIN_AUTOMORPHISM_ACTION', quotient_status='CERTIFIED_CYCLE_SPACE_TARGET', composition_status='NOT_APPLICABLE', label_link_status='CERTIFIED_SAME_PRETIME_CHAIN_COMPLEX', eligibility=ARCHIVE_ONLY, role='TARGET_DEFINITION'),
    dict(key='v14.04-provenance-report', artifact_path='ResearchHistory/UQCF-GEM/v14/v14.04/REPORT.md', git_blob='e5d9566bfc86c801d2933e63453d1800f60a675b', carrier_type='provenance_representation_audit', carrier_dimension=None, action_status='CERTIFIED_ARCHIVE_AUDIT', quotient_status='AUDITED', composition_status='AUDITED', label_link_status='NO_CERTIFIED_LINK_TO_CYCLE_TARGET', eligibility=ARCHIVE_ONLY, role='FROZEN_EVIDENCE'),
    dict(key='v14.04-supplied-intertwiner-control', artifact_path='ResearchHistory/UQCF-GEM/v14/v14.04/REPORT.md', git_blob='e5d9566bfc86c801d2933e63453d1800f60a675b', carrier_type='supplied_intertwiner_control', carrier_dimension=None, action_status='SUPPLIED_CONTROL_ONLY', quotient_status='AUDITED', composition_status='NOT_APPLICABLE', label_link_status='SUPPLIED_NOT_NATURALLY_CERTIFIED', eligibility=CONDITIONAL_LINK, role='NEGATIVE_CONTROL'),
    dict(key='genesis-ledger', artifact_path='ResearchHistory/UQCF-GEM/v14/v14.04/REPORT.md', git_blob='e5d9566bfc86c801d2933e63453d1800f60a675b', carrier_type='append_only_provenance_ledger', carrier_dimension=None, action_status='CERTIFIED_LEDGER_IDENTITY_ONLY', quotient_status='NONE_CERTIFIED', composition_status='LINEAGE_APPEND_ONLY', label_link_status='NO_CERTIFIED_LINK_TO_CYCLE_TARGET', eligibility=NO_LINK, role='PROVENANCE_CANDIDATE'),
    dict(key='genesis-6d-field', artifact_path='ResearchHistory/UQCF-GEM/v14/v14.04/REPORT.md', git_blob='e5d9566bfc86c801d2933e63453d1800f60a675b', carrier_type='genesis_real_6d_field', carrier_dimension=6, action_status='CERTIFIED_MODEL_SPECIFIC_FIELD_ACTION', quotient_status='NONE_CERTIFIED_TO_TARGET', composition_status='NONE_CERTIFIED_TO_TARGET', label_link_status='NO_CERTIFIED_LINK_TO_CYCLE_TARGET', eligibility=NO_LINK, role='PROVENANCE_CANDIDATE'),
    dict(key='retained-scalar-source-grade', artifact_path='ResearchHistory/UQCF-GEM/v13/v13.26/REPORT.md', git_blob='9917085b211ca0e1f4737082227f55097cc72b66', carrier_type='retained_scalar_extensive_source_grade', carrier_dimension=1, action_status='CERTIFIED_SCALAR_TRIVIAL_ACTION', quotient_status='CERTIFIED_SCALAR_GRADE', composition_status='CERTIFIED_EXTENSIVE_GRADE', label_link_status='NO_CERTIFIED_LINK_TO_CYCLE_TARGET', eligibility=NO_LINK, role='PROVENANCE_CANDIDATE'),
    dict(key='retained-graph-source-current', artifact_path='ResearchHistory/UQCF-GEM/v13/v13.26/REPORT.md', git_blob='9917085b211ca0e1f4737082227f55097cc72b66', carrier_type='retained_graph_source_current', carrier_dimension=None, action_status='CERTIFIED_GRAPH_BALANCE_COVARIANCE', quotient_status='CERTIFIED_GRAPH_SOURCE_CURRENT', composition_status='GRAPH_COMPOSITION_NOT_CERTIFIED_TO_TORUS_TARGET', label_link_status='NO_CERTIFIED_LINK_TO_CYCLE_TARGET', eligibility=NO_LINK, role='PROVENANCE_CANDIDATE'),
    dict(key='v15.01-common-parent', artifact_path='ResearchHistory/UQCF-GEM/v15/v15.01/REPORT.md', git_blob='1afbb7aebe384a1fb761f99fd2b040e595be1fa5', carrier_type='common_parent_representation_audit', carrier_dimension=125, action_status='CERTIFIED_COMPATIBILITY_PARENT_ONLY', quotient_status='AUDITED', composition_status='THREE_FACTOR_PARENT', label_link_status='NO_COMMON_PARENT_REPRESENTATION', eligibility=NO_LINK, role='REPRESENTATION_LINK_EVIDENCE'),
    dict(key='v15.02-shared-label', artifact_path='ResearchHistory/UQCF-GEM/v15/v15.02/REPORT.md', git_blob='be1281621b0e2872e555223b2c1cdb98fe9d8011', carrier_type='shared_label_equivariance_audit', carrier_dimension=None, action_status='CERTIFIED_AUDIT_EVIDENCE', quotient_status='AUDITED', composition_status='AUDITED', label_link_status='NO_CERTIFIED_SHARED_LABEL_CARRIER', eligibility=NO_LINK, role='REPRESENTATION_LINK_EVIDENCE'),
    dict(key='v15.03-graph-site-source-lift', artifact_path='ResearchHistory/UQCF-GEM/v15/v15.03/REPORT.md', git_blob='6c3aed73c63c9c7554107d163e15b8fae7549c1c', carrier_type='graph_site_source_lift_audit', carrier_dimension=None, action_status='CERTIFIED_GRAPH_SITE_AUDIT', quotient_status='AUDITED', composition_status='AUDITED', label_link_status='NO_CERTIFIED_GRAPH_SITE_FACTORIZATION', eligibility=NO_LINK, role='REPRESENTATION_LINK_EVIDENCE'),
)


def frozen_inventory(repo_root: Path = REPO_ROOT) -> tuple[CarrierRecord, ...]:
    root = Path(repo_root)
    rows = []
    seen = set()
    for spec in sorted(_SPECS, key=lambda row: row['key']):
        key = spec['key']
        if key in seen:
            raise AssertionError(f'duplicate inventory key: {key}')
        seen.add(key)
        path = root / spec['artifact_path']
        if not path.is_file():
            raise FileNotFoundError(path)
        actual = git_blob_hash(path)
        if actual != spec['git_blob']:
            raise ValueError(f'frozen artifact hash drift for {key}: {actual} != {spec["git_blob"]}')
        row = CarrierRecord(**spec)
        if row.eligible:
            if not row.action_status.startswith('CERTIFIED'):
                raise AssertionError(f'eligible carrier lacks certified action: {key}')
            if not row.label_link_status.startswith('CERTIFIED'):
                raise AssertionError(f'eligible carrier lacks certified target link: {key}')
        rows.append(row)
    return tuple(rows)


def by_key(key: str, records: tuple[CarrierRecord, ...] | None = None) -> CarrierRecord:
    rows = frozen_inventory(REPO_ROOT) if records is None else records
    hits = [row for row in rows if row.key == key]
    if len(hits) != 1:
        raise KeyError(key)
    return hits[0]


def eligible_records(records: tuple[CarrierRecord, ...]) -> tuple[CarrierRecord, ...]:
    return tuple(row for row in records if row.eligible)


def inventory_payload(records: tuple[CarrierRecord, ...]) -> list[dict]:
    return [asdict(row) for row in sorted(records, key=lambda row: row.key)]


def write_inventory(path: Path, records: tuple[CarrierRecord, ...]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(inventory_payload(records), indent=2, sort_keys=True) + '\n')


if __name__ == '__main__':
    write_inventory(Path(__file__).with_name('docs') / 'REPRESENTATION_INVENTORY.json', frozen_inventory())
