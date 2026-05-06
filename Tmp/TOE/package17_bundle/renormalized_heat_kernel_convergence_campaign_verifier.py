
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

def raw_coeff(kind,n,seed,k=10):
    P=pts(kind,n,seed); L,h=lap(kind,P,k=k)
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

def run(ns=(60,90,120,180,240),reps=4):
    rows=[]
    for n in ns:
        flat=[]; sph=[]; fcvs=[]; scvs=[]; hs=[]
        for r in range(reps):
            f,fcv,h=raw_coeff("flat_torus",n,20000+n*11+r)
            s,scv,h2=raw_coeff("sphere",n,21000+n*11+r)
            flat.append(f); sph.append(s); fcvs.append(fcv); scvs.append(scv); hs.append((h+h2)/2)
        baseline=float(np.median(flat))
        flat_res=np.array(flat)-baseline
        sph_res=np.array(sph)-baseline
        sep=abs(np.median(sph_res))/(np.std(sph_res)+np.std(flat_res)+1e-12)
        rows.append((n,float(np.median(hs)),baseline,float(np.median(sph)),float(np.median(sph_res)),float(np.std(sph_res)),float(np.std(flat_res)),float(np.median(fcvs)),float(np.median(scvs)),float(sep)))
    return rows

def trend_slope(xs,ys):
    xs=np.asarray(xs,float); ys=np.asarray(ys,float)
    return float(np.polyfit(np.log(xs), np.log(np.abs(ys)+1e-12), 1)[0])

def main():
    print("Renormalized heat-kernel convergence campaign verifier")
    print("="*50)
    print("Route:")
    print("fixed flat-baseline residual heat coefficient across refinement ladder")
    print("No per-geometry calibration.")
    print()
    rows=run()
    print("n,h_median,flat_baseline_raw,sphere_raw_median,sphere_residual_median,sphere_residual_std,flat_residual_std,flat_window_cv,sphere_window_cv,residual_separation_z")
    for row in rows:
        print(",".join(str(x) for x in row))
    residuals=[r[4] for r in rows]; seps=[r[9] for r in rows]; hs=[r[1] for r in rows]
    pos=all(x>0 for x in residuals)
    cv_ok=all(r[7]<0.75 and r[8]<0.75 for r in rows)
    sep_last=seps[-1]; sep_first=seps[0]
    slope=trend_slope(hs,residuals)
    print(f"positive_residual_all_refinements: {pos}")
    print(f"window_cv_ok_all: {cv_ok}")
    print(f"separation_ratio_last_vs_first: {sep_last/(sep_first+1e-12)}")
    print(f"residual_vs_h_log_slope: {slope}")
    cls="CONVERGENCE_CAMPAIGN_PROMISING" if pos and cv_ok and sep_last>0.5 else "CONVERGENCE_CAMPAIGN_WEAK"
    print(f"classification: {cls}")

if __name__=="__main__":
    main()
