"""Set roots, representative unions, closed guard characterization and graphs."""
import json,sys
from functools import lru_cache
@lru_cache(None)
def hitting(roots):
 h={frozenset()}
 for r in roots:h={s|{x} for s in h for x in r}
 return min(map(len,h))
def roots(t):
 x,y,d,e,b,v,z=t
 return [{1}|({0} if not d else set())|({10} if x else set()),{3}|({2} if not e else set())|({10} if y else set()),{4,5}|({8} if v else set()),{6,7}|({4} if b else set())|({9} if z else set())]
def ht(r):return hitting(tuple(tuple(sorted(s)) for s in r))
def valid(w,c):return c[0]<=w[0] and c[1]<=w[1] and c[2]+w[0]*w[1]<=1
def codes(n):return [tuple((k>>(n-1-j))&1 for j in range(n)) for k in range(2**n)]
@lru_cache(None)
def expected():
 commands=[[0,0,0],[0,0,1],[1,2,0],[1,2,1],[2,8,0],[2,8,1],[3,4,0],[3,4,1],[3,9,0],[3,9,1]];places={(0,0):0,(1,2):1,(3,4):2,(2,8):3,(3,9):4};states=[];guarded=[]
 for t in codes(7):
  r=roots(t);n=ht(r);x,y,d,e,b,v,z=t;f=all(len(s)>=2 for s in r);adm=valid(t[:2],t[2:]);assert n==4-x*y-b and f==(d<=x and e<=y) and adm==(f and 3<=n<=4)
  states.append({'id':list(t),'supports':[sum(2**x for x in s) for s in r],'tau':n,'floor_valid':f,'admissible':adm})
  if adm:
   for cmd in commands:
    guarded.append([list(t),cmd,list(t)]);j=places[tuple(cmd[:2])];target=cmd[2] if j>=2 else 1-cmd[2];new=list(t);new[j+2]=target
    if new!=list(t) and valid(tuple(new[:2]),tuple(new[2:])):guarded.append([list(t),cmd,new])
 pairs=[];nonuniform=[]
 for a in range(4):
  for b in range(a,4):
   wa=(a//2,a%2);wb=(b//2,b%2);nodes=[list(c) for c in codes(5) if valid(wa,c) and valid(wb,c)];edges=[]
   for c in nodes:
    for j in range(5):
     n=c[:];n[j]=1-n[j]
     cmd=([0,0,1-n[j]] if j==0 else [1,2,1-n[j]] if j==1 else [3,4,n[j]] if j==2 else [2,8,n[j]] if j==3 else [3,9,n[j]])
     left,right=valid(wa,n),valid(wb,n)
     if n in nodes:
      for w in (wa,wb):
       before=roots(w+tuple(c));after=roots(w+tuple(n));r,x,add=cmd;changed=[v.copy() for v in before];assert (x in changed[r])!=bool(add)
       if add:changed[r].add(x)
       else:changed[r].remove(x)
       assert changed==after and [v-{10} for v in after]==[v-{10} for v in roots(wa+tuple(n))]
      edges.extend([[c,cmd,0,c],[c,cmd,1,n]])
     elif left!=right:nonuniform.append({'pair':[a,b],'core':c,'command':cmd,'left_legal':left,'right_legal':right})
   pairs.append({'worlds':[a,b],'nodes':nodes,'edges':sorted(edges)})
 trace=[[0,0,0,0,0],[0,0,0,1,0],[0,0,0,1,1],[0,0,0,0,1],[0,0,0,0,0]]
 for c in trace:assert valid((0,0),c) and valid((1,1),c)
 for c,n in zip(trace,trace[1:]):assert sum(a!=b for a,b in zip(c,n))==1
 worlds=[[{0},{0},{0},{1},{2},{3,4}],[{0},{0},{0},{1,6},{2,6},{3,4}]];states_app=[];taus=[];cores=[];admission=[]
 for w in worlds:
  stages=[w,[s|{5} if j==5 else s.copy() for j,s in enumerate(w)]];states_app.append([[sum(2**x for x in s) for s in r] for r in stages]);taus.append([ht(r) for r in stages]);cores.append([[sum(2**x for x in s if x<6) for s in r] for r in stages]);admission.append(not set.intersection(w[3],w[4]));assert all(len(s)>=f for r in stages for s,f in zip(r,[1,1,1,1,1,2]))
 return json.dumps({'scope_commit':'14fc8eafc5af1cbf263c3845c883324587d0e0e6','claims':{'core_may_change':True,'hidden_writes_in_general_proof':True,'hidden_writes_in_bounded_alphabet':False,'relies_on_all_noop':False,'all_commit_obstruction':True,'possible_trace_equality':True,'arbitrary_kernel_distribution_equality':False,'universal_no_observer':False,'native_access_derived':False},'commands':commands,'states':states,'guarded_edges':sorted(guarded),'pairs':pairs,'nonuniform':nonuniform,'scratch_trace':trace,'admission':{'states':states_app,'taus':taus,'cores':cores,'admission':admission,'floors':[1,1,1,1,1,2],'command':[5,5,1]}},sort_keys=True,separators=(',',':'))
def verify(d):
 if json.dumps(d,sort_keys=True,separators=(',',':'))!=expected():raise ValueError('complete native state/paired transition/record mismatch')
 return True
if __name__=='__main__':verify(json.load(open(sys.argv[1])));print('PASS independent complete guarded and uniformly safe paired graph reconstruction')
