#!/usr/bin/env python3
"""Archive unchanged research source and freshly reproduced deliverables.

Original conversation artifacts are a separate provenance class. A matching
SHA-256, not a filename or similar numerical result, establishes byte identity.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import mimetypes
import os
from pathlib import Path
import platform
import re
import shutil
import subprocess
import sys
import urllib.parse
import urllib.request
import zipfile

SOURCE_SHA='7b6459f18b0add90a2f88cf9b0a152e2aa5c7647'
REPOSITORY='proteinfoldingengine/WetLabEngine'
PREFIX='ResearchHistory/UQCF-GEM'
SUITES=[
 {'version':11,'path':'v15/v15.11','tests':20,'test_files':['test_continuity.py'],'model':'ontology_continuity_audit.py','renderer':None},
 {'version':12,'path':'demos/v15.12-pretime-to-history','tests':30,'test_files':['test_simulation.py','test_presentation.py'],'model':None,'renderer':'render.py'},
 {'version':13,'path':'demos/v15.13-independent-events','tests':27,'test_files':['test_model.py','test_replay.py'],'model':'event_model.py','renderer':'replay.py'},
 {'version':14,'path':'demos/v15.14-record-dependencies','tests':30,'test_files':['test_adaptive.py','test_replay.py'],'model':'adaptive.py','renderer':'replay.py'},
 {'version':15,'path':'demos/v15.15-coherent-records','tests':30,'test_files':['test_coherent.py','test_replay.py'],'model':'coherent_records.py','renderer':'replay.py'},
 {'version':16,'path':'demos/v15.16-partial-pruning','tests':33,'test_files':['test_recoverability.py','test_replay.py'],'model':'recoverability.py','renderer':'replay.py'},
 {'version':17,'path':'demos/v15.17-retained-motion','tests':32,'test_files':['test_motion.py','test_replay.py'],'model':'retained_motion.py','renderer':'replay.py'},
 {'version':18,'path':'demos/v15.18-invariant-completion','tests':34,'test_files':['test_completion.py','test_replay.py'],'model':'completion.py','renderer':'replay.py'},
 {'version':19,'path':'demos/v15.19-linear-prediction','tests':36,'test_files':['test_linear.py','test_replay.py'],'model':'linear_module.py','renderer':'replay.py'},
 {'version':20,'path':'demos/v15.20-physical-predictor','tests':38,'test_files':['test_channel.py','test_replay.py'],'model':'physical_predictor.py','renderer':'replay.py'},
]


def metadata(path: Path) -> dict:
    h=hashlib.sha256()
    with path.open('rb') as f:
        for chunk in iter(lambda:f.read(1024*1024),b''):h.update(chunk)
    return {'name':path.name,'bytes':path.stat().st_size,'sha256':h.hexdigest()}


def package(source: Path, destination: Path) -> None:
    """A deterministic container; it does not change member bytes."""
    files=[]
    for p in sorted(source.rglob('*')):
        if p.is_symlink():raise ValueError('symlink is not accepted in an archive')
        if p.is_file():files.append(p)
    members=[{**metadata(p),'name':p.relative_to(source).as_posix()} for p in files]
    destination.parent.mkdir(parents=True,exist_ok=True)
    with zipfile.ZipFile(destination,'w',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
        for p in files:
            info=zipfile.ZipInfo(p.relative_to(source).as_posix(),(2026,9,13,0,0,0))
            info.compress_type=zipfile.ZIP_DEFLATED
            z.writestr(info,p.read_bytes())
        info=zipfile.ZipInfo('PACKAGE_MANIFEST.json',(2026,9,13,0,0,0))
        info.compress_type=zipfile.ZIP_DEFLATED
        z.writestr(info,json.dumps({'files':members},indent=2)+'\n')
    with zipfile.ZipFile(destination) as z:
        if z.testzip() is not None:raise ValueError('archive CRC failure')
        for row in members:
            data=z.read(row['name'])
            if len(data)!=row['bytes'] or hashlib.sha256(data).hexdigest()!=row['sha256']:
                raise ValueError('archive member byte mismatch')


def verify_remote(local: dict, remote: dict) -> None:
    if (remote.get('name')!=local['name'] or remote.get('size')!=local['bytes'] or
        remote.get('digest')!='sha256:'+local['sha256'] or remote.get('state')!='uploaded'):
        raise ValueError(f"Remote asset is not byte-verified: {local['name']}")


def match_original(row: dict, manifest: dict) -> list[str]:
    return [v['name'] for v in manifest['files'] if v['bytes']==row['bytes'] and v['sha256']==row['sha256']]


def run_logged(command: list[str],cwd: Path,log: Path) -> str:
    log.parent.mkdir(parents=True,exist_ok=True)
    with log.open('w',encoding='utf-8') as out:
        out.write('Command: '+json.dumps(command)+'\n');out.flush()
        result=subprocess.run(command,cwd=cwd,stdout=out,stderr=subprocess.STDOUT,timeout=1500)
    if result.returncode:
        raise RuntimeError(f'Command failed with code {result.returncode}; see {log}')
    return log.read_text(errors='replace').split('\n',1)[1]


def release_notes(source: str,builder: str,count: int) -> str:
    return f'''# UQCF-GEM delivered-artifact archive through v15.20

Research source: `{source}`. Archive tooling: `{builder}`.

**These media, numerical outputs and run logs are regenerated from the unchanged source. They are not the original conversation artifact bytes unless a SHA-256 match is explicitly recorded.** Historical reports and source are preserved, not silently updated.

The release contains per-version source/data/log bundles for v15.11-v15.20, standalone MP4 and offline HTML files for v15.12-v15.20, the full pinned ResearchHistory/UQCF-GEM source snapshot, and asset/member SHA-256 manifests. The reproduction ran {count} selected research tests. It is not an independent scientific review, the entire repository test suite, or a derivation of physical time or gravity. HTML is a downloadable offline replay, not a deployed website.

`ORIGINAL_DELIVERY_MANIFEST.json` records the separately preserved 35 original conversation artifacts. Their combined original-byte bundle remains a separate upload requirement; checksums alone do not archive those bytes. Fresh CI logs do not replace original RED/GREEN logs.

No existing research file, outcome, tolerance, ontology, or main-branch ref is changed by this archive. Archive controls and release uploads use only this repository's temporary GitHub Actions credential.
'''


def build(root: Path,out: Path,originals_path: Path) -> dict:
    root=root.resolve();out=out.resolve()
    producer=subprocess.check_output(['git','rev-parse','HEAD'],cwd=root,text=True).strip()
    subprocess.run(['git','diff','--exit-code',SOURCE_SHA,'HEAD','--',PREFIX+'/demos',PREFIX+'/v15',PREFIX+'/results'],cwd=root,check=True)
    if out.exists():raise ValueError('output directory already exists; do not overwrite an earlier archive')
    assets=out/'assets';assets.mkdir(parents=True)
    original=json.loads(originals_path.read_text())
    if original['count']!=len(original['files']) or original['count']!=35:raise ValueError('original inventory coverage changed')
    shutil.copyfile(originals_path,assets/'ORIGINAL_DELIVERY_MANIFEST.json')
    environment={'python':sys.version,'platform':platform.platform(),
        'packages':subprocess.check_output([sys.executable,'-m','pip','freeze'],text=True).splitlines(),
        'ffmpeg':subprocess.check_output(['ffmpeg','-version'],text=True).splitlines()[0]}
    records=[];total=0
    for spec in SUITES:
        version=spec['version'];label=f'v15.{version}'
        print('Reproducing '+label,flush=True)
        stage=out/'work'/label;source=stage/'source';logs=stage/'fresh_run_logs';generated=stage/'outputs'
        shutil.copytree(root/PREFIX/spec['path'],source,
            ignore=shutil.ignore_patterns('__pycache__','*.pyc','outputs','evidence'))
        source_before={p.relative_to(source).as_posix():metadata(p)['sha256'] for p in source.rglob('*') if p.is_file()}
        log=run_logged([sys.executable,'-m','unittest','-v',*spec['test_files']],source,logs/'tests.log')
        match=re.search(r'Ran (\d+) tests? in',log)
        if not match or int(match.group(1))!=spec['tests'] or not re.search(r'^OK\s*$',log,re.M):
            raise RuntimeError('Test count/result mismatch for '+label)
        total+=spec['tests']
        if version==11:
            run_logged([sys.executable,spec['model'],'--check'],source,logs/'model.log')
            generated.mkdir()
            shutil.copyfile(source/'SUMMARY.json',generated/'FROZEN_SUMMARY.json')
        else:
            if spec['model']:
                run_logged([sys.executable,spec['model'],'--out',str(generated)],source,logs/'model.log')
            run_logged([sys.executable,spec['renderer'],'--out',str(generated),'--video'],source,logs/'render.log')
            videos=list(generated.glob('*.mp4'));html=list(generated.glob('*.html'))
            if len(videos)!=1 or len(html)!=1:raise RuntimeError('Missing/ambiguous generated media for '+label)
            info=json.loads(run_logged(['ffprobe','-v','error','-show_entries','stream=codec_name,width,height','-show_entries','format=duration','-of','json',str(videos[0])],source,logs/'video_info.json'))
            streams=info.get('streams',[])
            if not any(x.get('codec_name')=='h264' and x.get('width')==1280 and x.get('height')==720 for x in streams):
                raise RuntimeError('Unexpected media codec or dimensions for '+label)
            if float(info.get('format',{}).get('duration',0))<=0:
                raise RuntimeError('Empty movie for '+label)
        for rel,digest in source_before.items():
            if metadata(source/rel)['sha256']!=digest:raise RuntimeError('Frozen source mutated: '+rel)
        if version!=11:
            run_logged(['ffmpeg','-v','error','-i',str(videos[0]),'-f','null','-'],source,logs/'video_decode.log')
            shutil.copyfile(videos[0],assets/f'UQCF_GEM_v15_{version}_REPRODUCED.mp4')
            shutil.copyfile(html[0],assets/f'UQCF_GEM_v15_{version}_REPRODUCED.html')
        for p in list(source.rglob('__pycache__')):shutil.rmtree(p)
        (stage/'PROVENANCE.json').write_text(json.dumps({'source_sha':SOURCE_SHA,'builder_sha':producer,
            'kind':'regenerated-output-not-original-conversation-artifact','version':label,'selected_tests_passed':spec['tests'],
            'source_files_sha256':source_before,'environment':environment},indent=2)+'\n')
        package(stage,assets/f'UQCF_GEM_v15_{version}_REPRODUCED_bundle.zip')
        records.append({'version':label,'tests':spec['tests'],'media_generated':version!=11})
    if total!=310:raise RuntimeError('research regression count mismatch')
    subprocess.run(['git','archive','--format=zip','--output='+str(assets/'UQCF_GEM_PINNED_RESEARCH_SOURCE.zip'),SOURCE_SHA,PREFIX],cwd=root,check=True)
    rows=[]
    for p in sorted(assets.iterdir()):
        row=metadata(p);row['matching_original_filenames']=match_original(row,original);rows.append(row)
    report={'source_sha':SOURCE_SHA,'builder_sha':producer,'kind':'reproduced-archive',
        'selected_research_tests_passed':total,'versions':records,'assets':rows,'environment':environment,
        'all_original_conversation_bytes_uploaded':False,'original_manifest_only_is_not_preservation':True}
    (assets/'ARCHIVE_VERIFICATION.json').write_text(json.dumps(report,indent=2)+'\n')
    (assets/'SHA256SUMS.txt').write_text(''.join(metadata(p)['sha256']+'  '+p.name+'\n' for p in sorted(assets.iterdir())))
    (out/'RELEASE_NOTES.md').write_text(release_notes(SOURCE_SHA,producer,total))
    subprocess.run(['git','diff','--exit-code',SOURCE_SHA,'HEAD','--',PREFIX+'/demos',PREFIX+'/v15',PREFIX+'/results'],cwd=root,check=True)
    return report


def validate_url(url: str) -> None:
    parts=urllib.parse.urlsplit(url)
    if parts.scheme!='https' or parts.hostname not in ('api.github.com','uploads.github.com'):
        raise ValueError('Only official GitHub API/upload endpoints are accepted')


def request(url: str,method: str='GET',data=None,content_type='application/json'):
    validate_url(url)
    token=os.environ.get('GH_TOKEN')
    if not token:raise ValueError('Repository-scoped Actions token is required for publication')
    body=None if data is None else data if isinstance(data,bytes) else json.dumps(data).encode()
    req=urllib.request.Request(url,data=body,method=method,headers={
        'Authorization':'Bearer '+token,'Accept':'application/vnd.github+json',
        'X-GitHub-Api-Version':'2022-11-28','Content-Type':content_type,'User-Agent':'UQCF-artifact-archive'})
    with urllib.request.urlopen(req,timeout=180) as response:
        return json.load(response)


def publish(out: Path) -> dict:
    if os.environ.get('GITHUB_REPOSITORY')!=REPOSITORY:raise ValueError('Unexpected target repository')
    run_id=os.environ.get('GITHUB_RUN_ID','');attempt=os.environ.get('GITHUB_RUN_ATTEMPT','1')
    if not run_id.isdigit() or not attempt.isdigit():raise ValueError('Expected GitHub run identity')
    tag=f'uqcf-gem-v15.20-artifacts-{run_id}-a{attempt}'
    base='https://api.github.com/repos/'+REPOSITORY
    release=request(base+'/releases','POST',{'tag_name':tag,'target_commitish':SOURCE_SHA,
        'name':'UQCF-GEM through v15.20 — reproduced artifact archive',
        'body':(out/'RELEASE_NOTES.md').read_text(),'draft':True,'prerelease':True,'make_latest':'false'})
    upload=release['upload_url'].split('{',1)[0];validated=[]
    for path in sorted((out/'assets').iterdir()):
        local=metadata(path)
        remote=request(upload+'?'+urllib.parse.urlencode({'name':path.name}),'POST',path.read_bytes(),mimetypes.guess_type(path.name)[0] or 'application/octet-stream')
        verify_remote(local,remote)
        validated.append({'name':local['name'],'size':local['bytes'],'sha256':local['sha256'],'asset_id':remote['id']})
    remote_assets=request(base+f"/releases/{release['id']}/assets?per_page=100")
    remote_by_name={x['name']:x for x in remote_assets}
    for row in validated:
        verify_remote({'name':row['name'],'bytes':row['size'],'sha256':row['sha256']},remote_by_name[row['name']])
    if len(remote_assets)!=len(validated):raise ValueError('Unexpected remote release asset count')
    public=request(base+f"/releases/{release['id']}",'PATCH',{'draft':False,'make_latest':'false'})
    receipt={'url':public['html_url'],'tag':tag,'release_id':release['id'],'source_sha':SOURCE_SHA,
        'assets_verified':len(validated),'assets':validated,'verification':'GitHub-uploaded size and SHA-256 digest matched for every asset',
        'original_conversation_bundle_uploaded':False}
    (out/'PUBLISH_RECEIPT.json').write_text(json.dumps(receipt,indent=2)+'\n')
    print(json.dumps(receipt,indent=2),flush=True)
    return receipt


def main() -> None:
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('operation',choices=['build','publish'])
    p.add_argument('--root',type=Path,default=Path.cwd());p.add_argument('--out',type=Path,required=True)
    p.add_argument('--original-manifest',type=Path,default=Path(__file__).with_name('ORIGINAL_DELIVERY_MANIFEST.json'))
    a=p.parse_args()
    if a.operation=='build':build(a.root,a.out,a.original_manifest)
    else:publish(a.out.resolve())

if __name__=='__main__':main()
