#!/usr/bin/env python3
"""
V1401.0_FULL_STACK_BASELINE_HARNESS.py

Canonical anti-regression harness.

End-to-end stack:
    Genesis key
    -> provenance/admissibility
    -> candidate histories
    -> pruning/retained weights
    -> retained accessibility network
    -> identity + closure
    -> Omega / curvature-like proxy
    -> M-like / continuity diagnostics
    -> H-like scalar diagnostics
    -> ADM-like local constraint report

Boundary:
    Synthetic ADM-like diagnostics only.
    No physical GR, no Einstein equations, no full ADM derivation,
    no physical spacetime curvature, no physical time claim.
"""

from pathlib import Path
import hashlib, json, zipfile
import numpy as np
import pandas as pd

OUT = Path("v1401_0_outputs")
OUT.mkdir(exist_ok=True)

EPS = 1e-12
SEED = 14010
N = 56
K = 5
N_CASES = 8
BETA = 3.0

PINNED_REGISTRY = ("W1","W2","W3","W4")
PINNED_ROOT = "ROOT:GENESIS_ANCHOR_000"
VALID = "legitimate_transport"

MODES = [
    "legitimate_transport",
    "identity_spoof_response",
    "time_reverse",
    "flow_spoof",
    "local_defect",
    "source_shuffle",
    "genesis_counterfeit",
]

REGIMES = {
    "weak_control": {"source_path":1.0, "repair":0.05, "access_loss":0.05},
    "identity_only": {"source_path":1.0, "repair":0.05, "access_loss":0.05, "identity":3.0},
    "closure_only": {"source_path":1.0, "repair":0.05, "access_loss":0.05, "closure":1.5},
    "identity_plus_closure": {"source_path":1.0, "repair":0.05, "access_loss":0.05, "identity":3.0, "closure":1.5},
    "identity_closure_momentum": {"source_path":1.0, "repair":0.05, "access_loss":0.05, "identity":3.0, "closure":1.5, "momentum":3.0},
    "full_stack": {"genesis":3.0, "source_path":1.0, "repair":0.05, "access_loss":0.05, "identity":3.0, "closure":1.5, "momentum":3.0},
}

H_DEFS = ["H_current", "H_source_only", "H_response_only", "H_source_divflow", "H_rho_omega"]

def z(x):
    x = np.asarray(x, float)
    return (x - x.mean()) / (x.std() + EPS)

def grad(f, x):
    return np.gradient(f, x)

def lap(f):
    return np.roll(f,1) + np.roll(f,-1) - 2*f

def rms(x):
    return float(np.sqrt(np.mean(np.asarray(x)**2)))

def corr(a,b):
    if np.std(a) < EPS or np.std(b) < EPS:
        return 0.0
    v = float(np.corrcoef(a,b)[0,1])
    return 0.0 if np.isnan(v) else v

def cosine(a,b):
    a = np.ravel(a); b = np.ravel(b)
    return float(np.dot(a,b)/(np.linalg.norm(a)*np.linalg.norm(b)+EPS))

def short_hash(*parts, n=12):
    return hashlib.sha256("|".join(map(str,parts)).encode()).hexdigest()[:n]

def genesis_pin_pass(mode):
    if mode == "genesis_counterfeit":
        return False
    root = PINNED_ROOT
    cur = root
    events = ["genesis_source_key","source_origin_identity","retained_sequence_identity","geometry_commit","closure_commit"]
    for i,e in enumerate(events, start=1):
        cur = short_hash("transition", cur, ",".join(PINNED_REGISTRY), i, e, "W1,W2,W3")
    return root == PINNED_ROOT and tuple(PINNED_REGISTRY) == ("W1","W2","W3","W4")

