"""Stage C1: hash-pinned primitive representation contract."""
from __future__ import annotations
from hashlib import sha1
from pathlib import Path

SOURCES={
 "carrier_origin":("ResearchHistory/UQCF-GEM/v15/v15.09/REPORT.md","ec73ef9240dcef062c95a82c511a874d0d2923ef"),
 "coherent_records":("ResearchHistory/UQCF-GEM/demos/v15.15-coherent-records/README.md","a6b806406c0ac0edc8c42b44405f538f84129af6"),
 "partial_pruning":("ResearchHistory/UQCF-GEM/demos/v15.16-partial-pruning/README.md","982e54d04286eb365e6ee624879b882f3cdf281a"),
}
def blob(raw):
 return sha1(b"blob "+str(len(raw)).encode()+b"\0"+raw).hexdigest()

def load_contract(root:Path,overrides=None):
 root=Path(root).resolve(); overrides={} if overrides is None else dict(overrides)
 receipts={}
 texts={}
 for key,(path,pin) in SOURCES.items():
  raw=overrides.get(key,(root/path).read_bytes())
  if blob(raw)!=pin: raise ValueError("source_blob_mismatch:"+key)
  texts[key]=raw.decode("utf-8"); receipts[key]={"path":path,"git_blob_sha":pin}
 if "cross-domain relation      = NONE CERTIFIED" not in texts["carrier_origin"]:
  raise ValueError("carrier_origin_semantics_drift")
 if "supplied diagnostic model structure" not in texts["coherent_records"]:
  raise ValueError("coherent_semantics_drift")
 if "Masks are supplied alternative reductions" not in texts["partial_pruning"]:
  raise ValueError("pruning_semantics_drift")
 return {
  "schema":"uqcf-v1546-stage-c-contract-v1",
  "sources":receipts,
  "retained_sort":{"status":"FROZEN_PREDECESSOR_STRUCTURE"},
  "quantum_sort":{"carrier_origin":"NOT_DERIVED","factorization_selector":"NONE_CERTIFIED",
                  "joint_state_selector":"NONE_CERTIFIED"},
  "cross_domain_relations":[],
  "earned_gauge":{"node_site":"NONE_CERTIFIED"},
  "constraints":["NO_UNEARNED_CROSS_DOMAIN_MAP","NO_DOWNSTREAM_SELECTOR",
                 "PRESERVE_CARRIER_DIMENSION_TYPES"],
  "admissible_inputs":{"v15_39_incidence_source":False,
                       "v15_43_to_v15_45_geometry":False},
  "source_correspondence":"NOT_EVALUATED","Pillar_3":"OPEN"
 }
