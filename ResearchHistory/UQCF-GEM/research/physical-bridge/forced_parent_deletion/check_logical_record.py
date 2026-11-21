"""Reproduce logical and physical-copy controls with the two pinned original modules."""
import argparse
import hashlib
import json
from pathlib import Path
import sys
import numpy as np

PIN = {
    "ResearchHistory/UQCF-GEM/demos/v15.16-partial-pruning/recoverability.py": "0a01d2eea4f0114b119fbb7beaf4619775c0f9f6",
    "ResearchHistory/UQCF-GEM/demos/v15.16-partial-pruning/baseline/baseline/adaptive.py": "44a87e4cc5bcf531ef7798aadab5d9dbba3482cb",
    "ResearchHistory/UQCF-GEM/demos/v15.16-partial-pruning/baseline/baseline/vendor/__init__.py": "e69de29bb2d1d6434b8b29ae775ad8c2e48c5391",
    "ResearchHistory/UQCF-GEM/demos/v15.16-partial-pruning/baseline/baseline/vendor/v1513.py": "95d0303d617422d74e61ae017f0354233ec9454b",
    "ResearchHistory/UQCF-GEM/demos/v15.16-partial-pruning/baseline/coherent_records.py": "fdf5367b11729fc1e2bfccd8d8daa2a0c7209049",
    "ResearchHistory/UQCF-GEM/demos/v13.27-gravity-progress/uqcf_demo/__init__.py": "6711ad416e7b37cefe0c4fe28dc3a3f8b7add690",
    "ResearchHistory/UQCF-GEM/demos/v13.27-gravity-progress/uqcf_demo/quantum.py": "bf0b84e3b3e627d7916a5fb1b46ab9bd5eba03e6",
    "ResearchHistory/UQCF-GEM/demos/v13.27-gravity-progress/uqcf_demo/linalg.py": "28bdab47d7fc237beb96f7ed7dcc63bd707a652b"
}

def checked_sources(root):
    for path, target in PIN.items():
        data = (root/path).read_bytes()
        found = hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()
        if found != target:
            raise ValueError("Source pin mismatch: " + path)
    demos = root/"ResearchHistory/UQCF-GEM/demos"
    sys.path.insert(0, str(demos/"v15.16-partial-pruning"))
    import recoverability as prune
    sys.path.insert(0, str(demos/"v13.27-gravity-progress"))
    from uqcf_demo import quantum as qm
    return prune, qm

def close(a, b, tol=3e-10):
    if not np.allclose(a, b, atol=tol, rtol=0):
        raise AssertionError((a,b))

def one_logical(prune,qm,rho_input,f,bit):
    encoded_coords=f @ rho_input @ f.conj().T
    return qm.partial_trace(encoded_coords,[bit],[2]*4)

def moment(a, obs):
    return np.trace(a@obs).real

def susceptibility(qm, a, Z):
    if np.linalg.eigvalsh(a).min() <= 1.e-12:
        raise ValueError("Faithful state required")
    return float(qm.bkm_covariance(a,[Z])[0,0])

def physical_copies(prune,qm,rho,mask,schedule=0):
    v=prune.encoding(schedule); c=v@rho@v.conj().T
    after=prune.pinch_joint(c,mask)
    close(v.conj().T@after@v,prune.reduce_input(rho,mask,schedule))
    for axis in (0,1):
        marg=qm.partial_trace(c,[axis],[16,16])
        post=qm.partial_trace(after,[axis],[16,16])
        close(marg,post)
        # Both copies carry the same record distribution and no coherences.
        close(marg,np.diag(np.diag(marg)))
    return True

def qnum(v):
    # Stable scientific serialization, retaining far more than the validated effect.
    return round(float(v), 9) or 0.0

