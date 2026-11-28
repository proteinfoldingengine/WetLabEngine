"""Test source-before-receiver dependence at both stages of the original four-child transfer."""
from collections import Counter
import gzip
from hashlib import sha1
import json
from pathlib import Path
import sys
from unittest.mock import patch
from rank_dispatch import load


def observe(p,start,q,intervention=None):
    transfers=[]
    rejected=[]
    def watch(frame,event,arg):
        if event!="call":
            return
        name=frame.f_code.co_name
        parent=frame.f_back
        if name=="transfer" and frame.f_globals.get("__name__")=="cover" and start==[11,5,17]:
            assert parent.f_locals["owners"] == {0:1,1:0,2:0}
            assert parent.f_locals["goals"] == {0:2,1:0,2:0}
        if name=="edit" and parent.f_code.co_name=="transfer" and parent.f_globals.get("__name__")=="cover":
            f=frame.f_locals
            if not f["add"]:
                x=f["x"]
                source=parent.f_locals["j"]
                receiver=f["i"]
                bins=f["bins"]
                path=f["path"]
                assert {i for i,row in enumerate(bins) if x in row}=={source,receiver}
                assert {i for i,row in enumerate(path[-2]) if x in row}=={receiver}
                transfers.append((len(path)-2,x,source+1,receiver+1))
                if intervention=="planner" and transfers[-1]==(5,0,3,2):
                    bins[source].remove(x)
                    rejected.append("planner")
        if name=="roots" and parent.f_code.co_name=="lift_root_path":
            f=parent.f_locals
            if intervention=="tree" and f["current"]==[19,29,29] and len(f["path"])==7:
                # Restore just the released incidence before the next original
                # comparison with the unchanged proposed receiver frame.
                f["current"][0] |= 1 << 3
                rejected.append("tree")
    old=sys.getprofile()
    sys.setprofile(watch)
    try:
        path=p.normalize(start,p.Q,len(start),q)
    except (ValueError,p.ConstructionFailure) as exc:
        if intervention is None:
            raise
        assert rejected==[intervention]
        return str(exc),transfers
    finally:
        sys.setprofile(old)
    assert intervention is None
    return path,transfers


def nested_gate(p,v,atom,av,rows):
    reports=[]
    for idx in range(2847,2853):
        r=rows[idx]
        tree=r["tree"]
        assert r["identity"][:4]==["N","G",[3,3],3]
        path=r["path"]
        cut=len(path)-11
        previous,mid,first=path[cut-1:cut+2]
        assert [previous,mid,first]==[[79,403,291],[79,147,291],[79,155,291]]
        parents=[-1,0,1,1,1,1,0,0,0]
        views=[[u for u in range(9) if z & (1 << u)] for z in previous]
        receipt=atom.atomic(parents,views,1,8)
        assert av.verify_atomic(receipt)==(0,True)
        assert [sum(1 << u for u in col) for col in receipt["after"]]==mid
        assert v.profile_check(tree,3,previous)==[2,3] and v.profile_check(tree,3,mid)==[3,3]
        if idx==2847:
            alternatives=[]
            for site in (6,7,8):
                for x in range(3):
                    if mid[x] & (1 << site):
                        continue
                    alternate=mid[:]
                    alternate[x] |= 1 << site
                    cols=[[u for u in range(9) if z & (1 << u)] for z in alternate]
                    event=atom.atomic(parents,cols,x,site)
                    assert av.verify_atomic(event)==(0,True)
                    assert [sum(1 << u for u in col) for col in event["after"]]==mid
                    assert v.profile_check(tree,3,alternate)==[2,3]
                    assert all(((a^b)&62)==0 for a,b in zip(alternate,mid))
                    child_nodes=p.layout(tree)[0]
                    roots=lambda raw: [{j for j,z in enumerate(raw) if z & (1<<c)} for c in child_nodes]
                    assert p.lift_root_path(alternate,tree,[3,3],[roots(alternate),roots(mid)],[0,1,2],[])==[alternate,mid]
                    alternatives.append((site,x))
            assert len(alternatives)==6
        original_lift,original_check,original_normal=p.lift_root_path,p.require_exact_parent,p.normalize
        for block in (False,True):
            armed=False
            calls=[]
            guards=[]
            def lift(st,t,*args):
                nonlocal armed
                result=original_lift(st,t,*args)
                if t==tree:
                    assert result[-2:]==[previous,mid]
                    armed=True
                return result
            def guard(st,nodes,q):
                if armed and nodes==p.layout(tree) and not guards:
                    assert st==mid and q==3
                    guards.append(list(st))
                    if block:
                        return original_check(previous,nodes,q)
                return original_check(st,nodes,q)
            def enter(st,t,k,q,*args,**kwargs):
                result=original_normal(st,t,k,q,*args,**kwargs)
                if armed and t==p.Q:
                    calls.append((st,q,result))
                return result
            with patch.object(p,"lift_root_path",lift),patch.object(p,"require_exact_parent",guard),patch.object(p,"normalize",enter):
                try:
                    result=original_normal(r["start"],tree,3,r["q"])
                except p.ConstructionFailure as exc:
                    assert block and str(exc)=="recursive call requires exact parent"
                    assert exc.path==path[:cut+1] and not calls
                else:
                    assert not block and result==path and len(calls)==1
                    raw,rank,child_path=calls[0]
                    assert raw==[7,9,17] and rank==[3] and child_path==rows[348]["path"]
                    assert [[(z>>1)&31 for z in step] for step in path[cut:]]==child_path
            assert guards==[mid]
        v.path_check(tree,3,[3,3],path,r["start"],r["end"])
        reports.append(dict(case=idx,cut=cut,source_label=1,source_site=8,
                            first_receiver_leaf=3,flat_child_case=348,child_edits=10))
    return dict(stock=reports,possible_incoming_atoms_at_same_state=alternatives)


