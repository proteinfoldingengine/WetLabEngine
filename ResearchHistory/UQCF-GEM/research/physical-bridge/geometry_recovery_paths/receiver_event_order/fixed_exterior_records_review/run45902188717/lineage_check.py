"""Read the two pinned parent scripts; verify original named slots and original P1 output."""
from functools import lru_cache
from hashlib import sha1
from itertools import product
from pathlib import Path
from runpy import run_path
import argparse
import json

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("orbit_probe", type=Path)
parser.add_argument("p1_engine", type=Path)
parser.add_argument("study_replay", type=Path)
args = parser.parse_args()

def source(path, expected):
    data = path.read_bytes()
    actual = sha1(b"blob "+str(len(data)).encode()+b"\0"+data).hexdigest()
    if actual != expected:
        raise ValueError("Unexpected historical source: "+str(path))
    return run_path(str(path))

native = source(args.orbit_probe, "45eaeb0df71e6f6a5d9e205332f3bc015fcb4c8b")
p1 = source(args.p1_engine, "b18f52109ccff9c7dc77542d3b8f3e5d5989102a")["push"]
science = source(args.study_replay, "e31252cad791503ce6d5ca829d48cffa063522f6")
archive = native["orbit"]
row_order = list(product((False,True),(-1,1),(-1,1))).index((False,1,1))
start = row_order * 121
templates = archive[start:start+121]
assert templates == science["images"](11)
parents = (-1,)+(0,)*968
grades = (1,)+(2,)*968
ambient = tuple(range(969))

@lru_cache(None)
def record(row):
    ids = (0,)+tuple(j+1 for j in science["bits"](row))
    return ids, p1(parents, ambient, ids, grades)

checks = []
for side in (9,10):
    outside = native["full"] ^ science["region"](11,side)
    groups = science["classes"](templates,outside)
    ends = []
    for last in (False,True):
        columns = archive.copy()
        columns[start:start+121] = science["assign"](templates,groups,native["full"],last)
        rows = science["chart_rows"](columns,121)
        assert all(4*(r^s).bit_count() == native["work"][i][j]
                   for i,r in enumerate(rows) for j,s in enumerate(rows))
        ends.append([record(row) for row in rows])
    before, after = ends
    assert all(before[i] == after[i] for i in science["bits"](outside))
    pin_changes = sum(b[1][0] != a[1][0] for b,a in zip(before,after))
    assert pin_changes == {9:48,10:94}[side]
    checks.append(dict(side=side, identical_named_exterior_P1=outside.bit_count(),
                       interior_Pin_changes=pin_changes, all_ordered_work_entries=121**2))
print(json.dumps(dict(historical_variable_leaf_ids=[start+1,start+121],checks=checks),sort_keys=True))
