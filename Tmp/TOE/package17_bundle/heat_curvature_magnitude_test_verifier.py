
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

def operator(kind,P,k=10,alpha=1.0):
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

def coeff_from_evals(ev,h,scale):
    ev=np.maximum(ev*scale,0)
    windows=[np.array([0.8,1.1,1.5,2.0]), np.array([1.1,1.5,2.0,2.7])]
    vals=[]
    for c in windows:
        t=c*h*h
        H=np.array([np.sum(np.exp(-tt*ev)) for tt in t])
        Y=H*((4*np.pi*t)**1)
        m,b=np.polyfit(t,Y,1)
        vals.append(6*m)
    return float(np.median(vals)), float(np.std(vals)/(abs(np.mean(vals))+1e-12))

def raw(kind,n,seed):
    P=pts(kind,n,seed); L,h=operator(kind,P)
    ev=np.linalg.eigvalsh(L)
    return ev,h,float(max(ev[1],0))

def run(ns=(70,110,160),reps=4):
    target=8*np.pi
    rows=[]
    for n in ns:
        # Scale from flat torus lambda1, baseline from flat torus raw heat coefficient
        lam=[]; flat_coeff=[]; sphere_coeff=[]; fcv=[]; scv=[]
        for r in range(reps):
            ev,h,l1=raw("flat_torus",n,80000+n*17+r)
            lam.append(l1)
        scale=1/(np.median(lam)+1e-12)
        for r in range(reps):
            evf,hf,l1f=raw("flat_torus",n,81000+n*17+r)
            cf,cvf=coeff_from_evals(evf,hf,scale)
            evs,hs,l1s=raw("sphere",n,82000+n*17+r)
            cs,cvs=coeff_from_evals(evs,hs,scale)
            flat_coeff.append(cf); sphere_coeff.append(cs); fcv.append(cvf); scv.append(cvs)
        baseline=float(np.median(flat_coeff))
        residuals=np.array(sphere_coeff)-baseline
        med=float(np.median(residuals))
        rel_err=abs(med-target)/target
        rows.append((n,scale,baseline,med,float(np.std(residuals)),rel_err,float(np.median(fcv)),float(np.median(scv))))
    return rows

def main():
    print("Heat curvature magnitude test verifier")
    print("="*50)
    print("Route:")
    print("renormalized sphere coefficient -> compare to continuum target 8*pi")
    print("No per-sphere magnitude fit.")
    print()
    rows=run()
    print("n,flat_lambda1_scale,flat_baseline,sphere_residual_median,sphere_residual_std,relative_error_to_8pi,flat_window_cv,sphere_window_cv")
    for row in rows:
        print(",".join(str(x) for x in row))
    errs=[r[5] for r in rows]
    residuals=[r[3] for r in rows]
    positive=all(x>0 for x in residuals)
    trend_improves=errs[-1] < errs[0]
    final_reasonable=errs[-1] < 0.75
    print(f"positive_all: {positive}")
    print(f"relative_error_improves: {trend_improves}")
    print(f"final_relative_error_lt_0p75: {final_reasonable}")
    print(f"classification: {'MAGNITUDE_TEST_PROMISING' if positive and trend_improves and final_reasonable else 'MAGNITUDE_TEST_WEAK'}")

if __name__=="__main__":
    main()
