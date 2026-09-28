"""Post-run independent artifact checks; decode result.json.xz first."""
import pathlib,json,sympy as s,collections
p=pathlib.Path(__file__).resolve().parent;r=json.loads((p/'result.json').read_text());dec=lambda a:s.Matrix([[s.Rational(t) for t in row] for row in a]);cache={}
def proj(m):
 b=s.Matrix.hstack(*m.columnspace());return b*(b.T*b).inv()*b.T
for x in r['exact']:
 c,v,n=map(dec,[x['C'],x['V'],x['normal']]);pl,pr=proj(c),proj(c.T);assert (s.eye(3)-pl)*v*(s.eye(3)-pr)==n;assert n.rank()==x['normal_rank'];assert c.rank()==x['rank'];assert c.T*n==s.zeros(3) and c*n.T==s.zeros(3);assert x['rank_certificate']['certified'];cache[x['candidate'],x['a'],x['arm'],x['order']]=(c,n)
for x in r['pairs']:
 k=x['candidate'],x['a'],x['arm'];a=cache[*k,'after'];b=cache[*k,'before'];assert a[0]==b[0] and b[1]==s.Rational(*x['a'].as_integer_ratio())*a[1]
assert len(r['exact'])==144 and len(r['pairs'])==72 and len(r['rows'])==576 and len(r['finite'])==1440
out={'independent_column_basis_projector_checks':144,'exact_order_checks':72,'complete':True};(p/'PUBLICATION_CHECK.json').write_text(json.dumps(out,indent=2)+'\n');print(out)
