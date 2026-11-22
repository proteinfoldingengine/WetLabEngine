"""Replay all six orderings and both first-bit alternatives on the fixed three-view star."""
from fractions import Fraction
from hashlib import sha256
from itertools import groupby, permutations
import json
from pathlib import Path
import sys

import check_donor_read as inherited


U = Path("ResearchHistory/UQCF-GEM")
D = U / "demos"
STAR = inherited.STAR
ATOM = inherited.ATOM
GRADES = [(1, 1, 1), (Fraction(1, 3), 2, Fraction(3, 2)), (5, Fraction(2, 3), 1)]
# Original (editor, next projected change), control next projected change.
EXPECTED = {
    (1,7,13): (7, "A", (9,7), (5,7)),
    (7,1,13): (101, "A", (9,7), (5,7)),
    (7,13,1): (131, "A", (1,3), (1,3)),
    (1,13,7): (16, "R", (1,3), (3,7)),
    (13,1,7): (232, "R", (1,3), (3,7)),
    (13,7,1): (247, "R", (1,3), (1,5)),
}


def distinct(values):
    return [value for value, _ in groupby(values)]


def retained_vector(lin, mask, grades):
    keys = ((), (1,), (2,), (3,))
    ambient = lin.Carrier("star-work-replay", keys)
    live = tuple(key for v,key in enumerate(keys) if mask & (1 << v))
    reduced = lin.Carrier(ambient.genesis, live)
    values = dict(zip(live, lin.Pruning(ambient, reduced).aggregate((1, *grades)), strict=True))
    return tuple(values.get(key, 0) for key in keys[1:])


def pair_values(local, grades, lin, work):
    result = []
    for b, r in local:
        coordinates = [retained_vector(lin, mask, grades) for mask in (b, r)]
        actual = work.construct_response_geometry((0,1), coordinates, coordinates).work[0][1]
        direct = sum(g*g for v,g in enumerate(grades, 1) if (b^r) & (1 << v))
        assert actual == direct
        result.append(actual)
    return result


def verify_path(path, row, graph, lookup, checker):
    full = distinct(map(tuple, path))
    ids = [lookup[s] for s in full]
    endpoint = lookup[checker.canonical(3, 3, row["q"])]
    assert checker.path_valid(ids, row["state"], endpoint, graph, 2, 0)
    inherited.check_edges(full, graph, lookup, 4)


