#!/usr/bin/env python3
"""Independent complete reconstruction; does not import the producer."""
if not __debug__:
    raise RuntimeError("independent checker requires assertions enabled")

import gzip
import hashlib
import json
import pathlib
import sys

SCHEMA = "c3-star-carrier-v1"
SCOPE_COMMIT = "365d55c497d65f6003b5e7f8691438280e62c3fe"


def configurations(fixture=False):
    values = [(3, 3, 1)] if fixture else [
        (m, n, f) for m in (3, 4) for n in (3, 4) for f in (1, 2)
    ]
    yield from values


def unpack(number, child_count, palette_size):
    width = 2 ** palette_size
    result = []
    for _ in range(child_count):
        result.append(number % width)
        number //= width
    return tuple(result)


def pack(children, palette_size):
    width = 2 ** palette_size
    result = sum(value * width ** i for i, value in enumerate(children))
    return result


def hitting(children, palette_size):
    possible = list(range(2 ** palette_size))
    possible.sort(key=lambda value: (sum((value >> j) & 1 for j in range(palette_size)), value))
    for candidate in possible:
        if all(candidate & child for child in children):
            return sum((candidate >> j) & 1 for j in range(palette_size))
    return palette_size + 1


def star_h(children, palette_size):
    for k in range(palette_size + 1):
        for candidate in range(2 ** palette_size):
            if candidate.bit_count() == k and all(child & candidate for child in children):
                return k
    return palette_size + 1


def facts(children, palette_size, minimum):
    floor_ok = all(sum((child >> j) & 1 for j in range(palette_size)) >= minimum for child in children)
    t = hitting(children, palette_size)
    h = star_h(children, palette_size)
    assert t == h
    return floor_ok, t, h, floor_ok and t in (3, 4)


def reason(source, target):
    if not source[0]:
        return "SOURCE_FLOOR"
    if source[1] not in (3, 4):
        return "SOURCE_BAND"
    if not target[0]:
        return "TARGET_FLOOR"
    if target[1] not in (3, 4):
        return "TARGET_BAND"
    return "ACCEPTED"


def expected_rows(config):
    m, n, minimum = config
    total = (2 ** n) ** m
    all_facts = []
    counts = {k: 0 for k in (
        "admitted_states", "admitted_edges", "SOURCE_FLOOR", "SOURCE_BAND",
        "TARGET_FLOOR", "TARGET_BAND"
    )}
    counts.update(states=total, toggle_candidates=total * m * n)
    for state_id in range(total):
        children = unpack(state_id, m, n)
        state = facts(children, n, minimum)
        all_facts.append(state)
        counts["admitted_states"] += state[3]
        yield {
            "kind": "state", "config": [m, n, minimum], "id": state_id,
            "masks": list(children), "floor_ok": state[0], "tau": state[1],
            "h": state[2], "admitted": state[3],
        }, counts
    for source_id in range(total):
        children = list(unpack(source_id, m, n))
        for child_index in range(m):
            for label in range(n):
                changed = children.copy()
                present = bool(changed[child_index] & (1 << label))
                changed[child_index] ^= 1 << label
                target_id = pack(changed, n)
                why = reason(all_facts[source_id], all_facts[target_id])
                accepted = why == "ACCEPTED"
                counts["admitted_edges"] += accepted
                if not accepted:
                    counts[why] += 1
                yield {
                    "kind": "transition", "config": [m, n, minimum],
                    "source": source_id, "target": target_id, "child": child_index,
                    "label": label, "sign": 0 if present else 1,
                    "c3": accepted, "star": accepted, "reason": why,
                }, counts


def verify(certificate_path, fixture=False):
    certificate_file = pathlib.Path(certificate_path)
    data = json.loads(certificate_file.read_text())
    assert data["schema"] == SCHEMA
    assert data["scope_commit"] == SCOPE_COMMIT
    assert data["fixture"] is fixture
    stream_path = pathlib.Path(str(certificate_file) + ".identities.jsonl.gz")
    assert hashlib.sha256(stream_path.read_bytes()).hexdigest() == data["identity_archive_sha256"]
    global_counts = {k: 0 for k in data["counts"]}
    summaries = []
    try:
        with gzip.open(stream_path, "rt", encoding="utf-8") as stream:
            for config in configurations(fixture):
                final = None
                for expected, counts in expected_rows(config):
                    line = stream.readline()
                    assert line, "truncated canonical stream"
                    actual = json.loads(line)
                    assert actual == expected, "complete row mismatch"
                    final = counts
                assert final is not None
                summary = {"m": config[0], "palette": config[1], "floor": config[2], **final}
                summaries.append(summary)
                global_counts["configurations"] += 1
                for key in global_counts:
                    if key != "configurations":
                        global_counts[key] += final[key]
            assert stream.readline() == "", "extra canonical row"
    except (OSError, EOFError, json.JSONDecodeError) as exc:
        raise AssertionError("corrupt canonical stream") from exc
    assert summaries == data["configurations"]
    assert global_counts == data["counts"]
    return {
        "accepted": True,
        "counts": global_counts,
        "certificate_sha256": hashlib.sha256(certificate_file.read_bytes()).hexdigest(),
        "canonical_sha256": data["identity_archive_sha256"],
    }


if __name__ == "__main__":
    result = verify(sys.argv[1], "--fixture" in sys.argv[3:])
    pathlib.Path(sys.argv[2]).write_text(json.dumps(result, sort_keys=True, indent=2) + "\n")
    print(json.dumps(result, sort_keys=True))
