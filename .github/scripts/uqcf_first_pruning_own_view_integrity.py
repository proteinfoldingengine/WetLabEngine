"""Byte-integrity gate for an analytical-only audit. No scientific imports or execution."""
import hashlib
import io
import json
import os
from pathlib import Path, PurePosixPath
import re
import subprocess
import zipfile

REL = "ResearchHistory/UQCF-GEM/research/physical-bridge/first_pruning_own_view_review"
BASELINE = '89dab026b5312408cde3a98fd2f9ea416d3027ad'
LOCK_SHA256 = 'ad0e703284edafb8a321ecaa3f8febdc660c2cb4328ddacf83092dd638bc21e9'
WORKFLOW = ".github/workflows/uqcf-gem-first_pruning_own_view-review.yml"
DOCUMENTS = tuple(REL + "/" + n for n in ("RESULT.md", "FREEZE.md", "source_packet.json"))
SCRIPTS = tuple(".github/scripts/uqcf_first_pruning_own_view_" + n + ".py"
                for n in ("integrity", "review", "publication", "tests"))
ROOT = Path(__file__).resolve().parents[2]


def require(condition, message):
    if not condition:
        raise ValueError(message)


def sha256(data):
    return hashlib.sha256(data).hexdigest()


def identity(data):
    return {"sha256": sha256(data), "bytes": len(data),
            "git_blob": hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()}


def parse_json(data):
    def unique(pairs):
        obj = {}
        for key, value in pairs:
            require(key not in obj, "Duplicate JSON key")
            obj[key] = value
        return obj
    return json.loads(data, object_pairs_hook=unique)


def safe_path(path):
    require(isinstance(path, str) and path and "\\" not in path, "Invalid path")
    p = PurePosixPath(path)
    require(not p.is_absolute() and all(x not in (".", "..") for x in path.split("/")), "Unsafe path")
    require(str(p) == path, "Noncanonical path")
    return path


def index(records, key):
    require(isinstance(records, list), "Expected list")
    out = {}
    for record in records:
        require(isinstance(record, dict), "Expected object")
        name = safe_path(record[key])
        require(name not in out, "Duplicate source or member")
        out[name] = record
    return out


def verify_bytes(record, data, git=True):
    expected_keys = ("sha256", "bytes", "git_blob") if git else ("sha256", "bytes")
    actual = identity(data)
    require(type(record["bytes"]) is int, "Invalid byte count")
    for key in expected_keys:
        require(record[key] == actual[key], "Source bytes or digest mismatch")
    return {key: actual[key] for key in expected_keys}


def validate_packet(root, packet, lock):
    """Validate supplied text and selected archive members against original ZIP bytes."""
    require(set(packet) == {"baseline", "files", "archives"}, "Unexpected packet fields")
    require(packet["baseline"] == lock["baseline"] == BASELINE, "Wrong immutable baseline")
    files, originals = index(packet["files"], "path"), index(lock["files"], "path")
    archives, archive_lock = index(packet["archives"], "path"), index(lock["archives"], "path")
    require(set(files) == set(originals), "Missing or substituted source file")
    require(set(archives) == set(archive_lock), "Missing or substituted archive")
    require(not set(files).intersection(archives), "Duplicated original path")
    result = {"baseline": BASELINE, "files": [], "archives": []}
    for path, source in sorted(files.items()):
        require(set(source) == {"path", "git_blob", "sha256", "bytes", "content"}, "Unexpected source fields")
        require({k: v for k, v in source.items() if k != "content"} == originals[path], "Source lock mismatch")
        data = source["content"].encode("utf-8")
        result["files"].append({"path": path, **verify_bytes(source, data)})
    copy_paths = set()
    for path, archive in sorted(archives.items()):
        require(set(archive) == {"path", "git_blob", "sha256", "bytes", "copy_path", "members"}, "Unexpected archive fields")
        copy_path = safe_path(archive["copy_path"])
        require(copy_path.startswith(REL + "/sources/") and copy_path.endswith(".zip"), "Archive outside sources folder")
        require(copy_path not in copy_paths, "Duplicate copied archive path")
        copy_paths.add(copy_path)
        canonical = archive_lock[path]
        require({k: v for k, v in archive.items() if k != "members"} ==
                {k: v for k, v in canonical.items() if k != "members"}, "Archive lock mismatch")
        raw = (root / copy_path).read_bytes()
        found = {"path": path, "copy_path": copy_path, **verify_bytes(archive, raw), "members": [], "all_zip_members": []}
        selected, required = index(archive["members"], "name"), index(canonical["members"], "name")
        require(set(selected) == set(required), "Missing or substituted selected ZIP member")
        with zipfile.ZipFile(io.BytesIO(raw)) as zipped:
            infos = zipped.infolist()
            names = [i.filename for i in infos]
            require(len(names) == len(set(names)), "Duplicate member inside ZIP")
            require(all(not i.is_dir() for i in infos), "Unexpected ZIP directory entry")
            require(set(selected).issubset(names), "Selected member absent from original ZIP")
            for info in infos:
                safe_path(info.filename)
                data = zipped.read(info)
                found["all_zip_members"].append({"name": info.filename, "sha256": sha256(data), "bytes": len(data)})
            for name, member in sorted(selected.items()):
                require(set(member) == {"name", "sha256", "bytes", "content"}, "Unexpected member fields")
                require({k: v for k, v in member.items() if k != "content"} == required[name], "Member lock mismatch")
                data = member["content"].encode("utf-8")
                require(data == zipped.read(name), "Selected member differs from original ZIP")
                found["members"].append({"name": name, **verify_bytes(member, data, git=False)})
        found["all_zip_members"].sort(key=lambda item: item["name"])
        result["archives"].append(found)
    return result


