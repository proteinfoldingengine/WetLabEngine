"""Evidence aggregation: complete identities, mechanism witnesses, exact bytes.

Path mathematics is independently checked inside every primary/reproduction
shard. This aggregation rechecks complete identity membership and original
artifact/source bindings, rather than treating successful totals as coverage.
"""
from collections import Counter
import gzip
import hashlib
from itertools import zip_longest
import json
import os
from pathlib import Path,PurePosixPath
import re
import resource
import subprocess
import sys
import urllib.request
import urllib.error
import urllib.parse
import zipfile

HERE=Path(__file__).resolve().parent
BASE='ResearchHistory/UQCF-GEM/demos/v16.54-parent-support-connectivity/'
REPO='proteinfoldingengine/WetLabEngine'
REQUIRED={'direct_vacancy','buffered_cycle','repeated_row_colors','element_spare_is_old_owner',
          'original_packet_overlap','original_packet_repeat','neighbor_both_maximum','neighbor_one_maximum',
          'repeated_maximum_layers','saturated_partition','empty_contracted_edge','unsafe_repeated_clone',
          'ordinary_cyclic_balancing','exceptional_cyclic_balancing','explicit_module_pair','module_method_obstruction',
          'guard_slot_refusal','guard_transfer','palette_boundary_refusal','palette_split',
          'finite_reserve_reuse','native_clearance_under_excursion'}

def serial(x):return json.dumps(x,sort_keys=True,separators=(',',':'),allow_nan=False)
def dump(path,obj):Path(path).write_text(serial(obj)+'\n')
def digest_file(path):
    h=hashlib.sha256()
    with Path(path).open('rb') as f:
        for chunk in iter(lambda:f.read(1048576),b''):h.update(chunk)
    return h.hexdigest()

