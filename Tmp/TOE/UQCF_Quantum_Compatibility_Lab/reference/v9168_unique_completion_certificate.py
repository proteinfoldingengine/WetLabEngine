"""v9.168: uniqueness and an exact spectral distinction of optimal marginals.

SymPy only. The proof covers the entire optimal-extension set, not a
selection among certificates. No entropy or evolution calculation is used.
"""
import math
import sympy as s
R=s.Rational
n=5;D=R(51,5);tt=R(31,51);zz=R(8)
VA=s.Matrix(n,n,lambda i,j:(j-i)%n)
VB=s.Matrix([[0,1,2,3,4],[1,0,3,4,2],[2,4,0,1,3],[3,2,4,0,1],[4,3,1,2,0]])
roots={0:s.Integer(2),1:s.Integer(1),2:s.sqrt(R(8,5)),3:s.sqrt(R(12,5)),4:s.sqrt(R(16,5))}
def clean(M):return M.applyfunc(s.simplify)
def ix(a,b,c):return (n*a+b)*n+c
def embed(B,p):
 O=s.zeros(n**3,n**3,cls=s.SparseMatrix)
 for (i,j),v in B.todok().items():
  a,b=divmod(i,n);c,d=divmod(j,n)
  for k in range(n):
   u,w=(ix(a,b,k),ix(c,d,k)) if p==1 else (ix(a,k,b),ix(c,k,d))
   O[u,w]+=v
 return O
def marginal(T,p):
 O=s.zeros(n*n,n*n,cls=s.SparseMatrix)
 for (i,j),v in T.todok().items():
  a,b,c=i//n**2,(i//n)%n,i%n
  d,e,f=j//n**2,(j//n)%n,j%n
  if p==1 and c==f:O[n*a+b,n*d+e]+=v
  if p==2 and b==e:O[n*a+c,n*d+f]+=v
 return clean(O)
