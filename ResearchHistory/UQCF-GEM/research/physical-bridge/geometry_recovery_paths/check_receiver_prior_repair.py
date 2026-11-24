"""Check the pre-event receiver sufficiency theorem on the original 25-chart geometry."""
import argparse
from collections import Counter, defaultdict
from fractions import Fraction as F
import importlib.util
from itertools import combinations
import json
import lzma
from math import lcm
import os
from pathlib import Path
import sys
from unittest.mock import patch

import numpy as np
from check_receiver_command import FIXTURE, PINS, hash_blob
from check_fixed_geometry_source_gain import (
    bitset_outcomes, commands_by_column, commands_by_row, digest, incidence_outcomes,
    p1_values, raw, traced_run,
)
from check_source_gain_field import DRIVER, PIN, centered, exact_solve


def cut_coefficient(support, q):
    a,k,i,j=q
    delta=lambda u,v:int((u in support)!=(v in support))
    return (delta(a,i)+delta(k,j)-delta(a,k)-delta(i,j))//2


def quartet_value(work, q):
    a,k,i,j=q
    return F(work[a][i]+work[k][j]-work[a][k]-work[i][j],2)


def cone_sums(parents,row,values):
    sub=dict(zip(row,values,strict=True))
    for v in reversed(row):
        if v:
            sub[parents[v]]+=sub[v]
    return sub


def receiver_estimate(q, coefficients, work, local_cones):
    # coefficients below contain only registered receiver-held sites
    return quartet_value(work,q)-sum(c*local_cones[v]**2 for v,c in coefficients)


