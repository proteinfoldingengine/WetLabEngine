"""16.20 exact second-order local information classification."""
from pathlib import Path
import importlib.util,json,subprocess
import sympy as sp
HERE=Path(__file__).resolve().parent
def scalar_coeffs(C,V,W):
 s=sp.symbols('s');X=C+s*V+s*s*W;G=X.T*X
 vals=[sp.expand(sp.trace(G**k)) for k in (1,2,3)]+[sp.expand(X.det())]
 return [[sp.expand(z).coeff(s,i) for i in (0,1,2)] for z in vals]
def audit():
 # use 16.12 loader: exact C,V(lambda),W(lambda) already certified physical
 pth=HERE.parent/'continuous-response'/'gate.py';spec=importlib.util.spec_from_file_location('p12',pth);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
 parent=m.load_parent()
 if len(parent['exact'])!=144: raise ValueError('parent coverage')
 # exact archived coefficients; compare four jets per baseline: order x lambda basis endpoints 0,1
 groups={}
 for x in parent['exact']:
  C=m.B.decode(x['C']);vc=list(map(m.B.decode,x['V_coefficients']));wc=list(map(m.B.decode,x['W_coefficients']))
  ky=(x['candidate'],x['a'],x['arm'])
  for lam in (0,1):
   V=vc[0]+lam*vc[1];W=sum((sp.Integer(lam)**i*z for i,z in enumerate(wc)),sp.zeros(3))
   first=[];second=[]
   for c,v,w in [(C,V,W)]:
    for z in scalar_coeffs(c,v,w): first.append(z[1]);second.append(z[2])
   groups.setdefault(ky,[]).append({'order':x['order'],'lambda':lam,'V':V,'W':W,'first':tuple(first),'second':tuple(second)})
 out=[];adds=0
 for ky,recs in sorted(groups.items()):
  # Pairwise information test on finite realized jets: does second order separate a pair not separated at first?
  hidden=[]
  for i in range(len(recs)):
   for j in range(i):
    same1=recs[i]['first']==recs[j]['first'];same2=recs[i]['second']==recs[j]['second']
    matrixdiff=(recs[i]['V']!=recs[j]['V'] or recs[i]['W']!=recs[j]['W'])
    if same1 and matrixdiff and not same2:hidden.append([j,i])
  add=bool(hidden);adds+=add
  out.append({'candidate':ky[0],'a':ky[1],'arm':ky[2],'realized_jets':len(recs),'second_order_adds_distinction':add,'newly_separated_pairs':hidden})
 verdict='SECOND_ORDER_LOCAL_INFORMATION_ADDS_DISTINCTIONS' if adds==len(out) else 'FIRST_ORDER_LOCAL_INFORMATION_SUFFICIENT_FOR_REALIZED_JETS' if adds==0 else 'MIXED_SECOND_ORDER_INFORMATION'
 return {'version':'16.20','all_valid':len(out)==72,'verdict':verdict,'metrics':{'groups':len(out),'groups_with_second_order_gain':adds,'newly_separated_pairs':sum(len(x['newly_separated_pairs']) for x in out)},'groups':out,'scope':'Finite realized second-order physical jets; information classification only.'}
if __name__=='__main__':
 r=audit();r['execution_head']=subprocess.check_output(['git','rev-parse','HEAD'],cwd=HERE,text=True).strip();(HERE/'result.json').write_text(json.dumps(r,indent=2,sort_keys=True)+'\n');print(json.dumps({'all_valid':r['all_valid'],'verdict':r['verdict'],'metrics':r['metrics']}))
