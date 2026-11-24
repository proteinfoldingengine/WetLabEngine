"""Replay both native cuts and the already-running v16.43 writer at every flat switch."""
from collections import Counter
from functools import lru_cache
from hashlib import sha256
from itertools import combinations, permutations
import json
import lzma
from pathlib import Path
import sys

from check_all_chart_passage import load_sources, require, write_json
from check_cover_member_pruning import ARCHIVE_DIGEST, Deletions, load_star
from check_matched_source_events import state_masks

CHARTS = range(4)
LEAVES = range(1, 5)
NAMED = (1, 21, 15, 25)


@lru_cache(maxsize=None)
def covers(state):
    """All covers of minimum cardinality, in the archive's chart order."""
    for size in range(1, 5):
        choices = [list(group) for group in combinations(CHARTS, size)
                   if all(any(state[j] & (1 << v) for j in group) for v in LEAVES)]
        if choices:
            return choices
    raise ValueError("uncovered leaf")


def flip(state, chart, leaf):
    values = list(state)
    values[chart] ^= 1 << leaf
    return tuple(values)


def placements():
    cases = {}
    for blank, source, left, right in permutations(CHARTS):
        for private, x, y, z in permutations(LEAVES):
            rows = [1] * 4
            for leaf, holders in ((private, [source]), (x, [source, left]),
                                  (y, [source, right]), (z, [left, right])):
                for j in holders:
                    rows[j] |= 1 << leaf
            state = tuple(rows)
            identity = (blank, source, tuple(sorted((x, y))))
            if state in cases:
                require(cases[state] == identity, "inconsistent relabeling")
            cases[state] = identity
    return cases


class Archive:
    def __init__(self, entry):
        self.entry = entry
        self.graph = entry["graph"]
        self.rows = self.graph["states"]
        self.ids = {tuple(row): i for i, row in enumerate(self.rows)}
        exact, = (r for r in self.graph["profiles"] if r["q"] == [2, 0, 0, 0, 0])
        group, = exact["zero_components"]
        self.fiber = set(group)

    def q(self, state):
        i = self.ids[tuple(state)]
        return self.graph["attained_profiles"][self.graph["profile_ids"][i]][0]

    def edge(self, smaller, larger, chart, leaf):
        require(flip(smaller, chart, leaf) == tuple(larger) and smaller[chart] < larger[chart],
                "false oriented edge")
        row = self.ids[tuple(smaller)]
        require(self.graph["forward_moves"][row] & (1 << (4 * chart + leaf - 1)), "missing archived edge")
        return self.ids[tuple(larger)]

    def exact_additions(self, state):
        row = self.ids[state]
        moves = self.graph["forward_moves"][row]
        found = []
        for j in CHARTS:
            for v in LEAVES:
                if moves & (1 << (4 * j + v - 1)):
                    nxt = flip(state, j, v)
                    if self.q(nxt) == 2:
                        require(self.ids[nxt] in self.fiber, "foreign exact component")
                        found.append([j, v])
        return found


def fixed_paths(graph, state):
    q, moves = graph.next(state)
    paths = [[[j, v]] + tail for j, v, nxt, h in moves if h == q
             for tail in fixed_paths(graph, nxt)]
    return paths or [[]]


def arm(graph, archive, start, source, leaf, other):
    event = graph.cut(start, source, leaf)
    after = tuple(state_masks(event["after"]))
    archive.edge(after, start, source, leaf)
    require((event["h_before"], event["h_after"], event["trigger"]) == (2, 2, False), "cut signature")
    q, moves = graph.next(after)
    deletions = []
    for j, v, nxt, h in moves:
        archive.edge(nxt, after, j, v)
        require(archive.q(nxt) == h and ((archive.ids[nxt] in archive.fiber) == (h == 2)),
                "archive profile disagreement")
        deletions.append([j, v, h])
    paths = sorted(fixed_paths(graph, after))
    destinations = {p[0][0] for p in paths}
    require(len(destinations) == 1 and all(len(p) == 2 for p in paths), "next destination")
    receiver, = destinations
    additions = archive.exact_additions(after)
    require([source, leaf] in additions and archive.ids[start] in archive.fiber, "reverse to prior")
    join = graph.cut(after, source, other)
    joined = tuple(state_masks(join["after"]))
    require(join["h_after"] == archive.q(joined) == 3, "unrestricted join")
    return dict(leaf=leaf, row=archive.ids[after], signature=[q, event["delta_h"], event["trigger"]],
                receiver=receiver, deletions=deletions, fixed_paths=paths,
                exact_additions=additions, double_cut=archive.ids[joined])


