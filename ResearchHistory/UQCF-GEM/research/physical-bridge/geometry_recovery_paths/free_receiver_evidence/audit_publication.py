"""Check the original workflow ZIPs, raw scientific outputs, foundation and external status."""
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
from fixed_pair_evidence.audit_publication import need, manifest, object_

HIST="e61d5b0e827f7b412824ad46021e2ad6cc6f7875"
OUTPUTS=("free_receiver_words.json.xz","free_receiver_language.json","free_receiver_chart12.json.xz",
         "free_receiver_spectra.json","free_receiver_caller.json.xz","free_receiver_call_check.json",
         "free_receiver_threshold.json.xz","free_receiver_lengths.json")


def check_science(z,head,replay):
    manifest(z)
    marker="science-head.txt" if replay else "workflow-head.txt"
    need(z.read(marker).decode().strip()==head,"scientific revision")
    if replay:
        need(z.read("historical-head.txt").decode().strip()==HIST,"historical revision")
        for name in z.namelist():
            if name.endswith((".py",".md")):
                need(z.read(name)==(SCI/name).read_bytes(),"archived method "+name)
    hashes={}
    for name in OUTPUTS:
        raw=z.read(name)
        need(raw==(SCI/name).read_bytes(),"fresh scientific output "+name)
        hashes[name]=sha256(raw).hexdigest()
    language=object_(z,"free_receiver_language.json")
    expected=dict(cover_states=1042,families=5820,complete_visible_words=52646,fixed_visible_preparations=954,controls=10)
    need(language==expected,"complete visible words")
    spectrum=object_(z,"free_receiver_spectra.json")
    need([(r["mode"],r["cut"],r["minimum"],r["maximum"],r["optional"]) for r in spectrum]==
         [("original",662,242,3176,1305),("original",718,242,3176,1305),
          ("balanced",662,242,3176,1305),("balanced",718,242,3175,1304)],"chart 12 spectra")
    need(all(r["max_multiplicity"]==1 and r["distinct"]==r["maximum"]-241 for r in spectrum),"integer coverage")
    proof=json.loads(lzma.decompress(z.read("free_receiver_chart12.json.xz")))
    need(len(proof["cases"])==4 and len(proof["polynomials"])==2,"full polynomial outputs")
    for case in proof["cases"]:
        pol=proof["polynomials"][case["polynomial"]]
        need(sum(n for _,n in pol)==2**case["optional"] and pol[0][0]==case["minimum"]["root"]
             and pol[-1][0]==case["maximum"]["root"],"all multiplicities and witnesses")
    threshold=object_(z,"free_receiver_lengths.json")
    need(threshold==dict(shortest_increment_word=931,common_unit_prefix=930,first_positive_root=1173,
              root_after_common_prefix=1172,initial_unit_atoms=932,remaining_unit_atoms=1,next_nonunit=1174,
              rejecting_controls=5),"minimal numerical word")
    caller=object_(z,"free_receiver_call_check.json")
    need(caller==dict(arms=72,pairs=36,source_selected=0,representatives=12,graph_states=2989,files=278,
              named_calls=9,materialized_states=672,numeric_fork_grades=[8,6],stub_grades=[9,13],
              rejecting_controls=6),"original single-state campaign")
    required_logs=("check_words","verify_words","check_chart12","verify_chart12","check_caller","verify_caller",
                   "check_threshold","verify_threshold")
    need(all(z.read(name+".log").strip() for name in required_logs),"execution receipts")
    return hashes


