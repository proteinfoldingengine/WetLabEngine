"""Exact retained component certificates; no imported earlier adjudicator."""
from functools import lru_cache
from itertools import combinations,product
from pathlib import Path
import hashlib,json,lzma
VERSION='16.31'
GENESIS='v16.31-frozen-common-genesis'
P=Path(__file__).resolve().parent

def need(ok,message):
 if not ok:raise ValueError(message)

def inputs(raw,before,after):
 need(isinstance(raw,(list,tuple)) and raw,'empty parent carrier')
 p=tuple(raw);need(all(type(x)is int for x in p) and p[0]==-1,'parent types/root')
 need(all(0<=p[v]<len(p) for v in range(1,len(p))),'parent endpoints')
 for v in range(1,len(p)):
  seen=set();u=v
  while u:
   need(u not in seen,'parent cycle');seen.add(u);u=p[u]
 def views(raw):
  need(isinstance(raw,(list,tuple)) and raw,'empty view family');ans=[]
  for row in raw:
   need(isinstance(row,(list,tuple)) and row,'empty retained view')
   need(all(type(v)is int and 0<=v<len(p) for v in row),'retained identity')
   need(len(set(row))==len(row) and 0 in row,'duplicate/root')
   need(all(v==0 or p[v] in row for v in row),'missing ancestor')
   ans.append(tuple(row))
  return tuple(ans)
 a,b=views(before),views(after)
 need(len(a)==len(b),'indexed endpoint lengths')
 need(all(set(z)<=set(y) for y,z in zip(a,b)),'not componentwise retention')
 need(set().union(*map(set,a))==set().union(*map(set,b)),'same union required')
 return p,a,b

@lru_cache(maxsize=120000)
def profile(p,ys):
 U=set().union(*map(set,ys));answer=[]
 for v in range(len(p)):
  kids=sorted(w for w in U if w and p[w]==v)
  if not kids:answer.append(0);continue
  labels={w:1<<i for i,w in enumerate(kids)};target=(1<<len(kids))-1;dp={0:0}
  for y in ys:
   mask=sum(labels[w] for w in kids if w in y)
   for covered,cost in tuple(dp.items()):
    new=covered|mask;dp[new]=min(dp.get(new,len(ys)+1),cost+1)
  need(target in dp,'uncovered children');answer.append(dp[target])
 return tuple(answer)

def ancestry(p,events):
 pred=[]
 for i,n in events:
  mask=0
  for j,(k,w) in enumerate(events):
   if i!=k or w==n:continue
   u=p[w]
   while u!=-1:
    if u==n:mask|=1<<j;break
    u=p[u]
  pred.append(mask)
 return pred

def embed(mask,ids):return sum(1<<e for j,e in enumerate(ids) if mask>>j&1)

def parts(values):
 m=(len(values)-1).bit_length();mu=list(values)
 for bit in range(m):
  for s in range(1<<m):
   if s>>bit&1:mu[s]-=mu[s^(1<<bit)]
 edges=set()
 for s,x in enumerate(mu):
  if x:edges.update(combinations([j for j in range(m) if s>>j&1],2))
 unseen=set(range(m));components=[]
 while unseen:
  stack=[min(unseen)];block=set()
  while stack:
   j=stack.pop()
   if j in block:continue
   block.add(j);stack.extend(b if a==j else a for a,b in edges if a==j or b==j)
  unseen-=block;components.append(sorted(block))
 return mu,sorted(edges),components

def certify(raw,before,after):
 p,a,b=inputs(raw,before,after)
 events=sorted((i,n) for i,y in enumerate(a) for n in y if n not in b[i]);m=len(events)
 need(m<=12,'explicit certificate computational limit 12 events')
 pred=ancestry(p,events);states={}
 for s in range(1<<m):
  if any(s>>j&1 and pred[j]&s!=pred[j] for j in range(m)):continue
  removed={events[j] for j in range(m) if s>>j&1}
  ys=tuple(tuple(n for n in y if (i,n) not in removed) for i,y in enumerate(a))
  states[s]=profile(p,ys)
 local=[];edges=set();witnesses=[]
 for v in range(len(p)):
  ids=[j for j,e in enumerate(events) if p[e[1]]==v]
  if not ids:continue
  prelude=0
  for j in ids:prelude|=pred[j]
  values=[states[prelude|embed(s,ids)][v] for s in range(1<<len(ids))]
  mu,ed,blocks=parts(values);components=[]
  for block in blocks:
   glob=[ids[j] for j in block]
   vals=[values[embed(s,block)]-values[0] for s in range(1<<len(block))]
   components.append({'event_ids':glob,'values':vals})
  for e,f in ed:
   edges.add((ids[e],ids[f]))
   for s in range(1<<len(ids)):
    if s&(1<<e|1<<f):continue
    d=values[s|1<<e|1<<f]-values[s|1<<e]-values[s|1<<f]+values[s]
    if d:
     witnesses.append([ids[e],ids[f],prelude|embed(s,ids),d]);break
  local.append({'vertex':v,'event_ids':ids,'prelude':prelude,'values':values,'mobius':mu,'components':components})
 return {'version':VERSION,'genesis':GENESIS,'parents':list(p),'before':[list(y) for y in a],'after':[list(y) for y in b],
         'events':[list(e) for e in events],'predecessors':pred,'states':[[s,list(q)] for s,q in sorted(states.items())],
         'local':local,'edges':[list(e) for e in sorted(edges)],'edge_witnesses':sorted(witnesses),'product_states':1<<m}

