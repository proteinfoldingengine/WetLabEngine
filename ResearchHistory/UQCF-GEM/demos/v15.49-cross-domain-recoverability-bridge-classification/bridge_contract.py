"""v15.49 Task 1: frozen bridge typing and axiom contract."""
from hashlib import sha1
from pathlib import Path
SOURCES={
 "carrier_origin":("ResearchHistory/UQCF-GEM/v15/v15.09/REPORT.md","ec73ef9240dcef062c95a82c511a874d0d2923ef"),
 "independent_events":("ResearchHistory/UQCF-GEM/demos/v15.13-independent-events/README.md","0d65ef13285a51ba3dcd2cd023e53bdf3d578e2d"),
 "record_dependencies":("ResearchHistory/UQCF-GEM/demos/v15.14-record-dependencies/README.md","3877378a375a72c70587c98e8ff1c82d900774c5"),
 "coherent_records":("ResearchHistory/UQCF-GEM/demos/v15.15-coherent-records/README.md","a6b806406c0ac0edc8c42b44405f538f84129af6"),
}
AXIOMS=["type_preservation","covariance","composition_order","neutrality","refinement",
        "lineage_locality","disjoint_composition","gauge_respect","no_downstream_selection"]
def blob(raw): return sha1(b"blob "+str(len(raw)).encode()+b"\0"+raw).hexdigest()
def load_contract(root:Path,overrides=None):
 root=Path(root).resolve(); overrides={} if overrides is None else dict(overrides); receipts={}
 for k,(p,pin) in SOURCES.items():
  raw=overrides.get(k,(root/p).read_bytes())
  if blob(raw)!=pin: raise ValueError("source_blob_mismatch:"+k)
  receipts[k]={"path":p,"git_blob_sha":pin}
 return {
  "schema":"uqcf-v1549-bridge-contract-v1","sources":receipts,
  "domain":{"sort":"RETAINED_RECOVERABILITY","structure":["dependency","recoverability_order","lineage"]},
  "codomain":{"sort":"QUANTUM_OPERATIONAL_RECOVERABILITY","structure":["CMI","recovery_channel","subsystem_inclusion"]},
  "typing":{"status":"NO_CROSS_DOMAIN_MORPHISM_TYPE_CERTIFIED",
            "equal_cardinality_is_sufficient":False,"bridge_homset":None},
  "axioms":AXIOMS,
  "cross_domain":{"bridge":None,"node_site_dictionary":None},
  "earned_gauge":{"bridge":"NONE_CERTIFIED"},
  "prohibited_inputs":{"curvature":True,"holonomy":True,"source_response":True,"gravity":True,
                       "continuum":True,"empirical_fit":True,"physical_time":True},
  "source_correspondence":"NOT_EVALUATED","Pillar_3":"OPEN"}
