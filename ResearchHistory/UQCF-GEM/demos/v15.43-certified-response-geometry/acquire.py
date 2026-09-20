from __future__ import annotations

import argparse
import json
import sys
import tempfile
from fractions import Fraction
from hashlib import sha256
from pathlib import Path

LOCAL = str(Path(__file__).resolve().parent)
if LOCAL not in sys.path:
    sys.path.insert(0, LOCAL)

from evidence import git_blob, verify_evidence, verify_origins
from projection import DEPENDENCIES, FAMILY_KEYS, Field, Payload, Projection, canonical_bytes, decode_projection, encode_projection


def _verified_modules():
    root = Path(__file__).resolve().parents[4]
    receipt = verify_evidence(root)
    locations = {Path(path).stem: Path(item["path"]).parent
                 for path, item in receipt["acquisition"].items()
                 if Path(path).stem in ("response_generation", "response_geometry")}
    for location in locations.values():
        text = str(location)
        if text not in sys.path:
            sys.path.insert(0, text)
    import response_generation as generation
    import response_geometry as geometry
    pins = dict((Path(path).stem, blob) for path, blob in DEPENDENCIES
                if Path(path).stem in ("response_generation", "response_geometry"))
    verify_origins((generation, geometry), pins, "acquisition")
    return generation, geometry, receipt["parent"], DEPENDENCIES


def _project_modules(generation, geometry_module, parent, dependencies):
    payloads = []
    for L in (5, 7):
        for amplitude in (Fraction(1), Fraction(7, 3)):
            canonical = generation.response_family(L, "GLOBAL_BALANCE_COMPLETION", amplitude)
            geometry = geometry_module.construct_response_geometry(
                canonical.labels, canonical.sources, canonical.responses)
            fields = tuple(Field(key, response_index, tuple(values))
                           for key in FAMILY_KEYS
                           for response_index, values in enumerate(
                               generation.response_family(L, key, amplitude).responses))
            edges = tuple(sorted(tuple(sorted(edge)) for edge in geometry.neighbors))
            payloads.append(Payload(L, amplitude, tuple(geometry.labels),
                                    tuple(tuple(value for value in row) for row in geometry.work),
                                    edges, fields))
    hashes = tuple(sha256(canonical_bytes({
        "L": payload.L, "scale": str(payload.scale), "labels": list(payload.labels),
        "work": [[str(value) for value in row] for row in payload.work],
        "neighbors": [list(edge) for edge in payload.neighbors],
        "fields": [{"family": field.family, "response_index": field.response_index,
                    "values": [str(value) for value in field.values]} for field in payload.fields],
    })).hexdigest() for payload in payloads)
    return encode_projection(Projection(parent, tuple(dependencies), tuple(payloads), hashes))


def _verify_loaded_closure(receipt):
    expected = {Path(item["path"]).resolve(): item["blob"]
                for item in receipt["acquisition"].values()}
    local = {Path(__file__).resolve(), (Path(__file__).parent / "evidence.py").resolve(),
             (Path(__file__).parent / "projection.py").resolve()}
    permitted = set(expected) | local
    loaded = []
    pins = {}
    for module in tuple(sys.modules.values()):
        origin = module.__file__ if hasattr(module, "__file__") else None
        if type(origin) is not str:
            continue
        path = Path(origin).resolve()
        if Path(__file__).resolve().parents[4] in path.parents and path not in permitted:
            raise ValueError(f"unexpected acquisition repository module: {path.name}")
        if path in expected:
            loaded.append(module)
            pins[module.__name__] = expected[path]
    if {Path(module.__file__).resolve() for module in loaded} != set(expected):
        raise ValueError("incomplete acquisition module closure")
    inherited = verify_origins(tuple(loaded), pins, "acquisition")
    return {**{name: {"blob": item["blob"]} for name, item in inherited.items()},
            **{path.name: {"blob": git_blob(path.read_bytes())} for path in sorted(local)}}


def _acquire_with_receipt():
    generation, geometry, parent, dependencies = _verified_modules()
    raw = _project_modules(generation, geometry, parent, dependencies)
    receipt = verify_evidence(Path(__file__).resolve().parents[4])
    origins = _verify_loaded_closure(receipt)
    return decode_projection(raw), origins


def acquire_projection() -> Projection:
    return _acquire_with_receipt()[0]


def write_projection(path: Path) -> None:
    raw = encode_projection(acquire_projection())
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(dir=path.parent, prefix=path.name + ".", delete=False) as stream:
        temporary = Path(stream.name)
        stream.write(raw)
        stream.flush()
    temporary.replace(path)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", required=True, type=Path)
    parser.add_argument("--receipt", type=Path)
    args = parser.parse_args()
    projection, origins = _acquire_with_receipt()
    raw = encode_projection(projection)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_bytes(raw)
    if args.receipt:
        args.receipt.write_text(json.dumps(origins, sort_keys=True, indent=2) + "\n")


if __name__ == "__main__":
    main()