def main():
    info=json.loads((HERE/"run.json").read_bytes())
    head=info["head"]
    need(head==info["workflow_head"] and info["inherited"]==HIST,"workflow and historical revisions")
    jobs={x["name"]:x["conclusion"] for x in info["jobs"]}
    need(all(jobs[x]=="success" for x in ("replay","foundational-regression","publication")),"scientific jobs")
    names={"free-receiver-"+key for key in ("replay","foundation","publication","review")}
    need({x["name"] for x in info["archives"]}==names and len(info["archives"])==4,"original archives")
    for row in info["archives"]:
        path=HERE/(row["name"]+".zip")
        original=path.read_bytes()
        need(len(original)==row["size"] and "sha256:"+sha256(original).hexdigest()==row["digest"],row["name"])
        with ZipFile(path) as z:
            need(z.testzip() is None,"original ZIP integrity")
    with ZipFile(HERE/"free-receiver-replay.zip") as z:
        hashes=check_science(z,head,True)
    with ZipFile(HERE/"free-receiver-foundation.zip") as z:
        manifest(z)
        need(z.read("workflow-head.txt").decode().strip()==head and z.read("inherited-head.txt").decode().strip()==HIST,
             "foundation head")
        v=object_(z,"VERIFICATION.json")
        need(v["all_valid"] and v["coverage"]["instances"]==21 and object_(z,"TEST_RECEIPT.json")["passed"],
             "21 foundational checks")
        need(sha256(lzma.decompress(z.read("certificates.json.xz"))).hexdigest()==
             "21357bdc79429f9d4214024b125e75693609a2538a08a57037978b191ab432c6","foundation bytes")
        for name,n in (("tests.log",22),("parent-tests.log",15),("historical.log",2)):
            text=z.read(name).decode()
            need(re.search(r"Ran "+str(n)+r" tests? in ",text) and "\nOK" in text,name)
        foundation=z.read("VERIFICATION.json")
    with ZipFile(HERE/"free-receiver-publication.zip") as z:
        need(check_science(z,head,False)==hashes and z.read("VERIFICATION.json")==foundation,"fresh checkout")
        raw=z.read("publication_audit.json")
        audit=json.loads(raw)
    with ZipFile(HERE/"free-receiver-review.zip") as z:
        question,request=z.read("prompt.txt"),z.read("request.json")
        wire=json.loads(request)
        need(wire["contents"][0]["parts"][0]["text"].encode()==question and
             wire["generationConfig"]["maxOutputTokens"]==6144 and
             audit["request_sha256"]==sha256(request).hexdigest() and audit["prompt_sha256"]==sha256(question).hexdigest()
             and audit["checkout_sha"]==audit["workflow_sha"]==head and audit["run_id"]==str(info["run_id"])
             and audit["attempt"]==str(info["attempt"]),"frozen request and checkout")
        if "model_metadata.json" in z.namelist():
            model=object_(z,"model_metadata.json")
            need(model["name"]=="models/"+audit["model_requested"] and
                 "generateContent" in model["supportedGenerationMethods"],"external model metadata")
        if "provider_error.json" in z.namelist():
            marker="provider_error.json"
            error=object_(z,marker)
            need(audit==dict(audit="SCIENTIFIC_REPLAY_ONLY",**error) and error["external_review"]=="NO_MODEL_VERDICT"
                 and 400<=error["http_status"]<600 and not set(z.namelist())&{"response.json","receipt.json","review.txt"}
                 and jobs["argument-review"]==info["conclusion"]=="failure","provider disposition")
            status="PENDING_HTTP_"+str(error["http_status"])
        else:
            marker="response.json"
            reply=object_(z,marker)
            text="\n".join(part["text"] for part in reply["candidates"][0]["content"]["parts"]
                         if "text" in part and not part.get("thought")).strip()
            need(z.read("review.txt")==text.encode() and sha256(z.read(marker)).hexdigest()==audit["response_sha256"]
                 and audit==dict(audit=audit["audit"],**object_(z,"receipt.json")),"original model response")
            status="ACCEPTED" if audit["audit"]=="PASS" else "REVIEW_REQUIRES_ADJUDICATION"
            need((jobs["argument-review"]=="success")==(status=="ACCEPTED"),"review decision")
            if status=="ACCEPTED":
                verdict=json.loads(text)
                need(verdict["verdict"]=="ACCEPTED" and verdict["native_bridge_status"]=="OPEN" and
                     all(not verdict[k] for k in ("findings","counterexamples","missing_assumptions")),"external scope")
        echoed=dict(x.split("_B64=",1) for x in (HERE/"publication_readback.log").read_text().splitlines())
        need(set(echoed)=={marker,"publication_audit.json"} and
             base64.b64decode(echoed[marker],validate=True)==z.read(marker) and
             base64.b64decode(echoed["publication_audit.json"],validate=True)==raw,"independent job-log echo")
    old=HERE/"initial"
    first=json.loads((old/"run.json").read_bytes())
    need(first["run_id"]==45540575849 and first["science_head"]=="ec792b8cd37222e0e69b62b04a2397ecd847ce45"
         and {j["name"]:j["conclusion"] for j in first["jobs"]}==
         {"replay":"failure","argument-review":"failure","foundational-regression":"success","publication":"skipped"},
         "original failed run")
    need(len(first["archives"])==3 and {r["name"] for r in first["archives"]}==
         {"free-receiver-foundation","free-receiver-review","free-receiver-replay"},"failed-run archives")
    for row in first["archives"]:
        path=old/(row["name"]+".zip")
        need(path.stat().st_size==row["size"] and "sha256:"+sha256(path.read_bytes()).hexdigest()==row["digest"],
             "first run "+row["name"])
        with ZipFile(path) as z:
            need(z.testzip() is None,"first ZIP integrity")
    with ZipFile(old/"free-receiver-replay.zip") as z:
        for name in OUTPUTS[:4]:
            need(z.read(name)==(SCI/name).read_bytes(),"first completed calculation "+name)
    with ZipFile(old/"free-receiver-foundation.zip") as z:
        manifest(z)
        need(object_(z,"VERIFICATION.json")["coverage"]["instances"]==21,"first foundation")
    with ZipFile(old/"free-receiver-review.zip") as z:
        error=object_(z,"provider_error.json")
        need(error["checkout_sha"]==first["science_head"] and error["http_status"]==402
             and error["external_review"]=="NO_MODEL_VERDICT","first provider result")
    need("ValueError: invalid literal for int() with base 10: '13F'" in (old/"replay.log").read_text()
         and "Provider generateContent HTTP 402" in (old/"review.log").read_text(),"original error logs")
    return dict(run_id=info["run_id"],science_head=head,foundational_certificates=21,inherited_tests=[22,15,2],
                scientific_replay="PASS",fresh_publication="PASS",external_review=status,outputs_sha256=hashes,
                receiver_root_maxima=[3176,3175],shortest_anonymous_word=931,common_records_exponent=1304,
                languages=5820,local_words=52646,selected_post_source_cases=0,initial_failed_run=first["run_id"])


if __name__=="__main__":
    print(json.dumps(main(),sort_keys=True,indent=2))
