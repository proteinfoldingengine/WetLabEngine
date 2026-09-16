#!/usr/bin/env python3
"""Publish only a verified rewrite, with atomic per-reference leases."""
import base64, hashlib, json, os, pathlib, subprocess, sys
from cleanup_history import run
BASE=pathlib.Path(__file__).resolve().parent
REPO='https://github.com/proteinfoldingengine/WetLabEngine.git'
BRANCH='maintenance/withdrawn-lab-history-cleanup'
FILTER_SHA='67447413e273fc76809289111748870b6f6072f08b17efe94863a92d810b7d94'
def remote_refs():
    raw=subprocess.check_output(['git','ls-remote','--refs',REPO,'refs/heads/*','refs/tags/*']).decode()
    return {ref:sha for sha,ref in (line.split() for line in raw.splitlines())}
def main():
    assert os.environ['GITHUB_REPOSITORY']=='proteinfoldingengine/WetLabEngine'
    assert os.environ['GITHUB_REF']=='refs/heads/'+BRANCH
    expected=json.loads((BASE/'expected_refs.json').read_text())
    expected['refs/heads/'+BRANCH]=os.environ['GITHUB_SHA']
    assert remote_refs()==expected,'Remote refs changed since private archive; aborting'
    filter_tool=pathlib.Path('filter-deps/git_filter_repo.py').resolve()
    assert hashlib.sha256(filter_tool.read_bytes()).hexdigest()==FILTER_SHA,'Filter tool checksum mismatch'
    mirror=pathlib.Path('cleanup-mirror.git').resolve()
    subprocess.run(['git','clone','--mirror',REPO,str(mirror)],check=True)
    initial=subprocess.check_output(['git','--git-dir='+str(mirror),'for-each-ref','--format=%(objectname) %(refname)','refs/heads','refs/tags']).decode()
    assert {ref:sha for sha,ref in (line.split() for line in initial.splitlines())}==expected,'Refs changed during clone'
    report=run(mirror,filter_tool,pathlib.Path('cleanup-verification'))
    # Require exactly the original branches/tags plus this maintenance branch.
    newrefs={r:s for r,s in report['new_refs'].items() if r.startswith(('refs/heads/','refs/tags/'))}
    assert set(newrefs)==set(expected),'Unexpected public reference set'
    assert remote_refs()==expected,'Concurrent repository changes; aborting'
    # Use only this job's normal repository token, without printing it.
    token=os.environ['GH_TOKEN']
    header='AUTHORIZATION: basic '+base64.b64encode(('x-access-token:'+token).encode()).decode()
    env=os.environ.copy();env.update(GIT_CONFIG_COUNT='1',GIT_CONFIG_KEY_0='http.https://github.com/.extraheader',GIT_CONFIG_VALUE_0=header)
    leases=['--force-with-lease='+r+':'+expected[r] for r in sorted(expected)]
    updates=[newrefs[r]+':'+r for r in sorted(expected)]
    command=['git','--git-dir='+str(mirror),'push','--atomic',*leases,REPO,*updates]
    subprocess.run(command[:4]+['--dry-run']+command[4:],env=env,check=True)
    assert remote_refs()==expected,'Concurrent repository changes before push; aborting'
    subprocess.run(command,env=env,check=True)
    assert remote_refs()==newrefs,'Post-push reference verification failed'
    print('Published and verified '+str(len(newrefs))+' branches/tags; retired paths absent; unrelated trees unchanged.',flush=True)
if __name__=='__main__':main()
