"""v15.57 source-law specificity gate.

Compare the frozen normalized exponential tilt with a marginally closed
local-unitary source law using the same hidden and one-body source bases.
"""
from __future__ import annotations
import argparse, hashlib, importlib.util, json, math, pathlib, sys
import numpy as np

HERE=pathlib.Path(__file__).resolve().parent
PARENT=HERE.parent
sys.path.insert(0,str(PARENT))
import independent_hidden_fixture as F
import independent_hidden_geometry as G
import independent_hidden_ensemble as ENS
import response_quotient_rank as R

SE_PATH=PARENT/'source-edge-factorization'/'gate.py'
_spec=importlib.util.spec_from_file_location('source_edge_factorization_gate',SE_PATH)
SE=importlib.util.module_from_spec(_spec); _spec.loader.exec_module(SE)

FIXTURES=list(SE.FIXTURES)
ETA=1e-3
S=0.137
CLOSURE_TOL=1e-11
ACTIVE_TOL=1e-4
MIXED_RATIO_TOL=1e-9
SHAPES={
 'fixture':(3,), 'columns':(243,5), 'E_exp':(9,243), 'E_unitary':(9,243),
 'unitary_source_change':(9,), 'closure_residuals':(243,),
 'state_eigenvalues':(8,), 'edge_singular_values':(3,3)
}

def sha256(raw:bytes)->str:
    return hashlib.sha256(raw).hexdigest()

def local_unitary_update(rho:np.ndarray,s:float,p:np.ndarray)->np.ndarray:
    w,v=np.linalg.eigh((p+p.conj().T)/2)
    U=(v*np.exp(-0.5j*s*w))@v.conj().T
    out=U@rho@U.conj().T
    return (out+out.conj().T)/2

def _edge_rotations(rho:np.ndarray)->np.ndarray:
    return np.asarray(G.geom(rho)[1])

def _mixed_unitary_edges(rho:np.ndarray,h:np.ndarray,p:np.ndarray)->tuple[np.ndarray,float]:
    states={}; rots={}
    for ie in (-1,1):
        base=rho+ie*ETA*h
        for js in (-1,1):
            z=local_unitary_update(base,js*S,p)
            states[(ie,js)]=z
            rots[(ie,js)]=_edge_rotations(z)
    M=(rots[(1,1)]-rots[(1,-1)]-rots[(-1,1)]+rots[(-1,-1)])/(4*ETA*S)
    closure=G.marginal_diff(states[(1,1)],states[(-1,1)])
    return M,float(closure)

def measure_fixture(params:tuple[float,float,float])->dict[str,np.ndarray]:
    if tuple(params) not in FIXTURES:
        raise ValueError('unregistered fixture')
    rho=F.state(*params)
    ok,_=ENS.base_ok(rho)
    if not ok:
        raise ValueError('fixture outside frozen regular ensemble')
    exp=SE.measure_fixture(tuple(params))
    O=np.asarray(G.geom(rho)[1])
    M=np.zeros((3,243,3,3)); closure=np.zeros(243)
    source_change=np.zeros(9)
    for ip,p in enumerate(R.PB):
        source_change[ip]=float(np.linalg.norm(_edge_rotations(local_unitary_update(rho,S,p))-O))
    j=0
    for h in R.HB:
        for p in R.PB:
            mm,cc=_mixed_unitary_edges(rho,h,p)
            M[:,j]=mm; closure[j]=cc; j+=1
    Eu=SE.edge_map(M,O)
    Cs=[F.corr(rho,*e) for e in G.EDGES]
    sv=np.asarray([np.linalg.svd(c,compute_uv=False) for c in Cs])
    return {
      'fixture':np.asarray(params,float),'columns':SE.COLUMNS.copy(),
      'E_exp':np.asarray(exp['E'],float),'E_unitary':np.asarray(Eu,float),
      'unitary_source_change':source_change,'closure_residuals':closure,
      'state_eigenvalues':np.linalg.eigvalsh(rho),'edge_singular_values':sv
    }

def evaluate_arrays(a:dict[str,np.ndarray],params:tuple[float,float,float])->tuple[dict,list[str]]:
    errors=[]
    if set(a)!=set(SHAPES): errors.append('raw array keys differ from frozen schema')
    for k,sh in SHAPES.items():
        if k not in a or not isinstance(a[k],np.ndarray) or a[k].shape!=sh:
            errors.append(f'{k}: missing or wrong shape')
        elif not np.isfinite(a[k]).all(): errors.append(f'{k}: nonfinite')
    if errors: return {'controls_pass':False},errors
    if not np.array_equal(a['fixture'],np.asarray(params,float)): errors.append('fixture identity mismatch')
    if not np.array_equal(a['columns'],SE.COLUMNS): errors.append('column labels mismatch')
    if float(a['state_eigenvalues'].min())<.03-1e-14: errors.append('state outside regular stratum')
    if float(a['edge_singular_values'].min())<.02-1e-14: errors.append('edge outside regular stratum')
    max_closure=float(a['closure_residuals'].max())
    if max_closure>CLOSURE_TOL: errors.append(f'closure residual {max_closure} exceeds {CLOSURE_TOL}')
    max_source=float(a['unitary_source_change'].max())
    if max_source<=ACTIVE_TOL: errors.append(f'source inactive: maximum change {max_source}')
    re=SE.rank_info(a['E_exp'])
    exp_scale=float(re['singular_values'][0]) if re['singular_values'] else 0.0
    ru=SE.rank_info(a['E_unitary'],reference_scale=exp_scale)
    ratio=float(np.linalg.norm(a['E_unitary'])/max(np.linalg.norm(a['E_exp']),1e-300))
    metrics={
      'controls_pass':not errors,
      'ranks':{'E_exp':re,'E_unitary':ru},
      'unitary_to_exponential_norm_ratio':ratio,
      'max_closure_residual':max_closure,
      'max_unitary_source_change':max_source,
      'active_source_count':int(np.sum(a['unitary_source_change']>ACTIVE_TOL)),
      'min_state_eigenvalue':float(a['state_eigenvalues'].min()),
      'min_edge_singular_value':float(a['edge_singular_values'].min())
    }
    return metrics,errors

