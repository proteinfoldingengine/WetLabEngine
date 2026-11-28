"""Replay new controlled M9 inputs and certify the fixed-target archive control."""
import argparse
import gzip
import json
import os
import sys
from hashlib import sha256
from itertools import combinations
from pathlib import Path

from replay import FIRST, HERE, LINE_PINS, PINS, local_history, slot_values


BASE = [[0, 2], [0, 2, 3, 6], [3, 6], [1, 3, 4, 5], [0, 2, 4, 6, 7], [5, 7]]
PILOT = [[0, 1], [3, 7], [0, 1, 3], [0, 1, 3, 4, 5, 6], [0, 5], list(range(8))]
PILOT_TARGET = [[1, 6, 7], [2, 6], [5, 6], [4, 5], [0, 1, 4, 6], [0, 1, 2, 5, 7]]


def add_source(rows, label):
    return [sorted(set(rows[0]) | {label}), *rows[1:]]


def transform(rows, shift=1, reversal=1):
    mapped = [sorted(7 - x for x in row) if reversal else list(row) for row in rows]
    return [mapped[(j - shift) % len(rows)] for j in range(len(rows))]


def cover(rows):
    supports = [set(row) for row in rows]
    labels = sorted(set.union(*supports))
    for size in range(1, len(labels) + 1):
        for group in combinations(labels, size):
            if all(row.intersection(group) for row in supports):
                return group
    raise ValueError("Uncovered row")


def changed(left, right):
    return [(i, x) for i, (a, b) in enumerate(zip(left, right, strict=True))
            for x in sorted(set(a) ^ set(b))]


def registers(record, frame):
    nodes = record["nodes"]
    return [slot_values(record["nested_path"][frame], nodes[parent]) for parent in nodes[0]]


def suffix_size(left, right):
    for count, (a, b) in enumerate(zip(reversed(left), reversed(right))):
        if a != b:
            return count
    return min(len(left), len(right))


def word(path, row):
    return [v[row] for n, v in enumerate(path) if n == 0 or v[row] != path[n-1][row]]


def encoded(record):
    return (json.dumps(record, sort_keys=True, separators=(",", ":")) + "\n").encode()


