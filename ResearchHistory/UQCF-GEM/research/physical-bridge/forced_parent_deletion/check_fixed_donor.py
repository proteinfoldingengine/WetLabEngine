"""Fixed-donor six-call replay; original producer and independent exact checks."""
import copy
import hashlib
import itertools
import json
import sys
from collections import Counter
from fractions import Fraction
from pathlib import Path

import check_routed_chain as chain
import check_routed_grade as lift

P, X = chain.P, chain.X
D, B, H, J, S = 3, 1, 7, 1, 8
DEGREES = (2, 2, 2, 2)
PREPS = {"AD": (257, 63, 199, 319), "CD": (1, 63, 455, 319)}
MODES = ("delete_D", "delete_spectator", "no_external_deletion")
PINS = {k:v for k,v in chain.PINS.items() if k != chain.ARCHIVE and not k.startswith("v16.22")}
PINS.update({chain.OLD+"verifier.py":"a2f8b9d9b0be3b8d243b11fc5fdab443603f420f",
             chain.OLD+"graph_verifier.py":"ff8af4ecf743507d0d601daffa9b054441b85fd1"})
HELPERS = {"check_routed_chain.py":"29bf8ba4c5cdda5b824f4ad51563fccd617789e4",
           "check_routed_grade.py":"4c16f2f6243f4be4f0d34bd9a9e5f24a8c1e4133"}

def blob(data):
    return hashlib.sha1(b"blob "+str(len(data)).encode()+b"\0"+data).hexdigest()

def pins():
    for path,expected in PINS.items():
        assert blob((chain.DEMOS/path).read_bytes()) == expected, path
    for path,expected in HELPERS.items():
        assert blob((Path(__file__).parent/path).read_bytes()) == expected, path

def support(state,v):
    return {j for j,m in enumerate(state) if m>>v&1}

def profile(state):
    """Enumerate covering subsets, independently of graph.build/atomic/normalize."""
    out=[]
    for v in X:
        kids=[w for w in X if P[w]==v]
        out.append(0 if not kids else min(len(c) for k in range(1,5)
            for c in itertools.combinations(range(4),k)
            if all(set(c)&support(state,w) for w in kids)))
    return out

def valid(state):
    assert len(state)==4 and all(type(m) is int and 0<m<512 and m&1 for m in state)
    assert all(not(m>>v&1) or m>>P[v]&1 for m in state for v in X[1:])
    assert set.union(*(set(chain.view(m)) for m in state))==set(X)

def verify_path(path,q):
    assert path
    for state in path:
        valid(state)
        assert sum(abs(a-b) for a,b in zip(profile(state),q))<=1
    for before,after in zip(path,path[1:]):
        differences=[a^b for a,b in zip(before,after)]
        assert sum(d.bit_count() for d in differences)==1
    assert profile(path[-1])==q

def actor(name,mode):
    return D if mode=="delete_D" else (0 if name=="AD" else 2) if mode=="delete_spectator" else None

def produce(machine,atom,verifier):
    records=[]
    for name,prep in PREPS.items():
        for mode in MODES:
            a=actor(name,mode)
            event=None
            if a is not None:
                event=atom.atomic(P,list(map(chain.view,prep)),a,S)
                verifier.verify_atomic(event)
                start=[sum(1<<v for v in view) for view in event["after"]]
            else:
                start=list(prep)
            q=[atom.tau_at(P,list(map(chain.view,start)),v) for v in X]
            path=machine.normalize(start,DEGREES,4,q)
            records.append({"id":name+"/"+mode,"prep":list(prep),"event":event,"q":q,"path":path})
    return records

def verify_records(records):
    expected={name+"/"+mode for name in PREPS for mode in MODES}
    assert len(records)==len(expected) and {r["id"] for r in records}==expected
    for r in records:
        name,mode=r["id"].split("/");prep=PREPS[name];a=actor(name,mode)
        assert r["prep"]==list(prep)
        start=list(prep)
        if a is not None:start[a]&=~(1<<S)
        assert r["path"][0]==start and r["q"]==profile(start)
        event=r["event"]
        if a is None:assert event is None
        else:
            assert event["index"]==a and event["leaf"]==S
            assert event["before"]==[list(chain.view(m)) for m in prep]
            assert event["after"]==[list(chain.view(m)) for m in start]
            assert event["tau_before"]==1
            assert event["tau_after"]==(2 if name=="AD" and mode=="delete_D" else 1)
            assert event["trigger"]==(name=="AD" and mode=="delete_D")
        verify_path(r["path"],r["q"])
        special=r["id"]=="AD/delete_D"
        assert len(r["path"])-1==((14 if name=="AD" else 16) if a is None else 15)
        if special:
            assert r["path"][-1][B]==199
        else:
            assert all(s[B]==63 for s in r["path"])
        assert [int(s[B]>>H&1) for s in r["path"]]==([0]+[1]*(len(r["path"])-1) if special else [0]*len(r["path"]))

