"""Run actual star deletions and the archived cleanup on two equal-height source cuts."""
import argparse
from collections import Counter
from functools import lru_cache
import gzip
from hashlib import sha256
import importlib.util
from itertools import combinations, permutations, product
import json
import lzma
from pathlib import Path
import sys
from unittest.mock import patch

from check_all_chart_passage import direct_short_path, load_sources, relabel, require, run_writer, views, write_json
from check_receiver_command import hash_blob
from check_matched_source_events import CHILDREN, HIST, LABELS, SCI, STAR, WITNESS, atlas, state_masks, unit_grade

NAMED = [[], [1], [1, 2, 3, 4], [2, 3]]
SOURCE, RECEIVER = 2, 3
OLD = SCI / "demos/v16.43-star-fiber-classification"
ARCHIVE = "evidence/science/scientific/CERTIFICATE.json.gz"
ARCHIVE_DIGEST = "f2de35e7f7fea13621c332cae71dbdc69da63cf8dd806827601fa90b07145a25"


def encode(masks):
    return sum(m << (j*5) for j, m in enumerate(masks))


def decode(value):
    return [(value >> (j*5)) & 31 for j in LABELS]


def load_module(folder, name, filename):
    spec = importlib.util.spec_from_file_location(name, folder/filename)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def load_star(source):
    folder = source / OLD
    sys.path.insert(0, str(folder))

    for name, blob in {"producer":"ffd513619d182abea2b31bd90c38e12784557bf3",
                       "verifier":"80a47f10231a086af161c4999c582fa038d064c7",
                       "graph_producer":"6c8eca570cda82b64c0d06775672f33977be430a",
                       "graph_verifier":"ff8af4ecf743507d0d601daffa9b054441b85fd1"}.items():
        require(hash_blob((folder/(name+".py")).read_bytes())==blob, name)
    writer = load_module(folder, "cover_member_star", "producer.py")
    verifier = load_module(folder, "cover_member_star_verifier", "verifier.py")
    data = (folder/ARCHIVE).read_bytes()
    require(sha256(data).hexdigest() == ARCHIVE_DIGEST, "archived campaign digest")
    history, = (e for e in json.loads(gzip.decompress(data))["entries"] if (e["m"], e["k"]) == (4,4))
    return writer, verifier, history


class Deletions:
    def __init__(self, atom, verifier):
        self.atom = atom
        self.verify = verifier.verify_atomic

    def cut(self, before, j, v):
        d = self.atom.atomic(STAR, views(before), j, v)
        self.verify(d)
        return d

    @lru_cache(maxsize=None)
    def next(self, masks):
        rows = views(masks)
        h = self.atom.h(STAR, rows)
        moves = []
        for j, row in enumerate(rows):
            for v in row[1:]:
                if sum(v in cells for cells in rows) <= 1:
                    continue
                event = self.cut(masks, j, v)
                moves.append((j, v, tuple(state_masks(event["after"])), event["h_after"]))
        return h, moves

    @lru_cache(maxsize=None)
    def ends(self, masks, fixed):
        q, moves = self.next(masks)
        options = [s for _, _, s, h in moves if not fixed or h == q]
        if not options:
            return frozenset([encode(masks)])
        return frozenset().union(*(self.ends(s, fixed) for s in options))


def occupancy(ends, receiver):
    return frozenset(bool(decode(value)[receiver] >> 1) for value in ends)


def replay_star(writer, verifier, history, index, before, observed=False):
    graph = history["graph"]
    start = index[tuple(before)]
    rec = history["normalizations"][start]
    q = graph["attained_profiles"][graph["profile_ids"][start]][0]
    require(rec["state"] == start and rec["q"] == q, "archive association")
    traced = {}
    if observed:
        lines = Path(writer.__file__).read_text().splitlines()
        boundary, = (n for n,s in enumerate(lines,1) if s.startswith(" for a,b in zip(sorted(set(H)"))
        transfer, = (n for n,s in enumerate(lines,1) if s.strip().startswith("for v in leaves:change(b,v,True)"))
        require("leaves=[v for v" in lines[transfer-2], "historical donor line")
        captured = []

        def trace(frame, event, arg):
            if frame.f_code is not writer.normalize.__code__:
                return None
            if event == "line" and frame.f_lineno == boundary and not captured:
                scope = frame.f_locals
                captured.append(scope["s"])
                traced["keeper_cover"] = list(scope["H"])
                traced["cleanup_state"] = scope["s"][:]
                traced["donor_reads"] = []
            if event == "line" and frame.f_lineno == transfer:
                scope = frame.f_locals
                entry = [scope["a"], scope["b"], list(scope["leaves"]), len(scope["path"])-1]
                # The loop header can be reported once per iteration. Only record its initial read.
                if not traced["donor_reads"] or entry[:2] != traced["donor_reads"][-1][:2]:
                    require(scope["s"] is captured[0], "donor live state differs from cleanup state object")
                    require(entry[2] == [v for v in CHILDREN if scope["s"][entry[0]] & (1<<v)],
                            "read does not match live donor")
                    traced["donor_reads"].append(entry)
            return trace

        oldtrace = sys.gettrace()
        try:
            sys.settrace(trace)
            path = writer.normalize(before, 4, 4, q)
        finally:
            sys.settrace(oldtrace)
    else:
        path = writer.normalize(before, 4, 4, q)
    ids = [index[tuple(s)] for s in path]
    end = index[verifier.canonical(4,4,q)]
    require(ids == rec["path"] and verifier.path_valid(ids, start, end, graph, q, 0), "historical path")
    first = next(i for i,s in enumerate(path) if sum(x.bit_count()-1 for x in s) == 4)
    require(all(sum(a.bit_count() for a in b) - sum(a.bit_count() for a in c) == 1
                for b,c in zip(path[:first],path[1:first+1])), "non-deletion before singleton")
    return dict(archive_row=start, q=q, path=[encode(s) for s in path], first_singleton=first, **traced)


