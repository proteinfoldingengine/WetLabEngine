"""Trace a donor read through original star and fork controllers."""
import gzip
import hashlib
import importlib.util
import inspect
import json
import sys
from itertools import permutations
from pathlib import Path
from types import CodeType

U = Path("ResearchHistory/UQCF-GEM")
STAR = U / "demos/v16.43-star-fiber-classification"
FORK = U / "demos/v16.45-binary-fork-unit-barrier"
ATOM = U / "demos/v16.26-consistency-increment-law"
ARCHIVE = "evidence/science/scientific/CERTIFICATE.json.gz"


def blob(path, expected):
    raw = path.read_bytes()
    assert hashlib.sha1(f"blob {len(raw)}\0".encode() + raw).hexdigest() == expected
    return raw


def module(name, path, identity):
    blob(path, identity)
    spec = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(spec)
    sys.modules[name] = m
    spec.loader.exec_module(m)
    return m


def archive(folder, identity):
    return json.loads(gzip.decompress(blob(folder / ARCHIVE, identity)))["entries"]


def omit_clear(fn, args, slot, index, vertex, buffer):
    """Restore one source bit just before its snapshot. All subsequent code runs normally."""
    change, = [code for code in fn.__code__.co_consts if isinstance(code, CodeType) and code.co_name == "change"]
    lines, first = inspect.getsourcelines(change)
    snapshot, = [first+i for i,line in enumerate(lines)
                 if line.strip() in ("path.append(list(s))", "path.append(list(current))")]
    interventions = []
    def trace(frame, event, arg):
        if (event == "line" and frame.f_lineno == snapshot and
            frame.f_code is change):
            live = frame.f_locals
            if (len(live["path"]), live["j"], live["v"], live["add"]) == (slot,index,vertex,False):
                masks = live[buffer]
                assert not (masks[index] >> vertex & 1)
                masks[index] |= 1 << vertex
                interventions.append((slot,index,vertex))
        return trace
    old = sys.gettrace()
    try:
        sys.settrace(trace)
        result = fn(*args)
    finally:
        sys.settrace(old)
    assert interventions == [(slot,index,vertex)]
    return result


def check_edges(path, graph, lookup, n):
    for before, after in zip(path, path[1:]):
        assert tuple(before) in lookup and tuple(after) in lookup
        if before == after:
            continue
        (i, difference), = [(j,a^b) for j,(a,b) in enumerate(zip(before,after)) if a != b]
        assert difference.bit_count() == 1
        smaller = before if before[i] < after[i] else after
        bit = (n-1)*i + difference.bit_length()-2
        assert graph["forward_moves"][lookup[tuple(smaller)]] >> bit & 1


def certify(atom, verifier, parents, before, after, source, vertex):
    views = [[v for v in range(len(parents)) if mask >> v & 1] for mask in before]
    cert = atom.atomic(parents,views,source,vertex)
    verifier.verify_atomic(cert)
    assert [sum(1 << v for v in y) for y in cert["after"]] == after
    return cert


def star_pair(star, validate, atom, verifier):
    entries = archive(STAR, "b226fdef7d908f1f0186060ebf408eb0db823418")
    entry = next(e for e in entries if (e["m"],e["k"]) == (3,3))
    graph = entry["graph"]
    states = graph["states"]
    index = {tuple(s):i for i,s in enumerate(states)}
    rows = {r["state"]:r for r in entry["normalizations"]}
    assert set(rows) == set(range(len(states)))
    result = {}
    for reference, marked, survivor, expected_id in ((11,1,2,184), (13,2,1,232)):
        initial = (reference,1,7)
        row = rows[index[initial]]
        assert row["state"] == expected_id and row["q"] == 2
        path = star.normalize(initial,3,3,2)
        assert path == [states[i] for i in row["path"]]
        assert validate.path_valid(row["path"],row["state"],index[(11,5,1)],graph,2,0)
        source_certificate = certify(atom,verifier,(-1,0,0,0),path[0],path[1],2,marked)
        assert path[2][1] == 1 | (1 << survivor) and path[2][0] == reference and path[2][2] == path[1][2]
        control = omit_clear(star.normalize,(initial,3,3,2),1,2,marked,"s")
        check_edges(control,graph,index,4)
        assert control[:2] == [list(initial),list(initial)] and control[2][1] == 3 and control[3][1] == 7
        result[str(expected_id)] = {"source_certificate":source_certificate,"recorded_state_ids":row["path"],
                                    "recorded_path":path,"restored_bit_control":control}
    # A same-seed intervention whose compressed control also passes the full historical path test.
    reference_row = rows[7]
    start = (1,7,13)
    assert states[7] == list(start) and reference_row["q"] == 2
    original = star.normalize(start,3,3,2)
    assert original == [states[i] for i in reference_row["path"]]
    cert = certify(atom,verifier,(-1,0,0,0),original[0],original[1],2,2)
    restored = omit_clear(star.normalize,(start,3,3,2),1,2,2,"s")
    assert restored[0] == restored[1] == list(start) and (original[2][0],restored[2][0]) == (9,5)
    for path in (original,restored):
        check_edges(path,graph,index,4)
        compressed = [index[tuple(s)] for j,s in enumerate(path) if not j or s != path[j-1]]
        assert validate.path_valid(compressed,7,index[(11,5,1)],graph,2,0)
    same_endpoint = {"source_certificate":cert, "recorded_path":original, "restored_bit_control":restored}
    rankings = []
    for order in permutations(range(3)):
        receiver = order.index(1)
        first_masks = []
        for reference in (11,13):
            state = (reference,1,7)
            i = index[tuple(state[j] for j in order)]
            masks = [states[j][receiver] for j in rows[i]["path"]]
            first_masks.append(next((v for v in masks if v != 1), None))
        rankings.append({"order":order, "first_receiver_masks":first_masks})
    assert [r["first_receiver_masks"] for r in rankings] == [[5,3],[None,None],[5,3],[9,9],[None,None],[9,9]]
    return {"rows":result, "same_seed_row_7":same_endpoint, "rank_controls":rankings}


