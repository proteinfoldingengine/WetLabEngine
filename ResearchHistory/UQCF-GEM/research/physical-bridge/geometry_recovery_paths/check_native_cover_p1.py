"""Measure exact P1 root gains on the two typed chart paths of the strict successor."""
import inspect
import json
import os
from pathlib import Path
import sys
from hashlib import sha256

from check_native_cover_increment import HISTORICAL_CUT, digest
from check_receiver_command import FIXTURE, PINS, hash_blob


def run(sources, previous, cover):
    os.chdir(sources)
    assert hash_blob(FIXTURE.read_bytes())==PINS[FIXTURE]
    assert hash_blob(HISTORICAL_CUT.read_bytes())=="fc4a77fc4f01fce33fdb562423eca274cfb0c648"
    sys.path.insert(0,str(FIXTURE.parent.resolve()))
    import check_geometry_repair as fixture
    import importlib.util
    spec=importlib.util.spec_from_file_location("profile_cut",HISTORICAL_CUT)
    producer=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(producer)
    modules=fixture.modules()
    lineage, atom=modules["lineage"], modules["atom"]
    features,_=fixture.fixture()
    parents,base,_=map(tuple,zip(*features))
    keys=[()]
    for v in range(1,len(parents)):
        keys.append(keys[parents[v]]+(v,))
    fine=lineage.Carrier(atom.GENESIS,tuple(keys))
    def carrier(row):
        return lineage.Carrier(fine.genesis,tuple(keys[v] for v in row))
    def at(values, space, address):
        return int(values[space.keys.index(keys[address])])
    state=fixture.initial_state(features)
    for step in previous["preparation"]+cover["extra"]:
        state=producer.cut(parents,state,step)
    reference=cover["states"]["reinforced"]
    assert digest(state)==reference["common_rows_sha256"]
    args=list(inspect.signature(atom.atomic).parameters)
    assert args==["raw","before","index","leaf"]
    out=dict(genesis=fine.genesis, parents_sha256=digest(parents),
             common_rows_sha256=digest(state), atom_parameters=args, arms={})
    a,b=fixture.A,fixture.B
    for x,y in ((718,719),(719,718)):
        source=producer.cut(parents,state,(a,x))
        result=producer.cut(parents,source,(b,y))
        tested=next(event for event in cover["historical_checks"] if event["label"]=="reinforced_record_"+str(x))
        assert (digest(source),digest(result))==(tested["before"],tested["after"])
        assert (tested["index"],tested["leaf"],tested["trigger"])==(b,y,True)
        a0,a1,b0,b1=carrier(state[a]),carrier(source[a]),carrier(source[b]),carrier(result[b])
        assert carrier(state[b]).identity==b0.identity and b0.identity!=a1.identity
        pa,pb=lineage.Pruning(a0,a1),lineage.Pruning(b0,b1)
        try:
            pa.then(pb)
        except ValueError as exc:
            mismatch=str(exc)
        else:
            raise AssertionError("The local P1 maps unexpectedly compose")
        assert mismatch=="incompatible composition endpoints"
        arm=dict(typed_cross_composition=mismatch, source_event=[a,x], receiver_event=[b,y],
                 historical_before_sha256=tested["before"], historical_after_sha256=tested["after"], variations={})
        for label,vary in (("archived",None),("source_plus_one",x),("complement_plus_one",y)):
            g=list(base)
            if vary is not None:
                g[vary]+=1
            maps=lineage.Pruning(fine,a0),lineage.Pruning(fine,b0)
            va,vb=(m.aggregate(g) for m in maps)
            va1,vb1=pa.aggregate(va),pb.aggregate(vb)
            assert va1==maps[0].then(pa).aggregate(g) and vb1==maps[1].then(pb).aggregate(g)
            roots_a=[at(va,a0,0),at(va1,a1,0)]
            roots_b=[at(vb,b0,0),at(vb1,b1,0)]
            local_x=[at(vb,b0,x),at(vb1,b1,x)]
            gains=[roots_a[1]-roots_a[0],roots_b[1]-roots_b[0]]
            assert gains==[g[x],g[y]] and local_x==[g[x],g[x]]
            assert keys[y] in b0.keys and keys[y] not in b1.keys
            arm["variations"][label]=dict(root_a=roots_a, root_b=roots_b, gains=gains,
                                         retained_x_at_b=local_x, fine_weights=[g[x],g[y]])
        out["arms"][str(x)]=arm
    return out


if __name__=="__main__":
    if not __debug__:
        raise RuntimeError("Use enabled assertions")
    sources, old, cover, target=[Path(arg).resolve() for arg in sys.argv[1:]]
    assert sha256(old.read_bytes()).hexdigest()=="afa2a993f5a4fabc410df621b9377659fe6d98a1a3993a29990ea25a0abcf19b"
    evidence=run(sources,json.loads(old.read_bytes()),json.loads(cover.read_bytes()))
    target.write_text(json.dumps(evidence,indent=2,sort_keys=True)+"\n")
    print(json.dumps({x:{k:v["gains"] for k,v in a["variations"].items()} for x,a in evidence["arms"].items()}))
