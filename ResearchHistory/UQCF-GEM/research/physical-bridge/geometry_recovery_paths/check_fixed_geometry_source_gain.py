"""Compare one-step geometry repairs at fixed starting work using exact positive P1 grades."""
import argparse
from collections import Counter, defaultdict
from contextlib import ExitStack
from fractions import Fraction as F
from hashlib import sha256
from itertools import combinations
import json
import lzma
from math import lcm
import os
from pathlib import Path
import sys
from tempfile import TemporaryDirectory
import traceback
from unittest.mock import patch

from check_receiver_command import FIXTURE, PINS, hash_blob


def raw(obj):
    return json.dumps(obj,separators=(",",":"),sort_keys=True).encode()


def digest(obj):
    return sha256(raw(obj)).hexdigest()


def integer_if_exact(q):
    return int(q) if q.denominator==1 else q


def commands_by_row(rows, parents):
    menu=[]
    for i,row in enumerate(rows):
        other=set().union(*(set(r) for j,r in enumerate(rows) if i!=j))
        internal={parents[v] for v in row if v}
        menu.extend((i,v) for v in row if v and v in other and v not in internal)
    return menu


def commands_by_column(rows, parents):
    holders=defaultdict(set)
    children=defaultdict(list)
    for v in range(1,len(parents)):
        children[parents[v]].append(v)
    for i,row in enumerate(rows):
        for v in row:
            holders[v].add(i)
    return sorted((i,v) for v,s in holders.items() if v and len(s)>1 for i in s
                  if not any(i in holders[w] for w in children[v]))


def incidence_outcomes(rows, square_units, work_units, menu):
    """Use membership signs to update one row, then count degrees at the unrestricted minimum."""
    ids=range(len(rows))
    sets=list(map(set,rows))
    pairs=list(combinations(ids,2))
    outside={}
    for i in ids:
        keep=[(work_units[j][k],j,k) for j,k in pairs if i not in (j,k)]
        m=min(w for w,j,k in keep)
        hits=[(j,k) for w,j,k in keep if w==m]
        outside[i]=m,Counter(v for e in hits for v in e),len(hits)
    records=[]
    for i,v in menu:
        m,base,count=outside[i]
        changes=[(work_units[i][j]+(square_units[v] if v in sets[j] else -square_units[v]),j)
                 for j in ids if i!=j]
        level=min(m,min(w for w,j in changes))
        d=base.copy() if level==m else Counter()
        edges=count if level==m else 0
        for w,j in changes:
            if w==level:
                d[j]+=1
                d[i]+=1
                edges+=1
        records.append([level,edges,sum(n==4 for n in d.values())])
    return records


def bitset_outcomes(rows, square_units, menu):
    """Derive distances directly from row masks and degree counts from a mask of all minimizing pairs."""
    ids=range(len(rows))
    masks=[sum(1<<v for v in row if v) for row in rows]
    classes=defaultdict(int)
    for v,w in enumerate(square_units):
        if v:
            classes[w]|=1<<v
    buckets=list(classes.items())
    def distance(delta):
        return sum(w*(delta & group).bit_count() for w,group in buckets)
    pairs=list(combinations(ids,2))
    flags={(i,j):1<<k for k,(i,j) in enumerate(pairs)}
    flags.update({(j,i):mask for (i,j),mask in tuple(flags.items())})
    incidence=[sum(flags[i,j] for j in ids if j!=i) for i in ids]
    immutable={(i,j):distance(masks[i]^masks[j]) for i,j in pairs}
    outside={}
    incident_pairs={}
    for i in ids:
        pool=[(w,flags[a,b]) for (a,b),w in immutable.items() if i not in (a,b)]
        low=min(w for w,e in pool)
        outside[i]=low,sum(e for w,e in pool if w==low)
        incident_pairs[i]=[(masks[i]^masks[j],flags[i,j]) for j in ids if j!=i]
    records=[]
    for i,v in menu:
        low,edges=outside[i]
        bit=1<<v
        for old,e in incident_pairs[i]:
            value=distance(old^bit)
            if value < low:
                low,edges=value,e
            elif value==low:
                edges|=e
        records.append([low,edges.bit_count(),sum((edges&m).bit_count()==4 for m in incidence)])
    return records


