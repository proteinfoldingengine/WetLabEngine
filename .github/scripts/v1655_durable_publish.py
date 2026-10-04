"""Publish each original v16.55 evidence archive once; reference derived wrappers."""
from __future__ import annotations
import hashlib
import json
import os
from pathlib import Path
import re
import resource
import shutil
import sys
import urllib.error
import urllib.parse
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
AUDITED_WORKFLOW = ".github/workflows/v16.55-renewable-guard-validation.yml"
BASE = Path("ResearchHistory/UQCF-GEM/demos/v16.55-renewable-guard-repair")
PART_BYTES = 20 * 1024 * 1024
COMPONENTS = [
    {"component": "primary", "id": 11302736991, "name": f"v1655-recovery-primary-{RECOVERY_SHA}-attempt-1", "bytes": 47755058, "digest": "sha256:470e96998ecbb8b7e787a5c2b262a0f8b77c1f589bc1a47a9806f0a214620ae4"},
    {"component": "reproduction", "id": 11302517301, "name": f"v1655-recovery-reproduction-{RECOVERY_SHA}-attempt-1", "bytes": 47755038, "digest": "sha256:56d6a67414780620867a735cdcb3174fffe70ed63481936f29b29aac14ae949c"},
    {"component": "inherited", "id": 11302105924, "name": f"v1655-recovery-inherited-{RECOVERY_SHA}-attempt-1", "bytes": 317071692, "digest": "sha256:4587f585410f0237f0a95d7afb250c4b016ba01b82d230b86754d6cbb3327bcf"},
    {"component": "partial", "id": 11301163521, "name": f"v1655-recovery-partial-{RECOVERY_SHA}-attempt-1", "bytes": 190982776, "digest": "sha256:fc895cf2facc74093acd8ce9c258c4d445f6abd727c21d4ea296760e89a99b9f"},
]


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


def expected_original_names():
    suffix = f"-{AUDITED_SHA}-attempt-{AUDITED_ATTEMPT}"
    return (
        ["v1655-full-controls" + suffix]
        + [f"v1655-primary-{shard}" + suffix for shard in range(8)]
        + [f"v1655-reproduction-{shard}" + suffix for shard in range(8)]
        + ["v1655-inherited-development" + suffix]
        + [f"v1655-inherited-domain-{shard}" + suffix for shard in range(8)]
        + ["v1655-inherited-foundation" + suffix, "v1655-original-archive-audit" + suffix]
    )


def deduplicate_ledgers(ledgers):
    by_id = {}
    for ledger in ledgers:
        for supplied in ledger:
            row = {key: supplied[key] for key in ("id", "name", "digest", "bytes")}
            if type(row["id"]) is not int or type(row["bytes"]) is not int or row["bytes"] <= 0:
                raise ValueError("invalid original evidence ledger row")
            if not isinstance(row["name"], str) or not re.fullmatch("sha256:[0-9a-f]{64}", row["digest"]):
                raise ValueError("invalid original evidence ledger metadata")
            if row["id"] in by_id and by_id[row["id"]] != row:
                raise ValueError("conflicting duplicate original evidence ledger row")
            by_id[row["id"]] = row
    return sorted(by_id.values(), key=lambda row: row["id"])



def content_key(byte_count, digest):
    if type(byte_count) is not int or byte_count < 0 or not isinstance(digest, str) or not re.fullmatch("[0-9a-f]{64}", digest):
        raise ValueError("invalid content identity")
    return f"{byte_count}:{digest}"


def zip_members(archive):
    rows = []
    names = set()
    with zipfile.ZipFile(archive) as source:
        for info in source.infolist():
            if info.is_dir():
                continue
            if info.filename in names:
                raise ValueError("duplicate ZIP member name")
            names.add(info.filename)
            digest = hashlib.sha256()
            total = 0
            with source.open(info) as stream:
                for block in iter(lambda: stream.read(1024 * 1024), b""):
                    total += len(block)
                    digest.update(block)
            if total != info.file_size:
                raise ValueError("ZIP member byte length mismatch")
            rows.append({"name": info.filename, "bytes": total, "sha256": digest.hexdigest()})
    return sorted(rows, key=lambda row: row["name"])


