import sys,itertools; sys.dont_write_bytecode=True
import sympy as sp
src=open(__file__.replace('q165d.py','q165c.py')).read().replace("__file__","'"+__file__.replace('q165d.py','q165c.py')+"'")
src=src.replace("exact(1,3,9)","").replace("    ns=M.nullspace(); X=max(C,key=len)","    return C,idx,M\n    ns=None; X=None")
exec(src)
import sys
depth,arity,ms=int(sys.argv[1]),int(sys.argv[2]),int(sys.argv[3])
C,idx,M=exact(depth,arity,ms)
def fam(fn):
    v=sp.zeros(len(idx),1)
    for (X,i,j),n in idx.items(): v[n]=fn(X,i,j)
    return v
def kids(X,v): return sum(1 for w in X if len(w)==len(v)+1 and w[:len(v)]==v)
F={'id':fam(lambda X,i,j:int(i==j))}
for k in range(depth): F[f'T{k}']=fam(lambda X,i,j,k=k:int(i==(j[:k] if len(j)>k else j)))
for d in range(1,depth+1): F[f'D{d}']=fam(lambda X,i,j,d=d:int(len(i)==d)-(kids(X,i) if len(i)==d-1 else 0))
B=sp.Matrix.hstack(*F.values())
print(f"depth={depth} arity={arity} maxsize={ms}: residual |M f|=0 for each:",{k:(M*v).is_zero_matrix for k,v in F.items()}," rank(candidates)=",B.rank()," nullity(M)=",M.shape[1]-M.rank())
