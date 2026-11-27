"""Proof companion: constructed exact stock M4 cases, not archived catalog runs."""
from hashlib import sha1
from pathlib import Path
from itertools import permutations, product
import functools,json,random,sys
PINNED={
    'model.py':'a4a6407990c36084ab3b6e8e7da9022a4f9d63a8',
    'mechanisms.py':'ab3541cba29d5e1ebd4fe6c56128daf020c1a81f',
    'verifier.py':'e19999dfd46cd134d8191a59da7b8bf2cdb74b43',
}
d=Path(sys.argv[1]).resolve()
for filename,expected in PINNED.items():
    b=(d/filename).read_bytes()
    assert sha1(f'blob {len(b)}\0'.encode()+b).hexdigest()==expected
sys.path.insert(0,str(d))
from mechanisms import produce
from verifier import verify_record
from copy import deepcopy
BASE=[342,169,169,170,356,464,139,43]
F=[2,2,3,1,1,1,1,1]
EXT=[3414,681,681,682,356,3536,651,555]
G=[2,2,3,1,1,1,3,1]
COMMANDS=[[(1,5),(0,1)],[(1,7),(0,1)],[(0,1)]]
P8=tuple(range(8))
@functools.lru_cache(maxsize=None)
def content(m,k):
    return [i for i in range(k) if m & (1<<i)]
def mask(ls):
    return sum(1<<u for u in ls)
def case(m,f,k,ops,order=P8,labels=None):
    if labels is None: labels=tuple(range(k))
    return {'identity':['M4',{'kind':'clone','k':k,'a':[f[i] for i in order],'q':2},
              [sorted(labels[j] for j in content(m[i],k)) for i in order],
              {'operations':[[labels[u],labels[v]] for u,v in ops]}]}
def inspect(c,k,order=P8,labels=None):
    if labels is None:labels=tuple(range(k))
    back=[labels.index(j) for j in range(k)]
    inv=[order.index(j) for j in P8]
    r=produce(c)
    assert r['status']=='PASS' and set(r['tau'])=={2}
    assert not verify_record(c,r)
    path=[tuple(mask(back[u] for u in f[j]) for j in inv) for f in r['path']]
    # Independent fixed {3,6} cover and fixed disjoint rows 4 and 6.
    assert all(all(z&72 for z in f) and not f[4]&f[6] for f in path)
    assert all(min(z.bit_count()-floor for z,floor in zip(frame,[c['identity'][1]['a'][j] for j in inv]))>=0 for frame in path)
    assert all(w['f']==w['contraction']==w['before']==w['after']==2 and w['safe'] and w['exact'] for w in r['facts']['clones'])
    piv=[w['end'] for w in r['facts']['clones']]
    return path,piv,r
summary={}
for m,f,k in ((BASE,F,9),(EXT,G,12)):
    originals=[inspect(case(m,f,k,o),k) for o in COMMANDS]
    expected=[(326,325,169),(338,169,337),(342,169,341)] if k==9 else [(326,325,681),(3410,681,3409),(3414,681,3413)]
    assert [p[-1][:3] for p,_,_ in originals]==expected
    for i,(path,piv,r) in enumerate(originals):
        assert [j for j,(x,y) in enumerate(zip(path[0],path[-1])) if x!=y]==([0,1] if i==0 else [0,2] if i==1 else [2])
        if i<2:
            assert [j for j,(x,y) in enumerate(zip(path[0],path[piv[0]])) if x!=y]==[0]
            assert all(path[j][0]&path[j+1][0]==path[j+1][0] for j in range(piv[0]))
            # No source prefix: identical post-state is sufficient to replay suffix.
            bare,_,_=inspect(case(path[piv[0]],f,k,COMMANDS[-1]),k)
            assert bare==path[piv[0]:]
        bad=deepcopy(r)
        bad['facts']['clones'][-1]['demands'].reverse()
        assert verify_record(case(m,f,k,COMMANDS[i]),bad)
    for order in permutations(P8):
        for i,ops in enumerate(COMMANDS[:2]):
            p,ends,_=inspect(case(m,f,k,ops,order),k,order)
            assert (p,ends)==originals[i][:2]
    # The spectrum of sizes and floors proves the extended endpoint independence
    # for all simultaneous row/label relabelings; this finite set is a code check.
    reverse=tuple(reversed(range(k)))
    if k==9:
        # Label-order dependence in original witness: explicitly find one.
        forced=None
        for s in range(1,121):
            lab=list(range(k));random.Random(s).shuffle(lab)
            try:
                p,_,_=inspect(case(m,f,k,COMMANDS[0],labels=lab),k,labels=lab)
            except AssertionError:continue
            if p[-1]!=originals[0][0][-1]:
                forced=(lab,p[-1]);break
        assert forced
        summary[str(k)]={'counter_order':forced}
    else:
        variants=[reverse]
        for s in range(256):
            lab=list(range(k));random.Random(s).shuffle(lab); variants.append(tuple(lab))
        for lab in variants:
            for i,ops in enumerate(COMMANDS):
                p,ends,_=inspect(case(m,f,k,ops,labels=lab),k,labels=lab)
                assert ends==originals[i][1] and all(p[e]==originals[i][0][e] for e in ends)
        exact_counts=[]
        for post in [p[ends[0]] for p,ends,_ in originals[:2]]:
            alts={}
            for u,v in product(range(k),repeat=2):
                if u==v:continue
                col=case(post,f,k,[(u,v)])
                r=produce(col)
                if r['status']=='PASS' and all(q==2 for q in r['tau']):
                    assert not verify_record(col,r)
                    alts[u,v]=len(r['path'])-1
            assert (0,1) in alts and len(alts)>1 and (3,9) in alts and alts[3,9]==0
            exact_counts.append((len(alts),sum(n>0 for n in alts.values())))
        summary[str(k)]={'tested_label_orders':len(variants),'one_command_choices_pass_exact_and_nontrivial':exact_counts}
    summary[str(k)].update(normally_ordered_primitive_paths=[p for p,_,_ in originals],
        command_end_frame_indices=[e for _,e,_ in originals],row_order_calls=80640)
print(json.dumps(summary,sort_keys=True,indent=2))
