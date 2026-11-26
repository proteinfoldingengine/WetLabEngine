"""Explore the frozen marked-branch archive; no historical producer rerun."""
import json
from pathlib import Path
from hashlib import sha256
import sys
from hashlib import sha1
from importlib.util import spec_from_file_location, module_from_spec

def load(name, path, blob):
    data=path.read_bytes()
    assert sha1(b"blob "+str(len(data)).encode()+b"\0"+data).hexdigest()==blob
    spec=spec_from_file_location(name,path)
    mod=module_from_spec(spec);sys.modules[name]=mod
    spec.loader.exec_module(mod)
    return mod

demos=Path(sys.argv[2])/'ResearchHistory/UQCF-GEM/demos'
p1=load("p1",demos/'v16.23-overlap-descent/engine.py',"b18f52109ccff9c7dc77542d3b8f3e5d5989102a")
geom=load("geom",demos/'v15.40-global-balance-geometry-specificity/response_geometry.py',"9128c24b695c1b539ac60dc93aeaf0bd4795c57b")
construct_response_geometry,metric_passes=geom.construct_response_geometry,geom.metric_passes

def tree(names):
    parent = {'P':'Pin','Q':'Pin','X1':'P','X2':'P','A':'P','Y1':'Q','Y2':'Q','B':'Q','b1':'B','b2':'B'}
    return tuple(names.index(parent[v]) if v!='Pin' else -1 for v in names)

def totals(names, bit):
    fixed = {'Pin':80,'P':24,'Q':28,'A':2,'B':6,'b1':2,'b2':2}
    return tuple(fixed[v] if v in fixed else (1+7*bit if v.startswith('X') else 8-7*bit) for v in names)

def local(p, view, subtotal):
    full = tuple(range(len(p))); y = tuple(i for i in full if view>>i&1)
    x = tuple(subtotal[i]-sum(subtotal[j] for j,t in enumerate(p) if t==i) for i in full)
    assert min(x)>0
    g = p1.push(p,full,y,x)
    # The signed root-compensated Laplacian response slope is the subtree sum.
    # Use the archived cut representation (one axis per edge), not an assumed temporal law.
    cut = tuple(sum(a for v,a in zip(y,g) if i in p1.ancestors(p,v)) for i in full[1:])
    return y,g,cut

def calc(p,r,c,subtotal):
    j=r&c
    Y,Z,J=(local(p,v,subtotal) for v in (r,c,j))
    assert p1.push(p,Y[0],J[0],Y[1])==p1.push(p,Z[0],J[0],Z[1])==J[1]
    d=(Y[2],Z[2],J[2])
    result=construct_response_geometry((0,1,2),d,d)
    assert metric_passes(result)
    work=tuple(int(result.work[a][b]) for a,b in ((0,1),(0,2),(1,2)))
    assert work==tuple(sum(x*x for i,x in enumerate(subtotal) if (v^w)>>i&1) for v,w in ((r,c),(r,j),(c,j)))
    return work,tuple(sorted(tuple(sorted(e)) for e in result.neighbors)),Y[:2]

def main(path):
    raw=Path(path).read_bytes()
    assert sha256(raw).hexdigest()=='319c43442aee53b9da4e94bc2005841bcaba39629318d285b2b4f9d11838f515'
    rows=[]
    for row in json.loads(raw):
        names=row['order']; p=tree(names); r=row['receiver']; c=1-r
        path=[entry[0] for entry in row['path']]
        if len(path)==1:
            rows.append(None);continue
        for k,(old,mid) in enumerate(zip(path,path[1:])):
            d=old[r]^mid[r]
            if not d or d&(d-1) or not mid[r]&d or names[d.bit_length()-1][0] not in 'XY':continue
            leaf=d.bit_length()-1
            post=path[k+2]
            assert old[c]==mid[c] and post[c]==mid[c]^d and post[r]==mid[r]
            # Sort worlds by the grade of the identical handoff leaf in the two records.
            worlds=sorted((totals(names,i) for i in range(2)),key=lambda t:t[leaf])
            a,b=[tuple(calc(p,cut[r],cut[c],t) for cut in (path[0],old,mid,post)) for t in worlds]
            assert a[0]==b[0] and a[1][2]==b[1][2]
            assert a[2][2]==a[3][2] and b[2][2]==b[3][2] and a[3][2]!=b[3][2]
            # The no-additional-comparator control actually invokes the original operator.
            for z in worlds:
                d2=tuple(local(p,post[j],z)[2] for j in (r,c))
                assert construct_response_geometry((0,1),d2,d2).neighbors=={frozenset((0,1))}
            rows.append([k+1, names[leaf][0], [x[:2] for x in a], [x[:2] for x in b]])
            break
        else:raise AssertionError('nonidle run lacks handoff')
    print(json.dumps(rows,separators=(',',':')))
if __name__=='__main__':
    import sys
    main(sys.argv[1])
