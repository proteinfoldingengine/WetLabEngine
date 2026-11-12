# Float rank count (dimension only) + exact membership of depth-truncation families; arity 3, size-bounded carriers.
import sys,itertools; sys.dont_write_bytecode=True
import numpy as np
def universe(depth,arity):
    W=[()]
    for d in range(1,depth+1): W+=list(itertools.product(range(arity),repeat=d))
    return W
def carriers(U,maxsize):
    nonroot=[w for w in U if w]; out=[]
    for r in range(0,maxsize):
        for S in itertools.combinations(nonroot,r):
            X=[()]+list(S)
            if all(w[:-1] in X for w in S): out.append(tuple(sorted(X,key=lambda w:(len(w),w))))
    return out
def ret(k,Y): return max((v for v in Y if k[:len(v)]==v),key=len)
def build(depth,arity,maxsize):
    U=universe(depth,arity); C=carriers(U,maxsize); Cset=set(C); idx={}
    for X in C:
        for i in X:
            for j in X: idx[(X,i,j)]=len(idx)
    rows=[];r=0
    def add(terms):
        nonlocal r
        for k,c in terms: rows.append((r,k,c))
        r+=1
    for X in C:
        for Y in C:
            if Y!=X and set(Y)<=set(X):
                for y in Y:
                    for j in X:
                        t=[(idx[(X,i,j)],1.0) for i in X if ret(i,Y)==y]; t.append((idx[(Y,y,ret(j,Y))],-1.0)); add(t)
    # relabelings: all permutations of child tokens at every internal node of the universe
    for nd in [w for w in U if len(w)<depth]:
        for perm in itertools.permutations(range(arity)):
            def sw(w,nd=nd,perm=perm):
                if len(w)>len(nd) and w[:len(nd)]==nd: return w[:len(nd)]+(perm[w[len(nd)]],)+w[len(nd)+1:]
                return w
            for X in C:
                Xs=tuple(sorted([sw(w) for w in X],key=lambda w:(len(w),w)))
                for i in X:
                    for j in X: add([(idx[(X,i,j)],1.0),(idx[(Xs,sw(i),sw(j))],-1.0)])
    n=len(idx); G=np.zeros((n,n)); byrow={}
    for a,b,c in rows: byrow.setdefault(a,[]).append((b,c))
    for t in byrow.values():
        for b1,c1 in t:
            for b2,c2 in t: G[b1,b2]+=c1*c2
    return C,idx,G
def trunc(idx,k):
    v=np.zeros(len(idx))
    for (X,i,j),n in idx.items():
        if len(j)<=k and i==j: v[n]=1
        if len(j)>k and i==j[:k]: v[n]=1
    return v
for depth,arity,ms in ((1,2,9),(1,3,9),(2,2,8),(2,3,6)):
    C,idx,G=build(depth,arity,ms)
    ev=np.linalg.eigvalsh(G); dim=int((ev<1e-8).sum())
    res=[float(trunc(idx,k)@G@trunc(idx,k)) for k in range(depth+1)]
    print(f"depth={depth} arity={arity} maxsize={ms} carriers={len(C)} unknowns={len(idx)} nullity={dim} truncation residuals T_0..T_{depth}={res}")
