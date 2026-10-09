import itertools
import json
from functools import lru_cache
from pins import SCOPE

@lru_cache(None)
def tau(f,k):
    return min(h.bit_count() for h in range(1<<k) if all(s&h for s in f))

@lru_cache(None)
def star(f,k):
    w=1<<k
    return tuple(sum(not(s&h) for s in f) for h in [w]+[w|(1<<y) for y in range(k)])

def decode(delta):
    if not delta: raise ValueError('empty increment')
    sig=delta[0]
    if sig==0:
        if any(delta): raise ValueError('non-atomic star response')
        return None
    if sig not in (-1,1) or any(v not in (0,sig) for v in delta[1:]):
        raise ValueError('invalid marker response')
    return sum(1<<y for y,v in enumerate(delta[1:]) if v==0)

def produce():
    rows=[]
    for n in range(1,4):
        for f in itertools.product(range(1,8),repeat=n):
            for r,p,c in itertools.product(range(n),range(2),range(2)):
                before=list(f)
                if p: before[r]|=8
                after=before.copy()
                if c: after[r]^=8
                a,b=star(tuple(before),3),star(tuple(after),3)
                delta=[v-u for u,v in zip(a,b)]
                rows.append({'family':list(f),'root':r,'phase':p,'commit':c,
                             'floors':[s.bit_count() for s in f],
                             'star_before':list(a),'star_after':list(b),
                             'tau':[tau(tuple(before),4),tau(tuple(after),4)],
                             'readout':decode(delta),'next_phase':p+1 if c else p})
    native={'original':[3,6,5,24],'nonfresh':[11,6,5,24],'marked0':[35,6,5,24],
            'reused':[35,6,5,56],'hidden_a':[3,6,5,24],'hidden_b':[3,6,5,56],
            'hidden_a_marked':[3,6,5,88],'hidden_b_marked':[3,6,5,120]}
    f=native['original'].copy();values=[];history=[tau(tuple(f),6)]
    for r in range(4):
        a=star(tuple(f),5);f[r]|=32;b=star(tuple(f),5)
        values.append(decode([v-u for u,v in zip(a,b)]));history.append(tau(tuple(f),6))
        f[r]^=32;history.append(tau(tuple(f),6))
    return {'scope':SCOPE,'records':rows,'native':native,
            'scan':{'readouts':values,'final':f,'commits':8,'tau_history':history},
            'claims':{'guaranteed_completion':False,'count_access_derived':False,
                      'uniform_preissue_safety':True,'exact_restoration':True}}

if __name__=='__main__': print(json.dumps(produce(),sort_keys=True,separators=(',',':')))
