import itertools,json
from functools import lru_cache

SCOPE='e51e7333c581b1b343c2e6311b97d898b33e3203'
POOL=(0,3,4)

@lru_cache(None)
def tau(state):
    for n in range(1,9):
        for labels in itertools.combinations(range(8),n):
            h=sum(1<<x for x in labels)
            if all(s&h for s in state):return n
    raise ValueError('empty support')

def source(u,v,a):
    other=set(POOL)-{a}
    ss=[{a,1},{1,2},{a,2},other]
    for z,m in ((6,u),(7,v)):
        for i in range(4):
            if m&(1<<i):ss[i].add(z)
    return tuple(sum(1<<x for x in s) for s in ss)

@lru_cache(None)
def path(u,v,a,d):
    s=list(source(u,v,a));states=[s.copy()]
    for root,label,sign in ((3,5,1),(3,d,-1),(0,d,1),(0,a,-1),(2,d,1),(2,a,-1),(3,a,1),(3,5,-1)):
        present=bool(s[root]&(1<<label))
        if present!=(sign==-1):raise ValueError('syntax')
        s[root]^=1<<label;states.append(s.copy())
    return {'id':[u,v,a,d],'states':states,'tau':[tau(tuple(x)) for x in states],
            'minimum_sizes':[min(s[i].bit_count() for s in states) for i in range(4)]}

def produce():
    sources=[];paths=[];walks=[]
    allowed={0,1,2,3,4,5,6,8}
    for u,v,a in itertools.product(range(16),range(16),POOL):
        s=source(u,v,a);t=tau(s);protected=3<=t<=4
        sources.append({'id':[u,v,a],'state':list(s),'tau':t,'protected':protected,'separated':u in allowed and v in allowed})
        if protected:
            for d in POOL:
                if d==a:continue
                p=path(u,v,a,d);paths.append(p)
                for e in POOL:
                    if e==d:continue
                    q=path(u,v,d,e)
                    walks.append({'id':[u,v,a,d,e],'states':p['states']+q['states'][1:]})
    return {'scope_commit':SCOPE,'claims':{'observer_origin':False,'guaranteed_request_completion':False,'optimal':False},'sources':sources,'paths':paths,'walks':walks}

if __name__=='__main__':print(json.dumps(produce(),sort_keys=True,separators=(',',':')))
