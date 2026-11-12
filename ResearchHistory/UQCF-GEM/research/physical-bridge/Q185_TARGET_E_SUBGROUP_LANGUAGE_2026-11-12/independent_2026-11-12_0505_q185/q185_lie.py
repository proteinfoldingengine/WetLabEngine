# Q185 supplementary checks (added at revision 2026-11-12 for Engineering change 2; NOT preregistered; disclosed).
# Exact sympy checks of the finite-dimensional facts used in the H° -> H ⊆ N(L) argument.
import sympy as sp
I2=sp.eye(2); sx=sp.Matrix([[0,1],[1,0]]); sy=sp.Matrix([[0,-sp.I],[sp.I,0]]); sz=sp.Matrix([[1,0],[0,-1]])
S=[sx,sy,sz]; kron=sp.kronecker_product
k=lambda e,r: sp.Matrix([1 if i==2*e+r else 0 for i in range(4)])
def margR(v):
    M=v*v.H; return sp.Matrix(2,2,lambda r,s: sum(M[2*e+r,2*e+s] for e in range(2)))
def dR(e0,eu):
    Dm=sp.simplify(margR(eu)-margR(e0)); ev=Dm.eigenvals()
    return sp.simplify(sum(sp.Abs(x)*m for x,m in ev.items())/2/5)
def opschmidt(U):  # operator-Schmidt rank via realignment
    R=sp.zeros(4,4)
    for a in range(2):
     for b in range(2):
      for c in range(2):
       for d in range(2):
        R[2*a+c,2*b+d]=U[2*a+b,2*c+d]
    return R.rank()
# (e) u(4) = l ⊕ p ; Ad(L) acts irreducibly on p
loc=[sp.I*kron(s,I2) for s in S]+[sp.I*kron(I2,s) for s in S]
l=[sp.I*sp.eye(4)]+loc
p=[sp.I*kron(a,b) for a in S for b in S]
vec=lambda X: sp.Matrix([sp.re(x) for x in X]+[sp.im(x) for x in X])
print('(e1) dim span(l ⊕ p) over R =',sp.Matrix.hstack(*[vec(X) for X in l+p]).rank(),'(u(4) has 16)')
P=sp.Matrix.hstack(*[vec(X) for X in p])
def coords(Y):
    sol=P.solve_least_squares(vec(Y)) if False else (P.T*P).inv()*P.T*vec(Y)
    assert sp.simplify(P*sol-vec(Y))==sp.zeros(32,1), 'not in p'
    return sol
ads=[sp.Matrix.hstack(*[coords(sp.expand(X*Y-Y*X)) for Y in p]) for X in loc]
m=sp.symbols('m0:81'); M=sp.Matrix(9,9,m)
eqs=[e for A in ads for e in (M*A-A*M)]
sol=sp.linsolve(eqs,m); free=set().union(*[x.free_symbols for x in list(sol)[0]])
print('(e2) [loc,p] ⊆ p: True ; dim real commutant of ad(loc)|p =',len(free),'(1 => irreducible)')
# (f) SWAP
SW=sp.Matrix([[1,0,0,0],[0,0,1,0],[0,1,0,0],[0,0,0,1]])
print('(f) d_R(SWAP·W_R) =',dR(SW*k(0,0),SW*k(0,1)),' SWAP·|01> = |10>:',SW*k(0,1)==k(1,0),' op-Schmidt rank SWAP =',opschmidt(SW))
a,b,c,d=sp.symbols('a b c d')
A=sp.Matrix([[a,b],[c,d]]); B=sp.Matrix(2,2,sp.symbols('w x y z'))
print('    SWAP(A⊗B)SWAP = B⊗A:',sp.simplify(SW*kron(A,B)*SW-kron(B,A))==sp.zeros(4,4))
# (g) CZ
CZ=sp.diag(1,1,1,-1); plus=sp.Matrix([1,1])/sp.sqrt(2)
out=CZ*kron(plus,plus)
print('(g) op-Schmidt rank CZ =',opschmidt(CZ),' (A⊗B has 1)  Schmidt rank CZ|++> =',sp.Matrix(2,2,list(out)).rank(),' (product-preserving maps give 1)')
# (h) Ctrl_E sufficiency, general U0 in U(2)
al,be,ga,de=sp.symbols('alpha beta gamma delta',real=True)
U0=sp.Matrix([[sp.cos(al)*sp.exp(sp.I*be),-sp.sin(al)*sp.exp(-sp.I*ga)],[sp.sin(al)*sp.exp(sp.I*ga),sp.cos(al)*sp.exp(-sp.I*be)]])*sp.exp(sp.I*de)
U1=sp.Matrix(2,2,sp.symbols('u0:4'))  # arbitrary; does not act on E=0 inputs
g=kron(sp.diag(1,0),U0)+kron(sp.diag(0,1),U1)
Dm=sp.simplify(margR(g*k(0,1))-margR(g*k(0,0)))
print('(h) Ctrl_E: Tr(Dm) =',sp.simplify(Dm.trace()),' det(Dm) =',sp.simplify(Dm.det()),' (det=-1 => d=1/5); CZ in Ctrl_E with U0=I,U1=Z')
# (i) H_3 generator G is imprimitive
G=sp.eye(4); c3,s3=sp.cos(2*sp.pi/3),sp.sin(2*sp.pi/3); G[0,0]=c3;G[0,3]=-s3;G[3,0]=s3;G[3,3]=c3
print('(i) Schmidt rank G|00> =',sp.Matrix(2,2,list(G*k(0,0))).rank(),' op-Schmidt rank G =',opschmidt(G))
