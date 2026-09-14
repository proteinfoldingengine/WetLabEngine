#!/usr/bin/env python3
"""v15.20: CPTP representation of the fixed predictor and explicit readout cost.

The comparison channels are diagnostic inputs, not adopted collapse/pruning laws.
No entropy, physical clock, outcome selection, or changed dynamics is introduced.
"""
from __future__ import annotations
import argparse
from functools import lru_cache
import hashlib
import itertools
import json
import math
from numbers import Real
from pathlib import Path
import sys
import numpy as np

ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'baseline'))
import linear_module as prior
D=16
TOL=1e-10
CP_TOL=1e-12
LOCAL={'I':np.eye(2,dtype=complex),'X':np.array([[0,1],[1,0]],complex),
       'Y':np.array([[0,-1j],[1j,0]],complex),'Z':np.diag([1.,-1.]).astype(complex)}


def verify_baseline() -> dict:
    expected=json.loads((ROOT/'BASELINE_SHA256.json').read_text())
    for name,digest in expected.items():
        if hashlib.sha256((ROOT/'baseline'/name).read_bytes()).hexdigest()!=digest:
            raise ValueError(f'frozen baseline changed: {name}')
    prior.verify_baseline()
    return {'all_match':True,'python_files':len(expected)}


@lru_cache(None)
def labels() -> tuple[str,...]:
    return tuple(''.join(x) for x in itertools.product('IXYZ',repeat=4))


@lru_cache(None)
def paulis() -> np.ndarray:
    result=[]
    for word in labels():
        p=np.ones((1,1),complex)
        for x in word:p=np.kron(p,LOCAL[x])
        result.append(p)
    a=np.asarray(result);return np.frombuffer(a.tobytes(),dtype=complex).reshape(256,16,16)


def gamma_index() -> int:return labels().index('YYYY')

def gamma() -> np.ndarray:return paulis()[gamma_index()]


@lru_cache(None)
def characters() -> np.ndarray:
    words=labels();chi=np.empty((256,256),dtype=np.int16)
    for i,a in enumerate(words):
        for j,b in enumerate(words):
            n=sum(x!='I' and y!='I' and x!=y for x,y in zip(a,b))
            chi[i,j]=(-1)**n
    return np.frombuffer(chi.tobytes(),dtype=np.int16).reshape(256,256)


def commuting_visible_indices() -> np.ndarray:
    return np.array([j for j in range(256) if j not in (0,gamma_index()) and characters()[j,gamma_index()]==1])


def _matrix(a) -> np.ndarray:
    a=np.asarray(a,complex)
    if a.shape!=(D,D) or not np.isfinite(a).all():raise ValueError('finite 16x16 operator required')
    return a


def _state(a) -> np.ndarray:
    a=_matrix(a)
    if np.linalg.norm(a-a.conj().T)>TOL or abs(np.trace(a)-1)>TOL or np.linalg.eigvalsh(a).min() < -TOL:
        raise ValueError('positive normalized state required')
    return a


def parameters(lam: float,t: float) -> tuple[float,float]:
    for x in (lam,t):
        if isinstance(x,(bool,np.bool_)) or not isinstance(x,Real) or not math.isfinite(x) or not 0<=x<=1:
            raise ValueError('finite real parameters in [0,1] required; they are not physical time')
    return float(lam),float(t)


def linear_map(a: np.ndarray,lam: float,t: float) -> np.ndarray:
    """Algebraic family; may be nonpositive. Use apply_channel for physical checks.

    Identity gain=1; Gamma gain=t; all other Pauli gains=lam.
    """
    a=_matrix(a);lam,t=parameters(lam,t)
    return lam*a+(1-lam)*np.trace(a)*np.eye(D)/D+(t-lam)*np.trace(gamma()@a)*gamma()/D


def pauli_weights(lam: float,t: float) -> np.ndarray:
    """Normalized Choi eigenvalues; exact finite character-transform formula."""
    lam,t=parameters(lam,t)
    q=np.where(characters()[:,gamma_index()]==1,(1+t-2*lam)/256,(1-t)/256)
    q[0]=(1+t+254*lam)/256
    return q


