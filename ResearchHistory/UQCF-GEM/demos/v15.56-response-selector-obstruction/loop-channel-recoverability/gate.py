"""v15.84: conditional unital Bloch-channel and binary recovery diagnostics."""
import functools
import hashlib
import json
import pathlib
import sys
import mpmath as mp

HERE=pathlib.Path(__file__).resolve().parent
PARENT_HASH='bb2299a633e857beeabce7b05208b9c924d88b3bbceb1f033f772657457c7166'
I=mp.eye(2)
PAULI=[mp.matrix([[0,1],[1,0]]),mp.matrix([[0,-mp.j],[mp.j,0]]),mp.matrix([[1,0],[0,-1]])]
UNITS=[]
for a in range(2):
    for b in range(2):
        z=mp.zeros(2);z[a,b]=1;UNITS.append(z)


def tr(z):return sum(z[i,i] for i in range(z.rows))
def maximum(z):return max(abs(x) for x in z)
def number(x):return mp.nstr(x,80)
def matrix(a):return [[number(a[i,j]) for j in range(a.cols)] for i in range(a.rows)]
def real_matrix(a):return mp.matrix([[mp.mpf(v) for v in row] for row in a])

def bloch(v):
    out=mp.zeros(2)
    for i in range(3):out+=v[i]*PAULI[i]
    return out


def phi(t,z):
    out=tr(z)*I
    for j in range(3):
        coefficient=tr(PAULI[j]*z)
        for i in range(3):out+=t[i,j]*coefficient*PAULI[i]
    return out/2


def choi(t):
    j=mp.zeros(4)
    for a in range(2):
        for b in range(2):
            out=phi(t,UNITS[2*a+b])
            for i in range(2):
                for k in range(2):j[2*a+i,2*b+k]=out[i,k]
    return j


def choi_action(j,z):
    out=mp.zeros(2)
    for a in range(2):
        for b in range(2):
            for i in range(2):
                for k in range(2):out[i,k]+=z[a,b]*j[2*a+i,2*b+k]
    return out


def distance(a,b):return sum(abs(x) for x in mp.eighe(a-b,eigvals_only=True))/2


def density(z):
    return {'hermiticity':maximum(z-z.H),'trace':abs(tr(z)-1),
            'minimum_eigenvalue':min(mp.eighe(z,eigvals_only=True))}


def density_valid(d):
    return d['hermiticity']<=mp.mpf('1e-45') and d['trace']<=mp.mpf('1e-45') and d['minimum_eigenvalue']>=-mp.mpf('1e-40')


def channel_diagnostics(t):
    j=choi(t);tp=mp.zeros(2);unital=mp.zeros(2)
    for a in range(2):
        for b in range(2):
            tp[a,b]=sum(j[2*a+i,2*b+i] for i in range(2))
            unital[a,b]=sum(j[2*i+a,2*i+b] for i in range(2))
    residuals={'hermiticity':maximum(j-j.H),'trace_preserving':maximum(tp-I),
               'unital':maximum(unital-I),
               'action_reconstruction':max(maximum(phi(t,z)-choi_action(j,z)) for z in UNITS)}
    eigen=mp.eighe(j,eigvals_only=True)
    return j,list(eigen),residuals


def cp_class(minimum):
    x=mp.mpf(str(minimum))
    if x>=-mp.mpf('1e-40'):return 'CPTP'
    if x<=-mp.mpf('1e-8'):return 'NON_CP'
    return 'UNRESOLVED'


def adjudicate(valid,pattern,recovery):
    if not valid:return 'INVALID','INVALID'
    return ('LATE_CPTP_LOOP_POWER_CONFIRMED' if pattern else 'LATE_CPTP_LOOP_POWER_NOT_CONFIRMED',
            'CPTP_LOOP_RECOVERY_OBSTRUCTED' if recovery else 'CPTP_LOOP_RECOVERY_OBSTRUCTION_NOT_CONFIRMED')


