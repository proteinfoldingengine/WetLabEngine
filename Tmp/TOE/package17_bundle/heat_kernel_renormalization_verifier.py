
from __future__ import annotations
import numpy as np

def pts(kind,n,seed):
    rng=np.random.default_rng(seed)
    if kind=="flat_torus":
        u=rng.uniform(0,2*np.pi,n); v=rng.uniform(0,2*np.pi,n)
        return np.c_[u,v]
    if kind=="sphere":
        X=rng.normal(size=(n,3)); X/=np.linalg.norm(X,axis=1,keepdims=True); return X
    raise ValueError(kind)

def dist(kind,P):
    if kind=="flat_torus":
        u=P[:,0]; v=P[:,1]
        du=np.abs(u[:,None]-u[None,:]); du=np.minimum(du,2*np.pi-du)
        dv=np.abs(v[:,None]-v[None,:]); dv=np.minimum(dv,2*np.pi-dv)
        return np.sqrt(du*du+dv*dv)
    dot=np.clip(P@P.T,-1,1)
    return np.arccos(dot)

def lap(kind,P,k=10):
    D=dist(kind,P); np.fill_diagonal(D,np.inf); n=len(P)
    nbr=np.argsort(D,axis=1)[:,:k]
    h=np.median([D[i,j] for i in range(n) for j in nbr[i]])
    W=np.zeros((n,n))
    for i in range(n):
        for j in nbr[i]:
            w=np.exp(-D[i,j]**2/(4*h*h+1e-12))
            W[i,j]=max(W[i,j],w); W[j,i]=max(W[j,i],w)
    deg=np.sum(W,axis=1)
    inv=np.where(deg>1e-12,1/np.sqrt(deg),0)
    L=(np.eye(n)-inv[:,None]*W*inv[None,:])/(h*h+1e-12)
    return L,h

def coeff(kind,n,seed):
    P=pts(kind,n,seed); L,h=lap(kind,P)
    ev=np.maximum(np.linalg.eigvalsh(L),0)
    windows=[np.array([0.7,1.0,1.4,2.0]),np.array([1.0,1.4,2.0,2.8]),np.array([1.4,2.0,2.8,4.0])]
    vals=[]
    for c in windows:
        t=c*h*h
        H=np.array([np.sum(np.exp(-tt*ev)) for tt in t])
        Y=H*((4*np.pi*t)**1)
        m,b=np.polyfit(t,Y,1)
        vals.append(6*m)
    vals=np.array(vals)
    return float(np.median(vals)), float(np.std(vals)/(abs(np.mean(vals))+1e-12)), h

def run(n=120,reps=8):
    # Universal baseline: flat_torus median under same n,k,window rule.
    tor=[]; sph=[]; tor_cv=[]; sph_cv=[]
    for r in range(reps):
        v,cv,h=coeff("flat_torus",n,13000+r)
        tor.append(v); tor_cv.append(cv)
        v2,cv2,h2=coeff("sphere",n,14000+r)
        sph.append(v2); sph_cv.append(cv2)
    baseline=float(np.median(tor))
    tor_res=np.array(tor)-baseline
    sph_res=np.array(sph)-baseline
    out={
        "baseline_flat_torus_coeff": baseline,
        "flat_torus_raw_median": float(np.median(tor)),
        "sphere_raw_median": float(np.median(sph)),
        "flat_torus_residual_median": float(np.median(tor_res)),
        "sphere_residual_median": float(np.median(sph_res)),
        "flat_torus_residual_std": float(np.std(tor_res)),
        "sphere_residual_std": float(np.std(sph_res)),
        "flat_torus_window_cv_median": float(np.median(tor_cv)),
        "sphere_window_cv_median": float(np.median(sph_cv)),
    }
    # Expected residual sphere > 0 if sign convention matches + curvature.
    out["sphere_residual_positive"]=bool(out["sphere_residual_median"]>0)
    out["residual_separation_z"]=float(abs(out["sphere_residual_median"]-out["flat_torus_residual_median"])/(out["sphere_residual_std"]+out["flat_torus_residual_std"]+1e-12))
    out["classification"]="RENORMALIZED_PROMISING" if out["sphere_residual_positive"] and out["residual_separation_z"]>1 else "RENORMALIZED_WEAK"
    return out

def main():
    print("Heat kernel renormalization verifier")
    print("="*50)
    print("Route:")
    print("flat boundaryless baseline subtraction -> residual heat coefficient")
    print("No per-geometry calibration; one flat reference baseline.")
    print()
    for k,v in run().items():
        print(f"{k}: {v}")
if __name__=="__main__":
    main()
