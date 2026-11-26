"""Replay ordinary primitive calls, with physical charts and leaves fixed across priorities."""
from collections import Counter
from functools import lru_cache
from hashlib import sha256
from importlib.util import module_from_spec, spec_from_file_location
from itertools import permutations
from pathlib import Path
import json
import sys

demos=Path(sys.argv[1]).resolve()
sys.path.insert(0,str(demos/'v16.43-star-fiber-classification'))
from producer import normalize

def historical(version):
    spec=spec_from_file_location(version,(demos/version/'engine.py'))
    module=module_from_spec(spec)
    spec.loader.exec_module(module)
    return module
p1=historical('v16.23-overlap-descent')
atomic=historical('v16.26-consistency-increment-law').atomic
cols=(3,5,14,23,25)
k=m=5
B=3

def rows(columns,chart_order,leaf_order):
    return tuple(1+sum(1<<(i+1) for i,v in enumerate(leaf_order) if columns[v] & (1<<a))
                 for a in chart_order)

def decode(row,leaf_order):
    return sum(1<<v for i,v in enumerate(leaf_order) if row & (1<<(i+1)))

def covers(columns,k):
    hits=[h for h in range(1,1<<k) if all(h&s for s in columns)]
    q=min(x.bit_count() for x in hits)
    return [x for x in hits if x.bit_count()==q]

def cut_at(columns,selected):
    n=len(columns);order=tuple(range(n));charts=range(max(s.bit_length() for s in columns))
    state=rows(columns,charts,order)
    views=[[i for i in range(n+1) if row>>i&1] for row in state]
    receipt=atomic((-1,)+(0,)*n,views,0,selected+1)
    after=tuple(sum(1<<a for a,y in enumerate(receipt['after']) if i+1 in y) for i in range(n))
    assert after==tuple(s^1 if i==selected else s for i,s in enumerate(columns))
    return after,{key:receipt[key] for key in ('tau_before','tau_after','h_before','h_after','delta_h','trigger')}

@lru_cache(None)
def grade(mask):
    view=(0,)+tuple(v+1 for v in range(m) if mask & (1<<v))
    vals=p1.push((-1,)+(0,)*m,tuple(range(m+1)),view,(1,)+(2,)*m)
    assert all(a==2 for a in vals[1:]) and vals[0]==11-2*mask.bit_count()
    return int(vals[0])

def receiver_trace(columns,chart_order,leaf_order):
    index=chart_order.index(B)
    path=normalize(rows(columns,chart_order,leaf_order),m,k,2)
    boundary=next(i for i,state in enumerate(path) if sum(x.bit_count()-1 for x in state)==m)
    word=[]
    change_steps=[]
    for i,state in enumerate(path):
        physical=decode(state[index],leaf_order)
        if not word or word[-1]!=physical:
            word.append(physical);change_steps.append(i)
    return dict(word=word,pin=[grade(x) for x in word],change_steps=change_steps,
                boundary=boundary,at_boundary=decode(path[boundary][index],leaf_order),
                terminal=path[-1])

def archived_example():
    tiny=(1,3,13);charts=tuple(range(4));leaves=tuple(range(3))
    # Index physical rows lexicographically as in the original graph archive.
    from itertools import product
    states=sorted(rows(s,charts,leaves) for s in product(range(1,16),repeat=3))
    lookup={s:i for i,s in enumerate(states)}
    out=[]
    for target in (1,2):
        changed,rec=cut_at(tiny,target)
        path=normalize(rows(changed,charts,leaves),3,4,2)
        out.append(dict(target=target+1,atomic=rec,q=2,state=lookup[tuple(path[0])],
                        path=[lookup[tuple(s)] for s in path],rows=path))
    return out

x,keep_receipt=cut_at(cols,4)
y,lose_receipt=cut_at(cols,3)
assert covers(cols,k)==[3,5,9] and covers(x,k)==[9] and covers(y,k)==[3,5]
orders=list(permutations(range(5)))
def first_gain(word):
    for before,after in zip(word,word[1:]):
        if after & ~before:
            return after.bit_count(), bool((after & ~before) & ~word[0]),after^before
    return None

counter=Counter();examples={};digest=sha256()
availability=Counter();after_counts=[Counter(),Counter()];fresh=[Counter(),Counter()]
matched_gain_examples={}

for chart_order in orders:
    for leaf_order in orders:
        left=receiver_trace(x,chart_order,leaf_order);right=receiver_trace(y,chart_order,leaf_order)
        assert left['at_boundary']==20 and right['at_boundary']==0
        assert left['word'][0]==right['word'][0]==20 and left['terminal']==right['terminal']
        same=left['word']==right['word']
        anonymous=left['pin']==right['pin']
        counter['trials']+=1
        counter['addressed_collisions']+=same
        counter['count_collisions']+=anonymous
        # At the boundary the positive arm has made no receiver edit; the other erased both leaves.
        assert all(i==0 or i>left['boundary'] for i in left['change_steps'])
        assert sum(0<i<=right['boundary'] for i in right['change_steps'])==2
        lg,rg=first_gain(left['word']),first_gain(right['word'])
        availability[('yes' if lg else 'no')+'_'+('yes' if rg else 'no')]+=1
        for side,gain in enumerate((lg,rg)):
            if gain:
                count,novel,_=gain
                assert (count>=2 if side==0 else count==1)
                after_counts[side][count]+=1
                fresh[side]['new_to_prior' if novel else 'held_initially']+=1
        if lg and rg:
            name='same_first_gained_leaf' if lg[2]==rg[2] else 'different_first_gained_leaf'
            matched_gain_examples.setdefault(name,dict(chart_order=chart_order,leaf_order=leaf_order,first=[lg,rg]))
            counter[name]+=1
        key='collision' if same else 'separation'
        examples.setdefault(key,dict(chart_order=chart_order,leaf_order=leaf_order,keep=left,lose=right))
        digest.update(bytes(chart_order+leaf_order)+bytes(left['word'])+b'|'+bytes(right['word'])+b'\n')
print(json.dumps(dict(census=counter,gain_availability=availability,counts_after_gain=after_counts,
                      gained_address=fresh,gain_examples=matched_gain_examples,word_digest=digest.hexdigest(),examples=examples,
                      initial_covers=covers(cols,k),survival_covers=covers(x,k),erasure_covers=covers(y,k),
                      cuts=[keep_receipt,lose_receipt],boundary_pin=[grade(20),grade(0)],
                      archived=archived_example()),sort_keys=True))
