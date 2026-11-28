"""Alternative legal nested transport under the archived initial carrier symmetry."""
import gzip,json,runpy,sys
from pathlib import Path
archive,parent_src,child_src,raw=map(lambda x:Path(x).resolve(),sys.argv[1:])
sys.argv=[str(archive/'inherited_nested_balance.py'),str(parent_src),str(child_src)]
d=runpy.run_path(sys.argv[0])
x,y=json.load(gzip.open(raw,'rt'))
a,b=(z["original_parent_or_diagnostic_record"] for z in (x,y))
assert a==d['new']
s=lambda p: {5:7,7:5}.get(p,p)
init=a['path'][0]
pi=[init.index(sorted(map(s,r))) for r in init]
assert all(pi[pi[i]]==i for i in range(len(pi)))
assert pi[6]==6
ns=x['nested_child_nodes']; rows=ns[0]; initial=x['verified_nested_path'][0]
np=[None]*len(ns); np[0]=0
for i,v in enumerate(rows):
    w=rows[pi[i]]
    np[v]=w
    for f in ns[v]:
        [p]=[z for z in ns[w] if initial[z]==sorted(map(s,initial[f]))]
        np[f]=p
assert sorted(np)==list(range(len(ns))) and all(np[np[i]]==i for i in range(len(ns)))
assert all(np[v]==v for v in [25,26,27,28])
assert all({np[j] for j in ns[i]}==set(ns[w]) for i,w in enumerate(np))
def transport(frame,perm):
    return [sorted(map(s,frame[perm[i]])) for i in range(len(frame))]
transported=[transport(f,np) for f in x['verified_nested_path']]
assert transported[0]==initial
p=a['identity'][1]
assert not d['verify_nested'](transported,ns,{int(i):q for i,q in x['targets'].items()},p['k'])
assert x['verified_nested_path'][0]==y['verified_nested_path'][0]
assert d['word'](transported,27)==[[2]]
assert d['word'](y['verified_nested_path'],27)==[[2],[2,3],[3],[0,3],[0]]
start=a['facts']['balancing'][0]['end']; assert start==36==b['facts']['balancing'][0]['end']
geo=transport(a['path'][start],pi)
assert [f for i,f in enumerate(b['path'][start]) if i==2]==[[0,2,7]]
assert geo[2]==[0,1,7] and sorted(geo)==sorted(b['path'][start])
assert all([frame[v] for v in [25,26,27,28]]==[[1,2,6],[1],[2],[6]] for frame in transported[:x['boundaries'][start]+1])
assert d['word'](transported,27)==d['word'](x['verified_nested_path'],27)
print(json.dumps(dict(fixed_receiver=[25,26,27,28],row_permutation=pi,legal_transported_nested_frames=len(transported),transported_word27=d['word'](transported,27),reordered_word27=d['word'](y['verified_nested_path'],27),row2_first_boundary_transported=geo[2],row2_first_boundary_reordered=b['path'][start][2]),sort_keys=True))
