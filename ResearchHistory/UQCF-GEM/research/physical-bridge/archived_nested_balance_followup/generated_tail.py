"""Verify the common generated last withdrawal, without consuming the supplied probe."""
import gzip,hashlib,json,runpy,sys
from pathlib import Path
archive,parent_src,child_src,raw=map(lambda x:Path(x).resolve(),sys.argv[1:])
sys.argv=[str(archive/'inherited_nested_balance.py'),str(parent_src),str(child_src)]
d=runpy.run_path(sys.argv[0])
assert hashlib.sha256(raw.read_bytes()).hexdigest()=='01fa5e1522bf6b393fe08c6c2726cb8b5cb8c3e3cec54b34d955f5eadc48f16e'
arms=json.loads(gzip.decompress(raw.read_bytes()))
I=[a['original_parent_or_diagnostic_record'] for a in arms]
assert I[0]==d['new'] and I[0]['identity']==I[1]['identity']
assert I[0]['path'][-2:]==I[1]['path'][-2:]
A,B=I[0]['path'][-2:]
assert [(i,a,b) for i,(a,b) in enumerate(zip(A,B)) if a!=b]==[(25,[4,5,6,7],[5,6,7])]
assert I[0]['path'][-3]!=I[1]['path'][-3]
result=[]
for stored,rec in zip(arms,I):
    raw_path=rec['path']; p=rec['identity'][1]
    frames,nodes,targets,clearances,bounds=d['lift'](raw_path,p['k'],p['q'],3)
    assert (frames,nodes,targets,clearances,bounds)==tuple(stored[x] for x in ('verified_nested_path','nested_child_nodes','targets','clearances','boundaries'))
    v=nodes[0][25]; leaves=nodes[v]; assert [v,*leaves]==[101,102,103,104]
    assert [frames[0][u] for u in [v,*leaves]]==[[5,6,7],[5],[6],[7]]
    i0,i1=bounds[-2:]
    [clear]=[c for c in clearances if c['start']==i0 and c['end']==i1-1]
    x=clear['x']; y=clear['y']
    [owner]=[u for u in leaves if x in frames[i0][u]]
    [spare]=set(A[25]).difference(*[frames[i0][u] for u in leaves])
    assert x==4 and y==spare and clear['child']==v
    assert [frames[i][owner] for i in range(i0,i1+1)]==[[x],sorted([x,y]),[y],[y]]
    cover=[d['covering_number']([f[u] for u in nodes[0]]) for f in frames[i0:i1+1]]
    assert all(abs(c-p['q'])<=1 for c in cover) and cover[-1]==p['q']
    result.append(dict(parent_index=len(raw_path)-2,nested_indices=[i0,i1],prior=[frames[i0][u] for u in leaves],after=[frames[i1][u] for u in leaves],receiving_leaf=owner,replacement=y,cover=cover))
assert [(x['receiving_leaf'],x['replacement']) for x in result]==[(102,7),(103,6)]
print(json.dumps(dict(identical_complete_parent_suffix_frames=2,parent_request=[25,'delete',4],arms=result),sort_keys=True))
