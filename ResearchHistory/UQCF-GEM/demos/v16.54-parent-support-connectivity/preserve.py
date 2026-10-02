"""Publish verified original campaign ZIP bytes without local science execution."""
import hashlib,json,os,re,resource,shutil,subprocess,sys
from pathlib import Path
from publication import api,archive_parts,compare_reproduction,digest_file,download_artifact,dump,BASE

def validated_campaign(aggregate,status,metadata,provenance):
    run=aggregate.get('run');attempt=aggregate.get('attempt');head=aggregate.get('scientific_sha')
    if type(run) is not int or run<=0 or type(attempt) is not int or attempt<=0 or not isinstance(head,str) or not re.fullmatch('[0-9a-f]{40}',head):raise ValueError('invalid campaign destination')
    if aggregate.get('status')!='PASS' or aggregate.get('workflow_sha')!=head:raise ValueError('aggregate campaign binding')
    if any(status.get(k)!=v for k,v in {'status':'PASS','run':run,'attempt':attempt,'scientific_sha':head}.items()):raise ValueError('campaign status substitution')
    if any(metadata.get(k)!=v for k,v in {'id':run,'run_attempt':attempt,'head_sha':head,'status':'completed','conclusion':'success'}.items()):raise ValueError('campaign run substitution')
    if provenance.get('target_head')!=head:raise ValueError('aggregate target substitution')
    return run,attempt,head

