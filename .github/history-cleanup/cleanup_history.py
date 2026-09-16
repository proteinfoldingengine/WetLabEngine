#!/usr/bin/env python3
"""Narrow, verified rewrite of retired WetLabEngine material."""
import argparse, hashlib, json, os, pathlib, subprocess, sys
REMOVED = ['ManuscriptBuilder.py','ManuscriptBuilderMultipleAI.py','UnifiedAuditEngine.py','SCHEMA.md','RunProteinFoldingAudit.ipynb']
PREFIXES = ['Labs/MECP2/','Labs/p53/']
ROOT_NOTE = '''# WetLabEngine

## Status update — September 16, 2026

Further testing did not support the previously reported p53 and MECP2 (Rett syndrome) findings. The lab materials and associated audit and manuscript-generation tools have been withdrawn. They should not be relied on as validation of those findings.

Previous versions are retained in a private archive. Some binary lab payloads were already unavailable from Git LFS; the archive records those gaps.

Separate research archives remain available in this repository.
'''
LAB_NOTE = '''# Lab findings update

September 16, 2026

Further testing did not support the previously reported p53 and MECP2 (Rett syndrome) findings. These lab materials have been withdrawn and should not be relied on as validated scientific results.

Previous versions are retained in a private archive. Some binary lab payloads were already unavailable from Git LFS; the archive records those gaps.
'''
def git(repo,*args):
    return subprocess.check_output(['git','--git-dir='+str(repo),*args])
def refs(repo):
    return dict(line.split(' ',1)[::-1] for line in git(repo,'for-each-ref','--format=%(objectname) %(refname)').decode().splitlines())
def stable_tree(repo,commit):
    out={}
    for entry in git(repo,'ls-tree','-z',commit).split(b'\0'):
        if not entry: continue
        attrs,name=entry.split(b'\t',1); name=name.decode()
        if name not in REMOVED+['README.md','Labs']:out[name]=attrs.decode()
    # Preserve any other Labs files exactly, except the withdrawal notice.
    for entry in git(repo,'ls-tree','-rz',commit,'--','Labs/').split(b'\0'):
        if not entry:continue
        attrs,name=entry.split(b'\t',1);name=name.decode()
        if name != 'Labs/README.md' and not any(name.startswith(p) for p in PREFIXES):out[name]=attrs.decode()
    return out

def run(repo,filter_tool,outdir):
    repo=pathlib.Path(repo).resolve(); outdir=pathlib.Path(outdir).resolve();outdir.mkdir(exist_ok=True,parents=True)
    oldrefs=refs(repo)
    commits=git(repo,'rev-list','--all').decode().splitlines()
    before={c:stable_tree(repo,c) for c in commits}
    parents={c:git(repo,'show','-s','--format=%P',c).decode().strip().split() for c in commits}
    metadata={c:git(repo,'show','-s','--format=%an%x00%ae%x00%at%x00%cn%x00%ce%x00%ct%x00%B',c) for c in commits}
    callback=outdir/'file_callback.py'
    callback.write_text('if filename == b"README.md":\n    blob_id = value.insert_file_with_contents('+repr(ROOT_NOTE.encode())+')\nelif filename == b"Labs/README.md":\n    blob_id = value.insert_file_with_contents('+repr(LAB_NOTE.encode())+')\nreturn filename, mode, blob_id\n')
    cmd=[sys.executable,str(pathlib.Path(filter_tool).resolve()),'--force','--no-gc','--prune-empty','never','--prune-degenerate','never','--preserve-commit-hashes','--preserve-commit-encoding','--replace-refs','delete-no-add','--invert-paths']
    for path in REMOVED+PREFIXES:cmd+=['--path',path]
    cmd+=['--file-info-callback',str(callback)]
    subprocess.run(cmd,cwd=repo,check=True)
    mapping=dict(line.split() for line in (repo/'filter-repo/commit-map').read_text().splitlines()[1:])
    assert set(mapping)==set(commits), 'Commit set changed'
    assert all(int(n,16) for n in mapping.values()), 'Commit was pruned'
    assert len(set(mapping.values()))==len(commits),'Commit identities collapsed'
    for old,new in mapping.items():
        assert stable_tree(repo,new)==before[old], 'Unrelated tree changed: '+old
        assert git(repo,'show','-s','--format=%P',new).decode().strip().split()==[mapping[p] for p in parents[old]],'Parent topology changed'
        assert git(repo,'show','-s','--format=%an%x00%ae%x00%at%x00%cn%x00%ce%x00%ct%x00%B',new)==metadata[old],'Commit metadata changed'
        assert git(repo,'show',new+':README.md')==ROOT_NOTE.encode(),'Notice absent'
    newrefs=refs(repo)
    assert newrefs=={r:mapping[s] for r,s in oldrefs.items()},'References changed unexpectedly'
    assert not git(repo,'rev-list','--objects','--all','--',*(REMOVED+PREFIXES)).strip(),'Retired paths still reachable'
    assert git(repo,'show','refs/heads/main:Labs/README.md')==LAB_NOTE.encode()
    report={'verified_commits':len(commits),'verified_refs':len(oldrefs),'unrelated_trees_unchanged':True,'parent_topology_unchanged':True,'retired_paths_reachable':False,'old_refs':oldrefs,'new_refs':newrefs}
    (outdir/'VERIFICATION.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items() if k not in ['old_refs','new_refs']}),flush=True)
    return report
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('repo');p.add_argument('filter_tool');p.add_argument('output');a=p.parse_args();run(a.repo,a.filter_tool,a.output)
