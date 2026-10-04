"""GitHub-only streaming execution of the complete prospective identity domain.

Eight predetermined lexicographically contiguous intervals, no sampling.
"""
from collections import Counter
import gzip
import hashlib
import json
import os
from pathlib import Path
import resource
import subprocess
import sys
import traceback
from itertools import zip_longest

HERE=Path(__file__).resolve().parent
MAX_VERTICES=10000000
MAX_BYTES=1073741824
REQUIRED=("leveling_donor_recipient_root","leveling_greedy_vacancy_transfers","temporarily_inexact_entries","saturated_cycles","repeated_cycle_colors","restored_cycle_boundaries","maximum_layer_conversion","multiple_patch_outside_witness","noncompact_exact_endpoint","mixed_grade_completion","sufficient_bound_refusal","zero_patch_restoration","zero_capacity_grade","native_clearance")

def serial(value):return json.dumps(value,sort_keys=True,separators=(",",":"),allow_nan=False)
def dump(path,value):Path(path).write_text(serial(value)+"\n")
def digest(path):
    h=hashlib.sha256()
    with Path(path).open("rb") as stream:
        for chunk in iter(lambda:stream.read(1048576),b""):h.update(chunk)
    return h.hexdigest()
def science_count(value):
    """Count every serialized primitive tuple, including repeated metadata legs."""
    if isinstance(value,dict):
        total=0
        for key,item in value.items():
            if key in ("preliminary","final","cycle_path","upper_entry","vertices"):
                total+=len(item)
            elif key in ("pair_witnesses","edges","assignment","progress","events","phases","steps","clearances"):continue
            else:total+=science_count(item)
        return total
    if isinstance(value,list):
        # A root tuple is a list of support arrays, whose items are integers.
        if value and all(isinstance(row,list) and all(type(x) is int for x in row) for row in value):return 1
        return sum(science_count(x) for x in value)
    return 0

def diagnostic(case,record):
    """Counts are derived from independently accepted actual metadata events."""
    from verifier import cover
    counts=Counter();status=record["status"];meta=record.get("meta",{})
    if status=="SUFFICIENT_BOUND_NOT_MET":counts["sufficient_bound_refusal"]+=1
    if status!="PATH":return counts
    method=case.get("parent_method",case["method"])
    if method=="X15N":
        for leg in meta["leveling"].values():
            counts["leveling_donor_recipient_root"]+=len(leg["events"])
            counts["leveling_greedy_vacancy_transfers"]+=len(leg["events"])
            counts["temporarily_inexact_entries"]+=len(cover(case["k"],leg["vertices"][-1]))!=4
        counts["saturated_cycles"]+=len(meta["cycles"])
        counts["restored_cycle_boundaries"]+=len(meta["cycles"])
        counts["repeated_cycle_colors"]+=sum(len({edge[2] for edge in event["edges"]})<len(event["edges"]) for event in meta["cycles"])
    counts["maximum_layer_conversion"]+=len(meta.get("conversion",[]))
    if method=="X32" and len(case["U"])>1:counts["multiple_patch_outside_witness"]+=1
    if method=="X33":
        counts["mixed_grade_completion"]+=len(set(case["floors"]))>1
        counts["noncompact_exact_endpoint"]+=any(len(row)>floor for row,floor in zip(case["C"],case["floors"]))
    if case["identity"][0]=="R4":
        typ=case["identity"][1]["type"]
        if typ=="ZERO_PATCH":counts["zero_patch_restoration"]+=1
        if typ=="ZERO_CAPACITY_GRADE":counts["zero_capacity_grade"]+=1
    if case["method"]=="NATIVE":counts["native_clearance"]+=len(record["nested"]["clearances"])
    return counts