def channel_kraus(lam: float,t: float) -> np.ndarray:
    q=pauli_weights(lam,t)
    if q.min() < -CP_TOL:raise ValueError('not completely positive: negative Pauli/Choi weight')
    # Only roundoff-sized negative weights can reach this line; no model repair.
    inds=np.flatnonzero(q>0)
    return np.sqrt(q[inds])[:,None,None]*paulis()[inds]


def apply_channel(rho: np.ndarray,lam: float,t: float) -> np.ndarray:
    rho=_state(rho)
    if pauli_weights(lam,t).min() < -CP_TOL:raise ValueError('non-CPTP parameter point')
    return linear_map(rho,lam,t)


def from_kraus(a: np.ndarray,ks) -> np.ndarray:
    a=_matrix(a);ks=np.asarray(ks,complex)
    if ks.ndim!=3 or ks.shape[1:]!=(D,D) or not len(ks) or not np.isfinite(ks).all():
        raise ValueError('finite nonempty matching Kraus list required')
    return sum((k@a@k.conj().T for k in ks),np.zeros_like(a))


def choi_from_action(action) -> np.ndarray:
    """Normalized Choi, input tensor output, obtained from all matrix units."""
    j=np.zeros((D*D,D*D),complex)
    for a in range(D):
        for b in range(D):
            e=np.zeros((D,D),complex);e[a,b]=1
            j[a*D:(a+1)*D,b*D:(b+1)*D]=action(e)/D
    return j


def fixture() -> np.ndarray:return prior.old.old.old.fixture()

def frozen_motions() -> list[np.ndarray]:return prior.old.input_motions('all_six')


def parity_twins() -> tuple[np.ndarray,np.ndarray]:
    return (np.eye(D)+gamma())/D,(np.eye(D)-gamma())/D


def y_product_state() -> np.ndarray:
    v=np.array([1,1j])/np.sqrt(2);p=v
    for _ in range(3):p=np.kron(p,v)
    return np.outer(p,p.conj())


def distance(a,b) -> float:
    d=np.asarray(a)-np.asarray(b)
    return float(np.abs(np.linalg.eigvalsh((d+d.conj().T)/2)).sum()/2)


@lru_cache(None)
def baseline_control() -> dict:
    verify_baseline();f=prior.old.old.old.basis()
    module=prior.family_module('all_six','1111');q=module['basis']
    g=prior.coordinates(f@gamma()@f.conj().T).real/4
    err=float(np.linalg.norm(q@q.T-(np.eye(256)-np.outer(g,g))))
    return {'linear_dimension':module['dimension'],'projector_error':err,
            'motion_commutator':max(float(np.linalg.norm(u@gamma()-gamma()@u)) for u in frozen_motions()),
            'scope':'same frozen all-six fully-pinched target module; no rank tolerance changed'}


def rigidity_control() -> dict:
    # Fixed local X_i,Z_i generate every Pauli word by products (up to phases).
    generator_words=[]
    for i in range(4):
        for letter in 'XZ':generator_words.append('I'*i+letter+'I'*(3-i))
    gs=[paulis()[labels().index(w)] for w in generator_words]
    coeffs=[]
    for subset in itertools.product((0,1),repeat=8):
        a=np.eye(D,dtype=complex)
        for flag,g in zip(subset,gs):
            if flag:a=a@g
        # Identify a Pauli modulo its physically irrelevant global phase.
        c=np.einsum('aij,ji->a',paulis(),a)/D
        coeffs.append(int(np.argmax(abs(c))))
    a=paulis()[labels().index('YIII')];b=paulis()[labels().index('IYYY')]
    return {'fixed_visible_generators':8,'pauli_words_generated':len(set(coeffs)),
            'two_visible_unitaries_product_error':float(np.linalg.norm(a@b-gamma())),
            'minimum_output_hilbert_dimension_with_common_cptp_recovery':16,
            'theorem':'A UCP adjoint fixing visible unitary generators fixes their generated M16. Hence a CPTP encode/decode composition preserving the whole module exactly is identity.',
            'boundary':'Does not prohibit ensemble-level signed readout, state restrictions, or a non-quantum coordinate representation.'}


