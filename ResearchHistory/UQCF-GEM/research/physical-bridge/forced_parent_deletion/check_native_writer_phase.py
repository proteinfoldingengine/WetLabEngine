"""Replay the same-event counterexamples from the inherited recorded paths."""
from copy import deepcopy
from hashlib import sha1, sha256
import gzip
import importlib.util
from itertools import groupby
import json
from pathlib import Path
import sys
from tempfile import TemporaryFile
from zipfile import ZipFile


U = Path("ResearchHistory/UQCF-GEM")
D = U / "demos"
TERNARY = D / "v16.52-recursive-ternary-composition"
FOUR = D / "v16.53-four-child-boundary"
ATOM = D / "v16.26-consistency-increment-law"
LINEAGE = U / "foundational-closure-verification/lineage.py"
ARCHIVE = FOUR / "evidence/science-artifact.chunks/ARCHIVE.json"
PARENT_ARCHIVE = TERNARY / "evidence/science-artifact.chunks/ARCHIVE.json"
PINS = {'ResearchHistory/UQCF-GEM/demos/v16.26-consistency-increment-law/engine.py': 'c10ac57f988a439144e21898bd2b33ece0838a9b',
 'ResearchHistory/UQCF-GEM/demos/v16.26-consistency-increment-law/verify.py': '91cd1e507e955683e744fbdbb0745cac19d66cb3',
 'ResearchHistory/UQCF-GEM/demos/v16.52-recursive-ternary-composition/coverage.py': '973244d0eb8a48bcb2464870377139cf4e9870c6',
 'ResearchHistory/UQCF-GEM/demos/v16.52-recursive-ternary-composition/evidence/science-artifact.chunks/ARCHIVE.json': 'f9b6f43a70e962c41021d4ea0c166e8f43957be2',
 'ResearchHistory/UQCF-GEM/demos/v16.52-recursive-ternary-composition/producer.py': '90108c926299ca7cb66dca6acc4530bafcdb4a7e',
 'ResearchHistory/UQCF-GEM/demos/v16.52-recursive-ternary-composition/verifier.py': '93fb1a7f40e304fc8fd05767a086b912cf4288a6',
 'ResearchHistory/UQCF-GEM/demos/v16.53-four-child-boundary/cover.py': '7680cbacb22eac984f5377ad0b679e95b4632785',
 'ResearchHistory/UQCF-GEM/demos/v16.53-four-child-boundary/coverage.py': 'e90576a0285357f62ca2f9d9cac872b2a226e823',
 'ResearchHistory/UQCF-GEM/demos/v16.53-four-child-boundary/evidence/science-artifact.chunks/ARCHIVE.json': '7c6bffcc122b976c853d190ef270f290cc3fa486',
 'ResearchHistory/UQCF-GEM/demos/v16.53-four-child-boundary/feasibility.py': '9e995e21c9a477034a2fd4be615e28a2551b0bf9',
 'ResearchHistory/UQCF-GEM/demos/v16.53-four-child-boundary/producer.py': '0501a1b32c0a660646ff95ecbb8a37a8f2e04b80',
 'ResearchHistory/UQCF-GEM/demos/v16.53-four-child-boundary/verifier.py': '54e23706c170d0bb82c1b78161290145b6b99af7',
 'ResearchHistory/UQCF-GEM/foundational-closure-verification/lineage.py': 'e95e3e978779164dd91f09b80e3389247e6320c2'}
MEMBERS = {
    "16.52": ("scientific/parent52/CERTIFICATE.json.gz",
              "374769815047dbfeebf14cc73b628ca4510dc385075cfb67e440b5a20533f0b9", 7236),
    "16.53": ("scientific/CERTIFICATE.json.gz",
              "bad1d22fb839dcf904fda3acdb4defc63bc1eeda3a6c680528d434aaa66128d1", 2863),
}


