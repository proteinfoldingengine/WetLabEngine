"""Call the complete archived star normalizer on both full 121-chart histories."""
from hashlib import sha1
import importlib.util
import json
from pathlib import Path
import sys

from replay import ARMS, LINE, PINS, RECEIVERS, original, prepare, remove, required, row_at


def load_module(name, path, pin):
    raw = Path(path).read_bytes()
    assert sha1(b'blob '+str(len(raw)).encode()+bytes(1)+raw).hexdigest() == pin
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def run(state, order, leaves, normalize):
    winner_set = required(state)
    address = {leaf: i+1 for i,leaf in enumerate(leaves)}
    encoded = tuple(1 | sum(1<<address[a] for a in row_at(state,j)) for j in order)
    path = normalize(encoded, len(leaves), len(order), len(winner_set))
    boundary = sum(len(owners)-1 for owners in state.values())
    expected = [1] * len(order)
    for leaf in leaves:
        j = next(k for k,chart in enumerate(order) if chart in winner_set and chart in state[leaf])
        expected[j] |= 1 << address[leaf]
    assert list(path[boundary]) == expected
    first_gain = None
    for step,(before,after) in enumerate(zip(path,path[1:]),1):
        changes = [(a,b) for a,b in zip(before,after) if a!=b]
        assert len(changes)==1 and (changes[0][0]^changes[0][1]).bit_count()==1
        if changes[0][1] > changes[0][0] and first_gain is None:
            first_gain = step
    assert first_gain == boundary+1
    records = {j: (expected[order.index(j)].bit_count()-1) for j in RECEIVERS}
    return dict(contraction_edits=boundary, total_edits=len(path)-1, records=records), path[-1]


if __name__=='__main__':
    orbit, graph, producer = sys.argv[1:]
    load_module('graph_producer', graph, '6c8eca570cda82b64c0d06775672f33977be430a')
    normalize = load_module('historic_star_writer', producer, 'ffd513619d182abea2b31bd90c38e12784557bf3').normalize
    _, common, _ = prepare(original(orbit,PINS[0])['orbit'])
    states = []
    for arm in ARMS:
        s = common.copy()
        for a in arm:
            remove(s,0,a)
        states.append(s)
    remaining = sorted(set(range(121)) - LINE - set(RECEIVERS))
    leaves = sorted(common)
    outputs = []
    for name,charts,addresses in [
        ('line first',sorted(LINE)+list(RECEIVERS)+remaining,leaves),
        ('both receivers before source',sorted(LINE-{0},reverse=True)+[5,15,0]+remaining[::-1],leaves[::-1])
    ]:
        outcomes = [run(s,charts,addresses,normalize) for s in states]
        assert outcomes[0][1] == outcomes[1][1]
        outputs.append(dict(priority=name, arms=[x[0] for x in outcomes], same_terminal_state=True))
    extremes = []
    for s,r in zip(states, RECEIVERS):
        cover = required(s)
        priority = [r] + sorted(cover-{r}) + sorted(set(range(121))-cover)
        data,_ = run(s, priority, leaves, normalize)
        assert data['records'][r]==200
        extremes.append(data)
    print(json.dumps(dict(common_priorities=outputs, compulsory_chart_first=extremes),sort_keys=True,indent=2))
