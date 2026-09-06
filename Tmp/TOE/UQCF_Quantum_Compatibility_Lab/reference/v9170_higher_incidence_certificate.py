"""v9.170: exact equal-marginal kernel dimensions on the full optimal support.

This script uses exact arithmetic in Q(sqrt(2),sqrt(5)); no numerical ranks.
Additional validation and reporting are completed in the accompanying proof.
"""
import collections
import itertools
import sympy as s
from sympy.polys.matrices import DomainMatrix
R=s.Rational
n=5;z=R(16);t=R(21,41);D=R(74,5);c=R(1,164)
VA=s.Matrix(n,n,lambda i,j:(j-i)%n)
VB=s.Matrix([[0,1,2,3,4],[1,0,3,4,2],[2,4,0,1,3],[3,2,4,0,1],[4,3,1,2,0]])
field=s.QQ.algebraic_field(s.sqrt(2),s.sqrt(5))
def coords(V):
 F=V.applyfunc(lambda v:s.Integer(2) if v==0 else s.sqrt(min(s.Integer(4),z*v/10)))
 vectors=[]
 for k in range(n):
  v={}
  for i in range(n):
   amp=s.Integer(1) if i==k else F[i,k]
   for ijk in ((i,i,k),(i,k,i)):v[ijk]=v.get(ijk,0)+amp
  vectors.append(v)
 exterior=[]
 for i in range(n):
  neighbors=[j for j in range(n) if V[i,j]>=3]
  assert len(neighbors)==2
  for j in neighbors:
   for k in neighbors:
    vectors.append({(i,j,k):s.Integer(1)});exterior.append((i,j,k))
 return F,vectors,exterior

def maps(vectors):
 d=len(vectors);out=[{},{}]
 for u,U in enumerate(vectors):
  for v,V in enumerate(vectors):
   col=u*d+v
   for (a,b,c),x in U.items():
    for (e,f,g),y in V.items():
     if c==g:
      row=out[0].setdefault((n*a+b,n*e+f),{})
      row[col]=row.get(col,0)+x*y
     if b==f:
      row=out[1].setdefault((n*a+c,n*e+g),{})
      row[col]=row.get(col,0)+x*y
 return out

def dm_from_rows(rows,cols):
 # Small coefficient alphabet: cache field conversion of exact expanded entries.
 cache={};data={}
 for i,row in enumerate(rows):
  dr={}
  for j,v in row.items():
   v=s.expand(v)
   if v==0:continue
   if v not in cache:cache[v]=field.from_sympy(v)
   dr[j]=cache[v]
  if dr:data[i]=dr
 return DomainMatrix(data,(len(rows),cols),field)

def clean(M):return M.applyfunc(s.simplify)
def ix(i,j,k):return (n*i+j)*n+k
def matrix_of(vectors):
 return s.SparseMatrix(n**3,len(vectors),{(ix(*ijk),col):v for col,vec in enumerate(vectors) for ijk,v in vec.items()})
def marginal(T,p):
 M=s.zeros(n*n,n*n,cls=s.SparseMatrix)
 for (i,j),v in T.todok().items():
  a,b,c=i//n**2,(i//n)%n,i%n
  d,e,f=j//n**2,(j//n)%n,j%n
  if p==1 and c==f:M[n*a+b,n*d+e]+=v
  if p==2 and b==e:M[n*a+c,n*d+f]+=v
 return clean(M)
def embed(B,p):
 O=s.zeros(n**3,n**3,cls=s.SparseMatrix)
 for (i,j),v in B.todok().items():
  a,b=divmod(i,n);c,d=divmod(j,n)
  for k in range(n):
   u,w=(ix(a,b,k),ix(c,d,k)) if p==1 else (ix(a,k,b),ix(c,k,d))
   O[u,w]+=v
 return O