def main(demos):
    sys.path.insert(0,str(demos/"v16.53-four-child-boundary"))
    import producer as p
    import verifier as v
    atom=load("historical_atom",demos/"v16.26-consistency-increment-law/engine.py")
    av=load("historical_atom_check",demos/"v16.26-consistency-increment-law/verify.py")
    doc=p.produce()
    raw=gzip.compress((json.dumps(doc,sort_keys=True,separators=(",",":"))+"\n").encode(),mtime=0)
    blob=sha1(b"blob "+str(len(raw)).encode()+b"\0"+raw).hexdigest()
    assert blob=="9dd2e4445bca36dfe59f10fc7b7debd1ee2bc81e"
    counts=Counter()
    events=[]
    for i,r in enumerate(doc["records"]):
        if r["identity"][0]!="R" or r["q"]!=[3]:
            continue
        counts["rank_three_runs"]+=1
        path, operations=observe(p,r["start"],r["q"])
        assert path==r["path"]
        v.path_check(p.Q,r["k"],r["q"],path,r["start"],r["end"])
        counts["runs_with_transfer"]+=bool(operations)
        for h,x,s,t in operations:
            a,b,c=path[h:h+3]
            assert a[x]==(31 ^ (1 << t))
            released=a[:]
            released[x] &= ~(1 << s)
            received=released[:]
            received[x] |= 1 << t
            assert b==released and c==received and t!=s
            views=[[u for u in range(5) if z & (1<<u)] for z in a]
            receipt=atom.atomic([-1,0,0,0,0],views,x,s)
            av.verify_atomic(receipt)
            assert [sum(1<<u for u in col) for col in receipt["after"]]==b
            forbidden=a[:]
            forbidden[x] |= 1<<t
            assert v.profile_check(p.Q,len(a),forbidden)==[1]
            stays=all(row[x] & (1<<t) for row in path[h+2:])
            counts["transfers"]+=1
            counts["retained_to_endpoint"]+=stays
            counts["positive_local_trigger"]+=receipt["trigger"]
            events.append(dict(case=i,start_frame=h,label=x,source=s,receiver=t,retained=stays))
    focal=doc["records"][390]
    failures={k:observe(p,focal["start"],[3],k)[0] for k in ("planner","tree")}
    assert failures=={"planner":"cover deletion","tree":"root step not primitive"}
    # Independent reversed word: only reverse the two edits in the otherwise
    # identical archived run. The original path verifier rejects rank one.
    reordered=[f[:] for f in focal["path"]]
    reordered[6]=[31,29,29]
    try:
        v.path_check(p.Q,3,[3],reordered,focal["start"],focal["end"])
    except v.InterfaceNotPreserved as exc:
        failures["reverse"]=str(exc)
    else:
        raise AssertionError("reversed release was accepted")
    return dict(blob=blob,counts=counts,events=events,controls=failures,
                nested=nested_gate(p,v,atom,av,doc["records"]),
                examples=[doc["records"][i] for i in (390,684,348,2847)])


if __name__=="__main__":
    print(json.dumps(main(Path(sys.argv[1]).resolve()),sort_keys=True,separators=(",",":")))
