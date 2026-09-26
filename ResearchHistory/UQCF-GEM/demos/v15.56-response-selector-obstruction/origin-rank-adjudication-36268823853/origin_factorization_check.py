"""Independent algebra check, not a rerun of the 243-column source experiment.
Uses only the archived fixture parameters and exact SO(3) product identities.
Run: python origin_factorization_check.py
"""
from pathlib import Path
import hashlib
import json
import numpy as np

HERE = Path(__file__).resolve().parent
ARCHIVE_SHA = 'b49b4707b297029685c5545983681fdbb7bea67450389c360b95bfef6d865bea'
JSON_SHA = 'e756d960ef4b8d5469f457ed2401c4a77b494c98454a7bcb84de70c3bbda29e2'

def skew(x):
    return (x-x.T)/2

def basis3():
    out=[]
    for i,j in [(0,1),(0,2),(1,2)]:
        q=np.zeros((3,3)); q[i,j]=1/np.sqrt(2); q[j,i]=-1/np.sqrt(2)
        out.append(q)
    return np.array(out)

B=basis3()
def coeff(a):
    return np.einsum('kij,ij->k',B,a)

def rand_rotation(rng):
    q,r=np.linalg.qr(rng.normal(size=(3,3)))
    q=q@np.diag(np.where(np.diag(r)<0,-1.,1.))
    if np.linalg.det(q)<0: q[:,0]*=-1
    return q

def check_rotations(Os,rng):
    o0,o1,o2=Os
    h=o0@o1@o2
    t=o0@o1
    def loop(a0,a1,a2):
        return a0+o0@a1@o0.T+t@a2@t.T
    # Exact left-trivialized product derivative, represented in HS orthonormal bases.
    L=np.column_stack([coeff(loop(*(b if k==e else np.zeros((3,3)) for k in range(3))))
                       for e in range(3) for b in B])
    # Construct 6 independent kernel vectors from free A0, A1.
    ns=[]
    for e in range(2):
        for b in B:
            a0=b if e==0 else np.zeros((3,3))
            a1=b if e==1 else np.zeros((3,3))
            a2=-t.T@(a0+o0@a1@o0.T)@t
            ns.append(np.concatenate([coeff(a0),coeff(a1),coeff(a2)]))
    N=np.column_stack(ns)
    P=L.T@L/3
    product_error=0.
    for _ in range(20):
        aa=[skew(rng.normal(size=(3,3))) for _ in range(3)]
        mm=[a@o for a,o in zip(aa,Os)]
        K=mm[0]@o1@o2+o0@mm[1]@o2+o0@o1@mm[2]
        product_error=max(product_error,float(np.linalg.norm(K@h.T-loop(*aa))))
    return {
        'loop_map_rank':int(np.linalg.matrix_rank(L,tol=1e-10)),
        'loop_map_singular_values':np.linalg.svd(L,compute_uv=False).tolist(),
        'kernel_basis_rank':int(np.linalg.matrix_rank(N,tol=1e-10)),
        'loop_gram_error':float(np.linalg.norm(L@L.T-3*np.eye(3))),
        'kernel_residual':float(np.linalg.norm(L@N)),
        'visible_projector_error':float(np.linalg.norm(P@P-P)),
        'product_rule_error':product_error,
    }

