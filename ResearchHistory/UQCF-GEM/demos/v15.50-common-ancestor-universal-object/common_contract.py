"""v15.50 Task 1: target-blind common-ancestor contract."""
from hashlib import sha1
from pathlib import Path
SOURCES={
 "carrier_origin":("ResearchHistory/UQCF-GEM/v15/v15.09/REPORT.md","ec73ef9240dcef062c95a82c511a874d0d2923ef"),
 "independent_events":("ResearchHistory/UQCF-GEM/demos/v15.13-independent-events/README.md","0d65ef13285a51ba3dcd2cd023e53bdf3d578e2d"),
 "record_dependencies":("ResearchHistory/UQCF-GEM/demos/v15.14-record-dependencies/README.md","3877378a375a72c70587c98e8ff1c82d900774c5"),
 "partial_pruning":("ResearchHistory/UQCF-GEM/demos/v15.16-partial-pruning/README.md","982e54d04286eb365e6ee624879b882f3cdf281a"),
}
def blob(raw): return sha1(b"blob "+str(len(raw)).encode()+b"\0"+raw).hexdigest()
def load_contract(root:Path,overrides=None):
 root=Path(root).resolve(); overrides={} if overrides is None else dict(overrides); receipts={}
 for k,(p,pin) in SOURCES.items():
  raw=overrides.get(k,(root/p).read_bytes())
  if blob(raw)!=pin: raise ValueError("source_blob_mismatch:"+k)
  receipts[k]={"path":p,"git_blob_sha":pin}
 return {
  "schema":"uqcf-v1550-common-contract-v1","sources":receipts,
  "U":{"sort":"ORDERED_RECOVERABILITY_INCIDENCE",
       "objects":["o0","o1","o2","o3"],
       "relations":["lineage","dependency","recoverability"],
       "composition":[["a","b","ba"]],
       "refinement":{"left_path":["a","b"],"right_path":["c","d"],"common":"q"},
       "disjoint_composition":[["o0","o2"],["o1","o3"]]},
  "targets":{"retained":{"sort":"RETAINED_RECOVERABILITY"},
             "quantum":{"sort":"QUANTUM_OPERATIONAL_RECOVERABILITY"}},
  "legs":{"F_R":None,"F_Q":None},
  "earned_gauge":{"U_automorphism":"NONE_CERTIFIED","target":"NONE_CERTIFIED"},
  "forbidden":{"pair_object":True,"target_labels_in_U":True,"lookup_quantum_leg":True},
  "prohibited_inputs":{"geometry":True,"curvature":True,"source_response":True,"gravity":True,
                       "entropy_selector":True,"physical_time":True,"empirical_fit":True},
  "source_correspondence":"NOT_EVALUATED","Pillar_3":"OPEN"}
