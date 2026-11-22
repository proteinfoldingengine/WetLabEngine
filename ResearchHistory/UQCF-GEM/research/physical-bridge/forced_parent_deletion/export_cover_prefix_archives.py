"""Preserve exact review/audit ZIPs using the inherited fixed-donor export pattern."""
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
    return subprocess.run(["gh", "api", ROOT + path], capture_output=True, check=True).stdout


def sha(data):
    return hashlib.sha256(data).hexdigest()


def main():
    run = int(os.environ["GITHUB_RUN_ID"])
    head = os.environ["GITHUB_SHA"]
    listing = json.loads(api(f"actions/runs/{run}/artifacts?per_page=100"))
    archives = {a["name"].removeprefix("cover-prefix-"): a for a in listing["artifacts"]
                if a["name"].startswith("cover-prefix-")}
    assert set(archives) == {"review", "publication"}
    payloads, report, binaries = {}, {}, {}
    for name, artifact in sorted(archives.items()):
        binary = api(f'actions/artifacts/{artifact["id"]}/zip')
        assert len(binary) == artifact["size_in_bytes"]
        assert artifact["digest"] == "sha256:" + sha(binary)
        with ZipFile(io.BytesIO(binary)) as archive:
            assert archive.testzip() is None
            assert all(Path(n).name == n for n in archive.namelist())
            data = {p: archive.read(p) for p in archive.namelist()}
        binaries[name], payloads[name] = binary, data
        report[name] = {"artifact_id": artifact["id"], "sha256": sha(binary), "bytes": len(binary),
                        "entries": {f: {"bytes": len(v), "sha256": sha(v)} for f, v in data.items()}}
    audit = json.loads(payloads["publication"]["publication_audit.json"])
    review = payloads["review"]
    assert audit["checkout_sha"] == audit["workflow_sha"] == head
    assert int(audit["run_id"]) == run and audit["audit"] == "PASS"
    # Preserve adverse verdicts too; successful byte audit is not scientific acceptance.
    for filename, key in (("response.json", "response"), ("prompt.txt", "prompt"), ("request.json", "request")):
        assert audit[key + "_sha256"] == sha(review[filename])
    assert json.loads(review["response.json"])["modelVersion"] == audit["model_returned"]
    for alias, binary in binaries.items():
        for i in range(0, len(binary), 6000):
            print(f"PREFIX_ARCHIVE_{alias}_{i // 6000}=" + base64.b64encode(binary[i:i + 6000]).decode())
    print("PREFIX_MANIFEST=" + json.dumps(report, sort_keys=True))


if __name__ == "__main__":
    main()
