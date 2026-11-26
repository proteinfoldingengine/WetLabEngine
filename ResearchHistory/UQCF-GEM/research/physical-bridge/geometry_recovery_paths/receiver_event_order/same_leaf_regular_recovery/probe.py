from collections import Counter
from fractions import Fraction
from itertools import combinations
from importlib.util import spec_from_file_location,module_from_spec
import hashlib,json,os
from pathlib import Path
import sys

def main(checkout):
    os.chdir(checkout)
    p=Path("ResearchHistory/UQCF-GEM/research/physical-bridge/forced_parent_deletion/check_geometry_repair.py")
    b=p.read_bytes()
    assert hashlib.sha1(b"blob "+str(len(b)).encode()+b"\0"+b).hexdigest()=="3324c0b46e09120ae526338444a19070b692d049"
    spec=spec_from_file_location("hist",p)
    hist=module_from_spec(spec);spec.loader.exec_module(hist)
    m=hist.modules()
    F,target=hist.fixture()
    par, g, _=map(tuple,zip(*F))
    sizes=len(par); n=len(hist.LABELS)
    T,U,A,B=hist.T,hist.ULEAF,hist.A,hist.B
    assert F[T][2] == hist.ALL-F[U][2]
    sub=list(g)
    for i in range(sizes-1,0,-1):sub[par[i]]+=sub[i]
    assert sub[T]==sub[U]==2
    sq=[x*x for x in sub]
    before=hist.initial_state(F)
    def remove(state,chart,leaf):
        d=m["atom"].atomic(par,state,chart,leaf)
        m["verify"].verify_atomic(d)
        return tuple(map(tuple,d["after"]))
    after=remove(before,A,T)
    mu=hist.MU
    W0=hist.work_for(before,sq)
    W1=hist.work_for(after,sq)
    assert W0==target
    labels=hist.LABELS
    def construct(w):
        _, near=hist.edges(w)
        p=m["projection"].Payload(hist.SIDE,Fraction(1),labels,tuple(tuple(map(Fraction,row)) for row in w),near,())
        return m["carriers"].build_carrier(p)
    def checkresponse(state,w):
        coords=tuple(tuple(sub[j] if j in v else 0 for j in range(1,sizes)) for v in map(set,state))
        geo=m["work"].construct_response_geometry(labels,coords,coords)
        assert geo.work==w and m["work"].metric_passes(geo)
        return geo
    rows=list(map(set,after)); support=Counter(j for row in rows for j in row)
    degree=Counter(i for e in hist.edges(W1)[1] for i in e)
    augmented=[]
    count=Counter()
    for i,r in enumerate(rows):
        active_parents={par[v] for v in r}
        for j in range(1,sizes):
            if j in r:
                ds=-1
                if j in active_parents or support[j]<2:continue
            else:
                ds=+1
                if par[j] not in r:continue
            count[ds]+=1
            d=degree.copy()
            for z in hist.ALL-{i}:
                c=W1[i][z]+ds*sq[j]*(1-2*int(j in rows[z]))
                if c<mu:break
                change=int(c==mu)-int(W1[i][z]==mu)
                d[i]+=change;d[z]+=change
            else:
                if all(d[k]==4 for k in labels):augmented.append((i,j,ds))
    def toggle(state,i,j):
        s=list(map(set,state));s[i]^={j}
        out=tuple(tuple(sorted(r)) for r in s)
        if j in state[i]: assert remove(state,i,j)==out
        else: assert remove(out,i,j)==state
        return out
    def effect(carrier):
        field=tuple(Fraction(i==A)-Fraction(1,n) for i in labels)
        f=m["application"].evaluate_field(carrier,field)
        return str(next(v for face,_,v in f.records if set(face)==set(hist.FACE)))
    K=[()]
    for j in range(1,sizes):K.append(K[par[j]]+(j,))
    lin=m["lineage"]; X=lin.Carrier("source-leaf-transfer",tuple(K))
    def P1(state):
        Y=lin.Carrier(X.genesis,tuple(K[j] for j in state[B]))
        x=lin.Pruning(X,Y).aggregate(g)
        rec=dict(zip(state[B],x))
        return [str(rec[0]),str(rec.get(T,"absent")),str(rec.get(U,"absent"))]
    recap={}; full_atlas={}
    for name,state in [('prior',before),('just-source',after),('no-source-acquire',toggle(before,B,T)),*[(f'{i},{j},{d}',toggle(after,i,j)) for i,j,d in augmented]]:
        w=hist.work_for(state,sq)
        entry={'degree':sorted(Counter(x for pair in hist.edges(w)[1] for x in pair).items()),'A-B':w[A][B],'rec':P1(state),'min':hist.edges(w)[0]}
        try:
            c=construct(w)
        except ValueError as e:
            entry['call']=str(e)
        else:
            checkresponse(state,w)
            entry['call']='ADMITTED'
            entry['effect']=effect(c)
            full_atlas[name]=c
        recap[name]=entry
    alt=hist.work_for(toggle(after,B,T),sq)
    old=hist.work_for(toggle(after,B,U),sq)
    diffs=[(i,j,old[i][j],alt[i][j]) for i,j in combinations(labels,2) if old[i][j]!=alt[i][j]]
    swap={A:B,B:A}
    assert alt==tuple(tuple(W0[swap.get(i,i)][swap.get(j,j)] for j in labels) for i in labels)
    assert diffs==[(0,12,1990,1998)]
    old_c,new_c=(full_atlas[k] for k in ('12,2,-1','12,1,1'))
    same_inputs=('labels','neighbors','adjacency','cycles','directed_edges','direction_classes','tangent_rank','local_vectors','d4_actions')
    assert all(getattr(old_c.complex,k)==getattr(new_c.complex,k) for k in same_inputs)
    assert old_c.baseline==new_c.baseline
    print(json.dumps({'all_field_inputs_match':same_inputs,'same_baseline':True,'gain_metric_is_exact_swap':True,'count':count,'degree_candidates':augmented,'report':recap,'alt_vs_old':diffs},sort_keys=True))
if __name__=='__main__':
    main(Path(sys.argv[1]).resolve())
