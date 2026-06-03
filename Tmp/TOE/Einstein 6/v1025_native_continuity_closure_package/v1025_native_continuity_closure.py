#!/usr/bin/env python3
from pathlib import Path
import json, zipfile
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

OUT = Path("v1025_native_continuity_closure_outputs")
OUT.mkdir(exist_ok=True)

N=34; BOUND=4.0; EPS=1e-9; ALPHA=0.127348327184804; ETA=0.35; DT=0.045; STEPS=7
FAMILIES=["calibration","holdout_shifted","ood_multi"]
KINDS=["legitimate_native","source_shuffled_control","forged_static_control"]

def rms(x): return float(np.sqrt(np.mean(np.asarray(x).ravel()**2)))
def corr(a,b):
    a=np.asarray(a).ravel(); b=np.asarray(b).ravel()
    if np.std(a)<EPS or np.std(b)<EPS: return float("nan")
    return float(np.corrcoef(a,b)[0,1])
def grad(F,dx):
    gy,gx=np.gradient(F,dx,edge_order=2); return gx,gy
def div(Fx,Fy,dx):
    return np.gradient(Fx,dx,axis=1,edge_order=2)+np.gradient(Fy,dx,axis=0,edge_order=2)
def family_offset(f): return {"calibration":0,"holdout_shifted":100000,"ood_multi":200000}[f]
def params(f):
    if f=="calibration": return (0.65,1.25,2.0,2.4,1.25,0.85)
    if f=="holdout_shifted": return (0.75,1.45,1.8,2.7,1.05,0.95)
    return (0.50,1.65,1.6,2.9,1.55,0.70)
def init_fields(seed,fam):
    rng=np.random.default_rng(seed); x=np.linspace(-BOUND,BOUND,N); dx=x[1]-x[0]
    X,Y=np.meshgrid(x,x,indexing="xy"); R=np.sqrt(X*X+Y*Y)
    wlo,whi,a1,a2,freq,decay=params(fam)
    c1=rng.uniform(-1.4,1.4,2); c2=rng.uniform(-1.8,1.8,2)
    w1=rng.uniform(wlo,whi); w2=rng.uniform(wlo,whi)
    source=a1*np.exp(-((X-c1[0])**2+(Y-c1[1])**2)/w1)+a2*np.exp(-((X-c2[0])**2+(Y-c2[1])**2)/w2)
    if fam=="ood_multi":
        c3=rng.uniform(-1.6,1.6,2); w3=rng.uniform(wlo,whi)
        source += 1.2*np.exp(-((X-c3[0])**2+(Y-c3[1])**2)/w3)
    repair=np.cos(freq*R+rng.uniform(0,2*np.pi))*np.exp(-R/(BOUND*decay))
    return source,repair,dx
def geom(source,repair):
    C=ETA*repair-0.25*source
    A=np.exp(C-source+ETA*repair)
    psi=np.log(A+EPS)
    return psi
def native_update(source,repair,dx):
    psi=geom(source,repair)
    gx,gy=grad(psi,dx); Jx,Jy=-gx,-gy
    flux=div(Jx*source,Jy*source,dx)
    nxt=np.maximum(source-DT*flux,0.0)
    rep=0.985*repair+0.015*(source/(np.max(source)+EPS)-0.5)
    return nxt,rep,flux
def control_update(source,repair,dx,rng,kind):
    if kind=="source_shuffled_control":
        nxt=rng.permutation(np.roll(source,1,axis=0).ravel()).reshape(source.shape)
        return nxt,repair,None
    if kind=="forged_static_control":
        nxt=np.maximum(source+0.01*rng.normal(size=source.shape),0)
        return nxt,repair,None
    raise ValueError(kind)
def continuity(source0,source1,repair0,dx):
    psi=geom(source0,repair0); gx,gy=grad(psi,dx); Jx,Jy=-gx,-gy
    flux=div(Jx*source0,Jy*source0,dx)
    C=(source1-source0)+DT*flux
    return dict(C_rms=rms(C), C_norm=float(rms(C)/(rms(source1-source0)+EPS)),
                delta_source_rms=rms(source1-source0), flux_div_rms=rms(flux),
                corr_delta_flux=corr(source1-source0,-DT*flux))
