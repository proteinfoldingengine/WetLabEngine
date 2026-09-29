from itertools import combinations,product
import importlib.util,pathlib,json,hashlib
P=pathlib.Path(__file__).resolve().parents[1]/'v16.26-consistency-increment-law'/'engine.py';s=importlib.util.spec_from_file_location('v26',P);v26=importlib.util.module_from_spec(s);s.loader.exec_module(v26)
def legal_steps(p,cur,target):
 out=[]
 for i,(y,z) in enumerate(zip(cur,target)):
  for leaf in y:
   if leaf in z or leaf==0:continue
   if any(p[w]==leaf and w in y for w in y):continue
   try:d=v26.atomic(p,cur,i,leaf)
   except ValueError:continue
   out.append(d)
 return out
def paths(p,before,after,limit=20000):
 out=[]
 def rec(cur,rows):
  if tuple(cur)==tuple(after):out.append(rows);return
  if len(out)>=limit:return
  for d in legal_steps(p,cur,after):rec(tuple(map(tuple,d['after'])),rows+[d])
 rec(tuple(before),[]);return out
def endpoint_cases(bound):
 for _,p in v26.shapes(bound):
  L=v26.legal(p)
  for n in range(1,min(4,len(L))+1):
   for ys in combinations(L,n):
    if set().union(*map(set,ys))!=set(range(len(p))):continue
    pools=[[z for z in L if set(z)<=set(y)] for y in ys]
    for zs in product(*pools):
     if set().union(*map(set,zs))!=set(range(len(p))):continue
     removed=sum(len(set(y)-set(z)) for y,z in zip(ys,zs))
     if 2<=removed<=5:yield p,ys,zs
def event_map(path):return {(d['index'],d['leaf']):d['delta_h'] for d in path}
def witness(p,ys,zs,ps):
 for a,b in combinations(ps,2):
  A,B=event_map(a),event_map(b);chg=sorted(k for k in A if A[k]!=B[k])
  if chg:return {'version':'16.27','parents':list(p),'before':[list(x) for x in ys],'after':[list(x) for x in zs],'path_a':a,'path_b':b,'changed_events':[list(x) for x in chg]}
def find_witness(bound=4):
 for p,ys,zs in endpoint_cases(bound):
  ps=paths(p,ys,zs)
  if len(ps)>1:
   w=witness(p,ys,zs,ps)
   if w:return w
def produce(bound=4):
 endpoints=multi=dependent=paths_total=0;first=None;digest=hashlib.sha256()
 for p,ys,zs in endpoint_cases(bound):
  ps=paths(p,ys,zs);endpoints+=1;paths_total+=len(ps);multi+=len(ps)>1
  w=witness(p,ys,zs,ps) if len(ps)>1 else None
  if w:dependent+=1;first=first or w
  sig=sorted(tuple(sorted(event_map(x).items())) for x in ps);digest.update((repr((p,ys,zs,sig))+'\n').encode())
 return {'version':'16.27','bound':bound,'endpoints':endpoints,'multi_path':multi,'path_dependent':dependent,'paths':paths_total,'first_witness':first,'digest':digest.hexdigest()}

if __name__=='__main__':
 d=produce(4);print(json.dumps(d,sort_keys=True));
