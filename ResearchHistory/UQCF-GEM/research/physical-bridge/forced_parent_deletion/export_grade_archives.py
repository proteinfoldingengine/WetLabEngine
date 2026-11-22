"""Verify the original GitHub artifacts before emitting archive bytes for preservation."""
import base64
import hashlib
import io
import json
import os
import subprocess
from pathlib import Path
from zipfile import ZipFile

ROOT = "repos/proteinfoldingengine/WetLabEngine/"

def api(path):
    return subprocess.run(["gh", "api", ROOT+path], capture_output=True,check=True).stdout

def sha(data):
    return hashlib.sha256(data).hexdigest()

def main():
    run = int(os.environ["GITHUB_RUN_ID"])
    head = os.environ["GITHUB_SHA"]
    listing = json.loads(api(f"actions/runs/{run}/artifacts?per_page=100"))
    archives = {a["name"].removeprefix("routed-grade-"):a for a in listing["artifacts"]
                if a["name"].startswith("routed-grade-")}
    assert set(archives) == {"replay","review","publication"}
    payloads, report, binaries = {}, {}, {}
    for name,a in sorted(archives.items()):
        binary = api(f'actions/artifacts/{a["id"]}/zip')
        assert len(binary) == a["size_in_bytes"] and a["digest"] == "sha256:"+sha(binary)
        with ZipFile(io.BytesIO(binary)) as z:
            assert z.testzip() is None and all(Path(n).name == n for n in z.namelist())
            data = {p:z.read(p) for p in z.namelist()}
        binaries[name] = binary
        payloads[name] = data
        report[name] = {"artifact_id":a["id"],"sha256":sha(binary),"bytes":len(binary),
                        "entries":{f:{"bytes":len(v),"sha256":sha(v)} for f,v in data.items()}}
    replay = json.loads(payloads["replay"]["grade.json"])
    assert replay["basis_family_states_checked"] == 306
    audit = json.loads(payloads["publication"]["publication_audit.json"])
    review = payloads["review"]
    assert audit["checkout_sha"] == audit["workflow_sha"] == head and int(audit["run_id"]) == run
    assert audit["audit"] == "PASS" and audit["verdict"] == "ACCEPTED"
    for filename, key in (("response.json","response"),("prompt.txt","prompt"),("request.json","request")):
        assert audit[key+"_sha256"] == sha(review[filename])
    raw = json.loads(review["response.json"])
    assert raw["modelVersion"] == audit["model_returned"]
    for alias,binary in binaries.items():
        for i in range(0,len(binary),6000):
            encoded=base64.b64encode(binary[i:i+6000]).decode()
            print(f"GRADE_ARCHIVE_{alias}_{i//6000}={encoded}")
    print("GRADE_MANIFEST="+json.dumps(report,sort_keys=True))

if __name__ == "__main__":
    main()
