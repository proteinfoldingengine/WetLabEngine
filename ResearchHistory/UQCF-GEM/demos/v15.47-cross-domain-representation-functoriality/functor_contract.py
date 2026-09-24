"""v15.47 Task 1: frozen finite source/target category contract."""
from hashlib import sha1
from pathlib import Path

SOURCES={
 "carrier_origin":("ResearchHistory/UQCF-GEM/v15/v15.09/REPORT.md","ec73ef9240dcef062c95a82c511a874d0d2923ef"),
 "independent_events":("ResearchHistory/UQCF-GEM/demos/v15.13-independent-events/README.md","0d65ef13285a51ba3dcd2cd023e53bdf3d578e2d"),
 "record_dependencies":("ResearchHistory/UQCF-GEM/demos/v15.14-record-dependencies/README.md","3877378a375a72c70587c98e8ff1c82d900774c5"),
 "partial_pruning":("ResearchHistory/UQCF-GEM/demos/v15.16-partial-pruning/README.md","982e54d04286eb365e6ee624879b882f3cdf281a"),
}
def _blob(raw): return sha1(b"blob "+str(len(raw)).encode()+b"\0"+raw).hexdigest()

def load_contract(root:Path,overrides=None):
 root=Path(root).resolve(); overrides={} if overrides is None else dict(overrides)
 receipts={}
 for key,(path,pin) in SOURCES.items():
  raw=overrides.get(key,(root/path).read_bytes())
  if _blob(raw)!=pin: raise ValueError("source_blob_mismatch:"+key)
  receipts[key]={"path":path,"git_blob_sha":pin}
 # This finite category is a NEW-ASSUMPTION test fixture: its arrows are declared
 # abstractly and are not claimed to have been derived from these reports.
 objects=["R0","R1","R2","R3"]
 morphisms=["id","a","b","ba","c","d","dc"]
 composition=[["a","b","ba"],["c","d","dc"]]
 square={"left_path":["a","b"],"right_path":["c","d"],
         "left_composite":"q","right_composite":"q","common_composite":"q"}
 return {
  "schema":"uqcf-v1547-functor-contract-v1",
  "new_assumption":"RETAINED_TO_QUANTUM_FUNCTORIALITY",
  "sources":receipts,
  "source_category":{"objects":objects,"morphisms":morphisms,
                     "composition":composition,"refinement_square":square},
  "target_category":{"equivalence":"IDENTITY_ONLY","allowed_dimensions":[32,125]},
  "cross_domain":{"node_site_dictionary":None},
  "prohibited_inputs":{"curvature":True,"gravity":True,"source_response":True,
                       "entropy":True,"spectral_edge":True,"physical_time":True},
  "source_correspondence":"NOT_EVALUATED","Pillar_3":"OPEN"
 }
