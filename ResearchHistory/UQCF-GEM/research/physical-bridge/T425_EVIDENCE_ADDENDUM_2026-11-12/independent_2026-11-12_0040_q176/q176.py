import sys,random,itertools; sys.dont_write_bytecode=True
from fractions import Fraction as F
random.seed(176)
def dep(par,v):
    d=0
    while par[v] is not None: v=par[v]; d+=1
    return d
def anc(par,v):
    ch=[]
    while par[v] is not None: v=par[v]; ch.append(v)
    return ch[::-1]
def kids(par,v): return [c for c in par if par[c]==v]
def mass(par,x):
    m={v:x.get(v,0) for v in par}
    for v in sorted(par,key=lambda v:-dep(par,v)):
        if par[v] is not None: m[par[v]]+=m[v]
    return m
def h(r): return {F(1,4):F(2,5),F(1,2):F(6,5)}.get(r,F(1,100))
def S4(par,x):
    m=mass(par,x); r=[v for v in par if par[v] is None][0]; w={v:0 for v in par}; w[r]=m[r]
    for c in par:
        q=par[c]
        if q is None or m[c]==0: continue
        d=dep(par,c); A=anc(par,c)
        if d==1: e=m[c]
        elif d==2: e=m[c]*h(m[c]/m[q])
        else: a2=A[2]; e=m[c]*h(m[a2]/m[A[1]])
        w[c]+=e; w[q]-=e
    return w
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
def in_Ddc(par,x):
    return all(x[v]>=0 for v in par) and all(x[c]==0 for v in par if x[v]==0 for c in par if v in anc(par,c))
C={'o':None,'p':'o','u':'p','v':'p','w':'u','s':'o','t':'s'}
def rand_Ddc(par,atom=False):
    zero=set()
    for v in sorted(par,key=lambda v:dep(par,v)):
        if par[v] is not None and (par[v] in zero or random.random()<0.25): zero.add(v)
    x={v:(0 if v in zero else F(random.randint(1,12),random.randint(1,12))) for v in par}
    if atom:  # force atom ratio m_u/m_p = 1/2 or 1/4 where possible
        x={'o':F(1,5),'p':F(1,5),'u':F(1,5),'v':F(1,5),'w':F(1,5),'s':0,'t':0}
    return x
stab=0; neg=0; npts=0
for k in range(320):
    x=rand_Ddc(C,atom=(k%40==0)); assert in_Ddc(C,x); npts+=1
    w=S4(C,x); neg+=sum(1 for v in C if w[v]<0)
    for Y in prefixes(C):
        pY={v:C[v] for v in Y}; y=P(C,Y,x); stab+= (not in_Ddc(pY,y)); neg+=sum(1 for v in Y if S4(pY,y)[v]<0)
    for q in list(C):
        for ext in ({'z1':q},{'z1':q,'z2':'z1'}):
            p2=dict(C); p2.update(ext); x2=dict(x); x2.update({z:0 for z in ext}); stab+=(not in_Ddc(p2,x2)); neg+=sum(1 for v in p2 if S4(p2,x2)[v]<0)
print('D_dc points',npts,'stability violations',stab,'negative S4 entries on D_dc (incl. P1/I images)',neg)
# orbit from strictly positive points
viol=0
for k in range(50):
    x={v:F(random.randint(1,9),random.randint(1,9)) for v in C}; par=C
    for step in range(6):
        if random.random()<0.5:
            Y=random.choice(list(prefixes(par))); x=P(par,Y,x); par={v:par[v] for v in Y}
        else:
            q=random.choice(list(par)); z='n%d_%d'%(k,step); par=dict(par); par[z]=q; x=dict(x); x[z]=0
        viol+=(not in_Ddc(par,x))
print('orbit violations',viol)
T={'o':None,'p':'o','u':'p','v':'p'}
xp=dict(o=F(1,5),p=F(1,5),u=F(2,5),v=F(1,5)); xm=dict(o=F(1,5),p=F(1,5),u=F(1,5),v=F(2,5)); xc=dict(o=F(1,5),p=F(0),u=F(2,5),v=F(2,5))
for lab,x in (('x+',xp),('x-',xm)):
    w=S4(T,x); print(lab,'in D_dc',in_Ddc(T,x),'f',[w[k] for k in 'opuv'],'fixed',w['p']*x['u']==w['u']*x['p'])
print('control (1/5,0,2/5,2/5) in D_dc',in_Ddc(T,xc),'S4 f_p',S4(T,xc)['p'])