def bind(out):
    if os.environ.get("GITHUB_ACTIONS")!="true":raise RuntimeError("all scientific execution is GitHub-only")
    resource.setrlimit(resource.RLIMIT_AS,(4294967296,4294967296))
    actual=subprocess.check_output(["git","rev-parse","HEAD"],text=True).strip()
    if actual!=os.environ["SCIENTIFIC_SHA"] or actual!=os.environ["GITHUB_SHA"] or actual!=os.environ["GITHUB_WORKFLOW_SHA"]:raise ValueError("actual scientific/workflow source mismatch")
    prereg="891470cfc817f26d9721f96278b2c0f8652c3fdf"
    if os.environ["PREREGISTRATION_SHA"]!=prereg:raise ValueError("unapproved preregistration")
    for name in ("protocol.json","PROSPECTIVE_EXECUTION_PROTOCOL.md","APPROVAL_AND_PREREGISTRATION.md","INHERITED_SOURCE_INVENTORY.json"):
        path=HERE/name;gitpath=str(path.relative_to(Path.cwd()))
        if path.read_bytes()!=subprocess.check_output(["git","show",prereg+":"+gitpath]):raise ValueError("prospectively frozen prerequisite changed: "+name)
    protocol=json.loads((HERE/"protocol.json").read_text())
    raw=(HERE/"PROSPECTIVE_EXECUTION_PROTOCOL.md").read_bytes()
    if hashlib.sha256(raw).hexdigest()!=protocol["approved_protocol_sha256"]:raise ValueError("approved protocol modified")
    inventory=json.loads((HERE/"INHERITED_SOURCE_INVENTORY.json").read_text())
    # inventory format is checked explicitly, no silent fallback.
    paths=inventory["git_blobs"]
    listing=subprocess.check_output(["git","ls-tree","-r",actual],text=True).splitlines()
    current_blobs={line.split("\t",1)[1]:line.split("\t",1)[0].split()[2] for line in listing}
    for name,item in protocol["proofs"].items():
        path=HERE/"analytical"/name;gitpath=str(path.relative_to(Path.cwd()))
        if current_blobs.get(gitpath)!=item["git_blob"] or path.read_bytes()!=subprocess.check_output(["git","show",prereg+":"+gitpath]):raise ValueError("accepted analytical proof/review changed: "+name)
    for path,item in paths.items():
        expected=item if isinstance(item,str) else item["git_blob"]
        current=current_blobs.get(path)
        if current!=expected:raise ValueError("inherited source changed: "+path)
    provenance=dict(workflow_sha=os.environ["GITHUB_SHA"],scientific_sha=actual,preregistration_sha=os.environ["PREREGISTRATION_SHA"],run_id=os.environ["GITHUB_RUN_ID"],attempt=os.environ["GITHUB_RUN_ATTEMPT"],approved_protocol_sha256=hashlib.sha256(raw).hexdigest())
    dump(out/"PROVENANCE.json",provenance)
    source={}
    for path in sorted([*HERE.glob("*.py"),*HERE.glob("*.md"),*HERE.glob("*.json"),*HERE.glob("tests/*.py"),*HERE.glob("analytical/*.md")]):
        if path.name.endswith("REQUEST.json"):continue
        relative=str(path.relative_to(HERE));data=path.read_bytes()
        if subprocess.check_output(["git","show",actual+":"+str(path.relative_to(Path.cwd()))])!=data:raise ValueError("untracked executing source")
        source[relative]=hashlib.sha256(data).hexdigest();destination=out/"source"/relative;destination.parent.mkdir(parents=True,exist_ok=True);destination.write_bytes(data)
    dump(out/"SOURCE_MANIFEST.json",source)
    return provenance

class Stream:
    def __init__(self,path):
        self.raw=Path(path).open("wb");self.zipped=gzip.GzipFile(filename="",mode="wb",fileobj=self.raw,mtime=0);self.count=0
    def write(self,value):self.zipped.write((serial(value)+"\n").encode());self.count+=1
    def close(self):self.zipped.close();self.raw.close()

def ordered_domain(builder):
    values=sorted(builder(),key=lambda case:serial(case["identity"]))
    if len({serial(case["identity"]) for case in values})!=len(values):raise ValueError("duplicate formula identity")
    return values

