from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path
import argparse
import hashlib
import importlib.util
import json
import sys

REPO_ROOT = Path(__file__).resolve().parents[4]
V1529_DIR = REPO_ROOT / 'ResearchHistory/UQCF-GEM/demos/v15.29-provenance-faithfulness'
V1529_BASE_SHA = '6535ea69214f6661e340fe201813dfd17ddbb7e1'
SCIENTIFIC_SOURCE_SHA = '42244310b065f473c8bd459a6f065a61afbd2292'

V1529_PINS = {
    'provenance_inventory.py': '81a41442d2f3b26817657ebb5f3dc948e62d14b2',
    'fiber_model.py': 'e04cf0b24bbce6f908b83c9472c1f1b5639b7e8b',
    'source_extension_gate.py': '305af411792c08906ea8eed2c9aeba3de25be1cf',
    'docs/RESULTS.json': '0984a8238a7fd2a115ab673a3d4f23b0706c7b12',
}


@dataclass(frozen=True)
class CandidateEvidence:
    key: str
    domain: str
    evidence_keys: tuple[str, ...]
    artifact_pins: tuple[tuple[str, str], ...]
    transformation_source: str
    certified_relation_claims: tuple[str, ...]
    claim_boundary: str


@dataclass(frozen=True)
class FrozenModules:
    provenance_inventory: object
    fiber_model: object
    source_extension_gate: object
    v1529_results: dict


def git_blob_sha(raw: bytes) -> str:
    return hashlib.sha1(f'blob {len(raw)}\0'.encode() + raw).hexdigest()


def verify_blob(path: Path, expected_blob: str) -> None:
    if not path.is_file():
        raise FileNotFoundError(path)
    actual = git_blob_sha(path.read_bytes())
    if actual != expected_blob:
        raise ValueError(f'frozen blob changed: {path}: {actual} != {expected_blob}')


