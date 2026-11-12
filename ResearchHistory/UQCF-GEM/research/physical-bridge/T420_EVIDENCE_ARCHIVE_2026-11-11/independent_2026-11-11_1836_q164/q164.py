import sys,random,importlib.util,os; sys.dont_write_bytecode=True
spec=importlib.util.spec_from_file_location('pca',os.path.join(os.path.dirname(__file__),'pca_94d946df.py')); pca=importlib.util.module_from_spec(spec); spec.loader.exec_module(pca)
from fractions import Fraction as F
random.seed(164)
def col(v): return [[F(a)] for a in v]
def vec(M): return [r[0] for r in M]
def G(keys): return pca.green(pca.laplacian(keys))
def run(fine,coarse,pv,label,gpt=None):
    d=pca.operators(fine,coarse); P=d['P']; S=d['S']; n,m=len(fine),len(coarse)
    Gf,Gc=G(fine),G(coarse); ip,iv=[coarse.index(k) for k in pv]; jp,jv=[fine.index(k) for k in pv]
    def contrast_before(x,ref): y=vec(pca.mul(Gf,col([a-sum(x)*r for a,r in zip(x,ref)]))); return y[jp]-y[jv]
    def contrast_after(x,ref): px=vec(pca.mul(P,col(x))); y=vec(pca.mul(Gc,col([a-sum(px)*r for a,r in zip(px,ref)]))); return y[ip]-y[iv]
    cf=[F(1,n)]*n; cc=[F(1,m)]*m
    bg=vec(pca.mul(Gc,col([a-b for a,b in zip(vec(pca.mul(P,col(cf))),cc)]))); gain=bg[ip]-bg[iv]
    ok=True
    if gpt:
        for x,(b,a) in gpt.items():
            cb,ca=contrast_before(x,cf),contrast_after(x,cc); print(label,'C1 x=',x,'before',cb,'after',ca,'match',(cb,ca)==(b,a)); ok&=(cb,ca)==(b,a)
    for t in range(20):
        x=[F(random.randint(0,9)) for _ in range(n)]; x=[a/(sum(x) or 1) for a in x]
        c2=contrast_after(x,cc)-contrast_before(x,cf)==gain; ok&=c2
        w=[F(random.randint(1,9)) for _ in range(n)]; w=[a/sum(w) for a in w]; wc=vec(pca.mul(P,col(w)))
        c3=contrast_before(x,w)==contrast_after(x,wc); ok&=c3
    c4=(vec(pca.mul(P,col(cf)))==cc)
    print(label,'gain(counting reset)=',gain,'C2,C3 all',ok,' counting P-covariant:',c4,' fiber sizes',[int(sum(r)) for r in P])
    return ok
X=[(),(0,),(0,0),(0,1)]; Y=[(),(0,),(0,1)]   # o,p,u,v ; delete u
a=run(X,Y,[(0,),(0,1)],'GPT',{(F(1,5),F(1,5),F(2,5),F(1,5)):(F(1,20),F(2,15)),(F(1,5),F(1,5),F(1,5),F(2,5)):(F(-3,20),F(-1,15))})
b=run([(),(0,),(1,),(0,0),(0,1),(1,0)],[(),(0,),(1,),(0,1)],[(0,),(1,)],'T6')
c=run([(),(0,),(0,0),(0,0,0),(0,1)],[(),(0,),(0,1)],[(0,),(0,1)],'T5chain')
print('ALL_PASS' if a and b and c else 'SOME_FAIL')