def run_shard(shard,out):
    from universe import generate_cases
    from verifier import reconstruct_cases,verify_universe,verify_record
    from mechanisms import produce,ResourceLimit
    out=Path(out);out.mkdir(parents=True,exist_ok=True);dump(out/"SUMMARY.json",dict(status="INCOMPLETE",reason="initialization or execution not finished",shard=shard));bind(out)
    if not 0<=shard<8:raise ValueError("invalid declared shard")
    producer=ordered_domain(generate_cases);independent=ordered_domain(reconstruct_cases)
    if producer!=independent:raise ValueError("independent identity/full-input reconstruction mismatch")
    total=len(independent);start=total*shard//8;stop=total*(shard+1)//8
    whole_hash=hashlib.sha256((serial([case["identity"] for case in independent])+"\n").encode()).hexdigest()
    identities=Stream(out/"identities.jsonl.gz");records=Stream(out/"records.jsonl.gz")
    summary=dict(status="PASS",shard=shard,shards=8,total=total,start=start,stop=stop,whole_universe_sha256=whole_hash,expected=stop-start,checked=0,serialized_vertices=0,diagnostics={},refusals={},common_degree_greedy_transfers=0,strict_slack_X15S_exercised=False)
    dump(out/"DOMAIN_FREEZE.json",dict(shard=shard,shards=8,total=total,start=start,stop=stop,whole_universe_sha256=whole_hash,first=independent[start]["identity"],last=independent[stop-1]["identity"]))
    dump(out/"SUMMARY.json",dict(summary,status="INCOMPLETE",reason="execution not finished"))
    counts=Counter();refusals=Counter();current=None
    try:
        for current in independent[start:stop]:
            dump(out/"CURRENT_ATTEMPT.json",dict(case=current,ordinal=start+summary["checked"],phase="production-and-independent-verification"))
            record=produce(current);errors=verify_record(current,record)
            count=science_count(record)
            if count>1000000:raise ResourceLimit("serialized per-identity primitive vertices, including metadata/native, exceeded")
            summary["serialized_vertices"]+=count
            if summary["serialized_vertices"]>MAX_VERTICES:raise ResourceLimit("whole campaign bound exceeded within shard")
            entry=dict(case=current,record=record)
            records.write(entry);identities.write(current["identity"])
            records.zipped.flush();identities.zipped.flush()
            if records.raw.tell()+identities.raw.tell()>MAX_BYTES:raise ResourceLimit("compressed deterministic science bound exceeded within shard")
            if errors:
                dump(out/"FIRST_FAILURE.json",dict(case=current,record=record,errors=errors));summary["status"]="FAIL";break
            summary["checked"]+=1;counts.update(diagnostic(current,record))
            if record["status"]!="PATH":refusals[record["status"]]+=1
    except ResourceLimit as error:
        summary["status"]="INCOMPLETE";dump(out/"FIRST_FAILURE.json",dict(case=current,reason=str(error)))
    except MemoryError:
        summary["status"]="INCOMPLETE";dump(out/"FIRST_FAILURE.json",dict(case=current,reason="approved memory bound exhausted"))
    except Exception as error:
        summary["status"]="FAIL";dump(out/"FIRST_FAILURE.json",dict(case=current,reason=repr(error),traceback=traceback.format_exc()))
    finally:records.close();identities.close()
    summary["diagnostics"]=dict(counts);summary["refusals"]=dict(refusals)
    summary["compressed_bytes"]=0
    while True:
        dump(out/"SUMMARY.json",summary)
        manifest={name:digest(out/name) for name in ("records.jsonl.gz","identities.jsonl.gz","SUMMARY.json","DOMAIN_FREEZE.json")}
        dump(out/"SCIENCE_MANIFEST.json",manifest)
        actual_bytes=sum((out/name).stat().st_size for name in list(manifest)+["SCIENCE_MANIFEST.json"])
        if actual_bytes==summary["compressed_bytes"]:break
        summary["compressed_bytes"]=actual_bytes
        if actual_bytes>MAX_BYTES:summary["status"]="INCOMPLETE"
    print(serial(summary),flush=True)
    return 0 if summary["status"]=="PASS" and summary["checked"]==summary["expected"] else 1

def read_records(directory,name):
    with gzip.open(Path(directory)/name,"rt") as stream:
        for line in stream:yield json.loads(line)

