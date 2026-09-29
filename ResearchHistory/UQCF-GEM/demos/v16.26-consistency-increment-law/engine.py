from itertools import combinations,product
import hashlib,json
GENESIS='v16.26-common-genesis'
def need(x,m):
 if not x:raise ValueError(m)
def parents(raw):
 p=tuple(raw);need(p and all(type(x)is int for x in p) and p[0]==-1,'parents');need(all(0<=p[i]<len(p) for i in range(1,len(p))),'endpoint');return p
def view(p,y):
 y=tuple(y);need(y and 0 in y and len(set(y))==len(y),'view');need(all(type(v)is int and 0<=v<len(p) for v in y),'identity');need(all(v==0 or p[v] in y for v in y),'ancestor');return y
def h(p,ys):
 U=set().union(*map(set,ys));a=[1]
 for v in U:
  kids={w for w in U if w and p[w]==v}
  if kids:a.append(min(r for r in range(1,len(ys)+1) if any(kids<=set().union(*(set(ys[i]) for i in S)) for S in combinations(range(len(ys)),r))))
 return max(a)
def tau_at(p,ys,v):
 U=set().union(*map(set,ys));kids={w for w in U if w and p[w]==v}
 if not kids:return 0
 return min(r for r in range(1,len(ys)+1) if any(kids<=set().union(*(set(ys[i]) for i in S)) for S in combinations(range(len(ys)),r)))
def trigger(p,ys,zs,parent):
 t=tau_at(p,ys,parent);U=set().union(*map(set,ys));kids={w for w in U if w and p[w]==parent}
 old=[S for S in combinations(range(len(ys)),t) if kids<=set().union(*(set(ys[i]) for i in S))]
 return bool(old) and all(not kids<=set().union(*(set(zs[i]) for i in S)) for S in old)
def atomic(raw,before,index,leaf):
 p=parents(raw);ys=tuple(view(p,y) for y in before);need(type(index)is int and 0<=index<len(ys),'index');y=ys[index];need(leaf in y and leaf!=0,'leaf');need(not any(p[w]==leaf and w in y for w in y),'non-leaf');z=tuple(v for v in y if v!=leaf);zs=list(ys);zs[index]=z;zs=tuple(zs);need(set().union(*map(set,ys))==set().union(*map(set,zs)),'same union');hb,ha=h(p,ys),h(p,zs);par=p[leaf];tr=trigger(p,ys,zs,par)
 return {'version':'16.26','genesis':GENESIS,'parents':list(p),'before':[list(x) for x in ys],'after':[list(x) for x in zs],'index':index,'leaf':leaf,'parent':par,'tau_before':tau_at(p,ys,par),'tau_after':tau_at(p,zs,par),'h_before':hb,'h_after':ha,'delta_h':ha-hb,'trigger':tr}
def factor(raw,before,after):
 p=parents(raw);cur=[view(p,y) for y in before];zs=tuple(view(p,z) for z in after);need(len(cur)==len(zs) and all(set(z)<=set(y) for y,z in zip(cur,zs)),'endpoint');need(set().union(*map(set,cur))==set().union(*map(set,zs)),'same union');hb=h(p,cur);steps=[]
 while tuple(cur)!=zs:
  moved=False
  for i,(y,z) in enumerate(zip(cur,zs)):
   rem=[v for v in y if v not in z and not any(p[w]==v and w in y and w not in z for w in y)]
   if rem:
    d=atomic(p,cur,i,max(rem));steps.append(d);cur=[tuple(x) for x in d['after']];moved=True;break
  need(moved,'factor')
 return {'version':'16.26','genesis':GENESIS,'parents':list(p),'before':[list(x) for x in before],'after':[list(x) for x in zs],'h_before':hb,'h_after':h(p,zs),'steps':steps}
def code(p):
 ch={v:[] for v in range(len(p))}
 for w in range(1,len(p)):ch[p[w]].append(w)
 def rec(v):return '('+''.join(sorted(rec(w) for w in ch[v]))+')'
 return rec(0)
def shapes(nmax):
 d={}
 for n in range(1,nmax+1):
  for q in product(*(range(i) for i in range(1,n))):
   p=(-1,)+q;d.setdefault(code(p),p)
 return [(k,d[k]) for k in sorted(d,key=lambda x:(len(x),x))]
def legal(p):
 out=[]
 for mask in range(1,1<<len(p),2):
  y=tuple(i for i in range(len(p)) if mask>>i&1)
  if all(v==0 or p[v] in y for v in y):out.append(y)
 return out
def covers(p):
 L=legal(p)
 for n in range(1,min(4,len(L))+1):
  for ys in combinations(L,n):
   if set().union(*map(set,ys))==set(range(len(p))):yield ys
def produce(bound=5):
 inst=[];total=strict=trigs=0
 for sc,p in shapes(bound):
  cnt=inc=tg=0;hist={};dig=hashlib.sha256()
  for ys in covers(p):
   for i,y in enumerate(ys):
    for leaf in y:
     if leaf and not any(p[w]==leaf and w in y for w in y):
      try:d=atomic(p,ys,i,leaf)
      except ValueError:continue
      cnt+=1;inc+=d['delta_h']==1;tg+=d['trigger'];k=f"{d['h_before']}->{d['h_after']}";hist[k]=hist.get(k,0)+1;dig.update((repr((ys,i,leaf,d['tau_before'],d['tau_after'],d['h_before'],d['h_after'],d['trigger']))+'\n').encode())
  total+=cnt;strict+=inc;trigs+=tg;inst.append({'code':sc,'parents':list(p),'atomic':cnt,'strict':inc,'triggers':tg,'transitions':hist,'digest':dig.hexdigest()})
 return {'version':'16.26','genesis':GENESIS,'bound':bound,'atomic':total,'strict':strict,'triggers':trigs,'instances':inst}

if __name__=='__main__':
 import pathlib
 d=produce(5);p=pathlib.Path(__file__).resolve().parent/'evidence';p.mkdir(exist_ok=True);(p/'PRODUCTION.json').write_text(json.dumps(d,sort_keys=True,indent=2)+'\n');print(json.dumps({'atomic':d['atomic'],'strict':d['strict'],'triggers':d['triggers'],'shapes':len(d['instances'])}))
