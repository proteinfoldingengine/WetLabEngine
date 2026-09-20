from hashlib import sha1
from pathlib import Path


EVIDENCE = {
    "v15.41-design": (
        "../../../../docs/superpowers/specs/"
        "2026-09-19-v1541-formal-connection-curvature-source-correspondence-design.md",
        "6d35aae0ccb6c2584d26d5a83d522b3cc7036728",
    ),
    "v15.41-erratum": (
        "../../../../docs/superpowers/specs/"
        "2026-09-20-v1541-transport-protocol-erratum-design.md",
        "d40d03d9d2498ce54839b15dad00c1505c1a586a",
    ),
    "v15.41-results": (
        "../v15.41-formal-connection-curvature-source-correspondence/docs/RESULTS.json",
        "46cae26d91c709fdde4c5cc39cd3cf3908980e97",
    ),
    "v15.42-design": (
        "../../../../docs/superpowers/specs/"
        "2026-09-20-v1542-duality-covariant-transport-repair-design.md",
        "91f2c66bea982b3180a07c61ccc4bef76e9c031d",
    ),
}


def git_blob_sha(path: Path) -> str:
    data = path.read_bytes()
    return sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()


def verify_evidence() -> dict[str, str]:
    root = Path(__file__).resolve().parent
    observed = {}
    for key, (relative, expected) in EVIDENCE.items():
        actual = git_blob_sha((root / relative).resolve())
        if actual != expected:
            raise ValueError(f"evidence mismatch: {key}")
        observed[key] = actual
    return observed
