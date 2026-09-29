from itertools import combinations
def need(x,m):
 if not x:raise ValueError(m)
def mobius_top(vals,n):
 need(set(vals)==set(range(1<<n)),'cube')
 return sum(((-1)**(n-(mask.bit_count())))*vals[mask] for mask in vals)
def tau(p,ys,v):
 U=set().union(*map(set,ys));K={w for w in U if w and p[w]==v}
 if not K:return 0
 return min(r for r in range(1,len(ys)+1) if any(K<=set().union(*(set(ys[i]) for i in S)) for S in combinations(range(len(ys)),r)))
def verify_case(c):
 p=tuple(c['parents']);ys=tuple(map(tuple,c['views']));e,f=map(tuple,c['events'])
 def de(s,q):i,n=q;z=list(s);z[i]=tuple(x for x in z[i] if x!=n);return tuple(z)
 states=(ys,de(ys,e),de(ys,f),de(de(ys,e),f));P=[tuple(tau(p,s,v) for v in range(len(p))) for s in states];H=[max([1]+list(x)) for x in P];lm=tuple(P[3][v]-P[1][v]-P[2][v]+P[0][v] for v in range(len(p)))
 need(c['profiles']==[list(x) for x in P] and c['h']==H and c['local_mixed']==list(lm) and c['global_mixed']==H[3]-H[1]-H[2]+H[0],'case');return True
def verify_document(d):
 need(d['version']=='16.30','version')
 for c in d.get('cases',[]):
  p=tuple(c['parents'])
  for e,f in c['edges']:need(p[e[1]]==p[f[1]],'cross-parent edge')
 return {'execution_status':'COMPLETED'}
