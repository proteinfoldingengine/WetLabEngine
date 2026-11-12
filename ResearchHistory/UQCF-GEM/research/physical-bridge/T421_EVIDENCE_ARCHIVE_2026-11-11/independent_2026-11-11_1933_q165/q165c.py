import sys,itertools; sys.dont_write_bytecode=True
import sympy as sp
exec(open(__file__.replace('q165c.py','q165b.py')).read().split('def trunc')[0].replace('import numpy as np',''))
def exact(depth,arity,ms):
    U=universe(depth,arity); C=carriers(U,ms); idx={}
    for X in C:
        for i in X:
            for j in X: idx[(X,i,j)]=len(idx)
    eqs=[]
    for X in C:
        for Y in C:
            if Y!=X and set(Y)<=set(X):
                for y in Y:
                    for j in X:
                        e={}; 
                        for i in X:
                            if ret(i,Y)==y: e[idx[(X,i,j)]]=e.get(idx[(X,i,j)],0)+1
                        k=idx[(Y,y,ret(j,Y))]; e[k]=e.get(k,0)-1; eqs.append(e)
    for nd in [w for w in U if len(w)<depth]:
        for perm in itertools.permutations(range(arity)):
            def sw(w,nd=nd,perm=perm):
                if len(w)>len(nd) and w[:len(nd)]==nd: return w[:len(nd)]+(perm[w[len(nd)]],)+w[len(nd)+1:]
                return w
            for X in C:
                Xs=tuple(sorted([sw(w) for w in X],key=lambda w:(len(w),w)))
                for i in X:
                    for j in X:
                        a,b=idx[(X,i,j)],idx[(Xs,sw(i),sw(j))]
                        if a!=b: eqs.append({a:1,b:-1})
    M=sp.zeros(len(eqs),len(idx))
    for r,e in enumerate(eqs):
        for k,c in e.items(): M[r,k]=c
    ns=M.nullspace(); X=max(C,key=len)
    print(f"depth={depth} arity={arity} dim={len(ns)} largest carrier {X}")
    for b in ns: print('  ',[[b[idx[(X,i,j)]] for j in X] for i in X])
exact(1,3,9)