def decode_expectation(a: np.ndarray,sigma: np.ndarray,lam: float) -> float:
    a=_matrix(a);sigma=_state(sigma);lam,_=parameters(lam,0)
    if lam==0:raise ValueError('cannot decode zero-gain feature')
    if np.linalg.norm(a-a.conj().T)>TOL or abs(np.trace(gamma()@a))>TOL*max(1,np.linalg.norm(a)):
        raise ValueError('only Hermitian observables in Gamma-perp are decoded')
    return float(((np.trace(a@sigma)-(1-lam)*np.trace(a)/D)/lam).real)


def readout_variance(expectation: float,lam: float) -> dict:
    lam,_=parameters(lam,0)
    if not isinstance(expectation,Real) or not math.isfinite(expectation) or not -1<=expectation<=1 or lam==0:
        raise ValueError('finite Pauli expectation in [-1,1] and positive gain required')
    return {'input_expectation':float(expectation),'readout_gain':1/lam,
            'decoded_single_shot_variance':1/lam**2-expectation**2,
            'ideal_single_shot_variance':1-expectation**2,
            'interpretation':'Ensemble estimation, not quantum state recovery. No random outcomes are sampled here.'}


def amplitude_damping_kraus(eta: float) -> np.ndarray:
    _,eta=parameters(0,eta)
    k0=np.diag([1,np.sqrt(1-eta)]);k1=np.array([[0,np.sqrt(eta)],[0,0]])
    return np.array([np.kron(k,np.eye(8)) for k in (k0,k1)])


def twirl_certificate(ks) -> dict:
    """Check a GENERAL channel via its Pauli-twirl diagonal; no noise fit.

    q_E = sum_j |Tr(E K_j)|^2 / d^2. This follows from normalized Choi
    diagonal entries in the orthonormal Pauli-Bell basis and is always >=0.
    The original channel need not be unital or Pauli diagonal.
    """
    ks=np.asarray(ks,complex)
    if ks.ndim!=3 or ks.shape[1:]!=(D,D) or not len(ks) or not np.isfinite(ks).all():raise ValueError('finite Kraus list required')
    tp=np.linalg.norm(sum(k.conj().T@k for k in ks)-np.eye(D))
    if tp>TOL:raise ValueError('trace-preserving Kraus list required')
    traces=np.einsum('aij,kji->ka',paulis(),ks)
    q=np.sum(abs(traces)**2,axis=0)/D**2
    diagonals=characters().T@q
    outputs=np.zeros_like(paulis())
    for k in ks:outputs+=k@paulis()@k.conj().T
    measured=np.einsum('aij,aji->a',paulis(),outputs).real/D
    t=float(measured[gamma_index()]);mean=float(np.mean(measured[commuting_visible_indices()]))
    bound=(1+t)/2
    return {'t':t,'mean_commuting_visible_gain':mean,'bound':bound,
            'lower_bound_max_direct_feature_error':(1-t)/2,
            'character_bound_slack':bound-mean,
            'max_diagonal_transfer_error':float(np.max(abs(measured-diagonals))),
            'q_sum_error':float(abs(q.sum()-1)),
            'unital_error':float(np.linalg.norm(sum(k@k.conj().T for k in ks)-np.eye(D))),
            'scope':'Worst-input direct expectation error over all 254 visible Pauli observables; not necessarily the error for one chosen record probability.'}


