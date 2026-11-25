"""Rebuild the representative graph, semantic full paths and source-call inventory."""
from collections import Counter
from copy import deepcopy
from hashlib import sha1
from itertools import combinations, permutations, product
from pathlib import Path
import re
import sys
from free_receiver_io import DEMOS, read_xz, require, same, save


def graph():
    views=[s for s in range(1,64,2) if s&2 or not s&28]
    states=sorted(s for s in product(views,repeat=3) if s[0]|s[1]|s[2]==63)
    ids={s:i for i,s in enumerate(states)}
    def hit(state,children):
        for n in (1,2,3):
            for combo in combinations(state,n):
                if all(any(m&(1<<v) for m in combo) for v in children):
                    return n
    profiles=[(hit(s,(1,5)),hit(s,(2,3,4))) for s in states]
    reps={}
    edges=0
    for start,s in enumerate(states):
        edges+=sum(tuple(m^(1<<v) if i==j else m for i,m in enumerate(s)) in ids
                   for j in range(3) for v in range(1,6) if s[j]&(1<<v))
        if start in reps:
            continue
        reps[start]=start
        queue=[start]
        while queue:
            old=states[queue.pop()]
            for j in range(3):
                for vertex in range(1,6):
                    new=list(old)
                    new[j]^=1<<vertex
                    other=ids.get(tuple(new))
                    if other is not None and other not in reps and profiles[other]==profiles[start]:
                        reps[other]=start
                        queue.append(other)
    return ids,reps,profiles,edges


def model(order,tips,cut,ids,reps):
    S,H,R=map(order.index,"SHR")
    a,b,c=tips
    live=[{0,1} for _ in order]
    live[S].update((a,b,c))
    live[H].update((a,5))
    live[R].add(b)
    live[S].remove(a if cut=="a" else b)
    def bitmasks():
        return [sum(1<<v for v in y) for y in live]
    path=[bitmasks()]
    def change(j,v,add):
        require((v not in live[j])==add,"unexpected change")
        if add: live[j].add(v)
        else: live[j].remove(v)
        path.append(bitmasks())
    def move(v,old,new):
        if old!=new:
            change(new,v,True)
            change(old,v,False)
    move(5,H,0)
    begin=len(path)-1
    cover=(S,H) if cut=="a" else (S,R)
    reads=[]
    edits=[]
    raw=(2,3,4)
    for v in raw:
        owners=[j for j,view in enumerate(live) if v in view]
        keeper,=(j for j in owners if j in cover)
        reads.append(dict(tip=v,holders=owners,keeper=keeper))
        for j in owners:
            if j!=keeper:
                change(j,v,False)
                edits.append([j,v,False])
    p=3+sum(x for v,x in ((a,2),(b,2),(c,1)) if v not in live[R])
    if 2 in cover:
        replacement,={0,1}-set(cover)
        transfer=sorted(set(raw)&live[2])
        for v in transfer:
            change(replacement,v,True)
        for v in transfer:
            change(2,v,False)
    def owner(v):
        j,=(i for i in (0,1) if v in live[i])
        return j
    for i,v in enumerate(raw[:2]):
        old=owner(v)
        if old==i:
            continue
        if sum(owner(t)==old for t in raw)==1:
            donor=next(t for t in raw[i+1:] if sum(owner(q)==owner(t) for q in raw)>1)
            move(donor,owner(donor),old)
        move(v,old,i)
    move(4,owner(4),0)
    change(2,1,False)
    require(all(tuple(s) in ids for s in path),"state outside graph")
    start=ids[tuple(path[0])]
    return dict(order=order,abc=list(tips),cut=cut,source_start=start,representative=reps[start],
                actually_called=reps[start]==start,source_calls=[["engine.py",key] for key in
                    ("h","need","parents","tau_at","trigger")],q=[1,2,0,0,0,0],
                trace=dict(start=begin,supports=reads,edits=edits),path=path,p=p)


def check_inventory(root, audit):
    expected={}
    calls=[]
    for path in sorted((root/DEMOS).glob("v16.*-*/*.py")):
        if not 22<=int(path.parent.name.split("-")[0][4:])<=54:
            continue
        rel=path.relative_to(root/DEMOS).as_posix()
        raw=path.read_bytes()
        expected[rel]=sha1(b"blob "+str(len(raw)).encode()+b"\0"+raw).hexdigest()
        func=""
        for line,text in enumerate(raw.decode().splitlines(),1):
            definition=re.match(r"\s*def\s+(\w+)\s*\(",text)
            if definition: func=definition.group(1)
            for match in re.finditer(r"\batomic\s*\(",text):
                if not re.search(r"\bdef\s*$",text[:match.start()]):
                    calls.append([rel,line,func])
    same(audit,dict(files=expected,atomic_named_calls=sorted(calls)),"source inventory")
    require(len(expected)==278 and len(calls)==9,"historical audit scope")
    return len(expected),len(calls)


def verify(root,doc):
    ids,reps,q,edges=graph()
    same(doc["campaign_calls"],sorted(set(reps.values())),"originally invoked states")
    expected_counts=dict(states=len(ids),profiles=len(set(q)),components=len(set(reps.values())),edges=edges)
    stats=doc["campaign_receipt"]["per_graph"][0]
    require(doc["states"]==len(ids) and all(stats[k]==v for k,v in expected_counts.items())
            and doc["campaign_receipt"]["construction_failures"]==[],"campaign graph")
    cases={(r["order"],tuple(r["abc"]),r["cut"]):r for r in doc["cases"]}
    require(len(cases)==len(doc["cases"])==72,"fixture count")
    for chars in permutations("SHR"):
        order="".join(chars)
        for tips in permutations((2,3,4)):
            for cut in ("a","b"):
                rec=cases.pop((order,tips,cut))
                same(rec,model(order,tips,cut,ids,reps),"historical branch and all output states")
    dead=[dict(cut=v,receiver_move=[1,1],p1_prior=[9,4],p1_after=[13]) for v in (2,4)]
    same(doc["stub"],dead,"genuine required receiver edit")
    files,calls=check_inventory(root,doc["audit"])
    return dict(arms=72,pairs=36,source_selected=sum(r["actually_called"] for r in doc["cases"]),
                representatives=len(doc["campaign_calls"]),graph_states=len(ids),files=files,named_calls=calls,
                materialized_states=sum(len(r["path"]) for r in doc["cases"]),
                numeric_fork_grades=[8,6],stub_grades=[9,13])


if __name__=="__main__":
    root,data=map(Path,sys.argv[1:])
    doc=read_xz(data/"free_receiver_caller.json.xz")
    result=verify(root,doc)
    case=doc["cases"][0]
    changes=[
        ("actually_called",True),("representative",case["source_start"]),("p",7),
        ("path",case["path"][1:]),("trace",{**case["trace"],"edits":[]}),("source_calls",[])
    ]
    for key,value in changes:
        bad={**doc,"cases":[{**case,key:value},*doc["cases"][1:]]}
        try: verify(root,bad)
        except ValueError: continue
        raise ValueError("accepted corruption "+key)
    result["rejecting_controls"]=len(changes)
    save(data/"free_receiver_call_check.json",result)
    print(result)
