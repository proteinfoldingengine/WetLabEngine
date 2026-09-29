"""Independent v16.28 verifier: permutations, complete endpoint reconstruction, modular tests.
No imports from producer, earlier engines or earlier adjudicators.
"""
from collections import Counter
from functools import lru_cache
from itertools import combinations, permutations, product
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

def fields(value,required):
    need(isinstance(value,dict) and set(required)<=value.keys(),'missing required fields')

def ints(value,n=None):
    need(isinstance(value,(list,tuple)) and all(type(x) is int for x in value),'exact integer sequence')
    if n is not None:need(len(value)==n,'integer sequence length')
    return tuple(value)

def validate(raw,before,after):
    p=ints(raw);need(p and p[0]==-1,'root')
    need(all(0<=v<len(p) for v in p[1:]),'parent endpoint')
    for v in range(1,len(p)):
        seen=set()
        while v:
            need(v not in seen,'parent cycle');seen.add(v);v=p[v]
    def views(raw):
        need(isinstance(raw,(list,tuple)) and len(raw)>0,'empty indexed cover')
        out=[]
        for value in raw:
            y=ints(value);need(y and 0 in y and len(y)==len(set(y)),'root/duplicate')
            need(all(0<=v<len(p) for v in y),'view endpoint')
            need(all(v==0 or p[v] in y for v in y),'non-prefix view');out.append(y)
        return tuple(out)
    ys,zs=views(before),views(after)
    need(len(ys)==len(zs) and all(set(z)<=set(y) for y,z in zip(ys,zs)),'indexed retained endpoints')
    need(set().union(*map(set,ys))==set().union(*map(set,zs)),'changed union')
    return p,ys,zs

@lru_cache(maxsize=100000)
def height(p,ys):
    union=set().union(*map(set,ys));max_tau=1
    subfamilies=[]
    for mask in range(1,1<<len(ys)):
        nodes=set().union(*(set(y) for i,y in enumerate(ys) if mask>>i&1))
        subfamilies.append((mask.bit_count(),nodes))
    for node in union:
        children={v for v in union if v and p[v]==node}
        if children:max_tau=max(max_tau,min(size for size,nodes in subfamilies if children<=nodes))
    return max_tau

def reconstruct(p,ys,zs):
    events=tuple((i,v) for i in range(len(ys)) for v in sorted(set(ys[i])-set(zs[i])))
    n=len(events);ancestors=[]
    for v in range(len(p)):
        chain=set();node=v
        while node:node=p[node];chain.add(node)
        ancestors.append(chain)
    pred=[sum(1<<a for a,(j,u) in enumerate(events) if i==j and v in ancestors[u]) for i,v in events]
    states={};paths={};outgoing={}
    def value(mask):
        if mask not in states:
            removed={events[e] for e in range(n) if mask>>e&1}
            cur=tuple(tuple(sorted(set(y)-{v for i2,v in removed if i2==i})) for i,y in enumerate(ys))
            states[mask]=height(p,cur)
        return states[mask]
    for order in permutations(range(n)):
        mask=0
        if any(pred[e]&~sum(1<<a for a in order[:j]) for j,e in enumerate(order)):continue
        hs=[value(0)];attribution=[0]*n
        for e in order:
            outgoing.setdefault(mask,set()).add(e);new=mask|(1<<e);hv=value(new)
            d=hv-hs[-1];need(d in (0,1),'actual atomic bound violated')
            attribution[e]=d;hs.append(hv);mask=new
        paths[order]=(tuple(hs),tuple(attribution))
    need(paths,'no admissible full path')
    diamonds={}
    for mask,enabled in outgoing.items():
        for e,f in combinations(sorted(enabled),2):
            end=mask|(1<<e)|(1<<f)
            need(end in states,'missing actual common state')
            d=states[end]-states[mask|(1<<e)]-states[mask|(1<<f)]+states[mask]
            need(d in (-1,0,1),'mixed difference bound')
            diamonds[(mask,e,f)]=d
    return events,pred,states,paths,diamonds