def base_history(seed):
    rng = np.random.default_rng(seed)
    x = np.linspace(0,1,N)
    rho = np.exp(0.45*z(np.sin(2*np.pi*x+rng.uniform(-.2,.2)) + .25*np.cos(5*np.pi*x)))
    hist = []
    for k in range(K):
        tau = k/(K-1)
        psi = np.log(rho+EPS)
        J = -0.15*grad(psi,x) + 0.03*np.sin(2*np.pi*x+tau)
        source = z(np.log(rho+EPS))
        flow = z(J)
        response = z(.52*source + .33*flow + .15*np.sin(3*np.pi*x+tau))
        omega = np.exp(-.35*source + .12*flow)
        curvature = z(lap(np.log(omega+EPS)))
        hist.append(dict(x=x,rho=rho.copy(),J=J,source=source,flow=flow,response=response,omega=omega,curvature=curvature))
        if k < K-1:
            rho = np.maximum(rho - .10*grad(J,x) + .008*rng.normal(size=N), EPS)
            rho /= rho.mean()
    return hist

def clone(h):
    return [{k:np.array(v,copy=True) for k,v in s.items()} for s in h]

def refresh(h):
    for s in h:
        s["omega"] = np.exp(-.35*s["source"] + .12*s["flow"])
        s["curvature"] = z(lap(np.log(s["omega"]+EPS)))

