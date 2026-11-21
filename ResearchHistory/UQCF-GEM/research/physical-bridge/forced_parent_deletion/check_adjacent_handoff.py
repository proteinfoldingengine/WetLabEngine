"""Exploratory census of adjacent donor loss and receiver gain at the same root leaf."""
import argparse
import gzip
import hashlib
import json
import sys
from collections import Counter
from pathlib import Path

import sympy as sp


ARCHIVE = "evidence/science/scientific/CERTIFICATE.json.gz"
PINS = {
    ARCHIVE: "ff8244239fb5ce092b07cbe775382593018b256d",
    "producer.py": "7c4f65714d6b9ccda7f4bb0fc378b0daef957fff",
    "graph_producer.py": "6c8eca570cda82b64c0d06775672f33977be430a",
    "star_normalize.py": "d58cc9d1168d219b2869affd2d4ede889ebe579b",
}


def edits(path):
    for before, after in zip(path, path[1:]):
        (actor,) = [i for i, (x, y) in enumerate(zip(before, after)) if x != y]
        bit = before[actor] ^ after[actor]
        assert bit.bit_count() == 1
        yield actor, bit.bit_length() - 1, bool(after[actor] & bit)


def root_handoffs(path, parents):
    tape = list(edits(path))
    for t, ((donor, site, add), (receiver, w, gained)) in enumerate(zip(tape, tape[1:])):
        if (not add and gained and donor != receiver and site == w
                and parents[site] == 0 and site not in parents[1:]):
            yield t, donor, receiver, site


def parent_p1_rows(parents, mask):
    rows = {v: [0] * len(parents) for v in range(len(parents)) if mask >> v & 1}
    for site in range(len(parents)):
        ancestor = site
        while ancestor not in rows:
            ancestor = parents[ancestor]
        rows[ancestor][site] = 1
    return rows


def exact_constraints(parents, path, site, donor, receiver):
    # O2/O3 allow a separate compatible ambient grade for each complete cover.
    # W1 fixes each unchanged chart across its step. No single ambient source
    # is imposed across different states and no constraint uses edited grades.
    n = len(parents)
    width = n * len(path)
    def form(t, row):
        a = [0] * width
        a[n*t:n*(t+1)] = row
        return sp.Matrix(a)
    def chart(t, j, v):
        return form(t, parent_p1_rows(parents, path[t][j])[v])
    def basis(t, v):
        return form(t, [int(i == v) for i in range(n)])
    constraints = []
    for t, (before, after) in enumerate(zip(path, path[1:])):
        for x, y in zip(before, after):
            if x == y:
                for row in parent_p1_rows(parents, x).values():
                    constraints.append((form(t, row) - form(t+1, row)).T)
    matrix = sp.Matrix.vstack(*constraints)
    kernel = matrix.nullspace()
    def forced(v):
        return all(v.dot(direction) == 0 for direction in kernel)
    t = 3
    g = basis(0, site)
    anchor = 1
    predictions = {
        'anchor_leaf_from_initial_source': chart(t, anchor, site) - g,
        'donor_root_increment': chart(t+1, donor, 0) - chart(t, donor, 0) - g,
        'receiver_root_increment': chart(t+2, receiver, 0) - chart(t+1, receiver, 0) + g,
        'receiver_source_leaf': chart(t+2, receiver, site) - g,
        'receiver_source_after_relay_exit': chart(t+3, receiver, site) - g,
        'receiver_root_before_gain': chart(t+1, receiver, 0) - basis(0,0) - basis(0,9) - basis(0,10),
        'receiver_root_after_gain': chart(t+2, receiver, 0) - basis(0,0) - basis(0,10),
    }
    assert all(forced(v) for v in predictions.values())
    # A zero receiver root increment does not hold for every admissible history.
    assert not forced(chart(t+2, receiver, 0) - chart(t+1, receiver, 0))
    # Arbitrary W1/W2 histories may change unrelated exclusive coordinates.
    same_source_drift = sp.Matrix.vstack(matrix, sp.eye(n).row_join(sp.zeros(n,width-n))).nullspace()
    def drift_possible(t, j, v):
        return any(chart(t,j,v).dot(w) != 0 for w in same_source_drift)
    free_before = [v for v in parent_p1_rows(parents, path[t+1][receiver]) if drift_possible(t+1, receiver, v)]
    positive = [2] * n
    shifted = positive.copy()
    shifted[0] -= 1
    shifted[site] += 1
    def grade(t, j, source):
        return {v: sum(a*b for a,b in zip(row,source))
                for v,row in parent_p1_rows(parents,path[t][j]).items()}
    assert grade(0,receiver,positive) == grade(0,receiver,shifted)
    lens = [[grade(i,receiver,src)[0] for src in (positive,shifted)] for i in (t+1,t+2)]
    assert lens == [[6,6],[4,3]]
    return {"ambient_unknowns":width,"constraint_rows":matrix.rows,"rank":width-len(kernel),
            "forced_identities":list(predictions),"positive_pair_receiver_roots":lens,
            "pre_gain_unconstrained_receiver_coordinates":free_before}


