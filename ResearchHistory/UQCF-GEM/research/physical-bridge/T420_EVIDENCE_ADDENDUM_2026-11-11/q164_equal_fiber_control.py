import sys,importlib.util,os; sys.dont_write_bytecode=True
spec=importlib.util.spec_from_file_location('q164',os.path.join(os.path.dirname(__file__),'q164.py'))
# reuse run() without re-running the module's main checks: exec only defs
src=open(os.path.join(os.path.dirname(__file__),'q164.py')).read().split("X=[(),(0,),(0,0),(0,1)]")[0]
ns={'__file__':os.path.join(os.path.dirname(__file__),'q164.py')}; exec(src,ns)
F=ns['F']
# GPT 6811938453 counterexample: o=(),p=(0,),u=(1,),v=(0,0); prune u,v -> Y=(o,p); fibers {o,u},{p,v}
ok=ns['run']([(),(0,),(1,),(0,0)],[(),(0,)],[(),(0,)],'EQUAL_FIBER_4to2')
# corrected C4 criterion across trees: counting covariant iff all b_y == n/m
pca=ns['pca']
cases=[([(),(0,),(0,0),(0,1)],[(),(0,),(0,1)]),([(),(0,),(1,),(0,0)],[(),(0,)]),([(),(0,),(1,),(0,0),(1,0)],[(),(0,),(1,)]),([(),(0,),(1,),(0,0),(0,1),(1,0)],[(),(0,),(1,),(0,1)])]
for f,c in cases:
    P=pca.operators(f,c)['P']; n,m=len(f),len(c); b=[int(sum(r)) for r in P]
    cov=[sum(F(x,n) for x in r) for r in P]==[F(1,m)]*m; crit=all(F(x)==F(n,m) for x in b)
    print('fibers',b,'n/m',F(n,m),'covariant',cov,'criterion',crit,'agree',cov==crit); ok&=(cov==crit)
print('ALL_PASS' if ok else 'SOME_FAIL')
