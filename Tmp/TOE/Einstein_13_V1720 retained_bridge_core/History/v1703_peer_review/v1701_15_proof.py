from pathlib import Path
import json, shutil
import numpy as np
import pandas as pd

BASE = Path("/home/claude")
OUT = BASE / "V1701_15_out"
if OUT.exists(): shutil.rmtree(OUT)
OUT.mkdir(parents=True)

SIZES=[17,33,65,129]; FAMS=["gaussian3","dipole","chirp","mixed"]; MODES=["dynamic_g","frozen_g","flat_g_rho"]

def clean(x):
    if isinstance(x,np.bool_): return bool(x)
    if isinstance(x,np.integer): return int(x)
    if isinstance(x,np.floating): return float(x)
    if isinstance(x,np.ndarray): return x.tolist()
    if isinstance(x,dict): return {k:clean(v) for k,v in x.items()}
    if isinstance(x,list): return [clean(v) for v in x]
    return x

def src(n,fam):
    x=np.arange(n)/n
    if fam=="gaussian3": s=np.exp(-((x-0.15)/0.055)**2)-0.7*np.exp(-((x-0.52)/0.075)**2)-0.3*np.exp(-((x-0.78)/0.06)**2)
    elif fam=="dipole": s=np.sin(2*np.pi*x)+0.35*np.sin(4*np.pi*x+0.4)
    elif fam=="chirp": s=np.sin(2*np.pi*(x+2.2*x*x))+0.25*np.cos(10*np.pi*x)
    elif fam=="mixed": s=0.65*np.sin(2*np.pi*x+0.3)+0.45*np.exp(-((x-0.33)/0.07)**2)-0.55*np.exp(-((x-0.72)/0.09)**2)
    else: raise ValueError(fam)
    s-=s.mean(); return s/(np.max(np.abs(s))+1e-12)

def retained_derivative(n):
    D=np.zeros((n,n))
    for i in range(n):
        D[i,(i+1)%n]=0.5; D[i,(i-1)%n]=-0.5
    return D

def retained_density(n,fam):
    x=np.arange(n)/n; return np.maximum(1+0.18*np.cos(2*np.pi*x)+0.05*src(n,fam),0.25)
def retained_metric_inverse(n,fam):
    x=np.arange(n)/n; return 1/(1+0.08*np.sin(2*np.pi*x)+0.04*src(n,fam))**2
def lapses(n):
    x=np.arange(n)/n
    N=np.sin(4*np.pi*x+0.4)+0.1*np.cos(2*np.pi*x); M=np.cos(4*np.pi*x-0.1)+0.12*np.sin(8*np.pi*x)
    return N-N.mean(),M-M.mean()

def old_scalar_blocks(N,D,rho,ginv):
    A=2*np.diag(N); B=np.diag(1/rho)@D.T@np.diag(ginv)@D@np.diag(rho*N); return A,B
def omegaW_rederive_scalar(A_old,B_old,W):
    WA=W[:,None]*A_old; WB=W[:,None]*B_old
    return 0.5*(WA+WA.T)/W[:,None], 0.5*(WB+WB.T)/W[:,None]
def momentum_blocks(c,D,W):
    Ag=np.diag(c)@D+np.diag(D@c); Ak=-(Ag.T*W[None,:])/W[:,None]; return Ag,Ak
def scalar_frame_residual(A,B,W):
    WA=W[:,None]*A; WB=W[:,None]*B
    num=np.linalg.norm(WA-WA.T,"fro")**2+np.linalg.norm(WB-WB.T,"fro")**2
    den=np.linalg.norm(WA,"fro")**2+np.linalg.norm(WB,"fro")**2
    return float(np.sqrt(num/(den+1e-24)))
def momentum_frame_residual(Ag,Ak,W):
    WAg=W[:,None]*Ag; WAk=W[:,None]*Ak
    num=np.linalg.norm(WAk+WAg.T,"fro"); den=np.sqrt(np.linalg.norm(WAk,"fro")**2+np.linalg.norm(WAg,"fro")**2)+1e-12
    return float(num/den)
def obstruction_blocks(AN,BN,AM,BM,Ag,Ak):
    C11=-AN@BM+AM@BN; C22=-BN@AM+BM@AN; return C11-Ag, C22-Ak
def total_hh_residual(O_g,O_K,Ag,Ak):
    num=np.linalg.norm(O_g,"fro")**2+np.linalg.norm(O_K,"fro")**2
    den=np.linalg.norm(Ag,"fro")**2+np.linalg.norm(Ak,"fro")**2
    return float(np.sqrt(num/(den+1e-24)))
