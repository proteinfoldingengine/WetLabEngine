"""Verify four original v16.54 M9 records and the closed-row transport result."""
import argparse
from collections import deque
import gzip
from hashlib import sha256
from itertools import combinations, permutations
import json
import os
from pathlib import Path
import sys
from zipfile import ZipFile

HERE = Path(__file__).resolve().parent
RUN = 37059520424
ARTIFACT = 11251351546
ZIP_SHA = "4cb17f4395c811d96121ac322c5ab54844a2b583ef7833a933fcabbc9cceb7ec"
FIRST = 2393446
PINS = {
    "mechanisms.py": "6a54d4fbb6d26b7f07e08e62e42afabaeb45b12995a5686ec25d13942f85dbdb",
    "model.py": "3c01f1f348d1d9bc4a4b4ad6b501d41db24b02e54cfe8cd394eeac80152bbee7",
    "universe.py": "acae5a97c27549cc12908adc662a54e77319f3c493707c35b9d5c18c4737f52f",
    "inherited_binding.py": "5d95155c79cf5fc3a9126a9b21d6805188a4fad9ceb9423903a28674d777ea43",
    "verifier.py": "19f3cb383e3976a72285ad30a0cd5a52a74b4b7f2e9a86653a2f8ecfbaaac150",
}
LINE_PINS = (
    "8f158daa442e7e153f4aaa8fa2408ded7a5b7755d6e185e6d42a12b67b5d6cb8",
    "4341d70cc3ee321b37ddb64202743ca55482c261f6c512d69ab03483c98e1ff3",
    "faf1ae83095b9f38b4ef8a7f9828a823ccc2b49996163b337e5a36e63202bb09",
    "257d11545a8ba240ba72ea09de8d7576e4750b55b7291b5b455f0032d653b413",
)


def check_shard(archive, extracted):
    assert sha256(archive.read_bytes()).hexdigest() == ZIP_SHA
    with ZipFile(archive) as z:
        provenance = json.loads(z.read("PROVENANCE.json"))
        assert int(provenance["run_id"]) == RUN and provenance["shard"] == 7
        freeze = json.loads(z.read("scientific/DOMAIN_FREEZE.json"))
        assert freeze["stop"]-4 == FIRST
        summary = json.loads(z.read("scientific/SUMMARY.json"))
        assert summary["counts"]["M9:PASS"] == 4
        for name, pin in PINS.items():
            assert sha256(z.read("source/"+name)).hexdigest() == pin
        for name in ("CASES","RECORDS"):
            with z.open("scientific/"+name+".jsonl.gz") as raw, gzip.GzipFile(fileobj=raw) as stream:
                tail = list(deque(enumerate(stream,freeze["start"]),maxlen=4))
            assert [i for i,_ in tail] == list(range(FIRST,FIRST+4))
            for (_,line),saved in zip(tail,extracted):
                if name == "RECORDS":
                    assert line == saved
                else:
                    assert json.loads(line)["identity"] == json.loads(saved)["identity"]


def slot_values(state, leaves):
    assert all(len(state[leaf]) == 1 for leaf in leaves)
    return tuple(state[leaf][0] for leaf in leaves)


def local_history(record,row):
    nodes = record["nodes"]
    root = nodes[0][row]
    leaves = nodes[root]
    p = record["path"]
    nested = record["nested_path"]
    boundaries = record["facts"]["parent_boundaries"]
    history = []
    for t in range(1,len(p)):
        old,new = set(p[t-1][row]),set(p[t][row])
        if old == new:
            continue
        x, = old ^ new
        before = slot_values(nested[boundaries[t-1]],leaves)
        after = slot_values(nested[boundaries[t]],leaves)
        dest = [i for i,(l,r) in enumerate(zip(before,after)) if l != r]
        # Independently transcribe only the row and its own leaf incidences.
        changed = []
        for s in range(boundaries[t-1]+1,boundaries[t]+1):
            edits = [(v,j,j in nested[s][v]) for v in [root]+leaves
                     for j in set(nested[s][v]) ^ set(nested[s-1][v])]
            assert len(edits)==1
            changed.extend(edits)
        expected = [(root,x,x in new)]
        if x in before and x not in new:
            i = before.index(x)
            spare = min(old-set(before))
            assert dest == [i] and after[i] == spare
            expected = [(leaves[i],spare,True),(leaves[i],x,False)] + expected
        else:
            assert not dest
        assert changed == expected
        history.append(dict(parent_frame=t,nested_frames=[boundaries[t-1],boundaries[t]],
                            before=sorted(old),after=sorted(new),x=x,add=x in new,
                            slots_before=before,slots_after=after,changes=changed))
    return history


