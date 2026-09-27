"""v15.72: numerical adjudication of the v15.71 enriched-descent NO."""
import importlib.util
import json
import pathlib
import sys
import numpy as np
import mpmath as mp

HERE=pathlib.Path(__file__).resolve().parent
PARENT=HERE.parent

def load(path,name):
    s=importlib.util.spec_from_file_location(name,path)
    m=importlib.util.module_from_spec(s)
    s.loader.exec_module(m)
    return m

V71=load(PARENT/'minimal-extension-memory'/'gate.py','v71_num')
V70=V71.V70
V64=V71.V64
EDGES=V71.EDGES
HIDDEN=V71.HIDDEN
EXPECTED=V71.EXPECTED
ETA=V71.ETA
STRENGTH=V71.STRENGTH
MP_DPS=80
mp.mp.dps=MP_DPS

def adjudicate(valid,float_failure_reproduced,increment_pass,mp_pass):
    if not valid:
        return 'INVALID'
    if float_failure_reproduced and increment_pass and mp_pass:
        return 'EXTENSION_MEMORY_CANCELLATION_CONFIRMED'
    return 'EXTENSION_MEMORY_NUMERIC_DISAGREEMENT'

def mpcmat(a):
    a=np.asarray(a)
    return mp.matrix([[mp.mpc(str(float(a[i,j].real)),str(float(a[i,j].imag)))
                       for j in range(a.shape[1])] for i in range(a.shape[0])])

def mp_to_np(a):
    return np.array([[complex(float(mp.re(a[i,j])),float(mp.im(a[i,j])))
                      for j in range(a.cols)] for i in range(a.rows)])

def mp_norm(a):
    return mp.sqrt(mp.fsum([abs(a[i,j])**2 for i in range(a.rows) for j in range(a.cols)]))

def _global_index(bits):
    return (bits[0]<<2)|(bits[1]<<1)|bits[2]

def mp_restrict(a,keep):
    """80-digit partial trace with retained qubits in the explicit order 'keep'."""
    if a.rows!=8 or a.cols!=8 or len(keep)!=2 or len(set(keep))!=2:
        raise ValueError('expected 3-qubit matrix and ordered two-qubit keep tuple')
    rest=[q for q in range(3) if q not in keep]
    if len(rest)!=1:
        raise ValueError('invalid retained coordinates')
    out=mp.matrix(4,4)
    for r in range(4):
        rb=[0,0,0]
        for pos,q in enumerate(keep):
            rb[q]=(r>>(1-pos))&1
        for c in range(4):
            cb=[0,0,0]
            for pos,q in enumerate(keep):
                cb[q]=(c>>(1-pos))&1
            val=mp.mpc(0)
            for t in (0,1):
                rr=rb.copy();cc=cb.copy()
                rr[rest[0]]=t;cc[rest[0]]=t
                val += a[_global_index(rr),_global_index(cc)]
            out[r,c]=val
    return out

