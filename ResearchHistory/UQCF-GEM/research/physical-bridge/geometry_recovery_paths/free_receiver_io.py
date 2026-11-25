"""Shared file formats and pinned historical module loading."""
from hashlib import sha1
import importlib.util
import json
import lzma
from pathlib import Path

DEMOS = Path("ResearchHistory/UQCF-GEM/demos")
FIXTURE = Path("ResearchHistory/UQCF-GEM/research/physical-bridge/forced_parent_deletion/check_geometry_repair.py")
ATOM = DEMOS / "v16.26-consistency-increment-law/engine.py"
P1 = DEMOS / "v16.23-overlap-descent/engine.py"
TWO = DEMOS / "v16.44-two-branch-unit-barrier"


def require(ok, why):
    if not ok:
        raise ValueError(why)


def module(root, rel, name, blob):
    path = root / rel
    data = path.read_bytes()
    require(sha1(f"blob {len(data)}\0".encode()+data).hexdigest() == blob, str(rel))
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def write_xz(path, data):
    raw = (json.dumps(data, sort_keys=True, separators=(",", ":")) + "\n").encode()
    path.write_bytes(lzma.compress(raw, preset=6))


def read_xz(path):
    return json.loads(lzma.decompress(path.read_bytes()))


def save(path, data):
    path.write_text(json.dumps(data, sort_keys=True, indent=2) + "\n")


def same(actual, expected, label):
    require(json.dumps(actual, sort_keys=True, separators=(",", ":")) ==
            json.dumps(expected, sort_keys=True, separators=(",", ":")), label)
