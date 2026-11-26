"""Enumerate the historical finite star domain, reducing permutations of leaves and source charts."""
from collections import Counter
from functools import lru_cache
from itertools import combinations, combinations_with_replacement, permutations
from math import factorial, prod
import json

DOMAIN = [(m,k) for m in range(2,5) for k in range(2,5)] + [(5,2),(5,3)]

@lru_cache(None)
def cover_info(cols,k):
    hits = [h for h in range(1,1<<k) if all(h&s for s in cols)]
    q = min(h.bit_count() for h in hits)
    opts = [h for h in hits if h.bit_count()==q]
    every, some=(1<<k)-1,0
    for h in opts:
        every &= h
        some |= h
    return q,every,some

def remap(s,order):
    return sum(1<<order[i] for i in range(len(order)) if s & (1<<i))

@lru_cache(None)
def symmetries(cols,k):
    return [order for order in permutations(range(k)) if sorted(remap(s,order) for s in cols)==list(cols)]

def run(m,k):
    tally=Counter()
    witness={}
    for cols in combinations_with_replacement(range(1,1<<k),m):
        mult=Counter(cols)
        weight=factorial(m)//prod(factorial(x) for x in mult.values())
        tally['states']+=weight
        cuts=[]
        for i,s in enumerate(cols):
            if not s&1 or s==1:
                continue
            cut=tuple(sorted((*cols[:i],s^1,*cols[i+1:])))
            q,e,u=cover_info(cut,k)
            cuts.append((i,s,q,e,u,min(x.bit_count() for x in cut)))
        for arm,other in combinations(cuts,2):
            i,s,q,e,u,min_s=arm
            j,t,qt,et,ut,min_t=other
            if s==t or q!=qt:
                continue
            w=k*weight
            tally['eligible_source_pairs']+=w
            roles=(e&~ut | et&~u)&~1
            if not roles:
                continue
            tally['positive_source_pairs']+=w
            depth=min(min_s,min_t)
            pre_q,pre_all,_=cover_info(cols,k)
            assert pre_all&1
            for b in range(1,k):
                bit=1<<b
                if not roles & bit:
                    continue
                tally['positive_receiver_witnesses']+=w
                keep,lose=(i,j) if e&bit else (j,i)
                grp=symmetries(cols,k)
                fixed_b=all(p[b]==b for p in grp)
                fixed_a=all(p[0]==0 for p in grp)
                distinct=not any(p[0]==0 and remap(s,p)==t for p in grp)
                deg=lambda c:sum(bool(x & (1<<c)) for x in cols)
                flags={'all':True,'at_least_two':depth>=2,'pre_fixed_B':fixed_b,
                       'pre_fixed_A_B':fixed_b and fixed_a,'one_remote':roles.bit_count()==1,
                       'equal_A_B_degree':deg(0)==deg(b),'inequivalent_events':distinct,
                       'strong':depth>=2 and fixed_a and fixed_b and distinct,
                       'recognizable':fixed_a and fixed_b and distinct,
                       'recognizable_one_remote':fixed_a and fixed_b and distinct and roles.bit_count()==1,
                       'at_least_two_one_remote':depth>=2 and roles.bit_count()==1}
                for key,flag in flags.items():
                    if flag:
                        tally[key]+=w
                        witness.setdefault(key,dict(m=m,k=k,cols=cols,A=0,B=b,keep=keep,lose=lose,
                                                    original_q=pre_q,cut_q=q,min_post=depth,
                                                    roles=roles,group=grp))
    assert tally['states']==((1<<k)-1)**m
    return dict(m=m,k=k,tallies=dict(tally),examples=witness)

if __name__=='__main__':
    records=[run(m,k) for m,k in DOMAIN]
    pooled=Counter()
    for r in records:
        pooled.update(r['tallies'])
    print(json.dumps(dict(pooled=dict(pooled),cells=records),sort_keys=True))
