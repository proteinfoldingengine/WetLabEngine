"""Exact grounded fields, old-port response, and allowed weak-history drift."""
import gzip
import itertools
import json
import sys
from fractions import Fraction
from pathlib import Path
import sympy as sp
import check_routed_chain as chain
import check_fixed_donor as fixed

def vertices(mask, n):
    return tuple(v for v in range(n) if mask & (1 << v))

def local_tree(parents, view):
    return (-1,) + tuple(view.index(parents[v]) for v in view[1:])

def full_laplacian(parents, view):
    edges = sp.zeros(len(view)-1, len(view))
    for i, v in enumerate(view[1:]):
        edges[i, i+1] = 1
        edges[i, view.index(parents[v])] = -1
    return edges.T * edges

def cuts(parents):
    mat = sp.zeros(len(parents)-1,len(parents))
    for v in range(1,len(parents)):
        u = v
        while u:
            mat[u-1,v]=1
            u = parents[u]
    return mat

def push(p, view, g, src):
    return src.push(p, tuple(range(len(p))), view, tuple(Fraction(x) for x in g))

def fields(p, view, g, green, src):
    y = push(p,view,g,src)
    q = local_tree(p,view)
    inv = green.candidate(q)
    assert inv * green.root_laplacian(q) == sp.eye(len(view)-1)
    phi = {v:t for v,t in zip(view,[0]+list(inv*sp.Matrix(y[1:])))}
    grad = {v:phi[v]-phi[p[v]] for v in view[1:]}
    ref = cuts(p)*sp.Matrix(g)
    assert all(val==ref[v-1] for v,val in grad.items())
    assert all((phi[v]+13)-(phi[p[v]]+13)==val for v,val in grad.items())
    return grad

def energy(grad):
    return sum(sp.Rational(1,2)*x*x for x in grad.values())

def port_test(p, coarse, fine, green, src):
    assert set(fine)-set(coarse)=={9} and p[9]==0
    ordered=coarse+(9,)
    full=full_laplacian(p,ordered)
    reduced=full[:-1,:-1]-full[:-1,-1:]*full[-1:,:-1]/full[-1,-1]
    assert reduced==full_laplacian(p,coarse)
    # Grounded response matrices independently use native common-ancestor formula.
    fine_green=green.candidate(local_tree(p,ordered))
    coarse_green=green.candidate(local_tree(p,coarse))
    assert fine_green[:-1,:-1]==coarse_green
    assert full[1:,1:]*fine_green==sp.eye(len(ordered)-1)
    # On the newly resolved edge, a balanced root-to-leaf drive has unit drop.
    # Every old coordinate in the grounded response has zero such drive.
    drive=fine_green[:,-1]
    assert list(drive)==[0]*(len(ordered)-2)+[1]
    def resistance(G,i,j):
        get=lambda a,b:G[a-1,b-1] if a and b else 0
        return get(i,i)+get(j,j)-2*get(i,j)
    pairs=list(itertools.combinations(range(len(coarse)),2))
    assert all(resistance(fine_green,i,j)==resistance(coarse_green,i,j) for i,j in pairs)
    # A balanced arbitrary load is handled linearly; test a spanning family.
    for k in range(1,len(ordered)):
        load=tuple(int(i==k)-int(i==0) for i in range(len(ordered)))
        folded=src.push(p,ordered,coarse,load)
        rhs=sp.Matrix(load[:-1])-full[:-1,-1:]*load[-1]/full[-1,-1]
        assert rhs==sp.Matrix(folded)
    return len(pairs)

def case_test(index, path, p, green, src):
    n=len(p)
    full=tuple(range(n))
    def chart(step,j):return vertices(path[step][j],n)
    c0,c1=chart(4,2),chart(5,2)
    ports=port_test(p,c0,c1,green,src)+port_test(p,chart(4,3),chart(3,3),green,src)
    unchanged=[chart(4,j) for j in (0,1,3)]
    assert all(chart(5,j)==chart(4,j) for j in (0,1,3))
    free=sorted(set(full)-set.union(*(set(v) for v in unchanged)))
    # Independent exact W1 constraints, stacked from native projected unit sources.
    bases=list(sp.eye(n).columnspace())
    rows=sp.Matrix.vstack(*(sp.Matrix.hstack(*(sp.Matrix(push(p,y,b,src)) for b in bases)) for y in unchanged))
    kernel=rows.nullspace()
    drift=cuts(p)*sp.Matrix.hstack(*kernel)
    assert drift.rank()==len(free)
    assert [v for v in range(1,n) if any(drift[v-1,:])]==free
    g=[2]*n
    shift=g.copy()
    shift[9]+=Fraction(1,2);shift[0]-=Fraction(1,2)
    observed=[]
    for name,source in [('base',g),('shifted',shift),('zero',[0 if v==9 else 2 for v in full]),
                        ('signed',[-1 if v==9 else 2 for v in full])]:
        pre=fields(p,chart(4,1),source,green,src)
        post=fields(p,chart(5,1),source,green,src)
        c=fields(p,c1,source,green,src)
        assert pre[9]==post[9]==c[9]==source[9]
        observed.append([name,str(pre[9]),str(post[9]),str(c[9]),str(c[9]**2/2)])
    # Exact positive alternative at C's gain, fixing the prior history.
    varied=g.copy()
    for v in (4,6):
        assert v in free
        varied[v]-=1;varied[p[v]]+=1
    assert min(varied)>0
    assert all(push(p,y,g,src)==push(p,y,varied,src) for y in unchanged)
    pre=fields(p,c0,g,green,src)
    cg=fields(p,c1,g,green,src);cv=fields(p,c1,varied,green,src)
    ambient=fields(p,full,g,green,src);alternate=fields(p,full,varied,green,src)
    delta=energy(alternate)-energy(ambient)
    assert {v for v in alternate if alternate[v]!=ambient[v]}=={4,6}
    assert cg[9]==cv[9]==2 and delta==-3
    assert energy(cg)-energy(pre)==2 and energy(cv)-energy(pre)==-1
    return dict(case=index,old_port_pairs=ports,free_gradient_edges=free,weak_increment_rank=len(kernel),
                edge9=[dict(zip(['input','B_before','B_after','C_after','C_edge_term'],row)) for row in observed],
                C_energy=[int(energy(x)) for x in (pre,cg,cv)],ambient_energy_change=[0,int(delta)])

def main():
    fixed.pins()
    raw=(chain.DEMOS/chain.ARCHIVE).read_bytes()
    assert fixed.blob(raw)==chain.PINS[chain.ARCHIVE]
    gpath="v16.22-response-selection-closure/engine.py"
    assert fixed.blob((chain.DEMOS/gpath).read_bytes())==chain.PINS[gpath]
    src=chain.module("v16.23-overlap-descent/engine.py","edge_source")
    green=chain.module(gpath,"edge_green")
    sys.path.insert(0,str(chain.DEMOS/chain.OLD))
    import producer,verifier
    arch=json.loads(gzip.decompress(raw))["corpus"]
    assert producer.produce(domain=())["corpus"]==arch
    result=[]
    for ix in (178,184,190):
        row=arch[ix];p=tuple(verifier.structure(row["spec"]["degrees"]))
        result.append(case_test(ix,row["path"],p,green,src))
    print(json.dumps(dict(cases=result,old_pair_tests=sum(row["old_port_pairs"] for row in result),
                          bridge="OPEN"),indent=2,sort_keys=True))

if __name__=="__main__":
    main()
