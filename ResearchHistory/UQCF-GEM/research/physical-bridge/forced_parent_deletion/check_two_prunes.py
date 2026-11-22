"""Exact search of ordered two-prune histories for both historical responses."""
from pathlib import Path
import itertools
import json
from fractions import Fraction
import hashlib

import numpy as np
import check_bracket_ports as archive


def merge(values, branch, removed, parent):
    values[branch, parent] += values[branch, removed]
    values[branch, removed] = 0


def cross(left, right):
    return np.roll(left, 1, axis=-1)*right - left*np.roll(right, -1, axis=-1)


def main():
    root = Path(__file__).resolve().parents[5]
    original = archive.original_functions(root/archive.HISTORICAL_PATH)
    base = original["build_base"]()
    x = np.array(base["branches"][1:], dtype=np.int64)
    assert np.array_equal(x, base["branches"][1:])
    g = {k: Fraction((i+1)%11+2,(2*i+1)%7+3) for i,k in enumerate(base["gates"])}
    assert {k:float(v) for k,v in g.items()} == base["gates"]
    assert (g["g23"],g["g34"],g["g234"],g["g1234r"]) == (Fraction(2,3),Fraction(8,7),1,3)

    def pinned(v, arm):
        a,b,c = (np.array([int(y) for y in q], dtype=object) for q in v)
        op = original["recombine"]
        if arm == "B3":
            return list(op(op(a,b,g["g23"]),c,g["g234"]))
        return list(op(a,op(b,c,g["g34"]),g["g234"]))

    def scaled(v, arm):
        a,b,c = [v[...,i,:] for i in range(3)]
        # Each input coordinate after at most two edits is bounded by 42.
        # Even the products of the inner numerator and the remaining grade
        # are below one million in magnitude, far below int64 capacity.
        if arm == "B3":
            inner = 3*(a+b)+2*cross(a,b)
            return 7*(inner+3*c+cross(inner,c))
        inner = 7*(b+c)+8*cross(b,c)
        return 3*(7*a+inner+cross(a,inner))

    edits = list(itertools.product(range(3),range(12),range(12)))
    edits = [e for e in edits if e[1]!=e[2]]
    targets = {arm:scaled(x,arm) for arm in ("B3","B4")}
    assert all(list(targets[k])==[21*y for y in pinned(x,k)] for k in targets)
    result = {}
    for arm, other in (("B3","B4"),("B4","B3")):
        counts = {"same_operand":0,"different_operands":0,"pinned_checks":0}
        hits, scalar = [], []
        best_distance = 13
        closest = []
        digest = hashlib.sha256()
        for first in edits:
            y = x.copy()
            merge(y,*first)
            second = [e for e in edits if first[0]!=e[0] or first[1] not in e[1:]]
            batch = np.repeat(y[None,:,:],len(second),axis=0)
            for row,e in zip(batch,second):
                merge(row,*e)
            assert np.max(np.abs(batch))<=42
            assert np.all(batch.sum(axis=-1)==x.sum(axis=-1))
            outcomes = scaled(batch,arm)
            digest.update(outcomes.astype("<i8").tobytes())
            distances = np.count_nonzero(outcomes!=targets[other],axis=-1)
            for index, (row, e, distance) in enumerate(zip(batch,second,distances)):
                counts["same_operand" if e[0]==first[0] else "different_operands"] += 1
                if distance < best_distance:
                    best_distance = int(distance)
                    closest = []
                if distance == best_distance:
                    closest.append([first,e])
                full = distance == 0
                local = bool(outcomes[index,3] == targets[other][3])
                if index%97==0 or local or full:
                    assert list(outcomes[index])==[21*z for z in pinned(row,arm)]
                    counts["pinned_checks"] += 1
                if full:
                    hits.append([first,e])
                if local:
                    scalar.append({"edits":[first,e],"right_operand_scaled_by_21":outcomes[index].tolist()})
        assert counts["same_operand"]==3*132*110
        assert counts["different_operands"]==3*132*264
        result[arm]={"counts":counts,"full_hits":hits,"scalar_hits":scalar,
                     "minimum_different_coordinates":best_distance,"nearest_histories":closest,
                     "ordered_scaled_outputs_sha256":digest.hexdigest()}
    print(json.dumps(result,indent=2,sort_keys=True))


if __name__=="__main__":
    main()
