"""v15.58 held-out asymmetric ensemble gate."""
from __future__ import annotations
import argparse, hashlib, importlib.util, json, math, pathlib, sys
import numpy as np
HERE=pathlib.Path(__file__).resolve().parent; PARENT=HERE.parent
sys.path.insert(0,str(PARENT))
import independent_hidden_fixture as F
import independent_hidden_geometry as G
import response_quotient_rank as R
def _load(path,name):
 s=importlib.util.spec_from_file_location(name,path); m=importlib.util.module_from_spec(s); s.loader.exec_module(m); return m
SE=_load(PARENT/'source-edge-factorization'/'gate.py','v1556se')
SL=_load(PARENT/'source-law-specificity'/'gate.py','v1557sl')
SEED=20260928; TARGET=12; ETA=SL.ETA; S=SL.S
CLOSURE_TOL=SL.CLOSURE_TOL; ACTIVE_TOL=SL.ACTIVE_TOL; MIXED_RATIO_TOL=SL.MIXED_RATIO_TOL
EDGES=[(0,1),(1,2),(2,0)]
def sha256(x): return hashlib.sha256(x).hexdigest()
def candidate(index:int)->np.ndarray:
 rng=np.random.default_rng(SEED)
 for k in range(index+1):
  one=rng.normal(0,.035,size=(3,3))
  pairs=rng.normal(0,.055,size=(3,3,3))
 rho=np.eye(8,dtype=complex)
 for q in range(3):
  for a in range(3):
   ids=[0,0,0];ids[q]=a+1;rho+=one[q,a]*F.op(*ids)
 base=np.diag([.11,.085,.060]); base[0,1]-=.045; base[1,0]+=.025
 for e,(i,j) in enumerate(EDGES):
  C=base+pairs[e]
  for a in range(3):
   for b in range(3):
    ids=[0,0,0];ids[i]=a+1;ids[j]=b+1;rho+=C[a,b]*F.op(*ids)
 return rho/8
def diagnostics(rho):
 eig=np.linalg.eigvalsh(rho)
 Cs=[F.corr(rho,*e) for e in EDGES]; pol=[F.polar(c) for c in Cs]
 O=[x[0] for x in pol]; sv=[x[1] for x in pol]
 H=O[0]@O[1]@O[2]
 pair=max(float(np.linalg.norm(Cs[i]-Cs[0])) for i in (1,2))
 bloch=np.array([[F.expect(rho,{q:a}).real for a in range(1,4)] for q in range(3)])
 ba=max(float(np.linalg.norm(bloch[i]-bloch[j])) for i in range(3) for j in range(i))
 Spos=[O[e].T@Cs[e] for e in range(3)]
 return {'min_eigenvalue':float(eig.min()),'min_edge_singular':float(min(x.min() for x in sv)),
 'holonomy_angle':F.angle(H),'pair_asymmetry':pair,'bloch_asymmetry':ba,
 'min_positive_polar_eigenvalue':float(min(np.linalg.eigvalsh((x+x.T)/2).min() for x in Spos)),
 'min_rotation_determinant':float(min(np.linalg.det(x) for x in O))}
def select_states():
 out=[]
 for idx in range(5000):
  rho=candidate(idx); d=diagnostics(rho)
  ok=d['min_eigenvalue']>=.025 and d['min_edge_singular']>=.020 and d['holonomy_angle']>=.15 and d['pair_asymmetry']>=.06 and d['bloch_asymmetry']>=.025 and d['min_positive_polar_eigenvalue']>0 and d['min_rotation_determinant']>0
  if not ok: continue
  if any(np.linalg.norm(rho-z['rho'])<.02 for z in out): continue
  out.append({'candidate_index':idx,'rho':rho,'diagnostics':d})
  if len(out)==TARGET:return out
 raise RuntimeError(f'only {len(out)} states pass frozen selector')
def exponential_edge_map(rho):
 O=np.asarray(G.geom(rho)[1]); M=np.zeros((3,243,3,3));j=0
 for h in R.HB:
  for p in R.PB:
   L=G.herm_log(rho)
   # Reuse the exact historical analytic edge derivative through ORIGIN helper.
   Q=SE.ORIGIN.edge_data(rho,h,p)
   for e in range(3): M[e,j]=Q[e][3]
   j+=1
 return SE.edge_map(M,O)
def unitary_edge_map(rho):
 O=np.asarray(G.geom(rho)[1]); M=np.zeros((3,243,3,3)); closure=np.zeros(243)
 activity=np.array([np.linalg.norm(SL._edge_rotations(SL.local_unitary_update(rho,S,p))-O) for p in R.PB])
 j=0
 for h in R.HB:
  for p in R.PB:
   mm,cc=SL._mixed_unitary_edges(rho,h,p);M[:,j]=mm;closure[j]=cc;j+=1
 return SE.edge_map(M,O),activity,closure
def measure_state(row):
 rho=row['rho']; Eu,act,cl=unitary_edge_map(rho); Ee=exponential_edge_map(rho)
 return {'candidate_index':np.array(row['candidate_index']), 'rho':rho,'columns':SE.COLUMNS.copy(),
 'E_exp':Ee,'E_unitary':Eu,'unitary_source_change':act,'closure_residuals':cl,
 'selection_diagnostics':np.array([row['diagnostics'][k] for k in ['min_eigenvalue','min_edge_singular','holonomy_angle','pair_asymmetry','bloch_asymmetry','min_positive_polar_eigenvalue','min_rotation_determinant']])}
