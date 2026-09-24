"""v15.50 Task 3: independent legs from target-blind U."""
def derive_retained_leg(contract,u):
 required={"lineage","dependency","recoverability"}
 if not required.issubset(set(u["relations"])): raise ValueError("retained_structure_missing")
 return {"status":"RETAINED_LEG_DERIVED","target":"RETAINED_RECOVERABILITY",
         "object_map":{o:o for o in u["objects"]},"preserves_composition":bool(u["composition"]),
         "preserves_refinement":bool(u["refinement"]),"uses_quantum_target":False}

def derive_quantum_legs(contract,u):
 # U has incidence/order data but no independently earned quantum carrier,
 # subsystem factorization, channel extraction, or cross-domain Hom-set.
 return {"status":"QUANTUM_LEG_UNDERDETERMINED","lawful_legs":[],
         "missing_information":["quantum_carrier","quantum_subsystem_structure",
                                "quantum_recovery_channel_extraction","cross_domain_morphism_type"],
         "lookup_table_used":False,"uses_retained_leg_inverse":False}

def classify_factorizations(contract,u,fr,fq):
 if fr.get("status")!="RETAINED_LEG_DERIVED": raise ValueError("retained_leg_failure")
 if fq.get("status")=="QUANTUM_LEG_UNDERDETERMINED" and not fq.get("lawful_legs"):
  return {"status":"COMMON_ANCESTOR_INSUFFICIENT_EVIDENCE",
          "reason":"U_DOES_NOT_ORIGINATE_QUANTUM_LEG",
          "retained_leg":"DERIVED","quantum_leg":"UNDERDETERMINED",
          "source_correspondence":"NOT_EVALUATED","Pillar_3":"OPEN"}
 raise ValueError("unclassified_factorization_state")
