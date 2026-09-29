"""Independent v16.27 verifier: Prüfer shapes, permutation paths, set-cover DP.

Imports no producer, historical engine, or helper implementing the adjudication.
"""
from collections import Counter
from functools import lru_cache
from itertools import combinations, permutations, product
from pathlib import Path
import hashlib
import json
import lzma

HERE=Path(__file__).resolve().parent
ORIGIN='v16.27-common-genesis'
SCHEMA='v16.27-completion-1'

def need(ok,message):
    if not ok:raise ValueError(message)

def fields(obj,required):
    need(isinstance(obj,dict) and set(required)<=obj.keys(),'missing required fields: '+str(required))

def integers(raw,n=None):
    need(isinstance(raw,(list,tuple)) and (n is None or len(raw)==n),'integer sequence dimension')
    need(all(type(x) is int for x in raw),'exact integer required; Boolean/float disallowed')
    return tuple(raw)

def validate(raw,before,after):
    p=integers(raw);need(p and p[0]==-1,'root/carrier')
    need(all(0<=x<len(p) for x in p[1:]),'parent endpoint')
    for v in range(1,len(p)):
        reached=set();u=v
        while u:
            need(u not in reached,'cycle in lineage');reached.add(u);u=p[u]
    def cover(raw):
        need(isinstance(raw,(list,tuple)) and len(raw)>0,'empty indexed views')
        ys=[]
        for row in raw:
            y=integers(row);need(y and 0 in y and len(y)==len(set(y)),'retained root/duplicate')
            need(all(0<=v<len(p) for v in y),'retained endpoint')
            need(all(v==0 or p[v] in y for v in y),'retained prefix closure')
            ys.append(y)
        return tuple(ys)
    ys,zs=cover(before),cover(after)
    need(len(ys)==len(zs),'indexed endpoint count')
    need(all(set(z)<=set(y) for y,z in zip(ys,zs)),'endpoint is not retained')
    need(set().union(*map(set,ys))==set().union(*map(set,zs)),'union changed')
    return p,ys,zs

@lru_cache(None)
def profile(p,ys):
    U=set().union(*map(set,ys));result=[]
    for v in range(len(p)):
        kids=tuple(w for w in U if w and p[w]==v)
        if v not in U or not kids:result.append(0);continue
        bit={w:1<<j for j,w in enumerate(kids)};target=(1<<len(kids))-1;dp={0:0}
        for y in ys:
            added=sum(bit[w] for w in kids if w in y)
            nxt=dict(dp)
            for mask,value in dp.items():nxt[mask|added]=min(nxt.get(mask|added,len(ys)+1),value+1)
            dp=nxt
        need(target in dp,'children not covered');result.append(dp[target])
    return tuple(result)

def state_h(p,ys):return max((1,)+profile(p,ys))

def events(ys,zs):return tuple(sorted((i,v) for i,y in enumerate(ys) for v in set(y)-set(zs[i])))

@lru_cache(None)
def legal_orders(p,ys,zs):
    E=events(ys,zs);relations=[]
    for a in E:
        for b in E:
            if a[0]!=b[0] or a==b:continue
            u=a[1]
            while u:
                u=p[u]
                if u==b[1]:relations.append((a,b));break
    accepted=[]
    for order in permutations(E):
        pos={e:k for k,e in enumerate(order)}
        if all(pos[a]<pos[b] for a,b in relations):accepted.append(order)
    need(accepted,'no legal permutation for valid endpoint')
    return tuple(accepted)

def delete(p,cur,event,target):
    i,v=integers(event,2)
    need(0<=i<len(cur) and 0<v<len(p),'event endpoint')
    need(v in cur[i] and v not in target[i],'event outside required deletion set')
    need(not any(p[w]==v for w in cur[i] if w),'non-leaf event')
    nxt=list(cur);nxt[i]=tuple(w for w in cur[i] if w!=v);nxt=tuple(nxt)
    need(set().union(*map(set,nxt))==set().union(*map(set,cur)),'atomic union loss')
    return nxt

def local_trigger(p,cur,nxt,v):
    U=set().union(*map(set,cur));kids={w for w in U if w and p[w]==v};old=profile(p,cur)[v]
    old_min=[s for s in combinations(range(len(cur)),old) if kids<=set().union(*(set(cur[i]) for i in s))]
    return bool(old_min) and all(not kids<=set().union(*(set(nxt[i]) for i in s)) for s in old_min)

