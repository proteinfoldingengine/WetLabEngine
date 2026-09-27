"""v15.74 fixed-Hamiltonian coefficient kernel; ordered source labels only."""
import importlib.util
import itertools
import json
import pathlib
import sys
import numpy as np

HERE=pathlib.Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('unitary73_classification',HERE.parent/'two-body-unitary-source'/'gate.py')
V73=importlib.util.module_from_spec(spec);spec.loader.exec_module(V73)
M=V73.M
LABELS=[x for x in itertools.product(range(4),repeat=3) if any(x)]
PAULIS=np.array([M.F.op(*x) for x in LABELS])
WEIGHTS=np.array([sum(a!=0 for a in x) for x in LABELS])
GROUPS={'local':np.flatnonzero(WEIGHTS==1),'two_body':np.flatnonzero(WEIGHTS==2),
        'three_body':np.flatnonzero(WEIGHTS==3),'interacting':np.flatnonzero(WEIGHTS>=2)}
THRESHOLDS=[1e-9,1e-10,1e-11]
S=1e-3

def rank_sweep(a,reference):
    sv=np.linalg.svd(a,compute_uv=False)
    return [int(np.count_nonzero(sv>t*reference)) for t in THRESHOLDS]

def kernel_basis(a,reference):
    if a.shape[0]<a.shape[1]:raise ValueError('kernel helper requires tall or square matrix')
    _,sv,vh=np.linalg.svd(a,full_matrices=False)
    return vh[sv<=THRESHOLDS[1]*reference].T

def kernel_projector(a,reference):
    k=kernel_basis(a,reference);return k@k.T

def summary(a,reference=None):
    sv=np.linalg.svd(a,compute_uv=False)
    ref=float(sv[0]) if reference is None else float(reference)
    return {'singular_values':sv.tolist(),'reference':ref,'ranks':rank_sweep(a,ref)}

def coordinate_projector(indices):
    p=np.zeros((63,63));p[indices,indices]=1.;return p

def describe(a):
    out=summary(a);ref=out['reference']
    out['groups']={name:summary(a[:,idx],ref) for name,idx in GROUPS.items()}
    out['local_relative_norm']=float(np.linalg.norm(a[:,GROUPS['local']])/np.linalg.norm(a))
    out['null_projector']=kernel_projector(a,ref).tolist()
    return out

def adjudicate(valid,passed):
    if not valid:return 'INVALID'
    return 'HAMILTONIAN_NULL_KERNEL_LOCAL_ONLY_CONFIRMED' if passed else 'HAMILTONIAN_INTERACTION_NULL_NOT_EXCLUDED'

def geometry_from_retained(rho,retained):
    """retained shape: (source, hidden, 36); output hidden-major rows."""
    one=M.moments(rho,M.ONE).reshape(3,3)
    cs=M.correlations(rho)
    # Positive-polar decomposition and Sylvester eigensystem per edge, shared over probes.
    pol=[]
    for c in cs:
        o,p,_=M.polar(c);vals,v=np.linalg.eigh((p+p.T)/2)
        pol.append((o,p,vals,v))
    ns,nh,_=retained.shape
    qmap=np.zeros((nh,9,ns));emap=np.zeros_like(qmap);sylvester=0.
    for j in range(ns):
        for k in range(nh):
            u=retained[j,k,:9].reshape(3,3);pair=retained[j,k,9:].reshape(3,3,3)
            for e,(i,l) in enumerate(M.EDGES):
                dc=pair[e]-np.outer(u[i],one[l])-np.outer(one[i],u[l])
                o,p,vals,v=pol[e];q=o.T@dc-dc.T@o
                w=v@((v.T@q@v)/(vals[:,None]+vals[None,:]))@v.T
                sylvester=max(sylvester,float(np.linalg.norm(p@w+w@p-q)))
                qmap[k,3*e:3*e+3,j]=V73.skew_coords(q)
                emap[k,3*e:3*e+3,j]=V73.skew_coords(w)
    return qmap.reshape(nh*9,ns),emap.reshape(nh*9,ns),sylvester

def control_fixture(beta=0.):
    rho=np.eye(8,dtype=complex)
    for i,j in M.EDGES:
        for a in range(1,4):
            label=[0,0,0];label[i]=label[j]=a;rho+=.04*M.F.op(*label)
    rho+=beta*M.F.op(0,1,0)
    return rho/8

