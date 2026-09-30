import json
from collections import deque
import construct,check

def encoded(x):return json.dumps(x,sort_keys=True,separators=(',',':'))
def identity(g,r):return encoded([g['parents'],g['views'],r['q'],r['components'],r['representatives']])
def allowed_vertices(g,q,coordinate=None):
 return {i for i,row in enumerate(g['q']) if sum(abs(a-b) for a,b in zip(row,q))<=1 and (coordinate is None or all(a==b for j,(a,b) in enumerate(zip(row,q)) if j!=coordinate))}
def bfs(adj,allowed,a,b):
 seen={a};prev={};todo=deque([a])
 while todo:
  u=todo.popleft()
  for v in adj[u]:
   if v in allowed and v not in seen:seen.add(v);prev[v]=u;todo.append(v)
 if b not in seen:return {'reachable':sorted(seen)}
 path=[b]
 while path[-1]!=a:path.append(prev[path[-1]])
 return {'path':list(reversed(path))}
def summary(base,records):
 counts={'graphs':len(base['graphs']),'component_pairs':len(records),'endpoint_pairs':sum(r['endpoint_pairs'] for g in base['graphs'] for r in g['pairs']),'sc_pairs':0,'endpoint_only_pairs':0,'obstruction_pairs':0,'static_sufficient_pairs':0,'moving_required_pairs':0}
 for r in records:
  c=r['classification']
  if c['sc']:counts['sc_pairs']+=1
  elif c['endpoint_full']:counts['endpoint_only_pairs']+=1
  else:
   counts['obstruction_pairs']+=1
   counts['static_sufficient_pairs' if any('path' in z for z in r['static']) else 'moving_required_pairs']+=1
 return counts
def outcome(s):
 return 'OBSTRUCTION_CLASS_EMPTY' if s['obstruction_pairs']==0 else ('MOVING_LOCATION_REQUIRED' if s['moving_required_pairs'] else 'ALL_OBSTRUCTION_PAIRS_STATIC_SUFFICIENT')
def produce(base):
 records=[]
 for g in base['graphs']:
  p=g['parents'];k=g['views'];S=g['states'];ids={tuple(s):i for i,s in enumerate(S)};adj=[[] for _ in S]
  for a,b in g['edges']:adj[a].append(b);adj[b].append(a)
  for row in adj:row.sort()
  for r in g['pairs']:
   q=r['q'];a,b=r['representatives'];c=construct.classify(p,k,q,S[a],S[b]);proof=None;static=[]
   if c['sc'] or c['endpoint_full']:
    raw=construct.build(p,k,q,S[a],S[b]);proof={'path':[ids[tuple(s)] for s in raw['states']],'zero_prefix':raw['zero_prefix'],'zero_suffix':raw['zero_suffix']}
   else:
    for v in range(len(p)):static.append({'coordinate':v,**bfs(adj,allowed_vertices(g,q,v),a,b)})
   full=bfs(adj,allowed_vertices(g,q),a,b)
   if 'path' not in full:raise ValueError('full unit disconnection: requires independent nonunit adjudication')
   records.append({'identity':identity(g,r),'classification':c,'constructed':proof,'static':static,'full_unit_path':full['path']})
 s=summary(base,records)
 return {'campaign':'16.39','records':records,'summary':s,'outcome':'THEOREM_CONSTRUCTION_VALIDATED_WITHIN_DOMAIN','obstruction_outcome':outcome(s),'universal_unit_law':'UNRESOLVED'}

