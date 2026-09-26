"""v15.59 second non-closed source-law comparison."""
from __future__ import annotations
import argparse,hashlib,importlib.util,json,pathlib,sys,numpy as np
HERE=pathlib.Path(__file__).resolve().parent;PARENT=HERE.parent;sys.path.insert(0,str(PARENT))
import independent_hidden_fixture as F
import independent_hidden_geometry as G
import response_quotient_rank as R
def load(path,name):
 s=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
SE=load(PARENT/'source-edge-factorization'/'gate.py','se')
ASYM=load(PARENT/'asymmetric-heldout-ensemble'/'gate.py','asym')
ETA=1e-3;S_FILTER=.137;NONCLOSURE_MIN=1e-8;ACTIVE_TOL=1e-4
EXPECTED=[13,16,22,25,27,29,37,39,46,50,66,77]
def sha(x):return hashlib.sha256(x).hexdigest()
def states():
 z=ASYM.select_states()
 if [x['candidate_index'] for x in z]!=EXPECTED:raise RuntimeError('frozen state identity mismatch')
 return z
def filter_update(rho,s,p):
 w,v=np.linalg.eigh((p+p.conj().T)/2);A=(v*np.exp(.5*s*w))@v.conj().T
 z=A@rho@A;z=z/np.trace(z);return (z+z.conj().T)/2
def filter_edge_map(rho):
 O=np.asarray(G.geom(rho)[1]);activity=np.array([np.linalg.norm(np.asarray(G.geom(filter_update(rho,S_FILTER,p))[1])-O) for p in R.PB])
 M=np.zeros((3,243,3,3));nonclosure=np.zeros(243);j=0
 for h in R.HB:
  for p in R.PB:
   ro={};st={}
   for ie in (-1,1):
    for js in (-1,1):
     z=filter_update(rho+ie*ETA*h,js*S_FILTER,p);st[(ie,js)]=z;ro[(ie,js)]=np.asarray(G.geom(z)[1])
   M[:,j]=(ro[(1,1)]-ro[(1,-1)]-ro[(-1,1)]+ro[(-1,-1)])/(4*ETA*S_FILTER)
   # Hidden distinguishability of proper marginals after active positive filter.
   nonclosure[j]=G.marginal_diff(st[(1,1)],st[(-1,1)])
   j+=1
 return SE.edge_map(M,O),activity,nonclosure
def align(A,B):
 # Compare normalized maps and their 9-dimensional row subspaces in R^243.
 ua,sa,vha=np.linalg.svd(A,full_matrices=False);ub,sb,vhb=np.linalg.svd(B,full_matrices=False)
 ra=int(np.sum(sa>sa[0]*1e-10));rb=int(np.sum(sb>sb[0]*1e-10))
 Va=vha[:ra].T;Vb=vhb[:rb].T
 cos=np.linalg.svd(Va.T@Vb,compute_uv=False) if ra and rb else np.array([])
 alpha=float(np.vdot(A,B).real/max(np.vdot(A,A).real,1e-300))
 resid=float(np.linalg.norm(B-alpha*A)/max(np.linalg.norm(B),1e-300))
 nres=float(np.linalg.norm(B/np.linalg.norm(B)-A/np.linalg.norm(A)))
 return {'principal_cosines':cos.tolist(),'min_principal_cosine':float(cos.min()) if len(cos) else 0.,'optimal_scalar_alpha':alpha,'scalar_fit_relative_residual':resid,'normalized_map_distance':nres}
def measure_state(row):
 rho=row['rho'];Ee=ASYM.exponential_edge_map(rho);Ef,act,nc=filter_edge_map(rho)
 return {'candidate_index':np.array(row['candidate_index']),'rho':rho,'columns':SE.COLUMNS.copy(),'E_exp':Ee,'E_filter':Ef,'filter_source_change':act,'nonclosure':nc}
def evaluate_arrays(z):
 e=[]
 if not np.array_equal(z['columns'],SE.COLUMNS):e.append('columns mismatch')
 if not all(np.isfinite(np.asarray(x)).all() for x in z.values()):e.append('nonfinite')
 active=int(np.sum(z['filter_source_change']>ACTIVE_TOL));mn=float(z['nonclosure'].max())
 if active!=9:e.append('filter source inactive')
 if mn<=NONCLOSURE_MIN:e.append('filter nonclosure not demonstrated')
 re=SE.rank_info(z['E_exp']);rf=SE.rank_info(z['E_filter']);al=align(z['E_exp'],z['E_filter'])
 return {'ranks':{'E_exp':re,'E_filter':rf},'active_source_count':active,'max_nonclosure':mn,'exp_norm':float(np.linalg.norm(z['E_exp'])),'filter_norm':float(np.linalg.norm(z['E_filter'])),'alignment':al},e
def run(out):
 out=pathlib.Path(out)
 if out.exists():raise ValueError('output exists')
 out.mkdir(parents=True);rows=[];hashes={};valid=True
 for i,row in enumerate(states()):
  z=measure_state(row);m,e=evaluate_arrays(z);valid&=not e
  fn=out/f'state_{i:02d}.npz';np.savez_compressed(fn,**z);hashes[fn.name]=sha(fn.read_bytes())
  rows.append({'candidate_index':row['candidate_index'],'metrics':m,'errors':e,'artifact':fn.name})
 suff=all(x['metrics']['ranks']['E_filter']['rank']>0 for x in rows)
 verdict='INVALID' if not valid else ('NONCLOSURE_SUFFICIENT_FOR_RESPONSE_ON_ENSEMBLE' if suff else 'NONCLOSURE_NOT_SUFFICIENT_ON_ENSEMBLE')
 r={'selected_count':len(rows),'candidate_indices':EXPECTED,'all_controls_pass':bool(valid),'response_on_all_states':bool(suff),'verdict':verdict,'artifact_sha256':hashes,'rows':rows}
 (out/'report.json').write_text(json.dumps(r,indent=2,sort_keys=True)+'\n')
 if verdict=='INVALID':raise RuntimeError('invalid')
 return r
def verify(out):
 out=pathlib.Path(out);r=json.loads((out/'report.json').read_text());rows=[];valid=True
 if r['candidate_indices']!=EXPECTED:raise ValueError('state identity mismatch')
 for i in range(12):
  fn=out/f'state_{i:02d}.npz'
  if r['artifact_sha256'].get(fn.name)!=sha(fn.read_bytes()):raise ValueError('hash mismatch')
  with np.load(fn,allow_pickle=False) as a:z={k:a[k] for k in a.files}
  m,e=evaluate_arrays(z);rows.append(m);valid&=not e
 suff=all(x['ranks']['E_filter']['rank']>0 for x in rows)
 verdict='INVALID' if not valid else ('NONCLOSURE_SUFFICIENT_FOR_RESPONSE_ON_ENSEMBLE' if suff else 'NONCLOSURE_NOT_SUFFICIENT_ON_ENSEMBLE')
 if verdict!=r['verdict']:raise ValueError('verdict mismatch')
 return {'verified':True,'verdict':verdict,'selected_count':12}
def main():
 ap=argparse.ArgumentParser();x=ap.add_mutually_exclusive_group(required=True);x.add_argument('--output');x.add_argument('--verify');a=ap.parse_args()
 try:z=run(a.output) if a.output else verify(a.verify);print(json.dumps(z,indent=2,sort_keys=True));return 0
 except Exception as e:print(json.dumps({'verdict':'INVALID','error':str(e)}),file=sys.stderr);return 2
if __name__=='__main__':raise SystemExit(main())
