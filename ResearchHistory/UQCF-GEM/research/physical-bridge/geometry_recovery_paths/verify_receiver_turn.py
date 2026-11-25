"""Rebuild all receiver moves directly from tip multiplicities and local atom addition."""
from copy import deepcopy
from hashlib import sha256
import json
import lzma
from pathlib import Path
import sys

from verify_fixed_pair import compare, encoded, need


def trees(last=6, nodes=(-1,)):
    if len(nodes) >= 3:
        yield nodes
    if len(nodes) != last:
        for father in range(len(nodes)):
            yield from trees(last, nodes + (father,))


def local_after(g, p, leaf=None):
    record = [[i, n] for i, n in enumerate(g) if i != leaf]
    if leaf is not None:
        for atom in record:
            if atom[0] == p[leaf]:
                atom[1] += g[leaf]
    return record


def build(p, g, l, s):
    same_parent = p[l[0]] == p[l[1]]
    parent_fields = [1, 2, 1, 2, 1, True] if same_parent else [1, 1, 1, 1, 0, False]
    rows = {}
    for lost, available in (l, l[::-1]):
        order = {}
        for v in range(len(g)):
            if v == 0:
                result = "leaf"
            elif v == lost:
                result = "same union"
            elif v == available:
                result = "legal"
            else:
                result = "non-leaf"
            order[str(v)] = result
        rows[str(lost)] = dict(receiver=1-s, source_fields=[1, 1, 1, 1, 0, False],
                                source_payload=local_after(g, p, lost), receiver_before=local_after(g, p),
                                candidate_status=order, executed=available, receiver_fields=parent_fields,
                                receiver_after=local_after(g, p, available), other_order=local_after(g, p),
                                third_chart_choices=list(l))
    return rows


def independent():
    result = {}
    diff = sib = tested = 0
    for p in trees():
        degrees = [0] * len(p)
        for parent in p[1:]:
            degrees[parent] += 1
        leaves = tuple(i for i, degree in enumerate(degrees) if degree == 0)
        if len(leaves) != 2:
            continue
        g = tuple(3 if i == 0 else (4 if degrees[i] else 2) for i in range(len(p)))
        result["/".join(map(str, p))] = {str(s): build(p, g, leaves, s) for s in range(2)}
        if p[leaves[0]] == p[leaves[1]]:
            sib += 2
        else:
            diff += 2
        tested += 4 * len(p)
    count = dict(parent_arrays=len(result), source_role_pairs=diff+sib, histories=2*(diff+sib),
                 distinct_parent_pairs=diff, sibling_pairs=sib, distinguished_receiver_parent=diff,
                 matched_source_and_receiver_cover=diff+sib, candidate_trials=tested, positive_receiver_moves=2*(diff+sib))
    witness = build((-1, 0, 0, 2, 1, 3), (3, 4, 1, 4, 2, 2), (4, 5), 1)
    return dict(trees=result, witness=witness, counts=count)


def main(folder):
    data = lzma.decompress((folder / "receiver_turn_universe.json.xz").read_bytes())
    expected = independent()
    compare(expected, json.loads(data))
    need(data == encoded(expected), "raw identity")
    cert = dict(raw_sha256=sha256(data).hexdigest(), historical_sha="e61d5b0e827f7b412824ad46021e2ad6cc6f7875",
                counts=expected["counts"], witness=expected["witness"],
                historical_blobs=dict(overlap="b18f52109ccff9c7dc77542d3b8f3e5d5989102a",
                                      cut="c10ac57f988a439144e21898bd2b33ece0838a9b", gate="91cd1e507e955683e744fbdbb0745cac19d66cb3"))
    compare(cert, json.loads((folder / "receiver_turn_certificate.json").read_bytes()))
    a, b = [expected["witness"][key] for key in ("4", "5")]
    need(a["receiver_before"] == b["receiver_before"] == a["other_order"] == b["other_order"] and
         [dict(x["receiver_after"])[1] for x in (a, b)] == [4, 6] and
         all(sum(n for _, n in x["receiver_after"]) == 16 and x["third_chart_choices"] == [4, 5] for x in (a, b)),
         "receiver-only observation/control")
    def reject(obj, mutate):
        bad = deepcopy(obj)
        mutate(bad)
        try:
            compare(obj, bad)
        except ValueError:
            return
        raise AssertionError("bad evidence passed")
    checks = [
        (expected["witness"], lambda x: x.pop("4")),
        (expected["witness"], lambda x: x.update(duplicate=x["4"])),
        (a, lambda x: x.update(executed=4)),
        (a, lambda x: x["candidate_status"].update({"4": "legal"})),
        (b, lambda x: x["receiver_after"][1].__setitem__(1, 4)),
        (a, lambda x: x.update(other_order=x["receiver_after"])),
        (b, lambda x: x.update(third_chart_choices=[4])),
        (cert, lambda x: x.update(historical_sha="bad")),
        (cert, lambda x: x["counts"].update(histories=0)),
    ]
    for obj, fn in checks:
        reject(obj, fn)
    print(json.dumps(dict(status="PASS", rejecting_controls=len(checks), **expected["counts"]), sort_keys=True))


if __name__ == "__main__":
    main(Path(sys.argv[1]))