def add_content_reference(index, byte_count, digest, reference):
    key = content_key(byte_count, digest)
    index.setdefault(key, [])
    if reference not in index[key]:
        index[key].append(reference)


def classify_wrapper_members(members, retained_names, archive_index, member_index):
    mapped = []
    for supplied in members:
        row = {key: supplied[key] for key in ("name", "bytes", "sha256")}
        key = content_key(row["bytes"], row["sha256"])
        if row["name"] in retained_names:
            classification = "RETAINED_METADATA"
            references = [{"published_name": row["name"]}]
        elif key in archive_index:
            classification = "ARCHIVE_REFERENCE"
            references = archive_index[key]
        elif key in member_index:
            classification = "MEMBER_REFERENCE"
            references = member_index[key]
        else:
            raise ValueError("unaccounted wrapper member " + row["name"])
        mapped.append({**row, "classification": classification, "references": references})
    return mapped


def mapping_stats(mapped):
    result = {}
    for row in mapped:
        item = result.setdefault(row["classification"], {"count": 0, "bytes": 0})
        item["count"] += 1
        item["bytes"] += row["bytes"]
    return result


def scalar_values(value):
    if isinstance(value, dict):
        for item in value.values():
            yield from scalar_values(item)
    elif isinstance(value, list):
        for item in value:
            yield from scalar_values(item)
    else:
        yield value

def size_inventory(originals, components, package):
    unique = sum(row["bytes"] for row in originals)
    wrappers = sum(row["bytes"] for row in components)
    recursive = package["bytes"]
    return {
        "publication_policy": "ORIGINAL_ARCHIVES_ONCE_MANIFEST_REFERENCED_WRAPPERS",
        "unique_original_count": len(originals),
        "unique_original_bytes": unique,
        "published_binary_bytes": unique,
        "recovery_component_wrapper_count": len(components),
        "recovery_component_wrapper_bytes": wrappers,
        "recursive_package_wrapper_bytes": recursive,
        "git_bytes_avoided": recursive - unique,
        "wrapper_classification": {
            "recovery_components": "DERIVED_ZIPS_PLUS_EXTRACTED_ORIGINAL_COPIES_NOT_PUBLISHED",
            "recursive_package": "COMPONENT_ZIPS_PLUS_EXTRACTED_COMPONENT_TREES_NOT_PUBLISHED",
        },
    }


def split_archive(source, destination, expected_bytes, expected_sha256, part_bytes=PART_BYTES):
    source = Path(source)
    destination = Path(destination)
    if source.stat().st_size != expected_bytes:
        raise ValueError("archive byte length mismatch")
    if sha256_file(source) != expected_sha256:
        raise ValueError("archive digest mismatch")
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
    manifest = {"format": "ordered-concatenation", "bytes": expected_bytes, "sha256": expected_sha256, "part_bytes": part_bytes, "parts": parts}
    dump(destination / "PARTS.json", manifest)
    if verify_parts(destination) != (expected_bytes, expected_sha256):
        raise ValueError("archive parts self-verification failed")
    return manifest


def verify_parts(destination):
    destination = Path(destination)
    manifest = json.loads((destination / "PARTS.json").read_text())
    expected_names = [item["name"] for item in manifest["parts"]]
    actual_names = sorted(path.name for path in destination.glob("original.zip.part*"))
    if actual_names != expected_names:
        raise ValueError("archive part inventory mismatch")
    total = 0
    result = hashlib.sha256()
    for item in manifest["parts"]:
        path = destination / item["name"]
        if path.stat().st_size != item["bytes"] or sha256_file(path) != item["sha256"]:
            raise ValueError("archive part mismatch")
        total += item["bytes"]
        with path.open("rb") as stream:
            for chunk in iter(lambda: stream.read(1024 * 1024), b""):
                result.update(chunk)
    digest = result.hexdigest()
    if total != manifest["bytes"] or digest != manifest["sha256"]:
        raise ValueError("reconstructed archive mismatch")
    return total, digest


