import itertools
import json
import sys
from functools import lru_cache
from pins import SCOPE

@lru_cache(None)
def hits(f):
    choices=[[i for i in range(max(f).bit_length()) if s&(2**i)] for s in f]
    return min(len(set(picks)) for picks in itertools.product(*choices))

@lru_cache(None)
def observe(f,k):
    w=[int(bool(s&(2**k))) for s in f];n=len(f)
    values=[n-sum(w)]
    for y in range(k):
        present=[int(bool(s&(2**y))) for s in f]
        values.append(n-sum(w)-sum(present)+sum(a*b for a,b in zip(w,present)))
    return tuple(values)

@lru_cache(None)
def inverse(delta,k):
    if not any(delta): return None
    candidates=[]
    for bits in itertools.product((0,1),repeat=k):
        s=sum(2**i for i,b in enumerate(bits) if b)
        if not s: continue
        for old,new in [(s,s+2**k),(s+2**k,s)]:
            change=tuple(b-a for a,b in zip(observe((old,),k),observe((new,),k)))
            if change==delta: candidates.append(s)
    if len(candidates)!=1: raise ValueError('nonunique/invalid probe response')
    return candidates[0]

def check(data):
    rows=[];families=0;contexts=0
    for n in range(1,4):
        for bits in itertools.product((0,1),repeat=3*n):
            f=[sum(bits[3*r+x]*2**x for x in range(3)) for r in range(n)]
            if 0 in f: continue
            families+=1;contexts+=n
            for r in range(n):
                for phase in (0,1):
                    before=f.copy();before[r]+=8*phase
                    for commit in (0,1):
                        after=before.copy();after[r]+=commit*(8 if phase==0 else -8)
                        a,b=observe(tuple(before),3),observe(tuple(after),3)
                        delta=tuple(v-u for u,v in zip(a,b))
                        floors=[sum((s>>i)&1 for i in range(3)) for s in f]
                        tt=[hits(tuple(before)),hits(tuple(after))]
                        assert tt[0]==tt[1]==hits(tuple(f))
                        assert all(s.bit_count()>=v for s,v in zip(after,floors))
                        reading=inverse(delta,3)
                        assert reading==(f[r] if commit else None)
                        rows.append({'family':f,'root':r,'phase':phase,'commit':commit,
                                     'floors':floors,'star_before':list(a),'star_after':list(b),
                                     'tau':tt,'readout':reading,'next_phase':phase+commit})
    rows.sort(key=lambda q:(len(q['family']),q['family'],q['root'],q['phase'],q['commit']))
    def enc(s): return sum(2**'abcdeuw'.index(x) for x in s)
    # The reuse example uses u as its fresh marker; the hidden-world example uses w.
    raw={'original':['ab','bc','ac','de'],'nonfresh':['abd','bc','ac','de'],
         'marked0':['abu','bc','ac','de'],'reused':['abu','bc','ac','deu'],
         'hidden_a':['ab','bc','ac','de'],'hidden_b':['ab','bc','ac','deu'],
         'hidden_a_marked':['ab','bc','ac','dew'],'hidden_b_marked':['ab','bc','ac','deuw']}
    native={name:[enc(s) for s in f] for name,f in raw.items()}
    native_tau=[hits(tuple(f)) for f in native.values()]
    assert native_tau==[3,2,3,2,3,3,3,3]
    assert all(s.bit_count()>=2 for f in native.values() for s in f)
    for name in ('hidden_a','hidden_b','hidden_a_marked','hidden_b_marked'):
        assert [s&31 for s in native[name]]==native['original']
    da=tuple(v-u for u,v in zip(observe(tuple(native['hidden_a']),6),observe(tuple(native['hidden_a_marked']),6)))
    db=tuple(v-u for u,v in zip(observe(tuple(native['hidden_b']),6),observe(tuple(native['hidden_b_marked']),6)))
    assert da!=db and inverse(da,6)==24 and inverse(db,6)==56
    f=native['original'].copy();readouts=[];history=[hits(tuple(f))]
    for r in range(4):
        before=observe(tuple(f),5);f[r]+=32;after=observe(tuple(f),5)
        readouts.append(inverse(tuple(b-a for a,b in zip(before,after)),5));history.append(hits(tuple(f)))
        f[r]-=32;history.append(hits(tuple(f)))
    assert f==native['original'] and readouts==f and history==[3]*9
    expected={'scope':SCOPE,'records':rows,'native':native,
              'scan':{'readouts':readouts,'final':f,'commits':8,'tau_history':history},
              'claims':{'guaranteed_completion':False,'count_access_derived':False,
                        'uniform_preissue_safety':True,'exact_restoration':True}}
    if data!=expected: raise ValueError('exact canonical identity/value/provenance/scope mismatch')
    return {'status':'PASS_BOUNDED_NOT_GENERAL_PROOF','families':families,'probe_contexts':contexts,
            'records':len(rows),'native_tau':native_tau,'scan_commits':8,
            'scan_exact_restoration':True,'count_channel_derived':False}

if __name__=='__main__': print(json.dumps(check(json.load(open(sys.argv[1]))),sort_keys=True,indent=2))