def closed_and_twins(record):
    path,nested,nodes = record["path"],record["nested_path"],record["nodes"]
    closed = []
    twins = []
    registers = [(slot_values(nested[0],nodes[row]),slot_values(nested[-1],nodes[row]))
                 for row in nodes[0]]
    for i,(start,end) in enumerate(registers):
        if path[0][i] == path[-1][i] and start != end:
            closed.append(i)
    for i,j in combinations(range(len(registers)),2):
        a,b = registers[i],registers[j]
        if (a[0] == b[0] and path[0][i] == path[0][j] and path[-1][i] == path[-1][j]
                and set(a[1]) != set(b[1])):
            twins.append((i,j))
    return closed,twins


def matched(record, histories, clear_role):
    p = record["identity"][1]
    h,k,n = p["h"],p["k"],p["N"]
    assert p["q"] == 3
    early,last = n+1,2*n-1
    marked = 2*h
    receipts = []
    for row,slot,old in ((early,h-1,2*h-1),(last,0,h)):
        hist = histories[row]
        write, = [e for e in hist if not e["add"] and e["slots_before"]==tuple(range(h,2*h))
                  and e["slots_after"][slot]==marked]
        assert write["before"]==list(range(h,2*h+1)) and write["x"]==old
        read, = [e for e in hist if e["before"]==list(range(h))+[marked] and not e["add"]
                 and e["x"]==marked]
        assert read["slots_before"].index(marked)==slot and read["slots_after"][slot]==h-1
        assert all(e["slots_after"][slot]==marked for e in hist
                   if write["parent_frame"] <= e["parent_frame"] < read["parent_frame"])
        leaves=record["nodes"][record["nodes"][0][row]]
        assert all(e["slots_after"]==read["slots_after"] for e in hist if e["parent_frame"]>=read["parent_frame"])
        # Project the actual pre-read subtree and replay the original writer.
        # Sorting the slots is a separate intervention with the identical parent command.
        def replay_local(held):
            parent=set(read["before"])
            states = [parent]+[{x} for x in held]
            raw = [sum(1<<v for v,z in enumerate(states) if j in z) for j in range(k)]
            start=raw[:]
            trace=[]
            clear_role(raw,[list(range(1,h+1))]+[[] for _ in held],0,marked,h-1,trace)
            assert len(trace)==2
            gain=trace[0][h-1]^start[h-1]
            assert gain.bit_count()==1
            return gain.bit_length()-2
        assert replay_local(read["slots_before"])==slot
        erased_slot = replay_local(sorted(read["slots_before"]))
        assert erased_slot == h-1
        receipts.append(dict(row=row,leaf=leaves[slot],slot=slot,write=write,read=read,
                             terminal_parent=record["path"][-1][row],
                             terminal_leaves=hist[-1]["slots_after"],sorted_control_slot=erased_slot))
    assert receipts[0]["write"]["slots_before"]==receipts[1]["write"]["slots_before"]
    assert receipts[0]["read"]["before"]==receipts[1]["read"]["before"]
    assert receipts[0]["read"]["after"]==receipts[1]["read"]["after"]
    assert set(receipts[0]["read"]["slots_before"])==set(receipts[1]["read"]["slots_before"])
    return receipts


