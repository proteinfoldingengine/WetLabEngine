import sys; sys.dont_write_bytecode=True
import sympy as sp
a10,a11,a20,a21,a22,b=sp.symbols('a10 a11 a20 a21 a22 b')
def ref(x):  # x=(o,p,u,v); tree o->p, p->u, p->v; o=root depth0, p depth1, u,v depth2
    xo,xp,xu,xv=x; M=xo+xp+xu+xv; mp=xp+xu+xv; mu,mv=xu,xv
    w={'o':b*M,'p':0,'u':0,'v':0}
    # edge (o,p), child depth 1: weights j=0 -> M, j=1 -> m_p
    e=a10*M+a11*mp; w['p']+=e; w['o']-=e
    for c,mc in (('u',mu),('v',mv)):  # edges (p,c), child depth 2: j=0 M, j=1 m_p, j=2 m_c
        e=a20*M+a21*mp+a22*mc; w[c]+=e; w['p']-=e
    return w
F=sp.Rational
xp=(F(1,5),F(1,5),F(2,5),F(1,5)); xm=(F(1,5),F(1,5),F(1,5),F(2,5))
def cond(x): w=ref(x); return sp.expand(x[1]*w['u']-x[2]*w['p'])  # fixed iff 0
cp,cm=cond(xp),cond(xm)
print("fixed(x+) iff",cp,"= 0"); print("fixed(x-) iff",cm,"= 0")
print("difference",sp.expand(cp-cm))
sub={a10:0,a20:0,a21:0}
print("diagonal-only (j=d): x+:",cp.subs(sub)," x-:",cm.subs(sub)," coincide-as-sets:",sp.simplify(cp.subs(sub)/cm.subs(sub)) if cm.subs(sub)!=0 else 'x- cond 0')