def route_control(source, r, v, graph):
    folder = source / SCI / "demos/v16.39-theorem-validation"
    for name, pin in (("construct","284b8cc9305c14f3ff6f3693c67a2c61ea00e93e"),
                      ("check","d4acda0e79a35b6c42ef0984ad362ba5e3bfb684")):
        require(hash_blob((folder/(name+".py")).read_bytes())==pin, name)
    constructor = load_module(folder, "endpoint_constructor", "construct.py")
    checker = load_module(folder, "endpoint_verifier", "check.py")
    event = graph.cut(tuple(state_masks(atlas(WITNESS))), SOURCE, 4)
    a = state_masks(event["after"])
    old = run_writer(r, v, a)
    target = old["end"]
    q = [2,0,0,0,0]
    proof = constructor.build(STAR, 4, q, a, target)
    bypass = direct_short_path(r, v, a, target)
    records = {}
    for name, route in (("v16.39",proof),("v16.53",dict(states=old["path"],zero_prefix=0,zero_suffix=0)),
                        ("direct",dict(states=bypass,zero_prefix=0,zero_suffix=0))):
        checker.path_states(STAR,4,q,a,target,route)
        path = route["states"]
        v.path_check(r.Q,4,[2],path,a,target)
        records[name] = dict(path=path, covers=[checker.profile(STAR,4,s)[0] for s in path],
                             minimum_work=min(sum((s[i]^s[j]).bit_count() for i,j in combinations(LABELS,2))
                                              for s in path),
                             charts_ever_full=[any(s[i]==31 for s in path) for i in LABELS])
    return records


