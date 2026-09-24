"""v15.46 Stage B: static fail-closed trace of one supplied joint-state record.

This does not execute the historical demo or infer missing subsystem/incidence data.
It verifies the pinned source bytes and stops at the first unearned native interface.
"""
from __future__ import annotations
from hashlib import sha1
import json
from pathlib import Path

SOURCE_PATH = "ResearchHistory/UQCF-GEM/demos/v13.27-gravity-progress/uqcf_demo/quantum.py"
SOURCE_BLOB = "bf0b84e3b3e627d7916a5fb1b46ab9bd5eba03e6"


def git_blob(raw: bytes) -> str:
    return sha1(b"blob " + str(len(raw)).encode() + b"\0" + raw).hexdigest()


def canonical_bytes(value) -> bytes:
    return (json.dumps(value, sort_keys=True, separators=(",", ":"),
                       ensure_ascii=True, allow_nan=False) + "\n").encode("ascii")


def _verify_source_semantics(raw: bytes) -> None:
    try:
        text = raw.decode("utf-8")
    except UnicodeError as exc:
        raise ValueError("candidate_not_utf8") from exc
    required = (
        "def build_default_model(n=6, beta=0.72, source_scale=1.0):",
        "rho0 = hermitian_exp_normalized(-beta * H)",
        '"rho0": rho0',
        '"P": P',
        '"source_nodes": (0, 3)',
        "def pair_reduction(rho, i, j, n):",
        'raise ValueError("default demo is frozen at n=6")',
    )
    if any(token not in text for token in required):
        raise ValueError("candidate_semantics_drift")


def trace_candidate(root: Path, *, source_bytes: bytes | None = None) -> dict:
    root = Path(root).resolve()
    path = root / SOURCE_PATH
    raw = path.read_bytes() if source_bytes is None else source_bytes
    actual = git_blob(raw)
    if actual != SOURCE_BLOB:
        raise ValueError("candidate_blob_mismatch")
    _verify_source_semantics(raw)

    not_run = {"status": "NOT_EXECUTED_AFTER_FIRST_FAILURE"}
    return {
        "schema": "uqcf-v1546-native-record-trace-v1",
        "scope": "STATIC_PINNED_RECORD_TRACE_NOT_SOURCE_ADMISSION",
        "candidate": "V13_27_SIX_QUBIT_THERMAL_DEMO",
        "selection_rationale": (
            "STRONGEST_SCOPED_EXISTING_CANDIDATE_WITH_EXPLICIT_JOINT_STATE_GRAPH_AND_SOURCE_OPERATOR"
        ),
        "source": {
            "path": SOURCE_PATH,
            "git_blob_sha": actual,
            "executed": False,
        },
        "stages": {
            "joint_state_provenance": {
                "status": "FAILED_NATIVE_PROVENANCE",
                "joint_state_constructed": True,
                "construction": "NORMALIZED_EXP_MINUS_BETA_H",
                "model_scope": "FROZEN_SIX_QUBIT_DEMO",
                "provenance": "SUPPLIED_DEMO_MODEL",
                "native_derivation_certified": False,
                "reason": (
                    "SOURCE_FILE_CONSTRUCTS_A_DECLARED_DEMO_STATE_BUT_CONTAINS_NO_DERIVATION_"
                    "FROM_PRIMITIVE_RETAINED_RECORDS"
                ),
            },
            "overlap_inclusions": dict(not_run),
            "support_domain": dict(not_run),
            "occurrence_link": dict(not_run),
            "coupling_law": dict(not_run),
        },
        "status": "SUPPLIED_JOINT_STATE_PRESENT_NATIVE_PROVENANCE_UNESTABLISHED",
        "first_unmet_stage": "B1_NATIVE_JOINT_STATE_PROVENANCE",
        "interface_admitted": False,
        "later_stages": "NOT_EXECUTED_AFTER_FIRST_FAILURE",
        "source_value": "NOT_EVALUATED",
        "claims": {
            "source_correspondence": "NOT_EVALUATED",
            "physical_source_law_adopted": False,
            "physical_gravity": False,
            "full_v1546_certification": False,
            "archive_absence_proved": False,
            "Pillar_3": "OPEN",
        },
    }
