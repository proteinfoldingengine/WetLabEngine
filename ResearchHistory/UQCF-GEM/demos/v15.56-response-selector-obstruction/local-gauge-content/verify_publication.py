"""Independent exact orbit-witness and physical determinant coefficient checks."""
import pathlib,json,lzma,sympy as s,itertools
p=pathlib.Path(__file__).resolve().parent;r=json.loads(lzma.decompress((p/'result.json.xz').read_bytes()));parent=json.loads(lzma.decompress((p.parent/'continuous-response/result.json.xz').read_bytes()));key=lambda x:(x['candidate'],x['a'],x['arm'],x['order']);old={key(x):x for x in parent['exact']};dec=lambda a:s.Matrix([[s.Rational(z) for z in row] for row in a]);t,lam=s.symbols('t ell',real=True);cache={}
# Direct six-term formula avoids the audit's determinant/cofactor routines.
def det(m):return m[0,0]*(m[1,1]*m[2,2]-m[1,2]*m[2,1])-m[0,1]*(m[1,0]*m[2,2]-m[1,2]*m[2,0])+m[0,2]*(m[1,0]*m[2,1]-m[1,1]*m[2,0])
for x in r['exact']:
 k=key(x);c,n,j=map(dec,[x['C'],x['N'],x['J']]);b=s.Matrix.hstack(*c.columnspace());proj=b*(b.T*b).inv()*b.T;assert j==2*proj-s.eye(3) and j.T*j==s.eye(3) and j*c==c and j*n==-n
 assert det(j)==s.Rational(x['J_determinant']);poly=s.expand(det(c+t*n));coeff=[poly.coeff(t,i) for i in range(4)];assert coeff==list(map(s.Rational,x['determinant_coefficients']))
 if x['classification']=='SO_SIGN_EQUIVALENT':assert det(j)==1 and c.rank()==1
 elif x['classification']=='SO_SIGN_DISTINGUISHED':assert coeff[1]!=0 and c.rank()==2 and det(j)==-1
 else:raise AssertionError('unclassified')
 assert c==dec(old[k]['C']) and n==dec(old[k]['normal']);vc=list(map(dec,old[k]['V_coefficients']));wc=list(map(dec,old[k]['W_coefficients']));v=vc[0]+lam*vc[1];w=sum((lam**i*m for i,m in enumerate(wc)),s.zeros(3));actual=s.expand(det(c+t*v+t*t*w));first=actual.coeff(t,1);second=actual.coeff(t,2)
 assert first==lam*coeff[1]
 if c.rank()==1:assert second==lam**2*coeff[2]
 parsed=[s.sympify(z.replace('lambda','ell'),locals={'ell':lam}) for z in x['physical_determinant_s_coefficients']];assert parsed==[first,second]
 assert s.trace(n.T*n)==s.Rational(x['normal_norm_squared']);cache[k]=(c,n)
for x in r['pairs']:
 k=x['candidate'],x['a'],x['arm'];ca,na=cache[*k,'after'];cb,nb=cache[*k,'before'];a=s.Rational(*x['a'].as_integer_ratio());assert ca==cb and nb==a*na;assert s.trace(nb.T*nb)==a*a*s.trace(na.T*na);assert x['energy_distinguishes_order']==(x['a']!=1.)
expected={(k,d,f) for k in cache for d in [80,120] for f in [0,1]};actual={(key(x),x['precision'],x['frame']) for x in r['rows']};assert len(cache)==144 and len(r['pairs'])==72 and expected==actual and len(r['rows'])==576
out={'independent_stabilizer_checks':144,'determinant_pencil_checks':144,'full_physical_polynomial_checks':144,'amplitude_order_checks':72,'complete_numeric_keys':576,'complete':True};(p/'PUBLICATION_CHECK.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out))
