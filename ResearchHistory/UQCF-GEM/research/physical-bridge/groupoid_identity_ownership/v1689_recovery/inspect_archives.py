"""Read original V1689 ZIPs; no historical scientific module is executed.

Run from the packet directory: python3 inspect_archives.py
Archives are inputs; extracted/ and INSPECTION.json are deterministic outputs.
This verifies archive bytes/schema facts, not the archived scientific claims.
"""
from pathlib import Path
import csv
import hashlib
import io
import json
import zipfile

ROOT = Path(__file__).resolve().parent

def identities(data):
    return {
        "bytes": len(data),
        "sha256": hashlib.sha256(data).hexdigest(),
        "git_blob": hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest(),
    }

def inspect():
    archives = []
    expected = json.loads((ROOT / "SOURCE_PROVENANCE.json").read_text())
    expected_names = {x["archive"] for x in expected["archives"]}
    actual_names = {p.name for p in (ROOT / "archives").glob("*.zip")}
    if actual_names != expected_names:
        raise ValueError("archive identity set differs")
    for source in sorted(expected["archives"], key=lambda x: x["archive"]):
        path = ROOT / "archives" / source["archive"]
        data = path.read_bytes()
        if identities(data) != source["downloaded_bytes"]:
            raise ValueError("archive hash/length mismatch: " + path.name)
        members = []
        with zipfile.ZipFile(io.BytesIO(data)) as z:
            if z.testzip() is not None:
                raise ValueError("CRC failure: " + path.name)
            names = z.namelist()
            if len(names) != len(set(names)):
                raise ValueError("duplicate ZIP member")
            for info in z.infolist():
                if info.is_dir():
                    continue
                payload = z.read(info)
                out = ROOT / "extracted" / path.stem / info.filename
                if not out.resolve().is_relative_to((ROOT / "extracted" / path.stem).resolve()):
                    raise ValueError("unsafe ZIP path")
                out.parent.mkdir(parents=True, exist_ok=True)
                out.write_bytes(payload)
                item = {"path": info.filename, **identities(payload), "crc32": f"{info.CRC:08x}"}
                if info.filename.endswith(".csv"):
                    reader = csv.DictReader(io.StringIO(payload.decode("utf-8")))
                    rows = list(reader)
                    item.update(headers=reader.fieldnames, row_count=len(rows))
                    if "event_type" in (reader.fieldnames or []):
                        types = sorted({row["event_type"] for row in rows})
                        item.update(event_types=types, branch_prune_count=sum(row["event_type"] == "branch_prune" for row in rows))
                members.append(item)
        archives.append({"archive": path.name, **identities(data), "members": members})
    result = {
        "schema": "uqcf-v1689-original-archive-inspection-v1",
        "scope": "Original ZIP/member integrity and literal table schema only; no scientific reproduction or acceptance.",
        "archives": archives,
        "source_code_members": [a["archive"] + ":" + m["path"] for a in archives for m in a["members"] if Path(m["path"]).suffix.lower() in {".py", ".ipynb", ".jl", ".r", ".m", ".js", ".ts", ".cpp", ".c", ".sh"}],
    }
    (ROOT / "INSPECTION.json").write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({"archives": len(archives), "members": sum(len(a["members"]) for a in archives), "source_code_members": result["source_code_members"], "zip_and_member_crc": "PASS"}))

if __name__ == "__main__":
    inspect()
