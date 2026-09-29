"""Checksum-bound preservation and fresh verification of v16.22 evidence."""
from pathlib import Path
import argparse
import hashlib
import io
import json
import lzma
import os
import subprocess
import zipfile

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[3]
REL=str(HERE.relative_to(ROOT))
REPO='proteinfoldingengine/WetLabEngine'


def need(ok,message):
    if not ok:raise RuntimeError(message)


def sha(b):return hashlib.sha256(b).hexdigest()


def gh(path):
    return subprocess.check_output(['gh','api','--allow-escape-sequences',f'repos/{REPO}/'+path],cwd=ROOT)


def verify_published():
    for line in (HERE/'PUBLICATION_SHA256SUMS').read_text().splitlines():
        digest,name=line.split('  ',1)
        need(sha((HERE/name).read_bytes())==digest,'publication checksum: '+name)
    print('Every durable publication checksum verified.')


def stage():
    e=HERE/'evidence';e.mkdir(exist_ok=True)
    archives=e/'archives';archives.mkdir(exist_ok=True)
    history=e/'history';history.mkdir(exist_ok=True)
    records=json.loads((HERE/'RUN_REGISTRY.json').read_text());decoded={};metadata=[]
    for r in records:
        raw=gh(f"actions/artifacts/{r['artifact']}/zip")
        need(sha(raw)==r['digest'],'original ZIP hash '+r['name'])
        (archives/(r['name']+'.zip')).write_bytes(raw)
        with zipfile.ZipFile(io.BytesIO(raw)) as z:
            need(z.testzip() is None,'ZIP CRC')
            members={n:z.read(n) for n in z.namelist()}
        for line in members['SHA256SUMS'].decode().splitlines():
            digest,name=line.split('  ',1);need(sha(members[name])==digest,'original member hash')
        runraw=gh(f"actions/runs/{r['run']}");run=json.loads(runraw)
        jobsraw=gh(f"actions/runs/{r['run']}/jobs");jobs=json.loads(jobsraw)['jobs']
        need(run['head_sha']==r['sha'] and run['status']=='completed' and run['conclusion']==r['conclusion'],'run binding')
        need(run['run_attempt']==1 and len(jobs)==1,'attempt/job coverage')
        need(jobs[0]['conclusion']==r['conclusion'],'job conclusion')
        (history/(r['name']+'-run.json')).write_bytes(runraw)
        (history/(r['name']+'-jobs.json')).write_bytes(jobsraw)
        (history/(r['name']+'-job.log')).write_bytes(gh(f"actions/jobs/{jobs[0]['id']}/logs"))
        metadata.append({**r,'job':jobs[0]['id'],'attempt':run['run_attempt']})
        need(f"Ran {r['tests']} tests" in members['test.log'].decode(),'test count binding')
        decoded[r['name']]=members
    need('FAILED (failures=18)' in decoded['wiring-red']['test.log'].decode(),'wiring RED reason')
    need('FAILED (failures=2)' in decoded['schema-red']['test.log'].decode(),'schema RED reason')
    original=decoded['final-green']
    need(original['certificates.json.xz']==decoded['initial-green']['certificates.json.xz'],'schema repair changed scientific certificate')
    for name,data in original.items():
        need(Path(name).name==name,'unexpected artifact path')
        (e/('ORIGINAL_SHA256SUMS' if name=='SHA256SUMS' else name)).write_bytes(data)
    for name,n in [('test.log',20),('parent.log',15),('v1621.log',22)]:
        text=original[name].decode();need(f'Ran {n} tests' in text and '\nOK\n' in text,'scientific test record')
    need(all(line.split('\t')[1]=='0' for line in original['exit_codes.tsv'].decode().splitlines()),'scientific exit code')
    with zipfile.ZipFile(io.BytesIO(original['source.zip'])) as z:
        for name in ['engine.py','verify.py','test_gate.py','test_schema.py','PROOFS.md','TYPE_LEDGER.md','PREREGISTRATION.md']:
            need(z.read(REL+'/'+name)==(HERE/name).read_bytes(),'scientific source changed after execution: '+name)
    commands=[]
    def execute(name,cmd,cwd):
        p=subprocess.run(cmd,cwd=cwd,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
        (e/('publication-'+name+'.log')).write_bytes(p.stdout)
        commands.append({'name':name,'command':cmd,'exit_code':p.returncode})
        need(p.returncode==0,'fresh publication command failed: '+name)
    execute('tests',['python','-m','unittest','discover','-v'],HERE)
    execute('parent',['python','-m','unittest','-v','test_pruning_consistency_audit'],HERE.parent/'v15.56-response-selector-obstruction')
    execute('v1621',['python','tests/test_fcv.py'],ROOT/'ResearchHistory/UQCF-GEM/foundational-closure-verification')
    execute('producer',['python','engine.py'],HERE)
    execute('verifier',['python','verify.py'],HERE)
    for name in ['certificates.json.xz','VERIFICATION.json','rejections.json']:
        need((e/name).read_bytes()==original[name],'fresh scientific output not byte-identical: '+name)
    raw=lzma.decompress(original['certificates.json.xz'])
    verification=json.loads(original['VERIFICATION.json'])
    record={'version':'16.22','scientific_execution_sha':records[-1]['sha'],'original_runs':metadata,
            'publication_workflow_head':os.environ['GITHUB_SHA'],'publication_run':os.environ['GITHUB_RUN_ID'],
            'publication_attempt':os.environ['GITHUB_RUN_ATTEMPT'],'fresh_commands':commands,
            'fresh_scientific_bytes_equal':True,'raw_certificate_sha256':sha(raw),'raw_certificate_bytes':len(raw),
            'xz_certificate_sha256':sha(original['certificates.json.xz']),
            'verification_sha256':sha(original['VERIFICATION.json']),'verification':verification,
            'test_counts':{'new':20,'inherited_exact':15,'v1621':22},
            'review':'self-reviewed; algorithmically independent verification, no separate reviewer',
            'scope':'research/v16.22-response-selection-closure; no main merge'}
    (HERE/'PUBLICATION_EVIDENCE.json').write_text(json.dumps(record,indent=2,sort_keys=True)+'\n')
    parent_names=['foundational-closure-verification/TYPE_LEDGER.md','foundational-closure-verification/PROOFS.md',
                  'demos/v15.56-response-selector-obstruction/pruning_consistency_audit.py']
    binding={'parent_commit':'6a9fe4450c4a711a4c0d3b2170e7e31eff550ee6',
             'files':{n:sha((ROOT/'ResearchHistory/UQCF-GEM'/n).read_bytes()) for n in parent_names}}
    (HERE/'PARENT_BINDING.json').write_text(json.dumps(binding,indent=2,sort_keys=True)+'\n')
    files=[p for p in HERE.rglob('*') if p.is_file() and '__pycache__' not in p.parts and p.name!='PUBLICATION_SHA256SUMS']
    (HERE/'PUBLICATION_SHA256SUMS').write_text(''.join(sha(p.read_bytes())+'  '+str(p.relative_to(HERE))+'\n' for p in sorted(files)))
    verify_published()


if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--stage',action='store_true');ap.add_argument('--verify',action='store_true');a=ap.parse_args()
    if a.stage:stage()
    if a.verify:verify_published()
