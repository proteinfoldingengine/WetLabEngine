"""Audit the prospectively designated outer root leaf on every original directed call."""
import gzip
import hashlib
import json
import sys
from collections import Counter
from fractions import Fraction
from pathlib import Path

import check_routed_chain as chain
import check_fixed_donor as fixed

def holders(state, site):
    return {j for j, mask in enumerate(state) if mask & (1 << site)}

def edits(path):
    for before, after in zip(path, path[1:]):
        changes = [(j, a ^ b) for j, (a, b) in enumerate(zip(before, after)) if a != b]
        (actor, diff), = changes
        assert diff.bit_count() == 1
        yield (actor, diff.bit_length() - 1, bool(after[actor] & diff))

def exact_pair(engine, parents, old, new, site):
    full = tuple(range(len(parents)))
    fine = tuple(v for v in full if new >> v & 1)
    coarse = tuple(v for v in full if old >> v & 1)
    assert set(fine) == set(coarse) | {site} and site not in coarse
    base = (2,) * len(full)
    varied = tuple(2 + Fraction((v == site) - (v == 0), 2) for v in full)
    pairs = [tuple(engine.push(parents, full, view, g) for g in (base, varied)) for view in (coarse, fine)]
    assert pairs[0][0] == pairs[0][1]
    delta = tuple(b-a for a,b in zip(*pairs[1]))
    assert delta == tuple(Fraction((v == site)-(v == 0), 2) for v in fine)
    for index, g in enumerate(pairs[1]):
        assert engine.push(parents, fine, coarse, g) == pairs[0][index]

def scan(index, row, checker, engine):
    path = row["path"]
    parents = tuple(checker.structure(row["spec"]["degrees"]))
    site = len(parents) - 1
    assert parents[site] == 0
    steps = list(edits(path))
    at = [holders(state, site) for state in path]
    protected = [(at[i] & at[i+1]) - {actor} for i,(actor,_,_) in enumerate(steps)]
    delete_rows, copies = [], []
    for i,(donor,v,add) in enumerate(steps):
        if v != site or add:
            continue
        # Recover deletion and gain independently from source holder sets.
        assert at[i] - at[i+1] == {donor}
        twins = sorted(j for j, mask in enumerate(path[i]) if j != donor and mask == path[i+1][donor])
        entry = {"delete":i,"donor":donor,"twins":twins}
        if len(twins) == 1:
            b, = twins
            gain = next((z for z in range(i+1,len(steps)) if steps[z] == (b,site,True)),None)
            independently = next((z for z in range(i+1,len(steps)) if b in at[z+1]-at[z]),None)
            assert gain == independently
            entry["gain"] = gain
            if gain is not None:
                exact_pair(engine,parents,path[gain][b],path[gain+1][b],site)
                entry.update(protected=all(protected[i:gain+1]),endpoint_has=b in at[-1],
                             protected_to_end=all(protected[i:]),protected_from_start=all(protected[:gain+1]))
        delete_rows.append(entry)
        if i and steps[i-1][1:]==(site,True) and len(at[i-1])==len(at[i+1])==1 and at[i-1]!=at[i+1]:
            receiver = steps[i-1][0]
            assert at[i-1]=={donor} and at[i+1]=={receiver} and at[i]=={receiver,donor}
            exact_pair(engine,parents,path[i-1][receiver],path[i][receiver],site)
            copies.append({"add":i-1,"delete":i,"donor":donor,"receiver":receiver})
    direct_deletes=[z for z in range(len(steps)) if at[z]-at[z+1]]
    direct_copies=[z for z in range(1,len(steps)) if len(at[z-1])==len(at[z+1])==1 and
                   at[z-1]!=at[z+1] and at[z]==at[z-1]|at[z+1]]
    assert direct_deletes==[e["delete"] for e in delete_rows]
    assert direct_copies==[e["delete"] for e in copies]
    return {"case":index,"site":site,"steps":len(steps),"deletions":delete_rows,"copy_then_release":copies}

def main():
    fixed.pins()
    raw = (chain.DEMOS/chain.ARCHIVE).read_bytes()
    assert fixed.blob(raw) == chain.PINS[chain.ARCHIVE]
    archive = json.loads(gzip.decompress(raw))["corpus"]
    sys.path.insert(0,str(chain.DEMOS/chain.OLD))
    import producer, verifier
    replay = producer.produce(domain=())
    assert len(archive)==210 and replay["corpus"] == archive
    checked = verifier.verify(replay,domain=())
    assert not checked["construction_failures"] and checked["directed_cases"]==210
    engine = chain.module("v16.23-overlap-descent/engine.py","exact_source")
    records = [scan(i,row,verifier,engine) for i,row in enumerate(archive)]
    deletions=[e for r in records for e in r["deletions"]]
    copies=[e for r in records for e in r["copy_then_release"]]
    twins=[e for e in deletions if len(e["twins"])==1]
    counts={"calls":len(records),"edits":sum(r["steps"] for r in records),
            "designated_leaf_deletions":len(deletions),"unique_twin":len(twins),
            "unique_twin_later_gain":sum(e["gain"] is not None for e in twins),
            "protected_twin_gains":sum(e.get("protected",False) for e in twins),
            "unique_holder_copy_then_release":len(copies),
            "calls_with_copy_then_release":sum(bool(r["copy_then_release"]) for r in records)}
    print(json.dumps({"counts":counts,"archive_blob":chain.PINS[chain.ARCHIVE],"records":records},sort_keys=True,indent=2))

if __name__=="__main__":
    main()
