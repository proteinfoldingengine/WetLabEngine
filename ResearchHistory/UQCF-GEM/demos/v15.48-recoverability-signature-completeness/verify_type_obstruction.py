"""v15.48 independent verification of the recoverability-signature type obstruction."""
from pathlib import Path

REQUIRED_MARKERS={
 "carrier_origin":(
   "cross-domain relation      = NONE CERTIFIED",
   "CANONICAL_NEUTRAL_STRUCTURE_DOES_NOT_DERIVE_RETAINED_QUANTUM_CARRIER",
 ),
 "independent_events":(
   "supplied four-qubit carrier",
 ),
 "record_dependencies":(
   "carrier,",
   "classical record wire remain supplied",
 ),
 "coherent_records":(
   "supplied diagnostic model structure",
 ),
}

FORBIDDEN_BRIDGE_MARKERS=(
 "retained recoverability relation = quantum recovery",
 "retained recoverability = conditional mutual information",
 "lineage address = quantum subsystem",
)

def verify(root:Path,contract:dict)->dict:
    root=Path(root).resolve()
    if contract.get("type_audit",{}).get("status")!="NO_COMMON_TYPE_CERTIFIED":
        raise ValueError("unsupported_type_promotion")
    if contract.get("type_audit",{}).get("equality_relation") is not None:
        raise ValueError("unsupported_type_promotion")
    if contract.get("cross_domain",{}).get("node_site_dictionary") is not None:
        raise ValueError("hidden_dictionary")
    if not all(contract.get("prohibited_inputs",{}).values()):
        raise ValueError("downstream_firewall_open")

    checked=[]
    for key,receipt in contract["sources"].items():
        text=(root/receipt["path"]).read_text(encoding="utf-8")
        markers=REQUIRED_MARKERS.get(key,())
        if any(m not in text for m in markers):
            raise ValueError("predecessor_semantics_drift:"+key)
        if any(m in text.lower() for m in FORBIDDEN_BRIDGE_MARKERS):
            raise ValueError("unexpected_certified_cross_domain_bridge:"+key)
        checked.append(key)

    return {
      "schema":"uqcf-v1548-type-obstruction-verification-v1",
      "status":"VERIFIED_NO_COMMON_TYPE_CERTIFIED",
      "sources_checked":checked,
      "retained_coordinates":list(contract["retained_signature_schema"]),
      "quantum_coordinates":list(contract["quantum_signature_schema"]),
      "comparison_executable":False,
      "hidden_dictionary_found":False,
      "downstream_selector_permitted":False,
      "required_new_axiom":"CROSS_DOMAIN_RECOVERABILITY_EQUALITY_OR_FUNCTOR",
      "tasks_2_and_3":"STOPPED_BY_PREREGISTERED_TYPE_GATE",
      "source_correspondence":"NOT_EVALUATED",
      "Pillar_3":"OPEN",
    }
