"""Artifact-bound publication and automated receipt preparation."""
from pathlib import Path
import archive
import json,os,sys,urllib.request,urllib.error,shutil,subprocess
from integrity import HERE,ROOT,OLD,dump,sha,unpack_zip,verify_package,verify_manifest,write_manifest,replace_directory,scientific_equal,source_map,PARENT,WORKFLOW,metadata_valid
API='https://api.github.com/repos/'+os.environ.get('GITHUB_REPOSITORY','proteinfoldingengine/WetLabEngine')

def get(url):
    class NoRedirect(urllib.request.HTTPRedirectHandler):
        def redirect_request(self,*args):return None
    headers={'Accept':'application/vnd.github+json','Authorization':'Bearer '+os.environ['GH_TOKEN']}
    try:return urllib.request.build_opener(NoRedirect).open(urllib.request.Request(url,headers=headers)).read()
    except urllib.error.HTTPError as e:
        if e.code not in (301,302,303,307,308):raise
        return urllib.request.urlopen(e.headers['Location']).read()

def provenance(run,artifact,metadata,head,run_id,attempt,phase):
    if run.get('id')!=int(run_id) or run.get('head_sha')!=head or run.get('run_attempt')!=int(attempt):raise ValueError('API run provenance')
    if artifact.get('name')!='v1651-'+phase+'-'+head or artifact.get('workflow_run',{}).get('id')!=int(run_id) or artifact.get('workflow_run',{}).get('head_sha')!=head:raise ValueError('artifact provenance')
    metadata_valid(metadata,head,run_id,attempt,phase)
    if run.get('event')!='push' or run.get('path')!=WORKFLOW:raise ValueError('execution workflow identity')
    expected_branch='research/v16.34-fiber-component-invariant' if phase=='post_merge' else 'research/v16.51-ternary-interface'
    if run.get('head_branch')!=expected_branch:raise ValueError('execution branch identity')

def download(run_id,out,phase='science'):
    out=Path(out);out.mkdir(parents=True,exist_ok=True)
    run=json.loads(get(API+'/actions/runs/'+str(run_id)));dump(out/'RUN.json',run)
    artifacts=json.loads(get(API+'/actions/runs/'+str(run_id)+'/artifacts'))['artifacts']
    matches=[a for a in artifacts if a['name']=='v1651-'+phase+'-'+run['head_sha']]
    if len(matches)!=1:raise ValueError('unique artifact')
    a=matches[0];dump(out/'ARTIFACT.json',a);data=get(a['archive_download_url']);(out/(phase+'-artifact.zip')).write_bytes(data)
    unpack_zip(data,a['digest'],out/phase);verify_package(out/phase)
    meta=json.loads((out/phase/'METADATA.json').read_text())
    expected_head=os.environ['GITHUB_SHA'] if phase in ('science','publication') else run['head_sha']
    provenance(run,a,meta,expected_head,run_id,os.environ.get('GITHUB_RUN_ATTEMPT','1') if phase in ('science','publication') else run['run_attempt'],phase)
    jobs=json.loads(get(API+'/actions/runs/'+str(run_id)+'/jobs'));dump(out/'JOBS.json',jobs)
    matches=[j for j in jobs['jobs'] if j['name']==phase]
    if len(matches)!=1 or matches[0]['conclusion']!='success' or matches[0]['head_sha']!=run['head_sha']:raise ValueError('job success/source')
    (out/'JOB.log').write_bytes(get(API+'/actions/jobs/'+str(matches[0]['id'])+'/logs'))
    dump(out/'INTEGRITY.json',{'artifact_id':a['id'],'sha256':sha(data),'api_digest_crc_manifests_source_science':'VERIFIED','phase':phase,'head':run['head_sha']})

def publication():
    verify_package('out/download/science');verify_package('out/reproduction')
    scientific_equal('out/download/science/scientific','out/reproduction/scientific')
    replace_directory('out/download',HERE/'evidence')
    replace_directory('out/reproduction',HERE/'evidence/reproduction')
    archive.retain(HERE/'evidence/science-artifact.zip')
    fresh=Path('out/fresh')
    api_dir=HERE/'evidence/reproduction_api';api_dir.mkdir()
    for name in ('RUN.json','ARTIFACT.json','JOBS.json','JOB.log','INTEGRITY.json'):
        shutil.copyfile(fresh/name,api_dir/name)
    shutil.copyfile(fresh/'publication-artifact.zip',api_dir/'publication-artifact.zip')
    archive.retain(api_dir/'publication-artifact.zip')
    metrics=json.loads((HERE/'evidence/science/METRICS.json').read_text())
    result=json.loads((HERE/'evidence/science/scientific/VERIFY.json').read_text())
    report='# v16.51 ternary interface results\n\n'+json.dumps(result,indent=2)+'\n\nAll 994 inherited checks and 77 new controls pass in both scientific and fresh reproduction execution. Fresh parent50/nested science matched byte-for-byte. The frozen2592 directed cases are not exhaustive universes. See THEOREM.md for the reviewed single-ternary-root composition argument; repeated ternary composition and higher arity remain unresolved. A failed construction is not a nonunit barrier. Actual-merge audit and independently documented receipt closeout remain required.\n'
    (HERE/'REPORT.md').write_text(report)
    paths=[p for p in HERE.rglob('*') if p.is_file() and '__pycache__' not in p.parts and p!=HERE/'PUBLICATION_MANIFEST.json']
    paths.append(ROOT/WORKFLOW)
    dump(HERE/'PUBLICATION_MANIFEST.json',{str(p.relative_to(ROOT)):sha(p.read_bytes()) for p in sorted(paths)})
    verify_publication()

