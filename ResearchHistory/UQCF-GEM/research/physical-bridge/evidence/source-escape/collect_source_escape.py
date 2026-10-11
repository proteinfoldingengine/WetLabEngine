#!/usr/bin/env python3
"""Preserve and audit one pinned, already completed scientific run. No science rerun."""
import argparse
import json
import os
from pathlib import Path
import shutil
import subprocess
import time
import urllib.error
import urllib.request
from audit_helpers import require, sha256, git_blob, check_zip, check_review, check_inputs, check_tests, check_log

REPO = 'proteinfoldingengine/WetLabEngine'
BRANCH = 'research/uqcf-overlapping-guard-exchange'
BASE = 'ResearchHistory/UQCF-GEM/research/physical-bridge'
EVENT = '5091874b16ca70d13f2b62c99e46d6817df9df07'
RUN = 38105740578
CERT = 'fe42f879d864a8138b3220d1312b73cdf59aacf16b0e16736158a80efa68d778'
CANON = 'a2eb36d2e233796dee29ef89e5b657d0d501846c42a305bd222096b3f56582e9'
ARTIFACTS = {
 'verification': (11689277555, 22895312, 'b58b8cce52fa58168ece321dd9ec7c996161dfed3e904adbd263eb0cc21c5528', 114370783282),
 'fresh-reproduction': (11689212787, 22895716, '1d4d129d2321071448c55cfd447c0efe46e2322bdf177c299fdf60bced23767b', 114371636556),
 'mathematical-review': (11690216565, 3970, '31cee3dd9517ed28e4ef37ba5237bb80d4fbcf00219cb1393a76b8b6e6a88d4e', 114372111206),
 'publication-audit': (11690157041, 4768, '48e6d9b235c67a79db82f60a6f99e8c15f6dede42e6b93f2fb7a07c13ac117dd', 114372249396),
}
SOURCES = ['COUPLED_C3_SOURCE_ESCAPE_RESULT.md','COUPLED_C3_SOURCE_ESCAPE_SCOPE.md','COUPLED_C3_SOURCE_ESCAPE_ANALYTICAL_REVIEW.md','COUPLED_C3_SOURCE_ESCAPE_REPORT.md','COUPLED_C3_SOURCE_ESCAPE_REVIEW.md','COUPLED_C3_COVER_STATIC_CLOSEOUT.md','COUPLED_C3_NONUNIFORM_RESERVE_CLOSEOUT.md','COUPLED_C3_ORIGIN_REENTRY_DECISION.md','COUPLED_C3_COVERAGE_ORIGIN_SCREEN.md','COUPLED_C3_AUTONOMY_CLOSEOUT.md','source_escape/producer.py','source_escape/independent.py','source_escape/test_escape.py','source_escape/PLAN.md']
SUITES = {'contracts.log':42, **{'inherited_'+k+'.log':n for k,n in {'cover_static':35,'nonuniform_reserve':34,'weak_trace':32,'fingerprint_lock':33,'private_cover':26,'moving_cover':28,'saturated_handover':26,'slack_handover':24,'handover_graph':20,'anchored_release':20,'local_progress':17,'capacity_gap':20,'saturated_transfer':22,'label_release':26,'footprint':22,'fixed_family':28}.items()}}
VMEM = set(SUITES) | {'certificate.json','certificate.json.identities.jsonl.gz','certificate.sha256','counts.json','frozen_proof_scope.md','identities.sha256','independent.json','independent.log','independent.py','producer.py','provenance.txt','red.log','test_escape.py'}
MEMBERS = {'verification':VMEM, 'fresh-reproduction':VMEM|{'fresh_independent.json'}, 'mathematical-review':{'manifest.json','review.txt'}, 'publication-audit':{'source_escape_gate.json','source_escape_publication/manifest.json','source_escape_publication/review.txt'}}
COUNTS = {'candidates':2570928,'distinct_states':183904,'escape_sources':6688,'hidden_checks':501629984,'routes':109440,'slice_occurrences':427968,'sources':7360,'vacancy_candidates':54912}


def write_json(path, data):
 path.parent.mkdir(parents=True, exist_ok=True)
 path.write_text(json.dumps(data, indent=2, sort_keys=True)+'\n', encoding='utf-8')