def sector_decompose(O,rho):
    n=O.shape[0]; norm=np.linalg.norm(O,"fro")+1e-12
    diag=np.diag(np.diag(O)); sym=0.5*(O+O.T); asym=0.5*(O-O.T); off=O-diag
    I,J=np.meshgrid(np.arange(n),np.arange(n),indexing="ij"); dist=np.minimum((I-J)%n,(J-I)%n)
    local_mask=dist<=1; near2_mask=dist<=2; far_mask=dist>2
    dens=rho-rho.mean(); dens=dens/(np.linalg.norm(dens)+1e-12); dens_outer=np.outer(dens,dens)
    density_projection=abs(np.sum(O*dens_outer))/(np.linalg.norm(dens_outer,"fro")+1e-12)/norm
    return {"norm":float(norm),"diag_fraction":float(np.linalg.norm(diag,"fro")/norm),
        "symmetric_fraction":float(np.linalg.norm(sym,"fro")/norm),
        "antisymmetric_fraction":float(np.linalg.norm(asym,"fro")/norm),
        "offdiag_fraction":float(np.linalg.norm(off,"fro")/norm),
        "local_fraction":float(np.linalg.norm(O*local_mask,"fro")/norm),
        "near2_fraction":float(np.linalg.norm(O*near2_mask,"fro")/norm),
        "far_fraction":float(np.linalg.norm(O*far_mask,"fro")/norm),
        "density_projection_fraction":float(density_projection),"max_abs":float(np.max(np.abs(O)))}

def evaluate_case(n,fam,mode):
    D=retained_derivative(n); rho=retained_density(n,fam); ginv=retained_metric_inverse(n,fam)
    if mode=="frozen_g": ginv=np.ones(n)*float(np.mean(ginv))
    elif mode=="flat_g_rho": ginv=np.ones(n)*float(np.mean(ginv)); rho=np.ones(n)*float(np.mean(rho))
    elif mode!="dynamic_g": raise ValueError(mode)
    W=rho/ginv; N,M=lapses(n)
    ANo,BNo=old_scalar_blocks(N,D,rho,ginv); AMo,BMo=old_scalar_blocks(M,D,rho,ginv)
    ANn,BNn=omegaW_rederive_scalar(ANo,BNo,W); AMn,BMn=omegaW_rederive_scalar(AMo,BMo,W)
    c=(ginv/rho)*(N*(D@M)-M*(D@N)); Ag,Ak=momentum_blocks(c,D,W)
    RA_old=max(scalar_frame_residual(ANo,BNo,W),scalar_frame_residual(AMo,BMo,W))
    RA_new=max(scalar_frame_residual(ANn,BNn,W),scalar_frame_residual(AMn,BMn,W))
    RB=momentum_frame_residual(Ag,Ak,W)
    old_g,old_K=obstruction_blocks(ANo,BNo,AMo,BMo,Ag,Ak); new_g,new_K=obstruction_blocks(ANn,BNn,AMn,BMn,Ag,Ak)
    old_hh=total_hh_residual(old_g,old_K,Ag,Ak); new_hh=total_hh_residual(new_g,new_K,Ag,Ak)
    sector_rows=[]
    for bn,block in [("old_g_block",old_g),("old_K_block",old_K),("new_g_block",new_g),("new_K_block",new_K)]:
        d=sector_decompose(block,rho); d.update({"n":n,"source_family":fam,"mode":mode,"obstruction_block":bn}); sector_rows.append(d)
    case_row={"n":n,"source_family":fam,"mode":mode,"RA_old":float(RA_old),"RA_new":float(RA_new),"RB_momentum":float(RB),
        "HH_old_operator_residual":float(old_hh),"HH_new_operator_residual":float(new_hh),
        "HH_operator_improvement":float((old_hh-new_hh)/(old_hh+1e-12)),
        "old_g_norm":float(np.linalg.norm(old_g,"fro")),"old_K_norm":float(np.linalg.norm(old_K,"fro")),
        "new_g_norm":float(np.linalg.norm(new_g,"fro")),"new_K_norm":float(np.linalg.norm(new_K,"fro")),
        "g_block_improvement":float((np.linalg.norm(old_g,"fro")-np.linalg.norm(new_g,"fro"))/(np.linalg.norm(old_g,"fro")+1e-12)),
        "K_block_improvement":float((np.linalg.norm(old_K,"fro")-np.linalg.norm(new_K,"fro"))/(np.linalg.norm(old_K,"fro")+1e-12)),
        "scalar_B_correction_norm":float(np.linalg.norm(BNn-BNo,"fro")/(np.linalg.norm(BNo,"fro")+1e-12))}
    return sector_rows,case_row

