"""Check the original provider failure and the complete scientific publication separately."""
import base64
from hashlib import sha256
import json
import lzma
from pathlib import Path
import re
import sys
from zipfile import ZipFile

HERE=Path(__file__).resolve().parent
SCI=HERE.parent
sys.path.insert(0,str(SCI))
from audit_command_archives import check, check_manifest


def read(z,n):
    return json.loads(z.read(n))


def need(test,msg):
    if not test:
        raise ValueError(msg)


def validate_binaries(directory,info):
    for item in info["archives"]:
        data=(directory/(item["name"]+".zip")).read_bytes()
        need(len(data)==item["size"] and "sha256:"+sha256(data).hexdigest()==item["digest"],item["name"])


def scientific(directory,info):
    with ZipFile(directory/"cover-return-replay.zip") as z:
        check_manifest(z)
        for label,k in (("science-head.txt","head"),("historical-head.txt","inherited")):
            need(z.read(label).decode().strip()==info[k],label)
        for name in ("cover_return_universe.json.xz","cover_return_certificate.json"):
            need(z.read(name)==(SCI/name).read_bytes(),name)
        native=read(z,"independent.log")
        need(native["status"]=="PASS" and native["complete_arms"]==2112 and native["budget_arms"]==81
             and native["bounded_graphs"]==10 and native["rejecting_controls"]==12,"independent reconstruction")
    with ZipFile(directory/"cover-return-foundation.zip") as z:
        check_manifest(z)
        need(z.read("workflow-head.txt").decode().strip()==info["head"] and
             z.read("inherited-head.txt").decode().strip()==info["inherited"],"foundation identity")
        v=read(z,"VERIFICATION.json")
        need(v["all_valid"] and v["coverage"]["instances"]==21 and read(z,"TEST_RECEIPT.json")["passed"],"foundation")
        need(sha256(lzma.decompress(z.read("certificates.json.xz"))).hexdigest()==
             "21357bdc79429f9d4214024b125e75693609a2538a08a57037978b191ab432c6","foundation bytes")
        for f,n in (("tests.log",22),("parent-tests.log",15),("historical.log",2)):
            need(re.search(r"Ran "+str(n)+r" tests? in ",z.read(f).decode()),"inherited suite")


def unavailable(directory,info,original):
    with ZipFile(directory/"cover-return-review.zip") as z:
        metadata=read(z,"model_metadata.json")
        need(metadata["name"]=="models/gemini-3.1-pro-preview","metadata")
        need(not set(z.namelist())&{"response.json","review.txt","receipt.json"},"ambiguous external verdict")
        request=read(z,"request.json")
        prompt=z.read("prompt.txt")
        need(request["contents"][0]["parts"][0]["text"].encode()==prompt,"original prompt")
        need(request["generationConfig"]["maxOutputTokens"]==(32768 if original else 6144),"requested ceiling")
        need(len(prompt)==(137938 if original else 35726),"prompt bytes")
        if original:
            need("urllib.error.HTTPError: HTTP Error 402: Payment Required" in (directory/"provider.log").read_text(),
                 "first provider log")
            return dict(run=info["run_id"],head=info["head"],http_status=402,external_review="NO_MODEL_VERDICT",
                        prompt_sha256=sha256(prompt).hexdigest(),request_sha256=sha256(z.read("request.json")).hexdigest())
        err=read(z,"provider_error.json")
        need(err["http_status"]==402 and err["stage"]=="generateContent" and err["external_review"]=="NO_MODEL_VERDICT",
             "specific provider error")
        need(err["checkout_sha"]==err["workflow_sha"]==info["head"] and str(info["run_id"])==err["run_id"] and
             err["prompt_sha256"]==sha256(prompt).hexdigest() and
             err["request_sha256"]==sha256(z.read("request.json")).hexdigest(),"frozen-request binding")
        err_raw=z.read("provider_error.json")
    with ZipFile(directory/"cover-return-publication.zip") as z:
        check_manifest(z)
        need(z.read("workflow-head.txt").decode().strip()==info["head"],"fresh checkout")
        for name in ("cover_return_universe.json.xz","cover_return_certificate.json"):
            need(z.read(name)==(SCI/name).read_bytes(),name)
        need(read(z,"independent.log")["status"]=="PASS" and read(z,"VERIFICATION.json")["coverage"]["instances"]==21,
             "fresh replay")
        audit=z.read("publication_audit.json")
        need(json.loads(audit)==dict(audit="SCIENTIFIC_REPLAY_ONLY",**err),"adjudication")
        markers=dict(row.split("_B64=",1) for row in (directory/"publication_readback.log").read_text().splitlines())
        need(set(markers)=={"provider_error.json","publication_audit.json"},"publication trace")
        for key,data in (("provider_error.json",err_raw),("publication_audit.json",audit)):
            need(base64.b64decode(markers[key],validate=True)==data,"fresh status echo")
    return dict(run=info["run_id"],head=info["head"],http_status=402,external_review="NO_MODEL_VERDICT",
                prompt_sha256=err["prompt_sha256"],request_sha256=err["request_sha256"])


def main():
    first=HERE/"first"
    raw=json.loads((first/"run.json").read_bytes())
    need(raw["conclusion"]=="failure" and {r["name"]:r["conclusion"] for r in raw["jobs"]}==
         {"replay":"success","argument-review":"failure","foundational-regression":"success","publication":"skipped"},"first jobs")
    need({r["name"] for r in raw["archives"]}=={"cover-return-"+s for s in ("replay","review","foundation")},"initial artifacts")
    validate_binaries(first,raw)
    scientific(first,raw)
    initial=unavailable(first,raw,True)
    latest=json.loads((HERE/"run.json").read_bytes())
    need(latest["inherited"]==raw["inherited"] and latest["previous_science_head"]==raw["head"],"research binding")
    need({r["name"] for r in latest["archives"]}=={"cover-return-"+s for s in ("replay","review","foundation","publication")},
         "published artifacts")
    validate_binaries(HERE,latest)
    scientific(HERE,latest)
    jobs={r["name"]:r["conclusion"] for r in latest["jobs"]}
    if latest["conclusion"]=="success":
        outcome=check(HERE,SCI)
        status="ACCEPTED"
    else:
        need(latest["conclusion"]=="failure" and jobs=={"replay":"success","argument-review":"failure",
             "foundational-regression":"success","publication":"success"},"scientific publication with review pending")
        outcome=unavailable(HERE,latest,False)
        status="PENDING_HTTP_402"
    return dict(scientific_replay="PASS",fresh_publication="PASS",external_review=status,
                primary_arms=2112,budget_arms=81,foundational_instances=21,first_attempt=initial,second_attempt=outcome)


if __name__=="__main__":
    if not __debug__:raise RuntimeError("Run with assertions enabled")
    print(json.dumps(main(),indent=2,sort_keys=True))
