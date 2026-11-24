"""One bounded Gemini request after a provider-side 402, with exact publication readback."""
import base64
from hashlib import sha1, sha256
import json
import os
from pathlib import Path
import subprocess
import sys
from urllib.error import HTTPError
from urllib.request import Request, urlopen

from review_cover_return import DOCUMENTS, QUESTION, TOPICS
from review_depth_two import ROOT

sys.path.insert(0,str(ROOT/".github/scripts"))
from uqcf_preparability_review import MODEL, accepted, parse_response

CAP=6144
FIRST_HEAD="f50d0bcd266662a0420b4dca66f0d16cb90f7a2d"
FIRST_RUN=45495339040


def wire(obj):
    return (json.dumps(obj,sort_keys=True,indent=2,ensure_ascii=False)+"\n").encode()


def digest(raw):
    return sha256(raw).hexdigest()


def checked(file,blob):
    raw=(ROOT/file).read_bytes()
    if sha1(f"blob {len(raw)}\0".encode()+raw).hexdigest()!=blob:
        raise ValueError("changed review source "+file)
    return raw


def prompt():
    data={p:checked(p,b).decode() for p,b in DOCUMENTS.items()}
    sci="ResearchHistory/UQCF-GEM/research/physical-bridge/geometry_recovery_paths/"
    demo="review_sources/ResearchHistory/UQCF-GEM/demos/"
    content=[QUESTION,"This request follows an HTTP 402 with no earlier model response. The mathematical claims and numerical questions are unchanged. The complete proof and selected verbatim implementation lines follow. Address every stated limitation independently."]
    sections=[(sci+"COVER_RETURN_WRITE.md",1,None),
              (demo+"v16.26-consistency-increment-law/engine.py",10,30),
              (demo+"v16.33-consistency-quotient-kernel/verifier.py",4,21),
              (demo+"v16.54-parent-support-connectivity/model.py",5,None),
              (demo+"v16.54-parent-support-connectivity/mechanisms.py",5,38),
              (demo+"v16.54-parent-support-connectivity/mechanisms.py",325,330),
              (demo+"v16.54-parent-support-connectivity/universe.py",29,50),
              (sci+"verify_cover_return_budget.py",1,None)]
    for file,first,last in sections:
        lines=data[file].splitlines(keepends=True)
        content.extend([f"BEGIN exact {file} lines {first} through {last or len(lines)}",
                        "".join(lines[first-1:last]),"END exact file section"])
    cert=json.loads(data[sci+"cover_return_certificate.json"])
    subset=dict(primary=cert["counts"],budget=cert["budget"],raw_sha256=cert["raw_sha256"],
                raw_archived_row=cert["archived_record"]["record_sha256"])
    content+=["Derived excerpt from the frozen certificate",json.dumps(subset,sort_keys=True)]
    return ("\n".join(content)+"\n").encode()


def verify_reply(doc):
    accepted(doc)
    if doc["verdict"]!="ACCEPTED" or doc["native_bridge_status"]!="OPEN":
        raise ValueError("external review not accepted")
    checks=doc.get("proof_checks",{})
    if set(checks)!=TOPICS or any(not isinstance(x,str) or len(x.split())<15 for x in checks.values()):
        raise ValueError("missing independent worked checks")
    expected=dict(six_active=[3,5],primary_arms=2112,budget_arms=81,q2_preserving=1,q3_preserving=2,
                  three_mark_bypass=3,three_mark_records=[[1],[1,2],[1,3]],rebuilt_first_chart=0,
                  no_source_input_scheduler=True)
    if json.dumps(doc["exact_checks"],sort_keys=True)!=json.dumps(expected,sort_keys=True):
        raise ValueError("external quantitative reconstruction differs")