all_sector=[]; case_rows=[]
for fam in FAMS:
    for n in SIZES:
        for mode in MODES:
            sr,cr=evaluate_case(n,fam,mode); all_sector.extend(sr); case_rows.append(cr)
sectors=pd.DataFrame(all_sector); cases=pd.DataFrame(case_rows)
sector_summary=sectors.groupby(["mode","obstruction_block"]).agg(mean_norm=("norm","mean"),
    mean_diag_fraction=("diag_fraction","mean"),mean_symmetric_fraction=("symmetric_fraction","mean"),
    mean_antisymmetric_fraction=("antisymmetric_fraction","mean"),mean_offdiag_fraction=("offdiag_fraction","mean"),
    mean_local_fraction=("local_fraction","mean"),mean_near2_fraction=("near2_fraction","mean"),
    mean_far_fraction=("far_fraction","mean"),mean_density_projection_fraction=("density_projection_fraction","mean")).reset_index()
case_summary=cases.groupby("mode").agg(mean_RA_old=("RA_old","mean"),mean_RA_new=("RA_new","mean"),
    mean_RB_momentum=("RB_momentum","mean"),mean_HH_old_operator_residual=("HH_old_operator_residual","mean"),
    mean_HH_new_operator_residual=("HH_new_operator_residual","mean"),mean_HH_operator_improvement=("HH_operator_improvement","mean"),
    mean_g_block_improvement=("g_block_improvement","mean"),mean_K_block_improvement=("K_block_improvement","mean"),
    mean_scalar_B_correction_norm=("scalar_B_correction_norm","mean"),mean_new_g_norm=("new_g_norm","mean"),
    mean_new_K_norm=("new_K_norm","mean")).reset_index()

dyn_case=case_summary[case_summary["mode"]=="dynamic_g"].iloc[0]
dyn_sectors=sector_summary[sector_summary["mode"]=="dynamic_g"].copy()
new_dyn=dyn_sectors[dyn_sectors["obstruction_block"].str.startswith("new")].copy()
sector_cols=["mean_diag_fraction","mean_symmetric_fraction","mean_antisymmetric_fraction","mean_offdiag_fraction",
    "mean_local_fraction","mean_near2_fraction","mean_far_fraction","mean_density_projection_fraction"]
sector_means={c.replace("mean_","").replace("_fraction",""):float(new_dyn[c].mean()) for c in sector_cols}
dominant_sector=max(sector_means,key=sector_means.get)
dominant_block=str(new_dyn.sort_values("mean_norm",ascending=False).iloc[0]["obstruction_block"])
RA_new=float(dyn_case["mean_RA_new"]); RB=float(dyn_case["mean_RB_momentum"]); HH_new=float(dyn_case["mean_HH_new_operator_residual"])
frame_pass=RA_new<1e-12 and RB<1e-12; hh_closed=HH_new<0.25
if frame_pass and not hh_closed: verdict="PROOF_PASS_POST_FRAME_HH_OBSTRUCTION_REAL_AND_LOCALIZED"
elif frame_pass and hh_closed: verdict="PROOF_PASS_HH_CLOSURE_CANDIDATE"
else: verdict="PROOF_FAIL_FRAME_GATE"

print("VERDICT:",verdict)
print(f"RA_old(mean)={float(dyn_case['mean_RA_old']):.3e}  RA_new(mean)={RA_new:.3e}  RB={RB:.3e}")
print(f"HH_old={float(dyn_case['mean_HH_old_operator_residual']):.4f}  HH_new={HH_new:.4f}  improvement={float(dyn_case['mean_HH_operator_improvement']):.4f}")
print(f"g_block_impr={float(dyn_case['mean_g_block_improvement']):.4f}  K_block_impr={float(dyn_case['mean_K_block_improvement']):.4f}")
print(f"dominant_block={dominant_block}  dominant_sector={dominant_sector}")
print("sector_means:",json.dumps({k:round(v,4) for k,v in sector_means.items()}))
print("\n--- frame_pass gate check ---")
print(f"RA_new<1e-12? {RA_new<1e-12}   RB<1e-12? {RB<1e-12}")
print("\n--- per-mode RA_new (does frame repair work in all modes?) ---")
print(case_summary[["mode","mean_RA_old","mean_RA_new","mean_RB_momentum","mean_HH_new_operator_residual"]].to_string(index=False))