def run_measurement():
    rows=[]
    try:
        states=V64.ASYM.select_states()
        indices=[x['candidate_index'] for x in states]
        if indices!=EXPECTED:
            return {'verdict':'INVALID','n_float_witnesses':0,'n_nonzero_mp_cases':0,
                    'error':'state identity mismatch','rows':[]}
        gram=V71.memory_gram()
        valid=(np.linalg.matrix_rank(gram)==27
               and np.max(np.abs(gram-np.eye(27)))<=1e-12)
        nfloat=0;nmp=0
        max_full_abs=0.;max_full_rel=0.;max_inc_abs=0.;max_inc_rel=0.;max_mp_rel=mp.mpf('0')
        for row in states:
            rho=row['rho']
            y,lift=V64.target_Y(rho)
            yl=[V71.local_retained_lift(V70.restrict(rho,e)) for e in EDGES]
            yr=[V70.restrict(y,e) for e in EDGES]
            local_rel=max(float(np.linalg.norm(a-b)/np.linalg.norm(b)) for a,b in zip(yl,yr))
            valid &= lift<=1e-10 and local_rel<=1e-10
            state_full_rel=0.;state_inc_rel=0.;state_mp_rel=mp.mpf('0')
            state_full_abs=0.;state_inc_abs=0.
            for ai,h in enumerate(HIDDEN):
                for sign in (-1,1):
                    sigma=rho+sign*ETA*h
                    m=V71.memory(sigma-rho)
                    sigma_mp=None
                    for bi in range(27):
                        coeff=STRENGTH*m[bi]
                        delta=coeff*y
                        gout=sigma+delta
                        for ei,e in enumerate(EDGES):
                            q=V70.restrict(sigma,e)
                            dr=coeff*yl[ei]
                            actual=V70.restrict(gout,e)
                            regional=q+dr
                            full_abs=float(np.linalg.norm(actual-regional))
                            state_full_abs=max(state_full_abs,full_abs)
                            max_full_abs=max(max_full_abs,full_abs)
                            dg=V70.restrict(delta,e)
                            inc_abs=float(np.linalg.norm(dg-dr))
                            state_inc_abs=max(state_inc_abs,inc_abs)
                            max_inc_abs=max(max_inc_abs,inc_abs)
                            nfloat+=1
                            if bi==ai:
                                denom=max(float(np.linalg.norm(dr)),1e-300)
                                full_rel=full_abs/denom
                                inc_rel=inc_abs/denom
                                state_full_rel=max(state_full_rel,full_rel)
                                state_inc_rel=max(state_inc_rel,inc_rel)
                                max_full_rel=max(max_full_rel,full_rel)
                                max_inc_rel=max(max_inc_rel,inc_rel)
                                if sigma_mp is None:
                                    sigma_mp=mpcmat(sigma)
                                dgmp=mpcmat(delta)
                                drmp=mpcmat(dr)
                                gmp=mp_restrict(sigma_mp+dgmp,e)
                                rmp=mp_restrict(sigma_mp,e)+drmp
                                denmp=max(mp_norm(drmp),mp.mpf('1e-300'))
                                relmp=mp_norm(gmp-rmp)/denmp
                                state_mp_rel=max(state_mp_rel,relmp)
                                max_mp_rel=max(max_mp_rel,relmp)
                                nmp+=1
            rows.append({
                'candidate_index':row['candidate_index'],
                'lift_relative_residual':float(lift),
                'local_lift_relative_residual':local_rel,
                'float_full_state_absolute_residual_max':state_full_abs,
                'float_full_state_relative_residual_max':state_full_rel,
                'float_increment_absolute_residual_max':state_inc_abs,
                'float_increment_relative_residual_max':state_inc_rel,
                'mp_full_state_relative_residual_max':float(state_mp_rel),
            })
        valid &= nfloat==52488 and nmp==1944
        float_failure=max_full_rel>1e-9
        increment_pass=max_inc_rel<=1e-12
        mp_pass=float(max_mp_rel)<=1e-12
        verdict=adjudicate(bool(valid),float_failure,increment_pass,mp_pass)
        return {
            'verdict':verdict,
            'historical_v15_71_verdict':'MINIMAL_EXTENSION_MEMORY_DESCENT_NOT_CONFIRMED',
            'n_states':len(states),
            'candidate_indices':indices,
            'n_float_witnesses':nfloat,
            'n_nonzero_mp_cases':nmp,
            'mp_dps':MP_DPS,
            'eta':ETA,'source_strength':STRENGTH,
            'float_full_state_absolute_residual_max':max_full_abs,
            'float_full_state_relative_residual_max':max_full_rel,
            'float_increment_absolute_residual_max':max_inc_abs,
            'float_increment_relative_residual_max':max_inc_rel,
            'mp_full_state_relative_residual_max':float(max_mp_rel),
            'float_failure_reproduced':bool(float_failure),
            'increment_identity_pass':bool(increment_pass),
            'high_precision_full_state_pass':bool(mp_pass),
            'valid':bool(valid),
            'python_version':sys.version,
            'numpy_version':np.__version__,
            'mpmath_version':mp.__version__,
            'rows':rows,
        }
    except Exception as exc:
        return {'verdict':'INVALID','n_float_witnesses':0,'n_nonzero_mp_cases':0,
                'error':repr(exc),'rows':rows}

def finalize_report(report):
    nonfinite=[]
    def clean(v,path):
        if isinstance(v,dict):
            return {k:clean(x,path+'.'+k) for k,x in v.items()}
        if isinstance(v,list):
            return [clean(x,path+'['+str(i)+']') for i,x in enumerate(v)]
        if isinstance(v,(float,np.floating)) and not np.isfinite(v):
            nonfinite.append(path);return None
        return v
    out=clean(report,'report')
    if nonfinite:
        out['verdict']='INVALID'
        out['nonfinite_diagnostic_paths']=nonfinite
    return out

if __name__=='__main__':
    r=finalize_report(run_measurement())
    print(json.dumps(r,indent=2,sort_keys=True,allow_nan=False))
    raise SystemExit(2 if r['verdict']=='INVALID' else 0)
