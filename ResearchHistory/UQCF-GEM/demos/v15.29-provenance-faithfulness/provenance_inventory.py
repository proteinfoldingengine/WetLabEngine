from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path
import argparse
import hashlib
import json

REPO_ROOT = Path(__file__).resolve().parents[4]
BASE_SCIENTIFIC_HEAD = "42244310b065f473c8bd459a6f065a61afbd2292"

_ALLOWED_RELATION_CLASSES = {
    "CERTIFIED_PROVENANCE_RELATION",
    "CERTIFIED_GAUGE_OR_EQUIVALENCE",
    "CERTIFIED_ACTION",
    "CERTIFIED_PROJECTION_TO_Q",
    "ARCHIVE_EVIDENCE_ONLY",
    "NO_TYPED_RELATION",
    "CONDITIONAL_ON_SUPPLIED_MAP",
}


@dataclass(frozen=True)
class EvidenceRecord:
    key: str
    path: str
    blob: str
    domain: str
    codomains: tuple[str, ...]
    relation_class: str
    value_type: str
    certifies_q_fiber_relation: bool
    certifies_action: bool
    claim_boundary: str


def git_blob_sha(raw: bytes) -> str:
    return hashlib.sha1(f"blob {len(raw)}\0".encode() + raw).hexdigest()


def verify_record(root: Path, record: EvidenceRecord) -> None:
    path = root / record.path
    if not path.is_file():
        raise FileNotFoundError(path)
    actual = git_blob_sha(path.read_bytes())
    if actual != record.blob:
        raise ValueError(
            f"frozen evidence changed: {record.key}: {actual} != {record.blob}"
        )


