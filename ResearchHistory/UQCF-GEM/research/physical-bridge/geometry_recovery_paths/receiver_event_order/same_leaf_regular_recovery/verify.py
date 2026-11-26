"""Independently derive all degree candidates by the defect-neighbor constraint."""
import json,os,sys
from pathlib import Path
from collections import Counter
from itertools import combinations
from importlib.util import spec_from_file_location,module_from_spec
from hashlib import sha1,sha256

raw=Path(sys.argv[2]).read_bytes()
os.chdir(sys.argv[1])
path=Path('ResearchHistory/UQCF-GEM/research/physical-bridge/forced_parent_deletion/check_geometry_repair.py')
data=path.read_bytes()
assert sha1(b"blob "+str(len(data)).encode()+b"\0"+data).hexdigest()=="3324c0b46e09120ae526338444a19070b692d049"
spec=spec_from_file_location('historical_input',path); hist=module_from_spec(spec); spec.loader.exec_module(hist)
F,init=hist.fixture(); L=set(hist.LABELS); A,B,T=0,12,1; Y0=hist.grid()
assert len(F)==1416 and F[1][2] == L-F[2][2]
low,high=Y0[A],Y0[B]; assert low.isdisjoint(high)
after=[(p,g,s-{A} if v==T else s) for v,(p,g,s) in enumerate(F)]
w=[g for _,g,_ in F]
for v in reversed(range(1,len(F))): w[F[v][0]]+=w[v]
assert {v for v,q in enumerate(w) if q==2}=={1,2,3}
def row(f,x):
    return {y: sum(w[v]**2 for v,(_,_,s) in enumerate(f) if (x in s)!=(y in s)) for y in L}
D={i:set(j for j,d in row(after,i).items() if d==1984) for i in L}
assert all(len(D[i])==(3 if i in low else 5 if i in high else 4) for i in L)
assert set.intersection(*(D[j] for j in high))=={A,B}
assert all(not (D[j]&high) for j in high)
candidates=set(); counts=Counter()
for v,(parent,g,s) in enumerate(after):
    if not v: continue
    adds=after[parent][2]-s
    drops=s-set().union(*(ss for pp,_,ss in after if pp==v)) if len(s)>1 else set()
    counts['1']+=len(adds);counts['-1']+=len(drops)
    if w[v]!=2: continue
    # After fixing the defects, the only possible edited chart is 0 or 12.
    # At either, it must raise work to all high and lower it to all low by 4.
    for sign,legal in ((1,adds),(-1,drops)):
        if sign==1 and not (low<=s and high.isdisjoint(s)): continue
        if sign==-1 and not (high<=s and low.isdisjoint(s)): continue
        for i in legal&{A,B}:
            candidates.add((i,v,sign))
assert candidates=={(0,1,1),(12,1,1),(12,2,-1)}
def audit(r):
    assert set(map(tuple,r['degree_candidates']))==candidates
    assert r['count']==dict(counts)=={'1':2777,'-1':32575}
    assert r['alt_vs_old']==[[0,12,1990,1998]] and r['same_baseline'] is True and r['gain_metric_is_exact_swap'] is True
    assert r['all_field_inputs_match']==['labels','neighbors','adjacency','cycles','directed_edges','direction_classes','tangent_rank','local_vectors','d4_actions']
    e=r['report']
    for scenario,pre,effect in [('prior',['242','absent','2'],'1/64'),('0,1,1',['242','absent','2'],'1/64'),
                                ('12,1,1',['240','2','2'],'0'),('12,2,-1',['244','absent','absent'],'0')]:
        assert set(map(tuple,e[scenario]['degree']))=={(i,4) for i in L}
        assert (e[scenario]['call'],e[scenario]['rec'],e[scenario]['effect'])==('ADMITTED',pre,effect)
    assert e['just-source']['call']==e['no-source-acquire']['call']=='degree_not_four'
    return True
x=json.loads(raw);audit(x)
for field,bad in (('alt_vs_old',[]),('degree_candidates',[[12,1,1]]),('same_baseline',False)):
    try: audit(dict(x,**{field:bad}))
    except AssertionError: pass
    else: raise AssertionError('rejecting control failed')
print(json.dumps({'degree_candidates':sorted(candidates),'count':counts,'rejecting_controls':3,'raw_sha256':sha256(raw).hexdigest()},sort_keys=True))