def provenance_trace(machine, star, record):
    changes = []
    def profiler(frame, event, arg):
        if (event != 'return' or frame.f_code.co_name != 'change'
                or frame.f_globals is not star.__dict__):
            return
        caller = frame.f_back
        norm = caller if caller.f_code is star.normalize.__code__ else caller.f_back
        if norm.f_code is star.normalize.__code__ and norm.f_locals['state'] == [1,1,5,3]:
            change = frame.f_locals
            changes.append([caller.f_code.co_name, caller.f_lineno, change['j'], change['v'], change['add']])
    spec = record['spec']
    old = sys.getprofile()
    try:
        sys.setprofile(profiler)
        replay = machine.normalize(record['start'],spec['degrees'],spec['k'],spec['q'])
    finally:
        sys.setprofile(old)
    assert replay == record['path']
    assert changes[3:6] == [['normalize',20,3,1,False],['recolor',24,2,1,True],['recolor',24,1,1,False]]
    return changes[:6]


def main():
    default = Path(__file__).resolve().parents[3] / 'demos/v16.48-recursive-chain-repair'
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--demo-dir', type=Path, default=default)
    root = parser.parse_args().demo_dir.resolve()
    for name, sha in PINS.items():
        b = (root / name).read_bytes()
        assert hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest() == sha, name
    sys.path.insert(0,str(root))
    import producer as machine
    import star_normalize as star
    archive = json.loads(gzip.decompress((root / ARCHIVE).read_bytes()))
    corpus = archive['corpus']
    assert machine.produce(domain=())['corpus'] == corpus
    results = []
    counts = Counter()
    for index, rec in enumerate(corpus):
        p = machine.graph.parents(machine.tree(rec['spec']['degrees']))
        path = rec['path']
        counts['corpus_paths'] += 1
        counts['corpus_edits'] += len(path)-1
        for t,donor,receiver,site in root_handoffs(path,p):
            assert (t,donor,receiver,site) == (3,3,2,9)
            assert [v for v in range(len(p)) if p[v]==0] == [1,9,10]
            assert all(not mask>>9 & 1 for mask in (path[0][receiver],path[t+1][receiver],path[-1][receiver]))
            assert [j for j,x in enumerate(path[t]) if j!=donor and x==path[t+1][donor]] == []
            overlap = [v for v in range(len(p)) if path[t+1][1] & path[t+2][receiver] & 1<<v]
            assert {0,1,9}.issubset(overlap) and 10 not in overlap
            results.append({"index":index,"spec":rec['spec'],"steps":[t,t+1],
                "states":path[:7],"final_receiver_mask":path[-1][receiver],
                "caller_trace":provenance_trace(machine,star,rec),
                "w1_w2":exact_constraints(p,path[:7],site,donor,receiver)})
    graph_hits = []
    for entry in archive['entries']:
        graph = entry['graph']
        for rec in entry['normalizations']:
            path = [graph['states'][i] for i in rec['path']]
            counts['graph_paths'] += 1
            counts['graph_edits'] += len(path)-1
            graph_hits.extend(root_handoffs(path,graph['parents']))
    assert not graph_hits
    assert [r['index'] for r in results] == [178,184,190]
    assert counts['corpus_paths'] == 210 and counts['graph_paths'] == 106
    # Exact same receiver and donor support edit alone is not a route assignment.
    # v16.26 factor's permissible endpoint equals this post-deletion state.
    atom_path = root.parent / 'v16.26-consistency-increment-law/engine.py'
    import importlib.util
    raw = atom_path.read_bytes()
    assert hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()=='c10ac57f988a439144e21898bd2b33ece0838a9b'
    spec = importlib.util.spec_from_file_location('historical_atom',atom_path)
    atom = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(atom)
    for hit in results:
        p = machine.graph.parents(machine.tree(hit['spec']['degrees']))
        def family(row):
            return [tuple(v for v in range(len(p)) if m>>v&1) for m in row]
        old, new = map(family,hit['states'][3:5])
        assert atom.factor(p,old,new)['steps'] == [atom.atomic(p,old,3,9)]
    print(json.dumps({"archive_blob":PINS[ARCHIVE],"search":"All root leaves; adjacent loss then gain by another chart. Exploratory extension beyond the registered source definition.","counts":dict(counts),
        "directed_hits":results,"graph_hits":graph_hits,
        "same_atom_terminal_factor":True,"physical_binding_and_access":"OPEN"},sort_keys=True,indent=2))


if __name__ == '__main__':
    main()