def load_sources(root):
    lock_raw = (root / REL / "source_lock.json").read_bytes()
    require(sha256(lock_raw) == LOCK_SHA256, "Frozen source lock changed")
    packet = parse_json((root / REL / "source_packet.json").read_bytes())
    lock = parse_json(lock_raw)
    return packet, validate_packet(root, packet, lock)


def input_manifest(root, packet):
    names = list(DOCUMENTS) + list(SCRIPTS) + [WORKFLOW, REL + "/source_lock.json"]
    names += [a["copy_path"] for a in packet["archives"]]
    require(len(names) == len(set(names)), "Duplicate input path")
    return {name: identity((root / safe_path(name)).read_bytes()) for name in sorted(names)}


def run_identity(root):
    head = os.environ["GITHUB_SHA"]
    workflow = os.environ["UQCF_WORKFLOW_SHA"]
    require(re.fullmatch(r"[a-f0-9]{40}", head) is not None, "Invalid source SHA")
    require(head == workflow, "Source/workflow SHA mismatch")
    checkout = subprocess.check_output(["git", "-C", str(root), "rev-parse", "HEAD"], text=True).strip()
    require(checkout == head, "Checkout SHA mismatch")
    run, attempt = os.environ["GITHUB_RUN_ID"], os.environ["GITHUB_RUN_ATTEMPT"]
    require(run.isdigit() and attempt.isdigit() and int(attempt) > 0, "Invalid run identity")
    require(os.environ.get("GITHUB_REPOSITORY") == "proteinfoldingengine/WetLabEngine", "Unexpected repository")
    return {"source_sha": head, "workflow_sha": workflow, "run_id": run, "run_attempt": attempt,
            "repository": os.environ["GITHUB_REPOSITORY"]}


def write_json(path, obj):
    path.write_text(json.dumps(obj, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def main():
    out = Path("first_pruning_own_view_integrity")
    out.mkdir(exist_ok=True)
    try:
        run = run_identity(ROOT)
        packet, sources = load_sources(ROOT)
        write_json(out / "input_manifest.json", input_manifest(ROOT, packet))
        write_json(out / "source_manifest.json", sources)
        write_json(out / "integrity.json", {"status": "PASS", **run,
                   "input_manifest_sha256": sha256((out / "input_manifest.json").read_bytes()),
                   "source_manifest_sha256": sha256((out / "source_manifest.json").read_bytes()),
                   "source_lock_sha256": LOCK_SHA256, "scientific_execution": False})
        print("Source and selected archive-member byte integrity PASS; no scientific execution.")
    except Exception as exc:
        write_json(out / "failure.json", {"status": "FAIL", "error_type": type(exc).__name__})
        raise SystemExit("Integrity gate failed; sanitized evidence retained.")


if __name__ == "__main__":
    main()
