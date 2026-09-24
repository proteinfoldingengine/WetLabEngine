"""v15.53 Task 1: frozen lawful-realization certification contract."""
from copy import deepcopy
from hashlib import sha1
from pathlib import Path

SOURCES = {
    "v1546_stage_c": {
        "path": "ResearchHistory/UQCF-GEM/demos/v15.46-primitive-joint-source-admissibility/docs/STAGE_C_RESULTS.json",
        "git_blob_sha": "30e0b10c9317f81c7f7627a15919148a31583c73",
    },
    "v1551_results": {
        "path": "ResearchHistory/UQCF-GEM/demos/v15.51-minimal-quantum-origin-primitive/docs/RESULTS.json",
        "git_blob_sha": "e52c2d1e8330d6699f84b293ec456b375f7fc7d0",
    },
    "v1552_verification": {
        "path": "ResearchHistory/UQCF-GEM/demos/v15.52-quantum-origin-invariance-obstruction/docs/VERIFICATION.json",
        "git_blob_sha": "670b881a0d7db1da784caa6ec522dc4fd4465949",
    },
    "v1552_spec": {
        "path": "docs/superpowers/specs/2026-09-23-v1552-quantum-origin-invariance-obstruction.md",
        "git_blob_sha": "e85d252189a23fbfdd6e347e1ad605dd657ae59b",
    },
}
RETAINED_OBSERVABLES = (
    "object_count", "lineage_incidence", "dependency_incidence",
    "recoverability_relation", "composition_table", "refinement_diagram",
    "disjoint_partition",
)
PRIMARY_VERDICTS = (
    "CERTIFIED_FAMILY_OBSTRUCTION_WITNESS",
    "NO_WITNESS_IN_FROZEN_FAMILY",
    "FAMILY_INVALID",
    "VERIFICATION_FAILED",
)
FORBIDDEN_FIELDS = (
    "target_class", "E_observables", "node_site_dictionary",
    "fixture_order_selector", "post_result_gauge", "enumeration_index",
    "geometry", "curvature", "gravity", "continuum", "empirical_fit",
    "physical_time", "dark_matter",
)

_CONTRACT = {
    "schema": "uqcf-v1553-realization-contract-v1",
    "sources": SOURCES,
    "retained_observables": RETAINED_OBSERVABLES,
    "primary_verdicts": PRIMARY_VERDICTS,
    "forbidden_fields": FORBIDDEN_FIELDS,
    "equivalence_frozen_before_enumeration": True,
    "reduction_target_blind": True,
    "independent_semantic_verification_required": True,
    "source_correspondence": "NOT_EVALUATED",
    "Pillar_3": "OPEN",
    "physical_source_law": False,
    "geometry_or_curvature": False,
    "continuum_limit": False,
    "empirical_fit": False,
    "fundamental_physical_time": False,
    "dark_matter_primitive": False,
}

def load_contract(root: Path) -> dict:
    """Return an isolated copy after verifying every pinned predecessor blob."""
    contract = deepcopy(_CONTRACT)
    verify_sources(root, contract)
    return contract

def _git_blob_sha(raw: bytes) -> str:
    header = b"blob " + str(len(raw)).encode("ascii") + b"\0"
    return sha1(header + raw).hexdigest()

def verify_sources(root: Path, contract: dict) -> dict:
    sources = contract.get("sources")
    if not isinstance(sources, dict) or sources != SOURCES:
        raise ValueError("source_manifest_changed")
    for key, record in sources.items():
        if set(record) != {"path", "git_blob_sha"}:
            raise ValueError("source_record_schema:" + key)
        path = root / record["path"]
        if not path.is_file() or path.is_symlink():
            raise ValueError("source_missing_or_unsafe:" + key)
        if _git_blob_sha(path.read_bytes()) != record["git_blob_sha"]:
            raise ValueError("source_blob_mismatch:" + key)
    return deepcopy(sources)