def check_partition(shards):
    if len(shards)!=8:return ['missing or extra shard']
    errors=[]
    try:
        ordered=sorted(shards,key=lambda x:x['shard']);total=ordered[0]['total'];whole=ordered[0]['whole_universe_sha256'];scope=ordered[0]['scope']
        if type(total) is not int or total<8 or not re.fullmatch('[0-9a-f]{64}',whole):errors.append('invalid full universe binding')
        if [x['shard'] for x in ordered]!=list(range(8)):errors.append('duplicate/substituted shard')
        for i,s in enumerate(ordered):
            if s['shards']!=8 or s['total']!=total or s['whole_universe_sha256']!=whole or s['scope']!=scope:errors.append('inconsistent shard universe')
            if type(s['start']) is not int or type(s['stop']) is not int or (s['start'],s['stop'])!=(total*i//8,total*(i+1)//8):errors.append('overlapping/missing/nonprescribed interval')
            if not re.fullmatch('[0-9a-f]{64}',s['identity_sha256']):errors.append('invalid shard identity binding')
    except (KeyError,TypeError,ValueError):errors.append('malformed partition')
    return errors

def check_required_diagnostics(diagnostics):
    return ['missing mechanism witness: '+name for name in sorted(REQUIRED) if type(diagnostics.get(name)) is not int or diagnostics[name]<=0]

def compare_reproduction(primary,reproduction):
    return [] if primary and primary==reproduction else ['deterministic scientific membership or bytes differ']

def check_run_binding(metadata,run,attempt,head):
    expected={'head_sha':head,'status':'completed','conclusion':'success','run_attempt':attempt,
              'id':run,'path':'.github/workflows/v16.54-mechanism-validation.yml'}
    errors=['campaign metadata mismatch: '+key for key,value in expected.items() if metadata.get(key)!=value]
    if metadata.get('event') not in ('push','workflow_dispatch'):errors.append('unapproved campaign event')
    return errors

def check_helper_binding(expected,actual):
    return [] if expected and expected==actual else ['executing scientific helpers differ from target campaign']

def check_merge_sources(parents,expected,actual):
    errors=[]
    if len(parents)!=2 or any(not re.fullmatch('[0-9a-f]{40}',p) for p in parents):errors.append('actual audit requires a two-parent merge')
    if not expected or expected!=actual:errors.append('actual merge scientific source differs from certified primary')
    return errors

def archive_parts(source,destination,expected_digest,chunk_bytes=16*1024**2):
    source=Path(source);destination=Path(destination)
    if type(chunk_bytes) is not int or not 0<chunk_bytes<=16*1024**2:raise ValueError('invalid archive part size')
    if digest_file(source)!=expected_digest:raise ValueError('original archive digest mismatch before publication')
    destination.mkdir(parents=True,exist_ok=False);parts=[]
    with source.open('rb') as stream:
        while True:
            data=stream.read(chunk_bytes)
            if not data:break
            name='original.zip.part'+str(len(parts)).zfill(4)
            (destination/name).write_bytes(data)
            parts.append({'name':name,'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest()})
    rebuilt=hashlib.sha256();length=0
    for part in parts:
        data=(destination/part['name']).read_bytes()
        if len(data)!=part['bytes'] or hashlib.sha256(data).hexdigest()!=part['sha256']:raise ValueError('published part changed')
        rebuilt.update(data);length+=len(data)
    if rebuilt.hexdigest()!=expected_digest or length!=source.stat().st_size:raise ValueError('original archive reconstruction differs')
    manifest={'archive_sha256':expected_digest,'archive_bytes':length,'parts':parts,'reconstruction':'Concatenate parts in listed order as original.zip; verify archive_sha256 before extracting.'}
    dump(destination/'PARTS.json',manifest)
    return manifest

def bind_actual_merge(out):
    if os.environ.get('GITHUB_ACTIONS')!='true' or os.environ['GITHUB_REF']!='refs/heads/research/v16.34-fiber-component-invariant':raise ValueError('audit requires actual integration branch event')
    out=Path(out);out.mkdir(parents=True,exist_ok=True)
    head=subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip()
    if head!=os.environ['GITHUB_SHA'] or head!=os.environ['GITHUB_WORKFLOW_SHA']:raise ValueError('actual merge checkout/workflow mismatch')
    contract=json.loads((HERE/'AUDIT_CONTRACT.json').read_text())
    if set(contract)!={'certified_primary_sha','preregistration_sha','scope'} or contract['scope']!='all' or contract['preregistration_sha']!='a189546887e8744092deebecbdf73076b66ec044':raise ValueError('invalid audit contract')
    target=contract['certified_primary_sha']
    if not re.fullmatch('[0-9a-f]{40}',target):raise ValueError('invalid primary SHA')
    parents=subprocess.check_output(['git','show','-s','--format=%P',head],text=True).split()
    def science(ref):
        # Mutable reporting prose is excluded; frozen proof/review bytes remain
        # enforced by protocol verification in every complete domain shard.
        result={BASE+name:digest for name,digest in _source_inventory(ref).items() if name.endswith('.py') or name=='protocol.json'}
        for name in ('v16.54-mechanism-validation.yml','v16.54-publication.yml','v16.54-red.yml','v16.54-evidence.yml'):
            path='.github/workflows/'+name
            result[path]=hashlib.sha256(subprocess.check_output(['git','show',ref+':'+path])).hexdigest()
        return result
    expected=science(target);actual=science(head)
    errors=check_merge_sources(parents,expected,actual)
    if errors:raise ValueError(errors)
    subprocess.run(['git','merge-base','--is-ancestor',target,parents[1]],check=True)
    subprocess.run(['git','merge-base','--is-ancestor',contract['preregistration_sha'],target],check=True)
    if any(Path(name).read_bytes()!=subprocess.check_output(['git','show',head+':'+name]) for name in actual):raise ValueError('dirty audit checkout')
    dump(out/'ACTUAL_MERGE_BINDING.json',{'merge_sha':head,'parents':parents,'primary_sha':target,'scientific_source_hashes':actual,'workflow_sha':os.environ['GITHUB_WORKFLOW_SHA'],'run_id':os.environ['GITHUB_RUN_ID'],'attempt':os.environ['GITHUB_RUN_ATTEMPT']})

def execution_binding(head,out):
    actual_head=subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip()
    provenance={'head':actual_head,'workflow_sha':os.environ['GITHUB_WORKFLOW_SHA'],
                'trigger_sha':os.environ['GITHUB_SHA'],'run_id':os.environ['GITHUB_RUN_ID'],
                'attempt':os.environ['GITHUB_RUN_ATTEMPT'],'target_head':head,
                'publication_sha256':digest_file(HERE/'publication.py')}
    dump(out/'AGGREGATOR_PROVENANCE.json',provenance)
    if provenance['workflow_sha']!=actual_head or provenance['trigger_sha']!=actual_head:raise ValueError('aggregator checkout/workflow mismatch')
    if subprocess.check_output(['git','show',actual_head+':'+BASE+'publication.py'])!=(HERE/'publication.py').read_bytes():raise ValueError('aggregator source mismatch')
    names=('campaign.py','verifier.py')
    wanted={name:hashlib.sha256(subprocess.check_output(['git','show',head+':'+BASE+name])).hexdigest() for name in names}
    actual={name:digest_file(HERE/name) for name in names}
    if check_helper_binding(wanted,actual):raise ValueError('executing scientific helpers differ from target campaign')
    dump(out/'EXECUTING_HELPERS.json',actual)

def verify_inherited_package(folder,head):
    recorded=json.loads((folder/'SOURCE_MANIFEST.json').read_text())
    if not recorded:raise ValueError('empty inherited source inventory')
    for name,digest in recorded.items():
        path=PurePosixPath(name)
        if path.is_absolute() or '..' in path.parts:raise ValueError('invalid inherited source path')
        target=subprocess.check_output(['git','show',head+':'+name])
        if hashlib.sha256(target).hexdigest()!=digest or Path(name).read_bytes()!=target:raise ValueError('inherited source differs from target Git or executing checkout')
    inherited='ResearchHistory/UQCF-GEM/demos/v16.53-four-child-boundary'
    if any(inherited+'/'+name not in recorded for name in ('integrity.py','snapshot.py','bindings.py')) or 'tools/retained_ci/core.py' not in recorded:raise ValueError('unbound inherited verification helper')
    # Separate import namespace; the unchanged verifier enforces source archive,
    # exact 45 scientific files, 1193 controls and their frozen assertion identities.
    command='import sys;sys.path.insert(0,sys.argv[1]);import integrity;integrity.verify_package(sys.argv[2])'
    subprocess.run([sys.executable,'-c',command,inherited,str(folder.resolve())],check=True)

def checkpoint(out,phase,**fields):
    path=out/'STATUS.json';state=json.loads(path.read_text()) if path.exists() else {}
    state.update(status='INCOMPLETE',phase=phase,**fields)
    temporary=out/'STATUS.tmp';dump(temporary,state);temporary.replace(path)

def api(path):
    request=urllib.request.Request('https://api.github.com/repos/'+REPO+'/'+path,headers={'Accept':'application/vnd.github+json','Authorization':'Bearer '+os.environ['GH_TOKEN'],'X-GitHub-Api-Version':'2022-11-28'})
    with urllib.request.urlopen(request) as r:return json.load(r)

def download_artifact(item,dest):
    dest=Path(dest);dest.parent.mkdir(parents=True,exist_ok=True)
    expected_url='https://api.github.com/repos/'+REPO+'/actions/artifacts/'+str(item['id'])+'/zip'
    if item['archive_download_url']!=expected_url:raise ValueError('artifact endpoint not bound to repository')
    request=urllib.request.Request(expected_url,headers={'Authorization':'Bearer '+os.environ['GH_TOKEN'],'Accept':'application/vnd.github+json'})
    class NoRedirect(urllib.request.HTTPRedirectHandler):
        def redirect_request(self,req,fp,code,msg,headers,newurl):return None
    try:
        response=urllib.request.build_opener(NoRedirect()).open(request)
    except urllib.error.HTTPError as exc:
        if exc.code not in (301,302,303,307,308):raise
        location=exc.headers['Location']
        if urllib.parse.urlparse(location).scheme!='https':raise ValueError('non-HTTPS artifact redirect')
        # GitHub credentials stay on api.github.com; signed download needs none.
        response=urllib.request.urlopen(location)
    with response,dest.open('wb') as output:
        for chunk in iter(lambda:response.read(1048576),b''):output.write(chunk)
    if item['digest']!='sha256:'+digest_file(dest) or dest.stat().st_size!=item['size_in_bytes']:raise ValueError('original GitHub archive digest/length mismatch')
    folder=dest.with_suffix('');folder.mkdir(exist_ok=True)
    with zipfile.ZipFile(dest) as archive:
        for entry in archive.infolist():
            path=PurePosixPath(entry.filename)
            if path.is_absolute() or '..' in path.parts or '\\' in entry.filename:raise ValueError('unsafe archive member')
        archive.extractall(folder)
    return folder

def _source_inventory(head):
    paths=subprocess.check_output(['git','ls-tree','-r','--name-only',head,'--',BASE],text=True).splitlines()
    wanted=[]
    for name in paths:
        relative=name[len(BASE):];parts=PurePosixPath(relative).parts
        if len(parts)==1 and (relative.endswith('.py') or relative.endswith('.md') or relative=='protocol.json') or len(parts)==2 and parts[0]=='tests' and relative.endswith('.py'):wanted.append(relative)
    return {name:hashlib.sha256(subprocess.check_output(['git','show',head+':'+BASE+name])).hexdigest() for name in wanted}

def _checked_source(folder,head):
    recorded=json.loads((folder/'SOURCE_MANIFEST.json').read_text());wanted=_source_inventory(head)
    if recorded!=wanted:raise ValueError('exact scientific source inventory mismatch')
    files={str(p.relative_to(folder/'source')):digest_file(p) for p in (folder/'source').rglob('*') if p.is_file()}
    if files!=wanted:raise ValueError('archived source bytes/membership mismatch')

def _records(path):
    with gzip.open(path,'rt',encoding='utf-8') as stream:
        for line in stream:yield json.loads(line)

def _diagnose(case,record):
    from verifier import covering_number
    family,p,roots,ch=case['identity'];f=record.get('facts',{});out=Counter()
    for event in record.get('events',[]):
        out[event['kind']]+=1
        if event['kind']=='buffered_cycle' and len({e[2] for e in event['edges']})<len(event['edges']):out['repeated_row_colors']+=1
        if event['kind']=='element_buffer' and event['target']==event['old_owner']:out['element_spare_is_old_owner']+=1
    if family=='M1':
        if p['kind']=='double_packet':
            if set(ch[0])&set(ch[1]):out['original_packet_overlap']+=1
            if ch[0]==ch[1]:out['original_packet_repeat']+=1
        if p['kind']=='neighbor':out['neighbor_one_maximum' if ch['right'] is None else 'neighbor_both_maximum']+=1
        if p['kind']=='layers' and len(f['layers'])>=2:out['repeated_maximum_layers']+=1
    if family=='M3' and p['kind']=='saturated':out['saturated_partition']+=1
    if family=='M4':
        if any(x['contraction']=='infinity' for x in f['clones']):out['empty_contracted_edge']+=1
        if f['completed_tau']==[6,5,4]:out['unsafe_repeated_clone']+=1
    if family=='M5':
        if p['kind']=='module_pair':out['explicit_module_pair']+=1
        if p['kind']=='obstruction':out['module_method_obstruction']+=1
        if p.get('form')=='cyclic':
            for move in f.get('balancing',[]):out['exceptional_cyclic_balancing' if move['before'][0]==move['after'][0] else 'ordinary_cyclic_balancing']+=1
    if family=='M6':out['guard_slot_refusal' if record['status']=='REFUSED' else 'guard_transfer']+=1
    if family=='M7':out['palette_boundary_refusal' if record['status']=='REFUSED' else 'palette_split']+=1
    if family=='M8':
        history={}
        for assignment in f['assignments']:
            for original,reserve in assignment:history.setdefault(reserve,set()).add(original)
        if any(len(labels)>1 for labels in history.values()):out['finite_reserve_reuse']+=1
    if family=='M9':
        for event in f['clearance']:
            vertex=record['nested_path'][event['start']]
            if covering_number([vertex[v] for v in record['nodes'][0]])==p['q']-1:out['native_clearance_under_excursion']+=1
    return out

def aggregate(run,attempt,head,out):
    if os.environ.get('GITHUB_ACTIONS')!='true':raise RuntimeError('scientific aggregation is GitHub-only')
    out=Path(out);out.mkdir(parents=True,exist_ok=True)
    checkpoint(out,'initialization',run=run,attempt=attempt,scientific_sha=head,reason='aggregation not completed')
    try:
        resource.setrlimit(resource.RLIMIT_AS,(4294967296,4294967296))
        return _aggregate(run,attempt,head,out)
    except BaseException as error:
        phase=json.loads((out/'STATUS.json').read_text())['phase']
        checkpoint(out,phase,reason=type(error).__name__+': '+str(error))
        raise

def _aggregate(run,attempt,head,out):
    checkpoint(out,'execution_binding')
    execution_binding(head,out)
    from campaign import validate_campaign_summary
    from verifier import reconstruct_cases
    checkpoint(out,'target_run_metadata')
    metadata=api('actions/runs/'+str(run)+'/attempts/'+str(attempt));dump(out/'RUN.json',metadata)
    if check_run_binding(metadata,run,attempt,head):raise ValueError('campaign attempt/source/workflow binding failed')
    inventory=[];page=1
    while True:
        response=api('actions/runs/'+str(run)+'/artifacts?per_page=100&page='+str(page));inventory+=response['artifacts']
        if len(response['artifacts'])<100:break
        page+=1
    dump(out/'ARTIFACTS.json',inventory);folders=[];freezes=[];manifests={};provenances=[]
    for i in range(8):
        checkpoint(out,'shard_artifacts',shard=i)
        stem='v1654-domain-'+str(i)+'-'+head
        candidates=[a for a in inventory if a['name'] in (stem,stem+'-attempt-'+str(attempt))]
        if len(candidates)!=1:raise ValueError('missing or ambiguous original shard artifact')
        folder=download_artifact(candidates[0],out/('shard-'+str(i)+'.zip'));folders.append(folder)
        provenance=json.loads((folder/'PROVENANCE.json').read_text());provenances.append(provenance)
        if provenance['scientific_sha']!=head or provenance['workflow_sha']!=head or str(provenance['run_id'])!=str(run) or int(provenance['attempt'])!=attempt or provenance['shard']!=i or provenance['scope']!='all':raise ValueError('shard provenance mismatch')
        _checked_source(folder,head)
        science=folder/'scientific';manifest=json.loads((science/'MANIFEST.json').read_text())
        if set(manifest)!={'CASES.jsonl.gz','RECORDS.jsonl.gz','DOMAIN_FREEZE.json','SUMMARY.json'}:raise ValueError('scientific manifest membership')
        if {p.name for p in science.iterdir() if p.is_file()}!=set(manifest)|{'MANIFEST.json'}:raise ValueError('unmanifested scientific file')
        if any(digest_file(science/name)!=digest for name,digest in manifest.items()):raise ValueError('scientific byte corruption')
        manifests.update({str(i)+'/'+name:digest for name,digest in manifest.items()})
        freeze=json.loads((science/'DOMAIN_FREEZE.json').read_text());freezes.append(freeze)
        summary=json.loads((science/'SUMMARY.json').read_text());status=json.loads((folder/'STATUS.json').read_text())
        if any(status.get(key)!=value for key,value in summary.items()) or validate_campaign_summary({**summary,**provenance}):raise ValueError('campaign success/count/provenance mismatch')
    errors=check_partition(freezes)
    if errors:raise ValueError(errors)
    protocol=json.loads(subprocess.check_output(['git','show',head+':'+BASE+'protocol.json'],text=True))
    expected=iter(reconstruct_cases(protocol));whole=hashlib.sha256();total=0;diagnostics=Counter();family_counts=Counter()
    for i,folder in enumerate(folders):
        checkpoint(out,'independent_identity_stream',shard=i,checked=total)
        science=folder/'scientific';freeze=freezes[i];summary=json.loads((science/'SUMMARY.json').read_text());identities=hashlib.sha256();record_hash=hashlib.sha256();count=0;first=None;last=None
        for case,record in zip_longest(_records(science/'CASES.jsonl.gz'),_records(science/'RECORDS.jsonl.gz')):
            if case is None or record is None:raise ValueError('case/record multiplicity mismatch')
            want=next(expected,None)
            if want is None or serial(case)!=serial(want) or record['identity']!=case['identity']:raise ValueError('full independent aggregate identity/input mismatch')
            if record['status'] not in ('PASS','REFUSED'):raise ValueError('unfinished mechanism result')
            whole.update((serial(case)+'\n').encode());identities.update((serial(case['identity'])+'\n').encode());record_hash.update((serial(record)+'\n').encode());count+=1;total+=1;first=first or case['identity'];last=case['identity'];diagnostics.update(_diagnose(case,record));family_counts[case['identity'][0]]+=1
        if count!=freeze['stop']-freeze['start'] or count!=summary['checked'] or first!=freeze['first'] or last!=freeze['last'] or identities.hexdigest()!=freeze['identity_sha256'] or identities.hexdigest()!=summary['verified_identity_sha256'] or record_hash.hexdigest()!=summary['record_sha256']:raise ValueError('shard complete stream binding mismatch')
    if next(expected,None) is not None or total!=freezes[0]['total'] or whole.hexdigest()!=freezes[0]['whole_universe_sha256']:raise ValueError('aggregate omitted/substituted universe')
    checkpoint(out,'mechanism_diagnostics',checked=total)
    errors=check_required_diagnostics(diagnostics)
    if errors:raise ValueError(errors)
    checkpoint(out,'inherited_package')
    inherited_names=('v1654-inherited-'+head,'v1654-inherited-'+head+'-attempt-'+str(attempt));inherited=[a for a in inventory if a['name'] in inherited_names]
    if len(inherited)!=1:raise ValueError('complete inherited artifact unavailable')
    inherited_folder=download_artifact(inherited[0],out/'inherited.zip')
    inherited_manifest=json.loads((inherited_folder/'MANIFEST.json').read_text())
    inherited_actual={str(p.relative_to(inherited_folder)):digest_file(p) for p in inherited_folder.rglob('*') if p.is_file() and p!=inherited_folder/'MANIFEST.json'}
    if inherited_manifest!=inherited_actual:raise ValueError('inherited internal manifest mismatch')
    verify_inherited_package(inherited_folder,head)
    metrics=json.loads((inherited_folder/'METRICS.json').read_text());meta=json.loads((inherited_folder/'METADATA.json').read_text())
    if metrics['inherited_tests']!=1150 or metrics['new_controls']!=43 or not metrics['all_commands_passed']:raise ValueError('inherited full-stack metrics')
    if meta['head']!=head or meta['workflow_sha']!=head or meta['trigger_sha']!=head or str(meta['run_id'])!=str(run) or int(meta['run_attempt'])!=attempt:raise ValueError('inherited provenance mismatch')
    for p in sorted((inherited_folder/'scientific').rglob('*')):
        if p.is_file():manifests['inherited/'+str(p.relative_to(inherited_folder/'scientific'))]=digest_file(p)
    dump(out/'SCIENTIFIC_MANIFEST.json',manifests)
    dump(out/'AGGREGATE.json',{'status':'PASS','run':run,'attempt':attempt,'scientific_sha':head,'workflow_sha':head,'total':total,'family_counts':dict(family_counts),'diagnostics':dict(diagnostics),'universal_higher_floor':'OPEN','certification':'PENDING_REPRODUCTION_AND_ACTUAL_MERGE'})
    final={'status':'PASS','phase':'complete','run':run,'attempt':attempt,'scientific_sha':head,'checked':total}
    dump(out/'STATUS.tmp',final);(out/'STATUS.tmp').replace(out/'STATUS.json')
    return manifests

if __name__=='__main__':aggregate(int(sys.argv[1]),int(sys.argv[2]),sys.argv[3],sys.argv[4])
