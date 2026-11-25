"""Independent finite incidence checker; imports neither emitter nor replay."""
import itertools
import json
from pathlib import Path
import sys

D = Path(__file__).resolve().parent
F = json.loads((D / "FIXTURE.json").read_text())
C = F["charts"]
P = [-1] + [0] * len(F["tip_holders"])
MOVES = [(C.index(i), v) for i, v in F["edits"]]
B = C.index("B")
H = [sum(1 << i for i, label in enumerate(C) if label in holds)
     for holds in [C, *F["tip_holders"]]]

def columns(mask):
    h = H.copy()
    for j, (i, v) in enumerate(MOVES):
        if mask & (1 << j):
            h[v] &= ~(1 << i)
    assert all(h)
    return h

def covers(cols):
    matches = [query for query in range(1, 1 << len(C))
               if all(query & m for m in cols[1:])]
    s = min(q.bit_count() for q in matches)
    return s, tuple(q for q in matches if q.bit_count() == s)

def chart_rows(cols):
    return [[v for v, m in enumerate(cols) if m & (1 << i)] for i in range(len(C))]

def work(cols):
    return [[sum(g*g for m,g in zip(cols[1:], F["fine_grade"][1:])
                 if bool(m & (1 << i)) != bool(m & (1 << j)))
             for j in range(len(C))] for i in range(len(C))]

def receiver(cols):
    row = chart_rows(cols)[B]
    grades = F["fine_grade"]
    outside = sum(g for v,g in enumerate(grades) if v not in row)
    return (row, [outside + grades[0], *(grades[v] for v in row[1:])],
            [cols[v] for v in row],
            [v for v in row[1:] if cols[v].bit_count() > 1], work(cols)[B])

def check(raw):
    receipts = {}
    for entry in raw["rows"]:
        m,k = entry["mask"],entry["edit"]
        assert 0 <= m < 32 and 0 <= k < 5 and not m & (1 << k) and (m,k) not in receipts
        i,v = MOVES[k]
        before,after = columns(m),columns(m | (1 << k))
        assert before[v] & (1 << i) and before[v].bit_count() > 1
        hb, old = covers(before)
        ha, new = covers(after)
        assert hb == 3 + int(m & 20 == 20)
        assert ha == 3 + int((m | (1 << k)) & 20 == 20)
        r = ha-hb, not bool(set(old) & set(new))
        assert entry["result"] == list(r)
        cert = entry["certificate"]
        assert cert["before"] == chart_rows(before) and cert["after"] == chart_rows(after)
        assert cert["parents"] == P and (cert["index"], cert["leaf"], cert["parent"]) == (i,v,0)
        assert cert["tau_before"] == cert["h_before"] == hb
        assert cert["tau_after"] == cert["h_after"] == ha
        assert (cert["delta_h"],cert["trigger"]) == r
        receipts[m,k] = r
    assert len(receipts) == 80
    arms = (3, 12)
    assert tuple(receipts[m,4] for m in arms) == ((0, False), (1, True))
    for a,b in ((1,4),(3,12),(19,28)):
        assert receiver(columns(a)) == receiver(columns(b))
    for a,b in ((3,12),(19,28)):
        assert work(columns(a)) == work(columns(b))
    first = sum(1 << C.index(i) for i in "BEX")
    # Proof-specific rejecting control: supplying just this same minimum
    # would mispredict the first arm because additional minimum AFX survives.
    assert all(covers(columns(m))[1][0] == first for m in arms)
    counts = [0,0]
    for order in itertools.permutations(range(5)):
        m=0
        for k in order:
            if k==4:
                counts[receipts[m,k][0]] += 1
            m |= 1 << k
    assert counts == raw["probe_counts"] == [60, 60]

if __name__ == "__main__":
    raw = json.loads(Path(sys.argv[1]).read_text())
    check(raw)
    raw["rows"][0]["certificate"]["trigger"] = not raw["rows"][0]["certificate"]["trigger"]
    try:
        check(raw)
    except AssertionError:
        pass
    else:
        raise AssertionError("checker accepted deliberately false trigger")
    print("Verified 32 states, 80 edges, 120 orders, matched restrictions and work; tamper rejected.")