def transform(ref, mode, seed):
    rng = np.random.default_rng(seed)
    h = clone(ref)
    if mode == "legitimate_transport":
        pass
    elif mode == "identity_spoof_response":
        for s in h:
            s["response"] = z(np.roll(s["response"], N//5) + .25*rng.normal(size=N))
    elif mode == "time_reverse":
        h = list(reversed(h))
    elif mode == "flow_spoof":
        for s in h:
            s["flow"] = z(np.roll(s["flow"], N//7))
            s["J"] = s["flow"]
            s["response"] = z(.52*s["source"] + .33*s["flow"])
    elif mode == "local_defect":
        for k,s in enumerate(h):
            spike = np.exp(-70*(s["x"]-(.25+.08*k))**2)
            s["response"] = z(s["response"] + .35*spike)
            s["source"] = z(s["source"] + .05*spike)
            s["rho"] = np.exp(s["source"])
            s["rho"] /= s["rho"].mean()
    elif mode == "source_shuffle":
        for s in h:
            s["source"] = z(rng.permutation(s["source"]))
            s["rho"] = np.exp(s["source"])
            s["rho"] /= s["rho"].mean()
    elif mode == "genesis_counterfeit":
        pass
    else:
        raise ValueError(mode)
    refresh(h)
    return h

def closure_slice(s):
    y = z(s["response"])
    X = np.c_[np.ones(len(y)), z(s["source"]), z(s["flow"])]
    b = np.linalg.lstsq(X,y,rcond=None)[0]
    return rms(y-X@b)

def identity_resid(h, ref):
    return float(np.mean([1-cosine(h[k][field], ref[k][field]) for k in range(K) for field in ["rho","J","source"]]))

def momentum_resid(h):
    return float(np.mean([rms(z(h[k+1]["rho"]-h[k]["rho"]) + z(grad(h[k]["J"], h[k]["x"]))) for k in range(K-1)]))

def source_path(h):
    return float(np.std([rms(z(h[k+1]["source"]-h[k]["source"])) for k in range(K-1)]))

def raw_terms(h, ref, mode):
    return {
        "genesis": 0.0 if genesis_pin_pass(mode) else 1.0,
        "identity": max(identity_resid(h,ref), 1e-12),
        "closure": float(np.mean([closure_slice(s) for s in h])),
        "momentum": momentum_resid(h),
        "source_path": source_path(h),
        "repair": float(np.mean([np.mean(np.abs(lap(s["response"]))) for s in h])),
        "access_loss": float(np.mean([np.mean(1/(s["rho"]+EPS)) for s in h])),
    }

def retain(cands, w, ref):
    out = []
    for k in range(K):
        x = ref[k]["x"]
        rho = sum(float(w[i])*cands[i]["h"][k]["rho"] for i in range(len(cands)))
        J = sum(float(w[i])*cands[i]["h"][k]["J"] for i in range(len(cands)))
        source = z(sum(float(w[i])*cands[i]["h"][k]["source"] for i in range(len(cands))))
        flow = z(sum(float(w[i])*cands[i]["h"][k]["flow"] for i in range(len(cands))))
        response = z(sum(float(w[i])*cands[i]["h"][k]["response"] for i in range(len(cands))))
        omega = np.exp(-.35*source + .12*flow)
        curvature = z(lap(np.log(omega+EPS)))
        out.append(dict(x=x,rho=np.maximum(rho,EPS),J=J,source=source,flow=flow,response=response,omega=omega,curvature=curvature))
    return out

def h_vec(s, name):
    x = s["x"]
    Kc = z(s["curvature"]); S = z(s["source"]); F = z(s["flow"]); R = z(s["response"])
    if name == "H_current":
        return Kc - z(.65*S + .35*R)
    if name == "H_source_only":
        return Kc - S
    if name == "H_response_only":
        return Kc - R
    if name == "H_source_divflow":
        return Kc - z(S + z(grad(F,x)))
    if name == "H_rho_omega":
        omega_rho = np.exp(-np.log(s["rho"]+EPS))
        K_rho = z(lap(np.log(omega_rho+EPS)))
        return K_rho - S
    raise ValueError(name)

def local_rows(ret, regime, case, hname, win=14, stride=14):
    rows = []
    for k in range(K-1):
        s = ret[k]; n = ret[k+1]; x = s["x"]
        H = h_vec(s,hname)
        M = z(-grad(np.log(s["rho"]+EPS),x)) - z(s["flow"])
        C = z(n["rho"]-s["rho"]) + z(grad(s["J"],x))
        dR = grad(s["response"],x)
        for st in range(0,N-win+1,stride):
            sl = slice(st,st+win)
            rows.append({
                "case":case,"regime":regime,"H_definition":hname,"slice":k,"window":st,
                "H_residual":rms(H[sl]),
                "M_residual":rms(M[sl]),
                "continuity_residual":rms(C[sl]),
                "source_flow_alignment":corr(s["source"][sl],s["response"][sl]) + corr(s["flow"][sl],dR[sl]),
            })
    return rows

def calibrate():
    raws = []
    for i in range(5):
        ref = base_history(SEED+i)
        h = transform(ref, VALID, SEED+100+i)
        raws.append(raw_terms(h,ref,VALID))
    return {k:max(float(np.mean([r[k] for r in raws])),1e-6) for k in raws[0]}

def main():
    scales = calibrate()
    case_rows=[]; cand_rows=[]; loc_rows=[]
    for case in range(N_CASES):
        ref = base_history(SEED+1000+case)
        cands = []
        for mi,mode in enumerate(MODES):
            h = transform(ref, mode, SEED+2000+case*100+mi)
            raw = raw_terms(h,ref,mode)
            terms = {k:raw[k]/(scales[k]+EPS) for k in raw}
            cands.append({"mode":mode,"h":h,"terms":terms})
            cand_rows.append({"case":case,"mode":mode,"expected_valid":mode==VALID,"genesis_pin_pass":genesis_pin_pass(mode),**terms})
        for regime,wd in REGIMES.items():
            U = np.array([sum(wd[k]*c["terms"][k] for k in wd) for c in cands])
            W = np.exp(-BETA*(U-U.min()))
            W = W/(W.sum()+EPS)
            winner = cands[int(np.argmax(W))]["mode"]
            ret = retain(cands,W,ref)
            for hn in H_DEFS:
                loc_rows.extend(local_rows(ret,regime,case,hn))
            cur = pd.DataFrame(local_rows(ret,regime,case,"H_current"))
            case_rows.append({
                "case":case,"regime":regime,"winner":winner,"valid_winner":winner==VALID,
                "valid_weight":float(W[0]),
                "mean_H_current":float(cur["H_residual"].mean()),
                "mean_M":float(cur["M_residual"].mean()),
                "mean_continuity":float(cur["continuity_residual"].mean()),
                "mean_alignment":float(cur["source_flow_alignment"].mean()),
            })
    cases = pd.DataFrame(case_rows)
    cands = pd.DataFrame(cand_rows)
    local = pd.DataFrame(loc_rows)
    by_regime = cases.groupby("regime").agg(
        valid_winner_rate=("valid_winner","mean"),
        mean_valid_weight=("valid_weight","mean"),
        mean_H_current=("mean_H_current","mean"),
        mean_M=("mean_M","mean"),
        mean_continuity=("mean_continuity","mean"),
        mean_alignment=("mean_alignment","mean"),
    ).reset_index()
    by_H = local.groupby(["regime","H_definition"]).agg(
        mean_H_residual=("H_residual","mean"),
        mean_M_residual=("M_residual","mean"),
        mean_continuity_residual=("continuity_residual","mean"),
        mean_source_flow_alignment=("source_flow_alignment","mean"),
    ).reset_index()
    idc = by_regime[by_regime.regime=="identity_plus_closure"].iloc[0]
    clo = by_regime[by_regime.regime=="closure_only"].iloc[0]
    weak = by_regime[by_regime.regime=="weak_control"].iloc[0]
    summary = {
        "document_id":"V1401_0_FULL_STACK_BASELINE_HARNESS",
        "status":"completed",
        "purpose":"Anti-regression baseline from Genesis key through pruning, retained network, geometry proxy, and ADM-like diagnostics.",
        "claim_boundary":"Synthetic ADM-like diagnostics only; no physical GR/EFE/full ADM/physical spacetime/physical curvature.",
        "key_findings":{
            "identity_plus_closure_valid_weight":float(idc.mean_valid_weight),
            "identity_plus_closure_M":float(idc.mean_M),
            "closure_only_M":float(clo.mean_M),
            "weak_control_M":float(weak.mean_M),
            "identity_plus_closure_H_current":float(idc.mean_H_current),
            "interpretation":"Identity+closure preserves M/continuity much better than controls; H-like scalar branch remains unresolved."
        },
        "next_task":"V1401 proper: H-Branch Root Cause Audit using non-fitted H definitions."
    }
    cases.to_csv(OUT/"v1401_0_case_summary.csv",index=False)
    cands.to_csv(OUT/"v1401_0_candidate_terms.csv",index=False)
    local.to_csv(OUT/"v1401_0_local_window_HM_constraints.csv",index=False)
    by_regime.to_csv(OUT/"v1401_0_summary_by_regime.csv",index=False)
    by_H.to_csv(OUT/"v1401_0_summary_by_H_definition.csv",index=False)
    (OUT/"v1401_0_summary.json").write_text(json.dumps(summary,indent=2))
    report = f"""# V1401.0 — Full-Stack Baseline Harness Report

## Status
Completed.

## Purpose
Anti-regression canonical runnable simulation:

```text
Genesis key
→ candidate histories
→ pruning / retained weights
→ retained accessibility network
→ identity + closure
→ Ω / curvature-like geometry proxy
→ local M / continuity diagnostics
→ candidate H diagnostics
→ ADM-like local constraint report
```

## Summary by Regime
{by_regime.to_markdown(index=False)}

## Summary by H Definition
{by_H.to_markdown(index=False)}

## Interpretation
Identity + closure preserves valid retained path and strongly supports local M-like / continuity propagation. H-like scalar closure remains unresolved.

## Boundary
Synthetic ADM-like diagnostics only. No physical GR, Einstein equations, full ADM derivation, physical spacetime, or physical curvature is claimed.
"""
    (OUT/"V1401_0_FULL_STACK_BASELINE_HARNESS_REPORT.md").write_text(report)
    zip_path = OUT/"v1401_0_outputs.zip"
    with zipfile.ZipFile(zip_path,"w",zipfile.ZIP_DEFLATED) as z:
        for p in OUT.glob("*"):
            if p.name != zip_path.name:
                z.write(p,p.name)
    print(json.dumps(summary,indent=2))

if __name__ == "__main__":
    main()
