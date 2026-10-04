"""Partitioned audit of immutable v16.55 artifacts after publication timeout.

This adapter never executes a new scientific identity.  It checks out and
imports the immutable audited commit, downloads the original archives, and
repeats the accepted independent reconstruction with an explicit archived
run context.  Actual recovery provenance is recorded separately; GITHUB_*
variables are never rewritten to historical values.
"""
from __future__ import annotations

import argparse
import ast
from collections import Counter
from dataclasses import dataclass
import gzip
import hashlib
from itertools import zip_longest
import json
import os
from pathlib import Path, PurePosixPath
import re
import resource
import subprocess
import sys
import urllib.error
import urllib.parse
import urllib.request
import zipfile

REPO = "proteinfoldingengine/WetLabEngine"
AUDITED_RUN = 37180275767
AUDITED_SHA = "60c48b818366354d26366af35726788553865455"
AUDITED_ATTEMPT = 1
AUDITED_WORKFLOW = ".github/workflows/v16.55-renewable-guard-validation.yml"
CERTIFIED_PARENT = "466aa8a6d55a9b21cbf6bfe8a34dd8e6f5c6946f"
PREREG = "891470cfc817f26d9721f96278b2c0f8652c3fdf"
BASE = Path("ResearchHistory/UQCF-GEM/demos/v16.55-renewable-guard-repair")
V154 = Path("ResearchHistory/UQCF-GEM/demos/v16.54-parent-support-connectivity")
BASELINE_MANIFEST = V154 / "evidence/validated/run-37059520424-attempt-1/SCIENTIFIC_MANIFEST.json"
BASELINE_BLOB = "f5cd6b94c506d7fef457ae6072a4dc3319454639"
TEST_BLOBS = {
    "test_campaign.py": "9bfd5287119275b19372c954eeec303317cde049",
    "test_publication.py": "c1f043cbd0190d655fa6a9af7ef254d1560ee419",
    "test_review.py": "3ce6597e4adce936968a85cac727f7a21aeda8af",
    "test_task1.py": "f40877df0229fd65881a8ef37983f80092519f3e",
    "test_task2.py": "962e67e2d1d7549fbc85bd1a98032b5308af7a99",
    "test_task3.py": "5ce7c032e30fe51827fecebbf5a8a8497bad130f",
}


