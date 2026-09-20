from __future__ import annotations

import argparse
import sys
import tempfile
from fractions import Fraction
from hashlib import sha256
from pathlib import Path

LOCAL = str(Path(__file__).resolve().parent)
if LOCAL not in sys.path:
    sys.path.insert(0, LOCAL)

from evidence import verify_evidence, verify_origins
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
    verify_origins((generation, geometry), pins)
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


def acquire_projection() -> Projection:
    generation, geometry, parent, dependencies = _verified_modules()
    return decode_projection(_project_modules(generation, geometry, parent, dependencies))


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
    args = parser.parse_args()
    write_projection(args.out)


if __name__ == "__main__":
    main()
