"""Reconstruct the v16.26 atom from the two participants in a v16.53 flat transfer."""
from collections import Counter, defaultdict
import gzip
from hashlib import sha1, sha256
from itertools import product
import json
from pathlib import Path
import sys
from guarded_peer_transfer import observe
from rank_dispatch import load

PARENTS = [-1,0,0,0,0]


def holding(state, site):
    return frozenset(j for j,mask in enumerate(state) if mask & (1 << site))


def views(state):
    return [[u for u in range(5) if mask & (1 << u)] for mask in state]


def decode(atom,k,receiver,old_row,new_row,read_overlap):
    """Only reads the receiver transition and one participant's current holding."""
    x, = new_row-old_row
    assert old_row < new_row and len(new_row)==len(old_row)+1
    sender = 3 if x==0 else 1
    third, = {1,2,3}-{sender,receiver}
    unknown = frozenset(j for j in old_row if j > x)
    overlap = read_overlap(sender,unknown) if unknown else frozenset()
    completed = []
    for j in range(k):
        if j == x:
            missing = sender
        elif j < x:
            missing = 3 if j==0 else 1
        elif j not in new_row:
            missing = receiver
        elif j in overlap:
            missing = third
        else:
            missing = sender
        completed.append(31 ^ (1 << missing))
    before = completed[:]
    before[x] = 31 ^ (1 << receiver)
    return sender,completed,atom.atomic(PARENTS,views(before),x,sender)


def main(demos):
    sys.path.insert(0,str(demos/"v16.53-four-child-boundary"))
    import producer as p
    import verifier as v
    atom = load("historical_atom",demos/"v16.26-consistency-increment-law/engine.py")
    av = load("historical_atom_verify",demos/"v16.26-consistency-increment-law/verify.py")
    doc=p.produce()
    raw=gzip.compress((json.dumps(doc,sort_keys=True,separators=(",",":"))+"\n").encode(),mtime=0)
    blob=sha1(b"blob "+str(len(raw)).encode()+b"\0"+raw).hexdigest()
    assert blob=="9dd2e4445bca36dfe59f10fc7b7debd1ee2bc81e"
    records=doc["records"]
    totals=defaultdict(Counter)
    local=defaultdict(set)
    immediate=defaultdict(set)
    log=sha256()
    def run(start,k,category,archive=None):
        path,calls=observe(p,start,[3])
        if archive is not None:
            assert path==archive
        v.path_check(p.Q,k,[3],path,start,v.model(p.Q,[3],k)[2])
        totals[category]["runs"]+=1
        for h,x,s,t in calls:
            a,b,c=path[h:h+3]
            old,new=holding(b,t),holding(c,t)
            local_only = all(j < x for j in old)
            def read_overlap(site, labels):
                assert not local_only
                return holding(c,site)&labels
            predicted,complete,reconstructed=decode(atom,k,t,old,new,read_overlap)
            if local_only:
                totals[category]["complete_from_receiver_transition"]+=1
                totals[category]["also_retains_label_at_endpoint_without_loss"]+=all(
                    step[x] & (1 << t) != 0 for step in path[h+2:])
            original=atom.atomic(PARENTS,views(a),x,s)
            assert av.verify_atomic(original)==(0,False)
            assert (predicted,complete,reconstructed)==(s,c,original)
            assert reconstructed["after"]==views(b)
            totals[category]["receipts"]+=1
            log.update((json.dumps(original,sort_keys=True)+"\n").encode())
            if archive is not None:
                local[(t,x,h,tuple(holding(f,t) for f in path))].add(tuple(a))
                immediate[t,x,old].add(tuple(a))
    for row in records:
        if row["identity"][0]=="R" and row["q"]==[3]:
            run(row["start"],row["k"],"archived",row["path"])
    # Every ordered choice of four nonempty rows on a four-label palette.
    for rows in product(range(1,16),repeat=4):
        start=[1+sum(1 << u for u,row in enumerate(rows,1) if row & (1 << j)) for j in range(4)]
        if p.coordinate(start,[1,2,3,4])==3:
            run(start,4,"four_label_controls")
    a,b=(records[i]["path"] for i in (684,733))
    assert len(a)==len(b) and [holding(f,1) for f in a]==[holding(f,1) for f in b]
    assert a[5:8]==[[29,27,29],[21,27,29],[23,27,29]]
    assert b[5:8]==[[29,23,29],[21,23,29],[23,23,29]]
    # A change of traversal order on the same physical initial tree.
    def exchange_sites(st):
        return [(z & ~6)|((z & 2)<<1)|((z & 4)>>1) for z in st]
    assert exchange_sites(b[0])==b[0] and exchange_sites(b[-1])==b[-1]
    paths=[]
    for perm in (lambda z:z[:],exchange_sites):
        path,calls=observe(p,perm(b[0]),[3])
        v.path_check(p.Q,3,[3],path,path[0],path[-1])
        assert (7,1,1,3) in calls
        paths.append([perm(f) for f in path])
    first,second=paths
    assert first[0]==second[0] and first[-1]==second[-1]
    assert first[7][1]^first[8][1]==2 and second[7][1]^second[8][1]==4
    assert [holding(f,3) for f in first]==[holding(f,3) for f in second]
    assert all((len(values)==1)==all(j<x for j in old)
               for (t,x,old),values in immediate.items())
    return dict(blob=blob,immediate_keys=len(immediate),ambiguous_immediate_keys=sum(len(w)>1 for w in immediate.values()),totals=totals,archived_receiver_histories=len(local),
                histories_with_multiple_receipts=sum(len(s)>1 for s in local.values()),
                canonical_atom_log_sha256=log.hexdigest(),examples={n:records[n] for n in (684,733,1368)},
                order_control=paths)


if __name__=="__main__":
    print(json.dumps(main(Path(sys.argv[1]).resolve()),sort_keys=True,indent=2))
