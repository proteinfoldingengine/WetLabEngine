"""Enumerate labeled states, source charts and cut pairs without symmetry weights."""
from collections import Counter
from functools import lru_cache
from itertools import combinations,product
from pathlib import Path
import gzip
import json
import sys

demos=Path(sys.argv[1]).resolve()
sys.path.insert(0,str(demos/'v16.43-star-fiber-classification'))
from producer import normalize,DOMAIN

@lru_cache(None)
def min_covers(family,k):
    labels=range(k)
    for n in range(1,k+1):
        hits=[h for h in combinations(labels,n) if all(any(v>>a&1 for a in h) for v in family)]
        if hits: return tuple(hits)
    raise ValueError('uncovered leaf')

def direct():
    pooled=Counter()
    signals=Counter()
    for m,k in DOMAIN:
        for cols in product(range(1,1<<k),repeat=m):
            pooled['states']+=1
            h=min_covers(tuple(sorted(set(cols))),k)[0]
            q=len(h)
            if m>q:
                state=tuple(1+sum(1<<(i+1) for i,s in enumerate(cols) if s>>a&1) for a in range(k))
                trace=normalize(state,m,k,q)
                signals['states']+=1
                for a in range(k):
                    found=False
                    for old,new in zip(trace,trace[1:]):
                        if new[a]&~old[a]:
                            assert ((new[a].bit_count()-1)>=2)==(a in h)
                            signals['selected_gain' if a in h else 'unselected_gain']+=1
                            found=True;break
                    if not found: signals['silent']+=1
            for a in range(k):
                cuts=[]
                for i,s in enumerate(cols):
                    if (s & (1<<a)) and s!=(1<<a):
                        reduced=s & ~(1<<a)
                        family=set(cols[:i]+cols[i+1:]+(reduced,))
                        hs=min_covers(tuple(sorted(family)),k)
                        any_held=set.union(*(set(hh) for hh in hs))
                        all_held=set.intersection(*(set(hh) for hh in hs))
                        cuts.append((s,len(hs[0]),any_held,all_held,min(x.bit_count() for x in family)))
                for x,y in combinations(cuts,2):
                    if x[0]==y[0] or x[1]!=y[1]:continue
                    pooled['eligible_source_pairs']+=1
                    receivers=(x[3]-y[2] | y[3]-x[2])-{a}
                    if receivers:
                        pooled['positive_source_pairs']+=1
                        pooled['positive_receiver_witnesses']+=len(receivers)
                        if len(receivers)==1: pooled['one_remote']+=1
                        if min(x[4],y[4])>=2: pooled['at_least_two']+=len(receivers)
    return dict(pooled=pooled,gain_theorem=signals)

def audit_archive(demos,probe):
    doc=json.loads(gzip.decompress((demos/'v16.43-star-fiber-classification/evidence/science/scientific/CERTIFICATE.json.gz').read_bytes()))
    entry=next(e for e in doc['entries'] if (e['m'],e['k'])==(3,4))
    states=entry['graph']['states']
    for row in probe['archived']:
        normalized=entry['normalizations'][row['state']]
        assert normalized=={key:row[key] for key in ('q','state','path')}
        assert [states[i] for i in normalized['path']]==row['rows']
    return [r['state'] for r in probe['archived']]

if __name__=='__main__':
    here=Path(__file__).resolve().parent
    if len(sys.argv)==3 and sys.argv[2]=='archive':
        print(json.dumps(dict(archived_states=audit_archive(demos,json.loads((here/'trace.json').read_bytes()))),sort_keys=True))
    else:
        out=direct();expected=json.loads((here/'census.json').read_bytes())['pooled']
        for k in ('states','eligible_source_pairs','positive_source_pairs','positive_receiver_witnesses','one_remote','at_least_two'):
            assert out['pooled'].get(k,0)==expected.get(k,0)
        print(json.dumps(out,sort_keys=True))
