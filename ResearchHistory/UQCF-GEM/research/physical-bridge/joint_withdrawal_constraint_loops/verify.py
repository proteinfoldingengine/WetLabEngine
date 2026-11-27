"""Regenerate the full matched-pair census from independent incidence masks."""
from collections import Counter
from functools import cache
from hashlib import sha256
from itertools import combinations, product
import json
from pathlib import Path
import sys


def root_forms(n):
    def shape(p,x):
        return tuple(sorted(shape(p,j) for j in range(1,n) if p[j]==x))
    reps={}
    for parents in product(*(range(v) for v in range(1,n))):
        p=(-1,)+parents
        reps.setdefault(shape(p,0),p)
    return reps.values()


def union(seq):
    out=0
    for x in seq:
        out |= x
    return out


def candidates(p):
    size=len(p)
    all_sites=(1<<size)-1
    views=[v for v in range(1,all_sites+1,2) if all(v & (1<<p[x]) or not v & (1<<x) for x in range(1,size))]
    leaves=[x for x in range(1,size) if x not in p]
    kids=[sum(1<<j for j in range(1,size) if p[j]==i) for i in range(size)]

    @cache
    def cover(s):
        options=[(len(group),union(group)) for k in range(len(s)+1) for group in combinations(s,k)]
        return tuple(min(k for k,u in options if u & child == child) for child in kids)

    for k in range(1,min(4,len(views))+1):
        for s in combinations(views,k):
            if union(s)!=all_sites:
                continue
            holders={x:frozenset(i for i,v in enumerate(s) if v & 1<<x) for x in leaves}
            for x,y in combinations([x for x in leaves if len(holders[x])==3],2):
                if holders[x]==holders[y]:
                    continue
                for a in sorted(holders[x] & holders[y]):
                    u=s[:a]+(s[a]^(1<<x),)+s[a+1:]
                    v=s[:a]+(s[a]^(1<<y),)+s[a+1:]
                    old,l,r=map(cover,(s,u,v))
                    def fields(x,q):
                        return old[p[x]],q[p[x]],max(1,*old),max(1,*q),q[p[x]]>old[p[x]]
                    if fields(x,l)!=fields(y,r):
                        continue
                    before={tuple(sorted(h)) for h in holders.values() if len(h)==2 and a not in h}
                    left=before | {tuple(sorted(holders[x]-{a}))}
                    right=before | {tuple(sorted(holders[y]-{a}))}
                    yield [p,s,a,x,y,sorted(before),sorted(left),sorted(right)]


def digest(items):
    return sha256((json.dumps(sorted(items),separators=(",",":"))+"\n").encode()).hexdigest()


def main(path):
    rows=[r for n in range(1,6) for p in root_forms(n) for r in candidates(p)]
    hits=[r for r in rows if len(r[5])<3 and sorted((len(r[6]),len(r[7])))==[2,3]]
    native=json.loads(path.read_bytes())
    assert native["matched"]==len(rows) and native["matched_sha256"]==digest(rows)
    assert native["triangle_sha256"]==digest(hits)
    assert json.loads(json.dumps(sorted(hits)))==native["triangle_pairs_complete"]
    assert digest(hits[1:]+hits[1:2])!=digest(hits)
    wrong=[r.copy() for r in hits]
    wrong[0][6],wrong[0][7]=wrong[0][7],wrong[0][6]
    assert digest(wrong)!=digest(hits)
    classes=Counter((len(r[0]), len(r[1]), sum(1 for x in range(1,len(r[0])) if x not in r[0])) for r in hits)
    example=native["example"]
    assert example["relabelings"]==576 and [len(s["edges"]) for s in example["stages"]]==[2,2,3]
    assert [s["word_pair_counts"][2][1:] for s in example["stages"]]==[[3,80,80],[3,80,80],[3,80,47]]
    return dict(matched=len(rows),triangle_pairs=len(hits),matched_sha256=digest(rows),triangle_sha256=digest(hits),
                sites_charts_leaves=[[a,b,c,n] for (a,b,c),n in sorted(classes.items())])


if __name__=="__main__":
    print(json.dumps(main(Path(sys.argv[1])),sort_keys=True,indent=2))
