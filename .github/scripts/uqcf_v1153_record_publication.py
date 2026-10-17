"""Separate immutable remote publication audit. No review code imported."""
import base64,hashlib,json,os,urllib.request,urllib.parse
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
REL="ResearchHistory/UQCF-GEM/research/physical-bridge/v1153_record_screen"
OUT=Path("v1153_publication"); OUT.mkdir(exist_ok=True)
def h(b): return hashlib.sha256(b).hexdigest()
def get(path):
    q=urllib.request.Request("https://api.github.com/repos/proteinfoldingengine/WetLabEngine"+path,headers={"Authorization":"Bearer "+os.environ["GH_READ_TOKEN"],"Accept":"application/vnd.github+json"})
    with urllib.request.urlopen(q,timeout=60) as r:return json.load(r)
try:
    head=os.environ["GITHUB_SHA"]; assert head==os.environ["UQCF_WORKFLOW_SHA"]
    commit=get("/commits/"+head); assert commit["author"]["login"]=="proteinfolding-gpt"
    m=json.loads(Path("v1153_review/manifest.json").read_text())
    assert m["scientific_sha"]==m["workflow_sha"]==head and m["run_id"]==os.environ["GITHUB_RUN_ID"] and m["run_attempt"]==os.environ["GITHUB_RUN_ATTEMPT"]
    checked=[]
    def remote(path,ref,data):
        rec=get("/contents/"+urllib.parse.quote(path,safe="/")+"?ref="+ref)
        blob=get("/git/blobs/"+rec["sha"]); assert blob["encoding"]=="base64"
        got=base64.b64decode(blob["content"]); assert got==data
        digest=hashlib.sha1(b"blob "+str(len(got)).encode()+b"\0"+got).hexdigest()
        assert digest==rec["sha"]
        checked.append({"path":path,"ref":ref,"git_blob":digest,"sha256":h(got)})
    for n,e in m["inputs"].items():
        data=(ROOT/n).read_bytes(); assert h(data)==e["sha256"]
        remote(n,head,data); assert checked[-1]["git_blob"]==e["git_blob"]
    packet=json.loads((ROOT/REL/"source_packet.json").read_text())
    for f in packet["files"]:
        remote(f["path"],packet["baseline"],f["content"].encode()); assert checked[-1]["git_blob"]==f["git_blob"]
    prompt=Path("v1153_review/prompt.txt").read_bytes(); assert h(prompt)==m["prompt_sha256"]
    for n in ["RESULT.md","source_packet.json"]: assert (ROOT/REL/n).read_bytes() in prompt
    raw=Path("v1153_review/response.json").read_bytes(); assert h(raw)==m["response_sha256"]
    obj=json.loads(raw); assert len(obj["candidates"])==1 and obj["candidates"][0]["finishReason"]=="STOP"
    text="\n".join(p["text"] for p in obj["candidates"][0]["content"]["parts"] if not p.get("thought",False)).strip().encode()
    assert text==Path("v1153_review/review.txt").read_bytes() and h(text)==m["review_sha256"]
    v=json.loads(text); assert v==json.loads(Path("v1153_review/verdict.json").read_text())
    assert v["verdict"]=="ACCEPTED" and all(v[k]==[] for k in ["findings","missing_assumptions","counterexamples"])
    report={"status":"PASS","scientific_sha":head,"checked":checked,"review_manifest":m,"scope":"immutable reviewed-byte consistency; not native mechanism certification"}
    (OUT/"remote_readback.json").write_text(json.dumps(report,indent=2,sort_keys=True)+"\n")
    print("Immutable source, argument and review byte audit PASS")
except Exception as exc:
    (OUT/"failure.json").write_text(json.dumps({"status":"FAIL","error_type":type(exc).__name__}))
    raise SystemExit("Publication audit failed; sanitized evidence retained.")
