"""Check the frozen row lemmas using every legal raw same-editor pair, in batches."""
from collections import Counter
from hashlib import sha256
import json
from pathlib import Path
import sys
import numpy as np
import check_geometry_repair as f

def run(witness):
    assert sha256(Path(f.__file__).read_bytes()).hexdigest() == "4d9c4a2c9392acf02fb62fd07dadb996ecedfcb03c1a2aa95885e5777e195cfe"
    features,_ = f.fixture()
    n=len(f.LABELS)
    rows=list(map(set,f.initial_state(features)))
    rows[f.A].remove(f.T)
    total=[x[1] for x in features]
    for v in reversed(range(1,len(features))):
        total[features[v][0]]+=total[v]
    square=np.square(total)
    work=np.array(f.work_for(rows,square))
    held=np.array([[v in row for row in rows] for v in range(len(total))])
    change=square[:,None]*np.where(held,1,-1)
    grid=f.grid()
    D,E=grid[f.A],grid[f.B]
    Dlist=sorted(D)
    captures=[]
    single_exceptions=[]
    nonunit=None
    counts=[]
    for i,row in enumerate(rows):
        if i==f.B:
            continue
        blocked={features[v][0] for v in row}
        legal=np.array(sorted(v for v in row if v>0 and v not in blocked and held[v].sum()>=2))
        assert all(features[v][0]==0 for v in legal)
        # Two distinct deletable raw features are independent root leaves; deleting one
        # cannot affect the other's root, local children, members, or union guard.
        other=sorted(set(range(n))-{i})
        ties=work[i][None,:]+change[legal]==f.MU
        for index in np.flatnonzero(ties[:,other].any(axis=1)):
            neighbors=[k for k in other if ties[index,k]]
            single_exceptions.append([i,int(legal[index]),neighbors])
        coverage=(E & grid[i]) | ({i} if i in E else set())
        if i!=f.A:
            assert len(coverage)<=2
            if len(coverage)==2:
                assert i in {f.offset(f.B,dx,dy) for dx in (-1,1) for dy in (-1,1)}
        if i in E and nonunit is None:
            for j in Dlist:
                high=next((int(v) for v in legal if v>=6 and not held[v,j] and square[v]>1),None)
                second=next((int(v) for v in legal if v>=6 and v!=high and not held[v,j]),None)
                if high is None or second is None:
                    continue
                def direct(vs):
                    state=[r.copy() for r in rows]
                    state[i].difference_update(vs)
                    return int(sum(square[v] for v in state[i]^state[j]))
                w=int(work[i,j])
                mixed=direct([high,f.ULEAF])
                both=direct([high,second])
                assert mixed==w-int(square[high])-4 and both==w-int(square[high])-int(square[second])
                nonunit={"editor":i,"other":j,"work_before":w,"high_feature":high,
                         "high_square":int(square[high]),"second_feature":second,
                         "second_square":int(square[second]),"mixed_after":mixed,"substrates_after":both}
                break
        pair_count=0
        for start in range(0,len(legal),32):
            left=legal[start:start+32]
            pair=left[:,None]<legal
            pair_count+=int(pair.sum())
            gains=np.zeros(pair.shape,dtype=np.int8)
            for k in Dlist:
                if k!=i and work[i,k]>f.MU:
                    gains+=(work[i,k]+change[left,k,None]+change[legal,k]==f.MU)
            if i==f.A:
                assert not np.any(pair & (gains>0))
            elif i not in E:
                assert not np.any(pair & (gains>2))
                if len(coverage)==2:
                    x,y=np.nonzero(pair & (gains==2))
                    if len(x):
                        vals=work[i,other]+change[np.ix_(left[x],other)]+change[np.ix_(legal[y],other)]
                        assert np.all(np.count_nonzero(vals==f.MU,axis=1)<=2)
            else:
                x,y=np.nonzero(pair & (gains==4))
                if len(x):
                    normals=sorted(grid[i]-{f.A,f.B})
                    vals=work[i,normals]+change[np.ix_(left[x],normals)]+change[np.ix_(legal[y],normals)]
                    assert np.all(np.min(vals,axis=1)<f.MU)
                    captures.extend([i,int(left[a]),int(legal[b])] for a,b in zip(x,y))
        assert pair_count==len(legal)*(len(legal)-1)//2
        counts.append([i,len(legal),pair_count])
    assert single_exceptions==[[i,f.T,[f.A,f.B]] for i in Dlist]
    assert nonunit is not None and nonunit["mixed_after"]<nonunit["work_before"]-5
    assert nonunit["substrates_after"]<nonunit["work_before"]-2
    edge=next((i,k) for i in sorted(E) for k in sorted(grid[i]-{f.A,f.B}) if work[i,k]==f.MU)
    witness_counts=Counter(i for i,v in witness)
    assert len(witness)==100 and all(total[v]==1 for i,v in witness)
    assert Counter(witness_counts.values())=={4:19,6:4}
    assert set(witness_counts).isdisjoint({f.A,f.B})
    return {"fixture_sha256":sha256(Path(f.__file__).read_bytes()).hexdigest(),"single_exceptions":single_exceptions,
            "raw_domain_by_actor":counts,"total_unordered_pairs":sum(r[2] for r in counts),
            "E_reaches_four_D_with_subminimum_neighbor":captures,"ordinary_min_edge_at_E":[*edge,int(work[edge])],
            "nonunit_counterexample":nonunit,"witness_counts":dict(sorted(witness_counts.items())),"outcome":"PASS"}

if __name__=="__main__":
    witness=json.loads(Path(sys.argv[1]).read_bytes())
    print(json.dumps(run(witness),indent=2,sort_keys=True))
