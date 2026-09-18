from __future__ import annotations

import argparse
import csv
import hashlib
import itertools
import json
import math
import statistics
from pathlib import Path

TARGETS=("1VII","1L2Y","1UAO")
SEEDS=tuple(range(6))
MODES=("recovered_state_gate","fixed_step99_lockin","static_lockin","compaction_only")
CONTROLS=("fixed_step99_lockin","static_lockin","compaction_only")
EXPECTED_STEPS=2000

def _bool(value) -> bool:
    if isinstance(value,bool):
        return value
    return str(value).strip().lower() in {"1","true","yes"}

def exact_sign_flip_p(differences):
    values=[float(v) for v in differences]
    if not values:
        raise ValueError("empty differences")
    observed=abs(sum(values)/len(values))
    extreme=0
    total=1<<len(values)
    for bits in range(total):
        signed=0.0
        for i,value in enumerate(values):
            signed += value if ((bits>>i)&1) else -value
        statistic=abs(signed/len(values))
        if statistic + 1e-15 >= observed:
            extreme += 1
    return extreme/total

def holm_three(p_values):
    vals=[float(x) for x in p_values]
    if len(vals)!=3:
        raise ValueError("holm_three requires exactly 3 p-values")
    order=sorted(range(3),key=lambda i:vals[i])
    adjusted=[0.0]*3
    running=0.0
    for rank,idx in enumerate(order):
        value=min(1.0,(3-rank)*vals[idx])
        running=max(running,value)
        adjusted[idx]=running
    return tuple(adjusted)

def _mean(rows,key):
    return statistics.mean(float(r[key]) for r in rows)

def recompute(rows, *, precertified_prerequisites=True):
    observed=[(str(r["target"]),int(r["seed"]),str(r["mode"])) for r in rows]
    expected=[(t,s,m) for t in TARGETS for s in SEEDS for m in MODES]
    complete=(len(observed)==72 and len(set(observed))==72 and set(observed)==set(expected))
    if not complete:
        return {
            "decision":"NO_GO_RECOVERED_TOPOLOGY_GATED_PREORGANIZATION",
            "conditions":{"complete_unique_72_run_matrix":False},
            "primary_comparisons":[],
        }

    pooled={}
    for mode in MODES:
        pooled[mode]=_mean([r for r in rows if r["mode"]==mode],"final_topk_native_contact_precision")

    index={(r["target"],int(r["seed"]),r["mode"]):r for r in rows}
    comparisons=[]
    raw=[]
    target_deltas={}
    for control in CONTROLS:
        diffs=[]
        by_target={t:[] for t in TARGETS}
        for target in TARGETS:
            for seed in SEEDS:
                c=float(index[(target,seed,"recovered_state_gate")]["final_topk_native_contact_precision"])
                b=float(index[(target,seed,control)]["final_topk_native_contact_precision"])
                d=c-b
                diffs.append(d)
                by_target[target].append(d)
        p=exact_sign_flip_p(diffs)
        raw.append(p)
        target_deltas[control]={t:statistics.mean(by_target[t]) for t in TARGETS}
        comparisons.append({
            "comparison":f"recovered_state_gate_vs_{control}",
            "n_pairs":len(diffs),
            "candidate_minus_control_mean_precision":statistics.mean(diffs),
            "candidate_minus_control_median_precision":statistics.median(diffs),
            "candidate_wins":sum(d>0 for d in diffs),
            "ties":sum(d==0 for d in diffs),
            "raw_exact_sign_flip_p":p,
            **{f"{t}_mean_delta_precision":statistics.mean(by_target[t]) for t in TARGETS},
        })
    adjusted=holm_three(raw)
    for row,p in zip(comparisons,adjusted):
        row["holm_adjusted_p"]=p

    candidate=[r for r in rows if r["mode"]=="recovered_state_gate"]
    final_by_target={}
    start_by_target={}
    rg_median={}
    for target in TARGETS:
        subset=[r for r in candidate if r["target"]==target]
        final_by_target[target]=_mean(subset,"final_topk_native_contact_precision")
        start_by_target[target]=_mean(subset,"start_topk_native_contact_precision")
        rg_median[target]=statistics.median(float(r["final_rg_ratio"]) for r in subset)

    conditions={
        "complete_unique_72_run_matrix":complete,
        "candidate_highest_pooled_mean_primary_precision":
            all(pooled["recovered_state_gate"]>pooled[m] for m in CONTROLS),
        "candidate_beats_every_control_on_every_target":
            all(target_deltas[c][t]>0.0 for c in CONTROLS for t in TARGETS),
        "all_three_holm_adjusted_p_lt_0_05":
            all(p<0.05 for p in adjusted),
        "candidate_improves_from_start_on_every_target":
            all(final_by_target[t]>start_by_target[t] for t in TARGETS),
        "all_candidate_trajectories_exercise_lockin":
            all(_bool(r["transitioned_to_lockin"]) and int(r["lockin_active_steps"])>0 for r in candidate),
        "candidate_rg_ratio_gate_every_target":
            all(0.75<=rg_median[t]<=1.25 for t in TARGETS),
        "all_runs_preserve_canonical_covalent_geometry":
            all(float(r["max_bond_length_drift_A"])<1e-8 and float(r["max_bond_angle_drift_rad"])<1e-8 for r in rows),
        "all_runs_numerically_healthy":
            all((not _bool(r["failed"])) and int(r["final_step"])==EXPECTED_STEPS and
                math.isfinite(float(r["final_topk_native_contact_precision"])) and
                math.isfinite(float(r["final_rg_ratio"])) for r in rows),
        "precertified_native_firewall_and_source_integrity":
            bool(precertified_prerequisites),
    }
    decision=("GO_RECOVERED_TOPOLOGY_GATED_PREORGANIZATION"
              if all(conditions.values())
              else "NO_GO_RECOVERED_TOPOLOGY_GATED_PREORGANIZATION")
    return {
        "decision":decision,
        "conditions":conditions,
        "pooled_primary_precision_mean":pooled,
        "candidate_target_final_primary_mean":final_by_target,
        "candidate_target_start_primary_mean":start_by_target,
        "candidate_target_rg_ratio_median":rg_median,
        "primary_comparisons":comparisons,
    }