def verify_path(p,ys,zs,row):
    fields(row,('events','heights','profiles','deltas','triggers'))
    need(isinstance(row['events'],list),'path events')
    seq=tuple(integers(e,2) for e in row['events']);E=events(ys,zs)
    need(len(seq)==len(E) and set(seq)==set(E),'missing/duplicate/foreign event')
    need(seq in legal_orders(p,ys,zs),'illegal atomic event order')
    hs=integers(row['heights'],len(E)+1);ds=integers(row['deltas'],len(E))
    need(isinstance(row['profiles'],list) and len(row['profiles'])==len(E)+1,'profile coverage')
    ps=tuple(integers(q,len(p)) for q in row['profiles'])
    ts=row['triggers'];need(isinstance(ts,list) and len(ts)==len(E) and all(type(t) is bool for t in ts),'trigger types/coverage')
    cur=ys;need(ps[0]==profile(p,cur) and hs[0]==state_h(p,cur),'false initial state/profile')
    for k,e in enumerate(seq):
        nxt=delete(p,cur,e,zs);v=p[e[1]];q=profile(p,nxt);h1=state_h(p,nxt)
        need(ps[k+1]==q and hs[k+1]==h1,'false recorded state/profile')
        need(all(q[u]==ps[k][u] for u in range(len(p)) if u!=v),'nonlocal profile change')
        tr=local_trigger(p,cur,nxt,v)
        need(q[v]-ps[k][v] in (0,1) and tr==(q[v]>ps[k][v]),'local trigger identity')
        delta=h1-hs[k];need(delta in (0,1) and ds[k]==delta,'false atomic delta')
        need(ts[k]==tr,'false local trigger');cur=nxt
    need(all(set(a)==set(b) for a,b in zip(cur,zs)),'wrong path endpoint')
    need(sum(ds)==state_h(p,zs)-state_h(p,ys),'endpoint telescoping failure')
    return seq,tuple(ds)

def verify_case(d):
    try:
        fields(d,('version','schema','genesis','parents','before','after','paths','dependent','changed_events'))
        need(d['version']=='16.27' and d['schema']==SCHEMA and d['genesis']==ORIGIN,'case origin/schema')
        p,ys,zs=validate(d['parents'],d['before'],d['after'])
        need(isinstance(d['paths'],list),'path records missing')
        observed={}
        for row in d['paths']:
            seq,ds=verify_path(p,ys,zs,row);need(seq not in observed,'duplicate path');observed[seq]=ds
        need(set(observed)==set(legal_orders(p,ys,zs)),'incomplete legal path coverage')
        maps=[dict(zip(seq,ds)) for seq,ds in observed.items()]
        changed=sorted(e for e in events(ys,zs) if len({a[e] for a in maps})>1)
        need(type(d['dependent']) is bool and d['dependent']==bool(changed),'false attribution verdict')
        need(isinstance(d['changed_events'],list),'changed event list')
        got=tuple(integers(e,2) for e in d['changed_events'])
        need(len(got)==len(set(got)) and set(got)==set(changed),'false changed event set')
        return {'path_count':len(observed),'dependent':bool(changed),'total_delta':state_h(p,zs)-state_h(p,ys)}
    except (KeyError,IndexError,TypeError) as exc:raise ValueError('malformed path certificate') from exc

