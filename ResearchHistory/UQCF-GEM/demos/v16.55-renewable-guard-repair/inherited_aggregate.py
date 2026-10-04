"""Read-only independent aggregation of the full inherited v16.54 replay.

Run as a separate process so frozen imports retain their original namespaces.
"""
from collections import Counter
import gzip
import hashlib
from itertools import zip_longest
import json
import os
from pathlib import Path
import resource
import sys

BASE=Path(__file__).resolve().parent.parent/"v16.54-parent-support-connectivity"
sys.path.insert(0,str(BASE))
from verifier import reconstruct_cases,verify_record
from campaign import validate_campaign_summary
from publication import check_partition,check_required_diagnostics,_checked_source,_diagnose,verify_inherited_package,digest_file

def serial(value):return json.dumps(value,sort_keys=True,separators=(",",":"),allow_nan=False)
def records(path):
    with gzip.open(path,"rt") as stream:
        for line in stream:yield json.loads(line)

def main(root,out):
    if os.environ.get("GITHUB_ACTIONS")!="true":raise RuntimeError("GitHub only")
    resource.setrlimit(resource.RLIMIT_AS,(4294967296,4294967296))
    root=Path(root);out=Path(out);head=os.environ["SCIENTIFIC_SHA"];freezes=[];diagnostics=Counter();manifests={};expected=iter(reconstruct_cases(json.loads((BASE/"protocol.json").read_text())));whole=hashlib.sha256();total=0
    for shard in range(8):
        folder=root/f"inherited-domain-{shard}";_checked_source(folder,head);science=folder/"scientific"
        provenance=json.loads((folder/"PROVENANCE.json").read_text())
        for key,value in dict(scientific_sha=head,workflow_sha=os.environ["GITHUB_SHA"],run_id=os.environ["GITHUB_RUN_ID"],attempt=os.environ["GITHUB_RUN_ATTEMPT"],shard=shard,scope="all").items():
            if str(provenance.get(key))!=str(value):raise ValueError("inherited shard provenance mismatch")
        manifest=json.loads((science/"MANIFEST.json").read_text())
        if set(manifest)!={"CASES.jsonl.gz","RECORDS.jsonl.gz","DOMAIN_FREEZE.json","SUMMARY.json"}:raise ValueError("inherited science membership mismatch")
        if any(digest_file(science/name)!=value for name,value in manifest.items()):raise ValueError("inherited science corruption")
        summary=json.loads((science/"SUMMARY.json").read_text());freeze=json.loads((science/"DOMAIN_FREEZE.json").read_text());freezes.append(freeze)
        if validate_campaign_summary({**summary,**provenance}):raise ValueError("inherited unfinished summary")
        identity_hash=hashlib.sha256();record_hash=hashlib.sha256();count=0
        for case,record in zip_longest(records(science/"CASES.jsonl.gz"),records(science/"RECORDS.jsonl.gz")):
            wanted=next(expected,None)
            if case is None or record is None or wanted is None or case!=wanted or record["identity"]!=wanted["identity"]:raise ValueError("inherited full identity/input mismatch")
            errors=verify_record(case,record)
            if errors:raise ValueError("inherited independent path rejection: "+repr(errors))
            whole.update((serial(case)+"\n").encode());identity_hash.update((serial(case["identity"])+"\n").encode());record_hash.update((serial(record)+"\n").encode());count+=1;total+=1;diagnostics.update(_diagnose(case,record))
        if count!=summary["checked"] or count!=freeze["stop"]-freeze["start"] or identity_hash.hexdigest()!=freeze["identity_sha256"] or record_hash.hexdigest()!=summary["record_sha256"]:raise ValueError("inherited full stream mismatch")
        manifests.update({str(shard)+"/"+name:value for name,value in manifest.items()})
    if next(expected,None) is not None or total!=freezes[0]["total"] or whole.hexdigest()!=freezes[0]["whole_universe_sha256"]:raise ValueError("inherited omitted domain")
    if check_partition(freezes) or check_required_diagnostics(diagnostics):raise ValueError("inherited partition/diagnostics mismatch")
    foundation=root/"inherited-foundation";verify_inherited_package(foundation,head)
    manifest=json.loads((foundation/"MANIFEST.json").read_text())
    actual={str(path.relative_to(foundation)):digest_file(path) for path in foundation.rglob("*") if path.is_file() and path!=foundation/"MANIFEST.json"}
    if manifest!=actual:raise ValueError("inherited package manifest mismatch")
    metrics=json.loads((foundation/"METRICS.json").read_text());meta=json.loads((foundation/"METADATA.json").read_text())
    if metrics["inherited_tests"]!=1150 or metrics["new_controls"]!=43 or not metrics["all_commands_passed"]:raise ValueError("inherited complete stack not green")
    if meta["head"]!=head or meta["workflow_sha"]!=head or meta["trigger_sha"]!=head or str(meta["run_id"])!=os.environ["GITHUB_RUN_ID"]:raise ValueError("inherited actual checkout provenance mismatch")
    out.parent.mkdir(parents=True,exist_ok=True);out.write_text(serial(dict(status="PASS",total=total,diagnostics=dict(diagnostics),manifests=manifests))+"\n")

if __name__=="__main__":main(sys.argv[1],sys.argv[2])
