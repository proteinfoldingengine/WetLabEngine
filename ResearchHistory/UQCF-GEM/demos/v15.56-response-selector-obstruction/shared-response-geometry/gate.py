"""v15.60 shared response geometry and amplitude stability."""
from __future__ import annotations
import argparse,hashlib,importlib.util,json,pathlib,sys,numpy as np
HERE=pathlib.Path(__file__).resolve().parent;PARENT=HERE.parent
def load(path,name):
 s=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
ASYM=load(PARENT/'asymmetric-heldout-ensemble'/'gate.py','asym60')
NC=load(PARENT/'nonclosed-source-class'/'gate.py','nc60')
SE=NC.SE
AMPLITUDES=[.0685,.137,.274];EXPECTED=NC.EXPECTED
def states():
 z=ASYM.select_states()
 if [x['candidate_index'] for x in z]!=EXPECTED:raise RuntimeError('state identity mismatch')
 return z
def sha(x):return hashlib.sha256(x).hexdigest()
def basis(E):
 u,s,vh=np.linalg.svd(E,full_matrices=False);r=int(np.sum(s>s[0]*1e-10))
 if r!=9:raise ValueError(f'rank {r} != 9')
 return vh[:9].T,s
def projector(E):
 V,_=basis(E);return V@V.T
def filter_at(rho,s):
 old=NC.S_FILTER
 try:
  NC.S_FILTER=s
  return NC.filter_edge_map(rho)
 finally:NC.S_FILTER=old
def compare(A,B):
 Va,_=basis(A);Vb,_=basis(B);c=np.linalg.svd(Va.T@Vb,compute_uv=False);Pa=Va@Va.T;Pb=Vb@Vb.T
 alpha=float(np.vdot(A,B).real/max(np.vdot(A,A).real,1e-300))
 return {'principal_cosines':c.tolist(),'min_cosine':float(c.min()),'projector_distance':float(np.linalg.norm(Pa-Pb)/np.sqrt(2)),'scalar_residual':float(np.linalg.norm(B-alpha*A)/np.linalg.norm(B)),'normalized_map_distance':float(np.linalg.norm(A/np.linalg.norm(A)-B/np.linalg.norm(B)))}
def measure_state(row):
 rho=row['rho'];Ee=ASYM.exponential_edge_map(rho);fm={};act={};nc={}
 for s in AMPLITUDES:
  E,a,n=filter_at(rho,s);fm[s]=E;act[s]=a;nc[s]=n
 return {'candidate_index':row['candidate_index'],'E_exp':Ee,'filter_maps':fm,'activity':act,'nonclosure':nc}
def evaluate(z):
 e=[];re=SE.rank_info(z['E_exp'])
 if re['rank']!=9:e.append('exponential rank != 9')
 fr=[];expcomp=[]
 for s in AMPLITUDES:
  ri=SE.rank_info(z['filter_maps'][s]);fr.append(ri['rank'])
  if ri['rank']!=9:e.append(f'filter rank !=9 at {s}')
  if np.sum(z['activity'][s]>NC.ACTIVE_TOL)!=9:e.append(f'inactive filter at {s}')
  if float(z['nonclosure'][s].max())<=NC.NONCLOSURE_MIN:e.append(f'nonclosure absent at {s}')
  expcomp.append(compare(z['E_exp'],z['filter_maps'][s]))
 pairs=[]
 for i in range(3):
  for j in range(i+1,3):pairs.append(compare(z['filter_maps'][AMPLITUDES[i]],z['filter_maps'][AMPLITUDES[j]]))
 center=expcomp[1]['projector_distance'];maxdr=max(x['projector_distance'] for x in pairs)
 cat='amplitude-stable overlap' if maxdr<center else 'amplitude-sensitive overlap'
 # Average-projector spectrum at center: canonical continuous measure of commonality.
 P=.5*(projector(z['E_exp'])+projector(z['filter_maps'][.137]))
 avg=np.linalg.eigvalsh(P)[::-1][:18]
 return {'exp_rank':re['rank'],'filter_ranks':fr,'exp_filter_min_cosines':[x['min_cosine'] for x in expcomp],'exp_filter_projector_distances':[x['projector_distance'] for x in expcomp],'filter_pair_min_cosines':[x['min_cosine'] for x in pairs],'filter_pair_projector_distances':[x['projector_distance'] for x in pairs],'exp_filter_scalar_residuals':[x['scalar_residual'] for x in expcomp],'average_projector_top18_eigenvalues':avg.tolist(),'max_amplitude_projector_drift':maxdr,'center_exp_filter_projector_distance':center,'category':cat},e
def pack(z):
 d={'candidate_index':np.array(z['candidate_index']),'E_exp':z['E_exp']}
 for i,s in enumerate(AMPLITUDES):d[f'E_filter_{i}']=z['filter_maps'][s];d[f'activity_{i}']=z['activity'][s];d[f'nonclosure_{i}']=z['nonclosure'][s]
 return d
def unpack(d):
 return {'candidate_index':int(d['candidate_index']),'E_exp':d['E_exp'],'filter_maps':{s:d[f'E_filter_{i}'] for i,s in enumerate(AMPLITUDES)},'activity':{s:d[f'activity_{i}'] for i,s in enumerate(AMPLITUDES)},'nonclosure':{s:d[f'nonclosure_{i}'] for i,s in enumerate(AMPLITUDES)}}
def run(out):
 out=pathlib.Path(out)
 if out.exists():raise ValueError('output exists')
 out.mkdir(parents=True);rows=[];hashes={};valid=True
 for i,row in enumerate(states()):
  z=measure_state(row);m,e=evaluate(z);valid&=not e;fn=out/f'state_{i:02d}.npz';np.savez_compressed(fn,**pack(z));hashes[fn.name]=sha(fn.read_bytes());rows.append({'candidate_index':row['candidate_index'],'metrics':m,'errors':e,'artifact':fn.name})
 verdict='SHARED_GEOMETRY_MEASURED' if valid else 'INVALID';r={'amplitudes':AMPLITUDES,'candidate_indices':EXPECTED,'all_controls_pass':bool(valid),'verdict':verdict,'artifact_sha256':hashes,'rows':rows}
 (out/'report.json').write_text(json.dumps(r,indent=2,sort_keys=True)+'\n')
 if not valid:raise RuntimeError('invalid')
 return r
def verify(out):
 out=pathlib.Path(out);r=json.loads((out/'report.json').read_text());valid=True
 if r['candidate_indices']!=EXPECTED or r['amplitudes']!=AMPLITUDES:raise ValueError('frozen identity mismatch')
 for i in range(12):
  fn=out/f'state_{i:02d}.npz'
  if r['artifact_sha256'].get(fn.name)!=sha(fn.read_bytes()):raise ValueError('hash mismatch')
  with np.load(fn,allow_pickle=False) as a:d={k:a[k] for k in a.files}
  m,e=evaluate(unpack(d));valid&=not e
 if not valid or r['verdict']!='SHARED_GEOMETRY_MEASURED':raise ValueError('verification invalid')
 return {'verified':True,'verdict':'SHARED_GEOMETRY_MEASURED','selected_count':12}
def main():
 ap=argparse.ArgumentParser();x=ap.add_mutually_exclusive_group(required=True);x.add_argument('--output');x.add_argument('--verify');a=ap.parse_args()
 try:z=run(a.output) if a.output else verify(a.verify);print(json.dumps(z,indent=2,sort_keys=True));return 0
 except Exception as e:print(json.dumps({'verdict':'INVALID','error':str(e)}),file=sys.stderr);return 2
if __name__=='__main__':raise SystemExit(main())
