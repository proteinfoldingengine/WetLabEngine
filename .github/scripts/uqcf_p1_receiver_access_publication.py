"""Separate immutable publication audit for the corrected P1 receiver/access review."""
import hashlib
import json
import os
from pathlib import Path
import subprocess
import urllib.error

from uqcf_p1_receiver_access_review import (
    SOURCE_COMMIT, DOCUMENTS, FREEZE, REQUEST, build_prompt, remote
)
from uqcf_preparability_review import MODEL

OUT = Path("p1_receiver_access_review")
TARGET = Path("p1_receiver_access_publication")


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def audit():
    manifest = json.loads((OUT / "artifact_manifest.json").read_bytes())
    required = {
        "integrity.json", "prompt.txt", "model_metadata.json", "request.json",
        "response.json", "review.txt", "verdict.json", "review_identity.json",
    }
    if not required.issubset(manifest):
        raise ValueError("Incomplete review evidence")
    for name, expected in manifest.items():
        if Path(name).name != name:
            raise ValueError("Invalid artifact path")
        raw = (OUT / name).read_bytes()
        if len(raw) != expected["bytes"] or digest(raw) != expected["sha256"]:
            raise ValueError("Artifact mismatch: " + name)

    integrity = json.loads((OUT / "integrity.json").read_bytes())
    review = json.loads((OUT / "review_identity.json").read_bytes())
    if integrity.get("status") != "PASS" or integrity.get("scientific_execution") is not False:
        raise ValueError("Invalid integrity evidence")
    current = {
        "scientific_sha": SOURCE_COMMIT,
        "checkout_sha": subprocess.check_output(["git", "rev-parse", "HEAD"], text=True).strip(),
        "workflow_sha": os.environ.get("UQCF_WORKFLOW_SHA"),
        "run_id": os.environ.get("GITHUB_RUN_ID"),
        "run_attempt": os.environ.get("GITHUB_RUN_ATTEMPT"),
    }
    for field, value in current.items():
        if integrity.get(field) != value or review.get(field) != value:
            raise ValueError("Review/integrity identity mismatch: " + field)

    freeze_raw = FREEZE.read_bytes()
    request_raw = REQUEST.read_bytes()
    freeze = json.loads(freeze_raw)
    if freeze.get("source_commit") != SOURCE_COMMIT or list(freeze.get("documents", {})) != DOCUMENTS:
        raise ValueError("Freeze mismatch")
    docs = {}
    for path in DOCUMENTS:
        raw = Path(path).read_bytes()
        remote_raw = remote(SOURCE_COMMIT, path)
        if raw != remote_raw:
            raise ValueError("Immutable remote readback mismatch: " + path)
        blob = hashlib.sha1(("blob %d\0" % len(raw)).encode("ascii") + raw).hexdigest()
        if blob != freeze["documents"][path]:
            raise ValueError("Frozen blob mismatch: " + path)
        docs[path] = raw

    prompt = (OUT / "prompt.txt").read_bytes()
    expected_prompt = build_prompt(freeze_raw, request_raw, docs)
    if prompt != expected_prompt or digest(prompt) != review["prompt_sha256"]:
        raise ValueError("Exact prompt mismatch")

    metadata = json.loads((OUT / "model_metadata.json").read_bytes())
    if metadata.get("name") != "models/" + MODEL or "generateContent" not in metadata.get("supportedGenerationMethods", []):
        raise ValueError("Model availability evidence mismatch")
    expected_request = {
        "contents": [{"role": "user", "parts": [{"text": prompt.decode("utf-8")}]}],
        "generationConfig": {
            "temperature": 0,
            "maxOutputTokens": 32768,
            "responseMimeType": "application/json",
        },
    }
    expected_request_raw = (json.dumps(expected_request, ensure_ascii=False, sort_keys=True) + "\n").encode("utf-8")
    if (OUT / "request.json").read_bytes() != expected_request_raw:
        raise ValueError("Exact request mismatch")

    response_raw = (OUT / "response.json").read_bytes()
    if digest(response_raw) != review["response_sha256"]:
        raise ValueError("Raw response digest mismatch")
    response = json.loads(response_raw)
    returned = response.get("modelVersion")
    if returned != review.get("model_returned") or not isinstance(returned, str) or not (
        returned == MODEL or returned.startswith(MODEL + "-")
    ):
        raise ValueError("Returned model mismatch")
    if response.get("promptFeedback", {}).get("blockReason"):
        raise ValueError("Review prompt blocked")
    candidates = response.get("candidates")
    if not isinstance(candidates, list) or len(candidates) != 1 or candidates[0].get("finishReason") != "STOP":
        raise ValueError("Incomplete model response")
    answer = "\n".join(
        part["text"] for part in candidates[0]["content"]["parts"]
        if not part.get("thought", False) and isinstance(part.get("text"), str)
    ).strip().encode("utf-8")
    if answer != (OUT / "review.txt").read_bytes():
        raise ValueError("Review text mismatch")
    verdict = json.loads(answer)
    if verdict != json.loads((OUT / "verdict.json").read_bytes()):
        raise ValueError("Stored verdict mismatch")
    if verdict.get("verdict") != "ACCEPTED":
        raise ValueError("Review not accepted")
    if any(verdict.get(k) != [] for k in ("findings", "missing_assumptions", "counterexamples")):
        raise ValueError("Accepted verdict contains unresolved findings")
    if verdict.get("native_bridge_status") != "NOT_DERIVED":
        raise ValueError("Native bridge scope mismatch")

    receipt = dict(
        current,
        status="PASS",
        model=returned,
        prompt_sha256=digest(prompt),
        response_sha256=digest(response_raw),
        document_blobs=freeze["documents"],
        adverse_evidence=freeze["adverse_evidence"],
        native_bridge="NOT_DERIVED",
        scientific_execution=False,
    )
    (TARGET / "publication.json").write_text(
        json.dumps(receipt, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print("Separate P1 receiver/access publication audit PASS.")


def main():
    TARGET.mkdir(exist_ok=True)
    try:
        audit()
    except Exception as exc:
        if isinstance(exc, urllib.error.HTTPError):
            (TARGET / "http-error.bin").write_bytes(exc.read())
        (TARGET / "failure.json").write_text(
            json.dumps({
                "status": "PUBLICATION_AUDIT_FAILED",
                "error_type": type(exc).__name__,
                "http_status": getattr(exc, "code", None),
            }, indent=2) + "\n",
            encoding="utf-8",
        )
        raise SystemExit("Publication audit failed; sanitized failure and raw evidence retained.")
    finally:
        manifest = {
            p.name: {"bytes": p.stat().st_size, "sha256": digest(p.read_bytes())}
            for p in TARGET.iterdir() if p.is_file() and p.name != "artifact_manifest.json"
        }
        (TARGET / "artifact_manifest.json").write_text(
            json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8"
        )


if __name__ == "__main__":
    main()
