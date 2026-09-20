from __future__ import annotations

import json
import subprocess
from hashlib import sha1
from importlib import metadata
from pathlib import Path


SCHEMA = "uqcf-v1543-dependencies-v1"
ROLES = ("evidence", "acquisition", "evaluator", "parent_replay", "regression")
MANIFEST_KEYS = frozenset(("schema", "parent", "spec", "external", *ROLES))


def git_blob(raw: bytes) -> str:
    return sha1(b"blob " + str(len(raw)).encode() + b"\0" + raw).hexdigest()


def _demo(root: Path) -> Path:
    return root / "ResearchHistory/UQCF-GEM/demos/v15.43-certified-response-geometry"


def _manifest(root: Path) -> dict:
    def unique_object(pairs):
        value = {}
        for key, item in pairs:
            if key in value:
                raise ValueError(f"duplicate JSON key: {key}")
            value[key] = item
        return value

    manifest = json.loads((_demo(root) / "dependencies.json").read_text(), object_pairs_hook=unique_object)
    if type(manifest) is not dict or set(manifest) != MANIFEST_KEYS or manifest["schema"] != SCHEMA:
        raise ValueError("invalid dependency manifest schema")
    if type(manifest["parent"]) is not str or len(manifest["parent"]) != 40:
        raise ValueError("invalid scientific parent")
    if (type(manifest["external"]) is not dict or set(manifest["external"]) != {"numpy"} or
            type(manifest["external"]["numpy"]) is not str or not manifest["external"]["numpy"]):
        raise ValueError("invalid external dependency inventory")
    for role in ROLES:
        if type(manifest[role]) is not dict:
            raise ValueError(f"invalid {role} inventory")
    return manifest


def _verified_item(root: Path, name: str, item: object) -> dict[str, str]:
    if type(item) is not dict or set(item) != {"path", "blob"}:
        raise ValueError(f"invalid evidence item: {name}")
    relative, expected = item["path"], item["blob"]
    if type(relative) is not str or type(expected) is not str or len(expected) != 40:
        raise ValueError(f"invalid evidence pin: {name}")
    resolved_root = root.resolve()
    path = (resolved_root / relative).resolve(strict=True)
    if path != resolved_root and resolved_root not in path.parents:
        raise ValueError(f"evidence escapes repository: {name}")
    actual = git_blob(path.read_bytes())
    if actual != expected:
        raise ValueError(f"blob mismatch: {name}: {actual}")
    return {"path": str(path), "blob": actual}


def verify_repository_evidence(root: Path) -> dict:
    root = Path(root).resolve(strict=True)
    manifest = _manifest(root)
    ancestry = subprocess.run(
        ["git", "merge-base", "--is-ancestor", manifest["parent"], "HEAD"],
        cwd=root, capture_output=True, text=True,
    )
    if ancestry.returncode:
        raise ValueError("scientific parent is not an ancestor")
    receipt = {"schema": SCHEMA, "parent": manifest["parent"]}
    receipt["spec"] = _verified_item(root, "spec", manifest["spec"])
    for role in ROLES:
        receipt[role] = {name: _verified_item(root, name, item) for name, item in manifest[role].items()}
    return receipt


def verify_evidence(root: Path) -> dict:
    root = Path(root).resolve(strict=True)
    receipt = verify_repository_evidence(root)
    expected = _manifest(root)["external"]["numpy"]
    try:
        actual = metadata.version("numpy")
    except metadata.PackageNotFoundError as error:
        raise ValueError("external dependency missing: numpy") from error
    if actual != expected:
        raise ValueError(f"external dependency mismatch: numpy: {actual}")
    receipt["external"] = {"numpy": actual}
    return receipt


def verify_origins(modules: tuple[object, ...], allowed: dict[str, str]) -> dict:
    if type(modules) is not tuple or type(allowed) is not dict:
        raise TypeError("explicit modules and origin pins required")
    root = Path(__file__).resolve().parents[4]
    manifest = _manifest(root)
    inventory = [item for role in ("acquisition", "evaluator", "parent_replay", "regression")
                 for item in manifest[role].values()]
    receipt = {}
    for module in modules:
        name = getattr(module, "__name__", None)
        origin = getattr(module, "__file__", None)
        if name not in allowed or type(origin) is not str:
            raise ValueError("unexpected repository module")
        try:
            path = Path(origin).resolve(strict=True)
        except OSError as error:
            raise ValueError(f"module origin mismatch: {name}") from error
        expected = allowed[name]
        candidates = {(root / item["path"]).resolve() for item in inventory
                      if item["blob"] == expected and Path(item["path"]).stem == name.rsplit(".", 1)[-1]}
        if path not in candidates or git_blob(path.read_bytes()) != expected:
            raise ValueError(f"module origin mismatch: {name}")
        receipt[name] = {"path": str(path), "blob": expected}
    if set(receipt) != set(allowed):
        raise ValueError("incomplete module origin verification")
    return receipt
