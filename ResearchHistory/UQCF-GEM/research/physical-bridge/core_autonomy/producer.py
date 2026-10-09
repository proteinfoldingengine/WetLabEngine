"""Literal incidence states, subset transversals and paired safe transitions."""
import itertools,json,sys
from functools import lru_cache
POSITIONS=[(0,0),(1,2),(3,4),(2,8),(3,9)]
COMMANDS=sorted([[r,x,a] for r,x in POSITIONS for a in (0,1)])
CLAIMS={'core_may_change':True,'hidden_writes_in_general_proof':True,'hidden_writes_in_bounded_alphabet':False,'relies_on_all_noop':False,'all_commit_obstruction':True,'possible_trace_equality':True,'arbitrary_kernel_distribution_equality':False,'universal_no_observer':False,'native_access_derived':False}
@lru_cache(None)
def tau(s):
 labels=sorted({x for v in s for x in range(11) if v&2**x})
 for k in range(1,len(labels)+1):
  for h in itertools.combinations(labels,k):
   mask=sum(2**x for x in h)
   if all(v&mask for v in s):return k
 raise ValueError('empty root')
def supports(t):
 x,y,d1,d2,b,v,z=t
 return (2|(1 if not d1 else 0)|(1024 if x else 0),8|(4 if not d2 else 0)|(1024 if y else 0),48|(256 if v else 0),192|(16 if b else 0)|(512 if z else 0))
def command(j,new):
 r,x=POSITIONS[j];return [r,x,1-new if j<2 else new]
def application():
 worlds=[(1,1,1,2,4,24),(1,1,1,66,68,24)];states=[[list(s),list(s[:-1]) + [s[-1]|32]] for s in worlds]
 return {'states':states,'taus':[[tau(tuple(s)) for s in w] for w in states],'cores':[[[v&63 for v in s] for s in w] for w in states],'admission':[True,False],'floors':[1,1,1,1,1,2],'command':[5,5,1]}
def produce():
 states=[];lookup={}
 for ident in itertools.product((0,1),repeat=7):
  s=supports(ident);t=tau(s);floor=all(v.bit_count()>=2 for v in s);row={'id':list(ident),'supports':list(s),'tau':t,'floor_valid':floor,'admissible':floor and 3<=t<=4};states.append(row);lookup[ident]=row
 guarded=[]
 for ident,row in lookup.items():
  if not row['admissible']:continue
  for cmd in COMMANDS:
   guarded.append([list(ident),cmd,list(ident)])
   j=POSITIONS.index(tuple(cmd[:2]));new=1-cmd[2] if j<2 else cmd[2];n=list(ident);n[j+2]=new
   if n!=list(ident) and lookup[tuple(n)]['admissible']:guarded.append([list(ident),cmd,n])
 pairs=[];nonuniform=[]
 for a,b in itertools.combinations_with_replacement(range(4),2):
  worlds=[(a//2,a%2),(b//2,b%2)];nodes=[];edges=[]
  for core in itertools.product((0,1),repeat=5):
   if not all(lookup[w+core]['admissible'] for w in worlds):continue
   nodes.append(list(core))
   for j in range(5):
    n=list(core);n[j]^=1;cmd=command(j,n[j]);legal=[lookup[w+tuple(n)]['admissible'] for w in worlds]
    if all(legal):edges.extend([[list(core),cmd,0,list(core)],[list(core),cmd,1,n]])
    elif legal[0]!=legal[1]:nonuniform.append({'pair':[a,b],'core':list(core),'command':cmd,'left_legal':legal[0],'right_legal':legal[1]})
  pairs.append({'worlds':[a,b],'nodes':nodes,'edges':sorted(edges)})
 trace=[[0,0,0,0,0],[0,0,0,1,0],[0,0,0,1,1],[0,0,0,0,1],[0,0,0,0,0]]
 return {'scope_commit':'14fc8eafc5af1cbf263c3845c883324587d0e0e6','claims':CLAIMS,'commands':COMMANDS,'states':states,'guarded_edges':sorted(guarded),'pairs':pairs,'nonuniform':nonuniform,'scratch_trace':trace,'admission':application()}
if __name__=='__main__':
 d=produce();open(sys.argv[1],'w').write(json.dumps(d,sort_keys=True,separators=(',',':'))+'\n');print(json.dumps({'states':len(d['states']),'admissible':sum(s['admissible'] for s in d['states']),'guarded_edges':len(d['guarded_edges']),'world_pairs':len(d['pairs']),'paired_nodes':sum(len(g['nodes']) for g in d['pairs']),'paired_safe_edges':sum(len(g['edges']) for g in d['pairs']),'nonuniform_boundaries':len(d['nonuniform'])}))
