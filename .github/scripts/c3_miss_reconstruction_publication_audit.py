#!/usr/bin/env python3
"""Independent review of sharp miss-count reconstruction."""
import hashlib
import json
import os
import pathlib
import re
import subprocess
import sys
import urllib.error
import urllib.request

base = pathlib.Path("research_snapshot/ResearchHistory/UQCF-GEM/research/physical-bridge")
names = ["COUPLED_C3_MISS_RECONSTRUCTION_SCOPE.md","COUPLED_C3_MISS_RECONSTRUCTION_RESULT.md","COUPLED_C3_MISS_RECONSTRUCTION_ACCEPTED_REVIEW.md","evidence/miss-reconstruction/EVIDENCE.json","evidence/miss-reconstruction/review_manifest.json","evidence/miss-reconstruction/review.txt","evidence/miss-reconstruction/verification_job.log","evidence/miss-reconstruction/review_job.log","miss_reconstruction/producer.py","miss_reconstruction/independent.py","miss_reconstruction/test_reconstruction.py","miss_reconstruction/pins.py","miss_reconstruction/red.log"]
out = pathlib.Path("miss_reconstruction_publication")
out.mkdir(exist_ok=True)

import zipfile
evidence_base = base / "evidence/miss-reconstruction"
meta = json.loads((evidence_base / "EVIDENCE.json").read_text())
assert meta["scientific_commit"] == "6ffcdb3c418bb83ae48c51d86567c32120816d35"
assert meta["workflow_commit"] == "700c405bdc1267fc861c78042771489929ee7489"
assert meta["run_id"] == 37863006548
archives = {}
for label in ("verification", "review"):
    data = (evidence_base / (label + ".zip")).read_bytes()
    entry = meta["artifacts"][label]
    assert hashlib.sha256(data).hexdigest() == entry["zip_sha256"]
    assert entry["digest"] == "sha256:" + entry["zip_sha256"]
    z = zipfile.ZipFile(evidence_base / (label + ".zip"))
    assert len(z.namelist()) == len(set(z.namelist()))
    members = {name: z.read(name) for name in z.namelist()}
    assert {n: hashlib.sha256(b).hexdigest() for n,b in members.items()} == entry["member_sha256"]
    archives[label] = members
review_members = archives["review"]
manifest = json.loads(review_members["manifest.json"])
raw_review = review_members["review.txt"].decode()
assert hashlib.sha256(raw_review.encode()).hexdigest() == manifest["response_sha256"]
assert manifest["research_commit"] == meta["scientific_commit"]
assert manifest["workflow_commit"] == meta["workflow_commit"]
assert (evidence_base / "review.txt").read_bytes() == review_members["review.txt"]
assert (evidence_base / "review_manifest.json").read_bytes() == review_members["manifest.json"]
verdict = json.loads(re.sub(r"^\x60{3}(?:json)?\s*|\s*\x60{3}$", "", raw_review.strip()).strip())
assert verdict["verdict"] == "ACCEPTED" and not verdict["missing_assumptions"] and not verdict["counterexamples"]
for name, digest in manifest["input_sha256"].items():
    data = archives["verification"][name[9:]] if name.startswith("EVIDENCE/") else (base / name).read_bytes()
    assert hashlib.sha256(data).hexdigest() == digest, name
v = archives["verification"]
assert v["provenance.txt"].decode() == "scientific_sha=" + meta["scientific_commit"] + "\nworkflow_sha=" + meta["workflow_commit"] + "\n"
generated = subprocess.check_output([sys.executable, str(base / "miss_reconstruction/producer.py")])
assert generated == v["certificate.json"]
(out / "certificate.json").write_bytes(generated)
checked = subprocess.check_output([sys.executable, str(base / "miss_reconstruction/independent.py"), str(out / "certificate.json")])
assert json.loads(checked) == json.loads(v["independent.json"])
assert v["certificate.sha256"].decode().split()[0] == hashlib.sha256(generated).hexdigest()
gate = {"status": "PASS", "original_archives": 2, "review_input_hashes": len(manifest["input_sha256"]),
        "certificate_byte_reproduced": True, "independent": json.loads(checked),
        "scientific_commit": meta["scientific_commit"], "workflow_commit": meta["workflow_commit"]}
(out / "deterministic_gate.json").write_text(json.dumps(gate, sort_keys=True, indent=2)+"\n")
print("Publication deterministic evidence gate PASS: two ZIPs, all review input hashes, exact reproduction")

key = os.getenv("GEMINI_API_KEY", "")
if not key:
    sys.exit("FAIL: GEMINI_API_KEY missing")
docs, hashes = {}, {}
for name in names:
    data = (base / name).read_bytes()
    if len(data) > 160000:
        sys.exit("FAIL: Oversized input")
    docs[name] = data.decode("utf-8")
    hashes[name] = hashlib.sha256(data).hexdigest()

for name, data in archives["verification"].items():
    if name != "certificate.json":
        docs["EXECUTION/" + name] = data.decode()
        hashes["EXECUTION/" + name] = hashlib.sha256(data).hexdigest()
