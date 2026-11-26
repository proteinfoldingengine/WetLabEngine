"""Check all paired historical R withdrawals using stored paths and independent set covers."""
from collections import Counter
from functools import lru_cache
from itertools import combinations
from pathlib import Path
import gzip
import hashlib
import json
import sys

demo=Path(sys.argv[1]).resolve()/'v16.53-four-child-boundary'
raw=(demo/'evidence/science/scientific/CERTIFICATE.json.gz').read_bytes()
assert hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()=='9dd2e4445bca36dfe59f10fc7b7debd1ee2bc81e'
records=json.loads(gzip.decompress(raw))['records']
table={}
for rec in records:
    if rec['identity'][0]!='R':continue
    assert rec['status']=='ok'
    rows=tuple(x>>1 for x in rec['start'])
    assert rows not in table
    table[rows]=rec

def number(rows):
    for n in range(1,5):
        if any(set.union(*c)=={0,1,2,3} for c in combinations([set(i for i in range(4) if s>>i&1) for s in rows],n)):
            return n
    raise ValueError('uncovered leaf')

@lru_cache(None)
def words(rows):
    w=[[] for _ in rows]
    for row in table[rows]['path']:
        for i,x in enumerate(row):
            s=frozenset(v for v in range(4) if x>> (v+1)&1)
            if not w[i] or s!=w[i][-1]:w[i].append(s)
    return w

def change_order(rows,order,sites):
    return tuple(sum(1<<n for n,i in enumerate(sites) if rows[a]>>i&1) for a in order)

def equal_order(rows,a,q):
    k=len(rows);order=list(range(k));sites=list(range(4))
    if q==3:
        first=next(i for i in sites if not rows[a]>>i&1)
        sites.remove(first);sites.insert(0,first)
    if q==4:
        order.remove(a);order.append(a)
    return order,sites

pairs=Counter();local_checks=Counter()
for rows,rec in table.items():
    assert number(rows)==rec['q'][0]
    for a,r in enumerate(rows):
        legal=[v for v in range(4) if r>>v&1 and any(s>>v&1 for i,s in enumerate(rows) if i!=a)]
        for s,t in combinations(legal,2):
            arms=[tuple(v^(1<<j) if i==a else v for i,v in enumerate(rows)) for j in (s,t)]
            qs=[table[arm]['q'][0] for arm in arms]
            tag='-'.join(map(str,sorted(qs)));pairs[tag]+=1
            if qs[0]==qs[1]:
                order,sites=equal_order(rows,a,qs[0])
                wx,wy=[words(change_order(arm,order,sites)) for arm in arms]
                assert all(wx[i]==wy[i] for i,b in enumerate(order) if b!=a)
                local_checks['erasing_common_orders']+=1
                continue
            assert sorted(qs)==[2,3]
            for b in range(len(rows)):
                if b==a:continue
                for arm,q in zip(arms,qs):
                    w=words(arm)[b];h=4-len(w[0])
                    first=next((i,new) for i,(old,new) in enumerate(zip(w,w[1:]),1) if old-new)
                    assert len(w[h])==(4 if q==2 else 2)
                    assert first[0]==(h+1 if q==2 else h) and len(first[1])==(3 if q==2 else 2)
                local_checks['unequal_receiver_checks']+=1
                local_checks['equal_incident_work']+=int((rows[b]>>s&1)==(rows[b]>>t&1))

here=Path(__file__).resolve().parent
selected=json.loads((here/'replay.json').read_bytes())
for case in selected['historical_paths']:
    rec=table[tuple(x>>1 for x in case['start'])]
    assert all(rec[key]==case[key] for key in ('identity','start','end','q','path'))
assert pairs['2-3']==288 and local_checks['unequal_receiver_checks']==576 and local_checks['equal_incident_work']==144
# The archived k=4 singleton starts have no paired withdrawal. Replay the q=4
# equal-profile argument with a redundant source in a five-chart instance.
import replay
extra=(3,1,2,4,8);order=(1,2,3,4,0);leaves=tuple(range(4))
xx,yy=(replay.perform_cut(extra,0,j)[0] for j in (0,1))
qa,wa=replay.traces(xx,order,leaves);qb,wb=replay.traces(yy,order,leaves)
assert qa==qb==4 and all(wa[b]==wb[b] for b in range(1,5))
print(json.dumps(dict(archive_states=len(table),paired_q=pairs,local=local_checks,
                      historical_paths=len(selected['historical_paths']),q4_remote_words=[wa[b] for b in range(1,5)]),sort_keys=True))
