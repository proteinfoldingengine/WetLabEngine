import sys; sys.dont_write_bytecode=True
import importlib.util, os
spec=importlib.util.spec_from_file_location('pca',os.path.join(os.path.dirname(__file__),'pca_94d946df.py')); pca=importlib.util.module_from_spec(spec); spec.loader.exec_module(pca)
from fractions import Fraction as F
trees={'chain2':[(),(0,)],'chain4':[(),(0,),(0,0),(0,0,0)],'star4':[(),(0,),(1,),(2,)],
 'q157shape':[(),(0,),(0,0),(0,1)],'branched6':[(),(0,),(1,),(0,0),(0,1),(1,0)],'mixed7':[(),(0,),(1,),(0,0),(0,0,0),(0,0,1),(1,5)]}
ok=True
for name,keys in trees.items():
    L=pca.laplacian(keys); n=len(keys)
    rows=[]
    for i in range(n):
        for j in range(n):
            if i!=j and L[i][j]!=0:
                r=[F(0)]*n; r[i]+=L[i][j]; r[j]-=L[i][j]; rows.append(r)   # w_i L_ij - L_ij w_j = 0 (diag terms cancel)
    rk=pca.rank(rows) if rows else 0
    ker=n-rk; ok&=(ker==1)
    print(f"{name:11s} n={n} kernel_dim={ker} {'PASS' if ker==1 else 'FAIL'}")
print('ALL_PASS' if ok else 'SOME_FAIL')
# consequence on Q157 balanced pair with the forced (uniform) weight
xp=(F(1,5),F(2,5)); xm=(F(1,5),F(1,5)); w=(F(1),F(1))
print('forced w: fixed(x+)=',xp[0]*w[1]==xp[1]*w[0],' fixed(x-)=',xm[0]*w[1]==xm[1]*w[0])
