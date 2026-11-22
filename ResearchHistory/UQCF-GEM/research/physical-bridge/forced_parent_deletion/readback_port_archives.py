"""Check complete GitHub artifact archives against the frozen fixed-port experiment."""
import base64
import hashlib
import json
import subprocess
import zipfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = "proteinfoldingengine/WetLabEngine"
ARCHIVES = {"review":[14713861451,121286,"5d22f6561cf092e857e70fc0301c3171a7189dac2c3dcd2d3c797f661ac35145"],"audit":[14713846857,1281,"f7c0b2034012d011f1036fa9fae36409186a2ad69f6cc34c855acf47625262ec"],"replay":[14713797044,1725,"f821848cb64d446989db4b7c5beaca40147182ecb95f67f16e76df5add4ba139"]}
HEAD = "60b731e3e9048460a73627783abf6a6e2b065f5e"
RUN = 44921237892
RESPONSE = "d9b8843110cf1e85d8a9af54a7f3e7b616941a4cbcde6d1d14c6ad3f7665de47"

def digest(data):
    return hashlib.sha256(data).hexdigest()

def read_artifact(artifact_id):
    target = f"repos/{REPO}/actions/artifacts/{artifact_id}/zip"
    return subprocess.run(["gh", "api", target], capture_output=True, check=True).stdout

def main():
    target = Path("frozen_port_artifacts")
    target.mkdir(exist_ok=True)
    contents = {}
    manifest = {}
    for name, (artifact_id, size, expected_hash) in sorted(ARCHIVES.items()):
        raw = read_artifact(artifact_id)
        assert len(raw) == size and digest(raw) == expected_hash
        path = target / (name + ".zip")
        path.write_bytes(raw)
        with zipfile.ZipFile(path) as archive:
            assert archive.testzip() is None
            assert all(entry == Path(entry).name for entry in archive.namelist())
            docs = {entry: archive.read(entry) for entry in archive.namelist()}
        contents[name] = docs
        manifest[name] = {"artifact_id": artifact_id, "bytes": size, "sha256": expected_hash,
                          "entries": {entry: {"bytes": len(data), "sha256": digest(data)}
                                      for entry, data in docs.items()}}
    assert contents["replay"]["replay.json"] == (HERE / "remote_port_results.json").read_bytes()
    audit = json.loads(contents["audit"]["publication_audit.json"])
    docs = contents["review"]
    assert audit["checkout_sha"] == audit["workflow_sha"] == HEAD and int(audit["run_id"]) == RUN
    assert audit["audit"] == "PASS" and audit["verdict"] == "ACCEPTED"
    assert audit["response_sha256"] == RESPONSE == digest(docs["response.json"])
    assert audit["prompt_sha256"] == digest(docs["prompt.txt"])
    assert audit["request_sha256"] == digest(docs["request.json"])
    model = json.loads(docs["response.json"])
    verdict = json.loads(docs["review.txt"])
    assert model["modelVersion"] == audit["model_returned"]
    assert verdict["verdict"] == "ACCEPTED" and not any(verdict[k] for k in ("findings","missing_assumptions","counterexamples"))
    for which in sorted(ARCHIVES):
        data = (target / (which + ".zip")).read_bytes()
        for i in range(0, len(data), 6000):
            print(f"PORT_ARCHIVE_{which}_{i//6000}=" + base64.b64encode(data[i:i+6000]).decode())
    print("PORT_MANIFEST=" + json.dumps(manifest, sort_keys=True))

if __name__ == "__main__":
    main()
