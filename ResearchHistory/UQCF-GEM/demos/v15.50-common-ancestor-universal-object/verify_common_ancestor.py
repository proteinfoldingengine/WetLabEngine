"""v15.50 Task 4: independent common-ancestor insufficiency verifier."""
def verify(contract,u,fr,fq):
 if any(k in u for k in ("quantum_labels","node_site_dictionary","hilbert_dimension","geometry","curvature","source_response")):
  raise ValueError("target_contamination")
 if u.get("pair_object"): raise ValueError("pair_object")
 if fr.get("status")!="RETAINED_LEG_DERIVED" or not fr.get("preserves_composition") or not fr.get("preserves_refinement") or fr.get("uses_quantum_target"):
  raise ValueError("retained_leg")
 if fq.get("lookup_table_used") or fq.get("uses_retained_leg_inverse"): raise ValueError("lookup_quantum_leg")
 if fq.get("lawful_legs"): raise ValueError("unearned_quantum_leg")
 required={"quantum_carrier","quantum_subsystem_structure","quantum_recovery_channel_extraction","cross_domain_morphism_type"}
 if fq.get("status")!="QUANTUM_LEG_UNDERDETERMINED" or not required.issubset(set(fq.get("missing_information",[]))):
  raise ValueError("quantum_leg_accounting")
 if not all(contract["prohibited_inputs"].values()): raise ValueError("downstream_firewall")
 return {"schema":"uqcf-v1550-verification-v1",
         "status":"VERIFIED_COMMON_ANCESTOR_INSUFFICIENT",
         "U_target_blind":True,"retained_leg_lawful":True,"quantum_leg_derivable":False,
         "missing_quantum_information":sorted(required),
         "source_correspondence":"NOT_EVALUATED","Pillar_3":"OPEN"}
