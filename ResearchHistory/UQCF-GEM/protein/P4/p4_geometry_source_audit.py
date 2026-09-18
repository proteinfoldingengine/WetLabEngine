#!/usr/bin/env python3
import ast, hashlib, importlib.util, json
from pathlib import Path
import numpy as np

ROOT=Path(__file__).resolve().parent
SRC=ROOT/"recovered_patch630"
EXPECTED=json.load(open(ROOT/"SOURCE_MANIFEST.json"))["source_sha256"]

def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def summ(x,t):
    x=np.asarray(x,float); e=np.abs(x-t)
    return {"n":int(x.size),"min":float(x.min()),"max":float(x.max()),"mean":float(x.mean()),
            "rmse_to_declared":float(np.sqrt(np.mean((x-t)**2))),
            "min_abs_error_to_declared":float(e.min()),
            "within_0p1A":int(np.sum(e<=0.1))}
def angles(a,b,c):
    u=a-b; v=c-b
    u=u/np.linalg.norm(u,axis=1,keepdims=True); v=v/np.linalg.norm(v,axis=1,keepdims=True)
    return np.arccos(np.clip((u*v).sum(1),-1,1))
def load_generate_ideal_backbone():
    text=(SRC/"protein_model.py").read_text()
    tree=ast.parse(text)
    fn=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=="_generate_ideal_backbone")
    mod=ast.Module(body=[fn],type_ignores=[])
    ast.fix_missing_locations(mod)
    ns={"np":np}
    exec(compile(mod,str(SRC/"protein_model.py"),"exec"),ns)
    return ns["_generate_ideal_backbone"]
def contract():
    ft=(SRC/"force_field.py").read_text(); mt=(SRC/"main.py").read_text(); pt=(SRC/"protein_model.py").read_text()
    tree=ast.parse(ft); calc=next(n for c in tree.body if isinstance(c,ast.ClassDef) and c.name=="ForceField"
        for n in c.body if isinstance(n,ast.FunctionDef) and n.name=="calculate_total_force_loss")
    args=[a.arg for a in calc.args.args]
    pmtree=ast.parse(pt); declared=False; loads=0
    for n in ast.walk(pmtree):
        if isinstance(n,ast.Assign):
            for t in n.targets:
                if isinstance(t,ast.Tuple):
                    names=[e.id if isinstance(e,ast.Name) else None for e in t.elts]
                    if "C_N_dist" in names and isinstance(n.value,ast.Tuple):
                        v=n.value.elts[names.index("C_N_dist")]
                        declared=isinstance(v,ast.Constant) and float(v.value)==1.33
        if isinstance(n,ast.Name) and n.id=="C_N_dist" and isinstance(n.ctx,ast.Load): loads+=1
    explicit=any(isinstance(n,ast.FunctionDef) and any(k in n.name.lower() for k in ("covalent","bond_length","peptide_bond")) for n in ast.walk(tree))
    return {"generator_declares_C_N_dist_1p33":declared,"generator_uses_C_N_dist_after_declaration":loads>0,
      "forcefield_args":args,"forcefield_receives_N_coords":"n_coords" in args or "N_coords" in args,
      "forcefield_receives_C_coords":"c_coords" in args or "C_coords" in args,
      "main_passes_CA_as_force_coordinates":"force_field.calculate_total_force_loss(\n        ca_coords" in mt,
      "main_computes_phi_psi_from_N_CA_C":"compute_true_phi_psi(n_coords, ca_coords, c_coords)" in mt,
      "explicit_covalent_bond_force_function_present":explicit}
def audit():
    got={k:sha(SRC/k) for k in EXPECTED}; match={k:got[k]==EXPECTED[k] for k in EXPECTED}
    if not all(match.values()): raise RuntimeError("source hash mismatch")
    generate=load_generate_ideal_backbone(); n,ca,c=generate(36,42)
    nca=np.linalg.norm(n-ca,axis=1); cac=np.linalg.norm(ca-c,axis=1); cn=np.linalg.norm(c[:-1]-n[1:],axis=1)
    cnang=angles(ca[:-1],c[:-1],n[1:]); ct=contract()
    bad_cn=bool(np.all(np.abs(cn-1.33)>1.0))
    no_enforce=(not ct["explicit_covalent_bond_force_function_present"] and not ct["forcefield_receives_N_coords"]
      and not ct["forcefield_receives_C_coords"] and ct["main_passes_CA_as_force_coordinates"])
    verdict="NO_GO_HISTORICAL_PHYSICAL_BACKBONE_INTERPRETATION" if bad_cn and no_enforce else "UNRESOLVED_PHYSICAL_BACKBONE_VALIDITY"
    return {"schema":"protein-p4-patch630-geometry-source-audit-v1","source_hash_match":match,
      "historical_initializer":{"N_CA":summ(nca,1.46),"N_CA_interior":summ(nca[1:-1],1.46),
       "CA_C":summ(cac,1.53),"CA_C_interior":summ(cac[1:-1],1.53),"C_N_peptide":summ(cn,1.33),
       "CA_C_Nnext_rad":summ(cnang,2.03)},
      "source_contract":ct,
      "gate_conditions":{"all_35_peptide_C_N_links_more_than_1A_from_declared_1p33A":bad_cn,
                         "historical_force_objective_has_no_covalent_N_CA_C_enforcement":no_enforce},
      "verdict":verdict,
      "claim_boundary":"Rejects only the historical physical-backbone interpretation; constrained/kinematic prospective work remains open."}
if __name__=="__main__": print(json.dumps(audit(),indent=2,sort_keys=True))
