"""v15.52 Task 1: frozen obstruction theorem contract."""
from hashlib import sha1
from pathlib import Path
SOURCES={
 "v1551_result":("ResearchHistory/UQCF-GEM/demos/v15.51-minimal-quantum-origin-primitive/docs/RESULTS.json","e52c2d1e8330d6699f84b293ec456b375f7fc7d0"),
 "v1550_U":("ResearchHistory/UQCF-GEM/demos/v15.50-common-ancestor-universal-object/common_contract.py","3dada32767cad81dbf02dd78107e8ede7f89fca7"),
 "v1546_stage_c":("ResearchHistory/UQCF-GEM/demos/v15.46-primitive-joint-source-admissibility/docs/STAGE_C_RESULTS.json","30e0b10c9317f81c7f7627a15919148a31583c73"),
}
ALLOWED=["objects","lineage","dependency","recoverability","composition","refinement","disjoint_composition"]
FORBIDDEN=["target_labels","target_dimension","hilbert_space","matrix_algebra","node_site_dictionary","quantum_leg","fixture_order_selector"]
OBS=[{"id":x,"source_definable":True} for x in ("object_count","lineage_incidence","dependency_incidence","recoverability_relation","composition_table","refinement_diagram","disjoint_partition")]
def blob(raw): return sha1(b"blob "+str(len(raw)).encode()+b"\0"+raw).hexdigest()
def load_contract(root:Path,overrides=None):
 root=Path(root).resolve(); overrides={} if overrides is None else dict(overrides); receipts={}
 for k,(p,pin) in SOURCES.items():
  raw=overrides.get(k,(root/p).read_bytes())
  if blob(raw)!=pin: raise ValueError("source_blob_mismatch:"+k)
  receipts[k]={"path":p,"git_blob_sha":pin}
 return {"schema":"uqcf-v1552-obstruction-contract-v1","sources":receipts,
  "E":{"allowed_fields":ALLOWED,"observables":OBS,"automorphism_requirement":"COMPLETE_FINITE_ACTION"},
  "quantum_equivalence":"IDENTITY_ONLY",
  "theorems":["T1_INVARIANCE_OBSTRUCTION","T2_REPRESENTATION_ORIGIN_COROLLARY","T3_NECESSARY_NEW_DATUM"],
  "forbidden_fields":FORBIDDEN,
  "prohibited_inputs":{"geometry":True,"curvature":True,"source_response":True,"gravity":True,"continuum":True,"empirical_fit":True,"physical_time":True},
  "source_correspondence":"NOT_EVALUATED","Pillar_3":"OPEN"}
