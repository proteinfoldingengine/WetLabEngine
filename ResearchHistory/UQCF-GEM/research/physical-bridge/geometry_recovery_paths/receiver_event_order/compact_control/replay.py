"""Replay on immutable historical source, not on a new receiver primitive."""
import hashlib
import importlib.util
import itertools
import json
from pathlib import Path
import sys

D = Path(__file__).resolve().parent
F = json.loads((D / "FIXTURE.json").read_text())
C, H = F["charts"], F["tip_holders"]
P = (-1,) + (0,) * len(H)
Y = tuple((0,) + tuple(v for v, h in enumerate(H, 1) if i in h) for i in C)
MOVES = [(C.index(i), v) for i, v in F["edits"]]

def pinned(file, blob):
    data = file.read_bytes()
    assert hashlib.sha1(f"blob {len(data)}".encode() + b"\0" + data).hexdigest() == blob
    spec = importlib.util.spec_from_file_location(file.stem, file)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

def produce(engine_dir):
    atom = pinned(engine_dir / "engine.py", F["engine_blob"]).atomic
    check = pinned(engine_dir / "verify.py", F["verify_blob"]).verify_atomic
    states = {0: Y}
    receipts, rows = {}, []
    for mask in range(32):
        for k, move in enumerate(MOVES):
            if mask & (1 << k):
                continue
            e = atom(P, states[mask], *move)
            result = check(e)
            final = mask | (1 << k)
            after = tuple(map(tuple, e["after"]))
            assert states.setdefault(final, after) == after
            receipts[mask, k] = result
            rows.append({"mask": mask, "edit": k, "result": list(result), "certificate": e})
    count = [0, 0]
    for order in itertools.permutations(range(5)):
        m = 0
        for k in order:
            if k == 4:
                count[receipts[m,k][0]] += 1
            m |= 1 << k
    e = rows[0]["certificate"]
    try:
        check(dict(e, trigger=not e["trigger"]))
    except ValueError:
        pass
    else:
        raise AssertionError("historical verifier accepted a false trigger")
    return {"rows": rows, "probe_counts": count}

if __name__ == "__main__":
    out = produce(Path(sys.argv[1]))
    sys.stdout.write(json.dumps(out, sort_keys=True, separators=(",", ":")) + "\n")
