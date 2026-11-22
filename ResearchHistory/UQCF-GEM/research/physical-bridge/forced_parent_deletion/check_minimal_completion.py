"""Complete exact-profile incidence domains and order-independent receiver bound.

The endpoint-minimizing selection is a supplied comparison contract. These are
constructed legal paths, not a claim that the old normalizer executes them.
"""
import copy
import hashlib
import itertools
import json
import sys
from collections import deque
from pathlib import Path

import check_routed_chain as chain
import check_routed_grade as lift
import check_fixed_donor as old

P, X = chain.P, chain.X
PAIR = ((1,8),(2,7),(3,6),(4,5))
Q = {"high":(2,1,2,1),"low":(1,1,2,1)}
PREP = {"high":(257,63,199,319),"low":(1,63,455,319)}
START = {name:state[:3]+(63,) for name,state in PREP.items()}
B,D = 1,3

def size(state):return sum(m.bit_count() for m in state)

def legal_masks():
    return [m for m in range(1,512,2) if all(not(m>>v&1) or m>>P[v]&1 for v in X[1:])]

def mask_production():
    masks=legal_masks();out={name:[] for name in Q}
    for a,b,c in itertools.product(masks,[m for m in masks if m&2],masks):
        s=(a,b,c,63)
        if a|b|c|63 != 511:continue
        q=tuple(1 if any(m>>u&1 and m>>v&1 for m in s) else 2 for u,v in PAIR)
        for name,target in Q.items():
            if q==target:out[name].append(s)
    return {name:sorted(states) for name,states in out.items()}

def support_reconstruction(target):
    """Independent representation: nonempty nested label sets at each site."""
    supports=[15];answer=[]
    completed={5:3,6:2,7:1,8:0}
    def descend(v):
        if v==9:
            state=tuple(sum(1<<w for w,labels in enumerate(supports) if labels>>j&1) for j in range(4))
            answer.append(state);return
        parent=supports[P[v]]
        for labels in range(1,16):
            if labels&parent!=labels:continue
            if bool(labels&8)!=bool(63>>v&1):continue
            if v==1 and not(labels&2):continue
            supports.append(labels)
            if v not in completed:
                descend(v+1)
            else:
                i=completed[v];a,b=PAIR[i]
                if (1 if supports[a]&supports[b] else 2)==target[i]:descend(v+1)
            supports.pop()
    descend(1)
    return sorted(answer)

def check_universe(candidate,reference):
    assert len(candidate)==len(set(candidate)),"duplicate identity"
    assert set(candidate)==set(reference),"complete identity mismatch"

def neighbors(s,domain):
    for j in (0,1,2):
        for v in X[1:]:
            t=list(s);t[j]^=1<<v;t=tuple(t)
            if t in domain:yield t

def distances(start,domain):
    dist={start:0};queue=deque([start]);prev={start:None}
    while queue:
        s=queue.popleft()
        for t in neighbors(s,domain):
            if t not in dist:dist[t]=dist[s]+1;prev[t]=s;queue.append(t)
    return dist,prev

def edited_path(start,edits):
    path=[list(start)]
    for j,v,add in edits:
        s=path[-1][:]
        assert bool(s[j]>>v&1)!=add
        s[j]^=1<<v;path.append(s)
    return path

def required_paths(name):
    moves=[(B,v,False) for v in (5,4,3)]
    moves += [(B,6,True),(2,6,False),(B,7,True),(2,7,False)]
    if name=="low":moves += [(B,8,True),(2,8,False)]
    moves += [(2,2,False),(2,1,False)]
    return edited_path(START[name],moves)

def independent_push(carrier,source):
    # Neither the native push nor the reviewed subtree helper is used.
    out={v:0 for v in carrier}
    for v,a in enumerate(source):
        while v not in out:v=P[v]
        out[v]+=a
    return tuple(out[v] for v in carrier)

def read_root(s,source,sources):
    y=chain.view(s[B]);g=sources.push(P,X,y,source)
    assert tuple(g)==independent_push(y,source)
    return int(g[0])

