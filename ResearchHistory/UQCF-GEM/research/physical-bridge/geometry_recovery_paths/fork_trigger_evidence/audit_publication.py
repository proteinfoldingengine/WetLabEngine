"""Verify the four original CI archives and the scientific and external review dispositions."""
import base64
from hashlib import sha1, sha256
import json
import lzma
from pathlib import Path
import re
import sys
from zipfile import ZipFile

HERE=Path(__file__).resolve().parent
SCI=HERE.parent
sys.path.insert(0,str(SCI))
from fixed_pair_evidence.audit_publication import manifest, need, object_

OUTPUTS=("fork_trigger_universe.json.xz","fork_trigger_caller.json.xz","fork_trigger_certificate.json")


def checked_science(z, head, prefix):
    manifest(z)
    name="science-head.txt" if prefix=="replay" else "workflow-head.txt"
    need(z.read(name).decode().strip()==head,"exact science head")
    outputs={}
    for file in OUTPUTS:
        data=z.read(file)
        need(data==(SCI/file).read_bytes(),"reproduced "+file)
        outputs[file]=sha256(data).hexdigest()
    proof=object_(z,"fork_trigger_certificate.json")
    need(sha256(lzma.decompress(z.read(OUTPUTS[0]))).hexdigest()==proof["raw_sha256"],"primary raw bytes")
    native=object_(z,"independent.log")
    need(native==dict(status="PASS",rejecting_controls=11,**proof["bare"]) and
         native["source_arms"]==168 and native["complete_histories"]==912 and native["with_fork_trigger"]==456 and
         native["reading_before_trigger"]==184 and native["distinct_mass_pairs"]==64,"scientific readback")
    builder=object_(z,"caller_independent.log")
    need(builder==dict(status="PASS",rejecting_controls=5,arms=168,deep_readded=140,different_receiver_roots=12,
                       matched_pairs=84,receiver_changes=70,target_runs=504),"historical caller readback")
    return outputs