def trace_writer(writer, verifier, archive, start, source, cuts):
    """Observe the existing closure and the same mutable state before each cleanup call."""
    lines = Path(writer.__file__).read_text().splitlines()
    bound, = (i for i, line in enumerate(lines, 1) if line == " for v in range(1,m+1):")
    done, = (i for i, line in enumerate(lines, 1) if line.startswith(" for a,b in zip(sorted(set(H)"))
    control = {}
    steps = []

    def observe(frame, event, arg):
        if frame.f_code is writer.normalize.__code__ and event == "line":
            scope = frame.f_locals
            if frame.f_lineno == bound and not control:
                require(scope["s"] == list(start) and len(scope["path"]) == 1, "late binding")
                control.update(team=scope["H"], live=scope["s"], pruning=True)
            if frame.f_lineno == done:
                control["pruning"] = False
        if event == "call" and frame.f_code.co_name == "change" and frame.f_back.f_code is writer.normalize.__code__:
            if control.get("pruning"):
                context = frame.f_back.f_locals
                local = frame.f_locals
                require(context["H"] is control["team"] and context["s"] is control["live"], "rebound controller")
                require(not local["add"], "addition in cleanup")
                prior = tuple(context["s"])
                j, v = local["j"], local["v"]
                after = flip(prior, j, v)
                pre_covers = covers(prior)
                post_covers = covers(after)
                record = dict(chart=j, leaf=v, keeper=context["keep"], before=archive.ids[prior],
                              after=archive.ids[after], covers_before=pre_covers, covers_after=post_covers)
                if j == source and v in cuts:
                    other, = set(cuts) - {v}
                    valid = any(prior[m] & (1 << other) for m in CHARTS if m != source)
                    alternative = covers(flip(prior, source, other)) if valid else []
                    record["opposite"] = dict(legal=valid, keeps_q=bool(alternative and len(alternative[0]) == 2),
                                              keeps_bound=list(control["team"]) in alternative)
                steps.append(record)
        return observe

    old = sys.gettrace()
    try:
        sys.settrace(observe)
        path = writer.normalize(start, 4, 4, 2)
    finally:
        sys.settrace(old)
    ids = [archive.ids[tuple(row)] for row in path]
    i = ids[0]
    rec = archive.entry["normalizations"][i]
    end = archive.ids[verifier.canonical(4, 4, 2)]
    require(rec == {"state": i, "q": 2, "path": ids} and verifier.path_valid(ids, i, end, archive.graph, 2, 0),
            "historical path mismatch")
    require([s["after"] for s in steps] == ids[1:4] and len(steps) == 3, "cleanup trace mismatch")
    return dict(bound_before=ids[0], bound_cover=list(control["team"]), cleanup=steps, archived_path=ids)


def counts(rows):
    stats = Counter(starts=len(rows), source_first=0, source_second=0, source_last=0,
                    source_absent=0, source_resolves_visible_cover=0, source_after_visible_resolution=0,
                    source_followed_by_receiver=0, opposite_native=0, opposite_flat=0, opposite_keeps_bound=0)
    for row in rows:
        steps = row["writer"]["cleanup"]
        index = next((i for i, step in enumerate(steps) if "opposite" in step), None)
        if index is None:
            stats["source_absent"] += 1
            continue
        stats[("source_first", "source_second", "source_last")[index]] += 1
        step = steps[index]
        stats["source_resolves_visible_cover" if len(step["covers_before"]) == 2
              else "source_after_visible_resolution"] += 1
        receiver, = [a["receiver"] for a in row["arms"] if a["leaf"] == step["leaf"]]
        if index + 1 < len(steps):
            require(steps[index + 1]["chart"] == receiver, "wrong receiver in same invocation")
            stats["source_followed_by_receiver"] += 1
        for key, field in (("opposite_native", "legal"), ("opposite_flat", "keeps_q"),
                           ("opposite_keeps_bound", "keeps_bound")):
            stats[key] += int(step["opposite"][field])
    return dict(stats)


def main(source_dir, output):
    _, _, atom, verify_atom, _, _ = load_sources(source_dir)
    writer, verifier, entry = load_star(source_dir)
    archive = Archive(entry)
    graph = Deletions(atom, verify_atom)
    rows = []
    for start, (blank, source, cuts) in sorted(placements().items()):
        arms = [arm(graph, archive, start, source, v, w) for v, w in (cuts, cuts[::-1])]
        require(arms[0]["receiver"] != arms[1]["receiver"] and arms[0]["double_cut"] == arms[1]["double_cut"],
                "opposed receivers or common join")
        rows.append(dict(start=list(start), row=archive.ids[start], blank=blank, source=source,
                         arms=arms, writer=trace_writer(writer, verifier, archive, start, source, cuts)))
    core = [r for r in rows if r["blank"] == 0 and r["source"] == 2]
    raw = (json.dumps(rows, separators=(",", ":"), sort_keys=True) + "\n").encode()
    output.mkdir(exist_ok=True, parents=True)
    (output / "flat_cover_universe.json.xz").write_bytes(lzma.compress(raw, preset=9))
    named, = (r for r in core if tuple(r["start"]) == NAMED)
    evidence = dict(archive_sha256=ARCHIVE_DIGEST, universe_sha256=sha256(raw).hexdigest(),
                    chart_leaf_relabelings=576, original=counts(core), all_labels=counts(rows), named=named)
    write_json(output / "flat_cover_certificate.json", evidence)
    print(json.dumps({k: evidence[k] for k in ("original", "all_labels", "universe_sha256")}, sort_keys=True))


if __name__ == "__main__":
    main(Path(sys.argv[1]).resolve(), Path(sys.argv[2]))