def traced_run(f, modules, features, target):
    """Record exact original call arguments and return values without changing selector/primitive logic."""
    state={"calls":[],"verified":[],"aggregate_before_second":0}
    tables=[]
    work,select=f.work_for,f.degree_candidates
    atom,verify=modules["atom"].atomic,modules["verify"].verify_atomic
    cls=modules["lineage"].Pruning
    aggregate=cls.aggregate
    def measured_work(*args):
        obj=work(*args)
        tables.append(obj)
        return obj
    def selection(feats,after,work_arg,squares):
        state["same_work_object"]=(len(tables)==2 and work_arg is tables[1])
        state["minimum_seen"]=str(f.edges(work_arg)[0])
        counts,candidates=select(feats,after,work_arg,squares)
        state["available"]=sum(counts.values())
        state["candidate_return"]=[list(item) for item in candidates]
        return counts,candidates
    def observe_atom(p,before,i,v):
        if len(state["verified"])<2:
            state["calls"].append([i,v])
        event=atom(p,before,i,v)
        if not state["verified"]:
            state["raw_source_event_sha256"]=digest(event)
        return event
    def observe_verify(event):
        result=verify(event)
        if len(state["verified"])<2:
            state["verified"].append([event["index"],event["leaf"]])
        return result
    def observe_grade(mapping,values):
        if len(state["verified"])<2:
            state["aggregate_before_second"]+=1
        return aggregate(mapping,values)
    with TemporaryDirectory() as tmp, ExitStack() as stack:
        for obj,attr,replacement in ((f,"fixture",lambda:(features,target)),(f,"modules",lambda:modules),
               (f,"work_for",measured_work),(f,"degree_candidates",selection),
               (modules["atom"],"atomic",observe_atom),(modules["verify"],"verify_atomic",observe_verify),
               (cls,"aggregate",observe_grade)):
            stack.enter_context(patch.object(obj,attr,replacement))
        try:
            actual=f.run(Path(tmp))
        except AssertionError as error:
            frame=traceback.extract_tb(error.__traceback__)[-1]
            assert Path(frame.filename).resolve()==FIXTURE.resolve()
            reasons={"assert minimum == MU":"minimum guard",
                     "assert candidates == [(B,ULEAF)], candidates":"singleton guard"}
            state["exit"]=reasons[frame.line.strip()]
        else:
            state["exit"]="completed"
            state["receiver_root"]=actual["receiver_root_grade"]
            state["face_invariant"]=actual["face_invariant"]
    return state


def p1_values(lineage,keys,initial,source,grades,a):
    fine=lineage.Carrier("recovery-test",tuple(keys))
    def chart(row):
        return lineage.Carrier(fine.genesis,tuple(keys[v] for v in row))
    before,after=chart(initial[a]),chart(source[a])
    first=lineage.Pruning(fine,before)
    second=lineage.Pruning(before,after)
    before_values=first.aggregate(grades)
    out=second.aggregate(before_values)
    assert out==first.then(second).aggregate(grades)
    # Independently resolve each fine address by literal parent ascent.
    sums=dict.fromkeys(after.keys,F(0))
    for key,g in zip(keys,grades,strict=True):
        while key not in sums:
            key=key[:-1]
        sums[key]+=g
    assert tuple(sums.values())==out
    return before_values,out,before,after


def verify_pair(x, target, afterwork, holder_signs):
    return all(afterwork[0][j]-target[0][j]==sign*x*x for j,sign in holder_signs)


