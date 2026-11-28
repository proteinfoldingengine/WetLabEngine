"""Read back an original M5 run and test a two-boundary historical selector."""
import hashlib,itertools,json,runpy,sys
from pathlib import Path
archive,parents,children=map(lambda x:Path(x).resolve(),sys.argv[1:])
sys.argv=[str(archive/'inherited_nested_balance.py'),str(parents),str(children)]
d=runpy.run_path(sys.argv[0])
here=Path(__file__).resolve().parent
def load(name,sha):
    b=(here/name).read_bytes()
    assert hashlib.sha256(b).hexdigest()==sha
    return json.loads(b)
case=load('migrant-original-cases.json','f81ea8e677f111854716073999313ede0a2b80a0619143104c13de82571a30e7')
record=load('migrant-original-records.json','7e6bab30dd992d5f9825c3c35d934431b8da1fb2f2da9cc3b5d945ac52969ada')
p=record['identity'][1]
assert d['produce'](case)==record and not d['verify_record'](case,record)
path=record['path'];moves=record['facts']['balancing']
assert [(m['start'],m['end'],m['source'],m['destination'],m['label']) for m in moves]==[(0,26,0,1,0),(26,42,1,2,0)]
def candidate_partitions(rows,k):
    expected={tuple(row) for row in rows if len(row)!=k}
    result=[];count=0
    for tags in itertools.product(range(3),repeat=k):
        if tags[0]!=0 or len(set(tags))!=3:continue
        count+=1
        known=set()
        for tri in itertools.combinations(range(k),3):
            z=[sum(tags[j]==i for j in tri) for i in range(3)]
            if 3 in z or any(z[i]==2 and z[(i+1)%3]==1 for i in range(3)):
                known.add(tri)
        if known==expected:
            result.append([set(j for j in range(k) if tags[j]==i) for i in range(3)])
    [part]=result
    return part,count
def align(part,anchor,position):
    [j]=[i for i,g in enumerate(part) if g==anchor]
    pivot=(j-position)%3
    return part[pivot:]+part[:pivot]
parts=[];checks=[]
for frame in (0,26,42):
    groups,n=candidate_partitions(path[frame],7);checks.append(n)
    parts.append(groups)
[shared]=set(map(frozenset,parts[0]))&set(map(frozenset,parts[1]))
anchor=set(shared)
parts[0]=align(parts[0],anchor,2);parts[1]=align(parts[1],anchor,2)
[marker]=parts[1][1]-parts[0][1]
assert marker==0 and parts[0][1]<parts[1][1]
parts[2]=align(parts[2],parts[1][0],0)
assert parts==[[{0,1,2,3},{4,5},{6}],[{1,2,3},{0,4,5},{6}],[{1,2,3},{4,5},{0,6}]]
assert [i for i in range(3) if len(parts[0][i])-len(parts[0][(i+1)%3])>=2]==[0]
assert [i for i in range(3) if len(parts[1][i])-len(parts[1][(i+1)%3])>=2]==[1]
assert set(checks)=={602}
# The unchanged C is inferred among the matched endpoint cycle: exactly one common group.
assert list(set(map(frozenset,parts[0]))&set(map(frozenset,parts[1])))==[frozenset(anchor)]
# The previous archived witness is a negative control for this particular record.
controls=[candidate_partitions(d['new']['path'][f],8)[0] for f in (0,36)]
assert list(set(map(frozenset,controls[0]))&set(map(frozenset,controls[1])))==[frozenset({1,2,3,4})]
assert {1,2,3,4}==set(controls[1][1])==set(controls[0][1])
z,n,t,clear,bounds=d['lift'](path,p['k'],p['q'],3)
v=n[0][0];l=n[v][2]
assert len(path)==251 and len(z)==479
assert all(f[0]==[0,1,2] for f in path[:27])
assert path[42][0]==[0,1,6]
assert d['word'](z,l,bounds[26]+1)==[[2]]
assert d['word'](z,l,bounds[42]+1)==[[2],[2,6],[6]]
assert d['word'](z,l)==[[2],[2,6],[6],[3,6],[3],[0,3],[0]]
print(json.dumps(dict(reconstructed_partitions=[[sorted(g) for g in x] for x in parts],rank_check_counts=checks,marker=marker,negative_marker=[],path_counts=[len(path),len(z)],row0_leaf=l,nested_boundaries=[bounds[j] for j in [0,26,42,250]],row0_leaf_word=d['word'](z,l)),sort_keys=True))
