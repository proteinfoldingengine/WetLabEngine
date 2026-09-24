"""Exact structural target equivalence for the frozen v15.54 family."""
import json
from itertools import permutations

def _canon_without_metadata(x):
 return {"carrier":x["carrier"],"operations":x["operations"],"operational_table":x["operational_table"]}

def _relabel_candidate(x,p):
 n=len(x["carrier"])
 inv=[0]*n
 for i,j in enumerate(p): inv[j]=i
 ops=[]
 for op in x["operations"]:
  ops.append([p[op[inv[j]]] for j in range(n)])
 return {"carrier":list(range(n)),"operations":sorted(ops),"operational_table":x["operational_table"]}

def canonical_class_key(contract,x):
 n=len(x["carrier"]); keys=[]
 for p in permutations(range(n)):
  y=_relabel_candidate(x,p)
  keys.append(json.dumps(y,sort_keys=True,separators=(",",":")))
 return min(keys)

def are_equivalent(contract,left,right):
 if len(left["carrier"])!=len(right["carrier"]): return False
 return canonical_class_key(contract,left)==canonical_class_key(contract,right)
