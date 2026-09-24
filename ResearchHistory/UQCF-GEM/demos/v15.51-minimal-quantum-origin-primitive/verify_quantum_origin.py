"""v15.51 Task 4: independent insufficiency verifier."""
def verify(contract,realization_ledger,origin_ledger,minimality_ledger):
 forbidden=set(contract["forbidden_primitives"])
 for p,rs in realization_ledger.items():
  for r in rs:
   if forbidden.intersection(r): raise ValueError("forbidden_quantum_primitive")
   if set(r.get("assumptions",[]))!=set(contract["packages"][p]["assumptions"]): raise ValueError("realization_ledger")
   if r["id"].endswith("-C") and r.get("theory_class")!="CLASSICAL": raise ValueError("realization_ledger")
 for p,r in origin_ledger.items():
  if r.get("package")!=p or r.get("status")!="INSUFFICIENT": raise ValueError("origin_ledger")
  if not r.get("classical_realization_present"): raise ValueError("classical_control")
 if minimality_ledger.get("successful_packages") or minimality_ledger.get("minimal_successful_packages"):
  raise ValueError("minimality_ledger")
 if set(minimality_ledger.get("insufficient_packages",[]))!=set(contract["packages"]):
  raise ValueError("minimality_ledger")
 return {"schema":"uqcf-v1551-verification-v1","status":"VERIFIED_TESTED_PRIMITIVES_INSUFFICIENT",
         "successful_packages":[],"tested_packages":sorted(contract["packages"]),
         "source_correspondence":"NOT_EVALUATED","Pillar_3":"OPEN"}
