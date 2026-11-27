"""Run the unchanged v16.27 document reader separately on the four historical receipts."""
from concurrent.futures import ProcessPoolExecutor
from copy import deepcopy
import hashlib
import importlib.util
import json
from pathlib import Path
import sys

STAGE = "v16.27-increment-attribution-closure"
ATOM = "v16.26-consistency-increment-law"
PINS = {
    STAGE + "/verify.py": "f87d85f5882408af2e6725f0cc8802747e69a4a4",
    STAGE + "/engine.py": "48f132d141167d9cd85ff79ec41720b5dca4f8bb",
    STAGE + "/test_gate.py": "394888b094cefb1853ae09db9d16bb954de58351",
    STAGE + "/completion/run_campaign.py": "da099fc328cde949e14ecb9afbd3d6217f6b7366",
    STAGE + "/completion/evidence/historical-v1627.log": "47bb2590a2406e0206581c24cd0e77540c2aedce",
    STAGE + "/completion/evidence/historical-producer.log": "84ac51dc629da88adf84549a3c3a139f612c3cc6",
    ATOM + "/engine.py": "c10ac57f988a439144e21898bd2b33ece0838a9b",
    ATOM + "/verify.py": "91cd1e507e955683e744fbdbb0745cac19d66cb3",
}


def module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def examine(demos, mode):
    doc = json.loads((demos / STAGE / "completion/evidence/historical-producer.log").read_bytes())
    old = deepcopy(doc)
    witness = doc["first_witness"]
    steps = witness["path_a"] + witness["path_b"]
    assert len(steps) == 4
    per_atom_rejections = 0
    if mode == "flip_trigger":
        v26 = module("atom_verifier", demos / ATOM / "verify.py")
        for d in steps:
            d["trigger"] = not d["trigger"]
            try:
                v26.verify_atomic(d)
            except ValueError as err:
                assert str(err) == "false certificate"
                per_atom_rejections += 1
        assert per_atom_rejections == 4
    elif mode == "keep_four":
        for d in steps:
            for key in set(d) - {"before", "index", "leaf", "delta_h"}:
                del d[key]
    elif mode == "wrong_delta":
        steps[0]["delta_h"] = 1 - steps[0]["delta_h"]
    elif mode == "wrong_before":
        steps[0]["before"][0] = [0]
    assert all(doc[k] == old[k] for k in old if k != "first_witness")
    reader = module("v27_reader", demos / STAGE / "verify.py")
    try:
        output = reader.verify_document(doc)
    except ValueError as exc:
        return dict(mode=mode, rejected=str(exc))
    assert set(output) == {"endpoints", "multi_path", "path_dependent", "paths", "digest"}
    return dict(mode=mode, returned=output,
                v26_trigger_rejections=per_atom_rejections if mode == "flip_trigger" else None)


def run(demos):
    for name, blob in PINS.items():
        data = (demos / name).read_bytes()
        assert hashlib.sha1(f"blob {len(data)}\0".encode() + data).hexdigest() == blob
    modes = ("original", "flip_trigger", "keep_four", "wrong_delta", "wrong_before")
    with ProcessPoolExecutor(max_workers=3) as pool:
        rows = list(pool.map(examine, [demos] * len(modes), modes))
    assert rows[0]["returned"] == rows[1]["returned"] == rows[2]["returned"]
    assert [r["rejected"] for r in rows[3:]] == ["delta", "chain"]
    return rows


if __name__ == "__main__":
    print(json.dumps(run(Path(sys.argv[1])), indent=2, sort_keys=True))
