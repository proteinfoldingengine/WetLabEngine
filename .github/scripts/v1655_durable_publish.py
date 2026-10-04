"""Durably preserve the exact v16.55 recovery package without rerunning science."""
from __future__ import annotations
import hashlib
import json
import os
from pathlib import Path
import re
import resource
import shutil
import sys
import urllib.request
import zipfile

REPO = "proteinfoldingengine/WetLabEngine"
RECOVERY_RUN = 37196753029
RECOVERY_ATTEMPT = 1
RECOVERY_SHA = "a75c82f31c5547bf20feb75960fbedf2f7e5c0a6"
RECOVERY_WORKFLOW = ".github/workflows/v16.55-publication-recovery.yml"
PACKAGE_ID = 11301883937
PACKAGE_BYTES = 1207019319
PACKAGE_DIGEST = "ca76f0dbc839c3899f0162cf7475c06f69ef8c7f7e22b11ebc1e6199606b0bbe"
PACKAGE_NAME = f"v1655-recovery-package-{RECOVERY_SHA}-attempt-{RECOVERY_ATTEMPT}"
AUDITED_RUN = 37180275767
AUDITED_SHA = "60c48b818366354d26366af35726788553865455"
AUDITED_ATTEMPT = 1
BASE = Path("ResearchHistory/UQCF-GEM/demos/v16.55-renewable-guard-repair")
PART_BYTES = 20 * 1024 * 1024


