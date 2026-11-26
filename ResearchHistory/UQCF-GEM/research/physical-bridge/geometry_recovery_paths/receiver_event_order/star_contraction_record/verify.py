"""Cross-check all triple failures and index-order witnesses using coordinate sets."""
from collections import Counter
from itertools import product
import json
from pathlib import Path

here=Path(__file__).resolve().parent
receipt=json.loads((here/"orbit.json").read_bytes())
points={(0,0),(0,1),(0,2),(0,9),(0,10),(1,0),(1,1),(1,10),(2,0),(2,8),
        (3,7),(3,9),(4,8),(7,3),(7,8),(8,2),(8,4),(8,7),(8,9),(9,0),(9,3),
        (9,8),(10,0),(10,1),(10,10)}
def address(x,y):
    return x%11 + 11*(y%11)
images=[]
for swap in (False,True):
    oriented={(y,x) if swap else (x,y) for x,y in points}
    for sx,sy in product((-1,1),repeat=2):
        for x,y in product(range(11),repeat=2):
            images.append(frozenset(address(x+sx*i,y+sy*j) for i,j in oriented))
charts=range(121)
row=[{i for i,s in enumerate(images,1) if c in s} for c in charts]
hist=Counter()
interleaved=Counter()
pairs=Counter(images)
assert len(pairs)==484 and set(pairs.values())=={2}
for c in receipt["candidates"]:
    b=c["b"]
    common=row[0]&row[b]
    cnt={i:len((row[0]-row[b])&row[i]) for i in charts if i not in (0,b)}
    hist.update(cnt.values())
    failed=[i for i in cnt if not cnt[i]]
    possible=set.union(row[0],row[b],*(row[i] for i in failed))
    assert failed==c["excluded"] and 968-len(possible)==c["missing"]
    early,u,late=c["example_one_based"]
    assert {early,u,late}<=common and early<u<late and images[early-1]==images[late-1]
    twins=0
    for mask in {images[i-1] for i in common}:
        left,right=sorted(i for i in common if images[i-1]==mask)
        twins+=any(left<j<right for j in common)
    assert twins==c["interleaved_twins"]
    interleaved[twins]+=1
assert sorted(hist.items())==list(map(tuple,receipt["triples"]))
assert [c["b"] for c in receipt["candidates"]]==list(charts)[1:]
assert min(len(row[0]&r) for r in row[1:])==receipt["min_pair_overlap"]==16
assert sum(map(len,row))-1-len(images)==receipt["edits_to_contraction"]==23231
print(json.dumps(dict(unordered_masks=len(pairs),excluded_triples=hist[0],receivers=120,
                      min_leaves_uncovered=min(c["missing"] for c in receipt["candidates"]),
                      interleaved_twin_histogram=sorted(interleaved.items())),sort_keys=True))
