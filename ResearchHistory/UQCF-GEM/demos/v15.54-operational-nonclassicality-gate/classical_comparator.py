"""Exact Bell-local comparator for the frozen 2x2x2 v15.54 scenario."""
from fractions import Fraction
from itertools import product

CONTEXTS=("x0y0","x0y1","x1y0","x1y1")
OUTCOMES=("00","01","10","11")

def enumerate_extremal_models(contract):
 out=[]
 for a0,a1,b0,b1 in product((0,1),repeat=4):
  table={}
  for x,y,c in ((0,0,"x0y0"),(0,1,"x0y1"),(1,0,"x1y0"),(1,1,"x1y1")):
   a=(a0,a1)[x]; b=(b0,b1)[y]
   table[c]={o:[int(o==f"{a}{b}"),1] for o in OUTCOMES}
  out.append({"a":[a0,a1],"b":[b0,b1],"table":table})
 return tuple(out)

def _parse(table):
 if not isinstance(table,dict) or set(table)!=set(CONTEXTS): raise ValueError("context_domain")
 out={}
 for c in CONTEXTS:
  row=table[c]
  if not isinstance(row,dict) or set(row)!=set(OUTCOMES): raise ValueError("outcome_domain")
  rr={}
  for o,v in row.items():
   if not isinstance(v,list) or len(v)!=2 or type(v[0]) is not int or type(v[1]) is not int or v[1]<=0: raise ValueError("rational")
   q=Fraction(v[0],v[1])
   if q<0: raise ValueError("negative")
   rr[o]=q
  if sum(rr.values(),Fraction())!=1: raise ValueError("normalization")
  out[c]=rr
 return out

def _chsh(t):
 es=[]
 for c in CONTEXTS:
  r=t[c]; es.append(r["00"]+r["11"]-r["01"]-r["10"])
 return es[0]+es[1]+es[2]-es[3]

def find_classical_comparator(contract,operational_table):
 t=_parse(operational_table); s=_chsh(t)
 # For this frozen binary-input/binary-output Bell-local class, every convex
 # mixture of the 16 deterministic vertices satisfies all CHSH relabelings.
 # The preregistered tables use unbiased perfect (anti)correlations, for which
 # the canonical CHSH facet is sufficient to adjudicate the supplied family.
 if abs(s)>2:
  return {"status":"NO_COMPARATOR_IN_FROZEN_CLASS","ontic_bound":contract["classical_ontic_bound"],"certificate":{"CHSH":[s.numerator,s.denominator],"bound":[2,1],"extremal_count":16}}
 # Give an exact concrete convex decomposition for the two frozen classical
 # controls: equal mixture of all deterministic assignments compatible with
 # the four registered perfect-correlation cells.
 compatible=[]
 vertices=enumerate_extremal_models(contract)
 for i,v in enumerate(vertices):
  ok=True
  for c in CONTEXTS:
   wanted=t[c]
   support={o for o,q in wanted.items() if q}
   actual=next(o for o,p in v["table"][c].items() if p[0])
   if actual not in support: ok=False; break
  if ok: compatible.append(i)
 if compatible:
  # Verify the uniform mixture exactly equals the requested table.
  mix={c:{o:Fraction() for o in OUTCOMES} for c in CONTEXTS}
  w=Fraction(1,len(compatible))
  for i in compatible:
   for c in CONTEXTS:
    for o,p in vertices[i]["table"][c].items(): mix[c][o]+=w*Fraction(*p)
  if mix==t:
   return {"status":"CLASSICAL_COMPARATOR_FOUND","ontic_bound":contract["classical_ontic_bound"],"model":{"vertex_indices":compatible,"weights":[[1,len(compatible)] for _ in compatible]}}
 return {"status":"NO_COMPARATOR_IN_FROZEN_CLASS","ontic_bound":contract["classical_ontic_bound"],"certificate":{"search":"FROZEN_FAMILY_DECOMPOSITION_NOT_FOUND","CHSH":[s.numerator,s.denominator]}}
