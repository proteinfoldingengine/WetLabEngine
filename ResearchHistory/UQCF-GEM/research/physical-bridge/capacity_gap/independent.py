#!/usr/bin/env python3
import functools,itertools,json,pathlib,sys
@functools.lru_cache(None)
def minimum(fam):
    roots=[frozenset(r) for r in fam]
    if any(not r for r in roots):return 99
    frontier={frozenset()}
    for root in roots:
        c={v|{x} for v in frontier for x in root}
        frontier={v for v in c if not any(w<v for w in c)}
    return min(map(len,frontier))
def tau(s):return minimum(tuple(tuple(sorted(r)) for r in s))
def bitset(s):return [sum(2**x for x in r) for r in s]
def decode(s):return [{i for i in range(max(s).bit_length()) if (v//2**i)%2} for v in s]
def footprints(s,n):return [{i for i,r in enumerate(s) if x in r} for x in range(n)]
def maximal(s,n):
    fs={frozenset(f) for f in footprints(s,n) if f}
    return sorted([set(f) for f in fs if not any(f<g for g in fs)],key=lambda f:sum(2**i for i in f))
def packed(fs):return [sum(2**i for i in f) for f in fs]
def complete(s,q,u):return [r|({u} if (q//2**i)%2 else set()) for i,r in enumerate(s)]
def native(s,f):return all(len(r)>=d for r,d in zip(s,f)) and tau(s) in (3,4)

# Independent complete three-label core universe; no producer allocations.
THREE=[]
for v in itertools.product(range(1,8),repeat=4):
    s=decode(v);sizes=tuple(map(len,s));fp=footprints(s,3)
    THREE.append((sizes,fp))
@functools.lru_cache(None)
def static_small(M,f):
    old=[{i for i in range(4) if (j//2**i)%2} for j in M]
    for sizes,fp in THREE:
        if all(a>=b for a,b in zip(sizes,f)) and all(any(p<=o for o in old) for p in fp):return 3
    # no <=2-label candidate can be safe: it would map to an original <=2 cover.
    # Original core itself is a <=4-label universally admissible candidate.
    return 4
def family(n):
    s=[{0,3+i} for i in range(n)]+[{1,3+i} for i in range(n)]+[{2}]
    d=[{0,3} for _ in range(n)]+[{1,4} for _ in range(n)]+[{2}];f=[2]*(2*n)+[1]
    M=maximal(s,n+3)
    # Distinct algorithm: enumerate multisets of maximal sets, test actual root sizes and cover.
    cap=None
    for count in range(1,6):
        for assignment in itertools.combinations_with_replacement(range(len(M)),count):
            candidate=[{x for x,j in enumerate(assignment) if i in M[j]} for i in range(len(s))]
            if all(len(r)>=v for r,v in zip(candidate,f)) and tau(candidate)<=4:cap=count;break
        if cap is not None:break
    if cap!=5:raise ValueError('family capacity')
    qs=[q for q in range(2**len(s)) if native(complete(s,q,n+3),f)]
    ts=[tau(complete(d,q,n+3)) for q in qs]
    if not all(native(complete(d,q,n+3),f) for q in qs):raise ValueError('target')
    old=footprints(s,n+3);rows=[]
    for i in range(len(s)):
        for x in range(n+3):
            c=[r.copy() for r in s];c[i]=c[i]^{x}
            complement=set(range(len(s)))-(old[x]|{i})
            q=0 if x in s[i] else sum(2**j for j in complement)
            a=complete(s,q,n+3);b=complete(c,q,n+3)
            if not native(a,f) or native(b,f):raise ValueError('not isolated')
            rows.append({'root':i,'label':x,'q':q,'source_tau':tau(a),'candidate_tau':tau(b),'source_admitted':native(a,f),'candidate_admitted':native(b,f)})
    return {'n':n,'source':bitset(s),'target':bitset(d),'floors':f,'maximal':packed(M),'capacity':cap,'absent_labels':list(range(5,n+3)),'protected_masks':qs,'target_taus':ts,'first_toggles':rows}
def upper():
    s=[{0,3+i} for i in range(5)]+[{1 if i<3 else 2,3+i} for i in range(5)]
    d=[{3+i} for i in range(5)]*2;old=footprints(s,8);now=footprints(d,8)
    return {'source':bitset(s),'candidate':bitset(d),'taus':[tau(s),tau(d)],'floors':all(len(r)>=1 for r in d),'domination':all(any(f<=o for o in old) for f in now),'admitted':native(d,[1]*10)}
def build():
    rows=[]
    for v in itertools.product(range(1,16),repeat=4):
        s=decode(v)
        if set.union(*s)!=set(range(4)) or tau(s) not in (3,4):continue
        f=tuple(map(len,s));M=packed(maximal(s,4))
        rows.append({'core':list(v),'tau':tau(s),'maximal':M,'capacity':[static_small(tuple(M),f),static_small(tuple(M),tuple(max(1,x-1) for x in f))]})
    fam=[family(n) for n in (2,3,4,5)]
    return {'schema':'capacity-gap-v1','cores':rows,'family':fam,'upper_control':upper(),'counts':{'core_sources':len(rows),'floor_instances':2*len(rows),'family_sources':len(fam),'protected_completions':sum(len(r['protected_masks']) for r in fam),'rejecting_first_toggles':sum(len(r['first_toggles']) for r in fam),'upper_controls':1}}
def validate(actual,expected=None):
    if expected is None:expected=build()
    def check(a,b,p):
        if type(a)!=type(b):raise ValueError('type '+p)
        if isinstance(b,dict):
            if set(a)!=set(b):raise ValueError('members '+p)
            for k in b:check(a[k],b[k],p+'/'+k)
        elif isinstance(b,list):
            if len(a)!=len(b):raise ValueError('length '+p)
            for i,(x,y) in enumerate(zip(a,b)):check(x,y,p+'/'+str(i))
        elif a!=b:raise ValueError('value '+p)
    check(actual,expected,'root');return {'status':'PASS','complete_typed_reconstruction':True,**expected['counts']}
if __name__=='__main__':print(json.dumps(validate(json.loads(pathlib.Path(sys.argv[1]).read_text())),sort_keys=True))