def _npz_dict(path:pathlib.Path)->dict[str,np.ndarray]:
    with np.load(path,allow_pickle=False) as z: return {k:z[k] for k in z.files}

def run(out:pathlib.Path)->dict:
    out=pathlib.Path(out)
    if out.exists(): raise ValueError('output directory already exists')
    out.mkdir(parents=True)
    rows=[]; hashes={}; all_controls=True
    for i,p in enumerate(FIXTURES):
        a=measure_fixture(p); m,e=evaluate_arrays(a,p); all_controls &= not e
        fn=out/f'fixture_{i:02d}.npz'; np.savez_compressed(fn,**a); hashes[fn.name]=sha256(fn.read_bytes())
        rows.append({'fixture':list(p),'metrics':m,'errors':e,'artifact':fn.name})
    contrast=all(
      r['metrics'].get('ranks',{}).get('E_exp',{}).get('rank',0)>0 and
      r['metrics'].get('ranks',{}).get('E_unitary',{}).get('rank',-1)==0 and
      r['metrics'].get('unitary_to_exponential_norm_ratio',math.inf)<=MIXED_RATIO_TOL
      for r in rows)
    verdict='INVALID' if not all_controls else ('SOURCE_LAW_SPECIFICITY_CONFIRMED' if contrast else 'SOURCE_LAW_SPECIFICITY_NOT_SHOWN')
    report={
      'fixture_count':len(rows),'columns_per_fixture':243,'eta':ETA,'source_amplitude':S,
      'closure_tolerance':CLOSURE_TOL,'active_source_tolerance':ACTIVE_TOL,
      'mixed_ratio_tolerance':MIXED_RATIO_TOL,'all_controls_pass':bool(all_controls),
      'contrast_pass':bool(contrast),'verdict':verdict,'artifact_sha256':hashes,'rows':rows,
      'interpretation_boundary':'Source-law specificity only; no physical uniqueness, gravity, or universality claim.'
    }
    (out/'report.json').write_text(json.dumps(report,indent=2,sort_keys=True)+'\n')
    if verdict=='INVALID': raise RuntimeError('scientific controls invalid')
    return report

def verify(out:pathlib.Path)->dict:
    out=pathlib.Path(out); rp=out/'report.json'
    if not rp.exists(): raise ValueError('missing report.json')
    report=json.loads(rp.read_text())
    if report.get('fixture_count')!=len(FIXTURES) or report.get('columns_per_fixture')!=243:
        raise ValueError('report fixture/column count mismatch')
    if report.get('all_controls_pass') is not True: raise ValueError('report controls are not passing')
    rows=[]; all_controls=True
    for i,p in enumerate(FIXTURES):
        fn=out/f'fixture_{i:02d}.npz'
        if not fn.exists(): raise ValueError(f'missing {fn.name}')
        expected=report.get('artifact_sha256',{}).get(fn.name)
        if expected!=sha256(fn.read_bytes()): raise ValueError(f'hash mismatch {fn.name}')
        m,e=evaluate_arrays(_npz_dict(fn),p); all_controls &= not e
        rows.append((m,e))
    contrast=all(m['ranks']['E_exp']['rank']>0 and m['ranks']['E_unitary']['rank']==0 and
                 m['unitary_to_exponential_norm_ratio']<=MIXED_RATIO_TOL for m,e in rows)
    verdict='INVALID' if not all_controls else ('SOURCE_LAW_SPECIFICITY_CONFIRMED' if contrast else 'SOURCE_LAW_SPECIFICITY_NOT_SHOWN')
    if verdict!=report.get('verdict') or contrast!=report.get('contrast_pass'):
        raise ValueError('report verdict/metrics inconsistent with raw artifacts')
    return {'verified':True,'verdict':verdict,'fixture_count':len(rows)}

def main()->int:
    ap=argparse.ArgumentParser(); x=ap.add_mutually_exclusive_group(required=True)
    x.add_argument('--output',type=pathlib.Path); x.add_argument('--verify',type=pathlib.Path)
    args=ap.parse_args()
    try:
        z=run(args.output) if args.output else verify(args.verify)
        print(json.dumps(z,indent=2,sort_keys=True)); return 0
    except Exception as e:
        print(json.dumps({'error':str(e),'verdict':'INVALID'},indent=2),file=sys.stderr); return 2

if __name__=='__main__': raise SystemExit(main())
