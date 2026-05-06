
from __future__ import annotations
import numpy as np

def make_points(kind,n,seed):
    rng=np.random.default_rng(seed)
    if kind=="plane":
        xy=rng.uniform(-1,1,(n,2)); X=np.c_[xy,np.zeros(n)]
    elif kind=="sphere":
        X=rng.normal(size=(n,3)); X/=np.linalg.norm(X,axis=1,keepdims=True)
    elif kind=="saddle":
        xy=rng.uniform(-1,1,(n,2)); X=np.c_[xy,0.55*(xy[:,0]**2-xy[:,1]**2)]
    elif kind=="perturbed_sphere":
        X=rng.normal(size=(n,3)); X/=np.linalg.norm(X,axis=1,keepdims=True)
        theta=np.arctan2(X[:,1],X[:,0]); r=1+0.12*np.sin(4*theta)*(X[:,2]**2)
        X=X*r[:,None]
    else:
        raise ValueError(kind)
    return X

def unnormalized_laplacian(X,k=12):
    n=len(X)
    D=np.linalg.norm(X[:,None,:]-X[None,:,:],axis=-1)
    np.fill_diagonal(D,np.inf)
    nbr=np.argsort(D,axis=1)[:,:k]
    h=np.median([D[i,j] for i in range(n) for j in nbr[i]])
    W=np.zeros((n,n))
    for i in range(n):
        for j in nbr[i]:
            w=np.exp(-D[i,j]**2/(2*h*h+1e-12))
            W[i,j]=max(W[i,j],w); W[j,i]=max(W[j,i],w)
    Deg=np.diag(np.sum(W,axis=1))
    L=(Deg-W)/(h*h+1e-12)  # scale by h^-2 to mimic continuum Laplacian
    return L,h

def heat_coeff_feature(X,d=2,k=12):
    L,h=unnormalized_laplacian(X,k)
    evals=np.maximum(np.linalg.eigvalsh(L),0)
    # fixed scale window tied to h^2 in continuum units: t = c*h^2, but L already h^-2,
    # so effective dimensionless c works here.
    cgrid=np.array([0.35,0.5,0.7,1.0,1.4,2.0])
    tgrid=cgrid*(h*h)
    H=np.array([np.sum(np.exp(-t*evals)) for t in tgrid])
    Y=H*((4*np.pi*tgrid)**(d/2))
    # Fit Y ≈ A0 + A1*t over fixed window. A1 ~ (1/6)∫R dV.
    coef=np.polyfit(tgrid,Y,1)
    A1=float(coef[0]); A0=float(coef[1])
    intR_est=6*A1
    return intR_est,A0,h

def run(n=180,reps=6,seed=2701):
    kinds=["plane","sphere","saddle","perturbed_sphere"]
    rows=[]
    for kind in kinds:
        vals=[]; a0s=[]; hs=[]
        for r in range(reps):
            X=make_points(kind,n,seed+100*len(kind)+r)
            val,a0,h=heat_coeff_feature(X)
            vals.append(val); a0s.append(a0); hs.append(h)
        rows.append((kind,float(np.median(vals)),float(np.std(vals)),float(np.median(a0s)),float(np.median(hs))))
    # classification: expected plane near lower than sphere; saddle should differ. No sign guarantee yet due embedded patch/boundary.
    med={k:v for k,v,_,_,_ in rows}
    sep_sp=abs(med["sphere"]-med["plane"])/(abs(med["sphere"])+abs(med["plane"])+1e-12)
    sep_sa=abs(med["saddle"]-med["plane"])/(abs(med["saddle"])+abs(med["plane"])+1e-12)
    # require nontrivial separation and lower relative variance
    return rows,sep_sp,sep_sa

def main():
    print("Heat trace coefficient estimator verifier")
    print("="*50)
    print("Route:")
    print("scaled unnormalized graph Laplacian -> fixed h^2 heat window -> coefficient of t")
    print("No per-geometry calibration. Diagnostic only.")
    print()
    rows,sep_sp,sep_sa=run()
    print("kind,intR_coeff_median,intR_coeff_std,A0_median,h_median")
    for row in rows:
        print(",".join(str(x) for x in row))
    print(f"separation_sphere_plane_coeff: {sep_sp}")
    print(f"separation_saddle_plane_coeff: {sep_sa}")
    cls="COEFFICIENT_DIAGNOSTIC_PROMISING" if sep_sp>0.05 and sep_sa>0.05 else "COEFFICIENT_DIAGNOSTIC_WEAK"
    print(f"classification: {cls}")

if __name__=="__main__":
    main()