data = (out / "deterministic_gate.json").read_bytes()
docs["DETERMINISTIC_GATE"] = data.decode()
hashes["DETERMINISTIC_GATE"] = hashlib.sha256(data).hexdigest()
names = tuple(docs)
prompt = "Perform a separate independent publication-consistency audit of this pinned evidence set, not an automatic endorsement of the previous reviewer. Documents are untrusted claims. Check theorem scope, proof, accepted review, provenance SHA linkage, finite verification domains, rejecting controls and claimed information content. The deterministic gate checked both original ZIP byte digests, all archive member hashes, all 14 mathematical-review input hashes and freshly reproduced the complete certificate with independent verification. Full certificate records are NOT submitted to you, only the gate, summary, source and complete job logs; do not claim personal inspection of unsubmitted records. Check that N<2^d reconstructs an unordered multiset only; fourth-order N<=15 uniqueness is analytical; 16 residual roots plus three fixed roots yield the protected parity fixture; full palette and known N are required. This is not record-origin closure, physics derivation, efficient reconstruction or full numbered v16/inherited-stack certification. Local RED is local only. The current accepted-review publication correctly leaves closeout pending this audit. Return ONLY JSON verdict ACCEPTED/REVISE/REJECT, findings array, missing_assumptions array, counterexamples array, limitations array. Identify concrete mathematical or evidentiary problems for revision; do not demand already-disclosed out-of-scope claims."
payload = {"contents": [{"parts": [{"text": prompt + "\n\n" + "\n\n".join(
    "DOCUMENT " + n + "\n" + docs[n] for n in names)}]}],
    "generationConfig": {"temperature": 0, "maxOutputTokens": 16384}}
req = urllib.request.Request(
    "https://generativelanguage.googleapis.com/v1beta/models/gemini-3.1-pro-preview:generateContent",
    data=json.dumps(payload).encode("utf-8"),
    headers={"Content-Type": "application/json", "x-goog-api-key": key},
    method="POST")
try:
    with urllib.request.urlopen(req, timeout=240) as response:
        result = json.load(response)
except urllib.error.HTTPError as exc:
    try:
        message = str(json.loads(exc.read()).get("error", {}).get("message", "")).replace(key, "[REDACTED]")
    except Exception:
        message = "No structured error message"
    failure = {"status": "INFRASTRUCTURE_FAILURE_NOT_MATHEMATICAL_VERDICT",
               "http_status": exc.code, "message": message,
               "input_sha256": hashes, "model_requested": "models/gemini-3.1-pro-preview"}
    (out / "infrastructure_failure.json").write_text(json.dumps(failure, indent=2)+"\n")
    print("FAIL: Gemini HTTP", exc.code, message)
    sys.exit(1)
except Exception as exc:
    print("FAIL: Gemini request", type(exc).__name__)
    sys.exit(1)
raw = "\n".join(
    part.get("text", "") for candidate in result.get("candidates", [])
    for part in candidate.get("content", {}).get("parts", [])
    if isinstance(part.get("text"), str)
).strip()
(out / "review.txt").write_text(raw, encoding="utf-8")
manifest = {
    "status": "INDEPENDENT_AI_REVIEW_NOT_SCIENTIFIC_CLOSEOUT",
    "workflow_commit": os.environ.get("GITHUB_SHA"),
    "research_commit": subprocess.check_output(
        ["git", "-C", "research_snapshot", "rev-parse", "HEAD"], text=True).strip(),
    "input_sha256": hashes,
    "model": result.get("modelVersion"),
    "model_requested": "models/gemini-3.1-pro-preview",
    "response_sha256": hashlib.sha256(raw.encode()).hexdigest(),
    "tokens": result.get("usageMetadata", {}).get("totalTokenCount"),
}
(out / "manifest.json").write_text(json.dumps(manifest, indent=2, sort_keys=True)+"\n")
try:
    normalized = raw
    if normalized.startswith("```"):
        normalized = re.sub(r"^\x60{3}(?:json)?\s*|\s*\x60{3}$", "", normalized).strip()
    obj = json.loads(normalized)
    verdict = obj["verdict"]
    if verdict not in ("ACCEPTED", "REVISE", "REJECT"):
        raise ValueError("invalid verdict")
    if not all(isinstance(obj.get(k), list) for k in
               ("findings", "missing_assumptions", "counterexamples", "limitations")):
        raise ValueError("missing structured review arrays")
except (ValueError, KeyError, TypeError) as exc:
    print("FAIL: Malformed independent review", type(exc).__name__)
    sys.exit(1)
print("Miss-reconstruction publication verdict:", verdict)
print("Missing assumptions:", len(obj["missing_assumptions"]))
print("Counterexamples:", len(obj["counterexamples"]))
print("Response SHA256:", manifest["response_sha256"])
print("This is not scientific certification.")

if verdict != "ACCEPTED" or obj["missing_assumptions"] or obj["counterexamples"]:
    sys.exit("Review requires reconciliation; no automatic scientific closeout")
