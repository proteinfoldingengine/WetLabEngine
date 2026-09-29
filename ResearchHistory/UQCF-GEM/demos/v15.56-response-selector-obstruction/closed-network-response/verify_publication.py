"""Independent archived-output check; complementary-chain rather than matrix-unit gradient."""
import json,lzma,itertools,pathlib
import sympy as s
P=pathlib.Path(__file__).resolve().parent
r=json.loads(lzma.decompress((P/'result.json.xz').read_bytes()))
edges=[(0,1),(1,2),(2,0),(1,3),(3,0),(2,3)];cycles=[(0,1,2),(0,1,3),(0,2,3),(1,2,3),(0,1,2,3),(0,1,3,2),(0,2,1,3)]
def dec(a):return s.Matrix([[s.Rational(x) for x in row] for row in a])
def inner(a,b):return sum(x*y for x,y in zip(a,b))
def key(x):return x['candidate'],x['a'],x['arm'],x['order']
def refs(c,cy):
 gs=[s.zeros(3) for _ in edges]
 for k,i in enumerate(cy):
  j=cy[(k+1)%len(cy)];forward=(i,j) in edges;e=edges.index((i,j) if forward else (j,i));rest=s.eye(3)
  for z in range(1,len(cy)):
   a=cy[(k+z)%len(cy)];b=cy[(k+z+1)%len(cy)];rest=rest*(c[edges.index((a,b))] if (a,b) in edges else c[edges.index((b,a))].T)
  gs[e]+=rest.T if forward else rest
 return gs
paths={key(x):x for x in r['paths']};out={};checks=0
for x in r['exact']:
 p=paths[key(x)];c=list(map(dec,p['C']));vv=[list(map(dec,p[n])) for n in ['V0','V1']];n=dec(p['N']);g=refs(c,cycles[x['cycle']]);h=(s.eye(3)-dec(p['P']))*g[5]*(s.eye(3)-dec(p['Q']));total=[sum(inner(a,b) for a,b in zip(g,v)) for v in vv];normal=inner(h,n)
 assert g[5]==dec(x['gradient']) and h==dec(x['normal_reference'])
 assert total==list(map(s.Rational,x['total'])) and normal==s.Rational(x['normal'][1])
 assert normal**2<=inner(h,h)*inner(n,n)
 assert all(total[k]==s.Rational(x['normal'][k])+s.Rational(x['sixth_tangent'][k])+s.Rational(x['other_edges'][k]) for k in [0,1])
 out[key(x),x['cycle']]=(total,normal);checks+=1
for x in r['pairs']:
 a=out[(x['candidate'],x['a'],x['arm'],'after'),x['cycle']];b=out[(x['candidate'],x['a'],x['arm'],'before'),x['cycle']]
 assert [u-v for u,v in zip(a[0],b[0])]==list(map(s.Rational,x['total'])) and a[1]-b[1]==s.Rational(x['normal'][1])
expected={(ky,cy,lam,prec,fr) for ky in paths for cy in range(7) for lam in [-1,0,1] for prec in [80,120] for fr in [0,1]}
actual={(key(x),x['cycle'],x['lambda'],x['precision'],x['frame']) for x in r['rows']}
assert checks==1008 and len(r['pairs'])==504 and len(paths)==144 and expected==actual and len(r['rows'])==len(expected)==12096 and r['all_valid'] is True
report={'independent_path_cycle_checks':checks,'exact_squared_bound_checks':checks,'independent_order_contrasts':504,'complete_numeric_keys':len(actual),'complete':True}
(P/'PUBLICATION_CHECK.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