def synthetic_controls():
    with mp.workdps(80):
        ts=[mp.eye(3),mp.zeros(3),mp.diag([1,1,0]),mp.diag([mp.mpf('.3'),mp.mpf('.2'),0])]
        expected=[[0,0,0,2],[mp.mpf('.5')]*4,[-mp.mpf('.5'),mp.mpf('.5'),mp.mpf('.5'),mp.mpf('1.5')],
                  [mp.mpf('.25'),mp.mpf('.45'),mp.mpf('.55'),mp.mpf('.75')]]
        errors=[];rows=[]
        for t,target in zip(ts,expected):
            j,e,c=channel_diagnostics(t);error=max(abs(a-b) for a,b in zip(e,target))
            errors.extend([error,*c.values()]);rows.append({'spectrum':[number(x) for x in e],'spectrum_error':number(error)})
        # Y-axis inputs ensure the complex transport is actually exercised.
        plus=(I+PAULI[1])/2;minus=(I-PAULI[1])/2
        d1=distance(phi(ts[0],plus),phi(ts[0],minus));d0=distance(phi(ts[1],plus),phi(ts[1],minus))
        errors.extend([abs(d1-1),abs(d0),max(maximum(phi(ts[0],z)-z) for z in UNITS)])
        return {'valid':bool(max(errors)<=mp.mpf('1e-45')),'map_count':4,'rows':rows,
                'identity_distance':number(d1),'depolarized_distance':number(d0),'max_error':number(max(errors))}


def measurement_preparation(z,input_axis,output_axis):
    result=mp.zeros(2)
    for sign in [1,-1]:
        effect=(I+sign*bloch(input_axis))/2
        prepared=(I+sign*bloch(output_axis))/2
        result+=tr(effect*z)*prepared
    return result


def recovery_diagnostics(t):
    u,s,vh=mp.svd_r(t)
    left=[mp.matrix([u[i,a] for i in range(3)]) for a in range(3)]
    right=[mp.matrix([vh[a,i] for i in range(3)]) for a in range(3)]
    weights=[s[0],s[1],1-s[0]-s[1]]
    def constructed(z):
        return (weights[0]*measurement_preparation(z,right[0],left[0])+
                weights[1]*measurement_preparation(z,right[1],left[1])+weights[2]*tr(z)*I/2)
    construction_error=max(maximum(constructed(z)-phi(t,z)) for z in UNITS)
    densities=[];axes=[];errors=[]
    for a in range(3):
        inputs=[(I+sign*bloch(right[a]))/2 for sign in [1,-1]]
        outputs=[phi(t,z) for z in inputs]
        # This attaining recovery is specific to the chosen binary axis ensemble.
        recovered=[measurement_preparation(z,left[a],right[a]) for z in outputs]
        densities.extend(density(z) for z in inputs+outputs+recovered)
        din=distance(*inputs);dout=distance(*outputs)
        mean=sum(mp.re(tr(target*out)) for target,out in zip(inputs,recovered))/2
        optimum=(1+dout)/2
        errors.extend([abs(din-1),abs(dout-s[a]),abs(mean-optimum)])
        axes.append({'axis':a,'role':'active' if a<2 else 'kernel',
                     'input_axis':[number(x) for x in right[a]],'output_axis':[number(x) for x in left[a]],
                     'input_distance':number(din),'output_distance':number(dout),
                     'optimal_mean_overlap_fidelity':number(optimum),'attained_mean_overlap_fidelity':number(mean)})
    inverse=vh.T*mp.diag([1/s[0],1/s[1],0])*u.T
    pin=vh.T*mp.diag([1,1,0])*vh
    inversion_error=maximum(inverse*t-pin);witnesses=[]
    for a in range(2):
        source=(I+bloch(left[a]))/2;out=phi(inverse,source)
        densities.append(density(source));d=density(out)
        witnesses.append({'axis':a,'formal_output_eigenvalues':[number(x) for x in mp.eighe(out,eigvals_only=True)],
                          'minimum_eigenvalue':number(d['minimum_eigenvalue']),
                          'trace_error':number(d['trace']),'hermiticity_error':number(d['hermiticity'])})
        errors.extend([d['trace'],d['hermiticity']])
    valid=(min(weights)>=-mp.mpf('1e-40') and abs(sum(weights)-1)<=mp.mpf('1e-45') and
           construction_error<=mp.mpf('1e-45') and all(density_valid(d) for d in densities) and
           max(errors)<=mp.mpf('1e-45') and inversion_error<=mp.mpf('1e-45'))
    return {'valid':bool(valid),'weights':[number(x) for x in weights],
            'measure_prepare_reconstruction_error':number(construction_error),'axes':axes,
            'inverse_matrix':matrix(inverse),'inverse_initial_plane_error':number(inversion_error),
            'inverse_witnesses':witnesses,'max_distance_fidelity_error':number(max(errors)),
            'minimum_admissible_state_eigenvalue':number(min(d['minimum_eigenvalue'] for d in densities)),
            'max_admissible_state_trace_error':number(max(d['trace'] for d in densities)),
            'max_admissible_state_hermiticity_error':number(max(d['hermiticity'] for d in densities))}


