"""v15.46 Stage B2: bounded, pinned search for a primitive-derived joint record.

This is a finite declared-source audit, not an archive-wide absence theorem.
It reads source bytes and checks frozen semantic markers; it executes no historical model.
"""
from __future__ import annotations
from hashlib import sha1
import json
from pathlib import Path

SOURCES = (
    ("coherent_records","ResearchHistory/UQCF-GEM/demos/v15.15-coherent-records/README.md",
     "a6b806406c0ac0edc8c42b44405f538f84129af6",
     "JOINT_STATE_PRESENT","SUPPLIED_DIAGNOSTIC_STRUCTURE",
     ("Registers begin in a supplied\nblank state","supplied diagnostic model structure")),
    ("partial_pruning","ResearchHistory/UQCF-GEM/demos/v15.16-partial-pruning/README.md",
     "982e54d04286eb365e6ee624879b882f3cdf281a",
     "INHERITED_JOINT_ENCODING","SUPPLIED_REDUCTION_CHOICE",
     ("The v15.15 dynamics and coherent encoding are unchanged","Masks are supplied alternative reductions")),
    ("independent_events","ResearchHistory/UQCF-GEM/demos/v15.13-independent-events/README.md",
     "0d65ef13285a51ba3dcd2cd023e53bdf3d578e2d",
     "SUPPLIED_JOINT_EVENT_STATE","SUPPLIED_EVENT_RECORD_MODEL",
     ("on a supplied four-qubit carrier","sixteen supplied four-bit outcome assignments")),
    ("record_dependencies","ResearchHistory/UQCF-GEM/demos/v15.14-record-dependencies/README.md",
     "3877378a375a72c70587c98e8ff1c82d900774c5",
     "SUPPLIED_JOINT_EVENT_STATE","SUPPLIED_EVENT_RECORD_MODEL",
     ("sixteen supplied record assignments","carrier, RAS, RCR, motion generators and classical record wire remain supplied")),
    ("carrier_origin","ResearchHistory/UQCF-GEM/v15/v15.09/REPORT.md",
     "ec73ef9240dcef062c95a82c511a874d0d2923ef",
     "NO_NATIVE_CARRIER_DERIVATION","FROZEN_NEGATIVE_GATE",
     ("CANONICAL_NEUTRAL_STRUCTURE_DOES_NOT_DERIVE_RETAINED_QUANTUM_CARRIER",
      "cross-domain relation      = NONE CERTIFIED")),
)


def git_blob(raw: bytes) -> str:
    return sha1(b"blob "+str(len(raw)).encode()+b"\0"+raw).hexdigest()


def canonical_bytes(value) -> bytes:
    return (json.dumps(value,sort_keys=True,separators=(",",":"),
                       ensure_ascii=True,allow_nan=False)+"\n").encode("ascii")


def audit_scope(root: Path, *, overrides: dict[str,bytes] | None=None) -> dict:
    root=Path(root).resolve()
    overrides={} if overrides is None else dict(overrides)
    known={x[0] for x in SOURCES}
    if not set(overrides)<=known:
        raise ValueError("unknown_override")
    artifacts=[]
    by_key={}
    for key,path,expected,joint_status,provenance,markers in SOURCES:
        raw=overrides.get(key,(root/path).read_bytes())
        if git_blob(raw)!=expected:
            raise ValueError("source_blob_mismatch:"+key)
        try:
            text=raw.decode("utf-8")
        except UnicodeError as exc:
            raise ValueError("source_not_utf8:"+key) from exc
        if any(marker not in text for marker in markers):
            raise ValueError("source_semantics_drift:"+key)
        item={"key":key,"path":path,"git_blob_sha":expected,
              "joint_state_status":joint_status,"provenance_status":provenance,
              "native_derived":False}
        artifacts.append(item)
        by_key[key]=item
    return {
        "schema":"uqcf-v1546-native-record-search-v1",
        "scope":"DECLARED_FIVE_ARTIFACT_NATIVE_RECORD_SEARCH_NOT_ARCHIVE_WIDE",
        "status":"NO_NATIVE_DERIVED_JOINT_RECORD_FOUND_IN_DECLARED_SCOPE",
        "computed":{"artifacts_checked":len(artifacts)},
        "artifacts":artifacts,
        "by_key":by_key,
        "qualified_native_joint_records":[],
        "archive_absence_proved":False,
        "geometry_executed":False,
        "physical_source_law_adopted":False,
        "source_correspondence":"NOT_EVALUATED",
        "Pillar_3":"OPEN",
        "next_dependency":"NEW_PRIMITIVE_DERIVATION_OR_EXPLICIT_NEW_SOURCE_INTERFACE_ASSUMPTION",
    }
