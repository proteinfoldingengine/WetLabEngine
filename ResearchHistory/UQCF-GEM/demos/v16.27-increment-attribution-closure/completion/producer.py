"""Complete v16.27 path producer. DFS, no path cap, no imported research engine."""
from collections import Counter
from functools import lru_cache
from itertools import combinations, product
from pathlib import Path
import hashlib
import json
import lzma

HERE=Path(__file__).resolve().parent
ORIGIN='v16.27-common-genesis'
SCHEMA='v16.27-completion-1'

def need(ok,message):
    if not ok:raise ValueError(message)

def validate(raw,before,after):
    need(isinstance(raw,(list,tuple)) and len(raw)>0,'empty parent carrier')
    p=tuple(raw);need(all(type(x) is int for x in p) and p[0]==-1,'integer root/parent identifiers')
    need(all(0<=x<len(p) for x in p[1:]),'parent outside carrier')
    for node in range(1,len(p)):
        seen=set()
        while node:
            need(node not in seen,'cyclic lineage');seen.add(node);node=p[node]
    def family(rawviews):
        need(isinstance(rawviews,(list,tuple)) and len(rawviews)>0,'empty indexed cover')
        out=[]
        for item in rawviews:
            need(isinstance(item,(list,tuple)) and len(item)>0,'empty view')
            y=tuple(item)
            need(all(type(v) is int and 0<=v<len(p) for v in y),'retained identifier')
            need(len(y)==len(set(y)) and 0 in y,'duplicate identity or missing root')
            need(all(v==0 or p[v] in y for v in y),'missing ancestor')
            out.append(y)
        return tuple(out)
    ys,zs=family(before),family(after)
    need(len(ys)==len(zs),'indexed endpoint mismatch')
    need(all(set(z)<=set(y) for y,z in zip(ys,zs)),'not componentwise retention')
    need(set().union(*map(set,ys))==set().union(*map(set,zs)),'same union required')
    return p,ys,zs

@lru_cache(None)
def profile(p,ys):
    U=set().union(*map(set,ys));out=[]
    for v in range(len(p)):
        kids={w for w in U if w and p[w]==v}
        if v not in U or not kids:out.append(0);continue
        for r in range(1,len(ys)+1):
            if any(kids<=set().union(*(set(ys[i]) for i in ids)) for ids in combinations(range(len(ys)),r)):
                out.append(r);break
    return tuple(out)

def height(p,ys):return max((1,)+profile(p,ys))

def trigger(p,ys,zs,parent):
    U=set().union(*map(set,ys));kids={w for w in U if w and p[w]==parent}
    old=profile(p,ys)[parent]
    minima=[ids for ids in combinations(range(len(ys)),old) if kids<=set().union(*(set(ys[i]) for i in ids))]
    return bool(minima) and all(not kids<=set().union(*(set(zs[i]) for i in ids)) for ids in minima)

def certify(raw,before,after):
    p,ys,zs=validate(raw,before,after)
    events=tuple((i,v) for i,y in enumerate(ys) for v in sorted(set(y)-set(zs[i])))
    paths=[]
    def dfs(cur,seq,hs,ps,ds,ts):
        if all(set(a)==set(b) for a,b in zip(cur,zs)):
            paths.append({'events':[list(e) for e in seq],'heights':hs[:],'profiles':[list(q) for q in ps],
                          'deltas':ds[:],'triggers':ts[:]});return
        for i,y in enumerate(cur):
            for v in sorted(set(y)-set(zs[i])):
                if v==0 or any(p[w]==v for w in y if w):continue
                nxt=list(cur);nxt[i]=tuple(w for w in y if w!=v);nxt=tuple(nxt)
                need(set().union(*map(set,nxt))==set().union(*map(set,cur)),'unexpected union loss')
                q=profile(p,nxt);h1=max((1,)+q)
                dfs(nxt,seq+[(i,v)],hs+[h1],ps+[q],ds+[h1-hs[-1]],ts+[trigger(p,cur,nxt,p[v])])
    q=profile(p,ys);dfs(ys,[],[max((1,)+q)],[q],[],[])
    need(paths,'no legal endpoint factorization')
    maps=[dict(zip(map(tuple,row['events']),row['deltas'])) for row in paths]
    changed=[list(e) for e in events if len({a[e] for a in maps})>1]
    return {'version':'16.27','schema':SCHEMA,'genesis':ORIGIN,'parents':list(p),
            'before':[list(y) for y in ys],'after':[list(z) for z in zs],
            'paths':paths,'dependent':bool(changed),'changed_events':changed}

def shape_code(p):
    def walk(v):return '('+''.join(sorted(walk(w) for w in range(1,len(p)) if p[w]==v))+')'
    return walk(0)

