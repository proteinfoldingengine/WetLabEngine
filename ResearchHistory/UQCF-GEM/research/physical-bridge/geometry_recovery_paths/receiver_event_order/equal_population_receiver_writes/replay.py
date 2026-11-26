"""Execute the frozen star writer and P1 projection on all 968 inherited leaves."""
from collections import Counter
from hashlib import sha1, sha256
from itertools import combinations
from pathlib import Path
import json
import runpy
import sys

C = (0,15,30,34,49,64,68,83,98,102,117)
RELEASE = ((41,217,278,454),(91,157,338,404))
PARENTS = (-1,)+(0,)*968
AMBIENT = tuple(range(969))
GRADES = (1,)+(2,)*968
FULL = (1<<969)-1


def pinned(path, signature):
    raw = path.read_bytes()
    assert sha1(b"blob "+str(len(raw)).encode()+b"\0"+raw).hexdigest()==signature
    return path


def view(bits):
    return tuple(i for i in AMBIENT if bits>>i&1)


def union(rows):
    result=0
    for s in rows:
        result |= s
    return result


def work(rows):
    return [4*(x^y).bit_count() for x,y in combinations(rows,2)]


def chart_order(*first):
    return (*first,*(i for i in C if i not in first))


def writer(world, order, receiver, normalize, push):
    start=[world[i] for i in order]
    assert union(start)==FULL
    private=[s & ~union(start[:j]+start[j+1:]) for j,s in enumerate(start)]
    assert all(private)  # every chart must be in every cover of this family
    path=normalize(tuple(start),968,len(start),len(start))
    pos=order.index(receiver)
    word=[start[pos]]
    boundary=None
    first=None
    for step,state in enumerate(path):
        if boundary is None and sum(s.bit_count()-1 for s in state)==968:
            boundary=state[pos]
        if step:
            before=path[step-1]
            delta=[a^b for a,b in zip(before,state) if a!=b]
            assert len(delta)==1 and delta[0].bit_count()==1 and union(state)==FULL
        current=state[pos]
        if current==word[-1]:
            continue
        gained=current & ~word[-1]
        if gained and first is None:
            record=push(PARENTS,AMBIENT,view(current),GRADES)
            assert all(v==2 for v in record[1:]) and sum(record)==1937
            first=dict(step=step,local_edit=len(word),address=gained.bit_length()-1,
                       new_to_prior=not bool(gained & word[0]),leaves=current.bit_count()-1,pin=int(record[0]))
        word.append(current)
    assert boundary is not None
    return (dict(edits=len(path)-1,private_witnesses=[s.bit_count() for s in private],
                 first_gain=first, after_contraction=boundary.bit_count()-1,terminal=word[-1].bit_count()-1,
                 local_word_sha256=sha256(b''.join(s.to_bytes(122,'little') for s in word)).hexdigest()),
            word,path[-1])


def run(orbit,p1,at,prod,dep):
    original=runpy.run_path(str(pinned(orbit,"45eaeb0df71e6f6a5d9e205332f3bc015fcb4c8b")))
    push=runpy.run_path(str(pinned(p1,"b18f52109ccff9c7dc77542d3b8f3e5d5989102a")))['push']
    atomic=runpy.run_path(str(pinned(at,"c10ac57f988a439144e21898bd2b33ece0838a9b")))['atomic']
    pinned(dep,"6c8eca570cda82b64c0d06775672f33977be430a")
    assert dep.parent==prod.parent and dep.name=='graph_producer.py'
    sys.path.insert(0,str(dep.parent))
    normalize=runpy.run_path(str(pinned(prod,"ffd513619d182abea2b31bd90c38e12784557bf3")))['normalize']
    before=[1|(r<<1) for r in original['rows']]
    assert {s.bit_count()-1 for s in before}=={200}
    worlds=[]; receipts=[]; work_stages=[]
    for deletes in RELEASE:
        w=before.copy(); rs=[]; ws=[]
        for leaf in deletes:
            # Same local mutation in the full atlas; 24 other holders remain.
            assert w[0]>>leaf&1 and sum(s>>leaf&1 for s in w)==25
            receipt=atomic(PARENTS,[view(w[i]) for i in C],0,leaf)
            w[0] ^= 1<<leaf
            assert list(map(tuple,receipt['after']))==[view(w[i]) for i in C]
            rs.append([receipt[x] for x in ('tau_before','tau_after','h_before','h_after','delta_h','trigger')])
            ws.append(work(w))
        worlds.append(w);receipts.append(rs);work_stages.append(ws)
    mismatch=[sum(x!=y for x,y in zip(a,b)) for a,b in zip(*work_stages)]
    assert mismatch[-1]==0 and worlds[0][1:]==worlds[1][1:]==before[1:]
    assert all(s==[11,11,11,11,0,False] for arm in receipts for s in arm)
    first_order=chart_order(0,117,15)
    blind_order=chart_order(15,117,*[i for i in C if i not in (0,15,117)],0)
    def paired(ws,order,r):
        a,b=[writer(w,order,r,normalize,push) for w in ws]
        return dict(order=order,receiver=r,arms=[a[0],b[0]],same_receiver_word=a[1]==b[1],
                    same_terminal=a[2]==b[2])
    signal=paired(worlds,first_order,15)
    control=paired(worlds,blind_order,15)
    assert not signal['same_receiver_word'] and signal['same_terminal'] and control['same_receiver_word']
    original_work=work(before); changes=sum(x!=y for x,y in zip(work_stages[0][-1],original_work))
    # The previous reflected pair compares distinct preparations; no remote release is attributed to it.
    cols=original['orbit'].copy()
    def refl(i):
        return (-(i//11))%11+11*((-(i%11))%11)
    for k in range(363,484):
        cols[k]=sum(1<<refl(i) for i in range(121) if cols[k]>>i&1)
    reflected=[1+sum(1<<(k+1) for k,s in enumerate(cols) if s>>i&1) for i in range(121)]
    assert work(reflected)==original_work and reflected[0]==before[0]
    static=paired([before,reflected],chart_order(15,30,49,0),0)
    return dict(number_of_pairs=len(original_work), varied_source=0,leaf_addresses=RELEASE,
                histories_pair_mismatches_by_step=mismatch,endpoint_pair_changes_from_start=changes,
                identical_remote_priors=120,source_endpoint_count=worlds[0][0].bit_count()-1,
                single_source_collision=signal,source_last_control=control,
                reflected_preparation=static,source_primitive_receipts=receipts)


if __name__=="__main__":
    print(json.dumps(run(*(Path(x).resolve() for x in sys.argv[1:])),sort_keys=True,indent=2))
