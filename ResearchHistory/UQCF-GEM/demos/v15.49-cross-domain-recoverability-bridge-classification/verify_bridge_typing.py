"""v15.49 independent verification of bridge typing obstruction."""
from pathlib import Path

MARKERS={
 "carrier_origin":("cross-domain relation      = NONE CERTIFIED",),
 "independent_events":("supplied four-qubit carrier",),
 "record_dependencies":("classical record wire remain supplied",),
 "coherent_records":("supplied diagnostic model structure",),
}
def verify(root:Path,contract:dict)->dict:
 root=Path(root).resolve()
 if contract.get("typing",{}).get("status")!="NO_CROSS_DOMAIN_MORPHISM_TYPE_CERTIFIED":
  raise ValueError("unsupported_type_promotion")
 if contract["typing"].get("bridge_homset") is not None:
  raise ValueError("unsupported_type_promotion")
 if contract["typing"].get("equal_cardinality_is_sufficient") is not False:
  raise ValueError("cardinality_coercion")
 if contract["cross_domain"].get("bridge") is not None or contract["cross_domain"].get("node_site_dictionary") is not None:
  raise ValueError("hidden_bridge")
 if not all(contract["prohibited_inputs"].values()):
  raise ValueError("downstream_firewall_open")
 checked=[]
 for key,receipt in contract["sources"].items():
  txt=(root/receipt["path"]).read_text(encoding="utf-8")
  if any(m not in txt for m in MARKERS[key]): raise ValueError("predecessor_semantics_drift:"+key)
  checked.append(key)
 return {"schema":"uqcf-v1549-typing-verification-v1",
         "status":"VERIFIED_NO_CROSS_DOMAIN_MORPHISM_TYPE",
         "sources_checked":checked,
         "bridge_enumeration_executable":False,
         "equal_cardinality_used_as_typing":False,
         "required_new_object":"CROSS_DOMAIN_HOMSET_OR_TYPED_BRIDGE_AXIOM",
         "tasks_2_and_3":"STOPPED_BY_TYPE_GATE",
         "source_correspondence":"NOT_EVALUATED","Pillar_3":"OPEN"}