class SafeRedirect(urllib.request.HTTPRedirectHandler):
 def redirect_request(self, req, fp, code, msg, headers, newurl):
  new = super().redirect_request(req, fp, code, msg, headers, newurl)
  if new is not None:
   from urllib.parse import urlparse
   if urlparse(newurl).netloc != 'api.github.com':
    new.remove_header('Authorization')
  return new


def collect(out):
 require(not out.exists(), 'Evidence destination already exists; reconcile rather than overwrite')
 out.mkdir(parents=True)
 token = os.environ.get('GH_TOKEN','')
 require(bool(token), 'Missing archive API authorization')
 opener = urllib.request.build_opener(SafeRedirect())
 attempts = []
 def get(endpoint):
  for attempt in range(1,4):
   try:
    req=urllib.request.Request('https://api.github.com/repos/'+REPO+'/'+endpoint,headers={'Authorization':'Bearer '+token,'Accept':'application/vnd.github+json','X-GitHub-Api-Version':'2022-11-28'})
    with opener.open(req, timeout=180) as response: data=response.read()
    attempts.append({'endpoint':endpoint,'attempt':attempt,'result':'SUCCESS'})
    write_json(out/'transport_attempts.json',attempts)
    return data
   except (urllib.error.HTTPError,urllib.error.URLError,TimeoutError) as exc:
    status=getattr(exc,'code',None)
    attempts.append({'endpoint':endpoint,'attempt':attempt,'result':type(exc).__name__,'http_status':status})
    write_json(out/'transport_attempts.json',attempts)
    if status not in (None,429,500,502,503,504) or attempt==3:
     raise RuntimeError('Archive transport failed; sanitized attempts retained') from None
    time.sleep(2**attempt)
 for filename, endpoint in [('run.json',f'actions/runs/{RUN}'),('jobs.json',f'actions/runs/{RUN}/jobs?per_page=100'),('artifacts.json',f'actions/runs/{RUN}/artifacts?per_page=100')]:
  (out/filename).write_bytes(get(endpoint))
 for role,(artifact_id,size,digest,job_id) in ARTIFACTS.items():
  (out/('original-'+role+'.zip')).write_bytes(get(f'actions/artifacts/{artifact_id}/zip'))
  (out/(role+'-job.log')).write_bytes(get(f'actions/jobs/{job_id}/logs'))
 subprocess.run(['git','fetch','--no-tags','--depth=1','origin',EVENT],check=True)
 require(subprocess.check_output(['git','rev-parse',EVENT],text=True).strip()==EVENT,'Pinned science missing')
 for name in SOURCES:
  path=out/'scientific_inputs'/name;path.parent.mkdir(parents=True,exist_ok=True)
  path.write_bytes(subprocess.check_output(['git','show',EVENT+':'+BASE+'/'+name]))
 for name in ['source_escape/initial_test_syntax_failure.log','evidence/source-escape-local/archive_failure.json','evidence/source-escape-local/independent_attempt1_failure.log']:
  p=out/'retained_failure'/Path(name).name;p.parent.mkdir(exist_ok=True)
  p.write_bytes(subprocess.check_output(['git','show',EVENT+':'+BASE+'/'+name]))
 for name in ['audit_helpers.py','collect_source_escape.py','test_archive.py','red.log']:
  shutil.copyfile(Path(__file__).with_name(name),out/name)
 with (out/'audit_controls.log').open('w') as log:
  subprocess.run(['python3','-m','unittest','-v','test_archive.py'],cwd=out,stdout=log,stderr=subprocess.STDOUT,check=True)
 with __import__('zipfile').ZipFile(out/'original-verification.zip') as z:
  good=z.read('certificate.json.identities.jsonl.gz')
 damaged=good[:42126659]
 require(sha256(damaged)=='5bb1111754a4f9a37819bc7f929514a7ea7048c7135250f6c6010f65dd1e3329','Documented damaged-prefix reconstruction mismatch')
 (out/'retained_failure/reconstructed-damaged-companion.jsonl.gz').write_bytes(damaged)
 (out/'retained_failure/RECONSTRUCTION.md').write_text('The damaged bytes are reconstructed from the exact prefix of the completed original Actions companion, not independently downloaded as the initial damaged file. Length 42,126,659 and SHA256 5bb1111754a4f9a37819bc7f929514a7ea7048c7135250f6c6010f65dd1e3329 match the pre-existing immutable failure record. The missing 32,304 bytes and original failure remain explicit; the cause of truncation is not established.\n')
 for source,target,member in [('mathematical-review','mathematical-review.txt','review.txt'),('mathematical-review','mathematical-manifest.json','manifest.json'),('publication-audit','publication-review.txt','source_escape_publication/review.txt'),('publication-audit','publication-manifest.json','source_escape_publication/manifest.json'),('publication-audit','publication-gate.json','source_escape_gate.json')]:
  with __import__('zipfile').ZipFile(out/('original-'+source+'.zip')) as z:(out/target).write_bytes(z.read(member))


