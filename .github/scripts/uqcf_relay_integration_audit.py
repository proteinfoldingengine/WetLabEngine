"""PR116 byte-preserving integration audit; no model or scientific execution."""
import ast
import base64
import hashlib
import io
import json
import os
from pathlib import Path
import subprocess
import zipfile

ROOT=Path(__file__).resolve().parents[2]
BASE=Path('ResearchHistory/UQCF-GEM/research/physical-bridge')
CONTRACT=json.loads((ROOT/BASE/'role_transfer_consumer/integration/CONTRACT.json').read_bytes())

def digest(raw):
    return hashlib.sha256(raw).hexdigest()

def git(*args):
    return subprocess.check_output(['git',*args],cwd=ROOT)

def require(ok,message):
    if not ok: raise ValueError(message)

def verify_files(root,rows):
    found=[]
    require(len({r['path'] for r in rows})==len(rows),'Duplicate expected file')
    for row in rows:
        path=root/row['path']
        require(path.is_file() and not path.is_symlink(),'Missing accepted file')
        raw=path.read_bytes()
        blob=hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()
        require(blob==row['git_blob'],'Changed accepted bytes')
        found.append({'path':row['path'],'git_blob':blob,'bytes':len(raw),'sha256':digest(raw)})
    return found

def verify_diff(actual,expected):
    require(actual==expected,'Unexpected integration path set or change status')

def verify_archive(raw,expected):
    require(digest(raw)==expected,'Original ZIP digest mismatch')
    with zipfile.ZipFile(io.BytesIO(raw)) as z:
        names=z.namelist()
        require(len(names)==len(set(names)),'Duplicate ZIP member')
        require(all(Path(n).name==n and n not in ('.','..') for n in names),'Invalid ZIP path')
        require(z.testzip() is None,'ZIP integrity error')
        require('artifact_manifest.json' in names,'Missing archive manifest')
        files={name:z.read(name) for name in names}
    manifest=json.loads(files['artifact_manifest.json'])
    require(set(files)==set(manifest)|{'artifact_manifest.json'},'Incomplete archive member set')
    for name,identity in manifest.items():
        require(len(files[name])==identity['bytes'] and digest(files[name])==identity['sha256'],
                'Changed manifest member')
    return files

def verify_checkpoint(root,checkpoint):
    CONTRACT=checkpoint
    folder=BASE/checkpoint['folder']
    archives=[]
    contents=[]
    for row in CONTRACT['archives']:
        raw=base64.b64decode((root/BASE/row['path']).read_bytes())
        require(len(raw)==row['bytes'],'Original ZIP length mismatch')
        files=verify_archive(raw,row['sha256'])
        require(len(files)==row['members'],'Wrong archive size')
        contents.append(files)
        archives.append(dict(row,bytes=len(raw)))
    review,pub=contents
    require(review['response.json']==(root/folder/checkpoint['raw_copy']).read_bytes(),'Raw response copy mismatch')
    require(pub['publication.json']==(root/folder/checkpoint['audit_copy']).read_bytes(),'Audit copy mismatch')
    identity=json.loads(review['review_identity.json'])
    integrity=json.loads(review['integrity.json'])
    publication=json.loads(pub['publication.json'])
    required={'scientific_sha':CONTRACT['science'],'checkout_sha':CONTRACT['review_checkout'],
              'workflow_sha':CONTRACT['review_checkout'],'run_id':CONTRACT['review_run'],'run_attempt':'1'}
    for item in (identity,integrity,publication):
        require(all(item.get(k)==v for k,v in required.items()),'Original review identity mismatch')
    require(integrity.get('status')=='PASS' and publication.get('status')=='PASS','Original integrity/audit failure')
    require(integrity.get('scientific_execution') is False and publication.get('scientific_execution') is False,
            'Original execution scope mismatch')
    docs={name:(root/folder/name).read_bytes() for name in ('RESULT.md','SOURCE_PACKET.json','FREEZE.json')}
    hashes={k:digest(v) for k,v in docs.items()}
    require(hashes==integrity['documents']==publication['documents'],'Original document hashes differ')
    freeze=json.loads(docs['FREEZE.json'])
    require(freeze['documents']=={k:v for k,v in hashes.items() if k!='FREEZE.json'},'Freeze mismatch')
    prompt=checkpoint['header'].encode()
    for name,raw in docs.items():
        prompt+=('\nEXACT DOCUMENT '+name+'\nUTF8-BYTES '+str(len(raw))+'\n').encode()+raw+b'\nEND EXACT DOCUMENT\n'
    require(prompt==review['prompt.txt'] and digest(prompt)==identity['prompt_sha256']==publication['prompt_sha256'],
            'Original prompt mismatch')
    request={'contents':[{'role':'user','parts':[{'text':prompt.decode()}]}],
             'generationConfig':{'temperature':0,'maxOutputTokens':32768,'responseMimeType':'application/json'}}
    require((json.dumps(request,ensure_ascii=False,sort_keys=True)+'\n').encode()==review['request.json'],
            'Original request mismatch')
    response=json.loads(review['response.json'])
    require(response.get('modelVersion')=='gemini-3.1-pro-preview','Unexpected model')
    require(digest(review['response.json'])==identity['response_sha256']==publication['response_sha256'],
            'Original response digest mismatch')
    candidates=response['candidates']
    require(len(candidates)==1 and candidates[0].get('finishReason')=='STOP','Incomplete model response')
    answer='\n'.join(p['text'] for p in candidates[0]['content']['parts']
                     if not p.get('thought',False) and isinstance(p.get('text'),str)).strip().encode()
    require(answer==review['review.txt'],'Decoded review mismatch')
    verdict=json.loads(answer)
    require(verdict==json.loads(review['verdict.json']),'Stored verdict mismatch')
    require(verdict.get('verdict')=='ACCEPTED' and all(verdict.get(k)==[] for k in
            ('findings','missing_assumptions','counterexamples')),'Unresolved review findings')
    require(verdict.get('native_bridge_status')==publication.get('native_bridge')=='NOT_DERIVED','Scope upgrade')
    if checkpoint['disposition']=='historical_inconsistent':
        require(any('External-source freezing is not removed' in x for x in verdict['limitations']),'Contradictory first limitation lost')
    return archives,publication

