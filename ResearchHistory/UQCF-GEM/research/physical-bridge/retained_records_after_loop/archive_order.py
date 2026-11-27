"""Identify the original square and test the source's position without changing any remote word."""
from collections import Counter
from copy import deepcopy
from hashlib import sha256
from itertools import permutations
import json
import lzma
from pathlib import Path
import sys

from replay import STAGE, bits, module, pin, view


def compact(obj):
    return json.dumps(obj, sort_keys=True, separators=(",",":")).encode()


def run(demos):
    native = module(demos / STAGE / "engine.py", "c10ac57f988a439144e21898bd2b33ece0838a9b")
    validate = module(demos / STAGE / "verify.py", "91cd1e507e955683e744fbdbb0745cac19d66cb3")
    p1 = module(demos / "v16.23-overlap-descent/engine.py", "b18f52109ccff9c7dc77542d3b8f3e5d5989102a")
    stage = demos / "v16.29-local-profile-closure"
    original = module(stage/"producer.py","fc4a77fc4f01fce33fdb562423eca274cfb0c648")
    auditor = module(stage/"verifier.py","a38f82240f8533792314b5fc7d1b83f5a6cba00a")
    p = (-1,0,0,0,0)
    start = (7,15,21,27)  # A,C,D,B
    finish = (5,1,1,27)
    def step(s,event):
        d = native.atomic(p,tuple(map(view,s)),*event)
        assert validate.verify_atomic(d) == (d["delta_h"],d["trigger"])
        return bits(d["after"]),d
    source = (0,1)
    remote = ((1,1),(1,2),(2,2),(1,3),(2,4))
    candidates = sorted(permutations((source,)+remote))
    positions = Counter()
    word_digest = sha256()
    def local(mask):
        return tuple(map(int,p1.push(p,tuple(range(5)),view(mask),(1,)*5)))
    def trace(order):
        s = start
        history = {i:[(view(s[i]),local(s[i]))] for i in (1,2,3)}
        for event in order:
            s,d = step(s,event)
            f = tuple(d[k] for k in ("tau_before","tau_after","h_before","h_after","trigger","delta_h"))
            assert f == (2,2,2,2,False,0)
            i,_ = event
            if i:
                history[i].append((view(s[i]),local(s[i])))
        return s,history
    for word in candidates:
        s,_ = trace(word)
        assert s == finish
        positions[word.index(source)+1]+=1
        word_digest.update(compact([word,s])+b"\n")
    sf,rf=trace((source,)+remote)
    sl,rl=trace(remote+(source,))
    no,r0=trace(remote)
    assert sf == sl == finish and no[1:] == finish[1:] and no[0]==start[0]
    assert rf==rl==r0 and rf[1][-1][1]==rf[2][-1][1]==(5,)
    try:
        step(no,(0,2))
    except ValueError as err:
        assert str(err)=="same union"
    else:
        raise AssertionError("The other release should destroy the last copy")
    before,_ = trace((source,)+remote[:3])
    assert before == (5,9,17,27)
    events=remote[3:]
    cert=original.certify(p,tuple(map(view,before)),events)
    assert auditor.verify_case(cert)["diamonds"]==1
    assert tuple(bits(s) for s in cert["states"]) == (before,step(before,events[0])[0],step(before,events[1])[0],finish)
    for a,b in (events, events[::-1]):
        assert step(step(before,a)[0],b)[0] == finish
    corrupted=deepcopy(cert)
    corrupted["states"][3][1]=[0,3]
    try:
        auditor.verify_case(corrupted)
    except ValueError as exc:
        rejected=str(exc)
    else:
        raise AssertionError("Original verifier accepted a substituted retained row")
    raw=lzma.decompress(pin(stage/"evidence/FULL_CERTIFICATES.json.xz","45cefa46e2d0f50ecde74bab9bc3d498edc69752"))
    manifest=json.loads(pin(stage/"evidence/PRODUCTION.json","220e7644381df8e9f213a36a8f401bd18634cc69"))
    assert len(raw)==manifest["raw_bytes"] and sha256(raw).hexdigest()==manifest["raw_sha256"]
    end_token=b'],"code":'+compact(original.code(p))+b',"parents":'+compact(p)+b',"variant":"original"}'
    extension=raw.index(b'"extension":[')
    stop=raw.index(end_token,extension)
    assert b',"parent":[' not in raw[extension:stop]
    group_start=raw.rindex(b'{"cases":[',extension,stop)
    group=json.loads(raw[group_start:stop+len(end_token)])
    encoded=compact(cert)
    assert group["cases"].count(cert)==1 and raw.count(encoded,group_start,stop)==1
    pos=raw.index(encoded,group_start,stop)
    return dict(archive=dict(group=group["code"],variant=group["variant"],ordinal_zero_based=group["cases"].index(cert),
                             byte_offset=pos,certificate_sha256=sha256(encoded).hexdigest(),
                             complete_certificate=cert,corrupt_row_rejected=rejected,raw_sha256=manifest["raw_sha256"]),
                orders=len(candidates),all_orders_digest=word_digest.hexdigest(),orders_by_source_position=positions,
                source_first=(source,)+remote,source_last=remote+(source,),local_histories=rf,
                without_source=no,common_final=finish,blocked_source_alternative=2)


if __name__=="__main__":
    print(json.dumps(run(Path(sys.argv[1])),sort_keys=True,indent=2))
