import sys,random,itertools; sys.dont_write_bytecode=True
from fractions import Fraction as F
random.seed(1762)
exec(open('../independent_2026-11-12_0040_q176/q176.py').read().split("C={'o'")[0].split("random.seed(176)")[1])
C={'o':None,'p':'o','u':'p','v':'p','w':'u','s':'o','t':'s'}
T={'o':None,'p':'o','u':'p','v':'p'}
bad=0
for name,par in (('T',T),('C',C)):
    V=list(par); pre={frozenset(Y) for Y in prefixes(par)}
    sup=set()
    for k in range(1,len(V)+1):
        for S in itertools.combinations(V,k):
            x={v:(F(1) if v in S else F(0)) for v in V}
            if in_Ddc(par,x): sup.add(frozenset(S))
    ok=(sup==pre); bad+=not ok
    ext=0
    for Y in pre:
        x={v:(F(random.randint(1,9),random.randint(1,9)) if v in Y else F(0)) for v in V}
        ext+=(not in_Ddc(par,x))
    bad+=ext
    print(name,'|V|',len(V),'nonzero D_dc supports',len(sup),'prefixes',len(pre),'equal',ok,'I-extension failures',ext)
xc=dict(o=F(1,5),p=F(0),u=F(2,5),v=F(2,5))
print('control interior-zero support is prefix:',frozenset(v for v in xc if xc[v]!=0) in {frozenset(Y) for Y in prefixes(T)},'in D_dc',in_Ddc(T,xc))
print('PASS' if bad==0 else 'FAIL')
