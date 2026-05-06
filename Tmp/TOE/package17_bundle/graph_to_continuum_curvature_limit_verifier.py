
from __future__ import annotations
import numpy as np

def sphere_points(n, seed):
    rng=np.random.default_rng(seed)
    X=rng.normal(size=(n,3))
    X/=np.linalg.norm(X,axis=1,keepdims=True)
    return X

def knn_edges(X,k):
    n=len(X)
    D=np.linalg.norm(X[:,None,:]-X[None,:,:],axis=-1)
    np.fill_diagonal(D,np.inf)
    nbr=np.argsort(D,axis=1)[:,:k]
    return nbr

def curvature_signal(X,nbr):
    vals=[]; hs=[]
    for i in range(len(X)):
        Y=X[nbr[i]]-X[i]
        h=float(np.median(np.linalg.norm(Y,axis=1)))
        C=(Y.T@Y)/len(Y)
        eig=np.sort(np.linalg.eigvalsh(C))
        # normal variance / tangential variance scaled by h^-2
        sig=(eig[0]/(np.mean(eig[1:])+1e-12))/(h*h+1e-12)
        vals.append(sig); hs.append(h)
    return np.asarray(vals), float(np.median(hs))

def run_refinement(ns=(100,200,400,800),k=10,reps=4):
    raw=[]
    for n in ns:
        meds=[]; cvs=[]; hs=[]
        for r in range(reps):
            X=sphere_points(n,10000+n+r)
            nbr=knn_edges(X,k)
            sig,h=curvature_signal(X,nbr)
            meds.append(float(np.median(sig)))
            cvs.append(float(np.std(sig)/(np.mean(sig)+1e-12)))
            hs.append(h)
        raw.append((n,float(np.median(hs)),float(np.median(meds)),float(np.median(cvs))))
    # calibrate by largest n to R=2
    scale=2.0/raw[-1][2]
    out=[]
    for n,h,med,cv in raw:
        R=scale*med
        err=abs(R-2)/2
        out.append((n,h,R,err,cv))
    return out

def main():
    print("Graph-to-continuum curvature limit verifier")
    print("="*50)
    print("Route:")
    print("unit sphere sampled graph -> curvature proxy -> refinement stability")
    print("Diagnostic only; not proof of continuum curvature convergence.")
    print()
    print("n,h_median,R_est_calibrated,relative_error,coefficient_of_variation")
    rows=run_refinement()
    for row in rows:
        print(",".join(f"{x:.10g}" if isinstance(x,float) else str(x) for x in row))
    cvs=[r[4] for r in rows]
    rels=[r[3] for r in rows]
    cls="REFINEMENT_STABLE_PROXY" if rels[-1]<0.05 and cvs[-1] < cvs[0] else "PROXY_NOT_STABLE"
    print(f"stability_class: {cls}")
    print(f"cv_improvement_factor: {cvs[0]/(cvs[-1]+1e-12):.6g}")

if __name__=="__main__":
    main()
