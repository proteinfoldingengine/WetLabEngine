"""Post-run independent artifact checks; decode result.json.xz first."""
import pathlib,json,sympy as s
p=pathlib.Path(__file__).resolve().parent;r=json.loads((p/'result.json').read_text());dec=lambda a:s.Matrix([[s.Rational(t) for t in row] for row in a])
def proj(m):
 b=s.Matrix.hstack(*m.columnspace());return b*(b.T*b).inv()*b.T
for x in r['exact']:
 c=dec(x['C']);pl,pr=proj(c),proj(c.T);ns=[]
 for name in ['plus','minus']:
  z=x[name];n=(s.eye(3)-pl)*dec(z['V'])*(s.eye(3)-pr);assert n==dec(z['normal']);assert n.rank()==z['normal_rank'];assert z['rank_certificate']['certified'];ns.append(n)
 assert ns[0]!=s.zeros(3) and ns[1]==-ns[0];assert x['predicted_gap_squared']==4*ns[0].rank()
assert (len(r['exact']),len(r['rows']),len(r['finite']))==(144,576,1728)
out={'independent_column_basis_normal_checks':288,'nonzero_reversal_checks':144,'complete':True};(p/'PUBLICATION_CHECK.json').write_text(json.dumps(out,indent=2)+'\n');print(out)
