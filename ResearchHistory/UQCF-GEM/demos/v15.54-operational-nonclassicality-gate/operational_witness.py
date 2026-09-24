"""Exact CHSH witness over registered operational probabilities only."""
from fractions import Fraction

def _q(v):
 if not isinstance(v,list) or len(v)!=2 or type(v[0]) is not int or type(v[1]) is not int or v[1]<=0: raise ValueError("invalid_probability")
 q=Fraction(v[0],v[1])
 if q<0:return q
 return q

def evaluate_witness(contract,candidate):
 w=contract["operational_witness"]; table=candidate.get("operational_table")
 if not isinstance(table,dict) or set(table)!=set(w["contexts"]): raise ValueError("operational_context_domain")
 E=[]
 for c in w["contexts"]:
  row=table[c]
  if set(row)!=set(w["outcomes"]): raise ValueError("operational_outcome_domain")
  probs={o:_q(row[o]) for o in w["outcomes"]}
  if any(q<0 for q in probs.values()) or sum(probs.values(),Fraction())!=1: raise ValueError("invalid_probability_table")
  E.append(probs["00"]+probs["11"]-probs["01"]-probs["10"])
 score=E[0]+E[1]+E[2]-E[3]
 bound=Fraction(*w["classical_bound"])
 return {"witness_id":w["id"],"score":[score.numerator,score.denominator],"bound":[bound.numerator,bound.denominator],"passes":abs(score)>bound}
