"""Stock-Python recheck of a diagnostic first-source intervention on archived M5."""
import builtins
import copy
import gzip
import json
from pathlib import Path
import runpy
import sys

here=Path(__file__).resolve().parent
archive, parent_src, child_src, output = map(lambda x: Path(x).resolve(), sys.argv[1:])
sys.argv=[str(archive/'inherited_nested_balance.py'),str(parent_src),str(child_src)]
d=runpy.run_path(sys.argv[0])
raw_evidence=[]
import mechanisms
stock=d['new']
lift=d['lift']
verify_record=d['verify_record']
verify_nested=d['verify_nested']
cover=d['covering_number']
case={'identity':stock['identity']}
p=stock['identity'][1]
assert not verify_record(case,stock)
changed=[]
def intervene(*args,**kwargs):
    if (not changed and len(args)==1 and isinstance(args[0],set)
            and args[0]=={5,6,7} and not kwargs
            and sys._getframe(1).f_code is mechanisms.relocate.__code__):
        changed.append((5,7))
        return 7
    return builtins.min(*args,**kwargs)
assert 'min' not in mechanisms.__dict__
mechanisms.min=intervene
try:
    alt=mechanisms.produce(case)
finally:
    del mechanisms.min
assert changed==[(5,7)]
assert mechanisms.produce(case)==stock
errors=verify_record(case,alt)
assert 'nonprescribed balancing move' in errors
assert set(errors)=={'nonprescribed balancing move'}, errors
assert alt['path'][0]==stock['path'][0] and alt['path'][-1]==stock['path'][-1]
assert [tuple(m[k] for k in ('source','destination','label')) for m in stock['facts']['balancing']]==[(2,0,5),(1,2,1)]
assert [tuple(m[k] for k in ('source','destination','label')) for m in alt['facts']['balancing']]==[(2,0,7),(1,2,1)]
arms=[]
for rec in (stock,alt):
    raw=rec['path']
    balances=rec['facts']['balancing']
    frames,nodes,targets,clearances,boundaries=lift(raw,p['k'],p['q'],3)
    child=nodes[0][6]
    leaves=nodes[child]
    assert leaves==[26,27,28]
    target_lists={int(v):q for v,q in targets.items()}
    assert not verify_nested(frames,nodes,target_lists,p['k'])
    assert all([f[child],*[f[v] for v in leaves]]==[[1,2,6],[1],[2],[6]] for f in frames[:boundaries[balances[0]['end']]+1])
    word=d['word'](frames,27)
    end=raw[-1]
    a=copy.deepcopy(end);a[6]=[0,1,2,3]
    b=copy.deepcopy(a);b[6]=[0,1,3]
    tail=[end,a,b]
    assert all(cover(rows)==5 for rows in tail)
    continuation,nn,tt,tail_clear,bb=lift(tail,p['k'],p['q'],3,[[frames[-1][leaf] for leaf in nodes[v]] for v in nodes[0]])
    assert continuation[0]==frames[-1] and nn==nodes and tt==targets
    assert not verify_nested(frames+continuation[1:],nodes,target_lists,p['k'])
    affected=[v for v in leaves if continuation[0][v]!=continuation[-1][v]]
    assert len(tail_clear)==1 and tail_clear[0]['x']==2 and tail_clear[0]['y']==3
    raw_evidence.append({'original_parent_or_diagnostic_record':rec,'verified_nested_path':frames,'nested_child_nodes':nodes,'targets':targets,'boundaries':boundaries,'clearances':clearances,'probe':continuation,'probe_clearances':tail_clear})
    arms.append({'root_frames':len(raw),'nested_frames':len(frames),'clearances':len(clearances),'word27':word,'while_second':[raw[balances[1]['start']][6],raw[balances[1]['end']][6]],'changed_probe_leaf':affected,'final_leaves':[frames[-1][v] for v in leaves]})
assert arms[0]['word27']==[[2]] and arms[1]['word27']==[[2],[2,3],[3],[0,3],[0]]
assert arms[0]['changed_probe_leaf']==[27] and arms[1]['changed_probe_leaf']==[26]
assert [u['nested_frames'] for u in arms]==[425,557]
assert [u['root_frames'] for u in arms]==[229,295]
assert [u['final_leaves'] for u in arms]==[[[1],[2],[0]],[[2],[0],[1]]]
output.write_bytes(gzip.compress((json.dumps(raw_evidence,sort_keys=True,separators=(',',':'))+'\n').encode(),mtime=0))
print(json.dumps({'arms':arms,'altered_stock_admission_errors':errors},sort_keys=True))