def run(sources, dest, mode):
    os.chdir(sources)
    assert hash_blob(FIXTURE.read_bytes())==PINS[FIXTURE]
    sys.path.insert(0,str(FIXTURE.parent.resolve()))
    import check_geometry_repair as f
    modules=f.modules()
    plain, target=f.fixture()
    parents,original,_=map(tuple,zip(*plain))
    a,b,t,u=f.A,f.B,f.T,f.ULEAF
    initial=f.initial_state(plain)
    actual=modules["atom"].atomic(parents,initial,a,t)
    modules["verify"].verify_atomic(actual)
    source=tuple(map(tuple,actual["after"]))
    assert source==tuple(tuple(v for v in row if i!=a or v!=t) for i,row in enumerate(initial))
    assert plain[t][2]==f.ALL-plain[u][2] and all(p!=t and p!=u for p in parents)
    keys=[()]
    for v in range(1,len(parents)):
        keys.append(keys[parents[v]]+(v,))
    menu1=commands_by_row(source,parents)
    menu2=commands_by_column(source,parents)
    assert menu1==menu2 and len(menu1)==32575 and len(set(menu1))==len(menu1)
    menu=menu1 if mode=="incidence" else menu2
    signs=[(j,1 if t in source[j] else -1) for j in f.LABELS if j!=a]
    na,nb=f.grid()[a],f.grid()[b]
    holders=set(plain[t][2])
    assert na<=holders and f.ALL-holders==nb|{b}
    assert all(target[a][j]-f.MU==4 for j in nb) and target[a][b]-f.MU==14
    missing={v:len(na-set(plain[v][2])) for i,v in menu if i==a}
    assert len(missing)>0 and max(missing.values())<=2
    edge0={p for p in combinations(f.LABELS,2) if target[p[0]][p[1]]==f.MU}
    assert all(sum(j in pair for pair in edge0)==4 for j in f.LABELS)
    untouched_min=min(sum(a not in e and i not in e for e in edge0) for i in f.LABELS)
    assert untouched_min>0
    fixed_root=int(original[0])
    families=[("archive",F(2),F(2),0),("low5",F(2,5),F(14,5),0),("high5",F(14,5),F(2,5),0),
              ("low17",F(14,17),F(46,17),0),("high17",F(46,17),F(14,17),0),("root_only",F(2),F(2),1)]
    out=dict(archive_sha="e61d5b0e827f7b412824ad46021e2ad6cc6f7875",vertices=len(parents),charts=len(initial),
             legal=len(menu), legal_sha256=digest(menu), initial_rows_sha256=digest(initial), source_rows_sha256=digest(source),
             old_work_sha256=digest(target), holder_signs=signs,
             obstruction=dict(old_a_neighbors=sorted(na), complement_neighbors=sorted(nb),gap_to_neighbors=4,
                              gap_to_b=14, max_missing_old_neighbors=max(missing.values()),
                              untouched_minimum_edges_at_least=untouched_min),
             cases={})
    bulk=dict(commands=menu,cases={})
    source_objects={}
    before_vectors={}
    for name,s,h,root_extra in families:
        assert s*s+h*h==8 and min(s,h)>0
        grades=list(original)
        grades[t],grades[u]=integer_if_exact(s),integer_if_exact(h)
        grades[0]=integer_if_exact(F(fixed_root)+4-s-h+root_extra)
        assert grades[0]>0
        features=[(p,g,rec[2]) for p,g,rec in zip(parents,grades,plain,strict=True)]
        assert f.initial_state(features)==initial
        totals=grades[:]
        for v in range(len(parents)-1,0,-1):
            totals[parents[v]]+=totals[v]
        squares=[z*z for z in totals]
        before=f.work_for(initial,squares)
        after=f.work_for(source,squares)
        assert before==target
        old_vector,new_vector,old_carrier,new_carrier=p1_values(modules["lineage"],keys,initial,source,grades,a)
        root0,root1=old_vector[0],new_vector[0]
        assert root1-root0==s and verify_pair(s,before,after,signs)
        source_objects[name]=(new_carrier.identity,new_vector)
        before_vectors[name]=old_vector
        source_obj=digest([new_carrier.genesis,new_carrier.keys,list(map(str,new_vector))])
        if "source_carriers" not in bulk:
            bulk["source_carriers"]=dict(genesis=new_carrier.genesis,before=old_carrier.keys,after=new_carrier.keys)
        archived_pre=before_vectors["archive"]
        for index,key in enumerate(old_carrier.keys):
            expected_offset=(root_extra+2-s if key==() else s-2 if key==keys[t] else 0)
            assert old_vector[index]-archived_pre[index]==expected_offset
        scale=lcm(*(F(w).denominator for w in squares))
        weights=[int(w*scale) for w in squares]
        assert all(F(n,scale)==w for n,w in zip(weights,squares,strict=True))
        work_units=tuple(tuple(int(val*scale) for val in row) for row in after)
        if mode=="incidence":
            features_out=incidence_outcomes(source,weights,work_units,menu)
        else:
            features_out=bitset_outcomes(source,weights,menu)
        admitted=[]
        degree=[cmd for cmd,rec in zip(menu,features_out,strict=True) if rec[2]==len(f.LABELS)]
        for i,v in degree:
            endpoint=tuple(tuple(w for w in row if j!=i or w!=v) for j,row in enumerate(source))
            ew=f.work_for(endpoint,squares)
            payload=modules["projection"].Payload(f.SIDE,F(1),f.LABELS,tuple(tuple(map(F,r)) for r in ew),f.edges(ew)[1],())
            modules["carriers"].build_carrier(payload)
            admitted.append([i,v])
        trace=traced_run(f,modules,features,target)
        assert trace["same_work_object"] and trace["aggregate_before_second"]==0
        assert trace["raw_source_event_sha256"]==digest(actual)
        expected=[[b,u]] if s==2 else []
        assert admitted==expected and list(map(list,degree))==expected
        if s==2:
            assert trace["exit"]=="completed" and trace["verified"]==[[a,t],[b,u]]
        else:
            assert trace["verified"]==[[a,t]] and trace["exit"]==("minimum guard" if s>2 else "singleton guard")
            assert trace.get("candidate_return")==([] if s<2 else None)
        assert trace["calls"]==trace["verified"]
        # The minimum and all scores use exact integer units, scaled per case.
        bulk["cases"][name]=dict(scale=scale,records=features_out,
                                before_p1=list(map(str,old_vector)),after_p1=list(map(str,new_vector)))
        out["cases"][name]=dict(grades=[str(s),str(h),str(grades[0])],source_root=[str(root0),str(root1)],
                source_gain=str(root1-root0),typed_source_sha256=source_obj,after_work_sha256=digest(
                    [[str(v) for v in row] for row in after]),minimum=str(f.edges(after)[0]),
                degree_eligible=list(map(list,degree)), admitted=admitted,trace=trace, domain_sha256=digest(features_out))
    assert all(obj==source_objects["archive"] for k,obj in source_objects.items() if k!="root_only")
    assert source_objects["root_only"]!=source_objects["archive"]
    # Reject common corruptions against the independently formed reference and source relation.
    right=menu2
    controls={"missing_menu":menu1[:-1]!=right,"duplicated_menu":menu1+[menu1[0]]!=right,
              "substituted_menu":[(a,0)]+menu1[1:]!=right,
              "false_post_object_equality":source_objects["root_only"]!=source_objects["low5"],
              "false_receiver_execution":out["cases"]["low5"]["trace"]["verified"]!=[[a,t],[b,u]]}
    archive_table=f.work_for(source,[v*v for v in _subtotals(parents,original)])
    controls["false_gain"]=not verify_pair(F(3),target,archive_table,signs)
    altered=signs[:]
    j,k=altered[0]
    altered[0]=(j,-k)
    controls["wrong_holder_sign"]=not verify_pair(F(2),target,archive_table,altered)
    assert all(controls.values())
    out["rejecting_controls"]=controls
    domain=raw(bulk)+b"\n"
    out["universe_sha256"]=sha256(domain).hexdigest()
    dest.mkdir(parents=True,exist_ok=True)
    (dest/"fixed_geometry_source_gain_universe.json.xz").write_bytes(lzma.compress(domain,preset=6))
    (dest/"fixed_geometry_source_gain_certificate.json").write_text(json.dumps(out,sort_keys=True,indent=2)+"\n")
    return {k:v["trace"]["exit"] for k,v in out["cases"].items()}


def _subtotals(parents,grades):
    sums=list(grades)
    for v in reversed(range(1,len(parents))):
        sums[parents[v]]+=sums[v]
    return sums


if __name__=="__main__":
    if not __debug__:
        raise RuntimeError("Historical selectors and proof checks require enabled assertions")
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("sources",type=Path)
    parser.add_argument("destination",type=Path)
    parser.add_argument("--mode",choices=["incidence","bitsets"],default="incidence")
    args=parser.parse_args()
    print(json.dumps(run(args.sources.resolve(),args.destination.resolve(),args.mode),sort_keys=True))