_SPECS = (
    {'key': 'v15.28-report', 'path': 'ResearchHistory/UQCF-GEM/demos/v15.28-coupling-space/README.md', 'blob': '1ea6c653dd45b2c01da1bb5a09f629bd2d12e67d', 'domain': 'Q_ONLY_COUPLING_AUDIT', 'codomains': ('Q_SOURCE_QUOTIENT', 'CYCLE_RESPONSE_TARGET'), 'relation_class': 'ARCHIVE_EVIDENCE_ONLY', 'value_type': 'V15_28_COUPLING_REPORT', 'certifies_q_fiber_relation': False, 'certifies_action': False, 'claim_boundary': 'Q_ONLY_COUPLING_SPACE_DIMENSION_3_AND_PROVENANCE_LINK_BLOCK'},
    {'key': 'v15.28-ledger', 'path': 'ResearchHistory/UQCF-GEM/demos/v15.28-coupling-space/docs/RESULTS.json', 'blob': '6d1ed9766d89c2f66d072978a8fa4b60bedccb39', 'domain': 'Q_ONLY_COUPLING_AUDIT', 'codomains': ('Q_SOURCE_QUOTIENT', 'CYCLE_RESPONSE_TARGET'), 'relation_class': 'ARCHIVE_EVIDENCE_ONLY', 'value_type': 'V15_28_COUPLING_LEDGER', 'certifies_q_fiber_relation': False, 'certifies_action': False, 'claim_boundary': 'PRETIME_COUPLING_BLOCKED_BY_REPRESENTATION_LINK'},
    {'key': 'v15.27-target-origin', 'path': 'ResearchHistory/UQCF-GEM/demos/v15.27-target-origin/target_origin.py', 'blob': '1c33232050567bf3b2bf77b19570ec2b8a1fb5e0', 'domain': 'TORUS_CHAIN_SOURCE_RESPONSE_AUDIT', 'codomains': ('Q_SOURCE_QUOTIENT', 'CYCLE_RESPONSE_TARGET'), 'relation_class': 'ARCHIVE_EVIDENCE_ONLY', 'value_type': 'TARGET_ORIGIN_AUDIT', 'certifies_q_fiber_relation': False, 'certifies_action': False, 'claim_boundary': 'CYCLE_RESPONSE_TARGET_DOES_NOT_FACTOR_THROUGH_Q'},
    {'key': 'v15.26-selector-rank', 'path': 'ResearchHistory/UQCF-GEM/demos/v15.27-target-origin/baseline/selector_rank.py', 'blob': '623defd0d8284e5d9cba6d8f8679de698e5202bc', 'domain': 'TORUS_CHAIN_RESPONSE_COORDINATES', 'codomains': ('CYCLE_RESPONSE_TARGET',), 'relation_class': 'ARCHIVE_EVIDENCE_ONLY', 'value_type': 'METRIC_FREE_CYCLE_RESPONSE_COORDINATES', 'certifies_q_fiber_relation': False, 'certifies_action': False, 'claim_boundary': 'TARGET_SELECTOR_CONDITIONAL_NOT_SOURCE_PROVENANCE'},
    {'key': 'v15.25-pretime-canary', 'path': 'ResearchHistory/UQCF-GEM/demos/v15.27-target-origin/baseline/baseline/pretime_gravity_canary.py', 'blob': '99110f943550751645539c0c8a7339024d7fefd3', 'domain': 'TORUS_CHAIN_CANARY_FIXTURE', 'codomains': ('Q_SOURCE_QUOTIENT',), 'relation_class': 'ARCHIVE_EVIDENCE_ONLY', 'value_type': 'PRETIME_CANARY_FIXTURE', 'certifies_q_fiber_relation': False, 'certifies_action': False, 'claim_boundary': 'FIXTURE_ONLY_NO_PROVENANCE_FIBER_SEMANTICS'},
    {'key': 'v15.09-carrier-origin', 'path': 'ResearchHistory/UQCF-GEM/v15/v15.09/REPORT.md', 'blob': 'ec73ef9240dcef062c95a82c511a874d0d2923ef', 'domain': 'RETAINED_RELATIONAL_CARRIER', 'codomains': ('QUANTUM_SUBSYSTEM_CARRIER', 'COMPATIBILITY_PARENT'), 'relation_class': 'NO_TYPED_RELATION', 'value_type': 'CROSS_DOMAIN_CARRIER_ORIGIN_AUDIT', 'certifies_q_fiber_relation': False, 'certifies_action': False, 'claim_boundary': 'CANONICAL_NEUTRAL_STRUCTURE_DOES_NOT_DERIVE_RETAINED_QUANTUM_CARRIER'},
    {'key': 'v15.08-source-semantics', 'path': 'ResearchHistory/UQCF-GEM/v15/v15.08/REPORT.md', 'blob': '23bbeaecdb81adfe1a39b3140569d23c367b8b55', 'domain': 'FROZEN_PROVENANCE_SOURCE_ONTOLOGY', 'codomains': ('PHYSICAL_SOURCE_SEMANTICS', 'HERMITIAN_SOURCE_GENERATOR'), 'relation_class': 'NO_TYPED_RELATION', 'value_type': 'SOURCE_SEMANTICS_IRREDUCIBILITY', 'certifies_q_fiber_relation': False, 'certifies_action': False, 'claim_boundary': 'SOURCE_SEMANTICS_IRREDUCIBLE_RELATIVE_TO_FROZEN_ONTOLOGY'},
    {'key': 'v15.07-neutral-reference', 'path': 'ResearchHistory/UQCF-GEM/v15/v15.07/REPORT.md', 'blob': 'c3abb3af5b5c7210fc717392d4e2cc6fc4648284', 'domain': 'QUANTUM_STATE_CARRIER', 'codomains': ('FRAME_NEUTRAL_REFERENCE', 'CENTERED_LOG_INFORMATION_GENERATOR'), 'relation_class': 'ARCHIVE_EVIDENCE_ONLY', 'value_type': 'CANONICAL_QUANTUM_INFORMATION_STRUCTURE', 'certifies_q_fiber_relation': False, 'certifies_action': False, 'claim_boundary': 'CANONICAL_INTRA_QUANTUM_STRUCTURE_NOT_SOURCE_SEMANTICS'},
    {'key': 'v15.03-graph-site-source-lift', 'path': 'ResearchHistory/UQCF-GEM/v15/v15.03/REPORT.md', 'blob': '6c3aed73c63c9c7554107d163e15b8fae7549c1c', 'domain': 'RETAINED_GRAPH_CARRIER', 'codomains': ('QUANTUM_SITE_CARRIER',), 'relation_class': 'NO_TYPED_RELATION', 'value_type': 'GRAPH_SITE_SOURCE_LIFT_AUDIT', 'certifies_q_fiber_relation': False, 'certifies_action': False, 'claim_boundary': 'NO_CERTIFIED_GRAPH_SITE_FACTORIZATION'},
    {'key': 'v15.02-shared-label', 'path': 'ResearchHistory/UQCF-GEM/v15/v15.02/REPORT.md', 'blob': 'be1281621b0e2872e555223b2c1cdb98fe9d8011', 'domain': 'RETAINED_GRAPH_LABELS', 'codomains': ('QUANTUM_SITE_LABELS',), 'relation_class': 'NO_TYPED_RELATION', 'value_type': 'SHARED_LABEL_EQUIVARIANCE_AUDIT', 'certifies_q_fiber_relation': False, 'certifies_action': False, 'claim_boundary': 'NO_CERTIFIED_SHARED_LABEL_CARRIER'},
    {'key': 'v15.01-common-parent', 'path': 'ResearchHistory/UQCF-GEM/v15/v15.01/REPORT.md', 'blob': '1afbb7aebe384a1fb761f99fd2b040e595be1fa5', 'domain': 'COMPATIBILITY_PARENT', 'codomains': ('COMPATIBILITY_SUPPORT',), 'relation_class': 'ARCHIVE_EVIDENCE_ONLY', 'value_type': 'COMMON_PARENT_REPRESENTATION_AUDIT', 'certifies_q_fiber_relation': False, 'certifies_action': False, 'claim_boundary': 'NO_COMMON_PARENT_REPRESENTATION_FROM_PROVENANCE'},
    {'key': 'v14.04-provenance-representation', 'path': 'ResearchHistory/UQCF-GEM/v14/v14.04/REPORT.md', 'blob': 'e5d9566bfc86c801d2933e63453d1800f60a675b', 'domain': 'PROVENANCE_CARRIER', 'codomains': ('HERMITIAN_25_SUPPORT_SOURCE',), 'relation_class': 'CONDITIONAL_ON_SUPPLIED_MAP', 'value_type': 'PROVENANCE_REPRESENTATION_AUDIT', 'certifies_q_fiber_relation': False, 'certifies_action': False, 'claim_boundary': 'REQUIRES_NEW_REPRESENTATION_LINK'},
    {'key': 'v13.26-source-calibration', 'path': 'ResearchHistory/UQCF-GEM/v13/v13.26/REPORT.md', 'blob': '9917085b211ca0e1f4737082227f55097cc72b66', 'domain': 'RETAINED_SOURCE_CURRENT', 'codomains': ('OBSERVER_SOURCE_CALIBRATION', 'RETAINED_SOURCE_GRADE'), 'relation_class': 'ARCHIVE_EVIDENCE_ONLY', 'value_type': 'SOURCE_CALIBRATION_ORIGIN_BOUNDARY', 'certifies_q_fiber_relation': False, 'certifies_action': False, 'claim_boundary': 'ABSOLUTE_SOURCE_CALIBRATION_NOT_DERIVED'},
    {'key': 'v997-genesis-pin', 'path': 'Tmp/TOE/Einstein 4/V997_FULL_STACK_GENESIS_PIN_BRIDGE_REPORT.md', 'blob': '8f4ee48cbaf6c822b87dd5e30a5dfee4d596e26e', 'domain': 'HISTORY_PROVENANCE', 'codomains': ('PINNED_REGISTRY', 'GENESIS_ROOT', 'WITNESS_QUORUM', 'APPEND_ONLY_CONTINUITY'), 'relation_class': 'CERTIFIED_PROVENANCE_RELATION', 'value_type': 'GENESIS_HISTORY_LEGITIMACY', 'certifies_q_fiber_relation': False, 'certifies_action': False, 'claim_boundary': 'HISTORY_LEGITIMACY_NOT_MICROSCOPIC_INCIDENCE'},
    {'key': 'v923-source-role', 'path': 'Tmp/TOE/Einstein 3/v923_full_stack_source_role_closure_proof/FULL_REPORT_AND_PROOF.md', 'blob': '9a1523c08d2b9b2c5ba2d298dfed3d563a750bec', 'domain': 'RECOVERABILITY_SOURCE_LEGITIMACY', 'codomains': ('SOURCE_ROLE_CLASS',), 'relation_class': 'CERTIFIED_PROVENANCE_RELATION', 'value_type': 'TERNARY_SOURCE_ROLE', 'certifies_q_fiber_relation': False, 'certifies_action': False, 'claim_boundary': 'DISCRETE_SOURCE_LEGITIMACY_NOT_TORUS_EDGE_LABEL'},
)


