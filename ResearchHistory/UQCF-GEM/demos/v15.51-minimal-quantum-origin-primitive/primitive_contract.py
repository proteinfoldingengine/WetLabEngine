"""v15.51 Task 1: frozen primitive assumption lattice and output contract."""
from hashlib import sha1
from pathlib import Path
SOURCES={
 "v1550_result":("ResearchHistory/UQCF-GEM/demos/v15.50-common-ancestor-universal-object/docs/RESULTS.json","b3609e90b56f3d19b5936bdd5f2532a2cf9c5ba7"),
 "v1550_U":("ResearchHistory/UQCF-GEM/demos/v15.50-common-ancestor-universal-object/common_contract.py","3dada32767cad81dbf02dd78107e8ede7f89fca7"),
 "v1549_result":("ResearchHistory/UQCF-GEM/demos/v15.49-cross-domain-recoverability-bridge-classification/docs/RESULTS.json","bece64b16df9f003714565c6e0dce50e6919606d"),
}
FORBIDDEN=["hilbert_space","matrix_algebra","qubit","born_rule","density_operator","CPTP_map","target_dimension","tensor_factor"]
PACKAGES={
 "P0":[],
 "P1":["composition_with_interference"],
 "P2":["convex_operational_distinguishability"],
 "P3":["noncommutative_involutive_event_composition"],
 "P12":["composition_with_interference","convex_operational_distinguishability"],
 "P13":["composition_with_interference","noncommutative_involutive_event_composition"],
 "P23":["convex_operational_distinguishability","noncommutative_involutive_event_composition"],
 "P123":["composition_with_interference","convex_operational_distinguishability","noncommutative_involutive_event_composition"],
 "P4":["composition_with_interference","convex_operational_distinguishability","noncommutative_involutive_event_composition","purification","local_tomography"],
}
def blob(raw): return sha1(b"blob "+str(len(raw)).encode()+b"\0"+raw).hexdigest()
def load_contract(root:Path,overrides=None):
 root=Path(root).resolve(); overrides={} if overrides is None else dict(overrides); receipts={}
 for k,(p,pin) in SOURCES.items():
  raw=overrides.get(k,(root/p).read_bytes())
  if blob(raw)!=pin: raise ValueError("source_blob_mismatch:"+k)
  receipts[k]={"path":p,"git_blob_sha":pin}
 subs={}
 sets={k:set(v) for k,v in PACKAGES.items()}
 for k,s in sets.items(): subs[k]=sorted(j for j,t in sets.items() if j!=k and t<s)
 return {"schema":"uqcf-v1551-primitive-contract-v1","sources":receipts,
  "baseline":"v15.50_ORDERED_RECOVERABILITY_INCIDENCE",
  "packages":{k:{"assumptions":v} for k,v in PACKAGES.items()},
  "strict_subpackages":subs,
  "required_outputs":["carrier_representation_class","subsystem_composition","recovery_capable_operations","typed_quantum_leg"],
  "forbidden_primitives":FORBIDDEN,
  "prohibited_inputs":{"curvature":True,"geometry":True,"source_response":True,"gravity":True,"continuum":True,"empirical_fit":True,"physical_time":True},
  "source_correspondence":"NOT_EVALUATED","Pillar_3":"OPEN"}
