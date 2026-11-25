"""Realize the common numerical prefix and call the archived validator at its decisive next unit."""
from collections import Counter
from pathlib import Path
import sys
from free_receiver_io import ATOM,FIXTURE,P1,module,require,write_xz


def produce(root,out):
    original=module(root,FIXTURE,"threshold_fixture","3324c0b46e09120ae526338444a19070b692d049")
    atomic=module(root,ATOM,"threshold_atom","c10ac57f988a439144e21898bd2b33ece0838a9b").atomic
    push=module(root,P1,"threshold_p1","b18f52109ccff9c7dc77542d3b8f3e5d5989102a").push
    features,_=original.fixture()
    p,g,h=map(tuple,zip(*features))
    X=tuple(range(len(p)))
    output=[]
    for mode in ("original","balanced"):
        prepared=[set(r) for r in original.initial_state(features)]
        if mode=="balanced":
            for j in set(range(25))-{0,8,12,13}:
                prepared[j].remove(46)
                prepared[j].remove(718)
        for cut in (662,718):
            event=atomic(p,[sorted(row) for row in prepared],0,cut)
            views=[set(r) for r in event["after"]]
            outside=set.union(*(r for j,r in enumerate(views) if j!=12))
            eligible=sorted((views[12]&outside)-{0})
            quota=Counter(g[v] for v in eligible)
            prior_units=sum(g[v]==1 for v in views[12] if v)
            prefix=[v for v in eligible if g[v]==1 and v!=718]
            require(all(p[v]==0 and v not in p for v in views[12] if v),"chart is a fine-tip star")
            for v in prefix:
                require(v in views[12] and v in outside and g[v]==1,"legal common prefix")
                views[12].remove(v)
            native_before=[sorted(r) for r in views]
            before=int(push(p,X,tuple(native_before[12]),g)[0])
            remaining_units=sorted(v for v in views[12]&outside if v and g[v]==1)
            next_nonunit=next(v for v in eligible if g[v]>1)
            def attempt(v):
                try: end=atomic(p,native_before,12,v)
                except ValueError as e:
                    require(str(e)=="same union","unexpected rejection")
                    return dict(status="same union")
                local=tuple(end["after"][12])
                P=push(p,X,local,g)
                return dict(status="success",root=int(P[0]),nonroot_units=sum(x==1 for x in P[1:]),
                            receiver_count=len(local)-1)
            output.append(dict(mode=mode,cut=cut,quota=sorted(quota.items()),prior_units=prior_units,
                               prefix=prefix,root_after_prefix=before,remaining_units=remaining_units,
                               unit=attempt(718),nonunit_vertex=next_nonunit,nonunit=attempt(next_nonunit)))
    write_xz(out/"free_receiver_threshold.json.xz",output)
    for r in output:
        print(r["mode"],r["cut"],"quotas",r["quota"],"common prefix",len(r["prefix"]),"next",r["unit"])


if __name__=="__main__":
    produce(Path(sys.argv[1]),Path(sys.argv[2]))
