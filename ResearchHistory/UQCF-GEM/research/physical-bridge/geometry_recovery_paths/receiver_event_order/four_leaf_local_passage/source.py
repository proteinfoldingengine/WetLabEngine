"""Check all initial withdrawals, including source-at-receiver, and the no-cut control."""
from collections import Counter
from itertools import combinations
import json
import replay

rows=(7,1,1,2,10,12)
b=5
opts=[list(pair) for pair in combinations(range(len(rows)),2) if rows[pair[0]]|rows[pair[1]]==15]
assert opts==[[0,4],[0,5]]
cases=[]
for a,r in enumerate(rows):
    for v in range(4):
        if not r>>v&1:continue
        after,receipt=replay.perform_cut(rows,a,v)
        cases.append((a,v,after,receipt))
assert len(cases)==10
assert [(a,v) for a,v,_,rec in cases if rec['trigger']]==[(0,0)]
assert all(rec['delta_h']==int(rec['trigger']) for _,_,_,rec in cases)
cases.append((None,None,rows,None))
stats=[]
orders=set()
for direction in (-1,1):
    for i in range(6):
        orders.add(tuple((i+j*direction)%6 for j in range(6)))
for a,v,state,receipt in cases:
    outcomes=Counter();prefixes=set()
    for order in sorted(orders):
        for leaves in replay.LEAVES:
            q,words=replay.traces(state,order,leaves)
            assert q==(3 if (a,v)==(0,0) else 2)
            trace=words[b]
            if a==b:trace=(rows[b],)+trace
            n,mask,retained=replay.first_loss(trace)
            outcomes[retained.bit_count()]+=1
            prefixes.add(trace[:n+1])
    want=1 if a==b else (2 if (a,v)==(0,0) else 3)
    assert outcomes=={want:len(orders)*len(replay.LEAVES)}
    stats.append(dict(source=a,leaf=None if v is None else v+1,atomic=receipt,
                      first_loss=want,pin=replay.pin((1<<want)-1),orderings=sum(outcomes.values()),
                      distinct_addressed_prefixes=len(prefixes)))
first,rec1=replay.perform_cut(rows,0,1)
second,rec2=replay.perform_cut(first,0,2)
assert second[0]==1 and (rec1['tau_after'],rec2['tau_after'])==(2,3)
q,w=replay.traces(second,tuple(range(6)),tuple(range(4)))
assert q==3 and replay.first_loss(w[b])[2].bit_count()==2
print(json.dumps(dict(optimal_initial_chart_pairs=opts,cases=stats,
                     multiple_cut_control=dict(leaves=[2,3],last_q=q,B_word=w[b])),sort_keys=True))