def controls(prune,qm,x,schedule):
    ident,X,_,Z=qm.paulis();f=prune.basis(schedule)
    logical=(ident+x*X)/2
    rho=f.conj().T@np.kron(logical,np.eye(8)/8)@f
    generator=f.conj().T@np.kron(Z,np.eye(8))@f
    close(prune.reduce_input(generator,"1000",schedule),generator)
    close(prune.reduce_input(rho,"0000",schedule),rho)
    close(prune.reduce_input(rho,"0001",schedule),rho)
    nulled=prune.reduce_input(rho,"1000",schedule)
    pre=one_logical(prune,qm,rho,f,0)
    post=one_logical(prune,qm,nulled,f,0)
    close(pre,logical);close(post,ident/2)
    close(moment(pre,Z),moment(post,Z));close(moment(pre,Z@Z),moment(post,Z@Z))
    k0=susceptibility(qm,pre,Z);k1=susceptibility(qm,post,Z)
    exact=(x/np.arctanh(x) if x else 1.)
    close(k0,exact);close(k1,1.)
    # Noncommuting order of a fresh exponential preparation and the pinching.
    # Compare equal dimensionless amplitudes and the very same expectation.
    step=1.e-4
    def drive(t,first_tilt):
        base=rho if first_tilt else nulled
        new=qm.state_from_logtilt(qm.hermitian_log(base),t,generator)
        if first_tilt:
            new=prune.reduce_input(new,"1000",schedule)
        return moment(new,generator)
    finite={}
    for first_tilt,expected in [(True,exact),(False,1.)]:
        slope=(drive(step,first_tilt)-drive(-step,first_tilt))/(2*step)
        close(slope,expected,2.e-8)
        finite["tilt_then_pinch" if first_tilt else "pinch_then_tilt"]=qnum(slope)
    assert physical_copies(prune,qm,rho,"1000",schedule)
    return {"schedule":schedule,"x":x,"chi_before":qnum(k0),"chi_after":qnum(k1),"difference":qnum(k1-k0),
            "same_undriven_expectation_and_variance":True,
            "central_slopes":finite,"record_and_system_copies_fixed":True}

def default_fixture(prune,qm):
    # The historical audit actually calls reduce_input on this input at every
    # (schedule, mask). Here add a diagnostic on its four logical record factors.
    rho=prune.fixture()
    _,_,_,Z=qm.paulis()
    inputs=np.linalg.eigvalsh(rho)
    rows=[]
    for schedule in range(5):
        f=prune.basis(schedule)
        pre=[one_logical(prune,qm,rho,f,b) for b in range(4)]
        if any(np.linalg.eigvalsh(x).min()<=1.e-12 for x in pre):
            raise ValueError("nonfaithful default one-record reduction; cannot apply BKM directly")
        for mask in prune.masks():
            e=prune.reduce_input(rho,mask,schedule)
            changes=[]
            for bit in range(4):
                post=one_logical(prune,qm,e,f,bit)
                pred=np.diag(np.diag(pre[bit])) if mask[bit]=="1" else pre[bit]
                close(post,pred)
                close(moment(post,Z),moment(pre[bit],Z))
                d=susceptibility(qm,post,Z)-susceptibility(qm,pre[bit],Z)
                if mask[bit]=="0":
                    close(d,0.)
                changes.append(qnum(d))
            rows.append({"schedule":schedule,"mask":mask,"chi_differences":changes})
    assert physical_copies(prune,qm,rho,"1000")
    d=[z for row in rows for z in row["chi_differences"]]
    return {"fixture_input_min_eigenvalue":qnum(inputs[0]),"schedules":5,"masks_per_schedule":16,
            "record_probes":len(d),"nonzero_after_rounding":sum(z!=0 for z in d),
            "min_difference":min(d),"max_difference":max(d),"rows":rows}

def main():
    default=next((p for p in Path(__file__).resolve().parents if (p/"ResearchHistory/UQCF-GEM/demos").is_dir()),Path.cwd())
    parser=argparse.ArgumentParser();parser.add_argument("--repo",type=Path,default=default)
    args=parser.parse_args()
    prune,qm=checked_sources(args.repo)
    report={"contract":"faithful logical record reductions; Z eigenvalues +/-1; fresh log tilt",
            "analytic_cases":[controls(prune,qm,x,s) for x in (0.,0.6,-0.6) for s in range(5)],
            "default":default_fixture(prune,qm)}
    print(json.dumps(report,indent=2,sort_keys=True))
if __name__=="__main__":
    main()
