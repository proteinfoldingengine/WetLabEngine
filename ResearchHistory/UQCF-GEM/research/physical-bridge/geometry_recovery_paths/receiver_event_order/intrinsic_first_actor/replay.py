"""Full-atlas recovery and anonymous first-action test on the frozen four cuts."""
from collections import Counter
from functools import lru_cache
from hashlib import sha1
from itertools import combinations, product
from math import comb
from pathlib import Path
import json
import runpy
import sys

N=121
LEAVES=968
PINS={
    'orbit.py':'45eaeb0df71e6f6a5d9e205332f3bc015fcb4c8b',
    'operational_complex.py':'8163beba8e52bc2a3a6d0c8cf59dd1257222f65c',
    'carriers.py':'5cd286b014bb44025e16832ee91a6e6665291c8c',
    'projection.py':'f857f2cf1cd4c265c193121236af8e441b1f01dc',
    'exact_algebra.py':'c67ea42b61321469f7735ce589f2e729b241666a',
    'graph_producer.py':'6c8eca570cda82b64c0d06775672f33977be430a',
    'producer.py':'ffd513619d182abea2b31bd90c38e12784557bf3',
}
RELEASE=((41,217,278,454),(91,157,338,404))
C=tuple(i for i in range(N) if (i//11-3*(i%11))%11==0)


def point(x,y):
    return x%11+11*(y%11)


def bitset(items):
    return sum(1<<i for i in items)


def members(mask):
    while mask:
        low=mask&-mask
        yield low.bit_length()-1
        mask-=low


def pair_data(rows):
    return tuple(tuple(4*(u^v).bit_count() for v in rows) for u in rows)


def chart_maps():
    for swap,sx,sy in product((False,True),(-1,1),(-1,1)):
        out=[]
        for i in range(N):
            x,y=i%11,i//11
            if swap:x,y=y,x
            out.append(point(sx*x,sy*y))
        yield tuple(out)


def map_support(m,g):
    return bitset(g[i] for i in members(m))


def source_cut(cols,rows,addresses):
    changed=cols.copy()
    for a in addresses:
        assert changed[a-1]&1 and changed[a-1].bit_count()==25
        changed[a-1] ^= 1
    state=rows.copy()
    state[0]^=bitset(a-1 for a in addresses)
    return changed,state


def recovery(cols,rows,baseline,addresses):
    damaged,state=source_cut(cols,rows,addresses)
    work=pair_data(state)
    near=[i for i in range(N) if baseline[0][i]==704]
    low=sorted(i for i in near if work[0][i]==688)
    high=sorted(i for i in near if work[0][i]==720)
    assert len(low)==len(high)==2
    four=low+high
    far=[point(2*(i%11),2*(i//11)) for i in four]
    diff=[(work[0][i]-baseline[0][i])//4 for i in far]
    pool=[]
    improves=0
    for k,m in enumerate(damaged):
        b=m&1
        def change(i):
            return (2*b-1)*(2*((m>>i)&1)-1)
        if all(change(i)==1 for i in low):
            improves+=1
            if all(change(i)==-1 for i in high):
                pool.append((k+1,tuple(change(i) for i in far)))
    accepted=[]
    rejected=None
    for group in combinations(pool,4):
        ids=[a for a,d in group]
        if all(diff[k]+sum(d[k] for _,d in group)==0 for k in range(4)):
            accepted.append(ids)
        elif rejected is None:
            rejected=ids
    assert accepted==[list(addresses)] and rejected
    return dict(low=low,high=high,strict_minimum_choices=improves,nearest_pool=len(pool),
                nearest_repair_endpoints=comb(len(pool),4),accepted=accepted,
                example_nearest_only=rejected)


def canonical(cols,rows,addresses,maps,images):
    changed,state=source_cut(cols,rows,addresses)
    deficient={a for a,m in enumerate(changed) if m.bit_count()==24}
    assert len(deficient)==4 and [i for i,r in enumerate(state) if r.bit_count()==196]==[0]
    assert [m|1 if k in deficient else m for k,m in enumerate(changed)]==cols
    cuts={cols[a-1] for a in addresses}
    stab=[g for g in maps if {images[g][m] for m in cuts}==cuts]
    counts=Counter(changed)
    fixed=[i for i in range(N) if all(g[i]==i for g in stab)]
    singles=[m for m,n in counts.items() if n==1 and all(map_support(m,g)==m for g in stab)]
    assert len(stab)==1 and len(fixed)==121 and len(singles)==8
    return dict(chart_stabilizer=len(stab),fixed_charts=len(fixed),
                fixed_leaf_addresses=[k+1 for k,m in enumerate(changed) if m in singles],
                invariant_removals=sum(m.bit_count() for m in singles),
                invariant_additions=sum(N-m.bit_count() for m in singles))


def line_actions(cols,rows,addresses,normalize):
    changed,state=source_cut(cols,rows,addresses)
    mask=bitset(C)
    restrictions=[s&mask for s in changed]
    hist=Counter(restrictions)
    assert 0 not in hist
    assert all(any(s==1<<i for s in restrictions) for i in C)
    isolates=[k for k,s in enumerate(restrictions) if hist[s]==1]
    assert len(isolates)==1
    k=isolates[0];holders=list(members(restrictions[k]))
    def first(actor,leaf):
        here=list(members(restrictions[leaf]))
        first_chart=next(j for j in here if j!=actor)
        order=[first_chart,actor]+[j for j in C if j not in (first_chart,actor)]
        leaf_order=[leaf]+[u for u in range(LEAVES) if u!=leaf]
        start=tuple(1+bitset(t+1 for t,u in enumerate(leaf_order) if state[i]>>u&1) for i in order)
        path=normalize(start,LEAVES,len(C),len(C))
        assert path[1][1]==start[1]^2 and path[1][0]==start[0] and tuple(path[1][2:])==start[2:]
    for r in holders:
        first(r,k)
    for r in C:
        leaf=next(i for i,s in enumerate(restrictions) if s>>r&1 and s.bit_count()>1)
        first(r,leaf)
    work=pair_data([state[i] for i in C])
    cheapest=min(work[a][b] for a,b in combinations(range(11),2))
    tight=[(C[a],C[b]) for a,b in combinations(range(11),2) if work[a][b]==cheapest]
    assert len(tight)==2 and set(tight[0])&set(tight[1])=={0}
    # Puncturing the unique hub leaves a path in the remaining minimum graph.
    sub=C[1:];m=min((state[a]^state[b]).bit_count() for a,b in combinations(sub,2))
    adj={a:[b for b in sub if b!=a and (state[a]^state[b]).bit_count()==m] for a in sub}
    path=[next(a for a in sub if len(adj[a])==1)]
    while following:=[a for a in adj[path[-1]] if a not in path]:
        assert len(following)==1
        path.append(following[0])
    assert len(path)==10 and any((state[0]^state[a]).bit_count()!=(state[0]^state[b]).bit_count()
                                  for a,b in zip(path,reversed(path)))
    return dict(unique_leaf=k+1,holders=holders,ordinary_possible_first_charts=len(C),
                minimum_edges=tight,punctured_path=path)


def first_source_order_distribution(cols):
    other=C[1:]
    @lru_cache(None)
    def solve(prefix):
        if prefix==bitset(other):
            return {(0,0):1}
        counts=Counter()
        for i in other:
            if prefix>>i&1:continue
            wins=[sum(bool(cols[a-1]>>i&1) and not bool(cols[a-1]&prefix) for a in arm) for arm in RELEASE]
            for (addressed,scalar),multiplicity in solve(prefix|(1<<i)).items():
                counts[addressed+int(sum(wins)>0),scalar+int(wins[0]!=wins[1])]+=multiplicity
        return counts
    return [[*key,v] for key,v in sorted(solve(0).items())]


def run(native,old_verify):
    for name,sha in PINS.items():
        data=(native/name).read_bytes()
        assert sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()==sha
    sys.path.insert(0,str(native))
    from projection import Payload
    from carriers import build_carrier
    from producer import normalize
    from fractions import Fraction
    o=runpy.run_path(str(native/'orbit.py'))
    cols,rows=o['orbit'],o['rows']
    base=pair_data(rows)
    maps=list(chart_maps())
    images={g:{m:map_support(m,g) for m in set(cols)} for g in maps}
    assert all(Counter(images[g][m] for m in cols)==Counter(cols) for g in maps)
    types=list(dict.fromkeys(m for m in cols if m&1))
    all_arms=[tuple(cols.index(types[i])+1 for i in p) for p,n in old_verify['directed_minimal_vectors']]
    assert len(all_arms)==len(set(all_arms))==8
    cases=[dict(addresses=a,recovery=recovery(cols,rows,base,a),symmetry=canonical(cols,rows,a,maps,images))
           for a in all_arms]
    states=[source_cut(cols,rows,a)[1] for a in RELEASE]
    W=pair_data(states[0]);assert W==pair_data(states[1])
    g_work=[g for g in maps if all(W[0][j]==W[0][g[j]] for j in range(N))]
    assert len(g_work)==2
    reflect=next(g for g in g_work if tuple(range(N))!=g)
    assert {images[reflect][cols[k-1]] for k in RELEASE[0]}=={cols[k-1] for k in RELEASE[1]}
    first=recovery(cols,rows,base,RELEASE[0])
    def check(state):
        work=pair_data(state)
        mu=min(work[i][j] for i,j in o['pairs'])
        links=tuple((i,j) for i,j in o['pairs'] if work[i][j]==mu)
        try:
            g=build_carrier(Payload(11,Fraction(1),tuple(range(N)),tuple(tuple(map(Fraction,row)) for row in work),links,()))
        except ValueError as e:
            return str(e)
        assert g.baseline.flat and g.complex.tangent_rank==2
        return 'accepted'
    gate={}
    gate['restored']=check(rows)
    gate['damaged']=check(states[0])
    bad=states[0].copy();bad[0]^=bitset(i-1 for i in first['example_nearest_only'])
    gate['nearest_only']=check(bad)
    # A remote-first path with six distinct toggles. Its terminal row differs in cardinality.
    six=states[0].copy()
    for leaf in (14,21):
        assert six[1]>>(leaf-1)&1
        six[1]^=1<<(leaf-1)
    six[0]^=bitset(k-1 for k in RELEASE[0])
    assert six[0]==rows[0] and six[1].bit_count()==198
    gate['remote_first_six']=check(six)
    assert list(gate.values())==['accepted','degree_not_four','opposites_ambiguous','accepted']
    return dict(cases=cases,metric_fixed_charts=[i for i in range(N) if reflect[i]==i],
                full_gate=gate,line=[line_actions(cols,rows,a,normalize) for a in RELEASE],
                source_first_orders=first_source_order_distribution(cols))


if __name__=='__main__':
    native=Path(sys.argv[1]).resolve()
    data = Path(sys.argv[2]).read_bytes()
    expected = '9d03f2c4075bd25172b3df1ab6f7b5697f2ed96f'
    if sha1(b'blob ' + str(len(data)).encode() + bytes(1) + data).hexdigest() != expected:
        raise ValueError('Unexpected parent minimum-trade certificate')
    old_verify = json.loads(data)
    print(json.dumps(run(native,old_verify),sort_keys=True,indent=2))
