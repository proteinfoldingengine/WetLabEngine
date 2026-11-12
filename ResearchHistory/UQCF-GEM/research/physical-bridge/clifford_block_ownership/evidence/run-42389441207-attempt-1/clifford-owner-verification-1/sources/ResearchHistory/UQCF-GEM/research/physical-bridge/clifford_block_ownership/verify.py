"""Independent exact SymPy reconstruction of the entire frozen universe."""
import hashlib,itertools,json,sys
from pathlib import Path
import sympy as s
BASE=Path(__file__).resolve().parent
I=s.I; e=s.eye(2); x=s.Matrix([[0,1],[1,0]]);y=s.Matrix([[0,-I],[I,0]]);z=s.diag(1,-1)
single={'I':e,'X':x,'Y':y,'Z':z}
def tensor(*xs):return s.kronecker_product(*xs)
# Independently build Clifford matrices from the tensor definition.
g=[]
for site in range(4):
 for axis in (x,y):g.append(tensor(*([z]*site+[axis]+[e]*(3-site))))
g.append(tensor(z,z,z,z)); one=s.eye(16);zero=s.zeros(16)
local=[];omega=[];expected={f'G/{i}':a for i,a in enumerate(g)}
for v in range(3):
 a,b,c=g[3*v:3*v+3]
 row=[one,-I*b*c,-I*c*a,-I*a*b];local.append(row);omega.append(-I*a*b*c)
 expected[f'O/{v}']=omega[-1]
 for k in range(1,4):expected[f'L/{v}/{k}']=row[k]
for a,b,c in itertools.product(range(4),repeat=3):expected[f'B/{a}/{b}/{c}']=local[0][a]*local[1][b]*local[2][c]
data=json.loads(Path(sys.argv[1]).read_bytes())
assert set(data)=={'schema','source_sha256','count','records'}
assert data['schema']==1 and data['source_sha256']=='c60909871daba6a08219e0b9b84a0d017548b994080b5c8514addfb57419d740'
assert hashlib.sha256((BASE/'SOURCE_ARGUMENT.md').read_bytes()).hexdigest()==data['source_sha256']
records=data['records'];assert data['count']==85==len(records)
assert [r['id'] for r in records]==sorted(expected)
for r in records:
 assert set(r)=={'id','phase','word'} and type(r['phase'])==int and r['phase'] in range(4)
 assert len(r['word'])==4 and set(r['word'])<=set(single)
 matrix=I**r['phase']*tensor(*(single[c] for c in r['word']))
 assert matrix==expected[r['id']],r['id']
checks={}
count=0
for v,i,j in itertools.product(range(3),range(1,4),range(1,4)):
 rhs=one if i==j else sum((I*s.LeviCivita(i,j,k)*local[v][k] for k in range(1,4)),zero)
 assert local[v][i]*local[v][j]==rhs;count+=1
checks['local_products']=count
count=0
for a,b in itertools.combinations(range(3),2):
 for i,j in itertools.product(range(1,4),repeat=2):assert local[a][i]*local[b][j]==local[b][j]*local[a][i];count+=1
checks['cross_commutators']=count
for v,k in itertools.product(range(3),range(3)):assert omega[v]*local[v][k+1]==g[3*v+k]
checks['omega_factorization']=9
for i,v,k in itertools.product(range(9),range(3),range(1,4)):assert s.trace(g[i]*local[v][k])==0
checks['vector_local_traces']=81
basis=[expected[k] for k in sorted(expected) if k.startswith('B/')]
# Exact sparse Frobenius products; equals trace(A^dagger B).
sparse=[dict(m.todok()) for m in basis]
for i,a in enumerate(sparse):
 for j,b in enumerate(sparse):assert sum(s.conjugate(val)*b.get(key,0) for key,val in a.items())==(16 if i==j else 0)
checks['joint_basis_gram']=4096
for a,v,k in itertools.product(range(3),range(3),range(1,4)):assert omega[a]*local[v][k]==local[v][k]*omega[a]
checks['omega_local_commutators']=27
for a,b in itertools.combinations(range(3),2):assert omega[a]*omega[b]+omega[b]*omega[a]==zero
checks['omega_anticommutators']=3
for a in omega:assert a.H==a and a*a==one and s.trace(a)==0
print(json.dumps(dict(status='PASS',count=len(expected),checks=checks,native_bridge='NOT_DERIVED'),indent=2,sort_keys=True))