def verify_witness(d):
    """Strictly verify the historical raw witness format, including EVERY step field."""
    try:
        fields(d,('version','parents','before','after','path_a','path_b','changed_events'))
        need(d['version']=='16.27','witness version');p,ys,zs=validate(d['parents'],d['before'],d['after'])
        outputs=[]
        for name in ('path_a','path_b'):
            path=d[name];need(isinstance(path,list) and len(path)==len(events(ys,zs)),'witness path coverage')
            cur=ys;out={}
            for step in path:
                fields(step,('version','genesis','parents','before','after','index','leaf','parent','tau_before','tau_after','h_before','h_after','delta_h','trigger'))
                need(step['version']=='16.26' and step['genesis']=='v16.26-common-genesis','foreign step origin')
                need(integers(step['parents'])==p,'foreign step parent carrier')
                _,a,b=validate(p,step['before'],step['after'])
                need(tuple(map(frozenset,a))==tuple(map(frozenset,cur)),'witness state chain')
                i,v=integers([step['index'],step['leaf']],2);nxt=delete(p,cur,(i,v),zs)
                need(tuple(map(frozenset,b))==tuple(map(frozenset,nxt)),'false stored after state')
                par=p[v];q0,q1=profile(p,cur),profile(p,nxt);h0,h1=state_h(p,cur),state_h(p,nxt)
                expected={'parent':par,'tau_before':q0[par],'tau_after':q1[par],'h_before':h0,'h_after':h1,'delta_h':h1-h0}
                for key,value in expected.items():need(type(step[key]) is int and step[key]==value,'false/exact-type step '+key)
                need(type(step['trigger']) is bool and step['trigger']==local_trigger(p,cur,nxt,par),'false step trigger')
                need((i,v) not in out,'repeated witness event');out[(i,v)]=h1-h0;cur=nxt
            need(tuple(map(frozenset,cur))==tuple(map(frozenset,zs)),'witness endpoint')
            need(set(out)==set(events(ys,zs)) and sum(out.values())==state_h(p,zs)-state_h(p,ys),'witness events/total')
            outputs.append(out)
        changed=sorted(e for e in outputs[0] if outputs[0][e]!=outputs[1][e])
        got=[integers(e,2) for e in d['changed_events']]
        need(changed and len(got)==len(set(got)) and set(got)==set(changed),'witness does not show asserted attribution difference')
        return {'input_validity':'VALID','changed_events':[list(e) for e in changed],
                'total_delta':state_h(p,zs)-state_h(p,ys),'scientific_verdict':'EVENT_ATTRIBUTION_PATH_DEPENDENT'}
    except (KeyError,IndexError,TypeError) as exc:raise ValueError('malformed raw witness') from exc

def code(p):
    def rec(v):return '('+''.join(sorted(rec(w) for w in range(1,len(p)) if p[w]==v))+')'
    return rec(0)

@lru_cache(None)
def independent_shapes(bound):
    result=set()
    for n in range(1,bound+1):
        if n==1:result.add('()');continue
        for seq in product(range(n),repeat=n-2):
            degree=[seq.count(i)+1 for i in range(n)];adj=[set() for _ in range(n)]
            for v in seq:
                leaf=next(i for i in range(n) if degree[i]==1)
                adj[leaf].add(v);adj[v].add(leaf);degree[leaf]-=1;degree[v]-=1
            a,b=[i for i in range(n) if degree[i]==1];adj[a].add(b);adj[b].add(a)
            p=[-2]*n;p[0]=-1;stack=[0]
            while stack:
                v=stack.pop()
                for w in adj[v]:
                    if p[w]==-2:p[w]=v;stack.append(w)
            result.add(code(tuple(p)))
    return result

def endpoint_key(ys,zs):
    return tuple(sorted((tuple(sorted(y)),tuple(sorted(z))) for y,z in zip(ys,zs)))

def expected_endpoints(p):
    L=[]
    for bits in product((0,1),repeat=len(p)-1):
        y=(0,)+tuple(i+1 for i,b in enumerate(bits) if b)
        if all(v==0 or p[v] in y for v in y):L.append(y)
    expected=set();full=set(range(len(p)))
    for n in range(1,min(4,len(L))+1):
        for ys in combinations(L,n):
            if set().union(*map(set,ys))!=full:continue
            for zs in product(*[[z for z in L if set(z)<=set(y)] for y in ys]):
                if set().union(*map(set,zs))!=full:continue
                if 2<=sum(len(y)-len(z) for y,z in zip(ys,zs))<=5:expected.add(endpoint_key(ys,zs))
    return expected

