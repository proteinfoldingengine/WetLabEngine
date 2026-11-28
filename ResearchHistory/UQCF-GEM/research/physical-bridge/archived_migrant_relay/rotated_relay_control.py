"""Cross-check two original unmodified M5 executions, rather than alter a selector."""
import hashlib,json,runpy,sys
from pathlib import Path
archive,parent,child=map(lambda x:Path(x).resolve(),sys.argv[1:])
sys.argv=[str(archive/'inherited_nested_balance.py'),str(parent),str(child)]
d=runpy.run_path(sys.argv[0])
here=Path(__file__).resolve().parent
def item(name,sha):
    b=(here/name).read_bytes()
    assert hashlib.sha256(b).hexdigest()==sha
    return json.loads(b)
C=item('migrant-rotated-case.json','40715004b16443cd6d7b62477032643dbc574b74ca36f4109f4700bf71fb6d22')
R=item('migrant-rotated-record.json','44e0ec9ffe053ee5722ecf2b811710e4e7a6224a74b977ed9c6093229aa47ab7')
A=item('migrant-original-records.json','7e6bab30dd992d5f9825c3c35d934431b8da1fb2f2da9cc3b5d945ac52969ada')
assert d['produce'](C)==R and not d['verify_record'](C,R)
assert d['produce']({'identity':A['identity']})==A and not d['verify_record']({'identity':A['identity']},A)
m=A['facts']['balancing'];n=R['facts']['balancing']
sigma=[3,4,5,6,0,1,2]
transport=lambda rows: sorted(sorted(sigma[x] for x in r) for r in rows)
assert transport(A['path'][0])==sorted(R['path'][0])
assert transport(A['path'][m[0]['end']])==sorted(R['path'][n[0]['end']])
assert transport(A['path'][m[1]['end']])!=sorted(R['path'][n[1]['end']])
assert n[0]['label']==sigma[m[0]['label']]==3
assert [x['label'] for x in m]==[0,0] and [x['label'] for x in n]==[3,0]
assert [(x['source'],x['destination']) for x in m]==[(0,1),(1,2)]
assert [(x['source'],x['destination']) for x in n]==[(2,0),(0,1)]
assert [x['after'] for x in m]==[x['after'] for x in n]==[[19,14],[17,12]]
print(json.dumps(dict(palette_transport=sigma,positive=[x['label'] for x in m],rotated=[x['label'] for x in n],expected_rotated_history_selected=sigma[m[1]['label']],before_second_paths_iso=True,after_second_paths_iso_under_same_map=False),sort_keys=True))
