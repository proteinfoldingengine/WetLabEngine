
from __future__ import annotations
import numpy as np

def make_points(kind, n, seed):
    rng=np.random.default_rng(seed)
    if kind=="plane":
        xy=rng.uniform(-1,1,size=(n,2))
        X=np.c_[xy, np.zeros(n)]
    elif kind=="sphere":
        X=rng.normal(size=(n,3))
        X/=np.linalg.norm(X,axis=1,keepdims=True)
    elif kind=="saddle":
        xy=rng.uniform(-1,1,size=(n,2))
        z=0.55*(xy[:,0]**2-xy[:,1]**2)
        X=np.c_[xy,z]
    elif kind=="perturbed_sphere":
        X=rng.normal(size=(n,3))
        X/=np.linalg.norm(X,axis=1,keepdims=True)
        r=1+0.12*np.sin(4*np.arctan2(X[:,1],X[:,0]))*(X[:,2]**2)
        X=X*r[:,None]
    else:
        raise ValueError(kind)
    return X

def graph_laplacian(X,k=12):
    n=len(X)
    D=np.linalg.norm(X[:,None,:]-X[None,:,:],axis=-1)
    np.fill_diagonal(D,np.inf)
    nbr=np.argsort(D,axis=1)[:,:k]
    h=np.median([D[i,j] for i in range(n) for j in nbr[i]])
    W=np.zeros((n,n))
    for i in range(n):
        for j in nbr[i]:
            w=np.exp(-(D[i,j]**2)/(h*h+1e-12))
            W[i,j]=max(W[i,j],w)
            W[j,i]=max(W[j,i],w)
    deg=np.sum(W,axis=1)
    # symmetric normalized Laplacian
    inv=np.where(deg>1e-12,1/np.sqrt(deg),0)
    L=np.eye(n)- (inv[:,None]*W*inv[None,:])
    return L,h

def heat_features(X,k=12,t_grid=None):
    if t_grid is None:
        # fixed dimensionless time grid for normalized Laplacian; no per-geometry fit
        t_grid=np.array([0.25,0.5,1.0,2.0,4.0,8.0])
    L,h=graph_laplacian(X,k)
    evals=np.linalg.eigvalsh(L)
    traces=np.array([np.sum(np.exp(-t*evals)) for t in t_grid])
    # remove volume-like leading feature by normalizing trace by n
    norm_trace=traces/len(X)
    # curvature-like spectral feature: early-to-mid heat decay area and slope
    slope=np.polyfit(np.log(t_grid), np.log(norm_trace+1e-12), 1)[0]
    area=float(np.trapz(norm_trace, np.log(t_grid)))
    spectral_gap=float(np.sort(evals)[1]) if len(evals)>1 else np.nan
    return dict(slope=float(slope), area=area, gap=spectral_gap, h=float(h), traces=norm_trace)

def run(n=180, reps=8, seed=2601):
    kinds=["plane","sphere","saddle","perturbed_sphere"]
    rows=[]
    for kind in kinds:
        feats=[]
        for r in range(reps):
            X=make_points(kind,n,seed+r+100*len(kind))
            f=heat_features(X)
            feats.append(f)
        for key in ["slope","area","gap","h"]:
            vals=np.array([f[key] for f in feats],float)
            rows.append((kind,key,float(np.median(vals)),float(np.std(vals))))
    # simple fixed classification diagnostics:
    # We do not claim sign of R yet; test whether spectral signatures differ without calibration.
    area={k:np.median([row[2] for row in rows if row[0]==k and row[1]=="area"]) for k in kinds}
    slope={k:np.median([row[2] for row in rows if row[0]==k and row[1]=="slope"]) for k in kinds}
    sep_sphere_plane=abs(area["sphere"]-area["plane"])/(abs(area["sphere"])+abs(area["plane"])+1e-12)
    sep_saddle_plane=abs(area["saddle"]-area["plane"])/(abs(area["saddle"])+abs(area["plane"])+1e-12)
    return rows, sep_sphere_plane, sep_saddle_plane, area, slope

def main():
    print("Heat-kernel curvature action verifier")
    print("="*50)
    print("Route:")
    print("fixed graph Laplacian heat trace features across reference geometries")
    print("No per-geometry calibration. Diagnostic only.")
    print()
    rows, sep_sp, sep_sa, area, slope = run()
    print("kind,feature,median,std")
    for row in rows:
        print(",".join(str(x) for x in row))
    print(f"separation_sphere_plane_area: {sep_sp}")
    print(f"separation_saddle_plane_area: {sep_sa}")
    print(f"area_order: {area}")
    print(f"slope_order: {slope}")
    cls="SPECTRAL_DIAGNOSTIC_PROMISING" if sep_sp>0.02 and sep_sa>0.02 else "SPECTRAL_DIAGNOSTIC_WEAK"
    print(f"classification: {cls}")

if __name__=="__main__":
    main()