def main():
    info=json.loads((HERE/"run.json").read_bytes())
    head=info["head"]
    need(head==info["workflow_head"] and info["inherited"]=="e61d5b0e827f7b412824ad46021e2ad6cc6f7875","revisions")
    jobs={j["name"]:j["conclusion"] for j in info["jobs"]}
    need(all(jobs[j]=="success" for j in ("replay","foundational-regression","publication")),"scientific jobs")
    need({a["name"] for a in info["archives"]}=={"fork-trigger-"+s for s in ("replay","review","publication","foundation")}
         and len(info["archives"])==4,"archives")
    for a in info["archives"]:
        data=(HERE/(a["name"]+".zip")).read_bytes()
        need(len(data)==a["size"] and "sha256:"+sha256(data).hexdigest()==a["digest"],a["name"])
    with ZipFile(HERE/"fork-trigger-replay.zip") as z:
        hashes=checked_science(z,head,"replay")
        need(z.read("historical-head.txt").decode().strip()==info["inherited"],"historical pin")
        for f in z.namelist():
            if f.endswith((".md",".py")):
                need(z.read(f)==(SCI/f).read_bytes(),"archived method "+f)
    with ZipFile(HERE/"fork-trigger-foundation.zip") as z:
        manifest(z)
        v=object_(z,"VERIFICATION.json")
        need(z.read("workflow-head.txt").decode().strip()==head and z.read("inherited-head.txt").decode().strip()==info["inherited"],"inherited workflow")
        need(v["all_valid"] and v["coverage"]["instances"]==21 and object_(z,"TEST_RECEIPT.json")["passed"],"21 certificates")
        need(sha256(lzma.decompress(z.read("certificates.json.xz"))).hexdigest()==
             "21357bdc79429f9d4214024b125e75693609a2538a08a57037978b191ab432c6","foundational certificate bytes")
        for f,count in (("tests.log",22),("parent-tests.log",15),("historical.log",2)):
            log=z.read(f).decode()
            need(re.search(r"Ran "+str(count)+r" tests? in ",log) and "\nOK" in log,f)
        foundation=z.read("VERIFICATION.json")
    with ZipFile(HERE/"fork-trigger-publication.zip") as z:
        need(checked_science(z,head,"publication")==hashes and z.read("VERIFICATION.json")==foundation,"fresh checkout")
        audit_raw=z.read("publication_audit.json")
        audit=json.loads(audit_raw)
    with ZipFile(HERE/"fork-trigger-review.zip") as z:
        prompt,raw=z.read("prompt.txt"),z.read("request.json")
        request=json.loads(raw)
        need(request["contents"][0]["parts"][0]["text"].encode()==prompt and request["generationConfig"]["maxOutputTokens"]==6144,"request")
        need(audit["checkout_sha"]==audit["workflow_sha"]==head and audit["run_id"]==str(info["run_id"]) and
             audit["attempt"]==str(info["attempt"]) and audit["prompt_sha256"]==sha256(prompt).hexdigest()
             and audit["request_sha256"]==sha256(raw).hexdigest(),"review identity")
        if "provider_error.json" in z.namelist():
            marker="provider_error.json"
            error=object_(z,marker)
            need(audit==dict(audit="SCIENTIFIC_REPLAY_ONLY",**error) and error["stage"] in ("generateContent","model_metadata")
                 and error["external_review"]=="NO_MODEL_VERDICT" and 400<=error["http_status"]<600 and
                 not set(z.namelist())&{"response.json","receipt.json","review.txt"} and
                 jobs["argument-review"]==info["conclusion"]=="failure","original provider disposition")
            status="PENDING_HTTP_"+str(error["http_status"])
        else:
            marker="response.json"
            reply=object_(z,marker)
            answer="\n".join(part["text"] for part in reply["candidates"][0]["content"]["parts"]
                             if "text" in part and not part.get("thought")).strip()
            need(z.read("review.txt")==answer.encode() and sha256(z.read(marker)).hexdigest()==audit["response_sha256"]
                 and audit==dict(audit=audit["audit"],**object_(z,"receipt.json")),"original review")
            verdict=json.loads(answer)
            if audit["audit"]=="PASS":
                need(verdict["verdict"]=="ACCEPTED" and verdict["native_bridge_status"]=="OPEN" and
                     all(verdict[k]==[] for k in ("findings","counterexamples","missing_assumptions")) and
                     jobs["argument-review"]==info["conclusion"]=="success","acceptance")
                status="ACCEPTED"
            else:
                need(jobs["argument-review"]==info["conclusion"]=="failure","adjudication needed")
                status="REVIEW_REQUIRES_ADJUDICATION"
        if "model_metadata.json" in z.namelist():
            model=object_(z,"model_metadata.json")
            need(model["name"]=="models/"+audit["model_requested"] and "generateContent" in model["supportedGenerationMethods"],"model")
        echoed=dict(line.split("_B64=",1) for line in (HERE/"publication_readback.log").read_text().splitlines())
        need(set(echoed)=={marker,"publication_audit.json"} and base64.b64decode(echoed[marker],validate=True)==z.read(marker)
             and base64.b64decode(echoed["publication_audit.json"],validate=True)==audit_raw,"publication log echo")
    old=lzma.decompress((HERE/"initial/verifier.py.xz").read_bytes())
    need(sha1(f"blob {len(old)}\0".encode()+old).hexdigest()=="8fabc6c7c7dcd579d058adbdf66a09ddf16b297c" and
         "TypeError: unhashable type: 'list'" in (HERE/"initial/verifier.log").read_text(),"first local checker trace")
    return dict(run_id=info["run_id"],science_head=head,scientific_replay="PASS",fresh_publication="PASS",
                external_review=status,foundation=21,outputs_sha256=hashes,complete_histories=912,triggered=456,
                strict_leads=184,caller_target_runs=504,caller_separated_pairs=12)


if __name__=="__main__":
    print(json.dumps(main(),indent=2,sort_keys=True))
