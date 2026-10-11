"""Cross-check saved slices against the unchanged inherited v16.53 checker."""
import hashlib, importlib.util, json, pathlib, sys

def check(certificate, native_dir, bindings):
    expected=next(r for r in bindings if r['path'].endswith('/v16.53-four-child-boundary/verifier.py'))
    path=native_dir/'verifier.py'
    if hashlib.sha256(path.read_bytes()).hexdigest()!=expected['sha256']:raise ValueError('native source changed')
    sys.path.insert(0,str(native_dir))
    spec=importlib.util.spec_from_file_location('inherited_nested_checker',path);mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
    tree=(((),()),(),());count=0
    for row in certificate['rows']:
        k=row['id'][0]+5
        for i,(state,profile) in enumerate(zip(row['states'],row['profiles'])):
            raw=[sum(1<<v for v,s in enumerate(state) if s&(1<<x)) for x in range(k)]
            if mod.profile_check(tree,k,raw)!=profile:raise ValueError('native profile mismatch')
            if i:
                distance=sum((a^b).bit_count() for a,b in zip(state,row['states'][i-1]))
                if distance!=int(i in row['executed']):raise ValueError('native edge or skip mismatch')
            count+=1
    f=certificate['forgery']
    for i,(state,profile) in enumerate(zip(f['states'],f['profiles'])):
        raw=[sum(1<<v for v,s in enumerate(state) if s&(1<<x)) for x in range(5)]
        if mod.profile_check(tree,5,raw)!=profile:raise ValueError('forgery native profile')
        if i and sum((a^b).bit_count() for a,b in zip(state,f['states'][i-1]))!=1:raise ValueError('forgery primitive')
        count+=1
    return {'status':'VERIFIED','native_verifier_sha256':expected['sha256'],'native_slice_occurrences':count,'forgery_native_valid':True}

if __name__=='__main__':
    doc=json.loads(pathlib.Path(sys.argv[1]).read_text());bindings=json.loads((pathlib.Path(__file__).parent/'source_readbacks.json').read_text())
    result=check(doc,pathlib.Path(sys.argv[2]),bindings)
    pathlib.Path(sys.argv[3]).write_text(json.dumps(result,sort_keys=True,indent=2)+'\n');print(json.dumps(result,sort_keys=True))
