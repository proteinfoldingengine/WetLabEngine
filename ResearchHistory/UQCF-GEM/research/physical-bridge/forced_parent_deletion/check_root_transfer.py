"""Exhaust a proposed order-free transfer rule on archived fork graph states."""
from functools import cache
from itertools import permutations
import gzip
import hashlib
import importlib.util
import json
from pathlib import Path
from zipfile import ZipFile
import sys

U = Path("ResearchHistory/UQCF-GEM")
FORK = U / "demos/v16.45-binary-fork-unit-barrier"
ATOM = U / "demos/v16.26-consistency-increment-law"
FCV = U / "foundational-closure-verification"
ARCHIVE = FORK / "evidence/science/scientific/CERTIFICATE.json.gz"
P = (-1,0,1,1,0,4,4)
BRANCH = {1:(1,2,3),4:(4,5,6)}
PREP = (31,15,113)
ROLES = (0,1,2)
KEYS = ((),(0,),(0,0),(0,1),(1,),(1,0),(1,1))


def module(name,path,expected):
    data=path.read_bytes()
    assert hashlib.sha1(f"blob {len(data)}\0".encode()+data).hexdigest()==expected
    spec=importlib.util.spec_from_file_location(name,path)
    m=importlib.util.module_from_spec(spec)
    sys.modules[name]=m
    spec.loader.exec_module(m)
    return m


def root_cover(state):
    return 1 if any(mask & 18 == 18 for mask in state) else 2


def width(state):
    return sum((mask & 18).bit_count() for mask in state)


def transfer(state,child,donor,recipient):
    current=list(state)
    path=[state]
    for vertex in BRANCH[child][1:]:
        if current[donor] & (1<<vertex) and not current[recipient] & (1<<vertex):
            current[recipient] |= 1<<vertex
            path.append(tuple(current))
    for vertex in reversed(BRANCH[child]):
        if current[donor] & (1<<vertex):
            current[donor] ^= 1<<vertex
            path.append(tuple(current))
    return path


class Graph:
    def __init__(self,entry):
        self.states=list(map(tuple,entry["graph"]["states"]))
        self.index={s:i for i,s in enumerate(self.states)}
        self.edges=entry["graph"]["forward_moves"]
        self.moves=0
        self.steps=0

    def validate(self,path):
        for a,b in zip(path,path[1:]):
            (i,bit),=((i,x^y) for i,(x,y) in enumerate(zip(a,b)) if x!=y)
            assert bit.bit_count()==1 and a in self.index and b in self.index
            smaller=a if a[i]<b[i] else b
            assert self.edges[self.index[smaller]] >> (6*i+bit.bit_length()-2) & 1

    def choices(self,state):
        for child in BRANCH:
            holders=[i for i,x in enumerate(state) if x & (1<<child)]
            for donor,recipient in permutations(holders,2):
                trial=list(state)
                trial[donor] &= ~(1<<child)
                if root_cover(trial)!=root_cover(state):
                    continue
                path=transfer(state,child,donor,recipient)
                assert width(path[-1])==width(state)-1
                assert all(root_cover(s)==root_cover(state) for s in path)
                self.validate(path)
                yield path

    @cache
    def ends(self,state):
        paths=list(self.choices(state))
        assert bool(paths)==(width(state)>2)
        self.moves+=len(paths)
        self.steps+=sum(len(path)-1 for path in paths)
        if not paths:
            return frozenset([state])
        return frozenset().union(*(self.ends(path[-1]) for path in paths))


