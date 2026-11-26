"""Verify both original four-child review archives and their scoped scientific readback."""
from hashlib import sha1, sha256
import json
import lzma
from pathlib import Path
import sys
from zipfile import ZipFile

root = Path(__file__).resolve().parent
science = Path(sys.argv[1]) if len(sys.argv) > 1 else root.parent / "four_child_retained_grade_fork"
manifest = json.loads((root / "MANIFEST.json").read_bytes())
expected_raw = lzma.decompress((science / "positive_rows.json.xz").read_bytes())
for entry in manifest["reviews"]:
    path = root / entry["archive"]
    assert sha256(path.read_bytes()).hexdigest() == entry["sha256"]
    with ZipFile(path) as z:
        assert z.testzip() is None
        verdict = json.loads(z.read("review.txt"))
        receipt = json.loads(z.read("receipt.json"))
        assert receipt["checkout_sha"] == receipt["workflow_sha"] == entry["science_sha"]
        assert int(receipt["run_id"]) == entry["run"] and receipt["attempt"] == "1"
        assert receipt["model_returned"] == receipt["model_requested"] == "gemini-3.1-pro-preview"
        assert json.loads(z.read("publication_audit.json")) == {"audit": "PASS", **receipt}
        for key, name in (("response", "response.json"), ("request", "request.json"), ("prompt", "prompt.txt")):
            assert sha256(z.read(name)).hexdigest() == receipt[key + "_sha256"]
        assert json.loads(z.read("request.json"))["contents"][0]["parts"][0]["text"].encode() == z.read("prompt.txt")
        parts = json.loads(z.read("response.json"))["candidates"][0]["content"]["parts"]
        assert "\n".join(p["text"] for p in parts if "text" in p and not p.get("thought")).strip().encode() == z.read("review.txt")
        assert verdict["verdict"] == receipt["verdict"] == entry["reported_verdict"]
        assert verdict["native_bridge_status"] == entry["reported_bridge_status"]
        assert z.read("positive_rows.json") == expected_raw
        result = z.read("result.json")
        gid = sha1(b"blob " + str(len(result)).encode() + b"\0" + result).hexdigest()
        assert receipt["source_blobs"][manifest["science_path"] + "/result.json"] == gid
        counts = json.loads(result)["counts"]
        assert (counts["eligible"], counts["positive"], counts["same_local_history_at_fork"]) == (2730,312,260)
        if entry["includes_restoration_theorem"]:
            assert result == (science / "result.json").read_bytes()
            assert counts["fork_source_step_uniquely_restores_source_cover"] == 252
            assert counts["fork_source_step_does_not_reach_source_cover"] == 8
        print(entry["run"], receipt["model_returned"], verdict["verdict"], verdict["native_bridge_status"])
