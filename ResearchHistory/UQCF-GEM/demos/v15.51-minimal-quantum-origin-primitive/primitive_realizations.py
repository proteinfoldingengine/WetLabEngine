"""v15.51 Task 2: abstract finite operational realization controls."""
def enumerate_realizations(contract,p):
 a=set(contract["packages"][p]["assumptions"])
 out=[{"id":p+"-C","theory_class":"CLASSICAL","assumptions":sorted(a),
       "interference_witness":None,"noncommutative_witness":None}]
 if "composition_with_interference" in a:
  out.append({"id":p+"-I","theory_class":"GENERALIZED_INTERFERENCE","assumptions":sorted(a),
              "interference_witness":{"paths":["a","b"],"composition":"phase_sensitive"},
              "noncommutative_witness":None})
 if "noncommutative_involutive_event_composition" in a:
  out.append({"id":p+"-N","theory_class":"NONCOMMUTATIVE_OPERATIONAL","assumptions":sorted(a),
              "interference_witness":None,
              "noncommutative_witness":{"x*y":"xy","y*x":"yx","distinct":True}})
 if "convex_operational_distinguishability" in a:
  out.append({"id":p+"-V","theory_class":"CONVEX_OPERATIONAL","assumptions":sorted(a),
              "interference_witness":None,"noncommutative_witness":None})
 return tuple(out)
def check_realization(contract,p,r):
 if any(k in r for k in contract["forbidden_primitives"]): return {"status":"FORBIDDEN_QUANTUM_PRIMITIVE"}
 if set(r.get("assumptions",[]))!=set(contract["packages"][p]["assumptions"]): return {"status":"ASSUMPTION_MISMATCH"}
 if r.get("theory_class")=="GENERALIZED_INTERFERENCE" and not r.get("interference_witness"): return {"status":"MISSING_WITNESS"}
 if r.get("theory_class")=="NONCOMMUTATIVE_OPERATIONAL" and not r.get("noncommutative_witness"): return {"status":"MISSING_WITNESS"}
 return {"status":"REALIZATION_VALID"}
