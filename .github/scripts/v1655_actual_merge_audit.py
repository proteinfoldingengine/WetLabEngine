"""Current actual-merge reconstruction: parallel expensive audits, metadata-only join.

Historical recovery validation remains separate. No GITHUB_* variable is
rewritten, no scientific identity is executed here, and no certification is
issued. Temporary extraction is never part of the durable publication.
"""
from __future__ import annotations

import argparse
import ast
import json
import os
from pathlib import Path, PurePosixPath
import re
import resource
import shutil
import subprocess
import sys
import tempfile
from types import SimpleNamespace
import zipfile

import v1655_recovery_audit as audit
import v1655_durable_publish as publish

BASE = audit.BASE
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / BASE))
import transport

PENDING = "PENDING_ACTUAL_MERGE_WHOLE_EVIDENCE_REVIEW"
SCIENCE_NAMES = {"records.jsonl.gz", "identities.jsonl.gz", "SUMMARY.json", "DOMAIN_FREEZE.json"}
REQUIRED_DIAGNOSTICS = {
    "leveling_donor_recipient_root", "leveling_greedy_vacancy_transfers", "temporarily_inexact_entries",
    "saturated_cycles", "repeated_cycle_colors", "restored_cycle_boundaries", "maximum_layer_conversion",
    "multiple_patch_outside_witness", "noncompact_exact_endpoint", "mixed_grade_completion",
    "sufficient_bound_refusal", "zero_patch_restoration", "zero_capacity_grade", "native_clearance",
}


def validate_join(data, context, provenance, expected_ids, expected_hashes):
    if set(data) != {"primary", "reproduction", "inherited"}:
        raise ValueError("missing/extra join component")
    for component, files in data.items():
        status = files["STATUS.json"]
        audit.validate_component_status(status, component, context, provenance)
        if status.get("numbered_certification") != PENDING:
            raise ValueError("premature numbered certification")
    primary = data["primary"]["AGGREGATE.json"]
    reproduction = data["reproduction"]["AGGREGATE.json"]
    if primary != reproduction or primary.get("status") != "PASS":
        raise ValueError("aggregate equality/terminal status mismatch")
    if (primary.get("checked") != 3763 or primary.get("expected") != 3763
        or primary.get("errors") != [] or primary.get("incomplete") != []
        or primary.get("common_degree_greedy_transfers") != 0
        or primary.get("strict_slack_X15S_exercised") is not False):
        raise ValueError("incomplete/fabricated aggregate")
    diagnostics = primary.get("diagnostics", {})
    if not REQUIRED_DIAGNOSTICS <= set(diagnostics) or any(
        type(diagnostics[key]) is not int or diagnostics[key] <= 0 for key in REQUIRED_DIAGNOSTICS
    ):
        raise ValueError("missing required diagnostic")
    for name, bound in (("serialized_vertices", 10000000), ("compressed_bytes", 1073741824)):
        value = primary.get(name)
        if type(value) is not int or not 0 < value <= bound:
            raise ValueError("whole campaign resource bound")
    manifests = primary.get("shard_manifests", {})
    if set(manifests) != {str(i) for i in range(8)} or any(set(row) != SCIENCE_NAMES for row in manifests.values()):
        raise ValueError("incomplete scientific manifest membership")
    expected_science = {shard + "/" + name: digest for shard, row in manifests.items() for name, digest in row.items()}
    if any(not re.fullmatch(r"[0-9a-f]{64}", str(value)) for value in expected_science.values()):
        raise ValueError("malformed scientific digest")
    primary_science = data["primary"]["SCIENTIFIC_BYTES.json"]
    audit.compare_scientific_bytes(primary_science, data["reproduction"]["SCIENTIFIC_BYTES.json"])
    if primary_science != expected_science:
        raise ValueError("aggregate scientific manifest differs from byte ledger")
    inherited = data["inherited"]["INHERITED_AGGREGATE.json"]
    if inherited.get("status") != "PASS" or inherited.get("total") != 2393450:
        raise ValueError("incomplete inherited domain")
    audit.validate_inherited_baseline(expected_ids, inherited.get("control_ids"), expected_hashes,
                                     inherited.get("certified_hashes"))
    return {"status": "PASS", "component": "package", "audited": context.as_dict(),
            "recovery": provenance, "numbered_certification": PENDING,
            "scientific_execution": "CURRENT_ACTUAL_MERGE_COMPONENTS; JOIN_DID_NOT_RERUN_PATHS"}


