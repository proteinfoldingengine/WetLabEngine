# Q173 relabeling-naturality addendum (exact rationals). Reuses make()/prefixes()/P() from q173.py unchanged (defs only, not its main checks).
import sys, os, random, itertools; sys.dont_write_bytecode=True
import sympy as sp
here=os.path.dirname(os.path.abspath(__file__))
src=open(os.path.join(here,'q173.py')).read().split("psiA=lambda")[0]
ns={}; exec(src,ns)
F=sp.Rational; make=ns['make']; prefixes=ns['prefixes']; eps=ns['eps']
random.seed(1731)
psis={'psi=16r-7':lambda r:16*r-7,'psi=8r-3':lambda r:8*r-3}
def relabel_res(f,par,x,pi,shuffle=True):
    # f(pi T, pi x)[pi v] - f(T,x)[v] for every vertex v; dict insertion order shuffled to expose order dependence
    items=list(par.items());
    if shuffle: random.shuffle(items)
    par2={pi[v]:(pi[q] if q is not None else None) for v,q in items}
    x2={pi[v]:x[v] for v,_ in items}
    a=f(par2,x2); b=f(par,x)
    return sum(1 for v in par if sp.simplify(a[pi[v]]-b[v])!=0)
def child_perms(par):
    # all rooted relabelings that permute the children of each vertex among themselves (sibling permutations), as vertex maps
    root=[v for v in par if par[v] is None][0]
    kids={v:[c for c in par if par[c]==v] for v in par}
    vs=list(par); per=[list(itertools.permutations(kids[v])) for v in vs]
    for choice in itertools.product(*per):
        pi={root:root}
        # sibling permutation: child kids[v][i] takes the label choice[i] (names are swapped, subtrees keep their own structure)
        for v,ch in zip(vs,choice):
            for a,b in zip(kids[v],ch): pi[a]=b
        if sorted(pi.values())==sorted(vs): yield pi
def renamings(par):
    root=[v for v in par if par[v] is None][0]; vs=[v for v in par if v!=root]
    for perm in itertools.permutations(vs):
        pi=dict(zip(vs,perm)); pi[root]=root; yield pi
C={'o':None,'p':'o','u':'p','v':'p','w':'u','s':'o'}
total_all=0
# (1) tree flux form, both psi witnesses: every prefix subtree of C x 5 seeded rational grades x (all sibling permutations + all non-root renamings)
for nm,ps in psis.items():
    f=make(ps); cnt=0; res=0
    for k in range(5):
        x={v:F(random.randint(1,9),random.randint(1,9)) for v in C}
        for Y in prefixes(C):
            pY={v:C[v] for v in Y}; xY={v:x[v] for v in Y}
            for pi in itertools.chain(child_perms(pY),renamings(pY)):
                res+=relabel_res(f,pY,xY,pi); cnt+=1
    print('flux',nm,'relabelings checked',cnt,'residual count',res); total_all+=res
# (2) frozen pair carrier T, both witnesses, x+ and x-: swap u<->v and all renamings
T={'o':None,'p':'o','u':'p','v':'p'}
xp=dict(o=F(1,5),p=F(1,5),u=F(2,5),v=F(1,5)); xm=dict(o=F(1,5),p=F(1,5),u=F(1,5),v=F(2,5))
for nm,ps in psis.items():
    f=make(ps); res=0; cnt=0
    for x in (xp,xm):
        for pi in itertools.chain(child_perms(T),renamings(T)): res+=relabel_res(f,T,x,pi); cnt+=1
    # swap u<->v maps x+ to x- : f(T,x-) must equal swapped f(T,x+)
    a=f(T,xp); b=f(T,xm); sw={'o':'o','p':'p','u':'v','v':'u'}
    res2=sum(1 for v in T if sp.simplify(b[sw[v]]-a[v])!=0)
    print('frozen',nm,'relabelings checked',cnt,'residual count',res,'| u<->v maps f(x+) to f(x-): residual',res2); total_all+=res+res2
# (3) star form: f_c = gamma(x_c,M) = x_c(1+eps*psi(x_c/M)), f_root = M - sum_c gamma; star with 4 leaves, all 24 leaf permutations
def star_f(ps):
    def f(par,x):
        root=[v for v in par if par[v] is None][0]; M=sum(x.values()); w={}
        for c in par:
            if c==root: continue
            w[c]=0 if x[c]==0 else x[c]*(1+eps*ps(x[c]/M))
        w[root]=M-sum(w.values()); return w
    return f
S={'o':None,'a':'o','b':'o','c':'o','d':'o'}
for nm,ps in psis.items():
    f=star_f(ps); res=0; cnt=0
    for k in range(5):
        x={v:F(random.randint(0,9),random.randint(1,9)) for v in S}
        for pi in child_perms(S): res+=relabel_res(f,S,x,pi); cnt+=1
    print('star',nm,'relabelings checked',cnt,'residual count',res); total_all+=res
# (4) rejecting control: a non-natural map (depends on the NAME of a child) must give nonzero relabel residuals
def bad(par,x):
    w=make(psis['psi=16r-7'])(par,x); k=sorted(v for v in par if par[v] is not None)
    if k: w[k[0]]+=F(1,1000)
    return w
cres=sum(relabel_res(bad,T,xp,pi) for pi in renamings(T))
print('control (name-dependent map) relabel residual count',cres,'(must be > 0)')
print('ALL_RELABEL_RESIDUALS_ZERO' if total_all==0 and cres>0 else 'RELABEL_CHECK_FAILED')
