import itertools,json,sys
from functools import lru_cache

def require(x,msg):
    if not x:raise ValueError(msg)

@lru_cache(None)
def hitting(s):
    roots=[[b for b in range(8) if r>>b&1] for r in s]
    return min(len(set(reps)) for reps in itertools.product(*roots))

def augment(core,bits):
    return [sum(1<<x for x in r)+sum((1<<(6+j))*bits[j][i] for j in range(2)) for i,r in enumerate(core)]

def rows(bits,a,d):
    e=next(z for z in (0,3,4) if z not in (a,d))
    cores=[[{a,1},{1,2},{a,2},{d,e}],
           [{a,1},{1,2},{a,2},{d,e,5}],
           [{a,1},{1,2},{a,2},{e,5}],
           [{a,1,d},{1,2},{a,2},{e,5}],
           [{1,d},{1,2},{a,2},{e,5}],
           [{1,d},{1,2},{a,2,d},{e,5}],
           [{1,d},{1,2},{2,d},{e,5}],
           [{1,d},{1,2},{2,d},{a,e,5}],
           [{1,d},{1,2},{2,d},{a,e}]]
    return [augment(c,bits) for c in cores]

@lru_cache(None)
def expected_bytes():
    sources=[];paths=[];walks=[]
    columns=list(itertools.product((0,1),repeat=4))
    columns.sort(key=lambda b:sum(x<<i for i,x in enumerate(b)))
    for bits in itertools.product(columns,repeat=2):
        u,v=[sum(x<<i for i,x in enumerate(col)) for col in bits]
        separated=all(not (col[3] and any(col[:3])) and not all(col[:3]) for col in bits)
        for a in (0,3,4):
            rest=[x for x in (0,3,4) if x!=a]
            s=augment([{a,1},{1,2},{a,2},set(rest)],bits);t=hitting(tuple(s));protected=t>=3
            require(protected==separated,'structural classification')
            require(t<=3,'source upper bound')
            sources.append({'id':[u,v,a],'state':s,'tau':t,'protected':protected,'separated':separated})
            if not protected:continue
            for d in rest:
                states=rows(bits,a,d);ts=[hitting(tuple(s)) for s in states]
                require(all(t==3 for t in ts),'path hitting number')
                mins=[min(s[i].bit_count() for s in states) for i in range(4)]
                require(mins==[s.bit_count() for s in states[0]],'all original floors')
                for l,r in zip(states,states[1:]):
                    require(sum((x^y).bit_count() for x,y in zip(l,r))==1,'one native incidence')
                require(not any(x&32 for x in states[-1]),'marker retained')
                paths.append({'id':[u,v,a,d],'states':states,'tau':ts,'minimum_sizes':mins})
                for e in (0,3,4):
                    if e==d:continue
                    again=rows(bits,d,e)
                    require(states[-1]==again[0],'renewal middle')
                    final=augment([{e,1},{1,2},{e,2},set((0,3,4))-{e}],bits)
                    require(again[-1]==final,'renewal destination')
                    walks.append({'id':[u,v,a,d,e],'states':states+again[1:]})
    expected={'scope_commit':'e51e7333c581b1b343c2e6311b97d898b33e3203','claims':{'observer_origin':False,'guaranteed_request_completion':False,'optimal':False},'sources':sources,'paths':paths,'walks':walks}
    require((len(sources),len(paths),len(walks))==(768,384,768),'canonical domain')
    return json.dumps(expected,sort_keys=True,separators=(',',':'))

def verify(cert):
    require(json.dumps(cert,sort_keys=True,separators=(',',':'))==expected_bytes(),'full canonical identities, types or values differ')
    return {'status':'PASS','sources':768,'protected_sources':192,'paths':384,'two_exchange_words':768}

if __name__=='__main__':print(json.dumps(verify(json.load(open(sys.argv[1]))),sort_keys=True))
