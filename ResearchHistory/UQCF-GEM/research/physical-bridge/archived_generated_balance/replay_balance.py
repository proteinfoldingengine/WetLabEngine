"""Find original forward initiation and check its scope; not a new campaign."""
from hashlib import sha1,sha256
from pathlib import Path
from itertools import combinations,product,groupby
import copy,json,sys
root=Path(sys.argv[1]).resolve()
pins={'model.py':'a4a6407990c36084ab3b6e8e7da9022a4f9d63a8','mechanisms.py':'ab3541cba29d5e1ebd4fe6c56128daf020c1a81f','verifier.py':'e19999dfd46cd134d8191a59da7b8bf2cdb74b43'}
for f,pin in pins.items():
    b=(root/f).read_bytes()
    assert sha1(f'blob {len(b)}\0'.encode()+b).hexdigest()==pin
sys.path.insert(0,str(root))
from mechanisms import produce,relocate,group_parts
from model import Path as StockPath
from verifier import verify_record,covering_number
raw=(Path(__file__).parent/'original-143.json').read_bytes()
assert sha256(raw).hexdigest()=='13a954e573fbd21fac158163827069d766cf3a014a78a2b20c99debb324587fd'
record=json.loads(raw);case={'identity':record['identity']};p=case['identity'][1]
assert produce(case)==record and not verify_record(case,record)
path=record['path'];A,B=record['facts']['balancing']
assert [(u['source'],u['destination'],u['label'],u['start'],u['end']) for u in (A,B)]==[(2,0,5,0,36),(1,2,1,36,70)]
def eligible(widths):
    return [i for i,w in enumerate(widths) if w>=widths[(i+1)%3]+2]
ws=[[1,4,3],[2,4,2],[2,3,3]]
assert [eligible(w) for w in ws]==[[2],[1],[]]
assert [covering_number(path[i]) for i in (0,36,70)]==[5,5,5]
assert set(map(covering_number,path[:71]))=={4,5}
def word(v,i):
    return [x for x,_ in groupby(f[i] for f in v)]
def remote_6(cores,x,y):
    _,b,c=cores
    return sorted(sorted((y,z,t)) for z in b if z!=y for t in c if t!=x)
groups=[[(0,),(1,2,3,4),(5,6,7)],[(0,5),(1,2,3,4),(6,7)],[(0,5),(2,3,4),(1,6,7)]]
six=remote_6(groups[0],5,1)
data=[]
for r in six:
    i=path[0].index(r);assert word(path[:37],i)==[r]
    assert r!=path[70][i]
    data.append([i,r,path[70][i]])
assert word(path[:71],11)==[[1,3,7],[1,3,6,7],[1,6,7]]
assert path[-1][11]==[0,6,7]
# independent unordered core reconstruction, quotient by rotations fixing color(0)=0
by_core={}
for tail in product(range(3),repeat=7):
    c=(0,*tail)
    if len(set(c))!=3:continue
    def is_edge(edge):
        s=[c[i] for i in edge]
        return len(set(s))==1 or any(s.count(i)==2 and s.count((i+1)%3)==1 for i in range(3))
    key=frozenset(t for t in combinations(range(8),3) if is_edge(t))
    by_core.setdefault(key,[]).append(tuple(tuple(i for i,a in enumerate(c) if a==j) for j in range(3)))
assert sum(map(len,by_core.values()))==1932
for i,gv in zip((0,36,70),groups):
    key=frozenset(tuple(e) for e in path[i] if len(e)==3)
    assert by_core[key]==[tuple(gv)]
# Bypass only the scheduler, not the actual relocation code.
forced=StockPath(path[0]);g=group_parts(p['sizes'])
relocate(forced,g,1,2,3,True,8)
assert list(map(len,g))==[1,3,4]
assert set(map(covering_number,forced.vertices))=={4,5}
assert covering_number(forced.last)==5
assert min(len(x) for f in forced.vertices for x in f)>=3
# Fresh stock call at the reached state, encoding its groups into contiguous labels.
# Undo this encoding for the semantic comparison during the relocation only.
to_old=(0,5,1,2,3,4,6,7); to_new={x:i for i,x in enumerate(to_old)}
cp=copy.deepcopy(p);cp['sizes']=[2,4,2]
fresh={'identity':['M5',cp,[sorted(to_new[x] for x in r) for r in path[36]],{}]}
z=produce(fresh);assert not verify_record(fresh,z)
one,=z['facts']['balancing']
assert one['source']==1 and one['destination']==2 and to_old[one['label']]==1
back=[[sorted(to_old[i] for i in r) for r in f] for f in z['path'][:one['end']+1]]
assert word(back,11)==word(path[:71],11)
assert z['path'][-1]==path[-1]
# Reject swapped actual order in the archive metadata.
bad=copy.deepcopy(record);bad['facts']['balancing'].reverse()
assert verify_record(case,bad)
print(json.dumps({'record_sha256':sha256(raw).hexdigest(),'eligible':list(map(eligible,ws)),
    'relocations':[A,B],'six_rows':data,'row11':word(path,11),'fresh_raw_row11':word(back,11),
    'forced_early_widths':[1,3,4],'record_has_frames':len(path),'same_fresh_final':True,
    'fresh_does_not_replay_same_complete_suffix':back!=path[36:71]},sort_keys=True,indent=2))