def make_factorial(features,labels,s,u):
    """Keep the historical work exactly via ordinary cut groups on the five U holders."""
    grades=[g for _,g,_ in features]
    grades[1],grades[2]=s,u
    loss=8-s*s-u*u
    if not loss:
        return grades
    group=defaultdict(list)
    for v,(_,_,h) in enumerate(features[6:],6):
        group[tuple(sorted(labels-h))].append(v)
    q=sorted(features[2][2])
    for pair in combinations(q,2):
        ids=group[pair]
        if loss==6 and [grades[v] for v in ids]==[5,3,1]:
            replacement=[6,2,1]
        else:
            replacement=[grades[v] for v in ids]
            for _ in range(loss//3):
                replacement[replacement.index(1)]=2
        assert sum(x*x for x in replacement)-sum(grades[v]**2 for v in ids)==loss
        for v,g in zip(ids,replacement,strict=True):
            grades[v]=g
    versions={(3,(15,3,1,1)):(12,9,1,1),(3,(16,5,1,1)):(16,4,1,1),
              (6,(15,3,1,1)):(14,3,3,2),(6,(16,5,1,1)):(16,2,2,1)}
    for label in q:
        ids=group[(label,)]
        replacement=versions[loss,tuple(grades[v] for v in ids)]
        assert sum(x*x for x in replacement)-sum(grades[v]**2 for v in ids)==-3*loss
        for v,g in zip(ids,replacement,strict=True):
            grades[v]=g
    assert min(grades)>0
    return grades


def desired_stars(labels, post, threshold):
    near={p for p in combinations(labels,2) if post[p[0]][p[1]]==threshold}
    out={}
    for i in labels:
        residual=Counter(k for p in near if i not in p for k in p)
        want=[k for k in labels if k!=i and residual[k]==3]
        if len(want)==4 and all(residual[k] in (3,4) for k in labels if i!=k):
            out[i]=want
    return out


def run(sources, dest, mode):
    os.chdir(sources)
    assert hash_blob(FIXTURE.read_bytes())==PINS[FIXTURE] and hash_blob(DRIVER.read_bytes())==PIN
    sys.path.insert(0,str(FIXTURE.parent.resolve()))
    import check_geometry_repair as f
    modules=f.modules()
    spec=importlib.util.spec_from_file_location("pruning_response",DRIVER)
    response=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(response)
    plain,target=f.fixture()
    parents,original,support=map(tuple,zip(*plain))
    a,b,t,u=f.A,f.B,f.T,f.ULEAF
    labels=f.LABELS
    initial=f.initial_state(plain)
    source_event=modules["atom"].atomic(parents,initial,a,t)
    modules["verify"].verify_atomic(source_event)
    source=tuple(map(tuple,source_event["after"]))
    menu1,menu2=commands_by_row(source,parents),commands_by_column(source,parents)
    assert menu1==menu2 and len(set(menu1))==len(menu1)==32575
    menu=menu1 if mode=="incidence" else menu2
    na,nb=f.grid()[a],f.grid()[b]
    assert set(support[t])==f.ALL-({b}|nb) and set(support[u])=={b}|nb
    assert set(support[f.R])=={a}|nb and set(support[f.CHILD])=={a}
    assert all(len(f.ALL-h)<=2 for h in support[6:])
    assert all(target[a][i]==f.MU+4 for i in nb) and target[a][b]==f.MU+14
    assert max(len(na-support[v]) for i,v in menu if i==a)<=2
    assert [v for i,v in menu if i==b and not (na & support[v])]==[u]
    assert all(target[b][j]==f.MU+4 for j in na)
    pairs=list(combinations(labels,2))
    assert min(sum(a not in e and i not in e and target[e[0]][e[1]]==f.MU for e in pairs) for i in labels)==42
    qs=[(a,k,i,j) for k in sorted(f.ALL-{a,b}-nb) for i,j in combinations(sorted(nb),2)]
    key_q=(0,1,7,11)
    patterns={}
    full_q=[]
    for q in qs:
        aa,k,i,j=q
        items=[(v,cut_coefficient(h,q)) for v,h in enumerate(support) if cut_coefficient(h,q)]
        by_product=[(v,(int(aa in h)-int(j in h))*(int(k in h)-int(i in h))) for v,h in enumerate(support)]
        assert items==[(v,c) for v,c in by_product if c]
        assert [(v,c) for v,c in items if b not in support[v]]==[(t,1)]
        patterns[q]=[(v,c) for v,c in items if b in support[v]]
        full_q.append(dict(labels=q,contrast=str(quartet_value(target,q)),receiver_terms=patterns[q]))
    assert len(qs)==len(set(qs))==114 and quartet_value(target,key_q)==8
    keys=[()]
    for v in range(1,len(parents)):
        keys.append(keys[parents[v]]+(v,))
    lin=modules["lineage"]
    fine=lin.Carrier("recovery-test",tuple(keys))
    cb=lin.Carrier(fine.genesis,tuple(keys[v] for v in initial[b]))
    pb=lin.Pruning(fine,cb)
    cases={"archive":list(original)}
    for name,s,u0 in (("low5",F(2,5),F(14,5)),("high5",F(14,5),F(2,5)),
                        ("low17",F(14,17),F(46,17)),("high17",F(46,17),F(14,17))):
        g=list(original)
        g[t],g[u],g[0]=s,u0,5-s-u0
        cases[name]=g
    for s,u0 in ((1,2),(2,1),(1,1)):
        cases[f"factor_{s}_{u0}"]=make_factorial(plain,f.ALL,s,u0)
    g=list(original)
    g[160],g[161]=g[161],g[160]
    assert support[160]==support[161]==f.ALL-{1,b} and (g[160],g[161])==(3,5)
    cases["swapped"]=g
    g=list(original)
    g[t],g[0]=1,2
    cases["uncalibrated"]=g
    out=dict(charts=len(labels),keys=len(parents),legal=len(menu),menu_sha256=digest(menu),
             quartet_count=len(qs),reference_quartet=key_q,reference_contrast="8",
             reference_receiver_terms=patterns[key_q],calibration_sha256=digest(target),cases={})
    bulk=dict(commands=menu,quartets=full_q,cases={})
    b_prior={}
    w_post={}
    mean_fields={}
    numerical_errors={}
    sentinel_calls=[]
    def forbidden(*args):
        sentinel_calls.append(True)
        raise RuntimeError("counting-fiber mean interception")
    with patch.object(response,"aggregate",forbidden):
        try:
            response.run()
        except RuntimeError as exc:
            assert str(exc)=="counting-fiber mean interception"
        else:
            raise AssertionError("Historical field routine failed to reach the rejecting control")
    assert len(sentinel_calls)==1
    for name,grades in cases.items():
        feat=[(p,g,h) for p,g,h in zip(parents,grades,support,strict=True)]
        all_totals=cone_sums(parents,tuple(range(len(parents))),grades)
        squares=[all_totals[v]**2 for v in range(len(parents))]
        before=f.work_for(initial,squares)
        after=f.work_for(source,squares)
        b_prior[name]=pb.aggregate(grades)
        cones=cone_sums(parents,initial[b],b_prior[name])
        assert all(all_totals[v]==cones[v] for v in initial[b])
        vals=[receiver_estimate(q,patterns[q],before,cones) for q in qs]
        assert len(set(vals))==1 and vals[0]==grades[t]**2
        u2=cones[u]**2
        assert u2==grades[u]**2
        subtotal_term=sum(c*cones[v]**2 for v,c in patterns[key_q])
        item=dict(source_square=str(vals[0]),receiver_square=str(u2),receiver_term=str(subtotal_term),
                  ordinary_receiver_balance=str(subtotal_term-u2),
                  receiver_prior_sha256=digest(list(map(str,b_prior[name]))),
                  initial_work_matches=(before==target),post_work_sha256=digest([[str(x) for x in row] for row in after]))
        out["cases"][name]=item
        w_post[name]=after
        compact=dict(fine_changes=[[i,str(g)] for i,g in enumerate(grades) if g!=original[i]],
                     receiver_grade=list(map(str,b_prior[name])),quartet_estimates=list(map(str,vals)))
        bulk["cases"][name]=compact
        if name=="uncalibrated":
            assert before!=target and b_prior[name]==b_prior["archive"] and vals[0]==1
            item["incorrect_if_old_geometry_substituted"]=str(receiver_estimate(key_q,patterns[key_q],target,cones))
            assert item["incorrect_if_old_geometry_substituted"]=="4"
            continue
        assert before==target
        assert (subtotal_term-u2==0 and u2==4)==(vals[0]==u2==4)
        predicted=[[b,u]] if vals[0]==u2==4 else []
        scale=lcm(*(F(w).denominator for w in squares))
        weights=[int(w*scale) for w in squares]
        work_units=[[int(v*scale) for v in row] for row in after]
        scores=(incidence_outcomes(source,weights,work_units,menu) if mode=="incidence" else bitset_outcomes(source,weights,menu))
        compact["scale"],compact["all_outcomes"]=scale,scores
        eligible=[list(e) for e,sc in zip(menu,scores,strict=True) if sc[2]==len(labels)]
        assert eligible==predicted
        if vals[0]==4:
            stars=desired_stars(labels,after,f.MU)
            assert stars=={a:sorted(na),b:sorted(na)}
            item["possible_stars"]={str(i):n for i,n in stars.items()}
        # The canonical module is available, and any attempted historical use of its mean must fail.
        with patch.dict(sys.modules,{"pruning_response":response}),patch.object(response,"aggregate",forbidden):
            traced=traced_run(f,modules,feat,target)
        assert len(sentinel_calls)==1 and traced["same_work_object"]
        assert traced["verified"]==[[a,t]]+predicted and traced["raw_source_event_sha256"]==digest(source_event)
        item.update(predicted=predicted,actual=traced["verified"][1:],exit=traced["exit"],mean_calls_in_writer=0)
        if name in ("archive","swapped","factor_2_1"):
            # Original grade-fiber push and NumPy field solve/mean on the same actual source chart.
            va,_,ca,cc=p1_values(lin,keys,initial,source,grades,a)
            pf=exact_solve(ca.keys,va)
            idx={k:i for i,k in enumerate(ca.keys)}
            avg=[pf[idx[k]] for k in cc.keys]
            avg[0]=(pf[0]+pf[idx[keys[t]]])/2
            mean=centered(avg)
            numerical=response.aggregate(response.solve(ca.keys,np.array(va,dtype=float)),ca.keys,cc.keys)
            error=float(np.max(np.abs(numerical-np.array(mean,dtype=float))))
            assert error<1e-8
            numerical_errors[name]=error
            mean_fields[name]=mean
            i,j=cc.keys.index(keys[160]),cc.keys.index(keys[161])
            item["source_mean_160_minus_161"]=str(mean[i]-mean[j])
            compact["source_mean"]=list(map(str,mean))
    assert b_prior["swapped"]==b_prior["archive"] and w_post["swapped"]==w_post["archive"]
    assert w_post["factor_2_1"]==w_post["archive"] and w_post["factor_1_1"]==w_post["factor_1_2"]
    assert b_prior["factor_2_1"]!=b_prior["archive"]
    diff=F(out["cases"]["swapped"]["source_mean_160_minus_161"])-F(out["cases"]["archive"]["source_mean_160_minus_161"])
    assert diff==-4 and mean_fields["archive"]!=mean_fields["swapped"]
    out["source_mean_swap_contrast_change"]=str(diff)
    verified_cones=cone_sums(parents,initial[b],b_prior["archive"])
    terms=patterns[key_q]
    omit=[(v,c) for v,c in terms if v!=u]
    wrong_sign=[(v,-c if v==u else c) for v,c in terms]
    assert receiver_estimate(key_q,terms,target,verified_cones)==4
    out["rejecting_controls"]=dict(missing_or_duplicated_command=(menu[:-1]!=menu2 and menu+[menu[0]]!=menu2),
        substituted_command=([(a,0)]+menu[1:]!=menu2),faulty_work_only_prediction=(w_post["factor_2_1"]==w_post["archive"]
        and out["cases"]["factor_2_1"]["actual"]!=out["cases"]["archive"]["actual"]),
        stale_quartet=(out["cases"]["uncalibrated"]["incorrect_if_old_geometry_substituted"]!=out["cases"]["uncalibrated"]["source_square"]),
        field_trap_reached_on_original_field_run=(len(sentinel_calls)==1),
        wrong_receiver_sign=receiver_estimate(key_q,wrong_sign,target,verified_cones)!=4,
        omitted_receiver_leaf=receiver_estimate(key_q,omit,target,verified_cones)!=4)
    assert all(out["rejecting_controls"].values())
    domain=raw(bulk)+b"\n"
    import hashlib
    out["universe_sha256"]=hashlib.sha256(domain).hexdigest()
    dest.mkdir(parents=True,exist_ok=True)
    (dest/"receiver_prior_universe.json.xz").write_bytes(lzma.compress(domain,preset=6))
    (dest/"receiver_prior_certificate.json").write_text(json.dumps(out,indent=2,sort_keys=True)+"\n")
    (dest/"receiver_prior_numeric.log").write_text(json.dumps(numerical_errors,indent=2,sort_keys=True)+"\n")
    return {k:(v["source_square"],v["receiver_square"],v.get("actual")) for k,v in out["cases"].items()}


if __name__=="__main__":
    if not __debug__:
        raise RuntimeError("Use enabled scientific assertions")
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("sources",type=Path)
    parser.add_argument("dest",type=Path)
    parser.add_argument("--mode",choices=["incidence","bitsets"],default="incidence")
    args=parser.parse_args()
    print(json.dumps(run(args.sources.resolve(),args.dest.resolve(),args.mode),sort_keys=True))
