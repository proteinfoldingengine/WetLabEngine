#!/usr/bin/env python3
import functools,itertools,json,pathlib,sys
@functools.lru_cache(None)
def tau(s):
    if 0 in s:return 99
    active=0
    for v in s:active|=v
    labels=[1<<i for i in range(active.bit_length()) if active&(1<<i)]
    for k in range(len(labels)+1):
        for c in itertools.combinations(labels,k):
            h=sum(c)
            if all(v&h for v in s):return k
    raise AssertionError('cover')
def footprints(s,n):return tuple(sum(1<<i for i,v in enumerate(s) if v&(1<<x)) for x in range(n))
def maximal(s,n):
    fp=set(footprints(s,n))-{0}
    return tuple(sorted(j for j in fp if not any(j!=h and j&~h==0 for h in fp)))
def allocations(total,k):
    if k==1:yield (total,);return
    for v in range(total+1):
        for rest in allocations(total-v,k-1):yield (v,)+rest
def cover4(occupied,m):
    for k in range(1,min(4,len(occupied))+1):
        for c in itertools.combinations(occupied,k):
            union=0
            for j in c:union|=j
            if union==(1<<m)-1:return True
    return False
@functools.lru_cache(None)
def capacity(M,f):
    # Original safe core guarantees an allocation using the original palette.
    for total in range(1,sum(f)+1):
        for ns in allocations(total,len(M)):
            if not all(sum(n for j,n in zip(M,ns) if j&(1<<i))>=d for i,d in enumerate(f)):continue
            if cover4([j for j,n in zip(M,ns) if n],len(f)):return total
    raise AssertionError('capacity')
def complete(s,q,u):return tuple(v|(u if q&(1<<i) else 0) for i,v in enumerate(s))
def native(s,f):return all(v.bit_count()>=d for v,d in zip(s,f)) and 3<=tau(tuple(s))<=4
def family(n):
    # a0,b1,f2,c_i=3+i(index0)
    s=[1|(1<<(3+i)) for i in range(n)]+[2|(1<<(3+i)) for i in range(n)]+[4]
    d=[9]*n+[18]*n+[4];f=[2]*(2*n)+[1];u=1<<(n+3)
    qs=[q for q in range(1<<len(s)) if native(complete(s,q,u),f)]
    target_taus=[tau(complete(d,q,u)) for q in qs]
    assert all(native(complete(d,q,u),f) for q in qs)
    rows=[];old=footprints(s,n+3);allroots=(1<<len(s))-1
    for i in range(len(s)):
        for x in range(n+3):
            candidate=s.copy();candidate[i]^=1<<x
            q=0 if s[i]&(1<<x) else allroots^(old[x]|(1<<i))
            a=complete(s,q,u);b=complete(candidate,q,u)
            row={'root':i,'label':x,'q':q,'source_tau':tau(a),'candidate_tau':tau(b),'source_admitted':native(a,f),'candidate_admitted':native(b,f)}
            assert row['source_admitted'] and not row['candidate_admitted']
            rows.append(row)
    return {'n':n,'source':s,'target':d,'floors':f,'maximal':list(maximal(s,n+3)),'capacity':capacity(maximal(s,n+3),tuple(f)),'absent_labels':list(range(5,n+3)),'protected_masks':qs,'target_taus':target_taus,'first_toggles':rows}
def upper():
    # roots T1..T5,X1..X5; labels A0,B1,C2,p_i3+i
    s=[1|(1<<(3+i)) for i in range(5)]+[(2 if i<3 else 4)|(1<<(3+i)) for i in range(5)]
    d=[1<<(3+i) for i in range(5)]*2;f=[1]*10
    old=footprints(s,8);now=footprints(d,8)
    return {'source':s,'candidate':d,'taus':[tau(tuple(s)),tau(tuple(d))],'floors':all(v.bit_count()>=1 for v in d),'domination':all(any(j&~h==0 for h in old) for j in now),'admitted':native(d,f)}
def build():
    cores=[]
    for s in itertools.product(range(1,16),repeat=4):
        if (s[0]|s[1]|s[2]|s[3])!=15 or tau(s) not in (3,4):continue
        f=tuple(v.bit_count() for v in s);slack=tuple(max(1,v-1) for v in f);M=maximal(s,4)
        cores.append({'core':list(s),'tau':tau(s),'maximal':list(M),'capacity':[capacity(M,f),capacity(M,slack)]})
    families=[family(n) for n in (2,3,4,5)]
    return {'schema':'capacity-gap-v1','cores':cores,'family':families,'upper_control':upper(),'counts':{'core_sources':len(cores),'floor_instances':2*len(cores),'family_sources':len(families),'protected_completions':sum(len(r['protected_masks']) for r in families),'rejecting_first_toggles':sum(len(r['first_toggles']) for r in families),'upper_controls':1}}
if __name__=='__main__':
    r=build();pathlib.Path(sys.argv[1]).write_text(json.dumps(r,sort_keys=True,separators=(',',':'))+'\n');print(json.dumps(r['counts'],sort_keys=True))