def serial(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"), allow_nan=False)


def dump(path, value):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(serial(value) + "\n")


def sha256_bytes(value):
    return hashlib.sha256(value).hexdigest()


def sha256_file(path):
    result = hashlib.sha256()
    with Path(path).open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            result.update(chunk)
    return result.hexdigest()


def validate_request(value):
    expected = {
        "recovery_run_id": RECOVERY_RUN,
        "recovery_attempt": RECOVERY_ATTEMPT,
        "recovery_sha": RECOVERY_SHA,
        "package_artifact_id": PACKAGE_ID,
        "package_artifact_bytes": PACKAGE_BYTES,
        "package_artifact_digest": "sha256:" + PACKAGE_DIGEST,
        "audited_run_id": AUDITED_RUN,
        "audited_sha": AUDITED_SHA,
        "audited_attempt": AUDITED_ATTEMPT,
    }
    if set(value) != set(expected) | {"source_parent"}:
        raise ValueError("wrong durable publication request fields")
    for key, expected_value in expected.items():
        if value.get(key) != expected_value:
            raise ValueError("wrong durable publication request " + key)
    if not isinstance(value.get("source_parent"), str) or not re.fullmatch("[0-9a-f]{40}", value["source_parent"]):
        raise ValueError("wrong durable publication source_parent")
    return value


def split_archive(source, destination, expected_bytes, expected_sha256, part_bytes=PART_BYTES):
    source = Path(source)
    destination = Path(destination)
    if source.stat().st_size != expected_bytes:
        raise ValueError("package archive byte length mismatch")
    if sha256_file(source) != expected_sha256:
        raise ValueError("package archive digest mismatch")
    destination.mkdir(parents=True, exist_ok=False)
    parts = []
    with source.open("rb") as stream:
        index = 0
        while True:
            block = stream.read(part_bytes)
            if not block:
                break
            name = f"original.zip.part{index:04d}"
            path = destination / name
            path.write_bytes(block)
            parts.append({"name": name, "bytes": len(block), "sha256": sha256_bytes(block)})
            index += 1
    manifest = {
        "format": "ordered-concatenation",
        "bytes": expected_bytes,
        "sha256": expected_sha256,
        "part_bytes": part_bytes,
        "parts": parts,
    }
    dump(destination / "PARTS.json", manifest)
    if verify_parts(destination) != (expected_bytes, expected_sha256):
        raise ValueError("package parts self-verification failed")
    return manifest


def verify_parts(destination):
    destination = Path(destination)
    manifest = json.loads((destination / "PARTS.json").read_text())
    expected_names = [item["name"] for item in manifest["parts"]]
    actual_names = sorted(path.name for path in destination.glob("original.zip.part*"))
    if actual_names != expected_names:
        raise ValueError("package part inventory mismatch")
    total = 0
    result = hashlib.sha256()
    for item in manifest["parts"]:
        path = destination / item["name"]
        if path.stat().st_size != item["bytes"] or sha256_file(path) != item["sha256"]:
            raise ValueError("package part mismatch")
        total += item["bytes"]
        with path.open("rb") as stream:
            for chunk in iter(lambda: stream.read(1024 * 1024), b""):
                result.update(chunk)
    digest = result.hexdigest()
    if total != manifest["bytes"] or digest != manifest["sha256"]:
        raise ValueError("reconstructed package mismatch")
    return total, digest


def api(path):
    request = urllib.request.Request(
        f"https://api.github.com/repos/{REPO}/{path}",
        headers={
            "Authorization": "Bearer " + os.environ["GH_TOKEN"],
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
        },
    )
    with urllib.request.urlopen(request) as response:
        return json.load(response)


def download(item, destination):
    request = urllib.request.Request(
        item["archive_download_url"],
        headers={
            "Authorization": "Bearer " + os.environ["GH_TOKEN"],
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
        },
    )
    with urllib.request.urlopen(request) as response, Path(destination).open("wb") as stream:
        shutil.copyfileobj(response, stream, 1024 * 1024)


def prepare(request, out):
    if os.environ.get("GITHUB_ACTIONS") != "true":
        raise RuntimeError("GitHub-only durable evidence publication")
    validate_request(request)
    resource.setrlimit(resource.RLIMIT_AS, (4294967296, 4294967296))
    metadata = api(f"actions/runs/{RECOVERY_RUN}/attempts/{RECOVERY_ATTEMPT}")
    wanted_run = {
        "id": RECOVERY_RUN,
        "run_attempt": RECOVERY_ATTEMPT,
        "head_sha": RECOVERY_SHA,
        "path": RECOVERY_WORKFLOW,
        "status": "completed",
        "conclusion": "success",
    }
    if any(metadata.get(key) != value for key, value in wanted_run.items()):
        raise ValueError("recovery run metadata mismatch")
    artifacts = api(f"actions/runs/{RECOVERY_RUN}/artifacts?per_page=100")["artifacts"]
    candidates = [item for item in artifacts if item["id"] == PACKAGE_ID and item["name"] == PACKAGE_NAME and not item["expired"]]
    if len(candidates) != 1:
        raise ValueError("package artifact unavailable or ambiguous")
    item = candidates[0]
    if item["size_in_bytes"] != PACKAGE_BYTES or item["digest"] != "sha256:" + PACKAGE_DIGEST:
        raise ValueError("package artifact metadata mismatch")
    out = Path(out)
    out.mkdir(parents=True, exist_ok=False)
    transport = out / "package.zip"
    download(item, transport)
    destination = BASE / "evidence" / "recovery" / f"run-{RECOVERY_RUN}-attempt-{RECOVERY_ATTEMPT}"
    if destination.exists():
        raise ValueError("refusing to overwrite durable evidence")
    destination.mkdir(parents=True)
    split_archive(transport, destination / "package-archive", PACKAGE_BYTES, PACKAGE_DIGEST)
    with zipfile.ZipFile(transport) as archive:
        names = set(archive.namelist())
        for name in ("STATUS.json", "DURABLE_MANIFEST.json", "COMPONENT_ARTIFACTS.json"):
            if name not in names:
                raise ValueError("package metadata missing " + name)
            (destination / name).write_bytes(archive.read(name))
    transport.unlink()
    status = json.loads((destination / "STATUS.json").read_text())
    if status.get("status") != "PASS" or status.get("component") != "package":
        raise ValueError("package terminal status mismatch")
    if status.get("audited", {}).get("run_id") != AUDITED_RUN or status.get("audited", {}).get("sha") != AUDITED_SHA:
        raise ValueError("package audited provenance mismatch")
    if status.get("recovery", {}).get("run_id") != str(RECOVERY_RUN) or status.get("recovery", {}).get("sha") != RECOVERY_SHA:
        raise ValueError("package recovery provenance mismatch")
    if status.get("numbered_certification") != "PENDING_DURABLE_GIT_PUBLICATION_REVIEW_MERGE_AND_ACTUAL_MERGE_AUDIT":
        raise ValueError("package prematurely certified")
    dump(destination / "PACKAGE_ARTIFACT.json", item)
    receipt = {
        "status": "ORIGINAL_PACKAGE_BYTES_VERIFIED",
        "recovery_run": metadata,
        "package_artifact": item,
        "publication_workflow_sha": os.environ["GITHUB_WORKFLOW_SHA"],
        "publication_event_sha": os.environ["GITHUB_SHA"],
        "publication_run": os.environ["GITHUB_RUN_ID"],
        "publication_attempt": os.environ["GITHUB_RUN_ATTEMPT"],
        "audited_run_id": AUDITED_RUN,
        "audited_sha": AUDITED_SHA,
        "audited_attempt": AUDITED_ATTEMPT,
        "numbered_certification": "PENDING_REVIEW_MERGE_AND_ACTUAL_MERGE_AUDIT",
    }
    dump(destination / "PUBLICATION_RECEIPT.json", receipt)
    files = {str(path.relative_to(destination)): sha256_file(path) for path in sorted(destination.rglob("*")) if path.is_file()}
    dump(destination / "PUBLICATION_MANIFEST.json", files)
    (out / "DESTINATION.txt").write_text(str(destination) + "\n")
    receipt_out = out / "receipt"
    receipt_out.mkdir()
    for name in ("STATUS.json", "PACKAGE_ARTIFACT.json", "PUBLICATION_RECEIPT.json", "PUBLICATION_MANIFEST.json"):
        shutil.copyfile(destination / name, receipt_out / name)
    shutil.copyfile(destination / "package-archive" / "PARTS.json", receipt_out / "PARTS.json")
    return destination


if __name__ == "__main__":
    prepare(json.loads(Path(sys.argv[1]).read_text()), sys.argv[2])