def archive_control():
    lines = gzip.decompress((HERE / "original_m9.jsonl.gz").read_bytes()).splitlines(keepends=True)
    assert tuple(sha256(line).hexdigest() for line in lines) == LINE_PINS
    results = []
    for ordinal, line in enumerate(lines, FIRST):
        _, p, rows, ch = json.loads(line)["identity"]
        count = guards = width = 0
        for i, old in enumerate(rows):
            for x in range(p["k"]):
                edit = sorted(set(old) ^ {x})
                if len(edit) < p["h"]:
                    continue
                new = rows[:i] + [edit] + rows[i+1:]
                groups = cover(new + ch["target"])
                width = max(width, len(groups))
                assert len(groups) <= p["q"]
                guards += len(cover(new[:p["N"]])) == p["q"]-1
                count += 1
        results.append([ordinal, count, guards, width])
    assert results == [[2393446, 127, 107, 4], [2393447, 22, 19, 3],
                       [2393448, 41, 37, 3], [2393449, 58, 46, 4]]
    return results


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("demo", type=Path)
    parser.add_argument("--write-records", type=Path)
    args = parser.parse_args()
    raw_file = args.write_records.resolve() if args.write_records else None
    demo = args.demo.resolve()
    for file, expected in PINS.items():
        assert sha256((demo / file).read_bytes()).hexdigest() == expected
    os.chdir(demo)
    sys.path.insert(0, str(demo))
    import mechanisms
    import universe
    import verifier

    frozen = [c["identity"] for c in universe.m9({})]
    raw_lines = []

    def experiment(rows, target, shift=1, reversal=1):
        c = universe.case("M9", "native", 8, [2]*6, 3, rows,
                          dict(shift=shift, reversal=reversal, target=target), h=2, N=3)
        assert c["identity"] not in frozen
        r = mechanisms.produce(c)
        assert r["status"] == "PASS" and verifier.verify_record(c, r) == []
        assert r["path"][-1] == target
        raw_lines.append(encoded(r))
        return r

    # One source incidence and both endpoints of the historical shift/reversal formula.
    inputs = [BASE, add_source(BASE, 4)]
    targets = [transform(rows) for rows in inputs]
    assert changed(*inputs) == [(0, 4)] and changed(*targets) == [(1, 3)]
    matrix = [[experiment(rows, target) for target in targets] for rows in inputs]
    for s, row in enumerate(matrix):
        for t, r in enumerate(row):
            assert r["tau"][0] == r["tau"][-1] == 3
            assert registers(r, 0)[4] == (0, 2)
            assert registers(r, -1)[4] == ((2, 3) if s == 0 else (3, 2))
            assert r["nodes"][r["nodes"][0][4]] == [14, 15]
            hist = local_history(r, 4)
            writes = [e for e in hist if e["slots_after"] != e["slots_before"]]
            assert [e["x"] for e in writes[:2]] == ([2, 0] if s == 0 else [0, 2])
            tail = writes[-3:]
            assert [e["x"] for e in tail] == [4, 0, 1]
            assert [e["changes"][0][:2] for e in tail] == (
                [(14, 0), (14, 2), (15, 3)] if s == 0 else [(15, 0), (15, 2), (14, 3)])
            pre = r["facts"]["parent_record"]["facts"]["preliminary_path"]
            assert cover(pre[5]) == ((0, 1, 3, 5) if s == 0 else (3, 4, 5))
            chosen = (0, 2, 3, 5) if s == 0 else (2, 3, 5)
            assert all(set(pre[5][i]).isdisjoint(pre[5][j]) for i, j in combinations(chosen, 2))
            assert max(map(len, (cover(v) for v in pre))) == (4 if (s, t) != (1, 1) else 3)
            end = registers(r, -1)[4]
            same = sum(a == b for a, b in zip(registers(r, 0)[4], end))
            print(f"source={s} target={t} parent/nested frames={len(r['path'])}/{len(r['nested_path'])}"
                  f" receiver={end} own initial labels retained={same}"
                  f" common-withdrawal frames={[e['parent_frame'] for e in tail]}")
    for t in range(2):
        a, b = matrix[0][t], matrix[1][t]
        assert a["nodes"] == b["nodes"]
        assert changed(a["nested_path"][0], b["nested_path"][0]) == [(a["nodes"][0][0], 4)]
        assert a["path"][-1] == b["path"][-1]
        assert changed(a["nested_path"][-1], b["nested_path"][-1]) == [(14, 2), (14, 3), (15, 2), (15, 3)]
        n = suffix_size(a["path"], b["path"])
        assert n == (42, 38)[t]
        pa, pb = [r["facts"]["parent_record"]["facts"]["preliminary_path"] for r in (a, b)]
        assert word(pa, 4) == word(pb, 4)
        assert changed(pa[5], pb[5]) == [(0, 4)]
        # All three readouts occur on common full parent transitions in this suffix.
        offsets = []
        for r in (a, b):
            writes = [e for e in local_history(r, 4) if e["slots_after"] != e["slots_before"]]
            assert writes[-3]["parent_frame"] > len(r["path"]) - n
            offsets.append([e["parent_frame"] - len(r["path"]) for e in writes[-3:]])
        assert offsets[0] == offsets[1] == [-15, -7, -6]
        print(f"fixed target {t}: {n} identical terminal parent frames, only leaves 14 and 15 differ")
    pilot = [experiment(rows, PILOT_TARGET) for rows in (PILOT, add_source(PILOT, 2))]
    assert changed(pilot[0]["nested_path"][0], pilot[1]["nested_path"][0]) == [(1, 2)]
    assert suffix_size(pilot[0]["path"], pilot[1]["path"]) == 37
    for s, r in enumerate(pilot):
        e = [w for w in local_history(r, 5) if w["slots_after"] != w["slots_before"]][-1]
        assert e["before"] == [0, 1, 2, 5, 6, 7] and e["x"] == 6
        assert e["changes"][0] == ((18, 17)[s], 0, True)
        assert registers(r, -1)[5] == ((5, 0), (0, 5))[s]
    print("Pilot receiver 5: withdraw 6, native destination for 0 is leaf 18 versus 17")
    # All cyclic shifts crossed with both permitted label mappings. For each
    # pairing compare the two sources twice, each time freezing the full target.
    for reversal in (0, 1):
        for shift in range(6):
            crossing = matrix if (reversal, shift) == (1, 1) else [
                [experiment(rows, transform(other, shift, reversal), shift, reversal)
                 for other in inputs] for rows in inputs]
            for t in range(2):
                left, right = crossing[0][t], crossing[1][t]
                assert left["path"][-1] == right["path"][-1]
                assert changed(left["nested_path"][0], right["nested_path"][0]) == [(1, 4)]
                la, lb = registers(left, -1), registers(right, -1)
                different = [j for j in range(1, 6) if la[j] != lb[j]]
                assert different == ([4] if reversal else [])
                if reversal:
                    assert la[4] == lb[4][::-1]
        print(f"reversal={reversal}: all six shifts and both fixed-target contrasts checked")
    print("Archive controls [ordinal, floor-preserving flips, original guard rank preserved, maximum cover size]")
    print(archive_control())
    raw = b"".join(raw_lines)
    if raw_file:
        with raw_file.open("wb") as stream, gzip.GzipFile(filename="", fileobj=stream, mode="wb", mtime=0) as gz:
            gz.write(raw)
    else:
        assert gzip.decompress((HERE / "remote_records.jsonl.gz").read_bytes()) == raw
    print(f"{len(raw_lines)} full new records verified; uncompressed SHA-256 {sha256(raw).hexdigest()}")


if __name__ == "__main__":
    main()
