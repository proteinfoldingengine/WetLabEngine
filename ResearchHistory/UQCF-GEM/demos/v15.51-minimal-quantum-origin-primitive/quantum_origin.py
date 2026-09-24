"""v15.51 Task 3: quantum-origin output classification."""
def derive_outputs(contract,p,realizations):
 required=list(contract["required_outputs"])
 classical=any(r.get("theory_class")=="CLASSICAL" for r in realizations)
 assumptions=set(contract["packages"][p]["assumptions"])
 # None of the frozen packages derives a carrier/representation class or typed
 # quantum leg without adding a representation principle forbidden as primitive.
 derived=[]
 if "convex_operational_distinguishability" in assumptions: derived.append("recovery_capable_operations")
 if "local_tomography" in assumptions: derived.append("subsystem_composition")
 missing=[x for x in required if x not in derived]
 status="INSUFFICIENT" if missing else ("SUFFICIENT_NONUNIQUE" if classical else "SUFFICIENT_UNIQUE")
 return {"schema":"uqcf-v1551-origin-package-v1","package":p,"status":status,
         "derived_outputs":derived,"missing_outputs":missing,
         "classical_realization_present":classical,
         "representation_classes":sorted(set(r["theory_class"] for r in realizations)),
         "source_correspondence":"NOT_EVALUATED","Pillar_3":"OPEN"}
def classify_representations(contract,results):
 return {"sufficient_packages":sorted(p for p,r in results.items() if r["status"]!="INSUFFICIENT"),
         "insufficient_packages":sorted(p for p,r in results.items() if r["status"]=="INSUFFICIENT")}