def validate_original_ledgers(ledgers, context):
    rows = publish.deduplicate_ledgers(ledgers)
    stems = ["v1655-full-controls", "v1655-inherited-development", "v1655-inherited-foundation"]
    stems += [f"v1655-{mode}-{i}" for mode in ("primary", "reproduction", "inherited-domain") for i in range(8)]
    expected = {audit.original_artifact_name(stem, context) for stem in stems}
    if {row["name"] for row in rows} != expected or len(rows) != 27 or len({row["id"] for row in rows}) != 27:
        raise ValueError("incomplete/ambiguous exact original archive inventory")
    for row in rows:
        if (type(row["id"]) is not int or row["id"] <= 0
            or type(row["bytes"]) is not int or row["bytes"] <= 0
            or not re.fullmatch(r"sha256:[0-9a-f]{64}", str(row["digest"]))):
            raise ValueError("malformed original archive ledger")
    return rows


def validate_component_roles(files, component):
    common = {"STATUS.json", "ORIGINAL_RUN.json", "ORIGINAL_ARTIFACTS.json", "PRODUCING_JOBS.json",
              "EXECUTABLE_SOURCE_BINDING.json", "ORIGINAL_ARCHIVE_AUDIT.json",
              "ORIGINAL_MEMBER_MANIFESTS.json", "MANIFEST.json"}
    extras = {"primary": {"AGGREGATE.json", "SCIENTIFIC_BYTES.json", "FULL_CONTROLS.json"},
              "reproduction": {"AGGREGATE.json", "SCIENTIFIC_BYTES.json"},
              "inherited": {"INHERITED_AGGREGATE.json", "FULL_CONTROLS.json"}}
    if component not in extras or set(files) != common | extras[component]:
        raise ValueError("missing/extra exact component metadata role")


def declared_control_ids(root, mechanical=False):
    folder = root / (".github/scripts/tests" if mechanical else BASE / "tests")
    wanted = []
    for path in sorted(folder.glob("test_v1655*.py" if mechanical else "test_*.py")):
        for node in ast.parse(path.read_text()).body:
            if isinstance(node, ast.ClassDef):
                wanted.extend(f"{path.stem}.{node.name}.{child.name}" for child in node.body
                              if isinstance(child, ast.FunctionDef) and child.name.startswith("test_"))
    if not wanted or len(wanted) != len(set(wanted)):
        raise ValueError("empty/duplicate source-declared control identity")
    return sorted(wanted)


def validate_control_receipt(receipt, root):
    if set(receipt) != {"status", "control_ids", "mechanical_control_ids"} or receipt["status"] != "PASS":
        raise ValueError("full control receipt not exact PASS")
    for field, mechanical in (("control_ids", False), ("mechanical_control_ids", True)):
        values = receipt[field]
        if not isinstance(values, list) or sorted(values) != declared_control_ids(root, mechanical):
            raise ValueError("full control receipt source identity/multiplicity mismatch")


