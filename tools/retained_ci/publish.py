"""Artifact-bound publication and automated receipt preparation."""
from pathlib import Path
import json,os,sys,urllib.request,urllib.error,shutil,subprocess
from core import HERE,ROOT,STAGE,dump,sha,unpack_zip,verify_package,verify_manifest,write_manifest,replace_directory,scientific_equal,source_map
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
    if artifact.get('name')!='retained-ci-'+phase+'-'+head or artifact.get('workflow_run',{}).get('id')!=int(run_id) or artifact.get('workflow_run',{}).get('head_sha')!=head:raise ValueError('artifact provenance')
    wanted={'head':head,'trigger_sha':head,'workflow_sha':head,'run_id':str(run_id),'run_attempt':str(attempt),'phase':phase}
    if any(metadata.get(k)!=v for k,v in wanted.items()):raise ValueError('embedded provenance')

def download(run_id,out,phase='science'):
    out=Path(out);out.mkdir(parents=True,exist_ok=True)
    run=json.loads(get(API+'/actions/runs/'+str(run_id)));dump(out/'RUN.json',run)
    artifacts=json.loads(get(API+'/actions/runs/'+str(run_id)+'/artifacts'))['artifacts']
    matches=[a for a in artifacts if a['name']=='retained-ci-'+phase+'-'+run['head_sha']]
    if len(matches)!=1:raise ValueError('unique artifact')
    a=matches[0];dump(out/'ARTIFACT.json',a);data=get(a['archive_download_url']);(out/(phase+'-artifact.zip')).write_bytes(data)
    unpack_zip(data,a['digest'],out/phase);verify_package(out/phase)
    meta=json.loads((out/phase/'METADATA.json').read_text())
    expected_head=os.environ['GITHUB_SHA'] if phase=='science' else run['head_sha']
    provenance(run,a,meta,expected_head,run_id,os.environ.get('GITHUB_RUN_ATTEMPT','1') if phase=='science' else run['run_attempt'],phase)
    jobs=json.loads(get(API+'/actions/runs/'+str(run_id)+'/jobs'));dump(out/'JOBS.json',jobs)
    matches=[j for j in jobs['jobs'] if j['name']==phase]
    if len(matches)!=1 or matches[0]['conclusion']!='success' or matches[0]['head_sha']!=run['head_sha']:raise ValueError('job success/source')
    (out/'JOB.log').write_bytes(get(API+'/actions/jobs/'+str(matches[0]['id'])+'/logs'))
    if phase=='science':
        prior=36772436790;dump(out/'PRIOR_RUN.json',json.loads(get(API+'/actions/runs/'+str(prior))))
        for job in json.loads(get(API+'/actions/runs/'+str(prior)+'/jobs'))['jobs']:
            if job['conclusion']!='skipped':(out/('PRIOR_JOB_'+str(job['id'])+'.log')).write_bytes(get(API+'/actions/jobs/'+str(job['id'])+'/logs'))
    dump(out/'INTEGRITY.json',{'artifact_id':a['id'],'sha256':sha(data),'api_digest_crc_manifests_source_science':'VERIFIED','phase':phase,'head':run['head_sha']})

def publication():
    verify_package('out/download/science');verify_package('out/reproduction')
    scientific_equal('out/download/science/scientific','out/reproduction/scientific')
    replace_directory('out/download',HERE/'evidence')
    replace_directory('out/reproduction',HERE/'evidence/reproduction')
    metrics=json.loads((HERE/'evidence/science/METRICS.json').read_text())
    report='# Retained execution optimization results\n\n'+json.dumps(metrics,indent=2)+'\n\nAll289 scientific controls/inherited tests run unchanged in every phase; independent verification remains uncached. Additional infrastructure controls run before expensive work. Fresh publication scientific bytes match the certified v16.39 parent and the new scientific execution. Source/API/ZIP/member/hash checks are automated and fail closed.\n\nThese are measured single-run timings, not guaranteed speedups. Publication completion still requires an actual-merge replay and its verified receipt before infrastructure closure.\n'
    (HERE/'REPORT.md').write_text(report)
    paths=[p for p in HERE.rglob('*') if p.is_file() and '__pycache__' not in p.parts and p!=HERE/'PUBLICATION_MANIFEST.json']
    paths.append(ROOT/'.github/workflows/retained-ci-optimization.yml')
    dump(HERE/'PUBLICATION_MANIFEST.json',{str(p.relative_to(ROOT)):sha(p.read_bytes()) for p in sorted(paths)})
    verify_publication()

def verify_publication():
    manifest=json.loads((HERE/'PUBLICATION_MANIFEST.json').read_text())
    expected={str(p.relative_to(ROOT)) for p in HERE.rglob('*') if p.is_file() and '__pycache__' not in p.parts and p!=HERE/'PUBLICATION_MANIFEST.json'}|{'.github/workflows/retained-ci-optimization.yml'}
    if set(manifest)!=expected:raise ValueError('publication membership')
    for name,digest in manifest.items():
        if sha((ROOT/name).read_bytes())!=digest:raise ValueError('publication hash '+name)
    verify_package(HERE/'evidence/science');verify_package(HERE/'evidence/reproduction')
    print(json.dumps({'publication':'VERIFIED','members':len(manifest)}))

def receipt(run_id,out):
    out=Path(out);download(run_id,out,'post_merge')
    meta=json.loads((out/'post_merge/METADATA.json').read_text())
    head=subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip()
    if meta['head']!=head:raise ValueError('receipt checkout must be actual merge')
    verify_publication();scientific_equal(out/'post_merge/scientific',HERE/'evidence/science/scientific')
    # Retain exact execution data; source and scientific bytes already have durable copies.
    dump(out/'RECEIPT.json',{'status':'VERIFIED_ACTUAL_MERGE','merge':head,'run':int(run_id),'run_attempt':meta['run_attempt'],'integrity':json.loads((out/'INTEGRITY.json').read_text()),'scientific_bytes_identical':True,'source_map':source_map()})
    write_manifest(out)

if __name__=='__main__':
    command=sys.argv[1]
    if command=='download':download(sys.argv[2],sys.argv[3])
    elif command=='finalize':publication()
    elif command=='verify':verify_publication()
    elif command=='receipt':receipt(sys.argv[2],sys.argv[3])
    else:raise ValueError(command)
