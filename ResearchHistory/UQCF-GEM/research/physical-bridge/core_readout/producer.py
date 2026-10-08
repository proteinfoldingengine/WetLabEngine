import itertools,json
from pins import SCOPE,PROOF
COMMANDS={'+a1':(2,0),'-a1':(2,1),'+c2':(3,0),'-c2':(3,1),'+e4':(4,1),'-e4':(4,0)}
def supports(s):
 x,y,d1,d2,b=map(int,s)
 return [set('b')|({'a'} if not d1 else set())|({'w'} if x else set()),set('d')|({'c'} if not d2 else set())|({'w'} if y else set()),set('ef'),set('gh')|({'e'} if b else set())]
def tau(rr):
 labels=sorted(set.union(*rr))
 return next(k for k in range(len(labels)+1) if any(all(set(h)&r for r in rr) for h in itertools.combinations(labels,k)))
def produce():
 allstates={''.join(s):None for s in itertools.product('01',repeat=5)}
 vals={s:tau(supports(s)) for s in allstates}
 ids=sorted(s for s in allstates if min(map(len,supports(s)))>=2 and 3<=vals[s]<=4)
 edges=[]
 for s in ids:
  for cmd,(i,b) in COMMANDS.items():
   edges.append([s,cmd,s]);t=s[:i]+str(b)+s[i+1:]
   if t!=s and t in ids:edges.append([s,cmd,t])
 edges.sort();fibers={o:[s for s in ids if s[2:]==o] for o in sorted({s[2:] for s in ids})}
 restore={}
 for s in ids:
  path=[s];t=s
  for i in (2,3,4):
   if t[i]=='1':t=t[:i]+'0'+t[i+1:];path.append(t)
  restore[s]=path
 certificates={}
 for hidden in ('00','01','10','11'):
  s=hidden+'000';certificates[hidden]=[s,hidden+'001'] if hidden!='11' else [s,'11100','11110']
 service=sorted([[s,c,t] for s in ('10000','11000') for c in ('+w2','-w2') for t in sorted({s, s[0]+('1' if c[0]=='+' else '0')+s[2:]})])
 assert vals['11001']==2 and len(supports('00100')[0])==1
 return {'scope_commit':SCOPE,'proof_commit':PROOF,'states':[{'id':s,'tau':vals[s]} for s in ids], 'outcomes':edges,'fibers':fibers,'restorations':restore,'certificates':certificates,'service':service,
 'controls':{'no_readout':['00000','11000'],'no_uniform_safety':['00000','+e4','00001','11000','+e4','11001'],'band_guard_removed':['11000','+e4','11001'],'floor_guard_removed':['00000','-a1','00100'],'hidden_writer':['10000','11000'],'noop_ambiguity':['00000','11000']},
 'claims':{'tau_observed':False,'uniformly_safe_attempts':False,'guaranteed_completion':False,'immediate_payload_decode':False,'physical_origin_derived':False}}
if __name__=='__main__':print(json.dumps(produce(),sort_keys=True,indent=2))