def validate_member_maps(data, originals, context):
    stems = {
        "primary": ["v1655-full-controls"] + [f"v1655-primary-{i}" for i in range(8)],
        "reproduction": [f"v1655-reproduction-{i}" for i in range(8)],
        "inherited": ["v1655-full-controls", "v1655-inherited-development", "v1655-inherited-foundation"]
                     + [f"v1655-inherited-domain-{i}" for i in range(8)],
    }
    if set(data) != set(stems):
        raise ValueError("incomplete member-map components")
    original_by_id = {row["id"]: row for row in originals}
    merged = {}
    for component, files in data.items():
        supplied = files["ORIGINAL_ARCHIVE_AUDIT.json"]
        wanted = {audit.original_artifact_name(stem, context) for stem in stems[component]}
        ledger = publish.deduplicate_ledgers([supplied])
        if len(supplied) != len(wanted) or len(ledger) != len(wanted) or {row["name"] for row in ledger} != wanted:
            raise ValueError("wrong component original ledger ownership/multiplicity")
        maps = files["ORIGINAL_MEMBER_MANIFESTS.json"]
        if set(maps) != {str(row["id"]) for row in ledger}:
            raise ValueError("missing/extra original member-map ID")
        for row in ledger:
            if original_by_id.get(row["id"]) != row:
                raise ValueError("component original row differs from unique union")
            key = str(row["id"]); members = maps[key]
            if not isinstance(members, list) or not members:
                raise ValueError("empty original member map")
            names = []
            for member in members:
                if set(member) != {"name", "bytes", "sha256"}:
                    raise ValueError("malformed original member row")
                name = member["name"]
                if (not isinstance(name, str) or not name or PurePosixPath(name).is_absolute()
                    or ".." in PurePosixPath(name).parts or "\\" in name
                    or type(member["bytes"]) is not int or member["bytes"] < 0
                    or not re.fullmatch(r"[0-9a-f]{64}", str(member["sha256"]))):
                    raise ValueError("unsafe/malformed original member identity")
                names.append(name)
            if len(names) != len(set(names)) or names != sorted(names):
                raise ValueError("duplicate/unordered original member names")
            if key in merged and merged[key] != members:
                raise ValueError("shared original member map differs")
            merged[key] = members
    if set(merged) != {str(row["id"]) for row in originals}:
        raise ValueError("incomplete unique original member-map union")
    return merged


def preserve_original(item, temporary, out, members, *, download=None):
    archive = temporary / "originals" / (str(item["id"]) + ".zip")
    archive.parent.mkdir(parents=True, exist_ok=True)
    (download or publish.download)(item, archive)
    if archive.stat().st_size != item["size_in_bytes"] or audit.digest(archive) != item["digest"][7:]:
        raise ValueError("external original byte length/digest mismatch")
    if publish.zip_members(archive) != members:
        raise ValueError("original member map differs from downloaded ZIP bytes")
    relative = "originals/" + str(item["id"])
    publish.split_archive(archive, out / relative, item["size_in_bytes"], item["digest"][7:])
    if publish.verify_parts(out / relative) != (item["size_in_bytes"], item["digest"][7:]):
        raise ValueError("durable original reconstruction mismatch")
    archive.unlink()
    return {"id": item["id"], "name": item["name"], "bytes": item["size_in_bytes"],
            "digest": item["digest"], "published_at": relative}


def current_context():
    provenance = audit.recovery_provenance()
    if os.environ["GITHUB_REF"] != "refs/heads/research/v16.34-fiber-component-invariant":
        raise ValueError("current adapter requires the actual integration merge")
    context = audit.AuditContext(int(provenance["run_id"]), provenance["sha"],
                                int(provenance["attempt"]), audit.AUDITED_WORKFLOW, audit.CERTIFIED_PARENT)
    transport.bind_request()
    audit.bind_original_checkout(Path.cwd(), context)
    return context, provenance


def current_inventory(context, provenance, component, out):
    metadata = audit.api(f"actions/runs/{context.run_id}")
    audit.validate_current_run(metadata, context, provenance)
    jobs, artifacts = [], []
    for collection, key, result in (
        (f"actions/runs/{context.run_id}/attempts/{context.attempt}/jobs", "jobs", jobs),
        (f"actions/runs/{context.run_id}/artifacts", "artifacts", artifacts),
    ):
        page = 1
        while True:
            values = audit.api(f"{collection}?per_page=100&page={page}")[key]
            result.extend(values)
            if len(values) < 100:
                break
            page += 1
    audit.validate_current_jobs(jobs, component, context)
    for item in artifacts:
        audit.validate_current_artifact(item, context)
    audit.dump(out / "ORIGINAL_RUN.json", metadata)
    audit.dump(out / "ORIGINAL_ARTIFACTS.json", artifacts)
    audit.dump(out / "PRODUCING_JOBS.json", jobs)
    contract = json.loads((BASE / "MERGE_CONTRACT.json").read_text())
    audit.dump(out / "EXECUTABLE_SOURCE_BINDING.json", {
        "event_sha": context.sha, "workflow_sha": provenance["workflow_sha"],
        "reviewed_source_parent": contract["reviewed_source_parent"],
        "scientific_git_blobs": transport.scientific_inventory(context.sha),
    })
    return artifacts


