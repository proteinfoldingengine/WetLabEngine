from itertools import combinations,product
import hashlib
GENESIS='v16.26-common-genesis'
def need(x,m):
 if not x:raise ValueError(m)
def valid(p,ys):
 p=tuple(p);need(p and p[0]==-1 and all(type(x)is int for x in p),'parents');out=[]
 for y in ys:
  y=tuple(y);need(y and 0 in y and len(set(y))==len(y) and all(type(v)is int and 0<=v<len(p) for v in y) and all(v==0 or p[v] in y for v in y),'view');out.append(y)
 return p,tuple(out)
def hv(p,ys):
 U=set().union(*map(set,ys));vals=[1]
 for v in U:
  K={w for w in U if w and p[w]==v}
  if K:vals.append(min(r for r in range(1,len(ys)+1) if any(K<=set().union(*(set(ys[i]) for i in S)) for S in combinations(range(len(ys)),r))))
 return max(vals)
def tv(p,ys,v):
 U=set().union(*map(set,ys));K={w for w in U if w and p[w]==v}
 if not K:return 0
 return min(r for r in range(1,len(ys)+1) if any(K<=set().union(*(set(ys[i]) for i in S)) for S in combinations(range(len(ys)),r)))
def verify_atomic(d):
 need(d.get('version')=='16.26' and d.get('genesis')==GENESIS,'origin');p,ys=valid(d['parents'],d['before']);_,zs=valid(p,d['after']);i=d['index'];leaf=d['leaf'];need(type(i)is int and 0<=i<len(ys) and type(leaf)is int,'ids');need(all(ys[j]==zs[j] for j in range(len(ys)) if j!=i),'multi-view mutation');need(set(ys[i])-{leaf}==set(zs[i]) and len(ys[i])==len(zs[i])+1,'not atomic');need(not any(p[w]==leaf and w in ys[i] for w in ys[i]),'non-leaf');need(set().union(*map(set,ys))==set().union(*map(set,zs)),'union')
 par=p[leaf];tb,ta=tv(p,ys,par),tv(p,zs,par);hb,ha=hv(p,ys),hv(p,zs);need(ta-tb in (0,1),'local jump');need(ha-hb in (0,1),'global jump')
 U=set().union(*map(set,ys));K={w for w in U if w and p[w]==par};mins=[S for S in combinations(range(len(ys)),tb) if K<=set().union(*(set(ys[j]) for j in S))];tr=bool(mins) and all(not K<=set().union(*(set(zs[j]) for j in S)) for S in mins)
 need(d['parent']==par and d['tau_before']==tb and d['tau_after']==ta and d['h_before']==hb and d['h_after']==ha and d['delta_h']==ha-hb and d['trigger']==tr,'false certificate');return ha-hb,tr
def verify_factor(d):
 p,ys=valid(d['parents'],d['before']);_,zs=valid(p,d['after']);cur=ys;s=0
 for step in d['steps']:
  need(tuple(map(tuple,step['before']))==cur,'factor chain');delta,_=verify_atomic(step);s+=delta;cur=tuple(map(tuple,step['after']))
 need(cur==zs and s==d['h_after']-d['h_before'] and d['h_before']==hv(p,ys) and d['h_after']==hv(p,zs),'telescope');return True
def code(p):
 ch={v:[] for v in range(len(p))}
 for w in range(1,len(p)):ch[p[w]].append(w)
 def rec(v):return '('+''.join(sorted(rec(w) for w in ch[v]))+')'
 return rec(0)
def legal(p):
 return [tuple(i for i in range(len(p)) if mask>>i&1) for mask in range(1,1<<len(p),2) if all(v==0 or p[v] in tuple(i for i in range(len(p)) if mask>>i&1) for v in tuple(i for i in range(len(p)) if mask>>i&1))]
def summary(p):
 L=legal(p);cnt=inc=tg=0;hist={};dig=hashlib.sha256()
 for n in range(1,min(4,len(L))+1):
  for ys in combinations(L,n):
   if set().union(*map(set,ys))!=set(range(len(p))):continue
   for i,y in enumerate(ys):
    for leaf in y:
     if not leaf or any(p[w]==leaf and w in y for w in y):continue
     z=tuple(v for v in y if v!=leaf);zs=list(ys);zs[i]=z;zs=tuple(zs)
     if set().union(*map(set,zs))!=set(range(len(p))):continue
     tb,ta=tv(p,ys,p[leaf]),tv(p,zs,p[leaf]);hb,ha=hv(p,ys),hv(p,zs);K={w for w in range(len(p)) if w and p[w]==p[leaf]};mins=[S for S in combinations(range(len(ys)),tb) if K<=set().union(*(set(ys[j]) for j in S))];tr=bool(mins) and all(not K<=set().union(*(set(zs[j]) for j in S)) for S in mins)
     need(ta-tb in (0,1) and ha-hb in (0,1),'theorem violation');cnt+=1;inc+=ha-hb==1;tg+=tr;k=f'{hb}->{ha}';hist[k]=hist.get(k,0)+1;dig.update((repr((ys,i,leaf,tb,ta,hb,ha,tr))+'\n').encode())
 return cnt,inc,tg,hist,dig.hexdigest()
def verify_document(doc,bound=5):
 need(doc['version']=='16.26' and doc['genesis']==GENESIS and doc['bound']==bound,'doc');tot=inc=tg=0
 for x in doc['instances']:
  p=tuple(x['parents']);need(code(p)==x['code'],'shape');s=summary(p);need((x['atomic'],x['strict'],x['triggers'],x['transitions'],x['digest'])==s,'summary');tot+=s[0];inc+=s[1];tg+=s[2]
 need((doc['atomic'],doc['strict'],doc['triggers'])==(tot,inc,tg),'totals');return {'atomic':tot,'strict':inc,'triggers':tg,'shapes':len(doc['instances'])}

if __name__=='__main__':
 import json,pathlib
 p=pathlib.Path(__file__).resolve().parent/'evidence';d=json.loads((p/'PRODUCTION.json').read_text());r=verify_document(d,5);(p/'VERIFICATION.json').write_text(json.dumps(r,sort_keys=True,indent=2)+'\n');print(json.dumps(r))
