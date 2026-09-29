"""16.19 exact realized-response kernel classification."""
from pathlib import Path
import hashlib,json,lzma,subprocess
import sympy as sp
HERE=Path(__file__).resolve().parent; P=HERE.parent/'network-interpretation'
XZ='3b3f5e075ef129640f135b76780544ea268bd22bbc2efb17cd4d3b3dbebe2b81'
def dec(m): return sp.Matrix([[sp.Rational(x) for x in row] for row in m])
def local(c,v):
 g=c.T*c; dg=c.T*v+v.T*c
 return [sp.expand(k*sp.trace(g**(k-1)*dg)) for k in (1,2,3)]+[sp.expand(sum(c.cofactor(i,j)*v[i,j] for i in range(3) for j in range(3)))]
def classify_matrix(j):
 M=sp.Matrix(j); n=M.cols; r=int(M.rank()); k=n-r
 return n,r,k,'NONTRIVIAL_RESPONSE_INFORMATION_KERNEL' if k else 'LOCAL_SCALARS_COMPLETE_ON_REALIZED_RESPONSE'
def audit():
 raw=(P/'result.json.xz').read_bytes()
 if hashlib.sha256(raw).hexdigest()!=XZ: raise ValueError('parent hash')
 p=json.loads(lzma.decompress(raw)); paths=p.get('exact')
 # 16.15 exact omits full path matrices; reconstruct them from bound 16.14 through its parent loader.
 import importlib.util
 gp=HERE.parent/'network-interpretation'/'gate.py'; s=importlib.util.spec_from_file_location('p15',gp);m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
 parent=m.load_parent(); rows=parent['paths']
 if len(rows)!=144: raise ValueError('path coverage')
 groups={}
 for x in rows:
  ky=(x['candidate'],x['a'],x['arm'])
  C=[dec(z) for z in x['C']]; V0=[dec(z) for z in x['V0']];V1=[dec(z) for z in x['V1']]
  # realized coefficient responses are full six-edge V0 and V1; vectorize exactly
  for label,V in [('constant',V0),('coherence',V1)]:
   vec=sp.Matrix([q for z in V for q in list(z)])
   vals=sp.Matrix([q for c,v in zip(C,V) for q in local(c,v)])
   groups.setdefault(ky,[]).append((x['order'],label,vec,vals))
 out=[]
 for ky,recs in sorted(groups.items()):
  # response-span basis from realized vectors
  X=sp.Matrix.hstack(*[r[2] for r in recs]); inds=X.columnspace(); dx=len(inds)
  if dx==0: J=sp.zeros(24,0)
  else:
   # solve each basis vector as an original column and use its independently reconstructed scalar differential
   cols=[]
   for b in inds:
    idx=next(i for i,r in enumerate(recs) if r[2]==b); cols.append(recs[idx][3])
   J=sp.Matrix.hstack(*cols)
  rank=int(J.rank()); ker=dx-rank
  out.append({'candidate':ky[0],'a':ky[1],'arm':ky[2],'response_span_dim':dx,'local_rank_on_span':rank,'kernel_dim':ker,'nontrivial_kernel':ker>0})
 nk=sum(x['nontrivial_kernel'] for x in out)
 verdict='NONTRIVIAL_RESPONSE_INFORMATION_KERNEL' if nk==len(out) else 'LOCAL_SCALARS_COMPLETE_ON_REALIZED_RESPONSE' if nk==0 else 'MIXED_RESPONSE_INFORMATION_KERNEL'
 return {'version':'16.19','all_valid':len(out)==72,'verdict':verdict,'parent_xz_sha256':XZ,'groups':out,'metrics':{'groups':len(out),'nontrivial_kernel_groups':nk,'kernel_dimension_total':sum(x['kernel_dim'] for x in out),'response_span_dimension_total':sum(x['response_span_dim'] for x in out),'local_rank_total':sum(x['local_rank_on_span'] for x in out)},'interpretation':'Information-compression classification only; no geometry inferred.'}
if __name__=='__main__':
 r=audit();r['execution_head']=subprocess.check_output(['git','rev-parse','HEAD'],cwd=HERE,text=True).strip();(HERE/'result.json').write_text(json.dumps(r,indent=2,sort_keys=True)+'\n');print(json.dumps({'all_valid':r['all_valid'],'verdict':r['verdict'],'metrics':r['metrics']}))
