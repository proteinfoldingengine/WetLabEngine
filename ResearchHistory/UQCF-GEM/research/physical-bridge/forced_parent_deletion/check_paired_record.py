"""Two fixed record labels, three probe orders, and the encoded-copy control."""
import itertools
import json
import math
from pathlib import Path
import sys

import numpy as np

ROOT = Path(__file__).resolve()
DEMOS = next(p for p in ROOT.parents if (p / "demos/v15.16-partial-pruning").is_dir()) / "demos"
sys.path.insert(0,str(DEMOS / "v13.27-gravity-progress"))
from uqcf_demo import linalg, quantum
sys.path.insert(0,str(DEMOS / "v15.16-partial-pruning"))
import recoverability as records

I, X, _, Z = linalg.paulis()
ZA = linalg.embed_local(Z,0,4)
ZB = linalg.embed_local(Z,2,4)
XX = linalg.embed_pair(X,0,X,2,4)
ZZ = ZA @ ZB
UNIT = np.eye(16)
H = 0.0001

def checked(a,b,tol=2e-9):
    if not np.allclose(a,b,rtol=0,atol=tol):
        raise ValueError("numerical check failed: "+str(np.max(np.abs(np.asarray(a)-b))))

def read(r):
    return np.trace(ZB @ r).real

def tilt(r,h):
    return quantum.state_from_logtilt(linalg.hermitian_log(r),h,ZA)

def filt(r,h):
    # Scalar rescaling makes the diagonal operator a valid selected filter.
    d=np.exp((h*np.diag(ZA).real-abs(h))/2)
    y=(d[:,None]*r)*d[None,:]
    return y/np.trace(y).real

def derivatives(fn):
    return (fn(H)-fn(-H))/(2*H)

def rounded(x):
    return round(float(x),9) or 0.0

def audit(x,z,schedule):
    f=records.basis(schedule)
    v=records.encoding(schedule)
    r=((UNIT+x*XX)@(UNIT+z*ZZ))/16
    inp=f.conj().T@r@f
    pin=lambda u,mask="1000": f@records.reduce_input(f.conj().T@u@f,mask,schedule)@f.conj().T
    fixed=pin(r)
    expected_eig=sorted((1+u*x)*(1+w*z)/16 for u,w in itertools.product((-1,1),repeat=2) for _ in range(4))
    checked(np.linalg.eigvalsh(r),expected_eig)
    checked(fixed,(UNIT+z*ZZ)/16)
    for mask in ("0000","0100","0001"):
        checked(pin(r,mask),r)
    for observable in (ZA,ZB,ZZ):
        checked(pin(observable),observable)
    for site in (0,2):
        for state in (r,fixed):
            checked(linalg.partial_trace(state,[site],[2]*4),I/2)
    k=x/math.atanh(x) if x else 1.0
    target=z*k
    pre=quantum.bkm_covariance(r,[ZA,ZB])
    post=quantum.bkm_covariance(fixed,[ZA,ZB])
    checked(pre,k*np.array([[1,z],[z,1]]))
    checked(post,np.array([[1,z],[z,1]]))
    ordinary=float(np.trace(r @ ZZ).real)
    checked(ordinary,z)
    checked(np.diag(r),np.diag(fixed))
    before=lambda h: read(pin(tilt(r,h)))
    after=lambda h: read(tilt(fixed,h))
    for h in (-0.2,0.2):
        radius=math.hypot(math.atanh(x),h)
        checked(before(h),z*h*math.tanh(radius)/radius)
        checked(after(h),z*math.tanh(h))
        for state in (r,fixed):
            checked(read(filt(state,h)),z*math.tanh(h))
    checked(derivatives(before),target,1e-8)
    checked(derivatives(after),z,1e-8)
    # Trace the actual two output copies of the completed sharp encoding.
    joint=v@inp@v.conj().T
    joint_post=records.pinch_joint(joint,"1000")
    for copy in (0,1):
        marginal=linalg.partial_trace(joint,[copy],[16,16])
        marginal_post=linalg.partial_trace(joint_post,[copy],[16,16])
        checked(marginal,np.diag(np.diag(r)))
        checked(marginal_post,marginal)
        checked(quantum.bkm_covariance(marginal,[ZA,ZB])[0,1],z)
    return {"x":x,"z":z,"schedule":schedule,"logtilt_before_pinch":rounded(pre[0,1]),
            "logtilt_after_pinch":rounded(post[0,1]),"after_minus_before":rounded(post[0,1]-pre[0,1]),
            "conditional_local_filter_both":rounded(z),"bare_B_mean_both":0,
            "encoded_copy_cross_response_both":rounded(z)}

def main():
    records.verify_baseline()
    cases=[(.6,.5),(-.6,.5),(.6,-.5),(0.,.5),(.6,0.)]
    rows=[audit(x,z,s) for x,z in cases for s in range(5)]
    print(json.dumps({"basis":"record A1 (first) and B1 (third), Pauli signs +/-1",
                      "source_mask":"1000","rows":rows},indent=2,sort_keys=True))

if __name__=="__main__":
    main()
