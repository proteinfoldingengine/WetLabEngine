"""Additive, fail-closed source-to-edge factorization gate. See PREREGISTRATION.md.

The analytic source machinery is imported unchanged from the historical demo.
The verifier recomputes algebraic diagnostics from saved arrays; it is not an
independent remeasurement of all source columns. Three dense four-corner probes
provide a separate numerical-derivative check of the analytic machinery.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import math
import os
from pathlib import Path
import platform
import sys
from typing import Any
import numpy as np

HERE = Path(__file__).resolve().parent
PARENT = HERE.parent
sys.path.insert(0, str(PARENT))
import independent_hidden_fixture as F
import independent_hidden_geometry as G
import independent_hidden_ensemble as ENS
import response_quotient_rank as R
import polar_sylvester_rank3_origin as ORIGIN

FIXTURES = [(0.1,0.08,0.04),(0.1,0.08,0.08),(0.1,0.08,0.12),
            (0.1,0.12,0.04),(0.1,0.12,0.08),(0.1,0.16,0.04),
            (0.15,0.12,0.04),(0.15,0.12,0.08),(0.15,0.16,0.04),
            (0.2,0.12,0.04),(0.2,0.16,0.04)]
SOURCE_BLOBS = {
    'independent_hidden_fixture.py':'9a1580fe431a202caecb817545aae0cf894a51e4',
    'independent_hidden_geometry.py':'ebdefbcaa836b355e624f54118c04ad5597cc6fc',
    'independent_hidden_ensemble.py':'4f82748410f52e7aeee5f8365582515eeb239c23',
    'hidden_response_theorem.py':'0d2e6cf35494ab4bff455a13df5333c2cb159494',
    'closed_form_hidden_response.py':'6eb2fbfaa19938d105afdcbd363e3f3db6e49467',
    'response_quotient_rank.py':'2ee6b0d4ecc530f5878a32e389a39d462880eb8d',
    'polar_sylvester_rank3_origin.py':'fa641f1efd5cb1d88bf456191d033716fd0b8794',
}
ALG_TOL = 1e-10
BASIS_TOL = 1e-8
FD_TOL = 1e-5
PROBE_SEED = 20260927
FD_STEPS = (2e-4, 1e-4)
SHAPES = {'fixture':(3,), 'rho':(8,8), 'columns':(243,5), 'O':(3,3,3),
          'M':(3,243,3,3), 'O_eta':(3,243,3,3), 'O_s':(3,243,3,3),
          'E':(9,243), 'L':(3,9), 'K':(9,243),
          'E_visible':(9,243), 'E_invisible':(9,243),
          'probe_h_coeff':(3,27), 'probe_p_coeff':(3,9),
          'probe_analytic':(3,3,3), 'fd_large':(3,3,3), 'fd_small':(3,3,3),
          'K_identity':(3,3)}
B = np.zeros((3,3,3))
for k,(i,j) in enumerate([(0,1),(0,2),(1,2)]):
    B[k,i,j]=1/np.sqrt(2); B[k,j,i]=-1/np.sqrt(2)
COLUMNS = np.array([(a,b,c,i,p) for a in range(1,4) for b in range(1,4)
                    for c in range(1,4) for i in range(3) for p in range(1,4)])


def sha256(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def provenance() -> dict[str, Any]:
    blobs={}
    for name in SOURCE_BLOBS:
        raw=(PARENT/name).read_bytes()
        blobs[name]=hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()
    return {'source_commit':'0b7e9ca67cfa98831e60eb3e2add7c42a806f513',
            'parent_commit':'ec33024e0343193f6a5d0c7ed62d8512701dd541',
            'source_law':'normalized_exponential_tilt', 'source_blobs':blobs,
            'gate_sha256':sha256(Path(__file__).read_bytes()),
            'preregistration_sha256':sha256((HERE/'PREREGISTRATION.md').read_bytes())}


def rank_info(A: np.ndarray, reference_scale: float | None = None) -> dict[str, Any]:
    A=np.asarray(A)
    if A.ndim!=2 or not A.size or not np.isfinite(A).all():
        raise ValueError('rank input must be a nonempty finite matrix')
    s=np.linalg.svd(A,compute_uv=False)
    scale=float(s[0]) if reference_scale is None else float(reference_scale)
    if not math.isfinite(scale) or scale<0:
        raise ValueError('rank parent scale must be finite and nonnegative')
    floor=100*np.finfo(float).eps*max(A.shape)
    cuts={str(c):max(c,floor)*scale for c in (1e-9,1e-10,1e-11)}
    ranks={k:int(np.sum(s>v)) for k,v in cuts.items()}
    return {'rank':ranks[str(1e-10)],'singular_values':s.tolist(),
            'parent_scale':scale,'threshold':cuts[str(1e-10)],
            'rank_sweep':ranks,'rank_stable':len(set(ranks.values()))==1,
            'frobenius_norm':float(np.linalg.norm(A))}


def coordinates(mats: np.ndarray) -> np.ndarray:
    """Last axes are matrix indices; no output-rank assumption is made here."""
    return np.einsum('kij,...ij->...k',B,mats)


def loop_map(O: np.ndarray) -> np.ndarray:
    prefixes=[np.eye(3),O[0],O[0]@O[1]]
    return np.concatenate([coordinates(q@B@q.T).T for q in prefixes],axis=1)


def edge_map(M: np.ndarray, O: np.ndarray) -> np.ndarray:
    left=M@O[:,None].swapaxes(-1,-2)
    return coordinates(left).transpose(0,2,1).reshape(9,243)


def direct_product(O: np.ndarray, M: np.ndarray, eta: np.ndarray,
                   source: np.ndarray) -> np.ndarray:
    """Full product rule, including cross terms rather than assuming them zero."""
    out=np.zeros((243,3,3))
    for i in range(3):
        terms=[M[j] if j==i else O[j] for j in range(3)]
        out+=terms[0]@terms[1]@terms[2]
        for k in range(3):
            if k==i:
                continue
            terms=[eta[j] if j==i else (source[j] if j==k else O[j]) for j in range(3)]
            out+=terms[0]@terms[1]@terms[2]
    return out.reshape(243,9).T


def probe_coefficients() -> tuple[np.ndarray, np.ndarray]:
    rng=np.random.default_rng(PROBE_SEED)
    hc=[]; pc=[]
    for _ in range(3):
        x=rng.normal(size=27); y=rng.normal(size=9)
        h=np.einsum('a,aij->ij',x,np.asarray(R.HB))
        p=np.einsum('a,aij->ij',y,np.asarray(R.PB))
        hc.append(x/np.linalg.norm(h,ord=2)); pc.append(y/np.linalg.norm(p,ord=2))
    return np.asarray(hc),np.asarray(pc)


def four_corner(rho: np.ndarray, h: np.ndarray, p: np.ndarray, step: float) -> np.ndarray:
    def hol(eta: float,s: float) -> np.ndarray:
        return G.geom(G.tilt(rho+eta*h,s,p))[2]
    return (hol(step,step)-hol(step,-step)-hol(-step,step)+hol(-step,-step))/(4*step*step)


def measure_fixture(params: tuple[float,float,float]) -> dict[str,np.ndarray]:
    if tuple(params) not in FIXTURES or provenance()['source_blobs']!=SOURCE_BLOBS:
        raise ValueError('unregistered fixture or altered historical source')
    rho=F.state(*params); O=np.asarray(G.geom(rho)[1])
    M=np.zeros((3,243,3,3)); eta=M.copy(); source=M.copy(); K=np.zeros((9,243))
    for ih,h in enumerate(R.HB):
        for ip,p in enumerate(R.PB):
            j=ih*9+ip
            Q=ORIGIN.edge_data(rho,h,p)
            for e in range(3):
                if np.linalg.norm(Q[e][0]-O[e])>ALG_TOL:
                    raise ValueError('inconsistent base polar rotation')
                eta[e,j]=Q[e][1]; source[e,j]=Q[e][2]; M[e,j]=Q[e][3]
            K[:,j]=R.K_for(rho,h,p).reshape(-1)
    E=edge_map(M,O); L=loop_map(O); Pi=L.T@L/3
    hc,pc=probe_coefficients(); analytic=[]; large=[]; small=[]
    for x,y in zip(hc,pc):
        h=np.einsum('a,aij->ij',x,np.asarray(R.HB))
        p=np.einsum('a,aij->ij',y,np.asarray(R.PB))
        analytic.append(R.K_for(rho,h,p))
        large.append(four_corner(rho,h,p,FD_STEPS[0]))
        small.append(four_corner(rho,h,p,FD_STEPS[1]))
    h0=np.einsum('a,aij->ij',hc[0],np.asarray(R.HB))
    return dict(fixture=np.asarray(params),rho=rho,columns=COLUMNS.copy(),O=O,M=M,
                O_eta=eta,O_s=source,E=E,L=L,K=K,E_visible=Pi@E,E_invisible=E-Pi@E,
                probe_h_coeff=hc,probe_p_coeff=pc,probe_analytic=np.asarray(analytic),
                fd_large=np.asarray(large),fd_small=np.asarray(small),
                K_identity=R.K_for(rho,h0,np.eye(8)))


def evaluate_arrays(a: dict[str,np.ndarray],params: tuple[float,float,float]) -> tuple[dict,list[str]]:
    errors=[]
    if set(a)!=set(SHAPES):
        errors.append('raw array keys differ from frozen schema')
    for key,shape in SHAPES.items():
        if key not in a or not isinstance(a[key],np.ndarray) or a[key].shape!=shape:
            errors.append(f'{key}: missing or wrong shape (expected {shape})')
        elif a[key].dtype.kind not in 'biufc' or not np.isfinite(a[key]).all():
            errors.append(f'{key}: nonnumeric or nonfinite value')
        elif key!='rho' and np.iscomplexobj(a[key]):
            errors.append(f'{key}: unexpected complex dtype')
    if errors:
        return {'controls_pass':False},errors
    if tuple(params) not in FIXTURES or not np.array_equal(a['fixture'],params):
        errors.append('fixture identity mismatch')
    if not np.array_equal(a['columns'],COLUMNS):
        errors.append('hidden/source columns missing, duplicated or reordered')
    O,M,E,L,K=a['O'],a['M'],a['E'],a['L'],a['K']
    rho=a['rho']; H=O[0]@O[1]@O[2]; Pi=L.T@L/3
    metrics={'checks':{},'ranks':{},'edge_diagnostics':[]}
    def check(name: str,value: float,limit: float=ALG_TOL) -> None:
        value=float(value); metrics['checks'][name]=value
        if not math.isfinite(value) or value>limit:
            errors.append(f'{name}: {value} exceeds {limit}')
    def relative(x: np.ndarray,y: np.ndarray) -> float:
        return float(np.linalg.norm(x-y)/max(np.linalg.norm(y),1e-15))
    check('state_reconstruction',float(np.linalg.norm(rho-F.state(*params))))
    check('state_hermiticity',float(np.linalg.norm(rho-rho.conj().T)))
    check('state_trace',float(abs(np.trace(rho)-1)))
    eigen=np.linalg.eigvalsh(rho); Cs,expected_O,_=G.geom(rho)
    eigs=[]; singular=[]; conditions=[]; determinants=[]; sylvester_spectra=[]
    for e,C in enumerate(Cs):
        s=np.linalg.svd(C,compute_uv=False); S=O[e].T@C
        w=np.linalg.eigvalsh((S+S.T)/2)
        sy=np.linalg.svd(np.kron(np.eye(3),S)+np.kron(S.T,np.eye(3)),compute_uv=False)
        eigs.append(w.tolist());singular.append(s.tolist());determinants.append(float(np.linalg.det(C)))
        sylvester_spectra.append(sy.tolist())
        conditions.append(float(sy[0]/sy[-1]) if sy[-1]>0 else None)
        if s[-1]<.02-1e-14 or w[0]<=0 or determinants[-1]<=0:
            errors.append(f'edge {e}: outside frozen regular polar stratum')
        check(f'polar_rotation_{e}',np.linalg.norm(O[e]-expected_O[e]))
        check(f'orthogonality_{e}',np.linalg.norm(O[e].T@O[e]-np.eye(3)))
        check(f'positive_polar_symmetry_{e}',np.linalg.norm(S-S.T))
        check(f'rotation_determinant_{e}',abs(np.linalg.det(O[e])-1))
    cyc=max(float(np.linalg.norm(c-Cs[0])) for c in Cs)
    angle=F.angle(H)
    if eigen.min()<.03-1e-14 or cyc>1e-12 or angle<.20-1e-14:
        errors.append('state outside historical base admissibility criteria')
    metrics['conditioning']={'state_eigenvalues':eigen.tolist(),
        'edge_singular_values':singular,'edge_determinants':determinants,
        'positive_polar_eigenvalues':eigs,'sylvester_singular_values':sylvester_spectra,
        'sylvester_condition_numbers':conditions,'cyclic_pair_difference':cyc,'holonomy_angle':angle}
    check('edge_coordinate_reconstruction',relative(E,edge_map(M,O)))
    check('loop_map_reconstruction',relative(L,loop_map(O)))
    check('loop_gram',np.linalg.norm(L@L.T-3*np.eye(3)))
    check('visible_projector',np.linalg.norm(Pi@Pi-Pi))
    check('visible_export',relative(a['E_visible'],Pi@E))
    check('invisible_export',relative(a['E_invisible'],E-Pi@E))
    check('edge_split',relative(a['E_visible']+a['E_invisible'],E))
    check('hidden_first_derivative_max',np.linalg.norm(a['O_eta'],axis=(-2,-1)).max())
    check('identity_source',np.linalg.norm(a['K_identity']))
    predicted=(np.einsum('ka,kij->aij',L@E,B)@H).reshape(243,9).T
    check('factorization',relative(predicted,K))
    check('full_product_rule',relative(direct_product(O,M,a['O_eta'],a['O_s']),K))
    Kc=coordinates(K.T.reshape(243,3,3)@H.T).T
    check('loop_skew_tangency',relative((np.einsum('ka,kij->aij',Kc,B)@H).reshape(243,9).T,K))
    check('invisible_loop',np.linalg.norm(L@a['E_invisible'])/max(np.linalg.norm(K),1e-15))
    rng=np.random.default_rng(20260926)
    qh=np.linalg.qr(rng.normal(size=(27,27)))[0];qp=np.linalg.qr(rng.normal(size=(9,9)))[0]
    T=np.kron(qh,qp)
    maps={'edge_map':E,'loop_map':L,'full_loop':K,'loop_coordinates':Kc,
          'visible_edge_map':a['E_visible'],'invisible_edge_map':a['E_invisible'],
          'raw_direct_sum':M.reshape(3,243,9).transpose(0,2,1).reshape(27,243)}
    for name,x in maps.items():
        metrics['ranks'][name]=rank_info(x)
    for name,x in [('edge',E),('loop',K)]:
        s=np.linalg.svd(x,compute_uv=False);s2=np.linalg.svd(x@T,compute_uv=False)
        check(name+'_basis_spectrum',np.linalg.norm(s-s2)/max(np.linalg.norm(s),1e-15),BASIS_TOL)
    for e in range(3):
        parent=M[e].reshape(243,9).T
        W=O[e].T@M[e];Ws=(W-W.swapaxes(-1,-2))/2
        sk=(O[e]@Ws).reshape(243,9).T
        non=(O[e]@(W-Ws)).reshape(243,9).T
        scale=float(np.linalg.svd(parent,compute_uv=False)[0])
        nr=float(np.linalg.norm(non)/max(np.linalg.norm(parent),1e-15))
        check(f'edge_{e}_nonskew_fraction',nr)
        metrics['edge_diagnostics'].append({'raw':rank_info(parent),'skew':rank_info(sk,scale),
            'nonskew':rank_info(non,scale),'nonskew_self_scaled':rank_info(non),
            'nonskew_parent_relative_norm':nr})
    hc,pc=probe_coefficients()
    check('hidden_probe_coefficients',np.linalg.norm(a['probe_h_coeff']-hc))
    check('source_probe_coefficients',np.linalg.norm(a['probe_p_coeff']-pc))
    probes=[]
    for i,(x,y) in enumerate(zip(hc,pc)):
        analytic=a['probe_analytic'][i]; full=(K@np.kron(x,y)).reshape(3,3)
        rich=(4*a['fd_small'][i]-a['fd_large'][i])/3
        check(f'probe_{i}_bilinear_reconstruction',relative(full,analytic))
        den=max(1.,float(np.linalg.norm(analytic)))
        err=float(np.linalg.norm(rich-analytic)/den)
        check(f'probe_{i}_finite_difference',err,FD_TOL)
        probes.append({'analytic_norm':float(np.linalg.norm(analytic)),
            'large_step_error':float(np.linalg.norm(a['fd_large'][i]-analytic)/den),
            'small_step_error':float(np.linalg.norm(a['fd_small'][i]-analytic)/den),
            'step_change':float(np.linalg.norm(a['fd_small'][i]-a['fd_large'][i])/den),
            'richardson_error':err})
    metrics['finite_difference_probes']=probes
    n2=float(np.linalg.norm(E)**2)
    v2=float(np.linalg.norm(a['E_visible'])**2);i2=float(np.linalg.norm(a['E_invisible'])**2)
    metrics['visible_squared_norm_fraction']=v2/n2 if n2 else 0.
    metrics['invisible_squared_norm_fraction']=i2/n2 if n2 else 0.
    check('squared_norm_partition',abs(v2+i2-n2)/max(n2,1e-30))
    metrics['controls_pass']=not errors
    return metrics,errors


def validate_manifest(r: dict[str,Any]) -> list[str]:
    errors=[]
    try:
        json.dumps(r,allow_nan=False)
    except (ValueError,TypeError):
        return ['manifest contains nonfinite or non-JSON data']
    if not isinstance(r,dict):
        return ['manifest must be an object']
    for key,value in [('schema',1),('fixture_count',11),('input_dimension',243),('fitted_parameters',0)]:
        if type(r.get(key)) is not int or r[key]!=value:
            errors.append(f'wrong or missing {key}')
    if r.get('controls_pass') is not True or r.get('verdict')=='INVALID':
        errors.append('manifest declares invalid controls or verdict')
    if r.get('provenance')!=provenance() or provenance()['source_blobs']!=SOURCE_BLOBS:
        errors.append('source or implementation provenance mismatch')
    rows=r.get('rows',[])
    if not isinstance(rows,list) or len(rows)!=11:
        return errors+['missing or extra fixture rows']
    for i,(row,p) in enumerate(zip(rows,FIXTURES)):
        if not isinstance(row,dict):
            errors.append(f'row {i} must be an object');continue
        if row.get('fixture')!=list(p):
            errors.append(f'row {i} wrong, duplicated or reordered fixture')
        if row.get('artifact')!=f'fixture_{i:02d}.npz':
            errors.append(f'row {i} wrong artifact path')
        digest=row.get('sha256','')
        if not isinstance(digest,str) or len(digest)!=64 or any(c not in '0123456789abcdef' for c in digest):
            errors.append(f'row {i} invalid artifact digest')
        if row.get('controls_pass') is not True:
            errors.append(f'row {i} controls not true')
    return errors


def save_fixture(directory: Path,index: int,params: tuple,arrays: dict) -> dict:
    directory=Path(directory);directory.mkdir(parents=True,exist_ok=True)
    name=f'fixture_{index:02d}.npz';path=directory/name
    metrics,errors=evaluate_arrays(arrays,params)
    np.savez_compressed(path,**arrays)
    return {'fixture':list(params),'artifact':name,'sha256':sha256(path.read_bytes()),
            'controls_pass':not errors,'metrics':metrics,'errors':errors}


def load_fixture(directory: Path,row: dict) -> dict[str,np.ndarray]:
    name=row.get('artifact','')
    if name not in {f'fixture_{i:02d}.npz' for i in range(11)}:
        raise ValueError('unexpected artifact path')
    path=Path(directory)/name
    if sha256(path.read_bytes())!=row.get('sha256'):
        raise ValueError('artifact SHA-256 mismatch')
    with np.load(path,allow_pickle=False) as z:
        return {k:z[k] for k in z.files}


def same_tree(a: Any,b: Any) -> bool:
    if isinstance(a,dict) and isinstance(b,dict):
        return a.keys()==b.keys() and all(same_tree(a[k],b[k]) for k in a)
    if isinstance(a,list) and isinstance(b,list):
        return len(a)==len(b) and all(same_tree(x,y) for x,y in zip(a,b))
    if isinstance(a,bool) or isinstance(b,bool):
        return type(a) is type(b) and a==b
    if isinstance(a,int) and isinstance(b,int):
        return a==b
    if isinstance(a,(int,float)) and isinstance(b,(int,float)):
        return math.isclose(a,b,rel_tol=1e-8,abs_tol=1e-12)
    return a==b


def verdict_for(rows: list[dict]) -> str:
    if not all(r['controls_pass'] for r in rows):
        return 'INVALID'
    names=('edge_map','full_loop','visible_edge_map','invisible_edge_map')
    if not all(r['metrics']['ranks'][n]['rank_stable'] for r in rows for n in names):
        return 'VALID_RANK_UNRESOLVED'
    if all([r['metrics']['ranks'][n]['rank'] for n in names]==[9,3,3,6] for r in rows):
        return 'FACTORIZATION_VERIFIED_243_9_3'
    return 'VALID_DIFFERENT_RANK_STRUCTURE'


def verify_bundle(directory: Path) -> dict[str,Any]:
    directory=Path(directory)
    report=json.loads((directory/'report.json').read_text())
    errors=validate_manifest(report)
    if errors:
        raise ValueError('; '.join(errors))
    rows=[]
    for i,row in enumerate(report['rows']):
        arrays=load_fixture(directory,row)
        metrics,issues=evaluate_arrays(arrays,FIXTURES[i])
        if issues or row.get('errors')!=[] or not same_tree(metrics,row.get('metrics')):
            raise ValueError(f'fixture {i}: raw validation or recomputed summary mismatch: {issues}')
        rows.append(row)
    if report.get('verdict')!=verdict_for(rows):
        raise ValueError('verdict inconsistent with recomputed evidence')
    return {'verified':True,'fixture_count':11,'input_dimension':243,'verdict':report['verdict']}


def run(directory: Path) -> dict[str,Any]:
    if provenance()['source_blobs']!=SOURCE_BLOBS:
        raise ValueError('historical source hash mismatch')
    admitted=[(m,d,a) for m in ENS.GRID_M for d in ENS.GRID_D for a in ENS.GRID_A
              if ENS.base_ok(F.state(m,d,a))[0]]
    if admitted!=FIXTURES:
        raise ValueError('historical admission enumeration differs from frozen 11 fixtures')
    directory=Path(directory);directory.mkdir(parents=True,exist_ok=False)
    rows=[]
    for i,params in enumerate(FIXTURES):
        row=save_fixture(directory,i,params,measure_fixture(params));rows.append(row)
        print(f'fixture {i+1}/11 {params}: controls={row["controls_pass"]}',file=sys.stderr,flush=True)
    report={'schema':1,'fixture_count':len(rows),'input_dimension':243,'fitted_parameters':0,
            'controls_pass':all(r['controls_pass'] for r in rows),'provenance':provenance(),
            'execution':{'github_sha':os.environ.get('GITHUB_SHA'),
                         'github_run_id':os.environ.get('GITHUB_RUN_ID'),
                         'python':platform.python_version(),'numpy':np.__version__},
            'verdict':verdict_for(rows),'rows':rows}
    (directory/'report.json').write_text(json.dumps(report,indent=2,allow_nan=False)+'\n')
    return verify_bundle(directory)


def main(argv: list[str] | None=None) -> int:
    parser=argparse.ArgumentParser(description=__doc__)
    group=parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--output',type=Path);group.add_argument('--verify',type=Path)
    args=parser.parse_args(argv)
    try:
        result=verify_bundle(args.verify) if args.verify is not None else run(args.output)
        print(json.dumps(result,sort_keys=True,allow_nan=False))
        return 0
    except Exception as exc:
        print(json.dumps({'verified':False,'verdict':'INVALID','error':str(exc)},allow_nan=False),file=sys.stderr)
        return 1

if __name__=='__main__':
    raise SystemExit(main())
