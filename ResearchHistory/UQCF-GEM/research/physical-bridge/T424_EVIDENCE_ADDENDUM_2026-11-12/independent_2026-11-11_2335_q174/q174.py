import sys,random,itertools; sys.dont_write_bytecode=True
from fractions import Fraction as F
random.seed(174)
T={'o':None,'p':'o','u':'p','v':'p'}
xp=dict(o=F(1,5),p=F(1,5),u=F(2,5),v=F(1,5)); xm=dict(o=F(1,5),p=F(1,5),u=F(1,5),v=F(2,5))
C={'o':None,'p':'o','u':'p','v':'p','w':'u','s':'o'}
def dep(par,v):
    d=0
    while par[v] is not None: v=par[v]; d+=1
    return d
def anc(par,v):
    ch=[]
    while par[v] is not None: v=par[v]; ch.append(v)
    return ch[::-1]
def mass(par,x):
    m={v:x.get(v,0) for v in par}
    for v in sorted(par,key=lambda v:-dep(par,v)):
        if par[v] is not None: m[par[v]]+=m[v]
    return m
def flux_ref(G,phi=lambda M:M,sib=False):
    def f(par,x):
        m=mass(par,x); r=[v for v in par if par[v] is None][0]; M=m[r]
        w={v:0 for v in par}; w[r]=phi(M)
        for c in par:
            q=par[c]
            if q is None: continue
            extra=sum(m[s] for s in par if par.get(s)==q and s!=c) if sib else 0
            e=G(dep(par,c),m[c],[m[a] for a in anc(par,c)],extra) if m[c]!=0 else 0
            w[c]+=e; w[q]-=e
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
    vs=[v for v in par if par[v] is not None]; r=[v for v in par if par[v] is None][0]
    for k in range(len(vs)+1):
        for S in itertools.combinations(vs,k):
            Y=set(S)|{r}
            if all(par[v] in Y for v in S): yield Y
def P1res(f,par,x):
    fx=f(par,x); n=0
    for Y in prefixes(par):
        pY={v:par[v] for v in Y}; l=f(pY,P(par,Y,x)); rr=P(par,Y,fx); n+=sum(l[v]!=rr[v] for v in Y)
    return n
def recon(f,par,x):  # subtree sums of f vs chain-carrier evaluation
    w=f(par,x); m=mass(par,x); n=0
    for c in par:
        if par[c] is None: continue
        sub=[v for v in par if v==c or c in anc(par,v)]
        e=sum(w[v] for v in sub)
        chain=anc(par,c)+[c]; cp={chain[0]:None}
        for i in range(1,len(chain)): cp[chain[i]]=chain[i-1]
        cx={chain[i]:m[chain[i]]-(m[chain[i+1]] if i+1<len(chain) else 0) for i in range(len(chain))}
        n+= (e!=f(cp,cx)[c])
    return n
psi=lambda r:16*r-7
maps={'Q173':lambda d,mc,A,e: mc if d==1 else mc*(1+F(1,100)*psi(mc/A[-1]))}
for k in range(3):
    co=[F(random.randint(1,9),random.randint(2,9)) for _ in range(4)]
    maps[f'rand{k}']=(lambda co:lambda d,mc,A,e: mc*(co[0]+co[1]*mc/A[0]+co[2]*(mc/A[-1])**2+co[3]*d*mc/A[0]))(co)
for nm,G in maps.items():
    f=flux_ref(G); p1=r=0
    for _ in range(4):
        x={v:F(random.randint(1,9),random.randint(1,9)) for v in C}; p1+=P1res(f,C,x); r+=recon(f,C,x)
    print(nm,'P1 residuals',p1,'reconstruction mismatches',r)
fb=flux_ref(lambda d,mc,A,e: mc*(1+F(1,10)*e/A[0])+0,sib=True); p1=0
for _ in range(4):
    x={v:F(random.randint(1,9),random.randint(1,9)) for v in C}; p1+=P1res(fb,C,x)
print('control sibling-dependent P1 residuals',p1)
bad=0
for _ in range(6):
    a,b,c=[F(random.randint(1,20),random.randint(1,20)) for _ in range(3)]
    for trial in range(3):
        if trial==1: a=b+F(3,2)*c
        if trial==2: a=2*b+c
        G=lambda d,mc,A,e,a=a,b=b,c=c: a if d==1 else {F(1,5):b,F(2,5):c}[mc]
        f=flux_ref(G)
        fx=lambda x:(lambda w:w['p']*x['u']==w['u']*x['p'])(f(T,x))
        bad+=(fx(xp)!=(2*a==2*b+3*c))+(fx(xm)!=(a==2*b+c))
print('guard-criterion mismatches',bad)