def cycle(record, histories):
    p = record["identity"][1]
    h,k,n = p["h"],p["k"],p["N"]
    row = 2*n-1
    hist = histories[row]
    full=list(range(k))
    assert hist[0]["before"]==hist[-1]["after"]==full
    init = tuple(range(h))
    assert hist[0]["slots_before"]==init
    assert hist[-1]["slots_after"]==(h-1,)+tuple(range(h-1))
    def move(ordered):
        held = list(ordered)
        for e in hist:
            if not e["add"] and e["x"] in held:
                held[held.index(e["x"])] = min(set(e["before"])-set(held))
        return tuple(held)
    held=init
    for num in range(1,h+1):
        held=move(held)
        assert (held==init)==(num==h)
    for ordering in permutations(init):
        assert move(ordering) == tuple((v-1)%h for v in ordering)
    return row


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("demo",type=Path)
    parser.add_argument("--shard",type=Path)
    parser.add_argument("--details",action="store_true")
    args=parser.parse_args()
    raw=gzip.decompress((HERE/"original_m9.jsonl.gz").read_bytes()).splitlines(keepends=True)
    assert tuple(sha256(line).hexdigest() for line in raw)==LINE_PINS
    if args.shard:
        check_shard(args.shard.resolve(),raw)
    demo=args.demo.resolve()
    for name,pin in PINS.items():
        assert sha256((demo/name).read_bytes()).hexdigest()==pin
    # The historical binding authenticates v16.53 using git show in this checkout.
    os.chdir(demo)
    sys.path.insert(0,str(demo))
    import mechanisms
    import universe
    import verifier
    from inherited_binding import load_clearance
    clear_role,_=load_clearance()
    cases = {json.dumps(c["identity"],sort_keys=True):c for c in universe.m9({})}
    assert len(cases)==4
    details=[]
    for number,line in enumerate(raw,FIRST):
        record=json.loads(line)
        case=cases.pop(json.dumps(record["identity"],sort_keys=True))
        actual=mechanisms.produce(case)
        assert (json.dumps(actual,sort_keys=True,separators=(",",":"))+"\n").encode()==line
        assert verifier.verify_record(case,record)==[]
        h,q = [case["identity"][1][j] for j in ("h","q")]
        histories = [local_history(record,i) for i in range(len(record["nodes"][0]))]
        closed,twins=closed_and_twins(record)
        result=dict(ordinal=number,h=h,q=q,parent_frames=len(record["path"]),
                    nested_frames=len(record["nested_path"]),closed_changed=closed,unequal_terminal_pairs=twins)
        if q==3:
            result["matched"]=matched(record,histories,clear_role)
            result["cycle_row"]=cycle(record,histories)
        if (h,q)==(3,3):
            initial=record["nested_path"][0]
            terminal=record["nested_path"][-1]
            leaves = [record["nodes"][record["nodes"][0][i]] for i in (6,7)]
            parts = [(slot_values(initial,vs),slot_values(terminal,vs)) for vs in leaves]
            assert parts==[((0,1,2),(3,6,5)),((0,1,2),(2,0,1))]
            assert (6,7) in twins
            result["rows_6_7_initial_terminal"]=parts
        details.append(result)
    assert not cases
    assert sum(len(r["unequal_terminal_pairs"]) for r in details)==35
    assert sum(len(r["closed_changed"]) for r in details)==14
    extra=[]
    for h in range(4,8):
        n=h+1
        case=universe.guard_case(h,3,2*n,1,1,"M9")
        record=mechanisms.produce(case)
        assert verifier.verify_record(case,record)==[]
        histories=[local_history(record,i) for i in range(len(record["nodes"][0]))]
        matched(record,histories,clear_role)
        row=cycle(record,histories)
        extra.append([h,row,len(record["path"]),len(record["nested_path"])])
    if args.details:
        print(json.dumps(dict(archived=details,additional_q3=extra),sort_keys=True,indent=2))
    else:
        for r in details:
            print(r["ordinal"],"h,q",r["h"],r["q"],"parent/nested frames",r["parent_frames"],r["nested_frames"],
                  "closed rows with changed slots",len(r["closed_changed"]),
                  "matched row pairs with distinct terminal leaf sets",len(r["unequal_terminal_pairs"]))
        print("Additional q=3 executions [h, last row, parent frames, nested frames]",extra)
        print("Original newline-terminated records regenerated byte for byte. All stock verification checks passed.")


if __name__=="__main__":
    main()