@lru_cache(None)
def prediction_control() -> dict:
    f=prior.old.old.old.basis();targets=[];mask_count=0
    for mask in prior.old.old.old.masks():
        if mask in ('0000','0001'):continue
        mask_count+=1
        seed=prior.block_seed(prior.old.old.old.groups(mask))
        ops=np.einsum('ak,aij->kij',seed,prior.hermitian_basis(D))
        targets.extend(f.conj().T@ops@f)
    targets=np.array(targets);motions=frozen_motions();direct=decoded=covariance=0.;count=0
    gamma_leak=float(np.max(abs(np.einsum('ij,aji->a',gamma(),targets))))
    for original in (fixture(),y_product_state()):
        rho=original.copy();sigma=apply_channel(rho,.5,0)
        for step in range(13):
            exact=np.einsum('aij,ji->a',targets,rho).real
            raw=np.einsum('aij,ji->a',targets,sigma).real
            predicted=(raw-.5*np.trace(targets,axis1=1,axis2=2).real/D)/.5
            direct=max(direct,float(np.max(abs(raw-exact))))
            decoded=max(decoded,float(np.max(abs(predicted-exact))))
            covariance=max(covariance,float(np.linalg.norm(sigma-apply_channel(rho,.5,0))))
            count+=len(targets)
            if step<12:
                u=motions[step%6] if step<6 else motions[step%6].conj().T
                rho=u@rho@u.conj().T;sigma=u@sigma@u.conj().T
    return {'mask_count':mask_count,'word_checkpoints':13,'input_states':2,
            'targets_per_checkpoint':len(targets),'observable_predictions_checked':count,
            'max_decoded_error':decoded,'max_direct_readout_error':direct,
            'max_channel_motion_covariance_error':covariance,'max_target_parity_component':gamma_leak,
            'scope':'Finite controls plus the exact all-input identity; no motion word is a physical clock.'}


def verify_result(a: dict) -> None:
    def finite(x):
        if isinstance(x,dict):
            for v in x.values():finite(v)
        elif isinstance(x,(list,tuple)):
            for v in x:finite(v)
        elif isinstance(x,(float,int)) and not isinstance(x,bool):
            if not math.isfinite(x):raise AssertionError('nonfinite result')
    finite(a)
    for key in ('max_kraus_formula_error','max_choi_spectrum_error','max_decoded_prediction_error','max_channel_motion_covariance_error','max_twirl_formula_error'):
        if a[key]>TOL:raise AssertionError((key,a[key]))
    if a['baseline']['linear_dimension']!=255 or a['baseline']['projector_error']>1e-9:raise AssertionError('baseline mismatch')
    if abs(a['raw_projection']['min_state_eigenvalue']+1/16)>TOL:raise AssertionError('invalid-state witness')
    if a['boundary_channel']['min_choi_eigenvalue'] < -TOL or a['boundary_channel']['parity_twin_output_distance']>TOL:raise AssertionError('channel witness')
    if abs(a['boundary_channel']['visible_pair_output_distance']-.5)>TOL:raise AssertionError('feature witness')
    if a['actual_record_selected'] is not None or a['physical_duration'] is not None or a['new_physical_axioms']!=[]:raise AssertionError('claim boundary')
    if a['physical_collapse_law_derived'] or a['physical_entropy_production_derived'] or a['smaller_quantum_carrier_derived']:raise AssertionError('unsupported claim')