def independent_field(carrier,source):
    """Root-grounded unit-tree potential via subtree cut loads."""
    totals={v:sum(source[w] for w in X if v in lift.ANCESTORS[w]) for v in X}
    phi={0:0}
    for v in carrier:
        if v:phi[v]=phi[P[v]]+totals[v]
    return phi

def grade_checks(records,sources):
    basis=[tuple(int(v==w) for v in X) for w in X]
    special_grades={"unit":(1,)*9,"positive_base":(2,)*9,
        "positive_shift":tuple(2+int(v==H)-int(v==J) for v in X),
        "zero_remote":tuple(int(v!=H) for v in X),
        "zero_deleted":tuple(int(v!=S) for v in X),
        "negative_remote":tuple(-1 if v==H else 1 for v in X)}
    counts=Counter();summaries={}
    for r in records:
        full=[r["prep"]]+r["path"] if r["event"] else r["path"]
        special=r["id"]=="AD/delete_D"
        for source in basis:
            lifted=lift.traverse(sources,full,source)
            for ix,(state,family) in enumerate(zip(full,lifted)):
                counts["basis_state_occurrences"]+=1
                named=dict(zip(chain.view(state[B]),family[B]))
                active=bool(state[B]>>H&1)
                assert named[J]==source[J]+(0 if active else source[H])
                for m,grade in zip(state,family):
                    y=chain.view(m)
                    assert grade==lift.independent_grade(y,source)
                    phi=independent_field(y,source)
                    local=dict(zip(y,grade))
                    for v in y[1:]:
                        divergence=phi[v]-phi[P[v]]+sum(phi[v]-phi[w] for w in y if P[w]==v)
                        assert divergence==local[v]
                    assert phi=={v:independent_field(X,source)[v] for v in y}
                    counts["local_field_checks"]+=1
                # The high endpoint trades inner branches: compare literal overlap,
                # not all of the initial B carrier, which need not stay contained.
                common=tuple(sorted(set(chain.view(state[B])) & set(chain.view(63))))
                assert sources.push(P,chain.view(state[B]),common,family[B])==sources.push(P,X,common,source)
        rows={}
        for label,source in special_grades.items():
            family=lift.traverse(sources,full,source)
            rows[label]=[int(dict(zip(chain.view(s[B]),g[B]))[J]) for s,g in zip(full,family)]
            assert rows[label][-1]==source[J]+(0 if special else source[H])
        source0,source1=special_grades["positive_base"],special_grades["positive_shift"]
        holders=[]
        for state in full:
            holders.append(["ABCD"[i] for i,m in enumerate(state)
                if sources.push(P,X,chain.view(m),source0)!=sources.push(P,X,chain.view(m),source1)])
        summaries[r["id"]]={"junction_traces":rows,"positive_contrast_holders":holders}
    by_id={r["id"]:r for r in records}
    high=by_id["AD/delete_D"];low=by_id["CD/delete_D"];running=by_id["AD/no_external_deletion"]
    assert running["path"][:2]==[high["prep"],high["path"][0]]
    assert running["path"][2]==[259,63,199,63] and high["path"][1]==[257,191,199,63]
    for source in basis:
        dy=chain.view(high["prep"][D]);dz=chain.view(high["path"][0][D])
        assert dy==chain.view(low["prep"][D]) and dz==chain.view(low["path"][0][D])
        before=dict(zip(dy,sources.push(P,X,dy,source)));after=dict(zip(dz,sources.push(P,X,dz,source)))
        loss=tuple(before.get(v,0)-after.get(v,0) for v in X)
        assert loss==tuple(source[S]*(int(v==S)-int(v==0)) for v in X)
        hf=lift.traverse(sources,[high["prep"]]+high["path"],source)
        nf=lift.traverse(sources,running["path"],source)
        assert hf[:2]==nf[:2]
    return {"counts":dict(counts),"arms":summaries,"identical_internal_atom_diverges":True,
        "same_D_source_and_loss_all_nine_basis":True,"common_coarse_B_grade_changes":0,
        "common_potential_changes":0}

