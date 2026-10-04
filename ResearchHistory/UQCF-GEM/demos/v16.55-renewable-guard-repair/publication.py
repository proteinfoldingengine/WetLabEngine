"""Audit original GitHub archives, complete streams, and fresh reproduction.

Reuse the immutable v16.54 credential-safe artifact download helper read-only.
"""
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import resource
import subprocess
import sys
from campaign import aggregate,serial,dump,digest

HERE=Path(__file__).resolve().parent

def inherited_helpers():
    path=HERE.parent/"v16.54-parent-support-connectivity"/"publication.py"
    gitpath=str(path.relative_to(Path.cwd()));parent=json.loads((HERE/"protocol.json").read_text())["certified_parent"]
    expected=subprocess.check_output(["git","show",parent+":"+gitpath])
    if path.read_bytes()!=expected:raise ValueError("frozen artifact helper modified")
    spec=importlib.util.spec_from_file_location("v1654_archive_helper",path);module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    return module

def main(out):
    if os.environ.get("GITHUB_ACTIONS")!="true":raise RuntimeError("GitHub only")
    resource.setrlimit(resource.RLIMIT_AS,(4294967296,4294967296))
    out=Path(out);out.mkdir(parents=True,exist_ok=True);dump(out/"STATUS.json",dict(status="INCOMPLETE",phase="original archive audit"))
    helper=inherited_helpers();run=os.environ["GITHUB_RUN_ID"];attempt=os.environ["GITHUB_RUN_ATTEMPT"];event=os.environ["GITHUB_SHA"]
    metadata=helper.api("actions/runs/"+run);dump(out/"RUN.json",metadata)
    if metadata["head_sha"]!=event or metadata["path"]!=".github/workflows/v16.55-renewable-guard-validation.yml" or str(metadata["run_attempt"])!=attempt:raise ValueError("actual workflow run binding")
    artifacts=[];page=1
    while True:
        response=helper.api("actions/runs/"+run+"/artifacts?per_page=100&page="+str(page));artifacts.extend(response["artifacts"])
        if len(response["artifacts"])<100:break
        page+=1
    dump(out/"ARTIFACTS.json",artifacts);audit=[]
    def obtain(stem,destination):
        name=stem+"-"+event+"-attempt-"+attempt;items=[item for item in artifacts if item["name"]==name and not item["expired"]]
        if len(items)!=1:raise ValueError("missing/ambiguous original archive: "+name)
        target=out/"archives"/(stem+".zip");folder=helper.download_artifact(items[0],target)
        destination.parent.mkdir(parents=True,exist_ok=True);folder.rename(destination)
        audit.append(dict(id=items[0]["id"],name=name,digest=items[0]["digest"],bytes=items[0]["size_in_bytes"],local_archive=str(target.relative_to(out))))
    for mode in ("primary","reproduction"):
        for shard in range(8):obtain("v1655-"+mode+"-"+str(shard),out/mode/f"shard-{shard}")
        if aggregate(out/mode,out/(mode+"-aggregate")):raise ValueError("complete independent aggregate failed")
    primary=json.loads((out/"primary-aggregate"/"AGGREGATE.json").read_text());repro=json.loads((out/"reproduction-aggregate"/"AGGREGATE.json").read_text())
    if primary!=repro:raise ValueError("fresh deterministic science differs")
    obtain("v1655-inherited-development",out/"inherited"/"inherited-development")
    for shard in range(8):obtain("v1655-inherited-domain-"+str(shard),out/"inherited"/f"inherited-domain-{shard}")
    obtain("v1655-inherited-foundation",out/"inherited"/"inherited-foundation")
    subprocess.run([sys.executable,str(HERE/"inherited_aggregate.py"),str(out/"inherited"),str(out/"INHERITED_AGGREGATE.json")],check=True)
    dump(out/"ORIGINAL_ARCHIVE_AUDIT.json",audit)
    manifest={str(path.relative_to(out)):digest(path) for path in sorted(out.rglob("*")) if path.is_file() and path.name!="STATUS.json"}
    dump(out/"DURABLE_MANIFEST.json",manifest)
    dump(out/"STATUS.json",dict(status="PASS",phase="original archives, full reconstruction, all inherited replay and fresh science equality",scientific_sha=os.environ["SCIENTIFIC_SHA"],workflow_sha=event,run_id=run,attempt=attempt,numbered_certification="PENDING_EXACT_REVIEW_MERGE_AND_ACTUAL_MERGE_AUDIT"))

if __name__=="__main__":main(sys.argv[1])
