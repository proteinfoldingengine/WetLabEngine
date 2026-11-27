import gzip, hashlib, importlib.util, itertools, json, sys
from pathlib import Path
demo = Path(sys.argv[1])
v51 = demo / "v16.51-ternary-interface"
spec = importlib.util.spec_from_file_location("stock", v51/"producer.py")
p = importlib.util.module_from_spec(spec)
spec.loader.exec_module(p)
cert = v51/"evidence/reproduction/scientific/CERTIFICATE.json.gz"
assert hashlib.sha256(cert.read_bytes()).hexdigest() == "91aac71f6e786af4a3876ee9a7ec09d78b4bbe0906eb5461e08d9be1318b93f9"
case = json.loads(gzip.decompress(cert.read_bytes()))["cases"][58]
q, k, tree = [2,1,1,2], 3, p.TREES["T"]
assert case["spec"] == {"q": q, "k":k, "tree":"T", "mode":"compact", "permutation":"cyclic"}
prior = [15,385,753]
assert case["path"][6] == prior and case["path"][7] == [15,401,753]
kids = p.layout(tree)
def support(state, v):
    return {i for i,z in enumerate(state) if z >> v & 1}
def check(path, tolerance):
    prof=[]
    for state in path:
        sets=[support(state,v) for v in range(len(kids))]
        assert sets[0] == set(range(k)) and all(sets)
        assert all(sets[c] <= sets[v] for v,cs in enumerate(kids) for c in cs)
        h=[next(n for n in range(1,k+1) if any(all(sets[c]&set(subset) for c in cs)
                  for subset in itertools.combinations(range(k),n))) for cs in kids if cs]
        assert sum(abs(a-b) for a,b in zip(h,q)) <= tolerance
        prof.append(h)
    assert all(sum((a^b).bit_count() for a,b in zip(s,t)) == 1 for s,t in zip(path,path[1:]))
    return prof
expect = {
    "gain_1": ([15,401,753],None,13,1,[1,2],5,[15,497,641],1),
    "gain_0": ([31,385,753],None,19,0,[0,1],5,[127,385,641],0),
    "no_gain": (prior,None,14,2,[1,2],0,prior,0),
    "order_control": ([15,401,753],[2,1,0],21,2,[1,2],5,prior,0),
}
out = {}
for name,(state,order,length,anchor,pair,phase,after,overlap) in expect.items():
    x=state[:]
    trace=[]
    if order is None:
        path=p.normalize(x,tree,k,q,trace=trace)
    else:
        path=p.normalize(x,tree,k,q,order=order,trace=trace)
    assert x == state and path[0] == state
    a=next(e for e in trace if e["kind"]=="anchor")
    assert a["label"]==anchor and a["pair"]==pair
    c=next(e for e in trace if e["kind"]=="child_normalization" and e["child"]==4)
    assert c["end"]==phase and len(path)-1==length and path[phase]==after
    assert all(support(s,8)=={1} for s in path[:phase+1])
    assert len(support(path[phase],5)&support(path[phase],8))==overlap
    assert len(support(path[-1],5)&support(path[-1],8))==0
    assert path[-1]==([399,753,1] if order is None else [1,753,399])
    frozen=0 if name.startswith("gain") else 1
    profile=check(path,frozen)
    if name.startswith("gain"):
        assert sum((a^b).bit_count() for a,b in zip(prior,state)) == 1
        assert [next((i,(a^b).bit_length()-1,a<b) for i,(a,b) in enumerate(zip(s,t)) if a!=b)
                for s,t in zip(path[:phase],path[1:phase+1])] == [
                (anchor,5,True),(anchor,6,True),(2,5,False),(2,6,False),(2,4,False)]
        check([prior]+path,0)
    out[name]={"path":path,"profile":profile,"anchor":anchor,"phase":phase,"overlap":overlap}
print(json.dumps(out,indent=2,sort_keys=True))