def _verify_case(d,parent_case=None):
    fields(d,['version','genesis','parents','before','after','events','predecessors','states','diamonds','independent','weights','witness'])
    need(d['version']=='16.28' and d['genesis']==GENESIS,'version/origin')
    p,ys,zs=validate(d['parents'],d['before'],d['after'])
    events,pred,values,paths,expected=reconstruct(p,ys,zs);n=len(events)
    need(isinstance(d['events'],list) and tuple(ints(e,2) for e in d['events'])==events,'incorrect event identities')
    need(ints(d['predecessors'],n)==tuple(pred),'incorrect predecessor relation')
    states={}
    need(isinstance(d['states'],list),'state list')
    for row in d['states']:
        mask,h=ints(row,2);need(mask not in states,'duplicate state');states[mask]=h
    need(states==values,'incorrect or incomplete reachable states')
    diamonds={}
    need(isinstance(d['diamonds'],list),'diamond list')
    for row in d['diamonds']:
        mask,e,f,delta=ints(row,4);key=(mask,e,f)
        need(key not in diamonds,'duplicate diamond');diamonds[key]=delta
    need(diamonds==expected,'incorrect or incomplete diamond certificate')
    independent=len({a for hs,a in paths.values()})==1
    zero_diamonds=all(d==0 for d in expected.values())
    modular=True;pair_count=0
    for a,b in combinations(sorted(values),2):
        pair_count+=1
        need(a|b in values and a&b in values,'ideal lattice closure')
        if values[a]+values[b]!=values[a|b]+values[a&b]:modular=False
    need(independent==zero_diamonds==modular,'candidate equivalence refuted')
    need(type(d['independent']) is bool and d['independent']==independent,'false independent verdict')
    candidate=[values[pred[e]|(1<<e)]-values[pred[e]] for e in range(n)]
    additive=all(values[s]==values[0]+sum(candidate[e] for e in range(n) if s>>e&1) for s in values)
    need(additive==independent,'candidate additive theorem refuted')
    if independent:
        need(ints(d['weights'],n)==tuple(candidate),'false actual coefficients')
        need(all(x in (0,1) for x in candidate),'coefficient atomic bound')
        need(d['witness'] is None,'spurious path-dependence witness')
    else:
        need(d['weights'] is None,'invalid additive allocation')
        w=d['witness'];fields(w,['mask','events','path_a','path_b','heights_a','heights_b'])
        mask=w['mask'];e,f=ints(w['events'],2)
        need(type(mask) is int and (mask,e,f) in expected and expected[(mask,e,f)]!=0,'witness not nonzero diamond')
        a,b=ints(w['path_a'],n),ints(w['path_b'],n)
        need(a in paths and b in paths,'illegal witness path')
        pos=mask.bit_count()
        need(a[:pos]==b[:pos] and sum(1<<j for j in a[:pos])==mask,'wrong common witness prefix')
        need(a[pos:pos+2]==(e,f) and b[pos:pos+2]==(f,e) and a[pos+2:]==b[pos+2:],'not the claimed adjacent swap')
        need(ints(w['heights_a'],n+1)==paths[a][0] and ints(w['heights_b'],n+1)==paths[b][0],'false witness heights')
        aa,bb=paths[a][1],paths[b][1];delta=expected[(mask,e,f)]
        need(bb[e]-aa[e]==delta and bb[f]-aa[f]==-delta,'witness attribution discrepancy')
        need(sum(aa)==sum(bb)==values[(1<<n)-1]-values[0],'endpoint total discrepancy')
    if parent_case is not None:
        need(tuple(map(tuple,parent_case['before']))==ys and tuple(map(tuple,parent_case['after']))==zs,'foreign parent endpoint')
        lookup={e:i for i,e in enumerate(events)};old={}
        for row in parent_case['paths']:
            order=tuple(lookup[tuple(e)] for e in row['events'])
            need(order not in old and order in paths,'parent path identity')
            hs,actual=paths[order]
            need(tuple(row['heights'])==hs and tuple(row['deltas'])==tuple(actual[e] for e in order),'parent path values disagree')
            old[order]=1
        need(set(old)==set(paths),'parent path coverage differs')
        need(parent_case['dependent']==(not independent),'parent classification disagrees')
    return {'endpoints':1,'independent':int(independent),'dependent':int(not independent),'states':len(values),
            'diamonds':len(expected),'positive':sum(x==1 for x in expected.values()),'negative':sum(x==-1 for x in expected.values()),
            'zero':sum(x==0 for x in expected.values()),'paths':len(paths),'modular_pairs':pair_count,
            'positive_weight_endpoints':int(independent and any(candidate))}