def run(out):
    atom=module("original_atomic",ATOM/"engine.py","c10ac57f988a439144e21898bd2b33ece0838a9b")
    verify=module("original_verify",ATOM/"verify.py","91cd1e507e955683e744fbdbb0745cac19d66cb3")
    lin=module("original_lineage",FCV/"lineage.py","e95e3e978779164dd91f09b80e3389247e6320c2")
    raw=ARCHIVE.read_bytes()
    assert hashlib.sha1(f"blob {len(raw)}\0".encode()+raw).hexdigest()=="3ed66277766b9836804ed9ec222d9728009b2b67"
    entries=json.loads(gzip.decompress(raw))["entries"]
    graphs={e["k"]:Graph(e) for e in entries if e["b"]==e["c"]==2}
    counts={}
    for k,graph in graphs.items():
        for state in graph.states:
            for end in graph.ends(state):
                assert root_cover(end)==root_cover(state)
                for source in range(k):
                    owners=[]
                    for v in BRANCH:
                        matches=[i for i in range(k) if i!=source and end[i] & (1<<v)]
                        assert len(matches)<=1
                        owners.append(matches[0] if matches else source)
                    assert len(set(owners))==root_cover(state)
        counts[k]={"states":len(graph.states),"transfers":graph.moves,"atomic_graph_steps":graph.steps}

    graph=graphs[3]
    views=[tuple(j for j in range(7) if mask>>j&1) for mask in PREP]
    sys.path.insert(0,str(FORK.resolve()))
    writer=module("fork_writer",FORK/"producer.py","e73a02ee05e11f0c6b041b783ba6ff9738271073")
    replay_path=U/"research/physical-bridge/forced_parent_deletion/fork_profile_write_evidence/fork-profile-write-replay.zip"
    with ZipFile(replay_path) as z:
        expected=json.loads(z.read("fork_certificate.json"))["cases"]
    baseline=[atom.tau_at(P,views,v) for v in range(7)]
    wired={}
    sources={}
    endpoints={}
    for name,v in (("junction",4),("leaf",2)):
        d=atom.atomic(P,views,0,v)
        verify.verify_atomic(d)
        start=tuple(sum(1<<j for j in view) for view in d["after"])
        q=baseline.copy()
        assert q[d["parent"]]==d["tau_before"]
        q[d["parent"]]=d["tau_after"]
        original_key="left_leaf" if name=="leaf" else name
        trajectory=writer.normalize(start,2,2,3,q)
        assert trajectory==expected[original_key]["masks"]
        wired[name]={"source_patch":[d["parent"],d["tau_after"]],"derived_profile":q,
                     "original_writer_endpoint":trajectory[-1]}
        sources[name]=start
        endpoints[name]=sorted(graph.ends(start))
    assert endpoints=={"junction":[(1,15,113),(15,1,113)],"leaf":[(127,1,1)]}
    for perm in permutations(ROLES):
        for name,s in sources.items():
            assert graph.ends(tuple(s[i] for i in perm))=={tuple(e[i] for i in perm) for e in endpoints[name]}

    # Removing the root guard gives a common legal terminal even with the same source events.
    j=transfer(sources["junction"],1,0,1)
    first=transfer(sources["leaf"],4,0,2)
    l=first+transfer(first[-1],1,0,1)[1:]
    graph.validate(j)
    graph.validate(l)
    assert j[-1]==l[-1]==(1,15,113)
    assert j[0][2]==l[0][2]==113 and all(s[2]==113 for s in j+l)
    rawviews=[tuple(i for i in range(7) if m>>i&1) for m in first[0]]
    veto=atom.atomic(P,rawviews,0,4)
    verify.verify_atomic(veto)
    assert veto["trigger"] and (veto["tau_before"],veto["tau_after"])==(1,2)

    full=lin.Carrier("fork",KEYS)
    def root_row(mask):
        view=lin.Carrier("fork",tuple(key for i,key in enumerate(KEYS) if mask>>i&1))
        projection=lin.Pruning(full,view)
        return tuple(int(projection.aggregate(tuple(int(i==v) for i in range(7)))[0]) for v in range(7))
    covector=tuple(a-b for a,b in zip(root_row(1),root_row(113)))
    assert covector==(0,0,0,0,1,1,1)
    cert={"certificate_to_original_writer":wired,"sources":sources,"terminal_sets":endpoints,"unguarded_control":[j,l],
          "original_veto_certificate":veto,"counts":counts,"C_root_covector":covector}
    out.mkdir(parents=True,exist_ok=True)
    data=(json.dumps(cert,indent=2,sort_keys=True)+"\n").encode()
    (out/"transfer_certificate.json").write_bytes(data)
    return {**counts,"terminal_sets":endpoints,"C_root_covector":covector,
            "certificate_sha256":hashlib.sha256(data).hexdigest()}


if __name__=="__main__":
    result=run(Path(sys.argv[1]))
    print(json.dumps({str(k):v for k,v in result.items()},indent=2,sort_keys=True))