def main(source, out):
    out.mkdir(parents=True, exist_ok=True)
    original, orig_verifier, atom, atom_verify, lineage, _ = load_sources(source)
    writer, verifier, history = load_star(source)
    index = {tuple(s):i for i,s in enumerate(history["graph"]["states"])}
    graph = Deletions(atom, atom_verify)
    starts, terms, pairs = [], {}, []
    partition = Counter()
    for cols in product(range(2,16,2), repeat=4):
        masks = tuple(state_masks(atlas(cols)))
        before_q, legal = graph.next(masks)
        arms = []
        for j,v,post,h in legal:
            if j != SOURCE:
                continue
            key = encode(post)
            if key not in terms:
                terms[key] = [h, sorted(graph.ends(post,True)), sorted(graph.ends(post,False))]
            arms.append([v,key])
        starts.append([list(cols),before_q,arms])
        for (v, vkey), (w, wkey) in combinations(arms,2):
            a,b = terms[vkey],terms[wkey]
            fixed, bare = [], []
            for j in (0,1,3):
                if not occupancy(a[1],j) & occupancy(b[1],j):
                    fixed.append(j)
                if not occupancy(a[2],j) & occupancy(b[2],j):
                    bare.append(j)
            require(set(a[2]) & set(b[2]), "bare native endpoints do not overlap")
            partition[(a[0]==b[0],bool(fixed))] += 1
            pairs.append([list(cols),v,w,fixed,bare])

    named = [[0]+x for x in NAMED]

    @lru_cache(maxsize=None)
    def archived(post):
        return replay_star(writer,verifier,history,index,post)

    catalog = {}
    orbit = []
    for cm in permutations(LABELS):
        for lm in permutations(CHILDREN):
            prior = relabel(named,cm,lm)
            ids = []
            for cut in (1,2):
                ev = graph.cut(tuple(state_masks(prior)), cm[SOURCE], lm[cut-1])
                post = tuple(state_masks(ev["after"]))
                row = archived(post)
                key = encode(post)
                catalog[key] = row
                at_cleanup = decode(row["path"][row["first_singleton"]])
                require((at_cleanup[cm[RECEIVER]] != 1) == (cut == 2), "transported structural receiver")
                ids.append(key)
            orbit.append([list(cm),list(lm),*ids])
    details = []
    for cut in (1,2):
        ev = graph.cut(tuple(state_masks(named)), SOURCE, cut)
        post = tuple(state_masks(ev["after"]))
        with patch.object(lineage.Pruning,"aggregate",side_effect=RuntimeError("unexpected P1 input")):
            rec = replay_star(writer,verifier,history,index,post,observed=True)
            other = run_writer(original,orig_verifier,post)
        first = rec["first_singleton"]
        clean = decode(rec["path"][first])
        require(clean == rec["cleanup_state"], "trace and mathematical stopping state disagree")
        local_moves = []
        for before,after in zip(rec["path"][:first],rec["path"][1:first+1]):
            a,b = decode(before),decode(after)
            if a[RECEIVER] != b[RECEIVER]:
                v = (a[RECEIVER]^b[RECEIVER]).bit_length()-1
                check = graph.cut(tuple(a),RECEIVER,v)
                require(state_masks(check["after"])==b, "wrong receiver primitive")
                local_moves.append(v)
        for donor,dest,leaves,t in rec["donor_reads"]:
            for i,v in enumerate(leaves):
                a,b = map(decode,rec["path"][t+i:t+i+2])
                require(b[dest] == a[dest] | (1<<v) and b[dest]!=a[dest], "undelivered donor copy")
        projection = [unit_grade(lineage, v)[0] for v in [named[SOURCE], ev["after"][SOURCE],
                                                          named[RECEIVER],views(clean)[RECEIVER]]]
        details.append(dict(cut=cut,source_mask=post[SOURCE],post=post,trigger=ev["trigger"],
                            source_height=[ev["h_before"],ev["h_after"]], source_delta=ev["delta_h"],
                            unit_roots_source_before_after_receiver_before_cleanup=projection,
                            receiver_deletions=local_moves, receiver_cleanup=clean[RECEIVER],
                            receiver_star_final=decode(rec["path"][-1])[RECEIVER],
                            all_chart_writer_end=other["end"], all_chart_writer_full=[31]*4 in other["path"],
                            star_record=rec))
    common = []
    for order in ((1,2),(2,1)):
        cur=tuple(state_masks(named))
        for v in order:
            cur=tuple(state_masks(graph.cut(cur,SOURCE,v)["after"]))
        common.append(cur)
    require(common[0]==common[1], "source double-cut diamond")
    common_terminal=min(graph.ends(common[0],False))
    # A full native path to the identical absorbing state from each source arm.
    def continue_to(start):
        state=tuple(start)
        path=[encode(state)]
        while encode(state)!=common_terminal:
            _,moves=graph.next(state)
            state=next(s for _,_,s,_ in moves if common_terminal in graph.ends(s,False))
            path.append(encode(state))
        return path
    joins=[[encode(d["post"]),*continue_to(common[0])] for d in details]
    routes=route_control(source, original, orig_verifier, graph)
    old_cols=list(WITNESS)
    old_pair,= (p for p in pairs if p[:3]==[old_cols,3,4])
    data=dict(preparations=starts,post_states=terms,pairs=pairs,archived_paths=catalog,permutations=orbit)
    raw=(json.dumps(data,sort_keys=True,separators=(",",":"))+"\n").encode()
    (out/"cover_member_universe.json.xz").write_bytes(lzma.compress(raw))
    stats=dict(preparations=len(starts),arms=sum(len(row[2]) for row in starts),pairs=len(pairs),
               equal_cover_pairs=sum(v for (equal,_),v in partition.items() if equal),
               pairs_separating_empty_nonempty=sum(bool(row[3]) for row in pairs),
               equal_cover_separating=partition[True,True],different_cover_separating=partition[False,True],
               pair_receiver_incidences=sum(len(row[3]) for row in pairs),
               bare_forced_pair_receivers=sum(len(row[4]) for row in pairs),
               distinct_base_poststates=len(terms), relabelings=len(orbit), archival_poststates=len(catalog))
    cert=dict(historical=HIST,archive_sha256=ARCHIVE_DIGEST,counts=stats,witness=details,
              prior=state_masks(named),bare_join=common[0],bare_common_terminal=decode(common_terminal),
              bare_control_paths=joins,same_endpoint_routes=routes,prior_strict_flat_receivers=old_pair[3],
              universe_sha256=sha256(raw).hexdigest())
    write_json(out/"cover_member_certificate.json",cert)
    print(json.dumps(stats,sort_keys=True))


if __name__ == "__main__":
    if not __debug__:
        raise RuntimeError("Historical verification requires assertions")
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("historical",type=Path)
    parser.add_argument("out",type=Path)
    args=parser.parse_args()
    main(args.historical.resolve(),args.out)