def run_measurement():
    rows=[];controls={};report={}
    try:
        selected=M.V70.V64.ASYM.select_states()
        indices=[s['candidate_index'] for s in selected]
        if indices!=M.EXPECTED:raise ValueError('frozen state identity mismatch')
        hidden=np.array(M.HIDDEN);observables=np.concatenate([M.ONE,M.PAIR])
        ys=np.array([[V73.response(p,h) for h in hidden] for p in PAULIS])
        raw=np.einsum('shij,kji->shk',ys,observables)
        retained=raw.real
        controls['imaginary_moment']=float(np.max(np.abs(raw.imag)))
        controls['tangent_trace']=float(np.max(np.abs(np.trace(ys,axis1=-2,axis2=-1))))
        controls['tangent_hermiticity']=float(np.max(np.linalg.norm(ys-ys.conj().transpose(0,1,3,2),axis=(-2,-1))))
        adjoint=np.zeros_like(raw)
        for j,p in enumerate(PAULIS):
            hamiltonian=p/2
            comm=hamiltonian@observables-observables@hamiltonian
            adjoint[j]=1j*np.einsum('hij,kji->hk',hidden,comm)
        controls['adjoint_moment_disagreement']=float(np.max(np.abs(raw-adjoint)))
        controls['centered_identity']=0.;controls['unitarity']=0.
        for j,p in enumerate(PAULIS):
            up=V73.unitary(p,S);um=V73.unitary(p,-S)
            controls['unitarity']=max(controls['unitarity'],*(float(np.linalg.norm(u.conj().T@u-np.eye(8))) for u in [up,um]))
            for k,h in enumerate(hidden):
                finite=(V73.channel(up,h)-V73.channel(um,h))/(2*S)
                controls['centered_identity']=max(controls['centered_identity'],float(np.linalg.norm(finite-np.sin(S)/S*ys[j,k])))
        b=retained.transpose(1,2,0).reshape(972,63)
        binfo=summary(b);bref=binfo['reference']
        bone=retained[:,:,:9].transpose(1,2,0).reshape(243,63)
        bpair=retained[:,:,9:].transpose(1,2,0).reshape(729,63)
        binfo['two_body_pair']=summary(bpair[:,GROUPS['two_body']],bref)
        binfo['three_body_one']=summary(bone[:,GROUPS['three_body']],bref)
        controls['local_retained_norm']=float(np.linalg.norm(b[:,GROUPS['local']]))
        zero=control_fixture();bloch=control_fixture(.02)
        controls['domain']=M.domain([s['rho'] for s in selected]+[zero,bloch])
        coefficients=(-1.)**np.arange(63)/np.sqrt(63)
        combined_h=sum(c*p/2 for c,p in zip(coefficients,PAULIS))
        combined_y=np.array([-1j*(combined_h@h-h@combined_h) for h in hidden])
        combined_ret=np.einsum('hij,kji->hk',combined_y,observables).real[None,:,:]
        controls['assembly_Q']=0.;controls['assembly_E']=0.;controls['sylvester']=0.
        controls['local_Q_relative']=0.;controls['local_E_relative']=0.
        qstack=[];estack=[]
        for state in selected:
            q,e,sy=geometry_from_retained(state['rho'],retained)
            qc,ec,syc=geometry_from_retained(state['rho'],combined_ret)
            controls['assembly_Q']=max(controls['assembly_Q'],float(np.max(np.abs(q@coefficients-qc[:,0]))))
            controls['assembly_E']=max(controls['assembly_E'],float(np.max(np.abs(e@coefficients-ec[:,0]))))
            controls['sylvester']=max(controls['sylvester'],sy,syc)
            dq,de=describe(q),describe(e)
            for key,d in [('local_Q_relative',dq),('local_E_relative',de)]:controls[key]=max(controls[key],d['local_relative_norm'])
            rows.append({'candidate_index':state['candidate_index'],'Q':dq,'E':de,'Q_map':q.tolist(),'E_map':e.tolist()})
            qstack.append(q);estack.append(e)
        qstack=np.concatenate(qstack);estack=np.concatenate(estack)
        stacks={'Q':describe(qstack),'E':describe(estack)}
        p_local=coordinate_projector(GROUPS['local'])
        for d in stacks.values():d['local_projector_error']=float(np.linalg.norm(np.array(d['null_projector'])-p_local))
        null_diagnostics={}
        for name,a in [('Q',qstack),('E',estack)]:
            k=kernel_basis(a[:,GROUPS['interacting']],stacks[name]['reference'])
            full=np.zeros((63,k.shape[1]));full[GROUPS['interacting']]=k
            null_diagnostics[name]={'dimension':k.shape[1],'coefficient_basis':full.tolist(),
                                   'B_norms':np.linalg.norm(b@full,axis=0).tolist(),
                                   'Q_norms':np.linalg.norm(qstack@full,axis=0).tolist(),
                                   'E_norms':np.linalg.norm(estack@full,axis=0).tolist()}
        q0,e0,sy0=geometry_from_retained(zero,retained)
        controls['sylvester']=max(controls['sylvester'],sy0)
        exceptional={'Q':describe(q0),'E':describe(e0)}
        p_zero=coordinate_projector(np.flatnonzero(WEIGHTS!=2))
        for name,a in [('Q',q0),('E',e0)]:
            d=exceptional[name]
            d['three_body_relative_norm']=float(np.linalg.norm(a[:,GROUPS['three_body']])/np.linalg.norm(a))
            d['expected_projector_error']=float(np.linalg.norm(np.array(d['null_projector'])-p_zero))
            controls['local_'+name+'_relative']=max(controls['local_'+name+'_relative'],d['local_relative_norm'])
        # An independently known single-source/probe geometry checks the Bloch subtraction.
        pj=LABELS.index((1,1,1));hk=M.LABELS.index((2,1,1))
        qb,eb,syb=geometry_from_retained(bloch,retained[pj:pj+1,hk:hk+1,:])
        controls['sylvester']=max(controls['sylvester'],syb)
        expected_q=np.array([0.,.08,0.,0.,0.,0.,0.,0.,0.])
        # D=-sqrt(8)*beta e_z e_x^T gives Q_02=+sqrt(8)*beta.
        controls['bloch_Q_error']=float(np.linalg.norm(qb[:,0]-expected_q))
        controls['bloch_E_error']=float(np.linalg.norm(eb[:,0]-expected_q/(2*.04)))
        controls['bloch_Q_norm']=float(np.linalg.norm(qb));controls['bloch_E_norm']=float(np.linalg.norm(eb))
        algebra_ok=binfo['ranks']==[54]*3 and binfo['two_body_pair']['ranks']==[27]*3 and binfo['three_body_one']['ranks']==[27]*3
        exception_ok=all(d['ranks']==[27]*3 and d['three_body_relative_norm']<=1e-12 and d['expected_projector_error']<=1e-8 for d in exceptional.values())
        limits={'imaginary_moment':1e-12,'tangent_trace':1e-12,'tangent_hermiticity':1e-12,
                'adjoint_moment_disagreement':1e-12,'centered_identity':1e-10,'unitarity':1e-12,
                'local_retained_norm':1e-12,'assembly_Q':1e-10,'assembly_E':1e-10,'sylvester':1e-10,
                'local_Q_relative':1e-12,'local_E_relative':1e-12,'bloch_Q_error':1e-12,'bloch_E_error':1e-12}
        controls['algebra_control_pass']=bool(algebra_ok);controls['exceptional_control_pass']=bool(exception_ok)
        valid=controls['domain']['valid'] and algebra_ok and exception_ok and all(controls[k]<=v for k,v in limits.items())
        valid=valid and len(rows)==12 and ys.shape[:2]==(63,27) and qstack.shape==(2916,63)
        passed=all(row[name]['groups']['two_body']['ranks']==[27]*3 for row in rows for name in ['Q','E'])
        passed=passed and all(d['ranks']==[54]*3 and d['groups']['interacting']['ranks']==[54]*3 and d['local_projector_error']<=1e-8 for d in stacks.values())
        report={'verdict':adjudicate(valid,passed),'all_valid':bool(valid),'scientific_pass':bool(passed),
                'candidate_indices':indices,'source_hidden_pairs':1701,'stack_shape':list(qstack.shape),
                'source_labels':LABELS,'hidden_labels':M.LABELS,'rank_thresholds':THRESHOLDS,
                'source_strength':S,'controls':controls,'B':binfo,'B_map':b.tolist(),'states':rows,
                'stacked':stacks,'interacting_null_diagnostics':null_diagnostics,'exceptional':exceptional}
        return M.V70.finalize_report(report)
    except (ValueError,np.linalg.LinAlgError,FloatingPointError) as exc:
        return M.V70.finalize_report({'verdict':'INVALID','all_valid':False,'error':str(exc),'controls':controls,'states':rows})

if __name__=='__main__':
    r=run_measurement();print(json.dumps(r,indent=2,allow_nan=False));sys.exit(2 if r['verdict']=='INVALID' else 0)
