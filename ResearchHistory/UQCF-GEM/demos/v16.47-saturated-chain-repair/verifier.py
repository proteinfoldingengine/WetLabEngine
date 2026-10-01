"""Independent chain identities, complete obstruction partitions and L1 paths."""
import graph_verifier as graph
require=graph.require
DOMAIN=((2,2,2,2),(2,2,2,3),(2,2,2,4),(2,2,3,2),(2,2,3,3),(2,3,2,2),(2,3,2,3),(3,2,2,2),(3,2,2,3))
def canonical(a,b,c,k,q):
 r,s,t=q[:3];S=[set() for _ in range(a+b+c+1)];S[0]=set(range(k))
 if r<a:
  labels=list(range(k));S[1]=set(labels);outer=[i if i<r else 0 for i in range(a-1)]
 else:
  d=max(s,t) if s<b else b-1+t;labels=list(range(a-1,a-1+d));S[1]=set(labels);outer=list(range(a-1))
 palette=labels[:t] if s<b else labels[b-1:b-1+t];S[2]=set(palette)
 for i in range(c):S[3+i]={palette[i] if i<t else palette[0]}
 colors=s if s<b else b-1
 for i in range(b-1):S[c+3+i]={labels[i] if i<colors else labels[0]}
 for i,label in enumerate(outer):S[b+c+2+i]={label}
 return tuple(sum(1<<v for v,z in enumerate(S) if j in z) for j in range(k))
def outcome(nonunit,construction):
 if nonunit:return 'NONUNIT_WITNESS'
 return 'CONSTRUCTION_REFUTED' if construction else 'THREE_INTERNAL_CHAIN_THEOREM_VALIDATED'
def path_valid(path,x,y,g,q):
 states=g['states']
 if not isinstance(path,list) or not path or path[0]!=x or path[-1]!=y:return False
 if any(type(i)is not int or not 0<=i<len(states) for i in path):return False
 if any(sum(abs(a-b) for a,b in zip(g['attained_profiles'][g['profile_ids'][i]],q))>1 for i in path):return False
 return all(sum((a^b).bit_count() for a,b in zip(states[i],states[j]))==1 for i,j in zip(path,path[1:]))
def verify(doc,domain=DOMAIN):
 require(set(doc)=={'schema','domain','entries'} and doc['schema']==1,'document membership')
 require(doc['domain']==[list(x) for x in domain] and [(e['a'],e['b'],e['c'],e['k']) for e in doc['entries']]==list(domain),'complete canonical chain domain')
 rows=[];pathfail=[]
 for e,(a,b,c,k) in zip(doc['entries'],domain):
  require(set(e)=={'a','b','c','k','graph','normalizations'},'entry membership');g=e['graph']
  bottom='('+'()'*c+')';middle='('+''.join(sorted([bottom]+['()']*(b-1)))+')';code='('+''.join(sorted([middle]+['()']*(a-1)))+')'
  require(g['code']==code and g['parents']==[-1,0,1]+[2]*c+[1]*(b-1)+[0]*(a-1),'canonical nested-chain identity')
  row=graph.verify_graph(g,k)
  identities=[(comp[0],rec['q']) for rec in g['profiles'] for comp in rec['zero_components']]
  require([(rec['state'],rec['q']) for rec in e['normalizations']]==identities,'complete canonical component-representative identities')
  index={tuple(s):i for i,s in enumerate(g['states'])}
  for rec in e['normalizations']:
   require(set(rec)=={'state','q','path'},'normalization membership');i=rec['state'];q=rec['q']
   y=index.get(canonical(a,b,c,k,q));require(y is not None and g['attained_profiles'][g['profile_ids'][y]]==q,'canonical endpoint admitted and exact')
   if not path_valid(rec['path'],i,y,g,q):pathfail.append({'a':a,'b':b,'c':c,'k':k,'state':i,'q':q})
  sat=[r for r in g['profiles'] if r['q'][0]==a];other=[r for r in g['profiles'] if r['q'][0]<a]
  rows.append(dict(row,a=a,b=b,c=c,k=k,normalizations=len(identities),saturated_normalizations=sum(len(r['zero_components']) for r in sat),saturated_profiles=len(sat),saturated_components=sum(len(r['zero_components']) for r in sat),saturated_pairs=sum(len(r['pairs']) for r in sat),non_saturated_pairs=sum(len(r['pairs']) for r in other),saturated_adjacent_active_pairs=sum(len(r['pairs']) for r in sat if r['q'][1]>=2 and r['q'][2]>=2),saturated_nonunit_pairs=sum(p['unit_path'] is None for r in sat for p in r['pairs'])))
 nonunit=sum(r['nonunit_pairs'] for r in rows)
 return {'status':'VERIFIED','outcome':outcome(nonunit,pathfail),'per_graph':rows,'construction_failures':pathfail,'nonunit_pairs':nonunit,'normalizations':sum(r['normalizations'] for r in rows),'profiles':sum(r['profiles'] for r in rows),'general_claim':'All three-internal-vertex chains of arbitrary degrees>=2 and k>=2 admit total L1 excursion<=1; see independently reviewed theorem','universal_unit_barrier':'REFUTED' if nonunit else 'UNRESOLVED','general_saturated_chain':'REFUTED' if any(r['saturated_nonunit_pairs'] for r in rows) else ('CONSTRUCTION_REFUTED' if pathfail else 'PROVED_BY_REVIEWED_CONSTRUCTION')}

def parent_graph_equal(doc,parent):
 require(doc['domain']==parent['domain'] and [e['graph'] for e in doc['entries']]==[e['graph'] for e in parent['entries']],'fresh graph records differ from parent')