@lru_cache(None)
def audit() -> dict:
    verify_baseline();prediction=prediction_control();spectrum_error=kraus_error=0.
    for lam,t in ((1,1),(1,0),(.5,0),(.75,.5),(.2,.8),(.5001,0)):
        numerical=np.linalg.eigvalsh(choi_from_action(lambda a:linear_map(a,lam,t)))
        spectrum_error=max(spectrum_error,float(np.max(abs(numerical-np.sort(pauli_weights(lam,t))))))
        if pauli_weights(lam,t).min()>=-CP_TOL:
            kraus_error=max(kraus_error,float(np.linalg.norm(from_kraus(fixture(),channel_kraus(lam,t))-linear_map(fixture(),lam,t))))
    twins=parity_twins();p=paulis()[labels().index('XIII')]
    visible=((np.eye(D)+p)/D,(np.eye(D)-p)/D)
    boundary=channel_kraus(.5,0)
    certificates=[twirl_certificate(channel_kraus((1+t)/2,t)) for t in (0.,.25,.5,.75,1.)]
    certificates+=[twirl_certificate(amplitude_damping_kraus(.37)),twirl_certificate([frozen_motions()[0]])]
    result={'version':'v15.20','status':'EXECUTED_CONDITIONAL_CPTP_PREDICTOR_WITH_READOUT_COST',
        'baseline':baseline_control(),'rigidity':rigidity_control(),
        'family':'Phi_(lambda,t)(rho)=lambda*rho+(1-lambda)*Tr(rho)*I/16+(t-lambda)*Tr(Gamma*rho)*Gamma/16',
        'cp_region_in_unit_square':'lambda <= (1+t)/2',
        'raw_projection':{'lambda':1.,'t':0.,'min_state_eigenvalue':float(np.linalg.eigvalsh(linear_map(y_product_state(),1,0)).min()),
                          'min_normalized_choi_eigenvalue':float(pauli_weights(1,0).min()),'negative_choi_directions':127},
        'boundary_channel':{'lambda':.5,'t':0.,'kraus_count':len(boundary),
            'min_choi_eigenvalue':float(np.linalg.eigvalsh(choi_from_action(lambda a:linear_map(a,.5,0))).min()),
            'tp_error':float(np.linalg.norm(sum(k.conj().T@k for k in boundary)-np.eye(D))),
            'parity_twin_output_distance':distance(*(apply_channel(r,.5,0) for r in twins)),
            'visible_pair_output_distance':distance(*(apply_channel(r,.5,0) for r in visible)),
            'readout_gain':2.,'output_hilbert_dimension':16,'linear_image_dimension':255,
            'normalized_output_coordinate_dimension':254,
            'not_idempotent':True,'direct_probability_error_for_balanced_pauli_effect':.25},
        'minimax':{'objective':'max over visible Pauli P of operator_norm(Phi*(P)-P)',
            'parity_coefficient':'t=Tr(Gamma*Phi(Gamma))/16',
            'bound':'delta >= (1-t)/2; tight in the displayed family',
            'exact_parity_erasure_bound':.5,'commuting_visible_paulis':126,
            'scope':'All CPTP maps on the same M16 carrier; t=0 follows if Phi(Gamma)=0. No bound on arbitrary re-encoded observables or classical estimation gain.'},
        'twirl_certificates':certificates,'prediction':prediction,
        'readout_variance_examples':[readout_variance(0,.5),readout_variance(1,.5)],
        'max_kraus_formula_error':kraus_error,'max_choi_spectrum_error':spectrum_error,
        'max_decoded_prediction_error':prediction['max_decoded_error'],
        'max_channel_motion_covariance_error':prediction['max_channel_motion_covariance_error'],
        'max_twirl_formula_error':max(x['max_diagonal_transfer_error'] for x in certificates),
        'actual_record_selected':None,'physical_duration':None,'new_physical_axioms':[],
        'physical_collapse_law_derived':False,'physical_entropy_production_derived':False,
        'smaller_quantum_carrier_derived':False,'Pillar_3':'OPEN','scientific_breakthrough':False,
        'scope':'Explicit diagnostic noisy CPTP representation on the same carrier. Direct predictions attenuate; ensemble readout can be rescaled. This is not a common CPTP inverse, a physical pruning selector, or a clock.'}
    verify_result(result);return result


def main() -> None:
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--out',type=Path,default=ROOT/'outputs')
    args=parser.parse_args();a=audit();args.out.mkdir(parents=True,exist_ok=True)
    (args.out/'verification.json').write_text(json.dumps(a,indent=2,allow_nan=False)+'\n')
    np.savez_compressed(args.out/'channel_witnesses.npz',gamma=gamma(),kraus=channel_kraus(.5,0),
        fixture=fixture(),encoded_fixture=apply_channel(fixture(),.5,0),
        raw_choi=choi_from_action(lambda a:linear_map(a,1,0)),boundary_choi=choi_from_action(lambda a:linear_map(a,.5,0)))
    print(json.dumps(a,indent=2,allow_nan=False))

if __name__=='__main__':main()
