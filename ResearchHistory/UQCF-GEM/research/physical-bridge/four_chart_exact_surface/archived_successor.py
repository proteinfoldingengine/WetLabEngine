"""Run with the pinned v16.51 demo directory. Check all 72 two-label q-root=2 paths."""
from collections import Counter
from pathlib import Path
import gzip
import hashlib
import json
import sys
sys.path.insert(0, str(Path(sys.argv[1]).resolve()))
import producer
import verifier
doc = producer.produce()
raw = (json.dumps(doc,sort_keys=True,separators=(',',':'))+'\n').encode()
packet = gzip.compress(raw,compresslevel=9,mtime=0)
# Normalize the gzip OS byte to the historical Unix header across Python versions.
packet = packet[:9] + bytes([3]) + packet[10:]
assert hashlib.sha1(f'blob {len(packet)}\0'.encode()+packet).hexdigest()=='571d38f08006b7023a65ec64cac77fe23e0db52a'

def exact_moves(s,tree,q):
    moves = {}
    for j in range(2):
        for site in range(1,len(producer.layout(tree))):
            nxt = s.copy()
            nxt[j] ^= 1<<site
            try:
                profile = verifier.profile_check(tree,2,nxt)
            except verifier.InterfaceNotPreserved:
                continue
            if profile == q:
                moves[(site,j, bool(nxt[j] & 1<<site))] = nxt
    return moves

def reachable_with_source_held(start,tree,q,source):
    pending=[start]; seen={tuple(start)}
    while pending:
        s=pending.pop()
        for (site,_,_),t in exact_moves(s,tree,q).items():
            if site!=source and tuple(t) not in seen:
                pending.append(t);seen.add(tuple(t))
    return seen

counts = Counter()
for case,row in enumerate(doc['cases']):
    spec = row['spec']; q = spec['q']
    if row['failure'] or spec['k']!=2 or q[0]!=2:continue
    counts['cases']+=1
    tree = producer.TREES[spec['tree']]
    roots=set(producer.layout(tree)[0]); path=row['path']
    for i,(before,mid,end) in enumerate(zip(path,path[1:],path[2:])):
        if any(verifier.profile_check(tree,2,s)!=q for s in (before,mid,end)):continue
        old=exact_moves(before,tree,q); new=exact_moves(mid,tree,q)
        release=next(k for k,v in old.items() if v==mid)
        gain=next(k for k,v in new.items() if v==end)
        a,x,add=release;b,y,take=gain
        if add or not take or a==b or x!=y or not {a,b}<=roots:continue
        premature=before.copy();premature[y]^=1<<b
        if verifier.profile_check(tree,2,premature)[0]!=1:continue
        assert [key for key in old if key[0] in roots]==[release]
        assert len(new)==2 and before in new.values()
        counts['adjacent exact enabling pairs']+=1
        if (case,i)==(14,5):
            print('case 14 frames 5/6/7:',before,mid,end)
            print('before exact moves:',sorted(old))
            print('after exact moves:',sorted(new))
            held=reachable_with_source_held(before,tree,q,a)
            assert all(all((z & (1<<b))==(base & (1<<b)) for z,base in zip(s,before)) for s in held)
            print('states reachable holding source at pre-release support:',len(held))
assert counts['adjacent exact enabling pairs']>0
print(dict(counts))