def verify_sha256sums(directory:Path):
    sums=directory/"SHA256SUMS.txt"
    if not sums.exists():
        raise AssertionError("missing SHA256SUMS.txt")
    verified={}
    for line in sums.read_text(encoding="utf-8").splitlines():
        digest,name=line.split(None,1)
        name=name.strip()
        data=(directory/name).read_bytes()
        actual=hashlib.sha256(data).hexdigest()
        if actual!=digest:
            raise AssertionError(f"hash mismatch: {name}")
        verified[name]=actual
    return verified

def verify_manifest(directory:Path):
    manifest=json.loads((directory/"p8b_run_manifest.json").read_text(encoding="utf-8"))
    assert manifest["targets"]==list(TARGETS)
    assert manifest["seeds"]==list(SEEDS)
    assert manifest["modes"]==list(MODES)
    assert manifest["steps"]==EXPECTED_STEPS
    assert manifest["native_information_used_in_objective"] is False
    assert manifest["native_information_used_in_controller"] is False
    assert manifest["common_random_initial_torsions"] is True
    return manifest

def verify_directory(directory:Path):
    hashes=verify_sha256sums(directory)
    manifest=verify_manifest(directory)
    with (directory/"p8b_results.csv").open(newline="",encoding="utf-8") as f:
        rows=list(csv.DictReader(f))
    independent=recompute(rows,precertified_prerequisites=True)
    generated=json.loads((directory/"p8b_acceptance.json").read_text(encoding="utf-8"))
    return {
        "artifact_hashes_verified":True,
        "manifest_verified":True,
        "generated_decision":generated["decision"],
        "independent":independent,
        "decision_matches_generated":independent["decision"]==generated["decision"],
        "verified_file_hashes":hashes,
        "git_head":manifest.get("git_head"),
    }

def main():
    p=argparse.ArgumentParser()
    p.add_argument("artifact_directory",type=Path)
    args=p.parse_args()
    print(json.dumps(verify_directory(args.artifact_directory),indent=2,sort_keys=True))

if __name__=="__main__":
    main()
