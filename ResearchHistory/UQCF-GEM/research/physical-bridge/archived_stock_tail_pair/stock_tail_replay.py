"""Two untouched original M5 executions with a common generated withdrawal."""
import gzip,hashlib,json,runpy,sys
from pathlib import Path
archive,parent,child=map(lambda x:Path(x).resolve(),sys.argv[1:])
sys.argv=[str(archive/'inherited_nested_balance.py'),str(parent),str(child)]
d=runpy.run_path(sys.argv[0]); here=Path(__file__).resolve().parent
def get(name,sha):
    b=gzip.decompress((here/name).read_bytes())
    assert hashlib.sha256(b).hexdigest()==sha
    return json.loads(b)
pins=[
('7cce932e8feb77130acf92b987bc997df2624bea2e262a49ae72f90485f8eb3a','4604a94751aaa7d6b4720e9cc9c6c92400444b317688e95dca1d6e16038050c2'),
('6e496aaa9bc5fb878a605b262f870825fed4010b4a4da4ae19970fa680daeff2','d72949a5542029956dace399f7b11c688349365204d6c4242a9459d46cf28469')]
root=[]; res=[]
for a,(c,h) in enumerate(pins):
    case=get(f'stock-tail-cases{a}.json.gz',c)
    rec=get(f'stock-tail-records{a}.json.gz',h)
    assert d['produce'](case)==rec and not d['verify_record'](case,rec)
    p=rec['identity'][1]; path=rec['path']; root.append(path)
    z,n,t,clear,bounds=d['lift'](path,p['k'],p['q'],3)
    i=rec['facts']['balancing'][0]['end']; parent=n[0][56]; leaves=n[parent]
    local=[parent,*leaves]; assert local==[225,226,227,228]
    local_state=lambda f:[f[v] for v in local]
    assert all(local_state(f)==[list(range(9)),[0],[1],[2]] for f in z[:bounds[i]+1])
    a0,a1=bounds[-2:]; old=local_state(z[a0]); new=local_state(z[a1])
    [leaf]=[v for v in leaves if z[a0][v]!=z[a1][v]]
    [c]=[r for r in clear if r['child']==parent and r['start']==a0 and r['end']==a1-1]
    assert c['x']==5
    assert [z[m][leaf] for m in range(a0,a1+1)]==[[5],sorted([5,c['y']]),[c['y']],[c['y']]]
    res.append(dict(path_sizes=[len(path),len(z)],first=rec['facts']['balancing'][0]['label'],first_end=i,prewrite=old,postwrite=new,recipient=leaf,replacement=c['y'],nested_last=[a0,a1]))
assert root[0][-2:]==root[1][-2:]
a,b=root[0][-2:]
assert [(i,x,y) for i,(x,y) in enumerate(zip(a,b)) if x!=y]==[(56,[5,6,7,8],[6,7,8])]
assert [u['first'] for u in res]==[2,1] and [u['recipient'] for u in res]==[226,227]
print(json.dumps(dict(starting_parent_rows_that_differ=sum(x!=y for x,y in zip(root[0][0],root[1][0])),common_generated_request=[56,'delete',5],arms=res),sort_keys=True))