def shapes(bound):
    found={}
    for n in range(1,bound+1):
        for q in product(*(range(i) for i in range(1,n))):
            p=(-1,)+q;found.setdefault(shape_code(p),p)
    return [(c,found[c]) for c in sorted(found,key=lambda s:(len(s),s))]

def legal(p):
    out=[]
    for mask in range(1,1<<len(p),2):
        y=tuple(v for v in range(len(p)) if mask>>v&1)
        if all(v==0 or p[v] in y for v in y):out.append(y)
    return out

def endpoints(p):
    L=legal(p);full=set(range(len(p)))
    for count in range(1,min(4,len(L))+1):
        for ys in combinations(L,count):
            if set().union(*map(set,ys))!=full:continue
            pools=[[z for z in L if set(z)<=set(y)] for y in ys]
            for zs in product(*pools):
                if set().union(*map(set,zs))!=full:continue
                removed=sum(len(y)-len(z) for y,z in zip(ys,zs))
                if 2<=removed<=5:yield ys,zs

def counters(cases):
    return {'endpoints':len(cases),'multi_path':sum(len(c['paths'])>1 for c in cases),
            'dependent':sum(c['dependent'] for c in cases),'paths':sum(len(c['paths']) for c in cases)}

def produce(bound=4):
    need(type(bound) is int and 1<=bound<=4,'declared tree bound')
    instances=[];totals={'original':Counter(),'relabeled':Counter()}
    for code,p in shapes(bound):
        cases=[certify(p,a,b) for a,b in endpoints(p)]
        instances.append({'code':code,'variant':'original','parents':list(p),'cases':cases})
        totals['original'].update(counters(cases))
        perm=[0]+list(range(len(p)-1,0,-1));q=[-1]*len(p)
        for v in range(1,len(p)):q[perm[v]]=perm[p[v]]
        transformed=[]
        for case in cases:
            a=[[perm[v] for v in reversed(y)] for y in reversed(case['before'])]
            b=[[perm[v] for v in reversed(y)] for y in reversed(case['after'])]
            transformed.append(certify(q,a,b))
        instances.append({'code':code,'variant':'relabeled','parents':q,'cases':transformed})
        totals['relabeled'].update(counters(transformed))
    return {'version':'16.27','schema':SCHEMA,'genesis':ORIGIN,'tree_bound':bound,'view_bound':4,
            'removed_min':2,'removed_max':5,'instances':instances,
            'summary':{k:dict(v) for k,v in totals.items()}}

def legacy_witness(case):
    if not case['dependent']:return None
    a=case['paths'][0];am=dict(zip(map(tuple,a['events']),a['deltas']))
    b=next(row for row in case['paths'][1:] if dict(zip(map(tuple,row['events']),row['deltas']))!=am)
    bm=dict(zip(map(tuple,b['events']),b['deltas']))
    changed=sorted(e for e in am if am[e]!=bm[e])
    def expand(row):
        cur=[x[:] for x in case['before']];out=[];p=case['parents']
        for k,(i,v) in enumerate(row['events']):
            nxt=[x[:] for x in cur];nxt[i]=[w for w in nxt[i] if w!=v]
            out.append({'version':'16.26','genesis':'v16.26-common-genesis','parents':p[:],
                        'before':cur,'after':nxt,'index':i,'leaf':v,'parent':p[v],
                        'tau_before':row['profiles'][k][p[v]],'tau_after':row['profiles'][k+1][p[v]],
                        'h_before':row['heights'][k],'h_after':row['heights'][k+1],
                        'delta_h':row['deltas'][k],'trigger':row['triggers'][k]})
            cur=nxt
        return out
    return {'version':'16.27','parents':case['parents'],'before':case['before'],'after':case['after'],
            'path_a':expand(a),'path_b':expand(b),'changed_events':[list(e) for e in changed]}

if __name__=='__main__':
    doc=produce(4);out=HERE/'evidence';out.mkdir(exist_ok=True)
    raw=(json.dumps(doc,sort_keys=True,separators=(',',':'))+'\n').encode()
    (out/'FULL_CERTIFICATES.json.xz').write_bytes(lzma.compress(raw))
    w=next((legacy_witness(c) for x in doc['instances'] if x['variant']=='original' for c in x['cases'] if c['dependent']),None)
    (out/'WITNESS.json').write_text(json.dumps(w,indent=2,sort_keys=True)+'\n')
    r={'execution_status':'COMPLETED','summary':doc['summary'],'raw_bytes':len(raw),
       'raw_sha256':hashlib.sha256(raw).hexdigest(),'proof_status':'producer only; independent verification required'}
    (out/'PRODUCTION.json').write_text(json.dumps(r,indent=2,sort_keys=True)+'\n');print(json.dumps(r))
