import sys; sys.dont_write_bytecode=True
import sympy as sp
F=sp.Rational
b,a10,a11,a20,a21,a22=sp.symbols('b a10 a11 a20 a21 a22')
A={(1,0):a10,(1,1):a11,(2,0):a20,(2,1):a21,(2,2):a22}
def depth(par,v): d=0
def info(par):
    dep={};anc={}
    for v in par:
        ch=[v];u=v
        while par[u] is not None: u=par[u]; ch.append(u)
        ch=ch[::-1]; dep[v]=len(ch)-1; anc[v]=ch
    return dep,anc
def mass(par,x):
    m={v:x.get(v,0) for v in par}
    dep,_=info(par)
    for v in sorted(par,key=lambda v:-dep[v]):
        if par[v] is not None: m[par[v]]+=m[v]
    return m
def f(par,x,A,bb):
    dep,anc=info(par); m=mass(par,x); root=[v for v in par if par[v] is None][0]
    w={v:0 for v in par}; w[root]+=bb*m[root]
    for c in par:
        q=par[c]
        if q is None: continue
        d=dep[c]
        e=sum(A.get((d,j),0)*m[anc[c][j]] for j in range(d+1))
        w[c]+=e; w[q]-=e
    return {v:sp.nsimplify(w[v]) for v in w}
T={'o':None,'p':'o','u':'p','v':'p'}
xp={'o':F(1,5),'p':F(1,5),'u':F(2,5),'v':F(1,5)}; xm={'o':F(1,5),'p':F(1,5),'u':F(1,5),'v':F(2,5)}
eps=F(1,100); GPT={(1,0):eps,(1,1):1,(2,0):2*eps/5,(2,1):0,(2,2):1}
print("(1) countermodel:")
for nm,x in (('x+',xp),('x-',xm)):
    w=f(T,x,GPT,1); print(nm,[w[k] for k in 'opuv'],'p/u=',w['p']/w['u'],'x p/u=',x['p']/x['u'])
# extensions by empty vertices (I = zero extension)
exts={'leaf@o':{'n1':'o'},'leaf@p':{'n1':'p'},'chain@o':{'n1':'o','n2':'n1'},'leaf@u':{'n1':'u'}}
def residual(x,AA,bb):
    out={}
    for nm,e in exts.items():
        par=dict(T); par.update(e)
        wx=f(par,x,AA,bb); wy=f(T,x,AA,bb)
        out[nm]={v:sp.simplify(wx[v]-wy.get(v,0)) for v in par if sp.simplify(wx[v]-wy.get(v,0))!=0}
    return out
print("(2a) I-naturality residuals (general alpha), x+:")
eqs=set()
for x in (xp,xm):
    r=residual(x,A,b)
    for nm,d in r.items():
        if x is xp: print(' ',nm,d)
        for v,val in d.items(): eqs.add(sp.expand(val))
sol=sp.solve(list(eqs),[a10,a20,a21],dict=True); print("solve:",sol)
print("GPT countermodel residual nonzero:",any(residual(xp,GPT,1)[k] for k in exts))
ID={(1,1):1,(2,2):1}; print("id residual zero:",not any(residual(xp,ID,1)[k] for k in exts))
# (2b) I-stable domain: positivity of f on x± extended by k empty leaves / chains, for all k
k=sp.symbols('k',positive=True,integer=True)
print("(2b) positivity under k-fold zero extension:")
cons=[]
for x,nm in ((xp,'x+'),(xm,'x-')):
    m=mass(T,x)
    # k empty children at o (depth1): o gets -k*(a10*M + a11*0); new child gets a10*M
    cons += [(nm,'leaf@o new',a10*m['o']),(nm,'leaf@o parent coeff of k',-a10*m['o']),
             (nm,'leaf@p new',a20*m['o']+a21*m['p']),(nm,'leaf@p parent coeff of k',-(a20*m['o']+a21*m['p'])),
             (nm,'chain@o depth2 new',a20*m['o']),(nm,'chain@o parent coeff of k',-a20*m['o'])]
for c in cons: print(' ',c)
print("  => each 'new' >=0 and each 'coeff of k' >=0 (k unbounded) forces equality to 0: a10=0, a20=0, a21*m_p=0 with m_p=4/5 -> a21=0")
cp=sp.expand((xp['p']*f(T,xp,A,b)['u']-xp['u']*f(T,xp,A,b)['p'])); cm=sp.expand((xm['p']*f(T,xm,A,b)['u']-xm['u']*f(T,xm,A,b)['p']))
s={a10:0,a20:0,a21:0}; print("after constraints: fixed(x+):",cp.subs(s)," fixed(x-):",cm.subs(s)," ratio:",sp.simplify(cp.subs(s)/cm.subs(s)))
print("check vs Q167 x+ cond:",sp.expand(cp - (-2*a10/5-8*a11/25+a20+4*a21/5+8*a22/25)))
