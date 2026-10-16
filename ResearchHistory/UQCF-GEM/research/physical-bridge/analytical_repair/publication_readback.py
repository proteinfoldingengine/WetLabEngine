"""Independent GitHub API byte readback and exact publication boundary audit."""
import base64
import hashlib
import json
import os
from pathlib import Path
import subprocess
import urllib.request
import urllib.parse

ROOT=Path(__file__).resolve().parents[5]
HERE=Path(__file__).resolve().parent
BASE='ResearchHistory/UQCF-GEM/research/physical-bridge/'
PARENT='cbefdb85f21cd9606d1a9260d38176c2dc068b91'
ORIGINAL='1ef7d25cedd5af6be6e72fea4e5963414a92cc0a'
OUT=Path('repair_remote_publication')
def sha(data):return hashlib.sha256(data).hexdigest()
def put(name,obj):
    (OUT/name).write_text(json.dumps(obj,sort_keys=True,indent=2)+'\n')
def get(path):
    request=urllib.request.Request('https://api.github.com/repos/proteinfoldingengine/WetLabEngine/'+path,headers={'Authorization':'Bearer '+os.environ['GH_READ_TOKEN'],'Accept':'application/vnd.github+json','X-GitHub-Api-Version':'2022-11-28'})
    with urllib.request.urlopen(request,timeout=60) as response:return json.load(response)
def contents(path,ref):
    obj=get('contents/'+urllib.parse.quote(path,safe='/')+'?ref='+ref)
    if obj.get('encoding')!='base64':raise ValueError('unsupported content representation')
    data=base64.b64decode(obj['content'])
    blob=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
    if blob!=obj['sha']:raise ValueError('Git blob identity mismatch')
    return data,obj['sha']
def main():
    OUT.mkdir(exist_ok=True)
    try:
        head=subprocess.check_output(['git','-C',str(ROOT),'rev-parse','HEAD'],text=True).strip()
        if head!=os.environ['GITHUB_SHA'] or head!=os.environ['UQCF_WORKFLOW_SHA']:raise ValueError('source/workflow identity mismatch')
        expected=json.loads((HERE/'publication_manifest.json').read_text())
        if expected['parent']!=PARENT or expected.get('contract_commit')!=PARENT or expected.get('source_parent')!=ORIGINAL:raise ValueError('manifest provenance mismatch')
        prior=expected.get('prior_repair_commits',[])
        if not isinstance(prior,list) or any(not isinstance(s,str) or len(s)!=40 or any(c not in '0123456789abcdef' for c in s) for s in prior) or len(prior)!=len(set(prior)) or head in prior or PARENT in prior:raise ValueError('invalid prior repair commits')
        expected_commits=prior+[head]
        immediate_parent=prior[-1] if prior else PARENT
        put('provenance.json',{'source_parent':ORIGINAL,'contract_commit':PARENT,'contract_sha256':'77017270c4dbb26935940a4542982b5b0e528f5aebcc64771361df2be11a08aa','scientific_sha':head,'workflow_sha':os.environ['UQCF_WORKFLOW_SHA'],'run_id':os.environ['GITHUB_RUN_ID'],'run_attempt':os.environ['GITHUB_RUN_ATTEMPT']})
        commit=get('git/commits/'+head);put('commit.json',commit)
        if commit.get('sha')!=head:raise ValueError('remote commit identity mismatch')
        if [p['sha'] for p in commit['parents']]!=[immediate_parent]:raise ValueError('unexpected parent')
        compare=get('compare/'+PARENT+'...'+head);put('compare.json',compare)
        if (compare.get('status')!='ahead' or compare.get('total_commits')!=len(expected_commits)
            or compare.get('base_commit',{}).get('sha')!=PARENT
            or compare.get('merge_base_commit',{}).get('sha')!=PARENT
            or [c.get('sha') for c in compare.get('commits',[])]!=expected_commits):
            raise ValueError('comparison ancestry mismatch')
        for entry,parent in zip(compare['commits'],[PARENT]+prior):
            if [p.get('sha') for p in entry.get('parents',[])]!=[parent]:raise ValueError('repair ancestry is not the declared linear chain')
        if expected['changed_paths']!=sorted(set(expected['changed_paths'])):raise ValueError('manifest paths not canonical')
        files=compare.get('files',[])
        if len(files)>=300 or sorted(f['filename'] for f in files)!=expected['changed_paths']:raise ValueError('publication changed-path mismatch')
        if any(f['status'] not in ('added','modified') for f in files):raise ValueError('unexpected change type')
        bound=json.loads((HERE/'input_manifest.json').read_text())
        index=BASE+'COUPLED_C3_NATIVE_RECORD_ORIGIN_CONTINUATION.md'
        paths=sorted(set(expected['changed_paths'])|set(bound['files'])|{index})
        evidence={}
        for path in paths:
            data,blob=contents(path,head)
            if data!=(ROOT/path).read_bytes():raise ValueError('remote byte mismatch: '+path)
            if path in bound['files'] and bound['files'][path]!={'bytes':len(data),'sha256':sha(data)}:raise ValueError('frozen input mismatch')
            evidence[path]={'bytes':len(data),'sha256':sha(data),'git_blob':blob,'ref':head}
        prior,blob=contents(index,ORIGINAL)
        appendix=(HERE/'INDEX_APPEND.md').read_bytes()
        current=(ROOT/index).read_bytes()
        if current!=prior+appendix:raise ValueError('continuation is not exact prior plus appendix')
        put('remote_readback.json',{'verified':True,'scientific_sha':head,'parent':PARENT,'immediate_parent':immediate_parent,'prior_repair_commits':expected_commits[:-1],'files':evidence,'continuation_parent':ORIGINAL,'continuation_parent_blob':blob,'continuation_appendix_sha256':sha(appendix),'scope':'exact cumulative scientific publication bytes and path boundary; final receipt readback remains separate'})
    except Exception as exc:
        put('failure.json',{'verified':False,'error_type':type(exc).__name__})
        raise SystemExit('Remote readback failed; sanitized evidence retained.')
    finally:
        put('file_manifest.json',{p.name:{'bytes':p.stat().st_size,'sha256':sha(p.read_bytes())} for p in sorted(OUT.iterdir()) if p.is_file() and p.name!='file_manifest.json'})
if __name__=='__main__':main()
