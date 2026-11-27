"""Trace the original withdrawals and every possible sequence of one chart's own cuts."""
from copy import deepcopy
import hashlib
import importlib.util
import json
import lzma
import sys
from collections import Counter
from functools import cache
from pathlib import Path

ATOM = "v16.26-consistency-increment-law"
LOG = "v16.27-increment-attribution-closure/completion/evidence/historical-producer.log"
SQUARES = "v16.29-local-profile-closure/evidence/FULL_CERTIFICATES.json.xz"


def pinned(path, blob):
    data = path.read_bytes()
    actual = hashlib.sha1(f"blob {len(data)}\0".encode() + data).hexdigest()
    if actual != blob:
        raise ValueError(f"Unexpected source bytes at {path}")
    return data


def module(path):
    spec = importlib.util.spec_from_file_location("original_atom", path)
    engine = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(engine)
    return engine


def family(rows):
    return tuple(map(tuple, rows))


def bits(row):
    return sum(1 << v for v in row)


def run(demos, output):
    pinned(demos / ATOM / "engine.py", "c10ac57f988a439144e21898bd2b33ece0838a9b")
    engine = module(demos / ATOM / "engine.py")
    official = json.loads(pinned(demos / ATOM / "evidence/PRODUCTION.json", "25e15faf44bb59c77cdd48abf7c8473395c1ae04"))
    by_shape = {item["code"]: item for item in official["instances"]}

    @cache
    def actions(p, state, actor):
        moves = []
        for v in state[actor]:
            try:
                receipt = engine.atomic(p, state, actor, v)
            except ValueError:
                continue
            moves.append((v, family(receipt["after"])))
        return moves

    @cache
    def words(p, state, actor):
        out = {()}
        for v, successor in actions(p, state, actor):
            out.update((v,) + tail for tail in words(p, successor, actor))
        return frozenset(out)

    def compare(receipt):
        old, new = map(family, (receipt["before"], receipt["after"]))
        p = tuple(receipt["parents"])
        actor, x = receipt["index"], receipt["leaf"]
        remote = []
        for r in range(len(old)):
            if r == actor:
                continue
            assert old[r] == new[r]
            before, after = words(p, old, r), words(p, new, r)
            assert after <= before
            lost = sorted(before - after)
            remote.append([r, len(before), len(after), lost])
        return remote

    records = []
    hist = Counter()
    for sc, p in engine.shapes(5):
        digest = hashlib.sha256()
        total = 0
        for state in engine.covers(p):
            for actor, row in enumerate(state):
                for x in row:
                    try:
                        event = engine.atomic(p, state, actor, x)
                    except ValueError:
                        continue
                    native_key = (state, actor, x, event["tau_before"], event["tau_after"],
                                  event["h_before"], event["h_after"], event["trigger"])
                    digest.update((repr(native_key) + "\n").encode())
                    remote = compare(event)
                    changed = [r for r, _, _, lost in remote if lost]
                    assert len(changed) <= 1
                    t, dh = int(event["trigger"]), event["delta_h"]
                    hist[t, dh, bool(changed)] += 1
                    records.append([p, tuple(map(bits, state)), actor, x, t, dh, remote])
                    total += 1
        assert (total, digest.hexdigest()) == (by_shape[sc]["atomic"], by_shape[sc]["digest"])
        words.cache_clear()
        actions.cache_clear()
    assert len(by_shape) == len(engine.shapes(5))
    packed = (json.dumps(sorted(records), separators=(",", ":")) + "\n").encode()
    output.write_bytes(lzma.compress(packed))
    rawlog = pinned(demos / LOG, "84ac51dc629da88adf84549a3c3a139f612c3cc6")
    campaign = json.loads(rawlog)["first_witness"]
    pinned(demos / ATOM / "verify.py", "91cd1e507e955683e744fbdbb0745cac19d66cb3")
    verifier = module(demos / ATOM / "verify.py")
    logged = []
    for name in ("path_a", "path_b"):
        for step, d in enumerate(campaign[name], 1):
            assert d == engine.atomic(d["parents"], d["before"], d["index"], d["leaf"])
            remote = compare(d)
            affected, = [r for r, _, _, lost in remote if lost]
            engine.atomic(d["parents"], d["before"], affected, d["leaf"])
            saved = deepcopy(d["after"])
            try:
                engine.atomic(d["parents"], d["after"], affected, d["leaf"])
            except ValueError as error:
                assert str(error) == "same union" and d["after"] == saved
            else:
                raise AssertionError("The last holder could release the site")
            assert verifier.verify_atomic(d) == (d["delta_h"], d["trigger"])
            try:
                verifier.verify_atomic({**d, "trigger": not d["trigger"]})
            except ValueError:
                pass
            else:
                raise AssertionError("Corrupted trigger passed verification")
            logged.append(dict(path=name, step=step, actor=d["index"], site=d["leaf"],
                               trigger=d["trigger"], delta_h=d["delta_h"], remote=remote,
                               challenged_receiver=affected, refusal="same union",
                               receiver_row_unchanged=True))

    # Use the independently located offsets and hashes in the preceding archive audit.
    raw = lzma.decompress(pinned(demos / SQUARES, "45cefa46e2d0f50ecde74bab9bc3d498edc69752"))
    assert hashlib.sha256(raw).hexdigest() == "19d291e2f51286051a1e1c2840ab2d5994b9f8fe52f88f574ad2460b7ba7e69b"
    archive = []
    positions = [(1392, 3859744, "1b3deca4a3cfcfef1525ab38174658be5ab3d198b1d999c8c458365570d76a31"),
                 (1393, 3860237, "335d4f45fb1ce9639c212a21cd2a7219c7eeb2b48a88e1911a91871dc733dd79")]
    for ordinal, start, expected in positions:
        row, length = json.JSONDecoder().raw_decode(raw[start:start + 8192].decode())
        assert hashlib.sha256(raw[start:start + length]).hexdigest() == expected
        first, second = row["events"]
        d = engine.atomic(row["parents"], row["before"], *first)
        e = engine.atomic(row["parents"], d["after"], *second)
        assert e["before"] == row["states"][1] and e["after"] == row["states"][3]
        p, actor = tuple(e["parents"]), e["index"]
        archive.append(dict(ordinal=ordinal, source=first, marked=second, trigger=e["trigger"],
                            delta_h=e["delta_h"], remote=compare(e),
                            actor_words_before=sorted(words(p, family(e["before"]), actor)),
                            actor_words_after=sorted(words(p, family(e["after"]), actor))))
    return dict(events=len(records), chart_comparisons=sum(len(record[-1]) for record in records),
                record_bytes=len(packed), record_sha256=hashlib.sha256(packed).hexdigest(),
                census=[dict(trigger=t, delta_h=dh, remote_loss=changed, events=n)
                        for (t, dh, changed), n in sorted(hist.items())],
                campaign_log_bytes=len(rawlog), logged_receipts=logged, masked_control=archive)


if __name__ == "__main__":
    print(json.dumps(run(Path(sys.argv[1]), Path(sys.argv[2])), indent=2, sort_keys=True))