def prepare(request,out):
    if os.environ.get('GITHUB_ACTIONS')!='true':raise RuntimeError('GitHub-only evidence packaging')
    reference=None
    if 'compare_to' in request:
        reference=request['compare_to']
        if not isinstance(reference,dict) or set(reference)!={'run','attempt'} or any(type(reference[k]) is not int or reference[k]<=0 for k in reference):raise ValueError('invalid reproduction reference')
    resource.setrlimit(resource.RLIMIT_AS,(4294967296,4294967296))
    out=Path(out);out.mkdir(parents=True,exist_ok=False)
    run=request['aggregate_run'];attempt=request['aggregate_attempt'];head=request['aggregate_head']
    if type(run) is not int or run<=0 or type(attempt) is not int or attempt<=0 or not re.fullmatch('[0-9a-f]{40}',head):raise ValueError('invalid aggregate target')
    metadata=api(f'actions/runs/{run}/attempts/{attempt}')
    wanted={'id':run,'run_attempt':attempt,'head_sha':head,'status':'completed','conclusion':'success','event':'push','path':'.github/workflows/v16.54-publication.yml'}
    if any(metadata.get(k)!=v for k,v in wanted.items()):raise ValueError('aggregate run binding')
    inventory=[];page=1
    while True:
        rows=api(f'actions/runs/{run}/artifacts?per_page=100&page={page}')['artifacts'];inventory+=rows
        if len(rows)<100:break
        page+=1
    matches=[a for a in inventory if a['name']==f'v1654-aggregate-{head}-attempt-{attempt}']
    if len(matches)!=1:raise ValueError('aggregate original artifact unavailable or ambiguous')
    folder=download_artifact(matches[0],out/'aggregate-transport.zip')
    aggregate=json.loads((folder/'AGGREGATE.json').read_text());status=json.loads((folder/'STATUS.json').read_text())
    provenance=json.loads((folder/'AGGREGATOR_PROVENANCE.json').read_text())
    if aggregate['status']!='PASS' or status['status']!='PASS' or provenance['head']!=head or provenance['workflow_sha']!=head or str(provenance['run_id'])!=str(run) or int(provenance['attempt'])!=attempt:raise ValueError('aggregate result/provenance mismatch')
    source=subprocess.check_output(['git','show',head+':'+BASE+'publication.py'])
    if provenance['publication_sha256']!=hashlib.sha256(source).hexdigest():raise ValueError('aggregate publication source mismatch')
    campaign,campaign_attempt,scientific=validated_campaign(aggregate,status,json.loads((folder/'RUN.json').read_text()),provenance)
    comparison=None
    if reference is not None:
        path=BASE+f"evidence/validated/run-{reference['run']}-attempt-{reference['attempt']}/SCIENTIFIC_MANIFEST.json"
        recorded=subprocess.check_output(['git','show','HEAD:'+path])
        current=(folder/'SCIENTIFIC_MANIFEST.json').read_bytes()
        if compare_reproduction(json.loads(recorded),json.loads(current)):raise ValueError('deterministic scientific reproduction differs')
        comparison={'status':'BYTE_IDENTICAL','reference':reference,'reference_manifest_git_blob':subprocess.check_output(['git','rev-parse','HEAD:'+path],text=True).strip(),
                    'reference_manifest_sha256':hashlib.sha256(recorded).hexdigest(),'current_manifest_sha256':hashlib.sha256(current).hexdigest(),'files':len(json.loads(current))}
    destination=Path(BASE)/'evidence/validated'/f'run-{campaign}-attempt-{campaign_attempt}'
    if destination.exists():raise ValueError('refusing to overwrite published evidence')
    destination.mkdir(parents=True)
    originals=json.loads((folder/'ARTIFACTS.json').read_text());receipts={}
    for label,stem in [(f'shard-{i}',f'v1654-domain-{i}-{scientific}') for i in range(8)]+[('inherited',f'v1654-inherited-{scientific}')]:
        candidates=[a for a in originals if a['name'] in (stem,stem+f'-attempt-{campaign_attempt}')]
        if len(candidates)!=1:raise ValueError('original campaign archive binding')
        item=candidates[0];archive=folder/(label+'.zip')
        if archive.stat().st_size!=item['size_in_bytes']:raise ValueError('original archive byte length')
        manifest=archive_parts(archive,destination/label,item['digest'].removeprefix('sha256:'))
        receipts[label]={'artifact':item,'archive':manifest}
    for name in ('AGGREGATE.json','STATUS.json','SCIENTIFIC_MANIFEST.json','RUN.json','ARTIFACTS.json','AGGREGATOR_PROVENANCE.json','EXECUTING_HELPERS.json'):
        shutil.copyfile(folder/name,destination/name)
    receipt={'aggregate_transport_artifact':matches[0],'aggregate_run':metadata,'original_campaign_archives':receipts,
             'publication_workflow_sha':os.environ['GITHUB_WORKFLOW_SHA'],'publication_event_sha':os.environ['GITHUB_SHA'],
             'publication_run':os.environ['GITHUB_RUN_ID'],'publication_attempt':os.environ['GITHUB_RUN_ATTEMPT'],
             'universal_higher_floor':'OPEN','status':'ORIGINAL_BYTES_VERIFIED'}
    dump(destination/'PUBLICATION_RECEIPT.json',receipt)
    if comparison is not None:dump(destination/'REPRODUCTION.json',comparison)
    files={str(p.relative_to(destination)):digest_file(p) for p in sorted(destination.rglob('*')) if p.is_file()}
    dump(destination/'PUBLICATION_MANIFEST.json',files)
    (out/'DESTINATION.txt').write_text(str(destination)+'\n')
    # Small receipt artifact permits independent inspection without redownloading
    # the redundant transport wrapper. Every original campaign ZIP is preserved.
    receipt_out=out/'receipt';receipt_out.mkdir()
    for name in ('PUBLICATION_RECEIPT.json','PUBLICATION_MANIFEST.json','AGGREGATE.json','SCIENTIFIC_MANIFEST.json'):
        shutil.copyfile(destination/name,receipt_out/name)
    if comparison is not None:shutil.copyfile(destination/'REPRODUCTION.json',receipt_out/'REPRODUCTION.json')
    return destination

if __name__=='__main__':prepare(json.loads(Path(sys.argv[1]).read_text()),sys.argv[2])
