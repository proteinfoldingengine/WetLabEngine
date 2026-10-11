#!/usr/bin/env python3
"""Canonical exhaustive producer for the frozen C3/star-carrier scope."""
if not __debug__:
    raise RuntimeError("producer requires assertions enabled")

import gzip
import hashlib
import itertools
import json
import pathlib
import sys

SCHEMA = "c3-star-carrier-v1"
SCOPE_COMMIT = "365d55c497d65f6003b5e7f8691438280e62c3fe"


def configurations(fixture=False):
    if fixture:
        yield (3, 3, 1)
        return
    for m in (3, 4):
        for n in (3, 4):
            for floor in (1, 2):
                yield (m, n, floor)


def decode(code, m, n):
    base = 1 << n
    masks = []
    for _ in range(m):
        masks.append(code % base)
        code //= base
    return tuple(masks)


def encode(masks, n):
    base = 1 << n
    value = 0
    for mask in reversed(masks):
        value = value * base + mask
    return value


def tau_c3(masks, n):
    """Minimum label subset meeting every indexed support; n+1 means none."""
    for size in range(n + 1):
        for labels in itertools.combinations(range(n), size):
            cover = sum(1 << x for x in labels)
            if all(mask & cover for mask in masks):
                return size
    return n + 1


def h_star(children, n):
    """Independent subset scan for the depth-one parent's child hitting number."""
    candidates = sorted(range(1 << n), key=lambda x: (x.bit_count(), x))
    for candidate in candidates:
        if all(candidate & child for child in children):
            return candidate.bit_count()
    return n + 1


def state_facts(masks, n, floor):
    floor_ok = all(mask.bit_count() >= floor for mask in masks)
    tau = tau_c3(masks, n)
    h = h_star(masks, n)
    assert tau == h
    admitted = floor_ok and 3 <= tau <= 4
    return floor_ok, tau, h, admitted


def rejection(source, target):
    sf, st, _, sa = source
    tf, tt, _, ta = target
    if not sf:
        return "SOURCE_FLOOR"
    if not 3 <= st <= 4:
        return "SOURCE_BAND"
    if not tf:
        return "TARGET_FLOOR"
    if not 3 <= tt <= 4:
        return "TARGET_BAND"
    assert sa and ta
    return "ACCEPTED"


def rows_for(config):
    m, n, floor = config
    total = (1 << n) ** m
    facts = []
    counts = {
        "states": total,
        "admitted_states": 0,
        "toggle_candidates": total * m * n,
        "admitted_edges": 0,
        "SOURCE_FLOOR": 0,
        "SOURCE_BAND": 0,
        "TARGET_FLOOR": 0,
        "TARGET_BAND": 0,
    }
    for code in range(total):
        masks = decode(code, m, n)
        fact = state_facts(masks, n, floor)
        facts.append(fact)
        counts["admitted_states"] += int(fact[3])
        yield {
            "kind": "state",
            "config": [m, n, floor],
            "id": code,
            "masks": list(masks),
            "floor_ok": fact[0],
            "tau": fact[1],
            "h": fact[2],
            "admitted": fact[3],
        }, counts
    for source_code in range(total):
        masks = decode(source_code, m, n)
        for child in range(m):
            for label in range(n):
                target_masks = list(masks)
                bit = 1 << label
                sign = 0 if target_masks[child] & bit else 1
                target_masks[child] ^= bit
                target_code = encode(target_masks, n)
                reason = rejection(facts[source_code], facts[target_code])
                accepted = reason == "ACCEPTED"
                counts["admitted_edges"] += int(accepted)
                if not accepted:
                    counts[reason] += 1
                yield {
                    "kind": "transition",
                    "config": [m, n, floor],
                    "source": source_code,
                    "target": target_code,
                    "child": child,
                    "label": label,
                    "sign": sign,
                    "c3": accepted,
                    "star": accepted,
                    "reason": reason,
                }, counts


def build(output_path, fixture=False):
    output = pathlib.Path(output_path)
    stream = pathlib.Path(str(output) + ".identities.jsonl.gz")
    per_config = []
    global_counts = {
        "configurations": 0,
        "states": 0,
        "admitted_states": 0,
        "toggle_candidates": 0,
        "admitted_edges": 0,
        "SOURCE_FLOOR": 0,
        "SOURCE_BAND": 0,
        "TARGET_FLOOR": 0,
        "TARGET_BAND": 0,
    }
    with stream.open("wb") as raw:
        with gzip.GzipFile(filename="", mode="wb", fileobj=raw, mtime=0) as archive:
            for config in configurations(fixture):
                final_counts = None
                for row, counts in rows_for(config):
                    archive.write((json.dumps(row, sort_keys=True, separators=(",", ":")) + "\n").encode())
                    final_counts = counts
                assert final_counts is not None
                item = {"m": config[0], "palette": config[1], "floor": config[2], **final_counts}
                per_config.append(item)
                global_counts["configurations"] += 1
                for key in global_counts:
                    if key != "configurations":
                        global_counts[key] += final_counts[key]
    certificate = {
        "schema": SCHEMA,
        "scope_commit": SCOPE_COMMIT,
        "fixture": fixture,
        "counts": global_counts,
        "configurations": per_config,
        "identity_archive_sha256": hashlib.sha256(stream.read_bytes()).hexdigest(),
    }
    output.write_text(json.dumps(certificate, sort_keys=True, indent=2) + "\n")
    return certificate


if __name__ == "__main__":
    result = build(sys.argv[1], "--fixture" in sys.argv[2:])
    print(json.dumps(result["counts"], sort_keys=True))
