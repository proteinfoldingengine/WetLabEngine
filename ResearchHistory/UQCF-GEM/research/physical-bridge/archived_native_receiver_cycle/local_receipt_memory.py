"""Recognize and retain locally decodable receipts without a supplied transfer frame."""
from collections import Counter, defaultdict
import gzip
from hashlib import sha1
from itertools import product
import json
from pathlib import Path
import sys

from guarded_peer_transfer import observe
from two_site_receipt import holding, decode, views, PARENTS
from rank_dispatch import load


def listen(path,site,atom,len_palette):
    """New passive receiver memory; inputs are this site's successive holdings."""
    seen_loss=False
    saved=[]
    previous=path[0]
    for frame,current in enumerate(path[1:],1):
        if previous-current:
            seen_loss=True
        elif current-previous and seen_loss:
            label,=current-previous
            receipt=None
            if all(j<label for j in previous):
                def remote(*args):
                    raise AssertionError("nonlocal read")
                _,_,receipt=decode(atom,len_palette,site,previous,current,remote)
            saved.append((frame,label,receipt))
        previous=current
    return saved


def main(demos):
    sys.path.insert(0,str(demos/"v16.53-four-child-boundary"))
    import producer as p
    import verifier as v
    atom=load("original_atom",demos/"v16.26-consistency-increment-law/engine.py")
    doc=p.produce()
    data=gzip.compress((json.dumps(doc,sort_keys=True,separators=(",",":"))+"\n").encode(),mtime=0)
    blob=sha1(b"blob "+str(len(data)).encode()+b"\0"+data).hexdigest()
    assert blob=="9dd2e4445bca36dfe59f10fc7b7debd1ee2bc81e"
    counts=defaultdict(Counter)
    keys=[defaultdict(set),defaultdict(set)]
    lives=Counter()
    examples={}
    signatures=Counter()
    contrasts=[]
    def test(start,category,idx=None):
        k=len(start)
        path,calls=observe(p,start,[3])
        v.path_check(p.Q,k,[3],path,start,v.model(p.Q,[3],k)[2])
        if idx is not None:
            assert path==doc["records"][idx]["path"]
        truth={(h+2,t):(x,atom.atomic(PARENTS,views(path[h]),x,s)) for h,x,s,t in calls}
        counts[category]["runs"]+=1
        counts[category]["transfers"]+=len(calls)
        for t in range(1,5):
            local=[holding(st,t) for st in path]
            saved=listen(local,t,atom,k)
            if idx is not None and t == 3:
                changes = [sorted(a) for n,a in enumerate(local) if n == 0 or a != local[n-1]]
                recognized = [receipt for _,_,receipt in saved if receipt is not None]
                if recognized:
                    signatures[json.dumps(changes[:4])] += 1
                if local[0] == frozenset({0}) and local[-1] == frozenset({1}):
                    contrasts.append((idx, changes, recognized, [r for (f,site),(x,r) in truth.items() if site == t]))
            for f,x,receipt in saved:
                assert (f,t) in truth and truth[f,t][0]==x
                counts[category]["self_identified"]+=1
                if receipt is not None:
                    assert truth[f,t][1]==receipt
                    counts[category]["self_identified_complete"]+=1
                    if idx is not None:
                        first = examples.setdefault("hit",dict(case=idx,site=t,frame=f,local=list(map(sorted,local)),receipt=receipt))
                        assert receipt == first["receipt"] and t == first["site"]
            if idx is not None:
                prefix=[local[0]]
                for f in range(1,len(local)):
                    if prefix[-1]==local[f]:continue
                    prefix.append(local[f])
                    event=truth.get((f,t))
                    outcome=None
                    if event and all(j<event[0] for j in local[f-1]):
                        x=event[0]
                        outcome=json.dumps(event[1],sort_keys=True)
                        loss=next(d for d,z in enumerate(local[f:]) if x not in z)
                        lives[loss]+=1
                    keys[0][t,tuple(prefix[-2:])].add(outcome)
                    keys[1][t,tuple(prefix)].add(outcome)
    for idx,r in enumerate(doc["records"]):
        if r["identity"][0]=="R" and r["q"]==[3]:
            test(r["start"],"archived",idx)
    for rows in product(range(1,16),repeat=4):
        st=[1+sum(1<<i for i,row in enumerate(rows,1) if row & (1<<j)) for j in range(4)]
        if p.coordinate(st,[1,2,3,4])==3:
            test(st,"four_label_controls")
    exact_keys=[sum(len(w)==1 and None not in w for w in mapping.values()) for mapping in keys]
    assert exact_keys==[0,2]
    target = examples["hit"]["receipt"]
    assert sum(signatures.values()) == 14
    assert all(receipt == target for _,_,found,_ in contrasts for receipt in found)
    examples["same_endpoints_without_target"] = next(dict(case=i, changes=changes)
        for i,changes,found,actual in contrasts if target not in actual and not found)
    return dict(local_prefix_counts=signatures,blob=blob,counts=counts,recognizable_complete_signatures=exact_keys,
                archived_edits_until_loss=lives,examples=examples)

if __name__=="__main__":
    print(json.dumps(main(Path(sys.argv[1]).resolve()),sort_keys=True,indent=2))