def verify_case(d,parent_case=None):
    try:return _verify_case(d,parent_case)
    except (KeyError,IndexError,TypeError,ZeroDivisionError) as exc:raise ValueError('malformed certificate: '+str(exc)) from exc

@lru_cache(None)
def parent_data():
    raw=lzma.decompress(PARENT.read_bytes())
    need(hashlib.sha256(raw).hexdigest()==PARENT_SHA,'parent SHA-256 mismatch')
    return json.loads(raw)

def shape_code(p):
    def rec(v):return '('+''.join(sorted(rec(w) for w in range(1,len(p)) if p[w]==v))+')'
    return rec(0)

@lru_cache(None)
def independent_shapes(bound):
    found=set()
    for n in range(1,bound+1):
        if n==1:found.add('()');continue
        for seq in product(range(n),repeat=n-2):
            degree=[1+seq.count(i) for i in range(n)];adj=[set() for _ in range(n)]
            for v in seq:
                leaf=next(i for i,d in enumerate(degree) if d==1)
                adj[leaf].add(v);adj[v].add(leaf);degree[v]-=1;degree[leaf]-=1
            a,b=[i for i,d in enumerate(degree) if d==1];adj[a].add(b);adj[b].add(a)
            p=[-2]*n;p[0]=-1;stack=[0]
            while stack:
                v=stack.pop()
                for w in adj[v]:
                    if p[w]==-2:p[w]=v;stack.append(w)
            found.add(shape_code(p))
    return found

def case_key(c):
    return (tuple(tuple(sorted(y)) for y in c['before']),tuple(tuple(sorted(z)) for z in c['after']))

def expected_endpoints(p):
    legal=[]
    for mask in range(1,1<<len(p),2):
        y=tuple(v for v in range(len(p)) if mask>>v&1)
        if all(v==0 or p[v] in y for v in y):legal.append(y)
    result=set();full=set(range(len(p)))
    for size in range(1,min(4,len(legal))+1):
        for ys in combinations(legal,size):
            if set().union(*map(set,ys))!=full:continue
            for zs in product(*[[z for z in legal if set(z)<=set(y)] for y in ys]):
                if set().union(*map(set,zs))!=full:continue
                if 2<=sum(len(y)-len(z) for y,z in zip(ys,zs))<=5:result.add((ys,zs))
    return result

def check_transport(old,new,perm):
    count=len(old['before'])
    for key in ('before','after'):
        want=[[perm[v] for v in reversed(y)] for y in reversed(old[key])]
        need(new[key]==want,'false declared view/storage relabeling')
    es=tuple(map(tuple,old['events']));ns=tuple(map(tuple,new['events']));positions={e:i for i,e in enumerate(ns)}
    mapping={i:positions[(count-1-view,perm[v])] for i,(view,v) in enumerate(es)}
    def maskmap(mask):return sum(1<<mapping[e] for e in mapping if mask>>e&1)
    need({maskmap(s):h for s,h in old['states']}==dict(new['states']),'state transport mismatch')
    trans={}
    for s,e,f,d in old['diamonds']:
        a,b=sorted((mapping[e],mapping[f]));trans[(maskmap(s),a,b)]=d
    need(trans=={tuple(row[:3]):row[3] for row in new['diamonds']},'diamond transport mismatch')
    need(old['independent']==new['independent'],'attribution transport mismatch')
    if old['weights'] is not None:
        need(all(new['weights'][mapping[e]]==w for e,w in enumerate(old['weights'])),'coefficient transport mismatch')

