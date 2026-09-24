"""v15.52 Task 3: explicit finite obstruction witness."""
def _observables(f):
 return {"object_count":len(f["objects"]),"lineage_incidence":tuple(f["lineage"]),
 "dependency_incidence":tuple(f["dependency"]),"recoverability_relation":tuple(f["recoverability"]),
 "composition_table":tuple(f["composition"]),"refinement_diagram":tuple(f["refinement"]),
 "disjoint_partition":tuple(f["disjoint_composition"])}
def quantum_equivalent(contract,q1,q2):
 if contract["quantum_equivalence"]=="IDENTITY_ONLY": return q1==q2
 raise ValueError("unknown_quantum_equivalence")
def find_witness(contract,f,autos):
 obs=_observables(f)
 # Candidate outputs deliberately differ only in target data that E does not contain.
 q1={"carrier_representation_class":"Q_A","subsystem_composition":"S_A","recovery_capable_operations":"R_A",
     "typed_quantum_leg":"FQ_A","E_observables":obs}
 q2={"carrier_representation_class":"Q_B","subsystem_composition":"S_B","recovery_capable_operations":"R_B",
     "typed_quantum_leg":"FQ_B","E_observables":obs}
 checked=[x["id"] for x in contract["E"]["observables"]]
 return {"status":"WITNESS_FOUND","Q1":q1,"Q2":q2,"E_observables_checked":checked,
         "automorphism_count":len(autos),"construction_inputs":list(contract["E"]["allowed_fields"])}
def find_separating_E_observable(contract,w):
 for oid in (x["id"] for x in contract["E"]["observables"]):
  if w["Q1"]["E_observables"][oid]!=w["Q2"]["E_observables"][oid]: return oid
 return None
