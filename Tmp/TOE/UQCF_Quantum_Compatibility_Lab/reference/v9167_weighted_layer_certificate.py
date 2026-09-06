"""v9.167: exact full-curve weighted-layer certificates (SymPy only).

General symbolic identities + independent finite operator regressions.
The accompanying analytic proof covers all dimensions and all regular layers.
"""
import sympy as s
R=s.Rational
z,a,ml,ms,wi,ws,h,n=s.symbols('z a ml ms wi ws h n',positive=True)
Ae=a+ml+2*ms;b=2*wi+ws
D=a+ml+z*wi+4*ms;C=Ae+s.sqrt(z)*h
H=b+2*Ae/z;t=1-1/H
beta=2*D*(1-t)/z;gamma=(1-t)*(ws-4*ms/z)
d=t-(1-t)*C*C/(n*z)
qbar=C*(wi-h/s.sqrt(z)+ws/2)/n
assert s.factor(beta+gamma-1)==0
assert s.factor(t+(1-t)*qbar-C/(2*n)-d)==0
assert s.simplify(s.diff(d,z)/s.diff(t,z)-(1-qbar))==0
assert s.simplify(s.diff(1-qbar,z)/s.diff(t,z)-h*H**3*z**R(3,2)/(8*n*Ae))==0
assert s.factor(z-2*Ae*(1-t)/(1-b*(1-t)))==0
print('General normalization, dual equality, scalar inversion and derivatives: PASS',flush=True)

def clean(M):return M.applyfunc(s.simplify)
def layers_of(W):
 nn=W.rows
 assert W.cols==nn and all(W[i,i]==0 for i in range(nn))
 assert all(sum(W.row(i))==1 and sum(W.col(i))==1 for i in range(nn))
 out=[]
 for w in sorted(set(W)-{s.Integer(0)}):
  edges={(i,j) for i in range(nn) for j in range(nn) if W[i,j]==w}
  m=len(edges)//nn
  assert w>0 and m>0
  assert all(sum(i==k for i,j in edges)==m and sum(j==k for i,j in edges)==m for k in range(nn))
  out.append((w,m,edges))
 return out

def scalar(layers,nn,zz):
 aa=nn+1-sum(m for w,m,e in layers)
 xs=[s.sqrt(min(s.Integer(4),max(s.Integer(1),zz*w))) for w,m,e in layers]
 DD=aa+sum(m*x*x for (w,m,e),x in zip(layers,xs))
 CC=aa+sum(m*x for (w,m,e),x in zip(layers,xs))
 HH=2*DD/zz+sum(m*(w-4/zz) for w,m,e in layers if zz*w>=4)
 tt=1-1/HH;bb=2*DD*(1-tt)/zz
 gs=[m*(1-tt)*(w-4/zz) if zz*w>=4 else s.Integer(0) for w,m,e in layers]
 dd=s.simplify(tt-(1-tt)*CC*CC/(nn*zz))
 assert HH>1 and 0<tt<1 and 0<bb<=1 and all(g>=0 for g in gs)
 assert bb+sum(gs)==1
 return xs,DD,CC,tt,bb,gs,dd

