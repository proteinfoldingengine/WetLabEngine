import sys,itertools; sys.dont_write_bytecode=True
from fractions import Fraction as F
import sympy as sp
def universe(depth,arity=2):
    W=[()]; 
    for d in range(1,depth+1): W+= [w for w in itertools.product(range(arity),repeat=d)]
    return W
def carriers(U):
    out=[]
    nonroot=[w for w in U if w]
    for r in range(len(nonroot)+1):
        for S in itertools.combinations(nonroot,r):
            X=[()]+list(S)
            if all(w[:-1] in X for w in S): out.append(tuple(sorted(X,key=lambda w:(len(w),w))))
    return out
def ret(k,Y): return max((v for v in Y if k[:len(v)]==v),key=len)
def solve(depth,relabel=True,arity=2):
    U=universe(depth,arity); C=carriers(U); var={}; syms=[]
    for X in C:
        for i in X:
            for j in X: s=sp.Symbol(f"f_{len(syms)}"); var[(X,i,j)]=s; syms.append(s)   # (f_X)_{i,j}: coeff of x_j in output i
    eqs=[]
    for X in C:
        for Y in C:
            if Y!=X and set(Y)<=set(X):
                # (P f_X x)_y = sum_{i: r(i)=y} sum_j f_X[i,j] x_j ; (f_Y P x)_y = sum_j f_Y[y, r(j)] x_j
                for y in Y:
                    for j in X:
                        eqs.append(sum(var[(X,i,j)] for i in X if ret(i,Y)==y) - var[(Y,y,ret(j,Y))])
    if relabel:
        nodes=[w for w in U if len(w)<depth]
        for nd in nodes:
            def sw(w,nd=nd):
                if len(w)>len(nd) and w[:len(nd)]==nd:
                    c=w[len(nd)]; return w[:len(nd)]+((c+1)%arity,)+w[len(nd)+1:]
                return w
            for X in C:
                Xs=tuple(sorted([sw(w) for w in X],key=lambda w:(len(w),w)))
                for i in X:
                    for j in X: eqs.append(var[(X,i,j)]-var[(Xs,sw(i),sw(j))])
    M=sp.Matrix([[e.coeff(s) for s in syms] for e in eqs]) if eqs else sp.zeros(0,len(syms))
    ns=M.nullspace()
    return C,syms,var,ns
for depth,rel in ((2,True),(2,False)):
    C,syms,var,ns=solve(depth,rel)
    print(f"depth={depth} relabel={rel} carriers={len(C)} unknowns={len(syms)} solution_dim={len(ns)}")
    # check whether span{id, delta_root (x) sum} equals solution space
    def fam(kind):
        v=sp.zeros(len(syms),1)
        for (X,i,j),s in var.items():
            k=syms.index(s)
            if kind=='id' and i==j: v[k]=1
            if kind=='root' and i==(): v[k]=1
        return v
    B=sp.Matrix.hstack(*ns) if ns else sp.zeros(len(syms),0)
    cand=sp.Matrix.hstack(fam('id'),fam('root'))
    print('  id,root in solution space:', sp.Matrix.hstack(B,cand).rank()==B.rank(), ' span equal:', B.rank()==cand.rank() and sp.Matrix.hstack(B,cand).rank()==B.rank())
    if len(ns)<=6 and len(ns)!=2:
        X=max(C,key=len)
        for b in ns:
            print('   basis elt on largest carrier', X, [[b[syms.index(var[(X,i,j)])] for j in X] for i in X])
