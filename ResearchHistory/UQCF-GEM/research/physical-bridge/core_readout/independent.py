import itertools,json,sys
# Independent pinned provenance; no import of the producer or its constants.
SCOPE = 'd68f460d6b594c83c8d7f5f242c85e4e61847580'
PROOF = 'f0fb556d39047e58e87e358b2433e58a0a25fb3b'
class Error(ValueError):pass
def loads(raw):
 def unique(pairs):
  d={}
  for k,v in pairs:
   if k in d:raise Error('duplicate JSON key')
   d[k]=v
  return d
 return json.loads(raw,object_pairs_hook=unique)
def reconstruct():
 def code(n):return format(n,'05b')
 def roots(n):return [(1,)+(() if n&4 else (0,))+((8,) if n&16 else ()),(3,)+(() if n&2 else (2,))+((8,) if n&8 else ()),(4,5),(6,7)+((4,) if n&1 else ())]
 def hit(rs):return min(len(set(h)) for h in itertools.product(*rs))
 values={n:hit(roots(n)) for n in range(32)}
 states={n for n in range(32) if all(len(r)>1 for r in roots(n)) and values[n] in (3,4)}
 edges=set()
 for n in states:
  for mask,label,inverted in ((4,'a1',True),(2,'c2',True),(1,'e4',False)):
   for sign in ('+','-'):
    c=sign+label;edges.add((code(n),c,code(n)))
    desired=(sign=='+')!=inverted
    if bool(n&mask)!=desired and n^mask in states:edges.add((code(n),c,code(n^mask)))
 fibers={}
 for n in sorted(states):fibers.setdefault(code(n&7)[2:],[]).append(code(n))
 restoration={}
 for n in sorted(states):
  path=[code(n)];t=n
  for mask in (4,2,1):
   if t&mask:t^=mask;path.append(code(t))
  restoration[code(n)]=path
 certificates={}
 for h in range(4):
  n=h<<3;path=[code(n)]
  if h==3:path.extend([code(n|4),code(n|6)])
  else:path.append(code(n|1))
  certificates[format(h,'02b')]=path
 for h,path in certificates.items():
  for a,b in zip(path,path[1:]):assert any(e[0]==a and e[2]==b for e in edges)
  completions=fibers[path[-1][2:]]
  assert {int(s[0])*int(s[1]) for s in completions}=={int(h[0])*int(h[1])}
 for path in restoration.values():
  assert path[-1][2:]=='000'
  for a,b in zip(path,path[1:]):assert any(e[0]==a and e[2]==b for e in edges)
 service=set()
 for n in (16,24):
  for c in ('+w2','-w2'):
   service.add((code(n),c,code(n)))
   if bool(n&8)!=(c[0]=='+'):service.add((code(n),c,code(n^8)))
 for a,c,b in service:assert (a!=b)==(a[1]!=b[1])
 assert values[25]==2 and min(map(len,roots(4)))==1
 return {'scope_commit':SCOPE,'proof_commit':PROOF,'states':[{'id':code(n),'tau':values[n]} for n in sorted(states)],'outcomes':[list(e) for e in sorted(edges)],'fibers':fibers,'restorations':restoration,'certificates':certificates,'service':[list(e) for e in sorted(service)],
 'controls':{'no_readout':['00000','11000'],'no_uniform_safety':['00000','+e4','00001','11000','+e4','11001'],'band_guard_removed':['11000','+e4','11001'],'floor_guard_removed':['00000','-a1','00100'],'hidden_writer':['10000','11000'],'noop_ambiguity':['00000','11000']},
 'claims':{'tau_observed':False,'uniformly_safe_attempts':False,'guaranteed_completion':False,'immediate_payload_decode':False,'physical_origin_derived':False}}
def verify(report):
 expected=reconstruct()
 if json.dumps(report,sort_keys=True)!=json.dumps(expected,sort_keys=True):raise Error('full canonical identity mismatch')
 return {'status':'PASS','states':len(expected['states']),'outcomes':len(expected['outcomes']),'service_outcomes':len(expected['service'])}
if __name__=='__main__':
 with open(sys.argv[1]) as f:r=loads(f.read())
 print(json.dumps(verify(r),sort_keys=True))
