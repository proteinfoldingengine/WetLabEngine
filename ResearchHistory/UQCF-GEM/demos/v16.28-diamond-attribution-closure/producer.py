"""v16.28: ideals/diamonds of the actual retained event poset; no path fitting."""
from collections import Counter
from functools import lru_cache
from itertools import combinations
from pathlib import Path
import hashlib
import json
import lzma

HERE=Path(__file__).resolve().parent
PARENT=HERE.parent/'v16.27-increment-attribution-closure/completion/evidence/FULL_CERTIFICATES.json.xz'
PARENT_SHA='1397e6d798c73126fc547afffb4bb7f681645bd83665af9b7ae6a66e472c866d'
GENESIS='v16.27-common-genesis'

def need(ok,message):
    if not ok:raise ValueError(message)

@lru_cache(None)
def parent_data():
    raw=lzma.decompress(PARENT.read_bytes())
    need(hashlib.sha256(raw).hexdigest()==PARENT_SHA,'parent certificate SHA-256')
    return json.loads(raw)

def validate(raw,before,after):
    need(isinstance(raw,(list,tuple)) and len(raw)>0,'empty lineage')
    p=tuple(raw)
    need(all(type(x) is int for x in p) and p[0]==-1,'exact parent identities')
    need(all(0<=x<len(p) for x in p[1:]),'parent endpoint')
    for node in range(1,len(p)):
        seen=set()
        while node:
            need(node not in seen,'cyclic lineage');seen.add(node);node=p[node]
    def family(items):
        need(isinstance(items,(list,tuple)) and len(items)>0,'empty cover')
        result=[]
        for item in items:
            need(isinstance(item,(list,tuple)) and len(item)>0,'empty view')
            y=tuple(item)
            need(all(type(v) is int and 0<=v<len(p) for v in y),'view identity')
            need(len(set(y))==len(y) and 0 in y,'root or duplicate identity')
            need(all(v==0 or p[v] in y for v in y),'missing ancestor')
            result.append(y)
        return tuple(result)
    ys,zs=family(before),family(after)
    need(len(ys)==len(zs) and all(set(z)<=set(y) for y,z in zip(ys,zs)),'indexed endpoint')
    need(set().union(*map(set,ys))==set().union(*map(set,zs)),'changed union')
    return p,ys,zs

@lru_cache(maxsize=100000)
def height(p,ys):
    U=set().union(*map(set,ys));answer=1
    for v in U:
        target=sum(1<<w for w in U if w and p[w]==v)
        if not target:continue
        dp={0:0}
        for y in ys:
            bits=sum(1<<w for w in y if w and p[w]==v)
            for old,cost in tuple(dp.items()):
                new=old|bits;dp[new]=min(dp.get(new,len(ys)+1),cost+1)
        need(target in dp,'uncovered child');answer=max(answer,dp[target])
    return answer

def predecessor_masks(p,events):
    masks=[]
    for i,v in events:
        bits=0
        for a,(j,u) in enumerate(events):
            if i!=j or u==v:continue
            node=u
            while node and node!=v:node=p[node]
            if node==v:bits|=1<<a
        masks.append(bits)
    return masks

def certify(raw,before,after):
    p,ys,zs=validate(raw,before,after)
    events=tuple((i,v) for i,y in enumerate(ys) for v in sorted(set(y)-set(zs[i])))
    n=len(events);pred=predecessor_masks(p,events);full=(1<<n)-1
    values={}
    for mask in range(1<<n):
        if any(pred[e]&~mask for e in range(n) if mask>>e&1):continue
        deleted={events[e] for e in range(n) if mask>>e&1}
        cur=tuple(tuple(v for v in y if (i,v) not in deleted) for i,y in enumerate(ys))
        values[mask]=height(p,cur)
    diamonds=[]
    for mask in values:
        enabled=[e for e in range(n) if not(mask>>e&1) and not(pred[e]&~mask)]
        for e,f in combinations(enabled,2):
            a,b=mask|(1<<e),mask|(1<<f);end=a|(1<<f)
            delta=values[end]-values[a]-values[b]+values[mask]
            diamonds.append([mask,e,f,delta])
    independent=all(row[3]==0 for row in diamonds)
    weights=[values[pred[e]|(1<<e)]-values[pred[e]] for e in range(n)] if independent else None
    if independent:
        need(all(values[s]==values[0]+sum(weights[e] for e in range(n) if s>>e&1) for s in values),'additive theorem violation')
    witness=None
    if not independent:
        mask,e,f,delta=next(row for row in diamonds if row[3])
        def extend(start,target):
            seq=[];current=start
            while current!=target:
                enabled=[a for a in range(n) if target>>a&1 and not(current>>a&1) and not(pred[a]&~current)]
                need(enabled,'no legal witness completion');a=enabled[0];seq.append(a);current|=1<<a
            return seq
        prefix=extend(0,mask);suffix=extend(mask|(1<<e)|(1<<f),full)
        a=prefix+[e,f]+suffix;b=prefix+[f,e]+suffix
        def hs(seq):
            used=0;out=[values[0]]
            for event in seq:used|=1<<event;out.append(values[used])
            return out
        witness={'mask':mask,'events':[e,f],'path_a':a,'path_b':b,'heights_a':hs(a),'heights_b':hs(b)}
    return {'version':'16.28','genesis':GENESIS,'parents':list(p),'before':[list(y) for y in ys],
            'after':[list(z) for z in zs],'events':[list(e) for e in events],'predecessors':pred,
            'states':[[mask,h] for mask,h in values.items()],'diamonds':diamonds,
            'independent':independent,'weights':weights,'witness':witness}

def produce(bound=4):
    need(type(bound) is int and 1<=bound<=4,'declared bound')
    old=parent_data();instances=[]
    for inst in old['instances']:
        if len(inst['parents'])>bound:continue
        cases=[certify(c['parents'],c['before'],c['after']) for c in inst['cases']]
        instances.append({'code':inst['code'],'variant':inst['variant'],'parents':list(inst['parents']),'cases':cases})
    return {'version':'16.28','genesis':GENESIS,'parent_raw_sha256':PARENT_SHA,'tree_bound':bound,
            'view_bound':4,'removed_min':2,'removed_max':5,'instances':instances}

if __name__=='__main__':
    doc=produce(4);out=HERE/'evidence';out.mkdir(exist_ok=True)
    raw=(json.dumps(doc,sort_keys=True,separators=(',',':'))+'\n').encode()
    (out/'FULL_CERTIFICATES.json.xz').write_bytes(lzma.compress(raw))
    examples={'negative':certify((-1,0,0),[(0,1),(0,2),(0,1,2)],[(0,1),(0,2),(0,)]),
              'positive':certify((-1,0,0),[(0,1,2),(0,1,2)],[(0,2),(0,1)]),
              'chain':certify((-1,0,0,1),[(0,1,2,3),(0,1,3)],[(0,2),(0,1,3)])}
    (out/'EXAMPLES.json').write_text(json.dumps(examples,indent=2,sort_keys=True)+'\n')
    result={'execution_status':'COMPLETED','raw_bytes':len(raw),'raw_sha256':hashlib.sha256(raw).hexdigest(),
            'parent_raw_sha256':PARENT_SHA,'proof_status':'producer; independent verification required'}
    (out/'PRODUCTION.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n');print(json.dumps(result))
