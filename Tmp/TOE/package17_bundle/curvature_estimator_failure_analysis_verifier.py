
from __future__ import annotations
import numpy as np

def sphere_points(n, seed):
    rng=np.random.default_rng(seed)
    X=rng.normal(size=(n,3))
    X/=np.linalg.norm(X,axis=1,keepdims=True)
    return X

def plane_points(n, seed):
    rng=np.random.default_rng(seed)
    X=rng.uniform(-1,1,size=(n,2))
    return np.c_[X, np.zeros(n)]

def knn(X,k):
    D=np.linalg.norm(X[:,None,:]-X[None,:,:],axis=-1)
    np.fill_diagonal(D,np.inf)
    return np.argsort(D,axis=1)[:,:k]

def cov_proxy(X,nbr):
    vals=[]
    for i in range(len(X)):
        Y=X[nbr[i]]-X[i]
        h=np.median(np.linalg.norm(Y,axis=1))
        C=(Y.T@Y)/len(Y)
        eig=np.sort(np.linalg.eigvalsh(C))
        vals.append((eig[0]/(np.mean(eig[1:])+1e-12))/(h*h+1e-12))
    return np.asarray(vals)

def angle_deficit_proxy(X,nbr):
    # Project neighbors to local PCA tangent plane, sort by angle, sum angles around center.
    # For manifold-like neighborhoods: deficit=2pi-angle_sum. Crude but more geometric.
    vals=[]
    for i in range(len(X)):
        Y=X[nbr[i]]-X[i]
        C=Y.T@Y/len(Y)
        eigvals,eigvecs=np.linalg.eigh(C)
        basis=eigvecs[:,np.argsort(eigvals)[-2:]]
        P=Y@basis
        ang=np.arctan2(P[:,1],P[:,0])
        order=np.argsort(ang)
        P=P[order]
        if len(P)<3: continue
        # sum angles between consecutive neighbor rays
        rays=P/(np.linalg.norm(P,axis=1,keepdims=True)+1e-12)
        total=0.0
        for a,b in zip(rays, np.roll(rays,-1,axis=0)):
            total+=np.arccos(np.clip(np.dot(a,b),-1,1))
        vals.append(2*np.pi-total)
    return np.asarray(vals)

def spectral_proxy(X,nbr):
    # local graph Laplacian trace proxy from neighbor distance weights
    vals=[]
    for i in range(len(X)):
        Y=X[nbr[i]]-X[i]
        d=np.linalg.norm(Y,axis=1)
        h=np.median(d)
        w=np.exp(-(d/(h+1e-12))**2)
        # variance of radial weights as rough nonflatness signal
        vals.append(np.var(w)/(h*h+1e-12))
    return np.asarray(vals)

def evaluate(estimator, geom, ns=(100,200,400,800), reps=3, k=12):
    rows=[]
    for n in ns:
        meds=[]; cvs=[]
        for r in range(reps):
            X=sphere_points(n, 3000+n+r) if geom=="sphere" else plane_points(n, 4000+n+r)
            nbr=knn(X,k)
            vals=estimator(X,nbr)
            vals=vals[np.isfinite(vals)]
            if len(vals):
                meds.append(float(np.median(vals)))
                cvs.append(float(np.std(vals)/(abs(np.mean(vals))+1e-12)))
        rows.append((n,float(np.median(meds)),float(np.median(cvs))))
    return rows

def score_estimator(estimator):
    sph=evaluate(estimator,"sphere")
    pl=evaluate(estimator,"plane")
    # Desired: separates sphere from plane and CV doesn't blow up.
    sep=abs(sph[-1][1]-pl[-1][1])/(abs(pl[-1][1])+abs(sph[-1][1])+1e-12)
    cv_ratio=sph[0][2]/(sph[-1][2]+1e-12)
    return sph, pl, sep, cv_ratio

def main():
    print("Curvature estimator failure analysis verifier")
    print("="*50)
    print("Route:")
    print("compare candidate local graph curvature proxies on sphere vs plane refinement")
    print()
    estimators=[("covariance_normal_variance",cov_proxy),
                ("angle_deficit_pca",angle_deficit_proxy),
                ("spectral_weight_variance",spectral_proxy)]
    for name,fn in estimators:
        sph,pl,sep,cv=score_estimator(fn)
        print(f"ESTIMATOR: {name}")
        print(f"sphere_rows_n_median_cv: {sph}")
        print(f"plane_rows_n_median_cv: {pl}")
        print(f"separation_score: {sep}")
        print(f"sphere_cv_improvement: {cv}")
        cls="CANDIDATE" if sep>0.2 and cv>0.8 else "WEAK"
        print(f"classification: {cls}")
        print()
if __name__=="__main__":
    main()
