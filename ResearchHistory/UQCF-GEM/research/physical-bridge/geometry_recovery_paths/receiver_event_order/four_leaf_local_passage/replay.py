"""Run the pinned R input calculation and normalizer at multiple chart and leaf orders."""
from collections import Counter
from functools import lru_cache
from importlib.util import module_from_spec, spec_from_file_location
from itertools import permutations, combinations
from hashlib import sha256
from pathlib import Path
import json
import sys

demos=Path(sys.argv[1]).resolve()
sys.path.insert(0,str(demos/'v16.53-four-child-boundary'))
import producer as p
from verifier import path_check

def engine(name):
    spec=spec_from_file_location(name,demos/name/'engine.py')
    mod=module_from_spec(spec);spec.loader.exec_module(mod)
    return mod
atomic=engine('v16.26-consistency-increment-law').atomic
push=engine('v16.23-overlap-descent').push
tree=p.Q
parents=(-1,0,0,0,0)
ambient=(0,1,2,3,4)
grades=(1,2,2,2,2)
def view(row):
    return [0]+[i+1 for i in range(4) if row>>i&1]
def perform_cut(rows,actor,site):
    rec=atomic(parents,[view(r) for r in rows],actor,site+1)
    after=tuple(sum(1<<(i-1) for i in y if i) for y in rec['after'])
    assert after==tuple(r^(1<<site) if i==actor else r for i,r in enumerate(rows))
    return after,{k:rec[k] for k in ('h_before','h_after','tau_after','delta_h','trigger')}
@lru_cache(None)
def pin(row):
    return int(push(parents,ambient,view(row),grades)[0])
LEAVES=tuple(permutations(range(4)))
def transform(row,leaves):
    return sum(1<<i for i,v in enumerate(leaves) if row>>v&1)
def unmap(row,leaves):
    return sum(1<<v for i,v in enumerate(leaves) if row>>i&1)
MAPS={o:tuple(transform(r,o) for r in range(16)) for o in LEAVES}
INVERSE={o:tuple(unmap(r,o) for r in range(16)) for o in LEAVES}

@lru_cache(maxsize=8192)
def original(rows):
    k=len(rows)
    roots=[[a for a,r in enumerate(rows) if r>>v&1] for v in range(4)]
    state=p.encode_roots(k,roots)
    profile=[p.coordinate(state,p.layout(tree)[0])]
    path=p.normalize(state,tree,k,profile)
    assert path[-1]==p.canonical(tree,k,profile)
    words=[[row] for row in rows]
    for old,new in zip(path,path[1:]):
        changed=[(a,n) for a,(o,n) in enumerate(zip(old,new)) if o!=n]
        assert len(changed)==1
        a,val=changed[0]
        assert (old[a]^val).bit_count()==1
        words[a].append(val>>1)
    return profile[0],tuple(tuple(w) for w in words)

def traces(rows,order,leaves):
    t,inv=MAPS[leaves],INVERSE[leaves]
    q,words=original(tuple(t[rows[a]] for a in order))
    return q,{a:tuple(inv[x] for x in w) for a,w in zip(order,words)}

def first_loss(word):
    return next((i,old^new,new) for i,(old,new) in enumerate(zip(word,word[1:]),1) if old&~new)

def run_case(rows,a,b,s,t):
    x,left=perform_cut(rows,a,s);y,right=perform_cut(rows,a,t)
    counts=Counter();examples={};before_sets=[set(),set()];after_sets=[set(),set()]
    digest=sha256()
    for order in permutations(range(len(rows))):
        for leaves in LEAVES:
            qx,wx=traces(x,order,leaves);qy,wy=traces(y,order,leaves)
            assert (qx,qy)==(2,3)
            for j,r in enumerate(rows):
                if j==a:continue
                d=r.bit_count();h=4-d
                l,rw=wx[j],wy[j]
                fx,fy=first_loss(l),first_loss(rw)
                assert [z.bit_count() for z in l[:h+2]]==list(range(d,5))+[3]
                assert [z.bit_count() for z in rw[:h+1]]==list(range(d,4))+[2]
                assert fx[0]==h+1 and fy[0]==h
                assert (pin(fx[2]),pin(fy[2]))==(3,5)
                counts['receiver_comparisons']+=1
                counts['all_matched_loss_addresses']+=int(fx[1]==fy[1])
            counts['order_pairs']+=1
            lw,rw=wx[b],wy[b];h=4-rows[b].bit_count()
            fx,fy=first_loss(lw),first_loss(rw)
            counts['B_matched_loss_address']+=int(fx[1]==fy[1])
            for i,w in enumerate((lw,rw)):
                before_sets[i].add(w[:h])
                after_sets[i].add(w[:h+1])
            for key,ok in [('identity',order==tuple(range(len(rows))) and leaves==tuple(range(4))),
                           ('common_loss',fx[1]==fy[1])]:
                if ok:examples.setdefault(key,dict(chart_order=order,leaf_order=leaves,q2_word=lw,q3_word=rw,
                                                  first_losses=[fx,fy]))
            digest.update(bytes(order+leaves+lw)+b'/'+bytes(rw)+b'\n')
    assert before_sets[0]==before_sets[1] and not after_sets[0]&after_sets[1]
    works=lambda h:[4*(h[b]^z).bit_count() for z in h]
    return dict(rows=rows,A=a,B=b,noncritical=s+1,critical=t+1,cuts=[left,right],counts=counts,
                earlier_addressed_prefixes=len(before_sets[0]),common_decisive_prefixes=0,
                work_rows=[works(rows),works(x),works(y)],examples=examples,sha256=digest.hexdigest())

def selected_paths(rows,a,s,t):
    saved=[]
    for site in (s,t):
        r,_=perform_cut(rows,a,site)
        roots=[[j for j,v in enumerate(r) if v>>i&1] for i in range(4)]
        k=len(r);init=p.encode_roots(k,roots);q=[p.coordinate(init,p.layout(tree)[0])]
        path=p.normalize(init,tree,k,q);end=p.canonical(tree,k,q)
        peak=path_check(tree,k,q,path,init,end)
        saved.append(dict(identity=['R',k,*roots],q=q,start=init,end=end,path=path,peak=peak))
    return saved

if __name__=='__main__':
    # From the preregistered search: a historical k=3 instance and the larger
    # no-singleton example with identical work at the indicated receiver.
    cases=[( (1,6,11),2,0,1,0),((7,1,1,2,10,12),0,5,1,0)]
    out=[run_case(*case) for case in cases]
    paths=[selected_paths(rows,a,s,t) for rows,a,b,s,t in cases]
    print(json.dumps(dict(cases=out,historical_paths=paths[0],extension_paths=paths[1]),sort_keys=True))