def verify_document(doc,bound=4):
    try:
        fields(doc,('version','schema','genesis','tree_bound','view_bound','removed_min','removed_max','instances','summary'))
        need(doc['version']=='16.27' and doc['schema']==SCHEMA and doc['genesis']==ORIGIN,'document origin/schema')
        need(type(bound) is int and 1<=bound<=4,'verifier bound')
        for key,value in [('tree_bound',bound),('view_bound',4),('removed_min',2),('removed_max',5)]:
            need(type(doc[key]) is int and doc[key]==value,'changed declared '+key)
        need(isinstance(doc['instances'],list),'missing instances');lookup={}
        for inst in doc['instances']:
            fields(inst,('code','variant','parents','cases'));key=(inst['code'],inst['variant'])
            need(key not in lookup,'duplicate shape instance');p,_,_=validate(inst['parents'],[[0]],[[0]])
            need(code(p)==inst['code'] and isinstance(inst['cases'],list),'wrong shape/cases');lookup[key]=inst
        shapes=independent_shapes(bound)
        need(set(lookup)=={(s,v) for s in shapes for v in ('original','relabeled')},'incomplete shape universe')
        totals={v:Counter({'endpoints':0,'multi_path':0,'dependent':0,'paths':0}) for v in ('original','relabeled')}
        maxpaths=0;steps=0
        for s in sorted(shapes):
            a,b=lookup[(s,'original')],lookup[(s,'relabeled')];p=tuple(a['parents']);n=len(p)
            need(all(0<=p[i]<i for i in range(1,n)),'original not ancestor-first')
            perm=[0]+list(range(n-1,0,-1));q=[-1]*n
            for i in range(1,n):q[perm[i]]=perm[p[i]]
            need(b['parents']==q,'false declared lineage relabeling')
            indexes={}
            for inst in (a,b):
                expected=expected_endpoints(tuple(inst['parents']));seen={};variant=inst['variant']
                for case in inst['cases']:
                    need(case.get('parents')==inst['parents'],'foreign case carrier')
                    ys,zs=case.get('before',[]),case.get('after',[]);key=endpoint_key(ys,zs)
                    need(key in expected and key not in seen,'duplicate/undeclared endpoint')
                    r=verify_case(case);seen[key]=case
                    totals[variant].update({'endpoints':1,'multi_path':int(r['path_count']>1),'dependent':int(r['dependent']),'paths':r['path_count']})
                    maxpaths=max(maxpaths,r['path_count']);steps+=sum(len(x['events']) for x in case['paths'])
                need(set(seen)==expected,'missing endpoint records');indexes[variant]=seen
            for case in indexes['original'].values():
                y=[[perm[v] for v in reversed(row)] for row in reversed(case['before'])]
                z=[[perm[v] for v in reversed(row)] for row in reversed(case['after'])]
                target=indexes['relabeled'][endpoint_key(y,z)]
                need(target['before']==y and target['after']==z,'false view/storage transformation')
                targetrows={tuple(map(tuple,row['events'])):row for row in target['paths']};m=len(y)
                for row in case['paths']:
                    e=tuple((m-1-i,perm[v]) for i,v in row['events']);t=targetrows[e]
                    need(t['heights']==row['heights'] and t['deltas']==row['deltas'] and t['triggers']==row['triggers'],'metamorphic scalar mismatch')
                    for old,new in zip(row['profiles'],t['profiles']):
                        need(all(new[perm[v]]==old[v] for v in range(n)),'metamorphic profile mismatch')
        summary={k:dict(v) for k,v in totals.items()}
        need(isinstance(doc['summary'],dict) and set(doc['summary'])==set(summary),'summary coverage')
        for variant in summary:
            for k,value in summary[variant].items():need(type(doc['summary'][variant].get(k)) is int and doc['summary'][variant][k]==value,'false summary '+variant+'/'+k)
        need(summary['original']==summary['relabeled'],'metamorphic coverage mismatch')
        verdict='EVENT_ATTRIBUTION_PATH_DEPENDENT' if summary['original']['dependent'] else 'NO_BOUNDED_COUNTEREXAMPLE_UNIVERSAL_CLAIM_UNRESOLVED'
        return {'version':'16.27','execution_status':'COMPLETED','input_validity':'VALID','scientific_verdict':verdict,
                'proof_status':'general counterexample/arguments C1-C7; complete bounded path reconstruction',
                'scope':'formal retained-view h; no physical/temporal/geometric inference','original':summary['original'],
                'relabeled':summary['relabeled'],'shapes':len(shapes),'max_paths_per_endpoint':maxpaths,'verified_atomic_step_occurrences':steps}
    except (KeyError,IndexError,TypeError) as exc:raise ValueError('malformed complete certificate') from exc

if __name__=='__main__':
    out=HERE/'evidence';raw=lzma.decompress((out/'FULL_CERTIFICATES.json.xz').read_bytes())
    r=verify_document(json.loads(raw),4)
    witness=json.loads((out/'WITNESS.json').read_text())
    if witness is not None:r['witness']=verify_witness(witness)
    else:need(r['original']['dependent']==0,'missing required noncanonicity witness')
    r['raw_sha256']=hashlib.sha256(raw).hexdigest()
    (out/'VERIFICATION.json').write_text(json.dumps(r,indent=2,sort_keys=True)+'\n');print(json.dumps(r))