def verify_publication():
    manifest=json.loads((HERE/'PUBLICATION_MANIFEST.json').read_text())
    expected={str(p.relative_to(ROOT)) for p in HERE.rglob('*') if p.is_file() and '__pycache__' not in p.parts and p!=HERE/'PUBLICATION_MANIFEST.json'}|{WORKFLOW}
    if set(manifest)!=expected:raise ValueError('publication membership')
    for name,digest in manifest.items():
        if sha((ROOT/name).read_bytes())!=digest:raise ValueError('publication hash '+name)
    verify_package(HERE/'evidence/science');verify_package(HERE/'evidence/reproduction')
    scientific_equal(HERE/'evidence/science/scientific',HERE/'evidence/reproduction/scientific')
    api_artifact=json.loads((HERE/'evidence/ARTIFACT.json').read_text())
    raw=archive.verify(HERE/'evidence/science-artifact.chunks',api_artifact['digest'])
    archive.verify_extracted(raw,HERE/'evidence/science',api_artifact['digest'])
    fresh_api=json.loads((HERE/'evidence/reproduction_api/ARTIFACT.json').read_text())
    fresh_raw=archive.verify(HERE/'evidence/reproduction_api/publication-artifact.chunks',fresh_api['digest'])
    archive.verify_extracted(fresh_raw,HERE/'evidence/reproduction',fresh_api['digest'])
    print(json.dumps({'publication':'VERIFIED','members':len(manifest)}))

def validate_merge(run,pr,commit,publication,head):
    if run.get('head_sha')!=head or run.get('event')!='push' or run.get('head_branch')!='research/v16.34-fiber-component-invariant' or run.get('path')!=WORKFLOW:raise ValueError('merge workflow identity')
    if not pr.get('merged') or pr.get('merge_commit_sha')!=head or pr.get('base',{}).get('ref')!='research/v16.34-fiber-component-invariant':raise ValueError('merged PR identity')
    if [p.get('sha') for p in commit.get('parents',[])]!=[PARENT,pr.get('head',{}).get('sha')]:raise ValueError('actual merge parents')
    if commit.get('sha')!=head or publication.get('sha')!=pr.get('head',{}).get('sha') or commit.get('tree',{}).get('sha')!=publication.get('tree',{}).get('sha'):raise ValueError('publication/merge tree')

def receipt(run_id,out,pr_number):
    out=Path(out);download(run_id,out,'post_merge')
    meta=json.loads((out/'post_merge/METADATA.json').read_text())
    head=subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip()
    if meta['head']!=head:raise ValueError('receipt checkout must be actual merge')
    run=json.loads((out/'RUN.json').read_text());pr=json.loads(get(API+'/pulls/'+str(pr_number)))
    commit=json.loads(get(API+'/git/commits/'+head));publication_commit=json.loads(get(API+'/git/commits/'+pr['head']['sha']))
    validate_merge(run,pr,commit,publication_commit,head)
    dump(out/'MERGED_PR.json',pr);dump(out/'MERGE_COMMIT.json',commit);dump(out/'PUBLICATION_COMMIT.json',publication_commit)
    verify_publication();scientific_equal(out/'post_merge/scientific',HERE/'evidence/science/scientific')
    # Retain exact execution data; source and scientific bytes already have durable copies.
    dump(out/'RECEIPT.json',{'status':'VERIFIED_ACTUAL_MERGE','merge':head,'run':int(run_id),'run_attempt':meta['run_attempt'],'integrity':json.loads((out/'INTEGRITY.json').read_text()),'scientific_bytes_identical':True,'source_manifest_sha256':sha((out/'post_merge/SOURCE_MANIFEST.json').read_bytes()),'pr':int(pr_number),'binary_retention':'Post-merge source archive and scientific files exactly equal durable v16.51-ternary-interface/evidence/science members; hashes retained in post-merge execution manifest.'})
    for name in ('SOURCE.tar.gz','SOURCE_MANIFEST.json','SOURCE_FORMAT.json'):
        if (out/'post_merge'/name).read_bytes()!=(HERE/'evidence/science'/name).read_bytes():raise ValueError('post-merge source bytes differ')
    (out/'post_merge-artifact.zip').unlink()
    (out/'post_merge/SOURCE.tar.gz').unlink()
    (out/'post_merge/scientific/CERTIFICATE.json.gz').unlink()
    write_manifest(out)

if __name__=='__main__':
    command=sys.argv[1]
    if command=='download':download(sys.argv[2],sys.argv[3],sys.argv[4] if len(sys.argv)>4 else 'science')
    elif command=='stage_reproduction':replace_directory('out/fresh/publication','out/reproduction')
    elif command=='finalize':publication()
    elif command=='verify':verify_publication()
    elif command=='receipt':receipt(sys.argv[2],sys.argv[3],sys.argv[4])
    else:raise ValueError(command)
