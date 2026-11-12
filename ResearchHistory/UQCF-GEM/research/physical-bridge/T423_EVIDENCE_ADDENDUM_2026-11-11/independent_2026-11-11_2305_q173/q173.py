import sys, random, itertools; sys.dont_write_bytecode=True
import sympy as sp
F=sp.Rational; random.seed(173)
def info(par):
    dep={};anc={}
    for v in par:
        ch=[v];u=v
        while par[u] is not None: u=par[u]; ch.append(u)
        ch=ch[::-1]; dep[v]=len(ch)-1; anc[v]=ch
    return dep,anc
def mass(par,x):
    dep,_=info(par); m={v:x.get(v,0) for v in par}
    for v in sorted(par,key=lambda v:-dep[v]):
        if par[v] is not None: m[par[v]]+=m[v]
    return m
eps=F(1,100)
def make(psi,bad=False):
    def Gam(d,mc,ancm,x,par):
        if mc==0: return 0
        if d==1: return mc
        if bad:
            root=[v for v in par if par[v] is None][0]; Mt=sum(x.values())
            return mc*(1+eps*psi(mc/Mt - x[root]))
        return mc*(1+eps*psi(mc/ancm[-1]))
    def f(par,x):
        dep,anc=info(par); m=mass(par,x); root=[v for v in par if par[v] is None][0]
        w={v:0 for v in par}; w[root]+=m[root]
        for c in par:
            q=par[c]
            if q is None: continue
            e=Gam(dep[c],m[c],[m[a] for a in anc[c][:-1]],x,par); w[c]+=e; w[q]-=e
        return w
    return f
def P(par,Y,x):
    out={v:0 for v in Y}
    for v in par:
        u=v
        while u not in Y: u=par[u]
        out[u]+=x.get(v,0)
    return out
def prefixes(par):
    vs=[v for v in par if par[v] is not None]; root=[v for v in par if par[v] is None][0]
    for r in range(len(vs)+1):
        for S in itertools.combinations(vs,r):
            Y=set(S)|{root}
            if all(par[v] in Y for v in S): yield Y
def P1_check(f,par,x):
    fx=f(par,x); bad=0
    for Y in prefixes(par):
        pY={v:par[v] for v in Y}; lhs=f(pY,P(par,Y,x)); rhs=P(par,Y,fx)
        bad+=sum(1 for v in Y if sp.simplify(lhs[v]-rhs[v])!=0)
    return bad
def I_check(f,par,x):
    bad=0
    for q in list(par):
        for ext in ({'z1':q},{'z1':q,'z2':'z1'}):
            p2=dict(par); p2.update(ext); a=f(p2,x); b=f(par,x)
            bad+=sum(1 for v in p2 if sp.simplify(a[v]-b.get(v,0))!=0)
    return bad
psiA=lambda r:16*r-7
C={'o':None,'p':'o','u':'p','v':'p','w':'u','s':'o'}
for name,psi,bad in (('candidate',psiA,False),('control-bad',psiA,True)):
    f=make(psi,bad); tot=[0,0]
    for k in range(5):
        x={v:F(random.randint(1,9),random.randint(1,9)) for v in C}
        tot[0]+=P1_check(f,C,x); tot[1]+=I_check(f,C,x)
    print(name,'P1 residual count',tot[0],'I residual count',tot[1])
f=make(psiA); x=dict(o=F(3,7),p=F(1,3),u=F(2,9),v=F(1,2),w=F(5,4),s=F(1,6)); t=F(7,3)
xt={k:t*v for k,v in x.items()}; print('homogeneity residual',[sp.simplify(f(C,xt)[v]-t*f(C,x)[v]) for v in C])
Csw={'o':None,'p':'o','v':'p','u':'p','w':'v','s':'o'}  # relabel u<->v (w moves under v) check by mapping
T={'o':None,'p':'o','u':'p','v':'p'}
xp=dict(o=F(1,5),p=F(1,5),u=F(2,5),v=F(1,5)); xm=dict(o=F(1,5),p=F(1,5),u=F(1,5),v=F(2,5))
for nm,ps in (('psi=16r-7',psiA),('reverse psi(r)=-4r+1 [psi(1/2)=-1? see below]',lambda r: 8*r-3)):
    f=make(ps)
    for lab,x in (('x+',xp),('x-',xm)):
        w=f(T,x); print(nm,lab,'f=',[w[k] for k in 'opuv'],'fixed:',w['p']*x['u']==w['u']*x['p'])
