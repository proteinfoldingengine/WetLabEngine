"""Producer: recursively ordered forests and deletion-to-retained-owner."""
from functools import lru_cache
import json
SCIENCE='20fedca0242791266e9851c1dc6cb4591888be15'
@lru_cache(None)
def forests(n):
    if n==0: return ((),)
    return tuple((child,)+tail for k in range(1,n+1) for child in forests(k-1) for tail in forests(n-k))
def addresses(tree):
    result=[]
    def visit(t,path):
        result.append(path)
        for i,child in enumerate(t): visit(child,path+(i,))
    visit(tree,()); return tuple(sorted(result))
def operators(x,y):
    p=[[0]*len(x) for _ in y]; s=[[0]*len(x) for _ in y]
    positions={v:i for i,v in enumerate(y)}
    for j,v in enumerate(x):
        a=v
        while a not in positions: a=a[:-1]
        p[positions[a]][j]=1
        if v in positions: s[positions[v]][j]=1
    return p,s
records=[]
for x in sorted(addresses(tree) for n in range(1,6) for tree in forests(n-1)):
    for mask in range(1,1<<len(x)):
        y=tuple(v for i,v in enumerate(x) if mask&(1<<i))
        if () not in y or any(v and v[:-1] not in y for v in y): continue
        p,s=operators(x,y); records.append({'X':x,'Y':y,'P':p,'S':s})
records.sort(key=lambda r:(r['X'],r['Y']))
x=((),(0,),(0,0)); y=((),(0,)); p,s=operators(x,y)
v0=[1,0,0]; v1=[1,0,1]
def act(a,v): return [sum(row[j]*v[j] for j in range(len(v))) for row in a]
witness={'initial_R':[v0[1],v1[1]],'native_outputs':[act(p,v0),act(p,v1)],
         'delivery_R':[act(p,v0)[1],act(p,v1)[1]],'blind_R':[act(s,v0)[1],act(s,v1)[1]]}
print(json.dumps({'source_sha':SCIENCE,'n_max':5,'records':records,'witness':witness},sort_keys=True,separators=(',',':')))
