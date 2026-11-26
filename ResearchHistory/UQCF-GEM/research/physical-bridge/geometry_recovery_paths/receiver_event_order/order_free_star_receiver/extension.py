"""Bounded simple-support search beyond the archived producer domain."""
from collections import Counter
from itertools import combinations
import json
from census import cover_info, symmetries, remap

def run(m,k):
    count=Counter()
    best={}
    for cols in combinations([s for s in range(1,1<<k) if s.bit_count()>=2],m):
        count['patterns']+=1
        q,ess,_=cover_info(cols,k)
        if not ess&1: continue
        cuts=[]
        for i,s in enumerate(cols):
            if not s&1 or s.bit_count()<3: continue
            cut=tuple(sorted((*cols[:i],s^1,*cols[i+1:])))
            cq,ce,cu=cover_info(cut,k)
            if cq==q: cuts.append((i,ce,cu))
        for (i,e,u),(j,f,v) in combinations(cuts,2):
            roles=(e&~v | f&~u)&~1
            if not roles: continue
            count['pairs']+=1
            group=symmetries(cols,k)
            for b in range(1,k):
                if not roles & (1<<b): continue
                keep,lose=(i,j) if e & (1<<b) else (j,i)
                fixed=all(p[b]==b and p[0]==0 for p in group)
                distinct=not any(p[0]==0 and remap(cols[i],p)==cols[j] for p in group)
                degrees=[sum(bool(s & 1<<c) for s in cols) for c in range(k)]
                for label,condition in {
                    'all':True,'identifiable':fixed and distinct,
                    'single_identifiable':fixed and distinct and roles.bit_count()==1,
                    'single_identifiable_degree_tie':fixed and distinct and roles.bit_count()==1 and degrees.count(degrees[b])>1,
                }.items():
                    if condition:
                        count[label]+=1
                        best.setdefault(label,dict(m=m,k=k,cols=cols,A=0,B=b,keep=keep,lose=lose,
                                                   group=group,degrees=degrees,roles=roles,q=q))
    return dict(m=m,k=k,counts=count,examples=best)

if __name__=='__main__':
    cells=[run(m,k) for k,sizes in ((4,(5,6,7)),(5,(3,4,5))) for m in sizes]
    print(json.dumps(cells,sort_keys=True))
