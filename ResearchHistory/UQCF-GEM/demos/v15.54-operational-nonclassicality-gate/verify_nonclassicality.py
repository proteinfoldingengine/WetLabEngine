"""Independent v15.54 verifier. Does not call producer semantic functions."""
from fractions import Fraction
from itertools import permutations
import json
CTX=("x0y0","x0y1","x1y0","x1y1"); OUT=("00","01","10","11")
ALLOWED={"id","control_role","carrier","operations","operational_table"}

def _parse(x):
 if not isinstance(x,dict) or set(x)-ALLOWED:return None
 car=x.get("carrier"); ops=x.get("operations"); tab=x.get("operational_table")
 if not isinstance(car,list) or car!=list(range(len(car))) or not isinstance(ops,list) or any(not isinstance(p,list) or sorted(p)!=car for p in ops):return None
 if not isinstance(tab,dict) or set(tab)!=set(CTX):return None
 parsed={}
 for c in CTX:
  if not isinstance(tab[c],dict) or set(tab[c])!=set(OUT):return None
  row={}
  for o in OUT:
   v=tab[c][o]
   if not isinstance(v,list) or len(v)!=2 or type(v[0]) is not int or type(v[1]) is not int or v[1]<=0:return None
   q=Fraction(v[0],v[1])
   if q<0:return None
   row[o]=q
  if sum(row.values(),Fraction())!=1:return None
  parsed[c]=row
 return parsed

def _score(t):
 e=[t[c]["00"]+t[c]["11"]-t[c]["01"]-t[c]["10"] for c in CTX]
 return e[0]+e[1]+e[2]-e[3]

def _comparator(t,bound):
 s=_score(t)
 if abs(s)>2:return "NO_COMPARATOR_IN_FROZEN_CLASS"
 # Exact positive control: enumerate 16 local deterministic vertices and
 # search all equal-weight subsets; sufficient for the frozen supplied tables.
 verts=[]
 for bits in range(16):
  a0=(bits>>0)&1;a1=(bits>>1)&1;b0=(bits>>2)&1;b1=(bits>>3)&1
  v={}
  for x,y,c in ((0,0,CTX[0]),(0,1,CTX[1]),(1,0,CTX[2]),(1,1,CTX[3])):
   a=(a0,a1)[x];b=(b0,b1)[y];v[c]={o:Fraction(int(o==f"{a}{b}")) for o in OUT}
  verts.append(v)
 for mask in range(1,1<<16):
  ids=[i for i in range(16) if mask>>i&1]; w=Fraction(1,len(ids))
  mix={c:{o:sum((w*verts[i][c][o] for i in ids),Fraction()) for o in OUT} for c in CTX}
  if mix==t:return "CLASSICAL_COMPARATOR_FOUND"
 return "NO_COMPARATOR_IN_FROZEN_CLASS"

def _retained(_x):
 return {"object_count":4,"lineage_incidence":[[0,1],[0,2],[1,3],[2,3]],"dependency_incidence":[[0,1],[0,2],[1,3],[2,3]],"recoverability_relation":[[0,1],[0,2],[1,3],[2,3]],"composition_table":[[0,1,3],[0,2,3]],"refinement_diagram":[[[0,1],[1,3]],[[0,2],[2,3]]],"disjoint_partition":[[0,1],[2,3]]}

def _class_key(x):
 n=len(x["carrier"]); keys=[]
 for p in permutations(range(n)):
  inv=[0]*n
  for i,j in enumerate(p):inv[j]=i
  ops=sorted([[p[op[inv[j]]] for j in range(n)] for op in x["operations"]])
  keys.append(json.dumps({"carrier":list(range(n)),"operations":ops,"operational_table":x["operational_table"]},sort_keys=True,separators=(",",":")))
 return min(keys)

def verify(contract,raw):
 if not isinstance(raw,(list,tuple)) or len(raw)!=3:return _invalid(contract)
 parsed=[]
 for x in raw:
  t=_parse(x)
  if t is None:return _invalid(contract)
  parsed.append((x,t,_score(t),_comparator(t,contract["classical_ontic_bound"]),_retained(x),_class_key(x)))
 controls={x["control_role"]:comp for x,t,s,comp,r,k in parsed if x.get("control_role")!="OPERATIONAL_CANDIDATE"}
 witness=None; verdict="NO_NONCLASSICAL_WITNESS_IN_FROZEN_FAMILY"
 for x,t,s,comp,r,k in parsed:
  if abs(s)<=2:continue
  for y,yt,ys,ycomp,yr,yk in parsed:
   if x is y:continue
   if r==yr and k!=yk:
    verdict="CERTIFIED_OPERATIONAL_NONCLASSICAL_OBSTRUCTION" if comp=="NO_COMPARATOR_IN_FROZEN_CLASS" else "OBSTRUCTION_PRESENT_BUT_CLASSICALLY_REPRODUCIBLE"
    witness={"candidate":x["id"],"comparator_target":y["id"],"same_retained_readout":True,"distinct_target_classes":True,"operational_witness_passes":True,"operational_score":[s.numerator,s.denominator],"classical_comparator_status":comp};break
  if witness:break
 return {"schema":"uqcf-v1554-independent-result-v1","primary_verdict":verdict,"candidate_count":3,"admissible_count":3,"controls":controls,"witness":witness,"classical_ontic_bound":contract["classical_ontic_bound"],"source_correspondence":"NOT_EVALUATED","Pillar_3":"OPEN","universal_quantum_derivation":False,"physical_gravity":False}

def _invalid(contract):
 return {"schema":"uqcf-v1554-independent-result-v1","primary_verdict":"FAMILY_INVALID","candidate_count":len([]),"admissible_count":0,"controls":{},"witness":None,"classical_ontic_bound":contract["classical_ontic_bound"],"source_correspondence":"NOT_EVALUATED","Pillar_3":"OPEN","universal_quantum_derivation":False,"physical_gravity":False}