def audit(out):
 run=json.loads((out/'run.json').read_text())
 require(run['id']==RUN and run['head_sha']==EVENT and run['head_branch']==BRANCH,'Wrong original run')
 require(run['status']=='completed' and run['conclusion']=='success','Original run incomplete')
 jobs=json.loads((out/'jobs.json').read_text())
 require(jobs['total_count']==4 and len(jobs['jobs'])==4,'Incomplete job universe')
 byname={j['name']:j for j in jobs['jobs']}
 require(set(byname)==set(ARTIFACTS),'Wrong job roles')
 artifacts=json.loads((out/'artifacts.json').read_text())
 require(artifacts['total_count']==4 and len(artifacts['artifacts'])==4,'Incomplete artifact universe')
 byid={a['id']:a for a in artifacts['artifacts']}
 require(set(byid)=={a[0] for a in ARTIFACTS.values()},'Artifact identity mismatch')
 data={}; archives={}; logs={}
 for role,(artifact_id,size,digest,job_id) in ARTIFACTS.items():
  job=byname[role];meta=byid[artifact_id]
  require(job['id']==job_id and job['run_id']==RUN and job['head_sha']==EVENT,'Wrong job binding')
  require(job['status']=='completed' and job['conclusion']=='success','Unsuccessful job')
  require(all(s['status']=='completed' and s['conclusion']=='success' for s in job['steps']),'Incomplete or adverse job step')
  require(meta['name']=='c3-source-escape-'+role and meta['size_in_bytes']==size and meta['digest']=='sha256:'+digest,'Wrong artifact metadata')
  require(meta['workflow_run']['id']==RUN and meta['workflow_run']['head_sha']==EVENT,'Artifact event mismatch')
  raw=(out/('original-'+role+'.zip')).read_bytes()
  require(len(raw)==size and sha256(raw)==digest,'Original ZIP digest mismatch')
  data[role]=check_zip(raw,MEMBERS[role])
  archives[role]={'artifact_id':artifact_id,'bytes':size,'sha256':digest,'git_blob_sha1':git_blob(raw),'members':{n:sha256(b) for n,b in data[role].items()}}
  log=(out/(role+'-job.log')).read_bytes();text=log.decode('utf-8-sig')
  check_log(text,EVENT,digest)
  require('Complete job name: '+role in text and str(artifact_id) in text,'Wrong log role or artifact')
  logs[role]={'job_id':job_id,'url':f'https://api.github.com/repos/{REPO}/actions/jobs/{job_id}/logs','sha256':sha256(log),'bytes':len(log)}
 v=data['verification'];f=data['fresh-reproduction'];m=data['mathematical-review'];p=data['publication-audit']
 require(all(v[n]==f[n] for n in v),'Reproduction member mismatch')
 require(sha256(v['certificate.json'])==CERT and len(v['certificate.json'])==530342,'Certificate mismatch')
 require(sha256(v['certificate.json.identities.jsonl.gz'])==CANON and len(v['certificate.json.identities.jsonl.gz'])==42158963,'Canonical companion mismatch')
 require(json.loads(v['certificate.json'])['counts']==COUNTS,'Unexpected census')
 for n in ('independent.json','fresh_independent.json'):
  obj=json.loads(f[n]);require(obj['accepted'] is True and obj['counts']==COUNTS and obj['canonical_sha256']==CANON and obj['certificate_sha256']==CERT,'Independent reconstruction mismatch')
 for name,n in SUITES.items():check_tests(v[name].decode(),n)
 require(sum(SUITES.values())==455,'Scientific test total mismatch')
 require(v['provenance.txt'].decode()==f'scientific_sha={EVENT}\nworkflow_sha={EVENT}\n','Incorrect source provenance')
 require('ModuleNotFoundError' in v['red.log'].decode(),'Missing original RED')
 source={n:(out/'scientific_inputs'/n).read_bytes() for n in SOURCES}
 require(source['COUPLED_C3_SOURCE_ESCAPE_RESULT.md']==v['frozen_proof_scope.md'],'Frozen proof mismatch')
 for n in ('producer.py','independent.py','test_escape.py'):require(source['source_escape/'+n]==v[n],'Reviewed code mismatch')
 mm=json.loads(m['manifest.json']);pm=json.loads(p['source_escape_publication/manifest.json'])
 check_review(m['review.txt'],mm,EVENT);check_review(p['source_escape_publication/review.txt'],pm,EVENT)
 actual={**source,**{'EVIDENCE/'+n:b for n,b in f.items()}}
 require(check_inputs(mm['input_sha256'],actual)==45,'Wrong mathematical input count')
 actual.update({'MATH_REVIEW/'+n:b for n,b in m.items()});actual['PUBLICATION_GATE']=p['source_escape_gate.json']
 require(check_inputs(pm['input_sha256'],actual)==48,'Wrong publication input count')
 require(mm['response_sha256']=='b1969182aa903208a3d86d781d03fb8b582d1edcde5226e49004899ea7edb854','Unpinned mathematical response')
 require(pm['response_sha256']=='012366d307625708f42147556af160450691ebe31bb19d6b6c9c2f650232415c','Unpinned publication response')
 gate=json.loads(p['source_escape_gate.json'])
 require(gate['status']=='PASS' and gate['scientific_commit']==EVENT and gate['verified_review_inputs']==45 and gate['certificate_reproduced_byte_exact'] is True and gate['independent_full_reconstruction'] is True and gate['response_sha256']==mm['response_sha256'],'Publication gate mismatch')
 failure=json.loads((out/'retained_failure/archive_failure.json').read_text())
 damaged=(out/'retained_failure/reconstructed-damaged-companion.jsonl.gz').read_bytes()
 require(len(damaged)==failure['original_size'] and sha256(damaged)==failure['original_sha256'] and v['certificate.json.identities.jsonl.gz'].startswith(damaged),'Retained failure mismatch')
 check_tests((out/'audit_controls.log').read_text(),9)
 summary={'status':'PASS_ORIGINAL_EVIDENCE_AUDIT_NOT_NEW_SCIENCE','scientific_commit':EVENT,'run_id':RUN,'test_counts':SUITES,'scientific_tests':455,'audit_tests':9,'audit_rejecting_controls':8,'counts':COUNTS,'archives':archives,'logs':logs,'math_inputs':45,'publication_inputs':48,'math_response_sha256':mm['response_sha256'],'publication_response_sha256':pm['response_sha256'],'damaged_prefix':'Reconstructed exact bytes matched pre-existing immutable failure record; not an independently downloaded initial damaged file','limitations':['First source escape only; X does not imply a subsequent vacancy','No optimal cost, full component classification, native record, enforcement, successor selection or progress derivation','Broad C3/general C4-C6 remain OPEN; no physical or full-stack closure']}
 write_json(out/'audit_summary.json',summary)
 return summary


