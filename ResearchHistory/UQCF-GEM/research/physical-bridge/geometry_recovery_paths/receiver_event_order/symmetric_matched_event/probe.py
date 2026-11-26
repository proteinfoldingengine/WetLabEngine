"""Exploratory check of role covariance and matched first-event response; not CI evidence."""
import hashlib, json, sys
from collections import Counter
from fractions import Fraction
from itertools import product, combinations
from pathlib import Path

R=Path(sys.argv[1]) if len(sys.argv)>1 else Path('/workspace/shared/uqcf-one-leaf-regular/reference/ResearchHistory/UQCF-GEM/demos')
core=R/'v15.42-duality-covariant-transport-repair'
app=R/'v15.43-certified-response-geometry'
for folder,name,sha in [(core,'operational_complex.py','8163beba8e52bc2a3a6d0c8cf59dd1257222f65c'),(app,'carriers.py','5cd286b014bb44025e16832ee91a6e6665291c8c'),(app,'application.py','30348d71d366a751932ec2d58d18a9148d81ae83')]:
    raw=(folder/name).read_bytes()
    assert hashlib.sha1(f'blob {len(raw)}\0'.encode()+raw).hexdigest()==sha
sys.path[:0]=[str(app),str(core)]
from carriers import build_carrier
from projection import Payload
from application import evaluate_field

L=11
P=tuple(range(L*L))
A,B,C=0,36,41
step=((1,0),(-1,0),(0,1),(0,-1))
pairs=tuple(combinations(P,2))
full=(1<<len(P))-1
def xy(i): return i%L,i//L
def idx(x,y): return x%L+L*(y%L)
def moved(i,dx,dy):
    x,y=xy(i)
    return idx(x+dx,y+dy)
def orbit(i, tx,ty,swap,sx,sy):
    x,y=xy(i)
    if swap:x,y=y,x
    return idx(sx*x+tx,sy*y+ty)
def dtype(i,j):
    return tuple(sorted(min(abs(a-b),L-abs(a-b)) for a,b in zip(xy(i),xy(j))))
nbr=tuple(frozenset(moved(i,*s) for s in step) for i in P)
def outer(i): return set().union(*(nbr[j] for j in nbr[i]))-{i}
def mandatory(i,j):
    return {i}|set(nbr[i])|outer(i)|{v for v in P if dtype(i,v) in {(2,3),(3,4)} and v not in nbr[j]|{j}}
S=mandatory(A,B); Q=mandatory(B,A)
assert not S&Q and len(set(nbr))==len(P)
def mask(xs): return sum(1<<x for x in xs)
transforms=tuple(product(range(L),range(L),(0,1),(-1,1),(-1,1)))
leaf_list=[mask(orbit(i,*t) for i in S) for t in transforms]
mB=mask(S); mC=mask(orbit(i,0,0,0,-1,1) for i in S)
assert B!=C and all(A in [i for i in P if m>>i&1] for m in (mB,mC))
def offset(i,j):
    d=dtype(i,j)
    return 0 if d==(0,1) else 12 if d==(0,2) else 4 if d in {(2,3),(3,4)} else 16 if d in {(1,3),(3,5)} else 8
D={(i,j):sum(4 for m in leaf_list if ((m>>i)^(m>>j))&1) for i,j in pairs}
assert len({(dtype(i,j),v) for (i,j),v in D.items()})==len({dtype(i,j) for i,j in pairs})
K=9
pair_w={ij:K-(offset(*ij)-w)//2 for ij,w in D.items()}
assert all(v>0 for v in pair_w.values())
combined=Counter()
for (i,j),v in pair_w.items(): combined[i]+=v; combined[j]+=v
S0=max(combined.values())+1
singleton={i:S0-combined[i] for i in P}
assert len(set(singleton.values()))==1 and min(singleton.values())>0
mu=2*S0-2*K
base=[[0]*len(P) for _ in P]
for i,j in pairs:
    # Sum of D, both singletons and every pair cut with exactly one endpoint:
    base[i][j]=base[j][i]=D[i,j]+singleton[i]+singleton[j]+combined[i]+combined[j]-2*pair_w[i,j]
    assert base[i][j]==mu+offset(i,j)
def build(w):
    mat=tuple(tuple(map(Fraction,row)) for row in w)
    neighbors=tuple((i,j) for i,j in pairs if w[i][j]==mu)
    return build_carrier(Payload(L,Fraction(1),P,mat,neighbors,()))
def change(w,i,m,sign,weight=4):
    assert bool(m>>i&1)==(sign==-1)
    dst=[row.copy() for row in w]
    for j in P:
        if i!=j: dst[i][j]=dst[j][i]=w[i][j]+weight*sign*(1-2*((m>>j)&1))
    return dst
def admit_return(j,m):
    w1=change(base,A,m,-1)
    support_after=m^(1<<A)
    found=[a for a in P if nbr[a]==frozenset(k for k in P if w1[A][k]==mu)]
    assert found==[j]
    try: build(w1)
    except ValueError as e: assert str(e)=='degree_not_four',str(e)
    else: raise AssertionError('source-only admitted')
    assert support_after.bit_count()>0 and not support_after>>j&1
    w2=change(w1,j,support_after,1)
    out=build(w2)
    flip=lambda i: j if i==A else A if i==j else i
    assert all(frozenset(out.complex.adjacency[i])==frozenset(flip(k) for k in nbr[flip(i)]) for i in P)
    rejected=Counter(); modes=Counter(); accepted_masks=set()
    actual_leaves=leaf_list.copy();actual_leaves.remove(m);actual_leaves.append(support_after)
    rows=set(actual_leaves)
    for n in rows:
        # Only grade-2 edits can bring the four old A neighbors down to μ.
        sign=1-2*((n>>j)&1)
        if not all((w1[j][k]+4*sign*(1-2*((n>>k)&1))==mu)==(k in nbr[A]) for k in P if k not in (A,j)):
            continue
        if w1[j][A]+4*sign*(1-2*((n>>A)&1))==mu:
            continue
        try: possible=build(change(w1,j,n,sign))
        except ValueError as err:
            rejected[str(err)]+=1;continue
        accepted_masks.add((n,sign));modes[sign]+=1
    assert (support_after,1) in accepted_masks
    values=tuple(Fraction(i==A)-Fraction(1,len(P)) for i in P)
    field=evaluate_field(out, values)
    return {"actor":j,"modes_distinct_masks":modes,"rejected_after_degree":rejected,"cycle_count":len(out.complex.cycles),"field_nonzero":field.nonzero_count,"known_same_leaf_gain":True,"B_Pin_change":-2 if j==B else 0}
start=build(base)
summary={
    "charts":len(P),"source_atoms":len(leaf_list),"unique_source_masks":len(set(leaf_list)),
    "support_size":len(S),"mandatory_opposed_size":len(Q),
    "mu":mu,"pair_weight_range":(min(pair_w.values()),max(pair_w.values())),
    "symmetry_order":len(start.complex.metric_automorphisms),
    "same_prior_two_events":[admit_return(B,mB),admit_return(C,mC)]
}
print(json.dumps(summary,sort_keys=True))
