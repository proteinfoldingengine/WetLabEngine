"""Verify the durable four-child publication and foundation archives."""
from hashlib import sha256
import json
from pathlib import Path
from zipfile import ZipFile

root = Path(__file__).resolve().parent
manifest = json.loads((root / "MANIFEST.json").read_bytes())
for key in ("foundation", "publication"):
    item = manifest["artifacts"][key]
    path = root / item["archive"]
    assert sha256(path.read_bytes()).hexdigest() == item["digest"].split(":", 1)[1]
    with ZipFile(path) as archive:
        assert archive.testzip() is None
        names = set(archive.namelist())
        assert "SHA256SUMS" in names
        checks = archive.read("SHA256SUMS").decode().splitlines()
        for line in checks:
            digest, name = line.split(None, 1)
            name = name.strip().removeprefix("./")
            assert sha256(archive.read(name)).hexdigest() == digest
assert manifest["adjudication"] == {
    "finite_result": "ACCEPTED",
    "native_bridge_status": "OPEN",
    "publication_audit": "PASS",
}
print("four-child publication readback PASS")
