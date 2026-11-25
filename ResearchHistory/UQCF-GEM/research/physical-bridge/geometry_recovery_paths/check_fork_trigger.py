"""Enumerate complete native deletion histories without selecting the post-source actor."""
from collections import Counter, defaultdict
from fractions import Fraction
from functools import lru_cache
from hashlib import sha1, sha256
import importlib.util
from itertools import product
import json
import lzma
from pathlib import Path
import sys

from check_fixed_pair import HIST, PINS, bitmask, integer_tuple, modules, require, wire
from check_fixed_pair_match import FIELDS

POS = "v16.28-diamond-attribution-closure/producer.py"
POS_BLOB = "36c894db328c0865007df3ca273ddb059475fe4a"


def load_poset(root):
    path = root / "ResearchHistory/UQCF-GEM/demos" / POS
    data = path.read_bytes()
    require(sha1(f"blob {len(data)}\0".encode()+data).hexdigest() == POS_BLOB, POS)
    spec = importlib.util.spec_from_file_location("fixed_fork_precedence", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def state_key(family):
    return "/".join(str(bitmask(view)) for view in family)


def run(ops, poset, parents, grade, before, source, leaf, fork):
    engine, gate, overlap = ops["cut"], ops["gate"], ops["overlap"]
    full = tuple(range(len(parents)))
    receiver = 1-source
    initial = engine.atomic(parents, before, source, leaf)
    gate.verify_atomic(initial)
    start = tuple(map(tuple, initial["after"]))
    states = {}
    terminal_states = {}
    histories = defaultdict(list)
    mass = defaultdict(Fraction)
    prior_amounts = overlap.push(parents, full, before[receiver], grade)

    def visit(family):
        key = state_key(family)
        if key in states:
            return
        view = family[receiver]
        projected = integer_tuple(overlap.push(parents, before[receiver], view, tuple(prior_amounts)))
        edges = {}
        nxt = []
        for i, chart in enumerate(family):
            for v in chart:
                try:
                    edge = engine.atomic(parents, family, i, v)
                except ValueError:
                    continue
                gate.verify_atomic(edge)
                after = tuple(map(tuple, edge["after"]))
                if i == receiver:
                    staged = integer_tuple(overlap.push(parents, view, after[i], projected))
                    direct = integer_tuple(overlap.push(parents, before[receiver], after[i], tuple(prior_amounts)))
                    require(staged == direct, "actual local grades do not compose")
                edges[str(i*len(parents)+v)] = [state_key(after), edge["parent"], [edge[f] for f in FIELDS]]
                nxt.append(after)
        states[key] = dict(receiver=[list(pair) for pair in zip(view, projected)], tau=engine.tau_at(parents, family, fork),
                           h=engine.h(parents, family), edges=edges)
        if not nxt:
            terminal_states[key] = family
        for after in nxt:
            visit(after)

    def unfold(key, word, weight):
        edges = states[key]["edges"]
        if not edges:
            histories[key].append(word)
            mass[key] += weight
            return
        for cmd, (after, _, _) in edges.items():
            unfold(after, [*word, int(cmd)], weight/len(edges))

    visit(start)
    unfold(state_key(start), [], Fraction(1))
    endpoints = {}
    for key, end in terminal_states.items():
        factor = engine.factor(parents, start, end)
        gate.verify_factor(factor)
        example = [event["index"]*len(parents)+event["leaf"] for event in factor["steps"]]
        p, before_, after_ = poset.validate(parents, start, end)
        removed = tuple((i, v) for i, y in enumerate(before_) for v in sorted(set(y)-set(after_[i])))
        pred = poset.predecessor_masks(p, removed)
        commands = [i*len(p)+v for i, v in removed]
        full_mask = (1 << len(removed))-1

        @lru_cache(None)
        def extensions(mask):
            if mask == full_mask:
                return 1
            return sum(extensions(mask | (1 << k)) for k, parents_mask in enumerate(pred)
                       if not mask & (1 << k) and not (parents_mask & ~mask))

        words = sorted(histories[key])
        require(example in words and len(words) == extensions(0) and len(set(map(tuple, words))) == len(words),
                "incorrect endpoint interval")
        for word in words:
            mask = 0
            for cmd in word:
                k = commands.index(cmd)
                require(not pred[k] & ~mask, "forbidden precedence")
                mask |= 1 << k
            require(mask == full_mask, "incomplete endpoint word")
        endpoints[key] = dict(words=words, factor=example, uniform_enabled=str(mass[key]))
    return dict(parents=list(parents), grades=list(grade), source=source, cut=leaf, fork=fork,
                before=state_key(before), after=state_key(start), prior_receiver=[list(t) for t in zip(before[receiver], integer_tuple(prior_amounts))],
                source_fields=[initial[k] for k in FIELDS], states=states, endpoints=endpoints)


def common_fork(parents, tip_a, tip_b):
    below_a = {tip_a}
    while tip_a:
        tip_a = parents[tip_a]
        below_a.add(tip_a)
    while tip_b not in below_a:
        tip_b = parents[tip_b]
    return tip_b


def summary(data):
    counts = Counter()
    examples = {}
    paired = defaultdict(list)
    for key, arm in data.items():
        is_bare = key.startswith("bare:")
        states, ends = arm["states"], arm["endpoints"]
        c, start, base = arm["fork"], arm["after"], dict(arm["prior_receiver"])[arm["fork"]]
        if is_bare:
            counts["source_arms"] += 1
            counts["indexed_states"] += len(states)
            counts["legal_edges"] += sum(len(s["edges"]) for s in states.values())
        details = {}
        for endpoint, terminal in ends.items():
            value = dict(states[endpoint]["receiver"])[c]
            kind = "write" if value != base else "unchanged"
            seen_early = with_trigger = with_global = receiver_last = 0
            for word in terminal["words"]:
                current = start
                changed = False
                fired = False
                early = False
                rises = 0
                for command in word:
                    current, at, fields = states[current]["edges"][str(command)]
                    now = dict(states[current]["receiver"])[c]
                    require(now in (base, value) and (not changed or now == value), "transient receiver reading")
                    changed = now != base
                    if fields[5] and at == c:
                        require(changed and not fired and fields[:2] == [1,2], "geometric event/read order")
                        fired = True
                        receiver_last += command//len(arm["parents"]) == 1-arm["source"]
                    if changed and not fired:
                        early = True
                    rises += fields[4]
                require(current == endpoint and changed == fired, "geometric event equivalence")
                seen_early += early
                with_trigger += fired
                with_global += bool(rises)
            details[kind] = dict(count=len(terminal["words"]), edits=len(terminal["factor"]), scalar=value,
                                 early=seen_early, local_triggers=with_trigger, global_rises=with_global,
                                 receiver_fired=receiver_last, uniform_enabled=terminal["uniform_enabled"])
            if is_bare:
                counts["complete_histories"] += len(terminal["words"])
                counts["with_fork_trigger"] += with_trigger
                counts["reading_before_trigger"] += seen_early
        require(set(details) == {"write", "unchanged"}, "terminal classes")
        if is_bare:
            paired[key.rsplit(":",1)[0]].append(details["write"])
        else:
            examples[key] = details
    for arms in paired.values():
        require(len(arms) == 2, "matched source comparison")
        distinct = arms[0]["scalar"] != arms[1]["scalar"]
        counts["distinct_mass_pairs" if distinct else "equal_mass_pairs"] += 1
        counts["distinct_mass_writes" if distinct else "equal_mass_writes"] += sum(a["count"] for a in arms)
    return dict(bare=dict(sorted(counts.items())), examples=examples)


def build(root):
    ops, poset = modules(root), load_poset(root)
    cases = {}
    for n in range(3, 7):
        for tail in product(*(range(i) for i in range(1, n))):
            p = (-1,) + tail
            leaves = tuple(v for v in range(1, n) if v not in tail)
            if len(leaves) != 2:
                continue
            c = common_fork(p, *leaves)
            g = tuple(3 if v==0 else 2 if v in leaves else 4 for v in range(n))
            chart = tuple(range(n))
            for source, leaf in product((0,1), leaves):
                label = "bare:" + "/".join(map(str,p)) + f":{source}:{leaf}"
                cases[label] = run(ops, poset, p, g, (chart,chart), source, leaf, c)
    for group, spectators in (("named",0), ("one",1), ("two",2), ("balanced",0)):
        p = (-1,0,1,1,3,2,4)
        g = (5,3,4,1,4,2,2) if group!="balanced" else (4,3,5,1,4,2,2)
        active = tuple(range(7))
        family = (active, active)
        if spectators:
            added = tuple(range(7, 8+spectators))
            p += (0,) + added[:-1]
            g = (g[0]-len(added),) + g[1:] + (1,)*len(added)
            family += ((0,)+added, (0,)+added[:-1])
        for leaf in (5,6):
            cases[f"{group}:{leaf}"] = run(ops, poset, p, g, family, 1, leaf, 1)
    return cases


def main(root, out):
    data = build(root)
    raw = wire(data)
    out.mkdir(exist_ok=True, parents=True)
    (out/"fork_trigger_universe.json.xz").write_bytes(lzma.compress(raw, preset=6))
    cert = dict(historical_sha=HIST, historical_blobs={**{k:b for k, (_, b) in PINS.items()}, "poset":POS_BLOB},
                raw_sha256=sha256(raw).hexdigest(), **summary(data))
    (out/"fork_trigger_certificate.json").write_text(json.dumps(cert, sort_keys=True, indent=2)+"\n")
    print(json.dumps(cert["bare"], sort_keys=True))


if __name__=="__main__":
    main(Path(sys.argv[1]), Path(sys.argv[2]))
