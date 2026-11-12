import numpy as np, itertools
rng=np.random.default_rng(155)
# tree o->p, p->u, p->v ; atoms indexed by names; P1 prune of a leaf adds its grade to its parent
par={'p':'o','u':'p','v':'p'}
def prune(x,leaf):
    if leaf not in x or any(par.get(c)==leaf for c in x): return None  # only current leaves
    y=dict(x); w=y.pop(leaf); y[par[leaf]]+=w; return y
def incl(x,atom): # P2 zero extension, re-adding a removed leaf with grade 0
    if atom in x or par.get(atom) not in x: return None
    y=dict(x); y[atom]=0.0; return y
def relab(x): # admissible relabeling: swap sibling leaves u,v when both present
    if 'u' in x and 'v' in x: y=dict(x); y['u'],y['v']=x['v'],x['u']; return y
    return None
cmds=[('P',l) for l in 'uvp']+[('I',a) for a in 'uvp']+[('R',None)]
def apply(x,c):
    k,a=c; return prune(x,a) if k=='P' else incl(x,a) if k=='I' else relab(x)
supp=lambda x:frozenset(k for k,v in x.items() if abs(v)>0)
table={}; bad=0; n=0
for trial in range(4000):
    names=['o','p','u','v']
    x={k:(0.0 if rng.random()<0.3 else rng.integers(1,6)) for k in names}
    for word in itertools.product(cmds,repeat=3):
        y=x; key=(frozenset(x),supp(x))
        for c in word:
            y2=apply(y,c)
            if y2 is None: break
            sig=(key,c); s=(frozenset(y2),supp(y2)); n+=1
            if sig in table and table[sig]!=s: bad+=1
            table.setdefault(sig,s); key=s; y=y2
print("support-equivariance checks:",n,"violations:",bad)
def transcript(x,word):
    out=[];y=x
    for c in word:
        y2=apply(y,c); out.append((c,y2 is not None, None if y2 is None else (frozenset(y2),supp(y2))))
        if y2 is None: break
        y=y2
    return out
xp={'o':1,'p':1,'u':2,'v':1}; xm={'o':1,'p':1,'u':1,'v':2}
diff=sum(transcript(xp,w)!=transcript(xm,w) for L in (1,2,3) for w in itertools.product(cmds,repeat=L))
print("balanced pair support-guarded transcript differences (words len<=3):",diff)
y1,y2=prune(xp,'u'),prune(xm,'u'); print("after removing u: x+ ->",y1," x- ->",y2," same support:",supp(y1)==supp(y2))
# signed control: where nonnegativity is used
xs={'o':1,'p':-2,'u':2,'v':1}; print("signed control: supp before",sorted(supp(xs)),"after prune u",sorted(supp(prune(xs,'u'))),"(p cancels)")