def shape_code(p):
 ch=[[] for _ in p]
 for w in range(1,len(p)):ch[p[w]].append(w)
 def rec(v):return '('+''.join(sorted(rec(w) for w in ch[v]))+')'
 return rec(0)

def decode(code):
 p=[];stack=[]
 for c in code:
  if c=='(':
   p.append(stack[-1] if stack else -1);stack.append(len(p)-1)
  else:stack.pop()
 return tuple(p)

def shapes(bound):
 codes=set()
 for n in range(1,bound+1):
  for q in product(*(range(i) for i in range(1,n))):codes.add(shape_code((-1,)+q))
 return [(c,decode(c)) for c in sorted(codes,key=lambda c:(len(c),c))]

def legal(p):
 return [tuple(v for v in range(len(p)) if s>>v&1) for s in range(1,1<<len(p),2)
         if all(not(s>>v&1) or s>>p[v]&1 for v in range(1,len(p)))]

def endpoints(p):
 L=legal(p);full=set(range(len(p)));cap=4 if len(p)<=4 else 3
 for k in range(1,min(cap,len(L))+1):
  for a in combinations(L,k):
   if set().union(*map(set,a))!=full:continue
   pools=[[z for z in L if set(z)<=set(y)] for y in a]
   for b in product(*pools):
    if sum(len(y)-len(z) for y,z in zip(a,b))>5:continue
    if set().union(*map(set,b))==full:yield a,b

def transport(p,views):
 pi=[0]+list(range(len(p)-1,0,-1));q=[-1]*len(p)
 for n in range(1,len(p)):q[pi[n]]=pi[p[n]]
 return tuple(q),tuple(tuple(pi[n] for n in reversed(y)) for y in reversed(views))

def produce(bound=5):
 need(type(bound)is int and 1<=bound<=5,'enumeration bound');instances=[]
 for code,p in shapes(bound):
  original=[];moved=[]
  for a,b in endpoints(p):
   original.append(certify(p,a,b));q,ta=transport(p,a);_,tb=transport(p,b);moved.append(certify(q,ta,tb))
  instances.extend([{'code':code,'variant':'original','parents':list(p),'cases':original},
                    {'code':code,'variant':'relabeled','parents':list(transport(p,[(0,)])[0]),'cases':moved}])
 return {'version':VERSION,'genesis':GENESIS,'bound':bound,'instances':instances}

def examples():
 return {'identity':certify((-1,),[(0,)],[(0,)]),
         'chain':certify((-1,0,0,1),[(0,1,2,3),(0,1,3)],[(0,2),(0,1,3)]),
         'third_order':certify((-1,0,0,0),[(0,1,2,3),(0,1),(0,2),(0,3)],[(0,),(0,1),(0,2),(0,3)]),
         'max_only':certify((-1,0,0,1,1),[(0,1,2),(0,1,3,4),(0,2),(0,1,4)],[(0,1),(0,1,3),(0,2),(0,1,4)]),
         'masked':certify((-1,0,0,1,1),[(0,1,3,4),(0,1,3),(0,1,4),(0,2)],[(0,1),(0,1,3),(0,1,4),(0,2)])}

if __name__=='__main__':
 doc=produce(5);raw=(json.dumps(doc,sort_keys=True,separators=(',',':'))+'\n').encode();e=P/'evidence';e.mkdir(exist_ok=True)
 (e/'FULL_CERTIFICATES.json.xz').write_bytes(lzma.compress(raw))
 receipt={'raw_sha256':hashlib.sha256(raw).hexdigest(),'raw_bytes':len(raw),'compressed_bytes':(e/'FULL_CERTIFICATES.json.xz').stat().st_size,
          'instances':len(doc['instances']),'original_cases':sum(len(i['cases']) for i in doc['instances'] if i['variant']=='original')}
 (e/'PRODUCTION.json').write_text(json.dumps(receipt,indent=2,sort_keys=True)+'\n')
 (e/'EXAMPLES.json').write_text(json.dumps(examples(),sort_keys=True,indent=2)+'\n');print(json.dumps(receipt),flush=True)
