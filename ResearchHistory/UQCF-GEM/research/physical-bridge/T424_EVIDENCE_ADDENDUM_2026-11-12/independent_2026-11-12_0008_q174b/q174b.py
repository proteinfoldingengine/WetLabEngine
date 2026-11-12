import sys,random,itertools; sys.dont_write_bytecode=True
from fractions import Fraction as F
random.seed(1742)
def dep(par,v):
    d=0
    while par[v] is not None: v=par[v]; d+=1
    return d
def anc(par,v):
    ch=[]
    while par[v] is not None: v=par[v]; ch.append(v)
    return ch[::-1]
def root(par): return [v for v in par if par[v] is None][0]
def mass(par,x):
    m={v:x.get(v,F(0)) for v in par}
    for v in sorted(par,key=lambda v:-dep(par,v)):
        if par[v] is not None: m[par[v]]+=m[v]
    return m
def flux_ref(G,phi=lambda M:M,sib=False):
    def f(par,x):
        m=mass(par,x); r=root(par); M=m[r]
        w={v:F(0) for v in par}; w[r]=phi(M)
        for c in par:
            q=par[c]
            if q is None: continue
            extra=sum(m[s] for s in par if par.get(s)==q and s!=c) if sib else 0
            e=G(dep(par,c),m[c],[m[a] for a in anc(par,c)],extra) if m[c]!=0 else F(0)
            w[c]+=e; w[q]-=e
        return w
    return f
def P(par,Y,x):
    out={v:F(0) for v in Y}
    for v in par:
        u=v
        while u not in Y: u=par[u]
        out[u]+=x.get(v,F(0))
    return out
def prefixes(par):
    vs=[v for v in par if par[v] is not None]; r=root(par)
    for k in range(len(vs)+1):
        for S in itertools.combinations(vs,k):
            Y=set(S)|{r}
            if all(par[v] in Y for v in S): yield Y
def P1res(f,par,x):
    fx=f(par,x); n=0
    for Y in prefixes(par):
        pY={v:par[v] for v in Y}; l=f(pY,P(par,Y,x)); rr=P(par,Y,fx); n+=sum(l[v]!=rr[v] for v in Y)
    return n
def Ires(f,par,y_rand):
    n=0
    for Y in prefixes(par):
        pY={v:par[v] for v in Y}; y={v:y_rand() for v in Y}
        fx=f(par,{v:(y[v] if v in Y else F(0)) for v in par}); fy=f(pY,y)
        n+=sum(fx[v]!=(fy[v] if v in Y else 0) for v in par)
    return n
def relabels(par,k):
    vs=[v for v in par]; out=[]
    for _ in range(k):
        names=['n%d'%i for i in range(len(vs))]; random.shuffle(names); mp=dict(zip(vs,names))
        out.append(mp)
    return out
def Rres(f,par,x,k=20):
    fx=f(par,x); n=0
    for mp in relabels(par,k):
        p2={mp[v]:(mp[par[v]] if par[v] is not None else None) for v in par}; x2={mp[v]:x[v] for v in par}
        f2=f(p2,x2); n+=sum(f2[mp[v]]!=fx[v] for v in par)
    return n
def rq(): return F(random.randint(1,9),random.randint(1,9))
T={'o':None,'p':'o','u':'p','v':'p'}
xp=dict(o=F(1,5),p=F(1,5),u=F(2,5),v=F(1,5)); xm=dict(o=F(1,5),p=F(1,5),u=F(1,5),v=F(2,5))
C={'o':None,'p':'o','u':'p','v':'p','w':'u','s':'o'}
C2={'o':None,'p':'o','u':'p','v':'p','w':'u','z':'w'}
S3={'o':None,'p':'o','a':'p','b':'p','c':'p'}; S4={'o':None,'p':'o','a':'p','b':'p','c':'p','d':'p'}
def fixed(f,x): w=f(T,x); return w['p']*x['u']==w['u']*x['p']
def abc(G): return G(1,F(4,5),[F(1)],0),G(2,F(1,5),[F(1),F(4,5)],0),G(2,F(2,5),[F(1),F(4,5)],0)
print('== S1 psi = 16r-7 witness (Q173/Q175 member)')
psi=lambda r:16*r-7
Gpsi=lambda d,mc,A,e: mc if d==1 else mc*(1+F(1,100)*psi(mc/A[-1]))
fpsi=flux_ref(Gpsi); a,b,c=abc(Gpsi)
print('a b c',a,b,c,'c==2b',c==2*b,'(Q175 recompute)')
print('f(x+)',[str(fpsi(T,xp)[v]) for v in 'opuv'],'f(x-)',[str(fpsi(T,xm)[v]) for v in 'opuv'])
print('f(x+) f(x-) entrywise >0',all(t>0 for t in fpsi(T,xp).values()) and all(t>0 for t in fpsi(T,xm).values()))
print('fixed x+',fixed(fpsi,xp),'fixed x-',fixed(fpsi,xm))
print('Gamma_2 factor 1+psi/100 min over r in (0,1] = at r->0:',1+F(1,100)*psi(F(0)),'>0; psi<0 iff r<7/16')
xb=dict(o=F(1,5),p=F(0),u=F(2,5),v=F(2,5)); w=fpsi(T,xb)
print('closed-cone point x=(1/5,0,2/5,2/5): f =',[str(w[v]) for v in 'opuv'],'negative entry:',any(t<0 for t in w.values()),'(control: must be True)')
neg=0
for _ in range(300):
    x={v:F(random.randint(0,9),9) for v in C}; x['p']=F(0) if random.random()<0.5 else x['p']
    neg+=any(t<0 for t in fpsi(C,x).values())