def ordering_diagnostic(machine,old_checker):
    out=[]
    for order in itertools.permutations(range(4)):
        named_B=order.index(B)
        for name,prep in PREPS.items():
            for mode in MODES:
                a=actor(name,mode);start=list(prep)
                if a is not None:start[a]&=~(1<<S)
                start=[start[i] for i in order];q=profile(start)
                path=machine.normalize(start,DEGREES,4,q)
                verify_path(path,q)
                end=old_checker.canonical(DEGREES,4,q)
                assert old_checker.raw_path_valid(path,DEGREES,4,q,start,end)
                bits=[int(s[named_B]>>H&1) for s in path]
                out.append({"order":"".join("ABCD"[i] for i in order),"arm":name+"/"+mode,
                    "final_B_leaf":bits[-1],"ever_B_leaf":max(bits),"moves":len(path)-1,
                    "final_original_label_masks":[path[-1][order.index(i)] for i in range(4)]})
    assert len(out)==144
    return out

def rejecting_controls(records,sources):
    errors=[]
    def reject(label,fn):
        try:fn()
        except (AssertionError,ValueError):errors.append(label)
        else:raise AssertionError("False acceptance: "+label)
    reject("missing_call",lambda:verify_records(records[:-1]))
    reject("duplicate_call",lambda:verify_records(records+[copy.deepcopy(records[0])]))
    wrong=copy.deepcopy(records);wrong[1]=copy.deepcopy(wrong[0])
    reject("substituted_call",lambda:verify_records(wrong))
    wrong=copy.deepcopy(records);wrong[0]["path"][1]=[257,63,199,63]
    reject("non_atomic_noop",lambda:verify_records(wrong))
    wrong=copy.deepcopy(records);wrong[0]["path"][-1][B]=63
    reject("wrong_receiver",lambda:verify_records(wrong))
    wrong=copy.deepcopy(records);wrong[0]["path"][1][B]&=~2
    reject("missing_ancestor",lambda:verify_records(wrong))
    data=(chain.DEMOS/(chain.OLD+"producer.py")).read_bytes()
    reject("false_source_provenance",lambda:assert_identity(data+b"\n",PINS[chain.OLD+"producer.py"]))
    high=records[0];before,after=high["path"][:2]
    old=chain.view(before[B]);new=chain.view(after[B]);holder=chain.view(before[2])
    grade=sources.push(P,X,old,(1,)*9);zeros=dict(zip(old,grade));fake=tuple(zeros.get(v,0) for v in new)
    reject("false_zero_grade_extension",lambda:sources.glue(P,new,holder,fake,sources.push(P,X,holder,(1,)*9)))
    return errors

def assert_identity(data,expected):
    assert blob(data)==expected

def main():
    pins();sys.path.insert(0,str(chain.DEMOS/chain.OLD))
    import producer as machine
    import verifier as old_checker
    atom=chain.module(chain.ATOM+"engine.py","fixed_donor_atom")
    verifier=chain.module(chain.ATOM+"verify.py","fixed_donor_atom_verifier")
    sources=chain.module("v16.23-overlap-descent/engine.py","fixed_donor_sources")
    records=produce(machine,atom,verifier);verify_records(records)
    for r in records:
        assert old_checker.raw_path_valid(r["path"],DEGREES,4,r["q"],r["path"][0],old_checker.canonical(DEGREES,4,r["q"]))
    corpus=machine.produce(domain=())
    regression=old_checker.verify(corpus,domain=())
    assert regression["directed_cases"]==210 and not regression["construction_failures"]
    result={"scope":"six constructed calls, not archived v16.48 representatives", "source_blobs":PINS,
        "helper_blobs":HELPERS,"records":records,"grade":grade_checks(records,sources),
        "palette_order_diagnostic":ordering_diagnostic(machine,old_checker),"rejecting_controls":rejecting_controls(records,sources),
        "inherited_directed_regression":regression,
        "native_physical_bridge":"OPEN"}
    print(json.dumps(result,sort_keys=True,indent=2))

if __name__=="__main__":main()
