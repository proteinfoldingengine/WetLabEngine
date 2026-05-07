
from __future__ import annotations
import numpy as np

def grid(N, amp=0.25):
    L=2*np.pi; dx=L/N
    x=np.arange(N)*dx; y=np.arange(N)*dx
    X,Y=np.meshgrid(x,y,indexing="ij")
    phi=amp*np.cos(X)*np.cos(Y)
    R=4*amp*np.exp(-2*phi)*np.cos(X)*np.cos(Y)
    dV=np.exp(2*phi)*dx*dx
    rho=R*dV
    return phi,R,dV,rho,dx

def graph_laplacian(phi,dx):
    N=phi.shape[0]; n=N*N
    W=np.zeros((n,n))
    def idx(i,j): return (i%N)*N+(j%N)
    for i in range(N):
        for j in range(N):
            a=idx(i,j)
            for di,dj in [(1,0),(-1,0),(0,1),(0,-1)]:
                ni=(i+di)%N; nj=(j+dj)%N
                phimid=0.5*(phi[i,j]+phi[ni,nj])
                ell=np.exp(phimid)*dx
                w=np.exp(-ell*ell/(4*dx*dx))
                b=idx(ni,nj)
                W[a,b]=w
    W=0.5*(W+W.T)
    deg=W.sum(axis=1)
    return (np.diag(deg)-W)/(dx*dx)

def corr(a,b):
    a=np.asarray(a).ravel(); b=np.asarray(b).ravel()
    a=a-np.mean(a); b=b-np.mean(b)
    return float(np.sum(a*b)/(np.sqrt(np.sum(a*a)*np.sum(b*b))+1e-12))

def local_hat(N):
    phi,R,dV,rho,dx=grid(N)
    L=graph_laplacian(phi,dx)
    ev,V=np.linalg.eigh(L)
    ev=np.maximum(ev,0); V2=V*V
    times=np.array([0.8,1.2,1.8])*dx*dx
    diags=np.array([V2 @ np.exp(-t*ev) for t in times])
    Y=diags*((4*np.pi*times)[:,None])
    slopes=np.empty(N*N)
    for i in range(N*N):
        m,b=np.polyfit(times,Y[:,i],1)
        slopes[i]=-6*m
    Rhat=slopes.reshape(N,N)
    # center because torus total curvature is zero and graph baseline shifts exist
    return Rhat-np.mean(Rhat), R-np.mean(R), rho-np.mean(rho), dx

def run(Ns=(10,12,14,16,18)):
    rows=[]
    scales=[]
    for N in Ns:
        Rhat,R,rho,dx=local_hat(N)
        x=Rhat.ravel()
        y=R.ravel()
        # fit y ≈ s*x with no intercept
        s=float(np.dot(x,y)/(np.dot(x,x)+1e-12))
        pred=s*x
        rel_l2=float(np.linalg.norm(pred-y)/(np.linalg.norm(y)+1e-12))
        rows.append((N,N*N,float(dx),s,rel_l2,corr(pred,y),corr(Rhat,R),float(np.std(Rhat)),float(np.std(R))))
        scales.append(s)
    scale_cv=float(np.std(scales)/(abs(np.mean(scales))+1e-12))
    return rows,scale_cv

def main():
    print("Local heat curvature magnitude verifier")
    print("="*50)
    print("Route:")
    print("fit one scale per grid: analytic R ≈ s*(-6B), evaluate L2 error and scale stability")
    print("Diagnostic only; scale not yet theorem-derived.")
    print()
    rows,scale_cv=run()
    print("N,nodes,dx,best_scale_s,relative_L2_error,corr_scaled_R,corr_raw_Rhat_R,std_Rhat,std_R")
    for row in rows:
        print(",".join(str(x) for x in row))
    print(f"scale_cv_across_grids: {scale_cv}")
    final_err=rows[-1][4]
    corr_ok=all(r[5]>0.90 for r in rows)
    err_ok=final_err<0.45
    scale_ok=scale_cv<0.25
    print(f"corr_ok_all: {corr_ok}")
    print(f"final_error_lt_0p45: {err_ok}")
    print(f"scale_cv_lt_0p25: {scale_ok}")
    print(f"classification: {'LOCAL_MAGNITUDE_PROMISING' if corr_ok and err_ok and scale_ok else 'LOCAL_MAGNITUDE_WEAK'}")

if __name__=="__main__":
    main()
