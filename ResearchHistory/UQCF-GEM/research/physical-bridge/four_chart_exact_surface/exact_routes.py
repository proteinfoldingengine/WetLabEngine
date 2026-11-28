from collections import Counter,deque
from itertools import product
import sys
from pathlib import Path
sys.path.insert(0,str(Path(sys.argv[1]).resolve()))
import producer as p
import verifier as v
def raw(s):
    return v.raw_roots(2,[({0},{0,1},{1})[x+1] for x in s])
def decode(s):
    return tuple(int(bool(s[1]&(1<<i)))-int(bool(s[0]&(1<<i))) for i in range(1,5))
states={s for s in product((-1,0,1),repeat=4) if v.profile_check(v.Q,2,raw(s))==[2]}
def l1(s,t):return sum(abs(x-y) for x,y in zip(s,t))
target=decode(v.model(v.Q,[2],2)[2])
suffixes=set(); excess=Counter(); canonical=Counter(); via=Counter(); examples={}
for s in sorted(states):
    prev={s:None}; dist={s:0}; queue=deque([s])
    while queue:
        a=queue.popleft()
        for b in sorted(states):
            if b in prev or l1(a,b)!=1:continue
            prev[b]=a;dist[b]=dist[a]+1;queue.append(b)
    assert len(prev)==50
    for t,d in dist.items():
        delta=d-l1(s,t)
        swap=(s.count(-1)==s.count(1)==1 and t==tuple(-x for x in s))
        assert delta==2*swap
        route_to_t=[]; at=t
        while at is not None:
            route_to_t.append(raw(at)); at=prev[at]
        assert v.path_check(v.Q,2,[2],route_to_t[::-1],raw(s),raw(t))==0
        excess[delta]+=1
        examples.setdefault(delta,(s,t,d))
    route=[]; a=target
    while a is not None:
        route.append(raw(a));a=prev[a]
    route.reverse()
    assert v.path_check(v.Q,2,[2],route,raw(s),raw(target))==0
    stock=p.normalize(raw(s),p.Q,2,[2])
    assert v.path_check(v.Q,2,[2],stock,raw(s),raw(target))==1
    assert stock.count([31,31])==1
    suffixes.add(tuple(map(tuple,stock[stock.index([31,31]):])))
    assert len(stock)-1==l1(s,(0,)*4)+l1((0,)*4,target)
    via[len(stock)-len(route)]+=1
    canonical[dist[target]-l1(s,target)]+=1
assert len(suffixes)==1
print('common suffix',next(iter(suffixes)))
print('target',target,'all pairs',excess,'examples',examples)
print('exact minus unrestricted to target',canonical,'stock minus exact',via)