@functools.lru_cache(maxsize=1)
def run_measurement():
    with mp.workdps(80):return _run()


def _run():
    payload=(HERE.parent/'support-loop-composition'/'RESULT.json').read_bytes();prior=json.loads(payload)
    parent_ok=(hashlib.sha256(payload).hexdigest()==PARENT_HASH and prior['all_valid'] and
               prior['crossing_verdict']=='SUPPORT_RESTRICTED_CROSSING_CONFIRMED' and
               prior['composition_verdict']=='SUPPORT_LOOP_COMPOSITION_OBSTRUCTED' and
               prior['core_verdict']=='LOSSLESS_LOOP_CORE_TRIVIAL')
    loop=real_matrix(prior['loop']);t=mp.eye(3);rows=[];all_rows=True;final=None
    for n in range(1,5):
        t=t*loop;j,e,residuals=channel_diagnostics(t);s=mp.svd_r(t,compute_uv=False)
        matrix_error=maximum(t-real_matrix(prior['powers'][n-1]['matrix']))
        spectrum_error=max(abs(s[i]-mp.mpf(prior['powers'][n-1]['singular_values'][i])) for i in range(3))
        predicted=[(1-s[0]-s[1])/2,(1-s[0]+s[1])/2,(1+s[0]-s[1])/2,(1+s[0]+s[1])/2]
        formula_error=max(abs(a-b) for a,b in zip(e,predicted))
        valid=(matrix_error<=mp.mpf('1e-60') and spectrum_error<=mp.mpf('1e-60') and
               s[1]>=mp.mpf('1e-4') and s[2]<=mp.mpf('1e-60') and s[0]<=1+mp.mpf('1e-40') and
               max(*residuals.values(),formula_error)<=mp.mpf('1e-45'))
        all_rows=all_rows and valid
        rows.append({'n':n,'classification':cp_class(e[0]),'singular_values':[number(x) for x in s],
                     'choi_eigenvalues':[number(x) for x in e],'bell_output_minimum_eigenvalue':number(e[0]/2),
                     'choi_real':matrix(j.apply(mp.re)),'choi_imag':matrix(j.apply(mp.im)),
                     'parent_matrix_error':number(matrix_error),'parent_spectrum_error':number(spectrum_error),
                     'rank_two_formula_error':number(formula_error),'controls':{k:number(v) for k,v in residuals.items()},'valid':bool(valid)})
        if n==4:final=t
    recovery=recovery_diagnostics(final) if rows[-1]['classification']=='CPTP' else None
    synthetic=synthetic_controls()
    valid=parent_ok and all_rows and synthetic['valid'] and (recovery is None or recovery['valid'])
    pattern=([r['classification'] for r in rows]==['NON_CP','NON_CP','NON_CP','CPTP'] and recovery is not None and recovery['valid'])
    recover_no=False
    if recovery is not None:
        recover_no=(recovery['valid'] and all(mp.mpf('1e-4')<=mp.mpf(x['output_distance'])<=1-mp.mpf('1e-4') for x in recovery['axes'][:2]) and
                    mp.mpf(recovery['axes'][2]['output_distance'])<=mp.mpf('1e-40') and
                    all(mp.mpf(x['minimum_eigenvalue'])<=-mp.mpf('1e-4') for x in recovery['inverse_witnesses']))
    verdict,rv=adjudicate(valid,pattern,recover_no)
    report={'version':'15.84','parent_result_sha256':PARENT_HASH,'candidate_index':46,'precision_digits':80,
            'interpretation':'Conditional unital Bloch extension of retained loop, not the original source channel.',
            'all_valid':bool(valid),'verdict':verdict,'recovery_verdict':rv,
            'controls':{'parent_valid':bool(parent_ok),'all_rows_valid':bool(all_rows),'synthetic':synthetic},
            'rows':rows,'recovery':recovery}
    def finite(a):
        if isinstance(a,dict):return all(finite(v) for v in a.values())
        if isinstance(a,list):return all(finite(v) for v in a)
        if isinstance(a,str):return a.lower() not in ['nan','inf','+inf','-inf']
        return True
    if not finite(report):report['all_valid']=False;report['verdict']='INVALID';report['recovery_verdict']='INVALID'
    return report

if __name__=='__main__':
    result=run_measurement();print(json.dumps(result,indent=2,allow_nan=False));sys.exit(0 if result['all_valid'] else 2)
