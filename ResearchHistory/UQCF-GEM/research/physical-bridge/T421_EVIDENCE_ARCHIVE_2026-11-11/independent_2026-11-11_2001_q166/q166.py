import sys,itertools; sys.dont_write_bytecode=True
import numpy as np
src=open(sys.argv[0].replace('q166.py','base.py')).read().split('for depth,arity,ms in')[0]
exec(src)
def kids(X,v): return [w for w in X if len(w)==len(v)+1 and w[:len(v)]==v]
def mass_coef(a,j): return 1 if j[:len(a)]==a else 0  # m_a(x) coefficient of x_j
def cand(idx,depth):
    C={}
    v=np.zeros(len(idx),dtype=np.int64)
    for (X,i,j),n in idx.items(): v[n]=int(i==())
    C['T0']=v
    for d in range(1,depth+1):
        for jj in range(0,d+1):
            v=np.zeros(len(idx),dtype=np.int64)
            for (X,i,j),n in idx.items():
                s=0
                if len(i)==d: s+=mass_coef(i[:jj],j)
                if len(i)==d-1:
                    for c in kids(X,i): s-=mass_coef(c[:jj],j)
                v[n]=s
            C[f'E{d}{jj}']=v
    return C
for depth,arity,ms in [(1,3,9),(2,2,8),(2,3,6),(3,2,7)]:
    Cr,idx,G=build(depth,arity,ms)
    ev=np.linalg.eigvalsh(G); null=int((ev<1e-8).sum())
    Cd=cand(idx,depth); Gi=np.rint(G).astype(np.int64)
    natural={k:bool((v@Gi@v)==0) for k,v in Cd.items()}
    B=np.stack(list(Cd.values()),1).astype(float); rk=np.linalg.matrix_rank(B)
    print(f"depth={depth} arity={arity} maxsize={ms} carriers={len(Cr)} nullity={null} candidates={len(Cd)} rank={rk} all_natural={all(natural.values())} {natural}",flush=True)