def check(Wgt,zz,label):
 nn=Wgt.rows;layers=layers_of(Wgt)
 xs,DD,CC,tt,bb,gs,dd=scalar(layers,nn,zz)
 lam=CC/nn
 qs=[s.simplify(lam*(1-1/x)) for x in xs]
 assert all((x-1).is_nonnegative and (2-x).is_nonnegative for x in xs)
 assert all(q.is_nonnegative and s.simplify(1-q).is_nonnegative and s.simplify(lam-2*q).is_nonnegative for q in qs)
 def ix(i,j,k):return (nn*i+j)*nn+k
 def embed(B,p):
  O=s.zeros(nn**3,nn**3,cls=s.SparseMatrix)
  for (i,j),v in B.todok().items():
   a,b=divmod(i,nn);c,d=divmod(j,nn)
   for k in range(nn):
    u,w=(ix(a,b,k),ix(c,d,k)) if p==1 else (ix(a,k,b),ix(c,k,d))
    O[u,w]+=v
  return O
 def marginal(T,p):
  O=s.zeros(nn*nn,nn*nn,cls=s.SparseMatrix)
  for (i,j),v in T.todok().items():
   a,b,c=i//nn**2,(i//nn)%nn,i%nn
   d,e,f=j//nn**2,(j//nn)%nn,j%nn
   if p==1 and c==f:O[nn*a+b,nn*d+e]+=v
   if p==2 and b==e:O[nn*a+c,nn*d+f]+=v
  return clean(O)
 bell=s.SparseMatrix(nn*nn,1,{((nn+1)*i,0):1 for i in range(nn)})
 Phi=bell*bell.T/nn
 Qs=[s.SparseMatrix(nn*nn,nn*nn,{(nn*i+j,nn*i+j):1 for i,j in edges}) for w,m,edges in layers]
 Ts=[s.SparseMatrix(nn**3,nn**3,{(ix(i,j,j),ix(i,j,j)):R(1,nn*m) for i,j in edges}) for w,m,edges in layers]
 B=sum((w*Q/nn for (w,m,e),Q in zip(layers,Qs)),s.zeros(nn*nn,nn*nn,cls=s.SparseMatrix))
 TB=sum((m*w*T for (w,m,e),T in zip(layers,Ts)),s.zeros(nn**3,nn**3,cls=s.SparseMatrix))
 assert marginal(TB,1)==B==marginal(TB,2)
 W=Phi+sum((q*Q for q,Q in zip(qs,Qs)),s.zeros(nn*nn,nn*nn,cls=s.SparseMatrix))
 O=embed(W,1)+embed(W,2)
 amps={edge:x for (w,m,edges),x in zip(layers,xs) for edge in edges}
 zs=[];stars=set()
 for k in range(nn):
  v=s.zeros(nn**3,1,cls=s.SparseMatrix)
  for i in range(nn):
   amp=amps.get((i,k),s.Integer(1))
   v[ix(i,i,k)]+=amp;v[ix(i,k,i)]+=amp
  assert s.simplify((v.T*v)[0]-2*DD)==0
  assert clean(O*v-lam*v)==s.zeros(nn**3,1)
  co={i for i,j in v.todok()};assert not stars.intersection(co);stars.update(co)
  zs.append(v)
 for (i,j),v in O.todok().items():
  if i not in stars or j not in stars:
   assert i==j and s.simplify(lam-v).is_nonnegative
 Tstar=sum((v*v.T for v in zs),s.zeros(nn**3,nn**3,cls=s.SparseMatrix))/(2*nn*DD)
 T=bb*Tstar+sum((g*Tj for g,Tj in zip(gs,Ts)),s.zeros(nn**3,nn**3,cls=s.SparseMatrix))
 assert not W.has(s.Float) and not T.has(s.Float)
 assert s.trace(T)==1
 for g,Tj in zip(gs,Ts):
  if g>0:assert clean(O*Tj-lam*Tj)==s.zeros(nn**3)
 sig=marginal(T,1);assert sig==marginal(T,2)
 E=clean(tt*Phi+(1-tt)*B-sig)
 assert clean(E*bell-dd*bell)==s.zeros(nn*nn,1)
 assert dd.is_nonnegative
 for i in range(nn):
  for j in range(nn):
   if i==j:continue
   expected=(1-tt)*(Wgt[i,j]-1/zz)/nn if zz*Wgt[i,j]<=1 else 0
   assert s.simplify(E[nn*i+j,nn*i+j]-expected)==0 and expected<=0
 for (i,j),v in E.todok().items():
  if i!=j:assert i%(nn+1)==0 and j%(nn+1)==0
 dual=s.simplify(s.trace(W*(tt*Phi+(1-tt)*B))-lam/2)
 assert s.simplify(dual-dd)==0
 print(label,'z =',zz,'t =',tt,': PASS',flush=True)
 return dd

VA=s.Matrix(5,5,lambda i,j:(j-i)%5)
VB=s.Matrix([[0,1,2,3,4],[1,0,3,4,2],[2,4,0,1,3],[3,2,4,0,1],[4,3,1,2,0]])
assert s.trace((VA/50)**2)==R(1,25)
assert s.trace((VB/50)**2)==R(13,250)
WA,WB=VA/10,VB/10
# One point in every open phase, plus the simultaneous boundary at z=10.
for zz in map(s.Integer,(1,3,4,8,10,12,16,25,64)):
 da=check(WA,zz,'Four-level cyclic arrangement')
 db=check(WB,zz,'Four-level inequivalent arrangement')
 assert s.simplify(da-db)==0
# Boundary continuity: both limiting single-layer H expressions agree.
w=s.symbols('w',positive=True)
assert s.simplify((2/z-2*w).subs(z,1/w))==0
assert s.simplify((2*w-(w+4/z)).subs(z,4/w))==0
layers=layers_of(WA)
for zz in sorted({R(1)/w for w,m,e in layers}|{R(4)/w for w,m,e in layers}):scalar(layers,5,zz)
assert scalar(layers,5,R(40))[3]==R(1,3)
assert scalar(layers,5,R(5,2))[3]==R(19,24)

# Sparse case: two simultaneously saturated levels and one interior level.
Ws=s.zeros(6)
for i in range(6):
 for j in (1,2,3):Ws[i,(i+j)%6]=R(j,6)
check(Ws,R(15),'Sparse three-level source')
# Repeated layer degrees: two incoming/outgoing edges of each weight.
Wr=s.zeros(5)
for i in range(5):
 for j in (1,2,3,4):Wr[i,(i+j)%5]=R(1,6) if j<=2 else R(1,3)
check(Wr,R(8),'Repeated-degree weighted layers')

# A known arrangement-sensitive control must not pass this theorem's hypothesis.
Vbad=s.Matrix([[0,1,2,4,3],[3,0,1,4,2],[2,4,0,1,3],[3,1,4,0,2],[2,4,3,1,0]])
try:layers_of(Vbad/10)
except AssertionError:pass
else:raise AssertionError('Irregular weight layers were incorrectly admitted')
print('20 exact operator regressions, all scalar boundaries, and hypothesis null: PASS')
print('Distinct target-unitary invariants 1/25 and 13/250: PASS')
print('All v9.167 checks PASS. General theorem is analytic, not inferred from samples.')
