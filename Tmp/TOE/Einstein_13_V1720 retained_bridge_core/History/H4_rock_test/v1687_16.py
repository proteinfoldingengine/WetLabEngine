from __future__ import annotations
import json
from pathlib import Path
import numpy as np
import sympy as sp
import pandas as pd

OUT = Path("/home/claude/v1687_16_out"); OUT.mkdir(parents=True, exist_ok=True)
N = 12; EPS = 1e-8; SEED = 168716

def roll_down(v): return np.r_[v[-1], v[:-1]]
def roll_up(v):   return np.r_[v[1:], v[0]]
def recombine(x, y, gamma): return x + y + gamma * (roll_down(x) * y - x * roll_up(y))
def assoc3(A,B,C,gAB,gBC,gL,gR):
    return recombine(recombine(A,B,gAB),C,gL) - recombine(A,recombine(B,C,gBC),gR)
def bracket4_all(J,g):
    J1,J2,J3,J4=J
    return {
        "B1_(((12)3)4)": recombine(recombine(recombine(J1,J2,g["g12"]),J3,g["g123"]),J4,g["g1234"]),
        "B2_((1(23))4)": recombine(recombine(J1,recombine(J2,J3,g["g23"]),g["g123_R"]),J4,g["g1234"]),
        "B3_(1((23)4))": recombine(J1,recombine(recombine(J2,J3,g["g23"]),J4,g["g234"]),g["g1234r"]),
        "B4_(1(2(34)))": recombine(J1,recombine(J2,recombine(J3,J4,g["g34"]),g["g234"]),g["g1234r"]),
        "B5_((12)(34))": recombine(recombine(J1,J2,g["g12"]),recombine(J3,J4,g["g34"]),g["g1234"]),
    }
def rank(cols,tol=1e-8):
    if not cols: return 0
    return int(np.linalg.matrix_rank(np.stack(cols,axis=1),tol=tol))
def norm(v): return float(np.linalg.norm(v))
def residual_to_span(v,basis):
    if not basis: return v.copy(),norm(v)
    B=np.stack(basis,axis=1); coeff=np.linalg.pinv(B)@v; res=v-B@coeff; return res,norm(res)
def apply(P,v): return P@v

MASKS={"J1":[1,1,1,0,1,0,0,1,0,0,0,1],"J2":[1,0,1,1,0,1,0,0,1,0,1,0],
       "J3":[0,1,1,1,0,0,1,0,0,1,1,0],"J4":[1,0,0,1,1,0,1,1,0,1,0,0]}
def values_for_mask(mask,prefix,seed=1):
    vals=[]
    for i,active in enumerate(mask):
        if active:
            raw=((seed+3)*(i+5)+len(prefix)*7)%29-14
            if raw==0: raw=i%7+1
            vals.append(float(raw))
        else: vals.append(0.0)
    return np.array(vals,dtype=float)
def gate_values(seed=1):
    names=["g12","g23","g13","g14","g24","g34","g123_L","g123_R","g124_L","g124_R",
           "g134_L","g134_R","g234_L","g234_R","g123","g1234","g234","g1234r"]
    return {name: float(sp.Rational(((idx+seed)%11)+2,((2*idx+seed)%7)+3)) for idx,name in enumerate(names)}
def build_base(seed=1):
    J=[values_for_mask(MASKS[f"J{k}"],f"j{k}",seed) for k in range(1,5)]
    g=gate_values(seed); J1,J2,J3,J4=J
    O123=assoc3(J1,J2,J3,g["g12"],g["g23"],g["g123_L"],g["g123_R"])
    O124=assoc3(J1,J2,J4,g["g12"],g["g24"],g["g124_L"],g["g124_R"])
    O134=assoc3(J1,J3,J4,g["g13"],g["g34"],g["g134_L"],g["g134_R"])
    O234=assoc3(J2,J3,J4,g["g23"],g["g34"],g["g234_L"],g["g234_R"])
    O3=[O123,O124,O134,O234]; br=bracket4_all(J,g)
    H4=br["B1_(((12)3)4)"]-br["B4_(1(2(34)))"]
    return {"branches":J,"O3":O3,"H4":H4,"gates":g,"bracketings":br}
def H4_residual_projection(base):
    res,resn=residual_to_span(base["H4"],base["branches"]+base["O3"])
    u=res/max(EPS,resn); P=np.eye(N)-np.outer(u,u); return P,u,resn

def pair_faithfulness(P,base):
    J=base["branches"]; g=base["gates"]
    pairs={(0,1):g["g12"],(1,2):g["g23"],(0,2):g["g13"],(0,3):g["g14"],(1,3):g["g24"],(2,3):g["g34"]}
    rows=[]
    for (i,j),gate in pairs.items():
        lhs=apply(P,recombine(J[i],J[j],gate)); rhs=apply(P,recombine(apply(P,J[i]),apply(P,J[j]),gate))
        rows.append({"test":f"pair_J{i+1}J{j+1}","gap":norm(lhs-rhs)})
    return rows
