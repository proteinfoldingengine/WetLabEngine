"""Replay two frozen model responses, with their original and differing scope labels."""
from hashlib import sha1, sha256
from pathlib import Path
from zipfile import ZipFile
import json
import sys

root, science, reviews, generated = map(Path, sys.argv[1:5])
expected = [
    ("45935921810", "c40aa2851fb6e2e903fd054e2306c504ba3dc1e6", "OPEN",
     "86673fc1e501914a2de0d3750614e2a79310b2ed55e030ed6d1ec93b9113ffbe"),
    ("45936122756", "45e2997b1494dc55047c085f845e3896fcbe25b5", "REFUTED",
     "5719ea070951927601b636cac5118a5a48f802a975158392cb583531b1354697"),
]
outputs = []
for n, (run, sha, label, digest) in enumerate(expected, start=1):
    folder = reviews / f"attempt{n}"
    archive = folder / "original_review.zip"
    assert sha256(archive.read_bytes()).hexdigest() == digest
    with ZipFile(archive) as packet:
        def read(name):
            return json.loads(packet.read(name))
        receipt = read("receipt.json")
        audit = read("publication_audit.json")
        assert receipt["checkout_sha"] == receipt["workflow_sha"] == sha
        assert receipt["run_id"] == run and audit == dict(receipt, audit="PASS")
        for name in ["receipt.json", "publication_audit.json", "response.json", "review.txt", "model_metadata.json"]:
            assert packet.read(name) == (folder / name).read_bytes()
        for key, name in [("prompt", "prompt.txt"), ("request", "request.json"), ("response", "response.json")]:
            assert sha256(packet.read(name)).hexdigest() == receipt[key + "_sha256"]
        assert read("request.json")["contents"][0]["parts"][0]["text"] == packet.read("prompt.txt").decode()
        for source, blob in receipt["source_blobs"].items():
            payload = (root / source).read_bytes()
            assert sha1(f"blob {len(payload)}\0".encode() + payload).hexdigest() == blob
        answer = read("review.txt")
        raw = read("response.json")
        saved_text = "".join(p["text"] for p in raw["candidates"][0]["content"]["parts"] if "text" in p)
        assert json.loads(saved_text) == answer
        assert answer["verdict"] == receipt["verdict"] == "ACCEPTED"
        assert answer["program_status"] == "DERIVED" and answer["native_bridge_status"] == label
        assert all(answer[k] == [] for k in ["findings", "missing_assumptions", "counterexamples"])
        assert bool(answer["limitations"]) == (n == 2)
        for name in ["records.json.xz", "results.json", "verification.json", "archive_order.json"]:
            assert (science/name).read_bytes() == packet.read(name) == (generated/name).read_bytes()
        outputs.append(dict(run=run, checkout=sha, archive_sha256=digest, verdict=answer["verdict"],
                            program_status=answer["program_status"], native_bridge_status=label,
                            limitations=len(answer["limitations"]), proof_checks=len(answer["proof_checks"])))
print(json.dumps(outputs, indent=2, sort_keys=True))
