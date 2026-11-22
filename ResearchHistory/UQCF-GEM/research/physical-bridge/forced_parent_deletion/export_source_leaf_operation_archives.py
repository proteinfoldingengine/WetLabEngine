"""Preserve exact source-leaf operation review/audit ZIPs."""
import base64, hashlib, io, json, os, subprocess
from pathlib import Path
from zipfile import ZipFile
ROOT = "repos/proteinfoldingengine/WetLabEngine/"
def api(path): return subprocess.run(["gh", "api", ROOT + path], capture_output=True, check=True).stdout
def sha(data): return hashlib.sha256(data).hexdigest()
def main():
    run=int(os.environ["GITHUB_RUN_ID"]); head=os.environ["GITHUB_SHA"]
    listing=json.loads(api(f"actions/runs/{run}/artifacts?per_page=100"))
    archives={a["name"].removeprefix("source-leaf-operation-"):a for a in listing["artifacts"] if a["name"].startswith("source-leaf-operation-")}
    assert set(archives)=={"review","publication"}; payloads={}; report={}; binaries={}
    for name,a in sorted(archives.items()):
        binary=api(f'actions/artifacts/{a["id"]}/zip'); assert len(binary)==a["size_in_bytes"] and a["digest"]=="sha256:"+sha(binary)
        with ZipFile(io.BytesIO(binary)) as z:
            assert z.testzip() is None and all(Path(n).name==n for n in z.namelist()); data={n:z.read(n) for n in z.namelist()}
        binaries[name]=binary; payloads[name]=data; report[name]={"artifact_id":a["id"],"bytes":len(binary),"sha256":sha(binary),"entries":{n:{"bytes":len(v),"sha256":sha(v)} for n,v in data.items()}}
    audit=json.loads(payloads["publication"]["publication_audit.json"]); review=payloads["review"]
    assert audit["checkout_sha"]==audit["workflow_sha"]==head and int(audit["run_id"])==run and audit["audit"]=="PASS"
    for f,k in (("response.json","response"),("prompt.txt","prompt"),("request.json","request")): assert audit[k+"_sha256"]==sha(review[f])
    for alias,binary in binaries.items():
        for i in range(0,len(binary),6000): print(f"SOURCE_LEAF_OPERATION_ARCHIVE_{alias}_{i//6000}="+base64.b64encode(binary[i:i+6000]).decode())
    print("SOURCE_LEAF_OPERATION_MANIFEST="+json.dumps(report,sort_keys=True))
if __name__=="__main__": main()
