"""Post-review-scope static role check on every support in the frozen grade-two orbit."""
from collections import Counter
from contextlib import redirect_stdout
from io import StringIO
import json
from pathlib import Path
import runpy
import sys

here = Path(__file__).resolve().parent
domain = here.parent.parent / "symmetric_matched_event/verify.py"
with redirect_stdout(StringIO()):
    g = runpy.run_path(str(domain))
points, work, supports = g["V"], g["prior"], Counter(g["images"])
near = {p: g["chosen"](p) for p in points}
offset = {p: {q: work(p, q) for q in points if q != p} for p in points}
candidate = {p: {b for b in points if p != b and all(work(p, k) == 4 for k in near[b])}
             for p in points}
rows = json.loads((here.parent.parent / "first_cut_return/raw.json").read_text())["starts"]
by_mask = {int(row["mask"], 16): row for row in rows}

def number(p):
    return p[0] + 11 * p[1]

counts = Counter()
for leaf, multiplicity in supports.items():
    core = {p for p in leaf if near[p] <= leaf}
    (sender,) = [p for p in core if near[p] <= core]
    options = candidate[sender]
    assert len(core) == 5 and len(options) == 4
    (recipient,) = [b for b in options if not (near[b] & leaf)]
    assert all(near[b] <= leaf for b in options - {recipient})
    cut_types = Counter()
    for holder in leaf:
        incident = [v + (4 if q in leaf else -4) for q, v in offset[holder].items()]
        cut_types[(incident.count(-4), incident.count(0))] += 1
        shifted = frozenset(((x-holder[0]) % 11, (y-holder[1]) % 11) for x, y in leaf)
        mask = sum(1 << number(p) for p in shifted)
        live = [a for a in by_mask[mask]["answers"] if a[-1] == "admitted"]
        if holder == sender:
            relative = ((recipient[0]-holder[0]) % 11, (recipient[1]-holder[1]) % 11)
            assert len(live) == 1 and live[0][0] == number(relative)
        else:
            assert live == []
        counts[holder == sender] += multiplicity
    assert cut_types == {(4, 12): 12, (3, 13): 4, (2, 10): 4, (0, 16): 4, (0, 4): 1}
assert counts == {True: 968, False: 23232}
print("PASS: prior work and chosen support identify the one transfer pair on all 484 masks; 968 indexed leaves.")
