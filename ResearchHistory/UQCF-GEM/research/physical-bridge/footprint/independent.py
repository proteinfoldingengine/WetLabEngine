"""Independent set/representative-union reconstruction. Does not import producer."""
import functools,itertools,json,pathlib,sys

def unpack(n): return frozenset(i for i in range(n.bit_length()) if n&(2**i))

@functools.lru_cache(None)
def hit(s):
    candidates={frozenset()}
    for root in s:
        candidates={h|{x} for h in candidates for x in root}
        if not candidates: return 99
        # Supersets cannot improve a minimum representative union.
        candidates={h for h in candidates if not any(g<h for g in candidates)}
    return min(map(len,candidates),default=0)

def with_hidden(d,q,p): return tuple(r|({p} if i in q else set()) for i,r in enumerate(d))

def core_conditions(c,d,p):
    ok=True
    for x in range(p):
        roots=[c[i] for i,r in enumerate(d) if x in r]
        if roots and not set.intersection(*(set(r) for r in roots)): ok=False
    return [all(len(a)>=len(b) for a,b in zip(d,c)),hit(tuple(d))<=4,ok]

def permitted(c,p):
    return [q for q in range(2**len(c)) if 3<=hit(with_hidden(c,unpack(q),p))<=4]

def reconstruct_fixture(name,values,p,single=False):
    c=tuple(map(unpack,values)); qs=permitted(c,p); rows=[]
    for code in range(2**(p*len(c))):
        d=tuple(unpack((code//2**(p*i))%(2**p)) for i in range(len(c)))
        if single and any(len(r)>1 for r in d): continue
        bad=[]
        for q in qs:
            full=with_hidden(d,unpack(q),p)
            if any(len(r)<len(s) for r,s in zip(full,c)) or not 3<=hit(full)<=4: bad.append(q)
        cond=core_conditions(c,d,p)
        if all(cond)!=(not bad): raise ValueError('theorem counterexample')
        rows.append([code,cond,not bad,bad])
    return dict(name=name,core=list(values),palette=p,floors=list(map(len,c)),source_masks=qs,rows=rows)

def reconstruct_application():
    c=tuple(map(unpack,[1,1,1,2,4,24])); qs=permitted(c,6)
    # Construct stages directly, independently of the producer action list.
    stages=[c,c[:-1]+(frozenset({3,4,5}),),c[:-1]+(frozenset({4,5}),)]
    for k in range(1,4): stages.append(tuple(frozenset({0,3}) if i<k else frozenset({0}) for i in range(3))+(c[3],c[4],frozenset({4,5})))
    for k in range(1,4): stages.append(tuple(frozenset({3}) if i<k else frozenset({0,3}) for i in range(3))+(c[3],c[4],frozenset({4,5})))
    stages.extend([stages[-1][:-1]+(frozenset({0,4,5}),),stages[-1][:-1]+(frozenset({0,4}),)])
    neighbors=[]
    for i in range(6):
        for x in range(6):
            d=list(c);d[i]=d[i]^{x}
            safe=all(all(len(a)>=len(b) for a,b in zip(with_hidden(d,unpack(q),6),c)) and 3<=hit(with_hidden(d,unpack(q),6))<=4 for q in qs)
            if safe: neighbors.append([i,x])
    cross=(c[0]|{3},)+c[1:]
    premature=(frozenset({3}),c[1],c[2],c[3],c[4],frozenset({4,5}))
    return dict(core=[1,1,1,2,4,24],source_masks=qs,path=[[sum(2**x for x in r) for r in s] for s in stages],
                cross_role_taus=[hit(with_hidden(c,{1,2,3,4},6)),hit(with_hidden(cross,{1,2,3,4},6))],
                premature_deletion_tau=hit(premature),
                path_taus=[[hit(with_hidden(s,unpack(q),6)) for s in stages] for q in qs],
                no_spare_safe_neighbors=[a for a in neighbors if a[1]!=5],spare_safe_neighbors=neighbors)

@functools.lru_cache(None)
def expected_json():
    fs=[reconstruct_fixture('three-with-spare',[1,2,4],4),reconstruct_fixture('repeated-role',[1,1,2,4],3),reconstruct_fixture('overlapping-role',[3,1,2,4],3),reconstruct_fixture('tau4-singleton-candidates',[1,2,4,8],4,True)]
    c=list(map(unpack,[1,1,2,2,4]));d=list(map(unpack,[1,2,4,8,16]))
    result=dict(schema='universal-footprint-v1',fixtures=fs,application=reconstruct_application(),upper_control=dict(core=[1,1,2,2,4],candidate=[1,2,4,8,16],candidate_tau=hit(tuple(d)),conditions=core_conditions(c,d,5)))
    return json.dumps(result,sort_keys=True,separators=(',',':'))

def validate(d):
    if json.dumps(d,sort_keys=True,separators=(',',':'))!=expected_json(): raise ValueError('complete typed reconstruction mismatch')
    return True

if __name__=='__main__':
    validate(json.loads(pathlib.Path(sys.argv[1]).read_text())); print(json.dumps({'status':'PASS','method':'complete independent set/representative-union reconstruction'}))
