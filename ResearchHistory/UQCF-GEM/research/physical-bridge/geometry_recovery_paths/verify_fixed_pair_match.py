"""Reconstruct the five-way partition directly from chart subsets and the tree grading."""
from collections import Counter
from itertools import combinations, product
import json
import lzma
from pathlib import Path
import sys

from verify_fixed_pair import compare, covers, encoded, label, members, need, read


def main(directory):
    p, g = (-1, 0, 0, 0, 0), (3, 1, 1, 1, 1)
    expected = {}
    for r, s, h in product(range(1, 32, 2), repeat=3):
        if r | s != 31:
            continue
        sets = (r, s, h)
        prior_covers = covers(sets, 31)
        partner = [0, 1] in prior_covers and [1, 2] not in prior_covers
        unique = prior_covers == [[0, 1]]
        for a, b in combinations(members(s & (r | h) & ~1, 5), 2):
            changed = [(r, s & ~(1 << v), h) for v in (a, b)]
            counts = [len(covers(t, 31)[0]) for t in changed]
            # Every leaf has unit grade. Each local raw array is determined by this
            # chart's cardinality once its root is known. The two source sizes agree.
            same_payload = all(i.bit_count() == j.bit_count() for i, j in zip(*changed))
            contrast = bool(r & 1 << a) != bool(r & 1 << b)
            same_cover = counts[0] == counts[1]
            expected[f"{label(sets)}/{a}/{b}"] = "".join(str(int(x)) for x in
                (same_payload, same_cover, contrast, partner, unique))
    cases = (directory / "fixed_pair_matched.json.xz").read_bytes()
    raw = json.loads(lzma.decompress(cases))
    flags = list(expected.values())
    summary = dict(pairs=len(flags), equal_payloads=sum(row[0] == "1" for row in flags),
                   equal_cover_and_contrast=sum(row.startswith("111") for row in flags),
                   equal_cover_contrast_unique_partner=sum(row.startswith("1111") for row in flags),
                   equal_cover_contrast_unique_global_pair=flags.count("11111"))
    before = (13, 23, 19)
    witness = dict(prior=read(p, before, g), covers=[[0, 1], [0, 2]], leaves=[1, 2],
                   fields=["tau_before", "tau_after", "h_before", "h_after", "delta_h", "trigger"],
                   arms=[dict(cover=[2, 2, 2, 2, 0, False], reading=read(p, (13, after, 19), g))
                         for after in (21, 19)])
    compare(dict(identities=expected, partition=dict(Counter(flags)), summary=summary, witness=witness), raw)
    need(lzma.decompress(cases) == encoded(raw), "noncanonical output")
    a, b = (z["reading"] for z in witness["arms"])
    need(a["pair"][0] == 4 and b["pair"][0] == 3 and a["local"] == b["local"]
         and a["local"][0] == [5, 1, 1] and a["total"] == b["total"] == 7, "matched example")
    need(summary["equal_cover_and_contrast"] > 0 and summary["equal_cover_contrast_unique_partner"] > 0
         and summary["equal_cover_contrast_unique_global_pair"] == 0, "supplement predictions")
    print(json.dumps(dict(status="PASS", **summary), sort_keys=True))


if __name__ == "__main__":
    main(Path(sys.argv[1]))
