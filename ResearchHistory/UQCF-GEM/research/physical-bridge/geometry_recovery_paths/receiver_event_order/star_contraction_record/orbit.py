"""Orbit incidence tests for the historical star contraction; no optimum is supplied."""
from collections import Counter
from functools import reduce
import json
from operator import or_
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "orbit_exchange"))
from probe import charts, orbit, rows, work

def separation():
    overlap = [(rows[0] & rows[b]).bit_count() for b in charts[1:]]
    spectra = Counter()
    candidates = []
    twins = {}
    for i, support in enumerate(orbit):
        twins.setdefault(support, []).append(i)
    assert all(len(ix) == 2 for ix in twins.values())
    for b in charts[1:]:
        counts = {d: (rows[0] & rows[d] & ~rows[b]).bit_count()
                  for d in charts[1:] if d != b}
        spectra.update(counts.values())
        excluded = sorted(d for d, count in counts.items() if count == 0)
        covered = reduce(or_, (rows[v] for v in [0, b, *excluded]))
        shared = {i for i,m in enumerate(orbit) if m & 1 and m & (1<<b)}
        choices = [(early,late) for early,late in twins.values()
                   if early in shared and any(early<u<late for u in shared)]
        assert len(choices) >= 8
        early,late = min(choices)
        middle = min(u for u in shared if early < u < late)
        candidates.append(dict(b=b, excluded=excluded, missing=len(orbit)-covered.bit_count(),
                               interleaved_twins=len(choices), example_one_based=[early+1,middle+1,late+1]))
    assert len(orbit) == 968 and {s.bit_count() for s in orbit} == {25}
    assert {r.bit_count() for r in rows} == {200}
    assert max(map(max,work)) == 1472 and min(overlap) == 16
    assert spectra[0] == 56 and sum(spectra.values()) == 14280
    assert min(x["missing"] for x in candidates) == 160
    return dict(min_pair_overlap=min(overlap), triples=sorted(spectra.items()),
                candidates=candidates, edits_to_contraction=sum(r.bit_count() for r in rows)-1-len(orbit))

if __name__ == "__main__":
    print(json.dumps(separation(), sort_keys=True))