def nested_bracketing_faithfulness(P,base):
    J=base["branches"]; g=base["gates"]; original=base["bracketings"]
    PJ=[apply(P,v) for v in J]; projected=bracket4_all(PJ,g); rows=[]
    for name,vec in original.items():
        rows.append({"test":f"nested_{name}","gap":norm(apply(P,vec)-apply(P,projected[name]))})
    return rows
def random_composite_faithfulness(P,base,trials=200):
    rng=np.random.default_rng(SEED); J=base["branches"]; gates=list(base["gates"].values())
    mx=0.0; mg=[]
    for t in range(trials):
        a=sum(rng.normal()*J[i] for i in range(4)); b=sum(rng.normal()*J[i] for i in range(4))
        gate=float(gates[int(rng.integers(0,len(gates)))])
        gap=norm(apply(P,recombine(a,b,gate))-apply(P,recombine(apply(P,a),apply(P,b),gate)))
        mx=max(mx,gap); mg.append(gap)
    return {"random_composite_trials":trials,"random_composite_gap_max":float(mx),
            "random_composite_gap_mean":float(np.mean(mg)),"random_composite_gap_median":float(np.median(mg))}
def algebra_generator_audit(P,base):
    J=base["branches"]; g=base["gates"]; vecs=[]; 
    for v in J: vecs.append(v)
    for (i,j),gate in {(0,1):g["g12"],(1,2):g["g23"],(0,2):g["g13"],(0,3):g["g14"],(1,3):g["g24"],(2,3):g["g34"]}.items():
        vecs.append(recombine(J[i],J[j],gate))
    for name,v in base["bracketings"].items(): vecs.append(v)
    rows=[]; gates=list(base["gates"].values())
    for ia in range(len(vecs)):
        for ib in range(ia+1,len(vecs)):
            gate=gates[(ia+3*ib)%len(gates)]
            rows.append(norm(apply(P,recombine(vecs[ia],vecs[ib],gate))-apply(P,recombine(apply(P,vecs[ia]),apply(P,vecs[ib]),gate))))
    return {"generated_pair_tests":len(rows),"generated_gap_max":float(np.max(rows)),
            "generated_gap_mean":float(np.mean(rows)),"generated_gap_median":float(np.median(rows))}

base=build_base(); P,u,resn=H4_residual_projection(base)
PB4=[apply(P,v) for v in base["branches"]]; PO3=[apply(P,v) for v in base["O3"]]; PH4=apply(P,base["H4"])
h4_res_after,h4_res_after_norm=residual_to_span(PH4,PB4+PO3)
pair_rows=pair_faithfulness(P,base); nested_rows=nested_bracketing_faithfulness(P,base)
random_audit=random_composite_faithfulness(P,base); algebra_audit=algebra_generator_audit(P,base)
all_pair_max=max(r["gap"] for r in pair_rows); all_nested_max=max(r["gap"] for r in nested_rows)
construction_depends_on_H4=True; construction_natural=False
passes_branch_proxy=(rank(PB4)==4 and rank(PB4+PO3)==8 and min(norm(v) for v in PB4)>EPS and min(norm(v) for v in PO3)>EPS)
erases_H4=(rank(PB4+PO3+[PH4])==rank(PB4+PO3)) or h4_res_after_norm<=1e-7
pair_faithful=all_pair_max<=1e-7; nested_faithful=all_nested_max<=1e-7
generated_faithful=algebra_audit["generated_gap_max"]<=1e-7 and random_audit["random_composite_gap_max"]<=1e-7
strict_admissible=bool(passes_branch_proxy and pair_faithful and nested_faithful and generated_faithful and construction_natural)
if erases_H4 and not strict_admissible and construction_depends_on_H4: verdict="H4_ERASURE_PROJECTION_INADMISSIBLE_POSTHOC"
elif erases_H4 and strict_admissible: verdict="H4_ERASURE_PROJECTION_TRUE_ADMISSIBLE_COUNTEREXAMPLE"
else: verdict="H4_ERASURE_PROJECTION_UNRESOLVED"

print("VERDICT:",verdict)
print(f"baseline rank(B4+O3)={rank(base['branches']+base['O3'])}  rank(B4+O3+H4)={rank(base['branches']+base['O3']+[base['H4']])}")
print(f"H4 residual to B4+O3 (before) = {resn:.6e}")
print(f"after projection: rank(PB4+PO3)={rank(PB4+PO3)}  rank(+PH4)={rank(PB4+PO3+[PH4])}  H4 resid after={h4_res_after_norm:.3e}  erases_H4={erases_H4}")
print(f"pair_gap_max={all_pair_max:.3e}  nested_gap_max={all_nested_max:.3e}")
print(f"random_composite_gap_max={random_audit['random_composite_gap_max']:.3e}")
print(f"generated_gap_max={algebra_audit['generated_gap_max']:.6e}  generated_gap_mean={algebra_audit['generated_gap_mean']:.6e}")
print(f"passes_branch_proxy={passes_branch_proxy} pair_faithful={pair_faithful} nested_faithful={nested_faithful} generated_faithful={generated_faithful}")
