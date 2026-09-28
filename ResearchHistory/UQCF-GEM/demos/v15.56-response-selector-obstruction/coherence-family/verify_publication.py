"""Independent post-run exact coefficient and rank checks; no ensemble rerun."""
import pathlib,json,lzma,itertools,sympy as s
p=pathlib.Path(__file__).resolve().parent;r=json.loads(lzma.decompress((p/'result.json.xz').read_bytes()));parent=json.loads(lzma.decompress((p.parent/'source-reversal/result.json.xz').read_bytes()));old={(x['candidate'],x['a'],x['arm'],x['order']):x for x in parent['exact']};dec=lambda a:s.Matrix([[s.Rational(t) for t in row] for row in a]);z=s.zeros(3);t=s.Symbol('s');lam=s.Symbol('lambda');cache={}
def proj(m):
 b=s.Matrix.hstack(*m.columnspace());return b*(b.T*b).inv()*b.T
for x in r['exact']:
 key=x['candidate'],x['a'],x['arm'],x['order'];c=dec(x['C']);vs=list(map(dec,x['V_coefficients']));ws=list(map(dec,x['W_coefficients']));n=dec(x['plus_normal']);pl,pr=proj(c),proj(c.T)
 assert (s.eye(3)-pl)*vs[0]*(s.eye(3)-pr)==z
 assert (s.eye(3)-pl)*vs[1]*(s.eye(3)-pr)==n!=z
 assert n.rank()==x['normal_rank'] and c.rank()==x['rank']
 cz=c+t*vs[0]+t*t*ws[0];rank=x['rank'];assert s.expand(cz.det())==0
 if rank==1:
  assert all(s.expand(cz.extract(i,j).det())==0 for i in itertools.combinations(range(3),2) for j in itertools.combinations(range(3),2))
 assert any(c.extract(i,j).det()!=0 for i in itertools.combinations(range(3),rank) for j in itertools.combinations(range(3),rank))
 if rank+x['normal_rank']!=3:assert all(m[i,2]==m[2,i]==0 for m in [c,*vs,*ws] for i in range(3))
 for sign,name in [(1,'plus'),(-1,'minus')]:
  assert vs[0]+sign*vs[1]==dec(old[key][name]['V'])
  assert ws[0]+sign*ws[1]+ws[2]==dec(old[key][name]['quadratic'])
 assert x['normal_identity'] and x['all_classes_certified'] and x['zero_certificate']['polynomial_rank']==rank
 cache[key]=(c,n)
for x in r['pairs']:
 key=x['candidate'],x['a'],x['arm'];a,b=cache[*key,'after'],cache[*key,'before'];assert a[0]==b[0] and b[1]==s.Rational(*x['a'].as_integer_ratio())*a[1]
keys=set(cache);assert len(keys)==144
expected={(k,l,d,f) for k in keys for l in ['-1/2','0','1/2'] for d in [80,120] for f in [0,1]}
observed={((x['candidate'],x['a'],x['arm'],x['order']),x['lambda'],x['precision'],x['frame']) for x in r['rows']};assert expected==observed and len(r['rows'])==1728
expected={(k,l,d,f) for k in keys for l in ['-1/2','0','1/2'] for d in [32,128,192] for f in [0,1]}
observed={((x['candidate'],x['a'],x['arm'],x['order']),x['lambda'],x['step_power'],x['frame']) for x in r['finite']};assert expected==observed and len(r['finite'])==2592
out={'independent_projector_normal_identity_checks':144,'independent_zero_rank_minor_checks':144,'endpoint_coefficient_checks':288,'order_agreement_checks':72,'complete_limit_keys':1728,'complete_finite_keys':2592,'complete':True};(p/'PUBLICATION_CHECK.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out))