def main():
    out=ROOT/'relay_integration_audit'
    out.mkdir(exist_ok=True)
    try:
        rows=verify_files(ROOT,CONTRACT['accepted_files'])
        require(len(rows)==66,'Incomplete expected accepted set')
        for row in CONTRACT['accepted_files']:
            require(git('show',CONTRACT['accepted_head']+':'+row['path'])==(ROOT/row['path']).read_bytes(),
                    'Accepted commit differs')
        actual={}
        for line in git('diff','--name-status','--no-renames',CONTRACT['baseline'],'HEAD').decode().splitlines():
            status,path=line.split('\t')
            require(path not in actual,'Duplicate changed path')
            actual[path]=status
        expected={r['path']:r['status'] for r in CONTRACT['accepted_files']}
        expected.update({p:'A' for p in CONTRACT['support_files']})
        verify_diff(actual,expected)
        for path in expected:
            mode,kind,blob_and_path=git('ls-tree','HEAD','--',path).decode().split(' ',2)
            require(mode=='100644' and kind=='blob','Unexpected mode/type')
        archives=[];summaries=[];total_sources=0
        require(len(CONTRACT['checkpoints'])==6 and sum(c['disposition']=='accepted' for c in CONTRACT['checkpoints'])==5,'Checkpoint disposition coverage')
        for checkpoint in CONTRACT['checkpoints']:
            raw_script=git('show',checkpoint['header_commit']+':'+checkpoint['script']) if checkpoint['header_commit'] else (ROOT/checkpoint['script']).read_bytes()
            require(digest(raw_script)==checkpoint['header_script_sha256'],'Review script identity mismatch')
            headers=[ast.literal_eval(n.value) for n in ast.parse(raw_script).body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='HEADER' for t in n.targets)]
            require(headers==[checkpoint['header']],'Review header differs')
            pair,publication=verify_checkpoint(ROOT,checkpoint);archives.extend(pair)
            packet=json.loads((ROOT/BASE/checkpoint['folder']/'SOURCE_PACKET.json').read_bytes())
            require(len(packet['sources'])==publication['source_count']==checkpoint['source_count'],'Source coverage changed')
            for source,locked in zip(packet['sources'],publication['sources'],strict=True):
                full=git('show',source['commit']+':'+source['path'])
                require(len(full)==source['full_bytes'] and digest(full)==source['full_sha256'],'Full dependency changed')
                require(hashlib.sha1(b'blob '+str(len(full)).encode()+b'\0'+full).hexdigest()==source['git_blob'],'Dependency blob mismatch')
                start,end=source['byte_start'],source['byte_end']
                require(type(start) is int and type(end) is int and 0<=start<end<=len(full),'Invalid interval')
                require(full[start:end]==source['content'].encode(),'Source excerpt mismatch')
                require(all(source[k]==locked[k] for k in ('commit','path','git_blob','full_bytes','full_sha256','byte_start','byte_end')),'Original binding changed')
            total_sources+=len(packet['sources'])
            summaries.append({'folder':checkpoint['folder'],'run':checkpoint['review_run'],'science':checkpoint['science'],'disposition':checkpoint['disposition'],'source_count':len(packet['sources'])})
        require(total_sources==35 and len(archives)==12,'Incomplete package')
        receipt={'status':'PASS','baseline':CONTRACT['baseline'],'accepted_head':CONTRACT['accepted_head'],
                 'checkout_sha':git('rev-parse','HEAD').decode().strip(),
                 'tree_sha':git('rev-parse','HEAD^{tree}').decode().strip(),
                 'workflow_sha':os.environ.get('UQCF_WORKFLOW_SHA'),'run_id':os.environ.get('GITHUB_RUN_ID'),
                 'run_attempt':os.environ.get('GITHUB_RUN_ATTEMPT'),'accepted_files':rows,
                 'original_archives':archives,'changed_paths':actual,'source_count':total_sources,'checkpoints':summaries,
                 'scientific_execution':False,'model_called':False,'native_bridge':'NOT_DERIVED'}
        (out/'audit.json').write_text(json.dumps(receipt,indent=2,sort_keys=True)+'\n')
        print('PASS: 66 accepted files; 12 original archives; 5 accepted checkpoints plus historical inconsistent review; 35 source bindings; 71-path integration scope.')
    except Exception as exc:
        (out/'failure.json').write_text(json.dumps({'status':'FAIL','error':str(exc),'type':type(exc).__name__})+'\n')
        raise

if __name__=='__main__': main()