bell=s.SparseMatrix(n*n,1,{((n+1)*i,0):1 for i in range(n)})
Phi=bell*bell.T/n
moments=[];distances=[]
for label,V in [('A',VA),('B',VB)]:
 assert all(sorted(V.row(i))==list(range(5)) and sorted(V.col(i))==list(range(5)) for i in range(5))
 F=V.applyfunc(lambda v:roots[v]);C=s.simplify(sum(F.row(0)))
 assert clean(F*s.ones(n,1)-C*s.ones(n,1))==s.zeros(n,1)
 assert clean(F.T*s.ones(n,1)-C*s.ones(n,1))==s.zeros(n,1)
 B=s.SparseMatrix(n*n,n*n,{(n*i+j,n*i+j):V[i,j]/50 for i in range(n) for j in range(n) if i!=j})
 qs={v:s.simplify(C/n*(1-1/roots[v])) for v in (1,2,3,4)}
 assert qs[1]==0 and all(qs[v].is_positive for v in (2,3,4))
 assert all(s.simplify(1-q).is_positive and s.simplify(C/n-2*q).is_positive for q in qs.values())
 W=Phi+s.SparseMatrix(n*n,n*n,{(n*i+j,n*i+j):qs[V[i,j]] for i in range(n) for j in range(n) if i!=j})
 O=embed(W,1)+embed(W,2)
 zs=[];stars=set()
 for k in range(n):
  v=s.zeros(n**3,1,cls=s.SparseMatrix)
  for i in range(n):
   amp=1 if i==k else F[i,k]
   v[ix(i,i,k)]+=amp;v[ix(i,k,i)]+=amp
  assert s.simplify((v.T*v)[0])==2*D
  assert clean(O*v-C*v/n)==s.zeros(n**3,1)
  co={i for i,j in v.todok()};assert not stars.intersection(co);stars.update(co)
  # Connected nonnegative star + positive eigenvector => simple top eigenvalue.
  reached={next(iter(co))}
  while True:
   more={j for i in reached for j in co if i!=j and O[i,j]!=0}
   new=reached|more
   if new==reached:break
   reached=new
  assert reached==co
  zs.append(v)
 for i in range(n**3):
  if i not in stars:assert s.simplify(C/n-O[i,i]).is_positive
 for (i,j),v in O.todok().items():
  if i not in stars or j not in stars:assert i==j
 for k in range(n):
  for l in range(n):assert s.simplify((zs[k].T*zs[l])[0])==(2*D if k==l else 0)
 T=sum((v*v.T for v in zs),s.zeros(n**3,n**3,cls=s.SparseMatrix))/(2*n*D)
 assert s.trace(T)==1
 sig=marginal(T,1);assert sig==marginal(T,2)
 E=clean(tt*Phi+(1-tt)*B-sig)
 dd=s.simplify(tt-C*C/(2*n*D));distances.append(dd)
 assert dd.is_positive
 assert clean(E*bell-dd*bell)==s.zeros(n*n,1)
 for i in range(n):
  for j in range(n):
   if i!=j:
    target=R(-1,510) if V[i,j]==1 else 0
    assert E[n*i+j,n*i+j]==target
 for (i,j),v in E.todok().items():
  if i!=j:assert i%(n+1)==0 and j%(n+1)==0
 assert s.simplify(s.trace(W*(tt*Phi+(1-tt)*B))-C/(2*n)-dd)==0

 # Exhaustive linear parametrization of every density operator in the top space.
 X=s.Matrix(n,n,lambda i,j:s.Symbol('x%d%d'%(i,j)))
 TX=sum((X[k,l]*zs[k]*zs[l].T for k in range(n) for l in range(n)),s.zeros(n**3,n**3,cls=s.SparseMatrix))/(2*D)
 sx=marginal(TX,1)
 sxb=clean(sx*bell)
 for i in range(n):
  for j in range(n):
   if i==j:continue
   assert s.simplify(sxb[n*i+j]-C*F[i,j]*X[j,i]/(2*D))==0
   assert s.simplify(sx[n*i+j,n*i+j]-F[i,j]**2*X[j,j]/(2*D))==0
 # Complementarity forces all off-diagonal X entries to vanish by the first
 # identity. One active edge in each column forces X_jj=1/n by the second.
 for j in range(n):
  i=next(i for i in range(n) if V[i,j]==4)
  diagonal_solution=s.simplify((1-tt)*B[n*i+j,n*i+j]*2*D/F[i,j]**2)
  assert diagonal_solution==R(1,n)
 assert clean(TX.subs({X[i,j]:R(1,n) if i==j else 0 for i in range(n) for j in range(n)})-T)==s.zeros(n**3)

 # Both optimal marginals also have identical one-system marginals.
 for side in (0,1):
  red=s.Matrix(n,n,lambda i,j:sum(sig[n*i+k,n*j+k] if side==0 else sig[n*k+i,n*k+j] for k in range(n)))
  assert clean(red-s.eye(n)/n)==s.zeros(n)
 moment=s.simplify(s.trace(sig*sig));moments.append(moment)
 assert not T.has(s.Float) and not sig.has(s.Float)
 print(label,'full optimum, top-space dimension 5, uniqueness equations and local marginals: PASS',flush=True)

gap=s.simplify(moments[1]-moments[0])
coeff={2:112,3:328,10:24,5:-280,6:-72,15:-148}
expected=(580+sum(c*s.sqrt(k) for k,c in coeff.items()))/65025
assert s.simplify(gap-expected)==0
# Rational lower bound; signed terms use the appropriate root endpoint.
scale=10**8
lower=s.Integer(580)
for k,c in coeff.items():
 lo=R(math.isqrt(k*scale*scale),scale);hi=lo+R(1,scale)
 assert lo*lo<=k<hi*hi
 lower+=c*(lo if c>0 else hi)
assert lower/65025>R(1,10000)
assert s.simplify(distances[0]-distances[1])==0
print('Exact second-moment gap B-A:',gap)
print('Rationally certified gap > 1/10000: PASS')
print('Both optimizer spectra: five eigenvalues 1/5; 120 zeros. Both fibers are singletons.')
print('All v9.168 checks PASS. No selection among alternative optimal certificates.')