def verify_controls(folder, root):
    wanted = declared_control_ids(root)
    log = (folder / "tests.log").read_text()
    actual = re.findall(r"^test_\w+ \(([A-Za-z0-9_.]+)\) \.\.\. ok$", log, re.M)
    if (len(wanted) != len(set(wanted)) or sorted(wanted) != sorted(actual)
        or f"Ran {len(wanted)} tests" not in log or "\nOK\n" not in log):
        raise ValueError("full new controls omitted/duplicated/failed")
    mechanical = (folder / "mechanical-tests.log").read_text()
    # Derive exact IDs from the actual contract-bound test source, not a passing count.
    mechanical_wanted = declared_control_ids(root, True)
    mechanical_actual = re.findall(r"^test_\w+ \(([A-Za-z0-9_.]+)\) \.\.\. ok$", mechanical, re.M)
    if (len(mechanical_wanted) != len(set(mechanical_wanted))
        or sorted(mechanical_wanted) != sorted(mechanical_actual)
        or f"Ran {len(mechanical_wanted)} tests" not in mechanical or "\nOK\n" not in mechanical):
        raise ValueError("mechanical source-bound controls incomplete")
    receipt = {"status": "PASS", "control_ids": actual, "mechanical_control_ids": mechanical_actual}
    validate_control_receipt(receipt, root)
    return receipt


def audit_component(component, out, context, provenance):
    out.mkdir(parents=True, exist_ok=False)
    audit.dump(out / "STATUS.json", {"status": "INCOMPLETE", "component": component})
    with tempfile.TemporaryDirectory(prefix="v1655-audit-") as temporary:
        scratch = Path(temporary)
        artifacts = current_inventory(context, provenance, component, scratch)
        args = SimpleNamespace(repo=str(Path.cwd()), out=str(scratch), component=component)
        if component == "inherited":
            audit.audit_inherited(args, context, provenance, artifacts=artifacts)
            controls = scratch / "originals/full-controls"
        else:
            audit.audit_mode(args, context, provenance, artifacts=artifacts)
            controls = None
        if component == "primary":
            ledger = json.loads((scratch / "ORIGINAL_ARCHIVE_AUDIT.json").read_text())
            controls = audit.obtain("v1655-full-controls", scratch / "originals/full-controls", context, artifacts, ledger)
            audit.dump(scratch / "ORIGINAL_ARCHIVE_AUDIT.json", ledger)
        if controls is not None:
            audit.dump(scratch / "FULL_CONTROLS.json", verify_controls(controls, Path.cwd()))
        member_manifests = {}
        for row in json.loads((scratch / "ORIGINAL_ARCHIVE_AUDIT.json").read_text()):
            member_manifests[str(row["id"])] = publish.zip_members(Path(row["local_archive"]))
        audit.dump(scratch / "ORIGINAL_MEMBER_MANIFESTS.json", member_manifests)
        for path in scratch.glob("*.json"):
            shutil.copyfile(path, out / path.name)
    status = json.loads((out / "STATUS.json").read_text())
    status["numbered_certification"] = PENDING
    audit.dump(out / "STATUS.json", status)
    audit.dump(out / "MANIFEST.json", {path.name: audit.digest(path) for path in sorted(out.glob("*.json"))})