if __name__=='__main__':
 parser=argparse.ArgumentParser();parser.add_argument('directory',type=Path);parser.add_argument('--collect',action='store_true');args=parser.parse_args()
 if args.collect:collect(args.directory)
 result=audit(args.directory)
 if args.collect:
  (args.directory/'README.md').write_text('# First-source-escape original evidence\n\nThis archive authenticates the already completed run38105740578 at5091874b16ca70d13f2b62c99e46d6817df9df07. No scientific or Gemini campaign is rerun here. Four original ZIPs and four complete raw job logs are retained. Audit tests are separate from455scientific tests. The damaged prior companion is explicitly reconstructed to its previously recorded exact digest, not relabelled as an independently downloaded original. Scope: first escape, not later vacancy reachability or native origin/progress. Final closeout and immutable publication readback remain separate gates.\n')
  manifest={p.relative_to(args.directory).as_posix():{'bytes':p.stat().st_size,'sha256':sha256(p.read_bytes()),'git_blob_sha1':git_blob(p.read_bytes())} for p in sorted(args.directory.rglob('*')) if p.is_file() and '__pycache__' not in p.parts}
  write_json(args.directory/'readback_manifest.json',{'scientific_commit':EVENT,'run_id':RUN,'files':manifest})
 print(json.dumps({'status':result['status'],'scientific_tests':455,'audit_tests':9,'original_archives':4,'full_job_logs':4,'math_inputs':45,'publication_inputs':48},sort_keys=True))
