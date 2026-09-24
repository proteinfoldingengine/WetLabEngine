"""Frozen v15.54 operational nonclassicality contract."""
from copy import deepcopy
from hashlib import sha1
from pathlib import Path
import json

SOURCES={
 "v1553_results":{"path":"ResearchHistory/UQCF-GEM/demos/v15.53-lawful-quantum-realization-reduction/docs/RESULTS.json","git_blob_sha":"dfe34bf7b98d708f2f706e293cd7b57d78ed2ea0"},
 "v1553_contract":{"path":"ResearchHistory/UQCF-GEM/demos/v15.53-lawful-quantum-realization-reduction/realization_contract.py","git_blob_sha":"dc40cf64f857697a24169389af0ad7c1d9b617d9"},
 "v1554_spec":{"path":"docs/superpowers/specs/2026-09-24-v1554-operational-nonclassicality-gate.md","git_blob_sha":"8e4f7fd6302da4bea50731c657cbf34d63c9e4ff"},
}
VERDICTS=("CERTIFIED_OPERATIONAL_NONCLASSICAL_OBSTRUCTION","OBSTRUCTION_PRESENT_BUT_CLASSICALLY_REPRODUCIBLE","NO_NONCLASSICAL_WITNESS_IN_FROZEN_FAMILY","FAMILY_INVALID","VERIFICATION_FAILED")
FORBIDDEN=("nonclassical","target_class","E_observables","post_result_gauge","fixture_order_selector","enumeration_index","gravity","geometry","curvature","physical_time","dark_matter")
CONTRACT={
 "schema":"uqcf-v1554-nonclassicality-contract-v1","sources":SOURCES,
 "required_v1553_verdict":"CERTIFIED_FAMILY_OBSTRUCTION_WITNESS",
 "classical_ontic_bound":4,
 "operational_witness":{"id":"CHSH_EXACT","contexts":["x0y0","x0y1","x1y0","x1y1"],"outcomes":["00","01","10","11"],"classical_bound":[2,1]},
 "primary_verdicts":VERDICTS,"forbidden_fields":FORBIDDEN,
 "source_correspondence":"NOT_EVALUATED","Pillar_3":"OPEN",
 "physical_source_law":False,"physical_gravity":False,"geometry_or_curvature":False,"continuum_limit":False,"empirical_fit":False,"fundamental_physical_time":False,"dark_matter_primitive":False,"universal_quantum_derivation":False,
}
def _blob(raw):
 return sha1(b"blob "+str(len(raw)).encode()+b"\0"+raw).hexdigest()
def verify_sources(root,contract):
 if contract.get("sources")!=SOURCES: raise ValueError("source_manifest_changed")
 for k,r in SOURCES.items():
  p=root/r["path"]
  if not p.is_file() or p.is_symlink() or _blob(p.read_bytes())!=r["git_blob_sha"]: raise ValueError("source_blob_mismatch:"+k)
 return deepcopy(SOURCES)
def load_contract(root:Path):
 c=deepcopy(CONTRACT); verify_sources(root,c)
 result=json.loads((root/SOURCES["v1553_results"]["path"]).read_text())
 if result.get("primary_verdict")!=c["required_v1553_verdict"]: raise ValueError("v1553_verdict_mismatch")
 return c