print('psi witness negative outputs among 300 closed-cone samples on C:',neg)
print('== S2 Prop 174b.1 boundary carriers (generic Gamma via table)')
def tableG(a,b,c):
    return lambda d,mc,A,e: a if d==1 else {F(1,5):b,F(2,5):c}.get(mc,mc)
for nm,par,x,expr in [('pair x_p=0 (2/5,2/5)',T,xb,'a-2*c'),
    ('3-star (1/5,1/5,2/5)',S3,dict(o=F(1,5),p=F(0),a=F(1,5),b=F(1,5),c=F(2,5)),'a-2*b-c'),
    ('4-star (1/5 x4)',S4,dict(o=F(1,5),p=F(0),a=F(1,5),b=F(1,5),c=F(1,5),d=F(1,5)),'a-4*b')]:
    bad=0
    for _ in range(20):
        A_,B_,C_=rq(),rq(),rq(); fp=flux_ref(tableG(A_,B_,C_))(par,x)['p']
        bad+=fp!=eval(expr,{'a':A_,'b':B_,'c':C_})
    print(nm,'f_p ==',expr,'mismatches',bad)
sep=0; feas=0; grid=[F(i,12) for i in range(0,25)]
for a in grid:
    for b in grid:
        for c in grid:
            if a>=2*c and a>=2*b+c and a>=4*b:
                feas+=1; fpl=(2*a==2*b+3*c); fmi=(a==2*b+c); sep+=(fpl!=fmi)
                if (fpl or fmi) and c!=2*b: sep+=1000
print('grid',len(grid)**3,'feasible (S2 inequalities)',feas,'separating or c!=2b-fixed',sep)
print('== S3 positive member Gamma_2 = m(1+r)/3, c != 2b, not separating')
G3=lambda d,mc,A,e: mc if d==1 else (mc*(1+mc/A[-1])/3 if d==2 else mc*(1+A[2]/A[1])/3)
f3=flux_ref(G3); a,b,c=abc(G3); print('a b c',a,b,c,'c==2b',c==2*b,'fixed x+',fixed(f3,xp),'fixed x-',fixed(f3,xm))
print('== S4 open-cone witness (discontinuous h)')
def h(r): return {F(1,4):F(2,5),F(1,2):F(6,5)}.get(r,F(1,100))
G4=lambda d,mc,A,e: mc if d==1 else (mc*h(mc/A[1]) if d==2 else mc*h(A[2]/A[1]))
f4=flux_ref(G4); a,b,c=abc(G4)
print('a b c',a,b,c,'c==2b',c==2*b,'2a==2b+3c',2*a==2*b+3*c,'a==2b+c',a==2*b+c)
print('fixed x+',fixed(f4,xp),'fixed x-',fixed(f4,xm),'f(x+)',[str(f4(T,xp)[v]) for v in 'opuv'],'f(x-)',[str(f4(T,xm)[v]) for v in 'opuv'])
neg=0;n=0
for par in [T,C,C2,S3,S4]:
    for _ in range(60):
        x={v:rq() for v in par}; n+=1; neg+=any(t<=0 for t in f4(par,x).values())
# adversarial open-cone points near the h atoms: children at exactly r=1/2 and 1/4 with tiny x_p
for eps in [F(1,10**k) for k in range(1,6)]:
    for par,ch in [(T,[F(1,2),F(1,4)]),(S3,[F(1,4)]*3),(S4,[F(1,2),F(1,4),F(1,8)])]:
        mp=F(1); kids=[v for v in par if par[v]=='p']; rs=ch+[F(1,1000)]*(len(kids)-len(ch))
        x={'o':F(1),'p':mp*(1-sum(rs[:len(kids)]))}
        if x['p']<=0: continue
        for v,r in zip(kids,rs): x[v]=mp*r
        n+=1; neg+=any(t<=0 for t in f4(par,x).values())
print('S4 open-cone samples',n,'non-positive outputs',neg)
w=f4(T,dict(o=F(1,5),p=F(0),u=F(2,5),v=F(2,5)))
print('S4 closed-cone point (1/5,0,2/5,2/5): f =',[str(w[v]) for v in 'opuv'],'negative:',any(t<0 for t in w.values()),'(control: must be True)')
print('== naturality residuals (P1 / I / relabel)')
for nm,f in [('psi',fpsi),('S3',f3),('S4',f4)]:
    p1=i1=r1=0
    for par in [C,C2]:
        for _ in range(3):
            x={v:rq() for v in par}; p1+=P1res(f,par,x); r1+=Rres(f,par,x)
        # S4 atom-hitting grades
        x={v:F(1) for v in par}; p1+=P1res(f,par,x); r1+=Rres(f,par,x)
        i1+=Ires(f,par,rq)
    print(nm,'P1',p1,'I',i1,'relabel',r1)
fs=flux_ref(lambda d,mc,A,e: mc*(1+F(1,10)*e/A[0]),sib=True); p1=sum(P1res(fs,C,{v:rq() for v in C}) for _ in range(3))
print('control sibling-dependent P1 residuals',p1,'(must be >0)')
def fname(par,x):
    w=flux_ref(G3)(par,x); r=root(par); k=sorted(v for v in par if v!=r)[0]; w=dict(w); w[k]+=F(1,7)*x[k]; w[r]-=F(1,7)*x[k]; return w
print('control name-dependent relabel residuals',sum(Rres(fname,C,{v:rq() for v in C}) for _ in range(3)),'(must be >0)')
