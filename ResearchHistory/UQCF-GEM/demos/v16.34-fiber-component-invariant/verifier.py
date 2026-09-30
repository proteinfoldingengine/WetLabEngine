from itertools import combinations
def need(x,m):
 if not x:raise ValueError(m)
def tau(p,ys,v):
 U=set().union(*map(set,ys));K={w for w in U if w and p[w]==v}
 if not K:return 0
 return min(r for r in range(1,len(ys)+1) if any(K<=set().union(*(set(ys[i]) for i in S)) for S in combinations(range(len(ys)),r)))
def mc(p,ys,v):
 U=set().union(*map(set,ys));K={w for w in U if w and p[w]==v}
 if not K:return [()]
 t=tau(p,ys,v);return [S for S in combinations(range(len(ys)),t) if K<=set().union(*(set(ys[i]) for i in S))]
def verify_state(c):
 p=tuple(c['parents']);ys=tuple(map(tuple,c['views']));M=[mc(p,ys,v) for v in range(len(p))];need(c['minimum_covers']==[[list(x) for x in z] for z in M],'minimum covers')
 ess=[];part=[]
 for v,m in enumerate(M):
  e=set.intersection(*(set(x) for x in m)) if m else set();ess.append(sorted([list((i,ch)) for i in e for ch in ys[i] if ch and p[ch]==v]));part.append([sum(i in S for S in m) for i in range(len(ys))])
 need(c['essential']==ess and c['participation']==part,'derived signature');return True
def verify_document(d):
 need(d['version']=='16.34','version');need(d['component_count']>=d['disconnected_fibers'],'counts');return {'execution_status':'COMPLETED'}
