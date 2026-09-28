"""Post-run independent coefficient checks; does not rerun the ensemble."""
import pathlib,json,lzma,sympy as s
p=pathlib.Path(__file__).resolve().parent;r=json.loads(lzma.decompress((p/'result.json.xz').read_bytes()));parent=json.loads(lzma.decompress((p.parent/'coherence-family/result.json.xz').read_bytes()));key=lambda x:(x['candidate'],x['a'],x['arm'],x['order']);old={key(x):x for x in parent['exact']};dec=lambda a:s.Matrix([[s.Rational(t) for t in row] for row in a]);lam=s.Symbol('ell',real=True);t=s.Symbol('s',real=True)
def proj(m):
 b=s.Matrix.hstack(*m.columnspace());return b*(b.T*b).inv()*b.T
cache={}
for x in r['exact']:
 k=key(x);c=dec(x['C']);vc=list(map(dec,x['V_coefficients']));wc=list(map(dec,x['W_coefficients']));n=dec(x['normal']);pp=proj(c);qq=proj(c.T);l=s.eye(3)-pp;rr=s.eye(3)-qq
 assert c==dec(old[k]['C']) and vc==list(map(dec,old[k]['V_coefficients'])) and wc==list(map(dec,old[k]['W_coefficients']))
 assert pp==dec(x['left_projector']) and qq==dec(x['right_projector'])
 assert l*vc[0]*rr==s.zeros(3) and l*vc[1]*rr==n!=s.zeros(3)
 assert c.T*n==s.zeros(3) and n.T*c==s.zeros(3)
 mc=[l*m*rr for m in wc];assert mc==list(map(dec,x['M_coefficients']))
 assert sum(abs(v) for m in vc for v in m)==s.Rational(x['uniform_bound_V'])
 assert sum(abs(v) for m in wc for v in m)==s.Rational(x['uniform_bound_W'])
 assert s.trace(n.T*n)==s.Rational(x['normal_norm_squared']) and n.rank()==x['normal_rank']
 m=sum((lam**i*z for i,z in enumerate(mc)),s.zeros(3));ks=lam*n+t*m
 parsed=[s.Matrix([[s.sympify(z.replace('lambda','ell'),locals={'ell':lam}) for z in row] for row in mat]) for mat in x['normal_energy_coefficients']]
 assert (ks.T*ks-sum((t**i*z for i,z in enumerate(parsed)),s.zeros(3))).applyfunc(s.expand)==s.zeros(3)
 for i in range(2):assert c.T*vc[i]+vc[i].T*c==dec(x['gram_derivative_coefficients'][i])
 assert all(x[z] for z in ['normal_identity','gram_first_order_blind','energy_identity','bound_valid']);cache[k]=(c,n)
for x in r['pairs']:
 k=x['candidate'],x['a'],x['arm'];c,n=cache[*k,'after'];cb,nb=cache[*k,'before'];a=s.Rational(*x['a'].as_integer_ratio());assert c==cb and nb==a*n
 assert dec(x['normal_contrast'])==n-nb;assert x['nonzero']==(x['a']!=1.);assert s.Rational(x['normal_contrast_norm_squared'])==s.trace((n-nb).T*(n-nb))
expected={(k,l,p,d,f) for k in cache for l in [-1,0,1] for p in [8,64] for d in [80,120] for f in [0,1]};observed={(key(x),x['lambda'],x['step_power'],x['precision'],x['frame']) for x in r['rows']};assert len(cache)==144 and len(r['pairs'])==72 and expected==observed and len(r['rows'])==3456
out={'independent_column_basis_projector_checks':144,'exact_normal_and_gram_blindness_checks':144,'energy_polynomial_checks':144,'uniform_bound_coefficient_checks':144,'order_pair_checks':72,'nonidentity_nonzero_coefficients':sum(x['a']!=1. for x in r['pairs']),'complete_numeric_keys':3456,'complete':True};(p/'PUBLICATION_CHECK.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out))