def verify_unique_marginal(V,F,mu):
 # Every optimal residual annihilates off-diagonal coordinate kets.
 # With two saturated incoming edges, each pair has at most two common
 # predecessors; among the other three labels a star coefficient can be isolated.
 for j in range(n):
  for k in range(n):
   if j==k:continue
   i=next(i for i in range(n) if i!=j and i!=k and not (V[i,j]>=3 and V[i,k]>=3))
   row=mu[0][(n*i+j,n*i+k)]
   assert set(row)=={j*25+k}
   assert s.simplify(row[j*25+k]-F[i,j]*F[i,k])==0
  i=next(i for i in range(n) if 0<V[i,j]<3)
  row=mu[0][(n*i+j,n*i+j)]
  assert set(row)=={j*25+j}
  assert s.simplify(row[j*25+j]-F[i,j]**2)==0
  assert s.simplify((1-t)*V[i,j]/50/F[i,j]**2)==c
 for i in range(n):
  for j in range(n):
   row=mu[0][((n+1)*i,(n+1)*j)]
   assert row==mu[1][((n+1)*i,(n+1)*j)]
   assert all(col//25<5 and col%25<5 for col in row)

def verify_geometry(V,F,vecs,ext):
 C=s.simplify(sum(F.row(0)));lam=C/n
 assert all(s.simplify(sum(F.row(i))-C)==0 and s.simplify(sum(F.col(i))-C)==0 for i in range(n))
 L=matrix_of(vecs)
 assert clean(L.T*L-s.diag(*([2*D]*5+[1]*20)))==s.zeros(25)
 bell=s.SparseMatrix(25,1,{((n+1)*i,0):1 for i in range(n)})
 Phi=bell*bell.T/n
 B=s.SparseMatrix(25,25,{(n*i+j,n*i+j):V[i,j]/50 for i in range(n) for j in range(n) if i!=j})
 qs={v:s.simplify(lam*(1-1/s.sqrt(min(s.Integer(4),z*v/10)))) for v in (1,2,3,4)}
 assert all(q.is_positive and s.simplify(1-q).is_positive for q in qs.values())
 assert all(s.simplify(lam-2*qs[v]).is_positive for v in (1,2))
 assert all(s.simplify(lam-2*qs[v])==0 for v in (3,4))
 W=Phi+s.SparseMatrix(25,25,{(n*i+j,n*i+j):qs[V[i,j]] for i in range(n) for j in range(n) if i!=j})
 O=embed(W,1)+embed(W,2)
 assert clean(O*L-lam*L)==s.zeros(125,25)
 stars=set()
 for vec in vecs[:5]:
  co={ix(*ijk) for ijk in vec};assert not co.intersection(stars);stars.update(co)
  reached={next(iter(co))}
  while True:
   new=reached|{j for i in reached for j in co if i!=j and O[i,j]!=0}
   if new==reached:break
   reached=new
  assert reached==co
 extcoords={ix(*ijk) for ijk in ext};assert not extcoords.intersection(stars)
 for i in range(125):
  if i not in stars|extcoords:assert s.simplify(lam-O[i,i]).is_positive
 for (i,j),v in O.todok().items():
  if i not in stars or j not in stars:assert i==j
 # Faithful state on ALL 25 top directions: positive product tables in
 # each two-neighbor exterior block, not just the diagonal |ijj> vectors.
 coeff=[c]*5+[R((1 if V[i,j]==3 else 3)*(1 if V[i,k]==3 else 3),820) for i,j,k in ext]
 assert all(x>0 for x in coeff)
 X0=s.SparseMatrix(s.diag(*coeff));T0=L*X0*L.T
 assert s.trace(T0)==1 and not T0.has(s.Float)
 sig=marginal(T0,1);assert sig==marginal(T0,2)
 E=clean(t*Phi+(1-t)*B-sig)
 dd=s.simplify(t-c*C*C);assert dd.is_positive
 assert clean(E*bell-dd*bell)==s.zeros(25,1)
 for (i,j),v in E.todok().items():assert i%(n+1)==0 and j%(n+1)==0
 assert s.simplify(s.trace(W*(t*Phi+(1-t)*B))-lam/2-dd)==0
 return sig

def exact_kernel(mu):
 M=dm_from_rows(list(mu[0].values())+list(mu[1].values()),625)
 reduced,pivots=M.rref()
 rank=len(pivots);nullity=625-rank
 kernel=reduced.nullspace()
 assert kernel.shape==(nullity,625)
 assert (M*kernel.transpose()).is_zero_matrix
 return rank,nullity

def parity_counts(vecs,ext):
 fixed=[{v:s.Integer(1)} for v in ext if v[1]==v[2]]
 pairs=[(i,j,k) for i,j,k in ext if j<k]
 plus=[{(i,j,k):s.Integer(1),(i,k,j):s.Integer(1)} for i,j,k in pairs]
 minus=[{(i,j,k):s.Integer(1),(i,k,j):s.Integer(-1)} for i,j,k in pairs]
 bs=vecs[:5]+fixed+plus+minus
 assert len(fixed)==10 and len(plus)==len(minus)==5
 mu=maps(bs)[0];result=[]
 choices=[('even',[u*25+v for u in range(25) for v in range(25) if (u<20)==(v<20)]),
          ('odd',[u*25+v for u in range(25) for v in range(25) if (u<20)!=(v<20)]),
          ('symmetric_support',[u*25+v for u in range(20) for v in range(20)])]
 for name,indices in choices:
  remap={old:new for new,old in enumerate(indices)}
  rows=[{remap[j]:x for j,x in row.items() if j in remap} for row in mu.values()]
  M=dm_from_rows(rows,len(indices))
  reduced,pivots=M.rref();kernel=reduced.nullspace()
  assert (M*kernel.transpose()).is_zero_matrix
  result.append(len(indices)-len(pivots))
 return tuple(result)

def normalized_arrangements():
 options=[]
 for i in range(5):
  opts=[]
  for p in itertools.permutations(range(1,5)):
   row=list(p);row.insert(i,0);opts.append(row)
  options.append(opts)
 result=[]
 def visit(mat):
  i=len(mat)
  if i==5:result.append(s.Matrix(mat));return
  for row in options[i]:
   if all(row[j] not in [r[j] for r in mat] for j in range(5)):visit(mat+[row])
 visit([[0,1,2,3,4]])
 return result

if __name__=='__main__':
 cache={}
 for label,V,expected in [('A',VA,(310,315)),('B',VB,(314,311))]:
  F,vecs,ext=coords(V)
  verify_geometry(V,F,vecs,ext)
  mu=maps(vecs);verify_unique_marginal(V,F,mu)
  ranks=exact_kernel(mu);assert ranks==expected;cache[tuple(V)]=ranks
  print(label,'full top support, faithful optimum, unique marginal, exact rank/nullity:',ranks,': PASS',flush=True)
  parity=parity_counts(vecs,ext)
  assert parity==((210,105,185) if label=='A' else (206,105,181))
  assert parity[0]+parity[1]==ranks[1]
  print(label,'swap-even / swap-odd / symmetric-support dimensions:',parity,': PASS',flush=True)
 arrangements=normalized_arrangements();assert len(arrangements)==56
 hist=collections.Counter();motifs=collections.Counter()
 for index,V in enumerate(arrangements):
  assert all(sorted(V.row(i))==list(range(5)) and sorted(V.col(i))==list(range(5)) for i in range(5))
  F,vecs,ext=coords(V);mu=maps(vecs);verify_unique_marginal(V,F,mu)
  if tuple(V) not in cache:cache[tuple(V)]=exact_kernel(mu)
  rank,dim=cache[tuple(V)];hist[dim]+=1
  S=V.applyfunc(lambda x:1 if x>=3 else 0)
  reciprocal=int(s.trace(S*S)/2);triangles=int(s.trace(S**3)/3)
  motifs[(reciprocal,triangles,dim)]+=1
  if (index+1)%14==0:print('Complete exact census:',index+1,'of 56',flush=True)
 assert hist=={311:10,313:20,315:6,321:20}
 assert set(motifs)=={(3,2,311),(2,2,313),(2,4,321),(5,0,315),(0,5,315)}
 print('Exact dimension census:',dict(sorted(hist.items())))
 print('Exact (reciprocal pairs, directed 3-cycles, dimension): counts:',dict(sorted(motifs.items())))
 print('All v9.170 checks PASS. Fixed n=5, four specified weights, z=16; no general motif law inferred.')
