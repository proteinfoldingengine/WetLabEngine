"""Four-child incidence census, with chart labels interpreted only for counting."""
from collections import Counter
from functools import lru_cache
from itertools import combinations, combinations_with_replacement, permutations, product
from math import comb
import json

PERMS=tuple(permutations(range(4)))
def permute(mask,p):
    return sum(1<<p[i] for i in range(4) if mask>>i&1)
MAPS={p:tuple(permute(i,p) for i in range(16)) for p in PERMS}
@lru_cache(maxsize=200000)
def q(types):
    best={0:0}
    for row in types:
        for s,n in list(best.items()):
            best[s|row]=min(best.get(s|row,5),n+1)
    return best.get(15,5)
def ranks(rows):
    return q(tuple(sorted(set(rows))))

def arms(rows,a):
    out={}
    for i in range(4):
        if rows[a]>>i&1 and any(s>>i&1 for b,s in enumerate(rows) if a!=b):
            cut=list(rows);cut[a]^=1<<i
            out[i]=ranks(cut)
    return [(i,j) for i in out for j in out if out[i]==2 and out[j]==3]

def symmetry(rows,a,b):
    bag=Counter(rows)
    perms=[p for p,t in MAPS.items() if Counter(t[r] for r in rows)==bag]
    fixed=lambda i:bag[rows[i]]==1 and all(MAPS[p][rows[i]]==rows[i] for p in perms)
    return fixed(a),fixed(b),perms

def evaluate(rows,a,pairs,counts,examples):
    for s,t in pairs:
        counts['source_pairs']+=1
        widths=[sum(r>>i&1 for r in rows)-(i in (s,t)) for i in range(4)]
        minimum=min(widths)
        for b,r in enumerate(rows):
            if a==b:continue
            counts['remote_instances']+=1
            degree=r.bit_count()
            counts['degree_'+str(degree)]+=1
            assert degree<=2
            equal=(r>>s&1)==(r>>t&1)
            if minimum>=2:counts['all_post_widths_ge2']+=1
            if equal:counts['equal_receiver_work']+=1
            af,bf,group=symmetry(rows,a,b)
            flags={'basic':True,
                   'fixed':af and bf,
                   'protected':minimum>=2 and af and bf,
                   'strong':minimum>=2 and af and bf and degree==2 and equal,
                   'neither':minimum>=2 and af and bf and degree==2 and not (r>>s&1 or r>>t&1)}
            for label,passed in flags.items():
                if passed and label not in examples:
                    examples[label]=dict(rows=rows,A=a,B=b,flat=s,cover=t,minimum=minimum,
                                         automorphisms=group,equal_work_row=equal)

def historical():
    result=[]
    for k in range(1,5):
        counts=Counter();examples={}
        cases=product(range(16),repeat=k) if k<4 else ([1<<i for i in p] for p in PERMS)
        for rows in cases:
            if ranks(rows)==5:continue
            counts['states']+=1
            for a in range(k):
                pairs=arms(rows,a)
                if pairs: evaluate(rows,a,pairs,counts,examples)
        result.append(dict(k=k,counts=counts,examples=examples))
    return result

def extension():
    # The q=3 arm implies every remote chart initially has degree <=2; its complement
    # can otherwise be covered by a single other chart. Require represented nonempty
    # remote charts here. Search chart multisets with source at physical index zero.
    small=[i for i in range(1,16) if i.bit_count()<=2]
    found=[]
    for k in range(4,8):
        counts=Counter();examples={}
        for a in range(1,16):
            if not 2<=a.bit_count()<=3:continue
            for others in combinations_with_replacement(small,k-1):
                rows=(a,*others)
                if ranks(rows)!=2:continue
                widths=[sum(r>>i&1 for r in rows) for i in range(4)]
                if min(widths)<2:continue
                pairs=[(s,t) for s,t in arms(rows,0) if min(widths[s],widths[t])>=3]
                if pairs:evaluate(rows,0,pairs,counts,examples)
        found.append(dict(k=k,counts=counts,examples=examples))
        if 'strong' in examples:break
    return found

if __name__=='__main__':
    print(json.dumps(dict(historical=historical(),extension=extension()),sort_keys=True))