def fork_boundaries(fork, atom, verifier):
    entries = archive(FORK, "3ed66277766b9836804ed9ec222d9728009b2b67")
    totals = dict(paths=0, left_deletions=0, nonempty_prefixes=0, left_removals=0, right_additions=0)
    highlighted = None
    for entry in entries:
        b,c,k = entry["b"],entry["c"],entry["k"]
        right = c+2
        graph = entry["graph"]
        states = graph["states"]
        index = {tuple(s):i for i,s in enumerate(states)}
        parents = graph["parents"]
        for row in entry["normalizations"]:
            totals["paths"] += 1
            args = (states[row["state"]],b,c,k,row["q"])
            path = fork.normalize(*args)
            assert path == [states[i] for i in row["path"]]
            for pos,(before,after) in enumerate(zip(path,path[1:]),1):
                (donor, bit), = [(j,x^y) for j,(x,y) in enumerate(zip(before,after)) if x != y]
                if bit != 2 or before[donor] < after[donor]:
                    continue
                cert = certify(atom,verifier,parents,before,after,donor,1)
                size = sum(bool(mask & 2) for mask in after[:donor])
                assert size == row["q"][1] and list(range(size)) == [i for i in range(donor) if after[i]&2]
                live = after[:]
                prefix = []
                for j in range(donor+1,k):
                    assert live[j] & 2
                    live[j] ^= 2
                    prefix.append(live[:])
                    totals["left_removals"] += 1
                for j in range(k):
                    if not live[j] >> right & 1:
                        live[j] |= 1 << right
                        prefix.append(live[:])
                        totals["right_additions"] += 1
                assert path[pos+1:pos+1+len(prefix)] == prefix
                control = omit_clear(fork.normalize,args,pos,donor,1,"current")
                expected = [s[:] for s in path]
                for s in expected[pos:]:
                    s[donor] |= 2
                assert expected == control
                check_edges(control,graph,index,len(parents))
                totals["left_deletions"] += 1
                totals["nonempty_prefixes"] += bool(prefix)
                if (b,c,k,row["state"],pos) == (2,2,3,0,8):
                    assert prefix == [[31,1,113],[31,17,113]]
                    highlighted = {"source_certificate":cert,"prefix":prefix,"original":path[pos:],
                                   "restored_bit_control":control[pos:]}
    assert highlighted and list(totals.values()) == [139,98,81,30,102]
    return {"counts":totals,"rise":highlighted}


def main(out):
    sys.path.insert(0,str(STAR.resolve()))
    star = module("original_star_writer",STAR/"producer.py","ffd513619d182abea2b31bd90c38e12784557bf3")
    verifier_path = STAR/"verifier.py"
    validate = module("star_check",verifier_path,"80a47f10231a086af161c4999c582fa038d064c7")
    sys.path.insert(0,str(FORK.resolve()))
    fork = module("original_fork_writer",FORK/"producer.py","e73a02ee05e11f0c6b041b783ba6ff9738271073")
    assert (STAR/"graph_producer.py").read_bytes() == (FORK/"graph_producer.py").read_bytes()
    atom = module("original_atom",ATOM/"engine.py","c10ac57f988a439144e21898bd2b33ece0838a9b")
    verifier = module("original_atomic_verifier",ATOM/"verify.py","91cd1e507e955683e744fbdbb0745cac19d66cb3")
    data = {"star":star_pair(star,validate,atom,verifier),"fork":fork_boundaries(fork,atom,verifier)}
    out.mkdir(parents=True,exist_ok=True)
    raw = (json.dumps(data,sort_keys=True,indent=2)+"\n").encode()
    (out/"donor_read_certificate.json").write_bytes(raw)
    return {"certificate_sha256":hashlib.sha256(raw).hexdigest(),"fork_counts":data["fork"]["counts"],
            "star_rows":sorted(data["star"]["rows"])}


if __name__ == "__main__":
    print(json.dumps(main(Path(sys.argv[1])),sort_keys=True,indent=2))
