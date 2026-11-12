import sympy as sp
t=sp.symbols('t',positive=True)
def kron(a,b): return sp.kronecker_product(a,b)
k=lambda e,r: sp.Matrix([1 if i==2*e+r else 0 for i in range(4)])  # |e r>
def margR(v):  # Tr_E |v><v| ; index 2e+r
    M=v*v.H; return sp.Matrix(2,2,lambda r,s: sum(M[2*e+r,2*e+s] for e in range(2)))
def dR(e0,eu):
    Dm=sp.simplify(margR(eu)-margR(e0)); ev=Dm.eigenvals()
    return sp.simplify(sum(sp.Abs(x)*m for x,m in ev.items())/2/5)
# (a)
eu=((1-t**2)*k(1,0)+2*t*k(0,1))/(1+t**2)
print('(a) d_R(W_t) - 4t^2/[5(1+t^2)^2] =',sp.simplify(dR(k(0,0),eu)-4*t**2/(5*(1+t**2)**2)), ' norm check', sp.simplify((eu.H*eu)[0]-1))
# (b) H_3
def rot(th):
    G=sp.eye(4); c,s=sp.cos(th),sp.sin(th)
    G[0,0]=c;G[0,3]=-s;G[3,0]=s;G[3,3]=c; return G
G=rot(2*sp.pi/3)
print('(b) G^3 = I:',sp.simplify(G**3)==sp.eye(4), ' unitary:',sp.simplify(G.H*G)==sp.eye(4))
for n in range(3):
    g=G**n; e0=g*k(0,0); e1=g*k(0,1)
    print('   n',n,'d =',dR(e0,e1),' Schmidt rank e0 =',sp.Matrix(2,2,list(e0)).rank())
# (c) L orbit symbolic
a,b,c,d,al,be=sp.symbols('a b c d alpha beta',real=True)
B=sp.Matrix([[sp.cos(a)*sp.exp(sp.I*b), -sp.sin(a)*sp.exp(-sp.I*c)],[sp.sin(a)*sp.exp(sp.I*c), sp.cos(a)*sp.exp(-sp.I*b)]])*sp.exp(sp.I*d)
A=sp.Matrix([[sp.cos(al),-sp.sin(al)],[sp.sin(al),sp.cos(al)]])*sp.diag(1,sp.exp(sp.I*be))
U=kron(A,B); Dm=sp.simplify(margR(U*k(0,1))-margR(U*k(0,0)))
print('(c) L: Tr(Dm)=',sp.simplify(Dm.trace()),' det(Dm)=',sp.simplify(Dm.det()),' (eigs ±1 iff det=-1, so d=1/5)')
# (d) control Z_4
G4=rot(sp.pi/2); vals=[dR(G4**n*k(0,0),G4**n*k(0,1)) for n in range(4)]
print('(d) Z_4 control d values',vals,' hits B_R:',0 in vals)
