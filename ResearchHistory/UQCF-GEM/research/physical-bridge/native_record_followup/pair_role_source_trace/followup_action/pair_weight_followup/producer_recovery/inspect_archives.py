"""Inventory the three original V1696 archives without executing their contents."""

import argparse
import csv
import hashlib
import io
import json
from pathlib import Path
import zipfile


SOURCES = {
    "V1696_1_renormalized_pair_transport_python_test_package.zip": {
        "library_file_id": "libfile_530426a7081481919ba8f5105b408799",
        "file_id": "file_0000000027d0720ebd529346be467507",
        "created_at": "2026-06-08T18:37:12.336628Z",
        "reported_size_bytes": 11552,
        "expected_sha256": "3995ad79f0dca764e4e7237d42e89210ecec3bbdd88c5bf2344c2aa9b4a6e982",
    },
    "V1696_3_retained_pair_equivalence_class_python_test_package.zip": {
        "library_file_id": "libfile_436c49a7b9d881918424428840370063",
        "file_id": "file_00000000244c720ebc1259ff228c6654",
        "created_at": "2026-06-08T18:42:51.036784Z",
        "reported_size_bytes": 29171,
        "expected_sha256": "362a15f7b130c063d7240d2f34386bad1c2d40c43af3261cfd1d0966438f0fb8",
    },
    "V1696_9_intrinsic_d1d2_operator_invariant_test_package.zip": {
        "library_file_id": "libfile_da94675564e48191a6f8ba41020a6b6f",
        "file_id": "file_0000000037a8720eb94ef129a495587b",
        "created_at": "2026-06-08T18:52:54.554794Z",
        "reported_size_bytes": 33637,
        "expected_sha256": "3b6d73384800ebd0982db484bfad4448dee4d4f8de6cae27be21ea3fdffcc314",
    },
}


def inspect(root):
    records = []
    for filename, identity in sorted(SOURCES.items()):
        raw = (root / filename).read_bytes()
        digest = hashlib.sha256(raw).hexdigest()
        if len(raw) != identity["reported_size_bytes"] or digest != identity["expected_sha256"]:
            raise ValueError(f"Archive identity mismatch: {filename}")
        with zipfile.ZipFile(io.BytesIO(raw)) as archive:
            if archive.testzip() is not None:
                raise ValueError(f"CRC error: {filename}")
            names = archive.namelist()
            if len(names) != len(set(names)):
                raise ValueError(f"Duplicate member: {filename}")
            members = []
            for name in names:
                data = archive.read(name)
                member = {
                    "name": name,
                    "bytes": len(data),
                    "sha256": hashlib.sha256(data).hexdigest(),
                }
                if name.endswith(".csv"):
                    rows = list(csv.reader(io.StringIO(data.decode("utf-8"))))
                    if not rows or any(len(row) != len(rows[0]) for row in rows):
                        raise ValueError(f"Invalid table shape: {filename}/{name}")
                    member.update(columns=rows[0], data_rows=len(rows) - 1)
                elif name.endswith(".json"):
                    member["top_level_keys"] = list(json.loads(data))
                elif name.endswith(".md"):
                    data.decode("utf-8")
                members.append(member)
            summary = next(name for name in names if name.endswith("_SUMMARY.json"))
            record = {
                "archive": filename,
                "source": identity,
                "bytes": len(raw),
                "sha256": digest,
                "git_blob_sha1": hashlib.sha1(b"blob " + str(len(raw)).encode() + b"\0" + raw).hexdigest(),
                "crc_error_member": None,
                "member_count": len(members),
                "member_extension_counts": {
                    suffix: sum(Path(name).suffix == suffix for name in names)
                    for suffix in sorted({Path(name).suffix for name in names})
                },
                "python_or_notebook_members": [
                    name for name in names if Path(name).suffix.lower() in {".py", ".pyw", ".ipynb"}
                ],
                "manifest_byte_identical_to_summary": archive.read("run_manifest.json") == archive.read(summary),
                "historical_verdict": json.loads(archive.read(summary))["verdict"],
                "members": members,
            }
            records.append(record)
    return {
        "scope": "Original-byte and table-schema inspection of these three archives only; no historical scientific code executed and no diagnostic rerun.",
        "records": records,
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("archive_directory", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    result = inspect(args.archive_directory)
    args.output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({
        "archives": len(result["records"]),
        "members": sum(record["member_count"] for record in result["records"]),
        "crc_errors": 0,
        "python_or_notebook_members": sum(len(record["python_or_notebook_members"]) for record in result["records"]),
        "duplicate_summary_manifests": sum(record["manifest_byte_identical_to_summary"] for record in result["records"]),
    }))