def evaluate_arrays(z):
 errors=[]; d=z['selection_diagnostics']
 if d[0]<.025 or d[1]<.020 or d[2]<.15 or d[3]<.06 or d[4]<.025 or d[5]<=0 or d[6]<=0:errors.append('selector diagnostics fail')
 if not np.array_equal(z['columns'],SE.COLUMNS):errors.append('columns mismatch')
 if not all(np.isfinite(np.asarray(v)).all() for v in z.values()):errors.append('nonfinite')
 mc=float(z['closure_residuals'].max()); ma=float(z['unitary_source_change'].max())
 if mc>CLOSURE_TOL:errors.append('closure failure')
 if np.sum(z['unitary_source_change']>ACTIVE_TOL)!=9:errors.append('unitary source inactive')
 re=SE.rank_info(z['E_exp']); scale=float(re['singular_values'][0]);ru=SE.rank_info(z['E_unitary'],reference_scale=scale)
 ratio=float(np.linalg.norm(z['E_unitary'])/max(np.linalg.norm(z['E_exp']),1e-300))
 return {'ranks':{'E_exp':re,'E_unitary':ru},'active_source_count':int(np.sum(z['unitary_source_change']>ACTIVE_TOL)),'max_closure_residual':mc,'unitary_to_exponential_norm_ratio':ratio,'exp_norm':float(np.linalg.norm(z['E_exp'])),'unitary_norm':float(np.linalg.norm(z['E_unitary']))},errors
def run(out):
 out=pathlib.Path(out)
 if out.exists():raise ValueError('output exists')
 out.mkdir(parents=True); selected=select_states()
 if len(selected)!=TARGET:raise RuntimeError('selector failed target')
 rows=[];hashes={};valid=True
 for i,row in enumerate(selected):
  z=measure_state(row);m,e=evaluate_arrays(z);valid&=not e
  fn=out/f'state_{i:02d}.npz';np.savez_compressed(fn,**z);hashes[fn.name]=sha256(fn.read_bytes())
  rows.append({'candidate_index':row['candidate_index'],'selection':row['diagnostics'],'metrics':m,'errors':e,'artifact':fn.name})
 contrast=all(r['metrics']['ranks']['E_exp']['rank']>0 and r['metrics']['ranks']['E_unitary']['rank']==0 and r['metrics']['active_source_count']==9 and r['metrics']['unitary_to_exponential_norm_ratio']<=MIXED_RATIO_TOL for r in rows)
 verdict='INVALID' if not valid else ('ASYMMETRIC_SOURCE_SPECIFICITY_REPLICATED' if contrast else 'ASYMMETRIC_SOURCE_SPECIFICITY_NOT_REPLICATED')
 report={'seed':SEED,'selected_count':len(rows),'candidate_indices':[r['candidate_index'] for r in rows],'all_controls_pass':bool(valid),'contrast_pass':bool(contrast),'verdict':verdict,'artifact_sha256':hashes,'rows':rows}
 (out/'report.json').write_text(json.dumps(report,indent=2,sort_keys=True)+'\n')
 if verdict=='INVALID':raise RuntimeError('invalid')
 return report
def verify(out):
 out=pathlib.Path(out);r=json.loads((out/'report.json').read_text());selected=select_states()
 if r['candidate_indices']!=[x['candidate_index'] for x in selected]:raise ValueError('selector mismatch')
 rows=[]
 for i,row in enumerate(selected):
  fn=out/f'state_{i:02d}.npz'
  if r['artifact_sha256'].get(fn.name)!=sha256(fn.read_bytes()):raise ValueError('hash mismatch')
  with np.load(fn,allow_pickle=False) as a:z={k:a[k] for k in a.files}
  m,e=evaluate_arrays(z);rows.append((m,e))
 valid=all(not e for m,e in rows);contrast=all(m['ranks']['E_exp']['rank']>0 and m['ranks']['E_unitary']['rank']==0 and m['active_source_count']==9 and m['unitary_to_exponential_norm_ratio']<=MIXED_RATIO_TOL for m,e in rows)
 verdict='INVALID' if not valid else ('ASYMMETRIC_SOURCE_SPECIFICITY_REPLICATED' if contrast else 'ASYMMETRIC_SOURCE_SPECIFICITY_NOT_REPLICATED')
 if verdict!=r['verdict'] or contrast!=r['contrast_pass']:raise ValueError('verdict mismatch')
 return {'verified':True,'verdict':verdict,'selected_count':len(rows)}
def main():
 ap=argparse.ArgumentParser();x=ap.add_mutually_exclusive_group(required=True);x.add_argument('--output');x.add_argument('--verify');a=ap.parse_args()
 try:z=run(a.output) if a.output else verify(a.verify);print(json.dumps(z,indent=2,sort_keys=True));return 0
 except Exception as e:print(json.dumps({'verdict':'INVALID','error':str(e)}),file=sys.stderr);return 2
if __name__=='__main__':raise SystemExit(main())