def run():
    raw=(HERE/'polar_sylvester_rank3_origin_result.json').read_bytes()
    assert hashlib.sha256(raw).hexdigest()==JSON_SHA
    z=HERE/'polar-sylvester-rank3-origin-36268823853.zip'
    zip_checked=z.exists()
    if zip_checked:
        assert hashlib.sha256(z.read_bytes()).hexdigest()==ARCHIVE_SHA
    data=json.loads(raw)
    assert data['fixture_count']==11 and len(data['rows'])==11
    assert data['controls_pass'] and data['fitted_parameters']==0
    for r in data['rows']:
        assert r['edge_ranks']==[3,3,3] and r['edge_skew_ranks']==[3,3,3]
        assert r['direct_sum_rank']==9 and r['loop_rank']==3
        assert r['loop_reconstruction_error']<=1e-10
        assert r['skew_only_loop_reconstruction_error']<=1e-10
    rng=np.random.default_rng(20260926)
    results=[]
    noise=[]
    for r in data['rows']:
        m,d,a=r['m'],r['d'],r['a']
        C=np.array([[d,-a,0],[a,d,0],[0,0,d/2-m*m]])
        u,s,vh=np.linalg.svd(C); o=u@vh
        assert s.min()>=.02-1e-14 and np.linalg.det(o)>0
        x=check_rotations([o,o,o],rng)
        x.update(m=m,d=d,a=a,minimum_edge_singular_value=float(s.min()))
        results.append(x)
        # Reproduce self-relative rank inflation on data known EXACTLY to be skew-tangent.
        # These are synthetic diagnostic columns, not measured source columns.
        weights=rng.normal(size=(3,243))
        W=np.einsum('ka,kij->aij',weights,B)
        M=np.einsum('ij,ajk->aik',o,W)
        recon=np.einsum('ji,ajk->aik',o,M)
        Ws=(recon-recon.transpose(0,2,1))/2
        Wn=recon-Ws
        A=M.reshape(243,9).T
        A_N=np.einsum('ij,ajk->aik',o,Wn).reshape(243,9).T
        sn=np.linalg.svd(A_N,compute_uv=False)
        se=np.linalg.svd(A,compute_uv=False)
        floor=100*np.finfo(float).eps*max(A.shape)*se[0]
        noise.append({
            'm':m,'d':d,'a':a,
            'synthetic_self_relative_nonskew_rank':int(np.sum(sn>sn[0]*1e-10)) if sn[0]>0 else 0,
            'parent_scaled_nonskew_rank':int(np.sum(sn>floor)),
            'nonskew_to_parent_norm':float(np.linalg.norm(A_N)/np.linalg.norm(A)),
            'parent_error_floor':float(floor),
            'nonskew_largest_singular_value':float(sn[0]),
        })
    random_rows=[check_rotations([rand_rotation(rng) for _ in range(3)],rng) for _ in range(100)]
    checks=results+random_rows
    for r in checks:
        assert r['loop_map_rank']==3 and r['kernel_basis_rank']==6
        assert np.max(np.abs(np.array(r['loop_map_singular_values'])-np.sqrt(3)))<1e-12
        for key in ['loop_gram_error','kernel_residual','visible_projector_error','product_rule_error']:
            assert r[key]<1e-12
    assert all(r['parent_scaled_nonskew_rank']==0 for r in noise)
    out={
        'kind':'independent_algebra_and_archived_summary_check_not_source_suite_rerun',
        'source_commit':'0b7e9ca67cfa98831e60eb3e2add7c42a806f513',
        'run_id':36268823853,'artifact_id':10914946906,
        'artifact_zip_sha256':ARCHIVE_SHA,'result_json_sha256':JSON_SHA,'original_zip_checked':zip_checked,
        'numpy_version':np.__version__,'seed':20260926,
        'all_checks_pass':True,'fixture_rotation_cases':11,'independent_random_rotation_cases':100,
        'max_recorded_loop_reconstruction_error':max(r['loop_reconstruction_error'] for r in data['rows']),
        'max_recorded_skew_only_loop_reconstruction_error':max(r['skew_only_loop_reconstruction_error'] for r in data['rows']),
        'max_recorded_basis_spectrum_error':max(r['basis_spectrum_error'] for r in data['rows']),
        'max_loop_gram_error':max(r['loop_gram_error'] for r in checks),
        'max_kernel_residual':max(r['kernel_residual'] for r in checks),
        'max_visible_projector_error':max(r['visible_projector_error'] for r in checks),
        'max_product_rule_error':max(r['product_rule_error'] for r in checks),
        'fixture_checks':results,'synthetic_roundoff_diagnostic':noise,
        'limitations':[
            'No raw source-to-edge matrices or non-skew norms were archived in the original JSON.',
            'Synthetic roundoff demonstration is not a measurement of the original non-skew residual.',
            'Rank-nine saturation remains numerical evidence on 11 fixtures, not a theorem for all states.',
            'No physical source law, gravity law, or spacetime dimension is derived by the SO(3) identity.'
        ]
    }
    (HERE/'origin_factorization_check_result.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({k:v for k,v in out.items() if k not in ['fixture_checks','synthetic_roundoff_diagnostic']},indent=2))
    print('Synthetic noise ranks:',[x['synthetic_self_relative_nonskew_rank'] for x in noise])
    print('Synthetic noise relative norm max:',max(x['nonskew_to_parent_norm'] for x in noise))

if __name__=='__main__':run()
