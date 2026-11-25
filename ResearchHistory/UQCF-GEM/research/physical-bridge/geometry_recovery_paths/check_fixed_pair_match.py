"""Compare complete local numeric payloads and all six archived cover fields."""
from collections import Counter
from itertools import combinations
import json
import lzma
from pathlib import Path
import sys

from check_fixed_pair import Reader, minimum_covers, modules, require, views, wire

FIELDS = ("tau_before", "tau_after", "h_before", "h_after", "delta_h", "trigger")


def main(history, directory):
    raw = json.loads(lzma.decompress((directory / "fixed_pair_universe.json.xz").read_bytes()))
    reader = Reader(modules(history))
    rows = {}
    witness = {}
    p, grade = (-1, 0, 0, 0, 0), (3, 1, 1, 1, 1)
    for key, prep in raw["star"]["preparations"].items():
        before = views(tuple(map(int, key)), 3)
        minimum = minimum_covers(before, range(5))
        partner = [x for x in minimum if len(x) == 2 and 1 in x] == [[0, 1]]
        exclusive_pair = minimum == [[0, 1]]
        arms = {}
        for leaf in map(int, prep["cuts"]):
            event = reader.op["cut"].atomic(p, before, 1, leaf)
            reader.op["gate"].verify_atomic(event)
            after = tuple(map(tuple, event["after"]))
            snap = reader.observe(p, after, grade)
            arms[leaf] = ([event[f] for f in FIELDS], snap)
        for a, b in combinations(sorted(arms), 2):
            meta_a, x = arms[a]
            meta_b, y = arms[b]
            payload = x["local"] == y["local"]
            matched = meta_a == meta_b
            different = x["pair"][0] != y["pair"][0]
            flags = (payload, matched, different, partner, exclusive_pair)
            rows[f"{key}/{a}/{b}"] = "".join("1" if f else "0" for f in flags)
            require(not (matched and different and exclusive_pair), "globally unique pair under a cover-matched contrast")
            if key == "6316" and (a, b) == (1, 2):
                witness = dict(prior=reader.observe(p, before, grade), covers=minimum, leaves=[a, b], fields=list(FIELDS),
                               arms=[dict(cover=meta_a, reading=x), dict(cover=meta_b, reading=y)])
    require(witness, "registered example missing")
    counts = dict(sorted(Counter(rows.values()).items()))
    summary = dict(pairs=len(rows), equal_payloads=sum(v[0] == "1" for v in rows.values()),
                   equal_cover_and_contrast=sum(v[:3] == "111" for v in rows.values()),
                   equal_cover_contrast_unique_partner=sum(v[:4] == "1111" for v in rows.values()),
                   equal_cover_contrast_unique_global_pair=sum(v == "11111" for v in rows.values()))
    out = dict(identities=rows, partition=counts, summary=summary, witness=witness)
    (directory / "fixed_pair_matched.json.xz").write_bytes(lzma.compress(wire(out), preset=6))
    print(json.dumps(summary, sort_keys=True))


if __name__ == "__main__":
    main(Path(sys.argv[1]), Path(sys.argv[2]))