def verify_domain(name,states,original_checker,sources,atom,atom_verifier):
    reference=support_reconstruction(Q[name]);check_universe(states,reference)
    domain=set(states);start=START[name]
    assert start in domain
    target=list(Q[name]) + [0]*5
    for s in states:assert original_checker.raw_profile(s,chain.DEGREES,4)==target
    minimum=min(map(size,states));mins=[s for s in states if size(s)==minimum]
    assert minimum==14
    expected=([(1,199,257,63),(257,199,1,63)] if name=="high" else [(1,455,1,63)])
    assert mins==expected
    bmask=199 if name=="high" else 455
    assert all(s[B]==bmask for s in mins)
    blind=[s for s in states if not(s[B]>>7&1)]
    assert min(map(size,blind))==15
    dist,prev=distances(start,domain)
    assert all(s in dist for s in mins)
    shortest=min(dist[s] for s in mins)
    assert shortest==(9 if name=="high" else 11)
    path=required_paths(name)
    assert all(tuple(s) in domain for s in path)
    assert original_checker.raw_path_valid(path,chain.DEGREES,4,target,start,path[-1])
    assert len(path)-1==shortest and size(path[-1])==minimum
    endpoint=list(start);endpoint[B]=3
    factor=atom.factor(P,list(map(chain.view,start)),list(map(chain.view,endpoint)))
    atom_verifier.verify_factor(factor)
    blind_path=[list(start)]+[[sum(1<<v for v in y) for y in step["after"]] for step in factor["steps"]]
    assert [s[B] for s in blind_path]==[63,31,15,7,3]
    assert all(tuple(s) in domain for s in blind_path) and size(blind_path[-1])==15
    assert all(step["delta_h"]==0 for step in factor["steps"])
    grade_cases={"unit":(1,)*9,"positive0":(2,)*9,
        "positive1":tuple(2+int(v==8)-int(v==0) for v in X),
        "zero_source":tuple(int(v!=8) for v in X),
        "negative_source":tuple(-1 if v==8 else 1 for v in X)}
    summaries={}
    basis_checks=0
    for v in X:
        g=tuple(int(v==w) for w in X)
        for s in mins:
            assert read_root(s,g,sources)==g[0]+(g[8] if name=="high" else 0)
        for row in (path,blind_path):
            full=[list(PREP[name])]+row
            live=lift.traverse(sources,full,g)
            for state,family in zip(full,live):
                basis_checks+=1
                for m,grade in zip(state,family):assert grade==independent_push(chain.view(m),g)
                # Whole-family glue stays g. Potentials on the common tree are
                # fixed by the same subtree-cut loads (not a chartwise degree fit).
                assert sources.glue_many(P,list(map(chain.view,state)),family)==g
    for label,g in grade_cases.items():
        b0=independent_push(chain.view(63),g)
        summaries[label]={"initial_B":b0,"minimum_B":[independent_push(chain.view(s[B]),g) for s in mins],
            "minimum_root":[read_root(s,g,sources) for s in mins],
            "path_root":[read_root(s,g,sources) for s in path],
            "blind_path_root":[read_root(s,g,sources) for s in blind_path]}
    assert summaries["positive0"]["initial_B"]==summaries["positive1"]["initial_B"]
    differences=[a-b for a,b in zip(summaries["positive0"]["minimum_root"],summaries["positive1"]["minimum_root"])]
    assert differences==([0,0] if name=="high" else [1])
    return {"states":[list(s) for s in states],"state_count":len(states),"minimum":minimum,
        "minimum_states":mins,"blind_minimum":15,"reachable_state_count":len(dist),
        "minimum_distances":[dist[s] for s in mins],"shortest_completion":shortest,
        "constructed_positive_path":path,"original_factor_blind_path":blind_path,
        "basis_path_states":basis_checks,"grades":summaries,
        "universe_sha256":hashlib.sha256(json.dumps(states,separators=(",",":")).encode()).hexdigest()}

def event_role(atom,verifier):
    result=[]
    for name,prep in PREP.items():
        for order in itertools.permutations(range(4)):
            donor=order.index(D);initial=[prep[j] for j in order]
            e=atom.atomic(P,list(map(chain.view,initial)),donor,8);verifier.verify_atomic(e)
            matches=[j for j,y in enumerate(e["before"]) if j!=donor and y==e["after"][donor]]
            assert matches==[order.index(B)]
            result.append({"arm":name,"order":order,"donor":donor,"twin":matches[0]})
    return result

def dropping_premises(checker,sources):
    q=list(Q["high"])+[0]*5;start=START["high"]
    no_anchor=edited_path(start,[(B,v,False) for v in (5,4,3,2,1)])
    no_freeze=edited_path(start,[(D,v,False) for v in (5,4,3,2,1)])
    for p in (no_anchor,no_freeze):
        assert checker.raw_path_valid(p,chain.DEGREES,4,q,start,p[-1])
        assert all(checker.raw_profile(s,chain.DEGREES,4)==q for s in p)
        assert size(p[-1])==14 and not(p[-1][B]>>7&1)
    return {"without_B_junction_retention":no_anchor,"without_donor_freeze":no_freeze}

def corruptions(states):
    rejections=[]
    def check(name,rows,reference):
        try:check_universe(rows,reference)
        except AssertionError:rejections.append(name)
        else:raise AssertionError("accepted corruption "+name)
    for name,rows in states.items():
        reference=support_reconstruction(Q[name])
        check(name+":missing",rows[:-1],reference)
        check(name+":duplicate",rows+[rows[0]],reference)
        check(name+":substituted",rows[:-1]+[(511,511,511,63)],reference)
    assert old.blob((chain.DEMOS/(chain.OLD+"producer.py")).read_bytes()+b"\n")!=old.PINS[chain.OLD+"producer.py"]
    rejections.append("changed_original_source")
    return rejections

def main():
    old.pins();assert old.blob((Path(__file__).parent/"check_fixed_donor.py").read_bytes())=="1dda2e6c075282731db9c5c8b34df321ceaf50e3"
    sys.path.insert(0,str(chain.DEMOS/chain.OLD))
    import verifier as checker
    sources=chain.module("v16.23-overlap-descent/engine.py","min_completion_sources")
    atom=chain.module(chain.ATOM+"engine.py","min_completion_atom")
    atom_verifier=chain.module(chain.ATOM+"verify.py","min_completion_atom_verifier")
    states=mask_production()
    report={"schema":1,"native_bridge":"OPEN","source_blobs":old.PINS,
        "domains":{name:verify_domain(name,rows,checker,sources,atom,atom_verifier) for name,rows in states.items()},
        "event_role_checks":event_role(atom,atom_verifier),
        "dropping_premise_paths":dropping_premises(checker,sources),"corruption_rejections":corruptions(states)}
    print(json.dumps(report,sort_keys=True,indent=2))

if __name__=="__main__":main()
