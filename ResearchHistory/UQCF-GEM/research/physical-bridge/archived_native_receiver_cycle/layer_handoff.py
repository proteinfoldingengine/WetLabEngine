"""Replay the historical layer repair and orient its two-label output by an atomic predecessor."""
from collections import Counter
import importlib.util
from itertools import product
import json
from pathlib import Path
import sys


def load_file(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main(demos):
    source = demos / "v16.54-parent-support-connectivity"
    sys.path.insert(0, str(source))
    from universe import case
    from mechanisms import produce
    from verifier import verify_record
    from model import state

    atom_dir = demos / "v16.26-consistency-increment-law"
    atom = load_file(atom_dir/"engine.py", "original_atom")
    check = load_file(atom_dir/"verify.py", "check_original_atom")

    def layer(rows, k, q, floors):
        c = case("M1","layers",k,floors,q,rows,{"peak":k})
        result = produce(c)
        assert verify_record(c,result) == []
        return result

    domain = Counter()
    for k in (4,5,6):
        for mask in range(1,1 << k):
            tail = [j for j in range(k) if mask & (1 << j)]
            rows = [[j] for j in range(k)] + [tail]
            for floor in range(1,len(tail)+1):
                result = layer(rows,k,3,[1]*k+[floor])
                domain[k] += 1
                if k == 4 and len(tail) == 4 and floor == 1:
                    example = result

    def receipt(parents, masks, x, site):
        views = [[u for u in range(len(parents)) if z & (1 << u)] for z in masks]
        rec = atom.atomic(parents,views,x,site)
        check.verify_atomic(rec)
        assert rec["trigger"] and (rec["tau_before"],rec["tau_after"]) == (1,2)
        return rec

    def read_rows(views, sites):
        return state([{j for j,col in enumerate(views) if u in col} for u in sites])

    def oriented(rec, sites):
        # New composition: run the unchanged layer routine at the old local rank
        # and orient its output using only the actual pre-deletion supports.
        before = read_rows(rec["before"],sites)
        peak = read_rows(rec["after"],sites)
        result = layer(peak,2,rec["tau_before"],[1]*len(sites))
        path = list(map(state,result["path"]))
        assert (path[0] == before) != (path[-1] == before)
        return path if path[0] == before else path[::-1]

    counts = Counter()
    for n in range(2,7):
        sites = list(range(1,n+1))
        for pattern in product((1,2,3),repeat=n):
            if 1 not in pattern or 2 not in pattern:
                continue
            for x in (0,1):
                y = 1-x
                if pattern.count(1 << y) != 1:
                    continue
                src = pattern.index(1 << y)
                masks = [1 + sum(1 << site for site,z in zip(sites,pattern) if z & (1 << j)) for j in (0,1)]
                masks[x] |= 1 << sites[src]
                rec = receipt([-1]+[0]*n,masks,x,sites[src])
                path = oriented(rec,sites)
                edits = [(i,j,j in b[i]) for a,b in zip(path,path[1:])
                         for i in range(n) for j in a[i]^b[i]]
                gains = [(i,y,True) for i,z in enumerate(pattern) if z == 1 << x]
                assert sorted(edits[:-1]) == gains and edits[-1] == (src,x,False)
                counts[n] += 1

    parents = [-1,0,1,1,0,4,4,0,7,7]
    sites = [1,4,7]
    forward = receipt(parents,[499,655],0,1)
    reverse = receipt(parents,[497,671],1,4)
    assert forward["after"] == reverse["after"]
    assert oriented(forward,sites) == oriented(reverse,sites)[::-1]
    peak = read_rows(forward["after"],sites)
    selected = layer(peak,2,1,[1]*3)
    quiet = layer(peak,2,2,[1]*3)
    assert list(map(state,quiet["path"])) == [peak]
    assert oriented(forward,sites) == [read_rows([[u for u in range(10) if z >> u & 1] for z in masks],sites)
                                        for masks in ([499,655],[499,671],[497,671])]
    return dict(domain=domain,controlled_stars=counts,witness=selected,
                relaxed_bound=quiet,original_example=example)


if __name__ == "__main__":
    print(json.dumps(main(Path(sys.argv[1]).resolve()),sort_keys=True,indent=2))
