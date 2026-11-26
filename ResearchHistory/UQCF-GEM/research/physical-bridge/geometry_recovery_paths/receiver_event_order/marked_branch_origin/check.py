"""Replay the original producer and P1 on all ordered presentations."""
from argparse import ArgumentParser
from collections import Counter
from itertools import permutations,product
import json
from pathlib import Path
import sys

sys.path.insert(0,str(Path(__file__).resolve().parent.parent/'endogenous_junction'))
from historical import History, positions, move

C={'Pin','P','Q','X1','X2','Y1','Y2'}
R={'Pin','P','Q','A','B','b1','b2'}
def flat(x):
    return [x[0]]+[v for y in x[1] for v in flat(y)]
def shape(x):
    return tuple(map(shape,x[1]))
def main(hist):
    H=History(Path(hist).resolve()); rows=[]
    for pp,qq,sw,rid,bs in product(permutations(('X1','X2','A')),permutations(('Y1','Y2','B')),range(2),range(2),range(2)):
        p=('P',[(v,[]) for v in pp])
        bnames=('b2','b1') if bs else ('b1','b2')
        s=('Q',[(v,[(w,[]) for w in bnames] if v=='B' else []) for v in qq])
        tree=('Pin',[s,p] if sw else [p,s])
        n=flat(tree); t=shape(tree); children=H.p.layout(t); parents=H.parents(t)
        q=tuple({'Pin':1,'P':2,'Q':2,'B':1}[v] for v in n if v in ('Pin','P','Q','B'))
        allv=tuple(range(len(n)))
        start=tuple(sum(1<<n.index(v) for v in (R if i==rid else C)) for i in range(2))
        assert H.profile(t,start)==q
        fronts=sorted(H.moves(t,start).values())
        exact=[v for v in fronts if H.profile(t,v)==q]
        path=H.normalize(t,q,start)
        for a,z in zip(path,path[1:]):
            assert H.moves(t,a).get(move(a,z))==z
        totals=[]
        for s in range(2):
            fixed={'Pin':80,'P':24,'Q':28,'A':2,'B':6,'b1':2,'b2':2}
            totals.append(tuple(fixed[v] if v in fixed else (1+7*s if v.startswith('X') else 8-7*s) for v in n))
        def rec(a,tot):
            fine=[x-sum(tot[c] for c in children[i]) for i,x in enumerate(tot)]
            assert min(fine)>0
            sites=positions(a[rid],len(n))
            return tuple(zip(sites,map(int,H.p1.push(parents,allv,sites,fine))))
        proof=[(a, [rec(a,p) for p in totals]) for a in path]
        exact_out=[(a, [rec(a,p) for p in totals]) for a in exact]
        rows.append(dict(order=n,receiver=rid,profile=q,prior=start,first_legal=fronts,exact=exact_out,path=proof))
    return rows
if __name__=='__main__':
    p=ArgumentParser()
    p.add_argument('historical');p.add_argument('--raw', required=True)
    a=p.parse_args()
    rows=main(a.historical)
    Path(a.raw).write_text(json.dumps(rows,separators=(',',':'),sort_keys=True)+'\n')
    print(json.dumps({'rows':len(rows)},sort_keys=True))