def api(path):
    request = urllib.request.Request(
        f"https://api.github.com/repos/{REPO}/{path}",
        headers={"Authorization": "Bearer " + os.environ["GH_TOKEN"], "Accept": "application/vnd.github+json", "X-GitHub-Api-Version": "2022-11-28"},
    )
    with urllib.request.urlopen(request) as response:
        return json.load(response)


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, request, file_pointer, code, message, headers, new_url):
        return None


def download(item, destination, api_opener=None, signed_open=None, token=None):
    api_url = item["archive_download_url"]
    match = re.fullmatch(rf"https://api\.github\.com/repos/{re.escape(REPO)}/actions/artifacts/([0-9]+)/zip", api_url)
    if not match or ("id" in item and int(match.group(1)) != item["id"]):
        raise ValueError("unexpected artifact download endpoint")
    request = urllib.request.Request(
        api_url,
        headers={"Authorization": "Bearer " + (token or os.environ["GH_TOKEN"]), "Accept": "application/vnd.github+json", "X-GitHub-Api-Version": "2022-11-28"},
    )
    opener = api_opener or urllib.request.build_opener(NoRedirect)
    try:
        response = opener.open(request)
    except urllib.error.HTTPError as error:
        if error.code not in (301, 302, 303, 307, 308):
            raise
        location = error.headers.get("Location")
    else:
        response.close()
        raise ValueError("artifact endpoint did not return an inspected redirect")
    parsed = urllib.parse.urlsplit(location or "")
    if parsed.scheme != "https" or not parsed.netloc or parsed.netloc == "api.github.com":
        raise ValueError("invalid signed artifact redirect")
    signed_request = urllib.request.Request(location)
    with (signed_open or urllib.request.urlopen)(signed_request) as response, Path(destination).open("wb") as stream:
        shutil.copyfileobj(response, stream, 1024 * 1024)


def exact_artifact(metadata, expected):
    wanted = {
        "id": expected["id"],
        "name": expected["name"],
        "size_in_bytes": expected["bytes"],
        "digest": expected["digest"],
        "expired": False,
    }
    if any(metadata.get(key) != value for key, value in wanted.items()):
        raise ValueError("artifact metadata mismatch " + expected["name"])
    return metadata


def root_json(archive, destination):
    destination.mkdir(parents=True, exist_ok=False)
    values = {}
    with zipfile.ZipFile(archive) as source:
        for name in sorted(source.namelist()):
            if name.endswith(".json") and "/" not in name.strip("/"):
                data = source.read(name)
                (destination / name).write_bytes(data)
                values[name] = json.loads(data)
    return values