def serial(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"), allow_nan=False)


def dump(path, value):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(serial(value) + "\n")


def digest(path):
    result = hashlib.sha256()
    with Path(path).open("rb") as stream:
        for chunk in iter(lambda: stream.read(1048576), b""):
            result.update(chunk)
    return result.hexdigest()


@dataclass(frozen=True)
class AuditContext:
    run_id: int
    sha: str
    attempt: int
    workflow: str
    certified_parent: str

    def as_dict(self):
        return {
            "run_id": self.run_id,
            "sha": self.sha,
            "attempt": self.attempt,
            "workflow": self.workflow,
            "certified_parent": self.certified_parent,
        }


def validate_request(value):
    required = {
        "audited_run_id": AUDITED_RUN,
        "audited_sha": AUDITED_SHA,
        "audited_attempt": AUDITED_ATTEMPT,
        "audited_workflow": AUDITED_WORKFLOW,
        "certified_parent": CERTIFIED_PARENT,
        "mode": "publication_recovery",
    }
    for key, expected in required.items():
        if value.get(key) != expected:
            raise ValueError("wrong recovery request " + key)
    return AuditContext(AUDITED_RUN, AUDITED_SHA, AUDITED_ATTEMPT, AUDITED_WORKFLOW, CERTIFIED_PARENT)


def validate_original_run(metadata, context):
    expected = {
        "id": context.run_id,
        "run_attempt": context.attempt,
        "head_sha": context.sha,
        "path": context.workflow,
        "status": "completed",
        "conclusion": "cancelled",
    }
    if any(metadata.get(key) != value for key, value in expected.items()):
        raise ValueError("audited original run metadata mismatch")


def original_artifact_name(stem, context):
    return f"{stem}-{context.sha}-attempt-{context.attempt}"


def validate_current_run(metadata, context, provenance):
    """Bind a live audit to its actual event, not the historical recovery tuple."""
    expected = {"id": context.run_id, "run_attempt": context.attempt,
                "head_sha": context.sha, "path": context.workflow}
    actual = {"run_id": str(context.run_id), "attempt": str(context.attempt),
              "sha": context.sha, "workflow_sha": context.sha}
    if any(metadata.get(key) != value for key, value in expected.items()) or provenance != actual:
        raise ValueError("current run identity/provenance mismatch")
    if (metadata.get("status"), metadata.get("conclusion")) not in (
        ("in_progress", None), ("completed", "success")
    ):
        raise ValueError("current run is failed, cancelled or not executing")


def validate_current_jobs(jobs, component, context):
    required = {
        "primary": ["controls"] + [f"domains ({i})" for i in range(8)],
        "reproduction": [f"reproduction ({i})" for i in range(8)],
        "inherited": ["controls", "inherited-development", "inherited-foundation"]
                     + [f"inherited-domains ({i})" for i in range(8)],
        "package": ["audit-primary", "audit-reproduction", "audit-inherited"],
    }
    if component not in required:
        raise ValueError("unknown current audit component")
    for name in required[component]:
        rows = [row for row in jobs if row.get("name") == name]
        expected = {"run_id": context.run_id, "run_attempt": context.attempt,
                    "head_sha": context.sha, "status": "completed", "conclusion": "success"}
        if len(rows) != 1 or any(rows[0].get(key) != value for key, value in expected.items()):
            raise ValueError("missing/ambiguous/unsuccessful current producing job " + name)


def validate_current_artifact(item, context):
    run = item.get("workflow_run", {})
    if (run.get("id") != context.run_id or run.get("head_sha") != context.sha
        or item.get("expired") is not False
        or not item.get("name", "").endswith(f"-{context.sha}-attempt-{context.attempt}")
        or type(item.get("id")) is not int or item["id"] <= 0
        or type(item.get("size_in_bytes")) is not int or item["size_in_bytes"] <= 0
        or not re.fullmatch(r"sha256:[0-9a-f]{64}", str(item.get("digest", "")))):
        raise ValueError("current artifact identity/length/digest mismatch")


def recovery_provenance():
    if os.environ.get("GITHUB_ACTIONS") != "true":
        raise RuntimeError("GitHub only")
    result = {
        "run_id": os.environ["GITHUB_RUN_ID"],
        "attempt": os.environ["GITHUB_RUN_ATTEMPT"],
        "sha": os.environ["GITHUB_SHA"],
        "workflow_sha": os.environ["GITHUB_WORKFLOW_SHA"],
    }
    if result["sha"] != result["workflow_sha"] or not re.fullmatch(r"[0-9a-f]{40}", result["sha"]):
        raise ValueError("actual recovery provenance mismatch")
    return result


def validate_component_status(status, component, context, recovery):
    if status.get("status") != "PASS" or status.get("component") != component:
        raise ValueError("component not terminal PASS")
    if status.get("audited") != context.as_dict() or status.get("recovery") != recovery:
        raise ValueError("component provenance mismatch")


def compare_scientific_bytes(primary, reproduction):
    if primary != reproduction:
        raise ValueError("primary/reproduction deterministic scientific bytes differ")


def validate_inherited_baseline(expected_ids, actual_ids, expected_hashes, actual_hashes):
    if len(expected_ids) != 83 or Counter(expected_ids) != Counter(actual_ids):
        raise ValueError("inherited 83-control identity mismatch")
    if len(expected_hashes) != 77 or expected_hashes != actual_hashes:
        raise ValueError("inherited 77-hash baseline mismatch")


def validate_exact_source_manifest(recorded, actual, expected):
    if recorded != expected or actual != expected:
        raise ValueError("inherited domain exact archived source mismatch")


def domain_source_relatives(paths, base):
    prefix = str(base).rstrip("/") + "/"
    result = []
    for path in paths:
        if not path.startswith(prefix):
            raise ValueError("source path outside inherited base")
        relative = path[len(prefix):]
        parts = PurePosixPath(relative).parts
        wanted = (
            len(parts) == 1
            and (relative.endswith(".py") or relative.endswith(".md") or relative == "protocol.json")
        ) or (
            len(parts) == 2 and parts[0] == "tests" and relative.endswith(".py")
        )
        if wanted:
            result.append(relative)
    return result


def validate_foundation_metadata(metadata, context):
    expected = {
        "head": context.sha,
        "workflow_sha": context.sha,
        "trigger_sha": context.sha,
        "run_id": str(context.run_id),
        "run_attempt": str(context.attempt),
        "verified_parent": "b6bf95798ec5892963c29f4020f8b75069fd2e3b",
        "preregistration": "8fcc46597ab7c2b83fe9dd2fd0611a07e66169cd",
    }
    if any(str(metadata.get(key)) != str(value) for key, value in expected.items()):
        raise ValueError("inherited foundation original provenance mismatch")


def api(path):
    request = urllib.request.Request(
        f"https://api.github.com/repos/{REPO}/{path}",
        headers={
            "Accept": "application/vnd.github+json",
            "Authorization": "Bearer " + os.environ["GH_TOKEN"],
            "X-GitHub-Api-Version": "2022-11-28",
        },
    )
    with urllib.request.urlopen(request) as response:
        return json.load(response)


def download_artifact(item, destination):
    destination = Path(destination)
    destination.parent.mkdir(parents=True, exist_ok=True)
    wanted = f"https://api.github.com/repos/{REPO}/actions/artifacts/{item['id']}/zip"
    if item["archive_download_url"] != wanted:
        raise ValueError("artifact repository endpoint mismatch")
    request = urllib.request.Request(wanted, headers={"Authorization": "Bearer " + os.environ["GH_TOKEN"]})

    class NoRedirect(urllib.request.HTTPRedirectHandler):
        def redirect_request(self, req, fp, code, msg, headers, newurl):
            return None

    try:
        response = urllib.request.build_opener(NoRedirect()).open(request)
    except urllib.error.HTTPError as error:
        if error.code not in (301, 302, 303, 307, 308):
            raise
        location = error.headers["Location"]
        if urllib.parse.urlparse(location).scheme != "https":
            raise ValueError("artifact redirect is not HTTPS")
        response = urllib.request.urlopen(location)
    with response, destination.open("wb") as output:
        for chunk in iter(lambda: response.read(1048576), b""):
            output.write(chunk)
    if item["digest"] != "sha256:" + digest(destination) or item["size_in_bytes"] != destination.stat().st_size:
        raise ValueError("external artifact digest/length mismatch")
    folder = destination.with_suffix("")
    folder.mkdir(exist_ok=False)
    with zipfile.ZipFile(destination) as archive:
        for entry in archive.infolist():
            member = PurePosixPath(entry.filename)
            if member.is_absolute() or ".." in member.parts or "\\" in entry.filename:
                raise ValueError("unsafe archive member")
        archive.extractall(folder)
    return folder


def original_inventory(context, out):
    metadata = api(f"actions/runs/{context.run_id}")
    validate_original_run(metadata, context)
    artifacts = []
    page = 1
    while True:
        response = api(f"actions/runs/{context.run_id}/artifacts?per_page=100&page={page}")
        artifacts.extend(response["artifacts"])
        if len(response["artifacts"]) < 100:
            break
        page += 1
    dump(Path(out) / "ORIGINAL_RUN.json", metadata)
    dump(Path(out) / "ORIGINAL_ARTIFACTS.json", artifacts)
    return artifacts


def obtain(stem, destination, context, artifacts, ledger):
    name = original_artifact_name(stem, context)
    candidates = [item for item in artifacts if item["name"] == name and not item["expired"]]
    if len(candidates) != 1:
        raise ValueError("missing/ambiguous original artifact " + name)
    item = candidates[0]
    archive = Path(destination).parent / (Path(destination).name + ".zip")
    folder = download_artifact(item, archive)
    Path(destination).parent.mkdir(parents=True, exist_ok=True)
    folder.rename(destination)
    ledger.append({
        "id": item["id"], "name": name, "digest": item["digest"],
        "bytes": item["size_in_bytes"], "local_archive": str(archive),
    })
    return Path(destination)


def bind_original_checkout(repo_root, context):
    repo_root = Path(repo_root).resolve()
    head = subprocess.check_output(["git", "-C", repo_root, "rev-parse", "HEAD"], text=True).strip()
    if head != context.sha:
        raise ValueError("immutable original checkout mismatch")
    for ancestor in (PREREG, context.certified_parent):
        subprocess.run(["git", "-C", repo_root, "merge-base", "--is-ancestor", ancestor, head], check=True)
    return repo_root


def git_bytes(root, ref, path):
    return subprocess.check_output(["git", "-C", root, "show", f"{ref}:{path}"])


def git_blob(root, ref, path):
    return subprocess.check_output(["git", "-C", root, "rev-parse", f"{ref}:{path}"], text=True).strip()


def load_v1655(root):
    base = root / BASE
    sys.path.insert(0, str(base))
    import campaign
    import verifier
    return base, campaign, verifier


def aggregate_mode_explicit(root, mode_root, output, context):
    base, campaign, verifier = load_v1655(root)
    expected = campaign.ordered_domain(verifier.reconstruct_cases)
    errors, identities = [], []
    counts, vertices, compressed, manifests = Counter(), 0, 0, {}
    whole_hash = hashlib.sha256((campaign.serial([case["identity"] for case in expected]) + "\n").encode()).hexdigest()
    source_expected = {}
    paths = [*base.glob("*.py"), *base.glob("*.md"), *base.glob("*.json"), *base.glob("tests/*.py"), *base.glob("analytical/*.md")]
    for path in sorted(paths):
        if path.name.endswith("REQUEST.json"):
            continue
        rel = str(path.relative_to(base))
        if path.read_bytes() != git_bytes(root, context.sha, str(path.relative_to(root))):
            raise ValueError("original scientific source differs from immutable Git")
        source_expected[rel] = hashlib.sha256(path.read_bytes()).hexdigest()
    protocol = json.loads((base / "protocol.json").read_text())
    wanted_provenance = {
        "scientific_sha": context.sha, "workflow_sha": context.sha,
        "run_id": str(context.run_id), "attempt": str(context.attempt),
        "preregistration_sha": PREREG,
        "approved_protocol_sha256": protocol["approved_protocol_sha256"],
    }
    scientific_bytes = {}
    for shard in range(8):
        directory = Path(mode_root) / f"shard-{shard}"
        summary = json.loads((directory / "SUMMARY.json").read_text())
        manifest = json.loads((directory / "SCIENCE_MANIFEST.json").read_text())
        if set(manifest) != {"records.jsonl.gz", "identities.jsonl.gz", "SUMMARY.json", "DOMAIN_FREEZE.json"}:
            errors.append("wrong science inventory")
        errors += verifier.verify_manifest({name: (directory / name).read_bytes() for name in manifest}, manifest)
        provenance = json.loads((directory / "PROVENANCE.json").read_text())
        errors += verifier.verify_provenance(provenance, wanted_provenance)
        recorded = json.loads((directory / "SOURCE_MANIFEST.json").read_text())
        archived = {str(path.relative_to(directory / "source")): path.read_bytes() for path in (directory / "source").rglob("*") if path.is_file()}
        if recorded != source_expected:
            errors.append("executing source inventory mismatch")
        errors += verifier.verify_manifest(archived, source_expected)
        if summary["status"] != "PASS" or summary["checked"] != summary["expected"]:
            errors.append("unfinished shard")
        start, stop = len(expected) * shard // 8, len(expected) * (shard + 1) // 8
        if (summary["shard"], summary["shards"], summary["total"], summary["start"], summary["stop"]) != (shard, 8, len(expected), start, stop):
            errors.append("wrong interval")
        freeze = dict(shard=shard, shards=8, total=len(expected), start=start, stop=stop, whole_universe_sha256=whole_hash, first=expected[start]["identity"], last=expected[stop - 1]["identity"])
        if json.loads((directory / "DOMAIN_FREEZE.json").read_text()) != freeze or summary["whole_universe_sha256"] != whole_hash:
            errors.append("wrong full domain freeze")
        actual = list(campaign.read_records(directory, "identities.jsonl.gz"))
        errors += verifier.verify_universe([case["identity"] for case in expected[start:stop]], actual)
        shardcounts, shardrefusals = Counter(), Counter()
        shardvertices = checked = 0
        for entry, case in zip_longest(campaign.read_records(directory, "records.jsonl.gz"), expected[start:stop]):
            if entry is None or case is None:
                errors.append("record cardinality mismatch")
                continue
            if entry["case"] != case or entry["record"]["identity"] != case["identity"]:
                errors.append("substituted full input")
                continue
            errors += verifier.verify_record(case, entry["record"])
            shardcounts.update(campaign.diagnostic(case, entry["record"]))
            amount = campaign.science_count(entry["record"])
            shardvertices += amount
            if amount > 1000000:
                errors.append("serialized identity resource bound")
            if entry["record"]["status"] != "PATH":
                shardrefusals[entry["record"]["status"]] += 1
            checked += 1
        shardbytes = sum((directory / name).stat().st_size for name in [*manifest, "SCIENCE_MANIFEST.json"])
        if checked != summary["checked"] or dict(shardcounts) != summary["diagnostics"] or dict(shardrefusals) != summary["refusals"] or shardvertices != summary["serialized_vertices"] or shardbytes != summary["compressed_bytes"]:
            errors.append("fabricated shard counters")
        if summary.get("common_degree_greedy_transfers") != 0 or summary.get("strict_slack_X15S_exercised") is not False:
            errors.append("fabricated strict-slack witness")
        for name, value in manifest.items():
            scientific_bytes[f"{shard}/{name}"] = value
        identities.extend(actual); counts.update(shardcounts); vertices += shardvertices; compressed += shardbytes; manifests[str(shard)] = manifest
    errors += verifier.verify_universe([case["identity"] for case in expected], identities)
    missing = verifier.verify_diagnostics(counts, campaign.REQUIRED)
    if vertices > campaign.MAX_VERTICES or compressed > campaign.MAX_BYTES:
        missing.append("whole campaign resource bound")
    result = dict(status="FAIL" if errors else "INCOMPLETE" if missing else "PASS", expected=len(expected), checked=len(identities), errors=errors, incomplete=missing, diagnostics=dict(counts), serialized_vertices=vertices, compressed_bytes=compressed, shard_manifests=manifests, common_degree_greedy_transfers=0, strict_slack_X15S_exercised=False)
    dump(Path(output) / "AGGREGATE.json", result)
    dump(Path(output) / "SCIENTIFIC_BYTES.json", scientific_bytes)
    if result["status"] != "PASS":
        raise ValueError("complete explicit-context aggregate failed")


def audit_mode(args, context, recovery):
    root = bind_original_checkout(args.repo, context)
    out = Path(args.out); out.mkdir(parents=True, exist_ok=True)
    dump(out / "STATUS.json", {"status": "INCOMPLETE", "component": args.component})
    artifacts = original_inventory(context, out); ledger = []
    mode_root = out / "originals"
    for shard in range(8):
        obtain(f"v1655-{args.component}-{shard}", mode_root / f"shard-{shard}", context, artifacts, ledger)
    aggregate_mode_explicit(root, mode_root, out, context)
    dump(out / "ORIGINAL_ARCHIVE_AUDIT.json", ledger)
    dump(out / "STATUS.json", {"status": "PASS", "component": args.component, "audited": context.as_dict(), "recovery": recovery})


def expected_control_ids(root):
    ids = []
    for name, blob in TEST_BLOBS.items():
        path = V154 / "tests" / name
        if git_blob(root, CERTIFIED_PARENT, str(path)) != blob:
            raise ValueError("certified control-source blob mismatch")
        tree = ast.parse(git_bytes(root, CERTIFIED_PARENT, str(path)))
        module = Path(name).stem
        for node in tree.body:
            if isinstance(node, ast.ClassDef):
                ids.extend(f"{module}.{node.name}.{child.name}" for child in node.body if isinstance(child, (ast.FunctionDef, ast.AsyncFunctionDef)) and child.name.startswith("test_"))
    if len(ids) != 83 or len(set(ids)) != 83:
        raise ValueError("certified control-source identity count")
    return ids


def actual_control_ids(log):
    rows = re.findall(r"^(test_[A-Za-z0-9_]+) \(([A-Za-z0-9_.]+)\) \.\.\. (\S+)$", log, re.M)
    if any(outcome != "ok" for _, _, outcome in rows) or "Ran 83 tests" not in log or "\nOK\n" not in log:
        raise ValueError("inherited development log is not complete green")
    return [qualified for _, qualified, _ in rows]


def baseline_hashes(root):
    path = str(BASELINE_MANIFEST)
    if git_blob(root, CERTIFIED_PARENT, path) != BASELINE_BLOB:
        raise ValueError("certified scientific baseline blob mismatch")
    value = json.loads(git_bytes(root, CERTIFIED_PARENT, path))
    if len(value) != 77:
        raise ValueError("certified scientific baseline count")
    return value


def load_v154(root):
    base = root / V154
    sys.path.insert(0, str(base))
    import verifier as v154_verifier
    import campaign as v154_campaign
    import publication as v154_publication
    return base, v154_verifier, v154_campaign, v154_publication


def audit_inherited(args, context, recovery):
    root = bind_original_checkout(args.repo, context)
    out = Path(args.out); out.mkdir(parents=True, exist_ok=True)
    dump(out / "STATUS.json", {"status": "INCOMPLETE", "component": "inherited"})
    artifacts = original_inventory(context, out); ledger = []
    controls = obtain("v1655-full-controls", out / "originals/full-controls", context, artifacts, ledger)
    development = obtain("v1655-inherited-development", out / "originals/inherited-development", context, artifacts, ledger)
    domains = []
    for shard in range(8):
        domains.append(obtain(f"v1655-inherited-domain-{shard}", out / f"originals/inherited-domain-{shard}", context, artifacts, ledger))
    foundation = obtain("v1655-inherited-foundation", out / "originals/inherited-foundation", context, artifacts, ledger)
    base55 = root / BASE
    control_names = re.findall(r"^    def (test_[A-Za-z0-9_]+)\(self\):", (base55 / "tests/test_contract.py").read_text(), re.M)
    control_log = (controls / "tests.log").read_text()
    if len(set(control_names)) != len(control_names) or any(not re.search(r"^" + re.escape(name) + r" \([^\n]+\) \.\.\. ok$", control_log, re.M) for name in control_names) or f"Ran {len(control_names)} tests" not in control_log or "\nOK\n" not in control_log:
        raise ValueError("complete v16.55 controls missing/failed")
    result = json.loads((development / "RESULT.json").read_text())
    provenance = json.loads((development / "PROVENANCE.json").read_text())
    expected_provenance = dict(scientific_sha=context.sha, workflow_sha=context.sha, run_id=str(context.run_id), attempt=str(context.attempt), phase="all", preregistration="a189546887e8744092deebecbdf73076b66ec044")
    if not result["successful"] or result["tests"] != 83 or result["failures"] or result["errors"] or result["skipped"]:
        raise ValueError("inherited development result not exact green")
    if any(str(result.get(key)) != str(value) or str(provenance.get(key)) != str(value) for key, value in expected_provenance.items()):
        raise ValueError("inherited development original provenance mismatch")
    ids_expected = expected_control_ids(root)
    ids_actual = actual_control_ids((development / "tests.log").read_text())
    hashes_expected = baseline_hashes(root)
    base54, v154_verifier, v154_campaign, v154_publication = load_v154(root)
    source_paths = subprocess.check_output(["git", "-C", root, "ls-tree", "-r", "--name-only", context.sha, "--", str(V154)], text=True).splitlines()
    source_expected = {}
    for path in source_paths:
        relative = str(Path(path).relative_to(V154))
        if Path(path).suffix in (".py", ".json", ".md") and "__pycache__" not in Path(path).parts:
            source_expected[relative] = hashlib.sha256(git_bytes(root, context.sha, path)).hexdigest()
    domain_source_expected = {
        relative: hashlib.sha256(git_bytes(root, context.sha, str(V154 / relative))).hexdigest()
        for relative in domain_source_relatives(source_paths, str(V154))
    }
    recorded = json.loads((development / "SOURCE_MANIFEST.json").read_text())
    actual_source = {str(path.relative_to(development / "source")): digest(path) for path in (development / "source").rglob("*") if path.is_file()}
    if recorded != source_expected or actual_source != source_expected:
        raise ValueError("inherited development frozen source mismatch")
    expected = iter(v154_verifier.reconstruct_cases(json.loads((base54 / "protocol.json").read_text())))
    whole = hashlib.sha256(); total = 0; diagnostics = Counter(); freezes = []
    actual_hashes = {}
    for shard, folder in enumerate(domains):
        science = folder / "scientific"
        recorded_source = json.loads((folder / "SOURCE_MANIFEST.json").read_text())
        archived_source = {str(path.relative_to(folder / "source")): digest(path) for path in (folder / "source").rglob("*") if path.is_file()}
        validate_exact_source_manifest(recorded_source, archived_source, domain_source_expected)
        provenance = json.loads((folder / "PROVENANCE.json").read_text())
        wanted = dict(scientific_sha=context.sha, workflow_sha=context.sha, run_id=str(context.run_id), attempt=str(context.attempt), shard=shard, scope="all")
        if any(str(provenance.get(key)) != str(value) for key, value in wanted.items()):
            raise ValueError("inherited shard original provenance mismatch")
        manifest = json.loads((science / "MANIFEST.json").read_text())
        if set(manifest) != {"CASES.jsonl.gz", "RECORDS.jsonl.gz", "DOMAIN_FREEZE.json", "SUMMARY.json"}:
            raise ValueError("inherited science membership mismatch")
        if any(digest(science / name) != value for name, value in manifest.items()):
            raise ValueError("inherited science corruption")
        for name in manifest:
            actual_hashes[f"{shard}/{name}"] = digest(science / name)
        summary = json.loads((science / "SUMMARY.json").read_text()); freeze = json.loads((science / "DOMAIN_FREEZE.json").read_text()); freezes.append(freeze)
        if v154_campaign.validate_campaign_summary({**summary, **provenance}):
            raise ValueError("inherited unfinished summary")
        count = 0; identity_hash = hashlib.sha256(); record_hash = hashlib.sha256()
        with gzip.open(science / "CASES.jsonl.gz", "rt") as cases, gzip.open(science / "RECORDS.jsonl.gz", "rt") as records:
            case_iter = (json.loads(line) for line in cases); record_iter = (json.loads(line) for line in records)
            for case, record in zip_longest(case_iter, record_iter):
                wanted_case = next(expected, None)
                if case is None or record is None or wanted_case is None or case != wanted_case or record["identity"] != wanted_case["identity"]:
                    raise ValueError("inherited full identity/input mismatch")
                errors = v154_verifier.verify_record(case, record)
                if errors:
                    raise ValueError("inherited independent path rejection " + repr(errors))
                row = v154_publication.serial(case) + "\n"; whole.update(row.encode()); identity_hash.update((v154_publication.serial(case["identity"]) + "\n").encode()); record_hash.update((v154_publication.serial(record) + "\n").encode())
                diagnostics.update(v154_publication._diagnose(case, record)); count += 1; total += 1
        if count != summary["checked"] or count != freeze["stop"] - freeze["start"] or identity_hash.hexdigest() != freeze["identity_sha256"] or record_hash.hexdigest() != summary["record_sha256"]:
            raise ValueError("inherited full stream mismatch")
    if next(expected, None) is not None or total != freezes[0]["total"] or whole.hexdigest() != freezes[0]["whole_universe_sha256"]:
        raise ValueError("inherited omitted domain")
    if v154_publication.check_partition(freezes) or v154_publication.check_required_diagnostics(diagnostics):
        raise ValueError("inherited partition/diagnostics mismatch")
    v154_publication.verify_inherited_package(foundation, context.sha)
    foundation_manifest = json.loads((foundation / "MANIFEST.json").read_text())
    foundation_actual = {str(path.relative_to(foundation)): digest(path) for path in foundation.rglob("*") if path.is_file() and path != foundation / "MANIFEST.json"}
    if foundation_manifest != foundation_actual:
        raise ValueError("inherited foundation manifest mismatch")
    metrics = json.loads((foundation / "METRICS.json").read_text())
    if metrics.get("inherited_tests") != 1150 or metrics.get("new_controls") != 43 or metrics.get("all_commands_passed") is not True:
        raise ValueError("inherited foundation complete-stack metrics mismatch")
    validate_foundation_metadata(json.loads((foundation / "METADATA.json").read_text()), context)
    for path in (foundation / "scientific").rglob("*"):
        if path.is_file():
            actual_hashes["inherited/" + str(path.relative_to(foundation / "scientific"))] = digest(path)
    validate_inherited_baseline(ids_expected, ids_actual, hashes_expected, actual_hashes)
    dump(out / "INHERITED_AGGREGATE.json", {"status": "PASS", "total": total, "diagnostics": dict(diagnostics), "control_ids": ids_actual, "certified_hashes": actual_hashes})
    dump(out / "ORIGINAL_ARCHIVE_AUDIT.json", ledger)
    dump(out / "STATUS.json", {"status": "PASS", "component": "inherited", "audited": context.as_dict(), "recovery": recovery})


def audit_partial(args, context, recovery):
    out = Path(args.out); out.mkdir(parents=True, exist_ok=True)
    artifacts = original_inventory(context, out); ledger = []
    folder = obtain("v1655-original-archive-audit", out / "partial-original-publication", context, artifacts, ledger)
    status = json.loads((folder / "STATUS.json").read_text())
    if status.get("status") != "INCOMPLETE" or not (folder / "primary-aggregate/AGGREGATE.json").exists():
        raise ValueError("original partial publication classification/content mismatch")
    primary = json.loads((folder / "primary-aggregate/AGGREGATE.json").read_text())
    if primary.get("status") != "PASS" or (folder / "DURABLE_MANIFEST.json").exists():
        raise ValueError("partial publication boundary mismatch")
    dump(out / "ORIGINAL_ARCHIVE_AUDIT.json", ledger)
    dump(out / "PARTIAL_INSPECTION.json", {"status": "INCOMPLETE_PRESERVED", "original_status": status, "primary_aggregate": primary})
    dump(out / "STATUS.json", {"status": "PASS", "component": "partial", "audited": context.as_dict(), "recovery": recovery})


def package(args, context, recovery):
    out = Path(args.out); out.mkdir(parents=True, exist_ok=True)
    dump(out / "STATUS.json", {"status": "INCOMPLETE", "component": "package"})
    artifacts = api(f"actions/runs/{recovery['run_id']}/artifacts?per_page=100")['artifacts']
    ledger = []
    folders = {}
    for component in ("primary", "reproduction", "inherited", "partial"):
        name = f"v1655-recovery-{component}-{recovery['sha']}-attempt-{recovery['attempt']}"
        candidates = [item for item in artifacts if item["name"] == name and not item["expired"]]
        if len(candidates) != 1:
            raise ValueError("missing/ambiguous recovery component artifact")
        item = candidates[0]
        folder = download_artifact(item, out / "components" / f"{component}.zip")
        folders[component] = folder
        ledger.append({"component": component, "id": item["id"], "name": name, "digest": item["digest"], "bytes": item["size_in_bytes"]})
        validate_component_status(json.loads((folder / "STATUS.json").read_text()), component, context, recovery)
    primary = json.loads((folders["primary"] / "AGGREGATE.json").read_text())
    reproduction = json.loads((folders["reproduction"] / "AGGREGATE.json").read_text())
    if primary != reproduction or primary.get("status") != "PASS":
        raise ValueError("aggregate equality/terminal status mismatch")
    compare_scientific_bytes(json.loads((folders["primary"] / "SCIENTIFIC_BYTES.json").read_text()), json.loads((folders["reproduction"] / "SCIENTIFIC_BYTES.json").read_text()))
    inherited = json.loads((folders["inherited"] / "INHERITED_AGGREGATE.json").read_text())
    partial = json.loads((folders["partial"] / "PARTIAL_INSPECTION.json").read_text())
    if inherited.get("status") != "PASS" or partial.get("status") != "INCOMPLETE_PRESERVED":
        raise ValueError("inherited/partial package gate mismatch")
    dump(out / "COMPONENT_ARTIFACTS.json", ledger)
    manifest = {str(path.relative_to(out)): digest(path) for path in sorted(out.rglob("*")) if path.is_file() and path != out / "STATUS.json"}
    dump(out / "DURABLE_MANIFEST.json", manifest)
    dump(out / "STATUS.json", {"status": "PASS", "component": "package", "audited": context.as_dict(), "recovery": recovery, "numbered_certification": "PENDING_DURABLE_GIT_PUBLICATION_REVIEW_MERGE_AND_ACTUAL_MERGE_AUDIT"})


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("component", choices=("primary", "reproduction", "inherited", "partial", "package"))
    parser.add_argument("request")
    parser.add_argument("repo")
    parser.add_argument("out")
    args = parser.parse_args()
    resource.setrlimit(resource.RLIMIT_AS, (4294967296, 4294967296))
    context = validate_request(json.loads(Path(args.request).read_text()))
    recovery = recovery_provenance()
    if args.component in ("primary", "reproduction"):
        audit_mode(args, context, recovery)
    elif args.component == "inherited":
        audit_inherited(args, context, recovery)
    elif args.component == "partial":
        audit_partial(args, context, recovery)
    else:
        package(args, context, recovery)


if __name__ == "__main__":
    main()
