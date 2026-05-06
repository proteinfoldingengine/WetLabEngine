
from __future__ import annotations
import numpy as np

def grid3(N, amp=0.15):
    L=2*np.pi; dx=L/N
    x=np.arange(N)*dx
    X,Y,Z=np.meshgrid(x,x,x,indexing="ij")
    phi=amp*np.cos(X)*np.cos(Y)*np.cos(Z)
    lap_phi=-3*amp*np.cos(X)*np.cos(Y)*np.cos(Z)
    phix=-amp*np.sin(X)*np.cos(Y)*np.cos(Z)
    phiy=-amp*np.cos(X)*np.sin(Y)*np.cos(Z)
    phiz=-amp*np.cos(X)*np.cos(Y)*np.sin(Z)
    grad2=phix*phix+phiy*phiy+phiz*phiz
    R=np.exp(-2*phi)*(-4*lap_phi-2*grad2)
    dV=np.exp(3*phi)*dx**3
    rho=R*dV
    return phi,R,dV,rho,dx

def degree3(phi, dx):
    N=phi.shape[0]
    deg=np.zeros((N,N,N))
    for i in range(N):
        for j in range(N):
            for k in range(N):
                s=0.0
                for di,dj,dk in [(1,0,0),(-1,0,0),(0,1,0),(0,-1,0),(0,0,1),(0,0,-1)]:
                    ni=(i+di)%N; nj=(j+dj)%N; nk=(k+dk)%N
                    phimid=0.5*(phi[i,j,k]+phi[ni,nj,nk])
                    ell=np.exp(phimid)*dx
                    s += np.exp(-ell*ell/(4*dx*dx))
                deg[i,j,k]=s
    return deg

def corr(a,b):
    a=np.asarray(a).ravel(); b=np.asarray(b).ravel()
    a=a-np.mean(a); b=b-np.mean(b)
    return float(np.sum(a*b)/(np.sqrt(np.sum(a*a)*np.sum(b*b))+1e-12))

def run(Ns=(8,10,12,16,20,24,32)):
    rows=[]; scales=[]
    for N in Ns:
        phi,R,dV,rho,dx=grid3(N)
        d=degree3(phi,dx)
        proxy=-(d-np.mean(d))
        target=R-np.mean(R)
        x=proxy.ravel(); y=target.ravel()
        s=float(np.dot(x,y)/(np.dot(x,x)+1e-12))
        pred=s*x
        rel_l2=float(np.linalg.norm(pred-y)/(np.linalg.norm(y)+1e-12))
        mask=np.abs(y)>=0.10*np.max(np.abs(y))
        sign_match=float(np.mean(np.sign(pred[mask])==np.sign(y[mask])))
        rows.append((N,N**3,float(dx),float(np.sum(rho)),s,rel_l2,corr(pred,y),corr(proxy,rho-np.mean(rho)),sign_match,float(np.mean(mask)),float(np.std(proxy)),float(np.std(target))))
        scales.append(s)
    return rows,float(np.std(scales)/(abs(np.mean(scales))+1e-12))

def main():
    print("Local heat 3D curvature density verifier")
    print("="*50)
    print("Route:")
    print("3D conductance precursor: -weighted-degree proxy vs analytic R^(3)")
    print("This is not the direct heat diagonal; it tests whether the 2D mechanism extends to 3D.")
    print()
    rows,scale_cv=run()
    print("N,nodes,dx,int_R_dV,best_scale_s,relative_L2_error,corr_scaled_R,corr_proxy_RdV,thresholded_sign_match,retained_fraction,std_proxy,std_R")
    for row in rows:
        print(",".join(str(x) for x in row))
    corr_ok=all(r[6]>0.75 for r in rows)
    sign_ok=all(r[8]>0.70 for r in rows)
    final_err_ok=rows[-1][5]<0.70
    scale_ok=scale_cv<0.25
    print(f"scale_cv_across_grids: {scale_cv}")
    print(f"corr_ok_all_gt_0p75: {corr_ok}")
    print(f"thresholded_sign_ok_all_gt_0p70: {sign_ok}")
    print(f"final_error_lt_0p70: {final_err_ok}")
    print(f"scale_cv_lt_0p25: {scale_ok}")
    print(f"classification: {'LOCAL_3D_CONDUCTANCE_PROMISING' if corr_ok and sign_ok and final_err_ok and scale_ok else 'LOCAL_3D_CONDUCTANCE_WEAK'}")

if __name__=="__main__":
    main()