def module(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    result = importlib.util.module_from_spec(spec)
    sys.modules[name] = result
    spec.loader.exec_module(result)
    return result


def archives():
    meta = json.loads(ARCHIVE.read_bytes())
    parent_meta = json.loads(PARENT_ARCHIVE.read_bytes())
    assert parent_meta["sha256"] == "86eb8509a7553e886ea93910f466d37ff0ff31ee385f3d33c9d7a198f30d6f31"
    assert meta["sha256"] == "089a43e34bcab29722429896610f10599b8c971fa70545930276f4c56763961c"
    with TemporaryFile() as out:
        digest = sha256()
        for chunk in meta["chunks"]:
            raw = ARCHIVE.with_name(chunk["name"]).read_bytes()
            assert len(raw) == chunk["size"] and sha256(raw).hexdigest() == chunk["sha256"]
            digest.update(raw)
            out.write(raw)
        assert out.tell() == meta["size"] and digest.hexdigest() == meta["sha256"]
        with ZipFile(out) as z:
            return {ver: unpack(z, path, digest, count) for ver, (path, digest, count) in MEMBERS.items()}


def unpack(zipfile, name, checksum, count):
    compressed = zipfile.read(name)
    assert sha256(compressed).hexdigest() == checksum
    doc = json.loads(gzip.decompress(compressed))
    assert len(doc.get("records", doc.get("cases"))) == count
    return doc


def state_views(raw, n):
    return [[v for v in range(n) if mask & (1 << v)] for mask in raw]


def own_history(path, view):
    return [mask for mask, _ in groupby(s[view] for s in path)]


def first_write(path, position, view):
    """Return the first actual local update after the source transition."""
    before = path[position + 1][view]
    for k in range(position + 2, len(path)):
        after = path[k][view]
        if before != after:
            edited = before ^ after
            assert edited.bit_count() == 1
            return {"vertex": edited.bit_length() - 1, "add": bool(after & edited),
                    "before": before, "after": after, "state_index": k}
    return None


def case_report(m, event_verify, lineage, parents, path, position, actor, leaf, receiver):
    before, after = (state_views(path[k], len(parents)) for k in (position, position+1))
    event = m.atomic(parents, before, actor, leaf)
    assert event_verify.verify_atomic(event) == (event["delta_h"], event["trigger"])
    assert event["after"] == after
    change = first_write(path, position, receiver)
    keys = [()]
    for v, parent in enumerate(parents[1:], 1):
        keys.append(keys[parent] + (v,))
    ambient = lineage.Carrier("historical-writer-replay", tuple(keys))

    def grade(raw):
        addresses = tuple(keys[v] for v in range(len(keys)) if raw & (1 << v))
        coarse = lineage.Carrier(ambient.genesis, addresses)
        vector = lineage.Pruning(ambient, coarse).aggregate((1,) * len(keys))
        assert all(v.denominator == 1 for v in vector)
        return list(map(int, vector))

    grade_before = grade(path[position + 1][receiver])
    grade_after = grade(change["after"]) if change else grade_before
    return {"event": event, "position": position, "first_write": change,
            "prior_receiver_history": own_history(path[:position + 2], receiver),
            "future_receiver_history": own_history(path[position + 1:], receiver),
            "receiver_grade_before": grade_before, "receiver_grade_after_first_write": grade_after}


def main(out):
    for path, digest in PINS.items():
        raw = Path(path).read_bytes()
        assert sha1(f"blob {len(raw)}\0".encode() + raw).hexdigest() == digest, path
    archived = archives()
    atom = module(ATOM / "engine.py", "frozen_atom")
    verify_atom = module(ATOM / "verify.py", "frozen_atomic_verifier")
    lin = module(LINEAGE, "frozen_lineage")
    records = {}
    for version, directory, selected in (("16.52", TERNARY, (5402, 5403)), ("16.53", FOUR, (2835,))):
        module(directory / "coverage.py", "coverage")
        if version == "16.53":
            for name in ("cover", "feasibility"):
                module(directory / f"{name}.py", name)
        maker = module(directory / "producer.py", f"production_{version}")
        old_verifier = module(directory / "verifier.py", f"verifier_{version}")
        regenerated = json.loads(json.dumps(maker.produce()))
        assert regenerated == archived[version]
        original_rows = regenerated.get("records", regenerated.get("cases"))
        for row_number in selected:
            row = original_rows[row_number]
            if version == "16.52":
                s = row["spec"]
                t, k, q = maker.TREES[s["tree"]], s["k"], s["q"]
                _, start, end = old_verifier.model(t, q, k, s["permutation"], s["mode"])
                assert row["failure"] is None
            else:
                _, title, q, k, perm, mode = row["identity"]
                t = maker.TREES[title]
                _, start, end = old_verifier.model(t, q, k, perm, mode)
                assert row["status"] == "ok" and row["end"] == end
            assert row["start"] == start
            peak = old_verifier.path_check(t, k, q, row["path"], start, end)
            trace = []
            assert maker.normalize(start, t, k, q, trace=trace) == row["path"]
            nodes = maker.layout(t)
            parents = [-1] * len(nodes)
            for i, children in enumerate(nodes):
                for v in children:
                    parents[v] = i
            records[row_number] = {"row": row, "trace": trace, "q": q, "parents": parents, "peak": peak}

    def replay(number, pos, actor, leaf, receiver):
        data = records[number]
        return case_report(atom, verify_atom, lin, data["parents"], data["row"]["path"], pos, actor, leaf, receiver)

    path = records[2835]["row"]["path"]
    assert path[:11] == path[22:]
    broad = (1 << 6) | (1 << 7) | (1 << 8)
    for before, after in zip(path[10:22], path[11:23], strict=True):
        assert all((u ^ v) & ~broad == 0 for u, v in zip(before, after, strict=True))
    assert records[2835]["q"] == [2, 3]
    silent = []
    same_run = []
    for first, second, actor, delta in ((8, 30, 0, 0), (9, 31, 1, 1)):
        early, late = replay(2835, first, actor, 5, 2), replay(2835, second, actor, 5, 2)
        assert early["event"] == late["event"] and early["event"]["delta_h"] == delta
        assert early["event"]["trigger"] == bool(delta)
        assert early["first_write"] == {"vertex": 6, "add": True, "before": 35, "after": 99, "state_index": 12}
        assert late["first_write"] is None and late["future_receiver_history"] == [35]
        assert [early["receiver_grade_before"][0], early["receiver_grade_after_first_write"][0]] == [4, 3]
        same_run.append([early, late])
        silent.append(late)

    active, passive = replay(5402, 9, 2, 1, 1), replay(5403, 4, 2, 1, 1)
    assert records[5402]["q"] == records[5403]["q"] == [2, 2, 1, 2, 1, 1]
    assert active["event"] == passive["event"]
    assert active["prior_receiver_history"] == passive["prior_receiver_history"] == [122947]
    assert active["first_write"] == {"vertex": 7, "add": True, "before": 122947, "after": 123075, "state_index": 11}
    assert passive["first_write"] is None and passive["future_receiver_history"] == [122947]
    assert active["future_receiver_history"][-1] == 122947
    assert [active["receiver_grade_before"][0], active["receiver_grade_after_first_write"][0]] == [7, 1]
    assert records[5402]["trace"][0]["label"] == 2 and records[5403]["trace"][0]["label"] == 0
    assert {"kind": "local_hole", "child": 7, "label": 1} in records[5402]["trace"]
    assert all(t["kind"] != "local_hole" for t in records[5403]["trace"])

    invalid = deepcopy(same_run[0][0]["event"])
    invalid["leaf"] = 1
    try:
        verify_atom.verify_atomic(invalid)
    except ValueError:
        pass
    else:
        raise AssertionError("substituted event accepted")
    changed_prefix = deepcopy(records[5403]["row"]["path"][:6])
    changed_prefix[0][1] ^= 1 << 7
    assert own_history(changed_prefix, 1) != active["prior_receiver_history"]
    assert all(x["first_write"] is None for x in [*silent, passive])

    report = {
        "archive_zip_sha256": json.loads(ARCHIVE.read_bytes())["sha256"],
        "archive_members": {k: [path, digest, count] for k, (path, digest, count) in MEMBERS.items()},
        "rows": records, "same_run": same_run, "same_receiver_history": [active, passive],
        "controls": ["false_atom_rejected", "false_local_history_rejected", "silent_suffix_checked"],
    }
    out.mkdir(parents=True, exist_ok=True)
    raw = (json.dumps(report, sort_keys=True, indent=2) + "\n").encode()
    (out / "native_writer_phase_certificate.json").write_bytes(raw)
    return {"certificate_sha256": sha256(raw).hexdigest(), "archived_rows_regenerated": [7236, 2863],
            "identical_atom_pairs": 3, "rising_pair": [2, 3], "changed_grades": [[4, 3], [7, 1]],
            "same_receiver_history": True, "same_run_repeat": True, "silent_controls": 3}


if __name__ == "__main__":
    print(json.dumps(main(Path(sys.argv[1])), sort_keys=True, indent=2))