def package(out, context, provenance):
    out.mkdir(parents=True, exist_ok=False)
    audit.dump(out / "STATUS.json", {"status": "INCOMPLETE", "component": "package"})
    with tempfile.TemporaryDirectory(prefix="v1655-join-") as temporary:
        scratch = Path(temporary)
        artifacts = current_inventory(context, provenance, "package", scratch)
        data, ledgers, components = {}, [], []
        for component in ("primary", "reproduction", "inherited"):
            name = audit.original_artifact_name(f"v1655-actual-merge-{component}", context)
            candidates = [item for item in artifacts if item["name"] == name and not item["expired"]]
            if len(candidates) != 1:
                raise ValueError("missing/ambiguous current component artifact")
            item = candidates[0]
            folder = audit.download_artifact(item, scratch / "components" / f"{component}.zip")
            recorded = json.loads((folder / "MANIFEST.json").read_text())
            actual = {str(path.relative_to(folder)): audit.digest(path) for path in folder.rglob("*")
                      if path.is_file() and path != folder / "MANIFEST.json"}
            if actual != recorded or any("/" in path or not path.endswith(".json") for path in actual):
                raise ValueError("component payload not complete metadata-only manifest")
            data[component] = {path.name: json.loads(path.read_text()) for path in folder.glob("*.json")}
            validate_component_roles(data[component], component)
            audit.validate_current_run(data[component]["ORIGINAL_RUN.json"], context, provenance)
            audit.validate_current_jobs(data[component]["PRODUCING_JOBS.json"], component, context)
            if component in ("primary", "inherited"):
                validate_control_receipt(data[component]["FULL_CONTROLS.json"], Path.cwd())
            if data[component]["EXECUTABLE_SOURCE_BINDING.json"] != json.loads((scratch / "EXECUTABLE_SOURCE_BINDING.json").read_text()):
                raise ValueError("component executable source mismatch")
            ledgers.append(data[component]["ORIGINAL_ARCHIVE_AUDIT.json"])
            target = out / "components" / component
            target.mkdir(parents=True)
            for path in folder.glob("*.json"):
                shutil.copyfile(path, target / path.name)
            components.append({"component": component, "id": item["id"], "name": name,
                               "bytes": item["size_in_bytes"], "digest": item["digest"]})
        result = validate_join(data, context, provenance, audit.expected_control_ids(Path.cwd()), audit.baseline_hashes(Path.cwd()))
        originals = validate_original_ledgers(ledgers, context)
        member_maps = validate_member_maps(data, originals, context)
        published = []
        for row in originals:
            candidates = [item for item in artifacts if item["id"] == row["id"]]
            if len(candidates) != 1:
                raise ValueError("original ledger artifact not in actual current run")
            item = candidates[0]
            if {"id": item["id"], "name": item["name"], "bytes": item["size_in_bytes"], "digest": item["digest"]} != row:
                raise ValueError("original ledger differs from external metadata")
            published.append(preserve_original(item, scratch, out, member_maps[str(row["id"])]))
        for name in ("ORIGINAL_RUN.json", "ORIGINAL_ARTIFACTS.json", "PRODUCING_JOBS.json", "EXECUTABLE_SOURCE_BINDING.json"):
            shutil.copyfile(scratch / name, out / name)
    audit.dump(out / "ORIGINAL_EVIDENCE_INVENTORY.json", published)
    audit.dump(out / "COMPONENT_ARTIFACTS.json", components)
    audit.dump(out / "RECONSTRUCTION.json", {"status": "PASS", "original_archives": 27,
        "original_bytes": sum(row["bytes"] for row in published), "publication_policy": "ORIGINAL_ARCHIVES_ONCE_METADATA_ONLY_COMPONENTS",
        "derived_component_zip_encodings": "REFERENCED_BY_EXACT_EXTERNAL_ID_LENGTH_SHA256_NOT_EMBEDDED",
        "temporary_extraction": "OUTSIDE_PUBLISHED_OUTPUT_REMOVED", "numbered_certification": PENDING})
    audit.dump(out / "STATUS.json", result)
    audit.dump(out / "PUBLICATION_MANIFEST.json", {str(path.relative_to(out)): audit.digest(path)
        for path in sorted(out.rglob("*")) if path.is_file()})


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("component", choices=("primary", "reproduction", "inherited", "package"))
    parser.add_argument("out")
    args = parser.parse_args()
    resource.setrlimit(resource.RLIMIT_AS, (4294967296, 4294967296))
    context, provenance = current_context()
    out = Path(args.out)
    if args.component == "package":
        expected = BASE / "evidence/actual-merge" / f"run-{context.run_id}-attempt-{context.attempt}"
        if out != expected:
            raise ValueError("unexpected actual-merge publication destination")
        package(out, context, provenance)
    else:
        audit_component(args.component, out, context, provenance)


if __name__ == "__main__":
    main()