def _verify_document(doc,bound):
    fields(doc,['version','genesis','parent_raw_sha256','tree_bound','view_bound','removed_min','removed_max','instances'])
    need(doc['version']=='16.28' and doc['genesis']==GENESIS and doc['parent_raw_sha256']==PARENT_SHA,'document provenance')
    need(type(bound) is int and 1<=bound<=4,'verification bound')
    for key,value in [('tree_bound',bound),('view_bound',4),('removed_min',2),('removed_max',5)]:
        need(type(doc[key]) is int and doc[key]==value,'changed bound')
    need(isinstance(doc['instances'],list),'instance list')
    old={(x['code'],x['variant']):x for x in parent_data()['instances'] if len(x['parents'])<=bound}
    shapes=independent_shapes(bound)
    need(set(old)=={(c,k) for c in shapes for k in ('original','relabeled')},'parent rooted-shape coverage')
    lookup={}
    for inst in doc['instances']:
        fields(inst,['code','variant','parents','cases']);key=(inst['code'],inst['variant'])
        need(key in old and key not in lookup,'extra/duplicate shape')
        need(ints(inst['parents'])==tuple(old[key]['parents']),'wrong parent representative/relabeling')
        lookup[key]=inst
    need(set(lookup)==set(old),'missing shape')
    totals={'original':Counter(),'relabeled':Counter()};transported=0
    for code in sorted(shapes):
        p=tuple(old[(code,'original')]['parents']);n=len(p);perm=[0]+list(range(n-1,0,-1))
        originals={}
        for variant in ('original','relabeled'):
            key=(code,variant);inst=lookup[key];need(isinstance(inst['cases'],list),'case list')
            archive={case_key(c):c for c in old[key]['cases']}
            if variant=='original':expected=expected_endpoints(p)
            else:expected={case_key({'before':[[perm[v] for v in y] for y in reversed(a)],'after':[[perm[v] for v in z] for z in reversed(b)]}) for a,b in expected_endpoints(p)}
            need(set(archive)==expected,'parent endpoint coverage mismatch')
            seen=set()
            for c in inst['cases']:
                need(c.get('parents')==inst['parents'],'foreign case carrier');ck=case_key(c)
                need(ck in expected and ck not in seen,'extra/duplicate endpoint');seen.add(ck)
                metrics=verify_case(c,archive[ck]);totals[variant].update(metrics)
                if variant=='original':originals[ck]=c
                else:
                    inverse=case_key({'before':[[perm[v] for v in y] for y in reversed(c['before'])],'after':[[perm[v] for v in z] for z in reversed(c['after'])]})
                    need(inverse in originals,'missing metamorphic source');check_transport(originals[inverse],c,perm);transported+=1
            need(seen==expected,'missing endpoint')
    need(totals['original']==totals['relabeled'],'metamorphic aggregate mismatch')
    return {'version':'16.28','execution_status':'COMPLETED','input_validity':'VALID',
            'scientific_verdict':'EXACT_DIAMOND_ADDITIVITY_ATTRIBUTION_EQUIVALENCE',
            'proof_status':'general written D1-D7; independently reconstructed bounded certificate',
            'parent_raw_sha256':PARENT_SHA,'shapes':len(shapes),'transported_endpoints':transported,
            'original':dict(totals['original']),'relabeled':dict(totals['relabeled']),
            'scope':'actual retained h on fixed finite endpoint intervals; no geometry or physical law'}

def verify_document(doc,bound=4):
    try:return _verify_document(doc,bound)
    except (KeyError,IndexError,TypeError,ZeroDivisionError) as exc:raise ValueError('malformed document: '+str(exc)) from exc

if __name__=='__main__':
    out=HERE/'evidence';raw=lzma.decompress((out/'FULL_CERTIFICATES.json.xz').read_bytes())
    result=verify_document(json.loads(raw),4)
    examples=json.loads((out/'EXAMPLES.json').read_text())
    result['examples']={key:verify_case(c) for key,c in examples.items()}
    result['raw_sha256']=hashlib.sha256(raw).hexdigest()
    (out/'VERIFICATION.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n');print(json.dumps(result))