def prepare(request, out):
    if os.environ.get("GITHUB_ACTIONS") != "true":
        raise RuntimeError("GitHub-only durable evidence publication")
    validate_request(request)
    resource.setrlimit(resource.RLIMIT_AS, (4294967296, 4294967296))
    recovery = api(f"actions/runs/{RECOVERY_RUN}/attempts/{RECOVERY_ATTEMPT}")
    recovery_wanted = {"id": RECOVERY_RUN, "run_attempt": RECOVERY_ATTEMPT, "head_sha": RECOVERY_SHA, "path": RECOVERY_WORKFLOW, "status": "completed", "conclusion": "success"}
    if any(recovery.get(key) != value for key, value in recovery_wanted.items()):
        raise ValueError("recovery run metadata mismatch")
    original = api(f"actions/runs/{AUDITED_RUN}/attempts/{AUDITED_ATTEMPT}")
    original_wanted = {"id": AUDITED_RUN, "run_attempt": AUDITED_ATTEMPT, "head_sha": AUDITED_SHA, "path": AUDITED_WORKFLOW, "status": "completed", "conclusion": "cancelled"}
    if any(original.get(key) != value for key, value in original_wanted.items()):
        raise ValueError("original run metadata mismatch")
    recovery_artifacts = api(f"actions/runs/{RECOVERY_RUN}/artifacts?per_page=100")["artifacts"]
    original_artifacts = api(f"actions/runs/{AUDITED_RUN}/artifacts?per_page=100")["artifacts"]
    by_recovery_id = {item["id"]: item for item in recovery_artifacts}
    by_original_id = {item["id"]: item for item in original_artifacts}
    package_expected = {"id": PACKAGE_ID, "name": PACKAGE_NAME, "bytes": PACKAGE_BYTES, "digest": "sha256:" + PACKAGE_DIGEST}
    package = exact_artifact(by_recovery_id[PACKAGE_ID], package_expected)

    out = Path(out)
    out.mkdir(parents=True, exist_ok=False)
    temporary = out / "temporary"
    temporary.mkdir()
    destination = BASE / "evidence" / "recovery" / f"run-{RECOVERY_RUN}-attempt-{RECOVERY_ATTEMPT}"
    if destination.exists():
        raise ValueError("refusing to overwrite durable evidence")
    destination.mkdir(parents=True)

    ledgers = []
    component_metadata = []
    component_root = destination / "recovery-components"
    component_transports = {}
    component_members = {}
    component_retained = {}
    for expected in COMPONENTS:
        item = exact_artifact(by_recovery_id[expected["id"]], expected)
        transport = temporary / f"{expected['component']}.zip"
        download(item, transport)
        if transport.stat().st_size != expected["bytes"] or sha256_file(transport) != expected["digest"].removeprefix("sha256:"):
            raise ValueError("recovery component bytes mismatch")
        values = root_json(transport, component_root / expected["component"])
        status = values.get("STATUS.json", {})
        if status.get("status") != "PASS" or status.get("component") != expected["component"]:
            raise ValueError("recovery component terminal status mismatch")
        if "ORIGINAL_ARCHIVE_AUDIT.json" not in values:
            raise ValueError("recovery component missing original archive ledger")
        ledgers.append(values["ORIGINAL_ARCHIVE_AUDIT.json"])
        component_metadata.append({key: expected[key] for key in ("component", "id", "name", "bytes", "digest")})
        component_transports[expected["component"]] = transport
        component_members[expected["component"]] = zip_members(transport)
        component_retained[expected["component"]] = set(values)

    originals = deduplicate_ledgers(ledgers)
    if len(originals) != 28 or {row["name"] for row in originals} != set(expected_original_names()):
        raise ValueError("recovery ledgers do not cover exact original evidence inventory")
    published = []
    archive_index = {}
    original_member_index = {}
    for row in sorted(originals, key=lambda value: value["name"]):
        if row["id"] not in by_original_id:
            raise ValueError("referenced original artifact absent")
        item = exact_artifact(by_original_id[row["id"]], row)
        transport = temporary / f"original-{row['id']}.zip"
        download(item, transport)
        relative = Path("original-archives") / row["name"]
        split_archive(transport, destination / relative, row["bytes"], row["digest"].removeprefix("sha256:"))
        archive_reference = {"artifact_id": row["id"], "artifact_name": row["name"], "published_at": str(relative)}
        add_content_reference(archive_index, row["bytes"], row["digest"].removeprefix("sha256:"), archive_reference)
        for member in zip_members(transport):
            add_content_reference(
                original_member_index,
                member["bytes"],
                member["sha256"],
                {"artifact_id": row["id"], "artifact_name": row["name"], "member": member["name"]},
            )
        transport.unlink()
        published.append({**row, "published_at": str(relative)})
    if len(archive_index) != 28:
        raise ValueError("original evidence archives are not content-unique")

    component_maps = []
    component_member_index = {}
    component_archive_index = {}
    for expected in COMPONENTS:
        name = expected["component"]
        mapped = classify_wrapper_members(
            component_members[name],
            component_retained[name],
            archive_index,
            original_member_index,
        )
        for member in component_members[name]:
            add_content_reference(
                component_member_index,
                member["bytes"],
                member["sha256"],
                {"component": name, "artifact_id": expected["id"], "member": member["name"]},
            )
        add_content_reference(
            component_archive_index,
            expected["bytes"],
            expected["digest"].removeprefix("sha256:"),
            {"component": name, "artifact_id": expected["id"], "artifact_name": expected["name"]},
        )
        component_maps.append({
            "component": name,
            "wrapper": {key: expected[key] for key in ("id", "name", "bytes", "digest")},
            "retained_metadata": sorted(component_retained[name]),
            "statistics": mapping_stats(mapped),
            "members": mapped,
        })
        component_transports[name].unlink()
    component_totals = {}
    for item in component_maps:
        for classification, values in item["statistics"].items():
            total = component_totals.setdefault(classification, {"count": 0, "bytes": 0})
            total["count"] += values["count"]
            total["bytes"] += values["bytes"]
    expected_component_totals = {
        "ARCHIVE_REFERENCE": {"count": 28, "bytes": 301804233},
        "MEMBER_REFERENCE": {"count": 2217, "bytes": 583060369},
        "RETAINED_METADATA": {"count": 22, "bytes": 188702},
    }
    if component_totals != expected_component_totals:
        raise ValueError("component duplication inventory mismatch")
    dump(destination / "COMPONENT_DUPLICATION_MAP.json", {"status": "PASS", "totals": component_totals, "components": component_maps})

    package_transport = temporary / "recovery-package.zip"
    download(package, package_transport)
    if package_transport.stat().st_size != PACKAGE_BYTES or sha256_file(package_transport) != PACKAGE_DIGEST:
        raise ValueError("recovery package bytes mismatch")
    package_metadata_dir = destination / "recovery-package-metadata"
    package_values = root_json(package_transport, package_metadata_dir)
    required_package_metadata = {"STATUS.json", "DURABLE_MANIFEST.json", "COMPONENT_ARTIFACTS.json"}
    if set(package_values) != required_package_metadata:
        raise ValueError("recovery package root metadata inventory mismatch")
    if package_values["STATUS.json"].get("status") != "PASS":
        raise ValueError("recovery package status is not PASS")
    component_scalars = set(scalar_values(package_values["COMPONENT_ARTIFACTS.json"]))
    for expected in COMPONENTS:
        if not {expected["id"], expected["name"], expected["bytes"], expected["digest"]}.issubset(component_scalars):
            raise ValueError("recovery package component reference mismatch")
    package_members = zip_members(package_transport)
    package_mapped = classify_wrapper_members(
        package_members,
        required_package_metadata,
        component_archive_index,
        component_member_index,
    )
    package_map = {
        "status": "PASS",
        "wrapper": {"id": PACKAGE_ID, "name": PACKAGE_NAME, "bytes": PACKAGE_BYTES, "digest": "sha256:" + PACKAGE_DIGEST},
        "retained_metadata": sorted(required_package_metadata),
        "statistics": mapping_stats(package_mapped),
        "members": package_mapped,
    }
    dump(destination / "PACKAGE_DUPLICATION_MAP.json", package_map)
    package_transport.unlink()

    wrapper_reference = {
        "recovery_components": component_metadata,
        "recovery_package": {key: package_expected[key] for key in ("id", "name", "bytes", "digest")},
        "policy": "EXACT_WRAPPER_BYTES_REFERENCED_NOT_RECURSIVELY_EMBEDDED",
    }
    dump(destination / "ORIGINAL_EVIDENCE_INVENTORY.json", published)
    dump(destination / "DERIVED_WRAPPER_REFERENCES.json", wrapper_reference)
    inventory = size_inventory(published, COMPONENTS, {"bytes": PACKAGE_BYTES})
    inventory.update({
        "component_uncompressed_duplication": component_totals,
        "package_uncompressed_duplication": package_map["statistics"],
        "retained_component_metadata_files": component_totals["RETAINED_METADATA"]["count"],
        "retained_package_metadata_files": len(required_package_metadata),
        "temporary_transport_directory": "out/preserve/temporary (removed before publication)",
    })
    dump(destination / "SIZE_HASH_INVENTORY.json", inventory)

    reconstructed = []
    for row in published:
        size, digest = verify_parts(destination / row["published_at"])
        reconstructed.append({"id": row["id"], "name": row["name"], "bytes": size, "sha256": digest})
    reconstruction = {
        "status": "PASS",
        "mode": "BYTE_EXACT_ORIGINAL_ARCHIVES_PLUS_COMPLETE_WRAPPER_PAYLOAD_MAP",
        "count": len(reconstructed),
        "bytes": sum(row["bytes"] for row in reconstructed),
        "artifacts": reconstructed,
        "component_payload_accounting": {"status": "PASS", "members": sum(sum(v["count"] for v in item["statistics"].values()) for item in component_maps), "totals": component_totals},
        "package_payload_accounting": {"status": "PASS", "members": len(package_mapped), "totals": package_map["statistics"]},
        "retained_metadata": {"component_files": 22, "package_files": 3},
        "wrapper_zip_encodings": "NOT_REPRODUCED; EXACT GITHUB ARTIFACT ID_SIZE_SHA256 REFERENCES RETAINED",
        "recovery_package": "DERIVED_RECURSIVE_WRAPPER_NOT_EMBEDDED",
        "scientific_execution": "NOT_RERUN",
    }
    if reconstruction["count"] != 28 or reconstruction["bytes"] != 301804233:
        raise ValueError("complete original evidence reconstruction mismatch")
    dump(destination / "RECONSTRUCTION.json", reconstruction)
    receipt = {
        "status": "ORIGINAL_ARCHIVES_ONCE_AND_ALL_WRAPPER_MEMBERS_ACCOUNTED",
        "audited_run": original,
        "recovery_run": recovery,
        "publication_workflow_sha": os.environ["GITHUB_WORKFLOW_SHA"],
        "publication_event_sha": os.environ["GITHUB_SHA"],
        "publication_run": os.environ["GITHUB_RUN_ID"],
        "publication_attempt": os.environ["GITHUB_RUN_ATTEMPT"],
        "numbered_certification": "PENDING_REVIEW_MERGE_AND_ACTUAL_MERGE_AUDIT",
    }
    dump(destination / "PUBLICATION_RECEIPT.json", receipt)
    files = {str(path.relative_to(destination)): sha256_file(path) for path in sorted(destination.rglob("*")) if path.is_file()}
    dump(destination / "PUBLICATION_MANIFEST.json", files)
    (out / "DESTINATION.txt").write_text(str(destination) + "\n")
    receipt_out = out / "receipt"
    receipt_out.mkdir()
    for name in (
        "ORIGINAL_EVIDENCE_INVENTORY.json",
        "DERIVED_WRAPPER_REFERENCES.json",
        "SIZE_HASH_INVENTORY.json",
        "COMPONENT_DUPLICATION_MAP.json",
        "PACKAGE_DUPLICATION_MAP.json",
        "RECONSTRUCTION.json",
        "PUBLICATION_RECEIPT.json",
        "PUBLICATION_MANIFEST.json",
    ):
        shutil.copyfile(destination / name, receipt_out / name)
    shutil.rmtree(temporary)
    return destination

if __name__ == "__main__":
    prepare(json.loads(Path(sys.argv[1]).read_text()), sys.argv[2])