def frozen_inventory(repo_root: Path = REPO_ROOT) -> tuple[EvidenceRecord, ...]:
    root = Path(repo_root)
    rows: list[EvidenceRecord] = []
    seen: set[str] = set()

    for spec in sorted(_SPECS, key=lambda row: row["key"]):
        key = spec["key"]
        if key in seen:
            raise AssertionError(f"duplicate evidence key: {key}")
        seen.add(key)

        record = EvidenceRecord(**spec)
        if record.relation_class not in _ALLOWED_RELATION_CLASSES:
            raise AssertionError(
                f"unregistered relation class for {key}: {record.relation_class}"
            )
        if record.certifies_q_fiber_relation and record.relation_class not in {
            "CERTIFIED_PROVENANCE_RELATION",
            "CERTIFIED_GAUGE_OR_EQUIVALENCE",
            "CERTIFIED_PROJECTION_TO_Q",
        }:
            raise AssertionError(
                f"q-fiber claim lacks a certified typed relation: {key}"
            )
        if record.certifies_action and record.relation_class != "CERTIFIED_ACTION":
            raise AssertionError(f"action claim lacks CERTIFIED_ACTION type: {key}")

        verify_record(root, record)
        rows.append(record)

    return tuple(rows)


def by_key(
    key: str, records: tuple[EvidenceRecord, ...] | None = None
) -> EvidenceRecord:
    rows = frozen_inventory(REPO_ROOT) if records is None else records
    hits = [row for row in rows if row.key == key]
    if len(hits) != 1:
        raise KeyError(key)
    return hits[0]


def inventory_payload(records: tuple[EvidenceRecord, ...]) -> list[dict]:
    return [asdict(row) for row in sorted(records, key=lambda row: row.key)]


def inventory_digest(records: tuple[EvidenceRecord, ...]) -> str:
    text = json.dumps(
        inventory_payload(records), sort_keys=True, separators=(",", ":")
    )
    return hashlib.sha256(text.encode()).hexdigest()


def write_inventory(path: Path, records: tuple[EvidenceRecord, ...]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(inventory_payload(records), indent=2, sort_keys=True) + "\n"
    )


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Verify and serialize frozen v15.29 provenance evidence."
    )
    parser.add_argument(
        "--out",
        type=Path,
        default=Path(__file__).with_name("docs") / "PROVENANCE_EVIDENCE.json",
    )
    args = parser.parse_args()
    records = frozen_inventory(REPO_ROOT)
    write_inventory(args.out, records)
    print(
        json.dumps(
            {
                "base_scientific_head": BASE_SCIENTIFIC_HEAD,
                "inventory_digest": inventory_digest(records),
                "records": len(records),
            },
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
