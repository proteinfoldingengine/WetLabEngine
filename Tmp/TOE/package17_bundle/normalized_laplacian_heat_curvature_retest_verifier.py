
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
    return np.arccos(np.clip(P@P.T,-1,1))

def operator(kind,P,k=12,alpha=1.0):
    D=dist(kind,P); np.fill_diagonal(D,np.inf); n=len(P)
    nbr=np.argsort(D,axis=1)[:,:k]
    h=np.median([D[i,j] for i in range(n) for j in nbr[i]])
    eps=h*h
    K=np.zeros((n,n))
    for i in range(n):
        for j in nbr[i]:
            w=np.exp(-D[i,j]**2/(4*eps+1e-12))
            K[i,j]=max(K[i,j],w); K[j,i]=max(K[j,i],w)
    q=np.sum(K,axis=1)+1e-12
    Ka=K/(q[:,None]**alpha*q[None,:]**alpha)
    d=np.sum(Ka,axis=1)+1e-12
    inv=np.where(d>1e-12,1/np.sqrt(d),0)
    S=inv[:,None]*Ka*inv[None,:]
    L=(np.eye(n)-S)/(eps+1e-12)
    return L,h

def raw_coeff_from_evals(evals,h,scale=1.0):
    # If L_raw ~= c Δ, then scale L by 1/c. Here scale multiplies eigenvalues.
    ev=np.maximum(evals*scale,0)
    windows=[np.array([0.7,1.0,1.4,2.0]),np.array([1.0,1.4,2.0,2.8]),np.array([1.4,2.0,2.8,4.0])]
    vals=[]
    for c in windows:
        t=c*h*h
        H=np.array([np.sum(np.exp(-tt*ev)) for tt in t])
        Y=H*((4*np.pi*t)**1)
        m,b=np.polyfit(t,Y,1)
        vals.append(6*m)
    vals=np.array(vals)
    return float(np.median(vals)), float(np.std(vals)/(abs(np.mean(vals))+1e-12))

def compute(kind,n,seed,scale=1.0):
    P=pts(kind,n,seed); L,h=operator(kind,P,alpha=1.0)
    ev=np.linalg.eigvalsh(L)
    coeff,cv=raw_coeff_from_evals(ev,h,scale)
    lam1=float(np.maximum(ev[1],0))
    return coeff,cv,h,lam1

def run(n=180,reps=6):
    # Universal spectral scale from flat torus lambda1 target=1.
    flat_lams=[]
    for r in range(reps):
        _,_,_,lam=compute("flat_torus",n,40000+r,scale=1.0)
        flat_lams.append(lam)
    median_lam=float(np.median(flat_lams))
    scale=1.0/(median_lam+1e-12)
    rows=[]
    coeffs={}
    for kind in ["flat_torus","sphere"]:
        raw=[]; scaled=[]; cvs=[]; lams=[]; hs=[]
        for r in range(reps):
            c,cv,h,lam=compute(kind,n,41000+r+len(kind)*31,scale=1.0)
            cs,cvs2,h2,lam2=compute(kind,n,42000+r+len(kind)*31,scale=scale)
            raw.append(c); scaled.append(cs); cvs.append(cvs2); lams.append(lam); hs.append(h)
        rows.append((kind,float(np.median(raw)),float(np.median(scaled)),float(np.std(scaled)),float(np.median(cvs)),float(np.median(lams)),float(np.median(hs))))
        coeffs[kind]=np.array(scaled)
    baseline=float(np.median(coeffs["flat_torus"]))
    flat_res=coeffs["flat_torus"]-baseline
    sph_res=coeffs["sphere"]-baseline
    out={
        "flat_lambda1_scale_factor":scale,
        "flat_scaled_residual_median":float(np.median(flat_res)),
        "sphere_scaled_residual_median":float(np.median(sph_res)),
        "sphere_residual_positive":bool(np.median(sph_res)>0),
        "residual_separation_z":float(abs(np.median(sph_res))/(np.std(sph_res)+np.std(flat_res)+1e-12)),
        "rows":rows
    }
    return out

def main():
    print("Normalized Laplacian heat curvature retest verifier")
    print("="*50)
    print("Route:")
    print("alpha=1 diffusion normalization + universal flat-torus lambda1 scale -> heat coefficient residual")
    print("No per-geometry calibration.")
    print()
    out=run()
    print(f"flat_lambda1_scale_factor: {out['flat_lambda1_scale_factor']}")
    print("geometry,raw_coeff_median,scaled_coeff_median,scaled_coeff_std,scaled_window_cv,raw_lambda1_median,h_median")
    for row in out["rows"]:
        print(",".join(str(x) for x in row))
    print(f"flat_scaled_residual_median: {out['flat_scaled_residual_median']}")
    print(f"sphere_scaled_residual_median: {out['sphere_scaled_residual_median']}")
    print(f"sphere_residual_positive: {out['sphere_residual_positive']}")
    print(f"residual_separation_z: {out['residual_separation_z']}")
    cls="NORMALIZED_HEAT_RETEST_PROMISING" if out["sphere_residual_positive"] and out["residual_separation_z"]>1 else "NORMALIZED_HEAT_RETEST_WEAK"
    print(f"classification: {cls}")

if __name__=="__main__":
    main()