def _load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise ImportError(path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


_FROZEN_MODULES: FrozenModules | None = None


def load_v1529() -> FrozenModules:
    global _FROZEN_MODULES
    if _FROZEN_MODULES is not None:
        return _FROZEN_MODULES

    for relative, blob in V1529_PINS.items():
        verify_blob(V1529_DIR / relative, blob)

    ledger = json.loads((V1529_DIR / 'docs/RESULTS.json').read_text())
    if ledger.get('version') != 'v15.29':
        raise ValueError('pinned v15.29 ledger version mismatch')
    if ledger.get('status') != 'PROVENANCE_RELATION_TO_Q_FIBERS_NOT_ENTAILED':
        raise ValueError('pinned v15.29 adjudication mismatch')
    if ledger.get('next_required_object') != 'INDEPENDENTLY_MOTIVATED_PROVENANCE_FIBER_RELATION':
        raise ValueError('pinned v15.29 next-object mismatch')

    provenance_inventory = _load_module(
        '_v1530_v1529_provenance_inventory', V1529_DIR / 'provenance_inventory.py'
    )
    fiber_model = _load_module(
        '_v1530_v1529_fiber_model', V1529_DIR / 'fiber_model.py'
    )

    inserted = False
    v1529_text = str(V1529_DIR)
    if v1529_text not in sys.path:
        sys.path.insert(0, v1529_text)
        inserted = True
    try:
        source_extension_gate = _load_module(
            '_v1530_v1529_source_extension_gate', V1529_DIR / 'source_extension_gate.py'
        )
    finally:
        if inserted:
            sys.path.remove(v1529_text)

    _FROZEN_MODULES = FrozenModules(
        provenance_inventory=provenance_inventory,
        fiber_model=fiber_model,
        source_extension_gate=source_extension_gate,
        v1529_results=ledger,
    )
    return _FROZEN_MODULES


_CANDIDATES = (
    CandidateEvidence(
        key='genesis-history-lineage',
        domain='HISTORY_PROVENANCE',
        evidence_keys=('v997-genesis-pin',),
        artifact_pins=(
            ('Tmp/TOE/Einstein 4/V997_FULL_STACK_GENESIS_PIN_BRIDGE_REPORT.md',
             '8f4ee48cbaf6c822b87dd5e30a5dfee4d596e26e'),
            ('Tmp/TOE/Einstein 6/v1172_full_stack_package/v1172_6d_gpu_full_stack_genesis_provenance_engine.py',
             '78d57450ac6a2b7fe3ab4ad42cf2f707c3e61f8d'),
        ),
        transformation_source='V997/V1172 ordered-lineage and append-only provenance certification',
        certified_relation_claims=(
            'PINNED_REGISTRY', 'GENESIS_ROOT', 'WITNESS_QUORUM', 'APPEND_ONLY_CONTINUITY'
        ),
        claim_boundary='history legitimacy is not microscopic torus incidence',
    ),
    CandidateEvidence(
        key='genesis-6d-carrier',
        domain='GENESIS_6D_PROVENANCE_CARRIER',
        evidence_keys=('v14.04-provenance-representation', 'v15.01-common-parent'),
        artifact_pins=(
            ('Tmp/TOE/Einstein 6/v1172_full_stack_package/v1172_6d_gpu_full_stack_genesis_provenance_engine.py',
             '78d57450ac6a2b7fe3ab4ad42cf2f707c3e61f8d'),
            ('ResearchHistory/UQCF-GEM/v14/v14.04/REPORT.md',
             'e5d9566bfc86c801d2933e63453d1800f60a675b'),
            ('ResearchHistory/UQCF-GEM/v14/v14.04/provenance_representation_audit.py',
             '1e75767a59a54b4fb7840ca355eb00845cf119e3'),
            ('ResearchHistory/UQCF-GEM/v15/v15.01/REPORT.md',
             '1afbb7aebe384a1fb761f99fd2b040e595be1fa5'),
            ('ResearchHistory/UQCF-GEM/v15/v15.01/common_parent_audit.py',
             'b8b6ef14b323659eb730b33bd3d36c99e7f03957'),
        ),
        transformation_source='V1172 model-specific 6-D grid/roll/pruning transformations audited by v14.04/v15.01',
        certified_relation_claims=('NONTRIVIAL_6D_CARRIER',),
        claim_boundary='nontrivial Genesis carrier has no frozen certified map to the torus q-fiber',
    ),
    CandidateEvidence(
        key='retained-source-current',
        domain='RETAINED_SOURCE_CURRENT',
        evidence_keys=('v13.26-source-calibration', 'v14.04-provenance-representation', 'v15.01-common-parent'),
        artifact_pins=(
            ('ResearchHistory/UQCF-GEM/v13/v13.26/REPORT.md',
             '9917085b211ca0e1f4737082227f55097cc72b66'),
            ('ResearchHistory/UQCF-GEM/v14/v14.04/REPORT.md',
             'e5d9566bfc86c801d2933e63453d1800f60a675b'),
            ('ResearchHistory/UQCF-GEM/v14/v14.04/provenance_representation_audit.py',
             '1e75767a59a54b4fb7840ca355eb00845cf119e3'),
            ('ResearchHistory/UQCF-GEM/v15/v15.01/REPORT.md',
             '1afbb7aebe384a1fb761f99fd2b040e595be1fa5'),
            ('ResearchHistory/UQCF-GEM/v15/v15.01/common_parent_audit.py',
             'b8b6ef14b323659eb730b33bd3d36c99e7f03957'),
        ),
        transformation_source='v13.26 retained graph balance/covariance and positive source/current scaling audited by v14.04/v15.01',
        certified_relation_claims=('RETAINED_SOURCE_GRADE', 'GRAPH_BALANCE_BJ_EQUALS_S_RET'),
        claim_boundary='retained graph source/current is a distinct carrier with no frozen certified torus-fiber relation',
    ),
    CandidateEvidence(
        key='ternary-source-role',
        domain='RECOVERABILITY_SOURCE_LEGITIMACY',
        evidence_keys=('v923-source-role',),
        artifact_pins=(
            ('Tmp/TOE/Einstein 3/v923_full_stack_source_role_closure_proof/FULL_REPORT_AND_PROOF.md',
             '9a1523c08d2b9b2c5ba2d298dfed3d563a750bec'),
            ('Tmp/TOE/Einstein 3/v923_full_stack_source_role_closure_proof/v923_full_stack_source_role_closure_proof.py',
             '90f69d5101e0ab14488d8d25da326e7b94341375'),
        ),
        transformation_source='V923 exact finite source-family partition into the minimal ternary legitimacy role',
        certified_relation_claims=(
            'SOURCE_ACTIVE_ROLE',
            'SOURCE_BASIN_ELIGIBLE_NONACTIVE_ROLE',
            'SOURCE_REJECTED_OR_BROKEN_ROLE',
        ),
        claim_boundary='ternary source legitimacy is not a torus edge label or q-fiber partition',
    ),
)


def verify_candidate(row: CandidateEvidence, repo_root: Path = REPO_ROOT) -> None:
    root = Path(repo_root)
    for relative, blob in row.artifact_pins:
        verify_blob(root / relative, blob)


def candidate_inventory(repo_root: Path = REPO_ROOT) -> tuple[CandidateEvidence, ...]:
    rows = tuple(sorted(_CANDIDATES, key=lambda row: row.key))
    if len(rows) != 4 or len({row.key for row in rows}) != 4:
        raise AssertionError('v15.30 requires exactly four unique candidate origins')
    for row in rows:
        verify_candidate(row, repo_root)
    return rows


def candidate_by_key(
    key: str, rows: tuple[CandidateEvidence, ...] | None = None
) -> CandidateEvidence:
    records = candidate_inventory(REPO_ROOT) if rows is None else rows
    hits = [row for row in records if row.key == key]
    if len(hits) != 1:
        raise KeyError(key)
    return hits[0]


def inventory_payload(rows: tuple[CandidateEvidence, ...]) -> list[dict]:
    return [asdict(row) for row in sorted(rows, key=lambda row: row.key)]


def inventory_digest(rows: tuple[CandidateEvidence, ...]) -> str:
    payload = json.dumps(
        inventory_payload(rows), sort_keys=True, separators=(',', ':'), allow_nan=False
    )
    return hashlib.sha256(payload.encode()).hexdigest()


def write_candidate_inventory(path: Path, rows: tuple[CandidateEvidence, ...]) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(inventory_payload(rows), indent=2, sort_keys=True) + '\n')


def main() -> None:
    parser = argparse.ArgumentParser(description='Verify frozen v15.30 candidate evidence.')
    parser.add_argument(
        '--out', type=Path,
        default=Path(__file__).with_name('docs') / 'CANDIDATE_EVIDENCE.json'
    )
    args = parser.parse_args()
    load_v1529()
    rows = candidate_inventory(REPO_ROOT)
    write_candidate_inventory(args.out, rows)
    print(json.dumps({
        'base_sha': V1529_BASE_SHA,
        'scientific_source_sha': SCIENTIFIC_SOURCE_SHA,
        'candidate_count': len(rows),
        'inventory_digest': inventory_digest(rows),
    }, sort_keys=True))


if __name__ == '__main__':
    main()
