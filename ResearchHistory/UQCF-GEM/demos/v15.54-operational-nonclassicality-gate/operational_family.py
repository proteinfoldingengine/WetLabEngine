"""Exact preregistered v15.54 operational family."""
from copy import deepcopy
from fractions import Fraction
import json

CONTEXTS=("x0y0","x0y1","x1y0","x1y1")
OUTCOMES=("00","01","10","11")

def _uniform(): return {o:[1,4] for o in OUTCOMES}
def _corr():
 return {"00":[1,2],"01":[0,1],"10":[0,1],"11":[1,2]}
def _anticorr():
 return {"00":[0,1],"01":[1,2],"10":[1,2],"11":[0,1]}
def _table(rows): return {c:deepcopy(r) for c,r in zip(CONTEXTS,rows)}

_RAW=(
 {"id":"V1553_CLASSICAL","control_role":"V1553_PERMUTATION_CLASSICAL","carrier":[0,1,2,3],"operations":[[0,1,2,3],[1,0,3,2]],"operational_table":_table([_corr(),_corr(),_corr(),_corr()])},
 {"id":"S3_NONCOMMUTING_CONTROL","control_role":"NONCOMMUTING_PERMUTATION_CLASSICAL","carrier":[0,1,2],"operations":[[1,0,2],[0,2,1]],"operational_table":_table([_corr(),_corr(),_corr(),_corr()])},
 {"id":"CHSH_PREREGISTERED","control_role":"OPERATIONAL_CANDIDATE","carrier":[0,1],"operations":[[0,1],[1,0]],"operational_table":_table([_corr(),_corr(),_corr(),_anticorr()])},
)

def canonical_candidate(x,ignore_id=False):
 y=deepcopy(x)
 if ignore_id:y.pop("id",None)
 return json.dumps(y,sort_keys=True,separators=(",",":"))

def enumerate_raw_candidates(contract):
 return deepcopy(_RAW)

def check_admissibility(contract,x):
 reasons=[]
 if not isinstance(x,dict): return {"admissible":False,"reasons":["SCHEMA"]}
 allowed={"id","control_role","carrier","operations","operational_table"}
 if set(x)-allowed: reasons.append("FORBIDDEN_OR_UNKNOWN_FIELD")
 if not isinstance(x.get("id"),str) or x.get("control_role") not in {"V1553_PERMUTATION_CLASSICAL","NONCOMMUTING_PERMUTATION_CLASSICAL","OPERATIONAL_CANDIDATE"}: reasons.append("METADATA")
 carrier=x.get("carrier")
 if not isinstance(carrier,list) or not carrier or carrier!=list(range(len(carrier))): reasons.append("CARRIER")
 ops=x.get("operations")
 if not isinstance(ops,list) or not carrier or any(not isinstance(p,list) or sorted(p)!=carrier for p in ops): reasons.append("OPERATIONS")
 table=x.get("operational_table")
 if not isinstance(table,dict) or set(table)!=set(CONTEXTS): reasons.append("CONTEXTS")
 else:
  for c,row in table.items():
   if not isinstance(row,dict) or set(row)!=set(OUTCOMES): reasons.append("OUTCOMES:"+c); continue
   total=Fraction(0)
   for o,v in row.items():
    if not isinstance(v,list) or len(v)!=2 or type(v[0]) is not int or type(v[1]) is not int or v[1]<=0:
     reasons.append("RATIONAL:"+c+":"+o); continue
    q=Fraction(v[0],v[1])
    if q<0: reasons.append("NEGATIVE:"+c+":"+o)
    total+=q
   if total!=1: reasons.append("NORMALIZATION:"+c)
 return {"admissible":not reasons,"reasons":sorted(set(reasons))}