def main(mode,out):
    if mode not in ("review","audit"):raise ValueError("mode")
    out.mkdir(exist_ok=True,parents=True)
    current=subprocess.check_output(["git","rev-parse","HEAD"],cwd=ROOT,text=True).strip()
    if current!=os.environ["GITHUB_SHA"] or current!=os.environ["UQCF_WORKFLOW_SHA"]:
        raise ValueError("review/workflow revision mismatch")
    checked(".github/scripts/uqcf_preparability_review.py","4c8029da503ed57f404e4424ecc243eb3c609347")
    checked(".github/scripts/uqcf_preparability_integrity.py","50b1043cda14b18b962f7930cf6a4391067a2a96")
    question=prompt()
    body=wire(dict(contents=[dict(role="user",parts=[dict(text=question.decode())])],
                   generationConfig=dict(temperature=0,maxOutputTokens=CAP,responseMimeType="application/json")))
    base=dict(checkout_sha=current,workflow_sha=current,run_id=os.environ["GITHUB_RUN_ID"],
              attempt=os.environ["GITHUB_RUN_ATTEMPT"],model_requested=MODEL,source_blobs=DOCUMENTS,
              prompt_sha256=digest(question),request_sha256=digest(body),output_token_cap=CAP,
              first_run=FIRST_RUN,first_head=FIRST_HEAD)
    url="https://generativelanguage.googleapis.com/v1beta/models/"+MODEL
    if mode=="review":
        if base["attempt"]!="1":raise ValueError("only first review attempt")
        (out/"prompt.txt").write_bytes(question)
        (out/"request.json").write_bytes(body)
        headers={"x-goog-api-key":os.environ["GEMINI_API_KEY"]}
        with urlopen(Request(url,headers=headers),timeout=60) as r:
            metadata=r.read()
        (out/"model_metadata.json").write_bytes(metadata)
        if json.loads(metadata).get("name")!="models/"+MODEL or "generateContent" not in json.loads(metadata).get("supportedGenerationMethods",[]):
            raise ValueError("model metadata mismatch")
        try:
            with urlopen(Request(url+":generateContent",data=body,headers={**headers,"Content-Type":"application/json"}),
                         timeout=600) as r:
                reply=r.read()
        except HTTPError as err:
            (out/"provider_error.json").write_bytes(wire(dict(**base,stage="generateContent",http_status=err.code,
                                                          external_review="NO_MODEL_VERDICT")))
            print("Provider generation HTTP",err.code,"without a model verdict")
            raise SystemExit(1)
        (out/"response.json").write_bytes(reply)
    else:
        if (out/"prompt.txt").read_bytes()!=question or (out/"request.json").read_bytes()!=body:
            raise ValueError("prompt/request mismatch")
        meta=json.loads((out/"model_metadata.json").read_bytes())
        if meta.get("name")!="models/"+MODEL:raise ValueError("wrong model metadata")
        if (out/"provider_error.json").is_file():
            expected=dict(**base,stage="generateContent",http_status=402,external_review="NO_MODEL_VERDICT")
            if json.loads((out/"provider_error.json").read_bytes())!=expected or any(
                    (out/n).exists() for n in ("response.json","receipt.json","review.txt")):
                raise ValueError("unverified provider failure")
            (out/"publication_audit.json").write_bytes(wire(dict(audit="SCIENTIFIC_REPLAY_ONLY",**expected)))
            for name in ("provider_error.json","publication_audit.json"):
                print(name+"_B64="+base64.b64encode((out/name).read_bytes()).decode())
            return
        reply=(out/"response.json").read_bytes()
    answer,verdict,model=parse_response(reply)
    receipt=dict(**base,model_returned=model,verdict=verdict["verdict"],response_sha256=digest(reply))
    if mode=="review":
        (out/"review.txt").write_bytes(answer)
        (out/"receipt.json").write_bytes(wire(receipt))
    verify_reply(verdict)
    if mode=="audit":
        if (out/"review.txt").read_bytes()!=answer or json.loads((out/"receipt.json").read_bytes())!=receipt:
            raise ValueError("review readback mismatch")
        (out/"publication_audit.json").write_bytes(wire(dict(audit="PASS",**receipt)))
        for name in ("response.json","publication_audit.json"):
            print(name+"_B64="+base64.b64encode((out/name).read_bytes()).decode())
    print("External verdict",verdict["verdict"])


if __name__=="__main__":
    main(sys.argv[1],Path(sys.argv[2]))
