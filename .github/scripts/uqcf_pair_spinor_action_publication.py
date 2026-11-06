"""Separate immutable GitHub readback and review-artifact audit."""
import base64, hashlib, json, os, re, urllib.parse, urllib.request
from pathlib import Path

REPO="proteinfoldingengine/WetLabEngine"
FILES=(
"ResearchHistory/UQCF-GEM/research/physical-bridge/pair_spinor_action_review/ARGUMENT.md",
".github/scripts/uqcf_pair_spinor_action_review.py",
".github/scripts/uqcf_pair_spinor_action_publication.py",
".github/workflows/uqcf-pair-spinor-action-review.yml",
)
OUT=Path("pair_spinor_publication")
def sha(b): return hashlib.sha256(b).hexdigest()
def parse(b): return json.loads(b)
def api(path):
    req=urllib.request.Request("https://api.github.com/repos/"+REPO+path,headers={"Authorization":"Bearer "+os.environ["GH_READ_TOKEN"],"Accept":"application/vnd.github+json","X-GitHub-Api-Version":"2022-11-28"})
    with urllib.request.urlopen(req,timeout=60) as r:return parse(r.read())
def main():
    OUT.mkdir(exist_ok=True)
    source=os.environ["GITHUB_SHA"]
    if not re.fullmatch(r"[0-9a-f]{40}",source): raise ValueError("invalid source sha")
    checked=[]
    for path in FILES:
        listing=api("/contents/"+urllib.parse.quote(path,safe="/")+"?ref="+source)
        blob=api("/git/blobs/"+listing["sha"])
        raw=base64.b64decode("".join(blob["content"].split()),validate=True)
        local=Path(path).read_bytes()
        if raw!=local: raise ValueError("immutable readback mismatch "+path)
        checked.append({"path":path,"git_blob":listing["sha"],"bytes":len(raw),"sha256":sha(raw)})
    review=Path("pair_spinor_review")
    integrity=Path("pair_spinor_integrity")
    iraw=(integrity/"integrity.json").read_bytes(); integ=parse(iraw)
    manifest=parse((review/"manifest.json").read_bytes())
    verdict=parse((review/"verdict.json").read_bytes())
    response=(review/"response.json").read_bytes()
    if integ.get("source_sha")!=source or manifest.get("source_sha")!=source: raise ValueError("run identity mismatch")
    if manifest.get("status")!="COMPLETE" or manifest.get("response_sha256")!=sha(response): raise ValueError("review artifact mismatch")
    result={"status":"PASS","source_sha":source,"run_id":os.environ.get("GITHUB_RUN_ID"),"run_attempt":os.environ.get("GITHUB_RUN_ATTEMPT"),"immutable_files":checked,"integrity_sha256":sha(iraw),"review_manifest_sha256":sha((review/"manifest.json").read_bytes()),"raw_response_sha256":sha(response),"verdict_sha256":sha((review/"verdict.json").read_bytes()),"verdict":verdict.get("verdict"),"native_bridge_status":verdict.get("native_bridge_status"),"raw_adverse_evidence_preserved":True}
    (OUT/"publication.json").write_text(json.dumps(result,indent=2,sort_keys=True)+"\n")
    print("Publication audit PASS:",result["verdict"],result["native_bridge_status"])
if __name__=="__main__":main()
