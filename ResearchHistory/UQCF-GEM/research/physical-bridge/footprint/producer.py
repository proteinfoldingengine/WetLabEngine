"""Bit-subset producer; no hidden-state data used by the core criterion."""
import functools,itertools,json,pathlib,sys

@functools.lru_cache(None)
def tau(s):
    if not s: return 0
    if 0 in s: return 99
    palette=0
    for x in s: palette|=x
    return min(h.bit_count() for h in range(palette+1) if h&palette==h and all(h&x for x in s))

def conditions(c,d,p):
    footprints=[sum(1<<i for i,r in enumerate(c) if r>>y&1) for y in range(p)]
    cur=[sum(1<<i for i,r in enumerate(d) if r>>x&1) for x in range(p)]
    return [all(x.bit_count()>=y.bit_count() for x,y in zip(d,c)),tau(tuple(d))<=4,
            all(any(j&~k==0 for k in footprints) for j in cur)]

def full(d,q,p): return tuple(x|((1<<p) if q>>i&1 else 0) for i,x in enumerate(d))

def masks(c,p): return [q for q in range(1<<len(c)) if 3<=tau(full(c,q,p))<=4]

def admissible(c,d,q,p):
    s=full(d,q,p)
    return all(x.bit_count()>=y.bit_count() for x,y in zip(s,c)) and 3<=tau(s)<=4

def fixture(name,c,p,single=False):
    qs=masks(c,p); rows=[]
    alphabet=[0]+[1<<x for x in range(p)] if single else range(1<<p)
    for d in itertools.product(alphabet,repeat=len(c)):
        code=sum(x<<(p*i) for i,x in enumerate(d)); cond=conditions(c,d,p)
        bad=[q for q in qs if not admissible(c,d,q,p)]
        safe=not bad
        assert safe==all(cond),(name,d,cond,bad)
        rows.append([code,cond,safe,bad])
    rows.sort(key=lambda x:x[0])
    return dict(name=name,core=list(c),palette=p,floors=[r.bit_count() for r in c],source_masks=qs,rows=rows)

def application():
    c=(1,1,1,2,4,24); p=6; qs=masks(c,p); d=list(c); path=[list(d)]
    actions=[(5,5),(5,3)]+[(i,3) for i in range(3)]+[(i,0) for i in range(3)]+[(5,0),(5,5)]
    for i,x in actions:
        d[i]^=1<<x; path.append(list(d)); assert all(conditions(c,d,p))
    neighbors=[]
    for i in range(6):
        for x in range(p):
            e=list(c); e[i]^=1<<x
            if all(conditions(c,e,p)): neighbors.append([i,x])
    ts=[[tau(full(s,q,p)) for s in path] for q in qs]
    assert all(3<=t<=4 for row in ts for t in row)
    cross=list(c); cross[0]|=8
    premature=list(path[3]); premature[0]&=~1
    return dict(core=list(c),source_masks=qs,path=path,path_taus=ts,
                cross_role_taus=[tau(full(c,30,p)),tau(full(cross,30,p))],
                premature_deletion_tau=tau(tuple(premature)),
                no_spare_safe_neighbors=[a for a in neighbors if a[1]<5],spare_safe_neighbors=neighbors)

def produce():
    fs=[fixture('three-with-spare',(1,2,4),4),fixture('repeated-role',(1,1,2,4),3),
        fixture('overlapping-role',(3,1,2,4),3),fixture('tau4-singleton-candidates',(1,2,4,8),4,True)]
    c=(1,1,2,2,4);d=(1,2,4,8,16)
    return dict(schema='universal-footprint-v1',fixtures=fs,application=application(),
                upper_control=dict(core=list(c),candidate=list(d),candidate_tau=tau(d),conditions=conditions(c,d,5)))

def counts(d):
    return {'candidates':sum(len(f['rows']) for f in d['fixtures']),
            'safe_by_fixture':{f['name']:sum(r[2] for r in f['rows']) for f in d['fixtures']},
            'source_masks_by_fixture':{f['name']:len(f['source_masks']) for f in d['fixtures']},
            'exchange_sources':len(d['application']['source_masks']),'exchange_slices':len(d['application']['path'])}

if __name__=='__main__':
    d=produce(); pathlib.Path(sys.argv[1]).write_text(json.dumps(d,sort_keys=True,separators=(',',':'))+'\n'); print(json.dumps(counts(d),sort_keys=True))