def _verify(base,doc):
 need=check.need
 need(isinstance(doc,dict) and set(doc)=={'campaign','records','summary','outcome','obstruction_outcome','universal_unit_law'},'certificate schema')
 need(doc['campaign']=='16.39' and doc['universal_unit_law']=='UNRESOLVED','campaign/universal claim')
 records=doc['records'];need(isinstance(records,list),'record list')
 expected={identity(g,r):(g,r) for g in base['graphs'] for r in g['pairs']}
 keys=[x['identity'] for x in records];need(len(keys)==len(set(keys)) and set(keys)==set(expected),'exact canonical pair coverage')
 sc_count=full_count=obstruction_count=static_count=moving_count=0
 def path(g,q,a,b,ids,coordinate=None):
  need(isinstance(ids,list) and ids and all(type(x) is int and 0<=x<len(g['states']) for x in ids),'path indices')
  states=[g['states'][i] for i in ids]
  check.path_states(g['parents'],g['views'],q,g['states'][a],g['states'][b],{'states':states,'zero_prefix':0,'zero_suffix':0})
  if coordinate is not None:
   for s in states:need(all(x==y for j,(x,y) in enumerate(zip(check.profile(g['parents'],g['views'],s),q)) if j!=coordinate),'wrong static coordinate')
 for rec in records:
  need(set(rec)=={'identity','classification','constructed','static','full_unit_path'},'record schema')
  g,r=expected[rec['identity']];p=g['parents'];k=g['views'];q=r['q'];a,b=r['representatives'];S=g['states']
  c=check.classify(p,k,q,S[a],S[b]);need(encoded(rec['classification'])==encoded(c),'independent structural classification')
  if c['sc']:sc_count+=1
  elif c['endpoint_full']:full_count+=1
  path(g,q,a,b,rec['full_unit_path'])
  if c['sc'] or c['endpoint_full']:
   proof=rec['constructed'];need(isinstance(proof,dict) and set(proof)=={'path','zero_prefix','zero_suffix'},'construction schema')
   path(g,q,a,b,proof['path'])
   check.path_states(p,k,q,S[a],S[b],{'states':[S[i] for i in proof['path']],'zero_prefix':proof['zero_prefix'],'zero_suffix':proof['zero_suffix']})
   need(rec['static']==[],'unexpected obstruction experiment')
  else:
   obstruction_count+=1;any_static=False
   need(rec['constructed'] is None and isinstance(rec['static'],list) and len(rec['static'])==len(p),'obstruction coverage')
   for v,z in enumerate(rec['static']):
    need(type(z.get('coordinate')) is int and z['coordinate']==v,'coordinate identity')
    # Separate predicate and union-find implementation; q rows came from independently reconstructed canonical parent.
    allowed={i for i,row in enumerate(g['q']) if all(row[j]==q[j] for j in range(len(p)) if j!=v) and abs(row[v]-q[v])<=1}
    reachable=check.reachable_union(g['edges'],allowed,a)
    if b in reachable:
     any_static=True
     need(set(z)=={'coordinate','path'},'false failed coordinate');path(g,q,a,b,z['path'],v)
    else:
     need(set(z)=={'coordinate','reachable'} and encoded(z['reachable'])==encoded(reachable),'false or incomplete failed-coordinate cut')
   if any_static:static_count+=1
   else:moving_count+=1
 s={'graphs':len(base['graphs']),'component_pairs':len(expected),'endpoint_pairs':sum(r['endpoint_pairs'] for g,r in expected.values()),'sc_pairs':sc_count,'endpoint_only_pairs':full_count,'obstruction_pairs':obstruction_count,'static_sufficient_pairs':static_count,'moving_required_pairs':moving_count}
 verdict='MOVING_LOCATION_REQUIRED' if moving_count else ('ALL_OBSTRUCTION_PAIRS_STATIC_SUFFICIENT' if obstruction_count else 'OBSTRUCTION_CLASS_EMPTY')
 need(encoded(doc['summary'])==encoded(s),'summary')
 need(doc['outcome']=='THEOREM_CONSTRUCTION_VALIDATED_WITHIN_DOMAIN' and doc['obstruction_outcome']==verdict,'verdict')
 return {'status':'VERIFIED','summary':s,'obstruction_outcome':verdict,'complete_pair_identity_equality':True,'independent_classification':True,'all_constructive_moves_checked':True,'independent_static_connectivity':True}

def verify(base,doc):
 try:return _verify(base,doc)
 except (KeyError,TypeError,IndexError) as e:raise ValueError('malformed experiment certificate') from e
