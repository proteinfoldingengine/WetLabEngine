"""New cross-family composition, with a blind original M9 replay control."""
from pathlib import Path
from hashlib import sha1,sha256
from itertools import groupby
import json,sys
here=Path(__file__).resolve().parent
root=Path(sys.argv[1]).resolve(); dep=Path(sys.argv[2]).resolve()
def pin(path, sha):
    b=path.read_bytes();assert sha1(f'blob {len(b)}\0'.encode()+b).hexdigest()==sha
for name,sha in [('mechanisms.py','ab3541cba29d5e1ebd4fe6c56128daf020c1a81f'),('model.py','a4a6407990c36084ab3b6e8e7da9022a4f9d63a8'),('verifier.py','e19999dfd46cd134d8191a59da7b8bf2cdb74b43')]:
    pin(root/name,sha)
for name,sha in [('producer.py','0501a1b32c0a660646ff95ecbb8a37a8f2e04b80'),('feasibility.py','9e995e21c9a477034a2fd4be615e28a2551b0bf9')]:
    pin(dep/name,sha)
sys.path[:0]=[str(root),str(dep)]
from mechanisms import produce
from model import state
from verifier import verify_record,verify_nested,covering_number
from producer import clear_role
def get(name,sha):
    b=(here/name).read_bytes();assert sha256(b).hexdigest()==sha;return json.loads(b)
old=get('m9-original-small.json','faf1ae83095b9f38b4ef8a7f9828a823ccc2b49996163b337e5a36e63202bb09')
new=get('original-143.json','13a954e573fbd21fac158163827069d766cf3a014a78a2b20c99debb324587fd')
assert produce({'identity':new['identity']})==new and not verify_record({'identity':new['identity']},new)
# Factor out the literal three-leaf-star construction and loop of M9 native(c).
# Only substitute the source of the root path; do not invoke original M9 with a forged family case.
def lift(raw,k,q,h,all_interiors=None):
    rootpath=[state(v) for v in raw]
    nodes=[[]];targets={0:q};supports=[frozenset(range(k))]
    for row in rootpath[0]:
        child=len(nodes);nodes[0].append(child);nodes.append([]);supports.append(row);targets[child]=h
        for x in sorted(row)[:h]:
            nodes[child].append(len(nodes));nodes.append([]);supports.append(frozenset([x]))
    if all_interiors is not None:
        for p,c in enumerate(nodes[0]):
            for j,leaf in enumerate(nodes[c]):supports[leaf]=frozenset(all_interiors[p][j])
    current=[sum(1<<v for v,row in enumerate(supports) if x in row) for x in range(k)]
    masks=[current[:]];trace=[];parent_boundaries=[0]
    for before,after in zip(rootpath,rootpath[1:]):
        flips=[(i,x) for i,(a,b) in enumerate(zip(before,after)) for x in sorted(a^b)]
        (i,x),=flips
        child=nodes[0][i];add=x in after[i]
        if not add:
            active={z for z in range(k) if any(current[z]&(1<<v) for v in nodes[child])}
            if x in active:
                y=min(before[i]-active);start=len(masks)-1
                clear_role(current,nodes,child,x,y,masks)
                trace.append({'child':child,'x':x,'y':y,'start':start,'end':len(masks)-1})
        if add:current[x]|=1<<child
        else:current[x]&=~(1<<child)
        masks.append(current[:]);parent_boundaries.append(len(masks)-1)
    nested=[[[x for x in range(k) if masks_at[x]&(1<<v)] for v in range(len(nodes))] for masks_at in masks]
    assert not verify_nested(nested,nodes,targets,k)
    assert all(covering_number([f[w] for w in nodes[v]])==t for f in nested for v,t in targets.items() if v)
    assert all([nested[b][v] for v in nodes[0]]==f for f,b in zip(raw,parent_boundaries))
    return nested,nodes,{str(v):t for v,t in targets.items()},trace,parent_boundaries
z,n,t,tr,bs=lift(old['path'],old['identity'][1]['k'],3,3)
assert z==old['nested_path'] and n==old['nodes'] and t==old['targets'] and tr==old['facts']['clearance'] and bs==old['facts']['parent_boundaries']
p=new['identity'][1]
z,n,t,tr,bs=lift(new['path'],p['k'],5,3)
v=n[0][11];leaf=n[v][1]
def word(z,v,until=None):
    return [x for x,_ in groupby(f[v] for f in z[:until])]
assert word(z,leaf,bs[36]+1)==[[3]]
assert word(z,leaf,bs[70]+1)==[[3],[3,6],[6]]
cut=next(a for a in tr if a['child']==v)
assert (cut['x'],cut['y'])==(3,6) and bs[36]<cut['start']<cut['end']<bs[70]
assert z[cut['start']][v]==[1,3,6,7] and z[cut['end']][v]==[1,3,6,7] and z[cut['end']+1][v]==[1,6,7]
# Wrong edit: skip both nested clearance frames but keep parent removal.
b0=z[cut['start']]; b1=b0[:]; b1[v]=z[cut['end']+1][v]
bad=[b0,b1]
assert 'native nesting' in verify_nested(bad,n,t,p['k'])
# Omit first move by restarting clearance from the exact reached nested state,
# with *the same* encoded parent suffix. This is not a fresh balancing call.
restart=z[bs[36]]
joined,nn,tt,_,_ = lift(new['path'][36:],p['k'],5,3,
    [[restart[leaf] for leaf in n[parent]] for parent in n[0]])
assert joined==z[bs[36]:] and nn==n and tt==t
print(json.dumps({'old_bound_frames':[len(old['path']),len(old['nested_path'])],
 'old_clearances':len(old['facts']['clearance']),'new_frames':[len(new['path']),len(z)], 'new_nodes':len(n),
 'new_clearances':len(tr),'phase_boundaries':[bs[i] for i in (0,36,70,228)],
 'row_11_child':v,'leaf':leaf,'cut_clearance':cut,'row_11_leaf_through_70':word(z,leaf,bs[70]+1),
 'row_11_leaf_through_return':word(z,leaf),'restart_matches_full_lifted_suffix':True},sort_keys=True,indent=2))