def run_one(seed,fam,kind):
    source,repair,dx=init_fields(seed,fam); rng=np.random.default_rng(seed+777); rows=[]
    for t in range(STEPS-1):
        s0=source.copy(); r0=repair.copy()
        if kind=="legitimate_native": source,repair,_=native_update(source,repair,dx)
        else: source,repair,_=control_update(source,repair,dx,rng,kind)
        m=continuity(s0,source,r0,dx)
        m.update(family=fam,kind=kind,seed=seed,transition=f"{t}->{t+1}")
        rows.append(m)
    return rows
def main():
    rows=[]
    for fam in FAMILIES:
        for g in range(20):
            seed=10000+g+family_offset(fam)
            for kind in KINDS:
                rows.extend(run_one(seed,fam,kind))
    df=pd.DataFrame(rows)
    by=df.groupby(["family","kind"]).agg(n=("kind","count"),mean_C_norm=("C_norm","mean"),mean_C_rms=("C_rms","mean"),mean_corr=("corr_delta_flux","mean")).reset_index()
    legit=df[df.kind=="legitimate_native"]; ctrl=df[df.kind!="legitimate_native"]
    summary={"document_id":"V1025_NATIVE_CONTINUITY_CLOSURE","transitions_tested":int(len(df)),
             "legitimate_mean_C_norm":float(legit.C_norm.mean()),"control_mean_C_norm":float(ctrl.C_norm.mean()),
             "legitimate_mean_C_rms":float(legit.C_rms.mean()),"control_mean_C_rms":float(ctrl.C_rms.mean()),
             "legitimate_mean_corr_delta_flux":float(legit.corr_delta_flux.mean()),"control_mean_corr_delta_flux":float(ctrl.corr_delta_flux.mean()),
             "pass_conditions":{"native_continuity_lower_than_controls":bool(legit.C_norm.mean()<ctrl.C_norm.mean()),
             "native_continuity_near_zero":bool(legit.C_rms.mean()<1e-8),"effect_gap":float(ctrl.C_norm.mean()-legit.C_norm.mean())},
             "claim_boundary":"Native source-continuity closure only; no physical GR/Bianchi/ADM/tensor claim."}
    df.to_csv(OUT/"v1025_native_continuity_results.csv",index=False); by.to_csv(OUT/"v1025_by_kind_summary.csv",index=False)
    (OUT/"v1025_summary.json").write_text(json.dumps(summary,indent=2),encoding="utf-8")
    ax=by.plot(x="kind",y="mean_C_norm",kind="bar",figsize=(9,5),legend=False)
    ax.set_ylabel("mean native continuity residual norm"); ax.set_title("V1025 Native Source Continuity Closure")
    plt.xticks(rotation=25,ha="right"); plt.tight_layout(); plt.savefig(OUT/"v1025_native_continuity_by_kind.png",dpi=170); plt.close()
    report=f"""# V1025 Native Continuity Closure

## Purpose

V1024.1 showed only a weak B_ADM-like gap. V1025 measures the primitive continuity law directly.

## Native Closure

```text
C_native = Δsource + dt * div(J * source)
J = -∇ψ
```

## Summary

```json
{json.dumps(summary, indent=2)}
```

## By-Kind Results

{by.to_markdown(index=False)}

## Interpretation

This tests whether the ordered accessibility-flow update has an internal conservation-like closure before lifting it to ADM-like H/M branches.

## Claim Boundary

Model-native source-continuity closure only.

Not physical Bianchi identity, not ADM, not GR, not Einstein equations, not tensor covariance.
"""
    (OUT/"V1025_NATIVE_CONTINUITY_CLOSURE_REPORT.md").write_text(report,encoding="utf-8")
    with zipfile.ZipFile(OUT/"v1025_source.zip","w",zipfile.ZIP_DEFLATED) as z: z.write(Path(__file__),arcname=Path(__file__).name)
    print(json.dumps(summary,indent=2))
if __name__=="__main__": main()
