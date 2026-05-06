
from __future__ import annotations
import numpy as np

def points(kind,n,seed):
    rng=np.random.default_rng(seed)
    if kind=="flat_torus":
        u=rng.uniform(0,2*np.pi,n); v=rng.uniform(0,2*np.pi,n)
        coords=np.c_[u,v]
        return coords
    if kind=="sphere":
        X=rng.normal(size=(n,3)); X/=np.linalg.norm(X,axis=1,keepdims=True)
        return X
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
    D=dist(kind,P)
    np.fill_diagonal(D,np.inf)
    n=len(P)
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
    P=points(kind,n,seed)
    L,h=lap(kind,P)
    ev=np.maximum(np.linalg.eigvalsh(L),0)
    windows=[np.array([0.7,1.0,1.4,2.0]),np.array([1.0,1.4,2.0,2.8]),np.array([1.4,2.0,2.8,4.0])]
    vals=[]
    for c in windows:
        t=c*h*h
        H=np.array([np.sum(np.exp(-tt*ev)) for tt in t])
        Y=H*((4*np.pi*t)**1) # d=2
        m,b=np.polyfit(t,Y,1)
        vals.append(6*m)
    vals=np.array(vals)
    return float(np.median(vals)), float(np.std(vals)/(abs(np.mean(vals))+1e-12)), float(h)

def run(n=120,reps=3):
    rows=[]
    for kind in ["flat_torus","sphere"]:
        vals=[]; cvs=[]; hs=[]
        for r in range(reps):
            v,cv,h=coeff(kind,n,12000+r+len(kind)*23)
            vals.append(v); cvs.append(cv); hs.append(h)
        rows.append((kind,float(np.median(vals)),float(np.std(vals)),float(np.median(cvs)),float(np.median(hs))))
    tor=rows[0][1]; sph=rows[1][1]
    ordering=sph>tor
    sep=abs(sph-tor)/(abs(sph)+abs(tor)+1e-12)
    stable=rows[0][3]<0.75 and rows[1][3]<0.75
    return rows,ordering,sep,stable

def main():
    print("Boundary-free heat-kernel tests verifier")
    print("="*50)
    print("Route:")
    print("intrinsic distances on flat torus and sphere -> heat coefficient plateau test")
    print("No per-geometry calibration.")
    print()
    rows,ordering,sep,stable=run()
    print("geometry,intR_coeff_median,intR_coeff_std,window_plateau_cv_median,h_median")
    for row in rows:
        print(",".join(str(x) for x in row))
    print(f"sphere_greater_than_flat_torus: {ordering}")
    print(f"separation_score: {sep}")
    print(f"plateau_stable: {stable}")
    cls="BOUNDARY_FREE_PROMISING" if ordering and sep>0.1 and stable else "BOUNDARY_FREE_WEAK"
    print(f"classification: {cls}")
if __name__=="__main__":
    main()