def aggregate(root,out):
    from verifier import reconstruct_cases,verify_universe,verify_manifest,verify_diagnostics,verify_record,verify_provenance
    if os.environ.get("GITHUB_ACTIONS")!="true":raise RuntimeError("GitHub only")
    resource.setrlimit(resource.RLIMIT_AS,(4294967296,4294967296))
    root=Path(root);out=Path(out);out.mkdir(parents=True,exist_ok=True)
    expected=ordered_domain(reconstruct_cases);errors=[];identities=[];counts=Counter();vertices=0;compressed=0;manifests={}
    whole_hash=hashlib.sha256((serial([case["identity"] for case in expected])+"\n").encode()).hexdigest()
    head=os.environ["SCIENTIFIC_SHA"];source_expected={}
    for path in sorted([*HERE.glob("*.py"),*HERE.glob("*.md"),*HERE.glob("*.json"),*HERE.glob("tests/*.py"),*HERE.glob("analytical/*.md")]):
        if path.name.endswith("REQUEST.json"):continue
        source_expected[str(path.relative_to(HERE))]=hashlib.sha256(path.read_bytes()).hexdigest()
    for shard in range(8):
        directory=root/f"shard-{shard}";summary=json.loads((directory/"SUMMARY.json").read_text());manifest=json.loads((directory/"SCIENCE_MANIFEST.json").read_text())
        if set(manifest)!={"records.jsonl.gz","identities.jsonl.gz","SUMMARY.json","DOMAIN_FREEZE.json"}:errors.append("wrong science inventory")
        errors+=verify_manifest({name:(directory/name).read_bytes() for name in manifest},manifest)
        provenance=json.loads((directory/"PROVENANCE.json").read_text())
        protocol=json.loads((HERE/"protocol.json").read_text())
        errors+=verify_provenance(provenance,dict(scientific_sha=head,workflow_sha=os.environ["GITHUB_SHA"],run_id=os.environ["GITHUB_RUN_ID"],attempt=os.environ["GITHUB_RUN_ATTEMPT"],preregistration_sha=os.environ["PREREGISTRATION_SHA"],approved_protocol_sha256=protocol["approved_protocol_sha256"]))
        source_recorded=json.loads((directory/"SOURCE_MANIFEST.json").read_text())
        source_files={str(p.relative_to(directory/"source")):p.read_bytes() for p in (directory/"source").rglob("*") if p.is_file()}
        if source_recorded!=source_expected:errors.append("executing source inventory mismatch")
        errors+=verify_manifest(source_files,source_expected)
        if summary["status"]!="PASS" or summary["checked"]!=summary["expected"]:errors.append("unfinished shard "+str(shard))
        if (summary["shard"],summary["shards"],summary["total"],summary["start"],summary["stop"])!=(shard,8,len(expected),len(expected)*shard//8,len(expected)*(shard+1)//8):errors.append("wrong interval "+str(shard))
        start=len(expected)*shard//8;stop=len(expected)*(shard+1)//8
        freeze_expected=dict(shard=shard,shards=8,total=len(expected),start=start,stop=stop,whole_universe_sha256=whole_hash,first=expected[start]["identity"],last=expected[stop-1]["identity"])
        if json.loads((directory/"DOMAIN_FREEZE.json").read_text())!=freeze_expected or summary["whole_universe_sha256"]!=whole_hash:errors.append("wrong full domain freeze")
        actual=list(read_records(directory,"identities.jsonl.gz"));errors+=verify_universe([c["identity"] for c in expected[summary["start"]:summary["stop"]]],actual)
        # Input membership is independently reconstructed; equal totals cannot substitute inputs.
        shardcounts=Counter();shardvertices=0;shardrefusals=Counter();checked=0
        for entry,case in zip_longest(read_records(directory,"records.jsonl.gz"),expected[summary["start"]:summary["stop"]]):
            if entry is None or case is None:errors.append("record cardinality mismatch");continue
            if entry["case"]!=case or entry["record"]["identity"]!=case["identity"]:errors.append("substituted full input");continue
            errors+=verify_record(case,entry["record"])
            shardcounts.update(diagnostic(case,entry["record"]));v=science_count(entry["record"]);shardvertices+=v
            if v>1000000:errors.append("serialized identity resource bound")
            if entry["record"]["status"]!="PATH":shardrefusals[entry["record"]["status"]]+=1
            checked+=1
        shardbytes=sum((directory/name).stat().st_size for name in list(manifest)+["SCIENCE_MANIFEST.json"])
        if checked!=summary["checked"] or dict(shardcounts)!=summary["diagnostics"] or dict(shardrefusals)!=summary["refusals"] or shardvertices!=summary["serialized_vertices"] or shardbytes!=summary["compressed_bytes"]:errors.append("fabricated shard counters")
        if summary.get("common_degree_greedy_transfers")!=0 or summary.get("strict_slack_X15S_exercised") is not False:errors.append("fabricated strict-slack witness")
        identities.extend(actual);counts.update(shardcounts);vertices+=shardvertices;compressed+=shardbytes;manifests[str(shard)]=manifest
    errors+=verify_universe([c["identity"] for c in expected],identities)
    missing=verify_diagnostics(counts,REQUIRED)
    if vertices>MAX_VERTICES or compressed>MAX_BYTES:missing.append("whole campaign resource bound")
    result=dict(status="FAIL" if errors else "INCOMPLETE" if missing else "PASS",expected=len(expected),checked=len(identities),errors=errors,incomplete=missing,diagnostics=dict(counts),serialized_vertices=vertices,compressed_bytes=compressed,shard_manifests=manifests,common_degree_greedy_transfers=0,strict_slack_X15S_exercised=False)
    dump(out/"AGGREGATE.json",result);print(serial(result),flush=True)
    return 0 if result["status"]=="PASS" else 1

if __name__=="__main__":
    mode=sys.argv[1]
    if mode=="shard":raise SystemExit(run_shard(int(sys.argv[2]),sys.argv[3]))
    if mode=="aggregate":raise SystemExit(aggregate(sys.argv[2],sys.argv[3]))
    raise SystemExit("unknown command")