def main(destination):
    inherited.blob(Path(__file__).with_name("check_donor_read.py"), "130151a17ee347734e8251a47cb0f439b0dbdd82")
    for filename, digest in (("graph_producer.py","6c8eca570cda82b64c0d06775672f33977be430a"),
                             ("graph_verifier.py","ff8af4ecf743507d0d601daffa9b054441b85fd1")):
        inherited.blob(STAR / filename, digest)
    sys.path.insert(0,str(STAR.resolve()))
    star = inherited.module("old_star",STAR/"producer.py","ffd513619d182abea2b31bd90c38e12784557bf3")
    checker = inherited.module("old_check",STAR/"verifier.py","80a47f10231a086af161c4999c582fa038d064c7")
    atom = inherited.module("old_atom",ATOM/"engine.py","c10ac57f988a439144e21898bd2b33ece0838a9b")
    verifier = inherited.module("old_verify",ATOM/"verify.py","91cd1e507e955683e744fbdbb0745cac19d66cb3")
    lin = inherited.module("old_lineage",U/"foundational-closure-verification/lineage.py","e95e3e978779164dd91f09b80e3389247e6320c2")
    work = inherited.module("old_work",D/"v15.40-global-balance-geometry-specificity/response_geometry.py","9128c24b695c1b539ac60dc93aeaf0bd4795c57b")
    entries = inherited.archive(STAR,"b226fdef7d908f1f0186060ebf408eb0db823418")
    entry, = [e for e in entries if (e["m"],e["k"]) == (3,3)]
    graph = entry["graph"]
    states = graph["states"]
    lookup = {tuple(s):i for i,s in enumerate(states)}
    rows = {row["state"]:row for row in entry["normalizations"]}
    cases = {}
    positive = []
    for seed in permutations((1,7,13)):
        b,r,a = (seed.index(v) for v in (1,7,13))
        row = rows[lookup[seed]]
        row_id, editor_name, normal_next, control_next = EXPECTED[seed]
        assert row["state"] == row_id and row["q"] == 2
        original = star.normalize(seed,3,3,2)
        assert original == [states[i] for i in row["path"]]
        actor, = [i for i in range(3) if original[0][i] != original[1][i]]
        assert actor == {"A":a,"R":r}[editor_name]
        event = inherited.certify(atom,verifier,(-1,0,0,0),original[0],original[1],actor,2)
        restored = inherited.omit_clear(star.normalize,(seed,3,3,2),1,actor,2,"s")
        local_pairs = []
        arms = {}
        for name, path, expected_next in (("original",original,normal_next),("restored",restored,control_next)):
            verify_path(path,row,graph,lookup,checker)
            local = distinct((s[b],s[r]) for s in path)
            local_pairs.append(local)
            assert local[:2] == [(1,7),expected_next]
            exact = []
            for grades in GRADES:
                values = pair_values(local, grades, lin, work)
                first = distinct(values)[1] - values[0]
                expected_rise = name == "original" and row_id in (7,101)
                assert (first > 0) == expected_rise and first != 0
                exact.append([str(x) for x in values])
            if expected_rise:
                positive.append(row_id)
            arms[name] = {"path":path, "BR_changes":local,"work_by_grade":exact}
        # Check the end of the donor's uninterrupted additions for every active order,
        # comparing B to the OTHER occupied view even if the editor role is R here.
        copy_gap = []
        if b != 2:
            assert actor == 2
            other = 3 - actor - b
            for g in GRADES:
                def at_copy_end(path):
                    j = 2
                    while j < len(path) and path[j][b] != path[j-1][b] and path[j][b] > path[j-1][b]:
                        j += 1
                    assert j > 2 and path[j][actor] < path[j-1][actor]
                    return pair_values([(path[j-1][b], path[j-1][other])],g,lin,work)[0]
                gap = at_copy_end(original)-at_copy_end(restored)
                assert gap == g[1]**2
                copy_gap.append(str(gap))
        if row_id == 131:
            assert local_pairs[0] == local_pairs[1] and all(x == 1 for x,y in local_pairs[0])
        if row_id == 232:
            blind = [distinct((s[b],s[a]) for s in path) for path in (original,restored)]
            assert blind[0] == blind[1] == [(1,13),(3,13),(7,13),(7,9),(7,11),(5,11)]
            assert original[2][b] == 3 and original[3][b] == 3 and restored[3][b] == 7
            assert original[3][r] == 1 and restored[3][r] == 7
            arms["blind_projection_B_and_noneditor"] = blind
        cases[str(row_id)] = {"order_masks":seed,"actual_first_editor":editor_name,"event":event,
                              "active_copy_work_gap":copy_gap,**arms}
    assert set(EXPECTED) == set(permutations((1,7,13))) and sorted(positive) == [7,101]
    assert len(cases) == 6 and len({row[0] for row in EXPECTED.values()}) == 6
    # Reject false signals and traces that satisfy a weaker scalar comparison.
    missing_midpoint = cases["7"]["original"]["path"][:1] + cases["7"]["original"]["path"][2:]
    bad_ids = [lookup[tuple(s)] for s in missing_midpoint]
    assert not checker.path_valid(bad_ids, 7, lookup[checker.canonical(3,3,2)], graph, 2, 0)
    active_mask_pair = cases["232"]["blind_projection_B_and_noneditor"]
    wrong_word = active_mask_pair[1].copy()
    wrong_word[2] = (5,13)
    assert wrong_word != active_mask_pair[0]
    assert cases["131"]["actual_first_editor"] == "A" and 131 not in positive
    assert "232" in cases and cases["232"]["actual_first_editor"] == "R"
    certificate = {"grades":[list(map(str,g)) for g in GRADES],"cases":cases}
    raw = (json.dumps(certificate,sort_keys=True,indent=2)+"\n").encode()
    destination.mkdir(parents=True,exist_ok=True)
    (destination/"remote_pair_work_certificate.json").write_bytes(raw)
    return {"cases":sorted(map(int,cases)), "positive_original_rows":sorted(positive),
            "active_blind_row":232, "silent_blind_row":131, "paths_validated":12,
            "certificate_sha256":sha256(raw).hexdigest()}


if __name__ == "__main__":
    print(json.dumps(main(Path(sys.argv[1])),sort_keys=True,indent=2))
